# Multi-Agent Orchestration Framework & 3 Core Agent Profiles

## 1. Executive Summary

`some-commerce` employs a scalable multi-agent engineering framework designed to deliver high-velocity, conflict-free parallel implementation across all 12 sprints.

The framework is founded on **3 Core Agent Profiles**:
1. **`backend-engineer`**: Systems, Microkernel & Axum API Engineer
2. **`client-engineer`**: Universal Expo SDK 58, React Native & Web UI Engineer
3. **`qa-security-auditor`**: OWASP ASVS Security, Invariant Verification & Gatekeeper Lead

Within any sprint, **multiple agent instances** can be spawned from these 3 profiles to operate in parallel on the same user story or across multiple user stories. Conflict-free operation is guaranteed through **physical directory isolation**, **strict write-boundary whitelisting**, and the standardized **7-PR Vertical Slicing Pipeline**.

Every agent instance operates inside its own dedicated **Sprint-Level Working Directory (`workdir`)** with tailored context files and isolated Git worktrees.

---

## 2. The 3 Core Agent Profiles

```mermaid
flowchart TD
    subgraph "Core Agent Profiles"
        P1["Profile 1: backend-engineer<br/>(Rust 2024 / Axum / Microkernel)"]
        P2["Profile 2: client-engineer<br/>(Expo SDK 58 / React Native / Tailwind)"]
        P3["Profile 3: qa-security-auditor<br/>(ASVS L2 / Gate M1 / CI Gatekeeper)"]
    end

    subgraph "Specialized Agent Instances (Spawned per Story / PR)"
        A_BE_BUILD["backend-builder<br/>• PR 1: Microkernel Logic<br/>• PR 2: Polyglot Schemas<br/>• PR 3: DB Repos & Caching<br/>• PR 4: Axum Route Handlers"]
        A_BE_TEST["backend-tester<br/>• Proptest Invariant Tests<br/>• Repository Integration Tests<br/>• Concurrency & Fault Suites"]
        
        A_FE_BUILD["client-builder<br/>• PR 5: Axios & WatermelonDB<br/>• PR 6: Custom Domain Hooks<br/>• PR 7: @expo/ui & Tailwind UI"]
        A_FE_TEST["client-tester<br/>• Jest & RNTL Unit Tests<br/>• Offline Sync Mock Tests<br/>• WCAG 2.1 AA a11y Audits"]
        
        A_SEC["security-tester<br/>• Threat Matrix Fuzzing<br/>• Multi-Tenant Isolation Pentest<br/>• Injection & SSRF Checks"]
        A_GATE["gatekeeper<br/>• G0–G4 & SG0–SG4 Gates<br/>• Gate M1 Zero-Clone Audit<br/>• PR Review & Merge Sign-Off"]
    end

    P1 --> A_BE_BUILD
    P1 --> A_BE_TEST
    P2 --> A_FE_BUILD
    P2 --> A_FE_TEST
    P3 --> A_SEC
    P3 --> A_GATE
```

### 2.1 Profile 1: `backend-engineer`
* **Primary Scope**: Rust 2024 microkernel packages, polyglot database schemas, repository caching handlers, and pure Axum HTTP routers.
* **Governing Rules**:
  * **Rust Zero-Clone Law**: Strict prohibition of `.clone()` on domain structs, payloads, and strings. Code must rely on borrowing (`&T`, `&mut T`), lifetimes (`'a`), and zero-copy byte buffers (`bytes::Bytes`). Reference counting is restricted exclusively to `Arc::clone(&handle)` for thread-safe state pointers.
  * **Microkernel Logic Purity (Gate M1)**: Zero cloud vendor SDKs (`aws-sdk-*`, `azure_*`, `google-cloud-*`), zero direct database drivers, and zero network runtimes inside `crates/some-*`.
  * **Axum Decoupling Law**: Axum router functions in `backend/src/features/` must be pure Tower services and must NEVER import `lambda_http`.
* **Allowed Paths**:
  * `crates/**`
  * `backend/src/features/<feature>/modules/<module>/behaviours/<behaviour>/[services, logic, types, constants]`
  * `backend/bins/**`
