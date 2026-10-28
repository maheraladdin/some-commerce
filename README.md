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

## Master Implementation Checklist

### Slice 1 (`v1.0`): Core B2C Storefront, Cognito Auth, Unlimited N-Level Categories, Dynamic Product Properties, Elasticsearch + General Filtration, Paymob/Stripe & Bosta Split COD
- [ ] **Sprint 1.1 (Weeks 1–2): Rust Workspace, Cognito Auth, Dynamic Taxonomy/Properties, Elasticsearch + General Filtration & Static Expo Web**
  - [ ] Initialize Cargo workspace (`crates/core-domain`, `crates/auth-cognito`, `crates/i18n-engine`, `crates/search-elastic`, `crates/notify-sns`, `crates/db-dynamo`, `crates/sdui-schema`, `bins/*`)
  - [ ] Provision [Amazon Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html), App Clients (Web + Native), RBAC Groups (`STORE_ADMIN`, `B2C_CUSTOMER`), and Pre-Token Generation Lambda Trigger
  - [ ] Implement DynamoDB single-table repository (`SomeCommerceTable`) for **Unlimited N-Level Categories** (`TAXONOMY_NODE#<node_id>`, `ancestors_path[]`), **User-Customizable Product Properties** (`PROPERTY_DEF#<prop_code>`), **Brands** (`BRAND#<brand_id>`), multilingual products, and `LOCALE_FEES#<country>#<zone>`
  - [ ] Implement `CatalogSearchProvider` trait in `crates/search-elastic` supporting **Tier 1 General Filtration** (DynamoDB GSIs + FilterExpressions) and **Tier 2 Elasticsearch / OpenSearch Faceted Filtration** ([Nested Aggregations](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-nested-aggregation) over arbitrary merchant-defined `properties[]` and N-level category trees)
  - [ ] Build Universal [Expo Router](https://docs.expo.dev/router/introduction/) + [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/) app with `<SduiRenderer />`, `SearchFacetFilterBlock` (rendering `COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`), `CategoryTreeDrawer`, and `BrandPillSelector`
  - [ ] Configure [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) stack with Private S3 + CloudFront (OAC), URL-rewrite CloudFront Function (`/[locale]/products/[slug]`), and `BucketDeployment` for `npx expo export --platform web`
- [ ] **Sprint 1.2 (Weeks 3–4): KMS Vault, Real-Time Elasticsearch Sync, Paymob/Stripe Checkout, Bosta Delivery & Split COD Deposit**
  - [ ] Implement `PaymentProvider` trait and KMS envelope encryption vault in `admin-vendor-api` (storing Paymob, Stripe, Bosta, and external Elasticsearch credentials)
  - [ ] Wire DynamoDB Streams + [EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-dynamodb.html) to `fulfillment-worker` for real-time `/_bulk` Elasticsearch indexing, automatic Bosta AWB generation, and localized [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) SMS/push alerts
  - [ ] Build [Stripe Payment Intents](https://docs.stripe.com/api/payment_intents) adapter and [Paymob Accept](https://developers.paymob.com/paymob-docs/integration-paths/apis) adapter
  - [ ] Implement `ShippingProvider` trait with `CustomZoneProvider` and [Bosta API](https://docs.bosta.co/) adapter
  - [ ] Implement **Upfront COD Deposit (`DEPOSIT_COD`)** state machine (`AWAITING_COD_DEPOSIT` -> `DEPOSIT_PAID_COD_PENDING` -> Bosta `collectionAmount = total - deposit`)
  - [ ] Tag and release **`v1.0.0`**

### Slice 2 (`v2.0`): Digital Products & 6-Mode Cryptographic Licensing Engine
- [ ] **Sprint 2.1 (Weeks 5–6): S3 Protected Delivery, Offline Ed25519 `.lic` Signing, CEK Envelope Encryption & Release-Timestamp Gating**
  - [ ] Support custom digital product properties (`OS Platform`, `File Format`, `Engine Version`, `License Verification Mode`) in Elasticsearch and DynamoDB General Filtration
  - [ ] Provision asymmetric Ed25519 signing key in [AWS KMS](https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html) and mint offline-verifiable `.lic` certificates (Mode 1) and release-timestamp gated certificates (Mode 5)
  - [ ] Implement AES-256-GCM Content Encryption Key (CEK) wrapping via X25519 key exchange (Mode 4) for anti-tamper asset decryption
  - [ ] Add hybrid Physical + Digital bundle support (unlocking digital license when Bosta webhook confirms physical delivery)
- [ ] **Sprint 2.2 (Weeks 7–8): Air-Gapped QR Challenge-Response, CloudFront Signed CRLs/Bloom Filters & Refund Revocation**
  - [ ] Implement Air-Gapped Challenge-Response `.req` / Mobile QR scanner activation endpoint (`/v1/licenses/challenge-activate` — Mode 2)
  - [ ] Implement automated S3 + CloudFront signed Revocation List / Bloom Filter publishing (`revoked.crl.bin` — Mode 3) and SNS silent push revocation (Mode 6) when Stripe/Paymob refund or Bosta return webhooks fire
  - [ ] Build localized SDUI `CustomerLicenseVaultBlock` (including QR scanner for offline device pairing) and publish Rust/TypeScript client verification SDKs
  - [ ] Tag and release **`v2.0.0`**

### Slice 3 (`v3.0`): B2B Wholesale, Cross-Border Express (Aramex & DHL), RFQ & B2B On-Premise License Proxy
- [ ] **Sprint 3.1 (Weeks 9–10): Cognito B2B Orgs, B2B Custom Property/MOQ Filtration, Aramex + DHL Express Adapters**
  - [ ] Add `B2B_ORG_ADMIN` and `B2B_BUYER` Cognito groups and B2B Elasticsearch facets (`moq_range`, `b2b_tier_price`, `authorized_distributor_brands`)
  - [ ] Build multilingual B2B SDUI components (`BulkOrderMatrix` across dynamic variant axes, `TieredPriceTable`, `RfqSubmissionDrawer`)
  - [ ] Implement `AramexProvider` ([Aramex API](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform)) and `DhlExpressProvider` ([MyDHL API](https://developer.dhl.com/)) with volumetric weight, HS codes, and bilingual (`ar` + `en`) commercial invoices
- [ ] **Sprint 3.2 (Weeks 11–12): RFQ State Machine, Milestone Deposits & B2B On-Premise License Server**
  - [ ] Build Request-for-Quote (RFQ) negotiation flow with custom B2B milestone deposit percentages (e.g., 30% upfront, 70% on delivery / Net-30)
  - [ ] Configure `durable-orchestrator` ([AWS Lambda Durable Functions](https://aws.plainenglish.io/aws-lambda-updates-in-2025-2e664f4070d2)) to publish localized Net-30 invoice reminders via Amazon SNS
  - [ ] Ship lightweight `some-commerce-license-proxy` Docker image for B2B LAN multi-seat management (Mode 6)
  - [ ] Tag and release **`v3.0.0`**

### Slice 4 (`v4.0`): Multi-Vendor Marketplace, Shippo/EasyPost Global Shipping, Split Escrow & Crypto
- [ ] **Sprint 4.1 (Weeks 13–14): Shippo & EasyPost Aggregators + Multi-Vendor Cart Splitting**
  - [ ] Add `VENDOR` Cognito group, vendor custom property proposals, and tenant/vendor ABAC isolation in `admin-vendor-api`
  - [ ] Implement `ShippoProvider` ([Shippo API](https://docs.goshippo.com/)) and `EasyPostProvider` ([EasyPost API](https://docs.easypost.com/)) for live 40+ carrier rate shopping
  - [ ] Implement multi-vendor cart splitting, proportional COD deposit allocation, per-vendor pickup dispatch, and localized vendor SNS alerts
- [ ] **Sprint 4.2 (Weeks 15–16): BTCPay Server Crypto Adapter & Delivery-Gated Escrow**
  - [ ] Implement `BtcpayProvider` ([BTCPay Greenfield API](https://docs.btcpayserver.org/API/Greenfield/v1/)) for Bitcoin, Lightning, and stablecoin checkout
  - [ ] Wire `durable-orchestrator` to release vendor escrow payouts N days after carrier `Delivered` webhook confirmation
  - [ ] Build multilingual SDUI Vendor Portal and tag **`v4.0.0`**

### Slice 5 (`v5.0`): Dual AWS Marketplace Editions — Standard Lambda vs. AWS Lambda Managed Instances
- [ ] **Sprint 5.1 (Weeks 17–18): Multi-Concurrency Stress Testing, OpenSearch Zero-ETL & Dual CDK Stacks**
  - [ ] Benchmark `storefront-sdui-api` and `checkout-webhooks-api` under multi-concurrent load on [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html)
  - [ ] Package CDK Stack A (Standard On-Demand Serverless) and CDK Stack B (Hybrid EC2 Graviton Capacity Provider + Managed Instances + [Amazon OpenSearch Zero-ETL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/OpenSearchIngestionForDynamoDB.html))
- [ ] **Sprint 5.2 (Weeks 19–20): AWS Marketplace Metering & Foundational Technical Review (FTR)**
  - [ ] Integrate AWS Marketplace Metering & Entitlement APIs and publish **`v5.0.0`**

### Slice 6 (`v6.0`): Visual Multilingual SDUI Studio, Dynamic Property/Taxonomy Studio & White-Label Mobile Pipeline
- [ ] **Sprint 6.1 (Weeks 21–22): Visual Drag-and-Drop SDUI Studio, N-Level Taxonomy/Property Designer & Regional Fee Matrix UI**
  - [ ] Build visual drag-and-drop SDUI editor, visual N-level Category/Brand tree manager, and custom Product Property & Filter Widget designer in Expo Admin using [Expo DOM Components](https://docs.expo.dev/guides/dom-components/)
- [ ] **Sprint 6.2 (Weeks 23–24): White-Label Mobile CI/CD & v6.0 Launch**
  - [ ] Create white-label EAS / AWS CodeBuild pipeline for compiling tenant-branded iOS & Android apps
  - [ ] Add edge SEO OpenGraph + `hreflang` meta-tag injection for localized category, brand, and product routes
  - [ ] Tag and release **`v6.0.0`**

## License

Released under the [MIT License](LICENSE). Sponsored and maintained by [@maheraladdin](https://github.com/maheraladdin).
