#!/usr/bin/env python3
"""
setup_agent_profiles.py - Populates the 3 Google AI Pro Account profiles (.agent_profiles/agent-[a,b,c]),
the master Agent Profiles catalog (.agents/profiles/), and native Antigravity CLI agents (.agents/agents/).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILES_DIR = REPO_ROOT / ".agents" / "profiles"
AGENTS_DIR = REPO_ROOT / ".agents" / "agents"
AGENT_PROFILES_DIR = REPO_ROOT / ".agent_profiles"

# The 3 Physical Authentication Profiles corresponding to the user's 3 Google AI Pro Accounts
AUTH_ACCOUNTS = {
    "agent-a": {
        "account_id": "a",
        "account_label": "Google AI Pro Account 1",
        "track": "Systems, Microkernel, Polyglot Schemas & Pure Axum APIs",
        "description": "Google AI Pro Account 1: Dedicated to Systems, Rust 2024 microkernel packages, DynamoDB/Moka/Redis caching, and pure Axum HTTP APIs.",
        "model": "gemini-3.8-flash-high",
        "effort": "high",
        "default_roles": ["backend-engineer", "junior-backend-engineer", "senior-backend-engineer", "system-architect", "devops-engineer"],
    },
    "agent-b": {
        "account_id": "b",
        "account_label": "Google AI Pro Account 2",
        "track": "Universal Expo SDK 58, React Native, @expo/ui & Tailwind Web",
        "description": "Google AI Pro Account 2: Dedicated to Universal Expo SDK 58 React Native mobile app, @expo/ui, Tailwind web layouts, and WatermelonDB offline sync.",
        "model": "gemini-3.8-flash-high",
        "effort": "high",
        "default_roles": ["client-engineer", "junior-client-engineer", "senior-client-engineer", "ui-ux-designer"],
    },
    "agent-c": {
        "account_id": "c",
        "account_label": "Google AI Pro Account 3",
        "track": "ASVS Security, Invariant Verification, Gates & Executive Agreement",
        "description": "Google AI Pro Account 3: Dedicated to QA test suites, OWASP ASVS v4.0.3 L2 pentesting, Quality Gates certification, PM Acceptance, and CTO Agreement.",
        "model": "gemini-3.8-flash-high",
        "effort": "high",
        "default_roles": ["testing-qa-engineer", "junior-testing-qa-engineer", "senior-security-qa-auditor", "security-engineer", "release-gatekeeper", "product-manager", "tech-lead", "chief-technology-officer"],
    },
}

COMPANY_ROLES = {
    "backend-engineer": {
        "title": "Backend & Systems Engineer",
        "description": "Systems, Microkernel & Axum API Engineer specializing in Rust 2024, zero-clone borrowing, and polyglot schemas.",
        "role": "builder",
        "seniority": "senior",
        "governing_rules": [
            "Rust Zero-Clone Law: .clone() forbidden on domain types; rely on borrowing and lifetimes",
            "Microkernel Purity: Zero cloud SDKs or direct DB drivers in crates/some-* (Gate M1)",
            "Axum Decoupling Law: Route handlers must be pure Tower services; never import lambda_http"
        ],
        "allowed_paths": ["crates/**", "backend/src/features/**", "backend/bins/**"],
        "forbidden_paths": ["apps/storefront/**", "packages/ui-components/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "junior-backend-engineer": {
        "title": "Junior Backend Engineer",
        "description": "Junior Systems Engineer implementing domain math (PR 1), database schemas (PR 2), repositories (PR 3), and Axum handlers (PR 4).",
        "role": "builder",
        "seniority": "junior",
        "governing_rules": [
            "Rust Zero-Clone Law: Strict prohibition of .clone(); use borrowing (&T, &mut T) and lifetimes ('a)",
            "Mandatory Senior Review: Cannot self-merge; must submit PR to Senior Backend Engineer for Layer 2 approval",
            "Microkernel Logic Abstraction: crates/ must remain pure logic with zero cloud vendor dependencies"
        ],
        "allowed_paths": ["crates/**", "backend/src/features/**"],
        "forbidden_paths": ["apps/storefront/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "senior-backend-engineer": {
        "title": "Senior Backend Reviewer & Systems Architect",
        "description": "Senior Backend Reviewer responsible for Layer 2 peer code reviews, Zero-Clone compliance, and Gate M1 audit.",
        "role": "reviewer",
        "seniority": "senior",
        "governing_rules": [
            "Enforce Zero-Clone invariant: reject any PR containing unauthorized .clone() calls",
            "Audit Microkernel purity: ensure no cloud SDKs or database drivers leaked into crates/",
            "Verify memory bounds, concurrency invariants, and proptest coverage before APPROVE"
        ],
        "allowed_paths": ["crates/**", "backend/**", "docs/validation/**"],
        "forbidden_paths": ["apps/storefront/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "client-engineer": {
        "title": "Client & Mobile/Web UI Engineer",
        "description": "Universal Expo SDK 58 React Native & Web UI Engineer specializing in Locality of Behavior, WatermelonDB, and @expo/ui.",
        "role": "builder",
        "seniority": "senior",
        "governing_rules": [
            "Locality of Behavior (LoB): Strict compliance with 4-tier hierarchy (features -> modules -> behaviours)",
            "Framework Scoping Law: features/ must reside exclusively under apps/storefront/src/features/",
            "Offline-First: All read and write mutations must integrate with WatermelonDB and TanStack Query v5",
            "Bilingual Accessibility: Support Arabic (ar-EG, RTL) and English (en-US, LTR) meeting WCAG 2.1 AA"
        ],
        "allowed_paths": ["apps/storefront/src/features/**", "apps/storefront/src/shared/**", "packages/**"],
        "forbidden_paths": ["crates/**", "backend/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "junior-client-engineer": {
        "title": "Junior Client Engineer",
        "description": "Junior Frontend Engineer implementing Axios/WatermelonDB sync (PR 5), domain hooks (PR 6), and UI screens (PR 7).",
        "role": "builder",
        "seniority": "junior",
        "governing_rules": [
            "Locality of Behavior: Colocate services, logic, and designs strictly within behavior subdirectories",
            "No Cross-Behaviour Sibling Imports: Promote shared logic to _shared/ before reusing across behaviours",
            "Mandatory Senior Review: Submit PR 5, 6, 7 to Senior Client Engineer for Layer 2 approval"
        ],
        "allowed_paths": ["apps/storefront/src/features/**", "packages/**"],
        "forbidden_paths": ["crates/**", "backend/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "senior-client-engineer": {
        "title": "Senior Client Reviewer & Mobile Architect",
        "description": "Senior Client Reviewer auditing frontend PRs for LoB hierarchy, offline-first sync consistency, and RTL styling.",
        "role": "reviewer",
        "seniority": "senior",
        "governing_rules": [
            "Audit Folder Architecture: Enforce Gate A2 rules and reject sibling cross-imports",
            "Audit UI & Accessibility: Ensure @expo/ui native controls, Tailwind web consistency, and RTL support",
            "Audit Offline Resilience: Ensure optimistic mutations update WatermelonDB SQLite cache properly"
        ],
        "allowed_paths": ["apps/storefront/**", "packages/**", "docs/validation/**"],
        "forbidden_paths": ["crates/**", "backend/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "testing-qa-engineer": {
        "title": "QA & Security Verification Engineer",
        "description": "QA & Security Auditor enforcing OWASP ASVS v4.0.3 L2, tenant isolation pentesting, and quality gate sign-offs.",
        "role": "auditor",
        "seniority": "senior",
        "governing_rules": [
            "Enforce Security Gateways (G2): Validate STRIDE threat matrix, multi-tenant partition keys, and KMS keys",
            "Execute automated gate validators: python3 scripts/validate_*.py must exit code 0",
            "Audit Quality Gates G0–G4 and Sprint Quality Gates SG0–SG4"
        ],
        "allowed_paths": ["docs/validation/**", "backend/tests/**", "apps/storefront/__tests__/**"],
        "forbidden_paths": ["crates/**", "backend/src/**", "apps/storefront/src/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "junior-testing-qa-engineer": {
        "title": "Junior QA Test Engineer",
        "description": "Junior QA Engineer authoring property-based tests (proptest), repository integration suites, and RNTL tests.",
        "role": "tester",
        "seniority": "junior",
        "governing_rules": [
            "Write comprehensive proptest suites verifying mathematical invariants and error bounds",
            "Author React Native Testing Library tests asserting WCAG 2.1 AA accessibility roles",
            "Submit test suites to Senior Security QA Auditor for review"
        ],
        "allowed_paths": ["backend/tests/**", "apps/storefront/__tests__/**", "docs/validation/**"],
        "forbidden_paths": ["backend/src/**", "apps/storefront/src/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "senior-security-qa-auditor": {
        "title": "Senior Security QA Auditor",
        "description": "Senior Security Lead performing fuzzing, multi-tenant breach audits, ASVS L2 verification, and Gate G2 sign-off.",
        "role": "auditor",
        "seniority": "senior",
        "governing_rules": [
            "Validate OWASP ASVS v4.0.3 Level 2 security controls across all endpoints",
            "Perform automated synthetic tenant-leak pentests across DynamoDB PK/SK boundaries",
            "Certify Gate G2 Security Audit sign-off prior to Tech Lead integration"
        ],
        "allowed_paths": ["docs/validation/**", "backend/tests/**"],
        "forbidden_paths": ["backend/src/**", "apps/storefront/src/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "product-manager": {
        "title": "Product Manager (PM)",
        "description": "Product Lead governing Spec Kit requirements, Gherkin acceptance criteria [AC-US-*], and Layer 5 acceptance sign-off.",
        "role": "pm",
        "seniority": "lead",
        "governing_rules": [
            "Validate every deliverable against explicit Gherkin Acceptance Criteria [AC-US-X.Y.Z-NN]",
            "Assert business KPIs (checkout conversion, offline availability, sub-150ms p95 latency)",
            "Grant Layer 5 Product Manager Acceptance Sign-Off only when all user story criteria pass"
        ],
        "allowed_paths": ["docs/**"],
        "forbidden_paths": ["crates/**", "backend/**", "apps/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "write_to_file", "run_command"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "tech-lead": {
        "title": "Tech Lead (TL)",
        "description": "Technical Lead orchestrating multi-agent sprint execution, load balancing, PR integration, and Gate G1/G4 sign-off.",
        "role": "lead",
        "seniority": "lead",
        "governing_rules": [
            "Coordinate Agent Profile Load Balancer assignments across junior authors and senior reviewers",
            "Ensure strict directory isolation between agents working concurrently on the same user story",
            "Certify Gate G1 (Specification Readiness) and Gate G4 (Integrated Release Sign-Off)"
        ],
        "allowed_paths": ["docs/**", "scripts/**", ".agents/**"],
        "forbidden_paths": [],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "system-architect": {
        "title": "System Architecture Engineer (SA)",
        "description": "Principal System Architect governing 10-layer architectural contracts, Gate A1, Gate A2, and Gate M1 microkernel purity.",
        "role": "architect",
        "seniority": "lead",
        "governing_rules": [
            "Audit conformance to docs/SYSTEM_ARCHITECTURE.md (Gate A1)",
            "Audit conformance to docs/FOLDER_ARCHITECTURE.md (Gate A2)",
            "Certify crates.io publishability and zero cloud-vendor coupling in crates/ (Gate M1)"
        ],
        "allowed_paths": ["docs/**", "scripts/**", "crates/**"],
        "forbidden_paths": [],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "ui-ux-designer": {
        "title": "UI/UX Design Systems Specialist",
        "description": "Design Systems Engineer governing Apple HIG, Tailwind tokens, @expo/ui styling, and bilingual accessibility.",
        "role": "designer",
        "seniority": "senior",
        "governing_rules": [
            "Enforce Design Token purity: no raw arbitrary hex colors or margins; use semantic tokens",
            "Validate RTL bidirectional mirroring for Arabic typography (IBM Plex Sans Arabic)",
            "Assert WCAG 2.1 AA 4.5:1 text contrast and minimum 44x44pt touch targets"
        ],
        "allowed_paths": ["apps/storefront/src/features/**/designs/**", "apps/storefront/src/shared/**", "packages/ui-components/**"],
        "forbidden_paths": ["crates/**", "backend/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "security-engineer": {
        "title": "Application Security Engineer",
        "description": "AppSec Specialist responsible for STRIDE threat models, KMS envelope encryption, Cognito JWT auth, and ASVS L2 audits.",
        "role": "security",
        "seniority": "senior",
        "governing_rules": [
            "Verify KMS CMK envelope encryption for sensitive fields in DynamoDB (AES-GCM-256)",
            "Assert Cognito JWT signature validation, issuer verification, and claim extraction",
            "Audit RBAC/ABAC authorization guards on every Axum route handler"
        ],
        "allowed_paths": ["docs/validation/**", "backend/tests/**"],
        "forbidden_paths": ["apps/storefront/src/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "devops-engineer": {
        "title": "DevOps & Cloud Infrastructure Engineer",
        "description": "Cloud Engineer managing Docker multi-stage builds, GitHub Actions workflows, multi-cloud decoupling, and CI automation.",
        "role": "devops",
        "seniority": "senior",
        "governing_rules": [
            "Ensure AWS Lambda packaging relies on pure Axum Tower service adaptation",
            "Maintain Docker multi-stage builds with non-root security contexts",
            "Validate GitHub Actions CI pipelines execute all Quality Gates on PRs"
        ],
        "allowed_paths": [".github/**", "docker/**", "scripts/**", "Dockerfile*", "backend/bins/**"],
        "forbidden_paths": ["crates/kernel-core/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "release-gatekeeper": {
        "title": "Release Gatekeeper",
        "description": "Release Gatekeeper certifying Quality Gates G0–G4 and Sprint Quality Gates SG0–SG4 prior to production deployment.",
        "role": "gatekeeper",
        "seniority": "lead",
        "governing_rules": [
            "Audit all 5 User Story Quality Gates (G0–G4) and verify evidence records exist",
            "Execute Sprint Quality Gates SG0 (Zero Blockers) through SG4 (CTO Authorization)",
            "Block release if any automated validator, test suite, or security gate fails"
        ],
        "allowed_paths": ["docs/validation/**", "GATES.md"],
        "forbidden_paths": ["crates/**", "backend/src/**", "apps/storefront/src/**"],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "multi_replace_file_content", "replace_file_content", "write_to_file",
            "run_command", "manage_task"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    },
    "chief-technology-officer": {
        "title": "Chief Technology Officer (CTO)",
        "description": "Executive Technical Officer providing Layer 6 Architectural Agreement and final SG4 Production Release Sign-Off.",
        "role": "cto",
        "seniority": "executive",
        "governing_rules": [
            "Verify microkernel crates.io publishability and zero cloud lock-in (Gate M1)",
            "Verify Axum transport decoupling from cloud runtimes (AWS Lambda, Azure, GCP)",
            "Verify operational SLA compliance (p95 latency < 150ms, multi-region resilience)",
            "Grant final Layer 6 Executive Agreement and authorize SG4 production deployment"
        ],
        "allowed_paths": ["docs/**", "GATES.md"],
        "forbidden_paths": [],
        "tools": [
            "send_message", "view_file", "read_url_content", "search_web",
            "write_to_file", "run_command"
        ],
        "model": "gemini-3.8-flash-high",
        "effort": "high"
    }
}


# Authentication is independent from job-title specialization.
for account_data in AUTH_ACCOUNTS.values():
    account_data["track"] = "All company roles; shared quota pool"
    account_data["default_roles"] = list(COMPANY_ROLES)
    account_data["description"] = account_data["account_label"] + ": eligible for every company role, selected by usage and quota availability."


def role_catalog():
    """Authored role details are the source for generated profiles and CLI prompts."""
    import json
    catalog = json.loads((PROFILES_DIR / "catalog.json").read_text(encoding="utf-8"))
    if set(catalog["roles"]) != set(COMPANY_ROLES):
        raise ValueError("Role catalog must cover every company role exactly once")
    return catalog


def render_role_profile(role_id, data, catalog):
    import json
    details = catalog["roles"][role_id]
    common = catalog["common"]
    # Retain model/tool/path settings, but role capabilities never select an account.
    metadata = {"name": role_id, "title": data["title"], "auth_account": "auto",
                "eligible_accounts": list(AUTH_ACCOUNTS), "role": data["role"],
                "seniority": data["seniority"], "description": details["description"],
                "model": data["model"], "effort": data["effort"],
                "responsibilities": details["responsibilities"],
                "required_inputs": details["required_inputs"],
                "validation_focus": details["validation_focus"], "handoff": details["handoff"],
                "decision_limits": details["decision_limits"],
                "planning_duties": details["planning_duties"],
                "collection_duties": details["collection_duties"],
                "governing_rules": list(common.values()),
                "allowed_paths": data["allowed_paths"], "forbidden_paths": data["forbidden_paths"],
                "tools": data["tools"]}
    # JSON scalars and arrays are valid YAML and avoid unsafe string interpolation.
    profile_yaml = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in metadata.items()) + "\n"
    # Keep role/seniority/account as plain scalars for existing shell consumers.
    for key in ("name", "role", "seniority", "auth_account", "model", "effort"):
        profile_yaml = profile_yaml.replace(f'{key}: {json.dumps(metadata[key])}\n', f'{key}: {metadata[key]}\n')
    prompt = f"""# {data['title']} (`{role_id}`)

