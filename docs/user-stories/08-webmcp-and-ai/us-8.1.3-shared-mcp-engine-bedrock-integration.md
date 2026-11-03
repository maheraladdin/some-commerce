# US-8.1.3: Shared MCP Engine & Bedrock Integration

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `catalog-and-discovery`  
> **Domain Module**: `webmcp-and-ai`  
> **Autonomous Behaviour**: `shared-mcp-engine`  
> **Client Framework Path**: `apps/storefront/src/features/catalog-and-discovery/modules/webmcp-and-ai/behaviours/shared-mcp-engine`  
> **Backend Framework Path**: `backend/src/features/catalog-and-discovery/modules/webmcp-and-ai/behaviours/shared-mcp-engine`  
> **Execution Sprint**: [Sprint 1.1](../../sprints/README.md)  
> **Slicing Standard**: [10-PR Vertical Slicing Framework](../../sprints/README.md#the-10-pr-vertical-slicing-standard-aligned-with-10-pillar-system-architecture)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

**As a** Developer,  
**I want** a shared MCP tool registry that serves both WebMCP (`navigator.modelContext`) on Web and Amazon Bedrock Converse on Mobile/in-app chat,  
**So that** all AI tools are defined once and available across all platforms.

### 1.2 Acceptance Criteria (Gherkin Scenarios)

```gherkin
Feature: Shared MCP Engine
  Scenario: [AC-US-8.1.3-01] Tool registration on Web
    When the Expo Web app loads
    Then all customer tools are registered on navigator.modelContext
    And admin tools are only registered if cognito:groups contains STORE_ADMIN
  Scenario: [AC-US-8.1.3-02] Tool execution on Mobile via Bedrock
    When a mobile user sends a chat message
    Then POST /v1/mcp/customer invokes Bedrock Converse with tool schemas
    And Bedrock selects the appropriate tool and returns structured output
  Scenario: [AC-US-8.1.3-03] Schema code generation
    When a developer runs the codegen pipeline
    Then Rust structs in crates/mcp-tools auto-export to TypeScript + JSON Schema
    And the WebMCP and Bedrock schemas stay in sync
  Scenario: [AC-US-8.1.3-LAW] Global e-commerce legal compliance and cloud AI provider data protection regulations
    Given the core MCP engine dispatching prompts and tool execution payloads to AWS Bedrock
    When processing LLM invocations across customer and admin contexts
    Then customer PII and sensitive credentials must be stripped or masked before transmitting prompts to foundational model endpoints
    And the LLM service integration must operate under a formal GDPR Art 28 Data Processing Agreement guaranteeing zero model training on customer data
    And model outputs must be passed through safety filters preventing generation of harmful, discriminatory, or unlawful content
```

### 1.3 Test Cases & Traceability Matrix


| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-8.1.3-01 | Primary user journey functional flow | Happy Path | User story outcome achieved |
| TC-8.1.3-02 | Edge case and boundary condition validation | Edge Case | Handled with typed error |
| TC-8.1.3-03 | Threat model and authorization boundary validation | Security | Unauthorized requests rejected |
| TC-8.1.3-LAW | Global legal & regulatory compliance (GDPR Art 28 DPA terms, zero LLM model training on customer data, automated PII redaction) | Legal / Regulatory | Statutory compliance verified with zero legal or regulatory violations |
---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/catalog-and-discovery/modules/webmcp-and-ai/behaviours/shared-mcp-engine/
├── services/
│   │   ├── mcp_rpc_handler.rs
│   │   ├── bedrock_converse_client.rs
│   │   ├── mcp_protocol_api.ts
├── designs/
│   │   ├── McpStatusIndicator.tsx
│   │   ├── ProtocolInspectorModal.tsx
│   │   ├── TokenUsageMeter.tsx
├── logic/
│   │   ├── useSharedMcpEngine.ts
│   │   ├── mcp_message_codec.rs
│   │   ├── rate_budget_governor.rs
├── types/
│   │   ├── JsonRpcRequest.ts
│   │   ├── JsonRpcResponse.ts
│   │   ├── McpContextSnapshot.ts
└── constants/
│   │   ├── McpSpecVersion.ts
│   │   ├── DefaultTokenLimits.ts
│   │   ├── McpErrorCodes.ts
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/catalog-and-discovery/modules/webmcp-and-ai/behaviours/shared-mcp-engine/
├── services/
│   │   ├── mcp_rpc_handler.rs
│   │   ├── bedrock_converse_client.rs
│   │   ├── mcp_protocol_api.ts
├── logic/
│   │   ├── useSharedMcpEngine.ts
│   │   ├── mcp_message_codec.rs
│   │   ├── rate_budget_governor.rs
├── types/
│   │   ├── JsonRpcRequest.ts
│   │   ├── JsonRpcResponse.ts
│   │   ├── McpContextSnapshot.ts
└── constants/
│   │   ├── McpSpecVersion.ts
│   │   ├── DefaultTokenLimits.ts
│   │   ├── McpErrorCodes.ts
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/shared-mcp-engine/` | `.../behaviours/shared-mcp-engine/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
| **Module-Shared** | `.../modules/webmcp-and-ai/_shared/` | `.../modules/webmcp-and-ai/_shared/` | Shared domain primitives and UI elements used by $\ge 2$ behaviours in `webmcp-and-ai`. |
| **Feature-Shared** | `.../features/catalog-and-discovery/_shared/` | `.../features/catalog-and-discovery/_shared/` | Feature-level contracts, ports, and cross-module bridges across `catalog-and-discovery`. |
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
| **Denial of Service / Abuse** | High | Denial of wallet via token exhaustion loops, arbitrary RPC command execution through malformed JSON-RPC | Token-bucket rate limiting per IP and account; strict input length validation. |
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
- [ ] **US-8.1.3-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **US-8.1.3-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against Denial of wallet via token exhaustion loops, arbitrary RPC command execution through malformed JSON-RPC. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **US-8.1.3-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G-Review — Code review
- [ ] **US-8.1.3-G-Review:** Independent senior code review signed off by the Code Reviewer; verification across Correctness, Security, Maintainability, Performance, and Testing using the Agency-Agents code review standard; zero open Blocker or unresolved Suggestion findings.

### G-Law — Law validation
- [ ] **US-8.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR Art 28 cloud provider data processing terms, complete customer PII redaction from LLM prompts, and AI content safety filters; certified by compliance reviewer (`agency-legal-compliance-checker`).

### G4 — Integrated acceptance
- [ ] **US-8.1.3-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module webmcp-and-ai Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
