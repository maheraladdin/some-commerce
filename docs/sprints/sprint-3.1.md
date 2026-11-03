# Sprint 3.1 — B2B Onboarding + Tiered Pricing + Cross-Border Shipping

> **Slice**: v3.0 · **Duration**: Weeks 9–10 · **Story Points**: 31

## Goal

Launch B2B wholesale capabilities with organization registration, tiered volume pricing, MOQ enforcement, and cross-border express shipping (Aramex + DHL).

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-1.1.4](../user-stories/01-auth-and-onboarding/us-1.1.4-b2b-organization-registration-admin-approval.md) | Auth | 5 | B2B organization registration |
| P0 | [US-10.1.1](../user-stories/10-b2b-wholesale/us-10.1.1-b2b-tiered-volume-pricing-moq-enforcement.md) | B2B | 8 | Tiered pricing + MOQ |
| P0 | [US-10.1.3](../user-stories/10-b2b-wholesale/us-10.1.3-b2b-custom-elasticsearch-facets.md) | B2B | 3 | B2B Elasticsearch facets |
| P1 | [US-5.1.2](../user-stories/05-fulfillment-and-shipping/us-5.1.2-cross-border-express-shipping-aramex-dhl.md) | Fulfillment | 8 | Aramex + DHL cross-border |
| P1 | [US-8.1.1](../user-stories/08-webmcp-and-ai/us-8.1.1-customer-webmcp-shopping-assistant.md) | WebMCP | 5 | Customer shopping assistant |
| P2 | [US-7.1.2](../user-stories/07-customer-account/us-7.1.2-address-book-management.md) | Account | 2 | Address book management |

## Definition of Done

- [ ] B2B registration → admin approval → Cognito group flow works
- [ ] Volume tier pricing displays correctly for B2B users
- [ ] MOQ validation blocks below-minimum orders
- [ ] Aramex + DHL rates fetched in parallel
- [ ] Cross-border commercial invoice PDF generated

## Mandatory Story Validation

- [ ] Every story delivered in this sprint passes [G0–G4](../QUALITY_GATES.md), including its tailored test, security and architecture checks; attach a [story evidence record](../validation/STORY_EVIDENCE_TEMPLATE.md).
- [ ] Resolve relevant [design and dependency blockers](../DOCS_STRESS_TEST.md) before commitment/release. Partial story work remains In Progress; P1/P2 priority does not exempt it from gates.
- [ ] Non-story tasks that change production behavior use the same gates and have an accountable owner and evidence record.
