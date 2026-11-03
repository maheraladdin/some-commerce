# End-of-sprint benchmark, integration, fuzz and Loom gates

## Scope and timing

Every sprint ends with E1–E5 below, including infrastructure, client-focused and final hardening sprints. These checks are prerequisites for **SG4 and CTO review**, supplementing SG1 integration, SG2 security and SG3 architecture checks. They do not postpone per-story G1–G4 or replace required reviews. Each [sprint plan](sprints/README.md) ends with its specific test targets.

**Current status: specification only.** The repository has no application Cargo manifests or runnable Rust benchmark/fuzz/Loom harnesses. Required application tests remain Pending until those implementations exist and run. Documentation checks verify the presence and consistency of these requirements only.

At SG0 approve the candidate scope, test owners and independent reviewers, executable target inventory, AC/TC/task mapping, environment, data fixtures, performance budgets, fuzz resources and Loom exploration bounds. Use Spec Kit plan/tasks and the [sprint evidence template](validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md). Test authors may operate in parallel with disjoint leases; their work and review capacity must be included in sprint estimates.

Run on the exact combined candidate after integration. Record source/tree and artifact digests, dependency/toolchain versions and commands. Any repair or relevant input change invalidates affected results and requires revalidation before promotion. Independent senior QA owns E1/E2 review, security/QA owns E3, architecture/QA owns E4; the gatekeeper verifies E5 and the CTO reviews the complete evidence package. An author cannot independently approve their own harness or repair.

## E1 — Benchmark tests

Benchmark the sprint's changed hot paths and affected existing baselines, including throughput, latency distributions, allocations/peak memory and relevant infrastructure costs. Use release builds, fixed datasets and comparable hardware/device/region/compiler settings. Distinguish domain microbenchmarks from HTTP/device/load tests; a microbenchmark timing is not a service p99.

