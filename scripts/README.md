# Repository tooling

Run commands from the repository root. Tools are grouped into Python modules with their tests beside them:

```text
scripts/
├── agents/          # Profiles, instances, account allocation, sprint allocation, worktrees
├── documentation/   # Docs export, sprint-plan generation, closeout requirements
└── validation/      # Documentation and structural M1/A1/A2 validators
```

## Agents

| Entry point | Purpose |
|:------------|:--------|
| `agents/agy_agent.sh` | Launch a registered role/instance through the shared account usage allocator; `a`, `b`, `c` explicitly select sign-in accounts |
| `agents/agent_account_pool.py` | Local usage reservations, budgets, cooldowns, status and conservative dead-reservation recovery |
| `agents/setup_agent_profiles.py --profiles-only` | Refresh authored profile/account descriptions without touching authentication |
| `agents/make_agy_agent.sh` | User-facing instance creation with profile-derived role/seniority and model options |
| `agents/generate_agent.py` | Underlying Spec Kit context, task, instance and runner generation |
| `agents/agent_load_balancer.py --sprint sprint-1.1 --balance` | Produce proposed worker/story allocations; this is not a durable runtime scheduler |
| `agents/manage_agent_worktrees.sh status` | Inspect/manage worktrees; review mutating subcommands before use |

```bash
./scripts/agents/agy_agent.sh junior-backend-engineer -p "Implement the approved assigned task"
./scripts/agents/agy_agent.sh --account b product-manager -p "Review assigned acceptance evidence"
python3 scripts/agents/agent_account_pool.py status
python3 scripts/agents/setup_agent_profiles.py --profiles-only
```

All roles can use any of agent-a, agent-b and agent-c. The allocator tracks estimates, not live provider quota. See [account/role instructions](../.agents/agents/README.md). Worktree management and generator scopes do not establish a sandbox or approval authority.

Company work starts with CTO direction, PM scope, architecture/specialist subplans and a reconciled approved master plan before junior dispatch; role outputs are collected and validated back to CTO. The load-balancer output labels this cycle and remains an allocation proposal, not proof of planning approval or a durable scheduler. Each task references the [canonical story record](../docs/validation/STORY_RECORD_TEMPLATE.md). Automatic authenticated action capture/event storage is a runtime requirement, not an implemented feature of these tooling scripts.

## Documentation

| Entry point | Purpose |
|:------------|:--------|
| `documentation/bundle_docs_to_txt.py --output /tmp/some-commerce-docs.txt` | Export Markdown docs in a searchable text bundle |
| `documentation/update_sprint_plans.py` | Refresh generated multi-agent sprint plans and preserve the required final closeout gates |
| `documentation/sprint_closeout.py` | Check all 12 sprint plans have final benchmark/integration/fuzz/Loom requirements; `--write` refreshes only those footers |

Sprint closeout generation is shared by the checker and sprint-plan updater to avoid two independent templates. [The testing policy](../docs/SPRINT_TESTING.md) defines execution requirements; checking documentation does not execute application tests.

## Validation and tests

```bash
python3 scripts/validation/validate_docs.py
python3 scripts/validation/validate_microkernel.py
python3 scripts/validation/validate_system_architecture.py
python3 scripts/validation/validate_folder_architecture.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

These validators are scoped structural checks, not application/security certification. Tooling tests use temporary fixtures and fake CLI processes; they do not consume account quota or touch real sign-ins. Tests are also runnable per module, for example `python3 -m unittest discover -s scripts/agents -p 'test_*.py'`. The workflow is now at [.github/workflows/docs-validation.yml](../.github/workflows/docs-validation.yml), where GitHub can discover it; the previous copy under `scripts/ci/` was inactive.

## Removed migrations and path changes

Removed `split_user_stories.py` and `apply_speckit_to_stories.py`: the 51 stories are already split and use Spec Kit. These were completed migration writers, not ongoing validation tools; rerunning them could overwrite current narratives, gates and catalog edits using obsolete templates or Git source. Edit approved specs directly through the Spec Kit lifecycle. Historical versions remain in Git if a deliberate migration needs investigation.

Other tools were moved, not discarded: use `scripts/agents/<name>`, `scripts/documentation/<name>` or `scripts/validation/<name>` instead of the old flat paths. Documentation, CI, profile generation and generated runners reference the grouped paths. Regenerate previously exported agent instances after a path change; they may embed old absolute paths. No authentication state, credentials, worktrees or application code were removed.
