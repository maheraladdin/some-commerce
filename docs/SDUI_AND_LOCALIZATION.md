# Server-Driven UI (SDUI) & Multilingual Localization Engine Specification

## 1. End-to-End Multilingual Architecture (`crates/i18n-engine` + `expo-localization`)

To make `some-commerce` work seamlessly across MENA (`ar-EG`, `ar-SA`, `ar-AE`), Europe (`en-GB`, `fr-FR`, `de-DE`, `es-ES`), North America (`en-US`), and Turkey (`tr-TR`), multilingual support is built into **six architectural layers**:

### 1.1 Deterministic Locale Resolution & Fallback Chain (`crates/i18n-engine`)
Every incoming HTTP request resolves the active locale in priority order:
1. Explicit query parameter or URL prefix (`?locale=ar-EG` or `/ar-eg/products/...`)
2. Authenticated user's [Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) JWT claim (`custom:preferred_locale`)
3. Client `Accept-Language` header populated via [`expo-localization`](https://docs.expo.dev/versions/latest/sdk/localization/) (`getLocales()`)
4. Country-to-locale mapping from [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-functions.html)'s `CloudFront-Viewer-Country` header (`EG` -> `ar-EG`, `SA` -> `ar-SA`, `FR` -> `fr-FR`, fallback -> tenant's `default_locale`).

**Fallback Hierarchy**:
$$\text{Requested Locale } (\text{e.g., } \texttt{ar-EG}) \rightarrow \text{Language Root } (\texttt{ar}) \rightarrow \text{Tenant Default Locale} \rightarrow \texttt{en-US}$$

### 1.2 Bidirectional Layout Mirroring (`RTL` & `LTR`) in Universal Expo
* Every `/v1/sdui/*` response returns `"locale": "ar-EG"` and `"direction": "rtl" | "ltr"`.
* On static Web (`npx expo export --platform web`), `<html lang="ar-EG" dir="rtl">` updates dynamically and loads locale-specific typography (`Cairo` / `Tajawal` for Arabic, `Inter` for Latin scripts).
* On iOS, Android, and Web, all Universal Expo SDUI components use logical start/end flex properties (`paddingStart`, `paddingEnd`, `marginStart`, `textAlign: "auto"`) so toggling between Arabic and English mirrors the layout instantaneously without restarting the app binary.

### 1.3 Multilingual Catalog, Variant Maps & Localized SEO Slugs in DynamoDB
* Product and category items in `SomeCommerceTable` store localized maps:
  * `titles_i18n: { "ar-EG": "كرسي مكتب طبي", "en-US": "Ergonomic Office Chair", "fr-FR": "Chaise de bureau ergonomique" }`
  * `descriptions_i18n`, `seo_slugs_i18n`, and `variant_options_i18n`.
* Localized SEO slug index (`GSI2PK = SLUG#<locale>#<slug>`, `GSI2SK = PRODUCT#<pid>`) allows `/ar/products/كرسي-مكتب-طبي` and `/en/products/ergonomic-office-chair` to resolve to the same product while serving localized `<title>`, OpenGraph tags, and `<link rel="alternate" hreflang="..." />` headers at the CloudFront edge.

### 1.4 ICU MessageFormat Translation Bundles (`I18N#<locale>#<namespace>`)
* UI strings, validation messages, and plural/currency rules are stored as ICU MessageFormat dictionaries in DynamoDB (`PK = TENANT#<tid>`, `SK = I18N#<locale>#<namespace>`) and cached at CloudFront and in Lambda memory.
* Merchants can edit translations live in the Admin Dashboard without redeploying the backend or rebuilding the static Expo web app.

### 1.5 Multilingual Transactional Notifications via [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
* Every `ORDER#<oid>` and `USER#<cognito_sub>` stores `preferred_locale`.
* When `fulfillment-worker` or `durable-orchestrator` dispatches an SMS or Mobile Push notification via Amazon SNS (e.g., Upfront COD Deposit link, [Bosta](https://docs.bosta.co/)/[Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) tracking link, or B2B Net-30 invoice reminder), `crates/notify-sns` renders the ICU template in the recipient's language.

### 1.6 Bilingual Commercial Invoices & Localized API Validation Errors
* All Rust API errors return a machine-readable `code` alongside a localized `user_message` matching `Accept-Language`.
* Cross-border shipments ([Aramex](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform) / [DHL Express](https://developer.dhl.com/)) and B2B tax receipts generate bilingual (`Arabic + English`) or target-locale PDFs.

## 2. SDUI JSON Schema Example (Localized Arabic RTL Checkout)

```json
{
  "schema_version": "1.0",
  "route": "/checkout",
  "locale": "ar-EG",
  "direction": "rtl",
  "persona": "B2C",
  "theme_tokens": {
    "primary_color": "#0F766E",
    "background_color": "#F8FAFC",
    "font_family": "Cairo"
  },
  "blocks": [
    {
      "id": "address_block",
      "type": "LocalizedAddressFormBlock",
      "props": {
        "country_code": "EG",
        "title": "عنوان التوصيل",
        "fields": ["governorate", "city_district", "street_address", "landmark", "phone_otp_verified"],
        "fee_lookup_endpoint": "/v1/rates/calculate"
      }
    },
    {
      "id": "shipping_selector",
      "type": "CarrierRateSelectorBlock",
      "props": {
        "title": "طريقة الشحن",
        "available_carriers": ["bosta", "aramex", "custom_zone"],
        "show_estimated_delivery": true
      }
    },
    {
      "id": "cod_deposit_summary",
      "type": "CodDepositSummaryCard",
      "props": {
        "enabled": true,
        "deposit_rule_label": "ادفع مصاريف الشحن الآن (80 ج.م) والباقي عند الاستلام (800 ج.م)",
        "pay_now_gateways": ["paymob_wallet", "paymob_card", "stripe"],
        "carrier_balance_provider": "bosta"
      }
    }
  ]
}
```

## 3. Core Universal SDUI Component Registry

| Component `type` | Persona Scope | Multilingual & RTL/LTR Behavior |
| :--- | :--- | :--- |
| `HeroBannerBlock` | `B2C`, `B2B` | Mirrors CTA placement and text alignment for RTL (`ar`) vs. LTR (`en`, `fr`, `de`) and loads locale-specific campaign artwork. |
| `ProductGridBlock` | `B2C`, `B2B` | Displays localized product titles, localized currency formatting, and localized stock/MOQ badges. |
| `B2BBulkVariantMatrix` | `B2B` | Renders localized variant option names (`اللون`/`المقاس` vs. `Color`/`Size`) and volume-tier discount tables. |
| `LocalizedAddressFormBlock` | `B2C`, `B2B` | Dynamically switches between `Governorate/District/Landmark` (Egypt/MENA) and `State/Province + Postal Code` (US/EU/UK). |
| `CarrierRateSelectorBlock` | `B2C`, `B2B` | Displays localized carrier names and delivery SLA estimates from Bosta, Aramex, DHL Express, Shippo, EasyPost, or custom zone tables. |
| `CodDepositSummaryCard` | `B2C`, `B2B` | Formats `Pay Now Deposit` vs. `Pay on Delivery Balance` in the shopper's active language and currency. |
| `ShipmentTrackerBlock` | `B2C`, `B2B` | Translates carrier webhook states (`In Transit`, `Out for Delivery`, `Delivered`) into the shopper's active language. |
| `CustomerLicenseVaultBlock` | `B2C`, `B2B` | Displays localized download instructions, Ed25519 `.lic` certificates, and B2B seat assignment controls. |
