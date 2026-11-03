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

This module contains **5 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

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