## Role and job-title responsibilities

{details['description']}

Seniority: `{data['seniority']}`. Assignment mode: `{data['role']}`. Receive the role, job context and detailed task in that order. A profile is not a complete assignment.

""" + "\n".join(f"- {item}." for item in details["responsibilities"]) + f"""

## Required job context and Spec Kit inputs

{common['spec_kit']}

Implementation/review inputs: {details['required_inputs']}. Planning-only assignments use approved upstream direction and their bounded draft-output task as described below.

{common['launch']}

Read `.specify/memory/constitution.md` (including sections 8-11), `docs/QUALITY_GATES.md`, `docs/AGENT_PROFILES_AND_MULTI_AGENT_FRAMEWORK.md`, and `docs/COMPANY_ROLES_AND_AGENT_PROFILES.md` at approved revisions. Resolve conflicting requirements with the owner before dependent work.

## Top-down company planning and upward collection

{common['planning']}

Planning duties: {details['planning_duties']}.

Collection/return duties: {details['collection_duties']}.

Use `.specify/templates/company-plan-template.md`; preserve the master-plan revision, parent node and expected-child manifest on every assignment. No implementation before approved planning/G0 inputs.

## Canonical story record

{common['story_record']}

## Detailed task execution

1. Verify task scope, pinned inputs, incoming dependency evidence and the independent reviewer assignment.
2. Inspect existing implementations/contracts and name the canonical owner before adding code or abstractions.
3. Perform only the assigned work; cover normal, denial, boundary, failure and recovery outcomes relevant to the role.
4. Run the approved scoped checks and record actual assertions/results, including failures and limitations.
5. Reconcile the canonical story record, log outcomes/artifacts and next-role acknowledgment, then submit the immutable candidate/evidence handoff and stop writing to its released lease.

