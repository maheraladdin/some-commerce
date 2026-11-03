# Security Gateway Template (Powered by security-audit)

## 1. Security Overview & Trust Boundaries
- **Trust Boundaries**:
  - Untrusted Boundary: Client App / Mobile WebView / Web Browser / Public API
  - Authentication Boundary: Amazon Cognito / JWKS Verifier / Pre-Token Trigger
  - Application Boundary: Axum Tower Route Guards / Tenant Isolation Extractor
  - Data / Secret Boundary: DynamoDB Single-Table / KMS Hardware Security Modules / ElastiCache Redis
- **Principal & Authentication Matrix**:
  - Allowed Actors: [Anonymous, Authenticated Customer, B2B Buyer, Vendor, Store Admin]
  - Required Scopes / Claims: `custom:tenant_id`, `custom:persona`, `sub`
  - Zero-Trust Invariant: `TenantId` must be derived strictly from the verified JWT claims, never from user query params or payload body.

## 2. Threat Modeling & Abuse Matrix (STRIDE / ASVS)
| Attack Vector | Threat Level | Vulnerability Mechanism | Mitigating Control & Security Invariant |
| :--- | :--- | :--- | :--- |
| **Spoofing / Impersonation** | High | Forged `sub` or `tenant_id` claims | Server-side RS256 JWKS token signature validation + Cognito Claims verification |
| **Tampering** | High | Client payload modification / price tampering | Server-side recalculation from authoritative DB state; strict schema validation |
| **Information Disclosure** | High | IDOR / cross-tenant query leakage | Enforce tenant-scoped partition keys (`PK = TENANT#<id>`) on all queries |
| **Denial of Service** | Medium | Brute-force requests / SMS bombing | Token-bucket rate limiting per IP and per account in API Gateway / Axum middleware |
| **Elevation of Privilege** | Critical | Unauthorized admin action execution | Axum `RequireStoreAdmin` / `RequireVendor` RBAC guard checks on route handlers |

## 3. Cryptographic Controls & Data Protection
- **Transit Protection**: TLS 1.3 mandatory; strict HSTS headers.
- **Rest Protection**: DynamoDB AWS-managed KMS key; S3 SSE-KMS for digital assets; AES-256-GCM for sensitive client storage.
- **Secret Redaction**: PII, credit card tokens, passwords, and OTPs stripped from logs and traces via `tracing` redaction layers.
- **Session Security**: Ephemeral tokens stored in `expo-secure-store` (iOS Keychain / Android Keystore).

## 4. Automated Security Verification Gates
- [ ] **SAST Analysis**: Zero high/critical issues from static code analysis.
- [ ] **Dependency Audit**: `cargo deny` and `bun audit` clean; 0 known vulnerabilities.
- [ ] **Abuse / Fuzz Testing**: Boundary violation tests with forged tenant/role parameters fail with 401/403.
- [ ] **Secret Scan**: Automated gitleaks check passes with zero hardcoded credentials or test API keys.

## 5. Security Gateway (G2) Sign-Off Checklist
- [ ] Threat boundary and entry points verified against ASVS Level 2 requirements.
- [ ] Multi-tenant isolation verified with automated cross-tenant penetration test.
- [ ] Anti-abuse and rate limiting confirmed active on all public interfaces.
- [ ] Audit log redaction verified — zero plaintext secrets in output logs.
- [ ] Independent reviewer sign-off obtained; zero open Critical or High findings.
