# some-commerce

> **Specification status:** Planned design, not verified implementation. The [quality gates](docs/QUALITY_GATES.md) define acceptance, and the [stress-test register](docs/DOCS_STRESS_TEST.md) identifies unresolved contradictions and unverified platform/performance/compliance claims. Examples below require those decisions and evidence before production use.

[![Sponsor maheraladdin](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/maheraladdin)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Rust: Cargo Lambda](https://img.shields.io/badge/Backend-Rust%202024%20%2B%20Tokio%201.54.1%20%2B%20Axum%200.8-orange?style=for-the-badge&logo=rust)](https://www.cargo-lambda.info/)
[![Search: Elasticsearch & OpenSearch](https://img.shields.io/badge/Search-Elasticsearch%20%2B%20DynamoDB-005571?style=for-the-badge&logo=elasticsearch)](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations)
[![AI: WebMCP Ready](https://img.shields.io/badge/AI-WebMCP%20(Customer%20%26%20Admin%20Tools)-8A2BE2?style=for-the-badge)](https://webmachinelearning.github.io/webmcp/)
[![Client: Universal Expo SDK 58](https://img.shields.io/badge/Client-Universal%20Expo%20SDK%2058%20(React%2019%20%2B%20RN%200.88)-000020?style=for-the-badge&logo=expo)](https://docs.expo.dev/)
[![AWS: 100% Native](https://img.shields.io/badge/Cloud-100%25%20AWS%20Serverless-FF9900?style=for-the-badge&logo=amazonaws)](https://aws.amazon.com/lambda/lambda-managed-instances/)
[![Caching: Moka L1 + Redis L2](https://img.shields.io/badge/Caching-Moka%20L1%20%2B%20Redis%20L2-DC382D?style=for-the-badge&logo=redis)](https://docs.rs/moka/)
[![Local-First: WatermelonDB SQLite JSI](https://img.shields.io/badge/Local--DB-WatermelonDB%20(SQLite%20JSI)-FF4154?style=for-the-badge)](https://watermelondb.dev/)
[![Server State: TanStack React Query](https://img.shields.io/badge/Frontend-TanStack%20Query%20v5-FF4154?style=for-the-badge&logo=reactquery)](https://tanstack.com/query/)

**`some-commerce`** is an open-source, 100% AWS-native, **multilingual (`RTL` & `LTR`) B2C & B2B Server-Driven UI (SDUI) e-commerce marketplace** for selling both **physical products** and **cryptographically licensed digital products**, featuring first-class **[WebMCP (`navigator.modelContext`)](https://webmachinelearning.github.io/webmcp/)** and **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/specification/2026-07-28)** tools for both **Customers** and **Store Admins**.

Built on a **Client-First, Multi-Tier Cached, Microkernel Architecture**, `some-commerce` combines a **5-binary Rust 2024 ([Axum 0.8](https://github.com/tokio-rs/axum) + [Tokio 1.54.1](https://tokio.rs/) + [Cargo Lambda](https://www.cargo-lambda.info/)) workspace**, **[Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html)** for authentication and zero-lookup RBAC/ABAC JWT authorization, a **Two-Tier Backend Cache (L1 [Moka 0.12](https://docs.rs/moka/latest/moka/) in-memory TinyLFU + L2 [Amazon ElastiCache Serverless for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html) with Pub/Sub invalidation)**, an **RFC 9110 HTTP `ETag` / `If-None-Match` (`304 Not Modified`) freshness protocol**, **[Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)** + **DynamoDB General Filtration** for **Unlimited N-Level Categories, Brands, User-Customizable Product Properties, and Nested Faceted Search**, **[WebMCP](https://developer.chrome.com/docs/ai/webmcp)** + **[Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html)** for agentic shopping & admin configuration, **[Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)** for localized mobile push (APNs/FCM) and SMS alerts, **[Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)** (Single-Table Design + `GSI5` delta sync), and a **Universal [Expo SDK 58](https://docs.expo.dev/) (React 19 + React Native 0.88 New Architecture) + [Expo Router v5](https://docs.expo.dev/router/introduction/) + [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/)** client powered by **[WatermelonDB](https://watermelondb.dev/docs)** (client-first SQLite via JSI on Mobile and IndexedDB on Web), **[TanStack React Query v5](https://tanstack.com/query/latest/docs/framework/react/overview)**, **Headless Custom Hooks (`packages/domain-hooks`)**, and **Platform-Adaptive UI** ([`@expo/ui`](https://docs.expo.dev/versions/latest/sdk/ui/) SwiftUI / Jetpack Compose + [Expo Native Modules](https://docs.expo.dev/modules/overview/) on Mobile, semantic HTML5 DOM + **Tailwind CSS v4** + [Expo DOM Components](https://docs.expo.dev/guides/dom-components/) on Web).

The project is funded slice-by-slice through **[GitHub Sponsors](https://github.com/sponsors/maheraladdin)** and packaged commercially on **[AWS Marketplace](https://aws.amazon.com/marketplace/)** in two editions:
1. **Standard Serverless Edition**: On-Demand [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-rust.html) + On-Demand DynamoDB (scales to zero when idle).
2. **Enterprise Managed Instances Edition**: [AWS Lambda Managed Instances](https://aws.amazon.com/lambda/lambda-managed-instances/) backed by Graviton4 EC2 Capacity Providers (`MaxConcurrency: 64` sharing L1 Moka RAM) + Dedicated [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) with [DynamoDB Zero-ETL Ingestion](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/OpenSearchIngestionForDynamoDB.html).

## Sponsor This Project

`some-commerce` is built in **6 vertical production slices**. Every slice is unlocked and shipped as a standalone, production-ready release funded by community and commercial sponsors:

* **[Sponsor @maheraladdin on GitHub Sponsors](https://github.com/sponsors/maheraladdin)**

## Documentation Index (`docs/`)

* **[Project Constitution & Spec Kit Standard (.specify/)](.specify/memory/constitution.md)** — Core governing principles, Spec-Driven Development (SDD), zero-clone borrowing discipline in Rust, and non-negotiable security laws.
* **[Master Behavior-Centric Folder Architecture (docs/FOLDER_ARCHITECTURE.md)](docs/FOLDER_ARCHITECTURE.md)** — Locality of Behavior (LoB) hierarchy: `features -> modules -> behaviours -> [services, designs, logic, types, constants]` with 4-tier scoping rules.
* **[Documentation stress test and gap register](docs/DOCS_STRESS_TEST.md)** — Prioritized design/dependency gaps, owners and closure evidence.
* **[Mandatory per-story quality gates](docs/QUALITY_GATES.md)** — Test coverage, security audit, architecture, reuse and maintainability requirements, plus the [evidence template](docs/validation/STORY_EVIDENCE_TEMPLATE.md).

* **[13-Module User Stories Master Index (`docs/user-stories/README.md`)](docs/user-stories/README.md)** — Complete catalog of **51 engineering user stories** organized across 13 functional modules, each featuring Gherkin acceptance criteria, comprehensive test cases (happy path, edge, error, concurrency, security), rendered Mermaid activity diagrams, and cross-module page/endpoint wiring maps.
* **[12-Sprint Delivery Schedule & DoD (`docs/sprints/README.md`)](docs/sprints/README.md)** — Master sprint calendar spanning **12 two-week sprints** across all 6 production slices (~35 story points/sprint), including dedicated Markdown specifications for [Sprint 1.1](docs/sprints/sprint-1.1.md) through [Sprint 6.3](docs/sprints/sprint-6.3.md) with exact story points, deliverables, dependencies, and Definition of Done.
* **[Deployment Infrastructure & AWS Marketplace Master Guide (`docs/DEPLOYMENT_AND_AWS_MARKETPLACE.md`)](docs/DEPLOYMENT_AND_AWS_MARKETPLACE.md)** — Production deployment blueprint covering the 9-stack AWS CDK v2 application, Standard Serverless vs. Enterprise Managed Instances on Graviton4, AWS Foundational Technical Review (FTR) compliance checklist, SaaS Contract/Usage Metering API (`BatchMeterUsage`), and zero-downtime blue/green deployment runbooks.
* **[10-Pillar System Architecture Specification (`docs/SYSTEM_ARCHITECTURE.md`)](docs/SYSTEM_ARCHITECTURE.md)** — Master architecture diagram, Microkernel traits (`crates/kernel-core`), Polyglot DB schemas (DynamoDB Single-Table + Elasticsearch + WatermelonDB), L1 Moka + L2 Redis caching, RFC 9110 HTTP `ETag` freshness protocol, TanStack React Query v5, WatermelonDB delta sync, Headless Custom Hooks (`packages/domain-hooks`), and `@expo/ui` + HTML DOM platform-adaptive design.
* **[Payments, Global Shipping, Split COD & 6-Mode Digital Licensing (`docs/PAYMENTS_SHIPPING_AND_LICENSING.md`)](docs/PAYMENTS_SHIPPING_AND_LICENSING.md)** — KMS-encrypted vault for Paymob, Stripe, and BTCPay Server; global shipping via Bosta, Aramex, DHL Express, Shippo, and EasyPost; Upfront Deposit + Split Cash-on-Delivery (`DEPOSIT_COD`); and **6 Non-Heartbeat E-Product License Verification Modes** (Offline Ed25519, Air-Gapped QR, CloudFront CRLs, AES-256-GCM CEK Unsealing, Release Gating, and B2B LAN Proxy).
* **[Server-Driven UI (SDUI), WebMCP Tools, Dynamic Properties & Multilingual Engine (`docs/SDUI_AND_LOCALIZATION.md`)](docs/SDUI_AND_LOCALIZATION.md)** — Universal Expo SDUI JSON schemas, **Customer & Admin WebMCP Tool Schemas (`navigator.modelContext`)**, `SearchFacetFilterBlock`, N-level `CategoryBreadcrumbBlock`, and bidirectional RTL/LTR layout mirroring.

## 10-Pillar System Architecture Summary

| # | Architectural Pillar | Technology Stack | Core Design & Rationale |
| :--- | :--- | :--- | :--- |
| **1** | **Microkernel Abstract Logic** | `crates/kernel-core` & `crates/plugins-*` | Isolates pure domain rules (`Split-COD` deposit math, N-level taxonomy inheritance, locale fallback, B2B MOQ volume tiers, 6-mode license validation) from external vendors via async Rust trait ports (`PaymentGatewayPlugin`, `ShippingCarrierPlugin`, `CatalogSearchPlugin`, `MultiTierCachePort`). |
| **2** | **Polyglot Database Schema** | `crates/db-schema` & `packages/watermelon-db` | Single-Table [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) (`PK`/`SK` + `GSI1`–`GSI5` delta-sync index), [Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) `nested` `properties[]` mapping, and local [WatermelonDB](https://watermelondb.dev/docs) client schema. |
| **3** | **Repository Tools & Monorepo Toolchain** | Cargo Workspace + Bun/Turborepo | 5-binary [Cargo Lambda](https://www.cargo-lambda.info/) workspace (`cargo-nextest`, `clippy`, `cargo-deny`, `proptest`), automated Rust-to-TypeScript/OpenAPI/[W3C WebMCP](https://webmachinelearning.github.io/webmcp/) schema codegen (`schemars` + `utoipa` + `ts-rs`), `Bun` + `Turborepo` + `Biome`, and [AWS CDK v2](https://docs.aws.amazon.com/cdk/api/v2/). |
| **4** | **L2 Distributed Caching with Redis** | [Amazon ElastiCache Serverless for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html) | [`redis-rs`](https://docs.rs/redis/latest/redis/) `MultiplexedConnection` storing compressed payloads + `etag:{key}` strings, with [Redis Pub/Sub](https://redis.io/docs/latest/develop/use-cases/pub-sub/rust/) (`cache:evict:{tenant}`) broadcasting cache evictions across all running Lambda instances on admin mutations. |
| **5** | **L1 In-Process Caching with Moka** | [`moka::future::Cache`](https://docs.rs/moka/latest/moka/) | Lock-free TinyLFU in-memory cache (`< 50µs` lookup) embedded in Tokio RAM with `try_get_with` request coalescing across 64 concurrent tasks on [AWS Lambda Managed Instances](https://aws.amazon.com/lambda/lambda-managed-instances/). |
| **6** | **HTTP `ETag` Freshness Protocol** | RFC 9110 Conditional Requests | Deterministic `BLAKE3` entity digests (`W/"v{version}-{hash}"`) verified at the Axum L1 Moka / L2 Redis edge in `< 0.1ms` to return [`HTTP 304 Not Modified`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/304) with a `0-byte` body when client data is fresh. |
| **7** | **Frontend Server-State Caching** | [TanStack React Query v5](https://tanstack.com/query/latest/docs/framework/react/overview) | ETag-aware query client (`fetchWithEtag`) managing faceted search aggregations, real-time rate quotes, Split COD calculations, and optimistic mutations. |
| **8** | **Client-First Local Database** | [WatermelonDB](https://watermelondb.dev/docs) | Reactive offline-first database (`SQLiteAdapter` over C++ JSI on iOS/Android; `LokiJSAdapter` + `IndexedDB` on Web) with delta sync (`synchronize()`) against `/v1/sync/pull` and `/v1/sync/push`. |
| **9** | **Headless Custom Hooks Layer** | `packages/domain-hooks` | Pure TypeScript hooks (`useSduiScreen`, `useCatalogSearchAndFacets`, `useProductConfigurator`, `useSplitCodCheckout`, `useDigitalLicenseVault`) that abstract all domain, caching, sync, and WebMCP logic from UI components. |
| **10** | **Platform-Adaptive UI Design Layer** | `packages/ui-primitives` & Native Modules | Native SwiftUI & Jetpack Compose controls via [`@expo/ui`](https://docs.expo.dev/versions/latest/sdk/ui/) + custom Swift/Kotlin [Expo Native Modules](https://docs.expo.dev/modules/overview/) on Mobile, paired with semantic HTML5 DOM (`<main>`, `<aside>`, `<fieldset>`, CSS Grid, CSS Logical RTL/LTR properties) styled with **Tailwind CSS v4** (`@theme` CSS-first engine) + [Expo DOM Components](https://docs.expo.dev/guides/dom-components/) on Web. |

## Master Engineering Checklist (Granular Task-by-Task Breakdown Across All 6 Slices & 12 Sprints)

### Slice 1 (`v1.0` — Weeks 1–4): Core Multilingual Storefront, Microkernel, Multi-Tier Caching, Client-First WatermelonDB, Cognito Auth, Taxonomy, Elasticsearch, WebMCP, Payments & Split COD

#### [Sprint 1.1 (Weeks 1–2): Auth + Storefront + Customer Foundation](docs/sprints/sprint-1.1.md) — 34 Story Points
- [ ] **1.1.1 — Rust Cargo Workspace, Microkernel Core & Codegen Pipeline (`crates/kernel-core` & `crates/db-schema`)**
  - [ ] Initialize root `Cargo.toml` workspace targeting `aarch64-unknown-linux-gnu` (AWS Graviton) with shared dependencies (`tokio`, `axum`, `tower`, `serde`, `moka`, `redis`, `aws-sdk-dynamodb`, `aws-sdk-kms`, `aws-sdk-sns`, `aws-sdk-bedrockruntime`, `tracing`, `schemars`, `utoipa`, `ts-rs`)
  - [ ] Define strongly typed domain identifiers (`TenantId`, `ProductId`, `TaxonomyNodeId`, `PropertyCode`, `BrandId`, `OrderId`, `CognitoSub`)
  - [ ] Define Microkernel trait ports (`PaymentGatewayPlugin`, `ShippingCarrierPlugin`, `CatalogSearchPlugin`, `MultiTierCachePort`, `LicenseAuthorityPlugin`)
  - [ ] Implement `Money` value object (minor units / cents + ISO-4217 currency code) with overflow-safe arithmetic
  - [ ] Define `PropertyDefinition` model supporting 6 data types (`ENUM_SINGLE`, `ENUM_MULTI`, `COLOR_SWATCH`, `NUMERIC_UNIT`, `BOOLEAN`, `TEXT_LOCALIZED`), `is_variant_axis: bool`, `is_filterable: bool`, and `FilterUiWidget` enum (`COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`, `TOGGLE_SWITCH`)
  - [ ] Define `TaxonomyNode` model supporting unlimited N-level nesting (`parent_node_id`, `depth_level: u8`, `ancestors_path: Vec<TaxonomyNodeId>`, `attached_property_ids: Vec<PropertyCode>`) with cycle-detection validation
  - [ ] Define `Brand` model (`names_i18n`, `descriptions_i18n`, `seo_slugs_i18n`, `logo_s3_key`, `is_verified`, `featured_node_ids`)
  - [ ] Define `Product` & `SkuVariant` models supporting inherited category properties, ad-hoc product-level `custom_properties[]`, Cartesian variant generation (`Color x Size`), weight in grams, and stock/reserved counters
  - [ ] Configure `ts-rs` and `schemars` pipeline to export Rust structs to TypeScript interfaces, OpenAPI 3.1 specs, and WebMCP JSON Schemas
- [ ] **1.1.2 — Two-Tier Backend Caching (`crates/cache-tier`) & RFC 9110 HTTP `ETag` Middleware**
  - [ ] Implement Pillar 5 L1 in-process cache using `moka::future::Cache` (TinyLFU admission, `try_get_with` request coalescing across concurrent Tokio tasks)
  - [ ] Implement Pillar 4 L2 distributed cache using `Amazon ElastiCache Serverless for Redis` (`redis::aio::MultiplexedConnection`) with pipelined `data:{key}` and `etag:{key}` reads/writes
  - [ ] Implement Redis Pub/Sub invalidation channel (`cache:evict:{tenant}`) to evict L1 Moka entries across active Lambda instances on admin mutations
  - [ ] Implement deterministic `BLAKE3` `ETag` generator (`W/"v{version}-{hash}"`) on all entities and SDUI layout payloads
  - [ ] Implement Pillar 6 Axum conditional request middleware (`If-None-Match` -> `< 0.1ms` `HTTP 304 Not Modified` short-circuit with 0-byte body; `If-Match` -> `HTTP 412 Precondition Failed` optimistic concurrency)
- [ ] **1.1.3 — Amazon Cognito Authentication & RBAC/ABAC Middleware (`crates/auth-cognito`)** — *[US-1.1.1, US-1.1.2, US-1.1.3]*
  - [ ] Implement Cognito JWKS client (`/.well-known/jwks.json`) with `Arc<RwLock<JwksCache>>` in L1 Moka memory and 60-second refresh rate-limiting on unknown `kid`
  - [ ] Implement RS256 JWT verifier extracting `AuthenticatedPrincipal { sub, tenant_id, persona, preferred_locale, cognito_groups, b2b_org_id, price_list_id, vendor_id }`
  - [ ] Build Axum Tower route-guard extractors: `RequireStoreAdmin`, `RequireVendor`, `RequireB2bBuyer`, `RequireAuthenticatedCustomer`, and `OptionalPrincipal`
  - [ ] Write Rust **Cognito Pre-Token Generation Lambda Trigger** that queries `USER#<sub_id>` in DynamoDB and injects `custom:tenant_id`, `custom:persona`, `custom:pref_locale`, `custom:b2b_org_id`, and `custom:vendor_id` into ID/Access tokens
  - [ ] Write Rust **Cognito Custom SMS Trigger** that inspects phone prefix (`+20`, `+966`, etc.) and `locale` attribute to send localized Arabic/English OTP codes via [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
  - [ ] Implement Passkeys (FIDO2 / WebAuthn) and Social OIDC (Google, Apple) federated identity mapping in Cognito User Pool
- [ ] **1.1.4 — Multilingual & i18n/l10n Fallback Engine (`crates/i18n-engine`)**
  - [ ] Implement 6-step locale resolution middleware (`?locale=` -> URL `/[locale]/...` -> JWT `custom:preferred_locale` -> `Accept-Language` -> `CloudFront-Viewer-Country` -> `tenant.default_locale` -> `en-US`)
  - [ ] Implement deterministic translation fallback chain (`ar-EG` -> `ar` -> `tenant.default_locale` -> `en-US`)
  - [ ] Integrate ICU MessageFormat parser for pluralization, gender rules, and localized currency/number formatting
  - [ ] Build localized API error responder (`AppError -> { code, user_message, locale, trace_id }`)
- [ ] **1.1.5 — DynamoDB Single-Table Repository & Delta Sync (`crates/db-dynamo`)**
  - [ ] Implement `SomeCommerceTable` key builders for `PK`, `SK`, `GSI1PK`/`GSI1SK`, `GSI2PK`/`GSI2SK`, `GSI3PK`/`GSI3SK`, and `GSI5PK`/`GSI5SK` (WatermelonDB Delta Sync index)
  - [ ] Implement CRUD + subtree move operations for `TAXONOMY_NODE#<node_id>` (atomically updating `ancestors_path[]` for descendants)
  - [ ] Implement CRUD for `PROPERTY_DEF#<prop_code>` and `BRAND#<brand_id>`
  - [ ] Implement `ProductRepository` writing master `PRODUCT#<pid>` items alongside localized slug index items (`GSI2PK = SLUG#<locale>#<slug>`)
  - [ ] Implement atomic inventory reservation (`UpdateItem` with `ConditionExpression: "stock_qty >= :qty"`) and release helpers
  - [ ] Implement `/v1/sync/pull` and `/v1/sync/push` delta synchronization endpoints using DynamoDB `GSI5`
- [ ] **1.1.6 — Dual-Tier Catalog Search & Filtration Engine (`crates/search-elastic`)** — *[US-2.1.2, US-2.1.4]*
  - [ ] Define `CatalogSearchProvider` async trait (`search_products`, `suggest_autocomplete`, `index_product_batch`, `delete_product`)
  - [ ] Implement **Tier 1 `DynamoGeneralFilterProvider`** (querying `GSI1` / `GSI2` + `FilterExpression` for `product_type`, `in_stock_only`, `is_on_sale`, `supports_cod`, `min_rating`, and dynamic `properties[]`)
  - [ ] Implement **Tier 2 `ElasticSearchProvider`** ([Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)) with `arabic`, `english`, `french`, and `german` analyzers, `nested` `properties` field, `post_filter` disjunctive faceting, and circuit-breaker fallback to Tier 1
- [ ] **1.1.7 — Customer & Admin WebMCP (`navigator.modelContext`) + Backend MCP Engine (`crates/mcp-tools` & `packages/domain-hooks`)** — *[US-8.1.1]*
  - [ ] Build client-side [W3C WebMCP (`navigator.modelContext.registerTool`)](https://webmachinelearning.github.io/webmcp/) bridge in Universal Expo Web (`useWebMcpBridge` hook) and backend MCP / [Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html) endpoints (`POST /v1/mcp/customer` on `storefront-sdui-api` and `POST /v1/mcp/admin` on `admin-vendor-api`)
  - [ ] Implement **Customer WebMCP Tools**: `search_and_filter_catalog`, `recommend_and_compare_products`, `update_customer_account_details`, `prepare_cart_and_quote_cod`
  - [ ] Implement **Admin WebMCP Tools**: `admin_style_and_generate_sdui`, `admin_configure_store_and_fees`, `admin_create_and_translate_product`
- [ ] **1.1.8 — Client-First Database, TanStack Query, Headless Hooks & Platform-Adaptive UI (`packages/*` & `infra/cdk`)** — *[US-2.1.1, US-7.1.1]*
  - [ ] Implement Pillar 8 WatermelonDB schema (`taxonomy_nodes`, `products`, `sdui_pages`, `cart_items`, `licenses_vault`, `etag_registry`) with JSI SQLite adapter on iOS/Android and LokiJS/IndexedDB adapter on Web
  - [ ] Implement Pillar 7 TanStack React Query v5 client with `fetchWithEtag` interceptor resolving `304 Not Modified` from local storage
  - [ ] Implement Pillar 9 Headless Custom Hooks (`useSduiScreen`, `useCatalogSearchAndFacets`, `useProductConfigurator`, `useSplitCodCheckout`, `useCustomerAccount`)
  - [ ] Build Pillar 10 Platform-Adaptive UI: native SwiftUI / Jetpack Compose controls via [`@expo/ui`](https://docs.expo.dev/versions/latest/sdk/ui/) on Mobile and semantic HTML5 DOM (`<main>`, `<aside>`, `<fieldset>`, CSS Grid, CSS Logical Properties) on Web
  - [ ] Author [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) stack provisioning `SomeCommerceTable`, Cognito User Pool, ElastiCache Serverless Redis, Private S3 Bucket + [CloudFront (OAC)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html), and [`BucketDeployment`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3_deployment.BucketDeployment.html) for `npx expo export --platform web`

#### [Sprint 1.2 (Weeks 3–4): Cart + Checkout + Payments + Fulfillment](docs/sprints/sprint-1.2.md) — 38 Story Points
- [ ] **1.2.1 — AWS KMS Envelope Encryption Vault (`crates/kms-vault` & `bins/admin-vendor-api`)** — *[US-4.1.4]*
  - [ ] Implement `KmsSecretVault` encrypting/decrypting gateway credentials with `EncryptionContext: {"tenant_id": tid, "gateway_type": gtype, "provider": id}` and a 5-minute TTL `ArcSwap` in-memory cache
  - [ ] Build Admin Dashboard endpoints (`PUT /v1/admin/vault/payment-gateways/{provider}`, `PUT /v1/admin/vault/shipping-carriers/{carrier}`, `PUT /v1/admin/vault/search-clusters/elasticsearch`, `PUT /v1/admin/vault/ai-providers/{provider}`)
- [ ] **1.2.2 — Localized Governorate/Zone Fee Engine (`LOCALE_FEES#<country>#<zone>`)** — *[US-4.1.2, US-4.1.3]*
  - [ ] Implement admin CRUD endpoints (`PUT /v1/admin/locale-fees/{country}/{zone}`) supporting bilingual zone names (`"الدقهلية - المنصورة"` / `"Dakahlia - Mansoura"`), base shipping fee, per-kg weight brackets, free-shipping threshold, VAT %, COD surcharge, and **Upfront COD Deposit Rule** (`NONE`, `SHIPPING_FEE_ONLY`, `PERCENTAGE`, `FIXED_AMOUNT`)
  - [ ] Implement `POST /v1/rates/calculate` in `bins/checkout-webhooks-api` with automatic split COD breakdown
- [ ] **1.2.3 — Pluggable Payment Adapters (`crates/plugins-payments`)** — *[US-4.1.1, US-4.1.2, US-4.1.3]*
  - [ ] Implement `PaymobAdapter` ([Paymob Accept API](https://developers.paymob.com/paymob-docs/integration-paths/apis)) with `HMAC-SHA512` signature verification and `StripeAdapter` ([Stripe Payment Intents API](https://docs.stripe.com/api/payment_intents)) with `Stripe-Signature` verification
  - [ ] Implement **Full Cash on Delivery (`FULL_COD`)** with phone OTP verification and courier delivery verification code
  - [ ] Implement **Upfront Deposit COD (`DEPOSIT_COD`)**: payment gateway charges deposit amount upfront; remaining balance assigned to courier collection
  - [ ] Build `PaymentSheet.native.tsx` ([`@stripe/stripe-react-native`](https://docs.expo.dev/versions/latest/sdk/stripe/) + Paymob React Native SDK) and `PaymentSheet.web.tsx`
- [ ] **1.2.4 — Bosta Shipping Adapter & Split COD Order State Machine (`crates/plugins-shipping` & `bins/durable-orchestrator`)** — *[US-5.1.1, US-6.1.1]*
  - [ ] Implement `BostaAdapter` ([Bosta API v2](https://docs.bosta.co/)) with automatic Air Waybill booking, tracking webhooks, and cash collection reconciliation
  - [ ] Implement **Split COD Order State Machine** (`AWAITING_COD_DEPOSIT` -> `DEPOSIT_PAID_COD_PENDING` -> `SHIPMENT_BOOKED` -> `OUT_FOR_DELIVERY` -> `COMPLETED` / `RTO_RETURNED`) inside `bins/durable-orchestrator`
- [ ] **1.2.5 — Async Fulfillment Worker, Real-Time Elasticsearch Indexer & Amazon SNS Notifications (`bins/fulfillment-worker` & `crates/notify-sns`)** — *[US-5.1.4, US-6.1.1]*
  - [ ] Configure DynamoDB Streams + [Amazon EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-dynamodb.html) routing catalog changes and paid/deposit-confirmed orders to `fulfillment-worker`
  - [ ] Implement real-time Elasticsearch `/_bulk` indexer and `SnsNotificationService` (`crates/notify-sns`) for APNs/FCM push and SMS alerts
  - [ ] Implement order tracking screen `/[locale]/orders/[order_id]/confirmation` with live status stepper and tag release **`v1.0.0`**

### Slice 2 (`v2.0` — Weeks 5–8): Digital Products & 6-Mode Non-Heartbeat Cryptographic Licensing Engine

#### [Sprint 2.1 (Weeks 5–6): Digital Asset Pipeline + Licensing Engine (Modes 1–4)](docs/sprints/sprint-2.1.md) — 30 Story Points
- [ ] **2.1.1 — S3 Protected Digital Vault & Presigned Delivery Pipeline (`crates/plugins-licensing`)** — *[US-9.1.1]*
  - [ ] Provision private `digital-vault-{tenant}-{env}` S3 bucket with default SSE-KMS encryption and blocked public access
  - [ ] Implement `POST /v1/products/{id}/assets` in `admin-vendor-api` generating presigned multipart upload URLs with SHA-256 checksum verification
  - [ ] Implement `GET /v1/orders/{id}/downloads/{asset_id}` generating 15-minute expiring presigned GET URLs strictly bound to buyer Cognito `sub`
  - [ ] Build automatic download rate limiting, IP binding, and max download attempt counters in DynamoDB `ORDER#<id>`
- [ ] **2.1.2 — Mode 1: Offline Ed25519 Cryptographic License Signing (`crates/plugins-licensing`)** — *[US-9.1.2]*
  - [ ] Provision asymmetric [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) signing key (`KeySpec::EccCurveEd25519`)
  - [ ] Implement `mint_offline_license_certificate` generating compact `.lic` binary and base64 certificates containing `license_id`, `product_id`, `features[]`, `expires_at`, and `hardware_fingerprint`
  - [ ] Implement high-performance offline verification logic executing in `< 0.2ms` without requiring network connectivity
- [ ] **2.1.3 — Mode 2: Air-Gapped Challenge-Response Activation (`crates/plugins-licensing`)** — *[US-9.1.2]*
  - [ ] Build offline client challenge generation algorithm combining local timestamp, nonce, and hardware SHA-256 fingerprint
  - [ ] Implement `POST /v1/licenses/challenge-activate` generating deterministic response codes
  - [ ] Build visual QR code challenge generator and response scanner using `modules/expo-crypto-license`
- [ ] **2.1.4 — Mode 3: Edge-Cached Certificate Revocation Lists (CRLs) & Bloom Filters** — *[US-9.1.2]*
  - [ ] Implement daily and event-driven Bloom filter CRL compiler serializing revoked license IDs into `revoked.crl.bin`
  - [ ] Publish signed CRL binary to S3 + CloudFront with RFC 9110 HTTP `ETag` caching returning `304 Not Modified` when unchanged
  - [ ] Implement passive client CRL sync with binary search and Bloom filter lookup (< 0.05ms)
- [ ] **2.1.5 — Mode 4: AES-256-GCM Anti-Patching Content Encryption Key (CEK) Unsealing** — *[US-9.1.2]*
  - [ ] Implement build-time asset encryptor generating AES-256-GCM ciphertexts with 96-bit initialization vectors
  - [ ] Implement `POST /v1/licenses/unseal-cek` using ephemeral X25519 Diffie-Hellman key exchange to unseal CEK directly into client enclave memory
- [ ] **2.1.6 — Custom Product Properties & PDP Variant Configuration Refinements** — *[US-2.1.3, US-2.1.5]*
  - [ ] Implement admin property definition management for digital assets (`min_os_version`, `architecture`, `file_format`, `max_activations`)
  - [ ] Wire dynamic property filter widgets (`PILL_TAGS`, `CHECKBOX_LIST`) into catalog PDP and search results

#### [Sprint 2.2 (Weeks 7–8): Licensing Modes 5–6 + SDKs + License Vault UI](docs/sprints/sprint-2.2.md) — 26 Story Points
- [ ] **2.2.1 — Mode 5: Version Release-Timestamp Gating** — *[US-9.1.2]*
  - [ ] Embed `maintenance_end_timestamp` and `allowed_major_version` into signed Ed25519 certificates
  - [ ] Build client verification check: app executable compile timestamp `T_build <= T_maintenance` allows execution; newer builds prompt renewal
  - [ ] Support perpetual fallback licensing (users keep perpetual access to versions released during active maintenance)
- [ ] **2.2.2 — Mode 6: Real-Time SNS Push Revocation (`crates/notify-sns`)** — *[US-9.1.2]*
  - [ ] Implement event trigger on refund, RMA return, or fraud detection publishing silent push notifications via Amazon SNS (APNs/FCM)
  - [ ] Implement client-side silent push handler in `packages/domain-hooks` immediately wiping local license certificates and cached CEK keys
- [ ] **2.2.3 — Client Verification SDKs (`some-commerce-license-rs` & `@some-commerce/license-sdk`)** — *[US-9.1.3]*
  - [ ] Publish standalone, zero-dependency Rust crate `some-commerce-license-rs` for desktop, CLI, and embedded integration
  - [ ] Publish TypeScript/JavaScript SDK `@some-commerce/license-sdk` supporting Node.js, Electron, React Native, and WebAssembly
  - [ ] Author integration test suite verifying Ed25519 signatures, CRL parsing, and offline validation across macOS, Linux, and Windows
- [ ] **2.2.4 — SDUI Customer License Vault & Mobile QR Scanner** — *[US-9.1.4]*
  - [ ] Build `/[locale]/account/licenses` screen displaying active licenses, expiration dates, seat allocations, and download links
  - [ ] Build `CustomerLicenseVaultBlock` SDUI component with native camera QR activation scanner using `expo-camera`
- [ ] **2.2.5 — Customer Account Features: Wishlist & Notification Preferences** — *[US-7.1.3, US-7.1.4]*
  - [ ] Implement `/[locale]/account/wishlist` with WatermelonDB offline sync and stock/price alert notifications
  - [ ] Implement `/[locale]/account/notifications` toggle matrix (SMS, Push, Email) and tag release **`v2.0.0`**

### Slice 3 (`v3.0` — Weeks 9–12): B2B Wholesale, Cross-Border Express, RFQ & B2B On-Premise License Proxy

#### [Sprint 3.1 (Weeks 9–10): B2B Onboarding + Tiered Pricing + Cross-Border Shipping](docs/sprints/sprint-3.1.md) — 31 Story Points
- [ ] **3.1.1 — B2B Organization Registration & Approval Flow (`bins/admin-vendor-api`)** — *[US-1.1.4]*
  - [ ] Implement `POST /v1/auth/b2b-register` collecting company legal name, tax ID / commercial register number, country, and billing address
  - [ ] Build Admin verification dashboard (`GET /v1/admin/b2b/applications`, `POST /v1/admin/b2b/applications/{id}/approve`)
  - [ ] Automate Cognito group assignment (`B2B_ORG_ADMIN`, `B2B_BUYER`) and custom JWT claims (`custom:b2b_org_id`, `custom:price_list_id`)
- [ ] **3.1.2 — B2B Tiered Volume Pricing & MOQ Enforcement (`crates/kernel-core`)** — *[US-10.1.1]*
  - [ ] Extend DynamoDB `PRODUCT#<pid>` schema with `b2b_pricing_tiers: [{ min_qty, unit_price_cents }]` and `min_order_quantity (MOQ)`
  - [ ] Implement volume pricing engine in Rust microkernel calculating bulk discounts automatically on PDP and cart
  - [ ] Enforce MOQ validation in cart addition and checkout with localized error messages
- [ ] **3.1.3 — B2B Elasticsearch Facets & Wholesale Filtration (`crates/search-elastic`)** — *[US-10.1.3]*
  - [ ] Add B2B search filters: `has_volume_pricing`, `max_moq`, `in_stock_bulk`, and `b2b_category`
  - [ ] Restrict wholesale pricing display strictly to verified B2B principals via Cognito ABAC token inspection
- [ ] **3.1.4 — Cross-Border Express Shipping via Aramex & DHL Express (`crates/plugins-shipping`)** — *[US-5.1.2]*
  - [ ] Implement `AramexAdapter` ([Aramex Platform API](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform)) supporting rate calculation, shipment creation, and pickup scheduling
  - [ ] Implement `DhlExpressAdapter` ([DHL Express MyDHL API](https://developer.dhl.com/)) with dimensional weight calculations and customs duty estimates
  - [ ] Implement automated bilingual (Arabic & English) commercial invoice and Air Waybill PDF generation
- [ ] **3.1.5 — Customer Shopping Assistant WebMCP Enhancements & Address Book** — *[US-7.1.2, US-8.1.1]*
  - [ ] Extend `search_and_filter_catalog` WebMCP tool to support natural language B2B queries ("Show bulk discounts for USB-C cables")
  - [ ] Implement customer multi-address management screen `/[locale]/account/addresses` with default billing/shipping toggles

#### [Sprint 3.2 (Weeks 11–12): RFQ Negotiation + Net-Terms + LAN License Proxy](docs/sprints/sprint-3.2.md) — 32 Story Points
- [ ] **3.2.1 — Durable RFQ Negotiation State Machine (`bins/durable-orchestrator`)** — *[US-10.1.2]*
  - [ ] Implement RFQ submission endpoint `POST /v1/b2b/rfq` supporting custom quantity requests, target unit price, and special packaging notes
  - [ ] Build RFQ negotiation workflow: `SUBMITTED` -> `SELLER_COUNTER_OFFER` -> `BUYER_ACCEPTED` -> `PO_GENERATED` -> `CONVERTED_TO_ORDER`
  - [ ] Author durable execution timer: 14-day negotiation expiration with automated SNS reminders to buyer and vendor
- [ ] **3.2.2 — B2B Invoicing & Net-Terms Milestone Payments (`crates/plugins-payments`)** — *[US-10.1.2]*
  - [ ] Implement milestone split payments: 30% upfront confirmation deposit + 70% upon delivery or Net-30/Net-60 terms
  - [ ] Build automated Net-30 invoice scheduler in `bins/durable-orchestrator` sending reminder alerts on Day 15, Day 25, and overdue alerts on Day 31
  - [ ] Generate downloadable PDF invoices with tax breakdown, VAT compliance, and wire transfer bank details
- [ ] **3.2.3 — B2B On-Premise LAN License Proxy (`crates/plugins-licensing`)** — *[US-10.1.4]*
  - [ ] Author lightweight Docker container `some-commerce-license-proxy` deployable on local enterprise Kubernetes or Docker networks
  - [ ] Implement periodic master lease refresh: proxy connects to cloud once every 30 days to obtain signed cryptographically bound quota
  - [ ] Build local LAN seat allocation server: local developer workstations checkout/heartbeat floating seats over local HTTP API
- [ ] **3.2.4 — Global Multi-Carrier Aggregation (Shippo & EasyPost) & Admin Copilot** — *[US-5.1.3, US-8.1.2, US-6.1.2]*
  - [ ] Implement `ShippoAdapter` and `EasyPostAdapter` querying 40+ international carriers for real-time rates
  - [ ] Extend Admin WebMCP tool `admin_configure_store_and_fees` to configure global shipping rate markups and tag **`v3.0.0`**

### Slice 4 (`v4.0` — Weeks 13–16): Multi-Vendor Marketplace, Split Escrow & Crypto Checkout

#### [Sprint 4.1 (Weeks 13–14): Multi-Vendor Onboarding + Sub-Order Splitting](docs/sprints/sprint-4.1.md) — 30 Story Points
- [ ] **4.1.1 — Vendor Onboarding & RBAC/ABAC Catalog Isolation (`bins/admin-vendor-api`)** — *[US-11.1.1]*
  - [ ] Implement vendor registration endpoint `POST /v1/vendor/register` collecting business details, commercial registry, and bank payout info
  - [ ] Implement Admin vendor approval workflow assigning `VENDOR` Cognito group and `custom:vendor_id` attribute
  - [ ] Enforce DynamoDB ABAC isolation: Vendor endpoints strictly filter queries by `vendor_id`; cross-tenant/cross-vendor access returns `403 Forbidden`
- [ ] **4.1.2 — Multi-Vendor Cart Grouping & Dynamic Shipping Estimation (`packages/domain-hooks`)** — *[US-3.1.2]*
  - [ ] Implement client-side cart grouping partitioning items by `vendor_id`
  - [ ] Display independent shipping carrier selection and rates per vendor in checkout
  - [ ] Compute combined cart summary with transparent itemization of sub-totals, per-vendor shipping fees, and taxes
- [ ] **4.1.3 — Atomic Sub-Order Splitting at Checkout (`bins/checkout-webhooks-api`)** — *[US-11.1.2]*
  - [ ] Implement atomic checkout transaction using DynamoDB `TransactWriteItems`: creates parent `ORDER#<id>` alongside individual `SUB_ORDER#<vendor_id>#<id>` items
  - [ ] Split upfront COD deposit and online payment totals proportionally across sub-orders
  - [ ] Generate independent Air Waybills and tracking codes per vendor sub-order
- [ ] **4.1.4 — Admin Payment Gateway Configuration Dashboard (`crates/kms-vault`)** — *[US-4.1.4]*
  - [ ] Build `/[locale]/admin/settings-gateways` UI for managing Stripe, Paymob, and BTCPay API keys
  - [ ] Implement real-time gateway health check probes verifying webhook secret validity and API connectivity
- [ ] **4.1.5 — Shared MCP Engine & Bedrock Integration Refactoring (`crates/mcp-tools`)** — *[US-8.1.3]*
  - [ ] Consolidate JSON schema tool registries across customer and admin personas into unified `crates/mcp-tools`
  - [ ] Implement Bedrock Converse API tool dispatcher with structured error recovery and model retry loops

#### [Sprint 4.2 (Weeks 15–16): Escrow Ledger + Vendor Portal + BTCPay + RMA](docs/sprints/sprint-4.2.md) — 34 Story Points
- [ ] **4.2.1 — Double-Entry Escrow Ledger & Automated Payout Engine (`crates/db-dynamo`)** — *[US-11.1.3]*
  - [ ] Implement immutable double-entry escrow ledger in DynamoDB (`LEDGER#<entry_id>`) recording credit/debit entries for every sub-order
  - [ ] Implement delivery-gated escrow holding: funds locked upon payment and automatically scheduled for release 14 days post-delivery
  - [ ] Build vendor payout disbursement pipeline calculating marketplace commission percentage and net vendor earnings
- [ ] **4.2.2 — Self-Service Vendor Portal Dashboard (`/[locale]/vendor/dashboard`)** — *[US-11.1.4]*
  - [ ] Build vendor dashboard displaying sales revenue, pending escrow balances, active sub-orders, and low-stock alerts
  - [ ] Implement vendor catalog management UI: create/edit products, manage variant stock, and view customer reviews
  - [ ] Build vendor order fulfillment view: download shipping labels, book courier pickups, and update fulfillment status
- [ ] **4.2.3 — Bitcoin & Lightning Network Checkout via BTCPay Server (`crates/plugins-payments`)** — *[US-4.1.5]*
  - [ ] Implement `BtcPayAdapter` integrating with self-hosted BTCPay Server Greenfield API
  - [ ] Build dynamic invoice generator displaying on-chain Bitcoin address and Lightning Network BOLT11 payment request QR code
  - [ ] Implement secure webhook listener verifying `BTCPAY-SIG` HMAC-SHA256 signatures to confirm zero-conf / 1-conf settlements
- [ ] **4.2.4 — Return Merchandise Authorization (RMA) & Reverse Logistics (`crates/plugins-shipping`)** — *[US-6.1.3]*
  - [ ] Build customer return filing UI `/[locale]/account/orders/[id]/return` with item selection, reason codes, and photo uploads
  - [ ] Implement RMA approval workflow in `admin-vendor-api`: automated return Air Waybill generation with Bosta / Aramex reverse logistics
  - [ ] Freeze escrow payouts automatically upon RMA filing until merchant inspects returned items
- [ ] **4.2.5 — Admin Order Management Dashboard & Multi-Step Checkout Refinements** — *[US-6.1.4, US-3.1.3]*
  - [ ] Build `/[locale]/admin/orders` featuring multi-faceted filtering (status, country, payment method, vendor, date range)
  - [ ] Refine checkout error handling for card declines, stock race conditions, and tag release **`v4.0.0`**

### Slice 5 (`v5.0` — Weeks 17–18): Dual AWS Marketplace Editions & SaaS Metering

#### [Sprint 5.1 (Weeks 17–18): CDK Packaging, AWS Marketplace Listing & SaaS Metering](docs/sprints/sprint-5.1.md) — 34 Story Points
- [ ] **5.1.1 — AWS CDK v2 Modular Infrastructure Stack Packaging (`infra/cdk`)** — *[US-13.1.1]*
  - [ ] Structure CDK application into 9 idempotent nested stacks (`VpcStack`, `StorageStack`, `DataStack`, `AuthStack`, `ComputeStack`, `SearchStack`, `ApiStack`, `WorkerStack`, `ObservabilityStack`)
  - [ ] Configure `context` parameters: `computeMode` (`ON_DEMAND` vs `MANAGED_INSTANCES`), `domainName`, `acmCertArn`, `environment`
  - [ ] Author 1-click CloudFormation Quick Start template packaging all resources for automated buyer-account deployment
- [ ] **5.1.2 — Multi-Concurrency & Graviton4 Optimization for AWS Lambda Managed Instances** — *[US-13.1.1, US-12.1.2]*
  - [ ] Configure `MaxConcurrency: 64` per execution container for [AWS Lambda Managed Instances](https://aws.amazon.com/lambda/lambda-managed-instances/)
  - [ ] Optimize lock-free in-memory caching: share single L1 Moka TinyLFU cache in RAM across all 64 concurrent Tokio async tasks
  - [ ] Implement OpenSearch Ingestion (OSIS) pipeline for automated DynamoDB Zero-ETL replication
- [ ] **5.1.3 — AWS Foundational Technical Review (FTR) Audit Compliance (`infra/security`)** — *[US-13.1.2]*
  - [ ] Enforce KMS encryption across all DynamoDB tables, S3 buckets, and ElastiCache Redis clusters
  - [ ] Validate zero wildcard (`*`) IAM policies; verify least-privilege role definitions across all 5 Lambda execution roles
  - [ ] Verify TLS 1.3 encryption on CloudFront, API Gateway, and internal inter-service communication
  - [ ] Ensure GDPR compliance: verify data erasure and export APIs (`POST /v1/account/erasure`)
- [ ] **5.1.4 — AWS Marketplace SaaS Metering & Usage-Based Billing (`bins/fulfillment-worker`)** — *[US-13.1.3]*
  - [ ] Implement customer onboarding webhook resolving `x-amzn-marketplace-token` via `ResolveCustomer` API
  - [ ] Implement hourly usage aggregation in `fulfillment-worker` metering API calls, active merchants, storage GB, and settled GMV
  - [ ] Integrate official `aws-sdk-marketplacemetering` calling `BatchMeterUsage` with idempotent SQS retry queues and Dead Letter Queues
  - [ ] Configure Free Tier entitlement limits and upgrade prompts, and tag release **`v5.0.0`**

### Slice 6 (`v6.0` — Weeks 19–24): Visual Multilingual SDUI Studio, White-Label Pipeline, Performance & Launch

#### [Sprint 6.1 (Weeks 19–20): SDUI Visual Studio & Dual-Edition Toggle](docs/sprints/sprint-6.1.md) — 30 Story Points
- [ ] **6.1.1 — Visual Drag-and-Drop SDUI Studio (`"use dom"` in Expo Admin)** — *[US-12.1.1]*
  - [ ] Build visual web canvas in `/[locale]/admin/sdui-studio` utilizing Expo DOM Components (`"use dom"`)
  - [ ] Implement drag-and-drop block palette: `HeroBannerBlock`, `ProductCarouselBlock`, `CategoryGridBlock`, `FlashSaleTimerBlock`, `RichTextBlock`
  - [ ] Build live property editor: modify block JSON attributes, typography, spacing, colors, and targeting rules with instant canvas re-render
- [ ] **6.1.2 — Dual-Viewport RTL/LTR Synchronous Live Preview** — *[US-12.1.1]*
  - [ ] Build side-by-side synchronized viewports previewing Arabic (`ar-EG`, RTL) and English (`en-US`, LTR) layouts simultaneously
  - [ ] Synchronize scroll position, active block selections, and viewport resizing across mobile and desktop breakpoints
- [ ] **6.1.3 — SDUI Version History, Draft Staging & Instant Cache Invalidation** — *[US-12.1.1]*
  - [ ] Implement draft state persistence in DynamoDB: staging changes without affecting live production storefronts
  - [ ] Implement 1-click publishing: atomically writes published layout to `SDUI#<route>#<persona>` and broadcasts Redis Pub/Sub cache eviction
  - [ ] Build revision history timeline supporting 1-click rollback to any previously published version
- [ ] **6.1.4 — Dual-Edition Deployment Toggle in Admin Dashboard** — *[US-12.1.2]*
  - [ ] Build deployment mode configuration view in `/[locale]/admin/settings-infrastructure`
  - [ ] Provide real-time telemetry comparing cold start latencies, P99 response times, and monthly operational costs between Serverless and Managed Instances
- [ ] **6.1.5 — Admin WebMCP Styling Copilot & Observability Telemetry** — *[US-8.1.2]*
  - [ ] Connect `admin_style_and_generate_sdui` WebMCP tool to visual studio canvas allowing natural-language UI restructuring
  - [ ] Build L1/L2/ETag cache hit ratio telemetry dashboard in CloudWatch

#### [Sprint 6.2 (Weeks 21–22): White-Label Mobile App CI/CD Pipeline & Edge SEO](docs/sprints/sprint-6.2.md) — 26 Story Points
- [ ] **6.2.1 — Automated White-Label Mobile App Build Pipeline (`infra/ci-cd`)** — *[US-12.1.3]*
  - [ ] Implement white-label configuration parser (`app.config.ts`) dynamically injecting app name, bundle ID, app icon, splash screen, and brand theme tokens
  - [ ] Author automated GitHub Actions / EAS Build workflow building production `.ipa` (iOS) and `.apk` / `.aab` (Android) binaries from single codebase
  - [ ] Implement over-the-air (OTA) update publishing via EAS Update for rapid SDUI client bundle patches
- [ ] **6.2.2 — Edge SEO `hreflang` & Dynamic Social OpenGraph Injection (`infra/edge`)** — *[US-12.1.3]*
  - [ ] Author CloudFront Function injecting bidirectional `hreflang` headers (`ar`, `en`, `x-default`) based on URL path
  - [ ] Implement dynamic OpenGraph meta tag injection for products, categories, and brand landing pages
  - [ ] Generate automated XML sitemaps (`/sitemap.xml`, `/sitemap-ar.xml`, `/sitemap-en.xml`) refreshed via EventBridge cron
- [ ] **6.2.3 — End-to-End Integration Test Suite & Automated Smoke Tests**
  - [ ] Build automated Playwright E2E test suite covering: user registration -> product search -> cart -> split COD checkout -> courier tracking
  - [ ] Validate RTL bidirectional layout rendering, font kerning, and icon mirroring on iOS, Android, and Web
- [ ] **6.2.4 — Public AWS Marketplace Production Launch Preparation**
  - [ ] Finalize Marketplace product listing, documentation assets, architecture diagrams, and pricing tiers
  - [ ] Publish automated onboarding wizard guiding new subscribers through store domain mapping and initial catalog import

#### [Sprint 6.3 (Weeks 23–24): Hardening, Performance Tuning & Launch Prep](docs/sprints/sprint-6.3.md) — 24 Story Points
- [ ] **6.3.1 — Security Hardening, Penetration Testing & OWASP Top 10 Audit**
  - [ ] Execute automated SAST/DAST security scans (`cargo-deny`, `semgrep`, OWASP ZAP)
  - [ ] Perform comprehensive penetration test: verify rate limiting, JWT token expiry, SQL/NoSQL injection resistance, and RBAC privilege escalation prevention
  - [ ] Validate KMS key rotation policies and verify zero plain-text secrets in repository or build logs
- [ ] **6.3.2 — Large-Scale Load Testing & Performance Optimization (k6 / Artillery)**
  - [ ] Execute distributed load tests simulating 10,000 concurrent shopping sessions and flash sale surges
  - [ ] Verify search performance: P99 latency < 50ms on faceted search queries across 1,000,000 SKU catalog
  - [ ] Verify checkout throughput: > 500 orders/second sustained without DynamoDB throttling or database hot partitioning
  - [ ] Validate ETag cache hit ratio > 85% on static and SDUI screen endpoints
- [ ] **6.3.3 — Chaos Engineering & Failure Resilience Drills**
  - [ ] Execute AWS Fault Injection Simulator (FIS) experiments: inject simulated ElastiCache node failure, KMS throttling, and carrier API timeouts
  - [ ] Validate circuit-breaker fallback: search gracefully falls back to Tier 1 DynamoDB filter when OpenSearch is degraded
  - [ ] Verify SQS Dead Letter Queue alerting and automated retry mechanisms for fulfillment workers
- [ ] **6.3.4 — Production Readiness & Public Release `v6.0.0`**
  - [ ] Finalize operational runbooks, incident response playbooks, and CloudWatch alarm threshold matrix
  - [ ] Establish 24/7 on-call escalation rotation and SLA monitoring
  - [ ] Publish official v6.0.0 GitHub release tag, release notes, and public documentation site

## License

Released under the [MIT License](LICENSE). Sponsored and maintained by [@maheraladdin](https://github.com/maheraladdin).
