# US-3.1.2: Multi-Vendor Cart Grouping & Shipping Estimation

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `order-processing-and-commerce`  
> **Domain Module**: `cart-and-checkout`  
> **Autonomous Behaviour**: `multi-vendor-cart-grouping`  
> **Client Framework Path**: `apps/storefront/src/features/order-processing-and-commerce/modules/cart-and-checkout/behaviours/multi-vendor-cart-grouping`  
> **Backend Framework Path**: `backend/src/features/order-processing-and-commerce/modules/cart-and-checkout/behaviours/multi-vendor-cart-grouping`  
> **Execution Sprint**: [Sprint 1.2](../../sprints/README.md)  
> **Slicing Standard**: [7-PR Vertical Slicing Framework](../../sprints/README.md#the-7-pr-vertical-slicing-standard)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** Shopper with items from multiple vendors in my cart,  
**I want** my cart to visually group items by vendor and show per-vendor shipping estimates,  
**So that** I understand the shipping cost breakdown before checkout.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Multi-Vendor Cart Grouping
  Scenario: [AC-US-3.1.2-01] Cart with items from 3 vendors
    Given the cart has items from Vendor A, Vendor B, and Vendor C
    Then the cart page groups items into 3 vendor sections
    And each section shows the vendor name and subtotal
    And per-vendor shipping estimates are calculated separately
  Scenario: [AC-US-3.1.2-02] Single-vendor cart
    Given all cart items are from the same vendor
    Then no vendor grouping header is shown
    And a single shipping estimate is displayed
  Scenario: [AC-US-3.1.2-03] Remove all items from one vendor group
    Given the cart has items from Vendor A and Vendor B
    When the user removes all Vendor A items
    Then the Vendor A group disappears
    And shipping is recalculated for Vendor B only
```

### 1.3 Test Cases & Traceability Matrix

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-3.1.2-01 | 3-vendor cart grouping | Happy Path | 3 groups with subtotals |
| TC-3.1.2-02 | Single vendor | Edge Case | No group headers |
| TC-3.1.2-03 | Remove vendor group | Happy Path | Group disappears, recalc |
| TC-3.1.2-04 | Per-vendor shipping estimate | Happy Path | Separate rates per vendor |
| TC-3.1.2-05 | 10 vendors in cart | Performance | All groups render <200ms |

---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/order-processing-and-commerce/modules/cart-and-checkout/behaviours/multi-vendor-cart-grouping/
├── services/
│   │   ├── vendor_grouping_client.rs
│   │   ├── shipping_estimator_service.rs
│   │   ├── grouping_api.ts
├── designs/
│   │   ├── VendorGroupSection.tsx
│   │   ├── VendorShippingEstimatePill.tsx
│   │   ├── SplitOrderBanner.tsx
├── logic/
│   │   ├── useVendorCartGroups.ts
│   │   ├── sub_cart_grouper.rs
│   │   ├── proportional_shipping_calc.ts
├── types/
│   │   ├── VendorCartGroup.ts
│   │   ├── SubOrderEstimate.ts
│   │   ├── VendorShippingRate.ts
└── constants/
│   │   ├── VendorGroupingEndpoints.ts
│   │   ├── ShippingEstimateLimits.ts
│   │   ├── GroupingErrors.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/order-processing-and-commerce/modules/cart-and-checkout/behaviours/multi-vendor-cart-grouping/
├── services/
│   │   ├── vendor_grouping_client.rs
│   │   ├── shipping_estimator_service.rs
│   │   ├── grouping_api.ts
├── logic/
│   │   ├── useVendorCartGroups.ts
│   │   ├── sub_cart_grouper.rs
│   │   ├── proportional_shipping_calc.ts
├── types/
│   │   ├── VendorCartGroup.ts
│   │   ├── SubOrderEstimate.ts
│   │   ├── VendorShippingRate.ts
└── constants/
│   │   ├── VendorGroupingEndpoints.ts
│   │   ├── ShippingEstimateLimits.ts
│   │   ├── GroupingErrors.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/multi-vendor-cart-grouping/` | `.../behaviours/multi-vendor-cart-grouping/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
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
    A([User opens cart]) --> B[Read cart_items from WatermelonDB]
    B --> C[Group items by vendor_id]
    C --> D{Multiple vendors?}
    D -->|Yes| E[Render vendor group headers]
    D -->|No| F[Render flat item list]
    E --> G[Calculate per-vendor subtotals]
    F --> G
    G --> H[POST /v1/rates/calculate per vendor group]
    H --> I[Display shipping estimates per group]
    I --> J[Show cart total = sum of all groups + shipping]
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
| **Denial of Service / Abuse** | High | Unauthorized vendor order tampering, shipping cost avoidance via vendor spoofing, and inventory race manipulation | Token-bucket rate limiting per IP and account; strict input length validation. |
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
- [ ] **US-3.1.2-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-3.1.2-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against Unauthorized vendor order tampering, shipping cost avoidance via vendor spoofing, and inventory race manipulation. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-3.1.2-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G4 — Integrated acceptance
- [ ] **US-3.1.2-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module cart-and-checkout Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
