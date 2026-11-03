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

## 2. Master Folder Architecture & Colocation Laws

The entire codebase is structured on the **Locality of Behavior (LoB)** and **Vertical Slice Architecture** principles.

### 2.1 The 4-Tier Hierarchical Model

```
features/
└── <feature-name>/                      # Domain Feature Slice
    ├── _shared/                         # Shared across modules in this feature
    │   ├── services/
    │   ├── designs/
    │   ├── logic/
    │   ├── types/
    │   └── constants/
    └── modules/
        └── <module-name>/               # Functional Module
            ├── _shared/                 # Shared across behaviours in this module
            │   ├── services/
            │   ├── designs/
            │   ├── logic/
            │   ├── types/
            │   └── constants/
            └── behaviours/
                └── <behaviour-name>/    # Concrete Autonomous Behaviour
                    ├── services/        # API clients, queries, mutations, network handlers
                    ├── designs/         # UI components, SDUI widgets, screens, styles
                    ├── logic/           # Domain state machines, custom hooks, validation
                    ├── types/           # Interfaces, DTOs, schemas, models
                    └── constants/       # Config keys, routes, error codes, limits
```

### 2.2 Project-Wide Shared Tier (`shared/`)

Items that cut across multiple distinct features are placed in the global root `shared/` directory:
- `shared/services/`: Global transport clients, DynamoDB client wrapper, KMS crypto client, Redis L2 cache connection multiplexer, EventBridge dispatcher.
- `shared/designs/`: Core design tokens, global theme provider, typography primitives, toast/dialog containers.
- `shared/logic/`: Currency/Money arithmetic (`crates/kernel-core`), RFC 9110 ETag generator, i18n locale resolver, rate-limiter primitives.
- `shared/types/`: Universal domain primitives (`TenantId`, `Money`, `CognitoSub`, `Result<T, E>`), standard HTTP/SDUI envelope schemas.
- `shared/constants/`: Universal HTTP headers (`ETag`, `If-None-Match`), system error codes, supported locales list.

### 2.3 Strict Colocation & Promotion Rules

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