- Rust domain routines can use [Criterion](https://bheisler.github.io/criterion.rs/book/), which records statistical measurements and supports regression comparison. Client/infra paths require appropriate browser/device/load/deployment measurements too.
- At SG0 name the last accepted baseline commit and absolute budgets plus the maximum permitted change for each metric. Unless a stricter approved threshold applies, more than 5% worsening of a key latency, memory or throughput metric blocks closeout until triaged. Compare on the same environment with at least three measured runs and recorded warm-up/sample configuration; investigate noise rather than approving from one favorable run.
- Record workload, dataset size, arrival rate/concurrency, warm/cold state, duration, completed request/sample counts and failure rates. Do not omit timeouts/failures from performance reporting. Validate low-traffic and saturation behavior, resource limits and tenant fairness where applicable.
- The first implementation establishes a baseline and still must meet approved absolute budgets. If comparable baseline/environment data are missing, the result is Pending; do not compare incompatible machines or reset the baseline to hide a regression. Changing a threshold requires independent approval and preserves the original failure.

## E2 — Integration tests

Run complete cross-story flows for the sprint plus affected regressions from previous sprints. Verify actual interfaces and state across domain rules, repository transactions/conditional writes, caches, events/workers, APIs and affected web/iOS/Android clients. Include real isolated storage/provider sandbox checks where mocks cannot establish behavior.

Exercise success, ownership denial, malformed/expired input, duplicated/reordered events, unknown external outcomes, cancellation, retry, process restart, partial failure and recovery. Assert final inventory, money/ledger, entitlements, state and side-effect counts. Use controlled clocks for long-running workflows. Test schema upgrade/rollback and local sync/account isolation where affected.

Record backend and platform test counts, required provider checks, fixtures, environment isolation and explicit limitations. Missing infrastructure/provider access leaves the relevant requirement Pending. A stubbed adapter is useful for unit tests but cannot alone satisfy integration acceptance. Use only authorized synthetic environments and data; deployment/publication is a separate action.

## E3 — Fuzz tests

“Fuzz tests” means generated adversarial inputs and state sequences with assertions, not merely random happy-path fixtures. Use coverage-guided [cargo-fuzz/libFuzzer](https://rust-fuzz.github.io/book/cargo-fuzz.html) for applicable Rust parsers/protocols; use appropriate schema/property/state-machine generators for TypeScript and infrastructure inputs. Property tests supplement coverage-guided fuzzing rather than being relabelled as it.

- Inventory targets for parsers, validation, license/QR/CRL formats, webhook decoders, money/quantity boundaries, query/SDUI schemas and operation/event sequences affected by the sprint. Add assertions for semantic invariants, tenant scope and bounded work; “does not panic” alone is insufficient.
- Default closeout budget is at least **600 seconds of fuzz execution per new/changed coverage-guided target**, with the prior saved regression corpus replayed and affected existing targets included. Approve the per-target time/iteration, input-size, memory and CPU budgets at SG0. A shorter budget requires a documented independent scope/risk decision; elapsed startup/build time is not fuzz execution time.
- Preserve toolchain/sanitizer configuration, corpus digest, seed/replay parameters when supported, executions/coverage metrics, elapsed fuzzing time and resource bounds. Distinguish intended budget termination from an unexpected timeout, OOM, sanitizer finding, harness crash or infrastructure failure.
- Every crash/invariant violation needs a minimized reproducer, owner, fix and deterministic regression test. Replay all relevant saved reproducers on the candidate. Unresolved findings block closeout; deleting a reproducer, shrinking scope silently or rerunning with a different seed does not resolve a failure. Store synthetic/redacted inputs only.

## E4 — Loom concurrency tests

Use [Loom](https://docs.rs/loom/latest/loom/) for changed or affected **in-process Rust shared-state synchronization**: atomics, locks, channels, publication, cancellation and ownership handoffs. Loom requires deterministic models and instrumented synchronization; ordinary `std`/Tokio/third-party primitives are not automatically explored by putting them inside `loom::model`. Its model and memory-ordering limitations must remain visible.

- Introduce a small conditional synchronization boundary so normal and Loom builds exercise the same production coordination algorithm. Use Loom synchronization/thread primitives in the model configuration and normal primitives in the production configuration. Compile/test both; a separately copied toy algorithm does not prove the implementation.
- Map models to actual source paths and invariants. Test bounded competing operations, cancellation/drop, stale versions and lock acquisition sequences. Assert no double acceptance, lost updates, invalid publication or deadlock in the specified model. Model opaque dependencies at explicit boundaries, and retain runtime tests for behavior the model omits.
- Approve and report threads, operation counts, memory-order assumptions, branch/permutation/preemption bounds, exploration configuration and the environment/tool version. Require each model to finish its configured exploration without violations. A timeout, unexplored configured schedules or reduced bounds after failure is Pending/Fail, never Pass. Clearly distinguish bounded completion from proof over arbitrary executions; review the bound and abstractions independently.
- Keep concurrency models deterministic: abstract clock, network, random inputs and external state explicitly. Loom does not prove DynamoDB transactions, distributed leases, third-party cache internals, TypeScript concurrency or real provider side effects. Race/retry integration tests remain required for those systems.
- Every sprint reviews and reruns affected existing Loom models. For each introduced/changed Rust coordination component, add or extend a corresponding model. For a sprint with **no changed or affected Rust shared-state coordination**, E4 can be N/A only after architecture + QA approve an inventory of examined paths, why no model applies, and alternative runtime concurrency tests. Missing Rust code/harnesses for an applicable requirement is Pending, not N/A. A client-only change does not justify skipping affected backend models.

Commands must name real package/test/target IDs in the approved plan. For a configuration using `cfg(loom)`, the Loom documentation illustrates a separate `RUSTFLAGS="--cfg loom" cargo test --test <actual-model-target> --release` run; replace the target, pin tools and configure supported cfg checking before execution. This example is not an implemented repository command. Keep Loom dependencies/configuration isolated from production artifacts and audit the actual dependency graph rather than assuming a crate name grants kernel purity.

## E5 — Evidence, pipeline and acceptance

Create a sprint-specific record from the [evidence template](validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md). Store raw result artifacts and authenticated independent decisions for E1–E4, with a manifest of **expected targets and observed counts**. Reports must bind to the candidate and approved Spec Kit/test-policy revisions. Required suites must collect actual tests/models/targets; a zero-test exit code is not success.

All four categories require a reviewed disposition. Benchmarks, integration and fuzz testing cannot be omitted wholesale; choose valid workload/input targets even for infrastructure work. Scope-based E4 N/A follows the narrow process above; any other permitted sub-check exclusion must be explicit, independently justified and consistent with quality gates. Missing, stale, skipped, cancelled, malformed or failed required results block SG4. No runtime result is inferred from a checked documentation box.

The continuous controller enqueues this suite when the sprint candidate is ready and lets unrelated approved work continue. Tests can run in parallel only with isolated resources; benchmarks need controlled load. A senior applying a fix creates a new candidate and obtains independent re-review plus affected E1–E4 reruns. Queue saturation, missing resources or bounded retry exhaustion produces a visible blocker, not automatic approval. CTO review receives the complete closeout evidence before a release recommendation.
