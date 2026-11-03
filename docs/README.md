# some-commerce: Master Documentation Portal

> **Fullstack Multi-Tenant Microkernel E-Commerce Platform**  
> Universal Expo SDK 58 (iOS, Android, Web) + Rust 2024 Cargo Lambda (AWS Graviton) + DynamoDB Single-Table + AWS Marketplace CDK

Welcome to the central documentation portal for `some-commerce`. This directory organizes the platform's architectural specifications, user stories, sprint execution plans, security/architecture audits, test reports, and quality validation records into dedicated, standardized documentation hubs.

---

## 1. Documentation Hubs Overview

| Hub | Directory Path | Description & Primary Contents |
|:----|:---------------|:-------------------------------|
| 🎯 **User Stories** | [`docs/user-stories/`](./user-stories/README.md) | **46 Spec Kit User Stories** across 13 functional modules, complete with Gherkin ACs, test cases, and Activity Diagrams. |
| 🚀 **Sprints & Execution** | [`docs/sprints/`](./sprints/README.md) | **12 Two-Week Sprint Roadmaps** across 6 architectural slices, including sprint plans, [canonical records](./sprints/records/README.md), and [retrospectives](./sprints/retrospectives/README.md). |
| 🛡️ **Platform Audits** | [`docs/audits/`](./audits/README.md) | **Centralized Platform Audits** covering Security (ASVS L2), Architecture (Zero-Clone Law), Compliance (AWS FTR), and Quality Gate sign-offs. |
| 📊 **Test & Operational Reports** | [`docs/reports/`](./reports/README.md) | **Empirical Test Reports** covering E1 Criterion Benchmarks, E2 Integration flows, E3 Fuzzing, E4 Loom Concurrency, and E5 Closeout Packages. |
| ⚖️ **Validation & Records** | [`docs/validation/`](./validation/README.md) | **Authoritative Validation Hub** housing canonical story records (`story-records/`), sprint records (`sprint-records/`), and evidence templates. |

---

## 2. Core Architectural Specifications

The following foundation documents define the core invariants, protocols, and architectural laws of the platform:

1. **[System Architecture (`SYSTEM_ARCHITECTURE.md`)](./SYSTEM_ARCHITECTURE.md)**: 10 Architectural Pillars, AWS serverless microservices, DynamoDB single-table schema, and WatermelonDB delta sync.
2. **[Microkernel & Cloud Portability (`MICROKERNEL_AND_CLOUD_PORTABILITY.md`)](./MICROKERNEL_AND_CLOUD_PORTABILITY.md)**: Gate M1 pure Rust microkernel traits, Axum Tower transport decoupling, and zero-clone invariants.
3. **[Folder Architecture & Locality of Behavior (`FOLDER_ARCHITECTURE.md`)](./FOLDER_ARCHITECTURE.md)**: Gate A2 4-tier behavioral hierarchy (`features -> modules -> behaviours -> [services, designs, logic, types, constants]`).
4. **[SDUI & Localization (`SDUI_AND_LOCALIZATION.md`)](./SDUI_AND_LOCALIZATION.md)**: Server-Driven UI schema, dual-tier catalog search (DynamoDB + OpenSearch), and Arabic/English RTL mirroring.
5. **[Payments, Shipping & Licensing (`PAYMENTS_SHIPPING_AND_LICENSING.md`)](./PAYMENTS_SHIPPING_AND_LICENSING.md)**: Split-COD payment state machine, Bosta courier integration, and 6-mode non-heartbeat licensing engine.
6. **[Deployment & AWS Marketplace (`DEPLOYMENT_AND_AWS_MARKETPLACE.md`)](./DEPLOYMENT_AND_AWS_MARKETPLACE.md)**: AWS CDK v2 IaC, CloudFront OAC, AWS Marketplace FTR compliance, and SaaS metering dimensions.
7. **[Quality Gates Specification (`QUALITY_GATES.md`)](./QUALITY_GATES.md)**: Formal gating contracts (G0–G4 per story, SG0–SG4 per sprint) governing code quality, coverage, and security.
8. **[End-of-Sprint Testing Standards (`SPRINT_TESTING.md`)](./SPRINT_TESTING.md)**: Execution policies for E1 Benchmarks, E2 Integration, E3 Fuzzing, E4 Loom Concurrency, and E5 Closeout.
9. **[Multi-Agent Framework (`AGENT_PROFILES_AND_MULTI_AGENT_FRAMEWORK.md`)](./AGENT_PROFILES_AND_MULTI_AGENT_FRAMEWORK.md)**: Autonomous agent orchestration, load balancing, physical workdir isolation, and 6-layer validation.

