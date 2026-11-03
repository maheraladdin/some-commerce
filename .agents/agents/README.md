# Agent roles and shared authentication accounts

`agent-a`, `agent-b` and `agent-c` can each execute **every company role**. They are separate authentication/quota pools; they are not permanent backend, frontend or QA teams. A role defines responsibilities and validation duties; an assignment supplies the approved Spec Kit context, detailed task and narrow permissions.

## Accounts

| Account | Definition | Eligible roles |
|:--------|:-----------|:---------------|
| agent-a | [Account A](agent-a/agent.md) | All 17 roles |
| agent-b | [Account B](agent-b/agent.md) | All 17 roles |
| agent-c | [Account C](agent-c/agent.md) | All 17 roles |

Sign in to the three accounts separately using the existing account homes:

```bash
./scripts/agents/agy_agent.sh a
./scripts/agents/agy_agent.sh b
./scripts/agents/agy_agent.sh c
```

These are interactive sessions; close each when finished. Use the role launcher for an assigned task:

```bash
./scripts/agents/agy_agent.sh junior-backend-engineer -p "Implement the approved assigned task"
./scripts/agents/agy_agent.sh senior-client-engineer -p "Validate the assigned candidate"
./scripts/agents/agy_agent.sh chief-technology-officer -p "Review the supplied release evidence"
```

The launcher atomically reserves an available account with the lowest recorded normalized usage, considering active reservations, configured budget, cooldown, disabled state and concurrency. The same role can use any account. Default concurrency is one active launcher per account to protect shared authentication state. When all pools are unavailable, the launch fails with a reason instead of starting work on an exhausted pool.

## Usage and quota controls

The local ledger is `.agent_profiles/quota.json` (ignored by Git). It contains usage estimates and reservations, never credentials or prompt content. A launch reserves one estimated unit by default and charges it on completion, including failure. Equal weights spread launches; custom budgets normalize selection by the configured available budget. Run weights/units are estimates, not exact provider tokens or a live quota query.

```bash
python3 scripts/agents/agent_account_pool.py status
python3 scripts/agents/agent_account_pool.py configure agent-a --budget 100 --used 25
python3 scripts/agents/agent_account_pool.py configure agent-b --weight 2
python3 scripts/agents/agent_account_pool.py configure agent-c --cooldown-seconds 3600
python3 scripts/agents/agent_account_pool.py configure agent-c --enabled no
python3 scripts/agents/agent_account_pool.py configure agent-c --enabled yes --cooldown-seconds 0
./scripts/agents/agy_agent.sh --account b product-manager -p "Review the assigned AC evidence"
```

The values above are examples of operator-defined local budgets, not Google plan limits. Update `--used`/`--budget` from actual usage evidence. On the real quota reset, set `--used 0`; there is no guessed automatic provider reset. `--clear-budget` removes a local budget cap. Explicit account selection still respects capacity, cooldown and budget controls.

After a provider quota error, record a cooldown or disable the pool, reconcile the interrupted task and launch a fresh attempt when eligible. There is no automatic cross-account task replay or provider error scraping. `recover` only clears reservations with both a known-dead local owner and a known-dead child; ambiguous launch crashes require operator reconciliation. This ledger is local admission accounting, not a sandbox or the full durable story scheduler.

## Roles

