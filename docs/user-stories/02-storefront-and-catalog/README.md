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

This module contains **5 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

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

## Autonomous Agent Implementation Standard

Every user story in this module is executed by an autonomous AI agent across the standardized **7-PR vertical slice framework**:

```
[PR 1: Kernel Core] ──> [PR 2: DB Schema] ──> [PR 3: Repo & Cache] ──> [PR 4: Axum API]
                                                                            │
[PR 7: Platform UI] <── [PR 6: Headless Hooks] <── [PR 5: Client Service & DB] <┘
```

1. **PR 1: Microkernel Logic** (`crates/kernel-core`)
2. **PR 2: Database Schema** (`crates/db-schema`)
3. **PR 3: Repository Handlers & Caching** (`crates/db-dynamo`, `crates/cache-tier`)
4. **PR 4: Axum Handlers & Middleware** (`bins/...`)
5. **PR 5: Client Services & Local Database** (`packages/api-client`, `packages/db-client`)
6. **PR 6: Headless Domain Hooks & Native Modules** (`packages/domain-hooks`, `modules/...`)
7. **PR 7: Platform-Adaptive UI** (`apps/storefront-mobile` with `@expo/ui`, `apps/storefront-web` with Tailwind CSS v4)

---

## Navigation & Cross-References

- [← Back to Master User Stories Index](../README.md)
- [Sprint Schedule & 3-Agent Parallel Framework](../../sprints/README.md)
- [System Architecture & Multi-Tier Caching](../../SYSTEM_ARCHITECTURE.md)
- [Deployment & AWS Marketplace Guide](../../DEPLOYMENT_AND_AWS_MARKETPLACE.md)
