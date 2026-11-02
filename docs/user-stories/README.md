# some-commerce: User Stories — Master Index

> **Total Modules**: 13 · **Total User Stories**: 46 · **Total Sprints**: 12 (across 6 slices)

This directory contains all user stories for the `some-commerce` platform, organized by functional module. Each module has its own README with detailed user stories including:

- **User Story Statement** (As a / I want / So that)
- **Acceptance Criteria** (Gherkin-style `Given/When/Then`)
- **Test Cases** (covering happy path, edge cases, error handling, concurrency, and security)
- **Activity Diagram** (Mermaid `flowchart TD`)
- **Pages & Endpoints** (routes, API endpoints, and how they link together)

---

## Module Directory

| # | Module | Stories | Slice | Description |
|:--|:-------|:--------|:------|:------------|
| 01 | [Auth & Onboarding](./01-auth-and-onboarding/README.md) | US-1.1.1 – US-1.1.4 | v1.0 | Cognito auth, OTP, Passkeys, Social OIDC, B2B org registration, JWT enrichment |
| 02 | [Storefront & Catalog](./02-storefront-and-catalog/README.md) | US-2.1.1 – US-2.1.5 | v1.0 | SDUI storefront, N-level taxonomy, brands, properties, dual-tier search, PDP |
| 03 | [Cart & Checkout](./03-cart-and-checkout/README.md) | US-3.1.1 – US-3.1.4 | v1.0 | Offline cart, multi-vendor grouping, checkout flow, address management |
| 04 | [Payments & COD](./04-payments-and-cod/README.md) | US-4.1.1 – US-4.1.5 | v1.0 / v4.0 | Paymob, Stripe, full COD, deposit-COD, BTCPay crypto payments |
| 05 | [Fulfillment & Shipping](./05-fulfillment-and-shipping/README.md) | US-5.1.1 – US-5.1.4 | v1.0 / v3.0 / v4.0 | Bosta domestic, Aramex/DHL cross-border, Shippo/EasyPost global, SNS notifications |
| 06 | [Orders & Returns](./06-orders-and-returns/README.md) | US-6.1.1 – US-6.1.4 | v1.0 / v4.0 | Order tracking, order history, RMA returns, refund processing |
| 07 | [Customer Account](./07-customer-account/README.md) | US-7.1.1 – US-7.1.4 | v1.0 | Profile management, address book, notification preferences, wishlist |
| 08 | [WebMCP & AI Assistant](./08-webmcp-and-ai/README.md) | US-8.1.1 – US-8.1.3 | v1.0 | Customer shopping assistant, admin copilot, Bedrock integration |
| 09 | [Digital Products & Licensing](./09-digital-products-and-licensing/README.md) | US-9.1.1 – US-9.1.4 | v2.0 | Digital asset delivery, 6-mode licensing engine, SDKs, license vault |
| 10 | [B2B Wholesale](./10-b2b-wholesale/README.md) | US-10.1.1 – US-10.1.4 | v3.0 | B2B onboarding, tiered pricing, MOQ, RFQ negotiation, net-terms, LAN proxy |
| 11 | [Multi-Vendor Marketplace](./11-multi-vendor-marketplace/README.md) | US-11.1.1 – US-11.1.4 | v4.0 | Vendor onboarding, sub-order splitting, escrow payouts, vendor portal |
| 12 | [Admin & SDUI Studio](./12-admin-and-sdui-studio/README.md) | US-12.1.1 – US-12.1.3 | v5.0 / v6.0 | Dual-edition deployment, SDUI visual studio, white-label mobile pipeline |
| 13 | [Deployment & AWS Marketplace](./13-deployment-and-aws-marketplace/README.md) | US-13.1.1 – US-13.1.3 | v5.0 | CDK stacks, Marketplace packaging, FTR audit, metering |

---

## Cross-Module Page Map

All pages live in a single Expo Router tree prefixed by `/[locale]`:

| Page Route | Module(s) | Primary Hook |
|:-----------|:----------|:-------------|
| `/[locale]/index` | 02, 08 | `useSduiScreen` |
| `/[locale]/c/[...category_slug]` | 02, 08 | `useCatalogSearchAndFacets` |
| `/[locale]/b/[brand_slug]` | 02 | `useBrandCatalog` |
| `/[locale]/products/[slug]` | 02, 03, 10 | `useProductConfigurator` |
| `/[locale]/compare` | 08 | `useWebMcpComparison` |
| `/[locale]/(auth)/sign-in` | 01 | `useCognitoAuth` |
| `/[locale]/(auth)/b2b-register` | 01, 10 | `useB2BOnboarding` |
| `/[locale]/cart` | 03 | `useOfflineCart` |
| `/[locale]/checkout` | 03, 04, 05 | `useSplitCodCheckout` |
| `/[locale]/orders/[order_id]/confirmation` | 06 | `useOrderLiveTracker` |
| `/[locale]/account/profile` | 07 | `useCustomerAccount` |
| `/[locale]/account/orders` | 06 | `useOrderHistory` |
| `/[locale]/account/wishlist` | 07 | `useWishlist` |
| `/[locale]/account/licenses` | 09 | `useDigitalLicenseVault` |
| `/[locale]/b2b/rfq` | 10 | `useB2BRfqNegotiation` |
| `/[locale]/vendor/dashboard` | 11 | `useVendorPortal` |
| `/[locale]/vendor/products/new` | 02, 11 | `useVendorProductEditor` |
| `/[locale]/admin/catalog-taxonomy` | 02, 12 | `useAdminTaxonomyBuilder` |
| `/[locale]/admin/settings-gateways` | 04, 12 | `useAdminGatewayConfig` |
| `/[locale]/admin/sdui-studio` | 12 | `useAdminSduiStudio` |
| `/[locale]/admin/orders` | 06 | `useAdminOrderManagement` |

---

## API Endpoint Map

| Lambda Binary | Base Path | Modules |
|:--------------|:----------|:--------|
| `storefront-sdui-api` | `/v1/sdui/*`, `/v1/search/*`, `/v1/sync/*`, `/v1/mcp/customer` | 02, 07, 08 |
| `checkout-webhooks-api` | `/v1/checkout/*`, `/v1/rates/*`, `/v1/webhooks/*`, `/v1/cart/*` | 03, 04, 05 |
| `admin-vendor-api` | `/v1/admin/*`, `/v1/vendor/*`, `/v1/mcp/admin` | 01, 02, 11, 12 |
| `fulfillment-worker` | Event-driven (DynamoDB Streams, EventBridge) | 05, 06, 09 |
| `durable-orchestrator` | `/v1/b2b/rfq/*`, durable state machines | 04, 06, 10, 11 |

---

## How to Navigate

1. **By Feature**: Browse the module directories above for domain-specific user stories
2. **By Sprint**: See [`docs/sprints/`](../sprints/) for time-boxed sprint breakdowns
3. **By Page/Route**: Use the Cross-Module Page Map above to find which stories affect a given page
4. **By API**: Use the API Endpoint Map to find which stories touch a given backend service
5. **By Autonomous Agent Slicing**: See the [7-PR Vertical Slicing Standard](../sprints/README.md#the-7-pr-vertical-slicing-standard) to execute any story via the 3-agent parallel workflow (Microkernel $\rightarrow$ DB Schema $\rightarrow$ Repositories/Cache $\rightarrow$ Axum Handlers $\rightarrow$ Axios/WatermelonDB $\rightarrow$ Hooks/Native Modules $\rightarrow$ UI Platform-Adaptive).
