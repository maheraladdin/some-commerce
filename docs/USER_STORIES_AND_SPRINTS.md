# Deep Engineering User Stories & 12-Sprint Execution Plan (Slices 1–6)

Each vertical slice is a **4-week milestone (two 2-week sprints)** funded via [GitHub Sponsors](https://github.com/sponsors/maheraladdin). Every slice ships a standalone, deployable production release across static AWS Web ([Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) + [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)), iOS, and Android via [Expo](https://docs.expo.dev/).

Every user story below includes its **Cognito Persona/Roles**, **Multilingual & RTL/LTR Requirements**, **Target Rust Lambda Binary & API Contract**, **DynamoDB / Elasticsearch Access Pattern**, and **Given/When/Then Acceptance Criteria & Edge Cases**.

## Slice 1 (`v1.0` — Weeks 1–4): Core B2C Storefront, Amazon Cognito Auth, Unlimited N-Level Categories, Dynamic Product Properties, Elasticsearch + General Filtration, Paymob/Stripe, Bosta & Split COD

### US-1.1: Amazon Cognito OIDC/PKCE Authentication, Phone OTP & Pre-Token Persona/Locale Injection
* **Actors & Cognito Roles**: `ANONYMOUS`, `B2C_CUSTOMER`, `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* shopper or store administrator on Web, iOS, or Android,
  * *I want* to register and sign in using [Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) (Email/Password, Phone SMS OTP, Passkeys, or Social OAuth) and have my preferred language, tenant ID, and role injected into my JWT claims via a [Pre-Token Generation Lambda Trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html),
  * *So that* every API call is cryptographically authenticated, authorized, and localized without extra database lookups.
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** an unauthenticated mobile shopper in Egypt (`+2010...`) signing up via Phone OTP with device locale `ar-EG`, **When** Cognito invokes the Custom SMS and Pre-Token triggers, **Then** the user receives an Arabic OTP SMS via [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) and obtains an RS256 JWT containing `"custom:persona": "B2C"` and `"custom:preferred_locale": "ar-EG"`.
  2. **Given** a non-admin customer holding `cognito:groups = ["B2C_CUSTOMER"]`, **When** they call `POST /v1/admin/products` on `admin-vendor-api` with `Accept-Language: ar-EG`, **Then** the `crates/auth-cognito` Tower middleware rejects the request in `<1ms` with HTTP `403 Forbidden` and localized JSON error `{"code": "FORBIDDEN_ROLE", "user_message": "عفواً، لا تملك صلاحية الوصول لإدارة المتجر"}`.

### US-1.2: Multilingual & Direction-Aware (`RTL` / `LTR`) Universal Expo SDUI Engine
* **Actors & Cognito Roles**: `ANONYMOUS`, `B2C_CUSTOMER`, `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* shopper on static Web (S3 + CloudFront), iOS, or Android,
  * *I want* the storefront to resolve Server-Driven UI (SDUI) layouts in my active language with automatic Right-to-Left (`RTL`) or Left-to-Right (`LTR`) layout mirroring, localized typography tokens, and localized SEO metadata,
  * *So that* the storefront renders natively in Arabic, English, French, German, or any tenant-configured language without redeploying the frontend.

### US-1.3: Unlimited N-Level Dynamic Category Trees, Brands & User-Customizable Product Properties (`PROPERTY_DEF`)
* **Actors & Cognito Roles**: `STORE_ADMIN`, `VENDOR`, `B2C_CUSTOMER`, `ANONYMOUS`
* **User Story Narrative**:
  * *As a* store admin or vendor,
  * *I want* to create an **unlimited N-level category hierarchy** (`Level 0 -> Level 1 -> Level 2 -> ... -> Level N`, e.g., `Electronics -> Computers -> Laptops -> Gaming Laptops -> RTX 40-Series`), manage **Brands** (`BRAND#<brand_id>`), and define **fully customizable Product Properties** (`PROPERTY_DEF#<prop_id>` such as `Color`, `Size`, `RAM`, `Fabric`, `Voltage`, `Author`, or any custom property on a category or directly on an individual product) with configurable data types (`ENUM_SINGLE`, `ENUM_MULTI`, `COLOR_SWATCH`, `NUMERIC_UNIT`, `BOOLEAN`, `TEXT_LOCALIZED`), variant-axis flags (`is_variant_axis`), and filter UI widgets (`CHECKBOX_LIST`, `COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `PILL_TAGS`, `TOGGLE_SWITCH`),
  * *So that* I can sell any type of physical or digital product with zero hardcoded schema limits, inherit properties automatically down N-level category trees, and override or add custom properties per product as I wish.

### US-1.4: Dual-Tier Product Filtration — General DynamoDB Filtration & Elasticsearch Dynamic Property/Taxonomy Faceted Search (`crates/search-elastic`)
* **Actors & Cognito Roles**: `ANONYMOUS`, `B2C_CUSTOMER`, `B2B_BUYER`, `STORE_ADMIN`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* shopper on Web, iOS, or Android,
  * *I want* to filter and search products using both **General Filtration** (any N-level Category/Sub-Category node, Brand, Price Range, In-Stock Only, On-Sale, Product Type `PHYSICAL`/`DIGITAL`, COD Eligibility, Minimum Rating, Sort Order) and **Advanced [Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) Dynamic Property Filtration** (multilingual full-text search with Arabic/English stemming and typo tolerance, plus [Nested Aggregations](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-nested-aggregation) over arbitrary merchant-defined `properties[]`—whether enum strings, color swatches, booleans, or numeric ranges),
  * *So that* the SDUI `SearchFacetFilterBlock` automatically renders the exact filter widgets (`COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `TOGGLE_SWITCH`) configured by the merchant with live product counts.

### US-1.5: Localized Governorate/Zone Fee Matrix & KMS-Encrypted Vault (Paymob, Stripe, Bosta & Elasticsearch)
* **Actors & Cognito Roles**: `STORE_ADMIN`, `checkout-webhooks-api`
* **User Story Narrative**:
  * *As a* store admin,
  * *I want* to store encrypted API credentials for [Paymob](https://developers.paymob.com/paymob-docs), [Stripe](https://docs.stripe.com/api), [Bosta](https://docs.bosta.co/), and external [Elasticsearch](https://www.elastic.co/) clusters in the dashboard alongside a **Localized Fee & Tax Matrix** (`LOCALE_FEES#<country>#<zone>`) with multilingual zone names (e.g., `"الدقهلية - المنصورة"` / `"Dakahlia - Mansoura"`), weight brackets, VAT %, and COD surcharges.

### US-1.6: Anti-RTO Upfront Deposit + Split Cash on Delivery (`DEPOSIT_COD`), Bosta AWB Dispatch & Multilingual SNS Alerts
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `STORE_ADMIN`, `checkout-webhooks-api`, `fulfillment-worker`, `durable-orchestrator`
* **User Story Narrative**:
  * *As a* merchant offering Cash on Delivery via [Bosta](https://docs.bosta.co/),
  * *I want* to require a configurable **Upfront COD Deposit** (`SHIPPING_FEE_ONLY`, `PERCENTAGE`, or `FIXED_AMOUNT`) paid online via [Paymob](https://developers.paymob.com/paymob-docs) or [Stripe](https://docs.stripe.com/api) before dispatching the order, and automatically book the remaining balance (`total - deposit`) as `collectionAmount` on Bosta with multilingual [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) SMS and Mobile Push notifications.

## Slice 2 (`v2.0` — Weeks 5–8): Digital Products & 6-Mode Non-Heartbeat Cryptographic Licensing Engine

### US-2.1: Multilingual Digital Catalog, Custom Digital Properties, Buyer-Country VAT & S3 Presigned Delivery
* **Actors & Cognito Roles**: `STORE_ADMIN`, `B2C_CUSTOMER`
* **User Story Narrative**:
  * *As a* digital creator selling software, plugins, or e-books globally,
  * *I want* to attach custom digital properties (`OS Platform`, `Architecture`, `File Format`, `Engine Version`, `License Verification Mode`) to my digital products for faceted filtering in Elasticsearch/DynamoDB, omit physical shipping fees at checkout, apply buyer-country digital VAT automatically, and deliver files via expiring 15-minute S3 presigned URLs.

### US-2.2: Offline Ed25519 Signed Certificates (`Mode 1`), AES-256-GCM Content Key Unsealing (`Mode 4`) & Release-Timestamp Gating (`Mode 5`)
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `STORE_ADMIN`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* digital creator or software vendor who wants **$0 ongoing Lambda/DynamoDB polling costs** and full offline usability,
  * *I want* `fulfillment-worker` to mint an offline-verifiable `.lic` certificate signed by an [AWS KMS](https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html) asymmetric **[Ed25519 (RFC 8032)](https://www.rfc-editor.org/info/rfc8032/)** private key (`Mode 1`), optionally wrap an **AES-256-GCM Content Encryption Key (CEK)** to the buyer's X25519 device public key so encrypted pro modules/assets cannot be unlocked by binary patching (`Mode 4`), and embed an `updates_entitled_until` timestamp so the client app locally verifies `release_published_at <= updates_entitled_until` without ever calling home during daily usage (`Mode 5`).
* **Target Lambda & API Contract**:
  * `fulfillment-worker`: Invokes `kms:Sign` (`SigningAlgorithm::Ed25519Sha512`) over canonical JSON `{ license_key, tenant_id, product_id, customer_sub, verification_mode, updates_entitled_until, issued_at, expires_at, entitlements[] }`.
  * `storefront-sdui-api`: `POST /v1/licenses/unseal-cek` (one-time X25519 key exchange returning the wrapped AES-256-GCM Content Encryption Key for `Mode 4`), `POST /v1/licenses/download-release/{version}` (verifies `release.published_at <= license.updates_entitled_until` for `Mode 5`).
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a buyer with a `Mode 1` + `Mode 5` `.lic` certificate whose `updates_entitled_until` is `2027-06-01`, **When** they run software release `v2.1.0` (published `2027-03-15`) completely offline on an air-gapped laptop, **Then** the embedded 32-byte Ed25519 public key verifies the `.lic` signature and release timestamp locally in `<1ms` with zero network requests.
  2. **Given** an encrypted AI model or VST plugin protected by `Mode 4` (AES-256-GCM CEK), **When** an attacker patches out boolean checks in the client binary without possessing a valid KMS-issued X25519-wrapped CEK, **Then** the encrypted asset payload remains mathematically undecryptable.

### US-2.3: Air-Gapped Challenge-Response / Mobile QR Hardware Activation (`Mode 2`) & CloudFront Edge-Cached Revocation Lists (`Mode 3`)
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `B2B_BUYER`, Client Software SDK, `storefront-sdui-api`, `checkout-webhooks-api`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* software vendor protecting against both offline machine cloning and payment refunds/chargebacks **without periodic online heartbeating**,
  * *I want* offline target machines to generate a hardware-fingerprint challenge QR code (or `.req` file) that the buyer scans once using the `some-commerce` [Expo](https://docs.expo.dev/) mobile app to receive a hardware-locked `.cert` file (`Mode 2`), and I want `fulfillment-worker` to publish a compact, Ed25519-signed **Certificate Revocation List / Bloom Filter (`revoked.crl.bin` — [RFC 5280](https://www.rfc-editor.org/info/rfc5280/))** to [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) + [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html) whenever a Stripe/Paymob refund or [Bosta](https://docs.bosta.co/) return occurs (`Mode 3`).
* **Target Lambda & API Contract**:
  * `storefront-sdui-api`: `POST /v1/licenses/challenge-activate` (accepts `{ license_key, machine_fingerprint_sha256, challenge_nonce }`, enforces `size(active_machines) < max_activations` in DynamoDB, and returns an AWS KMS Ed25519-signed `.cert` bound to `machine_fingerprint_sha256` + `challenge_nonce`).
  * CloudFront Static Edge Endpoint: `GET /crl/{tenant_id}/revoked.crl.bin` (served directly from S3 via CloudFront OAC with `Cache-Control: public, max-age=3600`—zero Lambda or DynamoDB invocations).
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** an air-gapped industrial PC displaying a `Mode 2` activation QR code containing its hardware fingerprint and nonce, **When** the buyer scans the QR code inside `CustomerLicenseVaultBlock` on their Expo mobile app, **Then** `/v1/licenses/challenge-activate` registers the seat in DynamoDB and displays a response QR code / downloadable `.cert` that permanently activates that exact PC offline.
  2. **Given** a Stripe/Paymob refund webhook or Bosta `Returned to Business` webhook for an order, **When** `checkout-webhooks-api` revokes the license in DynamoDB, **Then** `fulfillment-worker` updates the signed `revoked.crl.bin` Bloom filter in S3 and dispatches an [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) silent push notification (`Mode 6`), revoking the license across online clients without requiring heartbeat polling.

## Slice 3 (`v3.0` — Weeks 9–12): B2B Wholesale, Cross-Border Express ([Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) & [DHL Express](https://developer.dhl.com/)), RFQ & B2B On-Premise License Proxy

### US-3.1: Cognito B2B Organization Onboarding, B2B Custom Property/MOQ Filtration & Wholesale SDUI Switching
* **Actors & Cognito Roles**: `B2B_ORG_ADMIN`, `B2B_BUYER`, `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* wholesale company buyer (`cognito:groups = ["B2B_BUYER"]`),
  * *I want* the storefront SDUI engine and Elasticsearch search endpoint to filter products by B2B Minimum Order Quantity (`moq_max`), contracted B2B tier price ranges, bulk case-pack properties, and authorized distributor brands (`b2b_authorized_brands`), rendering `B2BBulkVariantMatrix` and `TieredPriceTable` in my preferred language.

### US-3.2: Cross-Border Shipping via Aramex & DHL Express with Landed Duties & Bilingual Commercial Invoices
* **Actors & Cognito Roles**: `B2B_BUYER`, `B2C_CUSTOMER`, `STORE_ADMIN`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* merchant exporting across MENA, GCC, Europe, and North America,
  * *I want* to configure [Aramex Shipping API](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) and [DHL Express MyDHL API](https://developer.dhl.com/api-reference/dhl-express-mydhl-api?language_content_entity=en) keys in the KMS vault so checkout calculates live volumetric air/road rates, HS-code customs duties, and automatically generates bilingual (`Arabic + English`) commercial invoices for Paperless Trade (PLT).

### US-3.3: B2B Request-for-Quote (RFQ) Negotiation, Milestone Deposits & Durable Net-30 Reminders
* **Actors & Cognito Roles**: `B2B_BUYER`, `STORE_ADMIN`, `durable-orchestrator`
* **User Story Narrative**:
  * *As a* wholesale buyer,
  * *I want* to submit an RFQ from my cart, negotiate custom unit prices, shipping incoterms (`EXW`, `FOB`, `DDP`), and milestone payment terms (e.g., `30% Upfront Deposit` via Paymob/Stripe, `70% Balance` via COD or Net-30) with localized [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) notifications and automated [AWS Lambda Durable Functions](https://aws.plainenglish.io/aws-lambda-updates-in-2025-2e664f4070d2) Net-30 payment reminders.

### US-3.4: B2B On-Premise LAN License Proxy (`Mode 6`) & Organization Multi-Seat Management
* **Actors & Cognito Roles**: `B2B_ORG_ADMIN`, `B2B_BUYER`
* **User Story Narrative**:
  * *As an* enterprise software buyer (`B2B_ORG_ADMIN`) whose corporate firewall blocks individual workstations from calling external cloud APIs,
  * *I want* to download a single KMS-signed master organization certificate (`50 seats`) and run the lightweight open-source `some-commerce-license-proxy` container on our internal LAN (`Mode 6`), or assign named employee seats via Cognito SSO from a localized SDUI license portal.

## Slice 4 (`v4.0` — Weeks 13–16): Multi-Vendor Marketplace, Global Aggregators ([Shippo](https://docs.goshippo.com/) & [EasyPost](https://docs.easypost.com/)), Split Escrow & Crypto

### US-4.1: Global 40+ Carrier Rate Shopping via Shippo & EasyPost
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `B2B_BUYER`, `VENDOR`, `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* global shopper in the US, EU, UK, or APAC,
  * *I want* checkout to query [Shippo API](https://docs.goshippo.com/shipments/rate-shopping-with-carriers) and [EasyPost API](https://docs.easypost.com/docs/shipments/rates) so I can compare live Economy Ground, 2-Day Air, and Overnight rates across 40+ carriers (USPS, UPS, FedEx, Royal Mail, Canada Post) in my local currency and language.

### US-4.2: Multi-Vendor Cart Splitting, Vendor-Defined Custom Properties & Per-Vendor Pickup Dispatch
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `VENDOR`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* marketplace vendor and shopper,
  * *I want* vendors to propose or attach custom product properties to their listings, shoppers to filter by **Vendor**, **Brand**, **N-Level Category**, and **Dynamic Properties** in Elasticsearch, and multi-vendor checkouts to atomically split into `SUBORDER#<parent_id>#<vendor_id>` with proportional COD deposit allocation and per-vendor carrier pickup dispatch.

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
  * *I want* a 1-click CloudFormation template that provisions all 5 Rust Lambdas on default On-Demand [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-rust.html), On-Demand DynamoDB (with General Filtration or optional OpenSearch Serverless), Amazon Cognito, Amazon SNS, KMS keys, and the static Expo web bundle in S3 + CloudFront so my infrastructure scales to $0 compute cost when idle.

### US-5.2: Enterprise Hybrid AWS Lambda Managed Instances + Dedicated OpenSearch Zero-ETL Stack
* **Actors**: AWS Marketplace Buyer (Enterprise)
* **User Story Narrative**:
  * *As an* enterprise buyer with high sustained traffic,
  * *I want* `storefront-sdui-api` and `checkout-webhooks-api` deployed onto [AWS Lambda Managed Instances](https://docs.aws.amazon.com/lambda/latest/dg/lambda-managed-instances.html) backed by an EC2 Graviton (`c8g`/`m8g`) Capacity Provider—paired with a dedicated [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) domain synced via [DynamoDB Zero-ETL OpenSearch Ingestion](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/OpenSearchIngestionForDynamoDB.html)—while keeping `admin-vendor-api` and `fulfillment-worker` on bursty On-Demand Lambda.

### US-5.3: AWS Marketplace Metering, Entitlement Verification & GitHub Sponsors Roadmap Webhook
* **Actors**: Platform Operator, Enterprise Buyer, GitHub Sponsor
* **User Story Narrative**:
  * *As the* creator of `some-commerce`,
  * *I want* commercial AWS Marketplace deployments to verify entitlements and report usage via the AWS Marketplace Metering API, and I want my public roadmap to automatically update slice funding progress when a [GitHub Sponsors](https://docs.github.com/en/sponsors) webhook fires.

## Slice 6 (`v6.0` — Weeks 21–24): Visual Multilingual SDUI Studio, Dynamic Property/Taxonomy Studio & White-Label Mobile Pipeline

### US-6.1: Visual Drag-and-Drop Multilingual SDUI Studio & Side-by-Side RTL/LTR Previewer (`"use dom"`)
* **Actors & Cognito Roles**: `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* non-technical merchant,
  * *I want* a drag-and-drop visual SDUI studio inside the static Expo Admin Dashboard (built with [Expo DOM Components](https://docs.expo.dev/guides/dom-components/)) where I can arrange storefront blocks, edit side-by-side translations (`ar-EG` RTL vs. `en-US` LTR), preview across Web, iOS, and Android viewports, and publish new schema versions with automatic CloudFront cache invalidation and 1-click rollback.

### US-6.2: Visual N-Level Category Tree Manager, Dynamic Property Designer & Regional Fee Matrix
* **Actors & Cognito Roles**: `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* store admin,
  * *I want* a visual taxonomy and property designer in the dashboard to drag-and-drop **unlimited N-level category trees**, create custom **Product Properties** (`Color Swatch`, `Size`, `RAM`, `Material`, `Custom Specs`) with chosen SDUI filter widgets (`COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`), manage **Brands**, and map countries/governorates to carriers and Upfront COD Deposit rules without editing raw JSON.

### US-6.3: White-Label Mobile App CI/CD Pipeline & Edge SEO `hreflang` Meta Injection
* **Actors & Cognito Roles**: `STORE_ADMIN`, Agency Sponsor, Search Engine Crawler
* **User Story Narrative**:
  * *As a* commercial brand or agency sponsor,
  * *I want* an automated AWS CodeBuild / EAS pipeline that compiles branded iOS and Android binaries from my tenant configuration, and an edge SEO injector that serves localized `<title>`, `<meta name="description">`, OpenGraph tags, and `hreflang` links for every `/[locale]/categories/[...slugs]`, `/[locale]/brands/[slug]`, and `/[locale]/products/[slug]` URL on static S3 + CloudFront web.
