# Company role profiles

These 17 profiles describe job responsibilities, required Spec Kit inputs, detailed execution, validation focus, handoffs, escalation and authority limits. Every role is eligible on **agent-a, agent-b and agent-c**; `auth_account: auto` delegates selection to the shared local usage/quota allocator.

## Files and source of truth

- `catalog.json`: authored role-specific descriptions and common Spec Kit, evidence, independence and pipeline requirements.
- `<role>/profile.yaml`: generated machine-readable description and eligible capabilities.
- `<role>/system_prompt.md`: generated complete job context and operating instructions, embedded by the instance launcher.
- `<role>/env.template`: existing environment template; credentials stay outside version control.

Update the catalog and regenerate with `python3 scripts/agents/setup_agent_profiles.py --profiles-only`. Role IDs, model/effort defaults, tool names and eligible path settings remain in the setup script. Preserve task-level grants and independent reviewers; YAML is not a sandbox. Refreshing descriptions does not edit account credentials.

## Profile index

| Role | Detailed operating prompt | Focus |
|:-----|:--------------------------|:------|
| backend-engineer | [System prompt](backend-engineer/system_prompt.md) | Implements cohesive backend vertical slices from approved domain contracts through infrastructure adapters and Axum endpoints. Owns correctness, explicit side effects and maintainable shared rules, while keeping implementation separate from independent approval. |
| junior-backend-engineer | [System prompt](junior-backend-engineer/system_prompt.md) | Implements a bounded backend task against an approved Spec Kit plan, with explicit behavior and failure assertions. Delivers reviewable domain, schema, repository or API changes and moves to the next independent task while senior validation proceeds. |
| senior-backend-engineer | [System prompt](senior-backend-engineer/system_prompt.md) | Independently validates backend candidates against their specifications and failure model. Finds and fixes scoped defects through separately assigned remediation work, while preserving independent review of every repair. |
| client-engineer | [System prompt](client-engineer/system_prompt.md) | Implements client services, local data, headless hooks and platform-adaptive views from approved contracts. Maintains one owner for each datum and shares business policy across web/native consumers without making the client authoritative. |
| junior-client-engineer | [System prompt](junior-client-engineer/system_prompt.md) | Implements a small client feature with complete user states and tests using the approved API and design contracts. Keeps service, hook and view responsibilities clear and submits a candidate that a senior can validate without reconstructing its intent. |
| senior-client-engineer | [System prompt](senior-client-engineer/system_prompt.md) | Independently reviews client contracts, state ownership, usability and cross-platform behavior. Validates that optimistic/offline interactions recover correctly and that reuse improves changeability rather than adding redundant wrappers. |
| junior-testing-qa-engineer | [System prompt](junior-testing-qa-engineer/system_prompt.md) | Authors independent requirement-based tests and reproducible evidence for a bounded story. Focuses on observable assertions, edge cases and meaningful failure detection rather than copying implementation details. |
| senior-security-qa-auditor | [System prompt](senior-security-qa-auditor/system_prompt.md) | Independently audits security and test assurance across a candidate, checking both exploit boundaries and the validity of reported evidence. Combines G1/G2 expertise only when qualified and independent of the reviewed changes. |
| security-engineer | [System prompt](security-engineer/system_prompt.md) | Owns the security analysis of concrete trust boundaries and provides independent G2 recommendations. Designs mitigations and regression checks for identity, authorization, untrusted inputs, keys and data lifecycle risks. |
| system-architect | [System prompt](system-architect/system_prompt.md) | Owns coherent dependency boundaries and shared domain contracts across stories. Reviews architecture with build graphs, consumer compatibility and concrete change exercises, keeping abstraction proportional to real reuse and substitution needs. |
| tech-lead | [System prompt](tech-lead/system_prompt.md) | Operates the continuous delivery control loop across independent juniors, seniors and later validation stages. Keeps ready work moving, preserves dependency and ownership safety, and makes stalled work visible with accountable recovery. |
| product-manager | [System prompt](product-manager/system_prompt.md) | Owns the approved user problem, persona outcomes and acceptance scope through Spec Kit. Keeps requirements testable and performs evidence-based L5 product acceptance without overriding engineering or security failures. |
| ui-ux-designer | [System prompt](ui-ux-designer/system_prompt.md) | Defines reusable presentation contracts and accessible interactions for the approved user journeys. Makes semantic tokens, SDUI schemas and platform states clear enough for implementation and independent usability review. |
| devops-engineer | [System prompt](devops-engineer/system_prompt.md) | Builds and verifies delivery infrastructure, isolated runners and recovery workflows for approved deployment requirements. Separates untrusted candidate execution from trusted promotion and produces reproducible operational evidence. |
| release-gatekeeper | [System prompt](release-gatekeeper/system_prompt.md) | Verifies that a candidate has the complete, current and independently produced evidence required for acceptance and release. Protects the integrity of the decision process instead of treating checkboxes or role prompts as authority. |
| chief-technology-officer | [System prompt](chief-technology-officer/system_prompt.md) | Provides L6 technical risk review and a release recommendation against the exact accepted candidate and operational evidence. Owns cross-system tradeoffs and escalation while preserving all lower-layer validation and explicit operator authority. |
| testing-qa-engineer | [System prompt](testing-qa-engineer/system_prompt.md) | Coordinates test assurance across complete user journeys and affected backend/client packages. Produces independent G1 recommendations and integrated G4 evidence, involving security specialists for G2 rather than treating every test as a penetration audit. |

See [account setup, quota commands and launch examples](../agents/README.md), the [constitution](../../.specify/memory/constitution.md) and [framework](../../docs/AGENT_PROFILES_AND_MULTI_AGENT_FRAMEWORK.md).

## Company-wide planning and story handoffs

The pipeline starts with CTO direction, then PM specification, architect/role subplans and tech-lead master planning before approved parallel execution. All expected child results are collected, integrated and independently validated, then returned through PM to CTO final review. Planning-only tasks can produce missing draft artifacts from approved upstream direction; they cannot authorize implementation.

Every role reads and updates the same canonical `docs/validation/story-records/US-<id>.md`: action intents/results, artifacts, findings, fixes, ownership and next-role acknowledgment. Use the Spec Kit company-plan and story-record templates; separate role notes are not the authoritative handoff.
