# Report Category 01: Benchmarks & Performance (E1)

> **Test Category**: **E1 Benchmark Tests**  
> **Toolchain**: Criterion (Rust) · k6 / autocannon (HTTP/API) · Lighthouse / React Native Performance  
> **Governing Quality Gate**: **Gate G1**, **SG1**, **Gate M1**, **SG4**  
> **Accountable Roles**: `junior-testing-qa-engineer` / `senior-backend-engineer`

---

## 1. Overview & Methodology

The Benchmarks & Performance report category tracks microbenchmark and load-testing metrics across changed hot paths in each sprint, enforcing the performance standards established in [`docs/SPRINT_TESTING.md`](../../SPRINT_TESTING.md).

### Performance SLA Budgets:
- **L1 In-Memory Cache Read (Moka)**: P99 $< 0.1\text{ ms}$
- **Conditional HTTP 304 Not Modified Response**: P99 $< 0.15\text{ ms}$
- **Storefront Faceted Search & Filtering**: P95 $< 25\text{ ms}$
- **DynamoDB Single-Table Query**: P95 $< 10\text{ ms}$
- **Zero-Clone Heap Allocations**: 0 heap bytes allocated on cached read paths
- **Allowed Regression Threshold**: Maximum 5% regression over previous accepted baseline

---

## 2. Standard Benchmark Execution Command

```bash
# Rust Criterion Domain Microbenchmarks (Release Build on Graviton)
RUSTFLAGS="-C target-cpu=native" cargo bench --workspace --all-targets

# API Concurrency & Latency Profile (autocannon / k6)
k6 run tests/load/storefront_sdui_load.js --vus 100 --duration 5m
```

---

## 3. Sprint Benchmark Report Catalog

| Report File | Sprint | Hot Path Tested | Target SLA | Status |
|:------------|:-------|:----------------|:-----------|:-------|
| `REPORT-BENCH-sprint-1.1-sdui-cache.md` | Sprint 1.1 | SDUI cache read, ETag 304 response, faceted search | P99 < 0.1ms | Pending |
| `REPORT-BENCH-sprint-1.2-cart-carrier-quotes.md` | Sprint 1.2 | Cart sync, checkout reservation, carrier fee calc | P95 < 20ms | Pending |
| `REPORT-BENCH-sprint-2.1-crypto-verify.md` | Sprint 2.1 | Ed25519 signature verification, Bloom filter search | P99 < 0.2ms | Pending |
| `REPORT-BENCH-sprint-2.2-sdk-evaluation.md` | Sprint 2.2 | Cross-SDK token evaluation, license vault render | P95 < 5ms | Pending |
| `REPORT-BENCH-sprint-3.1-moq-tier-pricing.md` | Sprint 3.1 | B2B tiered pricing matrix, parallel carrier quotes | P95 < 15ms | Pending |
| `REPORT-BENCH-sprint-3.2-lan-seat-checkout.md` | Sprint 3.2 | LAN proxy concurrent seat allocation & checkout | P99 < 1ms | Pending |
| `REPORT-BENCH-sprint-4.1-suborder-splitting.md` | Sprint 4.1 | Multi-vendor cart splitting & fee distribution | P95 < 10ms | Pending |
| `REPORT-BENCH-sprint-4.2-ledger-posting.md` | Sprint 4.2 | Double-entry balanced ledger postings & reconciliations | P99 < 5ms | Pending |
| `REPORT-BENCH-sprint-5.1-metering-throughput.md` | Sprint 5.1 | SaaS metering batch accumulator flush throughput | 1,000 rec/s | Pending |
| `REPORT-BENCH-sprint-6.1-sdui-studio-rendering.md` | Sprint 6.1 | SDUI studio live preview AST compile & render | P99 < 16ms | Pending |
| `REPORT-BENCH-sprint-6.2-whitelabel-bundle-size.md` | Sprint 6.2 | Expo client bundle size & cold startup time | < 2.5MB / < 800ms | Pending |
| `REPORT-BENCH-sprint-6.3-full-platform-load.md` | Sprint 6.3 | Full platform production workload P95/P99 SLA | P95 < 150ms | Pending |

---

## 4. How to Record a Benchmark Report

1. Copy `../REPORT_RECORD_TEMPLATE.md` to `docs/reports/01-benchmarks-and-performance/REPORT-BENCH-<sprint>-<topic>.md`
2. Run benchmark suites across at least three comparable runs.
3. Compare candidate metrics against the accepted baseline commit.
4. Record observed variances and sign off under `junior-testing-qa-engineer` and `senior-backend-engineer`.
