# Sprint 4.2 — Escrow Ledger + Vendor Portal + BTCPay + RMA

> **Slice**: v4.0 · **Duration**: Weeks 15–16 · **Story Points**: 34

## Goal

Complete the marketplace with escrow ledger, vendor portal dashboard, BTCPay crypto payments, and RMA return processing.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-11.1.3](../user-stories/11-multi-vendor-marketplace/us-11.1.3-double-entry-escrow-ledger-vendor-payouts.md) | Marketplace | 8 | Escrow ledger + payouts |
| P0 | [US-11.1.4](../user-stories/11-multi-vendor-marketplace/us-11.1.4-vendor-portal-dashboard.md) | Marketplace | 5 | Vendor portal dashboard |
| P0 | [US-6.1.3](../user-stories/06-orders-and-returns/us-6.1.3-return-merchandise-authorization-rma.md) | Orders | 8 | RMA returns |
| P1 | [US-4.1.5](../user-stories/04-payments-and-cod/us-4.1.5-bitcoin-lightning-network-checkout-btcpay-server.md) | Payments | 5 | BTCPay crypto payments |
| P1 | [US-6.1.4](../user-stories/06-orders-and-returns/us-6.1.4-admin-order-management-dashboard.md) | Orders | 5 | Admin order management |
| P2 | [US-3.1.3](../user-stories/03-cart-and-checkout/us-3.1.3-multi-step-checkout-flow.md) | Checkout | 3 | Checkout refinements |

## Definition of Done

- [ ] Escrow holds created on delivery, released after 14 days
- [ ] RMA filed within return window freezes escrow
- [ ] Vendor payout requests work
- [ ] BTCPay Lightning invoice generated + settled
- [ ] Admin order dashboard filters and updates work

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.

---

## Multi-Agent Sprint Implementation Plan (6-Layer Governance)

### Company planning → role execution → upward validation

**Status: allocation proposal, not dispatch authorization.** Leadership planning precedes the junior roster; the L1–L6 ladder below is the upward review path. Approve P0–P4 and the company master-plan revision before implementation.

| Stage | Accountable role | Required output |
|:------|:-----------------|:----------------|
| P0 | `chief-technology-officer` | Authorized initiative charter, constraints and success criteria |
| P1 | `product-manager` | Spec Kit requirements, personas, scope and acceptance criteria |
| P2 | `system-architect` | Shared contracts and affected specialist role subplans |
| P3 | `tech-lead` | Reconciled master plan, child manifest, task DAG and review/test capacity |
| P4 | `planning-control-owners-and-cto` | Approved plan baseline and G0/SG0 inputs before implementation |
| EXECUTE | `assigned-role-contributors-and-seniors` | Parallel approved tasks, independent branch reviews and bounded repairs |
| COLLECT | `tech-lead` | Every expected child output and canonical story record reconciled on one candidate |
| VALIDATE | `qa-security-architecture` | Integrated candidate plus E1-E5 sprint evidence and complete action history |
| ACCEPT | `product-manager` | Original charter/AC-to-delivery acceptance dossier |
| RETURN | `chief-technology-officer` | Final Accepted, Changes Required or Blocked decision |

Use the [company plan template](../../.specify/templates/company-plan-template.md). Every task references its master-plan parent and canonical `docs/validation/story-records/US-<id>.md`; log each action/result and next-role receipt there. Collect all expected children, verify the exact assembled candidate and closeout suites, then return product acceptance and the full dossier to CTO. Missing children, action history or required checks block parent acceptance.


Engineering delivery for **SPRINT-4.2** is executed by autonomous agent instances organized into **Junior Implementer / Senior Reviewer pairs** and governed by the **6-Layer Validation Ladder** leading up to **Product Manager Acceptance** and **CTO Agreement**.

Every agent operates inside an isolated working directory (`workdir`) with whitelisted write paths to guarantee **zero file conflicts**.

