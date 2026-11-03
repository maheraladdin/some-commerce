# Company master implementation plan: [Initiative / sprint]

**Status: Draft — not an implementation or release authorization.** Apply constitution section 10 and framework P0–P4. Each row requires an actual owner, revision and evidence before its stage exits.

## 1. Executive direction and approved request (P0)

- Authorized request/initiative ID and accountable CTO/operator:
- Goals, product outcomes, non-goals and explicit authority limits:
- Numeric success criteria, risk/cost/capacity constraints and decision deadlines:
- Approved upstream charter reference/digest and planning-task IDs:

## 2. Product specification (P1)

- PM owner; Spec Kit spec revision/digest; personas and included/excluded stories:
- Requirement and AC/TC IDs; observable success/error/denial outcomes:
- Priorities, product acceptance method and approved scope decisions:

## 3. Architecture and specialist subplans (P2)

| Parent/workstream node | Role owner | Upstream inputs and revisions | Planned outputs / canonical rule ownership | Contracts, dependencies and shared paths | Acceptance and reviewer |
|:-----------------------|:-----------|:------------------------------|:-------------------------------------------|:----------------------------------------|:------------------------|
| Pending | Pending | Pending | Pending | Pending | Pending |

Include affected backend/client, senior engineering, QA/security, design and DevOps plans. Record justified omissions. Address threat boundaries, state/data ownership, migrations/recovery, useful abstraction/reuse, supported platforms and consumer compatibility. Scope exploratory planning tasks explicitly; they cannot dispatch implementation.

## 4. Reconciled master plan and work decomposition (P3)

- Tech lead, master plan ID/revision/digest and integration owner:
- Conflicts, duplicate responsibilities and missing requirements resolved:
- Capacity, independent reviewers, quota pools, stage WIP and retry/repair budgets:

| Task / child node | Parent node | Role / accountable owner | AC/TC IDs | Incoming dependency and evidence condition | Exact write scope / contract revision | Deliverable / test oracle | Independent reviewer / next upward handoff |
|:------------------|:------------|:-------------------------|:----------|:-------------------------------------------|:--------------------------------------|:-------------------------|:-------------------------------------------|
| Pending | Pending | Pending | Pending | Pending | Pending | Pending | Pending |

Declare dependency-safe parallel groups and shared-file serialization; verify no cycles or orphan nodes. Each included requirement maps to owned tasks and final acceptance evidence. No task is created solely to fill seven PR layers.

Every story/task row must link the canonical `docs/validation/story-records/US-<id>.md`, including current record revision and required event/handoff IDs. Shared initiative decisions are referenced from each affected story record with the same decision/event ID.

## 5. Planning approval and dispatch baseline (P4)

| Decision | Authenticated reviewer | Exact charter/spec/master/contract revisions | Evidence / date | Approved / Changes Required / Blocked |
|:---------|:-----------------------|:--------------------------------------------|:----------------|:-------------------------------------|
| PM product scope | Pending | Pending | Pending | Draft |
| Architecture/security controls | Pending | Pending | Pending | Draft |
| CTO direction and plan baseline | Pending | Pending | Pending | Draft |

Record G0/SG0 disposition for the approved scope/wave. Implementation is blocked until required approvals exist. Planning tasks use the approved upstream request plus assigned draft outputs, not a fabricated approval of the plan they are creating.

## 6. Expected child manifest and collection

| Parent | Expected child/task IDs | Required outputs / candidate commits / evidence | Received and independently verified | Missing/failed/stale child / owner / next action |
|:-------|:------------------------|:-----------------------------------------------|:------------------------------------|:------------------------------------------------|
| Pending | Pending | Pending | Pending | Pending |

Collect every required child; validate interfaces and completeness before parent acceptance. Preserve original failures and repair/contributor history. Approved scope changes explicitly revise the manifest and invalidate affected descendants/reviews.

## 7. Integrated validation and upward return

- Exact assembled source/tree/build digests and consumer compatibility evidence:
- G1–G4 and SG0–SG4 references; [E1–E5 closeout evidence](../../docs/validation/SPRINT_TEST_EVIDENCE_TEMPLATE.md):
- Original charter/requirement/AC → task/PR → artifact/test result traceability:
- Independent senior → tech lead → QA/security/architecture → PM decisions:
- CTO final dossier and decision: Accepted / Changes Required / Blocked, with affected plan nodes and reasons:
- Replan/repair assignments, invalidated evidence, remaining risks and explicit deployment authorization (separate):

Do not mark the parent complete on a subset of successful children. Individual PR approval does not prove assembled behavior. Any final repair requires an independent reviewer and affected integration reruns before returning to CTO.
