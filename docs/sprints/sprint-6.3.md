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
