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
          | /* (Static Web Assets)                                      | /v1/* (API, SDUI, Search & Hooks)
          v                                                             v
+----------------------------------+          +--------------------------------------------------+
| Private Amazon S3 Bucket (OAC)   |          | 5-Binary Rust Cargo Lambda Workspace (Axum)      |
| - npx expo export --platform web |          | 1. storefront-sdui-api  (SDUI, Search & Filter)  |
| - Pre-rendered .html/.css/.js    |          | 2. checkout-webhooks-api(KMS Payment/Ship Hooks) |
+----------------------------------+          | 3. admin-vendor-api     (Cognito RBAC + KMS)     |
                                              | 4. fulfillment-worker   (Streams -> ES + Bosta)  |
+----------------------------------+          | 5. durable-orchestrator (Net-30 / Escrow Timers) |
| Amazon Cognito User Pool         |          +-----------+--------------------+-----------------+
| - OIDC / PKCE Auth (Web & Mobile)|                      |                    |
| - Pre-Token Lambda Trigger       |                      v                    v
+----------------------------------+          +-----------------------+  +-----------------------+
                                              | Amazon DynamoDB       |  | Elasticsearch /       |
+----------------------------------+          | (SomeCommerceTable)   |  | Amazon OpenSearch     |
| Amazon SNS Notification Engine   | <--------+ - N-Level Taxonomy    |  | - Multilingual Stemmer|
| - Mobile Push (APNs / FCM)       |          | - Dynamic Properties  |  | - Nested Property Aggs|
| - Transactional SMS & Fan-Out    |          | - Streams / Zero-ETL -+->| - N-Level Facet Trees |
+----------------------------------+          +-----------------------+  +-----------------------+
```

## 2. Dynamic Product Properties, Unlimited N-Level Taxonomy, Brands & Dual-Tier Filtration Engine

### 2.1 Unlimited N-Level Category Hierarchy (`TAXONOMY_NODE#<node_id>`)
* **Arbitrary Nesting Depth (`Level 0 .. Level N`)**: Merchants can create any number of category levels (`Electronics -> Computers -> Laptops -> Gaming Laptops -> RTX 40-Series -> 16-Inch RTX 40-Series`) without schema restrictions.
* **Materialized Ancestor Path & Property Inheritance**:
  * Every node stores `parent_node_id`, `depth_level` (`0..N`), `ancestors_path: ["node_l0", "node_l1", ..., "node_lk"]`, and `attached_property_ids[]`.
  * Child nodes automatically inherit all `attached_property_ids[]` from their ancestors while adding specialized properties for deeper levels.

### 2.2 User-Customizable Product Properties (`PROPERTY_DEF#<prop_code>`)
Merchants and vendors can define **any custom property** from the Admin Dashboard and attach it to a category node or directly to an individual product:
* **Supported Property Data Types (`data_type`)**:
  * `ENUM_SINGLE` & `ENUM_MULTI` (e.g., Material, OS, Fit, Connector Type)
  * `COLOR_SWATCH` (hex color code + localized label + optional swatch texture URL)
  * `NUMERIC_UNIT` (e.g., RAM in GB, Weight in kg, Refresh Rate in Hz, Screen Size in inches)
  * `BOOLEAN` (e.g., Waterproof, Supports 5G, Backlit Keyboard)
  * `TEXT_LOCALIZED` (free-form localized specification text)
* **Variant Axis vs. Specification Flag (`is_variant_axis`)**:
  * If `is_variant_axis = true` (e.g., `Color + Shoe Size` or `RAM + SSD Capacity`), the product builder generates distinct purchasable SKU variants for each combination with independent stock, price, barcode, and images.
  * If `is_variant_axis = false`, the property is stored as a product specification and indexed for search/filtration.
* **Customizable SDUI Filter Widgets (`filter_ui_widget`)**:
  * Merchants choose how each filterable property appears in the storefront filter drawer: `COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`, or `TOGGLE_SWITCH`.

### 2.3 First-Class Brands (`BRAND#<brand_id>`)
* Stores multilingual names (`names_i18n`), brand story (`descriptions_i18n`), localized SEO slugs (`SLUG#<locale>#<slug>`), logo S3 URL, `is_verified`, and custom brand properties.

### 2.4 Dual-Tier Filtration (`crates/search-elastic`)
All search and catalog browsing endpoints (`GET /v1/search/products`) are backed by the `CatalogSearchProvider` trait:

1. **Tier 1 — General Filtration Engine (`DynamoGeneralFilterProvider`)**:
   * Executes directly against `SomeCommerceTable` Global Secondary Indexes (`GSI1` for N-Level Category Node + Price, `GSI3` for Brand + Category Node + Price) combined with DynamoDB `FilterExpression` predicates (`product_type`, `in_stock`, `supports_cod`, `is_on_sale`, `min_rating`, and dynamic `properties`).
2. **Tier 2 — Elasticsearch / [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) Faceted Search (`ElasticSearchProvider`)**:
   * **Real-Time Ingestion**: Kept in sync via [DynamoDB Zero-ETL OpenSearch Ingestion](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/OpenSearchIngestionForDynamoDB.html) or `fulfillment-worker` DynamoDB Streams (`/_bulk` API).
   * **Single-Query Faceted Aggregations ([Elasticsearch Aggregations](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations) & [Nested Aggregations](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-nested-aggregation))**:
     * `taxonomy_children_agg` (`terms` on `taxonomy_ancestors` to return child sub-category counts at any depth `0..N`)
     * `brand_agg` (`terms` on `brand_id` with `post_filter` for disjunctive multi-brand selection)
     * `dynamic_properties_nested_agg` ([Nested Aggregation](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-nested-aggregation) on `properties` computing `terms` counts for enum/swatch properties and `stats`/`min`/`max` for numeric range sliders)
     * `price_stats_agg` & `general_flags_agg` (`in_stock`, `supports_cod`, `is_digital`, `rating_buckets`).

## 3. DynamoDB Single-Table Schema (`SomeCommerceTable`)

| Entity | `PK` | `SK` | `GSI1PK` / `GSI1SK` | `GSI2PK` / `GSI2SK` | `GSI3PK` / `GSI3SK` | Key Attributes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tenant Metadata** | `TENANT#<tid>` | `METADATA` | `DOMAIN#<host>` / `METADATA` | — | — | `store_name_i18n{}`, `default_locale`, `search_mode` (`ELASTIC`\|`DYNAMO`) |
| **N-Level Category Node** | `TENANT#<tid>` | `TAXONOMY_NODE#<nid>` | `PARENT_NODE#<pid>` / `SORT#<n>#<nid>` | `SLUG#<loc>#<slug>` / `TAXONOMY_NODE#<nid>` | — | `names_i18n{}`, `ancestors_path[]`, `depth_level`, `attached_property_ids[]` |
| **Property Definition** | `TENANT#<tid>` | `PROPERTY_DEF#<code >` | `TENANT#<tid>` / `PROP_TYPE#<type>` | — | — | `names_i18n{}`, `data_type`, `is_variant_axis`, `is_filterable`, `filter_ui_widget`, `unit_i18n{}` |
| **Brand Entity** | `TENANT#<tid>` | `BRAND#<bid>` | `TENANT#<tid>` / `BRAND_NAME#<name>` | `SLUG#<loc>#<slug>` / `BRAND#<bid>` | — | `names_i18n{}`, `logo_url`, `is_verified`, `featured_node_ids[]` |
| **Product Item** | `TENANT#<tid>` | `PRODUCT#<pid>` | `NODE#<leaf_nid>` / `PRICE#<cents>` | `SLUG#<loc>#<slug>` / `PRODUCT#<pid>` | `BRAND#<bid>` / `NODE#<leaf_nid>#PRICE#<cents>` | `type`, `taxonomy_node_id`, `taxonomy_ancestors[]`, `brand_id`, `properties[]`, `variants[]`, `stock_qty` |
| **Gateway / Search Vault** | `TENANT#<tid>` | `GW_VAULT#<type>#<id>` | `TENANT#<tid>` / `GW_ENABLED#<bool>` | — | — | `kms_ciphertext_blob` (Paymob, Stripe, BTCPay, Bosta, Aramex, DHL, Shippo, Elasticsearch) |
| **Localized Fee Rule** | `TENANT#<tid>` | `LOCALE_FEES#<iso>#<zone>` | `TENANT#<tid>` / `FEE_PRIORITY#<n>` | — | — | `zone_names_i18n{}`, `base_fee_cents`, `per_kg_cents`, `cod_deposit_rule`, `tax_vat_pct` |
| **Localized SDUI Layout** | `TENANT#<tid>` | `SDUI#<route>#<persona>#<loc>` | `SDUI_VER#<ver>` / `UPDATED#<ts>` | — | — | `direction` (`rtl`\|`ltr`), `theme_tokens`, `components_json` |
| **Order & Split COD** | `TENANT#<tid>` | `ORDER#<oid>` | `CUST#<sub_id>` / `CREATED#<ts>` | `STATUS#<st>` / `CREATED#<ts>` | — | `order_locale`, `total_cents`, `deposit_paid_cents`, `cod_collection_cents` |
| **Digital License** | `LICENSE#<key>` | `METADATA` | `CUST#<sub_id>` / `PRODUCT#<pid>` | `ORDER#<oid>` / `LICENSE#<key>` | — | `ed25519_sig`, `max_seats`, `active_fingerprints[]`, `status` |
