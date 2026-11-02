# Sprint 1.1 — Auth + Storefront + Customer Foundation

> **Slice**: v1.0 · **Duration**: Weeks 1–2 · **Story Points**: 34

## Goal

Stand up the authentication layer, SDUI storefront rendering, catalog search, and customer account foundation. By sprint end, a customer can sign in, browse the catalog, search with facets, view product details, and manage their profile.

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-1.1.1](../user-stories/01-auth-and-onboarding/README.md#us-111-phone-otp-passwordless-sign-in) | Auth | 5 | Phone OTP passwordless sign-in |
| P0 | [US-1.1.2](../user-stories/01-auth-and-onboarding/README.md#us-112-emailpassword--passkey-webauthn-sign-in) | Auth | 5 | Email/Password & Passkey sign-in |
| P0 | [US-1.1.3](../user-stories/01-auth-and-onboarding/README.md#us-113-social-oidc-sign-in-google--apple) | Auth | 3 | Social OIDC sign-in (Google & Apple) |
| P0 | [US-2.1.1](../user-stories/02-storefront-and-catalog/README.md#us-211-multilingual-sdui-storefront-with-instant-watermelondb-rendering) | Storefront | 8 | SDUI storefront with WatermelonDB |
| P1 | [US-2.1.2](../user-stories/02-storefront-and-catalog/README.md#us-212-unlimited-n-level-category-taxonomy--brand-management) | Storefront | 5 | N-Level taxonomy & brands |
| P1 | [US-2.1.4](../user-stories/02-storefront-and-catalog/README.md#us-214-dual-tier-catalog-search-with-nested-faceted-filtration) | Storefront | 5 | Dual-tier search + facets |
| P1 | [US-7.1.1](../user-stories/07-customer-account/README.md#us-711-customer-profile-management) | Account | 3 | Customer profile management |

## Dependencies

```mermaid
flowchart LR
    US_1_1_1 & US_1_1_2 & US_1_1_3 --> US_7_1_1
    US_2_1_2 --> US_2_1_4
    US_2_1_1 --> US_2_1_4
```

## Infrastructure Setup (Sprint 0 pre-work)

- [x] AWS Account + CDK bootstrap
- [x] Cognito User Pool + Identity Pool
- [x] DynamoDB table with GSI1 + GSI2
- [x] ElastiCache Serverless for Redis
- [x] Elasticsearch dev domain
- [x] S3 buckets (sdui-assets, digital-vault)

## Definition of Done

- [ ] All test cases for P0 stories pass
- [ ] ETag-based caching verified (304 responses)
- [ ] WatermelonDB offline browsing works
- [ ] RTL (ar-EG) and LTR (en-US) layouts validated
- [ ] Code review completed for all PRs
- [ ] No critical security findings
