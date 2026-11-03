# US-1.1.3: Social OIDC Sign-In (Google & Apple)

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `identity-and-access`  
> **Domain Module**: `auth-and-onboarding`  
> **Autonomous Behaviour**: `social-oidc-sign-in`  
> **Client Framework Path**: `apps/storefront/src/features/identity-and-access/modules/auth-and-onboarding/behaviours/social-oidc-sign-in`  
> **Backend Framework Path**: `backend/src/features/identity-and-access/modules/auth-and-onboarding/behaviours/social-oidc-sign-in`  
> **Execution Sprint**: [Sprint 1.1](../../sprints/README.md)  
> **Slicing Standard**: [10-PR Vertical Slicing Framework](../../sprints/README.md#the-10-pr-vertical-slicing-standard-aligned-with-10-pillar-system-architecture)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** new or returning Customer,  
**I want to** sign in with my Google or Apple account using OpenID Connect federation,  
**So that** I can create an account or sign in with one tap without creating new credentials.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Social OIDC Sign-In
  Scenario: [AC-US-1.1.3-01] First-time Google sign-in (account linking)
    Given the user taps "Continue with Google" on "/ar-EG/(auth)/sign-in"
    When the Google OAuth consent screen appears and the user authorizes
    Then Cognito creates a new user record linked to the Google identity
    And the Pre-Token Trigger creates a USER# record in DynamoDB with persona=B2C_CUSTOMER
    And the user is redirected to "/ar-EG/" with a welcome banner
  Scenario: [AC-US-1.1.3-02] Returning Apple sign-in
    Given the user previously signed in with Apple
    When the user taps "Continue with Apple"
    Then Face ID/Touch ID prompts for verification
    And the existing Cognito user is authenticated
    And the JWT contains the existing custom claims
  Scenario: [AC-US-1.1.3-03] Email conflict — Google email matches existing password account
    Given a user with email "user@gmail.com" already exists via email/password
    When the user attempts Google sign-in with the same email
    Then the system offers to link the Google identity to the existing account
    And requires the user to verify ownership via OTP to the existing email
  Scenario: [AC-US-1.1.3-04] Apple Private Relay email
    Given the user signs in with Apple and opts for "Hide My Email"
    Then the system stores the Apple relay email as the primary identifier
    And all transactional emails are sent to the relay address
  Scenario: [AC-US-1.1.3-LAW] Global e-commerce legal compliance and third-party identity transfer regulations
    Given a user authenticating via third-party Identity Providers (Google, Apple)
    When exchanging identity claims across international borders
    Then identity token requests must be restricted to minimal necessary scopes (sub, email) per GDPR Art 5(1)(c)
    And international identity exchanges must comply with EU-US Data Privacy Framework (DPF) transfer rules
    And users must be provided with an immediate self-service mechanism to unlink third-party credentials without data loss
```

### 1.3 Test Cases & Traceability Matrix

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-1.1.3-01 | New user via Google OIDC | Happy Path | Account created, JWT issued |
| TC-1.1.3-02 | Returning user via Apple | Happy Path | Existing account authenticated |
| TC-1.1.3-03 | Google user cancels OAuth consent | Edge Case | Return to sign-in, no error |
| TC-1.1.3-04 | Email conflict with existing account | Conflict | Account linking flow offered |
| TC-1.1.3-05 | Apple Private Relay email | Edge Case | Relay email stored correctly |
| TC-1.1.3-06 | Google token expired mid-flow | Error | Graceful retry prompt |
| TC-1.1.3-07 | Social sign-in on Web (popup) | Platform | Popup completes, tokens stored |
| TC-1.1.3-08 | Social sign-in on Mobile (in-app browser) | Platform | Deep link returns tokens |
| TC-1.1.3-LAW | Global legal & regulatory compliance (GDPR Art 5(1)(c) scope minimization, EU-US DPF transfer rules, Apple ID unlinking) | Legal / Regulatory | Statutory compliance verified with zero legal or regulatory violations |

---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/identity-and-access/modules/auth-and-onboarding/behaviours/social-oidc-sign-in/
├── services/
│   │   ├── cognito_oidc_adapter.rs
│   │   ├── apple_auth_client.rs
│   │   ├── google_oidc_api.ts
├── designs/
│   │   ├── SocialSignInButtons.tsx
│   │   ├── OidcRedirectHandlerScreen.tsx
│   │   ├── AccountLinkingSheet.tsx
├── logic/
│   │   ├── useSocialSignIn.ts
│   │   ├── oidc_nonce_verifier.rs
│   │   ├── identity_linker.rs
├── types/
│   │   ├── SocialAuthPayload.ts
│   │   ├── OidcTokenClaims.ts
│   │   ├── LinkedIdentityRecord.ts
└── constants/
│   │   ├── OidcProviders.ts
│   │   ├── SocialAuthRoutes.ts
│   │   ├── OidcErrorCodes.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/identity-and-access/modules/auth-and-onboarding/behaviours/social-oidc-sign-in/
├── services/
│   │   ├── cognito_oidc_adapter.rs
│   │   ├── apple_auth_client.rs
│   │   ├── google_oidc_api.ts
├── logic/
│   │   ├── useSocialSignIn.ts
│   │   ├── oidc_nonce_verifier.rs
│   │   ├── identity_linker.rs
├── types/
│   │   ├── SocialAuthPayload.ts
│   │   ├── OidcTokenClaims.ts
│   │   ├── LinkedIdentityRecord.ts
└── constants/
│   │   ├── OidcProviders.ts
│   │   ├── SocialAuthRoutes.ts
│   │   ├── OidcErrorCodes.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/social-oidc-sign-in/` | `.../behaviours/social-oidc-sign-in/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
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
    A([User taps Social Sign-In]) --> B{Provider?}
    B -->|Google| C[Open Google OAuth consent]
    B -->|Apple| D[Trigger Apple Sign-In]
    C --> E{User authorizes?}
    D --> E
    E -->|No| F([Return to sign-in])
    E -->|Yes| G[Cognito Hosted UI callback]
    G --> H{User exists?}
    H -->|No| I[Create Cognito user + DynamoDB USER#]
    H -->|Yes, same provider| J[Authenticate existing user]
    H -->|Yes, different provider| K{Email conflict?}
    K -->|Yes| L[Offer account linking + OTP verify]
    L --> M{Verified?}
    M -->|Yes| N[Link identities]
    M -->|No| F
    K -->|No| J
    I --> O[Pre-Token Trigger → JWT]
    J --> O
    N --> O
    O --> P[Store tokens + sync]
    P --> Q([Redirect to home])
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
| **Denial of Service / Abuse** | High | State parameter tampering, CSRF on OAuth redirect, token substitution, and identity pre-hijacking | Token-bucket rate limiting per IP and account; strict input length validation. |
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

**Status: Pending — specification only; no implementation evidence.** All [G0–G4 quality gates + G-Review + G-Borrow + G-UI + G-Law](../../QUALITY_GATES.md) apply to this story. The following checks add to its acceptance criteria and test cases; they do not replace them.

### G1 — Test coverage
- [ ] **US-1.1.3-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-1.1.3-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against State parameter tampering, CSRF on OAuth redirect, token substitution, and identity pre-hijacking. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-1.1.3-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G-Review — Code review
- [ ] **US-1.1.3-G-Review:** Independent senior code review signed off by the Code Reviewer; verification across Correctness, Security, Maintainability, Performance, and Testing using the Agency-Agents code review standard; zero open Blocker or unresolved Suggestion findings.

### G-Borrow — Rust zero-clone borrowing validation
- [ ] **US-1.1.3-G-Borrow:** Backend code relies strictly on borrowing (&T, &mut T), explicit lifetimes, zero-copy byte buffers (bytes::Bytes), and zero unauthorized deep .clone() calls on domain entities and models (Arc::clone and Rc::clone pointer copies permitted only); certified by systems reviewer.

### G-UI — UI/UX validation
- [ ] **US-1.1.3-G-UI:** Pure separation of presentation (designs/, owned by ui-ux-designer) and headless hooks (logic/, owned by client-engineer); mobile components use @expo/ui primitives and native modules; web components use semantic HTML5 styled with Tailwind CSS; WCAG 2.1 AA and Arabic RTL layout parity verified; certified by UI/UX designer.

### G-Law — Law validation
- [ ] **US-1.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR scope data minimization, EU-US DPF cross-border data protection, and platform third-party unlinking rights; certified by compliance reviewer (`agency-legal-compliance-checker`).

### G4 — Integrated acceptance
- [ ] **US-1.1.3-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module auth-and-onboarding Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