- [backend-engineer](backend-engineer/agent.md) — Implements cohesive backend vertical slices from approved domain contracts through infrastructure adapters and Axum endpoints. Owns correctness, explicit side effects and maintainable shared rules, while keeping implementation separate from independent approval.
- [junior-backend-engineer](junior-backend-engineer/agent.md) — Implements a bounded backend task against an approved Spec Kit plan, with explicit behavior and failure assertions. Delivers reviewable domain, schema, repository or API changes and moves to the next independent task while senior validation proceeds.
- [senior-backend-engineer](senior-backend-engineer/agent.md) — Independently validates backend candidates against their specifications and failure model. Finds and fixes scoped defects through separately assigned remediation work, while preserving independent review of every repair.
- [client-engineer](client-engineer/agent.md) — Implements client services, local data, headless hooks and platform-adaptive views from approved contracts. Maintains one owner for each datum and shares business policy across web/native consumers without making the client authoritative.
- [junior-client-engineer](junior-client-engineer/agent.md) — Implements a small client feature with complete user states and tests using the approved API and design contracts. Keeps service, hook and view responsibilities clear and submits a candidate that a senior can validate without reconstructing its intent.
- [senior-client-engineer](senior-client-engineer/agent.md) — Independently reviews client contracts, state ownership, usability and cross-platform behavior. Validates that optimistic/offline interactions recover correctly and that reuse improves changeability rather than adding redundant wrappers.
- [junior-testing-qa-engineer](junior-testing-qa-engineer/agent.md) — Authors independent requirement-based tests and reproducible evidence for a bounded story. Focuses on observable assertions, edge cases and meaningful failure detection rather than copying implementation details.
- [senior-security-qa-auditor](senior-security-qa-auditor/agent.md) — Independently audits security and test assurance across a candidate, checking both exploit boundaries and the validity of reported evidence. Combines G1/G2 expertise only when qualified and independent of the reviewed changes.
- [security-engineer](security-engineer/agent.md) — Owns the security analysis of concrete trust boundaries and provides independent G2 recommendations. Designs mitigations and regression checks for identity, authorization, untrusted inputs, keys and data lifecycle risks.
- [system-architect](system-architect/agent.md) — Owns coherent dependency boundaries and shared domain contracts across stories. Reviews architecture with build graphs, consumer compatibility and concrete change exercises, keeping abstraction proportional to real reuse and substitution needs.
- [tech-lead](tech-lead/agent.md) — Operates the continuous delivery control loop across independent juniors, seniors and later validation stages. Keeps ready work moving, preserves dependency and ownership safety, and makes stalled work visible with accountable recovery.
- [product-manager](product-manager/agent.md) — Owns the approved user problem, persona outcomes and acceptance scope through Spec Kit. Keeps requirements testable and performs evidence-based L5 product acceptance without overriding engineering or security failures.
- [ui-ux-designer](ui-ux-designer/agent.md) — Defines reusable presentation contracts and accessible interactions for the approved user journeys. Makes semantic tokens, SDUI schemas and platform states clear enough for implementation and independent usability review.
- [devops-engineer](devops-engineer/agent.md) — Builds and verifies delivery infrastructure, isolated runners and recovery workflows for approved deployment requirements. Separates untrusted candidate execution from trusted promotion and produces reproducible operational evidence.
- [release-gatekeeper](release-gatekeeper/agent.md) — Verifies that a candidate has the complete, current and independently produced evidence required for acceptance and release. Protects the integrity of the decision process instead of treating checkboxes or role prompts as authority.
- [chief-technology-officer](chief-technology-officer/agent.md) — Provides L6 technical risk review and a release recommendation against the exact accepted candidate and operational evidence. Owns cross-system tradeoffs and escalation while preserving all lower-layer validation and explicit operator authority.
- [testing-qa-engineer](testing-qa-engineer/agent.md) — Coordinates test assurance across complete user journeys and affected backend/client packages. Produces independent G1 recommendations and integrated G4 evidence, involving security specialists for G2 rather than treating every test as a penetration audit.

## Launch and validation contract

Every role must receive: **role/job title → approved job context → detailed task**. Read the constitution, spec/plan/tasks chain and Security Gateway at pinned revisions before work. Juniors hand off immutable candidates and request the next independent READY task while seniors validate. Senior fixes use a separate remediation assignment and a different non-contributing reviewer. Candidates advance through security/architecture, integration, PM and CTO with fresh evidence.

Using different accounts does not grant additional authority or prove reviewer independence. No profile name authorizes production deployment, publication, external messaging or modification of final evidence.

## Maintaining descriptions

Detailed source: [role catalog](../profiles/catalog.json). Human-readable profiles: [profile index](../profiles/README.md).

```bash
python3 scripts/agents/setup_agent_profiles.py --profiles-only
```

This refreshes role YAML, system prompts and these account/role agent definitions without modifying authentication files. The README is maintained separately. New instances created by `make_agy_agent.sh` embed their detailed role prompt and launch through the shared pool. Regenerate older instances to refresh embedded prompts and runner scripts.

See the [Spec Kit constitution](../../.specify/memory/constitution.md), [agent framework](../../docs/AGENT_PROFILES_AND_MULTI_AGENT_FRAMEWORK.md) and [role authority matrix](../../docs/COMPANY_ROLES_AND_AGENT_PROFILES.md).

## Company-wide planning and story handoffs

The pipeline starts with CTO direction, then PM specification, architect/role subplans and tech-lead master planning before approved parallel execution. All expected child results are collected, integrated and independently validated, then returned through PM to CTO final review. Planning-only tasks can produce missing draft artifacts from approved upstream direction; they cannot authorize implementation.

Every role reads and updates the same canonical `docs/validation/story-records/US-<id>.md`: action intents/results, artifacts, findings, fixes, ownership and next-role acknowledgment. Use the Spec Kit company-plan and story-record templates; separate role notes are not the authoritative handoff.