* **Specialized Instances**:
  * `backend-builder`: Writes domain math, state machines, schemas, repositories, and Axum handlers.
  * `backend-tester`: Writes unit tests, property tests (`proptest`), and repository integration tests without modifying production code.

### 2.2 Profile 2: `client-engineer`
* **Primary Scope**: Universal Expo SDK 58 React Native mobile app and Tailwind-styled Web app located under `apps/storefront/src/features/`.
* **Governing Rules**:
  * **Locality of Behavior (LoB)**: Code must strictly adhere to the 4-tier folder hierarchy (`features -> modules -> behaviours -> [services, designs, logic, types, constants]`).
  * **Offline-First Resilience**: All read and mutation paths must integrate with WatermelonDB local SQLite/IndexedDB and TanStack Query v5 cache.
  * **Platform Adaptation**: Use `@expo/ui` native components for iOS/Android, Tailwind CSS for Web, and SDUI AST renderers.
  * **Accessibility & Localization**: Mandatory support for Arabic (`ar-EG`, RTL) and English (`en-US`, LTR), meeting WCAG 2.1 AA standards.
* **Allowed Paths**:
  * `apps/storefront/src/features/<feature>/modules/<module>/behaviours/<behaviour>/[services, designs, logic, types, constants]`
  * `apps/storefront/src/shared/**`
  * `packages/api-client/**`, `packages/watermelon-db/**`, `packages/query-client/**`
* **Specialized Instances**:
  * `client-builder`: Writes API client services, WatermelonDB actions, custom hooks, and UI screens.
  * `client-tester`: Writes Jest component tests, React Native Testing Library suites, and offline sync mock tests.

### 2.3 Profile 3: `qa-security-auditor`
* **Primary Scope**: Security Gateways, OWASP ASVS verification, Gate M1 microkernel audits, and sprint quality gate sign-off.
* **Governing Rules**:
  * **Zero Critical/High Vulnerabilities**: Every PR must pass SAST, dependency scans, and secret audits with zero critical/high findings.
  * **Zero-Trust Multi-Tenancy**: All queries, cache keys, and data mutations must be partitioned by `TenantId`.
  * **Strict ASVS L2 Conformance**: Enforce authorization checks on every operation, preventing IDOR, injection, and privilege escalation.
  * **Gatekeeper Review**: Enforces G0–G4 and SG0–SG4 sign-offs before any branch or PR is merged.
* **Allowed Paths**:
  * `docs/validation/**`
  * `scripts/ci/**`
  * Security scanning configs (`deny.toml`, `.audit.json`)
* **Specialized Instances**:
  * `security-tester`: Executes adversarial penetration testing, injection attacks, IDOR checks, and rate-limiting fuzzing.
  * `gatekeeper`: Reviews test coverage ($\ge 90\%$ line / $\ge 85\%$ branch), verifies Gate M1, and executes PR merge certifications.

---

## 3. Conflict-Free Orchestration: The 7-PR Slicing Pipeline

To eliminate merge conflicts and allow multiple agents from the same profile to work simultaneously on the same user story, work is partitioned into **7 ordered, discrete Pull Requests**:

```mermaid
flowchart TD
    subgraph "PR 1: Microkernel Logic"
        PR1["PR 1: crates/kernel-core & crates/some-*<br/>Pure domain rules, value types, math calculations, proptests<br/><b>Agent: backend-builder + backend-tester</b>"]
    end

    subgraph "PR 2: Polyglot Database Schemas"
        PR2["PR 2: crates/db-schema & packages/watermelon-db<br/>DynamoDB keys (PK/SK), OpenSearch mappings, WatermelonDB schema, ts-rs codegen<br/><b>Agent: backend-builder + client-builder</b>"]
    end

    subgraph "Parallel Backend & Client Tracks"
        direction LR
        subgraph "Backend Track"
            PR3["PR 3: crates/db-dynamo & crates/cache-tier<br/>DynamoDB CRUD, TransactWriteItems, Moka L1, Redis L2, BLAKE3 ETag<br/><b>Agent: backend-builder + backend-tester</b>"]
            --> PR4["PR 4: backend/src/features/...<br/>Pure Axum Router, Tower middleware, Cognito JWT auth guards, WebMCP tools<br/><b>Agent: backend-builder + backend-tester</b>"]
        end

        subgraph "Client Track"
            PR5["PR 5: apps/storefront/.../services/<br/>Axios client with ETag, WatermelonDB models & pull/push sync, TanStack Query v5<br/><b>Agent: client-builder + client-tester</b>"]
            --> PR6["PR 6: apps/storefront/.../logic/<br/>Headless custom hooks, domain state machines, form validation<br/><b>Agent: client-builder + client-tester</b>"]
            --> PR7["PR 7: apps/storefront/.../designs/<br/>@expo/ui mobile screens, Tailwind web components, SDUI AST renderers, RTL<br/><b>Agent: client-builder + client-tester</b>"]
        end
    end

    PR1 --> PR2
    PR2 --> PR3
    PR2 --> PR5

    PR4 --> INTEGRATE["Integrated Acceptance & Release (Gate G4)<br/><b>Agent: qa-security-auditor (gatekeeper)</b>"]
    PR7 --> INTEGRATE
```

