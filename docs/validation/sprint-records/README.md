# Canonical Sprint Records (Validation Mirror)

> **Location**: `docs/validation/sprint-records/` · **Operational Source**: [`docs/sprints/records/`](../../sprints/records/)  
> **Template**: [`SPRINT_TEST_EVIDENCE_TEMPLATE.md`](../SPRINT_TEST_EVIDENCE_TEMPLATE.md) & [`SPRINT_RECORD_TEMPLATE.md`](../../sprints/records/SPRINT_RECORD_TEMPLATE.md)

This directory is the formal validation review location for each sprint's complete operational history, test evidence bindings, and current handoff snapshot. Create **one file per sprint**, named `SPRINT-<id>.md` (e.g. `SPRINT-1.1.md`), when that sprint enters planning at SG0.

## Review & Validation Protocol

1. **Sprint Validation Record**: Tracks SG0–SG4 sign-offs, links to canonical user story records in [`docs/validation/story-records/`](../story-records/), and binds to the exact candidate commit SHA.
2. **Closeout Test Evidence (E1–E5)**: Binds to Criterion benchmarks, integration runs, fuzzing logs, Loom models, and final closeout packages in [`docs/reports/`](../../reports/).
3. **Audit Attestations**: Links to independent security, zero-clone, compliance, and quality gate reviews in [`docs/audits/`](../../audits/).
4. **Independent Authority**: The `senior-security-qa-auditor` writes exclusively to `docs/validation/**` and test execution runners, ensuring that audit and test sign-offs remain independent of implementation branches.
