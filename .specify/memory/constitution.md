# Project Constitution: Spec-Driven Development & Architectural Governance

## 1. Core Philosophy: Spec-Driven Development (SDD)

`some-commerce` is governed strictly through **Spec-Driven Development (SDD)** powered by GitHub Spec Kit. No code shall be written, refactored, or reviewed without an approved, verified specification.

The lifecycle for every feature, change, and bugfix must follow:
1. **Constitution (`.specify/memory/constitution.md`)**: Foundation of non-negotiable architectural, security, and quality laws.
2. **Specify (`spec.md` / User Stories)**: Defines **what** problem is being solved, the personas, domain requirements, and Gherkin acceptance criteria without premature technical bias.
3. **Architecture & Folder Blueprint**: Maps the specification directly into the strict behavioral hierarchy (`features` -> `modules` -> `behaviours` -> `{services, designs, logic, types, constants}`).
4. **Plan (`plan.md`)**: Formulates the technical blueprint, domain models, state machines, invariants, and data flows.
5. **Tasks (`tasks.md`)**: Deconstructs the plan into ordered, granular, test-driven implementation tasks.
6. **Security Gateway (`security-audit`)**: Enforces threat boundaries, actor matrices, abuse testing, ASVS controls, cryptographic protection, and zero-trust tenant isolation before code execution.
7. **Implementation & Gate Verification (G0–G4)**: Code delivery strictly against the spec, backed by passing automated assertions and gate evidence.

---

## 2. Master Folder Architecture & Framework Scoping Laws

The codebase enforces **Locality of Behavior (LoB)** and **Vertical Slice Architecture** implemented directly **inside framework containers, NOT at the repository root**.

### 2.1 Framework Scoping Principle
- **Client App (Universal Expo SDK 58)**: Located under `apps/storefront/src/features/`.
  - Hierarchy: `apps/storefront/src/features/<feature>/modules/<module>/behaviours/<behaviour>/[services, designs, logic, types, constants]`
- **Backend Services (Rust 2024 Cargo Lambda + Axum 0.8)**: Located under `backend/src/features/` (or `backend/bins/<service>/src/features/`).
  - Hierarchy: `backend/src/features/<feature>/modules/<module>/behaviours/<behaviour>/[services, logic, types, constants]`
- The repository root is reserved strictly for monorepo workspaces (`apps/`, `backend/`, `packages/`, `infra/`, `docs/`, `.specify/`).

### 2.2 The 4-Tier Hierarchical Model (Inside Each Framework)

```
features/
└── <feature-name>/                      # Domain Feature Slice
    ├── _shared/                         # Shared across modules in this feature
    │   ├── services/
    │   ├── designs/                     # (Client only)
    │   ├── logic/
    │   ├── types/
    │   └── constants/
    └── modules/
        └── <module-name>/               # Functional Module
            ├── _shared/                 # Shared across behaviours in this module
            │   ├── services/
            │   ├── designs/             # (Client only)
            │   ├── logic/
            │   ├── types/
            │   └── constants/
            └── behaviours/
                └── <behaviour-name>/    # Concrete Autonomous Behaviour
                    ├── services/        # API clients / handlers, queries, mutations
                    ├── designs/         # UI components, screens, SDUI widgets (Client)
                    ├── logic/           # Domain state machines, custom hooks, validation
                    ├── types/           # Interfaces, DTOs, schemas, models
                    └── constants/       # Config keys, routes, error codes, limits
```

### 2.3 Framework-Level Shared Tier (`shared/`)

Items that cut across multiple distinct features inside a framework are placed in that framework's shared tier:
- Client (`apps/storefront/src/shared/`): Core design tokens, global theme provider, typography primitives, toast/dialog containers.
- Backend (`backend/crates/kernel-core/` or `backend/src/shared/`): Global transport clients, DynamoDB client wrapper, KMS crypto client, Redis L2 cache connection multiplexer, EventBridge dispatcher, `Money` arithmetic, RFC 9110 ETag generator, i18n locale resolver.

