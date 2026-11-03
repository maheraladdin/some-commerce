# Module 12: Admin & SDUI Studio

> **Slice**: v5.0 / v6.0 · **Sprints**: 5.1, 6.1, 6.2 · **Stories**: US-12.1.1 – US-12.1.3

## Overview

Covers the dual-edition deployment model (Standard vs. Managed Instances), the visual SDUI studio with drag-and-drop editing, AI styling, and the white-label mobile build pipeline.

## Pages

| Page Route | Access | Primary Hook |
|:-----------|:-------|:-------------|
| `/[locale]/admin/sdui-studio` | STORE_ADMIN | `useAdminSduiStudio` |
| `/[locale]/admin/sdui-studio/mobile-builds` | STORE_ADMIN | `useAdminSduiStudio` |
| `/[locale]/admin/settings-gateways` | STORE_ADMIN | `useAdminGatewayConfig` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| POST | `/v1/admin/sdui/publish` | `admin-vendor-api` | Publish SDUI layout |
| GET | `/v1/admin/sdui/drafts` | `admin-vendor-api` | List SDUI drafts |
| POST | `/v1/admin/sdui/preview` | `admin-vendor-api` | Generate draft preview |
| POST | `/v1/admin/mobile-builds/trigger` | `admin-vendor-api` | Trigger EAS build |
| GET | `/v1/admin/telemetry/cache` | `admin-vendor-api` | Cache hit ratio stats |

---

## User Stories Catalog

This module contains **3 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 7-PR implementation slice plan.

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-12.1.1](us-12.1.1-visual-drag-and-drop-sdui-studio.md)** | Visual Drag-and-Drop SDUI Studio | Brand Designer or Store Administrator | Sprint 5.1 / 6.1 / 6.2 | [View Specification →](us-12.1.1-visual-drag-and-drop-sdui-studio.md) |
| **[US-12.1.2](us-12.1.2-dual-edition-deployment-standard-vs-managed-instances.md)** | Dual-Edition Deployment (Standard vs. Managed Instances) | DevOps Engineer deploying some-commerce | Sprint 5.1 / 6.1 / 6.2 | [View Specification →](us-12.1.2-dual-edition-deployment-standard-vs-managed-instances.md) |
| **[US-12.1.3](us-12.1.3-white-label-mobile-build-pipeline.md)** | White-Label Mobile Build Pipeline | Store Administrator or Agency Developer | Sprint 5.1 / 6.1 / 6.2 | [View Specification →](us-12.1.3-white-label-mobile-build-pipeline.md) |

---

## Story Summaries

#### [US-12.1.1: Visual Drag-and-Drop SDUI Studio](us-12.1.1-visual-drag-and-drop-sdui-studio.md)
- **Target Persona**: Brand Designer or Store Administrator
- **Summary**: visually edit SDUI pages with drag-and-drop block reordering
- **Specification**: [`us-12.1.1-visual-drag-and-drop-sdui-studio.md`](us-12.1.1-visual-drag-and-drop-sdui-studio.md)

#### [US-12.1.2: Dual-Edition Deployment (Standard vs. Managed Instances)](us-12.1.2-dual-edition-deployment-standard-vs-managed-instances.md)
- **Target Persona**: DevOps Engineer deploying some-commerce
- **Summary**: toggle a single CDK parameter to deploy on scale-to-zero Lambda or dedicated Managed Instances
- **Specification**: [`us-12.1.2-dual-edition-deployment-standard-vs-managed-instances.md`](us-12.1.2-dual-edition-deployment-standard-vs-managed-instances.md)

#### [US-12.1.3: White-Label Mobile Build Pipeline](us-12.1.3-white-label-mobile-build-pipeline.md)
- **Target Persona**: Store Administrator or Agency Developer
- **Summary**: trigger white-label iOS/Android builds with custom branding from the SDUI Studio
- **Specification**: [`us-12.1.3-white-label-mobile-build-pipeline.md`](us-12.1.3-white-label-mobile-build-pipeline.md)


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
