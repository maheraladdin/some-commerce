# Sprint 2.2 — Licensing Modes 5–6 + SDKs + License Vault UI

> **Slice**: v2.0 · **Duration**: Weeks 7–8 · **Story Points**: 26

## Goal

Complete the licensing engine with release gating and push revocation, publish client SDKs (Rust + TypeScript), and build the license vault UI.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-9.1.2](../user-stories/09-digital-products-and-licensing/us-9.1.2-6-mode-non-heartbeat-licensing-engine.md) | Licensing | 8 | Licensing Modes 5–6 (Release Gating, Push Revocation) |
| P0 | [US-9.1.3](../user-stories/09-digital-products-and-licensing/us-9.1.3-client-verification-sdks.md) | Licensing | 5 | Client verification SDKs |
| P0 | [US-9.1.4](../user-stories/09-digital-products-and-licensing/us-9.1.4-digital-license-vault-ui.md) | Licensing | 5 | License vault UI |
| P1 | [US-7.1.4](../user-stories/07-customer-account/us-7.1.4-wishlist.md) | Account | 5 | Wishlist functionality |
| P2 | [US-7.1.3](../user-stories/07-customer-account/us-7.1.3-notification-preferences.md) | Account | 3 | Notification preferences |

## Definition of Done

- [ ] Mode 5: Release gating blocks updates past entitlement date
- [ ] Mode 6: SNS silent push revokes license on device
- [ ] Rust SDK published with documentation
- [ ] TypeScript SDK published with documentation
- [ ] License vault UI shows all purchased licenses
- [ ] QR scanner works on iOS and Android

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.