### 2.4 Strict Colocation & Promotion Rules

1. **Locality of Behavior (Default)**: Everything required to implement a behaviour MUST reside inside that behaviour's directory (`features/<F>/modules/<M>/behaviours/<B>/`). Never preemptively abstract code to a shared folder.
2. **Promotion to Module Shared (`_shared`)**: When and only when a type, validator, or service is needed by two or more behaviours within the same module `M`, it is promoted to `features/<F>/modules/<M>/_shared/`.
3. **Promotion to Feature Shared (`_shared`)**: When and only when an asset is needed by two or more modules within the same feature `F`, it is promoted to `features/<F>/_shared/`.
4. **Promotion to Global Shared (`shared/`)**: An asset is promoted to the global root `shared/` only when it is a true cross-cutting concern used across multiple top-level features.
5. **No Cross-Behaviour Sibling Imports**: A behaviour in module `M` MUST NOT directly import private files from a sibling behaviour in module `M`. If communication or reuse is needed, promote the shared contract to `_shared/` or invoke via domain ports.

---

## 3. Rust Code Performance & Memory Law: Zero-Clone & Borrowing Discipline

To guarantee sub-millisecond execution, zero-copy performance, and minimal memory footprint in high-concurrency AWS Lambda / Graviton4 environments:

1. **Strict Clone Prohibition**:
   - Rust code MUST NEVER call `.clone()` on data structures, structs, strings, vectors, payloads, or domain entities.
   - Calling `.clone()` to appease the borrow checker is strictly forbidden and constitutes an architectural violation that fails code review and CI.
2. **Explicit Reference Counting Exception**:
   - The **ONLY** permitted exception to `.clone()` is for cloning reference-counted pointer handles:
     - `std::sync::Arc<T>`: Thread-safe shared state (e.g. `Arc<DynamoDbClient>`, `Arc<JwksCache>`, `Arc<MokaCache>`).
     - `std::rc::Rc<T>`: Single-threaded reference counting where applicable.
   - Prefer `Arc::clone(&handle)` syntax over `handle.clone()` to make pointer-count increments explicit and distinguish them from value deep copies.
3. **Dependence on Borrowing & Lifetimes**:
   - All function signatures, handlers, validators, parsers, and data transformers must strictly depend on **borrowing**:
     - Pass immutable references `&T` or slices (`&str`, `&[T]`) by default.
     - Use mutable borrows `&mut T` when in-place mutations are needed.
     - Leverage Rust explicit lifetimes (`'a`) to borrow data across request contexts without heap reallocations.
4. **Zero-Copy Serialization & Deserialization**:
   - Use `serde` borrowed types (`&'a str`, `std::borrow::Cow<'a, str>`) when deserializing JSON/CBOR payloads.
   - Utilize zero-copy byte buffers (`bytes::Bytes`) for streaming network payloads and HTTP bodies.
5. **Compiler & Clippy Enforcement**:
   - Cargo workspace `clippy.toml` must enforce:
     - `#![deny(clippy::clone_on_ref_ptr)]`
     - `#![warn(clippy::redundant_clone)]`
     - Code reviews must reject deep `.clone()` or frivolous `.to_owned()` / `.to_string()` on referenced data.

---

## 4. Security-Audit Integration & Security Gateways

Every user story and specification must incorporate a **Security Gateway** governed by the `security-audit` skill.

