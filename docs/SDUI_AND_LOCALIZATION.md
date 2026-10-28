# Server-Driven UI (SDUI), Dynamic Product Properties, N-Level Taxonomy & Multilingual Localization Specification

## 1. End-to-End Multilingual Architecture (`crates/i18n-engine` + `expo-localization`)

To make `some-commerce` work seamlessly across MENA (`ar-EG`, `ar-SA`, `ar-AE`), Europe (`en-GB`, `fr-FR`, `de-DE`, `es-ES`), North America (`en-US`), and Turkey (`tr-TR`), multilingual support is built into **six architectural layers**:

1. **Deterministic Locale Resolution & Fallback Chain (`crates/i18n-engine`)**:
   * Priority order: `?locale=` or `/[locale]/...` URL prefix -> [Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) JWT `custom:preferred_locale` -> [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/) `Accept-Language` -> [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-functions.html) `CloudFront-Viewer-Country` -> `tenant.default_locale` -> `en-US`.
2. **Bidirectional Layout Mirroring (`RTL` & `LTR`) in Universal Expo**:
   * Every `/v1/sdui/*` response returns `"locale"` and `"direction": "rtl" | "ltr"`, mirroring flex layouts and switching fonts (`Cairo` vs. `Inter`) without restarting the app.
3. **Unlimited N-Level Taxonomy, Brands & User-Defined Product Properties**:
   * Every N-level category node (`TAXONOMY_NODE#<node_id>`), Brand (`BRAND#<brand_id>`), Property Definition (`PROPERTY_DEF#<prop_code>`), and Product (`PRODUCT#<pid>`) stores localized maps (`names_i18n`, `titles_i18n`, `unit_labels_i18n`, `seo_slugs_i18n`).

## 2. User-Customizable Product Properties & Unlimited N-Level Categorization

Merchants are never locked into fixed product columns or a rigid 2-level category tree:

### 2.1 Unlimited N-Level Category Hierarchy (`TAXONOMY_NODE#<node_id>`)
* **Arbitrary Depth (`Level 0 .. Level N`)**: Any category node can have a `parent_node_id` (`ROOT` or another `node_id`) and stores its materialized `ancestors_path: ["node_l0", "node_l1", "node_l2", ..., "node_ln"]` plus `depth_level`.
* **Property Inheritance + Ad-Hoc Overrides**:
  * A category node at depth `k` automatically inherits all `attached_property_ids[]` from its ancestor nodes (`0 .. k-1`) and can attach additional properties specific to depth `k`.
  * When editing any individual product, the merchant can also add **ad-hoc product-level properties** (`custom_properties[]`) on the fly without pre-attaching them to a category.

### 2.2 Dynamic Property Engine (`PROPERTY_DEF#<prop_code>`)
Merchants can create any property (e.g., `color`, `size`, `ram_gb`, `shoe_width`, `wattage`, `license_os`, `fabric_blend`) and customize:
* **`data_type`**: `ENUM_SINGLE` | `ENUM_MULTI` | `COLOR_SWATCH` | `NUMERIC_UNIT` | `BOOLEAN` | `TEXT_LOCALIZED`
* **`is_variant_axis`**: When `true`, combinations of variant-axis properties (`Color x Size` or `RAM x Storage`) generate distinct purchasable SKUs with independent price, stock, weight, and image galleries. When `false`, the property is stored as a product specification.
* **`is_filterable_facet` & `filter_ui_widget`**: Controls whether the property is aggregated in [Elasticsearch Nested Aggregations](https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-nested-aggregation) / DynamoDB General Filtration and which SDUI widget renders it (`COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`, or `TOGGLE_SWITCH`).

## 3. Dynamic SDUI Search, N-Level Category Tree, Brand & Custom Property Filter Schema

```json
{
  "schema_version": "1.0",
  "route": "/categories/cat_rtx40_gaming_laptops",
  "locale": "ar-EG",
  "direction": "rtl",
  "persona": "B2C",
  "blocks": [
    {
      "id": "n_level_breadcrumbs",
      "type": "CategoryBreadcrumbBlock",
      "props": {
        "trail": [
          { "id": "cat_l0_electronics", "depth": 0, "label": "إلكترونيات" },
          { "id": "cat_l1_computers", "depth": 1, "label": "كمبيوتر ولابتوب" },
          { "id": "cat_l2_laptops", "depth": 2, "label": "لابتوب" },
          { "id": "cat_l3_gaming", "depth": 3, "label": "لابتوب للألعاب" },
          { "id": "cat_l4_rtx40", "depth": 4, "label": "سلسلة RTX 40" }
        ]
      }
    },
    {
      "id": "brand_carousel",
      "type": "BrandPillSelectorBlock",
      "props": {
        "selected_brand_ids": ["brand_asus"],
        "brands": [
          { "id": "brand_asus", "name": "أسوس (ASUS)", "logo_url": "https://.../asus.svg", "doc_count": 28 },
          { "id": "brand_lenovo", "name": "لينوفو (Lenovo)", "logo_url": "https://.../lenovo.svg", "doc_count": 19 }
        ]
      }
    },
    {
      "id": "facet_filter_sidebar",
      "type": "SearchFacetFilterBlock",
      "props": {
        "search_endpoint": "/v1/search/products",
        "general_filters": {
          "in_stock_only": { "label": "متوفر في المخزن فقط", "active": true, "doc_count": 46 },
          "supports_cod": { "label": "متاح الدفع عند الاستلام (بوسطة)", "active": false, "doc_count": 42 },
          "on_sale_only": { "label": "عروض وخصومات", "active": false, "doc_count": 15 }
        },
        "price_range_facet": {
          "currency": "EGP",
          "min_available": 22000,
          "max_available": 95000,
          "selected_min": 25000,
          "selected_max": 65000
        },
        "child_taxonomy_facets": [
          { "id": "cat_l5_rtx4060", "depth": 5, "label": "لابتوب RTX 4060", "doc_count": 18 },
          { "id": "cat_l5_rtx4070", "depth": 5, "label": "لابتوب RTX 4070", "doc_count": 10 }
        ],
        "dynamic_property_facets": [
          {
            "prop_code": "color",
            "label": "اللون",
            "data_type": "COLOR_SWATCH",
            "filter_ui_widget": "COLOR_SWATCH_GRID",
            "buckets": [
              { "value": "black", "label": "أسود", "hex": "#111827", "doc_count": 30, "selected": true },
              { "value": "silver", "label": "فضي", "hex": "#E5E7EB", "doc_count": 16, "selected": false }
            ]
          },
          {
            "prop_code": "ram_gb",
            "label": "حجم الذاكرة (RAM)",
            "data_type": "NUMERIC_UNIT",
            "filter_ui_widget": "PILL_TAGS",
            "unit_label": "جيجابايت",
            "buckets": [
              { "value": "16", "label": "16 جيجابايت", "doc_count": 21, "selected": true },
              { "value": "32", "label": "32 جيجابايت", "doc_count": 7, "selected": false }
            ]
          },
          {
            "prop_code": "screen_refresh_hz",
            "label": "معدل تحديث الشاشة",
            "data_type": "NUMERIC_UNIT",
            "filter_ui_widget": "RANGE_SLIDER",
            "unit_label": "Hz",
            "min_available": 60,
            "max_available": 240,
            "selected_min": 144,
            "selected_max": 240
          }
        ]
      }
    }
  ]
}
```
