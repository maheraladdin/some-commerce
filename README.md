# some-commerce

[![Sponsor maheraladdin](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/maheraladdin)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](./LICENSE)

**Open-Source, 100% AWS-Native, Multilingual (`RTL` & `LTR`), Client-First & Multi-Tier Cached Server-Driven UI (SDUI) Commerce & 6-Mode Licensing Platform** for B2C, B2B Wholesale, Multi-Vendor Physical Fulfillment, and Offline-Verifiable Digital Products.

## 10-Pillar System Architecture

Full specification and diagrams in [`docs/SYSTEM_ARCHITECTURE.md`](./docs/SYSTEM_ARCHITECTURE.md):

1. **Microkernel Abstract Logic (`crates/kernel-core`)**: Pure domain rules (`Split-COD` math, N-level taxonomy inheritance, locale fallback, B2B MOQ tiers, 6-mode licensing) decoupled from external gateways via async Rust trait ports (`PaymentGatewayPlugin`, `ShippingCarrierPlugin`, `CatalogSearchPlugin`, `MultiTierCachePort`).
2. **Polyglot Database Schema (`crates/db-schema`)**: Backend Single-Table [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) (`PK`/`SK` + `GSI1`–`GSI5` delta sync index), [Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) `nested` `properties[]` facet mapping, and Frontend [WatermelonDB](https://watermelondb.dev/docs) schema.
3. **Repository Tools & Monorepo Toolchain**: 5-binary [Cargo Lambda](https://www.cargo-lambda.info/) workspace (`cargo-nextest`, `clippy`, `cargo-deny`, `proptest`), automated Rust-to-TypeScript/OpenAPI/[W3C WebMCP](https://webmachinelearning.github.io/webmcp/) schema codegen (`schemars` + `utoipa` + `ts-rs`), `Bun` + `Turborepo` + `Biome`, and [AWS CDK v2](https://docs.aws.amazon.com/cdk/api/v2/).
4. **L2 Distributed Caching with Redis (`crates/cache-tier`)**: [Amazon ElastiCache Serverless for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html) (`redis-rs` `MultiplexedConnection`) storing compressed payloads + `etag:{key}` strings, with [Redis Pub/Sub](https://redis.io/docs/latest/develop/use-cases/pub-sub/rust/) (`cache:evict:{tenant}`) to evict stale L1 cache entries across all running Lambda instances.
5. **L1 In-Process Caching with Moka (`crates/cache-tier`)**: [`moka::future::Cache`](https://docs.rs/moka/latest/moka/) TinyLFU lock-free in-memory cache (`< 50µs` lookup) with `try_get_with` request coalescing across 64 concurrent Tokio tasks on [AWS Lambda Managed Instances](https://aws.amazon.com/lambda/lambda-managed-instances/).
6. **HTTP `ETag` & `If-None-Match` (`304 Not Modified`) Freshness Protocol**: Deterministic `BLAKE3` entity digests (`W/"v{version}-{hash}"`) verified at the Axum L1 Moka / L2 Redis middleware in `< 0.1ms` to return [`HTTP 304 Not Modified`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/304) with a `0-byte` body when frontend data is still fresh.
7. **Frontend Server-State Caching with [TanStack React Query](https://tanstack.com/query/latest/docs/framework/react/overview) (`packages/query-etag-client`)**: ETag-aware query client (`fetchWithEtag`) managing faceted search, shipping rate quotes, Split COD calculations, and optimistic mutations.
8. **Client-First Local Database using [WatermelonDB](https://watermelondb.dev/docs) (`packages/watermelon-db`)**: Reactive offline-first database (`SQLiteAdapter` over C++ JSI on iOS/Android; `LokiJSAdapter` + `IndexedDB` on Web) with delta sync (`synchronize()`) against `/v1/sync/pull` and `/v1/sync/push`.
9. **Headless Custom Hooks Layer (`packages/domain-hooks`)**: Pure TypeScript hooks (`useSduiScreen`, `useCatalogSearchAndFacets`, `useProductConfigurator`, `useSplitCodCheckout`, `useDigitalLicenseVault`) that abstract all domain, caching, sync, and WebMCP logic from UI components.
10. **Platform-Adaptive UI Design Layer (`packages/ui-primitives` & `modules/expo-crypto-license`)**: Native SwiftUI & Jetpack Compose controls via [`@expo/ui`](https://docs.expo.dev/versions/latest/sdk/ui/) + custom Swift/Kotlin [Expo Native Modules](https://docs.expo.dev/modules/overview/) on Mobile, paired with semantic HTML5 DOM (`<main>`, `<aside>`, `<fieldset>`, CSS Grid, CSS Logical RTL/LTR properties) + [Expo DOM Components](https://docs.expo.dev/guides/dom-components/) on Web.

## Documentation Index

* **[`docs/SYSTEM_ARCHITECTURE.md`](./docs/SYSTEM_ARCHITECTURE.md)**: Complete 10-Pillar System Architecture, Microkernel traits, DynamoDB/Elasticsearch/WatermelonDB schemas, Moka L1 + Redis L2 + HTTP ETag protocol, Custom Hooks, and `@expo/ui` + HTML DOM specifications with Mermaid diagrams.
* **[`docs/USER_STORIES_AND_SPRINTS.md`](./docs/USER_STORIES_AND_SPRINTS.md)**: Deep User Stories (`US-1.1` through `US-6.1`), each with its **Pages & SDUI Screen Inventory**, **Step-by-Step End-to-End Workflow**, and **Mermaid Sequence/Architecture Diagram**.
* **[`docs/PAYMENTS_SHIPPING_AND_LICENSING.md`](./docs/PAYMENTS_SHIPPING_AND_LICENSING.md)**: Paymob, Stripe, BTCPay Server, Bosta, Aramex, DHL Express, Shippo, EasyPost, Split-COD math, and the 6-Mode Non-Heartbeat Digital Licensing Engine.
* **[`docs/SDUI_AND_LOCALIZATION.md`](./docs/SDUI_AND_LOCALIZATION.md)**: Multilingual (`RTL`/`LTR`) Server-Driven UI schemas, Customer & Admin WebMCP (`navigator.modelContext`) tool contracts, and Expo Router localization.

## Detailed Engineering Checklist (Slice 1 – Slice 6)

### Slice 1 (`v1.0`): Microkernel, Multi-Tier Cache, Client-First Storefront, Auth, Taxonomy, Elasticsearch, WebMCP & Split COD
- [ ] **1.1.1 Monorepo & Microkernel Core (`crates/kernel-core` & `crates/db-schema`)**
  - [ ] Initialize Cargo Workspace (`resolver = "2"`) + Bun/Turborepo (`Turbo.json`, `Biome`) + Docker Compose local harness (`DynamoDB Local`, `Redis 7.4`, `OpenSearch`, `LocalStack`)
  - [ ] Define Microkernel trait ports (`PaymentGatewayPlugin`, `ShippingCarrierPlugin`, `CatalogSearchPlugin`, `MultiTierCachePort`, `LicenseAuthorityPlugin`)
  - [ ] Implement DynamoDB Single-Table models (`PK`/`SK` + `GSI1`–`GSI5` delta sync index) and deterministic `BLAKE3` `ETag` generator (`W/"v{version}-{hash}"`)
  - [ ] Configure `schemars` + `utoipa` + `ts-rs` pipeline to export Rust schemas to TypeScript, OpenAPI 3.1, and WebMCP JSON Schemas
- [ ] **1.1.2 Two-Tier Backend Caching (`crates/cache-tier`) & HTTP `ETag` Middleware**
  - [ ] Implement Pillar 5 L1 in-process cache using `moka::future::Cache` (TinyLFU admission, `try_get_with` request coalescing)
  - [ ] Implement Pillar 4 L2 distributed cache using `Amazon ElastiCache Serverless for Redis` (`redis::aio::MultiplexedConnection`) with pipelined `data:{key}` and `etag:{key}` reads/writes
  - [ ] Implement Redis Pub/Sub invalidation listener (`cache:evict:{tenant}`) to evict L1 Moka entries across active Lambda instances on admin mutations
  - [ ] Implement Pillar 6 Axum conditional request middleware (`If-None-Match` -> `< 0.1ms` `HTTP 304 Not Modified` short-circuit; `If-Match` -> `HTTP 412 Precondition Failed` optimistic concurrency)
- [ ] **1.1.3 Client-First Data Layer (`packages/watermelon-db`, `packages/query-etag-client`, `packages/domain-hooks`)**
  - [ ] Implement Pillar 8 WatermelonDB schema (`taxonomy_nodes`, `products`, `sdui_pages`, `cart_items`, `licenses_vault`, `etag_registry`) with JSI SQLite adapter on iOS/Android and LokiJS/IndexedDB adapter on Web
  - [ ] Implement `/v1/sync/pull` and `/v1/sync/push` delta synchronization endpoints using DynamoDB `GSI5`
  - [ ] Implement Pillar 7 TanStack React Query v5 client with `fetchWithEtag` interceptor resolving `304 Not Modified` from local storage
  - [ ] Implement Pillar 9 Headless Custom Hooks (`useSduiScreen`, `useCatalogSearchAndFacets`, `useProductConfigurator`, `useSplitCodCheckout`, `useDigitalLicenseVault`)
- [ ] **1.1.4 Platform-Adaptive UI Layer (`packages/ui-primitives` & `modules/expo-crypto-license`)**
  - [ ] Build `.native.tsx` mobile components using `@expo/ui` (SwiftUI on iOS & Jetpack Compose on Android)
  - [ ] Build `.web.tsx` web components using semantic HTML5 DOM (`<main>`, `<nav>`, `<aside>`, `<fieldset>`, `<dialog>`), CSS Grid, and CSS Logical Properties (`margin-inline-start`, `padding-inline-end`) for `RTL`/`LTR`
  - [ ] Scaffold custom Swift/Kotlin Expo Native Module (`modules/expo-crypto-license`) for Secure Enclave / Keystore `Ed25519` storage and QR scanning
- [ ] **1.1.5 Auth, N-Level Taxonomy, Custom Properties & Dual-Tier Elasticsearch Filtration (`US-1.1` – `US-1.4`)**
  - [ ] Provision Amazon Cognito User Pool + Rust `pre-token-enrichment` Lambda Trigger (`STORE_ADMIN`, `VENDOR`, `B2B_ORG_ADMIN`, `B2B_BUYER`, `B2C_CUSTOMER`)
  - [ ] Implement Unlimited N-Level Categories (`TAXONOMY_NODE`), Brands (`BRAND`), and Admin-Customizable Product Properties (`PROPERTY_DEF` with `COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`)
  - [ ] Implement Tier 2 Elasticsearch/OpenSearch nested facet adapter + Tier 1 DynamoDB General Filtration circuit-breaker fallback
- [ ] **1.1.6 Customer & Admin WebMCP (`navigator.modelContext`) + Bedrock Converse (`US-1.7` – `US-1.8`)**
  - [ ] Implement Customer WebMCP suite (`search_and_filter_catalog`, `recommend_and_compare_products`, `prepare_cart_and_quote_cod`, `update_customer_account_details`)
  - [ ] Implement Admin WebMCP suite (`admin_style_and_generate_sdui`, `admin_configure_store_and_fees`, `admin_create_and_translate_product`)
- [ ] **1.1.7 Localized Checkout, Split COD Deposit, Bosta & Amazon SNS (`US-1.5` – `US-1.6`)**
  - [ ] Implement Paymob (`HMAC-SHA512`) and Stripe (`Stripe-Signature`) plugins + Split-COD upfront deposit calculator (`LOCALE_FEES#<country>#<zone>`)
  - [ ] Implement AWS Lambda Durable Function for 30-minute deposit reservation + Bosta AWB dispatch + localized Amazon SNS Push (APNs/FCM) & SMS alerts

### Slice 2 (`v2.0`): Digital Products & 6-Mode Non-Heartbeat Licensing (`US-2.1` – `US-2.2`)
- [ ] Implement `SSE-KMS` digital vault + 15-minute presigned S3 download URLs + digital VAT rules
- [ ] Implement all 6 Non-Heartbeat Licensing Modes (Offline Ed25519 `.lic`, Air-Gapped QR, CloudFront CRLs, AES-256-GCM CEK unsealing, Release-Timestamp Gating, SNS revocation)

### Slice 3 (`v3.0`): B2B Wholesale, Cross-Border Express & Durable RFQ (`US-3.1` – `US-3.4`)
- [ ] Implement B2B volume-tier contracts, MOQ enforcement, Durable RFQ negotiation saga, Aramex & DHL Express Paperless Trade plugins, and B2B LAN License Proxy

### Slice 4 (`v4.0`): Multi-Vendor Marketplace, Global Carriers & BTCPay (`US-4.1` – `US-4.3`)
- [ ] Implement Vendor RBAC isolation, atomic sub-order splitting, Shippo & EasyPost (40+ carriers), RMA return labels, Durable escrow payouts, and BTCPay Server Greenfield plugin

### Slice 5 (`v5.0`) & Slice 6 (`v6.0`): Enterprise Managed Instances & Visual SDUI Studio (`US-5.1` – `US-6.1`)
- [ ] Package AWS CDK dual editions (`ON_DEMAND` vs. `MANAGED_INSTANCES` with `MaxConcurrency: 64` + DynamoDB Zero-ETL to OpenSearch)
- [ ] Build Visual Multi-Locale SDUI Studio (`Expo DOM Components`) with simultaneous `ar-EG` (`RTL`) and `en-US` (`LTR`) preview and white-label EAS build pipeline