### 4.1 Non-Negotiable Security Invariants
- **Zero-Trust Multi-Tenancy**: Every request, query, cache key, and event MUST be explicitly partitioned by `TenantId`. Cross-tenant data leakage is a critical blocker.
- **Server-Side Authority**: Client inputs and client-asserted roles are untrusted. Permissions, prices, discount math, and stock availability must be validated strictly on the server.
- **Strict Authorization (RBAC/ABAC & IDOR Prevention)**: Object-level authorization (`sub` ownership or organization role) must be verified on every read, write, update, and delete operation.
- **Cryptographic Protection**: Sensitive data (tokens, API keys, private keys, payment credentials) must be encrypted using AWS KMS / AES-256-GCM / Ed25519. Production credentials or customer PII must never appear in logs, client bundles, or test fixtures.
- **Anti-Abuse & Rate Limiting**: All public or credential-accepting endpoints (SMS OTP, login, checkout, search, WebMCP tools) must have token bucket or sliding window rate limiting.
- **Zero Critical / High Findings**: No user story or PR may be merged with unresolved critical or high security vulnerabilities.

---

## 5. Quality Gates Standard (G0–G4)

- **G0 (Ready)**: Stable identifiers (`AC-*`, `TC-*`), dependency resolution, threat boundary mapping, measurable performance budgets.
- **G1 (Test Coverage)**: 90% line and 85% branch coverage in affected packages; 95% branch coverage in critical domain rules (auth, money, stock, licensing).
- **G2 (Security Audit)**: Formal security gateway sign-off, SAST, DAST, abuse testing, ASVS verification, 0 critical/high findings.
- **G3 (Architecture & Maintainability)**: Strict adherence to the `features -> modules -> behaviours` folder hierarchy, zero-clone borrowing discipline in Rust, verified import boundaries, zero circular dependencies.
- **G4 (Integrated Acceptance)**: End-to-end sandbox execution across affected web/mobile platforms, metrics recorded, release candidate verified.

---

## 6. Microkernel Architecture & Cloud Portability Law

