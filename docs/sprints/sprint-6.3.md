# Sprint 6.3 — Hardening, Performance Tuning + Launch Prep

> **Slice**: v6.0 · **Duration**: Weeks 23–24 · **Story Points**: 24

## Goal

Final hardening sprint: security audit, performance tuning, load testing, documentation polish, and production readiness checklist.

## Tasks

| Priority | Task | Points | Description |
|:---------|:-----|:-------|:------------|
| P0 | Security Audit | 5 | OWASP top 10 review, dependency audit, credential rotation |
| P0 | Load Testing | 5 | Artillery/k6 load tests: 1000 concurrent users, sub-50ms p99 search |
| P0 | Database Optimization | 3 | DynamoDB capacity review, GSI optimization, hot partition analysis |
| P1 | CDN Optimization | 3 | CloudFront cache policy tuning, origin shield config |
| P1 | Error Budget Review | 2 | SLO/SLA definition, CloudWatch alarm thresholds |
| P1 | Runbook Creation | 3 | Operational runbooks for incident response |
| P2 | Chaos Engineering | 3 | Simulate Elasticsearch failure, carrier API timeout, KMS outage |

## Production Readiness Checklist

- [ ] All 51 user stories have passed acceptance criteria
- [ ] Zero critical or high security findings
- [ ] p99 search latency < 50ms under load
- [ ] p99 checkout latency < 200ms under load
- [ ] ETag cache hit ratio > 85%
- [ ] Offline WatermelonDB browsing verified on iOS + Android + Web
- [ ] RTL (Arabic) layout verified across all pages
- [ ] COD flows (Full + Deposit) tested with real Bosta sandbox
- [ ] FTR audit passed
- [ ] AWS Marketplace listing live
- [ ] Monitoring dashboards operational
- [ ] Incident response runbook published
- [ ] Team on-call rotation established

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.

---

## Multi-Agent Hardening & Launch Orchestration Plan (6-Layer Governance)

### Company planning → role execution → upward validation

**Status: allocation proposal, not dispatch authorization.** Leadership planning precedes the junior roster; the L1–L6 ladder below is the upward review path. Approve P0–P4 and the company master-plan revision before implementation.

| Stage | Accountable role | Required output |
|:------|:-----------------|:----------------|
| P0 | `chief-technology-officer` | Authorized initiative charter, constraints and success criteria |
| P1 | `product-manager` | Spec Kit requirements, personas, scope and acceptance criteria |
| P2 | `system-architect` | Shared contracts and affected specialist role subplans |
| P3 | `tech-lead` | Reconciled master plan, child manifest, task DAG and review/test capacity |
| P4 | `planning-control-owners-and-cto` | Approved plan baseline and G0/SG0 inputs before implementation |
| EXECUTE | `assigned-role-contributors-and-seniors` | Parallel approved tasks, independent branch reviews and bounded repairs |
| COLLECT | `tech-lead` | Every expected child output and canonical story record reconciled on one candidate |
| VALIDATE | `qa-security-architecture` | Integrated candidate plus E1-E5 sprint evidence and complete action history |
| ACCEPT | `product-manager` | Original charter/AC-to-delivery acceptance dossier |
| RETURN | `chief-technology-officer` | Final Accepted, Changes Required or Blocked decision |

Use the [company plan template](../../.specify/templates/company-plan-template.md). Every task references its master-plan parent and canonical `docs/validation/story-records/US-<id>.md`; log each action/result and next-role receipt there. Collect all expected children, verify the exact assembled candidate and closeout suites, then return product acceptance and the full dossier to CTO. Missing children, action history or required checks block parent acceptance.


Sprint 6.3 is the final hardening and launch verification milestone. Engineering tasks are distributed across the junior-senior agent hierarchy and governed by the 6-Layer Validation Ladder:

