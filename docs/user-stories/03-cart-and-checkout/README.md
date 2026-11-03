# Module 03: Cart & Checkout

> **Slice**: v1.0 · **Sprint**: 1.2 · **Stories**: US-3.1.1 – US-3.1.4

## Overview

Covers offline-first cart management via WatermelonDB, multi-vendor cart grouping, multi-step checkout flow, and address management with governorate-based rate estimation.

## Pages

| Page Route | Access | Direction | Primary Hook |
|:-----------|:-------|:----------|:-------------|
| `/[locale]/cart` | Public / Auth | RTL / LTR | `useOfflineCart` |
| `/[locale]/checkout` | Authenticated | RTL / LTR | `useSplitCodCheckout` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| POST | `/v1/cart/items` | `checkout-webhooks-api` | Add item to server cart |
| PUT | `/v1/cart/items/:sku` | `checkout-webhooks-api` | Update item quantity |
| DELETE | `/v1/cart/items/:sku` | `checkout-webhooks-api` | Remove item from cart |
| POST | `/v1/cart/bulk-items` | `checkout-webhooks-api` | B2B bulk matrix add |
| POST | `/v1/rates/calculate` | `checkout-webhooks-api` | Shipping + COD rate calculation |
| POST | `/v1/checkout/session` | `checkout-webhooks-api` | Create checkout payment session |
| POST | `/v1/sync/push` | `storefront-sdui-api` | Sync offline cart changes |

---

## User Stories Catalog

This module contains **4 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-3.1.1](us-3.1.1-offline-first-cart-with-watermelondb-sync.md)** | Offline-First Cart with WatermelonDB Sync | Shopper on a mobile device with intermittent connectivity | Sprint 1.2 | [View Specification →](us-3.1.1-offline-first-cart-with-watermelondb-sync.md) |
| **[US-3.1.2](us-3.1.2-multi-vendor-cart-grouping-shipping-estimation.md)** | Multi-Vendor Cart Grouping & Shipping Estimation | Shopper with items from multiple vendors in my cart | Sprint 1.2 | [View Specification →](us-3.1.2-multi-vendor-cart-grouping-shipping-estimation.md) |
| **[US-3.1.3](us-3.1.3-multi-step-checkout-flow.md)** | Multi-Step Checkout Flow | authenticated Shopper | Sprint 1.2 | [View Specification →](us-3.1.3-multi-step-checkout-flow.md) |
| **[US-3.1.4](us-3.1.4-localized-address-management.md)** | Localized Address Management | Customer in Egypt/MENA or internationally | Sprint 1.2 | [View Specification →](us-3.1.4-localized-address-management.md) |

---

## Story Summaries

#### [US-3.1.1: Offline-First Cart with WatermelonDB Sync](us-3.1.1-offline-first-cart-with-watermelondb-sync.md)
- **Target Persona**: Shopper on a mobile device with intermittent connectivity
- **Summary**: Offline-First Cart with WatermelonDB Sync
- **Specification**: [`us-3.1.1-offline-first-cart-with-watermelondb-sync.md`](us-3.1.1-offline-first-cart-with-watermelondb-sync.md)

#### [US-3.1.2: Multi-Vendor Cart Grouping & Shipping Estimation](us-3.1.2-multi-vendor-cart-grouping-shipping-estimation.md)
- **Target Persona**: Shopper with items from multiple vendors in my cart
- **Summary**: Multi-Vendor Cart Grouping & Shipping Estimation
- **Specification**: [`us-3.1.2-multi-vendor-cart-grouping-shipping-estimation.md`](us-3.1.2-multi-vendor-cart-grouping-shipping-estimation.md)

#### [US-3.1.3: Multi-Step Checkout Flow](us-3.1.3-multi-step-checkout-flow.md)
- **Target Persona**: authenticated Shopper
- **Summary**: Multi-Step Checkout Flow
- **Specification**: [`us-3.1.3-multi-step-checkout-flow.md`](us-3.1.3-multi-step-checkout-flow.md)

#### [US-3.1.4: Localized Address Management](us-3.1.4-localized-address-management.md)
- **Target Persona**: Customer in Egypt/MENA or internationally
- **Summary**: Localized Address Management
- **Specification**: [`us-3.1.4-localized-address-management.md`](us-3.1.4-localized-address-management.md)


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
