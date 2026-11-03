# Sprint 4.1 — Multi-Vendor Onboarding + Sub-Order Splitting

> **Slice**: v4.0 · **Duration**: Weeks 13–14 · **Story Points**: 31

## Goal

Launch multi-vendor marketplace capabilities with vendor onboarding, RBAC-scoped catalog management, and automatic sub-order splitting at checkout.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-11.1.1](../user-stories/11-multi-vendor-marketplace/us-11.1.1-vendor-onboarding-rbac-scoped-catalog.md) | Marketplace | 8 | Vendor onboarding + RBAC |
| P0 | [US-11.1.2](../user-stories/11-multi-vendor-marketplace/us-11.1.2-automatic-sub-order-splitting-at-checkout.md) | Marketplace | 8 | Sub-order splitting |
| P0 | [US-3.1.2](../user-stories/03-cart-and-checkout/us-3.1.2-multi-vendor-cart-grouping-shipping-estimation.md) | Cart | 5 | Multi-vendor cart grouping |
| P1 | [US-4.1.4](../user-stories/04-payments-and-cod/us-4.1.4-admin-payment-gateway-configuration.md) | Payments | 5 | Gateway configuration UI |
| P2 | [US-8.1.3](../user-stories/08-webmcp-and-ai/us-8.1.3-shared-mcp-engine-bedrock-integration.md) | WebMCP | 5 | Shared MCP engine |

## Definition of Done

- [ ] Vendor registration → approval → Cognito group works
- [ ] Vendor A cannot access Vendor B's data (RBAC verified)
- [ ] Multi-vendor cart shows per-vendor groups
- [ ] Sub-orders created atomically with TransactWriteItems
- [ ] Each sub-order has independent status + tracking

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.
