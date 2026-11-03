# Module 05: Fulfillment & Shipping

> **Slice**: v1.0 / v3.0 / v4.0 · **Sprints**: 1.2, 3.1, 4.1 · **Stories**: US-5.1.1 – US-5.1.4

## Overview

Covers domestic shipping (Bosta), cross-border express (Aramex/DHL), global multi-carrier aggregation (Shippo/EasyPost), and localized SNS push/SMS notifications at every fulfillment milestone.

## Pages

| Page Route | Access | Primary Hook |
|:-----------|:-------|:-------------|
| `/[locale]/orders/[order_id]/confirmation` | Auth | `useOrderLiveTracker` |
| `/[locale]/vendor/dashboard` | VENDOR | `useVendorPortal` |
| `/[locale]/checkout` | Auth | `useSplitCodCheckout` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| POST | `/v1/rates/calculate` | `checkout-webhooks-api` | Multi-carrier rate shopping |
| POST | `/v1/webhooks/bosta` | `checkout-webhooks-api` | Bosta delivery status webhook |
| POST | `/v1/webhooks/aramex` | `checkout-webhooks-api` | Aramex tracking webhook |
| POST | `/v1/webhooks/dhl` | `checkout-webhooks-api` | DHL Express webhook |
| — | DynamoDB Stream → EventBridge | `fulfillment-worker` | AWB booking + SNS dispatch |

---

## User Stories Catalog

This module contains **4 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 10-PR implementation slice plan (10-Pillar System Architecture).

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-5.1.1](us-5.1.1-domestic-shipping-via-bosta-with-cod-collection.md)** | Domestic Shipping via Bosta with COD Collection | Customer ordering within Egypt/KSA and the Store Operations Manager | Sprint 1.2 / 3.1 / 4.1 | [View Specification →](us-5.1.1-domestic-shipping-via-bosta-with-cod-collection.md) |
| **[US-5.1.2](us-5.1.2-cross-border-express-shipping-aramex-dhl.md)** | Cross-Border Express Shipping (Aramex & DHL) | Cross-Border Merchant and International Buyer | Sprint 1.2 / 3.1 / 4.1 | [View Specification →](us-5.1.2-cross-border-express-shipping-aramex-dhl.md) |
| **[US-5.1.3](us-5.1.3-global-multi-carrier-aggregation-shippo-easypost.md)** | Global Multi-Carrier Aggregation (Shippo & EasyPost) | Global Marketplace Operator | Sprint 1.2 / 3.1 / 4.1 | [View Specification →](us-5.1.3-global-multi-carrier-aggregation-shippo-easypost.md) |
| **[US-5.1.4](us-5.1.4-localized-sns-push-sms-notifications-at-every-milestone.md)** | Localized SNS Push & SMS Notifications at Every Milestone | Customer | Sprint 1.2 / 3.1 / 4.1 | [View Specification →](us-5.1.4-localized-sns-push-sms-notifications-at-every-milestone.md) |

---

## Story Summaries

#### [US-5.1.1: Domestic Shipping via Bosta with COD Collection](us-5.1.1-domestic-shipping-via-bosta-with-cod-collection.md)
- **Target Persona**: Customer ordering within Egypt/KSA and the Store Operations Manager
- **Summary**: Domestic Shipping via Bosta with COD Collection
- **Specification**: [`us-5.1.1-domestic-shipping-via-bosta-with-cod-collection.md`](us-5.1.1-domestic-shipping-via-bosta-with-cod-collection.md)

#### [US-5.1.2: Cross-Border Express Shipping (Aramex & DHL)](us-5.1.2-cross-border-express-shipping-aramex-dhl.md)
- **Target Persona**: Cross-Border Merchant and International Buyer
- **Summary**: Cross-Border Express Shipping (Aramex & DHL)
- **Specification**: [`us-5.1.2-cross-border-express-shipping-aramex-dhl.md`](us-5.1.2-cross-border-express-shipping-aramex-dhl.md)

#### [US-5.1.3: Global Multi-Carrier Aggregation (Shippo & EasyPost)](us-5.1.3-global-multi-carrier-aggregation-shippo-easypost.md)
- **Target Persona**: Global Marketplace Operator
- **Summary**: Global Multi-Carrier Aggregation (Shippo & EasyPost)
- **Specification**: [`us-5.1.3-global-multi-carrier-aggregation-shippo-easypost.md`](us-5.1.3-global-multi-carrier-aggregation-shippo-easypost.md)

#### [US-5.1.4: Localized SNS Push & SMS Notifications at Every Milestone](us-5.1.4-localized-sns-push-sms-notifications-at-every-milestone.md)
- **Target Persona**: Customer
- **Summary**: receive push notifications (APNs/FCM) and SMS at every order milestone in my preferred language
- **Specification**: [`us-5.1.4-localized-sns-push-sms-notifications-at-every-milestone.md`](us-5.1.4-localized-sns-push-sms-notifications-at-every-milestone.md)


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
