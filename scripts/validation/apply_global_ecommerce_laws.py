#!/usr/bin/env python3
"""
Applies tailored, comprehensive Global E-Commerce Legal & Regulatory Compliance
requirements across all 51 user stories in some-commerce.
"""

import os
import re
from pathlib import Path

# Mapping of story_id to (title, scenario_text, tc_description, glaw_checklist)
GLOBAL_LAWS = {
    "US-1.1.1": {
        "title": "Global privacy, telecommunications consent, and age-gating compliance",
        "scenario": """  Scenario: [AC-US-1.1.1-LAW] Global e-commerce legal compliance and data protection regulations
    Given an international user initiating phone OTP authentication
    When evaluated against international privacy, telecommunications, and consumer protection laws
    Then phone numbers must be processed under GDPR Art 6 lawful basis with strict data minimization
    And SMS OTP transmission must comply with US TCPA and EU ePrivacy Directive carrier consent rules without unconsented marketing
    And anti-abuse rate limiting must prevent unauthorized toll fraud and SMS pumping without collecting unauthorized PII
    And age verification boundaries must enforce COPPA (under 13) and GDPR Art 8 (under 16) parental consent safeguards""",
        "tc": "Global legal & regulatory compliance (GDPR Art 6/7/8 lawful basis, ePrivacy/TCPA SMS consent, COPPA age gate)",
        "glaw": """### G-Law — Law validation
- [ ] **US-1.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR (Art 6/7/8 lawful basis & age gating), US TCPA / EU ePrivacy telecommunications consent, and data minimization; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-1.1.2": {
        "title": "Cryptographic credential security, FIDO2/eIDAS compliance, and breach notification",
        "scenario": """  Scenario: [AC-US-1.1.2-LAW] Global e-commerce legal compliance and authentication security regulations
    Given user registration or authentication using Passkeys or passwords
    When evaluated against international authentication and security standards
    Then biometric data must remain exclusively on the local authenticator hardware per FIDO2 and eIDAS (Regulation 910/2014) specifications
    And stored passwords must be hashed using memory-hard Argon2id with unique salts under GDPR Art 32 security of processing
    And credential failure telemetry must support mandatory 72-hour breach disclosure reporting under GDPR Art 33""",
        "tc": "Global legal & regulatory compliance (FIDO2/eIDAS biometric boundary, GDPR Art 32 Argon2id, Art 33 breach notification)",
        "glaw": """### G-Law — Law validation
- [ ] **US-1.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: FIDO2 / eIDAS biometric privacy boundaries, GDPR Art 32 cryptographic security, and Art 33 breach notification readiness; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-1.1.3": {
        "title": "OIDC scope data minimization, cross-border transfer, and account unlinking",
        "scenario": """  Scenario: [AC-US-1.1.3-LAW] Global e-commerce legal compliance and third-party identity transfer regulations
    Given a user authenticating via third-party Identity Providers (Google, Apple)
    When exchanging identity claims across international borders
    Then identity token requests must be restricted to minimal necessary scopes (sub, email) per GDPR Art 5(1)(c)
    And international identity exchanges must comply with EU-US Data Privacy Framework (DPF) transfer rules
    And users must be provided with an immediate self-service mechanism to unlink third-party credentials without data loss""",
        "tc": "Global legal & regulatory compliance (GDPR Art 5(1)(c) scope minimization, EU-US DPF transfer rules, Apple ID unlinking)",
        "glaw": """### G-Law — Law validation
- [ ] **US-1.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR scope data minimization, EU-US DPF cross-border data protection, and platform third-party unlinking rights; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-1.1.4": {
        "title": "Corporate KYB due diligence, VIES VAT verification, and trade sanctions screening",
        "scenario": """  Scenario: [AC-US-1.1.4-LAW] Global e-commerce legal compliance and B2B corporate verification regulations
    Given an enterprise submitting a B2B organization registration
    When vetted prior to administrative onboarding approval
    Then corporate entity credentials and VAT registration numbers must be validated against official registries (e.g., EU VIES)
    And corporate officers and beneficial owners must be screened against OFAC and EU international trade sanctions lists
    And an immutable audit trail of verification evidence must be recorded for statutory Anti-Money Laundering (AMLD) audits""",
        "tc": "Global legal & regulatory compliance (EU AMLD KYB due diligence, VIES VAT validation, OFAC/EU trade sanctions screening)",
        "glaw": """### G-Law — Law validation
- [ ] **US-1.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU AMLD corporate KYB verification, VIES VAT registry confirmation, and international trade sanctions screening; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-2.1.1": {
        "title": "Universal digital accessibility, bilingual consumer parity, and cookie consent",
        "scenario": """  Scenario: [AC-US-2.1.1-LAW] Global e-commerce legal compliance and universal digital accessibility regulations
    Given a consumer accessing the storefront via web or mobile devices
    When rendering dynamic SDUI layouts across locales (Arabic RTL, English LTR)
    Then all UI elements must conform to WCAG 2.1 Level AA and the European Accessibility Act (EAA Directive 2019/882)
    And touch targets must maintain minimum 44x44pt hit areas with 4.5:1 accessible color contrast
    And zero non-essential client storage tracking or analytics may execute without prior affirmative consent under ePrivacy""",
        "tc": "Global legal & regulatory compliance (European Accessibility Act Directive 2019/882, ADA Title III, ePrivacy consent)",
        "glaw": """### G-Law — Law validation
- [ ] **US-2.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: European Accessibility Act (EAA Directive 2019/882), US ADA Title III (WCAG 2.1 AA), and ePrivacy cookie/storage consent; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-2.1.2": {
        "title": "Age-restricted goods classification, trademark protection, and illegal content prevention",
        "scenario": """  Scenario: [AC-US-2.1.2-LAW] Global e-commerce legal compliance and regulated goods classification laws
    Given the product category taxonomy and brand catalog structure
    When categorizing regulated, branded, or age-restricted merchandise
    Then age-restricted merchandise (alcohol, tobacco, adult goods) must enforce mandatory age-verification classification flags
    And category structures must support trademark protection and counterfeit reporting under EU DSA notice-and-action rules
    And restricted categories must prevent deceptive reclassification to bypass municipal commerce prohibitions""",
        "tc": "Global legal & regulatory compliance (EU Digital Services Act trademark protection, age-restricted goods statutory gating)",
        "glaw": """### G-Law — Law validation
- [ ] **US-2.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Digital Services Act (DSA Regulation 2022/2065), trademark infringement notice-and-action, and age-restricted goods classification; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-2.1.3": {
        "title": "Mandatory product safety labeling, energy efficiency disclosures, and allergen declarations",
        "scenario": """  Scenario: [AC-US-2.1.3-LAW] Global e-commerce legal compliance and mandatory product safety disclosures
    Given product property schemas and filter widgets configured in the admin catalog
    When applied to consumer-facing product listings
    Then mandatory statutory disclosures (CE marks, manufacturer contact, GPSR traceability, energy efficiency ratings) must be enforced
    And food, cosmetics, and chemical listings must require verifiable ingredient and allergen property fields per FDA and EU FIC
    And catalog filter widgets must never allow concealment or suppression of legally required product safety warnings""",
        "tc": "Global legal & regulatory compliance (EU GPSR 2023/988 product safety, EU Energy Labeling 2017/1369, FDA/FIC allergen rules)",
        "glaw": """### G-Law — Law validation
- [ ] **US-2.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU General Product Safety Regulation (GPSR 2023/988), mandatory energy efficiency labeling, and food/cosmetic allergen declarations; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-2.1.4": {
        "title": "Search ranking transparency, anti-deceptive promotion, and P2B algorithmic fairness",
        "scenario": """  Scenario: [AC-US-2.1.4-LAW] Global e-commerce legal compliance and algorithmic search transparency regulations
    Given a consumer executing search queries or applying faceted filters across the catalog
    When search results and algorithmic ranking orders are generated
    Then the main parameters determining search ranking must be publicly disclosed in plain language per EU P2B Art 7 and DSA Art 27
    And sponsored or paid product placements must be unambiguously labeled as advertisements
    And search faceting algorithms must not covertly manipulate organic search results through deceptive dark patterns""",
        "tc": "Global legal & regulatory compliance (EU P2B Regulation Art 7 ranking transparency, DSA Art 27, FTC search guidance)",
        "glaw": """### G-Law — Law validation
- [ ] **US-2.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Platform-to-Business (P2B 2019/1150) ranking transparency, EU DSA Art 27 recommender disclosures, and anti-deceptive search promotion; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-2.1.5": {
        "title": "EU Omnibus Directive 30-day prior pricing, unit price indication, and total price transparency",
        "scenario": """  Scenario: [AC-US-2.1.5-LAW] Global e-commerce legal compliance and pricing transparency regulations
    Given a consumer viewing a product detail page with price discounts and variant selections
    When calculating and displaying variant pricing and promotional badges
    Then any discount claim must display the prior lowest price applied during a period not less than 30 days prior (EU Omnibus Art 6a)
    And standard unit pricing (e.g. price per kg, liter, or meter) must be displayed where required by the Price Indication Directive
    And the displayed product price must clearly indicate tax inclusion (VAT) or explicit jurisdictional tax terms""",
        "tc": "Global legal & regulatory compliance (EU Omnibus Directive 2019/2161 Art 6a 30-day baseline, Price Indication Directive 98/6/EC)",
        "glaw": """### G-Law — Law validation
- [ ] **US-2.1.5-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Omnibus Directive (Art 6a 30-day discount baseline), EU Price Indication Directive (unit pricing), and GPSR manufacturer traceability; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-3.1.1": {
        "title": "Offline data protection, transparent cart expiration, and price guarantee integrity",
        "scenario": """  Scenario: [AC-US-3.1.1-LAW] Global e-commerce legal compliance and consumer cart integrity regulations
    Given a user adding items to an offline-first cart stored in local SQLite
    When the client synchronizes cached cart data with the cloud server
    Then client-side storage must be encrypted and restricted strictly to cart identifiers without accumulating unconsented PII
    And price discrepancies arising from offline cache expiration must be transparently disclosed to the consumer before checkout
    And cached pricing must not be covertly altered or inflated without explicit consumer acknowledgement""",
        "tc": "Global legal & regulatory compliance (GDPR Art 5 data minimization, consumer price lock disclosures, anti-deceptive trade practices)",
        "glaw": """### G-Law — Law validation
- [ ] **US-3.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR client data minimization, transparent cart price lock terms, and anti-deceptive pricing safeguards; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-3.1.2": {
        "title": "Clear seller identity disclosure, transparent shipping breakdown, and anti-drip pricing",
        "scenario": """  Scenario: [AC-US-3.1.2-LAW] Global e-commerce legal compliance and multi-vendor cost transparency regulations
    Given a multi-vendor cart containing items from independent marketplace merchants
    When estimating shipping fees and grouping orders by vendor
    Then the legal identity and physical business address of each third-party seller must be clearly disclosed
    And shipping, customs, and handling fees must be itemized per vendor with zero hidden or surprise fees (anti-drip pricing)
    And separate contractual commitments per vendor must be made explicitly clear to the consumer prior to order submission""",
        "tc": "Global legal & regulatory compliance (EU Consumer Rights Directive total price transparency, FTC hidden fee/drip pricing ban)",
        "glaw": """### G-Law — Law validation
- [ ] **US-3.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Consumer Rights Directive (Directive 2011/83/EU), FTC hidden fee / drip pricing prohibition, and US INFORM Consumers Act seller disclosure; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-3.1.3": {
        "title": "Statutory order button labeling, pre-contractual summary, and prohibition of pre-ticked boxes",
        "scenario": """  Scenario: [AC-US-3.1.3-LAW] Global e-commerce legal compliance and checkout contract formation regulations
    Given a consumer progressing through the final checkout confirmation screen
    When presenting order totals and the final commitment trigger
    Then the final commitment button must be unambiguously labeled "Pay now" or "Order with obligation to pay" (Button-Lösung)
    And pre-ticked checkboxes for add-on warranties, expedited shipping, or optional services are strictly prohibited
    And an exhaustive pre-contractual summary displaying total price inclusive of taxes, delivery costs, and cancellation terms must be visible""",
        "tc": "Global legal & regulatory compliance (EU Consumer Rights Directive Art 8(2) button solution, pre-ticked box prohibition)",
        "glaw": """### G-Law — Law validation
- [ ] **US-3.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Consumer Rights Directive Art 8 (unambiguous button labeling), prohibition of pre-ticked optional checkboxes, and pre-contractual cost summary; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-3.1.4": {
        "title": "Address data privacy, Universal Postal Union standards, and trade embargo screening",
        "scenario": """  Scenario: [AC-US-3.1.4-LAW] Global e-commerce legal compliance and address verification regulations
    Given a user creating or modifying delivery addresses across multiple jurisdictions
    When validating and persisting localized address records
    Then customer delivery addresses must be protected under GDPR/CCPA with access restricted strictly to fulfillment necessity
    And address validation must conform to Universal Postal Union (UPU) postal formatting across international destinations
    And destination countries and postal codes must be verified against international export sanctions and trade embargo restrictions""",
        "tc": "Global legal & regulatory compliance (GDPR address protection, UPU postal standards, OFAC/EU trade sanctions checks)",
        "glaw": """### G-Law — Law validation
- [ ] **US-3.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR/CCPA customer address privacy, Universal Postal Union formatting standards, and destination trade embargo screening; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-4.1.1": {
        "title": "PCI-DSS v4.0 tokenization, PSD2/PSD3 Strong Customer Authentication, and credit card surcharge prohibition",
        "scenario": """  Scenario: [AC-US-4.1.1-LAW] Global e-commerce legal compliance and electronic payment regulations
    Given a consumer initiating an online prepaid card payment via Stripe or Paymob
    When processing the credit or debit card transaction
    Then cardholder data must be tokenized directly at the PCI-DSS compliant gateway iframe with zero raw PAN/CVV touching servers
    And Strong Customer Authentication (3D Secure 2.x) must be enforced for all applicable European and SCA-mandated card payments
    And payment surcharges on consumer debit and credit cards are strictly prohibited pursuant to EU PSD2 Art 62(4)""",
        "tc": "Global legal & regulatory compliance (PCI-DSS v4.0 SAQ-A tokenization, EU PSD2/PSD3 SCA 3DS2, card surcharge prohibition)",
        "glaw": """### G-Law — Law validation
- [ ] **US-4.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: PCI-DSS v4.0 SAQ-A compliance, EU PSD2/PSD3 Strong Customer Authentication (SCA), and prohibition of consumer payment surcharges; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-4.1.2": {
        "title": "National AML statutory cash transaction limits, fiscal cash receipts, and consumer refusal rights",
        "scenario": """  Scenario: [AC-US-4.1.2-LAW] Global e-commerce legal compliance and cash transaction ceiling regulations
    Given a customer placing an order with 100% Cash on Delivery
    When dispatching the order and collecting physical cash upon delivery
    Then orders exceeding national statutory AML cash payment ceilings must be blocked automatically from selecting COD
    And the courier must issue a legally binding fiscal cash receipt or stamped payment voucher immediately upon cash collection
    And consumer statutory rights to inspect goods and exercise pre-delivery withdrawal without penalty must be preserved""",
        "tc": "Global legal & regulatory compliance (National AML cash limits e.g. EU €1,000-€5,000, mandatory fiscal cash receipts)",
        "glaw": """### G-Law — Law validation
- [ ] **US-4.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: national statutory Anti-Money Laundering cash caps, mandatory fiscal cash receipt delivery, and consumer refusal rights; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-4.1.3": {
        "title": "Deposit forfeiture disclosure, split tax apportionment, and anti-structuring AML compliance",
        "scenario": """  Scenario: [AC-US-4.1.3-LAW] Global e-commerce legal compliance and split payment regulations
    Given a customer choosing split payment (upfront card deposit plus remainder on COD)
    When recording the transaction across dual payment channels
    Then terms governing deposit forfeiture or refundability upon delivery rejection must be disclosed clearly before payment
    And value-added tax (VAT) must be accurately apportioned across the deposit invoice and final COD fiscal settlement
    And split payment structures must comply with financial AML anti-structuring safeguards preventing illicit cash evasion""",
        "tc": "Global legal & regulatory compliance (Deposit terms disclosure, VAT apportionment accuracy, AML anti-structuring compliance)",
        "glaw": """### G-Law — Law validation
- [ ] **US-4.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: consumer deposit disclosure rules, accurate multi-tender tax apportionment, and AML anti-structuring compliance; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-4.1.4": {
        "title": "Payment gateway credential vaulting, central bank regulations, and PCI key lifecycle management",
        "scenario": """  Scenario: [AC-US-4.1.4-LAW] Global e-commerce legal compliance and payment gateway administration regulations
    Given an administrator configuring payment provider gateways and API credentials
    When storing or rotating payment gateway secrets in the management console
    Then gateway API keys, webhook signing secrets, and merchant credentials must be encrypted in KMS with strict access logging
    And payment routing configurations must adhere to national central bank payment service provider (PSP) regulatory operating mandates
    And administrative credential modifications must maintain an immutable audit trail for annual PCI-DSS compliance audits""",
        "tc": "Global legal & regulatory compliance (PCI-DSS Requirement 3 key management, central bank PSP regulations, KMS secret vaulting)",
        "glaw": """### G-Law — Law validation
- [ ] **US-4.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: PCI-DSS v4.0 Requirement 3 cryptographic key management, central bank PSP regulations (CBE, SAMA, FCA), and immutable access logging; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-4.1.5": {
        "title": "Virtual asset travel rule compliance, EU MiCA regulation, and cryptocurrency transaction transparency",
        "scenario": """  Scenario: [AC-US-4.1.5-LAW] Global e-commerce legal compliance and virtual asset payment regulations
    Given a customer selecting Bitcoin or Lightning Network payment via BTCPay Server
    When generating the payment invoice and confirming blockchain settlement
    Then cryptocurrency transactions must comply with FATF Travel Rule requirements and EU MiCA regulations for merchant processing
    And cryptocurrency exchange rates, network mining fees, and price expiration windows must be disclosed explicitly
    And refund terms must clearly specify whether statutory reversals occur in fiat equivalent or original digital asset amounts""",
        "tc": "Global legal & regulatory compliance (FATF Travel Rule, EU MiCA Regulation 2023/1114, crypto invoice price transparency)",
        "glaw": """### G-Law — Law validation
- [ ] **US-4.1.5-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Markets in Crypto-Assets (MiCA Regulation 2023/1114), FATF Travel Rule compliance, and cryptocurrency refund transparency; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-5.1.1": {
        "title": "Postal regulatory courier licensing, cash escrow fiduciary compliance, and courier receipt delivery",
        "scenario": """  Scenario: [AC-US-5.1.1-LAW] Global e-commerce legal compliance and domestic courier delivery regulations
    Given domestic parcel fulfillment dispatched via Bosta with cash collection
    When couriers handle parcels and collect physical COD funds
    Then courier integration must comply with national postal authority transport documentation and licensing requirements
    And collected COD cash must be held under strict fiduciary escrow accounting prior to merchant disbursement
    And couriers must provide immediate physical or electronic proof of delivery (POD) and fiscal payment receipt to the customer""",
        "tc": "Global legal & regulatory compliance (National postal regulatory compliance, courier cash escrow accounting, proof of delivery receipts)",
        "glaw": """### G-Law — Law validation
- [ ] **US-5.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: national postal courier licensing regulations, fiduciary COD cash escrow management, and legally binding proof of delivery; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-5.1.2": {
        "title": "Cross-border customs declarations, Harmonized System tariff codes, and EU IOSS VAT compliance",
        "scenario": """  Scenario: [AC-US-5.1.2-LAW] Global e-commerce legal compliance and international trade customs regulations
    Given international express consignments handled via Aramex or DHL
    When generating cross-border waybills and customs documentation
    Then every parcel must generate an automated commercial invoice and CN22/CN23 customs declaration with validated HS tariff codes
    And low-value consignments destined for the EU (<= 150 EUR) must incorporate valid IOSS identification to prevent double taxation
    And export control verification must ensure no prohibited, restricted, or sanctioned commodities are dispatched across borders""",
        "tc": "Global legal & regulatory compliance (WCO Harmonized System HS tariff codes, EU IOSS VAT compliance, CN22/CN23 customs documentation)",
        "glaw": """### G-Law — Law validation
- [ ] **US-5.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: World Customs Organization (WCO) HS tariff classification, EU IOSS VAT rules, and cross-border export control compliance; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-5.1.3": {
        "title": "Universal postal conventions, carrier liability limitations, and dangerous goods declarations",
        "scenario": """  Scenario: [AC-US-5.1.3-LAW] Global e-commerce legal compliance and multi-carrier transport liability regulations
    Given multi-carrier rate calculation and label generation via Shippo or EasyPost
    When contracting carriage across diverse regional and international couriers
    Then declared merchandise values and liability limits must be recorded in accordance with international carriage conventions (CMR, Montreal)
    And shipments containing restricted items (e.g., lithium batteries) must generate mandatory hazardous goods transport declarations
    And cross-carrier delivery terms and transit liability allocations must be transparently recorded before label issuance""",
        "tc": "Global legal & regulatory compliance (Universal Postal Union conventions, CMR/Montreal transport liability, dangerous goods declarations)",
        "glaw": """### G-Law — Law validation
- [ ] **US-5.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: Universal Postal Union (UPU) acts, international transport liability conventions (CMR, Montreal), and dangerous goods shipping rules; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-5.1.4": {
        "title": "Telecommunications carrier compliance, transactional vs marketing exemptions, and sender ID regulations",
        "scenario": """  Scenario: [AC-US-5.1.4-LAW] Global e-commerce legal compliance and transactional notification regulations
    Given automated milestone notifications dispatched via AWS SNS push and SMS
    When alerting customers of parcel dispatch, out-for-delivery, and delivery completion
    Then notifications must be strictly restricted to transactional shipping updates and must not include unconsented marketing solicitations
    And SMS messages must transmit via verified registered sender IDs adhering to national telecommunications registry standards
    And quiet hours regulations for customer text communications must be respected based on the recipient's geographic time zone""",
        "tc": "Global legal & regulatory compliance (US TCPA transactional exemption, EU ePrivacy marketing separation, carrier sender ID registry)",
        "glaw": """### G-Law — Law validation
- [ ] **US-5.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: US TCPA / EU ePrivacy transactional communication standards, verified sender ID compliance, and time zone quiet hours rules; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-6.1.1": {
        "title": "Statutory 30-day delivery deadline, loss-in-transit risk allocation, and dispatch transparency",
        "scenario": """  Scenario: [AC-US-6.1.1-LAW] Global e-commerce legal compliance and consumer order delivery regulations
    Given an active customer order progressing through fulfillment and delivery
    When updating the live status timeline and estimated delivery date
    Then the system must enforce statutory delivery deadlines (maximum 30 calendar days under EU law unless explicitly agreed otherwise)
    And legal risk of loss or transit damage must remain with the merchant until physical possession is acquired by the consumer
    And delivery milestone updates must provide accurate tracking data without deceptive progress indicators""",
        "tc": "Global legal & regulatory compliance (EU Consumer Rights Directive Art 18 30-day fulfillment, risk of loss transfer upon delivery)",
        "glaw": """### G-Law — Law validation
- [ ] **US-6.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Consumer Rights Directive Art 18 (statutory 30-day fulfillment limit), merchant transit loss liability, and accurate milestone disclosures; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-6.1.2": {
        "title": "Statutory durable medium access, fiscal invoice availability, and data retention schedules",
        "scenario": """  Scenario: [AC-US-6.1.2-LAW] Global e-commerce legal compliance and statutory invoice retention regulations
    Given a customer viewing their historical order records and downloading invoices
    When accessing archived orders and purchase documents
    Then order confirmations and invoices must remain accessible on a durable medium (PDF/downloadable format) for the statutory period
    And fiscal purchase records must be retained securely for statutory audit periods (6 to 10 years) under commercial tax laws
    And personal data masking must balance privacy rights with legal requirements to preserve immutable fiscal transactions""",
        "tc": "Global legal & regulatory compliance (EU Directive 2011/83/EU Art 8(7) durable medium, commercial tax code 6-10 year retention)",
        "glaw": """### G-Law — Law validation
- [ ] **US-6.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Consumer Rights Directive durable medium access, statutory commercial tax record retention (6–10 years), and fiscal audit integrity; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-6.1.3": {
        "title": "Statutory 14-day right of withdrawal, withdrawal exceptions, and statutory refund deadlines",
        "scenario": """  Scenario: [AC-US-6.1.3-LAW] Global e-commerce legal compliance and consumer right of withdrawal regulations
    Given a consumer initiating a return request for ordered products
    When evaluating the return eligibility under statutory withdrawal rules
    Then a minimum 14-calendar-day right of withdrawal without giving any reason must be granted for distance contracts
    And statutory exclusions (custom-made items, unsealed hygiene goods, rapidly perishable items) must be enforced strictly per statute
    And the consumer must be provided with the statutory standard model withdrawal form upon request""",
        "tc": "Global legal & regulatory compliance (EU Consumer Rights Directive Art 9-16 14-day withdrawal, statutory return exclusions)",
        "glaw": """### G-Law — Law validation
- [ ] **US-6.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Consumer Rights Directive (Directive 2011/83/EU) 14-day Right of Withdrawal, statutory exclusion tagging, and standard model withdrawal form; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-6.1.4": {
        "title": "Employee access controls, GDPR customer data protection, and administrative action audit trails",
        "scenario": """  Scenario: [AC-US-6.1.4-LAW] Global e-commerce legal compliance and administrative data governance regulations
    Given an administrator managing customer orders, cancellations, and manual interventions
    When viewing order details, customer addresses, or payment status
    Then customer personal information displayed in the dashboard must be minimized and masked where not required for order handling
    And any administrative modification, manual refund, or status override must be recorded in an immutable, tamper-evident audit log
    And role-based access controls must restrict customer financial information strictly to authorized customer service personnel""",
        "tc": "Global legal & regulatory compliance (GDPR Art 32 security of processing, employee PII access minimization, immutable audit logging)",
        "glaw": """### G-Law — Law validation
- [ ] **US-6.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR Art 32 access controls, customer PII masking on administrative screens, and tamper-evident audit logging; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-7.1.1": {
        "title": "GDPR Article 15 (Right of Access), Article 16 (Right to Rectification), and CCPA consumer rights",
        "scenario": """  Scenario: [AC-US-7.1.1-LAW] Global e-commerce legal compliance and consumer privacy rights regulations
    Given a customer managing their personal profile details in account settings
    When accessing, reviewing, or updating their personal data
    Then the consumer must be granted instantaneous self-service access to all stored personal data per GDPR Art 15 and CCPA
    And profile corrections and attribute updates must propagate immediately across all operational systems per GDPR Art 16
    And profile data collection must adhere to explicit purpose limitation without storing undeclared personal characteristics""",
        "tc": "Global legal & regulatory compliance (GDPR Art 15 Right of Access, Art 16 Right to Rectification, CCPA/CPRA Consumer Rights to Know/Correct)",
        "glaw": """### G-Law — Law validation
- [ ] **US-7.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR Art 15 (Right of Access), GDPR Art 16 (Right to Rectification), and CCPA/CPRA consumer data access mandates; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-7.1.2": {
        "title": "Customer address data privacy, right of erasure, and cross-border address persistence",
        "scenario": """  Scenario: [AC-US-7.1.2-LAW] Global e-commerce legal compliance and address data retention regulations
    Given a customer managing saved shipping and billing addresses
    When deleting or updating stored address book entries
    Then customer address deletions must immediately remove personal location records from active operational address books
    And archived historical address snapshots tied to fulfilled orders must be retained strictly under statutory fiscal audit rules
    And cross-border storage of customer address data must comply with international data transfer safeguards (SCCs / DPF)""",
        "tc": "Global legal & regulatory compliance (GDPR Art 17 Right to Erasure, statutory tax audit address preservation, cross-border safeguards)",
        "glaw": """### G-Law — Law validation
- [ ] **US-7.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR Art 17 ("Right to be Forgotten"), commercial tax address retention reconciliation, and international data transfer safeguards; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-7.1.3": {
        "title": "ePrivacy & CAN-SPAM express opt-in consent, 1-click unsubscribe, and consent revocation propagation",
        "scenario": """  Scenario: [AC-US-7.1.3-LAW] Global e-commerce legal compliance and marketing consent regulations
    Given a customer updating their communication and marketing preferences
    When opting in or out of marketing channels (Email, SMS, Push notifications)
    Then marketing channels must require explicit affirmative opt-in consent prior to transmitting commercial promotional content
    And every commercial communication must provide an easy, 1-click unsubscribe mechanism that executes immediately
    And consent revocation must be recorded with cryptographic timestamps and propagated to messaging gateways within 24 hours""",
        "tc": "Global legal & regulatory compliance (EU ePrivacy Directive express opt-in, US CAN-SPAM 1-click unsubscribe, CASL consent logging)",
        "glaw": """### G-Law — Law validation
- [ ] **US-7.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU ePrivacy Directive express consent, US CAN-SPAM / Canada CASL 1-click unsubscribe, and 24-hour consent revocation propagation; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-7.1.4": {
        "title": "Anti-deceptive price drop alerts, ePrivacy tracking consent, and wishlist data protection",
        "scenario": """  Scenario: [AC-US-7.1.4-LAW] Global e-commerce legal compliance and promotional price alert regulations
    Given a customer saving catalog items to a personal wishlist and enabling price drop notifications
    When generating price drop alerts or saving product preferences
    Then price drop alert notifications must reflect genuine price reductions calculated against the prior 30-day lowest price baseline
    And consumer wishlist preferences must not be shared with third-party advertisers without explicit affirmative consent
    And wishlist items must accurately reflect current stock availability without fabricated urgency warnings""",
        "tc": "Global legal & regulatory compliance (EU Omnibus Directive Art 6a price drop baseline, ePrivacy tracking consent, anti-dark patterns)",
        "glaw": """### G-Law — Law validation
- [ ] **US-7.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Omnibus Directive (Art 6a 30-day baseline for price drop alerts), ePrivacy behavioral tracking consent, and truth-in-advertising stock disclosures; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-8.1.1": {
        "title": "EU AI Act transparency, automated decision-making disclosures, and truthful AI recommendations",
        "scenario": """  Scenario: [AC-US-8.1.1-LAW] Global e-commerce legal compliance and consumer AI interaction regulations
    Given a customer interacting with the WebMCP shopping AI agent
    When the AI assistant recommends products, summarizes reviews, or assists in checkout
    Then the user must be informed clearly and unambiguously that they are interacting with an artificial intelligence system (EU AI Act Art 50)
    And AI recommendations must not manipulate consumer purchasing decisions through deceptive dark patterns or concealed sponsored bias
    And personal conversational prompts must be handled under strict data privacy safeguards without training external models on customer PII""",
        "tc": "Global legal & regulatory compliance (EU AI Act Regulation 2024/1689 Art 50 AI transparency, GDPR Art 22 automated decisions, FTC truth in AI)",
        "glaw": """### G-Law — Law validation
- [ ] **US-8.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Artificial Intelligence Act (Regulation 2024/1689 Art 50 transparency), GDPR Art 22 automated decision disclosures, and FTC anti-deceptive AI guidance; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-8.1.2": {
        "title": "EU AI Act human oversight mandate, automated pricing fairness, and administrative accountability",
        "scenario": """  Scenario: [AC-US-8.1.2-LAW] Global e-commerce legal compliance and administrative AI copilot governance
    Given a store administrator utilizing the WebMCP copilot for catalog edits, pricing adjustments, or bulk actions
    When the AI assistant executes store management operations
    Then human oversight mechanisms must require explicit human confirmation for high-impact actions (price changes, inventory write-offs)
    And algorithmic pricing suggestions must comply with anti-collusion competition laws prohibiting automated price-fixing
    And an audit record linking the human administrator to every AI-suggested catalog mutation must be maintained""",
        "tc": "Global legal & regulatory compliance (EU AI Act Art 14 human oversight mandate, competition law pricing rules, admin audit trails)",
        "glaw": """### G-Law — Law validation
- [ ] **US-8.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU AI Act Art 14 human oversight requirements, antitrust and algorithmic pricing fairness laws, and operator accountability logging; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-8.1.3": {
        "title": "GDPR Article 28 data processor agreements, zero customer PII leakage, and AI model safety",
        "scenario": """  Scenario: [AC-US-8.1.3-LAW] Global e-commerce legal compliance and cloud AI provider data protection regulations
    Given the core MCP engine dispatching prompts and tool execution payloads to AWS Bedrock
    When processing LLM invocations across customer and admin contexts
    Then customer PII and sensitive credentials must be stripped or masked before transmitting prompts to foundational model endpoints
    And the LLM service integration must operate under a formal GDPR Art 28 Data Processing Agreement guaranteeing zero model training on customer data
    And model outputs must be passed through safety filters preventing generation of harmful, discriminatory, or unlawful content""",
        "tc": "Global legal & regulatory compliance (GDPR Art 28 DPA terms, zero LLM model training on customer data, automated PII redaction)",
        "glaw": """### G-Law — Law validation
- [ ] **US-8.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR Art 28 cloud provider data processing terms, complete customer PII redaction from LLM prompts, and AI content safety filters; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-9.1.1": {
        "title": "Statutory right of withdrawal waiver for digital content, copyright protection, and secure delivery",
        "scenario": """  Scenario: [AC-US-9.1.1-LAW] Global e-commerce legal compliance and digital content delivery regulations
    Given a customer purchasing and downloading digital software, media, or licenses
    When generating presigned secure download links
    Then the consumer must provide express prior consent acknowledging that immediate download waives the 14-day statutory right of withdrawal
    And presigned download URLs must be cryptographically signed, time-limited, and bound to the authenticated purchaser
    And digital content delivery must incorporate intellectual property safeguards preventing unauthorized redistribution""",
        "tc": "Global legal & regulatory compliance (EU Consumer Rights Directive Art 16(m) digital withdrawal waiver, DMCA copyright safeguards)",
        "glaw": """### G-Law — Law validation
- [ ] **US-9.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Consumer Rights Directive Art 16(m) express withdrawal waiver on digital execution, time-limited presigned URLs, and DMCA copyright protection; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-9.1.2": {
        "title": "Software copyright licensing laws, anti-circumvention statutory compliance, and license grant transparency",
        "scenario": """  Scenario: [AC-US-9.1.2-LAW] Global e-commerce legal compliance and software licensing regulations
    Given the generation and cryptographic validation of software license grants (perpetual, node-locked, floating)
    When issuing and verifying digital license certificates
    Then license parameters and usage constraints must be disclosed unambiguously in the end-user license agreement (EULA)
    And cryptographic tamper-proofing must comply with legal anti-circumvention provisions protecting digital copyright
    And license issuance must preserve customer rights to lawful software resale and interoperability decompilation under EU law""",
        "tc": "Global legal & regulatory compliance (EU Software Directive 2009/24/EC, DMCA anti-circumvention statutory compliance, EULA transparency)",
        "glaw": """### G-Law — Law validation
- [ ] **US-9.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Software Directive (Directive 2009/24/EC), DMCA § 1201 anti-circumvention compliance, and statutory software decompilation/resale rights; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-9.1.3": {
        "title": "Fair license audit rights, zero unauthorized telemetric surveillance, and client privacy",
        "scenario": """  Scenario: [AC-US-9.1.3-LAW] Global e-commerce legal compliance and client verification SDK privacy regulations
    Given client verification SDKs embedded in customer host applications to validate software licenses
    When the SDK evaluates license entitlement tokens in online or offline environments
    Then verification telemetry must be strictly limited to cryptographic signature verification without collecting unauthorized host telemetry
    And license verification must execute locally in offline air-gapped environments without mandatory internet heartbeats
    And audit terms governing software license compliance must be transparently stated in commercial software contracts""",
        "tc": "Global legal & regulatory compliance (GDPR Art 5 data minimization in client SDKs, offline air-gapped license validity, fair audit clauses)",
        "glaw": """### G-Law — Law validation
- [ ] **US-9.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: client SDK data minimization (zero covert telemetry), air-gapped offline entitlement verification, and commercial contract audit terms; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-9.1.4": {
        "title": "Durable medium proof of purchase, perpetual license preservation, and certificate generation",
        "scenario": """  Scenario: [AC-US-9.1.4-LAW] Global e-commerce legal compliance and digital certificate vault regulations
    Given a customer accessing their digital license vault to view keys and download activation credentials
    When retrieving purchased license keys or certificates
    Then the customer must be provided with durable, permanent access to license credentials and activation keys on durable media (PDF)
    And purchased perpetual licenses must remain downloadable and viewable regardless of subsequent catalog deprecations
    And license transfer and assignment terms must be clearly disclosed within the digital vault interface""",
        "tc": "Global legal & regulatory compliance (EU Consumer Rights Directive Art 8 durable medium, perpetual software purchase preservation)",
        "glaw": """### G-Law — Law validation
- [ ] **US-9.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU durable medium proof of purchase, permanent consumer access to perpetual digital licenses, and transparent assignment terms; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-10.1.1": {
        "title": "Commercial pricing non-discrimination, Robinson-Patman Act compliance, and transparent B2B terms",
        "scenario": """  Scenario: [AC-US-10.1.1-LAW] Global e-commerce legal compliance and B2B wholesale pricing regulations
    Given a wholesale buyer purchasing merchandise under tiered volume pricing and minimum order quantities (MOQ)
    When applying volume discounts and enforcing MOQ rules
    Then volume price tiers must be established on objective, economically justifiable cost-of-sale criteria per Robinson-Patman Act
    And wholesale terms, freight thresholds, and minimum order quantities must be published transparently to all verified commercial buyers
    And tiered pricing calculation must properly distinguish between tax-exclusive wholesale net prices and statutory applicable VAT""",
        "tc": "Global legal & regulatory compliance (US Robinson-Patman Act 15 U.S.C. § 13, EU Competition Law non-discrimination, B2B VAT rules)",
        "glaw": """### G-Law — Law validation
- [ ] **US-10.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: US Robinson-Patman Act commercial pricing justification, EU antitrust non-discrimination principles, and B2B VAT calculation rules; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-10.1.2": {
        "title": "EU Late Payment Directive, statutory commercial interest, and legally binding digital contract formation",
        "scenario": """  Scenario: [AC-US-10.1.2-LAW] Global e-commerce legal compliance and B2B commercial invoicing regulations
    Given a B2B buyer and vendor negotiating customized quotes (RFQ) and agreeing to net-30/net-60 payment terms
    When generating the finalized purchase contract and issuing commercial net-terms invoices
    Then agreed quotes must constitute legally binding commercial contracts with explicit cryptographic acceptance timestamps
    And net-terms invoices must state statutory late payment interest rates and recovery costs mandated under the EU Late Payment Directive
    And commercial tax invoices must include complete seller and buyer corporate tax IDs, sequential numbering, and reverse-charge notices""",
        "tc": "Global legal & regulatory compliance (EU Late Payment Directive 2011/7/EU statutory interest, UN CISG binding contracts, VAT e-invoicing)",
        "glaw": """### G-Law — Law validation
- [ ] **US-10.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Late Payment Directive (Directive 2011/7/EU), commercial contract formation rules (UN CISG), and statutory reverse-charge VAT invoicing; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-10.1.3": {
        "title": "Trade catalog classification standards, search transparency, and non-discriminatory commercial discovery",
        "scenario": """  Scenario: [AC-US-10.1.3-LAW] Global e-commerce legal compliance and wholesale catalog classification regulations
    Given enterprise procurement buyers filtering wholesale catalogs using custom B2B facets (certifications, specs, lead times)
    When generating faceted wholesale search results
    Then product specification facets must map to standardized international commercial classification taxonomies (e.g., UNSPSC)
    And search ranking criteria and distributor visibility parameters must be transparently disclosed per EU P2B regulations
    And faceted attributes must reflect verified manufacturer specifications without misleading technical performance claims""",
        "tc": "Global legal & regulatory compliance (EU P2B Regulation search transparency, UNSPSC commodity classification standards)",
        "glaw": """### G-Law — Law validation
- [ ] **US-10.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Platform-to-Business (P2B) commercial search transparency, international trade commodity taxonomies (UNSPSC), and technical specification truthfulness; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-10.1.4": {
        "title": "Export administration regulations (EAR), corporate cryptographic perimeter security, and data sovereignty",
        "scenario": """  Scenario: [AC-US-10.1.4-LAW] Global e-commerce legal compliance and dual-use technology export regulations
    Given an enterprise deploying an on-premise LAN license proxy for internal floating license management
    When distributing and leasing cryptographic license tokens within the corporate intranet
    Then cryptographic software distribution must comply with international export controls and dual-use technology regulations (EAR)
    And internal license proxy telemetry must remain strictly within the enterprise security perimeter to ensure corporate data sovereignty
    And offline leasing mechanisms must adhere to contracted license seat maximums without unauthorized remote key disablement""",
        "tc": "Global legal & regulatory compliance (US Export Administration Regulations EAR, Wassenaar cryptographic controls, enterprise data sovereignty)",
        "glaw": """### G-Law — Law validation
- [ ] **US-10.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: US Export Administration Regulations (EAR) dual-use controls, Wassenaar Arrangement cryptographic rules, and corporate data sovereignty standards; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-11.1.1": {
        "title": "EU Digital Services Act (DSA Art 30 KYB Trader Traceability), US INFORM Consumers Act seller verification",
        "scenario": """  Scenario: [AC-US-11.1.1-LAW] Global e-commerce legal compliance and marketplace seller traceability regulations
    Given a prospective third-party merchant applying to sell on the multi-vendor marketplace
    When onboarding and verifying the vendor prior to catalog activation
    Then the platform must verify official business registration documents, corporate identity, bank account details, and tax ID per DSA Art 30
    And high-volume sellers must be verified and certified in compliance with the US INFORM Consumers Act
    And merchant onboarding records must be screened against global AML sanctions lists before granting product publishing rights""",
        "tc": "Global legal & regulatory compliance (EU Digital Services Act Art 30 KYB traceability, US INFORM Consumers Act, AML sanctions checks)",
        "glaw": """### G-Law — Law validation
- [ ] **US-11.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Digital Services Act (DSA Regulation 2022/2065 Art 30 KYB trader traceability), US INFORM Consumers Act verification, and global AML sanctions screening; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-11.1.2": {
        "title": "Multi-merchant contract formation, transparent fee separation, and consumer rights disclosure",
        "scenario": """  Scenario: [AC-US-11.1.2-LAW] Global e-commerce legal compliance and marketplace checkout contract regulations
    Given a checkout containing products sourced from multiple independent marketplace merchants
    When splitting the checkout into individual vendor sub-orders
    Then the consumer must be informed that they are entering into distinct, separate purchase contracts with each independent vendor
    And itemized shipping fees, return addresses, and estimated delivery dates must be clearly separated per vendor sub-order
    And tax liabilities and invoicing must be partitioned correctly between marketplace facilitator collections and vendor disbursements""",
        "tc": "Global legal & regulatory compliance (EU Consumer Rights Directive multi-merchant disclosure, marketplace facilitator sales tax apportionment)",
        "glaw": """### G-Law — Law validation
- [ ] **US-11.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Consumer Rights Directive merchant contract separation, FTC drip pricing fee transparency, and marketplace facilitator tax apportionment; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-11.1.3": {
        "title": "DAC7 marketplace tax reporting, US IRS 1099-K reporting, and fiduciary escrow regulations",
        "scenario": """  Scenario: [AC-US-11.1.3-LAW] Global e-commerce legal compliance and marketplace tax reporting regulations
    Given marketplace customer payments held in double-entry escrow and disbursed to vendors
    When computing vendor commissions, withholding funds, and executing automated bank payouts
    Then vendor annual gross sales and transaction counts must be recorded for mandatory DAC7 and IRS Form 1099-K tax reporting
    And customer escrow funds must remain segregated from operational platform funds until fulfillment obligations are satisfied
    And vendor commission deductions must strictly mirror agreed contractual rates without unauthorized hidden withholding""",
        "tc": "Global legal & regulatory compliance (EU DAC7 Directive 2021/514 tax reporting, US IRS Form 1099-K, fiduciary escrow fund segregation)",
        "glaw": """### G-Law — Law validation
- [ ] **US-11.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU DAC7 Directive (Directive 2021/514), US IRS Form 1099-K reporting, and fiduciary customer payment escrow segregation; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-11.1.4": {
        "title": "EU Platform-to-Business (P2B) regulation transparency, statement of reasons, and internal complaint handling",
        "scenario": """  Scenario: [AC-US-11.1.4-LAW] Global e-commerce legal compliance and marketplace vendor relations regulations
    Given a vendor accessing their merchant dashboard, performance metrics, and account status
    When platform policies, ranking rules, or account restrictions are applied
    Then any terms and conditions changes must provide a mandatory 15-day prior notice before taking effect per EU P2B Art 3
    And any product delisting or account restriction must be accompanied by an explicit, written statement of reasons per P2B Art 4
    And an accessible, free-of-charge internal complaint-handling system must be provided for dispute resolution per P2B Art 11 and DSA Art 20""",
        "tc": "Global legal & regulatory compliance (EU P2B Regulation 2019/1150 15-day notice, statement of reasons for restriction, DSA Art 20 complaints)",
        "glaw": """### G-Law — Law validation
- [ ] **US-11.1.4-G-Law:** Independent verification against global e-commerce legal and statutory requirements: EU Platform-to-Business (P2B Regulation 2019/1150) terms transparency, mandatory statement of reasons for restriction, and DSA Art 20 complaint-handling systems; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-12.1.1": {
        "title": "European Accessibility Act compliance in UI schemas, dark pattern prevention, and consumer transparency",
        "scenario": """  Scenario: [AC-US-12.1.1-LAW] Global e-commerce legal compliance and accessible interface design regulations
    Given a designer or merchandiser composing Server-Driven UI (SDUI) screens in the visual drag-and-drop studio
    When publishing layout schemas to the mobile and web storefronts
    Then the visual studio must validate that published layouts conform to WCAG 2.1 AA accessibility standards (text contrast, label semantics)
    And layout composition must prevent the insertion of manipulative dark patterns (e.g. concealed opt-outs, deceptive button hierarchies)
    And published promotional banners must include clear mandatory terms disclaimers and readable disclosure font sizes""",
        "tc": "Global legal & regulatory compliance (European Accessibility Act Directive 2019/882, EU DSA Art 25 anti-dark patterns, WCAG 2.1 AA)",
        "glaw": """### G-Law — Law validation
- [ ] **US-12.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: European Accessibility Act (EAA Directive 2019/882), EU Digital Services Act (DSA Art 25 prohibition of dark patterns), and accessible presentation schemas; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-12.1.2": {
        "title": "Data sovereignty, multi-tenant data isolation, and SLA contractual liability",
        "scenario": """  Scenario: [AC-US-12.1.2-LAW] Global e-commerce legal compliance and enterprise data residency regulations
    Given provisioning enterprise tenants on standard multitenant or dedicated managed single-tenant instances
    When isolating customer databases, KMS keys, and infrastructure environments
    Then tenant data residency must comply with geographic data localization laws and cross-border transfer restrictions
    And dedicated managed instances must maintain cryptographically segregated customer-managed encryption keys (CMEK)
    And service level agreements (SLAs), maintenance windows, and backup recovery objectives must be contractually defined and enforced""",
        "tc": "Global legal & regulatory compliance (GDPR Chapter V cross-border transfer, CMEK customer key segregation, enterprise SLA liability)",
        "glaw": """### G-Law — Law validation
- [ ] **US-12.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: GDPR Chapter V cross-border transfer restrictions, tenant data residency compliance, and CMEK cryptographic isolation; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-12.1.3": {
        "title": "App store developer legal terms, regional mobile compliance, and cryptographic export compliance",
        "scenario": """  Scenario: [AC-US-12.1.3-LAW] Global e-commerce legal compliance and mobile app distribution regulations
    Given automated compilation and signing of white-label iOS and Android storefront mobile applications
    When generating production app bundles for distribution across regional app stores
    Then mobile application builds must comply with Apple and Google app store legal agreements (privacy nutrition labels, in-app purchases)
    And app manifests must declare precise hardware permission scopes with explicit, user-facing privacy justification strings
    And embedded cryptographic libraries must maintain export compliance documentation for international distribution""",
        "tc": "Global legal & regulatory compliance (Apple App Store / Google Play legal agreements, mobile privacy manifest disclosures, crypto export compliance)",
        "glaw": """### G-Law — Law validation
- [ ] **US-12.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: Apple App Store and Google Play distribution agreements, mobile privacy manifest declarations, and international mobile cryptography export rules; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-13.1.1": {
        "title": "SOC 2 Type II / ISO 27001 infrastructure baselines, CIS AWS benchmark compliance, and data protection",
        "scenario": """  Scenario: [AC-US-13.1.1-LAW] Global e-commerce legal compliance and cloud infrastructure governance regulations
    Given synthesizing and deploying infrastructure-as-code (AWS CDK) cloud stacks for the e-commerce platform
    When configuring networking, storage buckets, database tables, and IAM execution roles
    Then all storage resources (DynamoDB, S3) must enforce mandatory encryption at rest with automated key rotation
    And IAM roles must implement the principle of least privilege with zero wildcard permissions on sensitive data stores
    And cloud infrastructure configurations must pass automated compliance checks against CIS AWS Foundations Benchmarks""",
        "tc": "Global legal & regulatory compliance (SOC 2 Type II / ISO 27001:2022 security baselines, CIS AWS Foundations Benchmark, mandatory encryption at rest)",
        "glaw": """### G-Law — Law validation
- [ ] **US-13.1.1-G-Law:** Independent verification against global e-commerce legal and statutory requirements: SOC 2 Type II / ISO 27001:2022 security controls, CIS AWS Foundations Benchmark compliance, and mandatory customer data encryption at rest; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-13.1.2": {
        "title": "AWS Marketplace Customer Agreement compliance, Foundational Technical Review (FTR), and legal warranties",
        "scenario": """  Scenario: [AC-US-13.1.2-LAW] Global e-commerce legal compliance and cloud marketplace procurement regulations
    Given listing the commerce platform on the AWS Marketplace for commercial customer procurement
    When validating product architecture against AWS Marketplace requirements
    Then the solution architecture must satisfy all AWS Foundational Technical Review (FTR) security and operational criteria
    And marketplace subscription agreements must incorporate transparent customer terms, SLAs, and liability limitations
    And disaster recovery RPO/RTO metrics must be verified through automated failover drills meeting marketplace listing requirements""",
        "tc": "Global legal & regulatory compliance (AWS Marketplace Customer Agreement, AWS Foundational Technical Review FTR security baselines)",
        "glaw": """### G-Law — Law validation
- [ ] **US-13.1.2-G-Law:** Independent verification against global e-commerce legal and statutory requirements: AWS Marketplace Customer Agreement compliance, AWS Foundational Technical Review (FTR) certification, and verified disaster recovery operational SLAs; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    },
    "US-13.1.3": {
        "title": "Truth in billing regulations, accurate tax computation per metered unit, and immutable audit logs",
        "scenario": """  Scenario: [AC-US-13.1.3-LAW] Global e-commerce legal compliance and SaaS metered billing regulations
    Given metering customer platform consumption (API calls, GMV volume, active vendors) and generating monthly billing events
    When transmitting usage records to AWS Marketplace Metering Service or Stripe Billing
    Then metered usage records must be calculated with idempotent deduplication preventing double billing or under-metering
    And billing statements must provide transparent itemized unit breakdowns with statutory applicable sales tax and VAT
    And raw metering telemetry must be preserved in immutable, tamper-resistant audit logs for financial and tax audit reconciliation""",
        "tc": "Global legal & regulatory compliance (FTC Truth in Billing guidelines, SaaS jurisdictional sales tax/VAT, SOX financial auditability)",
        "glaw": """### G-Law — Law validation
- [ ] **US-13.1.3-G-Law:** Independent verification against global e-commerce legal and statutory requirements: FTC Truth in Billing regulations, SaaS tax and VAT calculation accuracy, and SOX-compliant immutable financial audit logs; certified by compliance reviewer (`agency-legal-compliance-checker`)."""
    }
}


def update_story_file(file_path: Path) -> bool:
    content = file_path.read_text(encoding="utf-8")
    m = re.search(r"#\s+(US-[\d\.]+)", content)
    if not m:
        return False
    story_id = m.group(1)

    if story_id not in GLOBAL_LAWS:
        print(f"Warning: Story {story_id} not found in GLOBAL_LAWS dictionary!")
        return False

    info = GLOBAL_LAWS[story_id]
    new_scenario = info["scenario"]
    new_tc_desc = info["tc"]
    new_glaw = info["glaw"]

    # 1. Replace Scenario: [AC-US-X.Y.Z-LAW]
    scenario_pattern = re.compile(
        r"  Scenario: \[AC-" + re.escape(story_id) + r"-LAW\][^\n]*\n(?:    [^\n]*\n)*",
        re.MULTILINE
    )
    if scenario_pattern.search(content):
        content = scenario_pattern.sub(new_scenario + "\n", content, count=1)
    else:
        print(f"Warning: Scenario AC-{story_id}-LAW pattern not found in {file_path}")

    # 2. Update TC-X.Y.Z-LAW in Traceability Matrix
    # Pattern: | TC-X.Y.Z-LAW | ... | ... | ... |
    tc_pattern = re.compile(
        r"\| TC-" + re.escape(story_id[3:]) + r"-LAW \| [^|]+ \| [^|]+ \| [^|]+ \|",
        re.MULTILINE
    )
    if tc_pattern.search(content):
        # We preserve the table format: | TC | Description | Type | Expected Result |
        replacement_tc = f"| TC-{story_id[3:]}-LAW | {new_tc_desc} | Legal / Regulatory | Statutory compliance verified with zero legal or regulatory violations |"
        content = tc_pattern.sub(replacement_tc, content, count=1)
    else:
        # Try full story_id format e.g. TC-US-X.Y.Z-LAW or TC-X.Y.Z-LAW
        alt_pattern = re.compile(
            r"\| TC-.*-LAW \| [^|]+ \| [^|]+ \| [^|]+ \|",
            re.MULTILINE
        )
        if alt_pattern.search(content):
            replacement_tc = f"| TC-{story_id[3:]}-LAW | {new_tc_desc} | Legal / Regulatory | Statutory compliance verified with zero legal or regulatory violations |"
            content = alt_pattern.sub(replacement_tc, content, count=1)

    # 3. Update Section 6: ### G-Law — Law validation
    # Pattern: ### G-Law — Law validation\n(?:- [^\n]*\n)+
    glaw_pattern = re.compile(
        r"### G-Law — Law validation\n(?:- [^\n]*\n)+",
        re.MULTILINE
    )
    if glaw_pattern.search(content):
        content = glaw_pattern.sub(new_glaw + "\n", content, count=1)
    else:
        print(f"Warning: G-Law pattern not found in {file_path}")

    file_path.write_text(content, encoding="utf-8")
    return True


def main():
    root_dir = Path("docs/user-stories")
    count = 0
    updated = 0
    for root, dirs, files in os.walk(root_dir):
        for f in sorted(files):
            if f.startswith("us-") and f.endswith(".md"):
                count += 1
                p = Path(root) / f
                if update_story_file(p):
                    updated += 1

    print(f"Processed {count} stories, successfully updated {updated} with global e-commerce legal requirements.")


if __name__ == "__main__":
    main()
