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
| Amazon SNS Notification Engine   | <--------+ - Single-Table Design |  | - Multilingual Stemmer|
| - Mobile Push (APNs / FCM)       |          | - General Filtration  |  | - Nested Facet Aggs   |
| - Transactional SMS & Fan-Out    |          | - Streams / Zero-ETL -+->| - Category/Brand Trees|
+----------------------------------+          +-----------------------+  +-----------------------+
```

## 2. Catalog Taxonomy (Categories, Sub-Categories, Brands) & Dual-Tier Filtration Engine

### 2.1 Hierarchical Categories, Sub-Categories & Brands
* **Categories & Sub-Categories (`PK = TENANT#<tid>`, `SK = CATEGORY#<cat_id>`)**:
  * Supports unlimited nesting depth via `parent_category_id` (`ROOT` for top-level categories, or a parent `cat_id` for sub-categories and leaf sub-categories) and a materialized `ancestors_path: ["cat_electronics", "cat_computers", "cat_gaming_laptops"]`.
  * Each category defines `filter_schema_attributes[]` (e.g., `["ram_gb", "storage_ssd", "gpu"]` for Gaming Laptops vs. `["size", "color", "material"]` for Apparel) so the SDUI filter sidebar automatically adapts to the active category or sub-category.
* **Brands (`PK = TENANT#<tid>`, `SK = BRAND#<brand_id>`)**:
  * Stores multilingual names (`names_i18n`), brand story (`descriptions_i18n`), localized SEO slugs (`SLUG#<locale>#<slug>`), brand logo S3 URL, `is_verified`, and `featured_category_ids[]`.

### 2.2 Dual-Tier Filtration (`crates/search-elastic`)
All search and catalog browsing endpoints (`GET /v1/search/products`) are backed by the `CatalogSearchProvider` trait, which implements two complementary engines:

1. **Tier 1 — General Filtration Engine (`DynamoGeneralFilterProvider`)**:
   * Executes directly against `SomeCommerceTable` Global Secondary Indexes (`GSI1` for Category/Sub-Category + Price, `GSI3` for Brand + Sub-Category + Price) combined with DynamoDB `FilterExpression` predicates (`product_type`, `in_stock`, `supports_cod`, `is_on_sale`, `min_rating`, `vendor_id`).
   * Enables $0-idle-cost operation in the Standard Serverless edition and acts as an automatic circuit-breaker fallback if an Elasticsearch cluster is under maintenance.
