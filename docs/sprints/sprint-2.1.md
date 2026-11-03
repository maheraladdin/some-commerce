# Sprint 2.1 — Digital Asset Pipeline + Licensing Engine (Modes 1–4)

> **Slice**: v2.0 · **Duration**: Weeks 5–6 · **Story Points**: 31

## Goal

Build the digital asset ingestion pipeline with presigned S3 delivery and implement the first 4 modes of the non-heartbeat licensing engine (Ed25519 certificates, Air-gapped QR, CRL revocation, CEK unsealing).

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-9.1.1](../user-stories/09-digital-products-and-licensing/us-9.1.1-digital-asset-ingestion-presigned-s3-delivery.md) | Digital | 8 | Digital asset ingestion + presigned S3 |
| P0 | [US-9.1.2](../user-stories/09-digital-products-and-licensing/us-9.1.2-6-mode-non-heartbeat-licensing-engine.md) | Licensing | 13 | Licensing Modes 1–4 (Ed25519, QR, CRL, CEK) |
| P1 | [US-2.1.3](../user-stories/02-storefront-and-catalog/us-2.1.3-admin-customizable-product-properties-filter-widgets.md) | Storefront | 5 | Custom product properties + widgets |
| P1 | [US-2.1.5](../user-stories/02-storefront-and-catalog/us-2.1.5-product-detail-page-with-variant-configuration.md) | Storefront | 5 | PDP variant configuration |

## Key Deliverables

- S3 vault with SSE-KMS encryption for digital assets
- Ed25519 signing via KMS for .lic certificates
- Air-gapped QR challenge-response for offline activation
- CloudFront-served CRL binary for passive revocation checks
- AES-256-GCM CEK unsealing via X25519 key exchange

## Definition of Done

- [ ] Digital asset upload with SHA256 verification works
- [ ] Presigned download URL expires after 15 minutes
- [ ] Ed25519 offline verification completes in <0.2ms
- [ ] QR air-gapped activation end-to-end works
- [ ] CRL check returns 304 for non-revoked licenses

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.

---

---

## Multi-Agent Sprint Implementation Plan (6-Layer Governance)

Engineering delivery for **SPRINT-2.1** is executed by autonomous agent instances organized into **Junior Implementer / Senior Reviewer pairs** and governed by the **6-Layer Validation Ladder** leading up to **Product Manager Acceptance** and **CTO Agreement**.

Every agent operates inside an isolated working directory (`workdir`) with whitelisted write paths to guarantee **zero file conflicts**.

```mermaid
flowchart TD
    subgraph "Sprint Backlog: SPRINT-2.1"
        STORIES["4 User Stories × 7 PR Slices<br/>(28 Discrete Vertical Tasks)"]
    end

    subgraph "The 6-Layer Validation Ladder"
        L1["<b>Layer 1: Junior Author</b><br/>Writes PR 1–7 in isolated workdir"]
        --> L2["<b>Layer 2: Senior Reviewer</b><br/>Audits Zero-Clone, LoB & ASVS (APPROVE)"]
        --> L3["<b>Layer 3: Security & Architect</b><br/>Gate G2 & Gates A1, A2, M1"]
        --> L4["<b>Layer 4: Tech Lead & Gatekeeper</b><br/>Cross-PR Integration & G1/G4 Sign-Off"]
        --> L5["<b>Layer 5: Product Manager (PM)</b><br/>Gherkin AC Acceptance Sign-Off"]
        --> L6["<b>Layer 6: Chief Technology Officer (CTO)</b><br/>Executive Agreement & SG4 Release"]
    end

    STORIES --> L1
```

### 1. Agent Roster & Load Balancer Allocation
| Worker ID | Core Profile | Seniority | Specialized Role | Assigned Tasks / Reviews | Dedicated Sprint Workdir |
|:----------|:-------------|:----------|:-----------------|:-------------------------|:-------------------------|
| `sprint-2.1-junior-be-1` | `backend-engineer` | `junior` | `builder` | 8 implementation tasks | `.agents/workspaces/sprint-2.1/sprint-2.1-junior-be-1` |
| `sprint-2.1-junior-be-2` | `backend-engineer` | `junior` | `builder` | 8 implementation tasks | `.agents/workspaces/sprint-2.1/sprint-2.1-junior-be-2` |
| `sprint-2.1-junior-fe-1` | `client-engineer` | `junior` | `builder` | 7 implementation tasks | `.agents/workspaces/sprint-2.1/sprint-2.1-junior-fe-1` |
| `sprint-2.1-junior-fe-2` | `client-engineer` | `junior` | `builder` | 5 implementation tasks | `.agents/workspaces/sprint-2.1/sprint-2.1-junior-fe-2` |
| `sprint-2.1-junior-qa-1` | `testing-qa-engineer` | `junior` | `tester` | 4 implementation tasks | `.agents/workspaces/sprint-2.1/sprint-2.1-junior-qa-1` |
| `sprint-2.1-senior-be-1` | `backend-engineer` | `senior` | `reviewer` | 16 peer reviews | `.agents/workspaces/sprint-2.1/sprint-2.1-senior-be-1` |
| `sprint-2.1-senior-fe-1` | `client-engineer` | `senior` | `reviewer` | 12 peer reviews | `.agents/workspaces/sprint-2.1/sprint-2.1-senior-fe-1` |
| `sprint-2.1-senior-qa-1` | `security-engineer` | `senior` | `auditor` | 4 peer reviews | `.agents/workspaces/sprint-2.1/sprint-2.1-senior-qa-1` |
| `sprint-2.1-tech-lead` | `tech-lead` | `lead` | `lead` | Cross-story integration & G1/G4 sign-off | `.agents/workspaces/sprint-2.1/sprint-2.1-tech-lead` |
| `sprint-2.1-product-manager` | `product-manager` | `lead` | `pm` | Layer 5 Product Acceptance Sign-Off | `.agents/workspaces/sprint-2.1/sprint-2.1-product-manager` |
| `sprint-2.1-cto` | `chief-technology-officer` | `executive` | `cto` | Layer 6 Executive Agreement & SG4 Sign-Off | `.agents/workspaces/sprint-2.1/sprint-2.1-cto` |