### 3.1 Non-Conflicting Parallelism Rules

1. **Independent Workdirs**: Each agent runs in its own isolated sprint workdir:
   `.agents/workspaces/<sprint-id>/<agent-name>/`
   backed by an isolated Git branch (`agent/<sprint-id>/<agent-name>`).
2. **File Whitelisting & Non-Overlapping Targets**:
   - `backend-builder` edits `crates/` and `backend/src/features/...`
   - `backend-tester` edits `backend/tests/` and test modules
   - `client-builder` edits `apps/storefront/src/features/.../[services, logic, designs]`
   - `client-tester` edits `apps/storefront/__tests__/`
   - `qa-security-auditor` reviews code, executes scans, and signs off gates.
3. **Contract-First Concurrency**: Once PR 2 merges schema definitions and runs `ts-rs` codegen, the **Backend Track (PR 3 & 4)** and **Client Track (PR 5, 6 & 7)** execute completely in parallel without blocking each other.

---

## 4. Sprint-Level Agent Workdir Architecture

Each agent generated at the sprint level receives a fully populated, self-contained workspace:

```
.agents/workspaces/<sprint-id>/<agent-name>/
├── agent.yaml           # Agent metadata, profile, role, and path whitelists/blacklists
├── context.md           # Tailored story specifications, PR requirements, schemas & laws
├── tasks.md             # Granular, ordered execution checklist for this specific PR
└── workspace/           # (Optional) Dedicated Git worktree checkout on branch agent/<sprint>/<name>
```

### 4.1 `agent.yaml` Specification
```yaml
name: s11-us111-be-builder
profile: backend-engineer
role: builder
sprint: sprint-1.1
story: us-1.1.1
pr: 1
workdir: .agents/workspaces/sprint-1.1/s11-us111-be-builder
allowed_paths:
  - crates/kernel-core/**
  - crates/some-auth/**
forbidden_paths:
  - apps/storefront/**
  - backend/bins/lambda-serverless/**
rules:
  - zero_clone_borrowing_enforced: true
  - microkernel_purity_enforced: true
  - axum_lambda_decoupling_enforced: true
```

### 4.2 `context.md` Specification
Contains the exact subset of information required by that agent:
- Target User Story narrative and Gherkin Acceptance Criteria `[AC-US-X.Y.Z-NN]`
- Detailed PR deliverables for their assigned layer
- Colocated behaviour directory tree
- Security Gateway invariants (Trust boundaries, STRIDE threats, KMS keys)
- Concrete verification commands (`cargo test`, `proptest`, `validate_microkernel.py`)

---

## 5. Tooling: Automated Agent Generation Scripts

### 5.1 Single Agent Generator (`scripts/generate_agent.py`)
Generates an individual agent with customized profile, role, story, PR, and isolated workdir:

```bash
python3 scripts/generate_agent.py \
  --name s11-us111-be-builder \
  --profile backend-engineer \
  --role builder \
  --sprint sprint-1.1 \
  --story us-1.1.1 \
  --pr 1 \
  --create-git-worktree
```

### 5.2 Sprint Batch Generator (`scripts/generate_sprint_agents.py`)
Generates all agent instances, workdirs, and contexts required to deliver an entire sprint:

```bash
python3 scripts/generate_sprint_agents.py --sprint sprint-1.1
```
