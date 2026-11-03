# Module 02: Storefront & Catalog

> **Slice**: v1.0 · **Sprint**: 1.1 · **Stories**: US-2.1.1 – US-2.1.5

## Overview

This module covers the multilingual SDUI storefront rendering, N-level category taxonomy, brand management, custom product properties, dual-tier catalog search (Elasticsearch + DynamoDB fallback), and the Product Detail Page (PDP) with variant configuration.

## Pages

| Page Route | Access | Direction | Primary Hook |
|:-----------|:-------|:----------|:-------------|
| `/[locale]/index` | Public | RTL / LTR | `useSduiScreen` |
| `/[locale]/c/[...category_slug]` | Public | RTL / LTR | `useCatalogSearchAndFacets` |
| `/[locale]/b/[brand_slug]` | Public | RTL / LTR | `useBrandCatalog` |
| `/[locale]/products/[slug]` | Public | RTL / LTR | `useProductConfigurator` |
| `/[locale]/admin/catalog-taxonomy` | STORE_ADMIN | RTL / LTR | `useAdminTaxonomyBuilder` |
| `/[locale]/vendor/products/new` | STORE_ADMIN / VENDOR | RTL / LTR | `useVendorProductEditor` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| GET | `/v1/sdui/page?route=&locale=` | `storefront-sdui-api` | Fetch SDUI page layout with ETag |
| GET | `/v1/search?q=&category=&brand=&props=` | `storefront-sdui-api` | Dual-tier catalog search |
| GET | `/v1/products/:slug` | `storefront-sdui-api` | Product detail + variants |
| GET | `/v1/sync/pull?last_pulled_at=` | `storefront-sdui-api` | WatermelonDB delta sync |
| POST | `/v1/admin/taxonomy/nodes` | `admin-vendor-api` | Create/update category nodes |
| POST | `/v1/admin/properties` | `admin-vendor-api` | Create/update property definitions |
| POST | `/v1/admin/brands` | `admin-vendor-api` | Create/update brands |
| POST | `/v1/admin/products` | `admin-vendor-api` | Create/update products |

---

## User Stories Catalog

This module contains **5 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 10-PR implementation slice plan (10-Pillar System Architecture).

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-2.1.1](us-2.1.1-multilingual-sdui-storefront-with-instant-watermelondb-rendering.md)** | Multilingual SDUI Storefront with Instant WatermelonDB Rendering | global or regional shopper browsing in Arabic | Sprint 1.1 | [View Specification →](us-2.1.1-multilingual-sdui-storefront-with-instant-watermelondb-rendering.md) |
| **[US-2.1.2](us-2.1.2-unlimited-n-level-category-taxonomy-brand-management.md)** | Unlimited N-Level Category Taxonomy & Brand Management | Store Administrator | Sprint 1.1 | [View Specification →](us-2.1.2-unlimited-n-level-category-taxonomy-brand-management.md) |
| **[US-2.1.3](us-2.1.3-admin-customizable-product-properties-filter-widgets.md)** | Admin-Customizable Product Properties & Filter Widgets | Store Administrator | Sprint 1.1 | [View Specification →](us-2.1.3-admin-customizable-product-properties-filter-widgets.md) |
| **[US-2.1.4](us-2.1.4-dual-tier-catalog-search-with-nested-faceted-filtration.md)** | Dual-Tier Catalog Search with Nested Faceted Filtration | Shopper browsing a category page | Sprint 1.1 | [View Specification →](us-2.1.4-dual-tier-catalog-search-with-nested-faceted-filtration.md) |
| **[US-2.1.5](us-2.1.5-product-detail-page-with-variant-configuration.md)** | Product Detail Page with Variant Configuration | Shopper viewing a product | Sprint 1.1 | [View Specification →](us-2.1.5-product-detail-page-with-variant-configuration.md) |

---

## Story Summaries

#### [US-2.1.1: Multilingual SDUI Storefront with Instant WatermelonDB Rendering](us-2.1.1-multilingual-sdui-storefront-with-instant-watermelondb-rendering.md)
- **Target Persona**: global or regional shopper browsing in Arabic
- **Summary**: Multilingual SDUI Storefront with Instant WatermelonDB Rendering
- **Specification**: [`us-2.1.1-multilingual-sdui-storefront-with-instant-watermelondb-rendering.md`](us-2.1.1-multilingual-sdui-storefront-with-instant-watermelondb-rendering.md)

