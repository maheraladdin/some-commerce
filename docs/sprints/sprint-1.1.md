# Sprint 1.1 — Auth + Storefront + Customer Foundation

> **Slice**: v1.0 · **Duration**: Weeks 1–2 · **Story Points**: 34

## Goal

Stand up the authentication layer, SDUI storefront rendering, catalog search, and customer account foundation. By sprint end, a customer can sign in, browse the catalog, search with facets, view product details, and manage their profile.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-1.1.1](../user-stories/01-auth-and-onboarding/us-1.1.1-phone-otp-passwordless-sign-in.md) | Auth | 5 | Phone OTP passwordless sign-in |
| P0 | [US-1.1.2](../user-stories/01-auth-and-onboarding/us-1.1.2-email-password-passkey-webauthn-sign-in.md) | Auth | 5 | Email/Password & Passkey sign-in |
| P0 | [US-1.1.3](../user-stories/01-auth-and-onboarding/us-1.1.3-social-oidc-sign-in-google-apple.md) | Auth | 3 | Social OIDC sign-in (Google & Apple) |
| P0 | [US-2.1.1](../user-stories/02-storefront-and-catalog/us-2.1.1-multilingual-sdui-storefront-with-instant-watermelondb-rendering.md) | Storefront | 8 | SDUI storefront with WatermelonDB |
| P1 | [US-2.1.2](../user-stories/02-storefront-and-catalog/us-2.1.2-unlimited-n-level-category-taxonomy-brand-management.md) | Storefront | 5 | N-Level taxonomy & brands |
| P1 | [US-2.1.4](../user-stories/02-storefront-and-catalog/us-2.1.4-dual-tier-catalog-search-with-nested-faceted-filtration.md) | Storefront | 5 | Dual-tier search + facets |
| P1 | [US-7.1.1](../user-stories/07-customer-account/us-7.1.1-customer-profile-management.md) | Account | 3 | Customer profile management |

## Dependencies

```mermaid
flowchart LR
    US_1_1_1 & US_1_1_2 & US_1_1_3 --> US_7_1_1
    US_2_1_2 --> US_2_1_4
    US_2_1_1 --> US_2_1_4
```

## Infrastructure Setup (Sprint 0 pre-work)

Status: unverified prerequisites; attach deployment evidence before marking these complete.

- [ ] AWS Account + CDK bootstrap
- [ ] Cognito User Pool + Identity Pool
- [ ] DynamoDB table with GSI1 + GSI2
- [ ] ElastiCache Serverless for Redis
- [ ] Elasticsearch dev domain
- [ ] S3 buckets (sdui-assets, digital-vault)

## Definition of Done

- [ ] All test cases for P0 stories pass
- [ ] ETag-based caching verified (304 responses)
- [ ] WatermelonDB offline browsing works
- [ ] RTL (ar-EG) and LTR (en-US) layouts validated
- [ ] Code review completed for all PRs
- [ ] No critical security findings

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.

---

---

## Multi-Agent Sprint Implementation Plan (6-Layer Governance)

Engineering delivery for **SPRINT-1.1** is executed by autonomous agent instances organized into **Junior Implementer / Senior Reviewer pairs** and governed by the **6-Layer Validation Ladder** leading up to **Product Manager Acceptance** and **CTO Agreement**.

Every agent operates inside an isolated working directory (`workdir`) with whitelisted write paths to guarantee **zero file conflicts**.

