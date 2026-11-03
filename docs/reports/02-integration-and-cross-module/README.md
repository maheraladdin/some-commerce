# Report Category 02: Integration & Cross-Module Tests (E2)

> **Test Category**: **E2 Integration Tests**  
> **Toolchain**: `cargo test --test integration_*` · Real DynamoDB Local / Testcontainers · EventBridge sandbox  
> **Governing Quality Gate**: **Gate G1**, **Gate G4**, **SG1**, **SG4**  
> **Accountable Roles**: `testing-qa-engineer` / `senior-client-engineer` / `senior-backend-engineer`

---

## 1. Overview & Methodology

The Integration & Cross-Module report category covers complete multi-module journeys that verify real component boundaries, transactional rollbacks, and external sandbox interactions, as specified in [`docs/SPRINT_TESTING.md`](../../SPRINT_TESTING.md).

### Key Integration Test Focus Areas:
- **Real Component Boundaries**: Verified against actual DynamoDB tables, Redis caches, and SNS dispatchers (mocks alone cannot satisfy integration acceptance).
- **Fault, Race & Recovery Invariants**: Verification of double-spend prevention, network timeout recovery, idempotent webhook replay, and compensation transactions.
- **Client-to-Backend End-to-End Handshakes**: Verification of Expo Router requests (`fetchWithEtag`), WatermelonDB delta sync (`/v1/sync/pull` and `push`), and offline-to-online reconnection flows.

---

## 2. Standard Integration Test Execution Command

```bash
# Run isolated integration suites against local test containers
TEST_ENV=isolated cargo test --test '*' -- --test-threads=4

# Run mobile client E2E integration suites (Maestro / Detox)
maestro test .maestro/checkout_flow.yaml
```

---

## 3. Sprint Integration Report Catalog

| Report File | Sprint | Journey & Flow Tested | Status |
|:------------|:-------|:----------------------|:-------|
| `REPORT-INT-sprint-1.1-auth-storefront-sync.md` | Sprint 1.1 | Sign-in → scoped catalog browse → profile update → delta sync | Pending |
| `REPORT-INT-sprint-1.2-checkout-bosta-paymob.md` | Sprint 1.2 | Offline cart → split COD checkout → Bosta AWB book → webhook | Pending |
| `REPORT-INT-sprint-2.1-digital-download-crl.md` | Sprint 2.1 | S3 presigned asset upload → purchase → download → CRL revocation | Pending |
| `REPORT-INT-sprint-2.2-sdk-vault-sync.md` | Sprint 2.2 | Golden vector evaluation → vault offline sync → QR activation | Pending |
| `REPORT-INT-sprint-3.1-b2b-onboarding-moq.md` | Sprint 3.1 | B2B register → admin approval → MOQ cart → cross-border invoice | Pending |
| `REPORT-INT-sprint-3.2-rfq-lan-negotiation.md` | Sprint 3.2 | RFQ counter-offer → PO generation → LAN proxy seat failover | Pending |
| `REPORT-INT-sprint-4.1-vendor-suborders.md` | Sprint 4.1 | Vendor onboarding → product listing → multi-vendor sub-orders | Pending |
| `REPORT-INT-sprint-4.2-escrow-payout-rma.md` | Sprint 4.2 | Delivery confirmation → escrow freeze → RMA return & refund | Pending |
| `REPORT-INT-sprint-5.1-deploy-metering.md` | Sprint 5.1 | Fresh CDK deploy → tenant onboarding → AWS metering delivery | Pending |
| `REPORT-INT-sprint-6.1-sdui-studio-publish.md` | Sprint 6.1 | Studio visual draft → live preview → atomic publish cutover | Pending |
| `REPORT-INT-sprint-6.2-whitelabel-pipeline.md` | Sprint 6.2 | Brand config submit → isolated cloud build → signed app bundle | Pending |
| `REPORT-INT-sprint-6.3-full-monorepo-e2e.md` | Sprint 6.3 | Comprehensive full-system smoke test across web, iOS, and Android | Pending |

---

## 4. How to Record an Integration Report

1. Copy `../REPORT_RECORD_TEMPLATE.md` to `docs/reports/02-integration-and-cross-module/REPORT-INT-<sprint>-<topic>.md`
2. Execute the cross-module integration harnesses.
3. Record test counts, component boundaries verified, and assertions validated.
4. Obtain sign-off from `testing-qa-engineer`.
