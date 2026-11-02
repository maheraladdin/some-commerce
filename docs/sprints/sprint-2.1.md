# Sprint 2.1 — Digital Asset Pipeline + Licensing Engine (Modes 1–4)

> **Slice**: v2.0 · **Duration**: Weeks 5–6 · **Story Points**: 30

## Goal

Build the digital asset ingestion pipeline with presigned S3 delivery and implement the first 4 modes of the non-heartbeat licensing engine (Ed25519 certificates, Air-gapped QR, CRL revocation, CEK unsealing).

## User Stories

| Priority | Story | Module | Points | Description |
|:---------|:------|:-------|:-------|:------------|
| P0 | [US-9.1.1](../user-stories/09-digital-products-and-licensing/README.md#us-911-digital-asset-ingestion--presigned-s3-delivery) | Digital | 8 | Digital asset ingestion + presigned S3 |
| P0 | [US-9.1.2](../user-stories/09-digital-products-and-licensing/README.md#us-912-6-mode-non-heartbeat-licensing-engine) | Licensing | 13 | Licensing Modes 1–4 (Ed25519, QR, CRL, CEK) |
| P1 | [US-2.1.3](../user-stories/02-storefront-and-catalog/README.md#us-213-admin-customizable-product-properties--filter-widgets) | Storefront | 5 | Custom product properties + widgets |
| P1 | [US-2.1.5](../user-stories/02-storefront-and-catalog/README.md#us-215-product-detail-page-with-variant-configuration) | Storefront | 5 | PDP variant configuration |

## Key Deliverables

- S3 vault with SSE-KMS encryption for digital assets
- Ed25519 signing via KMS for .lic certificates
- Air-gapped QR challenge-response for offline activation
- CloudFront-served CRL binary for passive revocation checks
- AES-256-GCM CEK unsealing via X25519 key exchange

## Definition of Done

- [ ] Digital asset upload with SHA256 verification works
- [ ] Presigned download URL expires after 15 minutes
- [ ] Ed25519 offline verification completes in <0.2ms
- [ ] QR air-gapped activation end-to-end works
- [ ] CRL check returns 304 for non-revoked licenses