### 2. Non-Conflicting Concurrency & Directory Whitelisting
To ensure conflict-free parallel execution across agents working on the same user story:
- **Backend Track (`backend-engineer`)**: Writes exclusively to `crates/**` and `backend/**`. Operates under the **Rust Zero-Clone Law** and pure microkernel trait contracts. Junior authors submit PRs to `sprint-2.1-senior-be-1` for code review.
- **Client Track (`client-engineer`)**: Writes exclusively to `apps/storefront/src/features/**` and `packages/**`. Operates under **Locality of Behavior (LoB)** and `@expo/ui` native guidelines. Junior authors submit PRs to `sprint-2.1-senior-fe-1` for code review.
- **Security & Quality Track (`qa-security-auditor`)**: Writes exclusively to `docs/validation/**` and test execution runners. Junior testers submit test suites to `sprint-2.1-senior-qa-1`.
- **Contract Synchronization**: Once PR 2 merges schema definitions and generates TypeScript types via `ts-rs`, Backend (PR 3 & 4) and Client (PR 5, 6 & 7) execute simultaneously without blocking.

### 3. Story-by-Story 7-PR Slicing Pipeline with Junior Author & Senior Reviewer Pairings
Every story in this sprint is decomposed into the standardized 7 PRs with assigned Junior Authors and Senior Reviewers:

#### Story [US-9.1.1]: Digital asset ingestion + presigned S3 (8 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-2.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-2.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-2.1-junior-be-1` | `sprint-2.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-2.1-junior-be-2` | `sprint-2.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-2.1-junior-be-1` | `sprint-2.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-2.1-junior-be-2` | `sprint-2.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-2.1-junior-fe-1` | `sprint-2.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-2.1-junior-fe-2` | `sprint-2.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-2.1-junior-fe-1` | `sprint-2.1-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-9.1.2]: Licensing Modes 1–4 (Ed25519, QR, CRL, CEK) (13 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-2.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-2.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-2.1-junior-be-1` | `sprint-2.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-2.1-junior-be-2` | `sprint-2.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-2.1-junior-be-1` | `sprint-2.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-2.1-junior-be-2` | `sprint-2.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-2.1-junior-fe-2` | `sprint-2.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-2.1-junior-fe-1` | `sprint-2.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-2.1-junior-fe-2` | `sprint-2.1-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-2.1.3]: Custom product properties + widgets (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-2.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-2.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-2.1-junior-be-1` | `sprint-2.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-2.1-junior-be-2` | `sprint-2.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-2.1-junior-be-1` | `sprint-2.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-2.1-junior-be-2` | `sprint-2.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-2.1-junior-fe-1` | `sprint-2.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-2.1-junior-fe-1` | `sprint-2.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-2.1-junior-fe-2` | `sprint-2.1-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-2.1.5]: PDP variant configuration (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-2.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-2.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-2.1-junior-be-1` | `sprint-2.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-2.1-junior-be-2` | `sprint-2.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-2.1-junior-be-1` | `sprint-2.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-2.1-junior-be-2` | `sprint-2.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-2.1-junior-fe-1` | `sprint-2.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-2.1-junior-fe-2` | `sprint-2.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-2.1-junior-fe-1` | `sprint-2.1-senior-fe-1` | @expo/ui + RTL Parity |

### 4. Sprint Quality Gates Progression
- [ ] **SG0 (Planning Readiness)**: 100% of backlog stories pass Gate G0; microkernel ports and crate boundaries mapped.
- [ ] **SG1 (Cross-Story Integration)**: End-to-end integration flows across all 4 stories pass under concurrent load.
- [ ] **SG2 (Security & Tenant Isolation)**: Synthetic multi-tenant penetration testing confirms 0 data leaks across sprint endpoints.
- [ ] **SG3 (Architecture & Gate M1/A1/A2)**:
  - Gate M1: `python3 scripts/validate_microkernel.py` passes (zero cloud SDKs in pure crates, zero-clone compliance).
  - Gate A1: `python3 scripts/validate_system_architecture.py` passes (10-layer architectural contracts verified).
  - Gate A2: `python3 scripts/validate_folder_architecture.py` passes (framework-scoped LoB folder layout verified).
- [ ] **SG4 (Release Candidate & Operations)**: Staging smoke tests pass across mobile and web; p95 latency < 150ms; **Product Manager Acceptance (Layer 5)** and **CTO Agreement (Layer 6)** granted.
