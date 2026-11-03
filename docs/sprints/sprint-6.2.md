# Sprint 6.2 — White-Label Pipeline + Marketplace Launch

> **Slice**: v6.0 · **Duration**: Weeks 21–22 · **Story Points**: 26

## Goal

Complete the white-label mobile build pipeline and finalize the AWS Marketplace listing for production launch.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-12.1.3](../user-stories/12-admin-and-sdui-studio/us-12.1.3-white-label-mobile-build-pipeline.md) | Admin | 8 | White-label mobile pipeline |
| P0 | Marketplace Production Launch | Deployment | 8 | Final Marketplace submission + go-live |
| P1 | Integration test suite | QA | 5 | End-to-end integration tests |
| P1 | Documentation completion | Docs | 3 | API docs, user guides, onboarding wizard |
| P2 | Performance benchmarks | Observability | 2 | Load test all critical paths |

## Definition of Done

- [ ] White-label build produces working .ipa and .apk
- [ ] Custom branding (icon, splash, colors) applied correctly
- [ ] AWS Marketplace listing approved and live
- [ ] All integration tests pass (auth → checkout → fulfillment → payout)
- [ ] API documentation published

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.
