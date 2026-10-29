# System Architecture & Dual AWS Lambda Execution Model

## 1. High-Level Topology (100% AWS-Native)

`some-commerce` runs entirely inside an AWS account with zero external SaaS hosting dependencies. Every component is provisioned deterministically via [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) so the platform can be deployed either by open-source self-hosters or via 1-click CloudFormation templates on [AWS Marketplace](https://docs.aws.amazon.com/marketplace/latest/userguide/product-preparation.html).

```
                     +---------------------------------------------------+
                     |           Amazon CloudFront Distribution          |
                     |  - Viewer-Request CloudFront Function (URL/SEO)   |
                     |  - Forwards CloudFront-Viewer-Country & Language  |
                     +---------+-------------------+---------------------+
                               |                   |
          +--------------------+                   +--------------------+
          | /* (Static Web Assets + WebMCP)                             | /v1/* (API, SDUI, Search & MCP)
          v                                                             v
+----------------------------------+          +--------------------------------------------------+
| Private Amazon S3 Bucket (OAC)   |          | 5-Binary Rust Cargo Lambda Workspace (Axum)      |
| - npx expo export --platform web |          | 1. storefront-sdui-api  (SDUI, Search, Cust MCP) |
| - navigator.modelContext WebMCP  |          | 2. checkout-webhooks-api(KMS Payment/Ship Hooks) |
+----------------------------------+          | 3. admin-vendor-api     (RBAC, KMS, Admin MCP)   |
                                              | 4. fulfillment-worker   (Streams -> ES + Bosta)  |
+----------------------------------+          | 5. durable-orchestrator (Net-30 / Escrow Timers) |
| Amazon Cognito User Pool         |          +-----------+--------------------+-----------------+
| - OIDC / PKCE Auth (Web & Mobile)|                      |                    |
| - Pre-Token Lambda Trigger       |                      v                    v
+----------------------------------+          +-----------------------+  +-----------------------+
                                              | Amazon DynamoDB       |  | Elasticsearch /       |
+----------------------------------+          | (SomeCommerceTable)   |  | Amazon OpenSearch     |
| Amazon SNS + Amazon Bedrock      | <--------+ - N-Level Taxonomy    |  | - Multilingual Stemmer|
| - Mobile Push (APNs / FCM) & SMS |          | - Dynamic Properties  |  | - Nested Property Aggs|
| - Bedrock Converse Tool-Use API  |          | - Streams / Zero-ETL -+->| - N-Level Facet Trees |
+----------------------------------+          +-----------------------+  +-----------------------+
```

## 2. Dual-Role WebMCP (`navigator.modelContext`) & Backend MCP Architecture (`crates/mcp-tools`)

`some-commerce` implements the **[W3C Web Model Context Protocol (WebMCP)](https://webmachinelearning.github.io/webmcp/)** ([Chrome `navigator.modelContext` API](https://developer.chrome.com/docs/ai/webmcp)) in the Universal Expo Web app alongside a backend **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/specification/2026-07-28)** + **[Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html)** tool router in Rust (`crates/mcp-tools`).

This dual design means:
1. **Browser-Native AI Agents** (such as Chrome's built-in AI or user-installed WebMCP extensions) automatically discover structured JavaScript tools registered on `navigator.modelContext` when visiting the storefront or Admin Dashboard.
2. **In-App Mobile & Web Users** (on iOS, Android, or browsers without native WebMCP) interact with the exact same tools through the embedded `AiShoppingAssistantDrawerBlock` (for customers) and `AdminAiCopilotDrawer` (for store admins/vendors), backed by `/v1/mcp/customer` and `/v1/mcp/admin`.

### 2.1 Customer WebMCP Tool Suite (`storefront-sdui-api` + Storefront `navigator.modelContext`)
* **`search_and_filter_catalog`**: Converts natural-language queries in any language (e.g., *"أريد لابتوب للألعاب برامات 16 جيجا وسعر أقل من 45000 جنيه ومتاح دفع عند الاستلام"*) into structured Elasticsearch / DynamoDB General Filter parameters (`taxonomy_node_id`, `brand_ids`, `price_max`, `supports_cod`, `props_range[ram_gb]`) and updates the live SDUI `SearchFacetFilterBlock` and `ProductGridBlock`.
* **`recommend_and_compare_products`**: Evaluates matching products against the buyer's budget, use case, and custom `properties[]`, rendering a side-by-side `ProductComparisonTableBlock` and recommending the best option.
* **`update_customer_account_details`**: Assists authenticated customers (`B2C_CUSTOMER` / `B2B_BUYER`) in filling or updating their account profile (`preferred_locale`, full name, B2B tax ID) and delivery addresses (`Governorate`, `City/District`, `Street`, `Landmark`, `Phone`) in `USER#<cognito_sub>`—enforcing an explicit user confirmation step before writing to DynamoDB.
* **`prepare_cart_and_quote_cod`**: Adds selected SKU variants (`Color x Size`) to the cart and invokes `/v1/rates/calculate` to display itemized regional shipping fees, VAT, and **Upfront COD Deposit** amounts.

### 2.2 Admin WebMCP Tool Suite (`admin-vendor-api` + Admin Dashboard `navigator.modelContext`)
Strictly guarded by `RequireStoreAdmin` / `RequireVendor` [Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) RBAC middleware:
* **`admin_style_and_generate_sdui`**: Generates, styles, or modifies localized SDUI layout trees (`SDUI#<route>#<persona>#<locale>`) and `theme_tokens` (colors, `Cairo`/`Inter` typography, spacing, RTL/LTR component blocks) from natural language prompts, validating the JSON against `crates/sdui-schema` and rendering an instant draft preview in the Admin Studio before publishing to CloudFront.
* **`admin_configure_store_and_fees`**: Configures store metadata, N-level category hierarchies (`TAXONOMY_NODE`), custom product property definitions (`PROPERTY_DEF` and their SDUI filter widgets `COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `PILL_TAGS`), and localized governorate/zone shipping + **Upfront COD Deposit** rules (`LOCALE_FEES#<country>#<zone>`).
* **`admin_create_and_translate_product`**: Takes raw product descriptions, supplier specs, or images and generates a complete multilingual product listing (`titles_i18n`, `descriptions_i18n`, `seo_slugs_i18n` in Arabic, English, etc.), assigns the N-level category node and `BRAND#<bid>`, populates custom `properties[]` and Cartesian SKU variants (`Color x Size`), and indexes the product into DynamoDB and Elasticsearch.

## 3. Dynamic Product Properties, Unlimited N-Level Taxonomy, Brands & Dual-Tier Filtration Engine

### 3.1 Unlimited N-Level Category Hierarchy (`TAXONOMY_NODE#<node_id>`)
* **Arbitrary Nesting Depth (`Level 0 .. Level N`)**: Merchants can create any number of category levels (`Electronics -> Computers -> Laptops -> Gaming Laptops -> RTX 40-Series -> 16-Inch RTX 40-Series`) without schema restrictions.
* **Materialized Ancestor Path & Property Inheritance**: Every node stores `parent_node_id`, `depth_level` (`0..N`), `ancestors_path[]`, and `attached_property_ids[]`, automatically inheriting properties down the tree.

### 3.2 User-Customizable Product Properties (`PROPERTY_DEF#<prop_code>`)
* Supports `ENUM_SINGLE`, `ENUM_MULTI`, `COLOR_SWATCH`, `NUMERIC_UNIT`, `BOOLEAN`, and `TEXT_LOCALIZED` data types, `is_variant_axis: bool`, and customizable SDUI filter widgets (`COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`, `TOGGLE_SWITCH`).

### 3.3 Dual-Tier Filtration (`crates/search-elastic`)
* **Tier 1 (`DynamoGeneralFilterProvider`)**: Native DynamoDB GSIs (`GSI1` / `GSI3`) + `FilterExpression`.
* **Tier 2 (`ElasticSearchProvider`)**: [Elasticsearch](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) / [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) with [DynamoDB Zero-ETL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/OpenSearchIngestionForDynamoDB.html) and [Nested Aggregations](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-nested-aggregation) over `properties[]`.

## 4. DynamoDB Single-Table Schema (`SomeCommerceTable`)

| Entity | `PK` | `SK` | `GSI1PK` / `GSI1SK` | `GSI2PK` / `GSI2SK` | `GSI3PK` / `GSI3SK` | Key Attributes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tenant Metadata** | `TENANT#<tid>` | `METADATA` | `DOMAIN#<host>` / `METADATA` | — | — | `store_name_i18n{}`, `default_locale`, `search_mode`, `webmcp_enabled` |
| **N-Level Category Node** | `TENANT#<tid>` | `TAXONOMY_NODE#<nid>` | `PARENT_NODE#<pid>` / `SORT#<n>#<nid>` | `SLUG#<loc>#<slug>` / `TAXONOMY_NODE#<nid>` | — | `names_i18n{}`, `ancestors_path[]`, `depth_level`, `attached_property_ids[]` |
| **Property Definition** | `TENANT#<tid>` | `PROPERTY_DEF#<code>` | `TENANT#<tid>` / `PROP_TYPE#<type>` | — | — | `names_i18n{}`, `data_type`, `is_variant_axis`, `is_filterable`, `filter_ui_widget`, `unit_i18n{}` |
| **Brand Entity** | `TENANT#<tid>` | `BRAND#<bid>` | `TENANT#<tid>` / `BRAND_NAME#<name>` | `SLUG#<loc>#<slug>` / `BRAND#<bid>` | — | `names_i18n{}`, `logo_url`, `is_verified`, `featured_node_ids[]` |
| **Product Item** | `TENANT#<tid>` | `PRODUCT#<pid>` | `NODE#<leaf_nid>` / `PRICE#<cents>` | `SLUG#<loc>#<slug>` / `PRODUCT#<pid>` | `BRAND#<bid>` / `NODE#<leaf_nid>#PRICE#<cents>` | `type`, `taxonomy_node_id`, `taxonomy_ancestors[]`, `brand_id`, `properties[]`, `variants[]`, `stock_qty` |
| **Gateway / AI Vault** | `TENANT#<tid>` | `GW_VAULT#<type>#<id>` | `TENANT#<tid>` / `GW_ENABLED#<bool>` | — | — | `kms_ciphertext_blob` (Paymob, Stripe, BTCPay, Bosta, Aramex, DHL, Shippo, Elasticsearch, Bedrock/LLM) |
| **Localized Fee Rule** | `TENANT#<tid>` | `LOCALE_FEES#<iso>#<zone>` | `TENANT#<tid>` / `FEE_PRIORITY#<n>` | — | — | `zone_names_i18n{}`, `base_fee_cents`, `per_kg_cents`, `cod_deposit_rule`, `tax_vat_pct` |
| **Localized SDUI Layout** | `TENANT#<tid>` | `SDUI#<route>#<persona>#<loc>` | `SDUI_VER#<ver>` / `UPDATED#<ts>` | — | — | `direction` (`rtl`\|`ltr`), `theme_tokens`, `components_json` |
| **Order & Split COD** | `TENANT#<tid>` | `ORDER#<oid>` | `CUST#<sub_id>` / `CREATED#<ts>` | `STATUS#<st>` / `CREATED#<ts>` | — | `order_locale`, `total_cents`, `deposit_paid_cents`, `cod_collection_cents` |
| **Digital License** | `LICENSE#<key>` | `METADATA` | `CUST#<sub_id>` / `PRODUCT#<pid>` | `ORDER#<oid>` / `LICENSE#<key>` | — | `ed25519_sig`, `verification_mode`, `max_seats`, `active_fingerprints[]`, `status` |
