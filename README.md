# some-commerce

[![Sponsor maheraladdin](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/maheraladdin)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Rust: Cargo Lambda](https://img.shields.io/badge/Backend-Rust%20%2B%20Cargo%20Lambda-orange?style=for-the-badge&logo=rust)](https://www.cargo-lambda.info/)
[![Search: Elasticsearch & OpenSearch](https://img.shields.io/badge/Search-Elasticsearch%20%2B%20DynamoDB-005571?style=for-the-badge&logo=elasticsearch)](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations)
[![Client: Universal Expo](https://img.shields.io/badge/Client-Universal%20Expo%20(Multilingual%20RTL%2FLTR)-000020?style=for-the-badge&logo=expo)](https://docs.expo.dev/)
[![AWS: 100% Native](https://img.shields.io/badge/Cloud-100%25%20AWS%20Serverless-FF9900?style=for-the-badge&logo=amazonaws)](https://aws.amazon.com/lambda/lambda-managed-instances/)

**`some-commerce`** is an open-source, 100% AWS-native, **multilingual (`RTL` & `LTR`) B2C & B2B Server-Driven UI (SDUI) e-commerce marketplace** for selling both **physical products** and **cryptographically licensed digital products**.

Built with a **5-binary Rust ([Axum](https://github.com/tokio-rs/axum) + [Cargo Lambda](https://www.cargo-lambda.info/)) workspace**, **[Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html)** for authentication and role/persona authorization, **[Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)** + **DynamoDB General Filtration** for **Unlimited N-Level Categories, Brands, User-Customizable Product Properties, and Faceted Search**, **[Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)** for localized mobile push notifications and SMS alerts, **[Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/data-modeling-foundations.html)** (Single-Table Design), and a **Universal [Expo](https://docs.expo.dev/) + [Expo Router](https://docs.expo.dev/router/introduction/) + [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/)** client (exported as static HTML/CSS/JS on **[Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) + [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)** and compiled natively for iOS & Android), `some-commerce` is funded slice-by-slice through **[GitHub Sponsors](https://github.com/sponsors/maheraladdin)** and packaged commercially on **[AWS Marketplace](https://aws.amazon.com/marketplace/)** in two editions:

1. **Standard Serverless Edition**: On-Demand [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-rust.html) + On-Demand DynamoDB (with General Filtration or optional OpenSearch Serverless—scales to zero when idle).
2. **Enterprise Managed Instances Edition**: [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html) backed by customer-owned EC2 Graviton Capacity Providers + Dedicated [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) with [DynamoDB Zero-ETL Ingestion](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/OpenSearchIngestionForDynamoDB.html).

## Sponsor This Project

`some-commerce` is built in **6 vertical production slices**. Every slice is unlocked and shipped as a standalone, production-ready release funded by community and commercial sponsors.

* **[Sponsor @maheraladdin on GitHub Sponsors](https://github.com/sponsors/maheraladdin)**

## Documentation Index (`docs/`)

* **[System Architecture & Dual AWS Lambda Model (`docs/SYSTEM_ARCHITECTURE.md`)](docs/SYSTEM_ARCHITECTURE.md)** — 5-binary Cargo Lambda workspace, Amazon Cognito RBAC/ABAC, Elasticsearch + DynamoDB Dual-Tier Filtration, Unlimited N-Level Taxonomy (`TAXONOMY_NODE`), User-Customizable Product Properties (`PROPERTY_DEF`), Brands, and Amazon SNS notifications.
* **[Deep Engineering User Stories & 12-Sprint Execution Plan (`docs/USER_STORIES_AND_SPRINTS.md`)](docs/USER_STORIES_AND_SPRINTS.md)** — Exhaustive user stories across all 6 production slices (`v1.0` to `v6.0`), including Cognito Personas, Multilingual/RTL-LTR rules, Dynamic Property/N-Level Category filtration specs, 6-Mode Licensing stories, API Contracts, DynamoDB Access Patterns, and Given/When/Then Acceptance Criteria.
* **[Payments, Global Shipping, Split COD & 6-Mode Digital Licensing (`docs/PAYMENTS_SHIPPING_AND_LICENSING.md`)](docs/PAYMENTS_SHIPPING_AND_LICENSING.md)** — KMS-encrypted vault for Paymob, Stripe, and BTCPay Server; global shipping via Bosta, Aramex, DHL Express, Shippo, and EasyPost; Upfront Deposit + Split Cash-on-Delivery (`DEPOSIT_COD`); and **6 Non-Heartbeat E-Product License Verification Modes** (Offline Ed25519, QR Challenge-Response, CloudFront CRLs/Bloom Filters, AES-256-GCM Content Key Unsealing, Release-Timestamp Gating, and B2B On-Premise Proxy).
* **[Server-Driven UI (SDUI), Dynamic Properties & Multilingual Engine (`docs/SDUI_AND_LOCALIZATION.md`)](docs/SDUI_AND_LOCALIZATION.md)** — Universal Expo SDUI JSON schema, `SearchFacetFilterBlock` (with dynamic `COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`), N-level `CategoryBreadcrumbBlock`, `BrandPillSelector`, and bidirectional RTL/LTR layout mirroring.

## Core Architecture Overview

| Layer | Technology | Highlights |
| :--- | :--- | :--- |
| **Auth & Authorization** | [Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) + [Pre-Token Lambda Trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html) | OIDC/PKCE auth across Web & Mobile; JWT custom claims (`tenant_id`, `persona`, `preferred_locale`, `b2b_org_id`, `vendor_id`) + RBAC groups (`STORE_ADMIN`, `VENDOR`, `B2B_BUYER`, `B2C_CUSTOMER`). |
| **Dynamic Taxonomy, Properties & Search** | [Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) + DynamoDB General Filter | **Unlimited N-Level Categories** (`TAXONOMY_NODE`), **Brands**, and **User-Customizable Product Properties** (`PROPERTY_DEF`: `Color Swatch`, `Size`, `RAM`, `Custom Specs`) with automatic [Nested Aggregations](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-nested-aggregation) and customizable SDUI filter widgets. |
| **6-Mode Digital Licensing** | [AWS KMS Asymmetric Ed25519](https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html) + CloudFront CRLs + X25519/AES-256-GCM | 6 verification modes without constant heartbeating: Offline Ed25519 `.lic`, Air-Gapped QR Challenge-Response, CloudFront Signed Revocation Lists (`revoked.crl.bin`), CEK Content Decryption, Release-Timestamp Gating, and B2B LAN Proxy. |
| **Multilingual Engine** | [`expo-localization`](https://docs.expo.dev/guides/localization/) + `crates/i18n-engine` (ICU MessageFormat) | Unlimited tenant languages with deterministic fallback (`requested_locale -> language_root -> default_locale -> en`), instant RTL/LTR layout mirroring, localized catalog/category/brand/property labels, and localized API errors. |
| **Notifications & Pub/Sub** | [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) ([Mobile Push](https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-application-as-subscriber.html), SMS & Topic Fan-Out) | Sends localized Arabic/English/multi-language iOS (APNs) & Android (FCM) push notifications, transactional SMS shipment/COD alerts, and merchant webhook fan-out. |
| **Backend Compute** | Rust + [Axum](https://github.com/tokio-rs/axum) + [Cargo Lambda](https://www.cargo-lambda.info/) | 5 domain-scoped binaries (`storefront-sdui-api`, `checkout-webhooks-api`, `admin-vendor-api`, `fulfillment-worker`, `durable-orchestrator`). |
| **Database & Events** | [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) + [EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-dynamodb.html) | Single-table design (`SomeCommerceTable`) with DynamoDB Streams driving async order fulfillment, real-time Elasticsearch indexing, SNS notifications, and license minting. |
| **Storefront & Admin** | [Expo](https://docs.expo.dev/) + [Expo Router](https://docs.expo.dev/router/introduction/) + [Expo DOM](https://docs.expo.dev/guides/dom-components/) | Single TypeScript codebase exported via `npx expo export --platform web` to S3 + CloudFront (OAC) and compiled natively to iOS & Android. |
| **Payment Gateways** | Rust `PaymentProvider` Trait + [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) | Zero-redeploy dashboard config for [Paymob](https://developers.paymob.com/paymob-docs), [Stripe](https://docs.stripe.com/api), and [BTCPay Server](https://docs.btcpayserver.org/API/Greenfield/v1/) + **Upfront Deposit on COD**. |
| **Global Delivery** | Rust `ShippingProvider` Trait + Localized Fee Engine | Pluggable adapters for [Bosta](https://docs.bosta.co/), [Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform), [DHL Express](https://developer.dhl.com/), [Shippo](https://docs.goshippo.com/), [EasyPost](https://docs.easypost.com/), and custom governorate/zone tables. |

## Master Engineering Checklist (Granular Task-by-Task Breakdown)

### Slice 1 (`v1.0` — Weeks 1–4): Core B2C Storefront, Cognito Auth, Unlimited N-Level Categories, Dynamic Product Properties, Elasticsearch + General Filtration, Paymob/Stripe & Bosta Split COD

#### Sprint 1.1 (Weeks 1–2): Rust Workspace, Cognito Auth, Dynamic Taxonomy/Properties, Dual-Tier Search & Universal Expo Static Web
- [ ] **1.1.1 — Rust Cargo Workspace & Core Domain (`crates/core-domain`)**
  - [ ] Initialize root `Cargo.toml` workspace targeting `aarch64-unknown-linux-gnu` (AWS Graviton) with shared dependencies (`tokio`, `axum`, `tower`, `serde`, `aws-sdk-dynamodb`, `aws-sdk-kms`, `aws-sdk-sns`, `tracing`)
  - [ ] Define strongly typed domain identifiers (`TenantId`, `ProductId`, `TaxonomyNodeId`, `PropertyCode`, `BrandId`, `OrderId`, `CognitoSub`)
  - [ ] Implement `Money` value object (minor units / cents + ISO-4217 currency code) with overflow-safe arithmetic
  - [ ] Define `PropertyDefinition` model supporting 6 data types (`ENUM_SINGLE`, `ENUM_MULTI`, `COLOR_SWATCH`, `NUMERIC_UNIT`, `BOOLEAN`, `TEXT_LOCALIZED`), `is_variant_axis: bool`, `is_filterable: bool`, and `FilterUiWidget` enum (`COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`, `TOGGLE_SWITCH`)
  - [ ] Define `TaxonomyNode` model supporting unlimited N-level nesting (`parent_node_id`, `depth_level: u8`, `ancestors_path: Vec<TaxonomyNodeId>`, `attached_property_ids: Vec<PropertyCode>`) with cycle-detection validation
  - [ ] Define `Brand` model (`names_i18n`, `descriptions_i18n`, `seo_slugs_i18n`, `logo_s3_key`, `is_verified`, `featured_node_ids`)
  - [ ] Define `Product` & `SkuVariant` models supporting inherited category properties, ad-hoc product-level `custom_properties[]`, Cartesian variant generation (`Color x Size`), weight in grams, and stock/reserved counters
- [ ] **1.1.2 — Amazon Cognito Authentication & RBAC/ABAC Middleware (`crates/auth-cognito`)**
  - [ ] Implement Cognito JWKS client (`/.well-known/jwks.json`) with `Arc<RwLock<JwksCache>>` and 60-second refresh rate-limiting on unknown `kid`
  - [ ] Implement RS256 JWT verifier extracting `AuthenticatedPrincipal { sub, tenant_id, persona, preferred_locale, cognito_groups, b2b_org_id, price_list_id, vendor_id }`
  - [ ] Build Axum Tower route-guard extractors: `RequireStoreAdmin`, `RequireVendor`, `RequireB2bBuyer`, `RequireAuthenticatedCustomer`, and `OptionalPrincipal`
  - [ ] Write Rust **Cognito Pre-Token Generation Lambda Trigger** that queries `USER#<sub_id>` in DynamoDB and injects `custom:tenant_id`, `custom:persona`, and `custom:preferred_locale` into ID/Access tokens
  - [ ] Write Rust **Cognito Custom SMS Trigger** that inspects phone prefix (`+20`, `+966`, etc.) and `locale` attribute to send localized Arabic/English OTP codes via [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [ ] **1.1.3 — Multilingual & i18n/l10n Fallback Engine (`crates/i18n-engine`)**
  - [ ] Implement 6-step locale resolution middleware (`?locale=` -> URL `/[locale]/...` -> JWT `custom:preferred_locale` -> `Accept-Language` -> `CloudFront-Viewer-Country` -> `tenant.default_locale` -> `en-US`)
  - [ ] Implement deterministic translation fallback chain (`ar-EG` -> `ar` -> `tenant.default_locale` -> `en-US`)
  - [ ] Integrate ICU MessageFormat parser for pluralization, gender rules, and localized currency/number formatting
  - [ ] Build localized API error responder (`AppError -> { code, user_message, locale, trace_id }`)
- [ ] **1.1.4 — DynamoDB Single-Table Repository (`crates/db-dynamo`)**
  - [ ] Implement `SomeCommerceTable` key builders for `PK`, `SK`, `GSI1PK`/`GSI1SK`, `GSI2PK`/`GSI2SK`, and `GSI3PK`/`GSI3SK`
  - [ ] Implement CRUD + subtree move operations for `TAXONOMY_NODE#<node_id>` (atomically updating `ancestors_path[]` for descendants)
  - [ ] Implement CRUD for `PROPERTY_DEF#<prop_code>` and `BRAND#<brand_id>`
  - [ ] Implement `ProductRepository` writing master `PRODUCT#<pid>` items alongside localized slug index items (`GSI2PK = SLUG#<locale>#<slug>`)
  - [ ] Implement atomic inventory reservation (`UpdateItem` with `ConditionExpression: "stock_qty >= :qty"`) and release helpers
- [ ] **1.1.5 — Dual-Tier Catalog Search & Filtration Engine (`crates/search-elastic`)**
  - [ ] Define `CatalogSearchProvider` async trait (`search_products`, `suggest_autocomplete`, `index_product_batch`, `delete_product`)
  - [ ] Implement **Tier 1 `DynamoGeneralFilterProvider`**:
    - [ ] Query `GSI1` (`NODE#<leaf_nid>` + `PRICE#<cents>`) and `GSI3` (`BRAND#<bid>` + `NODE#<leaf_nid>#PRICE#<cents>`)
    - [ ] Apply `FilterExpression` for `product_type`, `in_stock_only`, `is_on_sale`, `supports_cod`, `min_rating`, and dynamic `properties[]`
    - [ ] Implement HMAC-signed cursor pagination (`next_cursor`)
  - [ ] Implement **Tier 2 `ElasticSearchProvider`** ([Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)):
    - [ ] Author index mapping template with `arabic`, `english`, `french`, and `german` analyzers + `edge_ngram` autocomplete analyzer
    - [ ] Configure `properties` as an Elasticsearch `nested` field (`code`, `data_type`, `widget`, `str_val`, `num_val`, `bool_val`, `hex`, `label_i18n`)
    - [ ] Build single-query `_search` DSL builder combining `bool.must` (fuzzy multi-match), `bool.filter` (`taxonomy_ancestors`, price range, general flags, nested properties), and `post_filter` (disjunctive brand/property selection)
    - [ ] Build aggregation parser for `taxonomy_children_agg`, `brand_agg`, `price_stats_agg`, `general_flags_agg`, and `dynamic_properties_nested_agg` (returning both `terms` buckets and `stats` min/max for numeric sliders)
    - [ ] Implement automatic circuit-breaker fallback from `ElasticSearchProvider` to `DynamoGeneralFilterProvider` on connection timeout
- [ ] **1.1.6 — Universal Expo App & Static AWS Web Hosting (`apps/universal-store` + `infra/cdk`)**
  - [ ] Initialize [Expo Router](https://docs.expo.dev/router/introduction/) universal project (`Web`, `iOS`, `Android`) with [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/)
  - [ ] Build `<SduiRenderer />` with dynamic `RTL` / `LTR` layout mirroring (`<html dir="rtl">` on Web + logical flex start/end styles on Native) and font switching (`Cairo` vs. `Inter`)
  - [ ] Implement core Slice 1 SDUI blocks: `HeroBannerBlock`, `CategoryTreeDrawerBlock` (unlimited N-level accordion), `CategoryBreadcrumbBlock`, `BrandPillSelectorBlock`, `ProductGridBlock`, and `SearchFacetFilterBlock` (rendering `COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`, `TOGGLE_SWITCH`)
  - [ ] Author [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) stack provisioning `SomeCommerceTable`, Cognito User Pool, Private S3 Bucket + [CloudFront (OAC)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html), viewer-request [CloudFront Function](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/example_cloudfront_functions_url_rewrite_single_page_apps_section.html) (rewriting `/[locale]/...` to static HTML shells), and [`BucketDeployment`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3_deployment.BucketDeployment.html) for `npx expo export --platform web`

#### Sprint 1.2 (Weeks 3–4): KMS Vault, Real-Time Elasticsearch Sync, Paymob/Stripe Checkout, Bosta Delivery, Split COD & SNS Alerts
- [ ] **1.2.1 — AWS KMS Envelope Encryption Vault (`crates/kms-vault` & `bins/admin-vendor-api`)**
  - [ ] Implement `KmsSecretVault` encrypting/decrypting gateway credentials with `EncryptionContext: {"tenant_id": tid, "gateway_type": gtype, "provider": id}` and a 5-minute TTL `ArcSwap` in-memory cache
  - [ ] Build Admin Dashboard endpoints (`PUT /v1/admin/vault/payment-gateways/{provider}`, `PUT /v1/admin/vault/shipping-carriers/{carrier}`, `PUT /v1/admin/vault/search-clusters/elasticsearch`)
  - [ ] Build Admin Dashboard UI forms in Expo (`apps/universal-store/app/(admin)/settings/vault.tsx`) to configure [Paymob](https://developers.paymob.com/paymob-docs), [Stripe](https://docs.stripe.com/api), [Bosta](https://docs.bosta.co/), and [Elasticsearch](https://www.elastic.co/) keys without redeploying Lambda
- [ ] **1.2.2 — Localized Governorate/Zone Fee Engine (`LOCALE_FEES#<country>#<zone>`)**
  - [ ] Implement admin CRUD endpoints (`PUT /v1/admin/locale-fees/{country}/{zone}`) supporting bilingual zone names (`"الدقهلية - المنصورة"` / `"Dakahlia - Mansoura"`), base shipping fee, per-kg weight brackets, free-shipping threshold, VAT %, COD surcharge, and **Upfront COD Deposit Rule** (`NONE`, `SHIPPING_FEE_ONLY`, `PERCENTAGE`, `FIXED_AMOUNT`)
  - [ ] Implement `POST /v1/rates/calculate` in `bins/checkout-webhooks-api` returning itemized localized checkout totals (`subtotal_cents`, `shipping_fee_cents`, `weight_surcharge_cents`, `cod_surcharge_cents`, `tax_vat_cents`, `total_cents`, `deposit_required_cents`, `cod_collection_cents`)
- [ ] **1.2.3 — Pluggable Payment Adapters (`crates/payment-providers`)**
  - [ ] Define `PaymentProvider` async trait (`create_payment_intent`, `verify_webhook`, `refund_payment`)
  - [ ] Implement `PaymobProvider` ([Paymob Accept API](https://developers.paymob.com/paymob-docs/integration-paths/apis)): Auth token exchange, Order registration, Payment Key generation (Cards, Meeza, Vodafone/Orange/Etisalat Wallets, InstaPay, ValU), and SHA-512 HMAC webhook verification
  - [ ] Implement `StripeProvider` ([Stripe Payment Intents API](https://docs.stripe.com/api/payment_intents)): Intent creation with `metadata[order_id]`, `Stripe-Signature` HMAC-SHA256 verification, and refund API
  - [ ] Build platform-specific Expo checkout components: `PaymentSheet.native.tsx` ([`@stripe/stripe-react-native`](https://docs.expo.dev/versions/latest/sdk/stripe/) + [Paymob React Native SDK](https://github.com/PaymobAccept/paymob-reactnative-sdk)) and `PaymentSheet.web.tsx` (Stripe Elements + Paymob Unified Checkout iframe)
- [ ] **1.2.4 — Bosta Shipping Adapter & Upfront COD Deposit State Machine (`crates/shipping-providers`)**
  - [ ] Define `ShippingProvider` async trait (`calculate_rates`, `create_shipment`, `print_awb_label`, `cancel_shipment`, `verify_webhook`)
  - [ ] Implement `CustomZoneProvider` (table-rate governorate/city calculator)
  - [ ] Implement `BostaProvider` ([Bosta API v2](https://docs.bosta.co/)):
    - [ ] Map `FulfillmentOrder` to `POST https://app.bosta.co/api/v2/deliveries` with `type: 10` (Deliver), `specs.packageDetails`, receiver address/governorate, and `cod = cod_collection_cents / 100` (`0` for 100% Prepaid, `total` for Full COD, or `total - deposit` for Split COD)
    - [ ] Implement AWB PDF label fetcher (`GET /api/v2/deliveries/awb/{id}`) and [Bosta Webhook](https://docs.bosta.co/docs/how-to/get-delivery-status-via-webhook/) verifier (`POST /v1/webhooks/shipping/bosta`)
  - [ ] Implement **Split COD Order State Machine**:
    - [ ] `AWAITING_COD_DEPOSIT` -> `DEPOSIT_PAID_COD_PENDING` -> `SHIPMENT_BOOKED` -> `OUT_FOR_DELIVERY` -> `COMPLETED`
    - [ ] Handle `RTO_RETURNED` (when Bosta reports `Returned to Business`): atomically restore `PRODUCT#<pid>.stock_qty`, retain shipping deposit per merchant rule, and auto-refund excess deposit
    - [ ] Build SDUI `CodDepositSummaryCard` and `ShipmentTrackerBlock`
- [ ] **1.2.5 — Async Fulfillment Worker, Real-Time Elasticsearch Indexer & Amazon SNS Notifications (`bins/fulfillment-worker` & `crates/notify-sns`)**
  - [ ] Configure DynamoDB Streams + [Amazon EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-dynamodb.html) routing catalog changes and paid/deposit-confirmed orders to `fulfillment-worker`
  - [ ] Implement real-time Elasticsearch `/_bulk` indexer inside `fulfillment-worker` triggered on `PRODUCT#*`, `TAXONOMY_NODE#*`, `BRAND#*`, and `PROPERTY_DEF#*` stream records
  - [ ] Implement `SnsNotificationService` (`crates/notify-sns`) dispatching localized Arabic/English [Amazon SNS Mobile Push](https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-application-as-subscriber.html) (APNs/FCM) and transactional SMS messages on `OrderConfirmed`, `ShipmentBooked`, `OutForDelivery`, and `Delivered`
  - [ ] Write integration tests for Split COD, flash-sale stock contention, and webhook idempotency (`TransactWriteItems` guard), and tag release **`v1.0.0`**

### Slice 2 (`v2.0` — Weeks 5–8): Digital Products & 6-Mode Non-Heartbeat Cryptographic Licensing Engine

#### Sprint 2.1 (Weeks 5–6): S3 Protected Delivery, Offline Ed25519 `.lic` Signing (Mode 1), CEK Envelope Encryption (Mode 4) & Release Gating (Mode 5)
- [ ] **2.1.1 — Digital Product Catalog, Custom Digital Properties & Buyer-Country Digital VAT**
  - [ ] Extend `Product` validation for `ProductType::Digital` and `ProductType::HybridBundle` (linking a physical SKU + digital license SKU)
  - [ ] Seed standard digital properties (`os_platform`, `cpu_arch`, `file_format`, `license_verification_mode`) into `crates/search-elastic`
  - [ ] Update `/v1/rates/calculate` to omit physical shipping/COD when a cart is 100% digital and compute localized digital VAT/GST from buyer country
  - [ ] Provision private S3 Digital Assets Bucket (`BlockPublicAccess.BLOCK_ALL`) and implement presigned upload (`POST /v1/admin/digital-assets/presign-upload`) and buyer-authenticated presigned download (`POST /v1/orders/{oid}/downloads/{aid}/presign` with 15-minute TTL)
- [ ] **2.1.2 — AWS KMS Asymmetric Ed25519 Offline Certificate Signer (`crates/licensing-ed25519` — Mode 1 & Mode 5)**
  - [ ] Provision asymmetric [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) signing key (`KeySpec::EccCurveEd25519`, `KeyUsage::SignVerify`) in CDK
  - [ ] Implement `mint_offline_license_certificate` calling `kms:Sign` (`SigningAlgorithm::Ed25519Sha512` — [RFC 8032](https://www.rfc-editor.org/info/rfc8032/)) over canonical JSON `{ license_key, tenant_id, product_id, customer_sub, verification_mode, max_activations, issued_at, expires_at, updates_entitled_until, entitlements[] }`
  - [ ] Implement **Mode 5 Release-Timestamp Gating** (`POST /v1/licenses/download-release/{version}` verifying `release.published_at <= license.updates_entitled_until` and embedding signed `release_published_at` metadata into release manifests)
  - [ ] Implement **Hybrid Physical + Digital Bundle Trigger**: hold license in `PENDING_PHYSICAL_DELIVERY` until Bosta webhook confirms physical hardware delivery, then auto-mint `.lic` and notify buyer via Amazon SNS
- [ ] **2.1.3 — Cryptographic Content Key Unsealing (`Mode 4` — Anti-Patching Envelope Encryption)**
  - [ ] Build CLI/Admin packaging helper that encrypts protected digital binaries, AI weights, VST banks, or pro templates using symmetric **AES-256-GCM** with a per-product Content Encryption Key (CEK)
  - [ ] Implement `POST /v1/licenses/unseal-cek` performing X25519 Diffie-Hellman key wrapping so activated client devices receive the wrapped CEK required to decrypt the protected asset in memory

#### Sprint 2.2 (Weeks 7–8): Air-Gapped QR Challenge-Response (Mode 2), CloudFront Signed CRLs (Mode 3), Push Revocation (Mode 6) & SDKs
- [ ] **2.2.1 — Air-Gapped Challenge-Response & Mobile QR Activation (`Mode 2`)**
  - [ ] Implement offline hardware fingerprint generator (`SHA-256(CPU_ID + Board_UUID + Disk_UUID) + random_nonce`) outputting a `.req` file and QR code payload
  - [ ] Implement `POST /v1/licenses/challenge-activate` in `storefront-sdui-api` using an atomic DynamoDB conditional update (`size(active_machines) < max_activations`) and returning a hardware-locked `.cert` signed by AWS KMS Ed25519
  - [ ] Build QR Scanner inside the Universal Expo `CustomerLicenseVaultBlock` so buyers can scan an air-gapped PC's challenge QR code with their phone and display/transfer the signed response QR/file immediately
- [ ] **2.2.2 — CloudFront Edge-Cached Revocation Lists / Bloom Filters (`Mode 3` — [RFC 5280](https://www.rfc-editor.org/info/rfc5280/)) & SNS Push Revocation (`Mode 6`)**
  - [ ] Wire Stripe (`charge.refunded`, `charge.dispute.created`), Paymob refund, and Bosta (`Returned to Business`) webhooks in `checkout-webhooks-api` to atomically set `LICENSE#<key>.status = REVOKED`
  - [ ] Implement compact **Ed25519-signed Bloom Filter / CRL generator** (`revoked.crl.bin`) in `fulfillment-worker` that writes to S3 behind CloudFront (`/crl/{tenant_id}/revoked.crl.bin`, `Cache-Control: public, max-age=3600`)
  - [ ] Dispatch silent [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-application-as-subscriber.html) push revocation event (`Mode 6`) on license revocation or seat reassignment
- [ ] **2.2.3 — Client Verification SDKs & SDUI License Vault**
  - [ ] Publish lightweight open-source verification SDKs in **Rust** (`some-commerce-license-rs`) and **TypeScript/JS** (`@some-commerce/license-sdk`) supporting all 6 verification modes
  - [ ] Build localized SDUI `CustomerLicenseVaultBlock` (viewing keys, downloading `.lic` files, scanning air-gapped QR codes, and deactivating old machines) and tag release **`v2.0.0`**

### Slice 3 (`v3.0` — Weeks 9–12): B2B Wholesale, Cross-Border Express ([Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) & [DHL Express](https://developer.dhl.com/)), RFQ & B2B On-Premise License Proxy

#### Sprint 3.1 (Weeks 9–10): Cognito B2B Orgs, B2B Custom Property/MOQ Filtration & Aramex/DHL Express Adapters
- [ ] **3.1.1 — Cognito B2B Organization Onboarding & Persona Switching**
  - [ ] Implement `B2B_ORG#<org_id>` registration flow (`POST /v1/b2b/organizations`) with S3 presigned upload for commercial registry & tax ID documents
  - [ ] Add `B2B_ORG_ADMIN` and `B2B_BUYER` Cognito groups and update Pre-Token Generation Trigger to inject `custom:persona = "B2B"`, `custom:b2b_org_id`, and `custom:price_list_id`
  - [ ] Index B2B fields in Elasticsearch (`moq_min`, `b2b_price_tiers`, `case_pack_qty`, `b2b_authorized_brands`) and build `B2BBulkVariantMatrix` and `TieredPriceTable` SDUI blocks
- [ ] **3.1.2 — Cross-Border Shipping via Aramex & DHL Express (`crates/shipping-providers`)**
  - [ ] Implement `AramexProvider` ([Aramex Shipping Services API](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform)): volumetric weight (`L*W*H/5000`), domestic + GCC/MENA rate calculator, cross-border COD, AWB label printing, and webhook tracking
  - [ ] Implement `DhlExpressProvider` ([DHL Express MyDHL API](https://developer.dhl.com/api-reference/dhl-express-mydhl-api?language_content_entity=en)): international air express rating, landed-cost duty/tax estimation (`HS Code`), Duties & Taxes Paid (`DTP`), and Paperless Trade (`PLT`) PDF commercial invoice generator (bilingual `Arabic + English`)

#### Sprint 3.2 (Weeks 11–12): RFQ Negotiation State Machine, Milestone Deposits, Durable Net-30 Timers & B2B LAN License Proxy
- [ ] **3.2.1 — B2B Request-for-Quote (RFQ) & Milestone Deposit Workflow**
  - [ ] Implement RFQ state machine (`DRAFT` -> `SUBMITTED` -> `MERCHANT_COUNTERED` -> `BUYER_APPROVED` -> `DEPOSIT_PAID` -> `IN_PRODUCTION` -> `SHIPPED` -> `NET_TERMS_SETTLED`)
  - [ ] Support custom B2B milestone deposit splits (e.g., `30% Upfront Deposit` via Paymob/Stripe/Wire, `70% Balance` via COD or Net-30/Net-60)
  - [ ] Implement `bins/durable-orchestrator` using [AWS Lambda Durable Functions](https://aws.plainenglish.io/aws-lambda-updates-in-2025-2e664f4070d2) to checkpoint multi-week timers for quote expiration and automated Day-23 / Day-28 / Day-30 localized Amazon SNS payment reminders
- [ ] **3.2.2 — B2B On-Premise LAN License Proxy (`Mode 6`) & Multi-Seat Management**
  - [ ] Build `some-commerce-license-proxy` (lightweight Rust Axum container for enterprise LANs) that loads a single KMS-signed master organization certificate (`N` seats) and leases/reclaims floating seats across internal workstations with zero external internet access
  - [ ] Build SDUI `B2BSeatManagementBlock` for `B2B_ORG_ADMIN` users and tag release **`v3.0.0`**

### Slice 4 (`v4.0` — Weeks 13–16): Multi-Vendor Marketplace, Global Aggregators ([Shippo](https://docs.goshippo.com/) & [EasyPost](https://docs.easypost.com/)), Split Escrow & Crypto

#### Sprint 4.1 (Weeks 13–14): Shippo & EasyPost 40+ Carrier Aggregators + Multi-Vendor Cart & Deposit Splitting
- [ ] **4.1.1 — Vendor Onboarding, Cognito ABAC Isolation & Vendor Elasticsearch Facets**
  - [ ] Implement `VENDOR#<vendor_id>` onboarding, warehouse pickup address management, and Cognito `custom:vendor_id` ABAC enforcement in `bins/admin-vendor-api`
  - [ ] Allow vendors to attach custom `PROPERTY_DEF` specifications to their products and index `vendor_id`, `vendor_rating`, and `vendor_country` as facets in Elasticsearch
- [ ] **4.1.2 — Global Multi-Carrier Aggregators (`ShippoProvider` & `EasyPostProvider`)**
  - [ ] Implement `ShippoProvider` ([Shippo API](https://docs.goshippo.com/shipments/rate-shopping-with-carriers)) and `EasyPostProvider` ([EasyPost API](https://docs.easypost.com/docs/shipments/rates)) unlocking live rate shopping, label purchasing, and tracking webhooks across 40+ carriers (USPS, UPS, FedEx, Royal Mail, Canada Post, Australia Post)
  - [ ] Build SDUI `CarrierRateSelectorBlock` allowing shoppers to pick Economy vs. Express per vendor shipment
- [ ] **4.1.3 — Multi-Vendor Cart Splitting & Proportional Split COD Allocation**
  - [ ] Split parent `ORDER#<parent_id>` into atomic `SUBORDER#<parent_id>#<vendor_id>` records in DynamoDB
  - [ ] Allocate upfront COD deposits and remaining carrier `collectionAmount` balances proportionally across each vendor's sub-order
  - [ ] Update `fulfillment-worker` to dispatch separate pickup requests to each vendor's warehouse address (`Bosta`, `Aramex`, or `Shippo`) and notify each vendor via localized Amazon SNS push/SMS

#### Sprint 4.2 (Weeks 15–16): BTCPay Server Crypto Adapter, Double-Entry Escrow Ledger & Vendor Portal
- [ ] **4.2.1 — Self-Hosted Crypto Checkout (`BtcpayProvider`)**
  - [ ] Implement `BtcpayProvider` ([BTCPay Server Greenfield API v1](https://docs.btcpayserver.org/API/Greenfield/v1/)) supporting Bitcoin on-chain, Lightning Network, and USDT/USDC invoices with HMAC webhook verification
- [ ] **4.2.2 — Double-Entry Escrow Ledger & Delivery-Gated Payouts**
  - [ ] Implement immutable DynamoDB ledger entries (`LEDGER#<vendor_id>#<entry_id>`) tracking `GROSS_SALE`, `PLATFORM_COMMISSION`, `SHIPPING_DEDUCTION`, `ESCROW_LOCKED`, and `PAYOUT_RELEASED`
  - [ ] Wire `durable-orchestrator` to start an `N`-day return-window timer upon receiving a carrier `Delivered` webhook, automatically transitioning vendor funds from `ESCROW_LOCKED` to `PAYOUT_READY` and triggering Stripe Connect / Paymob / Bank payouts
  - [ ] Build multilingual SDUI Vendor Portal (`apps/universal-store/app/(vendor)/*`) and tag release **`v4.0.0`**

### Slice 5 (`v5.0` — Weeks 17–20): Dual AWS Marketplace Editions — Standard Lambda vs. AWS Lambda Managed Instances

#### Sprint 5.1 (Weeks 17–18): Multi-Concurrency Tuning, OpenSearch Zero-ETL & Dual AWS CDK Marketplace Stacks
- [ ] **5.1.1 — Multi-Concurrency Optimization for [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html)**
  - [ ] Audit `storefront-sdui-api` and `checkout-webhooks-api` shared state (`Arc<AppState>`) replacing mutexes with lock-free `ArcSwap` / `DashMap` caches for KMS secrets, Cognito JWKS, and i18n bundles
  - [ ] Run load tests (`k6` / `oha`) simulating 64–128 concurrent invocations per execution environment on Graviton EC2 Nitro instances (`c8g.large` / `m8g.large`) verifying `<15ms` p99 latency
- [ ] **5.1.2 — Dual AWS CDK Commercial Packaging (`infra/cdk`)**
  - [ ] Author **Stack Edition A (`SomeCommerceServerlessStack`)**: On-Demand ARM64 Rust Lambdas + On-Demand DynamoDB + S3/CloudFront Static Expo Web + Cognito + SNS + KMS (scales to $0 when idle)
  - [ ] Author **Stack Edition B (`SomeCommerceManagedInstancesStack`)**: EC2 Graviton Capacity Provider + [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html) for `storefront-sdui-api` and `checkout-webhooks-api` + On-Demand Lambda for `admin-vendor-api` and `fulfillment-worker` + Dedicated [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) domain with [DynamoDB Zero-ETL OpenSearch Ingestion](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/OpenSearchIngestionForDynamoDB.html)

#### Sprint 5.2 (Weeks 19–20): AWS Marketplace Metering, FTR Security Audit & GitHub Sponsors Automation
- [ ] **5.2.1 — AWS Marketplace Metering & Entitlement Integration**
  - [ ] Integrate `aws-sdk-marketplacemetering` and `aws-sdk-marketplaceentitlement` into `admin-vendor-api` and `durable-orchestrator`
  - [ ] Implement [GitHub Sponsors](https://docs.github.com/en/sponsors) webhook handler (`POST /v1/webhooks/github-sponsors`) to automatically update slice funding badges and unlock sponsor perks
  - [ ] Pass AWS Foundational Technical Review (FTR) and `cfn-nag` / `cdk-nag` security checks, and tag release **`v5.0.0`**

### Slice 6 (`v6.0` — Weeks 21–24): Visual Multilingual SDUI Studio, Dynamic Property/Taxonomy Studio & White-Label Mobile Pipeline

#### Sprint 6.1 (Weeks 21–22): Visual Drag-and-Drop SDUI Studio, N-Level Taxonomy/Property Designer & Regional Fee Matrix UI
- [ ] **6.1.1 — Visual Multilingual SDUI Editor (`"use dom"` in Expo Admin)**
  - [ ] Build drag-and-drop SDUI block canvas using [Expo DOM Components](https://docs.expo.dev/guides/dom-components/) with live side-by-side `ar-EG` (`RTL`) and `en-US` (`LTR`) preview frames (`Web`, `iPhone`, `Android`)
  - [ ] Add JSON Schema validation, version history (`SDUI_VER#<version>`), 1-click rollback, and automatic CloudFront cache invalidation on publish
- [ ] **6.1.2 — Visual N-Level Category Tree, Dynamic Property & Regional Fee Studio**
  - [ ] Build interactive drag-and-drop tree editor for unlimited N-level `TAXONOMY_NODE` hierarchies and property inheritance visualization
  - [ ] Build visual `PROPERTY_DEF` designer (configuring `COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`, `TOGGLE_SWITCH` and previewing the resulting `SearchFacetFilterBlock`)
  - [ ] Build interactive country/governorate fee, carrier routing, and Upfront COD Deposit matrix editor

#### Sprint 6.2 (Weeks 23–24): White-Label Mobile App CI/CD Pipeline & Edge SEO `hreflang` Injection
- [ ] **6.2.1 — White-Label Mobile Build Pipeline & Edge SEO**
  - [ ] Create automated EAS / AWS CodeBuild workflow that compiles tenant-branded iOS (`.ipa`) and Android (`.aab`) apps pre-configured with the tenant's Cognito User Pool, SNS Push Application ARN, and SDUI API endpoint
  - [ ] Add edge SEO OpenGraph + `hreflang` meta-tag injection for localized `/[locale]/categories/[...slugs]`, `/[locale]/brands/[slug]`, and `/[locale]/products/[slug]` routes
  - [ ] Complete open-source contributor guide, sponsor showcase, and launch **`v6.0.0`**

## License

Released under the [MIT License](LICENSE). Sponsored and maintained by [@maheraladdin](https://github.com/maheraladdin).
