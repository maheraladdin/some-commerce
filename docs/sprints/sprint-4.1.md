# Sprint 4.1 — Multi-Vendor Onboarding + Sub-Order Splitting

> **Slice**: v4.0 · **Duration**: Weeks 13–14 · **Story Points**: 30

## Goal

Launch multi-vendor marketplace capabilities with vendor onboarding, RBAC-scoped catalog management, and automatic sub-order splitting at checkout.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-11.1.1](../user-stories/11-multi-vendor-marketplace/README.md#us-1111-vendor-onboarding--rbac-scoped-catalog) | Marketplace | 8 | Vendor onboarding + RBAC |
| P0 | [US-11.1.2](../user-stories/11-multi-vendor-marketplace/README.md#us-1112-automatic-sub-order-splitting-at-checkout) | Marketplace | 8 | Sub-order splitting |
| P0 | [US-3.1.2](../user-stories/03-cart-and-checkout/README.md#us-312-multi-vendor-cart-grouping--shipping-estimation) | Cart | 5 | Multi-vendor cart grouping |
| P1 | [US-4.1.4](../user-stories/04-payments-and-cod/README.md#us-414-admin-payment-gateway-configuration) | Payments | 5 | Gateway configuration UI |
| P2 | [US-8.1.3](../user-stories/08-webmcp-and-ai/README.md#us-813-shared-mcp-engine--bedrock-integration) | WebMCP | 5 | Shared MCP engine |

## Definition of Done

- [ ] Vendor registration → approval → Cognito group works
- [ ] Vendor A cannot access Vendor B's data (RBAC verified)
- [ ] Multi-vendor cart shows per-vendor groups
- [ ] Sub-orders created atomically with TransactWriteItems
- [ ] Each sub-order has independent status + tracking
