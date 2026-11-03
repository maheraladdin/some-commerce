# Canonical story record: US-[id]

**Status: template only — no actions, approvals or tests have been executed.** Create one record at `docs/validation/story-records/US-<id>.md` when a story enters planning. Do not invent missing historical events. See constitution sections 10–11 and the [framework](../AGENT_PROFILES_AND_MULTI_AGENT_FRAMEWORK.md).

## Identity and authoritative references

| Field | Value |
|:------|:------|
| Story ID / specification path and revision | Pending |
| Canonical record path / controller revision / last event sequence | Pending |
| Authorized request / CTO charter / PM requirement IDs | Pending |
| Master plan revision/digest / parent node / expected child tasks | Pending |
| Plan/tasks/Security Gateway/contract/policy revisions | Pending |
| Accountable story owner / current role / independent reviewers | Pending |

## Current handoff snapshot

This is a derived current view; the event history below preserves prior states. Update it through controller revision checks, not competing role edits.

- Phase/stage and current assignment/attempt:
- Exact candidate/base/tree/build artifact digests:
- Completed tasks and evidence references:
- Remaining expected child/tasks/actions and dependency conditions:
- Required check results, unresolved findings/repairs and invalidated prior approvals:
- Blockers with owner, deadline and next action:
- Current owner → next role/assignment, receipt event and acknowledged revision:
- Last reconciliation event; history complete from which intake event (any earlier history unknown):

## Append-only action and decision history

| Sequence / event ID / UTC time | Actor identity / role / account / assignment-attempt | Intent/result and correlation or prior event | Master plan / parent / task / AC-TC IDs | Candidate/base/contract/policy revisions | Action/tool/command and scoped paths (redacted) | Outcome / error / decision / next action | Artifact references and digests |
|:------------------------------|:---------------------------------------------------|:---------------------------------------------|:---------------------------------------|:----------------------------------------|:----------------------------------------------|:----------------------------------------|:--------------------------------|
| Not initialized | Pending | Pending | Pending | Pending | Pending | No historical action asserted | Pending |

Record planning/context reads, assignments, scoped tool/command calls, edits, external operations, tests/benchmarks/fuzz/Loom runs, reviews, findings, fixes, approvals/rejections, ownership/account changes, blockers/recovery, handoffs and final CTO decisions. Link intent and outcome events; include failures and cancelled/unknown outcomes. Shared multi-story actions reference the same event/artifact ID here and in each affected record. Store no credentials, raw sensitive data or private reasoning.

## Artifact and validation index

| Action / requirement / task | Immutable artifact path or run URL / digest | Candidate and producer | Result / independent reviewer / event IDs |
|:---------------------------|:-------------------------------------------|:-----------------------|:-------------------------------------------|
| Pending | Pending | Pending | Pending |

Link story G0–G4, G-Review, G-Borrow, G-UI, G-Law, and sprint E1–E5/SG0–SG4 evidence here, rather than making a separate role record authoritative. Large logs and restricted artifacts stay in suitable storage. A digest binds content; verify the trusted producer/issuer too.

## Handoff checklist (one event-backed instance per transfer)

- [ ] Expected tasks/actions and artifacts reconciled; no silently omitted failed child.
- [ ] Snapshot names exact candidate, blockers/findings, independent review needs and next executable action.
- [ ] Writer stopped, lease/capability transfer recorded, successor item durably queued.
- [ ] Next role acknowledges the record revision and assignment; prior owner/controller retains accountability until receipt.
- [ ] Repairs issue a new candidate, preserve original findings/history and invalidate affected evidence.
- [ ] CTO receives original charter/AC-to-delivery traceability and complete integrated evidence before a final decision.

Only a trusted, authenticated controller may serialize final events/decisions. Markdown is the canonical review location; production enforcement needs protected append-only/event storage and a verified projection. Missing logging, stale revision, duplicate conflicting event or unacknowledged transfer blocks dependent work/promotion. Correct mistakes by appending a linked correction event.