## Validation and evidence

{details['validation_focus']}.

{common['evidence']}

G0 means readiness; G1 tests/coverage; G2 security; G3 architecture/maintainability; G4 integrated acceptance. Review per-package coverage, critical invariants and useful reuse under the applicable quality policy. Never treat a successful directory scan as completed application verification.

## Continuous pipeline and remediation

{details['handoff']}.

{common['pipeline']}

{common['independence']}

Senior fixes use separate remediation tasks/leases, new candidate revisions and regression evidence. A non-contributing reviewer must validate them before progression through security/architecture, integration, PM and CTO. Do not stall the previous junior's next independent task or bypass a failed gate.

## Account selection and authority boundaries

{common['accounts']}

`auth_account: auto`; all three accounts are eligible. Authentication accounts are quota resources, not reviewer identities or permission grants. Existing authentication remains account-local.

{common['authority']}

Role-specific limit: {details['decision_limits']}.

Eligible path scope: {', '.join('`'+p+'`' for p in data['allowed_paths'])}. Task grants must narrow these paths. Explicit exclusions: {', '.join('`'+p+'`' for p in data['forbidden_paths']) or 'none additional; task and host restrictions still apply'}.

## Handoff and escalation contract

Include canonical story-record path/revision and action-event IDs, master-plan revision/parent node, assignment/attempt ID, contributor identities, spec/plan/tasks/policy revisions, candidate/base commits, changed paths, AC/TC/task mapping, check commands/environment/results, artifact digests, unresolved findings and the next required stage. Write only draft evidence; the trusted controller records final decisions.

