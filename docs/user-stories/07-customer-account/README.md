# Module 07: Customer Account

> **Slice**: v1.0 · **Sprint**: 1.1 · **Stories**: US-7.1.1 – US-7.1.4

## Overview

Covers customer profile management, address book, notification preferences, and wishlist functionality.

## Pages

| Page Route | Access | Primary Hook |
|:-----------|:-------|:-------------|
| `/[locale]/account/profile` | Auth | `useCustomerAccount` |
| `/[locale]/account/wishlist` | Auth | `useWishlist` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| GET | `/v1/account/profile` | `storefront-sdui-api` | Get profile |
| PUT | `/v1/account/profile` | `storefront-sdui-api` | Update profile |
| GET | `/v1/account/addresses` | `storefront-sdui-api` | List addresses |
| POST | `/v1/account/addresses` | `storefront-sdui-api` | Add address |
| PUT | `/v1/account/addresses/:id` | `storefront-sdui-api` | Update address |
| DELETE | `/v1/account/addresses/:id` | `storefront-sdui-api` | Delete address |
| GET | `/v1/account/wishlist` | `storefront-sdui-api` | Get wishlist |
| POST | `/v1/account/wishlist/:productId` | `storefront-sdui-api` | Add to wishlist |
| DELETE | `/v1/account/wishlist/:productId` | `storefront-sdui-api` | Remove from wishlist |
| PUT | `/v1/account/notifications` | `storefront-sdui-api` | Update notification prefs |

---

## User Stories Catalog

This module contains **4 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 10-PR implementation slice plan (10-Pillar System Architecture).

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-7.1.1](us-7.1.1-customer-profile-management.md)** | Customer Profile Management | registered Customer | Sprint 1.1 | [View Specification →](us-7.1.1-customer-profile-management.md) |
| **[US-7.1.2](us-7.1.2-address-book-management.md)** | Address Book Management | Customer | Sprint 1.1 | [View Specification →](us-7.1.2-address-book-management.md) |
| **[US-7.1.3](us-7.1.3-notification-preferences.md)** | Notification Preferences | Customer | Sprint 1.1 | [View Specification →](us-7.1.3-notification-preferences.md) |
| **[US-7.1.4](us-7.1.4-wishlist.md)** | Wishlist | Customer | Sprint 1.1 | [View Specification →](us-7.1.4-wishlist.md) |

---

## Story Summaries

#### [US-7.1.1: Customer Profile Management](us-7.1.1-customer-profile-management.md)
- **Target Persona**: registered Customer
- **Summary**: view and edit my profile including name
- **Specification**: [`us-7.1.1-customer-profile-management.md`](us-7.1.1-customer-profile-management.md)

#### [US-7.1.2: Address Book Management](us-7.1.2-address-book-management.md)
- **Target Persona**: Customer
- **Summary**: manage multiple delivery addresses with a default address for quicker checkout
- **Specification**: [`us-7.1.2-address-book-management.md`](us-7.1.2-address-book-management.md)

#### [US-7.1.3: Notification Preferences](us-7.1.3-notification-preferences.md)
- **Target Persona**: Customer
- **Summary**: control which notifications I receive (push
- **Specification**: [`us-7.1.3-notification-preferences.md`](us-7.1.3-notification-preferences.md)

#### [US-7.1.4: Wishlist](us-7.1.4-wishlist.md)
- **Target Persona**: Customer
- **Summary**: save products to a wishlist for later consideration
- **Specification**: [`us-7.1.4-wishlist.md`](us-7.1.4-wishlist.md)


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
