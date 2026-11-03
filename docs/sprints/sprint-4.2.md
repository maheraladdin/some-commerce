# Sprint 4.2 — Escrow Ledger + Vendor Portal + BTCPay + RMA

> **Slice**: v4.0 · **Duration**: Weeks 15–16 · **Story Points**: 34

## Goal

Complete the marketplace with escrow ledger, vendor portal dashboard, BTCPay crypto payments, and RMA return processing.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-11.1.3](../user-stories/11-multi-vendor-marketplace/us-11.1.3-double-entry-escrow-ledger-vendor-payouts.md) | Marketplace | 8 | Escrow ledger + payouts |
| P0 | [US-11.1.4](../user-stories/11-multi-vendor-marketplace/us-11.1.4-vendor-portal-dashboard.md) | Marketplace | 5 | Vendor portal dashboard |
| P0 | [US-6.1.3](../user-stories/06-orders-and-returns/us-6.1.3-return-merchandise-authorization-rma.md) | Orders | 8 | RMA returns |
| P1 | [US-4.1.5](../user-stories/04-payments-and-cod/us-4.1.5-bitcoin-lightning-network-checkout-btcpay-server.md) | Payments | 5 | BTCPay crypto payments |
| P1 | [US-6.1.4](../user-stories/06-orders-and-returns/us-6.1.4-admin-order-management-dashboard.md) | Orders | 5 | Admin order management |
| P2 | [US-3.1.3](../user-stories/03-cart-and-checkout/us-3.1.3-multi-step-checkout-flow.md) | Checkout | 3 | Checkout refinements |

## Definition of Done

- [ ] Escrow holds created on delivery, released after 14 days
- [ ] RMA filed within return window freezes escrow
- [ ] Vendor payout requests work
- [ ] BTCPay Lightning invoice generated + settled
- [ ] Admin order dashboard filters and updates work

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.
