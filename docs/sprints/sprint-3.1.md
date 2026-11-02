# Sprint 3.1 — B2B Onboarding + Tiered Pricing + Cross-Border Shipping

> **Slice**: v3.0 · **Duration**: Weeks 9–10 · **Story Points**: 31

## Goal

Launch B2B wholesale capabilities with organization registration, tiered volume pricing, MOQ enforcement, and cross-border express shipping (Aramex + DHL).

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-1.1.4](../user-stories/01-auth-and-onboarding/README.md#us-114-b2b-organization-registration--admin-approval) | Auth | 5 | B2B organization registration |
| P0 | [US-10.1.1](../user-stories/10-b2b-wholesale/README.md#us-1011-b2b-tiered-volume-pricing--moq-enforcement) | B2B | 8 | Tiered pricing + MOQ |
| P0 | [US-10.1.3](../user-stories/10-b2b-wholesale/README.md#us-1013-b2b-custom-elasticsearch-facets) | B2B | 3 | B2B Elasticsearch facets |
| P1 | [US-5.1.2](../user-stories/05-fulfillment-and-shipping/README.md#us-512-cross-border-express-shipping-aramex--dhl) | Fulfillment | 8 | Aramex + DHL cross-border |
| P1 | [US-8.1.1](../user-stories/08-webmcp-and-ai/README.md#us-811-customer-webmcp-shopping-assistant) | WebMCP | 5 | Customer shopping assistant |
| P2 | [US-7.1.2](../user-stories/07-customer-account/README.md#us-712-address-book-management) | Account | 2 | Address book management |

## Definition of Done

- [ ] B2B registration → admin approval → Cognito group flow works
- [ ] Volume tier pricing displays correctly for B2B users
- [ ] MOQ validation blocks below-minimum orders
- [ ] Aramex + DHL rates fetched in parallel
- [ ] Cross-border commercial invoice PDF generated
