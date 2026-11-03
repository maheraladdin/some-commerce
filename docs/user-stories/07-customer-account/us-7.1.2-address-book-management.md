# US-7.1.2: Address Book Management

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `identity-and-access`  
> **Domain Module**: `customer-account`  
> **Autonomous Behaviour**: `address-book-management`  
> **Client Framework Path**: `apps/storefront/src/features/identity-and-access/modules/customer-account/behaviours/address-book-management`  
> **Backend Framework Path**: `backend/src/features/identity-and-access/modules/customer-account/behaviours/address-book-management`  
> **Execution Sprint**: [Sprint 1.1](../../sprints/README.md)  
> **Slicing Standard**: [10-PR Vertical Slicing Framework](../../sprints/README.md#the-10-pr-vertical-slicing-standard-aligned-with-10-pillar-system-architecture)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** Customer,  
**I want to** manage multiple delivery addresses with a default address for quicker checkout,  
**So that** I can ship to different locations without re-entering address details.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Address Book
  Scenario: [AC-US-7.1.2-01] Add new address
    When the customer adds a new address with all required fields
    Then the address is saved in the USER# addresses array in DynamoDB
    And synced to WatermelonDB for offline access
  Scenario: [AC-US-7.1.2-02] Set default address
    When the customer marks an address as default
    Then that address is pre-selected during checkout
  Scenario: [AC-US-7.1.2-03] Delete address used in pending order
    Given an address is referenced by a pending order
    When the customer tries to delete it
    Then a warning "This address is used by a pending order" is shown
    And deletion is blocked until the order is fulfilled
  Scenario: [AC-US-7.1.2-04] Max address limit
    Given the customer has 10 addresses (maximum)
    When they try to add an 11th
    Then an error "Maximum 10 addresses allowed. Remove one first." is shown
  Scenario: [AC-US-7.1.2-LAW] Global e-commerce legal compliance and address data retention regulations
    Given a customer managing saved shipping and billing addresses
    When deleting or updating stored address book entries
    Then customer address deletions must immediately remove personal location records from active operational address books
    And archived historical address snapshots tied to fulfilled orders must be retained strictly under statutory fiscal audit rules
    And cross-border storage of customer address data must comply with international data transfer safeguards (SCCs / DPF)
```

### 1.3 Test Cases & Traceability Matrix

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-7.1.2-01 | Add valid address | Happy Path | Saved and synced |
| TC-7.1.2-02 | Set default address | Happy Path | Default used in checkout |
| TC-7.1.2-03 | Edit existing address | Happy Path | Updated |
| TC-7.1.2-04 | Delete unused address | Happy Path | Removed |
| TC-7.1.2-05 | Delete address used by order | Validation | Blocked |
| TC-7.1.2-06 | 11th address | Validation | Limit error |
| TC-7.1.2-07 | Offline address add | Edge Case | Synced on reconnect |
| TC-7.1.2-08 | Arabic address labels | i18n | RTL labels |
| TC-7.1.2-LAW | Global legal & regulatory compliance (GDPR Art 17 Right to Erasure, statutory tax audit address preservation, cross-border safeguards) | Legal / Regulatory | Statutory compliance verified with zero legal or regulatory violations |

---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/identity-and-access/modules/customer-account/behaviours/address-book-management/
├── services/
│   │   ├── address_book_service.rs
│   │   ├── default_address_setter.rs
│   │   ├── address_book_api.ts
├── designs/
│   │   ├── AddressBookScreen.tsx
│   │   ├── AddressCardWithActions.tsx
│   │   ├── SetDefaultAddressButton.tsx
├── logic/
│   │   ├── useAddressBook.ts
│   │   ├── default_address_switcher.ts
│   │   ├── address_limit_checker.rs
├── types/
│   │   ├── AddressBookEntry.ts
│   │   ├── NewAddressPayload.ts
│   │   ├── AddressMutationResponse.ts
└── constants/
│   │   ├── AddressBookEndpoints.ts
│   │   ├── MaxSavedAddresses.ts
│   │   ├── AddressBookErrors.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/identity-and-access/modules/customer-account/behaviours/address-book-management/
├── services/
│   │   ├── address_book_service.rs
│   │   ├── default_address_setter.rs
│   │   ├── address_book_api.ts
├── logic/
│   │   ├── useAddressBook.ts
│   │   ├── default_address_switcher.ts
│   │   ├── address_limit_checker.rs
├── types/
│   │   ├── AddressBookEntry.ts
│   │   ├── NewAddressPayload.ts
│   │   ├── AddressMutationResponse.ts
└── constants/
│   │   ├── AddressBookEndpoints.ts
│   │   ├── MaxSavedAddresses.ts
│   │   ├── AddressBookErrors.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/address-book-management/` | `.../behaviours/address-book-management/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
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
    A([Customer opens address book]) --> B[GET /v1/account/addresses]
    B --> C[Render address list from WatermelonDB]
    C --> D{Action?}
    D -->|Add| E[Show localized address form]
    E --> F{Valid?}
    F -->|No| G[Show errors]
    F -->|Yes| H[POST /v1/account/addresses]
    H --> I[Sync WatermelonDB]
    D -->|Edit| J[Pre-fill form]
    J --> K[PUT /v1/account/addresses/:id]
    K --> I
    D -->|Delete| L{Used by pending order?}
    L -->|Yes| M[Show warning, block delete]
    L -->|No| N[DELETE /v1/account/addresses/:id]
    N --> I
    D -->|Set Default| O[PUT /v1/account/addresses/:id default=true]
    O --> I
    I --> P([Address book updated])
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
| **Denial of Service / Abuse** | High | Address book pollution via automated bot scripts, IDOR modifying other customers saved addresses | Token-bucket rate limiting per IP and account; strict input length validation. |
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
- [ ] **US-7.1.2-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-7.1.2-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against Address book pollution via automated bot scripts, IDOR modifying other customers saved addresses. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-7.1.2-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G-Review — Code review
- [ ] **US-7.1.2-G-Review:** Independent senior code review signed off by the Code Reviewer; verification across Correctness, Security, Maintainability, Performance, and Testing using the Agency-Agents code review standard; zero open Blocker or unresolved Suggestion findings.

### G-Borrow — Rust zero-clone borrowing validation
- [ ] **US-7.1.2-G-Borrow:** Backend code relies strictly on borrowing (&T, &mut T), explicit lifetimes, zero-copy byte buffers (bytes::Bytes), and zero unauthorized deep .clone() calls on domain entities and models (Arc::clone and Rc::clone pointer copies permitted only); certified by systems reviewer.

### G-UI — UI/UX validation
- [ ] **US-7.1.2-G-UI:** Pure separation of presentation (designs/, owned by ui-ux-designer) and headless hooks (logic/, owned by client-engineer); mobile components use @expo/ui primitives and native modules; web components use semantic HTML5 styled with Tailwind CSS; WCAG 2.1 AA and Arabic RTL layout parity verified; certified by UI/UX designer.

### G-Law — Law validation
- [ ] **US-7.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR Art 17 ("Right to be Forgotten"), commercial tax address retention reconciliation, and international data transfer safeguards; certified by compliance reviewer (`agency-legal-compliance-checker`).

### G4 — Integrated acceptance
- [ ] **US-7.1.2-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module customer-account Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
