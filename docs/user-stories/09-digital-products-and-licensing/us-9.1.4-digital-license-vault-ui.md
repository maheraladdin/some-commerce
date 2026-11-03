# US-9.1.4: Digital License Vault UI

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `commercial-models`  
> **Domain Module**: `digital-products-and-licensing`  
> **Autonomous Behaviour**: `license-vault-ui`  
> **Client Framework Path**: `apps/storefront/src/features/commercial-models/modules/digital-products-and-licensing/behaviours/license-vault-ui`  
> **Backend Framework Path**: `backend/src/features/commercial-models/modules/digital-products-and-licensing/behaviours/license-vault-ui`  
> **Execution Sprint**: [Sprint 2.2](../../sprints/README.md)  
> **Slicing Standard**: [10-PR Vertical Slicing Framework](../../sprints/README.md#the-10-pr-vertical-slicing-standard-aligned-with-10-pillar-system-architecture)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** Buyer of digital products,  
**I want** a dedicated license vault page showing all my purchased licenses, download buttons, and activation tools,  
**So that** I can manage all my digital purchases in one place.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Digital License Vault
  Scenario: [AC-US-9.1.4-01] View purchased licenses
    Given the buyer navigates to "/[locale]/account/licenses"
    Then all purchased digital entitlements are listed
    And each card shows: product name, license status, verification mode, expiry
  Scenario: [AC-US-9.1.4-02] Download .lic certificate
    When the buyer clicks "Download Certificate"
    Then the Ed25519 .lic file downloads from WatermelonDB/Secure Enclave
  Scenario: [AC-US-9.1.4-03] Air-gapped QR scanner
    When the buyer clicks "Activate Offline Device"
    Then the native camera QR scanner opens (expo-crypto-license)
    And scans the ChallengeQR from the offline workstation
  Scenario: [AC-US-9.1.4-LAW] Global e-commerce legal compliance and digital certificate vault regulations
    Given a customer accessing their digital license vault to view keys and download activation credentials
    When retrieving purchased license keys or certificates
    Then the customer must be provided with durable, permanent access to license credentials and activation keys on durable media (PDF)
    And purchased perpetual licenses must remain downloadable and viewable regardless of subsequent catalog deprecations
    And license transfer and assignment terms must be clearly disclosed within the digital vault interface
```

### 1.3 Test Cases & Traceability Matrix


| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-9.1.4-01 | Primary user journey functional flow | Happy Path | User story outcome achieved |
| TC-9.1.4-02 | Edge case and boundary condition validation | Edge Case | Handled with typed error |
| TC-9.1.4-03 | Threat model and authorization boundary validation | Security | Unauthorized requests rejected |
| TC-9.1.4-LAW | Global legal & regulatory compliance (EU Consumer Rights Directive Art 8 durable medium, perpetual software purchase preservation) | Legal / Regulatory | Statutory compliance verified with zero legal or regulatory violations |
---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/commercial-models/modules/digital-products-and-licensing/behaviours/license-vault-ui/
├── services/
│   │   ├── license_vault_client.rs
│   │   ├── activation_counter_service.rs
│   │   ├── vault_api.ts
├── designs/
│   │   ├── LicenseVaultScreen.tsx
│   │   ├── LicenseKeyCopyButton.tsx
│   │   ├── SeatAllocationMeter.tsx
├── logic/
│   │   ├── useLicenseVault.ts
│   │   ├── seat_activation_manager.ts
│   │   ├── license_expiry_formatter.ts
├── types/
│   │   ├── UserLicenseSeat.ts
│   │   ├── ActivationRecord.ts
│   │   ├── DeactivationRequest.ts
└── constants/
│   │   ├── VaultEndpoints.ts
│   │   ├── MaxSeatTransfers.ts
│   │   ├── VaultErrorCodes.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/commercial-models/modules/digital-products-and-licensing/behaviours/license-vault-ui/
├── services/
│   │   ├── license_vault_client.rs
│   │   ├── activation_counter_service.rs
│   │   ├── vault_api.ts
├── logic/
│   │   ├── useLicenseVault.ts
│   │   ├── seat_activation_manager.ts
│   │   ├── license_expiry_formatter.ts
├── types/
│   │   ├── UserLicenseSeat.ts
│   │   ├── ActivationRecord.ts
│   │   ├── DeactivationRequest.ts
└── constants/
│   │   ├── VaultEndpoints.ts
│   │   ├── MaxSeatTransfers.ts
│   │   ├── VaultErrorCodes.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/license-vault-ui/` | `.../behaviours/license-vault-ui/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
| **Module-Shared** | `.../modules/digital-products-and-licensing/_shared/` | `.../modules/digital-products-and-licensing/_shared/` | Shared domain primitives and UI elements used by $\ge 2$ behaviours in `digital-products-and-licensing`. |
| **Feature-Shared** | `.../features/commercial-models/_shared/` | `.../features/commercial-models/_shared/` | Feature-level contracts, ports, and cross-module bridges across `commercial-models`. |
| **Framework-Shared** | `apps/storefront/src/shared/` | `backend/crates/kernel-core/` | System-wide microkernel traits, `Money` arithmetic, RFC 9110 ETag middleware, and database adapters. |

---

## 3. Technical Implementation Plan (Spec Kit Plan)

### 3.1 Domain Invariants & Storage Schema
- **State Machine**: Enforces valid state transitions and rejects unauthorized or out-of-order mutations.
- **Data Persistence**: Single-table Amazon DynamoDB partitioning (`PK = TENANT#<id>`, `SK = ENTITY#<id>`) paired with reactive local-first WatermelonDB sync.
- **Freshness & Caching**: Multi-tier caching (L1 Moka in-memory + L2 ElastiCache Redis) with RFC 9110 `ETag` conditional `304 Not Modified` short-circuiting.

### 3.2 Activity & Interaction Diagram



---

## 4. Granular Implementation Tasks (Spec Kit Tasks)

### Phase 1: Core Domain Logic, Types & Constants
- [ ] **Task 1.1 (Types)**: Define strongly typed models and DTO schemas in `types/`.
- [ ] **Task 1.2 (Constants)**: Define routes, action codes, and validation limits in `constants/`.
- [ ] **Task 1.3 (Logic)**: Implement pure business logic, calculations, and state machines in `logic/`.
- [ ] **Task 1.4 (Unit Tests)**: Write pure property-based and unit tests verifying domain invariants.

### Phase 2: Services & Infrastructure Adapters
- [ ] **Task 2.1 (API / Gateway)**: Implement client adapters and backend handlers in `services/`.
- [ ] **Task 2.2 (ETag & Cache)**: Integrate RFC 9110 ETag headers and multi-tier caching (Moka L1 / Redis L2).
- [ ] **Task 2.3 (Storage & Sync)**: Implement DynamoDB storage operations and WatermelonDB delta sync.
- [ ] **Task 2.4 (Integration Tests)**: Verify service contract tests and real database conditional writes.

### Phase 3: Platform-Adaptive Designs & UI
- [ ] **Task 3.1 (UI Presentation)**: Build platform-adaptive screens and SDUI components in `designs/`.
- [ ] **Task 3.2 (Headless Hooks)**: Bind headless domain hooks from `logic/` into the UI presentation.
- [ ] **Task 3.3 (i18n & RTL)**: Implement bidirectional RTL/LTR layout mirroring and localized font switching.
- [ ] **Task 3.4 (Component Tests)**: Test empty, loading, offline, and error states across web and mobile.

### Phase 4: Security Gateway Verification & Release Readiness
- [ ] **Task 4.1 (Abuse Testing)**: Execute automated adversarial penetration tests against the threat matrix.
- [ ] **Task 4.2 (Zero-Trust Audit)**: Verify strict tenant isolation and object-level authorization (IDOR).
- [ ] **Task 4.3 (SAST & Audit)**: Run static analysis, dependency audit, and secret scanning.
- [ ] **Task 4.4 (Gate Sign-Off)**: Obtain independent security sign-off for the G2 Security Gateway.

---

## 5. Security Gateway (Powered by security-audit)

### 5.1 Trust Boundaries & Security Actors
- **Trust Boundaries**:
  - `Untrusted Zone`: Mobile client app, public web browser, and external network callers.
  - `Gateway Edge`: AWS CloudFront, API Gateway, and Cognito JWT authentication guard.
  - `Secure Application Boundary`: Axum Tower route extractors enforcing tenant and RBAC/ABAC isolation.
  - `Encrypted Storage & Secret Vault`: Amazon DynamoDB KMS-encrypted tables and AWS KMS vault.
- **Authorized Principals**:
  - Identified Actors: `AuthenticatedCustomer`, `B2bBuyer`, `Vendor`, `StoreAdmin`, or `AnonymousShopper` (read-only).
  - Multi-Tenancy Invariant: Every request must extract `tenant_id` from verified JWT claims. Injections via query params or payload body are rejected with `403 Forbidden`.

### 5.2 Threat Modeling & Abuse Matrix (STRIDE / ASVS)

| Threat Vector | Severity | Vulnerability Mechanism | Mitigating Control & Security Invariant |
| :--- | :--- | :--- | :--- |
| **Spoofing & Impersonation** | Critical | Forged `sub` or `tenant_id` identity claims | Server-side RS256 JWKS signature verification; strict claims extraction in Axum. |
| **Tampering & Invariant Bypass** | High | Manipulating payload parameters or prices | Authoritative server recalculation; strict schema validation; BLAKE3 ETag integrity checks. |
| **Information Disclosure (IDOR)** | Critical | Cross-tenant or cross-user data scraping | Explicit `PK = TENANT#<id>` partition filtering on every database and cache operation. |
| **Denial of Service / Abuse** | High | IDOR allowing unauthorized seat revocation, license key leakage in frontend DOM rendering | Token-bucket rate limiting per IP and account; strict input length validation. |
| **Elevation of Privilege** | Critical | Bypassing role-based permission checks | Tower extractors (`RequireStoreAdmin`, `RequireVendor`) guard sensitive endpoints. |

### 5.3 Cryptographic & Data Protection Controls
- **Encryption in Transit**: TLS 1.3 enforced on all external and internal endpoints; HSTS active.
- **Encryption at Rest**: DynamoDB AWS KMS customer-managed keys; AES-256-GCM for sensitive client tokens in `expo-secure-store`.
- **PII & Secret Redaction**: Passwords, OTPs, auth tokens, and credit card numbers are stripped from logs and traces via `tracing` redaction filters.

### 5.4 Automated Security Verification Checklist
- [ ] **SAST Analysis**: Clean report from static code analyzers; 0 high or critical vulnerabilities.
- [ ] **Dependency Audit**: `cargo deny` and `bun audit` pass with 0 unreviewed security advisories.
- [ ] **Abuse & IDOR Fuzzing**: Test suite confirms that requests with modified `tenant_id` or `user_id` fail with `401 Unauthorized` or `403 Forbidden`.
- [ ] **Secret Scanning**: Gitleaks scanner confirms zero hardcoded credentials, API keys, or private keys.

### 5.5 Security Gateway (G2) Sign-Off Checklist
- [ ] Threat boundary and entry points verified against OWASP ASVS Level 2 requirements.
- [ ] Multi-tenant isolation verified with automated cross-tenant penetration test.
- [ ] Anti-abuse and rate limiting confirmed active on all public interfaces.
- [ ] Audit log redaction verified — zero plaintext secrets in output logs.
- [ ] Independent reviewer sign-off obtained; zero open Critical or High findings.

---

## 6. Validation Gates & Acceptance Sign-Off

**Status: Pending — specification only; no implementation evidence.** All [G0–G4 quality gates + G-Review + G-Law](../../QUALITY_GATES.md) apply to this story. The following checks add to its acceptance criteria and test cases; they do not replace them.

### G1 — Test coverage
- [ ] **US-9.1.4-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-9.1.4-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against IDOR allowing unauthorized seat revocation, license key leakage in frontend DOM rendering. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-9.1.4-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G-Review — Code review
- [ ] **US-9.1.4-G-Review:** Independent senior code review signed off by the Code Reviewer; verification across Correctness, Security, Maintainability, Performance, and Testing using the Agency-Agents code review standard; zero open Blocker or unresolved Suggestion findings.

### G-Law — Law validation
- [ ] **US-9.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU durable medium proof of purchase, permanent consumer access to perpetual digital licenses, and transparent assignment terms; certified by compliance reviewer (`agency-legal-compliance-checker`).

### G4 — Integrated acceptance
- [ ] **US-9.1.4-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module digital-products-and-licensing Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
