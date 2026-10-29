# Server-Driven UI (SDUI), WebMCP Tools, Dynamic Product Properties, N-Level Taxonomy & Multilingual Specification

## 1. End-to-End Multilingual Architecture (`crates/i18n-engine` + `expo-localization`)

To make `some-commerce` work seamlessly across MENA (`ar-EG`, `ar-SA`, `ar-AE`), Europe (`en-GB`, `fr-FR`, `de-DE`, `es-ES`), North America (`en-US`), and Turkey (`tr-TR`), multilingual support is built into **six architectural layers**:

1. **Deterministic Locale Resolution & Fallback Chain (`crates/i18n-engine`)**:
   * Priority order: `?locale=` or `/[locale]/...` URL prefix -> [Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) JWT `custom:preferred_locale` -> [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/) `Accept-Language` -> [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-functions.html) `CloudFront-Viewer-Country` -> `tenant.default_locale` -> `en-US`.
2. **Bidirectional Layout Mirroring (`RTL` & `LTR`) in Universal Expo**:
   * Every `/v1/sdui/*` response returns `"locale"` and `"direction": "rtl" | "ltr"`, mirroring flex layouts and switching fonts (`Cairo` vs. `Inter`) without restarting the app.
3. **Unlimited N-Level Taxonomy, Brands & User-Defined Product Properties**:
   * Every N-level category node (`TAXONOMY_NODE#<node_id>`), Brand (`BRAND#<brand_id>`), Property Definition (`PROPERTY_DEF#<prop_code>`), and Product (`PRODUCT#<pid>`) stores localized maps (`names_i18n`, `titles_i18n`, `unit_labels_i18n`, `seo_slugs_i18n`).

## 2. WebMCP (`navigator.modelContext`) & Backend MCP Tool Specifications

