# Sprint closeout test evidence

**Status: Pending — template only; no application tests have run.** Follow the [closeout policy](../SPRINT_TESTING.md) and the targets at the end of the relevant sprint plan.

## Candidate and accountability

| Field | Required evidence |
|:------|:------------------|
| Sprint / included stories and task IDs / plan | Pending |
| Approved company master-plan revision / expected-child manifest / canonical story-record links and acknowledged revisions | Pending |
| Spec Kit constitution/spec/plan/tasks and policy revisions | Pending |
| Candidate source/tree commit / deployable artifact digests | Pending |
| Prior accepted benchmark baseline commit | Pending |
| Test authors / contributor set / independent QA, security, architecture reviewers | Pending |
| G0/SG0-approved target inventory, workload, limits and thresholds | Pending |
| Environment, device/region/hardware, compiler/dependencies/tool versions | Pending |

## E1 — Benchmark results

| Target / invariant / source path | Baseline and candidate run IDs | Workload / concurrency / warm-up / samples / duration | Absolute budget / allowed regression | Observed baseline → candidate / variance / failure rate | Artifact / reviewer / result |
|:---------------------------------|:--------------------------------|:-----------------------------------------------------|:------------------------------------|:-------------------------------------------------------|:-----------------------------|
| Pending | Pending | Pending | Pending | Pending | Pending |

Attach at least three comparable measured runs; explain noise and any first-baseline decision. Report microbenchmark and service/device metrics separately, including resource cost and errors.

## E2 — Integration results

| Flow / AC/TC/task IDs | Real components / provider sandbox / platforms | Fault, race and recovery assertions | Expected / collected / passed / failed test counts | Candidate / artifact / independent reviewer | Result |
|:---------------------|:---------------------------------------------|:-----------------------------------|:--------------------------------------------------|:--------------------------------------------|:-------|
| Pending | Pending | Pending | Pending | Pending | Pending |

## E3 — Fuzz results

| Target / oracle / source path | Corpus digest / sanitizer / seed or replay parameters | Time/CPU/memory/input-size budgets and actual execution | Executions / coverage / saved regressions | Crash or invariant finding / minimized reproducer / fix | Artifact / reviewer / result |
|:-----------------------------|:----------------------------------------------------|:-------------------------------------------------------|:-----------------------------------------|:-------------------------------------------------------|:-----------------------------|
| Pending | Pending | Pending | Pending | Pending | Pending |

Separate intentional budget completion from infrastructure timeout/OOM or an actual resource-limit defect. Link replay results for every saved relevant regression.

## E4 — Loom results

| Model / production paths / invariant | Instrumentation / abstractions / memory orders | Threads / operations / branch, permutation, preemption limits | Observed exploration and completion / counterexample | Normal + Loom build/test artifacts | Reviewer / result |
|:------------------------------------|:----------------------------------------------|:-------------------------------------------------------------|:----------------------------------------------------|:-----------------------------------|:------------------|
| Pending | Pending | Pending | Pending | Pending | Pending |

Attach the model-to-production mapping, limitations and runtime tests for omitted behavior. If E4 is N/A, record all examined changed/affected paths, the scope rationale, alternative concurrency evidence and independent architecture + QA approval. Missing applicable code/harnesses remain Pending.

## E5 — Independent closeout decision

| Category | Expected targets / observed count | Candidate and artifact binding | Reviewer / date | Pass / Fail / Pending / reviewed N/A |
|:---------|:----------------------------------|:-------------------------------|:----------------|:------------------------------------|
| E1 Benchmark tests | Pending | Pending | Pending | Pending |
| E2 Integration tests | Pending | Pending | Pending | Pending |
| E3 Fuzz tests | Pending | Pending | Pending | Pending |
| E4 Loom concurrency tests | Pending | Pending | Pending | Pending |

- Open findings, blocked resources, exceptions with owner/expiry and repair task links:
- Candidate changes and the affected checks/reviews invalidated and rerun:
- Independent QA/security/architecture decisions and gatekeeper evidence verification:
- SG4/CTO review handoff and decision, separately from production authorization:

No sprint acceptance with missing/failed/stale required evidence or unreviewed exclusions. Preserve previous failures and candidate versions when repairs are applied.
