# Sprint 1.2 — Cart + Checkout + Payments + Fulfillment

> **Slice**: v1.0 · **Duration**: Weeks 3–4 · **Story Points**: 38

## Goal

Complete the purchasing flow: offline cart, multi-step checkout, all payment methods (Prepaid, Full COD, Deposit COD), Bosta domestic fulfillment, and order tracking. By sprint end, a customer can complete a full purchase.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-3.1.1](../user-stories/03-cart-and-checkout/README.md#us-311-offline-first-cart-with-watermelondb-sync) | Cart | 5 | Offline-first cart with WatermelonDB |
| P0 | [US-3.1.3](../user-stories/03-cart-and-checkout/README.md#us-313-multi-step-checkout-flow) | Checkout | 8 | Multi-step checkout flow |
| P0 | [US-4.1.1](../user-stories/04-payments-and-cod/README.md#us-411-full-prepaid-online-payment-paymob--stripe) | Payments | 5 | Full prepaid (Paymob & Stripe) |
| P0 | [US-4.1.2](../user-stories/04-payments-and-cod/README.md#us-412-full-cash-on-delivery-100-cod) | Payments | 3 | Full Cash on Delivery (100% COD) |
| P0 | [US-4.1.3](../user-stories/04-payments-and-cod/README.md#us-413-upfront-deposit--split-cash-on-delivery-deposit_cod) | Payments | 5 | Deposit + Split COD |
| P1 | [US-5.1.1](../user-stories/05-fulfillment-and-shipping/README.md#us-511-domestic-shipping-via-bosta-with-cod-collection) | Fulfillment | 5 | Bosta domestic shipping |
| P1 | [US-6.1.1](../user-stories/06-orders-and-returns/README.md#us-611-real-time-order-tracking--live-status-timeline) | Orders | 3 | Order tracking timeline |
| P1 | [US-3.1.4](../user-stories/03-cart-and-checkout/README.md#us-314-localized-address-management) | Cart | 2 | Localized address management |
| P2 | [US-5.1.4](../user-stories/05-fulfillment-and-shipping/README.md#us-514-localized-sns-push--sms-notifications-at-every-milestone) | Fulfillment | 2 | Localized SNS notifications |

## Dependencies

```mermaid
flowchart LR
    Sprint_1_1["Sprint 1.1 Auth + Storefront"] --> US_3_1_1
    US_3_1_1 --> US_3_1_3
    US_3_1_3 --> US_4_1_1 & US_4_1_2 & US_4_1_3
    US_4_1_1 & US_4_1_2 & US_4_1_3 --> US_5_1_1
    US_5_1_1 --> US_6_1_1
    US_3_1_4 --> US_3_1_3
```

## Key Deliverables

- SplitCodEngine fully operational (FULL_COD, DEPOSIT_COD, PREPAID)
- KMS vault with encrypted gateway credentials
- Bosta AWB auto-booking via fulfillment-worker
- End-to-end checkout test (product → cart → pay → shipped → delivered)

## Definition of Done

- [ ] Full checkout E2E test passes for all 3 payment modes
- [ ] COD surcharge correctly applied per zone
- [ ] Bosta AWB label generated and stored in S3
- [ ] SNS notifications sent in Arabic for ar-EG locale
- [ ] Webhook idempotency verified (duplicate rejection)
