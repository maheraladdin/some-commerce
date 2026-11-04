# Master Framework Folder Architecture & Behavioral Colocation Specification

## 1. Architectural Philosophy: Locality of Behavior (LoB) Inside Frameworks

`some-commerce` enforces a strict, maintainable folder architecture centered around **Vertical Slices** and the **Locality of Behavior (LoB)** principle.

> [!IMPORTANT]
> **Framework Scoping Law**: `features/` is **NEVER** placed at the repository root.
> In a fullstack modern monorepo, the repository root manages workspace configurations (Turborepo, Cargo Workspace, AWS CDK). The behavioral hierarchy (`features -> modules -> behaviours -> [services, designs, logic, types, constants]`) lives **directly inside the framework targets**:
> 1. **Client Framework**: Universal Expo SDK 58 (React 19 + React Native 0.88 + Expo Router v5) under `apps/storefront/src/features/`.
> 2. **Backend Framework**: Rust 2024 Cargo Lambda + Axum 0.8 workspace under `backend/src/features/` (or `crates/<crate>/src/features/`).

---

## 2. Monorepo Structural Layout

```
some-commerce/
├── apps/
│   ├── storefront/                      # Universal Expo SDK 58 Storefront (iOS, Android, Web)
│   │   ├── dist/                        # Static site build output (deployed via AWS CDK & CloudFront)
│   │   ├── app/                         # Customer Expo Router v5 route entrypoints
│   │   └── src/
│   │       ├── shared/                  # Client-wide shared UI tokens, global providers, client utilities
│   │       └── features/                # ◄◄ STOREFRONT BEHAVIORAL HIERARCHY
│   │           └── <feature-name>/
│   │               ├── _shared/         # Shared across modules in this feature
│   │               └── modules/
│   │                   └── <module-name>/
│   │                       ├── _shared/ # Shared across behaviours in this module
│   │                       └── behaviours/
│   │                           └── <behaviour-name>/
│   │                               ├── services/    # TanStack Query hooks, WatermelonDB queries, API fetchers
│   │                               ├── designs/     # @expo/ui components, screens, SDUI widget blocks
│   │                               ├── logic/       # Headless custom hooks, local state machines, validation
│   │                               ├── types/       # TypeScript interfaces, DTOs, Zod schemas
│   │                               └── constants/   # Route URLs, query keys, error strings, action tags
│   │
│   └── dashboard/                       # Admin & Vendor Portal Web Application (Static SPA)
│       ├── dist/                        # Static site build output (deployed via AWS CDK & CloudFront)
│       ├── app/                         # Admin & vendor routes (/admin/sdui-studio, /vendor/dashboard)
│       └── src/
│           ├── shared/
│           └── features/                # ◄◄ DASHBOARD BEHAVIORAL HIERARCHY
│               ├── administration-and-operations/
│               └── commercial-models/
│
├── backend/                             # Cargo Lambda + Axum 0.8 Rust Workspace
│   ├── Cargo.toml                       # Root Cargo workspace manifest
│   ├── crates/                          # Shared Rust domain crates (kernel-core, db-schema, etc.)
│   └── bins/                            # 5-binary Cargo Lambda services
│       ├── storefront-sdui-api/
│       ├── checkout-webhooks-api/
│       ├── admin-vendor-api/
│       ├── fulfillment-worker/
│       └── durable-orchestrator/
│           └── src/
│               ├── shared/              # Service-wide shared middleware, extractors, DB pools
│               └── features/            # ◄◄ BACKEND BEHAVIORAL HIERARCHY
│                   └── <feature-name>/
│                       ├── _shared/     # Shared domain traits across modules in this feature
│                       └── modules/
│                           └── <module-name>/
│                               ├── _shared/
│                               └── behaviours/
│                                   └── <behaviour-name>/
│                                       ├── services/   # DynamoDB queries, KMS crypto, external vendor calls
│                                       ├── logic/      # Pure business rules, state transitions, calculations
│                                       ├── types/      # Rust DTOs, request/response payloads, domain models
│                                       └── constants/  # Endpoint paths, timeout limits, error codes
│
├── packages/                            # Shared Monorepo TypeScript Packages
│   ├── domain-hooks/                    # Headless cross-framework hooks
│   ├── ui-primitives/                   # Platform-agnostic design system primitives
│   └── watermelon-db/                   # Client-first SQLite/IndexedDB schemas and delta sync
│
├── infra/                               # AWS CDK v2 Cloud Infrastructure Stacks
├── docs/                                # Master specifications, user stories, sprint roadmaps
└── .specify/                            # GitHub Spec Kit governance, constitution, and templates
```

