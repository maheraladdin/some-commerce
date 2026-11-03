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

This module contains **3 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 10-PR implementation slice plan (10-Pillar System Architecture).

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
