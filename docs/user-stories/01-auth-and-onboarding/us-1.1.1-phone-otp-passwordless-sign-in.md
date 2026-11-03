# US-1.1.1: Phone OTP Passwordless Sign-In

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `identity-and-access`  
> **Domain Module**: `auth-and-onboarding`  
> **Autonomous Behaviour**: `phone-otp-sign-in`  
> **Client Framework Path**: `apps/storefront/src/features/identity-and-access/modules/auth-and-onboarding/behaviours/phone-otp-sign-in`  
> **Backend Framework Path**: `backend/src/features/identity-and-access/modules/auth-and-onboarding/behaviours/phone-otp-sign-in`  
> **Execution Sprint**: [Sprint 1.1](../../sprints/README.md)  
> **Slicing Standard**: [7-PR Vertical Slicing Framework](../../sprints/README.md#the-7-pr-vertical-slicing-standard)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** B2C Customer in Egypt/MENA,  
**I want to** sign in using my phone number via a 6-digit SMS OTP sent through Amazon SNS in my preferred language (Arabic or English),  
**So that** I can access the storefront without remembering a password and receive OTP messages I can understand.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Phone OTP Passwordless Sign-In
  Scenario: [AC-US-1.1.1-01] Successful OTP sign-in with Egyptian phone number
    Given the user is on "/ar-EG/(auth)/sign-in"
    And the user selects the "Phone OTP" tab
    When the user enters phone number "+201012345678"
    And clicks "Send OTP"
    Then the system initiates a Cognito PKCE auth flow
    And Amazon SNS sends a 6-digit OTP via SMS in Arabic
    And the OTP input field is displayed with a 120-second countdown timer
    When the user enters the correct 6-digit OTP
    Then the system verifies the OTP via Cognito RespondToAuthChallenge
    And receives an enriched JWT with custom claims (tenant_id, persona, pref_locale)
    And the user is redirected to the storefront home "/ar-EG/"
    And the UI renders in RTL direction
  Scenario: [AC-US-1.1.1-02] OTP expiration
    Given the user requested an OTP for "+201012345678"
    When the 120-second timer expires before entering the OTP
    Then the OTP input is disabled
    And a "Resend OTP" button becomes active
    And a localized message "OTP expired. Please resend." is shown
  Scenario: [AC-US-1.1.1-03] Invalid OTP entry (3 failed attempts)
    Given the user has entered an incorrect OTP 3 times
    Then the account is temporarily locked for 5 minutes
    And a localized error "Too many attempts. Try again in 5 minutes." is shown
    And the lock state is tracked in Cognito
  Scenario: [AC-US-1.1.1-04] Unsupported country code
    Given the user enters a phone number with an unsupported country code
    When the user clicks "Send OTP"
    Then a validation error "This country code is not supported" is displayed
    And no Cognito auth flow is initiated
  Scenario: [AC-US-1.1.1-05] Network failure during OTP verification
    Given the user enters a valid 6-digit OTP
    When the network is unavailable during verification
    Then the system shows "Network error. Please check your connection and try again."
    And the OTP input remains editable for retry
```

### 1.3 Test Cases & Traceability Matrix

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-1.1.1-01 | Valid Egyptian phone (+20) with correct OTP | Happy Path | JWT issued, redirected to home |
| TC-1.1.1-02 | Valid Saudi phone (+966) with correct OTP | Happy Path | JWT issued, locale set to ar-SA |
| TC-1.1.1-03 | OTP entered after 120s expiration | Edge Case | OTP rejected, resend button shown |
| TC-1.1.1-04 | Incorrect OTP entered once | Negative | Error shown, 2 attempts remaining |
| TC-1.1.1-05 | 3 consecutive incorrect OTPs | Security | Account locked 5 minutes |
| TC-1.1.1-06 | Empty phone number submitted | Validation | Client-side validation error |
| TC-1.1.1-07 | Non-numeric characters in phone | Validation | Input rejected by mask |
| TC-1.1.1-08 | SQL injection in phone field | Security | Input sanitized, no auth flow |
| TC-1.1.1-09 | Concurrent OTP requests for same number | Concurrency | Only latest OTP is valid |
| TC-1.1.1-10 | OTP SMS language matches user locale | i18n | Arabic OTP for ar-EG, English for en-US |
| TC-1.1.1-11 | Network failure during SMS send | Error | Retry with exponential backoff |
| TC-1.1.1-12 | Cognito service unavailable | Error | Graceful error page shown |

---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/identity-and-access/modules/auth-and-onboarding/behaviours/phone-otp-sign-in/
├── services/
│   │   ├── cognito_auth_client.rs
│   │   ├── sns_sms_gateway.rs
│   │   ├── auth_session_api.ts
├── designs/
│   │   ├── PhoneOtpScreen.tsx
│   │   ├── OtpCountdownInput.tsx
│   │   ├── OtpStyles.ts
├── logic/
│   │   ├── usePhoneOtpAuth.ts
│   │   ├── phone_number_validator.rs
│   │   ├── otp_rate_limiter.rs
├── types/
│   │   ├── AuthPrincipal.ts
│   │   ├── InitiateOtpPayload.ts
│   │   ├── VerifyOtpPayload.ts
└── constants/
│   │   ├── AuthEndpoints.ts
│   │   ├── OtpDurationConstants.ts
│   │   ├── AuthErrorCodes.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/identity-and-access/modules/auth-and-onboarding/behaviours/phone-otp-sign-in/
├── services/
│   │   ├── cognito_auth_client.rs
│   │   ├── sns_sms_gateway.rs
│   │   ├── auth_session_api.ts
├── logic/
│   │   ├── usePhoneOtpAuth.ts
│   │   ├── phone_number_validator.rs
│   │   ├── otp_rate_limiter.rs
├── types/
│   │   ├── AuthPrincipal.ts
│   │   ├── InitiateOtpPayload.ts
│   │   ├── VerifyOtpPayload.ts
└── constants/
│   │   ├── AuthEndpoints.ts
│   │   ├── OtpDurationConstants.ts
│   │   ├── AuthErrorCodes.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/phone-otp-sign-in/` | `.../behaviours/phone-otp-sign-in/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
| **Module-Shared** | `.../modules/auth-and-onboarding/_shared/` | `.../modules/auth-and-onboarding/_shared/` | Shared domain primitives and UI elements used by $\ge 2$ behaviours in `auth-and-onboarding`. |
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
    A([User opens Sign-In page]) --> B{Select auth method}
    B -->|Phone OTP| C[Enter phone number]
    C --> D{Validate phone format}
    D -->|Invalid| E[Show validation error]
    E --> C
    D -->|Valid| F[POST /v1/auth/initiate]
    F --> G[Cognito InitiateAuth PKCE]
    G --> H[SNS sends localized OTP SMS]
    H --> I[Show OTP input + 120s timer]
    I --> J{Timer expired?}
    J -->|Yes| K[Disable input, show Resend button]
    K --> F
    J -->|No| L[User enters 6-digit OTP]
    L --> M[POST /v1/auth/verify-otp]
    M --> N{OTP valid?}
    N -->|No| O{Attempts < 3?}
    O -->|Yes| P[Show error, decrement attempts]
    P --> L
    O -->|No| Q[Lock account 5 minutes]
    Q --> R([Show lock message])
    N -->|Yes| S[Cognito Pre-Token Trigger]
    S --> T[Read USER# from DynamoDB]
    T --> U[Inject custom JWT claims]
    U --> V[Store tokens in expo-secure-store]
    V --> W[WatermelonDB delta sync]
    W --> X[Set UI direction RTL/LTR]
    X --> Y([Redirect to role landing page])
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
| **Denial of Service / Abuse** | High | SMS pumping, brute-force OTP guessing, session fixation, and cross-tenant claim spoofing | Token-bucket rate limiting per IP and account; strict input length validation. |
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
- [ ] **US-1.1.1-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-1.1.1-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against SMS pumping, brute-force OTP guessing, session fixation, and cross-tenant claim spoofing. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-1.1.1-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G4 — Integrated acceptance
- [ ] **US-1.1.1-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module auth-and-onboarding Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
