# Audit Domain 01: Security & Penetration Testing

> **Scope**: OWASP ASVS v4.0.3 Level 2 · Multi-Tenant Isolation Fuzzing · KMS Envelope Encryption · JWT/OAuth RBAC · Cryptographic Gating  
> **Governing Quality Gate**: **Gate G2** (Story Level) & **SG2** (Sprint Level)  
> **Accountable Role**: `senior-security-qa-auditor` / `security-engineer`

---

## 1. Domain Overview

The Security & Penetration Testing audit domain ensures the absolute security and tenant isolation of the `some-commerce` platform. Under the zero-trust multi-tenant model, tenants share compute infrastructure (Cargo Lambda microservices) and database tables (`SomeCommerceTable`), requiring mathematically verifiable partitioning at all layers.

### Key Audit Mandates:
- **OWASP ASVS v4.0.3 Level 2 Compliance**: Complete coverage across Authentication (V2), Session Management (V3), Access Control (V4), Cryptography (V6), and Data Protection (V8).
- **Adversarial Tenant Isolation Fuzzing**: Every data access layer must be subjected to synthetic tenant hijacking and IDOR attack fuzzing. Zero cross-tenant data leaks are permitted.
- **KMS Envelope Cryptography Verification**: Verification that merchant credentials, API keys, and sensitive tokens are encrypted using `KmsSecretVault` with tenant-specific encryption contexts (`tenant_id`, `gateway_type`, `provider_id`).
- **Cryptographic Licensing Engine Integrity**: Ed25519 offline signature validation, Bloom filter CRL lookup safety, AES-256-GCM Content Encryption Key unsealing, and anti-tamper protections.

---

## 2. Standard Security Audit Toolchain

Auditors must run and archive outputs from the following automated toolchain:

| Category | Recommended Tool | Command / Procedure | Pass Criteria |
|:---------|:-----------------|:--------------------|:--------------|
| **Dependency CVE Scan** | `cargo-audit` | `cargo audit --deny warnings` | 0 Critical, 0 High, 0 Unvetted Medium CVEs |
| **Static Application Security (SAST)** | `semgrep` | `semgrep scan --config p/owasp-top-ten --error` | Zero findings |
| **Secret Scanning** | `gitleaks` / `trivy` | `trivy fs --scanners secret .` | Zero detected credentials or private keys |
| **API Pentest & Fuzzing** | Custom Rust Fuzzers / OWASP ZAP | `cargo fuzz run <target> -- -max_total_time=600` | Zero panics, zero memory leaks, zero unauthorized 200s |

---

## 3. Sprint Security Audit Catalog

| Audit File | Sprint | Focus | Status |
|:-----------|:-------|:------|:-------|
| `AUDIT-SEC-sprint-1.1-cognito-jwt-rbac.md` | Sprint 1.1 | Cognito JWKS verification, OTP brute-force limits, role extractor safety | Pending |
| `AUDIT-SEC-sprint-1.2-kms-vault-webhooks.md` | Sprint 1.2 | KMS envelope encryption vault, Paymob/Stripe HMAC webhook signature verification | Pending |
| `AUDIT-SEC-sprint-2.1-licensing-ed25519-crl.md` | Sprint 2.1 | Ed25519 asymmetric signature validity, S3 vault presigned URL tamper-proofing | Pending |
| `AUDIT-SEC-sprint-2.2-airgap-qr-cek.md` | Sprint 2.2 | AES-256-GCM CEK unsealing, air-gapped QR challenge-response replay defense | Pending |
| `AUDIT-SEC-sprint-3.1-b2b-tenant-isolation.md` | Sprint 3.1 | B2B organization multi-tenant hierarchy isolation, wholesale price list leakage | Pending |
| `AUDIT-SEC-sprint-3.2-rfq-lan-proxy-auth.md` | Sprint 3.2 | RFQ counter-offer tampering, LAN seat proxy session hijacking | Pending |
| `AUDIT-SEC-sprint-4.1-vendor-portal-idor.md` | Sprint 4.1 | Vendor dashboard IDOR, sub-order splitting escrow authorization | Pending |
| `AUDIT-SEC-sprint-4.2-escrow-ledger-payouts.md` | Sprint 4.2 | Double-entry ledger balance integrity, BTCPay webhook forgery, payout double-spend | Pending |
| `AUDIT-SEC-sprint-5.1-iam-least-privilege.md` | Sprint 5.1 | CDK IAM policies, S3 bucket public access blocks, Lambda execution boundaries | Pending |
| `AUDIT-SEC-sprint-6.1-sdui-ast-injection.md` | Sprint 6.1 | SDUI JSON AST sanitizer, client XSS injection, visual studio schema traversal | Pending |
| `AUDIT-SEC-sprint-6.2-whitelabel-key-vault.md` | Sprint 6.2 | White-label iOS/Android signing certificate security, build runner isolation | Pending |
| `AUDIT-SEC-sprint-6.3-final-asvs-l2-pentest.md` | Sprint 6.3 | Comprehensive end-to-end OWASP ASVS v4.0.3 L2 penetration test & threat model | Pending |

---

## 4. How to Conduct and Record an Audit

1. Branch from candidate commit: `git checkout -b audit/sec-<sprint>`
2. Copy `../AUDIT_RECORD_TEMPLATE.md` to `docs/audits/01-security-and-penetration/AUDIT-SEC-<sprint>-<topic>.md`
3. Execute SAST, dependency scans, and adversarial fuzzers. Attach raw terminal digests.
4. Record all findings. Verify that all Critical and High findings are remediated before recommending Gate G2/SG2 approval.
5. Submit for independent review by `senior-security-qa-auditor`.
