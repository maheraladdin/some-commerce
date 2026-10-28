# Deep Engineering User Stories & 12-Sprint Execution Plan (Slices 1–6)

Each vertical slice is a **4-week milestone (two 2-week sprints)** funded via [GitHub Sponsors](https://github.com/sponsors/maheraladdin). Every slice ships a standalone, deployable production release across static AWS Web ([Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) + [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)), iOS, and Android via [Expo](https://docs.expo.dev/).

Every user story below includes its **Cognito Persona/Roles**, **Multilingual & RTL/LTR Requirements**, **Target Rust Lambda Binary & API Contract**, **DynamoDB Single-Table Access Pattern**, and **Given/When/Then Acceptance Criteria & Edge Cases**.

## Slice 1 (`v1.0` — Weeks 1–4): Core B2C Storefront, Amazon Cognito Auth, Multilingual RTL/LTR Engine, Governorate Fee Matrix, Paymob/Stripe, Bosta & Split COD

### US-1.1: Amazon Cognito OIDC/PKCE Authentication, Phone OTP & Pre-Token Persona/Locale Injection
* **Actors & Cognito Roles**: `ANONYMOUS`, `B2C_CUSTOMER`, `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* shopper or store administrator on Web, iOS, or Android,
  * *I want* to register and sign in using [Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) (Email/Password, Phone SMS OTP, Passkeys, or Social OAuth) and have my preferred language, tenant ID, and role injected into my JWT claims via a [Pre-Token Generation Lambda Trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html),
  * *So that* every API call is cryptographically authenticated, authorized, and localized without extra database lookups.
* **Multilingual & Localization Behavior**:
  * Cognito Custom SMS/Email triggers inspect `userAttributes["locale"]` (auto-detected via [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/) on the client or phone country prefix such as `+20` -> `ar-EG`, `+966` -> `ar-SA`, fallback -> `en-US`) and send localized OTP messages via [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html).
  * Authenticated users can switch languages at any time via `PATCH /v1/profile/locale`, updating both `USER#<cognito_sub>.preferred_locale` in DynamoDB and their Cognito user attribute.
* **Target Lambda & API Contract**:
  * Cognito Trigger (`PreTokenGeneration`): Injects `custom:tenant_id`, `custom:persona` (`B2C`), `custom:preferred_locale`, and `cognito:groups` (`STORE_ADMIN` | `B2C_CUSTOMER`).
  * `storefront-sdui-api`:
    * `PATCH /v1/profile/locale` (`{ "locale": "ar-EG" }`)
    * `POST /v1/profile/devices` (`{ "platform": "ios" | "android", "push_token": "...", "locale": "ar-EG" }` -> Registers endpoint in [Amazon SNS Mobile Push](https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-application-as-subscriber.html)).
* **DynamoDB Single-Table Access Pattern**:
  * Primary item: `PK = TENANT#<tid>`, `SK = USER#<cognito_sub>`
  * Secondary lookups: `GSI1PK = EMAIL#<email>`, `GSI2PK = PHONE#<e164_phone>`
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** an unauthenticated mobile shopper in Egypt (`+2010...`) signing up via Phone OTP with device locale `ar-EG`, **When** Cognito invokes the Custom SMS and Pre-Token triggers, **Then** the user receives an Arabic OTP SMS via Amazon SNS and obtains an RS256 JWT containing `"custom:persona": "B2C"` and `"custom:preferred_locale": "ar-EG"`.
  2. **Given** a non-admin customer holding `cognito:groups = ["B2C_CUSTOMER"]`, **When** they call `POST /v1/admin/products` on `admin-vendor-api` with `Accept-Language: ar-EG`, **Then** the `crates/auth-cognito` Tower middleware rejects the request in `<1ms` with HTTP `403 Forbidden` and localized JSON error `{"code": "FORBIDDEN_ROLE", "user_message": "عفواً، لا تملك صلاحية الوصول لإدارة المتجر"}`.
  3. **Given** a rotated Cognito signing key in `/.well-known/jwks.json`, **When** an incoming JWT has an unknown `kid`, **Then** `crates/auth-cognito` refreshes the JWKS cache with a 60-second rate-limit guard so valid logins never fail during key rotation.

### US-1.2: Multilingual & Direction-Aware (`RTL` / `LTR`) Universal Expo SDUI Engine
* **Actors & Cognito Roles**: `ANONYMOUS`, `B2C_CUSTOMER`, `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* shopper on static Web (S3 + CloudFront), iOS, or Android,
  * *I want* the storefront to resolve Server-Driven UI (SDUI) layouts in my active language with automatic Right-to-Left (`RTL`) or Left-to-Right (`LTR`) layout mirroring, localized typography tokens, and localized SEO metadata,
  * *So that* the storefront renders natively in Arabic, English, French, German, or any tenant-configured language without redeploying the frontend.
* **Multilingual & Localization Behavior**:
  * **Locale Resolution Priority**: `?locale=` query param -> URL path `/[locale]/...` -> Cognito JWT `custom:preferred_locale` -> `Accept-Language` header -> `CloudFront-Viewer-Country` mapping -> tenant `default_locale` -> `en-US`.
  * **Deterministic Translation Fallback**: `crates/i18n-engine` resolves missing keys across `requested_locale` (`ar-EG`) -> language root (`ar`) -> `tenant.default_locale` -> `en-US`.
  * **Bidirectional UI Mirroring**: When `"direction": "rtl"` is returned, the Universal Expo `<SduiRenderer />` sets `<html lang="ar-EG" dir="rtl">` on Web, applies logical flex start/end properties across iOS/Android/Web, and selects Arabic font tokens (`Cairo` / `Tajawal`).
* **Target Lambda & API Contract**:
  * `storefront-sdui-api`: `GET /v1/sdui/page?route=/home&locale=ar-EG` -> Returns `SduiPageResponse { schema_version, route, locale, direction: "rtl" | "ltr", theme_tokens, i18n_bundle, blocks[] }`.
  * `admin-vendor-api`: `PUT /v1/admin/i18n/{locale}/{namespace}` -> Upserts ICU MessageFormat dictionaries (`I18N#<locale>#<namespace>`) and invalidates CloudFront `/v1/sdui/*`.
* **DynamoDB Single-Table Access Pattern**:
  * `BatchGetItem` retrieving `PK = TENANT#<tid>, SK = SDUI#<route>#<persona>#<locale>` (with fallback to `SDUI#<route>#<persona>#default`) + `PK = TENANT#<tid>, SK = I18N#<locale>#storefront`.
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a shopper opening `/ar-eg/home` on static Web or switching language to Arabic inside the iOS/Android app, **When** `<SduiRenderer />` renders the response from `GET /v1/sdui/page`, **Then** all flex rows, icons, carousels, and text alignments flip to `RTL` immediately without requiring an app binary restart.
  2. **Given** a merchant updating the Arabic hero banner title via `PUT /v1/admin/sdui/home`, **When** the update commits to DynamoDB, **Then** `admin-vendor-api` triggers a CloudFront invalidation and all Web, iOS, and Android users see the new Arabic banner within seconds.

### US-1.3: Multilingual Physical Catalog, Localized SEO Slugs & Atomic Flash-Sale Stock Reservation
* **Actors & Cognito Roles**: `STORE_ADMIN`, `B2C_CUSTOMER`, `ANONYMOUS`
* **User Story Narrative**:
  * *As a* merchant,
  * *I want* to create physical products with multilingual titles, rich descriptions, localized SEO slugs, localized variant option maps (e.g., Size/Color in `ar` and `en`), multi-currency prices, physical weight/dimensions, and atomic stock reservation,
  * *So that* international shoppers discover products in their native language and high-concurrency checkouts never oversell inventory.
* **Multilingual & Localization Behavior**:
  * Product item stores `titles_i18n: Map<Locale, String>`, `descriptions_i18n: Map<Locale, String>`, `seo_slugs_i18n: Map<Locale, String>`, and `variant_labels_i18n`.
  * Localized URLs (`/ar/products/كرسي-مكتب` and `/en/products/office-chair`) both resolve to the same `PRODUCT#<pid>` via `GSI2`.
* **Target Lambda & API Contract**:
  * `admin-vendor-api`: `POST /v1/admin/products`, `PUT /v1/admin/products/{product_id}`
  * `storefront-sdui-api`: `GET /v1/catalog/products/{slug}?locale=ar-EG`, `POST /v1/cart/items`
* **DynamoDB Single-Table Access Pattern**:
  * Product master: `PK = TENANT#<tid>`, `SK = PRODUCT#<pid>`
  * Localized SEO slug index items: `PK = TENANT#<tid>`, `SK = PRODUCT_SLUG#<locale>#<slug>`, `GSI2PK = SLUG#<locale>#<slug>`, `GSI2SK = PRODUCT#<pid>`
  * Atomic inventory reservation during checkout: `UpdateItem` with `ConditionExpression: "stock_qty >= :qty"` and `SET stock_qty = stock_qty - :qty, reserved_qty = reserved_qty + :qty`.
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a SKU with `stock_qty = 1`, **When** two buyers concurrently submit checkout intents for that SKU in the same millisecond, **Then** DynamoDB `TransactWriteItems` succeeds for exactly one buyer and returns `ConditionalCheckFailedException` for the second, which `checkout-webhooks-api` translates into HTTP `409 Conflict` in the buyer's active language.

### US-1.4: Localized Governorate/Zone Fee Matrix & KMS-Encrypted Payment/Shipping Vault
* **Actors & Cognito Roles**: `STORE_ADMIN`, `checkout-webhooks-api`
* **User Story Narrative**:
  * *As a* store admin,
  * *I want* to store encrypted API credentials for [Paymob](https://developers.paymob.com/paymob-docs), [Stripe](https://docs.stripe.com/api), and [Bosta](https://docs.bosta.co/) in the dashboard alongside a **Localized Fee & Tax Matrix** (`LOCALE_FEES#<country>#<zone>`) with multilingual zone names, weight brackets, VAT %, and COD surcharges,
  * *So that* checkout dynamically calculates regional shipping/tax fees and routes payments without redeploying Lambda.
* **Multilingual & Localization Behavior**:
  * Zone definitions store `zone_names_i18n` (e.g., `{"ar-EG": "الدقهلية - المنصورة", "en-US": "Dakahlia - Mansoura"}`) and localized fee line-item labels (`"مصاريف الشحن"`, `"رسوم الدفع عند الاستلام"`, `"ضريبة القيمة المضافة 14%"`).
* **Target Lambda & API Contract**:
  * `admin-vendor-api`:
    * `PUT /v1/admin/vault/payment-gateways/{provider}`
    * `PUT /v1/admin/vault/shipping-carriers/{carrier}`
    * `PUT /v1/admin/locale-fees/{country}/{zone}`
  * `checkout-webhooks-api`: `POST /v1/rates/calculate` -> Returns localized line items for subtotal, carrier/zone fee, weight surcharge, COD surcharge, VAT, total, `deposit_required_cents`, and `cod_collection_cents`.
* **DynamoDB Single-Table Access Pattern**:
  * Secrets encrypted via `aws_sdk_kms::Client::encrypt` (`EncryptionContext: {"tenant_id": tid, "target": provider}`) at `PK = TENANT#<tid>, SK = PAYMENT_GW#<provider>` and `SK = SHIPPING_GW#<carrier>`.
  * Fee rules: `PK = TENANT#<tid>, SK = LOCALE_FEES#<country>#<zone>`.
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a store admin updating their Paymob API key and Integration IDs in the dashboard, **When** `admin-vendor-api` writes the record, **Then** the plaintext key is encrypted with AWS KMS, never logged, and cached in memory by `checkout-webhooks-api` with a 5-minute TTL.
  2. **Given** `LOCALE_FEES#EG#DAKAHLIA` configured with `base_fee = 65 EGP`, `per_kg_over_2kg = 10 EGP`, `cod_surcharge = 15 EGP`, and `vat_pct = 14%`, **When** a shopper in Mansoura quotes a 4 kg cart with COD in `ar-EG`, **Then** `/v1/rates/calculate` returns `85 EGP` shipping (`65 + 2*10`), `15 EGP` COD fee, and `14%` VAT with Arabic labels.

### US-1.5: Anti-RTO Upfront Deposit + Split Cash on Delivery (`DEPOSIT_COD`), Bosta AWB Dispatch & Multilingual SNS Alerts
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `STORE_ADMIN`, `checkout-webhooks-api`, `fulfillment-worker`, `durable-orchestrator`
* **User Story Narrative**:
  * *As a* merchant offering Cash on Delivery via [Bosta](https://docs.bosta.co/),
  * *I want* to require a configurable **Upfront COD Deposit** (`SHIPPING_FEE_ONLY`, `PERCENTAGE`, or `FIXED_AMOUNT`) paid online via [Paymob](https://developers.paymob.com/paymob-docs) or [Stripe](https://docs.stripe.com/api) before dispatching the order, and automatically book the remaining balance (`total - deposit`) as `collectionAmount` on Bosta with multilingual [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) SMS and Mobile Push notifications,
  * *So that* fake/uncollected RTO orders are eliminated.
* **Multilingual & Localization Behavior**:
  * Checkout UI (`CodDepositSummaryCard`) and all Amazon SNS SMS/Push messages (`OrderDepositConfirmed`, `BostaShipmentBooked`, `BostaOutForDelivery`, `BostaDelivered`) render in the order's `order_locale` (`ar-EG`, `en-US`, etc.).
* **Target Lambda & API Contract**:
  * `checkout-webhooks-api`: `POST /v1/checkout/intents`, `POST /v1/webhooks/paymob`, `POST /v1/webhooks/stripe`, `POST /v1/webhooks/shipping/bosta`
  * `fulfillment-worker`: Consumes DynamoDB Stream (`DEPOSIT_PAID_COD_PENDING` | `PAID`) -> Calls Bosta `POST /api/v2/deliveries` -> Calls `sns:Publish` for SMS & Push.
* **DynamoDB Single-Table Access Pattern**:
  * Atomic order + webhook idempotency write: `TransactWriteItems` updating `PK = TENANT#<tid>, SK = ORDER#<oid>` and inserting `PK = WEBHOOK#<provider>#<event_id>, SK = METADATA` (`attribute_not_exists(PK)`).
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** an `880 EGP` order in `ar-EG` with a `SHIPPING_FEE_ONLY` (`80 EGP`) upfront COD deposit rule, **When** the shopper submits checkout, **Then** `checkout-webhooks-api` creates a Paymob payment intent for `80 EGP`, sets `order_status = AWAITING_COD_DEPOSIT`, `deposit_required_cents = 8000`, `cod_collection_cents = 80000`, and starts a 2-hour expiration timer in `durable-orchestrator`.
  2. **Given** a verified Paymob HMAC webhook confirming the `80 EGP` deposit, **When** the order transitions to `DEPOSIT_PAID_COD_PENDING`, **Then** `fulfillment-worker` books the Bosta shipment with `collectionAmount: 800`, stores the Bosta AWB PDF URL, and sends an Arabic SMS + Push notification via Amazon SNS.
  3. **Given** a duplicate Paymob or Bosta webhook retry with the same `event_id`, **When** `checkout-webhooks-api` executes `TransactWriteItems`, **Then** the idempotency guard catches `ConditionalCheckFailedException` and returns HTTP `200 OK` without duplicating shipments or SNS messages.

## Slice 2 (`v2.0` — Weeks 5–8): Digital Products, Cryptographic Licensing Engine & Multilingual Digital Tax

### US-2.1: Multilingual Digital Catalog, Buyer-Country Digital VAT & Expiring S3 Presigned Delivery
* **Actors & Cognito Roles**: `STORE_ADMIN`, `B2C_CUSTOMER`
* **User Story Narrative**:
  * *As a* digital creator selling software, e-books, or templates globally,
  * *I want* digital products to omit physical shipping fees, apply buyer-country digital VAT/GST rules automatically, and serve protected files from a private S3 bucket via short-lived presigned URLs with localized download instructions.
* **Target Lambda & API Contract**:
  * `admin-vendor-api`: `POST /v1/admin/digital-assets/presign-upload`
  * `storefront-sdui-api`: `POST /v1/orders/{order_id}/downloads/{asset_id}/presign`
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a cart containing only `DIGITAL` items, **When** `/v1/rates/calculate` runs, **Then** physical shipping and COD options are omitted and digital VAT is computed from the buyer's country.
  2. **Given** an authenticated buyer requesting a download link for a `PAID` order, **When** they call `/presign`, **Then** `storefront-sdui-api` verifies `order.customer_sub == jwt.sub` and returns an S3 presigned URL with a 15-minute expiry.

### US-2.2: Asymmetric Ed25519 Offline & Online License Minting (`AWS KMS`) + Hybrid Physical-Digital Bundle Unlock
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* buyer of a software application or a physical hardware + software bundle,
  * *I want* `fulfillment-worker` to mint a unique license key and an offline-verifiable `.lic` certificate signed by an [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) asymmetric **Ed25519** key—immediately upon digital checkout or automatically when [Bosta](https://docs.bosta.co/) confirms physical delivery of my hardware bundle—and notify me in my preferred language via [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html).
* **Target Lambda & API Contract**:
  * `fulfillment-worker`: Invokes `kms:Sign` (`SigningAlgorithm::Ed25519Sha512`) over canonical JSON `{ license_key, tenant_id, product_id, customer_sub, max_activations, issued_at, expires_at, entitlements[] }` and writes `PK = LICENSE#<key>, SK = METADATA`.
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a pure digital order reaching `PAID`, **When** `fulfillment-worker` processes the stream event, **Then** it generates a KMS-signed Ed25519 `.lic` certificate and dispatches a localized SNS notification.
  2. **Given** a hybrid physical+digital bundle ordered via Split COD, **When** the upfront deposit is paid, **Then** the license is created with `status = PENDING_DELIVERY` and automatically flips to `ACTIVE` when the carrier's `Delivered` webhook arrives.

### US-2.3: Hardware Fingerprint Activation, Sub-10ms Heartbeat Verification & Automatic Refund/RTO Revocation
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, Client Software SDK, `storefront-sdui-api`, `checkout-webhooks-api`
* **User Story Narrative**:
  * *As a* software vendor,
  * *I want* client applications to bind hardware fingerprints (`machine_id`), perform sub-10ms online heartbeat checks, allow customers to deactivate old machines from a localized SDUI vault, and automatically revoke licenses if a payment refund/chargeback or physical bundle return occurs.
* **Target Lambda & API Contract**:
  * `storefront-sdui-api`: `POST /v1/licenses/activate`, `POST /v1/licenses/verify`, `POST /v1/licenses/deactivate`
* **DynamoDB Single-Table Access Pattern**:
  * Atomic activation: `UpdateItem` on `PK = LICENSE#<key>, SK = METADATA` with `ConditionExpression: "status = :active AND (contains(active_machines, :fp) OR size(active_machines) < max_activations)"`.
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a license with `max_activations = 2` and 2 active machines, **When** a 3rd machine calls `/v1/licenses/activate` with `Accept-Language: ar-EG`, **Then** the API returns HTTP `429 Too Many Requests` (`MAX_ACTIVATIONS_REACHED`) with an Arabic prompt to deactivate an existing device in `CustomerLicenseVaultBlock`.
  2. **Given** a Stripe/Paymob refund webhook or Bosta `Returned to Business` webhook for the order, **When** `checkout-webhooks-api` processes the event, **Then** `LICENSE#<key>.status` is atomically set to `REVOKED` and an SNS alert is sent to the customer and merchant.

## Slice 3 (`v3.0` — Weeks 9–12): B2B Wholesale, Cross-Border Express ([Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) & [DHL Express](https://developer.dhl.com/)), RFQ & Floating Seat Licenses

### US-3.1: Cognito B2B Organization Onboarding, Tax-ID Verification & Wholesale SDUI Persona Switching
* **Actors & Cognito Roles**: `B2B_ORG_ADMIN`, `B2B_BUYER`, `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* wholesale company administrator,
  * *I want* to register my organization (`B2B_ORG#<org_id>`), upload tax/commercial registry documents, invite team buyers into the `B2B_BUYER` Cognito group, and have the Cognito Pre-Token Trigger inject `"custom:persona": "B2B"` and `"custom:price_list_id"` into our JWTs so the storefront automatically renders localized B2B bulk SKU matrices, MOQ rules, and tiered volume pricing.
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a verified user in `cognito:groups = ["B2B_BUYER"]`, **When** they load any product route on Web or Mobile, **Then** `storefront-sdui-api` resolves `SDUI#<route>#B2B#<locale>` and returns `B2BBulkVariantMatrix` and `TieredPriceTable` with their organization's contracted price list.

### US-3.2: Cross-Border Shipping via Aramex & DHL Express with Landed Duties & Bilingual Commercial Invoices
* **Actors & Cognito Roles**: `B2B_BUYER`, `B2C_CUSTOMER`, `STORE_ADMIN`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* merchant exporting across MENA, GCC, Europe, and North America,
  * *I want* to configure [Aramex Shipping API](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) and [DHL Express MyDHL API](https://developer.dhl.com/api-reference/dhl-express-mydhl-api?language_content_entity=en) keys in the KMS vault so checkout calculates live volumetric air/road rates, HS-code customs duties, and automatically generates bilingual (`Arabic + English`) commercial invoices for Paperless Trade (PLT).
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** an international cart shipping from Egypt to KSA or UAE, **When** `/v1/rates/calculate` executes, **Then** `checkout-webhooks-api` queries Aramex and DHL Express concurrently, overlays `LOCALE_FEES#<country>#*` customs rules, and returns localized carrier options and estimated delivery dates.

### US-3.3: B2B Request-for-Quote (RFQ) Negotiation, Milestone Deposits & Durable Net-30 Reminders
* **Actors & Cognito Roles**: `B2B_BUYER`, `STORE_ADMIN`, `durable-orchestrator`
* **User Story Narrative**:
  * *As a* wholesale buyer,
  * *I want* to submit an RFQ from my cart, negotiate custom unit prices, shipping incoterms (`EXW`, `FOB`, `DDP`), and milestone payment terms (e.g., `30% Upfront Deposit` via Paymob/Stripe, `70% Balance` via COD or Net-30) with localized [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) notifications and automated [AWS Lambda Durable Functions](https://aws.plainenglish.io/aws-lambda-updates-in-2025-2e664f4070d2) Net-30 payment reminders.
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** an approved RFQ with 30% upfront deposit and 70% Net-30 terms, **When** the 30% deposit webhook succeeds, **Then** `fulfillment-worker` dispatches the shipment and `durable-orchestrator` checkpoints a 30-day workflow that dispatches localized SNS invoice reminders at Day 23, Day 28, and Day 30.

### US-3.4: B2B Organization Multi-Seat & Concurrent Floating Digital Licenses
* **Actors & Cognito Roles**: `B2B_ORG_ADMIN`, `B2B_BUYER`
* **User Story Narrative**:
  * *As an* enterprise software buyer (`B2B_ORG_ADMIN`),
  * *I want* to purchase a multi-seat organization license pool where I can assign named seats to employees or enable concurrent floating lease tokens (auto-releasing after 4 hours without a heartbeat) from a localized SDUI license portal.

## Slice 4 (`v4.0` — Weeks 13–16): Multi-Vendor Marketplace, Global Aggregators ([Shippo](https://docs.goshippo.com/) & [EasyPost](https://docs.easypost.com/)), Split Escrow & Crypto

### US-4.1: Global 40+ Carrier Rate Shopping via Shippo & EasyPost
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `B2B_BUYER`, `VENDOR`, `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* global shopper in the US, EU, UK, or APAC,
  * *I want* checkout to query [Shippo API](https://docs.goshippo.com/shipments/rate-shopping-with-carriers) and [EasyPost API](https://docs.easypost.com/docs/shipments/rates) so I can compare live Economy Ground, 2-Day Air, and Overnight rates across 40+ carriers (USPS, UPS, FedEx, Royal Mail, Canada Post) in my local currency and language.

### US-4.2: Multi-Vendor Cart Splitting, Proportional COD Deposit Allocation & Per-Vendor Pickup Dispatch
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `VENDOR`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* marketplace shopper buying items from multiple vendors in one cart,
  * *I want* to pay once at checkout while the backend atomically splits my parent order (`ORDER#<parent_id>`) into vendor sub-orders (`SUBORDER#<parent_id>#<vendor_id>`), allocates any Upfront COD Deposit and remaining COD collection balance proportionally per vendor shipment, books separate carrier pickups from each vendor's warehouse, and notifies each vendor in their preferred language via [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html).

### US-4.3: Pluggable Crypto Checkout ([BTCPay Server](https://docs.btcpayserver.org/API/Greenfield/v1/)) & Delivery-Gated Vendor Escrow Ledger
* **Actors & Cognito Roles**: `VENDOR`, `STORE_ADMIN`, `durable-orchestrator`
* **User Story Narrative**:
  * *As a* marketplace seller authenticated with the `VENDOR` Cognito role,
  * *I want* customer payments (via Stripe, Paymob, or self-hosted [BTCPay Server](https://docs.btcpayserver.org/API/Greenfield/v1/) Bitcoin/Lightning/USDT) recorded in an immutable double-entry DynamoDB escrow ledger and released automatically by `durable-orchestrator` N days after the carrier webhook confirms package delivery.

## Slice 5 (`v5.0` — Weeks 17–20): Dual AWS Marketplace Editions — Standard Lambda vs. AWS Lambda Managed Instances

### US-5.1: Standard On-Demand Serverless AWS Marketplace CloudFormation Stack
* **Actors**: AWS Marketplace Buyer (Startup / SMB)
* **User Story Narrative**:
  * *As a* startup buyer on [AWS Marketplace](https://docs.aws.amazon.com/marketplace/latest/userguide/product-preparation.html),
  * *I want* a 1-click CloudFormation template that provisions all 5 Rust Lambdas on default On-Demand [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-rust.html), On-Demand DynamoDB, Amazon Cognito, Amazon SNS, KMS keys, and the static Expo web bundle in S3 + CloudFront so my infrastructure scales to $0 compute cost when idle.

### US-5.2: Enterprise Hybrid AWS Lambda Managed Instances Stack (Zero Cold Starts & Multi-Concurrency)
* **Actors**: AWS Marketplace Buyer (Enterprise)
* **User Story Narrative**:
  * *As an* enterprise buyer with high sustained traffic,
  * *I want* `storefront-sdui-api` and `checkout-webhooks-api` deployed onto [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html) backed by an EC2 Graviton (`c8g`/`m8g`) Capacity Provider—handling 64–128 concurrent requests per container with zero cold starts and EC2 Savings Plan discounts—while keeping `admin-vendor-api` and `fulfillment-worker` on bursty On-Demand Lambda.

### US-5.3: AWS Marketplace Metering, Entitlement Verification & GitHub Sponsors Roadmap Webhook
* **Actors**: Platform Operator, Enterprise Buyer, GitHub Sponsor
* **User Story Narrative**:
  * *As the* creator of `some-commerce`,
  * *I want* commercial AWS Marketplace deployments to verify entitlements and report usage via the AWS Marketplace Metering API, and I want my public roadmap to automatically update slice funding progress when a [GitHub Sponsors](https://docs.github.com/en/sponsors) webhook fires.

## Slice 6 (`v6.0` — Weeks 21–24): Visual Multilingual SDUI Studio, Fee-Zone Builder & White-Label Mobile Pipeline

### US-6.1: Visual Drag-and-Drop Multilingual SDUI Studio & Side-by-Side RTL/LTR Previewer (`"use dom"`)
* **Actors & Cognito Roles**: `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* non-technical merchant,
  * *I want* a drag-and-drop visual SDUI studio inside the static Expo Admin Dashboard (built with [Expo DOM Components](https://docs.expo.dev/guides/dom-components/)) where I can arrange storefront blocks, edit side-by-side translations (`ar-EG` RTL vs. `en-US` LTR), preview across Web, iOS, and Android viewports, and publish new schema versions with automatic CloudFront cache invalidation and 1-click rollback.

### US-6.2: Visual Regional Fee, Tax, Split COD & Carrier Routing Matrix Builder
* **Actors & Cognito Roles**: `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* store admin,
  * *I want* an interactive visual matrix editor in the dashboard to map countries, governorates, and postal prefixes to preferred carriers (`Bosta` vs. `Aramex` vs. `DHL` vs. `Shippo`), configure weight brackets, set free-shipping thresholds, and define regional Upfront COD Deposit rules without editing raw JSON.

### US-6.3: White-Label Mobile App CI/CD Pipeline & Edge SEO `hreflang` Meta Injection
* **Actors & Cognito Roles**: `STORE_ADMIN`, Agency Sponsor, Search Engine Crawler
* **User Story Narrative**:
  * *As a* commercial brand or agency sponsor,
  * *I want* an automated AWS CodeBuild / EAS pipeline that compiles branded iOS and Android binaries from my tenant configuration, and an edge SEO injector that serves localized `<title>`, `<meta name="description">`, OpenGraph tags, and `hreflang` links for every `/[locale]/products/[slug]` URL on static S3 + CloudFront web.
