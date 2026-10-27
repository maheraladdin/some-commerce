# Payments, Global Shipping, Split COD, SNS Notifications & Digital Licensing Specification

## 1. KMS-Encrypted Dynamic Payment Vault (`PaymentProvider` Trait)

Store admins configure payment gateways directly from the Expo Admin Dashboard (`POST /v1/admin/payment-gateways`). Credentials are encrypted using [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) envelope encryption (`kms:Encrypt` with `EncryptionContext: {"tenant_id": "...", "provider": "..."}`) and stored in `SomeCommerceTable` (`PK = TENANT#<tid>`, `SK = PAYMENT_GW#<provider>`).

```rust
#[async_trait::async_trait]
pub trait PaymentProvider: Send + Sync {
    fn provider_id(&self) -> &'static str;
    async fn create_payment_intent(
        &self,
        ctx: &TenantPaymentConfig,
        req: CreateIntentRequest,
    ) -> Result<PaymentIntentResponse, PaymentError>;
    async fn verify_webhook(
        &self,
        ctx: &TenantPaymentConfig,
        headers: &HeaderMap,
        raw_body: &[u8],
    ) -> Result<VerifiedPaymentEvent, PaymentError>;
    async fn refund_payment(
        &self,
        ctx: &TenantPaymentConfig,
        intent_id: &str,
        amount_cents: u64,
    ) -> Result<RefundResponse, PaymentError>;
}
```

