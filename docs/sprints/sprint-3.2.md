# Sprint 3.2 — RFQ Negotiation + Net-Terms + LAN License Proxy

> **Slice**: v3.0 · **Duration**: Weeks 11–12 · **Story Points**: 32

## Goal

Complete B2B wholesale with durable RFQ negotiation, net-terms invoicing (NET_30/NET_60), and on-premise LAN license proxy for enterprise deployments.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-10.1.2](../user-stories/10-b2b-wholesale/us-10.1.2-durable-rfq-negotiation-net-terms-invoicing.md) | B2B | 13 | RFQ negotiation + net-terms |
| P0 | [US-10.1.4](../user-stories/10-b2b-wholesale/us-10.1.4-b2b-on-premise-lan-license-proxy.md) | B2B | 8 | LAN license proxy |
| P1 | [US-5.1.3](../user-stories/05-fulfillment-and-shipping/us-5.1.3-global-multi-carrier-aggregation-shippo-easypost.md) | Fulfillment | 5 | Shippo/EasyPost aggregation |
| P1 | [US-8.1.2](../user-stories/08-webmcp-and-ai/us-8.1.2-admin-webmcp-store-copilot.md) | WebMCP | 3 | Admin copilot |
| P2 | [US-6.1.2](../user-stories/06-orders-and-returns/us-6.1.2-customer-order-history-with-filtering.md) | Orders | 3 | Order history |

## Definition of Done

- [ ] RFQ durable state machine with 14-day timeout works
- [ ] Counter-quote → PO approval flow complete
- [ ] Net-30 timer with SNS reminders works
- [ ] LAN proxy container runs offline with master lease
- [ ] Seat checkout/release within pool limits

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.