1. **Pure Microkernel Domain Crates (`crates/some-*`)**:
   - Core domain business logic, validators, pricing math, ticket state machines, and license verification MUST be packaged into pure, standalone crates.
   - Microkernel crates must have **zero dependencies** on cloud vendor SDKs (`aws-sdk-*`, `azure-*`, `google-cloud-*`), zero direct database drivers, and zero network runtimes.
   - Microkernel crates must be publishable to [crates.io](https://crates.io) and target `wasm32-unknown-unknown` for edge execution.
2. **Axum HTTP Transport Decoupling**:
   - HTTP APIs in `backend/src/features/` must be pure `axum::Router` functions and Tower services.
   - Axum routers and handlers **MUST NEVER** import `lambda_http`, `aws_lambda_events`, or Cargo Lambda runtime packages.
   - Cargo Lambda runtime (`lambda_http::run`) is strictly restricted to thin entrypoint wrappers in `backend/bins/lambda-serverless/src/main.rs`.
   - The same Axum router must run unaltered under `axum::serve` in `backend/bins/standalone-server/src/main.rs` for portable Docker, GCP Cloud Run, Azure Container Apps, or bare metal deployments.
3. **Hexagonal Ports-and-Adapters**:
   - Backend features interact with external infrastructure (blob storage, database, messaging, AI inference) strictly through trait ports (`BlobStoragePort`, `DocumentDbPort`, `MessagingPort`).
   - Cloud vendor adapters (AWS, GCP, Azure) implement these traits without leaking proprietary SDK types into domain logic.

---

## 7. Sprint-Level Quality Gates (SG0–SG4 & Gate M1)

Every sprint delivery milestone must pass the five sprint-level quality gates before completion:
- **SG0 (Planning Readiness)**: 100% of backlog stories meet G0; microkernel ports and crate boundaries resolved.
- **SG1 (Cross-Story Integration)**: End-to-end multi-module flows verified under realistic integration suites; monorepo coverage maintained $\ge 90\%$ line and $\ge 85\%$ branch.
- **SG2 (Security & Multi-Tenant Audit)**: Synthetic penetration testing verifies zero cross-tenant data leaks; 0 Critical/High CVEs; OWASP ASVS L2 verification.
- **SG3 (Architecture & Gate M1 Compliance)**:
  - Automated execution of **Gate M1** (`scripts/validation/validate_microkernel.py`):
    - Crate Purity: Zero cloud SDKs or direct DB drivers in pure domain crates.
    - Transport Decoupling: Zero `lambda_http` imports in Axum routers.
    - Zero-Clone Law: Zero deep `.clone()` calls on domain structs (strict borrowing and `Arc::clone` only).
  - Framework-scoped LoB directory validation passes 100%.
  - Code duplication $< 3\%$; cyclomatic complexity $\le 10$.
- **SG4 (Release Candidate & Operations)**: Staging smoke tests pass across web and native mobile; p95 latency $< 150\text{ms}$; automated cloud provisioning verified.

### 7.1 Mandatory end-of-sprint test suite

Every sprint MUST end with **benchmark tests, integration tests, fuzz tests and applicable Rust Loom concurrency tests**, plus independent review of their evidence, before SG4 and CTO review. Put the sprint-specific targets at the end of its plan and approve authors, independent reviewers, baseline/workload, measurable thresholds, resource budgets and model bounds at SG0. Follow [the sprint testing policy](../../docs/SPRINT_TESTING.md) and [evidence template](../../docs/validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md).

Benchmarks compare the exact candidate to the last accepted comparable baseline and absolute budgets. Integration tests exercise cross-story storage/event/provider/client behavior and affected regressions. Fuzzing uses assertion-based adversarial input/state generation, bounded resources and saved regression replay. Loom tests instrument the actual Rust coordination algorithm, finish the declared bounded exploration and report assumptions/limits; they do not establish distributed database/provider correctness. A sprint with no changed or affected Rust shared-state coordination needs independent architecture + QA approval for E4 N/A and alternative concurrency evidence. Missing applicable code/harnesses, zero collected tests, crashes, incomplete exploration or absent evidence are Pending/Fail, never Pass or N/A. Candidate repairs invalidate affected results and require independent re-review before promotion. Sprint-plan generation must preserve these final gates.

---

## 8. Universal Agent Launch & Spec Kit Law

These requirements govern **every agent**, including juniors, seniors, QA, security, architecture, design, orchestration, DevOps, PM, gatekeeper and CTO agents. A title or seniority label grants no additional runtime authority.

1. **Mandatory launch order**: Give each agent (a) its role, job title, responsibilities and decision limits; (b) job context with approved source revisions and dependencies; then (c) the detailed task, steps, deliverables, affected paths, validation commands, stop conditions and handoff requirements. No generic role prompt can replace a task-specific brief.
2. **Spec Kit chain for all roles**: Every assignment MUST reference and acknowledge the approved constitution → specification/ACs → architecture/plan → task IDs → Security Gateway → gate evidence chain. Governance, review, fixes and release work require this chain too. Existing story sections can supply these artifacts; missing or stale references block admission. Planning-only assignments follow section 10: an approved upstream request/charter commissions the missing artifacts without authorizing implementation.
3. **Traceable assignments**: Record assignment/attempt ID, owner, base/candidate commit, spec/plan/tasks/policy/contract revisions, AC/TC/task mapping, exact write scope, dependencies, reviewer identities, budgets and expected evidence. Every reassignment receives a fresh brief; never inherit a previous story's mutable context.
4. **Authority and independence**: Effective capabilities are bounded by existing session authorization, host controls, profile policy and the assignment lease. Agents cannot grant themselves permissions, modify final evidence, bypass failed gates or obtain production authority by claiming a leadership title. Contributor identities and approvals must be independently authenticated.
5. **Scope changes**: Ambiguity or requirement changes go to the accountable spec owner. Update approved Spec Kit artifacts, re-plan and invalidate affected work/evidence before proceeding. Do not weaken acceptance criteria to make a test pass.
6. **Shared authentication pools**: `agent-a`, `agent-b` and `agent-c` are all eligible for every role. Job titles MUST NOT permanently bind to one account. Select available accounts through usage reservations, configured local budgets/cooldowns and concurrency limits; record quota estimates separately from actual provider evidence. Account rotation neither expands task authority nor establishes independent review. Quota failures require reconciliation before any fresh attempt; do not automatically replay partially executed work or guess provider reset times.

The normative launch schema and isolation/evidence requirements are in [the agent framework](../../docs/AGENT_PROFILES_AND_MULTI_AGENT_FRAMEWORK.md); accountable job-title responsibilities and independent validation layers are in [company roles](../../docs/COMPANY_ROLES_AND_AGENT_PROFILES.md).

## 9. Continuous Pipeline & Parallel Junior Law

1. **Dependency-driven parallelism**: Multiple juniors may implement independent PRs concurrently within or across stories. Admit work only when its approved task DAG prerequisites, stable contract revisions, non-overlapping writer leases, capacity and reviewer requirements are satisfied. PR numbers or job titles alone must not serialize independent work. Shared files/contracts require a single writer or explicit sequencing.
2. **Immediate worker reuse**: When a junior's valid immutable implementation handoff is durably accepted, enqueue senior validation, stop and release that candidate's writer lease, and assign the junior the next eligible READY story/task in the same scheduling cycle. Junior reassignment MUST NOT wait for the prior story's senior/PM/CTO approval. Submission is not story completion; G4 remains required.
3. **Continuous validation**: Senior review runs independently of the junior's next assignment. Accepted results durably advance the exact candidate through senior validation → security/architecture → integration → PM acceptance → CTO/release review. Independent checks may run concurrently; required predecessors must pass before promotion. A release candidate may group multiple accepted stories.
4. **Senior fixes are allowed and accountable**: A senior may fix an in-scope defect through a separate Spec Kit remediation task, fresh candidate and bounded write lease, or route it to another eligible engineer. The original junior can continue its next independent story. Record the finding and regression test before closing it; requirement changes need spec-owner approval.
5. **No self-approval after repair**: Any reviewer who changes relevant code, tests, fixtures or policy becomes a contributor. Another qualified non-contributing reviewer MUST validate the repair. New candidate revisions invalidate affected tests, security/design reviews and downstream acceptance; rerun them before advancing. Apply the same rule to fixes requested at any later layer, including CTO review.
6. **Reliable handoffs and recovery**: Persist decisions and successor events atomically or through a transactional outbox. Queue delivery is idempotent by assignment/candidate/stage/attempt. Recover after restart, reject stale lease/fencing tokens, and prevent duplicate callbacks from reassigning an already-busy worker or creating duplicate merge/release actions.
7. **Liveness with bounded work**: Approve numeric dispatch/watchdog/review deadlines, stage capacities, queue limits and repair/retry budgets before sprint execution. Monitor idle-with-ready workers, queue age, stalled stages and ownership. Recover or escalate overdue work; never auto-approve it. Reserve review/remediation capacity and throttle new implementation when review backlog limits are reached. Budgets apply across reassignments so repair loops cannot run indefinitely.
8. **Honest waiting and completion**: Continue unaffected READY work while another story is blocked or under review. If no eligible work exists, report waiting/blocked with reasons, owner and next action. Respect authorized pause/stop controls. Report the included backlog complete only after required G4/CTO decisions and sprint gates pass, active work and outgoing queues drain, and no unresolved repair/blocker remains. CTO acceptance does not itself authorize production deployment or publication.

These are mandatory design and acceptance requirements, **not a claim of implemented orchestration or continuous availability**. Before unattended adoption, independently demonstrate junior A-handoff/B-reassignment overlapping senior A-validation, senior repair followed by another reviewer, progression to CTO, crash-safe handoffs, stale-worker fencing, review backpressure and recovery. Runtime gaps remain visible until that evidence exists.

## 10. Top-Down Planning, Division of Work and Upward Validation Law

The company pipeline MUST start at leadership and return to leadership: **authorized request → CTO charter → PM specification → architect/specialist subplans → tech-lead master implementation plan → approved role/task decomposition → parallel junior/role execution with senior validation → collection of all expected outputs → integrated QA/security/architecture and sprint tests → PM acceptance → CTO final review**.

1. CTO direction defines goals/non-goals, constraints and success criteria within existing user authority. PM produces stable requirements/ACs. The architect coordinates shared contracts, data/domain ownership and affected specialist plans. Seniors, QA/security, design and DevOps contribute bounded role-specific plans; the tech lead reconciles them into one versioned Spec Kit master plan and dependency DAG before junior dispatch.
2. Use [the company plan template](../templates/company-plan-template.md). Every child/assignment retains the master-plan revision and parent node, requirements, owned paths, dependency conditions, expected deliverables, test obligations, independent reviewers and its next upward handoff. Reject orphan tasks, duplicated ownership, missing requirements and unresolved shared contracts. Assign only affected roles/layers, with justified omissions.
3. Planning assignments may start from an approved upstream request/charter plus a bounded planning task and produce the missing draft spec/plan/tasks. They cannot pretend their own draft is approved or implement production changes. Implementation/remediation admission requires actual approved feature plans, Security Gateway, G0/SG0 and recorded planning approvals from the accountable product/architecture/security/CTO owners.
4. Execute independent approved tasks concurrently and continuously reassign available juniors; preserve senior validation and independently reviewed repair loops. A top-down plan is not a reason to serialize independent branches or hold juniors idle until CTO acceptance.
5. Before fan-out, each parent declares an expected-child manifest. Collect every included child's exact revision, outputs and independently reviewed evidence; missing/failed/stale children block that parent's completion. Explicit scope changes revise the manifest and invalidate affected descendants/reviews.
6. Reconcile and validate the exact combined candidate, shared interfaces, end-to-end outcomes and E1–E5 sprint tests. Return the charter/AC-to-delivery dossier through senior → tech lead → QA/security/architecture → PM → CTO. Individual PR passes do not prove whole-system acceptance.
7. CTO final review records Accepted, Changes Required or Blocked with reasons and affected plan nodes. Replan from the responsible owner and revalidate affected dependencies; keep unrelated approved work moving. Initial CTO plan approval never pre-approves delivery, and final acceptance does not itself authorize production deployment.

## 11. One Authoritative Record for Every User Story

Each story has exactly one canonical record at `docs/validation/story-records/US-<id>.md`, initialized when the story enters planning from [the story record template](../../docs/validation/STORY_RECORD_TEMPLATE.md). Every role/task, plan node, PR, test run and handoff MUST reference that record. Specifications remain the authority for requirements; immutable logs/build artifacts stay in their appropriate storage but are indexed from this single record.

Record every story-related operational action and outcome: context/spec reads, plan/decision changes, assignments, tool/command executions, file/contract changes, provider operations, tests/benchmarks/fuzz/Loom results, reviews/findings, repairs, approvals/rejections, blocked/recovery events, account/worker changes and handoffs through final CTO review. Record observable actions/evidence, not private reasoning, credentials or raw sensitive data. Shared multi-story actions link the same event/artifact IDs into each affected story record.

The trusted controller serializes appends with unique event IDs, sequence/revision checks and idempotent replay. Preserve historical entries; correct them through linked new events. Agents submit scoped event proposals and draft evidence, never rewrite approval history or certify themselves. A mutable Markdown file alone does not enforce these guarantees; runtime collection/storage and authenticated writers still require implementation evidence.

Before a role starts, acknowledge the record's current revision, approved plan/candidate, prior findings and assigned next action. Log action intent before side effects and its result/failure afterward; crash reconciliation completes unknown outcomes before retries. Failure to durably record required actions blocks further side effects and promotion. Before handoff, reconcile expected tasks/actions/artifacts, update the current-status snapshot, record ownership transfer and next-role acknowledgment, and preserve unresolved blockers. Missing history, stale handoff or absent evidence blocks acceptance; never invent retrospective events to claim completeness.

