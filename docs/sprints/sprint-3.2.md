# Sprint 3.2 — RFQ Negotiation + Net-Terms + LAN License Proxy

> **Slice**: v3.0 · **Duration**: Weeks 11–12 · **Story Points**: 32

## Goal

Complete B2B wholesale with durable RFQ negotiation, net-terms invoicing (NET_30/NET_60), and on-premise LAN license proxy for enterprise deployments.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-10.1.2](../user-stories/10-b2b-wholesale/README.md#us-1012-durable-rfq-negotiation--net-terms-invoicing) | B2B | 13 | RFQ negotiation + net-terms |
| P0 | [US-10.1.4](../user-stories/10-b2b-wholesale/README.md#us-1014-b2b-on-premise-lan-license-proxy) | B2B | 8 | LAN license proxy |
| P1 | [US-5.1.3](../user-stories/05-fulfillment-and-shipping/README.md#us-513-global-multi-carrier-aggregation-shippo--easypost) | Fulfillment | 5 | Shippo/EasyPost aggregation |
| P1 | [US-8.1.2](../user-stories/08-webmcp-and-ai/README.md#us-812-admin-webmcp-store-copilot) | WebMCP | 3 | Admin copilot |
| P2 | [US-6.1.2](../user-stories/06-orders-and-returns/README.md#us-612-customer-order-history-with-filtering) | Orders | 3 | Order history |

## Definition of Done

- [ ] RFQ durable state machine with 14-day timeout works
- [ ] Counter-quote → PO approval flow complete
- [ ] Net-30 timer with SNS reminders works
- [ ] LAN proxy container runs offline with master lease
- [ ] Seat checkout/release within pool limits