```mermaid
flowchart TD
    subgraph "Sprint Backlog: SPRINT-4.2"
        STORIES["6 User Stories × 7 PR Slices<br/>(42 Discrete Vertical Tasks)"]
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
| `sprint-4.2-junior-be-1` | `backend-engineer` | `junior` | `builder` | 12 implementation tasks | `.agents/workspaces/sprint-4.2/sprint-4.2-junior-be-1` |
| `sprint-4.2-junior-be-2` | `backend-engineer` | `junior` | `builder` | 12 implementation tasks | `.agents/workspaces/sprint-4.2/sprint-4.2-junior-be-2` |
| `sprint-4.2-junior-fe-1` | `client-engineer` | `junior` | `builder` | 9 implementation tasks | `.agents/workspaces/sprint-4.2/sprint-4.2-junior-fe-1` |
| `sprint-4.2-junior-fe-2` | `client-engineer` | `junior` | `builder` | 9 implementation tasks | `.agents/workspaces/sprint-4.2/sprint-4.2-junior-fe-2` |
| `sprint-4.2-junior-qa-1` | `testing-qa-engineer` | `junior` | `tester` | 6 implementation tasks | `.agents/workspaces/sprint-4.2/sprint-4.2-junior-qa-1` |
| `sprint-4.2-senior-be-1` | `backend-engineer` | `senior` | `reviewer` | 24 peer reviews | `.agents/workspaces/sprint-4.2/sprint-4.2-senior-be-1` |
| `sprint-4.2-senior-fe-1` | `client-engineer` | `senior` | `reviewer` | 18 peer reviews | `.agents/workspaces/sprint-4.2/sprint-4.2-senior-fe-1` |
| `sprint-4.2-senior-qa-1` | `security-engineer` | `senior` | `auditor` | 6 peer reviews | `.agents/workspaces/sprint-4.2/sprint-4.2-senior-qa-1` |
| `sprint-4.2-tech-lead` | `tech-lead` | `lead` | `lead` | Cross-story integration & G1/G4 sign-off | `.agents/workspaces/sprint-4.2/sprint-4.2-tech-lead` |
| `sprint-4.2-product-manager` | `product-manager` | `lead` | `pm` | Layer 5 Product Acceptance Sign-Off | `.agents/workspaces/sprint-4.2/sprint-4.2-product-manager` |
| `sprint-4.2-cto` | `chief-technology-officer` | `executive` | `cto` | Layer 6 Executive Agreement & SG4 Sign-Off | `.agents/workspaces/sprint-4.2/sprint-4.2-cto` |

### 2. Non-Conflicting Concurrency & Directory Whitelisting
To ensure conflict-free parallel execution across agents working on the same user story:
- **Backend Track (`backend-engineer`)**: Writes exclusively to `crates/**` and `backend/**`. Operates under the **Rust Zero-Clone Law** and pure microkernel trait contracts. Junior authors submit PRs to `sprint-4.2-senior-be-1` for code review.
- **Client Track (`client-engineer`)**: Writes exclusively to `apps/storefront/src/features/**` and `packages/**`. Operates under **Locality of Behavior (LoB)** and `@expo/ui` native guidelines. Junior authors submit PRs to `sprint-4.2-senior-fe-1` for code review.
- **Security & Quality Track (`qa-security-auditor`)**: Writes exclusively to `docs/validation/**` and test execution runners. Junior testers submit test suites to `sprint-4.2-senior-qa-1`.
- **Contract Synchronization**: Once PR 2 merges schema definitions and generates TypeScript types via `ts-rs`, Backend (PR 3 & 4) and Client (PR 5, 6 & 7) execute simultaneously without blocking.

### 3. Story-by-Story 7-PR Slicing Pipeline with Junior Author & Senior Reviewer Pairings
Every story in this sprint is decomposed into the standardized 7 PRs with assigned Junior Authors and Senior Reviewers:

#### Story [US-11.1.3]: Escrow ledger + payouts (8 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-4.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-4.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-4.2-junior-fe-1` | `sprint-4.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-4.2-junior-fe-2` | `sprint-4.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-4.2-junior-fe-1` | `sprint-4.2-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-11.1.4]: Vendor portal dashboard (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-4.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-4.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-4.2-junior-fe-2` | `sprint-4.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-4.2-junior-fe-2` | `sprint-4.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-4.2-junior-fe-1` | `sprint-4.2-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-6.1.3]: RMA returns (8 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-4.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-4.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-4.2-junior-fe-2` | `sprint-4.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-4.2-junior-fe-1` | `sprint-4.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-4.2-junior-fe-2` | `sprint-4.2-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-4.1.5]: BTCPay crypto payments (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-4.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-4.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-4.2-junior-fe-1` | `sprint-4.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-4.2-junior-fe-1` | `sprint-4.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-4.2-junior-fe-2` | `sprint-4.2-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-6.1.4]: Admin order management (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-4.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-4.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-4.2-junior-fe-1` | `sprint-4.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-4.2-junior-fe-2` | `sprint-4.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-4.2-junior-fe-1` | `sprint-4.2-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-3.1.3]: Checkout refinements (3 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-4.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-4.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-4.2-junior-be-1` | `sprint-4.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-4.2-junior-be-2` | `sprint-4.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-4.2-junior-fe-2` | `sprint-4.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-4.2-junior-fe-1` | `sprint-4.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-4.2-junior-fe-2` | `sprint-4.2-senior-fe-1` | @expo/ui + RTL Parity |

### 4. Sprint Quality Gates Progression
- [ ] **SG0 (Planning Readiness)**: 100% of backlog stories pass Gate G0; microkernel ports and crate boundaries mapped.
- [ ] **SG1 (Cross-Story Integration)**: End-to-end integration flows across all 6 stories pass under concurrent load.
- [ ] **SG2 (Security & Tenant Isolation)**: Synthetic multi-tenant penetration testing confirms 0 data leaks across sprint endpoints.
- [ ] **SG3 (Architecture & Gate M1/A1/A2)**:
  - Gate M1: `python3 scripts/validation/validate_microkernel.py` passes (zero cloud SDKs in pure crates, zero-clone compliance).
  - Gate A1: `python3 scripts/validation/validate_system_architecture.py` passes (10-layer architectural contracts verified).
  - Gate A2: `python3 scripts/validation/validate_folder_architecture.py` passes (framework-scoped LoB folder layout verified).
- [ ] **SG4 (Release Candidate & Operations)**: Staging smoke tests pass across mobile and web; p95 latency < 150ms; **Product Manager Acceptance (Layer 5)** and **CTO Agreement (Layer 6)** granted.

## End-of-Sprint Test Gate

**Status: Pending — required closeout evidence, not executed test results.** Run this suite at the end of sprint-4.2, on the exact integration/release candidate, before SG4 and CTO review. Earlier story checks remain mandatory. Follow the [sprint closeout policy](../SPRINT_TESTING.md) and attach the [evidence record](../validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md).

- [ ] **E1 — Benchmark tests:** Balanced ledger postings, payout reservation, partial refunds, portal projections and payment reconciliation.
- [ ] **E2 — Integration tests:** Delivery/remittance → escrow → RMA freeze/refund or payout; race release/payout/return and crypto settlement while verifying balanced journal and no duplicate transfer.
- [ ] **E3 — Fuzz tests:** Ledger amounts/currency/rounding, return quantities, payout requests, BTCPay event decoders and bulk admin transitions.
- [ ] **E4 — Loom concurrency tests:** Rust payout/RMA/release coordination and ledger projection publication; no local double-spend or torn snapshot. Provider transfers and persisted journal races require integration tests.
- [ ] **E5 — Independent closeout review:** QA lead records actual test/target/model counts, candidate and baseline commits, tool/environment versions, performance thresholds/results, corpus/reproducers, Loom bounds/completion and independent reviewer decisions. Missing targets, crashes, regressions, unexplored bounds or unreviewed N/A block acceptance; repairing the candidate invalidates affected results.

At SG0, assign test authors and independent senior QA/security/architecture reviewers; approve workload, benchmark baseline/regression thresholds, fuzz time/memory/input budgets and Loom model bounds. Carry forward affected regression suites. E4 is mandatory for applicable changed or affected Rust shared-state synchronization; only the scope-based N/A procedure in the policy can exclude it, with architecture + QA approval and alternative concurrency evidence. A missing implementation/harness is Pending, never N/A or Pass. Keep this section last, including after sprint-plan regeneration.
