# System Architecture & Dual AWS Lambda Execution Model

## 1. High-Level Topology (100% AWS-Native)

`some-commerce` runs entirely inside an AWS account with zero external SaaS hosting dependencies. Every component is provisioned deterministically via [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) so the platform can be deployed either by open-source self-hosters or via 1-click CloudFormation templates on [AWS Marketplace](https://docs.aws.amazon.com/marketplace/latest/userguide/product-preparation.html).

```
                     +---------------------------------------------------+
                     |           Amazon CloudFront Distribution          |
                     |  - Viewer-Request CloudFront Function (URL/SEO)   |
                     |  - Forwards CloudFront-Viewer-Country & Language  |
                     +---------+-------------------+---------------------+
                               |                   |
          +--------------------+                   +--------------------+
          | /* (Static Web Assets)                                      | /v1/* (API, SDUI & Webhooks)
          v                                                             v
+----------------------------------+          +--------------------------------------------------+
| Private Amazon S3 Bucket (OAC)   |          | 5-Binary Rust Cargo Lambda Workspace (Axum)      |
| - npx expo export --platform web |          | 1. storefront-sdui-api  (Public/Auth Read+Cart)  |
| - Pre-rendered .html/.css/.js    |          | 2. checkout-webhooks-api(KMS Payment/Ship Hooks) |
+----------------------------------+          | 3. admin-vendor-api     (Cognito RBAC + KMS)     |
                                              | 4. fulfillment-worker   (Streams -> Bosta/KMS)   |
+----------------------------------+          | 5. durable-orchestrator (Net-30 / Escrow Timers) |
| Amazon Cognito User Pool         |          +------------------------+-------------------------+
| - OIDC / PKCE Auth (Web & Mobile)|                                   |
| - Pre-Token Lambda Trigger       |                                   v
| - RBAC Groups & Custom Claims    |          +--------------------------------------------------+
+----------------------------------+          | Amazon DynamoDB (SomeCommerceTable) + AWS KMS    |
                                              | - Single-Table Design (PK/SK + GSI1-GSI3)        |
+----------------------------------+          | - KMS Customer Managed Keys (Vault + Ed25519)    |
| Amazon SNS Notification Engine   | <--------+ - DynamoDB Streams + EventBridge Pipes           |
| - Mobile Push (APNs / FCM)       |          +--------------------------------------------------+
| - Transactional SMS & Fan-Out    |
+----------------------------------+
```

## 2. Authentication & Authorization with Amazon Cognito

All identity, authentication, and authorization flows are powered by **[Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html)** paired with a Rust **[Pre-Token Generation Lambda Trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html)**:

### 2.1 Authentication Flows Across Web & Mobile
* **Universal Expo Integration**: Uses OAuth 2.0 Authorization Code Grant with **PKCE** via `expo-auth-session`. On iOS and Android, refresh and access tokens are stored in hardware-backed `expo-secure-store`; on static Web, tokens are managed via secure session storage and silent refresh.
* **Supported Sign-In Methods**: Email/Password, Phone SMS/WhatsApp OTP (crucial for Egypt/MENA mobile shoppers), Passkeys (WebAuthn), and federated social/enterprise OIDC/SAML identity providers.

### 2.2 Role-Based & Attribute-Based Authorization (RBAC + ABAC)
1. **Cognito User Pool Groups (`cognito:groups`)**:
   * `SUPER_ADMIN`: Platform-wide configuration, AWS Marketplace entitlement inspection, and multi-tenant provisioning.
   * `STORE_ADMIN`: Full access to `/v1/admin/*` for their tenant—configuring KMS payment/shipping keys, localized fee matrices, SDUI layouts, and B2B quotes.
   * `VENDOR`: Scoped access to `/v1/vendor/*` in Slice 4—restricted strictly to products, Bosta/Shippo shipments, and escrow ledgers matching their `custom:vendor_id`.
   * `B2B_ORG_ADMIN` & `B2B_BUYER`: Wholesale accounts in Slice 3—unlocking B2B SDUI components, volume tier price lists, RFQ submission, and multi-seat license administration.
   * `B2C_CUSTOMER`: Authenticated retail shoppers accessing order history, saved addresses, and the SDUI `CustomerLicenseVaultBlock`.
2. **Pre-Token Generation Lambda Trigger (`custom:*` JWT Claims)**:
   * Before Cognito issues an ID or Access JWT, it invokes a lightweight Rust trigger that queries `SomeCommerceTable` and injects session claims (`custom:tenant_id`, `custom:persona`, `custom:b2b_org_id`, `custom:price_list_id`, `custom:vendor_id`).
3. **Zero-Lookup Axum Tower Middleware (`crates/auth-cognito`)**:
   * Every HTTP Rust Lambda caches Cognito's JSON Web Key Set (`/.well-known/jwks.json`) in memory (`Arc<RwLock<JwksCache>>`), validating RS256 JWT signatures in microseconds so `storefront-sdui-api` immediately resolves B2C vs. B2B SDUI layouts and wholesale pricing without an extra database round-trip.

## 3. Omnichannel Notifications & Pub/Sub Fan-Out with Amazon SNS

**[Amazon Simple Notification Service (Amazon SNS)](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)** powers all customer, vendor, and admin notifications through `crates/notify-sns`:

1. **Native Mobile Push Notifications ([SNS Mobile Push](https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-application-as-subscriber.html))**:
   * The Universal [Expo](https://docs.expo.dev/) app registers device push tokens with Amazon SNS Platform Applications (Apple APNs for iOS and Firebase FCM for Android), sending real-time push alerts when an order is confirmed, when a [Bosta](https://docs.bosta.co/)/[Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) courier is out for delivery, or when a B2B RFQ quote is approved.
2. **Transactional SMS Alerts (Egypt/MENA & Global)**:
   * Sends localized Arabic (`ar`) and English (`en`) SMS alerts for Upfront COD Deposit payment links, Bosta/Aramex tracking links, and delivery OTP codes.
3. **Topic Fan-Out (`OrderEvents`, `ShipmentEvents`, `LicenseEvents`)**:
   * `fulfillment-worker` and `durable-orchestrator` publish structured JSON events to SNS Topics with message attributes (`event_type`, `tenant_id`, `vendor_id`), allowing merchants and enterprise buyers to attach custom HTTPS webhooks, SQS queues, or email alerts.

## 4. The 5-Binary Rust Cargo Workspace Architecture

Using [Cargo Lambda](https://www.cargo-lambda.info/), the repository is organized as a single Rust workspace that compiles **5 specialized Lambda binaries**:

* `bins/storefront-sdui-api`: High-throughput SDUI, catalog, cart, and `/v1/licenses/verify` heartbeat.
* `bins/checkout-webhooks-api`: Checkout intents, Split COD, payment/carrier webhooks, and SNS event publishing.
* `bins/admin-vendor-api`: Cognito-protected admin & vendor dashboard APIs + KMS secret encryption.
* `bins/fulfillment-worker`: DynamoDB Stream consumer (Carrier AWB booking, Ed25519 KMS license minting, and SNS push/SMS dispatch).
* `bins/durable-orchestrator`: [AWS Lambda Durable Functions](https://aws.plainenglish.io/aws-lambda-updates-in-2025-2e664f4070d2) for long-running timers (COD deposit expiry, B2B Net-30 reminders, and delivery-gated vendor escrow payouts).

## 5. DynamoDB Single-Table Schema (`SomeCommerceTable`)

All entities reside in one [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/data-modeling-foundations.html) table with `PK` (Partition Key), `SK` (Sort Key), and three Global Secondary Indexes (`GSI1`–`GSI3`):

| Entity | `PK` | `SK` | `GSI1PK` | `GSI1SK` | Key Attributes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tenant Metadata** | `TENANT#<tid>` | `METADATA` | `DOMAIN#<host>` | `METADATA` | `store_name`, `default_currency`, `cognito_pool_id`, `sns_topic_arn` |
| **User & Push Endpoints** | `TENANT#<tid>` | `USER#<sub_id>` | `EMAIL#<email>` | `TENANT#<tid>` | `cognito_groups[]`, `persona`, `b2b_org_id`, `sns_endpoint_arns[]` |
| **Payment Gateway Secret** | `TENANT#<tid>` | `PAYMENT_GW#<id>` | `TENANT#<tid>` | `GW_ENABLED#<bool>` | `kms_ciphertext_blob`, `currencies[]`, `webhook_secret_hash` |
| **Shipping Carrier Secret** | `TENANT#<tid>` | `SHIPPING_GW#<id>` | `TENANT#<tid>` | `CARRIER_ENABLED#<bool>` | `kms_ciphertext_blob`, `pickup_location_id`, `countries[]` |
| **Localized Fee & COD Rule** | `TENANT#<tid>` | `LOCALE_FEES#<iso>#<zone>` | `TENANT#<tid>` | `FEE_PRIORITY#<n>` | `base_fee_cents`, `per_kg_cents`, `cod_deposit_rule`, `tax_vat_pct` |
| **Localized SDUI Layout** | `TENANT#<tid>` | `SDUI#<route>#<persona>#<loc>` | `SDUI_VER#<ver>` | `UPDATED#<ts>` | `direction` (`rtl`\|`ltr`), `theme_tokens`, `components_json` |
| **Product Item** | `TENANT#<tid>` | `PRODUCT#<pid>` | `CAT#<cid>` | `PRICE#<cents>` | `type` (`PHYSICAL`\|`DIGITAL`), `b2c_price`, `b2b_tiers[]`, `vendor_id` |
| **Order & Split COD** | `TENANT#<tid>` | `ORDER#<oid>` | `CUST#<sub_id>` | `CREATED#<ts>` | `order_status`, `total_cents`, `deposit_paid_cents`, `cod_collection_cents` |
| **Shipment & Tracking** | `TENANT#<tid>` | `SHIPMENT#<oid>#<vid>` | `TRACKING#<awb>` | `CARRIER#<id>` | `carrier_status`, `awb_pdf_url`, `pickup_id`, `cod_collected_bool` |
| **Digital License** | `LICENSE#<key>` | `METADATA` | `CUST#<sub_id>` | `PRODUCT#<pid>` | `ed25519_sig`, `max_seats`, `active_fingerprints[]`, `status` |
| **B2B Org & RFQ Quote** | `TENANT#<tid>` | `B2B_ORG#<org_id>` | `B2B_REP#<sub_id>` | `STATUS#<st>` | `tax_id`, `credit_limit_cents`, `cod_deposit_pct`, `price_list_id` |
