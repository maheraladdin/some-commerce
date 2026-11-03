# Canonical Report Record: REPORT-[CATEGORY]-[SPRINT]-[TOPIC]

> **Status: Template Only — Pending Formal Execution**  
> Formulate from this template when recording test suite results. See [Report Master Index](./README.md) and [SPRINT_TESTING.md](../SPRINT_TESTING.md).

---

## 1. Report Identity & Execution Context

| Metadata Field | Value |
|:---------------|:------|
| **Report Identifier** | `REPORT-<CATEGORY>-<SPRINT>-<TOPIC>` |
| **Report Category** | `[01-Benchmarks | 02-Integration | 03-Fuzzing | 04-Concurrency | 05-Closeout]` |
| **Target Sprint / Slice** | `Sprint X.Y (vZ.0)` |
| **Associated User Stories** | `[US-X.Y.Z, ...]` |
| **Candidate Tree / Commit SHA** | `Pending (git rev-parse HEAD)` |
| **Prior Accepted Baseline Commit** | `Pending (git rev-parse baseline)` |
| **Deployable Artifact Digests** | `Pending (sha256:...)` |
| **Executing Test Engineer** | `junior-testing-qa-engineer` / `backend-engineer` |
| **Independent Senior Reviewer** | `testing-qa-engineer` / `senior-security-qa-auditor` |
| **Environment / Hardware / Architecture** | `AWS Graviton c7g.xlarge / Linux aarch64 / rustc 1.85+` |
| **Execution Date & Duration** | `YYYY-MM-DD (Elapsed: XXm YYs)` |
| **Final Test Verdict** | **`[PENDING | PASSED | FAILED | RE-RUN_REQUIRED]`** |

---

## 2. Executive Summary & Verdict

*Provide a concise 2–3 paragraph summary of the test campaign, workloads executed, regression checks compared against baselines, and conclusive verdict for quality gate progression.*

---

## 3. Workload Parameters & Execution Setup

| Parameter | Configuration Value | Justification / Notes |
|:----------|:--------------------|:----------------------|
| **Target Harness / Binary** | `crates/<crate>/benches/<bench>.rs` | Hot path under test |
| **Warm-up Duration** | `30 seconds` | JIT / cache saturation |
| **Measurement Duration** | `300 seconds` | Statistical stability |
| **Concurrency / Worker Tasks** | `100 concurrent Tokio tasks` | Simulates peak merchant traffic |
| **Dataset Size & Fixtures** | `10,000 SKUs, 50,000 synthetic orders` | Representative production scale |
| **Fuzzing Budget / Seed** | `600 seconds per target / seed: 42` | Mandated ASVS closeout minimum |

---

## 4. Quantitative Results & Regression Analysis

| Target Metric / Flow | Prior Baseline | Candidate Observed | Delta (%) | Approved Budget | Variance / Status |
|:---------------------|:---------------|:-------------------|:----------|:----------------|:------------------|
| *L1 Cache Read P99* | `0.082 ms` | `0.079 ms` | `-3.6%` (faster) | `< 0.100 ms` | **PASSED** |
| *Axum ETag 304 Latency* | `0.110 ms` | `0.112 ms` | `+1.8%` | `< 0.150 ms` | **PASSED** |
| *DynamoDB Put P95* | `4.2 ms` | `4.3 ms` | `+2.3%` | `< 10.0 ms` | **PASSED** |
| *Allocations per Request* | `0 heap bytes` | `0 heap bytes` | `0.0%` | `0 bytes (Zero-Clone)` | **PASSED** |

> [!WARNING]
> Any latency regression greater than **5.0%** over the accepted baseline blocks sprint closeout until triaged and resolved.

---

## 5. Execution Commands & Raw Log Digest

```bash
# Exact execution command:
RUSTFLAGS="-C target-cpu=native" cargo bench --bench sdui_cache_bench -- --verbose

# Run digest / artifact link:
# Artifact: docs/reports/artifacts/benchmarks/sprint-1.1/criterion-report.tar.gz
# SHA-256 Digest: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

---

## 6. Flakiness, Concurrency & Adversarial Findings

| Incident ID | Target Component | Type (Crash / Timeout / Race / Invariant) | Minimized Reproducer | Root Cause & Resolution |
|:------------|:-----------------|:-----------------------------------------|:---------------------|:------------------------|
| N/A | None | Clean run | N/A | Zero crashes observed |

---

## 7. Independent Reviewer Sign-Off

| Review Role | Reviewer Identity | Signature / Attestation | Date | Sign-Off Status |
|:------------|:------------------|:------------------------|:-----|:----------------|
| **Executing Test Engineer** | `junior-testing-qa-engineer` | Certified execution commands and raw output | YYYY-MM-DD | `[SUBMITTED]` |
| **Independent Senior QA** | `testing-qa-engineer` | Validated test harness and budget thresholds | YYYY-MM-DD | `[APPROVED | REJECTED]` |
| **Release Gatekeeper** | `release-gatekeeper` | Verified candidate binding and run digests | YYYY-MM-DD | `[ACCEPTED | BLOCKED]` |
| **CTO Closeout Acceptance** | `chief-technology-officer` | Concurrence for SG4 release recommendation | YYYY-MM-DD | `[RECOMMENDED]` |
