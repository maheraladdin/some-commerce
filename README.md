# some-commerce

[![Sponsor maheraladdin](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/maheraladdin)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Rust: Cargo Lambda](https://img.shields.io/badge/Backend-Rust%20%2B%20Cargo%20Lambda-orange?style=for-the-badge&logo=rust)](https://www.cargo-lambda.info/)
[![Client: Universal Expo](https://img.shields.io/badge/Client-Universal%20Expo-000020?style=for-the-badge&logo=expo)](https://docs.expo.dev/)
[![AWS: 100% Native](https://img.shields.io/badge/Cloud-100%25%20AWS%20Serverless-FF9900?style=for-the-badge&logo=amazonaws)](https://aws.amazon.com/lambda/lambda-managed-instances/)

**`some-commerce`** is an open-source, 100% AWS-native **B2C & B2B Server-Driven UI (SDUI) e-commerce marketplace** for selling both **physical products** and **cryptographically licensed digital products**.

Built with a **5-binary Rust ([Axum](https://github.com/tokio-rs/axum) + [Cargo Lambda](https://www.cargo-lambda.info/)) workspace**, **[Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html)** for authentication and role/persona authorization, **[Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)** for mobile push notifications, SMS alerts, and event fan-out, **[Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/data-modeling-foundations.html)** (Single-Table Design), and a **Universal [Expo](https://docs.expo.dev/) + [Expo Router](https://docs.expo.dev/router/introduction/)** client (exported as static HTML/CSS/JS on **[Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) + [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)** and compiled natively for iOS & Android), `some-commerce` is funded slice-by-slice through **[GitHub Sponsors](https://github.com/sponsors/maheraladdin)** and packaged commercially on **[AWS Marketplace](https://aws.amazon.com/marketplace/)** in two editions:

1. **Standard Serverless Edition**: On-Demand [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-rust.html) + On-Demand DynamoDB (scales to zero when idle).
2. **Enterprise Managed Instances Edition**: [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html) backed by customer-owned EC2 Graviton Capacity Providers (zero cold starts, high-throughput multi-concurrency, and EC2 Compute Savings Plan compatibility).

## Sponsor This Project

`some-commerce` is built in **6 vertical production slices**. Every slice is unlocked and shipped as a standalone, production-ready release funded by community and commercial sponsors.

* **[Sponsor @maheraladdin on GitHub Sponsors](https://github.com/sponsors/maheraladdin)**

## Documentation Index (`docs/`)

* **[System Architecture & Dual AWS Lambda Model (`docs/SYSTEM_ARCHITECTURE.md`)](docs/SYSTEM_ARCHITECTURE.md)** — 5-binary Cargo Lambda workspace, Amazon Cognito RBAC/ABAC, Amazon SNS push/SMS notifications, DynamoDB Single-Table schema, 100% AWS S3 + CloudFront static Expo web hosting, and AWS Marketplace CDK packaging.
* **[User Stories & 12-Sprint Execution Plan (`docs/USER_STORIES_AND_SPRINTS.md`)](docs/USER_STORIES_AND_SPRINTS.md)** — Detailed user stories, acceptance criteria, and sprint goals across all 6 production slices (`v1.0` to `v6.0`).
* **[Payments, Global Shipping, Split COD & Digital Licensing (`docs/PAYMENTS_SHIPPING_AND_LICENSING.md`)](docs/PAYMENTS_SHIPPING_AND_LICENSING.md)** — KMS-encrypted vault for Paymob, Stripe, and BTCPay Server; global shipping via Bosta, Aramex, DHL Express, Shippo, and EasyPost; Upfront Deposit + Split Cash-on-Delivery (`DEPOSIT_COD`); and Ed25519 digital product licensing.
* **[Server-Driven UI (SDUI) & Localization Engine (`docs/SDUI_AND_LOCALIZATION.md`)](docs/SDUI_AND_LOCALIZATION.md)** — Universal Expo SDUI JSON schema, RTL/LTR localization (`ar-EG`, `ar-SA`, `en-US`), Cognito persona-based B2C/B2B layout switching, and localized fee matrices.

## Core Architecture Overview

| Layer | Technology | Highlights |
| :--- | :--- | :--- |
| **Auth & Authorization** | [Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) + [Pre-Token Lambda Trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html) | OIDC/PKCE auth across Web & Mobile; JWT custom claims (`tenant_id`, `persona`, `b2b_org_id`, `vendor_id`) + RBAC groups (`STORE_ADMIN`, `VENDOR`, `B2B_BUYER`, `B2C_CUSTOMER`). |
| **Notifications & Pub/Sub** | [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) ([Mobile Push](https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-application-as-subscriber.html), SMS & Topic Fan-Out) | Sends native iOS (APNs) & Android (FCM) push notifications to the Expo app, transactional SMS shipment/COD alerts, and merchant webhook/email fan-out. |
| **Backend Compute** | Rust + [Axum](https://github.com/tokio-rs/axum) + [Cargo Lambda](https://www.cargo-lambda.info/) | 5 domain-scoped binaries (`storefront-sdui-api`, `checkout-webhooks-api`, `admin-vendor-api`, `fulfillment-worker`, `durable-orchestrator`). |
| **Database & Events** | [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) + [EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-dynamodb.html) | Single-table design (`SomeCommerceTable`) with DynamoDB Streams driving async order fulfillment, SNS notifications, and license minting. |
| **Storefront & Admin** | [Expo](https://docs.expo.dev/) + [Expo Router](https://docs.expo.dev/router/introduction/) + [Expo DOM](https://docs.expo.dev/guides/dom-components/) | Single TypeScript codebase exported via `npx expo export --platform web` to S3 + CloudFront (OAC) and compiled natively to iOS & Android. |
| **Payment Gateways** | Rust `PaymentProvider` Trait + [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) | Zero-redeploy dashboard config for [Paymob](https://developers.paymob.com/paymob-docs), [Stripe](https://docs.stripe.com/api), and [BTCPay Server](https://docs.btcpayserver.org/API/Greenfield/v1/) + **Upfront Deposit on COD**. |
| **Global Delivery** | Rust `ShippingProvider` Trait + Localized Fee Engine | Pluggable adapters for [Bosta](https://docs.bosta.co/), [Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform), [DHL Express](https://developer.dhl.com/), [Shippo](https://docs.goshippo.com/), [EasyPost](https://docs.easypost.com/), and custom governorate/zone tables. |
| **Digital Licensing** | Ed25519 ([AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)) + S3 Presigned Delivery | Offline signed `.lic` certificates, online `/v1/licenses/heartbeat` verification, device seat limits, B2B floating licenses, and automatic refund revocation. |

## 6-Month Sponsor Slice & Sprint Timeline

| Slice & Release | Timeline | Sprints | Target Sponsor Milestone | Standalone Production Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Slice 1 (`v1.0`)** | Weeks 1–4 | Sprints 1.1 – 1.2 | Core B2C + MENA/Global Launch | Cognito Auth, Amazon SNS Push/SMS Alerts, Universal Expo Store (S3/CloudFront + Mobile), RTL/LTR SDUI, Governorate Fee Engine, Paymob, Stripe, Bosta & Split COD Deposit |
| **Slice 2 (`v2.0`)** | Weeks 5–8 | Sprints 2.1 – 2.2 | Digital Creators & SaaS Vendors | Digital Products, Localized Digital VAT, S3 Presigned Delivery, Ed25519 KMS Licensing & Hybrid Physical-Digital Unlock |
| **Slice 3 (`v3.0`)** | Weeks 9–12 | Sprints 3.1 – 3.2 | B2B Wholesalers & Exporters | Cognito B2B Orgs, Aramex & DHL Express Cross-Border Shipping, Customs Invoices, Volume Tiers, RFQ & Floating Seat Licenses |
| **Slice 4 (`v4.0`)** | Weeks 13–16 | Sprints 4.1 – 4.2 | Multi-Vendor & Web3 Marketplaces | Shippo & EasyPost (40+ Global Carriers), Multi-Vendor Cart Splitting, Delivery-Gated Escrow & BTCPay Server Crypto Adapter |
| **Slice 5 (`v5.0`)** | Weeks 17–20 | Sprints 5.1 – 5.2 | Enterprise & AWS Marketplace | Dual AWS CDK Stacks: Standard On-Demand Lambda vs. Hybrid AWS Lambda Managed Instances + Marketplace Metering |
| **Slice 6 (`v6.0`)** | Weeks 21–24 | Sprints 6.1 – 6.2 | Agencies & No-Code Brands | Visual Drag-and-Drop Multi-Locale SDUI Studio, Visual Fee-Zone Builder & White-Label Mobile Pipeline |

## Master Implementation Checklist

### Slice 1 (`v1.0`): Core B2C Physical Storefront, Cognito Auth, SNS Notifications, Localized SDUI, Paymob/Stripe & Bosta Split COD
- [ ] **Sprint 1.1 (Weeks 1–2): Rust Workspace, Cognito Auth, DynamoDB & Static Expo Web**
  - [ ] Initialize Cargo workspace (`crates/core-domain`, `crates/auth-cognito`, `crates/notify-sns`, `crates/db-dynamo`, `crates/sdui-schema`, `bins/*`)
  - [ ] Provision [Amazon Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html), App Clients (Web + Native), RBAC Groups (`STORE_ADMIN`, `B2C_CUSTOMER`), and Pre-Token Generation Lambda Trigger
  - [ ] Provision [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) Topics (`OrderEvents`, `ShipmentEvents`, `LicenseEvents`) and Platform Applications (APNs/FCM) for Expo push notifications and SMS alerts
  - [ ] Implement DynamoDB single-table repository (`SomeCommerceTable`) for tenants, products, localized SDUI layouts, and `LOCALE_FEES#<country>#<zone>`
  - [ ] Build Universal [Expo Router](https://docs.expo.dev/router/introduction/) app with `<SduiRenderer />` supporting RTL (`ar`) and LTR (`en`) design tokens
  - [ ] Configure [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) stack with Private S3 + CloudFront (OAC), URL-rewrite CloudFront Function, and `BucketDeployment` for `npx expo export --platform web`
- [ ] **Sprint 1.2 (Weeks 3–4): KMS Vault, Paymob/Stripe Checkout, Bosta Delivery & Split COD Deposit**
  - [ ] Implement `PaymentProvider` trait and KMS envelope encryption vault in `admin-vendor-api`
  - [ ] Build [Stripe Payment Intents](https://docs.stripe.com/api/payment_intents) adapter and [Paymob Accept](https://developers.paymob.com/paymob-docs/integration-paths/apis) adapter (Cards, Meeza, Mobile Wallets, ValU)
  - [ ] Implement `ShippingProvider` trait with `CustomZoneProvider` (governorate/city fee tables) and [Bosta API](https://docs.bosta.co/) adapter
  - [ ] Implement **Upfront COD Deposit (`DEPOSIT_COD`)** state machine (`AWAITING_COD_DEPOSIT` -> `DEPOSIT_PAID_COD_PENDING` -> Bosta `collectionAmount = total - deposit`)
  - [ ] Wire DynamoDB Streams + [EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-dynamodb.html) to `fulfillment-worker` for automatic Bosta AWB generation, live webhook tracking, and Amazon SNS customer SMS/push alerts
  - [ ] Tag and release **`v1.0.0`**

### Slice 2 (`v2.0`): Digital Products & Cryptographic Licensing Engine
- [ ] **Sprint 2.1 (Weeks 5–6): S3 Protected Delivery, Digital VAT & Ed25519 KMS Signing**
  - [ ] Add private S3 digital asset bucket and presigned download URL generator in `fulfillment-worker`
  - [ ] Provision asymmetric Ed25519 signing key in [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) and mint signed `.lic` offline certificates on `OrderPaid`
  - [ ] Add hybrid Physical + Digital bundle support (unlocking digital license and dispatching SNS push/email alert when Bosta webhook confirms physical delivery)
- [ ] **Sprint 2.2 (Weeks 7–8): Online License Heartbeat, Device Limits & Refund Revocation**
  - [ ] Implement `/v1/licenses/activate`, `/v1/licenses/verify`, and `/v1/licenses/deactivate` in `storefront-sdui-api`
  - [ ] Wire Stripe/Paymob refund webhooks and Bosta return webhooks to automatic license revocation and SNS security alerts
  - [ ] Build SDUI `CustomerLicenseVaultBlock` and publish Rust/TypeScript client verification SDKs
  - [ ] Tag and release **`v2.0.0`**

### Slice 3 (`v3.0`): B2B Wholesale, Cross-Border Express (Aramex & DHL), RFQ & Floating Seat Licenses
- [ ] **Sprint 3.1 (Weeks 9–10): Cognito B2B Orgs, Aramex + DHL Express Adapters & Landed Cost**
  - [ ] Add `B2B_ORG_ADMIN` and `B2B_BUYER` Cognito groups and inject `b2b_org_id` + `price_list_id` into JWT claims via Pre-Token Trigger
  - [ ] Build B2B SDUI components (`BulkOrderMatrix`, `TieredPriceTable`, `RfqSubmissionDrawer`)
  - [ ] Implement `AramexProvider` ([Aramex API](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform)) and `DhlExpressProvider` ([MyDHL API](https://developer.dhl.com/)) with volumetric weight, HS codes, and paperless commercial invoices
- [ ] **Sprint 3.2 (Weeks 11–12): RFQ State Machine, Milestone Deposits & B2B Seat Licensing**
  - [ ] Build Request-for-Quote (RFQ) negotiation flow with custom B2B milestone deposit percentages (e.g., 30% upfront, 70% on delivery / Net-30) and SNS quote status notifications
  - [ ] Configure `durable-orchestrator` ([AWS Lambda Durable Functions](https://aws.plainenglish.io/aws-lambda-updates-in-2025-2e664f4070d2)) to publish Net-30 invoice reminders via Amazon SNS
  - [ ] Implement multi-seat B2B floating license pools managed by `B2B_ORG_ADMIN`
  - [ ] Tag and release **`v3.0.0`**

### Slice 4 (`v4.0`): Multi-Vendor Marketplace, Shippo/EasyPost Global Shipping, Split Escrow & Crypto
- [ ] **Sprint 4.1 (Weeks 13–14): Shippo & EasyPost Aggregators + Multi-Vendor Cart Splitting**
  - [ ] Add `VENDOR` Cognito group and tenant/vendor ABAC isolation in `admin-vendor-api`
  - [ ] Implement `ShippoProvider` ([Shippo API](https://docs.goshippo.com/)) and `EasyPostProvider` ([EasyPost API](https://docs.easypost.com/)) for live 40+ carrier rate shopping
  - [ ] Implement multi-vendor cart splitting, proportional COD deposit allocation, per-vendor pickup dispatch, and vendor SNS new-order alerts
- [ ] **Sprint 4.2 (Weeks 15–16): BTCPay Server Crypto Adapter & Delivery-Gated Escrow**
  - [ ] Implement `BtcpayProvider` ([BTCPay Greenfield API](https://docs.btcpayserver.org/API/Greenfield/v1/)) for Bitcoin, Lightning, and stablecoin checkout
  - [ ] Wire `durable-orchestrator` to release vendor escrow payouts N days after carrier `Delivered` webhook confirmation and notify vendors via SNS
  - [ ] Build SDUI Vendor Portal for order, license, AWB label, and payout management
  - [ ] Tag and release **`v4.0.0`**

### Slice 5 (`v5.0`): Dual AWS Marketplace Editions — Standard Lambda vs. AWS Lambda Managed Instances
- [ ] **Sprint 5.1 (Weeks 17–18): Multi-Concurrency Stress Testing & Dual CDK Stacks**
  - [ ] Benchmark `storefront-sdui-api` and `checkout-webhooks-api` under multi-concurrent load on [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html)
  - [ ] Package CDK Stack A (Standard On-Demand Serverless) and CDK Stack B (Hybrid EC2 Graviton Capacity Provider + Managed Instances)
- [ ] **Sprint 5.2 (Weeks 19–20): AWS Marketplace Metering & Foundational Technical Review (FTR)**
  - [ ] Integrate AWS Marketplace Metering & Entitlement APIs
  - [ ] Complete AWS CloudFormation security/IAM audit and publish **`v5.0.0`**

### Slice 6 (`v6.0`): Visual Localized SDUI Studio, Fee-Zone Map Builder & White-Label Mobile Pipeline
- [ ] **Sprint 6.1 (Weeks 21–22): Visual Drag-and-Drop SDUI Studio & Regional Fee Matrix UI**
  - [ ] Build visual drag-and-drop SDUI editor in Expo Admin using [Expo DOM Components](https://docs.expo.dev/guides/dom-components/) with RTL/LTR & Web/iOS/Android viewport preview
  - [ ] Build visual regional fee-zone and carrier routing rule builder with automatic CloudFront cache invalidation
- [ ] **Sprint 6.2 (Weeks 23–24): White-Label Mobile CI/CD & v6.0 Launch**
  - [ ] Create white-label EAS / AWS CodeBuild pipeline for compiling tenant-branded iOS & Android apps
  - [ ] Add edge SEO OpenGraph meta-tag injection for localized product routes (`/ar/products/*`, `/en/products/*`)
  - [ ] Tag and release **`v6.0.0`**

## License

Released under the [MIT License](LICENSE). Sponsored and maintained by [@maheraladdin](https://github.com/maheraladdin).
