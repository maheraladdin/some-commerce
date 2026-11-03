#!/usr/bin/env python3
"""
Applies GitHub Spec Kit and security-audit gateways to each user story individually.
Extracts canonical narrative, acceptance criteria, test cases, and diagrams from git source,
and generates full Spec Kit specifications with:
1. Spec Kit Specification & Gherkin scenarios with [AC-US-X.Y.Z-NN]
2. Framework-scoped Behavior-Centric Architecture (Expo Client & Cargo Lambda Axum Backend)
3. Scoping & Promotion Blueprint
4. Technical Implementation Plan & Mermaid diagrams
5. Granular Implementation Tasks (Phases 1-4)
6. Comprehensive Security Gateway (Powered by security-audit)
7. Validation Gates (G0-G4)
"""

import os
import re
import subprocess

STORY_MAP = {
    # 01-auth-and-onboarding
    "US-1.1.1": {
        "feature": "identity-and-access",
        "module": "auth-and-onboarding",
        "behaviour": "phone-otp-sign-in",
        "sprint": "Sprint 1.1",
        "services": ["cognito_auth_client.rs", "sns_sms_gateway.rs", "auth_session_api.ts"],
        "designs": ["PhoneOtpScreen.tsx", "OtpCountdownInput.tsx", "OtpStyles.ts"],
        "logic": ["usePhoneOtpAuth.ts", "phone_number_validator.rs", "otp_rate_limiter.rs"],
        "types": ["AuthPrincipal.ts", "InitiateOtpPayload.ts", "VerifyOtpPayload.ts"],
        "constants": ["AuthEndpoints.ts", "OtpDurationConstants.ts", "AuthErrorCodes.ts"],
        "threat_focus": "SMS pumping, brute-force OTP guessing, session fixation, and cross-tenant claim spoofing"
    },
    "US-1.1.2": {
        "feature": "identity-and-access",
        "module": "auth-and-onboarding",
        "behaviour": "passkey-webauthn-sign-in",
        "sprint": "Sprint 1.1",
        "services": ["webauthn_client.rs", "cognito_passkey_adapter.rs", "passkey_api.ts"],
        "designs": ["PasskeySignInScreen.tsx", "PasskeyEnrollmentModal.tsx", "BiometricPrompt.tsx"],
        "logic": ["usePasskeyAuth.ts", "webauthn_challenge_verifier.rs", "credential_policy.ts"],
        "types": ["PasskeyRegistrationPayload.ts", "PasskeyAssertionResponse.ts", "WebAuthnCredential.ts"],
        "constants": ["PasskeyEndpoints.ts", "RelyingPartyConfig.ts", "PasskeyErrorCodes.ts"],
        "threat_focus": "Replay attacks, invalid WebAuthn origin spoofing, attestation tampering, and credential harvesting"
    },
    "US-1.1.3": {
        "feature": "identity-and-access",
        "module": "auth-and-onboarding",
        "behaviour": "social-oidc-sign-in",
        "sprint": "Sprint 1.1",
        "services": ["cognito_oidc_adapter.rs", "apple_auth_client.rs", "google_oidc_api.ts"],
        "designs": ["SocialSignInButtons.tsx", "OidcRedirectHandlerScreen.tsx", "AccountLinkingSheet.tsx"],
        "logic": ["useSocialSignIn.ts", "oidc_nonce_verifier.rs", "identity_linker.rs"],
        "types": ["SocialAuthPayload.ts", "OidcTokenClaims.ts", "LinkedIdentityRecord.ts"],
        "constants": ["OidcProviders.ts", "SocialAuthRoutes.ts", "OidcErrorCodes.ts"],
        "threat_focus": "State parameter tampering, CSRF on OAuth redirect, token substitution, and identity pre-hijacking"
    },
    "US-1.1.4": {
        "feature": "identity-and-access",
        "module": "auth-and-onboarding",
        "behaviour": "b2b-org-registration",
        "sprint": "Sprint 1.1",
        "services": ["b2b_registration_client.rs", "tax_vat_verifier.rs", "b2b_approval_api.ts"],
        "designs": ["B2bRegistrationFormScreen.tsx", "DocumentUploadSection.tsx", "PendingApprovalBanner.tsx"],
        "logic": ["useB2bRegistration.ts", "vat_tax_validator.rs", "org_domain_verifier.rs"],
        "types": ["OrganizationApplication.ts", "TaxVatProof.ts", "B2bApprovalStatus.ts"],
        "constants": ["B2bOrgEndpoints.ts", "VatValidationRules.ts", "OrgRegistrationErrors.ts"],
        "threat_focus": "Forged business registration documents, VAT tax ID spoofing, unauthorized organization ownership claims"
    },

    # 02-storefront-and-catalog
    "US-2.1.1": {
        "feature": "catalog-and-discovery",
        "module": "storefront-and-catalog",
        "behaviour": "instant-sdui-storefront",
        "sprint": "Sprint 1.1",
        "services": ["sdui_page_client.rs", "watermelondb_sdui_adapter.ts", "etag_query_client.ts"],
        "designs": ["SduiScreenHost.tsx", "PageSkeletonLoader.tsx", "SduiBlockRegistry.tsx"],
        "logic": ["useSduiPage.ts", "etag_freshness_verifier.ts", "watermelon_sdui_sync.ts"],
        "types": ["SduiLayoutSchema.ts", "SduiBlockPayload.ts", "EtagRegistryEntry.ts"],
        "constants": ["SduiPageRoutes.ts", "CacheTtlConstants.ts", "SduiBlockTypes.ts"],
        "threat_focus": "Cross-tenant SDUI block injection, unauthorized layout tampering, and cache poison attacks"
    },
    "US-2.1.2": {
        "feature": "catalog-and-discovery",
        "module": "storefront-and-catalog",
        "behaviour": "n-level-taxonomy",
        "sprint": "Sprint 1.1",
        "services": ["taxonomy_repository.rs", "category_cache_service.rs", "taxonomy_api.ts"],
        "designs": ["CategoryTreeView.tsx", "CategoryBreadcrumbBar.tsx", "BrandFilterGrid.tsx"],
        "logic": ["useCategoryTree.ts", "cycle_detection_validator.rs", "ancestor_path_calc.rs"],
        "types": ["TaxonomyNode.ts", "BrandRecord.ts", "AncestorsPath.ts"],
        "constants": ["TaxonomyEndpoints.ts", "DepthLimits.ts", "TaxonomyErrorCodes.ts"],
        "threat_focus": "Circular taxonomy reference exploits, unauthorized category subtree reassignment, and IDOR on brand editing"
    },
    "US-2.1.3": {
        "feature": "catalog-and-discovery",
        "module": "storefront-and-catalog",
        "behaviour": "dynamic-product-properties",
        "sprint": "Sprint 1.1",
        "services": ["property_def_client.rs", "widget_metadata_service.rs", "properties_api.ts"],
        "designs": ["ColorSwatchPicker.tsx", "NumericUnitSlider.tsx", "PropertyManagerModal.tsx"],
        "logic": ["useDynamicProperties.ts", "property_schema_validator.rs", "filter_widget_matcher.ts"],
        "types": ["PropertyDefinition.ts", "FilterUiWidget.ts", "PropertyValuePayload.ts"],
        "constants": ["PropertyDataTypes.ts", "WidgetTypes.ts", "PropertyErrorCodes.ts"],
        "threat_focus": "Prototype pollution via dynamic property keys, regex DoS on property validation, and cross-tenant schema leakage"
    },
    "US-2.1.4": {
        "feature": "catalog-and-discovery",
        "module": "storefront-and-catalog",
        "behaviour": "dual-tier-search",
        "sprint": "Sprint 1.1",
        "services": ["elasticsearch_search_client.rs", "dynamo_filter_provider.rs", "search_api.ts"],
        "designs": ["SearchFacetedView.tsx", "FilterDrawerSheet.tsx", "DisjunctiveFacetPills.tsx"],
        "logic": ["useCatalogSearch.ts", "query_ast_sanitizer.rs", "facet_disjunction_aggregator.ts"],
        "types": ["SearchQueryPayload.ts", "FacetedSearchResult.ts", "FacetAggregation.ts"],
        "constants": ["SearchEndpoints.ts", "SearchAnalyzerConfig.ts", "FacetKeys.ts"],
        "threat_focus": "Elasticsearch injection queries, ReDoS in search phrase parsers, and unauthorized unlisted product indexing leaks"
    },
    "US-2.1.5": {
        "feature": "catalog-and-discovery",
        "module": "storefront-and-catalog",
        "behaviour": "product-detail-configurator",
        "sprint": "Sprint 1.1",
        "services": ["product_detail_client.rs", "inventory_checker_service.rs", "pdp_api.ts"],
        "designs": ["ProductGalleryCarousel.tsx", "VariantMatrixSelector.tsx", "PriceDisplayTag.tsx"],
        "logic": ["useProductConfigurator.ts", "cartesian_variant_solver.rs", "stock_threshold_calculator.ts"],
        "types": ["ProductDetailSchema.ts", "SkuVariant.ts", "VariantAxisSelection.ts"],
        "constants": ["PdpEndpoints.ts", "StockBadgeThresholds.ts", "PdpErrorCodes.ts"],
        "threat_focus": "Inventory count harvesting, hidden variant pricing bypass, and manipulated price-list overrides"
    },

    # 03-cart-and-checkout
    "US-3.1.1": {
        "feature": "order-processing-and-commerce",
        "module": "cart-and-checkout",
        "behaviour": "offline-cart-sync",
        "sprint": "Sprint 1.2",
        "services": ["cart_sync_client.rs", "watermelondb_cart_adapter.ts", "cart_api.ts"],
        "designs": ["CartItemList.tsx", "CartItemRow.tsx", "OfflineSyncStatusBadge.tsx"],
        "logic": ["useOfflineCart.ts", "cart_reconciliation_engine.ts", "quantity_limiter.ts"],
        "types": ["CartRecord.ts", "CartItemRecord.ts", "SyncCartConflictResolution.ts"],
        "constants": ["CartEndpoints.ts", "MaxCartQuantities.ts", "CartSyncErrorCodes.ts"],
        "threat_focus": "Cart item price tampering in local SQLite, negative quantity injection, and cross-session cart leakage"
    },
    "US-3.1.2": {
        "feature": "order-processing-and-commerce",
        "module": "cart-and-checkout",
        "behaviour": "multi-vendor-cart-grouping",
        "sprint": "Sprint 1.2",
        "services": ["vendor_grouping_client.rs", "shipping_estimator_service.rs", "grouping_api.ts"],
        "designs": ["VendorGroupSection.tsx", "VendorShippingEstimatePill.tsx", "SplitOrderBanner.tsx"],
        "logic": ["useVendorCartGroups.ts", "sub_cart_grouper.rs", "proportional_shipping_calc.ts"],
        "types": ["VendorCartGroup.ts", "SubOrderEstimate.ts", "VendorShippingRate.ts"],
        "constants": ["VendorGroupingEndpoints.ts", "ShippingEstimateLimits.ts", "GroupingErrors.ts"],
        "threat_focus": "Unauthorized vendor order tampering, shipping cost avoidance via vendor spoofing, and inventory race manipulation"
    },
    "US-3.1.3": {
        "feature": "order-processing-and-commerce",
        "module": "cart-and-checkout",
        "behaviour": "multi-step-checkout",
        "sprint": "Sprint 1.2",
        "services": ["checkout_session_client.rs", "inventory_reservation_service.rs", "checkout_api.ts"],
        "designs": ["CheckoutStepperView.tsx", "OrderSummaryCard.tsx", "PlaceOrderButton.tsx"],
        "logic": ["useCheckoutFlow.ts", "checkout_state_machine.ts", "inventory_expiry_timer.ts"],
        "types": ["CheckoutSession.ts", "CheckoutStepState.ts", "OrderPlacementResult.ts"],
        "constants": ["CheckoutRoutes.ts", "ReservationTimeouts.ts", "CheckoutErrorCodes.ts"],
        "threat_focus": "Race condition in stock depletion, step-skipping state machine bypass, and double-submit order duplication"
    },
    "US-3.1.4": {
        "feature": "order-processing-and-commerce",
        "module": "cart-and-checkout",
        "behaviour": "localized-address-management",
        "sprint": "Sprint 1.2",
        "services": ["address_repository.rs", "national_address_verifier.rs", "address_api.ts"],
        "designs": ["AddressSelectorSheet.tsx", "NationalAddressForm.tsx", "GeoPinMapPicker.tsx"],
        "logic": ["useAddressManager.ts", "postal_code_validator.rs", "building_number_formatter.ts"],
        "types": ["AddressSnapshot.ts", "GovernorateDistrict.ts", "AddressValidationResponse.ts"],
        "constants": ["AddressEndpoints.ts", "SupportedGovernorates.ts", "AddressErrorCodes.ts"],
        "threat_focus": "IDOR on customer address update/delete, geographic boundary spoofing to manipulate delivery fees"
    },

    # 04-payments-and-cod
    "US-4.1.1": {
        "feature": "order-processing-and-commerce",
        "module": "payments-and-cod",
        "behaviour": "prepaid-card-payment",
        "sprint": "Sprint 1.2",
        "services": ["paymob_adapter.rs", "stripe_adapter.rs", "payment_webhook_handler.rs"],
        "designs": ["CardPaymentModal.tsx", "3dsChallengeIframe.tsx", "PaymentSuccessCelebration.tsx"],
        "logic": ["useCardPayment.ts", "hmac_signature_verifier.rs", "payment_status_poller.ts"],
        "types": ["PaymentIntention.ts", "WebhookNotificationPayload.ts", "PaymentTransactionRecord.ts"],
        "constants": ["PaymentEndpoints.ts", "GatewayProviders.ts", "PaymentErrorCodes.ts"],
        "threat_focus": "HMAC webhook forgery, 3DS authentication bypass, transaction replay, and currency denomination tampering"
    },
    "US-4.1.2": {
        "feature": "order-processing-and-commerce",
        "module": "payments-and-cod",
        "behaviour": "full-cash-on-delivery",
        "sprint": "Sprint 1.2",
        "services": ["cod_eligibility_client.rs", "risk_scoring_service.rs", "cod_order_api.ts"],
        "designs": ["CodSelectionRadio.tsx", "CodRiskVerificationModal.tsx", "CashPreparationNotice.tsx"],
        "logic": ["useCashOnDelivery.ts", "cod_eligibility_evaluator.rs", "customer_blacklist_checker.rs"],
        "types": ["CodEligibilityDecision.ts", "CodRiskAssessment.ts", "CodFeeConfiguration.ts"],
        "constants": ["CodEndpoints.ts", "MaxCodThresholds.ts", "CodErrorCodes.ts"],
        "threat_focus": "Fake high-value orders to deplete inventory, blacklisted customer identity rotation, and fee evasion"
    },
    "US-4.1.3": {
        "feature": "order-processing-and-commerce",
        "module": "payments-and-cod",
        "behaviour": "split-deposit-cod",
        "sprint": "Sprint 1.2",
        "services": ["split_cod_calculator.rs", "deposit_payment_service.rs", "split_cod_api.ts"],
        "designs": ["SplitBreakdownDisplay.tsx", "DepositPaymentSheet.tsx", "CourierBalanceBadge.tsx"],
        "logic": ["useSplitCodCheckout.ts", "deposit_math_engine.rs", "rto_deposit_allocator.rs"],
        "types": ["SplitCodCalculation.ts", "DepositRuleConfig.ts", "RtoPolicyOutcome.ts"],
        "constants": ["SplitCodEndpoints.ts", "DepositRuleTypes.ts", "SplitCodErrorCodes.ts"],
        "threat_focus": "Deposit rule tampering, refunding more than settled deposit, and mathematical rounding theft"
    },
    "US-4.1.4": {
        "feature": "order-processing-and-commerce",
        "module": "payments-and-cod",
        "behaviour": "payment-gateway-config",
        "sprint": "Sprint 1.2",
        "services": ["kms_secret_vault.rs", "gateway_config_repository.rs", "admin_gateway_api.ts"],
        "designs": ["GatewayConfigDashboard.tsx", "ApiKeyInputWithReveal.tsx", "WebhookTestRunner.tsx"],
        "logic": ["useGatewayConfig.ts", "secret_envelope_encryptor.rs", "credential_health_checker.rs"],
        "types": ["EncryptedGatewaySecret.ts", "GatewayConfigPayload.ts", "HealthCheckStatus.ts"],
        "constants": ["AdminGatewayEndpoints.ts", "SupportedGateways.ts", "ConfigErrorCodes.ts"],
        "threat_focus": "Exposure of merchant private keys, unauthorized payment route hijacking, and plaintext credential logging"
    },
    "US-4.1.5": {
        "feature": "order-processing-and-commerce",
        "module": "payments-and-cod",
        "behaviour": "lightning-bitcoin-payment",
        "sprint": "Sprint 4.2",
        "services": ["btcpay_client.rs", "lightning_invoice_service.rs", "lightning_api.ts"],
        "designs": ["LightningQrCodeDisplay.tsx", "InvoiceCountdownTimer.tsx", "BtcPaidCheckmark.tsx"],
        "logic": ["useLightningCheckout.ts", "sat_rate_converter.rs", "websocket_invoice_listener.ts"],
        "types": ["LightningInvoice.ts", "SatoshiConversionRate.ts", "BtcPaymentEvent.ts"],
        "constants": ["BtcPayEndpoints.ts", "LightningExpiryMinutes.ts", "BtcErrorCodes.ts"],
        "threat_focus": "Underpayment transaction pinning, zero-conf double spend attacks, and expired invoice race acceptance"
    },

    # 05-fulfillment-and-shipping
    "US-5.1.1": {
        "feature": "logistics-and-fulfillment",
        "module": "fulfillment-and-shipping",
        "behaviour": "bosta-domestic-shipping",
        "sprint": "Sprint 1.2",
        "services": ["bosta_client.rs", "bosta_webhook_receiver.rs", "bosta_api.ts"],
        "designs": ["BostaWaybillPreview.tsx", "PickupSchedulerForm.tsx", "BostaTrackingTimeline.tsx"],
        "logic": ["useBostaShipping.ts", "bosta_awb_generator.rs", "cod_reconciliation_validator.rs"],
        "types": ["BostaShipmentRequest.ts", "BostaAwbResponse.ts", "BostaTrackingEvent.ts"],
        "constants": ["BostaEndpoints.ts", "BostaStates.ts", "BostaErrorCodes.ts"],
        "threat_focus": "Tampered courier collection amounts, fake delivery confirmation webhooks, and AWB identifier reuse"
    },
    "US-5.1.2": {
        "feature": "logistics-and-fulfillment",
        "module": "fulfillment-and-shipping",
        "behaviour": "cross-border-shipping",
        "sprint": "Sprint 3.1",
        "services": ["aramex_client.rs", "dhl_express_client.rs", "customs_duty_service.rs"],
        "designs": ["CustomsDeclarationSheet.tsx", "InternationalRateMatrix.tsx", "DutyTaxBreakdown.tsx"],
        "logic": ["useCrossBorderShipping.ts", "hs_code_duty_calculator.rs", "carrier_rate_comparer.ts"],
        "types": ["CustomsDeclaration.ts", "InternationalRateQuote.ts", "CrossBorderWaybill.ts"],
        "constants": ["CrossBorderEndpoints.ts", "HsCodeRegistry.ts", "CrossBorderErrors.ts"],
        "threat_focus": "Customs undervaluation fraud, restricted country export violations, and unauthorized carrier account billing"
    },
    "US-5.1.3": {
        "feature": "logistics-and-fulfillment",
        "module": "fulfillment-and-shipping",
        "behaviour": "carrier-aggregation",
        "sprint": "Sprint 4.1",
        "services": ["shippo_adapter.rs", "easypost_adapter.rs", "carrier_fallback_router.rs"],
        "designs": ["CarrierSelectorRadioGroup.tsx", "DeliverySpeedComparison.tsx", "AggregationStatusPill.tsx"],
        "logic": ["useCarrierAggregation.ts", "least_cost_carrier_router.rs", "carrier_circuit_breaker.rs"],
        "types": ["CarrierRateAggregate.ts", "CarrierSelectionCriteria.ts", "AggregatedTrackingStatus.ts"],
        "constants": ["CarrierEndpoints.ts", "FallbackPriorityOrder.ts", "CarrierErrorCodes.ts"],
        "threat_focus": "Carrier API rate limit exhaustion attacks, manipulated parcel dimensions/weight, and SSRF on carrier webhook URLs"
    },
    "US-5.1.4": {
        "feature": "logistics-and-fulfillment",
        "module": "fulfillment-and-shipping",
        "behaviour": "milestone-notifications",
        "sprint": "Sprint 1.2",
        "services": ["sns_notification_dispatcher.rs", "fcm_apns_sender.rs", "notification_history_api.ts"],
        "designs": ["NotificationToastBanner.tsx", "PushPermissionPrompt.tsx", "SmsDeliveryLogCard.tsx"],
        "logic": ["useMilestoneNotifications.ts", "localized_template_renderer.rs", "deduplication_filter.rs"],
        "types": ["NotificationDispatchPayload.ts", "MilestoneEvent.ts", "DeliveryReport.ts"],
        "constants": ["NotificationChannels.ts", "SnsTopics.ts", "NotificationErrors.ts"],
        "threat_focus": "Notification SMS flood attacks, PII exposure in push payload notifications, and SMS spoofing"
    },

    # 06-orders-and-returns
    "US-6.1.1": {
        "feature": "order-processing-and-commerce",
        "module": "orders-and-returns",
        "behaviour": "realtime-order-tracking",
        "sprint": "Sprint 1.2",
        "services": ["live_tracking_client.rs", "order_event_stream_subscriber.rs", "tracking_api.ts"],
        "designs": ["LiveTrackingMapScreen.tsx", "OrderStatusTimeline.tsx", "DriverContactButton.tsx"],
        "logic": ["useRealtimeOrderTracking.ts", "status_progression_calculator.ts", "eta_recalculator.ts"],
        "types": ["OrderStatusSnapshot.ts", "TrackingMilestone.ts", "LiveLocationPayload.ts"],
        "constants": ["TrackingEndpoints.ts", "FinalOrderStates.ts", "TrackingErrorCodes.ts"],
        "threat_focus": "IDOR on live courier coordinates, unauthenticated order timeline scraping, and fake milestone events"
    },
    "US-6.1.2": {
        "feature": "order-processing-and-commerce",
        "module": "orders-and-returns",
        "behaviour": "customer-order-history",
        "sprint": "Sprint 1.2",
        "services": ["order_history_client.rs", "receipt_pdf_generator.rs", "order_search_api.ts"],
        "designs": ["OrderHistoryListScreen.tsx", "OrderCardSummary.tsx", "OrderFilterDropdown.tsx"],
        "logic": ["useCustomerOrderHistory.ts", "order_status_filter.ts", "invoice_downloader.ts"],
        "types": ["CustomerOrderSummary.ts", "OrderHistoryFilterCriteria.ts", "InvoiceMetadata.ts"],
        "constants": ["OrderHistoryEndpoints.ts", "OrderListPaging.ts", "OrderHistoryErrors.ts"],
        "threat_focus": "Horizontal privilege escalation to view other users invoices, order ID enumeration attacks"
    },
    "US-6.1.3": {
        "feature": "order-processing-and-commerce",
        "module": "orders-and-returns",
        "behaviour": "rma-returns-management",
        "sprint": "Sprint 4.2",
        "services": ["rma_request_client.rs", "reverse_shipping_service.rs", "rma_api.ts"],
        "designs": ["ReturnRequestFormScreen.tsx", "ReturnItemSelector.tsx", "RmaStatusBadge.tsx"],
        "logic": ["useRmaReturns.ts", "return_window_validator.rs", "return_fee_calculator.rs"],
        "types": ["RmaRequestPayload.ts", "RmaDecision.ts", "ReturnShippingLabel.ts"],
        "constants": ["RmaEndpoints.ts", "ReturnWindowDays.ts", "RmaErrorCodes.ts"],
        "threat_focus": "Fraudulent returns of non-purchased items, return window bypass, and double-refund exploits"
    },
    "US-6.1.4": {
        "feature": "order-processing-and-commerce",
        "module": "orders-and-returns",
        "behaviour": "admin-order-management",
        "sprint": "Sprint 1.2",
        "services": ["admin_order_service.rs", "manual_adjustment_ledger.rs", "admin_orders_api.ts"],
        "designs": ["AdminOrderDetailsView.tsx", "OrderStatusOverrideModal.tsx", "AuditTrailTimeline.tsx"],
        "logic": ["useAdminOrderControl.ts", "state_transition_authorizer.rs", "refund_limit_enforcer.rs"],
        "types": ["AdminOrderView.ts", "StateOverrideRequest.ts", "AuditLogEntry.ts"],
        "constants": ["AdminOrderEndpoints.ts", "AllowedOverrides.ts", "AdminOrderErrors.ts"],
        "threat_focus": "Unauthorized status tampering by compromised admin accounts, audit trail evasion, and unrecorded refunds"
    },

    # 07-customer-account
    "US-7.1.1": {
        "feature": "identity-and-access",
        "module": "customer-account",
        "behaviour": "customer-profile-management",
        "sprint": "Sprint 1.1",
        "services": ["profile_repository.rs", "avatar_upload_service.rs", "profile_api.ts"],
        "designs": ["ProfileEditScreen.tsx", "AvatarPicker.tsx", "AccountSecuritySection.tsx"],
        "logic": ["useCustomerProfile.ts", "email_change_verifier.rs", "phone_normalization.ts"],
        "types": ["CustomerProfile.ts", "ProfileUpdatePayload.ts", "AvatarUploadTicket.ts"],
        "constants": ["ProfileEndpoints.ts", "MaxAvatarSizeBytes.ts", "ProfileErrorCodes.ts"],
        "threat_focus": "Malicious SVG avatar upload (XSS), unverified email/phone change account takeover, IDOR on profile"
    },
    "US-7.1.2": {
        "feature": "identity-and-access",
        "module": "customer-account",
        "behaviour": "address-book-management",
        "sprint": "Sprint 1.1",
        "services": ["address_book_service.rs", "default_address_setter.rs", "address_book_api.ts"],
        "designs": ["AddressBookScreen.tsx", "AddressCardWithActions.tsx", "SetDefaultAddressButton.tsx"],
        "logic": ["useAddressBook.ts", "default_address_switcher.ts", "address_limit_checker.rs"],
        "types": ["AddressBookEntry.ts", "NewAddressPayload.ts", "AddressMutationResponse.ts"],
        "constants": ["AddressBookEndpoints.ts", "MaxSavedAddresses.ts", "AddressBookErrors.ts"],
        "threat_focus": "Address book pollution via automated bot scripts, IDOR modifying other customers saved addresses"
    },
    "US-7.1.3": {
        "feature": "identity-and-access",
        "module": "customer-account",
        "behaviour": "notification-preferences",
        "sprint": "Sprint 1.1",
        "services": ["preferences_repository.rs", "sns_channel_unsubscriber.rs", "preferences_api.ts"],
        "designs": ["NotificationSettingsScreen.tsx", "ChannelToggleList.tsx", "QuietHoursPicker.tsx"],
        "logic": ["useNotificationPreferences.ts", "opt_out_validator.rs", "quiet_hours_calculator.ts"],
        "types": ["NotificationPreferences.ts", "ChannelSettings.ts", "UpdatePreferencesPayload.ts"],
        "constants": ["PreferencesEndpoints.ts", "DefaultChannels.ts", "PreferencesErrorCodes.ts"],
        "threat_focus": "Unauthorized modification of marketing opt-out choices violating GDPR/telecom spam laws"
    },
    "US-7.1.4": {
        "feature": "identity-and-access",
        "module": "customer-account",
        "behaviour": "customer-wishlist",
        "sprint": "Sprint 1.1",
        "services": ["wishlist_repository.rs", "price_drop_notifier.rs", "wishlist_api.ts"],
        "designs": ["WishlistGridScreen.tsx", "WishlistItemCard.tsx", "MoveToCartButton.tsx"],
        "logic": ["useWishlist.ts", "wishlist_deduplicator.ts", "back_in_stock_listener.ts"],
        "types": ["WishlistItem.ts", "WishlistSyncPayload.ts", "PriceDropAlert.ts"],
        "constants": ["WishlistEndpoints.ts", "MaxWishlistCapacity.ts", "WishlistErrorCodes.ts"],
        "threat_focus": "Price-drop alert manipulation, scraping competitor product pricing through wishlist watchers"
    },

    # 08-webmcp-and-ai
    "US-8.1.1": {
        "feature": "catalog-and-discovery",
        "module": "webmcp-and-ai",
        "behaviour": "customer-shopping-assistant",
        "sprint": "Sprint 1.1",
        "services": ["webmcp_tool_provider.rs", "bedrock_agent_runtime.rs", "shopping_copilot_api.ts"],
        "designs": ["AiShoppingDrawer.tsx", "AgentChatMessageBubble.tsx", "ToolExecutionCard.tsx"],
        "logic": ["useShoppingAssistant.ts", "tool_call_sanitizer.rs", "prompt_injection_guard.rs"],
        "types": ["WebMcpToolDefinition.ts", "AssistantChatMessage.ts", "ToolCallInvocation.ts"],
        "constants": ["WebMcpToolNames.ts", "MaxChatTurns.ts", "AssistantErrorCodes.ts"],
        "threat_focus": "Indirect prompt injection via product descriptions, unauthorized tool invocation to purchase items"
    },
    "US-8.1.2": {
        "feature": "catalog-and-discovery",
        "module": "webmcp-and-ai",
        "behaviour": "admin-store-copilot",
        "sprint": "Sprint 1.1",
        "services": ["admin_tool_registry.rs", "analytics_query_tool.rs", "admin_copilot_api.ts"],
        "designs": ["AdminCopilotSidecar.tsx", "SchemaVisualizerWidget.tsx", "ExecutionApprovalPrompt.tsx"],
        "logic": ["useAdminStoreCopilot.ts", "admin_privilege_checker.rs", "destructive_action_guard.rs"],
        "types": ["AdminToolSchema.ts", "AnalyticsReportInsight.ts", "ActionConfirmationToken.ts"],
        "constants": ["AdminToolNames.ts", "HighRiskToolList.ts", "AdminCopilotErrors.ts"],
        "threat_focus": "Privilege escalation via LLM tool misuse, unauthorized bulk data exfiltration or catalog deletion"
    },
    "US-8.1.3": {
        "feature": "catalog-and-discovery",
        "module": "webmcp-and-ai",
        "behaviour": "shared-mcp-engine",
        "sprint": "Sprint 1.1",
        "services": ["mcp_rpc_handler.rs", "bedrock_converse_client.rs", "mcp_protocol_api.ts"],
        "designs": ["McpStatusIndicator.tsx", "ProtocolInspectorModal.tsx", "TokenUsageMeter.tsx"],
        "logic": ["useSharedMcpEngine.ts", "mcp_message_codec.rs", "rate_budget_governor.rs"],
        "types": ["JsonRpcRequest.ts", "JsonRpcResponse.ts", "McpContextSnapshot.ts"],
        "constants": ["McpSpecVersion.ts", "DefaultTokenLimits.ts", "McpErrorCodes.ts"],
        "threat_focus": "Denial of wallet via token exhaustion loops, arbitrary RPC command execution through malformed JSON-RPC"
    },

    # 09-digital-products-and-licensing
    "US-9.1.1": {
        "feature": "commercial-models",
        "module": "digital-products-and-licensing",
        "behaviour": "digital-asset-delivery",
        "sprint": "Sprint 2.1",
        "services": ["s3_presigned_url_signer.rs", "asset_integrity_verifier.rs", "download_api.ts"],
        "designs": ["DigitalAssetVaultView.tsx", "DownloadProgressBar.tsx", "AssetChecksumBadge.tsx"],
        "logic": ["useDigitalAssetDownload.ts", "download_token_validator.rs", "rate_limited_streamer.ts"],
        "types": ["DigitalAssetTicket.ts", "PresignedDownloadUrl.ts", "AssetChecksum.ts"],
        "constants": ["DigitalAssetEndpoints.ts", "PresignedUrlTtlSeconds.ts", "AssetErrorCodes.ts"],
        "threat_focus": "Presigned URL URL-sharing/hotlinking, IP address bypass, and unauthenticated digital binary downloads"
    },
    "US-9.1.2": {
        "feature": "commercial-models",
        "module": "digital-products-and-licensing",
        "behaviour": "six-mode-licensing-engine",
        "sprint": "Sprint 2.1 / 2.2",
        "services": ["ed25519_license_signer.rs", "crl_revocation_service.rs", "license_verification_api.ts"],
        "designs": ["LicenseModeSelector.tsx", "AirGappedQrCodeViewer.tsx", "CertificateInspectorCard.tsx"],
        "logic": ["useLicensingEngine.ts", "aes_cek_unsealer.rs", "license_mode_evaluator.rs"],
        "types": ["CryptographicLicense.ts", "LicenseModeEnum.ts", "RevocationCrlEntry.ts"],
        "constants": ["LicensingModes.ts", "KmsKeyAliases.ts", "LicenseErrorCodes.ts"],
        "threat_focus": "Signature forgery on offline license files, CRL cache bypass, and clock roll-back tamper attacks"
    },
    "US-9.1.3": {
        "feature": "commercial-models",
        "module": "digital-products-and-licensing",
        "behaviour": "client-verification-sdks",
        "sprint": "Sprint 2.2",
        "services": ["rust_license_verifier_crate.rs", "node_cffi_wrapper.rs", "sdk_distribution_api.ts"],
        "designs": ["SdkDownloadDashboard.tsx", "SampleCodeSnippetViewer.tsx", "SdkIntegrityPill.tsx"],
        "logic": ["useLicenseVerifierSdk.ts", "tamper_resistant_evaluator.rs", "embedded_pubkey_checker.rs"],
        "types": ["SdkVerificationResult.ts", "HardwareBindingClaims.ts", "SdkTelemetryReport.ts"],
        "constants": ["SupportedPlatforms.ts", "SdkVersions.ts", "SdkErrorCodes.ts"],
        "threat_focus": "Memory patching / binary hooking of verification SDK, decompilation and key extraction"
    },
    "US-9.1.4": {
        "feature": "commercial-models",
        "module": "digital-products-and-licensing",
        "behaviour": "license-vault-ui",
        "sprint": "Sprint 2.2",
        "services": ["license_vault_client.rs", "activation_counter_service.rs", "vault_api.ts"],
        "designs": ["LicenseVaultScreen.tsx", "LicenseKeyCopyButton.tsx", "SeatAllocationMeter.tsx"],
        "logic": ["useLicenseVault.ts", "seat_activation_manager.ts", "license_expiry_formatter.ts"],
        "types": ["UserLicenseSeat.ts", "ActivationRecord.ts", "DeactivationRequest.ts"],
        "constants": ["VaultEndpoints.ts", "MaxSeatTransfers.ts", "VaultErrorCodes.ts"],
        "threat_focus": "IDOR allowing unauthorized seat revocation, license key leakage in frontend DOM rendering"
    },

    # 10-b2b-wholesale
    "US-10.1.1": {
        "feature": "commercial-models",
        "module": "b2b-wholesale",
        "behaviour": "b2b-tiered-pricing-moq",
        "sprint": "Sprint 3.1",
        "services": ["b2b_price_list_engine.rs", "moq_enforcer_service.rs", "b2b_pricing_api.ts"],
        "designs": ["TieredPricingTable.tsx", "MoqWarningAlert.tsx", "VolumeDiscountBadge.tsx"],
        "logic": ["useB2bTieredPricing.ts", "tier_threshold_matcher.rs", "minimum_order_evaluator.rs"],
        "types": ["VolumePriceTier.ts", "MoqRequirement.ts", "B2bPriceQuote.ts"],
        "constants": ["B2bPricingEndpoints.ts", "DefaultTierThresholds.ts", "PricingErrorCodes.ts"],
        "threat_focus": "Manipulating quantity in order cart to unlock wholesale price and then cancelling split items"
    },
    "US-10.1.2": {
        "feature": "commercial-models",
        "module": "b2b-wholesale",
        "behaviour": "durable-rfq-negotiation-net-terms-invoicing",
        "sprint": "Sprint 3.2",
        "services": ["rfq_negotiation_service.rs", "net_terms_invoice_generator.rs", "rfq_api.ts"],
        "designs": ["RfqCreationScreen.tsx", "BidNegotiationThread.tsx", "NetTermsInvoiceView.tsx"],
        "logic": ["useB2bRfq.ts", "credit_limit_verifier.rs", "payment_terms_state_machine.rs"],
        "types": ["RfqProposal.ts", "QuoteCounterOffer.ts", "NetTermsInvoice.ts"],
        "constants": ["RfqEndpoints.ts", "AllowedPaymentTerms.ts", "RfqErrorCodes.ts"],
        "threat_focus": "Exceeding approved corporate credit limit, unauthorized quotation approval by non-procurement officers"
    },
    "US-10.1.3": {
        "feature": "commercial-models",
        "module": "b2b-wholesale",
        "behaviour": "b2b-custom-elasticsearch-facets",
        "sprint": "Sprint 3.1",
        "services": ["b2b_facet_query_service.rs", "custom_catalog_filter.rs", "b2b_search_api.ts"],
        "designs": ["B2bWholesaleFacetBar.tsx", "BulkPackFilterPills.tsx", "CustomPriceFacetSlider.tsx"],
        "logic": ["useB2bCatalogFacets.ts", "contract_catalog_filter.rs", "restricted_item_remover.ts"],
        "types": ["B2bSearchFacet.ts", "ContractCatalogItem.ts", "B2bSearchFilterPayload.ts"],
        "constants": ["B2bSearchEndpoints.ts", "B2bFacetKeys.ts", "B2bSearchErrors.ts"],
        "threat_focus": "Cross-organization price list discovery through Elasticsearch aggregation facets"
    },
    "US-10.1.4": {
        "feature": "commercial-models",
        "module": "b2b-wholesale",
        "behaviour": "b2b-on-premise-lan-license-proxy",
        "sprint": "Sprint 3.2",
        "services": ["lan_proxy_server.rs", "air_gapped_heartbeat_sync.rs", "lan_proxy_api.ts"],
        "designs": ["LanProxyConfigScreen.tsx", "ConnectedClientsTable.tsx", "LeaseExpirationMeter.tsx"],
        "logic": ["useB2bLanProxy.ts", "local_lease_allocator.rs", "tamper_proof_token_issuer.rs"],
        "types": ["LanProxyLease.ts", "ConnectedClientRecord.ts", "AirGappedAuditLog.ts"],
        "constants": ["LanProxyPorts.ts", "MaxLeaseDurationMinutes.ts", "LanProxyErrors.ts"],
        "threat_focus": "LAN replay attacks, forged local lease tokens, and exceeding enterprise contract concurrency caps"
    },

    # 11-multi-vendor-marketplace
    "US-11.1.1": {
        "feature": "commercial-models",
        "module": "multi-vendor-marketplace",
        "behaviour": "vendor-onboarding-rbac-scoped-catalog",
        "sprint": "Sprint 4.1",
        "services": ["vendor_onboarding_service.rs", "vendor_catalog_repository.rs", "vendor_api.ts"],
        "designs": ["VendorRegistrationScreen.tsx", "VendorKycUploader.tsx", "CatalogOwnershipBadge.tsx"],
        "logic": ["useVendorCatalog.ts", "vendor_rbac_authorizer.rs", "kyc_document_checker.rs"],
        "types": ["VendorProfile.ts", "VendorKycDocument.ts", "VendorCatalogItem.ts"],
        "constants": ["VendorEndpoints.ts", "KycStatusTypes.ts", "VendorErrorCodes.ts"],
        "threat_focus": "Vendors listing counterfeit products or modifying products owned by competing vendors"
    },
    "US-11.1.2": {
        "feature": "commercial-models",
        "module": "multi-vendor-marketplace",
        "behaviour": "sub-order-splitting",
        "sprint": "Sprint 4.1",
        "services": ["sub_order_router.rs", "vendor_notification_service.rs", "sub_orders_api.ts"],
        "designs": ["SplitOrderBreakdownView.tsx", "VendorSubOrderStatusList.tsx", "DisputeActionButton.tsx"],
        "logic": ["useSubOrderSplitting.ts", "atomic_split_orchestrator.rs", "commission_split_math.rs"],
        "types": ["MasterOrder.ts", "VendorSubOrder.ts", "SplitCommissionBreakdown.ts"],
        "constants": ["SubOrderEndpoints.ts", "CommissionRates.ts", "SubOrderErrorCodes.ts"],
        "threat_focus": "Atomicity breakdown during sub-order generation causing partial payment or phantom fulfillment"
    },
    "US-11.1.3": {
        "feature": "commercial-models",
        "module": "multi-vendor-marketplace",
        "behaviour": "escrow-ledger-payouts",
        "sprint": "Sprint 4.2",
        "services": ["double_entry_ledger.rs", "vendor_payout_service.rs", "escrow_api.ts"],
        "designs": ["VendorEarningsSummaryCard.tsx", "EscrowLedgerTable.tsx", "RequestPayoutButton.tsx"],
        "logic": ["useEscrowLedger.ts", "balance_sheet_calculator.rs", "payout_hold_enforcer.rs"],
        "types": ["LedgerJournalEntry.ts", "VendorPayoutRequest.ts", "EscrowBalanceSnapshot.ts"],
        "constants": ["EscrowEndpoints.ts", "PayoutHoldDays.ts", "EscrowErrorCodes.ts"],
        "threat_focus": "Double-spend payout requests, unauthorized ledger balance inflation, and payout to unverified bank accounts"
    },
    "US-11.1.4": {
        "feature": "commercial-models",
        "module": "multi-vendor-marketplace",
        "behaviour": "vendor-portal-dashboard",
        "sprint": "Sprint 4.2",
        "services": ["vendor_metrics_service.rs", "inventory_alert_service.rs", "vendor_portal_api.ts"],
        "designs": ["VendorDashboardScreen.tsx", "SalesRevenueChart.tsx", "RecentOrdersWidget.tsx"],
        "logic": ["useVendorPortal.ts", "vendor_data_scoper.rs", "fulfillment_sla_calculator.ts"],
        "types": ["VendorSalesMetric.ts", "LowStockAlert.ts", "FulfillmentSlaMetric.ts"],
        "constants": ["VendorPortalEndpoints.ts", "MetricsIntervals.ts", "PortalErrorCodes.ts"],
        "threat_focus": "IDOR allowing vendors to view financial metrics and customer PII of other marketplace vendors"
    },

    # 12-admin-and-sdui-studio
    "US-12.1.1": {
        "feature": "administration-and-operations",
        "module": "admin-and-sdui-studio",
        "behaviour": "visual-sdui-studio",
        "sprint": "Sprint 6.1",
        "services": ["sdui_schema_publisher.rs", "layout_version_repository.rs", "sdui_studio_api.ts"],
        "designs": ["SduiStudioCanvas.tsx", "BlockPaletteSidebar.tsx", "DevicePreviewFrame.tsx"],
        "logic": ["useSduiStudio.ts", "schema_validation_engine.rs", "undo_redo_manager.ts"],
        "types": ["StudioLayoutDraft.ts", "PublishedLayoutVersion.ts", "BlockPropertyChange.ts"],
        "constants": ["StudioEndpoints.ts", "MaxDraftVersions.ts", "StudioErrorCodes.ts"],
        "threat_focus": "Stored XSS in SDUI templates, malicious script injection into client-rendered JSON blocks"
    },
    "US-12.1.2": {
        "feature": "administration-and-operations",
        "module": "admin-and-sdui-studio",
        "behaviour": "dual-edition-deployment-standard-vs-managed-instances",
        "sprint": "Sprint 5.1 / 6.1",
        "services": ["edition_scaler_service.rs", "graviton_pool_monitor.rs", "orchestration_api.ts"],
        "designs": ["EditionSwitchDashboard.tsx", "CapacityProviderGauge.tsx", "LatencyBenchmarkCard.tsx"],
        "logic": ["useDualEditionOrchestrator.ts", "capacity_rule_evaluator.rs", "provisioning_state_machine.rs"],
        "types": ["EditionConfig.ts", "GravitonCapacitySnapshot.ts", "ScalingDecision.ts"],
        "constants": ["OrchestrationEndpoints.ts", "EditionTypes.ts", "OrchestrationErrors.ts"],
        "threat_focus": "Unauthorized compute capacity scaling triggering financial denial of service on AWS bills"
    },
    "US-12.1.3": {
        "feature": "administration-and-operations",
        "module": "admin-and-sdui-studio",
        "behaviour": "white-label-mobile-build-pipeline",
        "sprint": "Sprint 6.2",
        "services": ["eas_build_trigger_service.rs", "app_icon_asset_compiler.rs", "whitelabel_api.ts"],
        "designs": ["WhitelabelConfigScreen.tsx", "BrandedThemeColorPicker.tsx", "BuildTriggerButton.tsx"],
        "logic": ["useWhitelabelPipeline.ts", "app_json_generator.rs", "signing_credential_vault.rs"],
        "types": ["WhitelabelAppConfig.ts", "EasBuildJobStatus.ts", "AppStoreListingDraft.ts"],
        "constants": ["WhitelabelEndpoints.ts", "BuildProfiles.ts", "WhitelabelErrors.ts"],
        "threat_focus": "Extraction of production Apple/Google signing certificates and provisioning profiles"
    },

    # 13-deployment-and-aws-marketplace
    "US-13.1.1": {
        "feature": "administration-and-operations",
        "module": "deployment-and-aws-marketplace",
        "behaviour": "cdk-infrastructure-stack-packaging",
        "sprint": "Sprint 5.1",
        "services": ["cdk_synth_pipeline.rs", "cloudformation_validator.rs", "packaging_api.ts"],
        "designs": ["CdkDeploymentSummaryCard.tsx", "StackOutputTable.tsx", "DriftDetectionPill.tsx"],
        "logic": ["useCdkPackaging.ts", "iam_least_privilege_checker.rs", "cloudformation_parameter_builder.ts"],
        "types": ["CdkStackParameter.ts", "DeploymentReport.ts", "SecurityGroupRuleReview.ts"],
        "constants": ["CdkStackNames.ts", "AwsRegions.ts", "PackagingErrorCodes.ts"],
        "threat_focus": "Overly permissive IAM roles (`*`), public S3 bucket misconfigurations, unencrypted storage resources"
    },
    "US-13.1.2": {
        "feature": "administration-and-operations",
        "module": "deployment-and-aws-marketplace",
        "behaviour": "aws-marketplace-listing-ftr-compliance",
        "sprint": "Sprint 5.1",
        "services": ["ftr_compliance_auditor.rs", "aws_config_rule_checker.rs", "ftr_api.ts"],
        "designs": ["FtrAuditScorecardScreen.tsx", "ComplianceChecklistWidget.tsx", "ExportReportButton.tsx"],
        "logic": ["useFtrCompliance.ts", "well_architected_evaluator.rs", "disaster_recovery_tester.rs"],
        "types": ["FtrRequirementItem.ts", "ComplianceEvidenceRecord.ts", "FtrRemediationPlan.ts"],
        "constants": ["FtrEndpoints.ts", "FtrCategories.ts", "FtrErrorCodes.ts"],
        "threat_focus": "Falsifying compliance evidence reports, hidden non-compliant security group ingress rules"
    },
    "US-13.1.3": {
        "feature": "administration-and-operations",
        "module": "deployment-and-aws-marketplace",
        "behaviour": "saas-metering-usage-based-billing",
        "sprint": "Sprint 5.1",
        "services": ["marketplace_metering_client.rs", "usage_event_aggregator.rs", "metering_api.ts"],
        "designs": ["UsageBillingDashboard.tsx", "DimensionMeterGauge.tsx", "InvoiceDisputeSheet.tsx"],
        "logic": ["useSaasMetering.ts", "metering_signature_builder.rs", "batch_meter_reconciler.rs"],
        "types": ["UsageMeteringDimension.ts", "BatchMeterUsagePayload.ts", "MeterUsageResult.ts"],
        "constants": ["MeteringEndpoints.ts", "MarketplaceDimensions.ts", "MeteringErrorCodes.ts"],
        "threat_focus": "Under-reporting customer API usage to avoid licensing fees, duplicate event submission for overbilling"
    }
}