Stop dependent work on missing/stale inputs, denied scope, lost lease, exhausted quota/budget, failed required checks or unresolved requirement changes. Report the exact blocker, owner and next action. No production release, publication, external message or destructive operation follows solely from this job title.
"""
    role_dir = PROFILES_DIR / role_id
    role_dir.mkdir(parents=True, exist_ok=True)
    (role_dir / "profile.yaml").write_text(profile_yaml, encoding="utf-8")
    (role_dir / "system_prompt.md").write_text(prompt, encoding="utf-8")
    cli_dir = AGENTS_DIR / role_id
    cli_dir.mkdir(parents=True, exist_ok=True)
    frontmatter = f"---\nname: {role_id}\ndescription: {json.dumps(details['description'])}\ntools:\n"
    frontmatter += "\n".join(f"  - {tool}" for tool in data["tools"]) + "\n---\n\n"
    (cli_dir / "agent.md").write_text(frontmatter + prompt, encoding="utf-8")


def render_account_agents():
    import json
    count = len(COMPANY_ROLES)
    for account, data in AUTH_ACCOUNTS.items():
        description = f"{data['account_label']}: shared authentication and quota resource eligible for all {count} company roles; no fixed engineering track."
        tools = COMPANY_ROLES["backend-engineer"]["tools"]
        text = f"---\nname: {account}\ndescription: {json.dumps(description)}\ntools:\n"
        text += "\n".join(f"  - {tool}" for tool in tools)
        text += f"\n---\n\n# {data['account_label']} (`{account}`)\n\n"
        text += "This account can run every company role. It is an authentication/quota pool, not a backend, client, QA or leadership specialization.\n\n"
        text += "## Role, context and detailed task\n\nBefore work, load the assigned `.agents/profiles/<role>/system_prompt.md`, then the approved job context and detailed task. Follow the top-down CTO charter → PM spec → architect/role subplans → tech-lead master plan before implementation. Collect results and integrated validation back through PM to CTO. Every action and handoff belongs in the canonical story record. Follow the Spec Kit constitution, spec/plan/tasks/Security Gateway chain and current validation gates. Without a role and approved task brief, request the missing assignment rather than inventing work.\n\n"
        text += "## Quota and continuous delivery\n\nThe launcher balances recorded usage and active reservations across agent-a, agent-b and agent-c for all roles. Respect cooldowns, disabled pools and configured local budgets. Local usage is an estimate, not a provider quota reading. Do not bypass provider limits or automatically replay a partially completed task under another account. Junior submissions, senior validation/repairs and progression to CTO follow the same pipeline regardless of account selection.\n\n"
        text += "## Approval and permission boundaries\n\nAn account change does not grant authority. Same-account reviewer names do not prove independent approval. Never approve your own repairs, alter final evidence or infer deployment permission from a CTO role. Tools and paths require an explicit scoped task grant.\n\n## Eligible roles\n\n"
        text += "\n".join(f"- `{role}`" for role in COMPANY_ROLES) + "\n"
        folder = AGENTS_DIR / account
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "agent.md").write_text(text, encoding="utf-8")


def refresh_descriptions():
    catalog = role_catalog()
    for role, data in COMPANY_ROLES.items():
        render_role_profile(role, data, catalog)
    render_account_agents()
    print(f"Refreshed {len(COMPANY_ROLES)} role profiles and 3 shared account definitions; authentication files untouched.")


def setup_all():
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    AGENT_PROFILES_DIR.mkdir(parents=True, exist_ok=True)

    print("================================================================================")
    print("STEP 1: Setting up the 3 Google AI Pro Account Profiles (Physical Auth Homes)")
    print("================================================================================")
    for account_key, data in AUTH_ACCOUNTS.items():
        # Physical HOME directory for this account
        acc_home = AGENT_PROFILES_DIR / account_key
        acc_home.mkdir(parents=True, exist_ok=True)
        (acc_home / ".gemini" / "antigravity-cli").mkdir(parents=True, exist_ok=True)
        settings_file = acc_home / ".gemini" / "antigravity-cli" / "settings.json"
        if not settings_file.exists():
            settings_file.write_text('{}\n', encoding="utf-8")

        env_file = AGENT_PROFILES_DIR / f"{account_key}.env"
        env_content = f"""# Authentication Profile for {data['account_label']}