#### [US-2.1.2: Unlimited N-Level Category Taxonomy & Brand Management](us-2.1.2-unlimited-n-level-category-taxonomy-brand-management.md)
- **Target Persona**: Store Administrator
- **Summary**: create an unlimited N-level hierarchy of localized categories and sub-categories (e.g.
- **Specification**: [`us-2.1.2-unlimited-n-level-category-taxonomy-brand-management.md`](us-2.1.2-unlimited-n-level-category-taxonomy-brand-management.md)

#### [US-2.1.3: Admin-Customizable Product Properties & Filter Widgets](us-2.1.3-admin-customizable-product-properties-filter-widgets.md)
- **Target Persona**: Store Administrator
- **Summary**: define custom filterable product properties (e.g.
- **Specification**: [`us-2.1.3-admin-customizable-product-properties-filter-widgets.md`](us-2.1.3-admin-customizable-product-properties-filter-widgets.md)

#### [US-2.1.4: Dual-Tier Catalog Search with Nested Faceted Filtration](us-2.1.4-dual-tier-catalog-search-with-nested-faceted-filtration.md)
- **Target Persona**: Shopper browsing a category page
- **Summary**: filter products by category
- **Specification**: [`us-2.1.4-dual-tier-catalog-search-with-nested-faceted-filtration.md`](us-2.1.4-dual-tier-catalog-search-with-nested-faceted-filtration.md)

#### [US-2.1.5: Product Detail Page with Variant Configuration](us-2.1.5-product-detail-page-with-variant-configuration.md)
- **Target Persona**: Shopper viewing a product
- **Summary**: see a rich product detail page with a media gallery
- **Specification**: [`us-2.1.5-product-detail-page-with-variant-configuration.md`](us-2.1.5-product-detail-page-with-variant-configuration.md)


---

## Autonomous Agent Implementation Standard (10-Pillar System Architecture)

Every user story in this module is executed by an autonomous AI agent across the standardized **10-PR vertical slice framework** directly matching the [10-Pillar System Architecture](../../SYSTEM_ARCHITECTURE.md):

```
[PR 1: Kernel Core] ──> [PR 2: DB Schema] ──> [PR 3: Repositories] ──> [PR 4: L2 Redis] ──> [PR 5: L1 Moka]
                                                                                                 │
[PR 10: Platform UI] <── [PR 9: Headless Hooks] <── [PR 8: WatermelonDB] <── [PR 7: TanStack Query] <── [PR 6: ETag & Axum]
```

1. **PR 1: Microkernel Domain Logic & Plugin Ports** (`crates/kernel-core`, `crates/plugins-*`) [Pillar 1]
2. **PR 2: Polyglot Database Schema Definitions** (`crates/db-schema`, `packages/watermelon-db`) [Pillar 2]
3. **PR 3: Repository Adapters & Infrastructure Connectors** (`crates/db-dynamo`, `crates/search-elastic`, `crates/notify-sns`, `crates/kms-vault`) [Pillar 3]
4. **PR 4: Distributed L2 Cache & Pub/Sub Invalidation Engine** (`crates/cache-tier`) [Pillar 4]
5. **PR 5: In-Process L1 Moka Cache & Request Coalescing** (`crates/cache-tier`) [Pillar 5]
6. **PR 6: HTTP ETag Protocol & Pure Axum Handlers** (`bins/*`, `crates/cache-tier`) [Pillar 6]
7. **PR 7: Frontend Server-State Caching & TanStack Query** (`packages/query-client`, `packages/api-client`) [Pillar 7]
8. **PR 8: Client-First Local Database & WatermelonDB Sync** (`packages/watermelon-db`, `apps/storefront/src/features/.../services/`) [Pillar 8]
9. **PR 9: Headless Custom Hooks & Logic Abstraction** (`packages/domain-hooks`, `apps/storefront/src/features/.../logic/`) [Pillar 9]
10. **PR 10: Platform-Adaptive UI Design & Native Modules** (`apps/storefront`, `packages/ui-primitives`, `modules/expo-*`) [Pillar 10]

---

## Navigation & Cross-References

- [← Back to Master User Stories Index](../README.md)
- [Sprint Schedule & 3-Agent Parallel Framework](../../sprints/README.md)
- [System Architecture & Multi-Tier Caching](../../SYSTEM_ARCHITECTURE.md)
- [Deployment & AWS Marketplace Guide](../../DEPLOYMENT_AND_AWS_MARKETPLACE.md)
