# Sprint 4.2 — Escrow Ledger + Vendor Portal + BTCPay + RMA

> **Slice**: v4.0 · **Duration**: Weeks 15–16 · **Story Points**: 34

## Goal

Complete the marketplace with escrow ledger, vendor portal dashboard, BTCPay crypto payments, and RMA return processing.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-11.1.3](../user-stories/11-multi-vendor-marketplace/README.md#us-1113-double-entry-escrow-ledger--vendor-payouts) | Marketplace | 8 | Escrow ledger + payouts |
| P0 | [US-11.1.4](../user-stories/11-multi-vendor-marketplace/README.md#us-1114-vendor-portal-dashboard) | Marketplace | 5 | Vendor portal dashboard |
| P0 | [US-6.1.3](../user-stories/06-orders-and-returns/README.md#us-613-return-merchandise-authorization-rma) | Orders | 8 | RMA returns |
| P1 | [US-4.1.5](../user-stories/04-payments-and-cod/README.md#us-415-bitcoin--lightning-network-checkout-btcpay-server) | Payments | 5 | BTCPay crypto payments |
| P1 | [US-6.1.4](../user-stories/06-orders-and-returns/README.md#us-614-admin-order-management-dashboard) | Orders | 5 | Admin order management |
| P2 | [US-3.1.3](../user-stories/03-cart-and-checkout/README.md#us-313-multi-step-checkout-flow) | Checkout | 3 | Checkout refinements |

## Definition of Done

- [ ] Escrow holds created on delivery, released after 14 days
- [ ] RMA filed within return window freezes escrow
- [ ] Vendor payout requests work
- [ ] BTCPay Lightning invoice generated + settled
- [ ] Admin order dashboard filters and updates work