On static Expo Web, `some-commerce` registers structured tools via the **[W3C WebMCP (`navigator.modelContext`)](https://webmachinelearning.github.io/webmcp/)** API ([Chrome WebMCP](https://developer.chrome.com/docs/ai/webmcp)), while exposing the exact same tool schemas on `POST /v1/mcp/customer` and `POST /v1/mcp/admin` (powered by [Amazon Bedrock Converse API Tool Use](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html)) for mobile and in-app chat users.

### 2.1 Customer WebMCP Registration (`StorefrontWebMcpBridge.ts`)

```typescript
if (typeof navigator !== "undefined" && "modelContext" in navigator) {
  // 1. Conversational Search & Dynamic Property Filtration
  navigator.modelContext.registerTool({
    name: "search_and_filter_catalog",
    description: "Search products across N-level categories, brands, and dynamic properties, and update the storefront filter UI.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Keywords in user language (Arabic, English, etc.)" },
        taxonomy_node_id: { type: "string", description: "Category or sub-category node ID" },
        brand_ids: { type: "array", items: { type: "string" } },
        price_min: { type: "number" },
        price_max: { type: "number" },
        supports_cod: { type: "boolean" },
        in_stock_only: { type: "boolean", default: true },
        dynamic_properties: {
          type: "object",
          description: "Key-value map of custom product properties (e.g. {'ram_gb': '16', 'color': 'black'})"
        }
      }
    },
    execute: async (args) => storefrontMcpClient.searchAndUpdateUi(args)
  });

  // 2. Product Recommendation & Side-by-Side Comparison
  navigator.modelContext.registerTool({
    name: "recommend_and_compare_products",
    description: "Compare candidate products against customer budget, use case, and custom properties, rendering a comparison table.",
    inputSchema: {
      type: "object",
      required: ["use_case"],
      properties: {
        use_case: { type: "string", description: "Customer goal (e.g. 'gaming and 3D rendering under 45,000 EGP')" },
        candidate_product_ids: { type: "array", items: { type: "string" } },
        highlight_properties: { type: "array", items: { type: "string" } }
      }
    },
    execute: async (args) => storefrontMcpClient.recommendAndCompare(args)
  });

  // 3. Customer Account & Address Profile Assistant
  navigator.modelContext.registerTool({
    name: "update_customer_account_details",
    description: "Add or update the authenticated customer's profile preferences or delivery address (requires user confirmation).",
    inputSchema: {
      type: "object",
      properties: {
        preferred_locale: { type: "string", enum: ["ar-EG", "ar-SA", "en-US", "fr-FR", "de-DE"] },
        full_name: { type: "string" },
        shipping_address: {
          type: "object",
          properties: {
            country_code: { type: "string" },
            governorate_or_state: { type: "string" },
            city_district: { type: "string" },
            street_address: { type: "string" },
            landmark: { type: "string" },
            phone_e164: { type: "string" }
          }
        }
      }
    },
    execute: async (args) => storefrontMcpClient.promptAndSaveAccountDetails(args)
  });
}
```

### 2.2 Admin WebMCP Registration (`AdminWebMcpBridge.ts` — `STORE_ADMIN` / `VENDOR` Only)

```typescript
if (typeof navigator !== "undefined" && "modelContext" in navigator && isAuthenticatedAdmin) {
  // 1. SDUI Styling, Theme Token & Layout Generator
  navigator.modelContext.registerTool({
    name: "admin_style_and_generate_sdui",
    description: "Generate or restyle localized SDUI page layouts and theme tokens (colors, RTL/LTR blocks, fonts) with live draft preview.",
    inputSchema: {
      type: "object",
      required: ["route", "locale", "styling_instruction"],
      properties: {
        route: { type: "string", examples: ["/home", "/categories/cat_gaming_laptops"] },
        persona: { type: "string", enum: ["B2C", "B2B"], default: "B2C" },
        locale: { type: "string", examples: ["ar-EG", "en-US"] },
        styling_instruction: { type: "string" },
        theme_tokens_override: {
          type: "object",
          properties: {
            primary_color: { type: "string" },
            background_color: { type: "string" },
            font_family: { type: "string" }
          }
        }
      }
    },
    execute: async (args) => adminMcpClient.generateSduiDraftPreview(args)
  });

  // 2. Store Configuration, N-Level Taxonomy, Custom Property & Fee Rules Assistant
  navigator.modelContext.registerTool({
    name: "admin_configure_store_and_fees",
    description: "Create or update N-level category nodes, custom product properties (and filter widgets), or regional shipping/COD deposit rules.",
    inputSchema: {
      type: "object",
      required: ["action_type", "payload"],
      properties: {
        action_type: {
          type: "string",
          enum: ["UPSERT_TAXONOMY_NODE", "UPSERT_PROPERTY_DEF", "UPSERT_LOCALE_FEE_RULE", "UPSERT_BRAND"]
        },
        payload: { type: "object" }
      }
    },
    execute: async (args) => adminMcpClient.configureStoreEntity(args)
  });

  // 3. Multilingual Product & Variant Builder
  navigator.modelContext.registerTool({
    name: "admin_create_and_translate_product",
    description: "Create or update a physical or digital product with multilingual titles/descriptions, N-level category, brand, and custom properties.",
    inputSchema: {
      type: "object",
      required: ["product_type", "taxonomy_node_id", "raw_specs_or_prompt"],
      properties: {
        product_type: { type: "string", enum: ["PHYSICAL", "DIGITAL", "HYBRID_BUNDLE"] },
        taxonomy_node_id: { type: "string" },
        brand_id: { type: "string" },
        base_price_cents: { type: "integer" },
        target_locales: { type: "array", items: { type: "string" }, default: ["ar-EG", "en-US"] },
        raw_specs_or_prompt: { type: "string" }
      }
    },
    execute: async (args) => adminMcpClient.draftAndIndexMultilingualProduct(args)
  });
}
```

## 3. Core Universal SDUI Component Registry

| Component `type` | Persona Scope | Multilingual, Filtration & WebMCP Behavior |
| :--- | :--- | :--- |
| `AiShoppingAssistantDrawerBlock` | `B2C`, `B2B` | Embedded conversational shopping & account helper invoking Customer WebMCP / MCP tools (`search_and_filter_catalog`, `recommend_and_compare_products`, `update_customer_account_details`). |
| `ProductComparisonTableBlock` | `B2C`, `B2B` | Side-by-side matrix comparing candidate products across price, Split COD deposit, and dynamic `properties[]`, rendered by `recommend_and_compare_products`. |
| `CategoryTreeDrawerBlock` | `B2C`, `B2B` | Expandable N-level accordion of Categories and Sub-Categories (`0..N`) with RTL/LTR mirroring and live item counts. |
| `CategoryBreadcrumbBlock` | `B2C`, `B2B` | Renders the materialized N-level `ancestors_path[]` trail with localized links. |
| `BrandPillSelectorBlock` | `B2C`, `B2B` | Horizontal scannable bar of verified Brand logos and live Elasticsearch document counts (`brand_agg`). |
| `SearchFacetFilterBlock` | `B2C`, `B2B` | Renders General Filters and dynamic `PROPERTY_DEF` widgets (`COLOR_SWATCH_GRID`, `RANGE_SLIDER`, `CHECKBOX_LIST`, `PILL_TAGS`, `TOGGLE_SWITCH`). |
| `B2BBulkVariantMatrix` | `B2B` | Renders localized variant option names (`اللون`/`المقاس` vs. `Color`/`Size`) and volume-tier discount tables. |
| `LocalizedAddressFormBlock` | `B2C`, `B2B` | Dynamically switches between `Governorate/District/Landmark` (Egypt/MENA) and `State/Province + Postal Code` (US/EU/UK); pre-fillable via `update_customer_account_details`. |
| `CodDepositSummaryCard` | `B2C`, `B2B` | Formats `Pay Now Deposit` vs. `Pay on Delivery Balance` in the shopper's active language and currency. |
| `CustomerLicenseVaultBlock` | `B2C`, `B2B` | Displays localized download instructions, Ed25519 `.lic` certificates, air-gapped QR scanner (`Mode 2`), and B2B seat controls. |