2. **Tier 2 — Elasticsearch / [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) Faceted Search (`ElasticSearchProvider`)**:
   * **Real-Time Ingestion**: Kept in sync via [DynamoDB Zero-ETL OpenSearch Ingestion](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/OpenSearchIngestionForDynamoDB.html) or `fulfillment-worker` DynamoDB Streams (`/_bulk` API).
   * **Multilingual Full-Text Analyzers**: Indexes `titles_i18n`, `descriptions_i18n`, `brand_names_i18n`, and `category_names_i18n` with language-specific analyzers (`arabic` normalizing Alef/Teh Marbuta/diacritics, `english`, `french`, `german`), `edge_ngram` instant autocomplete, and fuzzy typo tolerance.
   * **Single-Query Faceted Aggregations ([Elasticsearch Aggregations](https://www.elastic.co/docs/explore-analyze/query-filter/aggregations))**:
     * `category_tree_agg` (`terms` on `category_ancestors` and `sub_category_id`)
     * `brand_agg` (`terms` on `brand_id` using `post_filter` for disjunctive multi-brand selection)
     * `attributes_nested_agg` ([Nested Aggregation](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-nested-aggregation) on `attributes.code` and `attributes.value` for dynamic variant/spec counts)
     * `price_stats_agg` & `general_flags_agg` (`in_stock`, `supports_cod`, `is_digital`, `rating_buckets`, `b2b_moq_ranges`).

## 3. Authentication & Authorization with Amazon Cognito

All identity, authentication, and authorization flows are powered by **[Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html)** paired with a Rust **[Pre-Token Generation Lambda Trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html)**:

* **Cognito User Pool Groups (`cognito:groups`)**: `SUPER_ADMIN`, `STORE_ADMIN`, `VENDOR`, `B2B_ORG_ADMIN`, `B2B_BUYER`, and `B2C_CUSTOMER`.
* **Pre-Token Claims**: Injects `custom:tenant_id`, `custom:persona` (`B2C` | `B2B`), `custom:preferred_locale`, `custom:b2b_org_id`, `custom:price_list_id`, and `custom:vendor_id`.

## 4. Omnichannel Notifications & Pub/Sub Fan-Out with Amazon SNS

**[Amazon Simple Notification Service (Amazon SNS)](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)** powers all localized customer, vendor, and admin notifications through `crates/notify-sns` ([Mobile Push](https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-application-as-subscriber.html) for iOS APNs & Android FCM, transactional SMS, and event fan-out topics).

## 5. DynamoDB Single-Table Schema (`SomeCommerceTable`)

| Entity | `PK` | `SK` | `GSI1PK` / `GSI1SK` | `GSI2PK` / `GSI2SK` | `GSI3PK` / `GSI3SK` | Key Attributes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tenant Metadata** | `TENANT#<tid>` | `METADATA` | `DOMAIN#<host>` / `METADATA` | — | — | `store_name_i18n{}`, `default_locale`, `search_mode` (`ELASTIC`\|`DYNAMO`) |
| **Category / Sub-Cat** | `TENANT#<tid>` | `CATEGORY#<cid>` | `PARENT_CAT#<pid>` / `SORT#<n>#<cid>` | `SLUG#<loc>#<slug>` / `CATEGORY#<cid>` | — | `names_i18n{}`, `ancestors_path[]`, `depth`, `filter_schema_attributes[]` |
| **Brand Entity** | `TENANT#<tid>` | `BRAND#<bid>` | `TENANT#<tid>` / `BRAND_NAME#<name>` | `SLUG#<loc>#<slug>` / `BRAND#<bid>` | — | `names_i18n{}`, `logo_url`, `is_verified`, `featured_categories[]` |
| **Product Item** | `TENANT#<tid>` | `PRODUCT#<pid>` | `CAT#<sub_cid>` / `PRICE#<cents>` | `SLUG#<loc>#<slug>` / `PRODUCT#<pid>` | `BRAND#<bid>` / `CAT#<sub_cid>#PRICE#<cents>` | `type`, `category_id`, `sub_category_id`, `category_ancestors[]`, `brand_id`, `attributes[]`, `stock_qty` |
| **Gateway / Search Vault** | `TENANT#<tid>` | `GW_VAULT#<type>#<id>` | `TENANT#<tid>` / `GW_ENABLED#<bool>` | — | — | `kms_ciphertext_blob` (Paymob, Stripe, BTCPay, Bosta, Aramex, DHL, Shippo, Elasticsearch) |
| **Localized Fee Rule** | `TENANT#<tid>` | `LOCALE_FEES#<iso>#<zone>` | `TENANT#<tid>` / `FEE_PRIORITY#<n>` | — | — | `zone_names_i18n{}`, `base_fee_cents`, `per_kg_cents`, `cod_deposit_rule`, `tax_vat_pct` |
| **Localized SDUI Layout** | `TENANT#<tid>` | `SDUI#<route>#<persona>#<loc>` | `SDUI_VER#<ver>` / `UPDATED#<ts>` | — | — | `direction` (`rtl`\|`ltr`), `theme_tokens`, `components_json` |
| **Order & Split COD** | `TENANT#<tid>` | `ORDER#<oid>` | `CUST#<sub_id>` / `CREATED#<ts>` | `STATUS#<st>` / `CREATED#<ts>` | — | `order_locale`, `total_cents`, `deposit_paid_cents`, `cod_collection_cents` |
| **Digital License** | `LICENSE#<key>` | `METADATA` | `CUST#<sub_id>` / `PRODUCT#<pid>` | `ORDER#<oid>` / `LICENSE#<key>` | — | `ed25519_sig`, `max_seats`, `active_fingerprints[]`, `status` |
