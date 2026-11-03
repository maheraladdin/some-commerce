# Tasks Template: [Feature / Story Name]

## Assignment & Continuous Pipeline Contract

Complete this section for implementation, testing, review, remediation and leadership tasks. Follow constitution sections 8–9; unresolved required fields block dispatch.

| Field | Required value |
|:------|:---------------|
| Role and job-title context | Agent title, responsibilities, accountable lead and decision limits |
| Company-plan lineage | Approved CTO charter/master-plan revision, parent node and expected-child manifest entry |
| Canonical story record | `docs/validation/story-records/US-<id>.md`, acknowledged revision, action-event IDs and next-role handoff |
| Spec Kit inputs | Approved constitution, spec/ACs, plan, task list and Security Gateway revisions |
| Detailed task | Stable task/AC/TC IDs, steps, observable outcome, deliverables and non-goals |
| Dependencies and concurrency | Prerequisite task/evidence revisions; independent parallel tasks; shared-file constraints |
| Ownership and authority | Assignment/attempt ID, exact leased paths, workspace, capabilities and stop conditions |
| Validation | Required commands, assertions, environment, artifacts and independent reviewer identities |
| Scheduling limits | Dispatch/review deadlines, WIP/queue capacity, retry/repair budget and escalation owner |
| Successor handoff | Immutable candidate, durable next-stage queue event and worker-release acknowledgment |
| Remediation | Finding/task link, fix owner, fresh candidate, affected invalidations and non-contributing reviewer |

- [ ] Junior submission queues senior validation and releases the worker for the next independent READY story/task without waiting for final approval.
- [ ] Senior validation/fixes have separate assignments; a contributor cannot approve their own repair.
- [ ] Accepted candidates advance through security/architecture, integration, PM and CTO/release review with current evidence.
- [ ] Missing prerequisites/review capacity, full queues or exhausted repair budgets produce explicit blocked/waiting states and bounded escalation.
- [ ] Story completion requires G4; backlog completion also requires applicable CTO/sprint decisions and drained queues, not just finished implementation.
- [ ] Read/acknowledge the canonical record before work; log each action intent and result/failure, link artifacts and update the snapshot before next-role acknowledgment. Missing history blocks promotion.
- [ ] Planning-only tasks name approved upstream direction and draft outputs; implementation tasks require approved master/role plans. Parent completion reconciles all expected child outputs and integrated evidence before upward PM/CTO return.

## The 10-PR Vertical Slicing Framework (Aligned with 10-Pillar System Architecture)

```
[PR 1: Kernel Core] ──> [PR 2: DB Schema] ──> [PR 3: Repositories] ──> [PR 4: L2 Redis] ──> [PR 5: L1 Moka]
                                                                                                 │
[PR 10: Platform UI] <── [PR 9: Headless Hooks] <── [PR 8: WatermelonDB] <── [PR 7: TanStack Query] <── [PR 6: ETag & Axum]
```

| PR # | Pillar | Architectural Layer | Primary Targets & Crates | Deliverables & Definition of Done | Accountable Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PR 1** | **Pillar 1** | **Microkernel Domain Logic & Plugin Ports** | `crates/kernel-core`, `crates/plugins-*` | Pure vendor-agnostic Rust domain rules, trait definitions, value objects, and property unit tests. | `junior-backend-engineer` / `senior-backend-engineer` |
| **PR 2** | **Pillar 2** | **Polyglot Database Schema Definitions** | `crates/db-schema`, `packages/watermelon-db` | DynamoDB keys (`PK = TENANT#<id>`, `SK`, GSIs), OpenSearch nested mappings, WatermelonDB schemas. | `junior-backend-engineer` / `senior-backend-engineer` |
| **PR 3** | **Pillar 3** | **Repository Adapters & Infrastructure Connectors** | `crates/db-dynamo`, `crates/search-elastic`, `crates/notify-sns`, `crates/kms-vault` | DynamoDB CRUD, KMS envelope encryption, OpenSearch query integration, and SNS notifications. | `junior-backend-engineer` / `senior-backend-engineer` |
| **PR 4** | **Pillar 4** | **Distributed L2 Cache & Invalidation Engine** | `crates/cache-tier` | ElastiCache Redis connection pool, pipelined data/etag caching, and pub/sub eviction channels. | `junior-backend-engineer` / `senior-backend-engineer` |
| **PR 5** | **Pillar 5** | **In-Process L1 Moka Cache & Request Coalescing** | `crates/cache-tier` | In-memory Moka cache (sub-50µs lookups) and `try_get_with` request coalescing against thundering herds. | `junior-backend-engineer` / `senior-backend-engineer` |
| **PR 6** | **Pillar 6** | **HTTP ETag Protocol & Pure Axum Handlers** | `bins/*`, `backend/src/features/.../services/` | RFC 9110 BLAKE3 ETag generator, 304 conditional request middleware, Cognito JWT extractors. | `junior-backend-engineer` / `senior-backend-engineer` |
| **PR 7** | **Pillar 7** | **Frontend Server-State Caching (TanStack Query)** | `packages/query-client`, `apps/storefront/.../services/` | TanStack Query hooks, `fetchWithEtag` client interceptor resolving 304 from local cache. | `junior-client-engineer` / `senior-client-engineer` |
| **PR 8** | **Pillar 8** | **Client-First Local Database (WatermelonDB Sync)** | `packages/watermelon-db`, `apps/storefront/.../services/` | WatermelonDB reactive models, SQLite/IndexedDB adapters, and delta sync against `/v1/sync`. | `junior-client-engineer` / `senior-client-engineer` |
| **PR 9** | **Pillar 9** | **Headless Custom Hooks & Logic Abstraction** | `packages/domain-hooks`, `apps/storefront/.../logic/` | Headless custom React hooks isolating state machines, domain math, and validation with zero UI markup. | `junior-client-engineer` / `senior-client-engineer` |
| **PR 10** | **Pillar 10** | **Platform-Adaptive UI Design & Native Modules** | `apps/storefront/.../designs/`, `packages/ui-primitives` | Native presentation using `@expo/ui` primitives (+ native modules) for iOS/Android, semantic HTML5 + Tailwind CSS for Web; Arabic RTL parity. | `ui-ux-designer` (presentation) / `client-engineer` (wiring) |

