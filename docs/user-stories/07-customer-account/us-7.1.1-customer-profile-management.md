# US-7.1.1: Customer Profile Management

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `identity-and-access`  
> **Domain Module**: `customer-account`  
> **Autonomous Behaviour**: `customer-profile-management`  
> **Client Framework Path**: `apps/storefront/src/features/identity-and-access/modules/customer-account/behaviours/customer-profile-management`  
> **Backend Framework Path**: `backend/src/features/identity-and-access/modules/customer-account/behaviours/customer-profile-management`  
> **Execution Sprint**: [Sprint 1.1](../../sprints/README.md)  
> **Slicing Standard**: [7-PR Vertical Slicing Framework](../../sprints/README.md#the-7-pr-vertical-slicing-standard)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** registered Customer,  
**I want to** view and edit my profile including name, email, phone, preferred locale, and connected sign-in methods,  
**So that** my account details are accurate and I can manage security settings.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Profile Management
  Scenario: [AC-US-7.1.1-01] View profile
    Given the customer navigates to "/[locale]/account/profile"
    Then the profile page shows: full name, email, phone, preferred locale, connected passkeys, role badge
  Scenario: [AC-US-7.1.1-02] Update preferred locale
    When the customer changes locale from en-US to ar-EG
    Then the Cognito custom:pref_locale attribute is updated
    And the WatermelonDB user record syncs
    And the UI immediately flips to RTL with Cairo font
  Scenario: [AC-US-7.1.1-03] Update phone number
    When the customer changes their phone number
    Then a verification OTP is sent to the new number
    And the phone is only updated after OTP verification
  Scenario: [AC-US-7.1.1-04] View connected sessions
    Then the profile shows active sessions (device, last active time)
    And the customer can revoke any session
```

### 1.3 Test Cases & Traceability Matrix

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-7.1.1-01 | View profile details | Happy Path | All fields displayed |
| TC-7.1.1-02 | Update name | Happy Path | Name saved, synced |
| TC-7.1.1-03 | Change locale en→ar | Happy Path | RTL switch, Cognito updated |
| TC-7.1.1-04 | Change phone with OTP | Happy Path | Verified and updated |
| TC-7.1.1-05 | Change phone — OTP fails | Negative | Phone not changed |
| TC-7.1.1-06 | Empty name | Validation | Error shown |
| TC-7.1.1-07 | XSS in name field | Security | Input sanitized |
| TC-7.1.1-08 | Revoke session | Happy Path | Session terminated |
| TC-7.1.1-09 | Concurrent profile edits | Concurrency | ETag If-Match → 412 |
| TC-7.1.1-10 | Unauthenticated access | Security | Redirect to sign-in |

---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/identity-and-access/modules/customer-account/behaviours/customer-profile-management/
├── services/
│   │   ├── profile_repository.rs
│   │   ├── avatar_upload_service.rs
│   │   ├── profile_api.ts
├── designs/
│   │   ├── ProfileEditScreen.tsx
│   │   ├── AvatarPicker.tsx
│   │   ├── AccountSecuritySection.tsx
├── logic/
│   │   ├── useCustomerProfile.ts
│   │   ├── email_change_verifier.rs
│   │   ├── phone_normalization.ts
├── types/
│   │   ├── CustomerProfile.ts
│   │   ├── ProfileUpdatePayload.ts
│   │   ├── AvatarUploadTicket.ts
└── constants/
│   │   ├── ProfileEndpoints.ts
│   │   ├── MaxAvatarSizeBytes.ts
│   │   ├── ProfileErrorCodes.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/identity-and-access/modules/customer-account/behaviours/customer-profile-management/
├── services/
│   │   ├── profile_repository.rs
│   │   ├── avatar_upload_service.rs
│   │   ├── profile_api.ts
├── logic/
│   │   ├── useCustomerProfile.ts
│   │   ├── email_change_verifier.rs
│   │   ├── phone_normalization.ts
├── types/
│   │   ├── CustomerProfile.ts
│   │   ├── ProfileUpdatePayload.ts
│   │   ├── AvatarUploadTicket.ts
└── constants/
│   │   ├── ProfileEndpoints.ts
│   │   ├── MaxAvatarSizeBytes.ts
│   │   ├── ProfileErrorCodes.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/customer-profile-management/` | `.../behaviours/customer-profile-management/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
| **Module-Shared** | `.../modules/customer-account/_shared/` | `.../modules/customer-account/_shared/` | Shared domain primitives and UI elements used by $\ge 2$ behaviours in `customer-account`. |
| **Feature-Shared** | `.../features/identity-and-access/_shared/` | `.../features/identity-and-access/_shared/` | Feature-level contracts, ports, and cross-module bridges across `identity-and-access`. |
| **Framework-Shared** | `apps/storefront/src/shared/` | `backend/crates/kernel-core/` | System-wide microkernel traits, `Money` arithmetic, RFC 9110 ETag middleware, and database adapters. |

---

## 3. Technical Implementation Plan (Spec Kit Plan)

### 3.1 Domain Invariants & Storage Schema
- **State Machine**: Enforces valid state transitions and rejects unauthorized or out-of-order mutations.
- **Data Persistence**: Single-table Amazon DynamoDB partitioning (`PK = TENANT#<id>`, `SK = ENTITY#<id>`) paired with reactive local-first WatermelonDB sync.
- **Freshness & Caching**: Multi-tier caching (L1 Moka in-memory + L2 ElastiCache Redis) with RFC 9110 `ETag` conditional `304 Not Modified` short-circuiting.

### 3.2 Activity & Interaction Diagram

```mermaid
flowchart TD
    A([Customer opens profile]) --> B[GET /v1/account/profile]
    B --> C[Render profile form with current data]
    C --> D{User edits field?}
    D -->|Name/Email| E[PUT /v1/account/profile with If-Match ETag]
    E --> F{ETag match?}
    F -->|No| G[412 Precondition Failed — reload]
    F -->|Yes| H[Update DynamoDB USER#]
    H --> I[Sync WatermelonDB]
    D -->|Phone| J[Send OTP to new phone]
    J --> K{OTP verified?}
    K -->|Yes| L[Update phone in Cognito + DDB]
    K -->|No| M[Show error, phone unchanged]
    D -->|Locale| N[Update Cognito pref_locale]
    N --> O[Switch UI direction RTL/LTR]
    I --> P([Profile updated])
    L --> P
    O --> P
```

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
| **Denial of Service / Abuse** | High | Malicious SVG avatar upload (XSS), unverified email/phone change account takeover, IDOR on profile | Token-bucket rate limiting per IP and account; strict input length validation. |
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

**Status: Pending — specification only; no implementation evidence.** All [G0–G4 quality gates](../../QUALITY_GATES.md) apply to this story. The following checks add to its acceptance criteria and test cases; they do not replace them.

### G1 — Test coverage
- [ ] **US-7.1.1-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-7.1.1-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against Malicious SVG avatar upload (XSS), unverified email/phone change account takeover, IDOR on profile. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-7.1.1-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G4 — Integrated acceptance
- [ ] **US-7.1.1-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module customer-account Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
