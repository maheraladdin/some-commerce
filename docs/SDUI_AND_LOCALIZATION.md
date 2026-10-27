# Server-Driven UI (SDUI) & Localization Engine Specification

## 1. Universal Expo Architecture (Static Web on S3/CloudFront + Native Mobile)

`some-commerce` uses a single [Expo](https://docs.expo.dev/) + [Expo Router](https://docs.expo.dev/router/introduction/) codebase (`apps/universal-store`) that targets **Web, iOS, and Android**:

* **Static Web Export (`npx expo export --platform web`)**: Compiles all routes into static `.html`, `.css`, and `.js` bundles hosted in a private [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) bucket behind [Amazon CloudFront (OAC)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html).
* **Sub-Millisecond Edge Routing**: A [CloudFront Function](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/example_cloudfront_functions_url_rewrite_single_page_apps_section.html) rewrites dynamic URLs (`/products/ergonomic-chair` -> `/products/[slug].html`) and forwards `CloudFront-Viewer-Country` and `Accept-Language` headers to `/v1/sdui/*`.
* **Native Mobile Apps & Amazon SNS Push**: The exact same `<SduiRenderer />` component tree compiles into native iOS and Android binaries and registers device push tokens with [Amazon SNS Mobile Push](https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-application-as-subscriber.html).

## 2. Context-Aware SDUI Resolution (`SDUI#<route>#<persona>#<locale>`)

When the universal Expo app requests `GET /v1/sdui/page?route=/products/ergonomic-chair`, `storefront-sdui-api` resolves the response using three dimensions:

1. **Persona (from [Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html) JWT Claims)**:
   * Anonymous or `B2C_CUSTOMER` -> Resolves `persona = B2C` (retail promotional banners, single-unit add-to-cart, instant wallet checkout).
   * Authenticated `B2B_BUYER` or `B2B_ORG_ADMIN` -> Resolves `persona = B2B` (bulk variant SKU matrix, MOQ badges, volume tier table, RFQ drawer, and Net-30 credit meter).
2. **Locale & Direction (`Accept-Language` / User Preference)**:
   * Arabic (`ar-EG`, `ar-SA`) -> Returns `direction: "rtl"`, Arabic font tokens (`Cairo` / `Tajawal`), and localized Arabic strings.
   * English (`en-US`, `en-GB`) -> Returns `direction: "ltr"`, Latin font tokens (`Inter`), and localized English strings.
3. **Geographic Region (`CloudFront-Viewer-Country`)**:
   * Injects localized currency symbols, regional payment badges (e.g., Vodafone Cash, InstaPay, Meeza, ValU, and Bosta Split COD in Egypt; Apple Pay, Stripe, and Shippo/EasyPost rate-shopping cards in the US/EU), and regional fee estimates (`LOCALE_FEES#<country>#<zone>`).

## 3. SDUI JSON Schema Example

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
        "fields": ["governorate", "city_district", "street_address", "landmark", "phone_otp_verified"],
        "fee_lookup_endpoint": "/v1/rates/quote"
      }
    },
    {
      "id": "shipping_selector",
      "type": "CarrierRateSelectorBlock",
      "props": {
        "available_carriers": ["bosta", "aramex", "custom_zone"],
        "show_estimated_delivery": true
      }
    },
    {
      "id": "cod_deposit_summary",
      "type": "CodDepositSummaryCard",
      "props": {
        "enabled": true,
        "deposit_rule_label": "ادفع مصاريف الشحن الآن والباقي عند الاستلام",
        "pay_now_gateways": ["paymob_wallet", "paymob_card", "stripe"],
        "carrier_balance_provider": "bosta"
      }
    }
  ]
}
```

## 4. Core Universal SDUI Component Registry

| Component `type` | Persona Scope | Description |
| :--- | :--- | :--- |
| `HeroBannerBlock` | `B2C`, `B2B` | Responsive promotional banner with RTL/LTR text alignment and deep-link CTA buttons. |
| `ProductGridBlock` | `B2C`, `B2B` | Paginated/infinite grid displaying localized prices, stock badges, and digital/physical tags. |
| `B2BBulkVariantMatrix` | `B2B` | Multi-SKU quantity input table with live volume-tier discount calculation and MOQ validation. |
| `LocalizedAddressFormBlock` | `B2C`, `B2B` | Adapts inputs per country (`Governorate/District/Landmark` for EG/MENA vs. `State/PostalCode` for US/EU). |
| `CarrierRateSelectorBlock` | `B2C`, `B2B` | Displays live delivery quotes from Bosta, Aramex, DHL Express, Shippo, EasyPost, or custom zone tables. |
| `CodDepositSummaryCard` | `B2C`, `B2B` | Breaks down `Pay Now Deposit` (via Paymob/Stripe) vs. `Pay on Delivery Balance` (collected by Bosta/Aramex). |
| `ShipmentTrackerBlock` | `B2C`, `B2B` | Real-time step indicator driven by Bosta, Aramex, DHL, Shippo, EasyPost, and Amazon SNS push updates. |
| `CustomerLicenseVaultBlock` | `B2C`, `B2B` | Displays Ed25519 `.lic` downloads, active hardware fingerprints, and B2B floating seat assignments. |
