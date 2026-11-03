# Canonical Audit Record: AUDIT-[DOMAIN]-[SPRINT]-[TOPIC]

> **Status: Template Only — Pending Formal Execution**  
> Formulate from this template when an audit enters scope at SG0/G0. See [Audit Master Index](./README.md) and [QUALITY_GATES.md](../QUALITY_GATES.md).

---

## 1. Audit Identity & Review Context

| Metadata Field | Value |
|:---------------|:------|
| **Audit Identifier** | `AUDIT-<DOMAIN>-<SPRINT>-<TOPIC>` |
| **Audit Domain** | `[01-Security | 02-Architecture | 03-Compliance | 04-Quality]` |
| **Target Sprint / Slice** | `Sprint X.Y (vZ.0)` |
| **Associated User Stories** | `[US-X.Y.Z, ...]` |
| **Candidate Tree / Commit SHA** | `Pending (git rev-parse HEAD)` |
| **Deployable Artifact Digests** | `Pending (sha256:...)` |
| **Lead Auditor (Independent)** | `senior-security-qa-auditor` / `system-architect` |
| **Contributing Authors (Disjoint)** | `[Junior Author 1, Junior Author 2]` |
| **Governing Quality Gates** | `[Gate G2, SG2, Gate M1, Gate A1, Gate A2, SG3]` |
| **Audit Execution Date** | `YYYY-MM-DD` |
| **Final Audit Disposition** | **`[PENDING | PASSED | FAILED | BLOCKED]`** |

---

## 2. Executive Summary & Gate Recommendation

*Provide a concise 2–3 paragraph summary of the audit scope, evaluated candidate, key threat vectors examined, and the conclusive gate recommendation for SG2/SG3/SG4.*

---

## 3. Scope & Target Attack Surfaces

### 3.1 Target Crates, Packages & Endpoints
| Component / Target | File Paths / Crates | Nature of Surface | Applicable Threat Model |
|:-------------------|:--------------------|:------------------|:------------------------|
| *Example: Auth Middleware* | `crates/auth-cognito/src/*` | HTTP Request Header / JWT verification | Spoofing, Replay, Privilege Escalation |

### 3.2 Excluded Surfaces & Scope Justification
*Document any components intentionally excluded from this audit pass with architectural and risk rationale.*

---

## 4. Audit Methodology & Toolchain Log

| Tool / Method | Version / Command | Scope / Flags | Exit Code / Result | Artifact Digest |
|:--------------|:------------------|:--------------|:-------------------|:----------------|
| `cargo-audit` | `cargo audit --deny warnings` | Rust dependencies | `0` (0 CVEs) | `sha256:...` |
| `cargo-clippy` | `cargo clippy -- -D warnings` | Zero-clone & lints | `0` (Clean) | `sha256:...` |
| `semgrep` | `semgrep scan --config p/owasp-top-ten` | Backend & Client | `0` (No issues) | `sha256:...` |
| Synthetic Fuzzer | `cargo fuzz run <target> -- -max_total_time=600` | Parsers & Decoders | `0` (0 crashes) | `sha256:...` |

---

## 5. Invariant Checklist & Behavioral Assertions

- [ ] **Tenant Isolation (SG2 / G2)**: 100% of queries strictly partition by `tenant_id`; zero cross-tenant query leaks under adversarial parameter tampering.
- [ ] **Cryptographic Hygiene**: No hardcoded keys; AES-256-GCM / Ed25519 routines use valid nonces/IVs; KMS envelope encryption strictly applies.
- [ ] **Rust Zero-Clone Law (SG3 / Gate M1)**: Zero unnecessary `.clone()` calls on hot paths; pass by reference `&T` or move semantics verified.
- [ ] **Axum Decoupling (SG3 / Gate M1)**: Axum handlers decouple from `lambda_http`; testable with pure standard HTTP types (`axum::http::Request`).
- [ ] **Locality of Behavior (Gate A2)**: 4-tier folder hierarchy strictly maintained; no sibling behavior cross-imports.
- [ ] **Input Sanitization & Schema Validation**: Untrusted client inputs strictly bounded and validated via Zod / Serde before evaluation.

---

## 6. Audit Findings & Severity Log

| Finding ID | Severity | Category | Description & Impact | Exact Location | Proof of Concept / Reproducer | Remediation PR | Status |
|:-----------|:---------|:---------|:---------------------|:---------------|:------------------------------|:---------------|:-------|
| *SEC-01* | *Critical* | *Auth Bypass* | *Example: JWT kid unvalidated* | `crates/auth/src/jwt.rs:42` | `curl -H 'kid: ../hack' ...` | *PR #123* | *RESOLVED* |

> **Severities**:
> - **Critical**: Immediate compromise of tenant boundary, cryptographic key, remote code execution, or money movement. Blocks gate immediately.
> - **High**: Significant security weakness or architectural rule violation (e.g. clone in hot path, unvalidated input). Blocks gate.
> - **Medium**: Compensating controls present; requires tracked repair ticket and expiration date.
> - **Low / Informational**: Best practice enhancement or documentation clarification.

---

## 7. Compensating Controls & Risk Waivers

| Finding ID | Risk Rationale | Compensating Control | Accountable Owner | Expiration Date |
|:-----------|:---------------|:---------------------|:------------------|:----------------|
| N/A | None | All Critical/High findings must be resolved prior to gate passage. | N/A | N/A |

---

## 8. Independent Reviewer Sign-Off & Approvals

| Review Role | Reviewer Identity | Signature / Attestation | Date | Gate Recommendation |
|:------------|:------------------|:------------------------|:-----|:--------------------|
| **Independent Senior Auditor** | `senior-security-qa-auditor` | Attested clean under ASVS L2 / Zero-Clone audit | YYYY-MM-DD | `[APPROVED | REJECTED]` |
| **System Architect** | `system-architect` | Architectural compliance (Gate M1, A1, A2) | YYYY-MM-DD | `[APPROVED | REJECTED]` |
| **Release Gatekeeper** | `release-gatekeeper` | Verified complete evidence & candidate binding | YYYY-MM-DD | `[ACCEPTED | BLOCKED]` |
| **CTO Review** | `chief-technology-officer` | Executive risk acceptance & release recommendation | YYYY-MM-DD | `[RECOMMENDED | PENDING]` |
