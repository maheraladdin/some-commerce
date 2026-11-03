# Sprint 3.2 — RFQ Negotiation + Net-Terms + LAN License Proxy

> **Slice**: v3.0 · **Duration**: Weeks 11–12 · **Story Points**: 32

## Goal

Complete B2B wholesale with durable RFQ negotiation, net-terms invoicing (NET_30/NET_60), and on-premise LAN license proxy for enterprise deployments.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-10.1.2](../user-stories/10-b2b-wholesale/us-10.1.2-durable-rfq-negotiation-net-terms-invoicing.md) | B2B | 13 | RFQ negotiation + net-terms |
| P0 | [US-10.1.4](../user-stories/10-b2b-wholesale/us-10.1.4-b2b-on-premise-lan-license-proxy.md) | B2B | 8 | LAN license proxy |
| P1 | [US-5.1.3](../user-stories/05-fulfillment-and-shipping/us-5.1.3-global-multi-carrier-aggregation-shippo-easypost.md) | Fulfillment | 5 | Shippo/EasyPost aggregation |
| P1 | [US-8.1.2](../user-stories/08-webmcp-and-ai/us-8.1.2-admin-webmcp-store-copilot.md) | WebMCP | 3 | Admin copilot |
| P2 | [US-6.1.2](../user-stories/06-orders-and-returns/us-6.1.2-customer-order-history-with-filtering.md) | Orders | 3 | Order history |

## Definition of Done

- [ ] RFQ durable state machine with 14-day timeout works
- [ ] Counter-quote → PO approval flow complete
- [ ] Net-30 timer with SNS reminders works
- [ ] LAN proxy container runs offline with master lease
- [ ] Seat checkout/release within pool limits

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


Engineering delivery for **SPRINT-3.2** is executed by autonomous agent instances organized into **Junior Implementer / Senior Reviewer pairs** and governed by the **6-Layer Validation Ladder** leading up to **Product Manager Acceptance** and **CTO Agreement**.

Every agent operates inside an isolated working directory (`workdir`) with whitelisted write paths to guarantee **zero file conflicts**.

