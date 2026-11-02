# Sprint 2.2 — Licensing Modes 5–6 + SDKs + License Vault UI

> **Slice**: v2.0 · **Duration**: Weeks 7–8 · **Story Points**: 26

## Goal

Complete the licensing engine with release gating and push revocation, publish client SDKs (Rust + TypeScript), and build the license vault UI.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-9.1.2](../user-stories/09-digital-products-and-licensing/README.md#us-912-6-mode-non-heartbeat-licensing-engine) | Licensing | 8 | Licensing Modes 5–6 (Release Gating, Push Revocation) |
| P0 | [US-9.1.3](../user-stories/09-digital-products-and-licensing/README.md#us-913-client-verification-sdks) | Licensing | 5 | Client verification SDKs |
| P0 | [US-9.1.4](../user-stories/09-digital-products-and-licensing/README.md#us-914-digital-license-vault-ui) | Licensing | 5 | License vault UI |
| P1 | [US-7.1.4](../user-stories/07-customer-account/README.md#us-714-wishlist) | Account | 5 | Wishlist functionality |
| P2 | [US-7.1.3](../user-stories/07-customer-account/README.md#us-713-notification-preferences) | Account | 3 | Notification preferences |

## Definition of Done

- [ ] Mode 5: Release gating blocks updates past entitlement date
- [ ] Mode 6: SNS silent push revokes license on device
- [ ] Rust SDK published with documentation
- [ ] TypeScript SDK published with documentation
- [ ] License vault UI shows all purchased licenses
- [ ] QR scanner works on iOS and Android