---

## 3. The 4 Sharing & Promotion Tiers Inside Each Framework

To prevent premature abstraction while keeping the codebase DRY when true reuse occurs, code follows a strict promotion hierarchy inside each framework:

| Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Promotion Rule |
| :--- | :--- | :--- | :--- |
| **Tier 1: Behaviour-Local** | `.../behaviours/<B>/[services, designs, logic, types, constants]` | `.../behaviours/<B>/[services, logic, types, constants]` | **Default**. Asset is needed only by this specific behavior. |
| **Tier 2: Module-Shared** | `.../modules/<M>/_shared/[services, designs, logic, types, constants]` | `.../modules/<M>/_shared/[services, logic, types, constants]` | Asset is actively shared by $\ge 2$ behaviours within the same module. |
| **Tier 3: Feature-Shared** | `.../features/<F>/_shared/[services, designs, logic, types, constants]` | `.../features/<F>/_shared/[services, logic, types, constants]` | Asset is actively shared by $\ge 2$ modules within the same feature. |
| **Tier 4: Framework-Shared** | `apps/storefront/src/shared/` | `backend/crates/<shared-crate>/` or `shared/` | Universal cross-cutting infrastructure, microkernel traits, or transport middleware. |

---

## 4. Framework Anatomy: Frontend vs Backend Colocation

### Frontend (Expo SDK 58 + React 19 + React Native 0.88)
* `services/`: API callers (`fetchWithEtag`), TanStack Query query/mutation definitions, local WatermelonDB query observers.
* `designs/`: Platform-adaptive UI components (`@expo/ui` SwiftUI/Jetpack Compose primitives on mobile, semantic HTML5/Tailwind v4 on web), screen views, SDUI block renderers.
* `logic/`: Headless custom React hooks (e.g. `usePhoneOtpAuth`, `useSplitCodCheckout`), local form state machines, UI validators.
* `types/`: TypeScript DTO schemas, navigation route param types, UI component prop interfaces.
* `constants/`: Route path templates, query cache keys, regex phone masks, countdown durations.

### Backend (Rust 2024 Cargo Lambda + Axum 0.8)
* `services/`: Axum Tower handlers, DynamoDB single-table repositories, SNS dispatcher, KMS crypto adapters. *(Note: `designs/` is omitted on backend as Axum does not render visual UI)*.
* `logic/`: Pure domain arithmetic (Money minor-unit calculation), state machine guards, authorization policy evaluators.
* `types/`: Strongly typed Rust models (`#[derive(Serialize, Deserialize)]`), request/response DTOs, domain identifiers (`TenantId`, `OrderId`).
* `constants/`: API route URL constants, DynamoDB partition prefixes (`PK = TENANT#...`), rate limit quotas, error code enums.

---

## 5. Master Feature & Module Taxonomy (Inside Frameworks)

The 6 Features, 13 Modules, and 51 Behaviours reside consistently inside both frameworks:

```
features/
├── identity-and-access/
│   ├── _shared/
│   └── modules/
│       ├── auth-and-onboarding/
│       │   ├── _shared/
│       │   └── behaviours/
│       │       ├── phone-otp-sign-in/                     # US-1.1.1
│       │       ├── passkey-webauthn-sign-in/              # US-1.1.2
│       │       ├── social-oidc-sign-in/                   # US-1.1.3
│       │       └── b2b-org-registration/                  # US-1.1.4
│       └── customer-account/
│           ├── _shared/
│           └── behaviours/
│               ├── customer-profile-management/           # US-7.1.1
│               ├── address-book-management/               # US-7.1.2
│               ├── notification-preferences/              # US-7.1.3
│               └── customer-wishlist/                     # US-7.1.4
│
├── catalog-and-discovery/
│   ├── _shared/
│   └── modules/
│       ├── storefront-and-catalog/
│       │   ├── _shared/
│       │   └── behaviours/
│       │       ├── instant-sdui-storefront/               # US-2.1.1
│       │       ├── n-level-taxonomy/                      # US-2.1.2
│       │       ├── dynamic-product-properties/            # US-2.1.3
│       │       ├── dual-tier-search/                      # US-2.1.4
│       │       └── product-detail-configurator/           # US-2.1.5
│       └── webmcp-and-ai/
│           ├── _shared/
│           └── behaviours/
│               ├── customer-shopping-assistant/           # US-8.1.1
│               ├── admin-store-copilot/                   # US-8.1.2
│               └── shared-mcp-engine/                     # US-8.1.3
│
├── order-processing-and-commerce/
│   ├── _shared/
│   └── modules/
│       ├── cart-and-checkout/
│       │   ├── _shared/
│       │   └── behaviours/
│       │       ├── offline-cart-sync/                     # US-3.1.1
│       │       ├── multi-vendor-cart-grouping/            # US-3.1.2
│       │       ├── multi-step-checkout/                   # US-3.1.3
│       │       └── localized-address-management/          # US-3.1.4
│       ├── payments-and-cod/
│       │   ├── _shared/
│       │   └── behaviours/
│       │       ├── prepaid-card-payment/                  # US-4.1.1
│       │       ├── full-cash-on-delivery/                 # US-4.1.2
│       │       ├── split-deposit-cod/                     # US-4.1.3
│       │       ├── payment-gateway-config/                # US-4.1.4
│       │       └── lightning-bitcoin-payment/             # US-4.1.5
│       └── orders-and-returns/
│           ├── _shared/
│           └── behaviours/
│               ├── realtime-order-tracking/               # US-6.1.1
│               ├── customer-order-history/                # US-6.1.2
│               ├── rma-returns-management/                # US-6.1.3
│               └── admin-order-management/                # US-6.1.4
│
├── logistics-and-fulfillment/
│   ├── _shared/
│   └── modules/
│       └── fulfillment-and-shipping/
│           ├── _shared/
│           └── behaviours/
│               ├── bosta-domestic-shipping/               # US-5.1.1
│               ├── cross-border-shipping/                 # US-5.1.2
│               ├── carrier-aggregation/                   # US-5.1.3
│               └── milestone-notifications/               # US-5.1.4
│
├── commercial-models/
│   ├── _shared/
│   └── modules/
│       ├── digital-products-and-licensing/
│       │   ├── _shared/
│       │   └── behaviours/
│       │       ├── digital-asset-delivery/                # US-9.1.1
│       │       ├── six-mode-licensing-engine/             # US-9.1.2
│       │       ├── client-verification-sdks/              # US-9.1.3
│       │       └── license-vault-ui/                      # US-9.1.4
│       ├── b2b-wholesale/
│       │   ├── _shared/
│       │   └── behaviours/
│       │       ├── b2b-tiered-pricing-moq/                # US-10.1.1
│       │       ├── b2b-rfq-invoicing/                     # US-10.1.2
│       │       ├── b2b-catalog-facets/                    # US-10.1.3
│       │       └── b2b-lan-license-proxy/                 # US-10.1.4
│       └── multi-vendor-marketplace/
│           ├── _shared/
│           └── behaviours/
│               ├── vendor-onboarding-catalog/             # US-11.1.1
│               ├── sub-order-splitting/                   # US-11.1.2
│               ├── escrow-ledger-payouts/                 # US-11.1.3
│               └── vendor-portal-dashboard/               # US-11.1.4
│
└── administration-and-operations/
    ├── _shared/
    └── modules/
        ├── admin-and-sdui-studio/
        │   ├── _shared/
        │   └── behaviours/
        │       ├── visual-sdui-studio/                    # US-12.1.1
        │       ├── dual-edition-orchestration/            # US-12.1.2
        │       └── whitelabel-mobile-pipeline/            # US-12.1.3
        └── deployment-and-aws-marketplace/
            ├── _shared/
            └── behaviours/
                ├── cdk-stack-packaging/                   # US-13.1.1
                ├── marketplace-ftr-compliance/            # US-13.1.2
                └── saas-metering-billing/                 # US-13.1.3
```