```mermaid
flowchart TD
    subgraph "Sprint Backlog: SPRINT-3.2"
        STORIES["5 User Stories × 7 PR Slices<br/>(35 Discrete Vertical Tasks)"]
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
| `sprint-3.2-junior-be-1` | `backend-engineer` | `junior` | `builder` | 10 implementation tasks | `.agents/workspaces/sprint-3.2/sprint-3.2-junior-be-1` |
| `sprint-3.2-junior-be-2` | `backend-engineer` | `junior` | `builder` | 10 implementation tasks | `.agents/workspaces/sprint-3.2/sprint-3.2-junior-be-2` |
| `sprint-3.2-junior-fe-1` | `client-engineer` | `junior` | `builder` | 7 implementation tasks | `.agents/workspaces/sprint-3.2/sprint-3.2-junior-fe-1` |
| `sprint-3.2-junior-fe-2` | `client-engineer` | `junior` | `builder` | 8 implementation tasks | `.agents/workspaces/sprint-3.2/sprint-3.2-junior-fe-2` |
| `sprint-3.2-junior-qa-1` | `testing-qa-engineer` | `junior` | `tester` | 5 implementation tasks | `.agents/workspaces/sprint-3.2/sprint-3.2-junior-qa-1` |
| `sprint-3.2-senior-be-1` | `backend-engineer` | `senior` | `reviewer` | 20 peer reviews | `.agents/workspaces/sprint-3.2/sprint-3.2-senior-be-1` |
| `sprint-3.2-senior-fe-1` | `client-engineer` | `senior` | `reviewer` | 15 peer reviews | `.agents/workspaces/sprint-3.2/sprint-3.2-senior-fe-1` |
| `sprint-3.2-senior-qa-1` | `security-engineer` | `senior` | `auditor` | 5 peer reviews | `.agents/workspaces/sprint-3.2/sprint-3.2-senior-qa-1` |
| `sprint-3.2-tech-lead` | `tech-lead` | `lead` | `lead` | Cross-story integration & G1/G4 sign-off | `.agents/workspaces/sprint-3.2/sprint-3.2-tech-lead` |
| `sprint-3.2-product-manager` | `product-manager` | `lead` | `pm` | Layer 5 Product Acceptance Sign-Off | `.agents/workspaces/sprint-3.2/sprint-3.2-product-manager` |
| `sprint-3.2-cto` | `chief-technology-officer` | `executive` | `cto` | Layer 6 Executive Agreement & SG4 Sign-Off | `.agents/workspaces/sprint-3.2/sprint-3.2-cto` |

### 2. Non-Conflicting Concurrency & Directory Whitelisting
To ensure conflict-free parallel execution across agents working on the same user story:
- **Backend Track (`backend-engineer`)**: Writes exclusively to `crates/**` and `backend/**`. Operates under the **Rust Zero-Clone Law** and pure microkernel trait contracts. Junior authors submit PRs to `sprint-3.2-senior-be-1` for code review.
- **Client Track (`client-engineer`)**: Writes exclusively to `apps/storefront/src/features/**` and `packages/**`. Operates under **Locality of Behavior (LoB)** and `@expo/ui` native guidelines. Junior authors submit PRs to `sprint-3.2-senior-fe-1` for code review.
- **Security & Quality Track (`qa-security-auditor`)**: Writes exclusively to `docs/validation/**` and test execution runners. Junior testers submit test suites to `sprint-3.2-senior-qa-1`.
- **Contract Synchronization**: Once PR 2 merges schema definitions and generates TypeScript types via `ts-rs`, Backend (PR 3 & 4) and Client (PR 5, 6 & 7) execute simultaneously without blocking.

### 3. Story-by-Story 7-PR Slicing Pipeline with Junior Author & Senior Reviewer Pairings
Every story in this sprint is decomposed into the standardized 7 PRs with assigned Junior Authors and Senior Reviewers:

#### Story [US-10.1.2]: RFQ negotiation + net-terms (13 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-3.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-3.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-3.2-junior-fe-1` | `sprint-3.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-3.2-junior-fe-2` | `sprint-3.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-3.2-junior-fe-1` | `sprint-3.2-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-10.1.4]: LAN license proxy (8 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-3.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-3.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-3.2-junior-fe-2` | `sprint-3.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-3.2-junior-fe-2` | `sprint-3.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-3.2-junior-fe-1` | `sprint-3.2-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-5.1.3]: Shippo/EasyPost aggregation (5 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-3.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-3.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-3.2-junior-fe-2` | `sprint-3.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-3.2-junior-fe-1` | `sprint-3.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-3.2-junior-fe-2` | `sprint-3.2-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-8.1.2]: Admin copilot (3 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-3.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-3.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-3.2-junior-fe-1` | `sprint-3.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-3.2-junior-fe-2` | `sprint-3.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-3.2-junior-fe-1` | `sprint-3.2-senior-fe-1` | @expo/ui + RTL Parity |

#### Story [US-6.1.2]: Order history (3 Story Points)
- **Layer 5 Product Manager Acceptance**: `sprint-3.2-product-manager`
- **Layer 6 CTO Executive Agreement**: `sprint-3.2-cto`

| PR # | Architectural Slice | Target Layers | Junior Author (Layer 1) | Senior Reviewer (Layer 2) | Gate Requirement |
|:-----|:--------------------|:--------------|:------------------------|:--------------------------|:-----------------|
| **PR 1** | Microkernel Domain Logic & Invariants | `crates/kernel-core`, `crates/some-*` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | Gate M1 + Proptest |
| **PR 2** | Polyglot Database Schema Definitions | `crates/db-schema`, `packages/watermelon-db` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Schema Codegen |
| **PR 3** | Repository Handlers & Caching Tier | `crates/db-dynamo`, `crates/cache-tier`, `crates/search-elastic` | `sprint-3.2-junior-be-1` | `sprint-3.2-senior-be-1` | ETag + L1/L2 Cache |
| **PR 4** | Pure Axum Handlers, Auth Guards & WebMCP | `backend/src/features/...` | `sprint-3.2-junior-be-2` | `sprint-3.2-senior-be-1` | Tower Axum Service |
| **PR 5** | Client Services & Local Database Models | `apps/storefront/src/features/.../services/`, `packages/api-client` | `sprint-3.2-junior-fe-2` | `sprint-3.2-senior-fe-1` | WatermelonDB Sync |
| **PR 6** | Headless Custom Hooks & Domain Logic | `apps/storefront/src/features/.../logic/` | `sprint-3.2-junior-fe-1` | `sprint-3.2-senior-fe-1` | Hooks State Machine |
| **PR 7** | Platform-Adaptive UI & SDUI Renderers | `apps/storefront/src/features/.../designs/` | `sprint-3.2-junior-fe-2` | `sprint-3.2-senior-fe-1` | @expo/ui + RTL Parity |

### 4. Sprint Quality Gates Progression
- [ ] **SG0 (Planning Readiness)**: 100% of backlog stories pass Gate G0; microkernel ports and crate boundaries mapped.
- [ ] **SG1 (Cross-Story Integration)**: End-to-end integration flows across all 5 stories pass under concurrent load.
- [ ] **SG2 (Security & Tenant Isolation)**: Synthetic multi-tenant penetration testing confirms 0 data leaks across sprint endpoints.
- [ ] **SG3 (Architecture & Gate M1/A1/A2)**:
  - Gate M1: `python3 scripts/validation/validate_microkernel.py` passes (zero cloud SDKs in pure crates, zero-clone compliance).
  - Gate A1: `python3 scripts/validation/validate_system_architecture.py` passes (10-layer architectural contracts verified).
  - Gate A2: `python3 scripts/validation/validate_folder_architecture.py` passes (framework-scoped LoB folder layout verified).
- [ ] **SG4 (Release Candidate & Operations)**: Staging smoke tests pass across mobile and web; p95 latency < 150ms; **Product Manager Acceptance (Layer 5)** and **CTO Agreement (Layer 6)** granted.

## End-of-Sprint Test Gate

**Status: Pending — required closeout evidence, not executed test results.** Run this suite at the end of sprint-3.2, on the exact integration/release candidate, before SG4 and CTO review. Earlier story checks remain mandatory. Follow the [sprint closeout policy](../SPRINT_TESTING.md) and attach the [evidence record](../validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md).

- [ ] **E1 — Benchmark tests:** RFQ transitions, credit checks, LAN seat checkout/release, aggregation quotes and paginated order history.
- [ ] **E2 — Integration tests:** RFQ → counter-offer → PO approval → net-terms/reminders using controlled time; proxy lease/seat recovery and carrier fallback without duplicate booking.
- [ ] **E3 — Fuzz tests:** RFQ/PO revisions, invoice/lease formats, seat commands, pagination cursors and malformed copilot tool payloads.
- [ ] **E4 — Loom concurrency tests:** Rust final-seat checkout/release/expiry and workflow wake-up ownership; no double issue, negative seats or lost wake-up. Distributed credit/timer races remain integration tests.
- [ ] **E5 — Independent closeout review:** QA lead records actual test/target/model counts, candidate and baseline commits, tool/environment versions, performance thresholds/results, corpus/reproducers, Loom bounds/completion and independent reviewer decisions. Missing targets, crashes, regressions, unexplored bounds or unreviewed N/A block acceptance; repairing the candidate invalidates affected results.

At SG0, assign test authors and independent senior QA/security/architecture reviewers; approve workload, benchmark baseline/regression thresholds, fuzz time/memory/input budgets and Loom model bounds. Carry forward affected regression suites. E4 is mandatory for applicable changed or affected Rust shared-state synchronization; only the scope-based N/A procedure in the policy can exclude it, with architecture + QA approval and alternative concurrency evidence. A missing implementation/harness is Pending, never N/A or Pass. Keep this section last, including after sprint-plan regeneration.
