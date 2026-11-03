# US-3.1.1: Offline-First Cart with WatermelonDB Sync

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `order-processing-and-commerce`  
> **Domain Module**: `cart-and-checkout`  
> **Autonomous Behaviour**: `offline-cart-sync`  
> **Client Framework Path**: `apps/storefront/src/features/order-processing-and-commerce/modules/cart-and-checkout/behaviours/offline-cart-sync`  
> **Backend Framework Path**: `backend/src/features/order-processing-and-commerce/modules/cart-and-checkout/behaviours/offline-cart-sync`  
> **Execution Sprint**: [Sprint 1.2](../../sprints/README.md)  
> **Slicing Standard**: [10-PR Vertical Slicing Framework](../../sprints/README.md#the-10-pr-vertical-slicing-standard-aligned-with-10-pillar-system-architecture)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** Shopper on a mobile device with intermittent connectivity,  
**I want** my cart to work offline using WatermelonDB and sync to the server when connectivity restores,  
**So that** I never lose my cart contents regardless of network conditions.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Offline-First Cart
  Scenario: [AC-US-3.1.1-01] Add item to cart while offline
    Given the user is offline
    When the user clicks "Add to Cart" on a product page
    Then the item is written to the local WatermelonDB cart_items table
    And the cart badge count updates immediately
    And a pending sync indicator appears
  Scenario: [AC-US-3.1.1-02] Cart sync on reconnection
    Given the user has 3 items added offline
    When the device regains connectivity
    Then WatermelonDB synchronize() pushes changes to POST /v1/sync/push
    And the server validates stock availability for all items
    And any unavailable items are flagged with a warning
  Scenario: [AC-US-3.1.1-03] Concurrent cart modification on another device
    Given the user has the same account on phone and web
    And adds item A on phone and item B on web
    When both devices sync
    Then the cart contains both items A and B (union merge)
    And no items are lost
  Scenario: [AC-US-3.1.1-04] Remove last item from cart
    When the user removes the last item from the cart
    Then the cart shows an empty state with "Continue Shopping" button
    And the cart badge shows 0
  Scenario: [AC-US-3.1.1-05] Quantity exceeds available stock
    Given a product has 5 units in stock
    When the user tries to set quantity to 10
    Then the quantity is capped at 5
    And a warning "Only 5 available" is shown
  Scenario: [AC-US-3.1.1-LAW] Global e-commerce legal compliance and consumer cart integrity regulations
    Given a user adding items to an offline-first cart stored in local SQLite
    When the client synchronizes cached cart data with the cloud server
    Then client-side storage must be encrypted and restricted strictly to cart identifiers without accumulating unconsented PII
    And price discrepancies arising from offline cache expiration must be transparently disclosed to the consumer before checkout
    And cached pricing must not be covertly altered or inflated without explicit consumer acknowledgement
```

### 1.3 Test Cases & Traceability Matrix

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-3.1.1-01 | Add item offline | Happy Path | Local cart updated, sync pending |
| TC-3.1.1-02 | Sync on reconnection | Happy Path | Server cart matches local |
| TC-3.1.1-03 | Remove item | Happy Path | Item removed, badge updated |
| TC-3.1.1-04 | Quantity > stock | Validation | Capped at max stock |
| TC-3.1.1-05 | Quantity = 0 | Edge Case | Item removed from cart |
| TC-3.1.1-06 | Negative quantity | Validation | Rejected |
| TC-3.1.1-07 | Add same item twice | Edge Case | Quantity incremented |
| TC-3.1.1-08 | 50 items in cart | Performance | No lag in UI |
| TC-3.1.1-09 | Cross-device merge | Concurrency | Union merge, no data loss |
| TC-3.1.1-10 | Deleted product in cart | Error | Warning + remove option |
| TC-3.1.1-LAW | Global legal & regulatory compliance (GDPR Art 5 data minimization, consumer price lock disclosures, anti-deceptive trade practices) | Legal / Regulatory | Statutory compliance verified with zero legal or regulatory violations |

---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/order-processing-and-commerce/modules/cart-and-checkout/behaviours/offline-cart-sync/
├── services/
│   │   ├── cart_sync_client.rs
│   │   ├── watermelondb_cart_adapter.ts
│   │   ├── cart_api.ts
├── designs/
│   │   ├── CartItemList.tsx
│   │   ├── CartItemRow.tsx
│   │   ├── OfflineSyncStatusBadge.tsx
├── logic/
│   │   ├── useOfflineCart.ts
│   │   ├── cart_reconciliation_engine.ts
│   │   ├── quantity_limiter.ts
├── types/
│   │   ├── CartRecord.ts
│   │   ├── CartItemRecord.ts
│   │   ├── SyncCartConflictResolution.ts
└── constants/
│   │   ├── CartEndpoints.ts
│   │   ├── MaxCartQuantities.ts
│   │   ├── CartSyncErrorCodes.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/order-processing-and-commerce/modules/cart-and-checkout/behaviours/offline-cart-sync/
├── services/
│   │   ├── cart_sync_client.rs
│   │   ├── watermelondb_cart_adapter.ts
│   │   ├── cart_api.ts
├── logic/
│   │   ├── useOfflineCart.ts
│   │   ├── cart_reconciliation_engine.ts
│   │   ├── quantity_limiter.ts
├── types/
│   │   ├── CartRecord.ts
│   │   ├── CartItemRecord.ts
│   │   ├── SyncCartConflictResolution.ts
└── constants/
│   │   ├── CartEndpoints.ts
│   │   ├── MaxCartQuantities.ts
│   │   ├── CartSyncErrorCodes.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/offline-cart-sync/` | `.../behaviours/offline-cart-sync/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
| **Module-Shared** | `.../modules/cart-and-checkout/_shared/` | `.../modules/cart-and-checkout/_shared/` | Shared domain primitives and UI elements used by $\ge 2$ behaviours in `cart-and-checkout`. |
| **Feature-Shared** | `.../features/order-processing-and-commerce/_shared/` | `.../features/order-processing-and-commerce/_shared/` | Feature-level contracts, ports, and cross-module bridges across `order-processing-and-commerce`. |
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
    A([User adds item to cart]) --> B{Online?}
    B -->|Yes| C[Write to WatermelonDB + POST /v1/cart/items]
    B -->|No| D[Write to WatermelonDB only]
    D --> E[Show pending sync indicator]
    C --> F[Server validates stock]
    F --> G{Stock available?}
    G -->|Yes| H[Cart updated, badge count++]
    G -->|No| I[Show "Out of stock" warning]
    
    E --> J{Connectivity restored?}
    J -->|Yes| K[WatermelonDB synchronize push]
    K --> L[Server reconciles cart]
    L --> M{Conflicts?}
    M -->|Yes| N[Show item availability warnings]
    M -->|No| H
    J -->|No| O[Continue offline with local cart]
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
| **Denial of Service / Abuse** | High | Cart item price tampering in local SQLite, negative quantity injection, and cross-session cart leakage | Token-bucket rate limiting per IP and account; strict input length validation. |
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
- [ ] **US-3.1.1-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-3.1.1-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against Cart item price tampering in local SQLite, negative quantity injection, and cross-session cart leakage. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-3.1.1-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G-Review — Code review
- [ ] **US-3.1.1-G-Review:** Independent senior code review signed off by the Code Reviewer; verification across Correctness, Security, Maintainability, Performance, and Testing using the Agency-Agents code review standard; zero open Blocker or unresolved Suggestion findings.

### G-Borrow — Rust zero-clone borrowing validation
- [ ] **US-3.1.1-G-Borrow:** Backend code relies strictly on borrowing (&T, &mut T), explicit lifetimes, zero-copy byte buffers (bytes::Bytes), and zero unauthorized deep .clone() calls on domain entities and models (Arc::clone and Rc::clone pointer copies permitted only); certified by systems reviewer.

### G-UI — UI/UX validation
- [ ] **US-3.1.1-G-UI:** Pure separation of presentation (designs/, owned by ui-ux-designer) and headless hooks (logic/, owned by client-engineer); mobile components use @expo/ui primitives and native modules; web components use semantic HTML5 styled with Tailwind CSS; WCAG 2.1 AA and Arabic RTL layout parity verified; certified by UI/UX designer.

### G-Law — Law validation
- [ ] **US-3.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR client data minimization, transparent cart price lock terms, and anti-deceptive pricing safeguards; certified by compliance reviewer (`agency-legal-compliance-checker`).

### G4 — Integrated acceptance
- [ ] **US-3.1.1-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module cart-and-checkout Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