MODULE_DIRS = [
    "01-auth-and-onboarding", "02-storefront-and-catalog", "03-cart-and-checkout",
    "04-payments-and-cod", "05-fulfillment-and-shipping", "06-orders-and-returns",
    "07-customer-account", "08-webmcp-and-ai", "09-digital-products-and-licensing",
    "10-b2b-wholesale", "11-multi-vendor-marketplace", "12-admin-and-sdui-studio",
    "13-deployment-and-aws-marketplace"
]

def get_git_content(ref, path):
    try:
        return subprocess.check_output(["git", "show", f"{ref}:{path}"]).decode("utf-8")
    except Exception:
        return None

def main():
    total_processed = 0

    for mod_dir in MODULE_DIRS:
        readme_raw = get_git_content("3041332", f"docs/user-stories/{mod_dir}/README.md")
        if not readme_raw:
            print(f"Failed to read 3041332:docs/user-stories/{mod_dir}/README.md")
            continue

        raw_stories = re.split(r'\n(?=## US-[\d\.]+)', readme_raw)[1:]

        for raw_s in raw_stories:
            m_id = re.search(r'##\s+(US-[\d\.]+):?\s*(.*)', raw_s)
            if not m_id:
                continue

            story_id = m_id.group(1)
            story_title = m_id.group(2).strip()

            meta = STORY_MAP.get(story_id)
            if not meta:
                print(f"Skipping {story_id}: not in STORY_MAP")
                continue

            feature_name = meta["feature"]
            module_name = meta["module"]
            behaviour_name = meta["behaviour"]
            sprint_str = meta["sprint"]

            # Extract narrative
            narr_m = re.search(r'(\*\*As an?\*\*[\s\S]*?)(?=\n#+\s*Acceptance Criteria)', raw_s)
            narrative = narr_m.group(1).strip() if narr_m else ""

            # Extract Acceptance Criteria
            ac_m = re.search(r'#+\s*Acceptance Criteria\s*\n\n([\s\S]*?)(?=\n#+\s*Test Cases)', raw_s)
            ac_raw = ac_m.group(1).strip() if ac_m else ""

            # Tag scenarios with [AC-US-X.Y.Z-NN]
            sc_count = 1
            def tag_scenario(match):
                nonlocal sc_count
                title = match.group(1).strip()
                res = f"  Scenario: [AC-{story_id}-{sc_count:02d}] {title}"
                sc_count += 1
                return res

            ac_processed = re.sub(r'^\s*Scenario:\s*(?:\[AC-[^\]]+\]\s*)?([^\n]+)', tag_scenario, ac_raw, flags=re.MULTILINE)

            # Extract Test Cases
            tc_m = re.search(r'#+\s*Test Cases\s*\n\n([\s\S]*?)(?=\n#+\s*Activity Diagram)', raw_s)
            tc_body = tc_m.group(1).strip() if tc_m else ""

            # Extract Activity Diagram
            diag_m = re.search(r'#+\s*Activity Diagram\s*\n\n([\s\S]*?)(?=\n---\n|\n#+\s*Sliced|\n#+\s*Validation|$)', raw_s)
            diag_body = diag_m.group(1).strip() if diag_m else ""

            services_list = "\n".join([f"│   │   ├── {s}" for s in meta["services"]])
            designs_list = "\n".join([f"│   │   ├── {d}" for d in meta["designs"]])
            logic_list = "\n".join([f"│   │   ├── {l}" for l in meta["logic"]])
            types_list = "\n".join([f"│   │   ├── {t}" for t in meta["types"]])
            constants_list = "\n".join([f"│   │   ├── {c}" for c in meta["constants"]])

            file_slug = f"{story_id.lower()}-{re.sub(r'[^a-z0-9]+', '-', story_title.lower()).strip('-')}.md"
            out_file_path = os.path.join("docs/user-stories", mod_dir, file_slug)

            story_md = f"""# {story_id}: {story_title}

> **Spec Kit Specification**: [Specification Lifecycle Active (.specify/)](../../../.specify/memory/constitution.md)  
> **Domain Feature**: `{feature_name}`  
> **Domain Module**: `{module_name}`  
> **Autonomous Behaviour**: `{behaviour_name}`  
> **Client Framework Path**: `apps/storefront/src/features/{feature_name}/modules/{module_name}/behaviours/{behaviour_name}`  
> **Backend Framework Path**: `backend/src/features/{feature_name}/modules/{module_name}/behaviours/{behaviour_name}`  
> **Execution Sprint**: [{sprint_str}](../../sprints/README.md)  
> **Slicing Standard**: [7-PR Vertical Slicing Framework](../../sprints/README.md#the-7-pr-vertical-slicing-standard)  
> **Security Gateway**: [ASVS Level 2 Verification Gate (security-audit)](#5-security-gateway-powered-by-security-audit)

---

## 1. Spec Kit Specification: User Story & Domain Scope

### 1.1 User Story Narrative

{narrative}

### 1.2 Acceptance Criteria (Gherkin Scenarios)

{ac_processed}

### 1.3 Test Cases & Traceability Matrix

{tc_body}

---

## 2. Behavior-Centric Architecture & Folder Blueprint

This user story is implemented directly inside the respective **Expo client** and **Cargo Lambda Axum backend** frameworks according to the **Locality of Behavior (LoB)** architectural law. Private services, designs, logic, types, and constants are strictly colocated within their framework behaviour directory.

### 2.1 Colocated Behaviour Directory Tree

#### Client Architecture (Universal Expo SDK 58):
```
apps/storefront/src/features/{feature_name}/modules/{module_name}/behaviours/{behaviour_name}/
├── services/
{services_list}
├── designs/
{designs_list}
├── logic/
{logic_list}
├── types/
{types_list}
└── constants/
{constants_list}
```

#### Backend Architecture (Cargo Lambda + Axum 0.8):
```
backend/src/features/{feature_name}/modules/{module_name}/behaviours/{behaviour_name}/
├── services/
{services_list}
├── logic/
{logic_list}
├── types/
{types_list}
└── constants/
{constants_list}
```

### 2.2 Scoping & Promotion Blueprint

| Layer / Tier | Client Path (Expo) | Backend Path (Cargo Lambda / Axum) | Purpose & Promotion Rules |
| :--- | :--- | :--- | :--- |
| **Behaviour-Local** | `.../behaviours/{behaviour_name}/` | `.../behaviours/{behaviour_name}/` | **Default Private Scope**: Colocated services, designs, logic, types, and constants private to this story. |
| **Module-Shared** | `.../modules/{module_name}/_shared/` | `.../modules/{module_name}/_shared/` | Shared domain primitives and UI elements used by $\ge 2$ behaviours in `{module_name}`. |
| **Feature-Shared** | `.../features/{feature_name}/_shared/` | `.../features/{feature_name}/_shared/` | Feature-level contracts, ports, and cross-module bridges across `{feature_name}`. |
| **Framework-Shared** | `apps/storefront/src/shared/` | `backend/crates/kernel-core/` | System-wide microkernel traits, `Money` arithmetic, RFC 9110 ETag middleware, and database adapters. |

---

## 3. Technical Implementation Plan (Spec Kit Plan)

### 3.1 Domain Invariants & Storage Schema
- **State Machine**: Enforces valid state transitions and rejects unauthorized or out-of-order mutations.
- **Data Persistence**: Single-table Amazon DynamoDB partitioning (`PK = TENANT#<id>`, `SK = ENTITY#<id>`) paired with reactive local-first WatermelonDB sync.
- **Freshness & Caching**: Multi-tier caching (L1 Moka in-memory + L2 ElastiCache Redis) with RFC 9110 `ETag` conditional `304 Not Modified` short-circuiting.

### 3.2 Activity & Interaction Diagram

{diag_body}

---

## 4. Granular Implementation Tasks (Spec Kit Tasks)

### Phase 1: Core Domain Logic, Types & Constants
- [ ] **Task 1.1 (Types)**: Define strongly typed models and DTO schemas in `types/`.
- [ ] **Task 1.2 (Constants)**: Define routes, action codes, and validation limits in `constants/`.
- [ ] **Task 1.3 (Logic)**: Implement pure business logic, calculations, and state machines in `logic/`.
- [ ] **Task 1.4 (Unit Tests)**: Write pure property-based and unit tests verifying domain invariants.

### Phase 2: Services & Infrastructure Adapters
- [ ] **Task 2.1 (API / Gateway)**: Implement client adapters and backend handlers in `services/`.
- [ ] **Task 2.2 (ETag & Cache)**: Integrate RFC 9110 ETag headers and multi-tier caching (Moka L1 / Redis L2).
- [ ] **Task 2.3 (Storage & Sync)**: Implement DynamoDB storage operations and WatermelonDB delta sync.
- [ ] **Task 2.4 (Integration Tests)**: Verify service contract tests and real database conditional writes.

### Phase 3: Platform-Adaptive Designs & UI
- [ ] **Task 3.1 (UI Presentation)**: Build platform-adaptive screens and SDUI components in `designs/`.
- [ ] **Task 3.2 (Headless Hooks)**: Bind headless domain hooks from `logic/` into the UI presentation.
- [ ] **Task 3.3 (i18n & RTL)**: Implement bidirectional RTL/LTR layout mirroring and localized font switching.
- [ ] **Task 3.4 (Component Tests)**: Test empty, loading, offline, and error states across web and mobile.

### Phase 4: Security Gateway Verification & Release Readiness
- [ ] **Task 4.1 (Abuse Testing)**: Execute automated adversarial penetration tests against the threat matrix.
- [ ] **Task 4.2 (Zero-Trust Audit)**: Verify strict tenant isolation and object-level authorization (IDOR).
- [ ] **Task 4.3 (SAST & Audit)**: Run static analysis, dependency audit, and secret scanning.
- [ ] **Task 4.4 (Gate Sign-Off)**: Obtain independent security sign-off for the G2 Security Gateway.

---

## 5. Security Gateway (Powered by security-audit)

### 5.1 Trust Boundaries & Security Actors
- **Trust Boundaries**:
  - `Untrusted Zone`: Mobile client app, public web browser, and external network callers.
  - `Gateway Edge`: AWS CloudFront, API Gateway, and Cognito JWT authentication guard.
  - `Secure Application Boundary`: Axum Tower route extractors enforcing tenant and RBAC/ABAC isolation.
  - `Encrypted Storage & Secret Vault`: Amazon DynamoDB KMS-encrypted tables and AWS KMS vault.
- **Authorized Principals**:
  - Identified Actors: `AuthenticatedCustomer`, `B2bBuyer`, `Vendor`, `StoreAdmin`, or `AnonymousShopper` (read-only).
  - Multi-Tenancy Invariant: Every request must extract `tenant_id` from verified JWT claims. Injections via query params or payload body are rejected with `403 Forbidden`.

### 5.2 Threat Modeling & Abuse Matrix (STRIDE / ASVS)

| Threat Vector | Severity | Vulnerability Mechanism | Mitigating Control & Security Invariant |
| :--- | :--- | :--- | :--- |
| **Spoofing & Impersonation** | Critical | Forged `sub` or `tenant_id` identity claims | Server-side RS256 JWKS signature verification; strict claims extraction in Axum. |
| **Tampering & Invariant Bypass** | High | Manipulating payload parameters or prices | Authoritative server recalculation; strict schema validation; BLAKE3 ETag integrity checks. |
| **Information Disclosure (IDOR)** | Critical | Cross-tenant or cross-user data scraping | Explicit `PK = TENANT#<id>` partition filtering on every database and cache operation. |
| **Denial of Service / Abuse** | High | {meta['threat_focus']} | Token-bucket rate limiting per IP and account; strict input length validation. |
| **Elevation of Privilege** | Critical | Bypassing role-based permission checks | Tower extractors (`RequireStoreAdmin`, `RequireVendor`) guard sensitive endpoints. |

### 5.3 Cryptographic & Data Protection Controls
- **Encryption in Transit**: TLS 1.3 enforced on all external and internal endpoints; HSTS active.
- **Encryption at Rest**: DynamoDB AWS KMS customer-managed keys; AES-256-GCM for sensitive client tokens in `expo-secure-store`.
- **PII & Secret Redaction**: Passwords, OTPs, auth tokens, and credit card numbers are stripped from logs and traces via `tracing` redaction filters.

### 5.4 Automated Security Verification Checklist
- [ ] **SAST Analysis**: Clean report from static code analyzers; 0 high or critical vulnerabilities.
- [ ] **Dependency Audit**: `cargo deny` and `bun audit` pass with 0 unreviewed security advisories.
- [ ] **Abuse & IDOR Fuzzing**: Test suite confirms that requests with modified `tenant_id` or `user_id` fail with `401 Unauthorized` or `403 Forbidden`.
- [ ] **Secret Scanning**: Gitleaks scanner confirms zero hardcoded credentials, API keys, or private keys.

### 5.5 Security Gateway (G2) Sign-Off Checklist
- [ ] Threat boundary and entry points verified against OWASP ASVS Level 2 requirements.
- [ ] Multi-tenant isolation verified with automated cross-tenant penetration test.
- [ ] Anti-abuse and rate limiting confirmed active on all public interfaces.
- [ ] Audit log redaction verified — zero plaintext secrets in output logs.
- [ ] Independent reviewer sign-off obtained; zero open Critical or High findings.

---

## 6. Validation Gates & Acceptance Sign-Off

**Status: Pending — specification only; no implementation evidence.** All [G0–G4 quality gates](../../QUALITY_GATES.md) apply to this story. The following checks add to its acceptance criteria and test cases; they do not replace them.

### G1 — Test coverage
- [ ] **{story_id}-G1:** Automated test suite maps 100% of acceptance criteria and test cases with >=90% line and >=85% branch coverage in affected packages.

### G2 — Security audit
- [ ] **{story_id}-G2:** Verify zero-trust tenant isolation, object-level authorization (IDOR), and defense against {meta['threat_focus']}. No unresolved critical or high findings.

### G3 — Architecture and maintainability
- [ ] **{story_id}-G3:** Strict compliance with framework colocation (`apps/storefront/src/features/` or `backend/src/features/`), zero-clone borrowing discipline in Rust, and clean domain boundaries.

### G4 — Integrated acceptance
- [ ] **{story_id}-G4:** End-to-end user journey validation across supported platforms (Web, iOS, Android) and verified sandbox integration.

---

[← Back to Module {module_name} Catalog (README.md)](README.md) | [Master User Stories Index](../README.md)
"""
            with open(out_file_path, "w", encoding="utf-8") as f:
                f.write(story_md)
            total_processed += 1

    print(f"Successfully generated {total_processed} individual Spec Kit user story specifications!")

if __name__ == "__main__":
    main()
