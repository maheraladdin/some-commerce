# Audit Domain 03: Compliance & AWS Foundational Technical Review (FTR)

> **Scope**: AWS Marketplace FTR · SaaS Metering Audit · Cloud Storage Retention · Multi-Tenant Privacy & Disaster Recovery  
> **Governing Quality Gate**: **Gate G2**, **SG4** (Release Candidate)  
> **Accountable Role**: `devops-engineer` / `chief-technology-officer`

---

## 1. Domain Overview

The Compliance & AWS FTR audit domain validates that `some-commerce` satisfies all strict technical, operational, and architectural requirements for enterprise deployment and AWS Marketplace listing, as outlined in [`docs/DEPLOYMENT_AND_AWS_MARKETPLACE.md`](../../DEPLOYMENT_AND_AWS_MARKETPLACE.md).

### Core Compliance Pillars:
1. **AWS Marketplace FTR Requirements**:
   - **Multi-Tenant Data Isolation**: Database partition keys must enforce `PK = TENANT#<tid>`. No cross-tenant access allowed.
   - **Cloud Storage Security**: All S3 buckets must have Public Access Blocked, enforce SSE-KMS encryption, and deliver web assets via CloudFront Origin Access Control (OAC).
   - **Disaster Recovery & Data Retention**: S3 audit buckets and DynamoDB tables must use `RemovalPolicy.RETAIN` and Point-in-Time Recovery (PITR).
2. **SaaS Metering Reconciliation**:
   - Metering records dispatched to the AWS Marketplace Metering Service (`BatchMeterUsage`) must be deduplicated, cryptographically signed, and reconciliation logs persisted in immutable storage.
   - Dimension catalog (`active_merchants_tier`, `monthly_gmv_bandwidth_gb`, `licensing_seats_tier`) must be strictly reconciled without loss or double-billing.
3. **Enterprise Privacy & SOC2 Readiness**:
   - PII fields (customer phone numbers, national IDs, addresses) must be pseudonymized or encrypted with dedicated tenant keys.

---

## 2. Automated Compliance Check Commands

```bash
# 1. Verify CDK CloudFormation template synthesis and IAM rules
npm --prefix infra run cdk synth

# 2. Check S3 and DynamoDB resource retention policies
grep -rn "RemovalPolicy.RETAIN" infra/

# 3. Verify CloudFront OAC private bucket policy bindings
grep -rn "OriginAccessControl" infra/
```

---

## 3. Sprint Compliance & FTR Audit Catalog

| Audit File | Sprint | Focus | Status |
|:-----------|:-------|:------|:-------|
| `AUDIT-COMP-sprint-1.1-dynamo-encryption-pitr.md` | Sprint 1.1 | DynamoDB table encryption, PITR, partition key tenant isolation | Pending |
| `AUDIT-COMP-sprint-1.2-s3-retention-oac.md` | Sprint 1.2 | S3 private buckets, CloudFront OAC, retention policy compliance | Pending |
| `AUDIT-COMP-sprint-2.1-digital-vault-retention.md` | Sprint 2.1 | Digital asset S3 KMS encryption, presigned URL lifespan enforcement | Pending |
| `AUDIT-COMP-sprint-2.2-customer-privacy-vault.md` | Sprint 2.2 | Customer license ledger tamper detection, data export compliance | Pending |
| `AUDIT-COMP-sprint-3.1-tax-invoice-compliance.md` | Sprint 3.1 | Cross-border tax calculations, VAT invoice immutable storage | Pending |
| `AUDIT-COMP-sprint-3.2-credit-terms-compliance.md` | Sprint 3.2 | Net-terms financial records, PO compliance and audit trail | Pending |
| `AUDIT-COMP-sprint-4.1-marketplace-escrow-segregation.md` | Sprint 4.1 | Vendor funds segregation, sub-order tax liability demarcation | Pending |
| `AUDIT-COMP-sprint-4.2-crypto-regulatory-compliance.md` | Sprint 4.2 | BTCPay self-hosted compliance, non-custodial crypto auditing | Pending |
| `AUDIT-COMP-sprint-5.1-aws-marketplace-ftr-readiness.md` | Sprint 5.1 | Formal AWS Marketplace FTR audit submission, metering dimensions | Pending |
| `AUDIT-COMP-sprint-6.1-edition-cutover-compliance.md` | Sprint 6.1 | Multi-edition runtime toggle safety, telemetry privacy audit | Pending |
| `AUDIT-COMP-sprint-6.2-whitelabel-distribution.md` | Sprint 6.2 | White-label licensing compliance, third-party OSS license attributions | Pending |
| `AUDIT-COMP-sprint-6.3-final-ftr-certification.md` | Sprint 6.3 | Comprehensive AWS FTR audit pass, production readiness review | Pending |

---

## 4. How to Conduct and Record an Audit

1. Copy `../AUDIT_RECORD_TEMPLATE.md` to `docs/audits/03-compliance-and-aws-ftr/AUDIT-COMP-<sprint>-<topic>.md`
2. Validate infrastructure definitions against AWS FTR requirements.
3. Review audit logs, encryption contexts, and retention configurations.
4. Record findings and sign off under `devops-engineer` and `chief-technology-officer` review.
