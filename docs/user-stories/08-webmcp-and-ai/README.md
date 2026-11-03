# Module 08: WebMCP & AI Assistant

> **Slice**: v1.0 · **Sprint**: 1.1 · **Stories**: US-8.1.1 – US-8.1.3

## Overview

Covers the WebMCP (`navigator.modelContext`) and Amazon Bedrock AI integration for customer shopping assistant tools, admin copilot tools, and the shared MCP engine.

## Pages

| Page Route | Access | Primary Hook |
|:-----------|:-------|:-------------|
| `/[locale]/c/[...category_slug]` | Public | `useWebMcpBridge` + `useCatalogSearchAndFacets` |
| `/[locale]/compare` | Public | `useWebMcpComparison` |
| `/[locale]/account/profile` | Auth | `useCustomerAccount` |
| `/[locale]/admin/sdui-studio` | STORE_ADMIN | `useAdminSduiStudio` |
| `/[locale]/admin/catalog-taxonomy` | STORE_ADMIN | `useAdminTaxonomyBuilder` |
| `/[locale]/vendor/products/new` | VENDOR | `useVendorProductEditor` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| POST | `/v1/mcp/customer` | `storefront-sdui-api` | Customer MCP tool execution |
| POST | `/v1/mcp/admin` | `admin-vendor-api` | Admin MCP tool execution |

---

## User Stories Catalog

This module contains **3 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-8.1.1](us-8.1.1-customer-webmcp-shopping-assistant.md)** | Customer WebMCP Shopping Assistant | Shopper browsing on a WebMCP-capable browser or using the in-app AI assistant | Sprint 1.1 | [View Specification →](us-8.1.1-customer-webmcp-shopping-assistant.md) |
| **[US-8.1.2](us-8.1.2-admin-webmcp-store-copilot.md)** | Admin WebMCP Store Copilot | Store Administrator or Vendor | Sprint 1.1 | [View Specification →](us-8.1.2-admin-webmcp-store-copilot.md) |
| **[US-8.1.3](us-8.1.3-shared-mcp-engine-bedrock-integration.md)** | Shared MCP Engine & Bedrock Integration | Developer | Sprint 1.1 | [View Specification →](us-8.1.3-shared-mcp-engine-bedrock-integration.md) |

---

## Story Summaries

#### [US-8.1.1: Customer WebMCP Shopping Assistant](us-8.1.1-customer-webmcp-shopping-assistant.md)
- **Target Persona**: Shopper browsing on a WebMCP-capable browser or using the in-app AI assistant
- **Summary**: search the catalog in natural language
- **Specification**: [`us-8.1.1-customer-webmcp-shopping-assistant.md`](us-8.1.1-customer-webmcp-shopping-assistant.md)

#### [US-8.1.2: Admin WebMCP Store Copilot](us-8.1.2-admin-webmcp-store-copilot.md)
- **Target Persona**: Store Administrator or Vendor
- **Summary**: use AI copilot tools to style SDUI pages
- **Specification**: [`us-8.1.2-admin-webmcp-store-copilot.md`](us-8.1.2-admin-webmcp-store-copilot.md)

#### [US-8.1.3: Shared MCP Engine & Bedrock Integration](us-8.1.3-shared-mcp-engine-bedrock-integration.md)
- **Target Persona**: Developer
- **Summary**: Shared MCP Engine & Bedrock Integration
- **Specification**: [`us-8.1.3-shared-mcp-engine-bedrock-integration.md`](us-8.1.3-shared-mcp-engine-bedrock-integration.md)


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
