# Audit Domain 02: Architecture & Zero-Clone Conformance

> **Scope**: Pure Microkernel Trait Abstraction · Rust Zero-Clone Law · Axum Decoupling · Locality of Behavior (LoB)  
> **Governing Quality Gate**: **Gate G3** (Story Level) & **SG3** / **Gate M1** / **Gate A1** / **Gate A2** (Sprint Level)  
> **Accountable Role**: `system-architect` / `senior-backend-engineer` / `senior-client-engineer`

---

## 1. Domain Overview

The Architecture & Zero-Clone Conformance audit domain guarantees that the monorepo adheres strictly to the architectural standards defined in [`docs/MICROKERNEL_AND_CLOUD_PORTABILITY.md`](../../MICROKERNEL_AND_CLOUD_PORTABILITY.md) and [`docs/FOLDER_ARCHITECTURE.md`](../../FOLDER_ARCHITECTURE.md).

### Core Architectural Laws:
1. **The Rust Zero-Clone Law (Gate M1)**: Zero `.clone()` calls on hot paths (e.g. SDUI tree rendering, cache key resolution, ETag computation, financial ledger calculations). Data must be passed by immutable/mutable reference (`&T`, `&mut T`), borrowed slices (`&str`, `&[u8]`), or moved by value.
2. **Microkernel Trait Purity (Gate M1)**: Domain logic in `crates/` must be pure Rust, independent of cloud SDKs or proprietary runtimes. Transport adapters (`axum::Router`) must never depend directly on `lambda_http`.
3. **Locality of Behavior & Framework Scoping (Gate A2)**: The 4-tier folder hierarchy (`features -> modules -> behaviours -> [services, designs, logic, types, constants]`) must be strictly framework-scoped inside `apps/storefront/src/features/` and `backend/src/features/`. `features/` must NEVER exist at the repo root.
4. **No Sibling Imports (Gate A2)**: Behaviours within a module must never import sibling behaviours directly. Any shared component must be promoted to the `_shared/` directory.

---

## 2. Automated Architecture Verification Commands

Auditors must run the automated validators before issuing architectural certification:

```bash
# 1. Verify Microkernel Logic Abstraction & Axum Decoupling (Gate M1)
python3 scripts/validation/validate_microkernel.py

# 2. Verify System Architecture Contracts & Layer Decoupling (Gate A1)
python3 scripts/validation/validate_system_architecture.py

# 3. Verify Folder Architecture & Locality of Behavior Conformance (Gate A2)
python3 scripts/validation/validate_folder_architecture.py

# 4. Zero-Clone Borrowing Linter
cargo clippy --workspace --all-targets -- -D clippy::redundant_clone -D clippy::clone_on_ref_ptr
```

---

## 3. Sprint Architecture Audit Catalog

| Audit File | Sprint | Focus | Status |
|:-----------|:-------|:------|:-------|
| `AUDIT-ARCH-sprint-1.1-m1-zero-clone-cache.md` | Sprint 1.1 | L1 Moka / L2 Redis cache tier trait purity, zero-clone BLAKE3 ETag generator | Pending |
| `AUDIT-ARCH-sprint-1.2-axum-decoupling-fees.md` | Sprint 1.2 | Axum checkout handlers decoupling from Lambda runtime, zero-clone fee engine | Pending |
| `AUDIT-ARCH-sprint-2.1-crypto-vault-traits.md` | Sprint 2.1 | Pure licensing authority traits, zero-clone Bloom filter lookups | Pending |
| `AUDIT-ARCH-sprint-2.2-sdk-shared-traits.md` | Sprint 2.2 | Cross-SDK golden vector abstractions, headless custom hook LoB adherence | Pending |
| `AUDIT-ARCH-sprint-3.1-b2b-tier-pricing.md` | Sprint 3.1 | Microkernel pricing trait ports, zero-clone MOQ matrix arithmetic | Pending |
| `AUDIT-ARCH-sprint-3.2-state-machine-lob.md` | Sprint 3.2 | Durable orchestrator state machine decoupling, LAN seat proxy architecture | Pending |
| `AUDIT-ARCH-sprint-4.1-cart-split-models.md` | Sprint 4.1 | Sub-order split domain model purity, zero-clone cart mutation allocations | Pending |
| `AUDIT-ARCH-sprint-4.2-double-entry-ledger.md` | Sprint 4.2 | Balanced ledger transaction isolation, zero-clone crypto payment decoders | Pending |
| `AUDIT-ARCH-sprint-5.1-cdk-cloud-portability.md` | Sprint 5.1 | Infrastructure-as-code portability, CDK stack modularity, clean cloud borders | Pending |
| `AUDIT-ARCH-sprint-6.1-sdui-ast-purity.md` | Sprint 6.1 | Universal SDUI JSON schema definitions, zero-clone layout AST traversal | Pending |
| `AUDIT-ARCH-sprint-6.2-whitelabel-pipeline.md` | Sprint 6.2 | White-label client architecture, Expo dynamic configuration, headless styling | Pending |
| `AUDIT-ARCH-sprint-6.3-final-arch-review.md` | Sprint 6.3 | Comprehensive repository-wide Gate M1, Gate A1, Gate A2, and Zero-Clone re-certification | Pending |

---

## 4. How to Conduct and Record an Audit

1. Copy `../AUDIT_RECORD_TEMPLATE.md` to `docs/audits/02-architecture-and-zero-clone/AUDIT-ARCH-<sprint>-<topic>.md`
2. Run validation scripts and clippy audits. Inspect codebase for any `.clone()` on request paths.
3. Verify that all pure traits in `crates/` compile without cloud SDK imports.
4. Record findings and sign off under `system-architect` authority.