### 1. Agent Roster & Load Balancer Allocation
| Worker ID | Profile | Seniority | Specialized Role | Primary Focus & Verification | Dedicated Workdir |
|:----------|:--------|:----------|:-----------------|:-----------------------------|:------------------|
| `sprint-6.3-junior-be-1` | `backend-engineer` | `junior` | `backend-builder` | DynamoDB Capacity, GSI index optimization, hot partition mitigation | `.agents/workspaces/sprint-6.3/sprint-6.3-junior-be-1` |
| `sprint-6.3-junior-be-2` | `backend-engineer` | `junior` | `backend-tester` | Chaos injection tests (KMS outage, carrier timeout, Redis failover) | `.agents/workspaces/sprint-6.3/sprint-6.3-junior-be-2` |
| `sprint-6.3-senior-be-1` | `backend-engineer` | `senior` | `reviewer` | Peer code review, zero-clone borrowing audit, Gate M1 certification | `.agents/workspaces/sprint-6.3/sprint-6.3-senior-be-1` |
| `sprint-6.3-junior-fe-1` | `client-engineer` | `junior` | `client-builder` | CloudFront cache policies, client bundle size optimization (<2.5MB) | `.agents/workspaces/sprint-6.3/sprint-6.3-junior-fe-1` |
| `sprint-6.3-junior-fe-2` | `client-engineer` | `junior` | `client-tester` | Offline reconnect drills, RTL layout stress testing on physical devices | `.agents/workspaces/sprint-6.3/sprint-6.3-junior-fe-2` |
| `sprint-6.3-senior-fe-1` | `client-engineer` | `senior` | `reviewer` | Peer code review, LoB compliance audit, WCAG 2.1 AA certification | `.agents/workspaces/sprint-6.3/sprint-6.3-senior-fe-1` |
| `sprint-6.3-junior-qa-1` | `testing-qa-engineer` | `junior` | `tester` | E2E test runs across mobile & web platforms | `.agents/workspaces/sprint-6.3/sprint-6.3-junior-qa-1` |
| `sprint-6.3-senior-qa-1` | `security-engineer` | `senior` | `auditor` | Final OWASP ASVS L2 audit, penetration testing, Gate M1/A1/A2 sign-off | `.agents/workspaces/sprint-6.3/sprint-6.3-senior-qa-1` |
| `sprint-6.3-tech-lead` | `tech-lead` | `lead` | `lead` | Sprint integration, Gate G1/G4 verification, PR merge coordination | `.agents/workspaces/sprint-6.3/sprint-6.3-tech-lead` |
| `sprint-6.3-product-manager` | `product-manager` | `lead` | `pm` | Product acceptance sign-off across all user stories | `.agents/workspaces/sprint-6.3/sprint-6.3-product-manager` |
| `sprint-6.3-cto` | `chief-technology-officer` | `executive` | `cto` | Executive architectural agreement & final SG4 production release authorization | `.agents/workspaces/sprint-6.3/sprint-6.3-cto` |

### 2. The 6-Layer Governance Ladder
1. **Layer 1 (Junior Execution)**: Implements capacity tuning, chaos suites, and bundle optimization.
2. **Layer 2 (Senior Peer Review)**: Audits code against zero-clone laws, memory limits, and LoB rules.
3. **Layer 3 (Security & Architect Gate)**: Verifies Gate G2 (ASVS L2), Gate A1 (system arch), Gate A2 (folder layout), Gate M1 (microkernel).
4. **Layer 4 (Tech Lead Integration)**: Verifies monorepo regression suites pass with 0 failures.
5. **Layer 5 (Product Manager Acceptance)**: Confirms product readiness across all customer and admin flows.
6. **Layer 6 (CTO Agreement)**: Grants final executive agreement and authorizes production release.

### 3. Sprint Quality Gates Sign-Off (SG0 — SG4)
- [ ] **SG0 (Readiness)**: Hardening backlogs, chaos injection parameters, and benchmark targets approved.
- [ ] **SG1 (Integration)**: Full platform end-to-end regression test suite passes (0 failures).
- [ ] **SG2 (Security Audit)**: Monorepo ASVS L2 verification; zero critical/high CVEs; 0 cross-tenant leaks.
- [ ] **SG3 (Architecture & Gate M1/A1/A2)**: Gate M1 (zero-clone), Gate A1 (system arch), and Gate A2 (folder layout) verified.
- [ ] **SG4 (Production Release Candidate)**: p99 search latency < 50ms under 1,000 concurrent virtual users; production rollback drill verified; **CTO Agreement Granted**.

## End-of-Sprint Test Gate

**Status: Pending — required closeout evidence, not executed test results.** Run this suite at the end of sprint-6.3, on the exact integration/release candidate, before SG4 and CTO review. Earlier story checks remain mandatory. Follow the [sprint closeout policy](../SPRINT_TESTING.md) and attach the [evidence record](../validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md).

- [ ] **E1 — Benchmark tests:** Full platform cold/warm capacity, search/checkout p95/p99, memory, queue age, cache hit rate and resource cost on the agreed launch workload.
- [ ] **E2 — Integration tests:** All accepted stories across web/iOS/Android plus backup/restore, canary rollback, dependency failure, controller restart and complete junior-to-CTO handoffs.
- [ ] **E3 — Fuzz tests:** All maintained security/protocol fuzz targets and saved regressions; extend high-risk auth/payment/license/sync inputs and stateful event-sequence targets.
- [ ] **E4 — Loom concurrency tests:** All maintained Rust Loom models with approved launch bounds, including cache/config, reservation, seat, payout, metering and queue coordination; reject any incomplete exploration.
- [ ] **E5 — Independent closeout review:** QA lead records actual test/target/model counts, candidate and baseline commits, tool/environment versions, performance thresholds/results, corpus/reproducers, Loom bounds/completion and independent reviewer decisions. Missing targets, crashes, regressions, unexplored bounds or unreviewed N/A block acceptance; repairing the candidate invalidates affected results.

At SG0, assign test authors and independent senior QA/security/architecture reviewers; approve workload, benchmark baseline/regression thresholds, fuzz time/memory/input budgets and Loom model bounds. Carry forward affected regression suites. E4 is mandatory for applicable changed or affected Rust shared-state synchronization; only the scope-based N/A procedure in the policy can exclude it, with architecture + QA approval and alternative concurrency evidence. A missing implementation/harness is Pending, never N/A or Pass. Keep this section last, including after sprint-plan regeneration.
