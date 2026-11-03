# US-6.1.1: Real-Time Order Tracking & Live Status Timeline

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `order-processing-and-commerce`  
> **Domain Module**: `orders-and-returns`  
> **Autonomous Behaviour**: `realtime-order-tracking`  
> **Client Framework Path**: `apps/storefront/src/features/order-processing-and-commerce/modules/orders-and-returns/behaviours/realtime-order-tracking`  
> **Backend Framework Path**: `backend/src/features/order-processing-and-commerce/modules/orders-and-returns/behaviours/realtime-order-tracking`  
> **Execution Sprint**: [Sprint 1.2](../../sprints/README.md)  
> **Slicing Standard**: [10-PR Vertical Slicing Framework](../../sprints/README.md#the-10-pr-vertical-slicing-standard-aligned-with-10-pillar-system-architecture)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** Customer who has placed an order,  
**I want to** track my order in real-time with a visual status timeline and live carrier tracking map,  
**So that** I know exactly where my package is and when to expect delivery.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Order Tracking
  Scenario: [AC-US-6.1.1-01] View order confirmation with timeline
    Given the customer opens "/[locale]/orders/ord_1/confirmation"
    Then a status timeline shows all milestones (Confirmed → Packed → Shipped → Delivered)
    And the current status is highlighted
    And for COD orders, the cash balance to prepare is prominently shown
  Scenario: [AC-US-6.1.1-02] Live carrier tracking
    Given the order has a Bosta AWB number
    Then a live tracking card shows the carrier's real-time status
    And the tracking URL deep-links to Bosta's tracking page
  Scenario: [AC-US-6.1.1-03] Order with multiple sub-orders
    Given a multi-vendor order has 3 sub-orders
    Then each sub-order shows its own timeline and tracking info
    And sub-orders may be at different statuses
  Scenario: [AC-US-6.1.1-LAW] Global e-commerce legal compliance and consumer order delivery regulations
    Given an active customer order progressing through fulfillment and delivery
    When updating the live status timeline and estimated delivery date
    Then the system must enforce statutory delivery deadlines (maximum 30 calendar days under EU law unless explicitly agreed otherwise)
    And legal risk of loss or transit damage must remain with the merchant until physical possession is acquired by the consumer
    And delivery milestone updates must provide accurate tracking data without deceptive progress indicators
```

### 1.3 Test Cases & Traceability Matrix

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-6.1.1-01 | View status timeline | Happy Path | All milestones shown |
| TC-6.1.1-02 | COD balance banner | Happy Path | Cash amount shown |
| TC-6.1.1-03 | Live tracking card | Happy Path | Real-time status |
| TC-6.1.1-04 | Multi-sub-order tracking | Happy Path | Separate timelines |
| TC-6.1.1-05 | Order not found | Error | 404 page |
| TC-6.1.1-06 | Access another user's order | Security | 403 Forbidden |
| TC-6.1.1-07 | RTL timeline layout | i18n | Mirrored timeline |
| TC-6.1.1-LAW | Global legal & regulatory compliance (EU Consumer Rights Directive Art 18 30-day fulfillment, risk of loss transfer upon delivery) | Legal / Regulatory | Statutory compliance verified with zero legal or regulatory violations |

---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/order-processing-and-commerce/modules/orders-and-returns/behaviours/realtime-order-tracking/
├── services/
│   │   ├── live_tracking_client.rs
│   │   ├── order_event_stream_subscriber.rs
│   │   ├── tracking_api.ts
├── designs/
│   │   ├── LiveTrackingMapScreen.tsx
│   │   ├── OrderStatusTimeline.tsx
│   │   ├── DriverContactButton.tsx
├── logic/
│   │   ├── useRealtimeOrderTracking.ts
│   │   ├── status_progression_calculator.ts
│   │   ├── eta_recalculator.ts
├── types/
│   │   ├── OrderStatusSnapshot.ts
│   │   ├── TrackingMilestone.ts
│   │   ├── LiveLocationPayload.ts
└── constants/
│   │   ├── TrackingEndpoints.ts
│   │   ├── FinalOrderStates.ts
│   │   ├── TrackingErrorCodes.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/order-processing-and-commerce/modules/orders-and-returns/behaviours/realtime-order-tracking/
├── services/
│   │   ├── live_tracking_client.rs
│   │   ├── order_event_stream_subscriber.rs
│   │   ├── tracking_api.ts
├── logic/
│   │   ├── useRealtimeOrderTracking.ts
│   │   ├── status_progression_calculator.ts
│   │   ├── eta_recalculator.ts
├── types/
│   │   ├── OrderStatusSnapshot.ts
│   │   ├── TrackingMilestone.ts
│   │   ├── LiveLocationPayload.ts
└── constants/
│   │   ├── TrackingEndpoints.ts
│   │   ├── FinalOrderStates.ts
│   │   ├── TrackingErrorCodes.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/realtime-order-tracking/` | `.../behaviours/realtime-order-tracking/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
| **Module-Shared** | `.../modules/orders-and-returns/_shared/` | `.../modules/orders-and-returns/_shared/` | Shared domain primitives and UI elements used by $\ge 2$ behaviours in `orders-and-returns`. |
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
    A([Customer opens order confirmation]) --> B[GET /v1/orders/:id]
    B --> C{Authorized?}
    C -->|No| D[403 Forbidden]
    C -->|Yes| E[Load order with sub-orders]
    E --> F[Render status timeline]
    F --> G{Has AWB?}
    G -->|Yes| H[Show live tracking card]
    G -->|No| I[Show "Preparing shipment"]
    H --> J{Is COD?}
    I --> J
    J -->|Yes| K[Show COD balance banner]
    J -->|No| L[No COD banner]
    K --> M([Render complete page])
    L --> M
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
| **Denial of Service / Abuse** | High | IDOR on live courier coordinates, unauthenticated order timeline scraping, and fake milestone events | Token-bucket rate limiting per IP and account; strict input length validation. |
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
- [ ] **US-6.1.1-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-6.1.1-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against IDOR on live courier coordinates, unauthenticated order timeline scraping, and fake milestone events. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-6.1.1-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G-Review — Code review
- [ ] **US-6.1.1-G-Review:** Independent senior code review signed off by the Code Reviewer; verification across Correctness, Security, Maintainability, Performance, and Testing using the Agency-Agents code review standard; zero open Blocker or unresolved Suggestion findings.

### G-Borrow — Rust zero-clone borrowing validation
- [ ] **US-6.1.1-G-Borrow:** Backend code relies strictly on borrowing (&T, &mut T), explicit lifetimes, zero-copy byte buffers (bytes::Bytes), and zero unauthorized deep .clone() calls on domain entities and models (Arc::clone and Rc::clone pointer copies permitted only); certified by systems reviewer.

### G-UI — UI/UX validation
- [ ] **US-6.1.1-G-UI:** Pure separation of presentation (designs/, owned by ui-ux-designer) and headless hooks (logic/, owned by client-engineer); mobile components use @expo/ui primitives and native modules; web components use semantic HTML5 styled with Tailwind CSS; WCAG 2.1 AA and Arabic RTL layout parity verified; certified by UI/UX designer.

### G-Law — Law validation
- [ ] **US-6.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Consumer Rights Directive Art 18 (statutory 30-day fulfillment limit), merchant transit loss liability, and accurate milestone disclosures; certified by compliance reviewer (`agency-legal-compliance-checker`).

### G4 — Integrated acceptance
- [ ] **US-6.1.1-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module orders-and-returns Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
