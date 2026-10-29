# some-commerce

[![Sponsor maheraladdin](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/maheraladdin)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Rust: Cargo Lambda](https://img.shields.io/badge/Backend-Rust%20%2B%20Cargo%20Lambda-orange?style=for-the-badge&logo=rust)](https://www.cargo-lambda.info/)
[![Search: Elasticsearch & OpenSearch](https://img.shields.io/badge/Search-Elasticsearch%20%2B%20DynamoDB-005571?style=for-the-badge&logo=elasticsearch)](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations)
[![AI: WebMCP Ready](https://img.shields.io/badge/AI-WebMCP%20(Customer%20%26%20Admin%20Tools)-8A2BE2?style=for-the-badge)](https://webmachinelearning.github.io/webmcp/)
[![Client: Universal Expo](https://img.shields.io/badge/Client-Universal%20Expo%20(Multilingual%20RTL%2FLTR)-000020?style=for-the-badge&logo=expo)](https://docs.expo.dev/)
[![AWS: 100% Native](https://img.shields.io/badge/Cloud-100%25%20AWS%20Serverless-FF9900?style=for-the-badge&logo=amazonaws)](https://aws.amazon.com/lambda/lambda-managed-instances/)

**`some-commerce`** is an open-source, 100% AWS-native, **multilingual (`RTL` & `LTR`) B2C & B2B Server-Driven UI (SDUI) e-commerce marketplace** for selling both **physical products** and **cryptographically licensed digital products**, featuring first-class **[WebMCP (`navigator.modelContext`)](https://webmachinelearning.github.io/webmcp/)** and **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/specification/2026-07-28)** tools for both **Customers** and **Store Admins**.

Built with a **5-binary Rust ([Axum](https://github.com/tokio-rs/axum) + [Cargo Lambda](https://www.cargo-lambda.info/)) workspace**, **[Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html)** for authentication and role/persona authorization, **[Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)** + **DynamoDB General Filtration** for **Unlimited N-Level Categories, Brands, User-Customizable Product Properties, and Faceted Search**, **[WebMCP](https://developer.chrome.com/docs/ai/webmcp)** + **[Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html)** for agentic shopping & admin configuration, **[Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)** for localized mobile push notifications and SMS alerts, **[Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/data-modeling-foundations.html)** (Single-Table Design), and a **Universal [Expo](https://docs.expo.dev/) + [Expo Router](https://docs.expo.dev/router/introduction/) + [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/)** client (exported as static HTML/CSS/JS on **[Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) + [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)** and compiled natively for iOS & Android), `some-commerce` is funded slice-by-slice through **[GitHub Sponsors](https://github.com/sponsors/maheraladdin)** and packaged commercially on **[AWS Marketplace](https://aws.amazon.com/marketplace/)** in two editions:

1. **Standard Serverless Edition**: On-Demand [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-rust.html) + On-Demand DynamoDB (with General Filtration or optional OpenSearch Serverless—scales to zero when idle).
2. **Enterprise Managed Instances Edition**: [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html) backed by customer-owned EC2 Graviton Capacity Providers + Dedicated [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) with [DynamoDB Zero-ETL Ingestion](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/OpenSearchIngestionForDynamoDB.html).

## Sponsor This Project

`some-commerce` is built in **6 vertical production slices**. Every slice is unlocked and shipped as a standalone, production-ready release funded by community and commercial sponsors.

* **[Sponsor @maheraladdin on GitHub Sponsors](https://github.com/sponsors/maheraladdin)**

## Documentation Index (`docs/`)

* **[System Architecture & Dual AWS Lambda Model (`docs/SYSTEM_ARCHITECTURE.md`)](docs/SYSTEM_ARCHITECTURE.md)** — 5-binary Cargo Lambda workspace, Amazon Cognito RBAC/ABAC, **Customer & Admin WebMCP (`navigator.modelContext`) + MCP Architecture**, Elasticsearch + DynamoDB Dual-Tier Filtration, Unlimited N-Level Taxonomy (`TAXONOMY_NODE`), User-Customizable Product Properties (`PROPERTY_DEF`), Brands, and Amazon SNS notifications.
* **[Deep Engineering User Stories & 12-Sprint Execution Plan (`docs/USER_STORIES_AND_SPRINTS.md`)](docs/USER_STORIES_AND_SPRINTS.md)** — Exhaustive user stories across all 6 production slices (`v1.0` to `v6.0`), including Cognito Personas, Multilingual/RTL-LTR rules, **Customer & Admin WebMCP stories**, Dynamic Property/N-Level Category filtration specs, 6-Mode Licensing stories, API Contracts, DynamoDB Access Patterns, and Given/When/Then Acceptance Criteria.
* **[Payments, Global Shipping, Split COD & 6-Mode Digital Licensing (`docs/PAYMENTS_SHIPPING_AND_LICENSING.md`)](docs/PAYMENTS_SHIPPING_AND_LICENSING.md)** — KMS-encrypted vault for Paymob, Stripe, and BTCPay Server; global shipping via Bosta, Aramex, DHL Express, Shippo, and EasyPost; Upfront Deposit + Split Cash-on-Delivery (`DEPOSIT_COD`); and **6 Non-Heartbeat E-Product License Verification Modes**.
* **[Server-Driven UI (SDUI), WebMCP Tools, Dynamic Properties & Multilingual Engine (`docs/SDUI_AND_LOCALIZATION.md`)](docs/SDUI_AND_LOCALIZATION.md)** — Universal Expo SDUI JSON schema, **Customer & Admin WebMCP Tool Schemas**, `SearchFacetFilterBlock`, N-level `CategoryBreadcrumbBlock`, `BrandPillSelector`, and bidirectional RTL/LTR layout mirroring.

## Core Architecture Overview

| Layer | Technology | Highlights |
| :--- | :--- | :--- |
| **Auth & Authorization** | [Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) + [Pre-Token Lambda Trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html) | OIDC/PKCE auth across Web & Mobile; JWT custom claims (`tenant_id`, `persona`, `preferred_locale`, `b2b_org_id`, `vendor_id`) + RBAC groups (`STORE_ADMIN`, `VENDOR`, `B2B_BUYER`, `B2C_CUSTOMER`). |
| **WebMCP & Agentic AI (Customer & Admin)** | [W3C WebMCP (`navigator.modelContext`)](https://webmachinelearning.github.io/webmcp/) + [MCP](https://modelcontextprotocol.io/specification/2026-07-28) + [Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html) | **Customer Tools**: conversational search/filter, product comparison/recommendation, and account/address profile updates. **Admin Tools**: SDUI layout & theme styling, store fee/gateway configuration, N-level taxonomy/property setup, and multilingual product creation. |
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

### Slice 1 (`v1.0` — Weeks 1–4): Core B2C Storefront, Cognito Auth, Unlimited N-Level Categories, Dynamic Product Properties, Elasticsearch + General Filtration, WebMCP Customer/Admin Tools, Paymob/Stripe & Bosta Split COD

#### Sprint 1.1 (Weeks 1–2): Rust Workspace, Cognito Auth, Dynamic Taxonomy/Properties, Dual-Tier Search, WebMCP Core & Universal Expo Static Web
- [ ] **1.1.1 — Rust Cargo Workspace & Core Domain (`crates/core-domain`)**
  - [ ] Initialize root `Cargo.toml` workspace targeting `aarch64-unknown-linux-gnu` (AWS Graviton) with shared dependencies (`tokio`, `axum`, `tower`, `serde`, `aws-sdk-dynamodb`, `aws-sdk-kms`, `aws-sdk-sns`, `aws-sdk-bedrockruntime`, `tracing`)
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
  - [ ] Implement **Tier 1 `DynamoGeneralFilterProvider`** (querying `GSI1` / `GSI3` + `FilterExpression` for `product_type`, `in_stock_only`, `is_on_sale`, `supports_cod`, `min_rating`, and dynamic `properties[]`)
  - [ ] Implement **Tier 2 `ElasticSearchProvider`** ([Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)) with `arabic`, `english`, `french`, and `german` analyzers, `nested` `properties` field, `post_filter` disjunctive faceting, and circuit-breaker fallback
- [ ] **1.1.6 — Customer & Admin WebMCP (`navigator.modelContext`) + Backend MCP Engine (`crates/mcp-tools` & `apps/universal-store`)**
  - [ ] Build client-side [W3C WebMCP (`navigator.modelContext.registerTool`)](https://webmachinelearning.github.io/webmcp/) bridge in Universal Expo Web (`useWebMcpTools` hook) and backend MCP / [Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html) endpoints (`POST /v1/mcp/customer` on `storefront-sdui-api` and `POST /v1/mcp/admin` on `admin-vendor-api`)
  - [ ] Implement **Customer WebMCP Tools**:
    - [ ] `search_and_filter_catalog` (translates natural-language shopping intents into structured Elasticsearch / General Filter queries and updates `SearchFacetFilterBlock` + `ProductGridBlock`)
    - [ ] `recommend_and_compare_products` (compares candidate products across budget, use case, and dynamic `properties[]`, rendering `ProductComparisonTableBlock`)
    - [ ] `update_customer_account_details` (helps authenticated customers add/edit delivery addresses, phone numbers, and preferred language in `USER#<cognito_sub>` with user confirmation)
    - [ ] `prepare_cart_and_quote_cod` (adds chosen SKU variants to cart and previews localized shipping + Upfront COD Deposit totals)
  - [ ] Implement **Admin WebMCP Tools** (strictly guarded by `RequireStoreAdmin` / `RequireVendor` Cognito RBAC):
    - [ ] `admin_style_and_generate_sdui` (generates/modifies localized `SDUI#<route>#<persona>#<locale>` layouts and `theme_tokens` with live preview before publishing)
    - [ ] `admin_configure_store_and_fees` (configures `LOCALE_FEES#<country>#<zone>`, Upfront COD Deposit rules, N-level `TAXONOMY_NODE` trees, and custom `PROPERTY_DEF` schemas)
    - [ ] `admin_create_and_translate_product` (generates multilingual product titles/descriptions/slugs in Arabic & English, maps N-level categories/brands, populates custom `properties[]` and SKU variants, and saves/indexes the product)
- [ ] **1.1.7 — Universal Expo App & Static AWS Web Hosting (`apps/universal-store` + `infra/cdk`)**
  - [ ] Initialize [Expo Router](https://docs.expo.dev/router/introduction/) universal project (`Web`, `iOS`, `Android`) with [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/)
  - [ ] Build `<SduiRenderer />` with dynamic `RTL` / `LTR` layout mirroring (`<html dir="rtl">` on Web + logical flex start/end styles on Native) and font switching (`Cairo` vs. `Inter`)
  - [ ] Implement core Slice 1 SDUI blocks: `HeroBannerBlock`, `CategoryTreeDrawerBlock`, `CategoryBreadcrumbBlock`, `BrandPillSelectorBlock`, `ProductGridBlock`, `ProductComparisonTableBlock`, `AiShoppingAssistantDrawerBlock`, and `SearchFacetFilterBlock`
  - [ ] Author [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) stack provisioning `SomeCommerceTable`, Cognito User Pool, Private S3 Bucket + [CloudFront (OAC)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html), viewer-request [CloudFront Function](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/example_cloudfront_functions_url_rewrite_single_page_apps_section.html), and [`BucketDeployment`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3_deployment.BucketDeployment.html) for `npx expo export --platform web`

#### Sprint 1.2 (Weeks 3–4): KMS Vault, Real-Time Elasticsearch Sync, Paymob/Stripe Checkout, Bosta Delivery, Split COD & SNS Alerts
- [ ] **1.2.1 — AWS KMS Envelope Encryption Vault (`crates/kms-vault` & `bins/admin-vendor-api`)**
  - [ ] Implement `KmsSecretVault` encrypting/decrypting gateway credentials with `EncryptionContext: {"tenant_id": tid, "gateway_type": gtype, "provider": id}` and a 5-minute TTL `ArcSwap` in-memory cache
  - [ ] Build Admin Dashboard endpoints (`PUT /v1/admin/vault/payment-gateways/{provider}`, `PUT /v1/admin/vault/shipping-carriers/{carrier}`, `PUT /v1/admin/vault/search-clusters/elasticsearch`, `PUT /v1/admin/vault/ai-providers/{provider}`)
- [ ] **1.2.2 — Localized Governorate/Zone Fee Engine (`LOCALE_FEES#<country>#<zone>`)**
  - [ ] Implement admin CRUD endpoints (`PUT /v1/admin/locale-fees/{country}/{zone}`) supporting bilingual zone names (`"الدقهلية - المنصورة"` / `"Dakahlia - Mansoura"`), base shipping fee, per-kg weight brackets, free-shipping threshold, VAT %, COD surcharge, and **Upfront COD Deposit Rule** (`NONE`, `SHIPPING_FEE_ONLY`, `PERCENTAGE`, `FIXED_AMOUNT`)
  - [ ] Implement `POST /v1/rates/calculate` in `bins/checkout-webhooks-api`
- [ ] **1.2.3 — Pluggable Payment Adapters (`crates/payment-providers`)**
  - [ ] Implement `PaymobProvider` ([Paymob Accept API](https://developers.paymob.com/paymob-docs/integration-paths/apis)) and `StripeProvider` ([Stripe Payment Intents API](https://docs.stripe.com/api/payment_intents))
  - [ ] Build `PaymentSheet.native.tsx` ([`@stripe/stripe-react-native`](https://docs.expo.dev/versions/latest/sdk/stripe/) + [Paymob React Native SDK](https://github.com/PaymobAccept/paymob-reactnative-sdk)) and `PaymentSheet.web.tsx`
- [ ] **1.2.4 — Bosta Shipping Adapter & Upfront COD Deposit State Machine (`crates/shipping-providers`)**
  - [ ] Implement `CustomZoneProvider` and `BostaProvider` ([Bosta API v2](https://docs.bosta.co/))
  - [ ] Implement **Split COD Order State Machine** (`AWAITING_COD_DEPOSIT` -> `DEPOSIT_PAID_COD_PENDING` -> `SHIPMENT_BOOKED` -> `OUT_FOR_DELIVERY` -> `COMPLETED` / `RTO_RETURNED`)
- [ ] **1.2.5 — Async Fulfillment Worker, Real-Time Elasticsearch Indexer & Amazon SNS Notifications (`bins/fulfillment-worker` & `crates/notify-sns`)**
  - [ ] Configure DynamoDB Streams + [Amazon EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-dynamodb.html) routing catalog changes and paid/deposit-confirmed orders to `fulfillment-worker`
  - [ ] Implement real-time Elasticsearch `/_bulk` indexer and `SnsNotificationService` (`crates/notify-sns`), run integration tests, and tag release **`v1.0.0`**

### Slice 2 (`v2.0` — Weeks 5–8): Digital Products & 6-Mode Non-Heartbeat Cryptographic Licensing Engine

#### Sprint 2.1 (Weeks 5–6): S3 Protected Delivery, Offline Ed25519 `.lic` Signing (Mode 1), CEK Envelope Encryption (Mode 4) & Release Gating (Mode 5)
- [ ] **2.1.1 — Digital Product Catalog, Custom Digital Properties & Buyer-Country Digital VAT**
  - [ ] Extend `Product` validation for `ProductType::Digital` and `ProductType::HybridBundle` and add S3 presigned upload/download (`15-min TTL`)
- [ ] **2.1.2 — AWS KMS Asymmetric Ed25519 Offline Certificate Signer (`crates/licensing-ed25519` — Mode 1 & Mode 5)**
  - [ ] Provision asymmetric [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) signing key (`KeySpec::EccCurveEd25519`) and implement `mint_offline_license_certificate` ([RFC 8032](https://www.rfc-editor.org/info/rfc8032/)) + Mode 5 Release-Timestamp Gating + Hybrid Physical-Digital Bundle unlock
- [ ] **2.1.3 — Cryptographic Content Key Unsealing (`Mode 4` — Anti-Patching Envelope Encryption)**
  - [ ] Implement AES-256-GCM asset encryption helper and X25519 Diffie-Hellman CEK unsealing (`POST /v1/licenses/unseal-cek`)

#### Sprint 2.2 (Weeks 7–8): Air-Gapped QR Challenge-Response (Mode 2), CloudFront Signed CRLs (Mode 3), Push Revocation (Mode 6) & SDKs
- [ ] **2.2.1 — Air-Gapped Challenge-Response & Mobile QR Activation (`Mode 2`)**
  - [ ] Implement `POST /v1/licenses/challenge-activate` and mobile QR scanner in `CustomerLicenseVaultBlock`
- [ ] **2.2.2 — CloudFront Edge-Cached Revocation Lists / Bloom Filters (`Mode 3` — [RFC 5280](https://www.rfc-editor.org/info/rfc5280/)) & SNS Push Revocation (`Mode 6`)**
  - [ ] Publish Ed25519-signed `revoked.crl.bin` to S3 + CloudFront on refund/return webhooks and dispatch SNS silent push revocation
- [ ] **2.2.3 — Client Verification SDKs & SDUI License Vault**
  - [ ] Publish Rust (`some-commerce-license-rs`) and TypeScript (`@some-commerce/license-sdk`) verification SDKs and tag **`v2.0.0`**

### Slice 3 (`v3.0` — Weeks 9–12): B2B Wholesale, Cross-Border Express ([Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) & [DHL Express](https://developer.dhl.com/)), RFQ & B2B On-Premise License Proxy

#### Sprint 3.1 (Weeks 9–10): Cognito B2B Orgs, B2B Custom Property/MOQ Filtration & Aramex/DHL Express Adapters
- [ ] **3.1.1 — Cognito B2B Organization Onboarding, B2B WebMCP Tools & Persona Switching**
  - [ ] Implement `B2B_ORG#<org_id>` onboarding, `B2B_ORG_ADMIN` / `B2B_BUYER` Cognito groups, B2B Elasticsearch facets, and `b2b_draft_rfq_from_specs` WebMCP tool
- [ ] **3.1.2 — Cross-Border Shipping via Aramex & DHL Express (`crates/shipping-providers`)**
  - [ ] Implement `AramexProvider` and `DhlExpressProvider` with volumetric weight, HS codes, and bilingual (`Arabic + English`) PDF commercial invoices

#### Sprint 3.2 (Weeks 11–12): RFQ Negotiation State Machine, Milestone Deposits, Durable Net-30 Timers & B2B LAN License Proxy
- [ ] **3.2.1 — B2B Request-for-Quote (RFQ) & Milestone Deposit Workflow**
  - [ ] Implement RFQ state machine (`30% Upfront Deposit`, `70% COD or Net-30`) and `bins/durable-orchestrator` ([AWS Lambda Durable Functions](https://aws.plainenglish.io/aws-lambda-updates-in-2025-2e664f4070d2)) Net-30 SNS reminders
- [ ] **3.2.2 — B2B On-Premise LAN License Proxy (`Mode 6`) & Multi-Seat Management**
  - [ ] Ship `some-commerce-license-proxy` LAN Docker container and `B2BSeatManagementBlock`, and tag **`v3.0.0`**

### Slice 4 (`v4.0` — Weeks 13–16): Multi-Vendor Marketplace, Global Aggregators ([Shippo](https://docs.goshippo.com/) & [EasyPost](https://docs.easypost.com/)), Split Escrow & Crypto

#### Sprint 4.1 (Weeks 13–14): Shippo & EasyPost 40+ Carrier Aggregators + Multi-Vendor Cart & Deposit Splitting
- [ ] **4.1.1 — Vendor Onboarding, Cognito ABAC Isolation, Vendor WebMCP Product Assistant & Elasticsearch Facets**
- [ ] **4.1.2 — Global Multi-Carrier Aggregators (`ShippoProvider` & `EasyPostProvider`)**
- [ ] **4.1.3 — Multi-Vendor Cart Splitting & Proportional Split COD Allocation**

#### Sprint 4.2 (Weeks 15–16): BTCPay Server Crypto Adapter, Double-Entry Escrow Ledger & Vendor Portal
- [ ] **4.2.1 — Self-Hosted Crypto Checkout (`BtcpayProvider`)**
- [ ] **4.2.2 — Double-Entry Escrow Ledger, Delivery-Gated Payouts & SDUI Vendor Portal (`v4.0.0`)**

### Slice 5 (`v5.0` — Weeks 17–20): Dual AWS Marketplace Editions — Standard Lambda vs. AWS Lambda Managed Instances

#### Sprint 5.1 (Weeks 17–18): Multi-Concurrency Tuning, OpenSearch Zero-ETL & Dual AWS CDK Marketplace Stacks
- [ ] **5.1.1 — Lock-Free Multi-Concurrency Optimization (`ArcSwap` / `DashMap`) for [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html)**
- [ ] **5.1.2 — Dual AWS CDK Commercial Packaging (`SomeCommerceServerlessStack` & `SomeCommerceManagedInstancesStack` with OpenSearch Zero-ETL)**

#### Sprint 5.2 (Weeks 19–20): AWS Marketplace Metering, FTR Security Audit & GitHub Sponsors Automation
- [ ] **5.2.1 — AWS Marketplace Metering API, GitHub Sponsors Webhook & FTR Audit (`v5.0.0`)**

### Slice 6 (`v6.0` — Weeks 21–24): Visual Multilingual SDUI Studio, WebMCP Styling Copilot, Dynamic Property/Taxonomy Studio & White-Label Mobile Pipeline

#### Sprint 6.1 (Weeks 21–22): Visual Drag-and-Drop SDUI Studio + AI/WebMCP Styling Copilot & N-Level Taxonomy/Property Designer
- [ ] **6.1.1 — Visual Multilingual SDUI Editor (`"use dom"` in Expo Admin) with Live WebMCP Styling Copilot (`admin_style_and_generate_sdui`)**
- [ ] **6.1.2 — Visual N-Level Category Tree, Dynamic Property & Regional Fee Studio (`admin_configure_store_and_fees`)**

#### Sprint 6.2 (Weeks 23–24): White-Label Mobile App CI/CD Pipeline & Edge SEO `hreflang` Injection
- [ ] **6.2.1 — White-Label Mobile Build Pipeline, Edge SEO `hreflang` Injection & Open-Source `v6.0.0` Launch**

## License

Released under the [MIT License](LICENSE). Sponsored and maintained by [@maheraladdin](https://github.com/maheraladdin).