```mermaid
flowchart TD
    subgraph "Sprint Backlog: SPRINT-1.1"
        STORIES["7 User Stories × 7 PR Slices<br/>(49 Discrete Vertical Tasks)"]
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
| `sprint-1.1-junior-be-1` | `backend-engineer` | `junior` | `builder` | 14 implementation tasks | `.agents/workspaces/sprint-1.1/sprint-1.1-junior-be-1` |
| `sprint-1.1-junior-be-2` | `backend-engineer` | `junior` | `builder` | 14 implementation tasks | `.agents/workspaces/sprint-1.1/sprint-1.1-junior-be-2` |
| `sprint-1.1-junior-fe-1` | `client-engineer` | `junior` | `builder` | 11 implementation tasks | `.agents/workspaces/sprint-1.1/sprint-1.1-junior-fe-1` |
| `sprint-1.1-junior-fe-2` | `client-engineer` | `junior` | `builder` | 10 implementation tasks | `.agents/workspaces/sprint-1.1/sprint-1.1-junior-fe-2` |
| `sprint-1.1-junior-qa-1` | `testing-qa-engineer` | `junior` | `tester` | 7 implementation tasks | `.agents/workspaces/sprint-1.1/sprint-1.1-junior-qa-1` |
| `sprint-1.1-senior-be-1` | `backend-engineer` | `senior` | `reviewer` | 28 peer reviews | `.agents/workspaces/sprint-1.1/sprint-1.1-senior-be-1` |
| `sprint-1.1-senior-fe-1` | `client-engineer` | `senior` | `reviewer` | 21 peer reviews | `.agents/workspaces/sprint-1.1/sprint-1.1-senior-fe-1` |
| `sprint-1.1-senior-qa-1` | `security-engineer` | `senior` | `auditor` | 7 peer reviews | `.agents/workspaces/sprint-1.1/sprint-1.1-senior-qa-1` |
| `sprint-1.1-tech-lead` | `tech-lead` | `lead` | `lead` | Cross-story integration & G1/G4 sign-off | `.agents/workspaces/sprint-1.1/sprint-1.1-tech-lead` |
| `sprint-1.1-product-manager` | `product-manager` | `lead` | `pm` | Layer 5 Product Acceptance Sign-Off | `.agents/workspaces/sprint-1.1/sprint-1.1-product-manager` |
| `sprint-1.1-cto` | `chief-technology-officer` | `executive` | `cto` | Layer 6 Executive Agreement & SG4 Sign-Off | `.agents/workspaces/sprint-1.1/sprint-1.1-cto` |

### 2. Non-Conflicting Concurrency & Directory Whitelisting
To ensure conflict-free parallel execution across agents working on the same user story:
- **Backend Track (`backend-engineer`)**: Writes exclusively to `crates/**` and `backend/**`. Operates under the **Rust Zero-Clone Law** and pure microkernel trait contracts. Junior authors submit PRs to `sprint-1.1-senior-be-1` for code review.
- **Client Track (`client-engineer`)**: Writes exclusively to `apps/storefront/src/features/**` and `packages/**`. Operates under **Locality of Behavior (LoB)** and `@expo/ui` native guidelines. Junior authors submit PRs to `sprint-1.1-senior-fe-1` for code review.
- **Security & Quality Track (`qa-security-auditor`)**: Writes exclusively to `docs/validation/**` and test execution runners. Junior testers submit test suites to `sprint-1.1-senior-qa-1`.
- **Contract Synchronization**: Once PR 2 merges schema definitions and generates TypeScript types via `ts-rs`, Backend (PR 3 & 4) and Client (PR 5, 6 & 7) execute simultaneously without blocking.

### 3. Story-by-Story 7-PR Slicing Pipeline with Junior Author & Senior Reviewer Pairings
Every story in this sprint is decomposed into the standardized 7 PRs with assigned Junior Authors and Senior Reviewers:

#### Story [US-1.1.1]: Phone OTP passwordless sign-in (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-1.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-1.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-1.1.2]: Email/Password & Passkey sign-in (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-1.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-1.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-1.1.3]: Social OIDC sign-in (Google & Apple) (3 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-1.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-1.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-2.1.1]: SDUI storefront with WatermelonDB (8 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-1.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-1.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-2.1.2]: N-Level taxonomy & brands (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-1.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-1.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-2.1.4]: Dual-tier search + facets (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-1.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-1.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-7.1.1]: Customer profile management (3 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-1.1-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-1.1-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-1.1-junior-be-1` | `sprint-1.1-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-1.1-junior-be-2` | `sprint-1.1-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-1.1-junior-fe-1` | `sprint-1.1-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-1.1-junior-fe-2` | `sprint-1.1-senior-fe-1` | @expo/ui + RTL Parity |

### 4. Sprint Quality Gates Progression
- [ ] **SG0 (Planning Readiness)**: 100% of backlog stories pass Gate G0; microkernel ports and crate boundaries mapped.
- [ ] **SG1 (Cross-Story Integration)**: End-to-end integration flows across all 7 stories pass under concurrent load.
- [ ] **SG2 (Security & Tenant Isolation)**: Synthetic multi-tenant penetration testing confirms 0 data leaks across sprint endpoints.
- [ ] **SG3 (Architecture & Gate M1/A1/A2)**:
  - Gate M1: `python3 scripts/validate_microkernel.py` passes (zero cloud SDKs in pure crates, zero-clone compliance).
  - Gate A1: `python3 scripts/validate_system_architecture.py` passes (10-layer architectural contracts verified).
  - Gate A2: `python3 scripts/validate_folder_architecture.py` passes (framework-scoped LoB folder layout verified).
- [ ] **SG4 (Release Candidate & Operations)**: Staging smoke tests pass across mobile and web; p95 latency < 150ms; **Product Manager Acceptance (Layer 5)** and **CTO Agreement (Layer 6)** granted.
