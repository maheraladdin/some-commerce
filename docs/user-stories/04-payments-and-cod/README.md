# Module 04: Payments & COD

> **Slice**: v1.0 / v4.0 · **Sprints**: 1.2, 4.2 · **Stories**: US-4.1.1 – US-4.1.5

## Overview

Covers all payment flows including full prepaid (Paymob/Stripe), full Cash on Delivery (100% COD), split Deposit COD (upfront deposit + cash balance), and self-hosted Bitcoin/Lightning payments via BTCPay Server.

## Pages

| Page Route | Access | Direction | Primary Hook |
|:-----------|:-------|:----------|:-------------|
| `/[locale]/checkout` | Authenticated | RTL / LTR | `useSplitCodCheckout` |
| `/[locale]/admin/settings-gateways` | STORE_ADMIN | RTL / LTR | `useAdminGatewayConfig` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| POST | `/v1/checkout/session` | `checkout-webhooks-api` | Create payment session |
| POST | `/v1/rates/calculate` | `checkout-webhooks-api` | Calculate shipping + COD rates |
| POST | `/v1/webhooks/paymob` | `checkout-webhooks-api` | Paymob HMAC-SHA512 webhook |
| POST | `/v1/webhooks/stripe` | `checkout-webhooks-api` | Stripe-Signature webhook |
| POST | `/v1/webhooks/btcpay` | `checkout-webhooks-api` | BTCPay-Sig webhook |
| PUT | `/v1/admin/vault/payment-gateways/:provider` | `admin-vendor-api` | Configure payment gateway |
| PUT | `/v1/admin/locale-fees/:country/:zone` | `admin-vendor-api` | Configure zone COD rules |

---

## User Stories Catalog

This module contains **5 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 10-PR implementation slice plan (10-Pillar System Architecture).

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-4.1.1](us-4.1.1-full-prepaid-online-payment-paymob-stripe.md)** | Full Prepaid Online Payment (Paymob & Stripe) | B2C Customer | Sprint 1.2 / 4.2 | [View Specification →](us-4.1.1-full-prepaid-online-payment-paymob-stripe.md) |
| **[US-4.1.2](us-4.1.2-full-cash-on-delivery-100-cod.md)** | Full Cash on Delivery (100% COD) | Customer in a region where online payments are not preferred | Sprint 1.2 / 4.2 | [View Specification →](us-4.1.2-full-cash-on-delivery-100-cod.md) |
| **[US-4.1.3](us-4.1.3-upfront-deposit-split-cash-on-delivery-deposit-cod.md)** | Upfront Deposit + Split Cash on Delivery (DEPOSIT_COD) | B2C Customer in Egypt/MENA | Sprint 1.2 / 4.2 | [View Specification →](us-4.1.3-upfront-deposit-split-cash-on-delivery-deposit-cod.md) |
| **[US-4.1.4](us-4.1.4-admin-payment-gateway-configuration.md)** | Admin Payment Gateway Configuration | Store Administrator | Sprint 1.2 / 4.2 | [View Specification →](us-4.1.4-admin-payment-gateway-configuration.md) |
| **[US-4.1.5](us-4.1.5-bitcoin-lightning-network-checkout-btcpay-server.md)** | Bitcoin & Lightning Network Checkout (BTCPay Server) | crypto-savvy Shopper | Sprint 1.2 / 4.2 | [View Specification →](us-4.1.5-bitcoin-lightning-network-checkout-btcpay-server.md) |

---

## Story Summaries

#### [US-4.1.1: Full Prepaid Online Payment (Paymob & Stripe)](us-4.1.1-full-prepaid-online-payment-paymob-stripe.md)
- **Target Persona**: B2C Customer
- **Summary**: pay 100% online via Paymob (Egypt/MENA) or Stripe (international)
- **Specification**: [`us-4.1.1-full-prepaid-online-payment-paymob-stripe.md`](us-4.1.1-full-prepaid-online-payment-paymob-stripe.md)

#### [US-4.1.2: Full Cash on Delivery (100% COD)](us-4.1.2-full-cash-on-delivery-100-cod.md)
- **Target Persona**: Customer in a region where online payments are not preferred
- **Summary**: place an order with 100% Cash on Delivery where I pay the full amount to the courier upon delivery
- **Specification**: [`us-4.1.2-full-cash-on-delivery-100-cod.md`](us-4.1.2-full-cash-on-delivery-100-cod.md)

#### [US-4.1.3: Upfront Deposit + Split Cash on Delivery (DEPOSIT_COD)](us-4.1.3-upfront-deposit-split-cash-on-delivery-deposit-cod.md)
- **Target Persona**: B2C Customer in Egypt/MENA
- **Summary**: pay a small deposit online (e.g.
- **Specification**: [`us-4.1.3-upfront-deposit-split-cash-on-delivery-deposit-cod.md`](us-4.1.3-upfront-deposit-split-cash-on-delivery-deposit-cod.md)

#### [US-4.1.4: Admin Payment Gateway Configuration](us-4.1.4-admin-payment-gateway-configuration.md)
- **Target Persona**: Store Administrator
- **Summary**: configure payment gateway credentials (Paymob
- **Specification**: [`us-4.1.4-admin-payment-gateway-configuration.md`](us-4.1.4-admin-payment-gateway-configuration.md)

#### [US-4.1.5: Bitcoin & Lightning Network Checkout (BTCPay Server)](us-4.1.5-bitcoin-lightning-network-checkout-btcpay-server.md)
- **Target Persona**: crypto-savvy Shopper
- **Summary**: pay using Bitcoin on-chain or Lightning Network via the merchant's self-hosted BTCPay Server
- **Specification**: [`us-4.1.5-bitcoin-lightning-network-checkout-btcpay-server.md`](us-4.1.5-bitcoin-lightning-network-checkout-btcpay-server.md)


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