## Phase 1: Core Domain Logic, Types & Constants (PR 1–2)
- [ ] Task 1.1: Define strongly typed models in `behaviours/<name>/types/`
- [ ] Task 1.2: Define routes, error keys, and limits in `behaviours/<name>/constants/`
- [ ] Task 1.3: Implement pure domain logic & state machines in `behaviours/<name>/logic/`
- [ ] Task 1.4: Write unit and property tests verifying domain invariants

## Phase 2: Services & Infrastructure Adapters (PR 3–6)
- [ ] Task 2.1: Implement API client / repository adapters in `behaviours/<name>/services/`
- [ ] Task 2.2: Implement RFC 9110 ETag headers and caching integration
- [ ] Task 2.3: Integrate WatermelonDB local-first persistence or server sync
- [ ] Task 2.4: Write service integration and mock-free contract tests

## Phase 3: Designs & Platform-Adaptive UI (PR 7–10)
- [ ] Task 3.1: Build platform-adaptive UI screens / components in `behaviours/<name>/designs/`
- [ ] Task 3.2: Connect Headless Hooks from `logic/` to UI components in `designs/`
- [ ] Task 3.3: Implement RTL/LTR bidirectional styling and localized fonts
- [ ] Task 3.4: Write component tests for loading, empty, error, and offline states

## Phase 4: Quality Gate Verification & Release Readiness (G0–G4 + G-Review + G-Borrow + G-UI + G-Law)
- [ ] Task 4.1: Execute security audit abuse tests (rate limits, IDOR, tampering)
- [ ] Task 4.2: Verify zero-trust tenant isolation on all queries and mutations (`PK = TENANT#<id>`)
- [ ] Task 4.3: Execute SAST / secret scanning / dependency checks
- [ ] Task 4.4: Complete G2 Security Gateway sign-off and compile integrated evidence
- [ ] Task 4.5: Complete G-Review independent senior code review across 5 pillars
- [ ] Task 4.6: Verify Gate R1 / G-Borrow zero deep `.clone()` borrowing discipline in backend code
- [ ] Task 4.7: Verify Gate F1 / G-UI `@expo/ui` mobile and semantic HTML/Tailwind web presentation
- [ ] Task 4.8: Verify Gate L1 / G-Law global e-commerce statutory legal compliance (`[AC-US-X.Y.Z-LAW]`)
- [ ] Task 4.9: Complete Gate G4 integrated sandbox validation across target platforms

## Phase 5: End-of-Sprint Test Gate (before SG4 / CTO review)

- [ ] Task 5.1: Run scoped benchmark tests against the approved comparable baseline and absolute budgets; capture workload, variance and resource metrics.
- [ ] Task 5.2: Run cross-story integration and affected regression suites on the exact candidate with real isolated components where required; assert failure/recovery state and side-effect counts.
- [ ] Task 5.3: Run fuzz targets within approved budgets, replay saved corpora, minimize failures and add deterministic regression tests.
- [ ] Task 5.4: Run applicable instrumented Rust Loom models to completed declared exploration; record bounds and limitations. Scope-based N/A needs architecture + QA review; missing applicable harnesses remain Pending.
- [ ] Task 5.5: Attach `docs/validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md` results and independent decisions for E1–E5. Rerun affected suites after repairs; enqueue SG4/CTO review only with current passing evidence.
