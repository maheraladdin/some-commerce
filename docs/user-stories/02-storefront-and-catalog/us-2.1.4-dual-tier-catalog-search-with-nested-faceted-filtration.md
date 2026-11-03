# US-2.1.4: Dual-Tier Catalog Search with Nested Faceted Filtration

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `catalog-and-discovery`  
> **Domain Module**: `storefront-and-catalog`  
> **Autonomous Behaviour**: `dual-tier-search`  
> **Client Framework Path**: `apps/storefront/src/features/catalog-and-discovery/modules/storefront-and-catalog/behaviours/dual-tier-search`  
> **Backend Framework Path**: `backend/src/features/catalog-and-discovery/modules/storefront-and-catalog/behaviours/dual-tier-search`  
> **Execution Sprint**: [Sprint 1.1](../../sprints/README.md)  
> **Slicing Standard**: [7-PR Vertical Slicing Framework](../../sprints/README.md#the-7-pr-vertical-slicing-standard)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** Shopper browsing a category page, brand page, or using the search bar,  
**I want to** filter products by category, brand, price range, stock status, COD eligibility, and any dynamic custom property with live facet counts,  
**So that** I can narrow down thousands of products in under 50ms.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Dual-Tier Catalog Search
  Scenario: [AC-US-2.1.4-01] Elasticsearch faceted search (Tier 2 primary)
    Given the user is on "/ar-EG/c/gaming-laptops"
    When the user toggles Brand=ASUS, Color=Black, RAM=16..64GB
    Then the system queries Elasticsearch with nested property filters
    And returns matching products with live facet counts in <50ms
    And the URL query string is updated for shareability
  Scenario: [AC-US-2.1.4-02] DynamoDB fallback search (Tier 1 circuit-breaker)
    Given Elasticsearch is unreachable (circuit breaker open)
    When the user performs a search
    Then the system falls back to DynamoDB GSI1/GSI2 with FilterExpression
    And returns filtered results (without nested facet counts)
    And a subtle "Limited filtering" indicator appears
  Scenario: [AC-US-2.1.4-03] ETag cache hit for identical query
    Given the user previously searched Brand=ASUS, RAM=16GB on this page
    And the results are cached in L1 Moka/L2 Redis
    When the user navigates back and the same query fires
    Then the server returns 304 Not Modified in <0.1ms
    And the UI renders from the TanStack Query cache
  Scenario: [AC-US-2.1.4-04] Empty search results
    Given no products match the filter combination
    Then a "No products found" message appears in the user's locale
    And suggestions to broaden filters are shown
    And the facet counts show 0 for all options
  Scenario: [AC-US-2.1.4-05] Search with COD eligibility filter
    When the user toggles "Cash on Delivery Available" filter
    Then only products with supports_cod=true are shown
    And the facet counts update accordingly
```

### 1.3 Test Cases & Traceability Matrix

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-2.1.4-01 | Multi-facet ES search | Happy Path | Results + facets in <50ms |
| TC-2.1.4-02 | ES unavailable, DDB fallback | Fallback | Results without facet counts |
| TC-2.1.4-03 | ETag 304 cache hit | Performance | <0.1ms response |
| TC-2.1.4-04 | Empty results | Edge Case | Helpful empty state |
| TC-2.1.4-05 | 10,000+ products in category | Performance | Pagination, <100ms |
| TC-2.1.4-06 | Arabic text search "لابتوب" | i18n | Arabic analyzer matches |
| TC-2.1.4-07 | COD eligibility filter | Happy Path | Only COD products shown |
| TC-2.1.4-08 | Price range slider 0 to max | Edge Case | All products in range |
| TC-2.1.4-09 | URL query string shareability | UX | Shared URL restores filters |
| TC-2.1.4-10 | Concurrent filter toggles | Concurrency | TanStack Query debounces |

---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/catalog-and-discovery/modules/storefront-and-catalog/behaviours/dual-tier-search/
├── services/
│   │   ├── elasticsearch_search_client.rs
│   │   ├── dynamo_filter_provider.rs
│   │   ├── search_api.ts
├── designs/
│   │   ├── SearchFacetedView.tsx
│   │   ├── FilterDrawerSheet.tsx
│   │   ├── DisjunctiveFacetPills.tsx
├── logic/
│   │   ├── useCatalogSearch.ts
│   │   ├── query_ast_sanitizer.rs
│   │   ├── facet_disjunction_aggregator.ts
├── types/
│   │   ├── SearchQueryPayload.ts
│   │   ├── FacetedSearchResult.ts
│   │   ├── FacetAggregation.ts
└── constants/
│   │   ├── SearchEndpoints.ts
│   │   ├── SearchAnalyzerConfig.ts
│   │   ├── FacetKeys.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/catalog-and-discovery/modules/storefront-and-catalog/behaviours/dual-tier-search/
├── services/
│   │   ├── elasticsearch_search_client.rs
│   │   ├── dynamo_filter_provider.rs
│   │   ├── search_api.ts
├── logic/
│   │   ├── useCatalogSearch.ts
│   │   ├── query_ast_sanitizer.rs
│   │   ├── facet_disjunction_aggregator.ts
├── types/
│   │   ├── SearchQueryPayload.ts
│   │   ├── FacetedSearchResult.ts
│   │   ├── FacetAggregation.ts
└── constants/
│   │   ├── SearchEndpoints.ts
│   │   ├── SearchAnalyzerConfig.ts
│   │   ├── FacetKeys.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/dual-tier-search/` | `.../behaviours/dual-tier-search/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
| **Module-Shared** | `.../modules/storefront-and-catalog/_shared/` | `.../modules/storefront-and-catalog/_shared/` | Shared domain primitives and UI elements used by $\ge 2$ behaviours in `storefront-and-catalog`. |
| **Feature-Shared** | `.../features/catalog-and-discovery/_shared/` | `.../features/catalog-and-discovery/_shared/` | Feature-level contracts, ports, and cross-module bridges across `catalog-and-discovery`. |
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
    A([User toggles filter on PLP]) --> B[useCatalogSearchAndFacets updates state]
    B --> C[TanStack Query: fetchWithEtag]
    C --> D[Attach If-None-Match header]
    D --> E[GET /v1/search]
    E --> F{L1/L2 ETag match?}
    F -->|Yes| G[304 Not Modified]
    G --> H[Render from cache — no UI change]
    F -->|No| I{Elasticsearch healthy?}
    I -->|Yes| J[Tier 2: ES bool + nested query + aggregations]
    J --> K[Return hits + facet counts]
    I -->|No - circuit breaker| L[Tier 1: DDB GSI1 + FilterExpression]
    L --> M[Return filtered items without facet counts]
    K --> N[Cache in L1 Moka + L2 Redis]
    M --> N
    N --> O[200 OK + ETag header]
    O --> P[Update TanStack Query cache]
    P --> Q[Render ProductCardGrid + facet sidebar]
    Q --> R[Update URL query string]
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
| **Denial of Service / Abuse** | High | Elasticsearch injection queries, ReDoS in search phrase parsers, and unauthorized unlisted product indexing leaks | Token-bucket rate limiting per IP and account; strict input length validation. |
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
- [ ] **US-2.1.4-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-2.1.4-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against Elasticsearch injection queries, ReDoS in search phrase parsers, and unauthorized unlisted product indexing leaks. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-2.1.4-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G4 — Integrated acceptance
- [ ] **US-2.1.4-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module storefront-and-catalog Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
