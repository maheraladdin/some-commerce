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

This module contains **4 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 10-PR implementation slice plan (10-Pillar System Architecture).

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
