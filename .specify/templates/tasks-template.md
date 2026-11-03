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

## Phase 1: Core Domain Logic, Types & Constants
- [ ] Task 1.1: Define strongly typed models in `behaviours/<name>/types/`
- [ ] Task 1.2: Define routes, error keys, and limits in `behaviours/<name>/constants/`
- [ ] Task 1.3: Implement pure domain logic & state machines in `behaviours/<name>/logic/`
- [ ] Task 1.4: Write unit and property tests verifying domain invariants

## Phase 2: Services & Infrastructure Adapters
- [ ] Task 2.1: Implement API client / repository adapters in `behaviours/<name>/services/`
- [ ] Task 2.2: Implement RFC 9110 ETag headers and caching integration
- [ ] Task 2.3: Integrate WatermelonDB local-first persistence or server sync
- [ ] Task 2.4: Write service integration and mock-free contract tests

## Phase 3: Designs & Platform-Adaptive UI
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