# ==============================================================================
# To use an API key, set GEMINI_API_KEY below.
# If left empty, running './scripts/agents/agy_agent.sh {data['account_id']}' launches browser OAuth
# sign-in to authenticate {data['account_label']}.
GEMINI_API_KEY=""

MODEL="{data['model']}"
EFFORT="{data['effort']}"
ACCOUNT_ID="{data['account_id']}"
ACCOUNT_LABEL="{data['account_label']}"
TRACK="{data['track']}"
"""
        if not env_file.exists():
            env_file.write_text(env_content, encoding="utf-8")

        # Also register agent in .agents/agents/<agent-a, agent-b, agent-c> for agy CLI discovery
        agent_dir = AGENTS_DIR / account_key
        agent_dir.mkdir(parents=True, exist_ok=True)
        agent_md = f"""---
name: {account_key}
description: "{data['description']}"
tools:
  - send_message
  - view_file
  - read_url_content
  - search_web
  - multi_replace_file_content
  - replace_file_content
  - write_to_file
  - run_command
  - manage_task
---

# {data['account_label']} (`{account_key}`)

## Purpose & Focus
You are authenticated using **{data['account_label']}**.
**Domain Track**: {data['track']}

{data['description']}

## Assigned Roles under this Account
""" + "\n".join(f"- `{r}`" for r in data['default_roles']) + "\n"
        (agent_dir / "agent.md").write_text(agent_md, encoding="utf-8")
        print(f"  [OK] {account_key}: {data['account_label']} -> {acc_home}")

    print("\n================================================================================")
    print("STEP 2: Setting up Company Role Profiles & Mapping to the 3 Auth Accounts")
    print("================================================================================")
    for role_id, data in COMPANY_ROLES.items():
        role_dir = PROFILES_DIR / role_id
        role_dir.mkdir(parents=True, exist_ok=True)

        render_role_profile(role_id, data, role_catalog())

        role_env_file = AGENT_PROFILES_DIR / f"{role_id}.env"
        if not role_env_file.exists():
            role_env_file.write_text('ACCOUNT="auto"\nROLE="' + role_id + '"\n', encoding="utf-8")
        print(f"  [OK] {role_id}: eligible on all three accounts")

    render_account_agents()
    print("\nSUCCESS: Configured exactly 3 Google AI Pro Account authentication homes and mapped all roles.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles-only", action="store_true", help="Refresh role/account descriptions without touching authentication")
    args = parser.parse_args()
    if args.profiles_only:
        refresh_descriptions()
    else:
        setup_all()
