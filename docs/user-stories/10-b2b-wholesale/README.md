# Module 10: B2B Wholesale

> **Slice**: v3.0 · **Sprints**: 3.1, 3.2 · **Stories**: US-10.1.1 – US-10.1.4

## Overview

Covers B2B organization onboarding, tiered volume pricing, MOQ enforcement, RFQ negotiation with durable state machines, net-terms invoicing, and B2B on-premise LAN license proxy.

## Pages

| Page Route | Access | Primary Hook |
|:-----------|:-------|:-------------|
| `/[locale]/(auth)/b2b-register` | Public | `useB2BOnboarding` |
| `/[locale]/c/[...category_slug]` | B2B_BUYER | `useCatalogSearchAndFacets` |
| `/[locale]/products/[slug]` | B2B_BUYER | `useProductConfigurator` |
| `/[locale]/b2b/rfq` | B2B_BUYER / B2B_ORG_ADMIN | `useB2BRfqNegotiation` |
| `/[locale]/account/licenses` | B2B_ORG_ADMIN | `useDigitalLicenseVault` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| POST | `/v1/b2b/rfq` | `durable-orchestrator` | Submit RFQ |
| POST | `/v1/b2b/rfq/:id/counter-quote` | `durable-orchestrator` | Vendor counter-quote |
| POST | `/v1/b2b/rfq/:id/accept` | `durable-orchestrator` | Buyer accept + PO |
| POST | `/v1/b2b/licenses/master-lease` | `storefront-sdui-api` | Generate master lease cert |
| POST | `/v1/cart/bulk-items` | `checkout-webhooks-api` | Bulk variant matrix add |

---

## User Stories Catalog

This module contains **4 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-10.1.1](us-10.1.1-b2b-tiered-volume-pricing-moq-enforcement.md)** | B2B Tiered Volume Pricing & MOQ Enforcement | B2B Wholesale Buyer | Sprint 3.1 / 3.2 | [View Specification →](us-10.1.1-b2b-tiered-volume-pricing-moq-enforcement.md) |
| **[US-10.1.2](us-10.1.2-durable-rfq-negotiation-net-terms-invoicing.md)** | Durable RFQ Negotiation & Net-Terms Invoicing | B2B Buyer and Vendor | Sprint 3.1 / 3.2 | [View Specification →](us-10.1.2-durable-rfq-negotiation-net-terms-invoicing.md) |
| **[US-10.1.3](us-10.1.3-b2b-custom-elasticsearch-facets.md)** | B2B Custom Elasticsearch Facets | B2B Buyer | Sprint 3.1 / 3.2 | [View Specification →](us-10.1.3-b2b-custom-elasticsearch-facets.md) |
| **[US-10.1.4](us-10.1.4-b2b-on-premise-lan-license-proxy.md)** | B2B On-Premise LAN License Proxy | B2B Organization Admin | Sprint 3.1 / 3.2 | [View Specification →](us-10.1.4-b2b-on-premise-lan-license-proxy.md) |

---

## Story Summaries

#### [US-10.1.1: B2B Tiered Volume Pricing & MOQ Enforcement](us-10.1.1-b2b-tiered-volume-pricing-moq-enforcement.md)
- **Target Persona**: B2B Wholesale Buyer
- **Summary**: B2B Tiered Volume Pricing & MOQ Enforcement
- **Specification**: [`us-10.1.1-b2b-tiered-volume-pricing-moq-enforcement.md`](us-10.1.1-b2b-tiered-volume-pricing-moq-enforcement.md)

#### [US-10.1.2: Durable RFQ Negotiation & Net-Terms Invoicing](us-10.1.2-durable-rfq-negotiation-net-terms-invoicing.md)
- **Target Persona**: B2B Buyer and Vendor
- **Summary**: submit RFQs
- **Specification**: [`us-10.1.2-durable-rfq-negotiation-net-terms-invoicing.md`](us-10.1.2-durable-rfq-negotiation-net-terms-invoicing.md)

#### [US-10.1.3: B2B Custom Elasticsearch Facets](us-10.1.3-b2b-custom-elasticsearch-facets.md)
- **Target Persona**: B2B Buyer
- **Summary**: B2B Custom Elasticsearch Facets
- **Specification**: [`us-10.1.3-b2b-custom-elasticsearch-facets.md`](us-10.1.3-b2b-custom-elasticsearch-facets.md)

#### [US-10.1.4: B2B On-Premise LAN License Proxy](us-10.1.4-b2b-on-premise-lan-license-proxy.md)
- **Target Persona**: B2B Organization Admin
- **Summary**: deploy a lightweight LAN license proxy container in my corporate network with a KMS-signed master lease
- **Specification**: [`us-10.1.4-b2b-on-premise-lan-license-proxy.md`](us-10.1.4-b2b-on-premise-lan-license-proxy.md)


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
