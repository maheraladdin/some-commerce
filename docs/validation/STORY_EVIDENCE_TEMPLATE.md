# Story validation evidence template

Status: **Pending — template only; no checks have run.**

Use one record per story/release candidate. Replace placeholders before review; a completed checkbox without a linked result is not evidence. See [quality gates](../QUALITY_GATES.md).

| Field | Value |
|:------|:------|
| Story ID and specification | Pending |
| Scope / affected layers and platforms | Pending |
| Source commit / PRs / release candidate | Pending |
| Story owner / test reviewer / security reviewer / architecture reviewer | Pending |
| Dependency stories and blocking findings | Pending |
| ADR or design note / threat model | Pending |
| Runtime, tool versions, advisory database date, test environment | Pending |

## Requirement-to-test traceability

| AC / TC / story gate scenario | Test path and name | Level / platform | Expected assertion | Run artifact / commit | Result |
|:----------------------------|:-------------------|:-----------------|:-------------------|:----------------------|:-------|
| Pending | Pending | Pending | Pending | Pending | Pending |

Include all original ACs and TCs as well as the story-specific validation scenarios. Link manual accessibility/provider evidence where applicable and explain why it is manual.

## Gate results

| Gate | Evidence required | Artifact / commit | Reviewer / date | Result |
|:-----|:------------------|:------------------|:----------------|:-------|
| G0 | Dependencies, decisions, contracts, numeric budgets | Pending | Pending | Pending |
| G1 | Test runs, per-package changed/total line and branch coverage, critical mutation report | Pending | Pending | Pending |
| G2 | Threat review, authorization matrix, SAST/SCA/secrets/IaC/runtime findings, SBOM | Pending | Pending | Pending |
| G3 | Import graph, lint/types, duplication report, reuse/change exercise, complexity review | Pending | Pending | Pending |
| G4 | Full flow, provider/platform checks, load/fault results, migration/rollback, operational drill | Pending | Pending | Pending |

## Performance and recovery evidence

| Scenario | Dataset / device / environment | Arrival rate / concurrency / duration / samples | Budget | Observed percentile / errors / resource cost | Artifact |
|:---------|:-------------------------------|:-----------------------------------------------|:-------|:-------------------------------------------|:---------|
| Pending | Pending | Pending | Pending | Pending | Pending |

For stateful features record recovery point/time objectives and measured restore results. Record repeated-event counts and final financial/inventory state for concurrency/fault tests.

## Reuse and maintainability review

- Existing components reused; domain policy owner:
- Duplicate logic removed or justified; detector scope and result:
- New abstraction and concrete consumer/substitution need:
- Complexity/size triggers and reviewer disposition:
- Change exercise and affected files:
- Public contract / migration / consumer compatibility:

## Exceptions and outstanding work

| Criterion / finding | Severity | Reason / compensating evidence | Owner / issue | Independent approval | Expiry | Status |
|:--------------------|:---------|:-------------------------------|:--------------|:---------------------|:-------|:-------|
| Pending review | Pending | Pending | Pending | Pending | Pending | Pending |

Mark this table “None” only after review. A story is Done only when G0–G4 pass and there are no unresolved blockers or expired exceptions.
