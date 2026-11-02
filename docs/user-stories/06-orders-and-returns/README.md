# Module 06: Orders & Returns

> **Slice**: v1.0 / v4.0 · **Sprints**: 1.2, 4.2 · **Stories**: US-6.1.1 – US-6.1.4

## Overview

Covers order tracking, order history, Return Merchandise Authorization (RMA), and refund processing.

## Pages

| Page Route | Access | Primary Hook |
|:-----------|:-------|:-------------|
| `/[locale]/orders/[order_id]/confirmation` | Auth | `useOrderLiveTracker` |
| `/[locale]/account/orders` | Auth | `useOrderHistory` |
| `/[locale]/admin/orders` | STORE_ADMIN | `useAdminOrderManagement` |

## API Endpoints

| Method | Endpoint | Lambda | Description |
|:-------|:---------|:-------|:------------|
| GET | `/v1/orders/:id` | `storefront-sdui-api` | Order detail with tracking |
| GET | `/v1/orders` | `storefront-sdui-api` | Customer order history |
| POST | `/v1/orders/:id/rma` | `durable-orchestrator` | Initiate RMA return |
| POST | `/v1/orders/:id/refund` | `checkout-webhooks-api` | Process refund |
| GET | `/v1/admin/orders` | `admin-vendor-api` | Admin order list + filters |
| PUT | `/v1/admin/orders/:id/status` | `admin-vendor-api` | Admin update order status |

---

## US-6.1.1: Real-Time Order Tracking & Live Status Timeline

**As a** Customer who has placed an order,  
**I want to** track my order in real-time with a visual status timeline and live carrier tracking map,  
**So that** I know exactly where my package is and when to expect delivery.

### Acceptance Criteria

```gherkin
Feature: Order Tracking

  Scenario: View order confirmation with timeline
    Given the customer opens "/[locale]/orders/ord_1/confirmation"
    Then a status timeline shows all milestones (Confirmed → Packed → Shipped → Delivered)
    And the current status is highlighted
    And for COD orders, the cash balance to prepare is prominently shown

  Scenario: Live carrier tracking
    Given the order has a Bosta AWB number
    Then a live tracking card shows the carrier's real-time status
    And the tracking URL deep-links to Bosta's tracking page

  Scenario: Order with multiple sub-orders
    Given a multi-vendor order has 3 sub-orders
    Then each sub-order shows its own timeline and tracking info
    And sub-orders may be at different statuses
```

### Test Cases

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-6.1.1-01 | View status timeline | Happy Path | All milestones shown |
| TC-6.1.1-02 | COD balance banner | Happy Path | Cash amount shown |
| TC-6.1.1-03 | Live tracking card | Happy Path | Real-time status |
| TC-6.1.1-04 | Multi-sub-order tracking | Happy Path | Separate timelines |
| TC-6.1.1-05 | Order not found | Error | 404 page |
| TC-6.1.1-06 | Access another user's order | Security | 403 Forbidden |
| TC-6.1.1-07 | RTL timeline layout | i18n | Mirrored timeline |

### Activity Diagram

```mermaid
flowchart TD
    A([Customer opens order confirmation]) --> B[GET /v1/orders/:id]
    B --> C{Authorized?}
    C -->|No| D[403 Forbidden]
    C -->|Yes| E[Load order with sub-orders]
    E --> F[Render status timeline]
    F --> G{Has AWB?}
    G -->|Yes| H[Show live tracking card]
    G -->|No| I[Show "Preparing shipment"]
    H --> J{Is COD?}
    I --> J
    J -->|Yes| K[Show COD balance banner]
    J -->|No| L[No COD banner]
    K --> M([Render complete page])
    L --> M
```

---

## US-6.1.2: Customer Order History with Filtering

**As a** returning Customer,  
**I want to** view my complete order history with filters for status, date range, and search,  
**So that** I can find past orders and reorder items easily.

### Acceptance Criteria

```gherkin
Feature: Order History

  Scenario: View order history
    Given the customer navigates to "/[locale]/account/orders"
    Then a paginated list of orders is shown (most recent first)
    And each order card shows: order ID, date, total, status, item thumbnails

  Scenario: Filter by status
    When the customer filters by status="Delivered"
    Then only delivered orders are shown

  Scenario: Reorder from history
    When the customer clicks "Reorder" on a past order
    Then all items are added to the current cart
    And unavailable items are flagged
```

### Test Cases

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-6.1.2-01 | View order list | Happy Path | Paginated, sorted |
| TC-6.1.2-02 | Filter by status | Happy Path | Correct results |
| TC-6.1.2-03 | Reorder | Happy Path | Items added to cart |
| TC-6.1.2-04 | Empty order history | Edge Case | "No orders yet" |
| TC-6.1.2-05 | Reorder with discontinued item | Edge Case | Item flagged |
| TC-6.1.2-06 | 500+ orders pagination | Performance | Pages load <200ms |

