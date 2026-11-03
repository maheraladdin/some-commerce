# Module 06: Orders & Returns

> **Slice**: v1.0 / v4.0 · **Sprints**: 1.2, 4.2 · **Stories**: US-6.1.1 – US-6.1.4

## Overview

Covers order tracking, order history, Return Merchandise Authorization (RMA), and refund processing.

## Pages

| Page Route | Access | Primary Hook |
|:-----------|:-------|:-------------|
| `/[locale]/orders/[order_id]/confirmation` | Auth | `useOrderLiveTracker` |
| `/[locale]/account/orders` | Auth | `useOrderHistory` |
| `/[locale]/admin/orders` | STORE_ADMIN | `useAdminOrderManagement` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| GET | `/v1/orders/:id` | `storefront-sdui-api` | Order detail with tracking |
| GET | `/v1/orders` | `storefront-sdui-api` | Customer order history |
| POST | `/v1/orders/:id/rma` | `durable-orchestrator` | Initiate RMA return |
| POST | `/v1/orders/:id/refund` | `checkout-webhooks-api` | Process refund |
| GET | `/v1/admin/orders` | `admin-vendor-api` | Admin order list + filters |
| PUT | `/v1/admin/orders/:id/status` | `admin-vendor-api` | Admin update order status |

---

## User Stories Catalog

This module contains **4 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-6.1.1](us-6.1.1-real-time-order-tracking-live-status-timeline.md)** | Real-Time Order Tracking & Live Status Timeline | Customer who has placed an order | Sprint 1.2 / 4.2 | [View Specification →](us-6.1.1-real-time-order-tracking-live-status-timeline.md) |
| **[US-6.1.2](us-6.1.2-customer-order-history-with-filtering.md)** | Customer Order History with Filtering | returning Customer | Sprint 1.2 / 4.2 | [View Specification →](us-6.1.2-customer-order-history-with-filtering.md) |
| **[US-6.1.3](us-6.1.3-return-merchandise-authorization-rma.md)** | Return Merchandise Authorization (RMA) | Customer within the return window | Sprint 1.2 / 4.2 | [View Specification →](us-6.1.3-return-merchandise-authorization-rma.md) |
| **[US-6.1.4](us-6.1.4-admin-order-management-dashboard.md)** | Admin Order Management Dashboard | Store Administrator | Sprint 1.2 / 4.2 | [View Specification →](us-6.1.4-admin-order-management-dashboard.md) |

---

## Story Summaries

#### [US-6.1.1: Real-Time Order Tracking & Live Status Timeline](us-6.1.1-real-time-order-tracking-live-status-timeline.md)
- **Target Persona**: Customer who has placed an order
- **Summary**: track my order in real-time with a visual status timeline and live carrier tracking map
- **Specification**: [`us-6.1.1-real-time-order-tracking-live-status-timeline.md`](us-6.1.1-real-time-order-tracking-live-status-timeline.md)

#### [US-6.1.2: Customer Order History with Filtering](us-6.1.2-customer-order-history-with-filtering.md)
- **Target Persona**: returning Customer
- **Summary**: view my complete order history with filters for status
- **Specification**: [`us-6.1.2-customer-order-history-with-filtering.md`](us-6.1.2-customer-order-history-with-filtering.md)

#### [US-6.1.3: Return Merchandise Authorization (RMA)](us-6.1.3-return-merchandise-authorization-rma.md)
- **Target Persona**: Customer within the return window
- **Summary**: initiate a return for one or more items from my order
- **Specification**: [`us-6.1.3-return-merchandise-authorization-rma.md`](us-6.1.3-return-merchandise-authorization-rma.md)

#### [US-6.1.4: Admin Order Management Dashboard](us-6.1.4-admin-order-management-dashboard.md)
- **Target Persona**: Store Administrator
- **Summary**: Admin Order Management Dashboard
- **Specification**: [`us-6.1.4-admin-order-management-dashboard.md`](us-6.1.4-admin-order-management-dashboard.md)


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
