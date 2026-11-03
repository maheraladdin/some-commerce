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

This module contains **4 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

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
