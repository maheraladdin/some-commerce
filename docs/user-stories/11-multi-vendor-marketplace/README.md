# Module 11: Multi-Vendor Marketplace

> **Slice**: v4.0 · **Sprints**: 4.1, 4.2 · **Stories**: US-11.1.1 – US-11.1.4

## Overview

Covers vendor onboarding, RBAC-scoped catalog management, automatic sub-order splitting, double-entry escrow ledger, and the vendor portal dashboard.

## Pages

| Page Route | Access | Primary Hook |
|:-----------|:-------|:-------------|
| `/[locale]/vendor/dashboard` | VENDOR | `useVendorPortal` |
| `/[locale]/vendor/products/new` | VENDOR | `useVendorProductEditor` |
| `/[locale]/cart` | Public / Auth | `useOfflineCart` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| POST | `/v1/vendor/onboarding` | `admin-vendor-api` | Vendor registration |
| GET | `/v1/vendor/sub-orders` | `admin-vendor-api` | Vendor's sub-orders |
| GET | `/v1/vendor/escrow` | `admin-vendor-api` | Escrow ledger balance |
| POST | `/v1/vendor/products` | `admin-vendor-api` | Vendor product CRUD |
| POST | `/v1/vendor/payout-request` | `admin-vendor-api` | Request payout |

---

## User Stories Catalog

This module contains **4 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-11.1.1](us-11.1.1-vendor-onboarding-rbac-scoped-catalog.md)** | Vendor Onboarding & RBAC-Scoped Catalog | Marketplace Vendor | Sprint 4.1 / 4.2 | [View Specification →](us-11.1.1-vendor-onboarding-rbac-scoped-catalog.md) |
| **[US-11.1.2](us-11.1.2-automatic-sub-order-splitting-at-checkout.md)** | Automatic Sub-Order Splitting at Checkout | Shopper with items from multiple vendors | Sprint 4.1 / 4.2 | [View Specification →](us-11.1.2-automatic-sub-order-splitting-at-checkout.md) |
| **[US-11.1.3](us-11.1.3-double-entry-escrow-ledger-vendor-payouts.md)** | Double-Entry Escrow Ledger & Vendor Payouts | Marketplace Operator and Vendor | Sprint 4.1 / 4.2 | [View Specification →](us-11.1.3-double-entry-escrow-ledger-vendor-payouts.md) |
| **[US-11.1.4](us-11.1.4-vendor-portal-dashboard.md)** | Vendor Portal Dashboard | Vendor | Sprint 4.1 / 4.2 | [View Specification →](us-11.1.4-vendor-portal-dashboard.md) |

---

## Story Summaries

#### [US-11.1.1: Vendor Onboarding & RBAC-Scoped Catalog](us-11.1.1-vendor-onboarding-rbac-scoped-catalog.md)
- **Target Persona**: Marketplace Vendor
- **Summary**: register
- **Specification**: [`us-11.1.1-vendor-onboarding-rbac-scoped-catalog.md`](us-11.1.1-vendor-onboarding-rbac-scoped-catalog.md)

#### [US-11.1.2: Automatic Sub-Order Splitting at Checkout](us-11.1.2-automatic-sub-order-splitting-at-checkout.md)
- **Target Persona**: Shopper with items from multiple vendors
- **Summary**: Automatic Sub-Order Splitting at Checkout
- **Specification**: [`us-11.1.2-automatic-sub-order-splitting-at-checkout.md`](us-11.1.2-automatic-sub-order-splitting-at-checkout.md)

#### [US-11.1.3: Double-Entry Escrow Ledger & Vendor Payouts](us-11.1.3-double-entry-escrow-ledger-vendor-payouts.md)
- **Target Persona**: Marketplace Operator and Vendor
- **Summary**: Double-Entry Escrow Ledger & Vendor Payouts
- **Specification**: [`us-11.1.3-double-entry-escrow-ledger-vendor-payouts.md`](us-11.1.3-double-entry-escrow-ledger-vendor-payouts.md)

#### [US-11.1.4: Vendor Portal Dashboard](us-11.1.4-vendor-portal-dashboard.md)
- **Target Persona**: Vendor
- **Summary**: Vendor Portal Dashboard
- **Specification**: [`us-11.1.4-vendor-portal-dashboard.md`](us-11.1.4-vendor-portal-dashboard.md)


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