---

## 3. Monorepo Structural Blueprint

```
docs/
├── README.md                              # ◄◄ THIS FILE (Master Documentation Portal)
├── SYSTEM_ARCHITECTURE.md                 # 10 Architectural Pillars & Data Flow
├── MICROKERNEL_AND_CLOUD_PORTABILITY.md   # Gate M1 Microkernel Traits & Cloud Decoupling
├── FOLDER_ARCHITECTURE.md                 # Gate A2 Locality of Behavior (LoB) Specification
├── SDUI_AND_LOCALIZATION.md               # Server-Driven UI & Multilingual Standards
├── PAYMENTS_SHIPPING_AND_LICENSING.md     # Split-COD, Bosta, and 6-Mode Licensing Engine
├── DEPLOYMENT_AND_AWS_MARKETPLACE.md      # AWS CDK Stacks, FTR Audit, SaaS Metering
├── QUALITY_GATES.md                       # G0–G4 and SG0–SG4 Quality Gate Definitions
├── SPRINT_TESTING.md                      # E1–E5 Test Execution Policies & Thresholds
├── COMPANY_ROLES_AND_AGENT_PROFILES.md    # 17 Autonomous Company Roles
├── AGENT_PROFILES_AND_MULTI_AGENT_FRAMEWORK.md # Load Balancer, Workdirs, & 6-Layer Governance
│
├── user-stories/                          # ◄◄ FUNCTIONAL SPECIFICATIONS
│   ├── README.md                          # Master User Stories Index & Cross-Module Maps
│   ├── 01-auth-and-onboarding/            # Cognito, OTP, Passkeys, B2B Org Registration
│   ├── 02-storefront-and-catalog/         # SDUI Storefront, Taxonomy, Dual-Tier Search
│   ├── 03-cart-and-checkout/              # Offline Cart, Multi-Vendor Grouping, Checkout Flow
│   ├── 04-payments-and-cod/               # Paymob, Stripe, Full COD, Deposit COD, BTCPay
│   ├── 05-fulfillment-and-shipping/       # Bosta, Aramex/DHL, Shippo, SNS Notifications
│   ├── 06-orders-and-returns/             # Live Order Stepper, History, RMA & Refunds
│   ├── 07-customer-account/               # Profile, Address Book, Notification Preferences
│   ├── 08-webmcp-and-ai/                  # WebMCP Customer Shopping Assistant & Admin Copilot
│   ├── 09-digital-products-and-licensing/ # 6-Mode Cryptographic Licensing Engine
│   ├── 10-b2b-wholesale/                  # Tiered Pricing, MOQ, RFQ Negotiation, LAN Proxy
│   ├── 11-multi-vendor-marketplace/       # Sub-Order Splitting, Escrow Ledger, Vendor Portal
│   ├── 12-admin-and-sdui-studio/          # SDUI Visual Studio, White-Label Mobile Pipeline
│   └── 13-deployment-and-aws-marketplace/ # CDK Packaging, AWS FTR Audit, SaaS Metering
│
├── sprints/                               # ◄◄ SPRINT PLANS & EXECUTION
│   ├── README.md                          # Master Sprints Index & Calendar (Sprints 1.1–6.3)
│   ├── sprint-1.1.md ... sprint-6.3.md    # Formally Approved 12 Sprint Specifications
│   ├── records/                           # Canonical Sprint Operational Records (SPRINT-<id>.md)
│   │   ├── README.md
│   │   └── SPRINT_RECORD_TEMPLATE.md
│   └── retrospectives/                    # Post-Sprint Retrospectives & Process Adaptations
│       ├── README.md
│       └── RETROSPECTIVE_TEMPLATE.md
│
├── audits/                                # ◄◄ PLATFORM AUDITS
│   ├── README.md                          # Master Audits Index & Sprint Audit Matrix
│   ├── AUDIT_RECORD_TEMPLATE.md           # Canonical Audit Record Template
│   ├── 01-security-and-penetration/       # OWASP ASVS L2, Multi-Tenant Fuzzing, KMS
│   ├── 02-architecture-and-zero-clone/    # Rust Zero-Clone Law, Gate M1 Microkernel Purity
│   ├── 03-compliance-and-aws-ftr/         # AWS Marketplace FTR, SaaS Metering Audit
│   └── 04-quality-and-gates/              # Story G0–G4 & Sprint SG0–SG4 Certifications
│
├── reports/                               # ◄◄ TEST & OPERATIONAL REPORTS
│   ├── README.md                          # Master Reports Index & Sprint Reports Matrix
│   ├── REPORT_RECORD_TEMPLATE.md          # Canonical Test Report Record Template
│   ├── 01-benchmarks-and-performance/     # E1 Criterion Benchmarks & P95/P99 Latency
│   ├── 02-integration-and-cross-module/   # E2 Cross-Story Integration & Provider Sandboxes
│   ├── 03-fuzzing-and-adversarial/        # E3 Coverage-Guided Fuzzing (≥600s/target)
│   ├── 04-concurrency-and-loom/           # E4 Loom Shared-State Concurrency Verification
│   └── 05-sprint-closeout-and-rc/         # E5 Sprint Closeout Packages & Release Candidates
│
└── validation/                            # ◄◄ VALIDATION & EVIDENCE BINDINGS
    ├── README.md                          # Validation Hub Guide
    ├── STORY_RECORD_TEMPLATE.md           # Template for Story Operational Records
    ├── STORY_EVIDENCE_TEMPLATE.md         # Template for Story G0–G4 Evidence
    ├── SPRINT_TEST_EVIDENCE_TEMPLATE.md   # Template for Sprint E1–E5 Evidence
    ├── story-records/                     # Canonical Story Operational History (US-<id>.md)
    └── sprint-records/                    # Canonical Sprint Operational History (SPRINT-<id>.md)
```

