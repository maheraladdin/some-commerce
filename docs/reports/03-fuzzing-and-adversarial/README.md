# Report Category 03: Fuzzing & Adversarial Testing (E3)

> **Test Category**: **E3 Fuzz Tests**  
> **Toolchain**: `cargo-fuzz` / `libFuzzer` · AddressSanitizer (ASan) · UndefinedBehaviorSanitizer (UBSan)  
> **Governing Quality Gate**: **Gate G2**, **SG2**, **SG4**  
> **Accountable Roles**: `senior-security-qa-auditor` / `backend-engineer`

---

## 1. Overview & Methodology

The Fuzzing & Adversarial report category captures continuous coverage-guided fuzz testing and property-based verification, as mandated by [`docs/SPRINT_TESTING.md`](../../SPRINT_TESTING.md) and [`docs/QUALITY_GATES.md`](../../QUALITY_GATES.md).

### Fuzzing Invariants & Budgets:
- **Minimum Execution Budget**: Mandatory **600 seconds of continuous fuzzing per new or changed target**.
- **Corpus Retention**: Prior crash reproducers and regression corpora must be replayed against the candidate.
- **Assertion Bounds**: Targets must assert semantic domain invariants and tenant scoping, not merely "does not panic".
- **Zero Crash Requirement**: Any crash, OOM, sanitizer finding, or invariant failure blocks sprint closeout until a minimized reproducer is triaged, fixed, and committed as a regression test.

---

## 2. Standard Fuzzing Execution Command

```bash
# Run coverage-guided fuzzer with ASan / UBSan for at least 600 seconds
cargo fuzz run fuzz_target_name -- -max_total_time=600 -rss_limit_mb=2048 -seed=42

# Replay regression corpus
cargo test --test fuzz_regression_replay
```

---

## 3. Sprint Fuzzing Report Catalog

| Report File | Sprint | Parser / Target Fuzzed | Status |
|:------------|:-------|:-----------------------|:-------|
| `REPORT-FUZZ-sprint-1.1-jwt-sdui-parsers.md` | Sprint 1.1 | Phone/locale decoders, JWT claim parser, SDUI JSON AST block decoder | Pending |
| `REPORT-FUZZ-sprint-1.2-webhooks-money-units.md` | Sprint 1.2 | Paymob/Stripe webhook decoders, Money minor-unit overflow parser | Pending |
| `REPORT-FUZZ-sprint-2.1-crl-qr-binary-parsers.md` | Sprint 2.1 | Ed25519 license binary decoder, Bloom filter CRL parser, QR payload | Pending |
| `REPORT-FUZZ-sprint-2.2-versioned-certs.md` | Sprint 2.2 | Cross-SDK certificate parser, wishlist JSON mutation sequences | Pending |
| `REPORT-FUZZ-sprint-3.1-moq-customs-fields.md` | Sprint 3.1 | B2B tiered discount expressions, customs declaration payload decoders | Pending |
| `REPORT-FUZZ-sprint-3.2-rfq-lan-seat-tokens.md` | Sprint 3.2 | RFQ revision parser, LAN seat token decoders, invoice cursors | Pending |
| `REPORT-FUZZ-sprint-4.1-vendor-mcp-arguments.md` | Sprint 4.1 | Sub-order split allocator, untrusted WebMCP tool JSON argument parser | Pending |
| `REPORT-FUZZ-sprint-4.2-btcpay-ledger-decoders.md` | Sprint 4.2 | BTCPay server webhook decoders, ledger transaction journal inputs | Pending |
| `REPORT-FUZZ-sprint-5.1-metering-dimensions.md` | Sprint 5.1 | AWS Marketplace metering batch decoders, subscription event schemas | Pending |
| `REPORT-FUZZ-sprint-6.1-sdui-ast-deep-nesting.md` | Sprint 6.1 | Recursive SDUI AST depth fuzzing, malformed props, unsafe URL inputs | Pending |
| `REPORT-FUZZ-sprint-6.2-whitelabel-metadata.md` | Sprint 6.2 | Brand config JSON, dynamic Expo plugin parameters, SVG image parsers | Pending |
| `REPORT-FUZZ-sprint-6.3-monorepo-regression.md` | Sprint 6.3 | Comprehensive replay of all cumulative saved crash corpora across all crates | Pending |

---

## 4. How to Record a Fuzzing Report

1. Copy `../REPORT_RECORD_TEMPLATE.md` to `docs/reports/03-fuzzing-and-adversarial/REPORT-FUZZ-<sprint>-<topic>.md`
2. Run coverage-guided fuzzers for the required $\ge 600\text{s}$ duration.
3. Record elapsed time, iterations, code coverage, and corpus size.
4. Verify zero crashes occurred; sign off under `senior-security-qa-auditor`.