### Supported Payment Providers
1. **[Paymob Accept](https://developers.paymob.com/paymob-docs/integration-paths/apis)** (`provider_id = "paymob"`):
   * Supports Cards, Meeza, Mobile Wallets (Vodafone Cash, Orange Cash, Etisalat Cash, WE Pay), InstaPay, and ValU / Sympl BNPL across Egypt, KSA, UAE, and Oman.
   * Verifies incoming webhooks via SHA-512 HMAC signature validation.
2. **[Stripe](https://docs.stripe.com/api/payment_intents)** (`provider_id = "stripe"`):
   * Supports global credit/debit cards, Apple Pay, Google Pay, SEPA, and B2B bank transfers.
   * Integrates with [`@stripe/stripe-react-native`](https://docs.expo.dev/versions/latest/sdk/stripe/) on iOS/Android and Stripe Elements on static Expo Web.
3. **[BTCPay Server](https://docs.btcpayserver.org/API/Greenfield/v1/)** (`provider_id = "btcpay"`):
   * Self-hosted, zero-fee cryptocurrency processor supporting Bitcoin (on-chain), Lightning Network, and stablecoins.

## 2. Global & Regional Shipping Engine (`ShippingProvider` Trait)

```rust
#[async_trait::async_trait]
pub trait ShippingProvider: Send + Sync {
    fn carrier_id(&self) -> &'static str;
    async fn calculate_rates(
        &self,
        ctx: &TenantShippingConfig,
        shipment: &RateQuoteRequest,
    ) -> Result<Vec<CarrierRateQuote>, ShippingError>;
    async fn create_shipment(
        &self,
        ctx: &TenantShippingConfig,
        order: &FulfillmentOrder,
    ) -> Result<CreatedShipment, ShippingError>;
    async fn verify_webhook(
        &self,
        ctx: &TenantShippingConfig,
        headers: &HeaderMap,
        raw_body: &[u8],
    ) -> Result<VerifiedShipmentEvent, ShippingError>;
}
```

### Supported Shipping Adapters & Regional Coverage
1. **`CustomZoneProvider` (Built-in Local Fleet / Table Rates)**:
   * Uses merchant-defined `LOCALE_FEES#<country>#<zone>` records in DynamoDB to compute delivery fees by governorate/city (e.g., Cairo, Giza, Mansoura/Dakahlia, Alexandria), weight brackets, and COD surcharges.
2. **[Bosta API](https://docs.bosta.co/)** (`carrier_id = "bosta"` — Egypt & KSA):
   * Automates `/api/v2/deliveries` booking, Air Waybill (AWB) PDF label generation, warehouse pickup requests, Open Package permissions, Cash-on-Delivery collection, and [webhook status tracking](https://docs.bosta.co/docs/how-to/get-delivery-status-via-webhook/).
3. **[Aramex Shipping Services API](https://www.aramex.com/eg/en/developers-solution-center/aramex.com-platform)** (`carrier_id = "aramex"` — MENA, GCC & Levant):
   * Supports domestic and cross-border MENA/GCC parcels, volumetric rate calculation, customs commercial invoices, and cross-border COD.
4. **[DHL Express MyDHL API](https://developer.dhl.com/api-reference/dhl-express-mydhl-api?language_content_entity=en)** (`carrier_id = "dhl_express"` — Global Express & B2B Air):
   * Provides international time-definite express shipping, landed-cost duty/tax estimation, Duties & Taxes Paid (DTP), and Paperless Trade (PLT) customs documentation.
5. **[Shippo API](https://docs.goshippo.com/) & [EasyPost API](https://docs.easypost.com/)** (`carrier_id = "shippo" | "easypost"` — US, EU, UK, Global 40+ Carriers):
   * Unlocks USPS, UPS, FedEx, Royal Mail, Canada Post, and Australia Post with live multi-carrier rate shopping at checkout.

## 3. Upfront Deposit + Split Cash on Delivery (`DEPOSIT_COD`) State Machine

To protect merchants from fake or uncollected Return-to-Origin (RTO) shipments on COD orders, `some-commerce` supports **Split COD**:

1. **Merchant Rule Configuration (`LOCALE_FEES#<country>#<zone>`)**:
   * `cod_deposit_rule`: `NONE` (100% COD), `SHIPPING_FEE_ONLY` (buyer pays the localized shipping + COD fee upfront online), `PERCENTAGE` (e.g., 20% upfront online), or `FIXED_AMOUNT` (e.g., 100 EGP upfront online).
2. **Checkout Calculation**:
   * `total_cents = subtotal_cents + localized_shipping_cents + cod_surcharge_cents + tax_vat_cents`
   * `deposit_required_cents = compute_deposit(total_cents, localized_shipping_cents, rule)`
   * `cod_collection_cents = total_cents - deposit_required_cents`
3. **Order Lifecycle & Amazon SNS Notification Triggers**:
   * `AWAITING_COD_DEPOSIT`: Payment intent created on Paymob/Stripe/BTCPay for `deposit_required_cents`. [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) dispatches an SMS/Push payment link if initiated via B2B/phone order.
   * `DEPOSIT_PAID_COD_PENDING`: Payment webhook confirms `deposit_paid_cents == deposit_required_cents`.
   * `SHIPMENT_BOOKED`: `fulfillment-worker` calls Bosta/Aramex with `collectionAmount = cod_collection_cents` (the remaining balance) and publishes an SNS `ShipmentBooked` push/SMS notification with the live tracking link.
   * `COMPLETED`: Carrier webhook reports `Delivered` (`state = 45` in Bosta), confirming the courier collected `cod_collection_cents`.
   * `RTO_RETURNED`: Carrier webhook reports `Returned to Business`. The merchant's RTO policy retains the shipping-fee deposit to cover return freight and automatically refunds any excess product deposit.

## 4. Cryptographic E-Product Licensing Engine (Ed25519 + AWS KMS)

Digital products (software binaries, plugins, mobile apps, datasets, e-books) and hybrid physical+digital bundles are protected by a two-layer licensing architecture:

1. **Offline Cryptographic Certificate (`.lic`)**:
   * Signed using an asymmetric **Ed25519** key pair stored inside [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html) (`kms:Sign` with `SigningAlgorithm: ED25519_SHA_512`).
   * The `.lic` payload is a canonical JSON structure containing `license_key`, `tenant_id`, `product_id`, `customer_sub`, `b2b_org_id`, `max_seats`, `issued_at`, `expires_at`, and `entitlements[]`, appended with the Base64Url Ed25519 signature.
   * Client applications embed only the public key to verify certificates offline with zero network dependency.
2. **Online Activation, Heartbeat & Seat Management (`/v1/licenses/*`)**:
   * `POST /v1/licenses/activate`: Registers a hashed hardware fingerprint (`machine_id`) in DynamoDB using an atomic conditional expression (`size(active_machines) < max_seats`).
   * `POST /v1/licenses/verify`: Sub-10ms heartbeat check served by `storefront-sdui-api` returning license validity, seat status, and signed timestamp.
   * **Automatic Refund & Return Revocation**: If a Stripe/Paymob refund or chargeback webhook fires—or if a Bosta/Aramex physical bundle is returned—`checkout-webhooks-api` atomically sets `license_status = REVOKED` and publishes a `LicenseRevoked` event to Amazon SNS.
