# Module 09: Digital Products & Licensing

> **Slice**: v2.0 · **Sprints**: 2.1, 2.2 · **Stories**: US-9.1.1 – US-9.1.4

## Overview

Covers digital asset ingestion, presigned S3 delivery, the 6-mode non-heartbeat licensing engine (Ed25519, QR, CRL, CEK, Release Gating, Push Revocation), and client verification SDKs.

## Pages

| Page Route | Access | Primary Hook |
|:-----------|:-------|:-------------|
| `/[locale]/vendor/products/new` | VENDOR | `useVendorProductEditor` |
| `/[locale]/account/licenses` | Auth | `useDigitalLicenseVault` |
| `/[locale]/admin/settings-gateways` | STORE_ADMIN | `useAdminGatewayConfig` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| POST | `/v1/admin/digital-assets/presign-upload` | `admin-vendor-api` | Presigned S3 PUT for upload |
| POST | `/v1/licenses/entitlement/:id/download-url` | `storefront-sdui-api` | Presigned S3 GET download |
| POST | `/v1/licenses/challenge-activate` | `storefront-sdui-api` | Air-gapped QR activation (Mode 2) |
| POST | `/v1/licenses/unseal-cek` | `storefront-sdui-api` | Content Key unsealing (Mode 4) |
| GET | `/licenses/revoked.crl.bin` | CloudFront (S3) | Edge-cached CRL (Mode 3) |
| POST | `/v1/licenses/revoke` | `admin-vendor-api` | Revoke a license |

---

## User Stories Catalog

This module contains **4 detailed user stories**. Each user story has its own dedicated specification document containing Gherkin acceptance criteria (`Given/When/Then`), comprehensive test matrices (happy path, edge cases, error handling, security, and concurrency), Mermaid activity diagrams, and the 10-PR implementation slice plan (10-Pillar System Architecture).

| Story ID | Title | Target Persona | Sprint | Specification Document |
| :--- | :--- | :--- | :--- | :--- |
| **[US-9.1.1](us-9.1.1-digital-asset-ingestion-presigned-s3-delivery.md)** | Digital Asset Ingestion & Presigned S3 Delivery | Digital Creator or Software Vendor | Sprint 2.1 / 2.2 | [View Specification →](us-9.1.1-digital-asset-ingestion-presigned-s3-delivery.md) |
| **[US-9.1.2](us-9.1.2-6-mode-non-heartbeat-licensing-engine.md)** | 6-Mode Non-Heartbeat Licensing Engine | Software Vendor or Digital Product Buyer | Sprint 2.1 / 2.2 | [View Specification →](us-9.1.2-6-mode-non-heartbeat-licensing-engine.md) |
| **[US-9.1.3](us-9.1.3-client-verification-sdks.md)** | Client Verification SDKs | third-party Software Developer integrating with some-commerce licensing | Sprint 2.1 / 2.2 | [View Specification →](us-9.1.3-client-verification-sdks.md) |
| **[US-9.1.4](us-9.1.4-digital-license-vault-ui.md)** | Digital License Vault UI | Buyer of digital products | Sprint 2.1 / 2.2 | [View Specification →](us-9.1.4-digital-license-vault-ui.md) |

---

## Story Summaries

#### [US-9.1.1: Digital Asset Ingestion & Presigned S3 Delivery](us-9.1.1-digital-asset-ingestion-presigned-s3-delivery.md)
- **Target Persona**: Digital Creator or Software Vendor
- **Summary**: upload encrypted digital assets and deliver them to verified buyers via time-limited presigned S3 URLs
- **Specification**: [`us-9.1.1-digital-asset-ingestion-presigned-s3-delivery.md`](us-9.1.1-digital-asset-ingestion-presigned-s3-delivery.md)

#### [US-9.1.2: 6-Mode Non-Heartbeat Licensing Engine](us-9.1.2-6-mode-non-heartbeat-licensing-engine.md)
- **Target Persona**: Software Vendor or Digital Product Buyer
- **Summary**: 6-Mode Non-Heartbeat Licensing Engine
- **Specification**: [`us-9.1.2-6-mode-non-heartbeat-licensing-engine.md`](us-9.1.2-6-mode-non-heartbeat-licensing-engine.md)

#### [US-9.1.3: Client Verification SDKs](us-9.1.3-client-verification-sdks.md)
- **Target Persona**: third-party Software Developer integrating with some-commerce licensing
- **Summary**: Client Verification SDKs
- **Specification**: [`us-9.1.3-client-verification-sdks.md`](us-9.1.3-client-verification-sdks.md)

#### [US-9.1.4: Digital License Vault UI](us-9.1.4-digital-license-vault-ui.md)
- **Target Persona**: Buyer of digital products
- **Summary**: Digital License Vault UI
- **Specification**: [`us-9.1.4-digital-license-vault-ui.md`](us-9.1.4-digital-license-vault-ui.md)


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