---

## 4. How to Navigate the Documentation

1. **If you need to understand or implement a feature**:
   - Go to [`docs/user-stories/`](./user-stories/README.md) to locate the relevant functional specification, Gherkin acceptance criteria, and Activity Diagram.
2. **If you need to understand or run a sprint**:
   - Go to [`docs/sprints/`](./sprints/README.md) for the active sprint plan, load balancer agent allocations, and workdir locations.
   - Use [`docs/sprints/records/`](./sprints/records/README.md) to log living sprint progress and handoffs.
3. **If you are performing a security, architectural, or compliance audit**:
   - Go to [`docs/audits/`](./audits/README.md) to review domain requirements, run the recommended scanners, and record findings in [`docs/audits/AUDIT_RECORD_TEMPLATE.md`](./audits/AUDIT_RECORD_TEMPLATE.md).
4. **If you are running tests or compiling closeout evidence**:
   - Go to [`docs/reports/`](./reports/README.md) to log Criterion benchmarks (E1), integration suites (E2), fuzz tests (E3), Loom models (E4), or release candidate closeout packages (E5).
5. **If you are acting as an independent validator or release gatekeeper**:
   - Go to [`docs/validation/`](./validation/README.md) to verify that canonical story records (`US-<id>.md`) and sprint records (`SPRINT-<id>.md`) have complete, tamper-evident evidence before promotion.
