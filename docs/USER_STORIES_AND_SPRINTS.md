# Deep Engineering User Stories & 12-Sprint Execution Plan (Slices 1–6)

Each vertical slice is a **4-week milestone (two 2-week sprints)** funded via [GitHub Sponsors](https://github.com/sponsors/maheraladdin). Every slice ships a standalone, deployable production release across static AWS Web ([Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) + [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)), iOS, and Android via [Expo](https://docs.expo.dev/).

Every user story below includes its **Cognito Persona/Roles**, **Multilingual & RTL/LTR Requirements**, **Target Rust Lambda Binary & API Contract**, **DynamoDB / Elasticsearch Access Pattern**, and **Given/When/Then Acceptance Criteria & Edge Cases**.

## Slice 1 (`v1.0` — Weeks 1–4): Core B2C Storefront, Amazon Cognito Auth, Unlimited N-Level Categories, Dynamic Product Properties, Elasticsearch + General Filtration, Customer & Admin WebMCP Tools, Paymob/Stripe, Bosta & Split COD

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
  * *I want* to filter and search products using both **General Filtration** (any N-level Category/Sub-Category node, Brand, Price Range, In-Stock Only, On-Sale, Product Type `PHYSICAL`/`DIGITAL`, COD Eligibility, Minimum Rating, Sort Order) and **Advanced [Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) Dynamic Property Filtration** (multilingual full-text search with Arabic/English stemming and typo tolerance, plus [Nested Aggregations](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-nested-aggregation) over arbitrary merchant-defined `properties[]`),
  * *So that* the SDUI `SearchFacetFilterBlock` automatically renders the exact filter widgets (`COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `TOGGLE_SWITCH`) configured by the merchant with live product counts.

### US-1.5: Localized Governorate/Zone Fee Matrix & KMS-Encrypted Vault (Paymob, Stripe, Bosta, Elasticsearch & AI Providers)
* **Actors & Cognito Roles**: `STORE_ADMIN`, `checkout-webhooks-api`
* **User Story Narrative**:
  * *As a* store admin,
  * *I want* to store encrypted API credentials for [Paymob](https://developers.paymob.com/paymob-docs), [Stripe](https://docs.stripe.com/api), [Bosta](https://docs.bosta.co/), external [Elasticsearch](https://www.elastic.co/) clusters, and AI/LLM providers in the dashboard alongside a **Localized Fee & Tax Matrix** (`LOCALE_FEES#<country>#<zone>`) with multilingual zone names (e.g., `"الدقهلية - المنصورة"` / `"Dakahlia - Mansoura"`), weight brackets, VAT %, and COD surcharges.

### US-1.6: Anti-RTO Upfront Deposit + Split Cash on Delivery (`DEPOSIT_COD`), Bosta AWB Dispatch & Multilingual SNS Alerts
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `STORE_ADMIN`, `checkout-webhooks-api`, `fulfillment-worker`, `durable-orchestrator`
* **User Story Narrative**:
  * *As a* merchant offering Cash on Delivery via [Bosta](https://docs.bosta.co/),
  * *I want* to require a configurable **Upfront COD Deposit** (`SHIPPING_FEE_ONLY`, `PERCENTAGE`, or `FIXED_AMOUNT`) paid online via [Paymob](https://developers.paymob.com/paymob-docs) or [Stripe](https://docs.stripe.com/api) before dispatching the order, and automatically book the remaining balance (`total - deposit`) as `collectionAmount` on Bosta with multilingual [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) SMS and Mobile Push notifications.

### US-1.7: Customer WebMCP (`navigator.modelContext`) & Conversational Shopping, Recommendation & Account Assistant
* **Actors & Cognito Roles**: `ANONYMOUS`, `B2C_CUSTOMER`, `B2B_BUYER`, In-Browser AI Agent ([WebMCP](https://webmachinelearning.github.io/webmcp/))
* **User Story Narrative**:
  * *As a* customer browsing on Web (via a WebMCP-enabled browser agent or the built-in store assistant) or on iOS/Android,
  * *I want* structured [WebMCP (`navigator.modelContext`)](https://developer.chrome.com/docs/ai/webmcp) and backend [MCP](https://modelcontextprotocol.io/specification/2026-07-28) tools (`search_and_filter_catalog`, `recommend_and_compare_products`, `prepare_cart_and_quote_cod`, and `update_customer_account_details`) that understand natural language in my active language (`ar-EG`, `en-US`, etc.) to search and filter products across N-level categories and dynamic properties, recommend and compare the best products for my budget/needs, and help me add or update my account profile and delivery addresses,
  * *So that* I have an intelligent third search and personal shopping tool alongside standard search and faceted filtration.
* **Multilingual & Localization Behavior**:
  * Understands conversational queries in Arabic, English, French, German, etc. (e.g., *"رشحلي أفضل لابتوب للهندسة والجيمينج تحت 45 ألف جنيه وضيف عنواني في المنصورة حي الجامعة"*), maps colloquial property names (`"رامات 16"` -> `props_range[ram_gb]=16..`), and returns localized product comparison cards (`ProductComparisonTableBlock`).
* **Target Lambda & API Contract**:
  * Client Browser API: `navigator.modelContext.registerTool(...)` registering `search_and_filter_catalog`, `recommend_and_compare_products`, `prepare_cart_and_quote_cod`, and `update_customer_account_details`.
  * `storefront-sdui-api`: `POST /v1/mcp/customer` (executes MCP tool calls and [Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html) orchestration for mobile/web in-app chat).
* **DynamoDB & Elasticsearch Access Pattern**:
  * Invokes `CatalogSearchProvider::search_products` (`crates/search-elastic`) to retrieve real-time grounded inventory, prices, and dynamic `properties[]`—never hallucinating out-of-stock products or fake prices.
  * Account updates (`update_customer_account_details`) write to `PK = TENANT#<tid>, SK = USER#<cognito_sub>` **only** after the user approves a pre-filled confirmation card (`confirm_mutation: true`).
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a shopper asking via WebMCP or `AiShoppingAssistantDrawerBlock`: *"Compare the top 3 gaming laptops with 16GB+ RAM and RTX 4060 under 50,000 EGP and tell me which one has the best screen"*, **When** `search_and_filter_catalog` and `recommend_and_compare_products` execute, **Then** the assistant queries Elasticsearch for in-stock matches, updates the live `SearchFacetFilterBlock` on screen, and renders a localized `ProductComparisonTableBlock` comparing `screen_refresh_hz`, `ram_gb`, `weight`, and `Split COD deposit`.
  2. **Given** an authenticated customer asking the assistant: *"Add my delivery address: Mansoura, Dakahlia, El-Gomhoria Street next to University Gate, phone 01012345678"*, **When** `update_customer_account_details` parses the structured fields (`governorate = "EG-DK"`, `city = "Mansoura"`, `street = "El-Gomhoria St"`, `landmark = "University Gate"`), **Then** the UI presents a pre-filled confirmation card and, upon user click, saves the address to `USER#<cognito_sub>` in DynamoDB.

### US-1.8: Admin WebMCP (`navigator.modelContext`) & AI Copilot for SDUI Styling, Store Configuration & Product Creation
* **Actors & Cognito Roles**: `STORE_ADMIN`, `VENDOR` (strictly guarded by `RequireStoreAdmin` / `RequireVendor` Cognito RBAC)
* **User Story Narrative**:
  * *As a* store administrator or vendor in the Admin Dashboard,
  * *I want* privileged WebMCP (`navigator.modelContext`) and backend MCP tools (`admin_style_and_generate_sdui`, `admin_configure_store_and_fees`, and `admin_create_and_translate_product`) that help me style and generate localized SDUI layouts and themes, configure N-level categories, custom product properties, and regional shipping/COD fees, and create/translate multi-variant products from raw notes or specs,
  * *So that* I can design, configure, and populate my store in minutes while every AI-generated change is validated against strict Rust schemas and previewed before publishing.
* **Target Lambda & API Contract**:
  * Client Browser API (registered only on `/admin/*` and `/vendor/*` routes when authenticated): `navigator.modelContext.registerTool(...)` for `admin_style_and_generate_sdui`, `admin_configure_store_and_fees`, and `admin_create_and_translate_product`.
  * `admin-vendor-api`: `POST /v1/mcp/admin` (enforces `cognito:groups` RBAC, validates generated JSON against `crates/sdui-schema` and `crates/core-domain`, writes `DRAFT` previews, and logs an immutable `AUDIT#<timestamp>` record in DynamoDB).
* **Acceptance Criteria (Given / When / Then)**:
  1. **Given** a `STORE_ADMIN` prompting via Admin WebMCP: *"Restyle the home page for our White Friday campaign with a dark-navy & gold theme, a countdown hero banner in Arabic and English, and a featured ASUS/Lenovo brand pill bar"*, **When** `admin_style_and_generate_sdui` runs, **Then** it generates schema-validated `SDUI#/home#B2C#ar-EG` (`direction: "rtl"`) and `SDUI#/home#B2C#en-US` (`direction: "ltr"`) draft JSON trees, renders a live side-by-side preview in the Admin Dashboard, and publishes to S3/CloudFront upon admin approval.
  2. **Given** a `STORE_ADMIN` prompting: *"Add a new property 'Screen Panel Type' (IPS, OLED, Mini-LED) as pill tags, attach it to Gaming Laptops, and set Dakahlia shipping to 65 EGP with shipping-fee-only COD deposit"*, **When** `admin_configure_store_and_fees` executes, **Then** it creates `PROPERTY_DEF#panel_type`, attaches it to `TAXONOMY_NODE#cat_gaming_laptops`, and updates `LOCALE_FEES#EG#DAKAHLIA` after admin confirmation.
  3. **Given** a `STORE_ADMIN` or `VENDOR` pasting raw English specs for a new product and prompting: *"Create this product in Arabic and English under Gaming Laptops with 16GB/32GB RAM variants and Black/Silver color swatches"*, **When** `admin_create_and_translate_product` executes, **Then** it populates `titles_i18n`, `descriptions_i18n`, `seo_slugs_i18n`, `properties[]`, and 4 Cartesian SKU variants (`2 RAM x 2 Colors`), saves the product to DynamoDB, and indexes it into Elasticsearch.

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

### US-2.3: Air-Gapped Challenge-Response / Mobile QR Hardware Activation (`Mode 2`) & CloudFront Edge-Cached Revocation Lists (`Mode 3`)
* **Actors & Cognito Roles**: `B2C_CUSTOMER`, `B2B_BUYER`, Client Software SDK, `storefront-sdui-api`, `checkout-webhooks-api`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* software vendor protecting against both offline machine cloning and payment refunds/chargebacks **without periodic online heartbeating**,
  * *I want* offline target machines to generate a hardware-fingerprint challenge QR code (or `.req` file) that the buyer scans once using the `some-commerce` [Expo](https://docs.expo.dev/) mobile app to receive a hardware-locked `.cert` file (`Mode 2`), and I want `fulfillment-worker` to publish a compact, Ed25519-signed **Certificate Revocation List / Bloom Filter (`revoked.crl.bin` — [RFC 5280](https://www.rfc-editor.org/info/rfc5280/))** to [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) + [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html) whenever a Stripe/Paymob refund or [Bosta](https://docs.bosta.co/) return occurs (`Mode 3`).

## Slice 3 (`v3.0` — Weeks 9–12): B2B Wholesale, Cross-Border Express ([Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) & [DHL Express](https://developer.dhl.com/)), RFQ & B2B On-Premise License Proxy

### US-3.1: Cognito B2B Organization Onboarding, B2B Custom Property/MOQ Filtration & Wholesale SDUI Switching
* **Actors & Cognito Roles**: `B2B_ORG_ADMIN`, `B2B_BUYER`, `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* wholesale company buyer (`cognito:groups = ["B2B_BUYER"]`),
  * *I want* the storefront SDUI engine, WebMCP shopping assistant, and Elasticsearch search endpoint to filter products by B2B Minimum Order Quantity (`moq_max`), contracted B2B tier price ranges, bulk case-pack properties, and authorized distributor brands (`b2b_authorized_brands`), rendering `B2BBulkVariantMatrix` and `TieredPriceTable` in my preferred language.

### US-3.2: Cross-Border Shipping via Aramex & DHL Express with Landed Duties & Bilingual Commercial Invoices
* **Actors & Cognito Roles**: `B2B_BUYER`, `B2C_CUSTOMER`, `STORE_ADMIN`, `fulfillment-worker`
* **User Story Narrative**:
  * *As a* merchant exporting across MENA, GCC, Europe, and North America,
  * *I want* to configure [Aramex Shipping API](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) and [DHL Express MyDHL API](https://developer.dhl.com/api-reference/dhl-express-mydhl-api?language_content_entity=en) keys in the KMS vault so checkout calculates live volumetric air/road rates, HS-code customs duties, and automatically generates bilingual (`Arabic + English`) commercial invoices for Paperless Trade (PLT).

### US-3.3: B2B Request-for-Quote (RFQ) Negotiation, Milestone Deposits & Durable Net-30 Reminders
* **Actors & Cognito Roles**: `B2B_BUYER`, `STORE_ADMIN`, `durable-orchestrator`
* **User Story Narrative**:
  * *As a* wholesale buyer,
  * *I want* to submit an RFQ from my cart (or via the WebMCP B2B assistant), negotiate custom unit prices, shipping incoterms (`EXW`, `FOB`, `DDP`), and milestone payment terms (e.g., `30% Upfront Deposit` via Paymob/Stripe, `70% Balance` via COD or Net-30) with localized [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) notifications and automated [AWS Lambda Durable Functions](https://aws.plainenglish.io/aws-lambda-updates-in-2025-2e664f4070d2) Net-30 payment reminders.

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
  * *I want* vendors to use the Admin/Vendor WebMCP assistant to attach custom product properties and translate their listings, shoppers to filter by **Vendor**, **Brand**, **N-Level Category**, and **Dynamic Properties** in Elasticsearch, and multi-vendor checkouts to atomically split into `SUBORDER#<parent_id>#<vendor_id>` with proportional COD deposit allocation and per-vendor carrier pickup dispatch.

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

## Slice 6 (`v6.0` — Weeks 21–24): Visual Multilingual SDUI Studio, WebMCP Styling Copilot, Dynamic Property/Taxonomy Studio & White-Label Mobile Pipeline

### US-6.1: Visual Drag-and-Drop Multilingual SDUI Studio & Side-by-Side RTL/LTR Previewer with WebMCP Styling Copilot (`"use dom"`)
* **Actors & Cognito Roles**: `STORE_ADMIN`
* **User Story Narrative**:
  * *As a* non-technical merchant,
  * *I want* a drag-and-drop visual SDUI studio inside the static Expo Admin Dashboard (built with [Expo DOM Components](https://docs.expo.dev/guides/dom-components/)) paired with the `admin_style_and_generate_sdui` WebMCP Copilot where I can either drag blocks manually or ask the AI to restyle/translate pages (`ar-EG` RTL vs. `en-US` LTR), preview across Web, iOS, and Android viewports, and publish with automatic CloudFront cache invalidation and 1-click rollback.

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
