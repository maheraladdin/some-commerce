# User Stories & 12-Sprint Execution Plan (Slices 1–6)

Each vertical slice is a **4-week milestone (two 2-week sprints)** funded via [GitHub Sponsors](https://github.com/sponsors/maheraladdin). Every slice ships a complete, deployable production release.

## Slice 1 (`v1.0` — Weeks 1–4): Core B2C Storefront, Amazon Cognito Auth, Amazon SNS Alerts, Localized SDUI, Paymob/Stripe & Bosta Split COD

### User Stories & Acceptance Criteria
* **US-1.1: Amazon Cognito Authentication & Role Guarding**
  * *As a* shopper or store administrator on Web, iOS, or Android,
  * *I want* to sign up and sign in via [Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) (Email, Phone OTP, or Social OIDC) with automatic role assignment (`STORE_ADMIN` vs. `B2C_CUSTOMER`),
  * *So that* my session is cryptographically verified across all `/v1/*` Rust Lambda endpoints.
* **US-1.2: Locale & Direction-Aware SDUI Storefront (`RTL` / `LTR`)**
  * *As a* shopper visiting from Egypt/MENA or internationally,
  * *I want* the static Expo web shell (hosted on S3 + CloudFront) and mobile app to render localized SDUI JSON schemas (`direction: "rtl"` for Arabic, `direction: "ltr"` for English),
  * *So that* store layouts, banners, and checkout forms adapt to my language and region without redeploying the frontend.
* **US-1.3: Localized Governorate/Zone Fee Engine**
  * *As a* store admin,
  * *I want* to define shipping base fees, per-kg weight tiers, VAT %, free-shipping thresholds, and COD surcharges per country and governorate/city (`LOCALE_FEES#<country>#<zone>`),
  * *So that* checkout calculates accurate regional delivery charges (e.g., Cairo/Giza vs. Mansoura/Dakahlia vs. Alexandria).
* **US-1.4: KMS Vault, Split COD Deposit & Amazon SNS Customer Alerts**
  * *As a* store admin,
  * *I want* to configure [Paymob](https://developers.paymob.com/paymob-docs), [Stripe](https://docs.stripe.com/api), and [Bosta](https://docs.bosta.co/) API credentials in the dashboard, require an **Upfront COD Deposit** before dispatching a Cash-on-Delivery order, and automatically notify customers via **[Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)** (Mobile Push & SMS) when their order is confirmed or out for delivery.

### Sprint Breakdown (Slice 1)
* **Sprint 1.1 (Weeks 1–2)**: Scaffold the 5-binary Cargo Lambda workspace, provision Amazon Cognito + Pre-Token Trigger and Amazon SNS Topics/Push Applications, implement DynamoDB single-table models (`METADATA`, `PRODUCT`, `SDUI`, `LOCALE_FEES`), build the Universal Expo SDUI renderer, and deploy static web assets to S3 + CloudFront via AWS CDK `BucketDeployment`.
* **Sprint 1.2 (Weeks 3–4)**: Build the KMS secret vault, implement `StripeProvider`, `PaymobProvider`, `CustomZoneProvider`, and `BostaProvider`, implement the Split COD state machine (`AWAITING_COD_DEPOSIT` -> `DEPOSIT_PAID_COD_PENDING` -> `DELIVERED` / `RTO_RETURNED`) with SNS push/SMS notifications, and cut release **`v1.0.0`**.

## Slice 2 (`v2.0` — Weeks 5–8): Digital Products & Cryptographic Licensing Engine

### User Stories & Acceptance Criteria
* **US-2.1: Protected S3 Digital Asset Delivery & Localized Digital VAT**
  * *As a* digital creator selling software, e-books, or assets,
  * *I want* files stored in a private S3 bucket and served via short-lived presigned URLs only after payment verification, with automatic buyer-country digital VAT calculation.
* **US-2.2: Ed25519 Offline & Online License Issuance + Hybrid Unlock**
  * *As a* buyer of a digital product or a physical+digital hardware bundle,
  * *I want* an Ed25519-signed `.lic` certificate minted via [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) immediately upon digital payment—or unlocked automatically (with an SNS push/SMS notification) when Bosta's webhook confirms delivery of the companion physical hardware.
* **US-2.3: Hardware Fingerprint Activation, Heartbeat & Refund Revocation**
  * *As a* software vendor,
  * *I want* `/v1/licenses/activate` and `/v1/licenses/verify` endpoints that enforce maximum machine activations per license key and automatically revoke keys if a Stripe/Paymob refund or carrier return webhook fires.

### Sprint Breakdown (Slice 2)
* **Sprint 2.1 (Weeks 5–6)**: Implement S3 presigned asset delivery, multi-currency digital VAT rules, and AWS KMS Ed25519 signing in `fulfillment-worker`.
* **Sprint 2.2 (Weeks 7–8)**: Build low-latency license activation/heartbeat routes in `storefront-sdui-api`, connect refund/return webhooks to license revocation and SNS security alerts, build the SDUI `CustomerLicenseVaultBlock`, publish Rust/JS verification SDKs, and release **`v2.0.0`**.

## Slice 3 (`v3.0` — Weeks 9–12): B2B Wholesale, Cross-Border Express (Aramex & DHL), RFQ & Floating Seat Licenses

### User Stories & Acceptance Criteria
* **US-3.1: Cognito B2B Persona & Wholesale SDUI Switching**
  * *As a* verified wholesale buyer (`cognito:groups = ["B2B_BUYER"]`),
  * *I want* the Cognito Pre-Token Trigger to inject `custom:persona = "B2B"` and `custom:price_list_id` into my JWT so `storefront-sdui-api` automatically renders bulk SKU matrices, MOQ rules, and tiered volume pricing.
* **US-3.2: Cross-Border Shipping via Aramex & DHL Express**
  * *As a* merchant shipping across MENA, GCC, and globally,
  * *I want* to configure [Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) and [DHL Express MyDHL API](https://developer.dhl.com/api-reference/dhl-express-mydhl-api?language_content_entity=en) keys in the dashboard to calculate volumetric air/road rates, customs duties, and generate paperless commercial invoices.
* **US-3.3: B2B Request-for-Quote (RFQ) & Milestone Deposits**
  * *As a* wholesale buyer,
  * *I want* to submit an RFQ from my cart, negotiate custom line-item prices and milestone deposits (e.g., 30% upfront deposit via Paymob/Stripe, 70% on delivery or Net-30), and receive automated Net-30 reminders via `durable-orchestrator` and Amazon SNS.
* **US-3.4: B2B Floating & Multi-Seat Digital Licenses**
  * *As a* `B2B_ORG_ADMIN`,
  * *I want* to manage a multi-seat organization license pool where I can assign, revoke, or float software seats across employees in my Cognito organization.

### Sprint Breakdown (Slice 3)
* **Sprint 3.1 (Weeks 9–10)**: Add B2B Cognito groups and organization onboarding, build `AramexProvider` and `DhlExpressProvider` with customs invoice generation, and implement B2B SDUI components.
* **Sprint 3.2 (Weeks 11–12)**: Build the RFQ negotiation state machine, wire `durable-orchestrator` ([AWS Lambda Durable Functions](https://aws.plainenglish.io/aws-lambda-updates-in-2025-2e664f4070d2)) + Amazon SNS for Net-30 timers, add floating seat licensing, and release **`v3.0.0`**.

## Slice 4 (`v4.0` — Weeks 13–16): Multi-Vendor Marketplace, Shippo/EasyPost Global Aggregators, Split Escrow & Crypto

### User Stories & Acceptance Criteria
* **US-4.1: Global Multi-Carrier Rate Shopping via Shippo & EasyPost**
  * *As a* global shopper in North America, Europe, UK, or MENA,
  * *I want* checkout to query [Shippo](https://docs.goshippo.com/) and [EasyPost](https://docs.easypost.com/) alongside regional carriers so I can compare live Economy vs. Express rates across 40+ carriers (USPS, UPS, FedEx, Royal Mail, DHL, Bosta, Aramex).
* **US-4.2: Multi-Vendor Cart Splitting, Origin Dispatch & Vendor SNS Alerts**
  * *As a* marketplace operator,
  * *I want* a multi-vendor cart to split into vendor-scoped sub-orders (`VENDOR#<vendor_id>`), allocating upfront COD deposits proportionally, booking pickups from each seller's warehouse address, and notifying each vendor immediately via Amazon SNS push/SMS.
* **US-4.3: Pluggable Crypto Checkout ([BTCPay Server](https://docs.btcpayserver.org/API/Greenfield/v1/)) & Delivery-Gated Escrow**
  * *As a* marketplace seller authenticated with the `VENDOR` Cognito role,
  * *I want* customer payments (via Stripe, Paymob, or BTCPay Bitcoin/Lightning/USDT) held in escrow and released automatically by `durable-orchestrator` N days after the carrier webhook confirms delivery.

### Sprint Breakdown (Slice 4)
* **Sprint 4.1 (Weeks 13–14)**: Add `VENDOR` Cognito RBAC isolation, implement `ShippoProvider` and `EasyPostProvider`, and build multi-vendor cart/deposit splitting with vendor SNS alerts.
* **Sprint 4.2 (Weeks 15–16)**: Implement `BtcpayProvider`, wire delivery-gated escrow payouts in `durable-orchestrator`, build the SDUI Vendor Dashboard, and release **`v4.0.0`**.

## Slice 5 (`v5.0` — Weeks 17–20): Dual AWS Marketplace Editions — Standard Lambda vs. AWS Lambda Managed Instances

### User Stories & Acceptance Criteria
* **US-5.1: Standard On-Demand Serverless Marketplace Stack**
  * *As a* startup buyer on AWS Marketplace,
  * *I want* a 1-click CloudFormation template that deploys all 5 Rust Lambdas on standard On-Demand AWS Lambda + On-Demand DynamoDB for zero idle cost.
* **US-5.2: Hybrid Enterprise AWS Lambda Managed Instances Stack**
  * *As an* enterprise buyer with high sustained traffic,
  * *I want* `storefront-sdui-api` and `checkout-webhooks-api` deployed on [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html) backed by Graviton EC2 Capacity Providers for zero cold starts, multi-concurrency, and EC2 Savings Plan discounts.

### Sprint Breakdown (Slice 5)
* **Sprint 5.1 (Weeks 17–18)**: Stress-test multi-concurrency under `tokio`/`axum`, tune DynamoDB/KMS client pooling, and author the dual AWS CDK Marketplace stacks.
* **Sprint 5.2 (Weeks 19–20)**: Integrate AWS Marketplace Metering & Entitlement APIs, complete AWS Foundational Technical Review (FTR) checks, and release **`v5.0.0`**.

## Slice 6 (`v6.0` — Weeks 21–24): Visual Localized SDUI Studio, Fee-Zone Builder & White-Label Mobile Pipeline

### User Stories & Acceptance Criteria
* **US-6.1: Drag-and-Drop Localized SDUI Studio (`"use dom"`)**
  * *As a* store admin,
  * *I want* a visual drag-and-drop SDUI editor inside the static Expo Admin app (built with [Expo DOM Components](https://docs.expo.dev/guides/dom-components/)) to design Arabic RTL and English LTR layouts, preview across Web/iOS/Android viewports, and publish with instant CloudFront invalidation.
* **US-6.2: Visual Regional Fee, Tax & Carrier Routing Builder**
  * *As a* store admin,
  * *I want* a visual map/matrix editor to assign countries, governorates, and postal prefixes to specific carriers, custom surcharges, and Split COD deposit rules.
* **US-6.3: White-Label Mobile CI/CD Pipeline**
  * *As a* commercial agency or sponsor,
  * *I want* an automated EAS / AWS CodeBuild template that compiles branded iOS and Android apps connected to my tenant's Cognito User Pool, SNS Push Platform Application, and SDUI endpoint.

### Sprint Breakdown (Slice 6)
* **Sprint 6.1 (Weeks 21–22)**: Build the visual SDUI studio and regional fee-zone matrix editor using Expo DOM components and wire CloudFront invalidations.
* **Sprint 6.2 (Weeks 23–24)**: Build the white-label mobile build pipeline, add edge SEO OpenGraph meta injection for localized product URLs, and launch **`v6.0.0`**.