---

## US-6.1.3: Return Merchandise Authorization (RMA)

**As a** Customer within the return window,  
**I want to** initiate a return for one or more items from my order,  
**So that** I can return products that don't meet my expectations and get a refund.

### Acceptance Criteria

```gherkin
Feature: Return Merchandise Authorization

  Scenario: Initiate return within 14-day window
    Given the order was delivered 5 days ago
    When the customer clicks "Request Return" on the order page
    And selects items to return with reason "Defective"
    Then an RMA request is created with status PENDING_APPROVAL
    And the durable orchestrator freezes the vendor's escrow

  Scenario: Return label generated
    Given the RMA is approved
    Then a prepaid return shipping label is generated
    And the customer receives the label via email and in-app notification

  Scenario: Return window expired
    Given the order was delivered 16 days ago
    When the customer tries to request a return
    Then a message "Return window has expired (14 days)" is shown
    And the return button is disabled

  Scenario: Return inspected and refund issued
    Given the returned item is inspected by the vendor
    When the vendor marks it as "Accepted"
    Then the refund is processed via the original payment method
    And the escrow hold is released
```

### Test Cases

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-6.1.3-01 | Return within window | Happy Path | RMA created |
| TC-6.1.3-02 | Return window expired | Validation | Button disabled |
| TC-6.1.3-03 | Return label generation | Happy Path | Label PDF created |
| TC-6.1.3-04 | Partial return (2 of 5 items) | Happy Path | Only selected items RMA'd |
| TC-6.1.3-05 | Return rejected by vendor | Happy Path | No refund, customer notified |
| TC-6.1.3-06 | Refund to original method | Happy Path | Paymob/Stripe refund |
| TC-6.1.3-07 | Return for COD order | Edge Case | Refund via bank transfer |
| TC-6.1.3-08 | Digital product return | Validation | Returns not allowed, license revoked |
| TC-6.1.3-09 | Concurrent return requests | Concurrency | Only one RMA per item |
| TC-6.1.3-10 | Return for multi-vendor order | Happy Path | Per-vendor RMA |

### Activity Diagram

```mermaid
flowchart TD
    A([Customer clicks Request Return]) --> B{Within 14-day window?}
    B -->|No| C[Show "Window expired"]
    B -->|Yes| D[Select items + reason]
    D --> E[POST /v1/orders/:id/rma]
    E --> F[Create RMA# PENDING_APPROVAL]
    F --> G[Freeze vendor escrow hold]
    G --> H[SNS notify vendor]
    H --> I{Vendor decision?}
    I -->|Approve| J[Generate return label]
    J --> K[SNS notify customer with label]
    K --> L{Return received + inspected?}
    L -->|Accepted| M[Process refund]
    M --> N[Release escrow]
    N --> O([Customer refunded])
    L -->|Rejected| P[SNS notify: return rejected]
    P --> Q[Release escrow back to vendor]
    I -->|Reject| R[SNS notify customer: denied]
```

---

## US-6.1.4: Admin Order Management Dashboard

**As a** Store Administrator,  
**I want** a centralized order management dashboard to view, filter, search, and update order statuses,  
**So that** I can oversee all marketplace operations efficiently.

### Acceptance Criteria

```gherkin
Feature: Admin Order Management

  Scenario: View all orders with filters
    Given the admin navigates to "/[locale]/admin/orders"
    Then a filterable table shows all orders across all vendors
    And filters include: status, date range, payment mode, vendor, customer

  Scenario: Manually update order status
    When the admin manually sets an order to SHIPPED with tracking info
    Then the order status updates in DynamoDB
    And the customer receives an SNS notification

  Scenario: Cancel order and process refund
    When the admin cancels a PENDING_PAYMENT order
    Then inventory reservations are released
    And if payment was made, a refund is initiated
```

### Test Cases

| # | Test Case | Type | Expected Result |
|:--|:----------|:-----|:----------------|
| TC-6.1.4-01 | View all orders | Happy Path | Table with filters |
| TC-6.1.4-02 | Filter by status | Happy Path | Correct results |
| TC-6.1.4-03 | Update status | Happy Path | Status changed, notify |
| TC-6.1.4-04 | Cancel with refund | Happy Path | Refund processed |
| TC-6.1.4-05 | Cancel without payment | Happy Path | Stock released only |
| TC-6.1.4-06 | Non-admin access | Security | 403 Forbidden |
| TC-6.1.4-07 | Export orders CSV | Happy Path | CSV downloads |
| TC-6.1.4-08 | Bulk status update | Happy Path | Multiple orders updated |
