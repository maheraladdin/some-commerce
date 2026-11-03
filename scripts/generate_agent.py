#!/usr/bin/env python3
"""
Agent Generator for some-commerce Multi-Agent Framework.
Generates an isolated agent workspace (workdir), configuration (agent.yaml),
tailored context file (context.md), and task checklist (tasks.md) for a given
sprint, user story, PR, and agent profile.

Supported Profiles:
- backend-engineer: Systems, Microkernel Crates, DynamoDB/Redis, and Axum APIs.
- client-engineer: Expo SDK 58, React Native, @expo/ui, Tailwind, and WatermelonDB.
- qa-security-auditor: OWASP ASVS L2, Zero-Trust Multi-Tenancy, Gate M1 & Gatekeeper.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

PROFILES = {
    "chief-technology-officer": {
        "description": "Chief Technology Officer: executive architectural agreement, multi-cloud strategy, crates.io distribution, and SG4 release authorization.",
        "default_role": "cto",
        "allowed_paths": [
            "docs/**",
            "crates/**",
            "scripts/**",
        ],
        "forbidden_paths": [],
        "rules": [
            "Executive Architectural Agreement: ensure all crates intended for crates.io are 100% pure and cloud-decoupled.",
            "Verify Gate SG4 production release readiness, operational SLA budgets, and rollback drills.",
        ],
    },
    "product-manager": {
        "description": "Product Manager: Spec Kit user stories, requirements, personas, acceptance criteria [AC-US-*], and business KPIs.",
        "default_role": "pm",
        "allowed_paths": [
            "docs/user-stories/**",
            "docs/sprints/**",
        ],
        "forbidden_paths": [
            "backend/**",
            "apps/**",
            "crates/**",
            "infra/**",
        ],
        "rules": [
            "Maintain Spec Kit integrity and map every requirement to stable [AC-US-X.Y.Z-NN] Gherkin scenarios.",
            "Verify Gate G0 readiness and Gate G4 acceptance criteria from user perspective.",
        ],
    },
    "tech-lead": {
        "description": "Tech Lead / Engineering Manager: sprint orchestration, task breakdown (7-PR standard), and code review.",
        "default_role": "lead",
        "allowed_paths": [
            "**",
        ],
        "forbidden_paths": [],
        "rules": [
            "Supervise the Agent Profile Load Balancer to guarantee zero-conflict task distribution.",
            "Enforce the 7-PR Vertical Slicing Pipeline for every user story.",
            "Ensure PR merges adhere strictly to G0–G4 and SG0–SG4 quality gates.",
        ],
    },
    "system-architect": {
        "description": "System Architecture Engineer: platform architecture, microkernel boundaries, and cloud portability.",
        "default_role": "architect",
        "allowed_paths": [
            "docs/**",
            "crates/**",
            "scripts/**",
        ],
        "forbidden_paths": [
            "apps/storefront/src/features/**",
        ],
        "rules": [
            "Enforce Gate A1 (System Architecture Conformance): verify 10-layer architectural contracts.",
            "Enforce Gate A2 (Folder Architecture Conformance): verify Framework Scoping Law and 4-tier LoB layout.",
            "Enforce Gate M1 (Microkernel Logic Abstraction): ensure pure domain crates have zero cloud SDK dependencies.",
        ],
    },
    "backend-engineer": {
        "description": "Backend & Systems Engineer: Rust 2024 microkernel crates, polyglot DB, Moka/Redis caching, and pure Axum HTTP APIs.",
        "default_role": "builder",
        "allowed_paths": [
            "crates/**",
            "backend/src/features/**",
            "backend/bins/**",
            "backend/tests/**",
        ],
        "forbidden_paths": [
            "apps/storefront/**",
            "packages/ui/**",
        ],
        "rules": [
            "Strict Rust Zero-Clone Law: never call .clone() on domain structs or payloads. Rely on borrowing (&T, &mut T), lifetimes, and zero-copy references.",
            "Permitted reference counting: Arc::clone(&handle) is allowed only for cheap pointer sharing of thread-safe infrastructure ports.",
            "Microkernel Logic Purity (Gate M1): zero cloud vendor SDKs (aws-sdk-*, azure, gcp) or direct DB drivers in pure domain crates (crates/some-*).",
            "Axum Decoupling Law: Axum feature handlers in backend/src/features/ must be pure Tower services and NEVER import lambda_http.",
        ],
    },
    "junior-backend-engineer": {
        "description": "Junior Backend Engineer: Implements domain math (PR 1), database schemas (PR 2), repositories (PR 3), and Axum handlers (PR 4).",
        "default_role": "builder",
        "allowed_paths": [
            "crates/**",
            "backend/src/features/**",
            "backend/bins/**",
        ],
        "forbidden_paths": [
            "apps/storefront/**",
        ],
        "rules": [
            "Strict Rust Zero-Clone Law: never call .clone() on domain structs or payloads. Rely on borrowing (&T, &mut T) and lifetimes.",
            "Mandatory Senior Review: cannot self-merge; must submit PRs to Senior Backend Engineer for Layer 2 approval.",
            "Microkernel Logic Purity (Gate M1): zero cloud vendor SDKs or direct DB drivers in pure domain crates.",
        ],
    },
    "senior-backend-engineer": {
        "description": "Senior Backend Reviewer & Systems Architect: Layer 2 code review, Zero-Clone enforcement, and Gate M1 audit.",
        "default_role": "reviewer",
        "allowed_paths": [
            "crates/**",
            "backend/**",
            "docs/validation/**",
        ],
        "forbidden_paths": [
            "apps/storefront/**",
        ],
        "rules": [
            "Enforce Zero-Clone invariant: reject any PR containing unauthorized .clone() calls.",
            "Audit Microkernel purity: ensure no cloud SDKs or database drivers leaked into crates/.",
            "Verify memory bounds, concurrency invariants, and proptest coverage before APPROVE.",
        ],
    },
    "client-engineer": {
        "description": "Client & Mobile Engineer: Universal Expo SDK 58 React Native, @expo/ui, Tailwind CSS, and WatermelonDB.",
        "default_role": "builder",
        "allowed_paths": [
            "apps/storefront/src/features/**",
            "apps/storefront/src/shared/**",
            "packages/api-client/**",
            "packages/watermelon-db/**",
            "packages/query-client/**",
            "apps/storefront/__tests__/**",
        ],
        "forbidden_paths": [
            "backend/**",
            "crates/**",
            "infra/**",
        ],
        "rules": [
            "Locality of Behavior (LoB): adhere strictly to the 4-tier folder hierarchy (features -> modules -> behaviours -> [services, designs, logic, types, constants]).",
            "Offline-First Invariant: all catalog, cart, and account reads must query WatermelonDB local cache first before hitting remote endpoints.",
            "Platform Adaptation: use @expo/ui for native iOS/Android controls, Tailwind CSS for web, and dynamic SDUI renderers.",
            "Accessibility & RTL: full support for Arabic (ar-EG, RTL) and English (en-US, LTR), meeting WCAG 2.1 AA standards.",
        ],
    },
    "junior-client-engineer": {
        "description": "Junior Client Engineer: Implements Axios/WatermelonDB sync (PR 5), custom hooks (PR 6), and UI designs (PR 7).",
        "default_role": "builder",
        "allowed_paths": [
            "apps/storefront/src/features/**",
            "packages/**",
        ],
        "forbidden_paths": [
            "crates/**",
            "backend/**",
        ],
        "rules": [
            "Locality of Behavior: Colocate services, logic, and designs strictly within behavior subdirectories.",
            "No Cross-Behaviour Sibling Imports: Promote shared logic to _shared/ before reusing across behaviours.",
            "Mandatory Senior Review: Submit PR 5, 6, 7 to Senior Client Engineer for Layer 2 approval.",
        ],
    },
    "senior-client-engineer": {
        "description": "Senior Client Reviewer: Audits frontend PRs for LoB hierarchy, offline-first sync consistency, and RTL styling.",
        "default_role": "reviewer",
        "allowed_paths": [
            "apps/storefront/**",
            "packages/**",
            "docs/validation/**",
        ],
        "forbidden_paths": [
            "crates/**",
            "backend/**",
        ],
        "rules": [
            "Audit Folder Architecture: Enforce Gate A2 rules and reject sibling cross-imports.",
            "Audit UI & Accessibility: Ensure @expo/ui native controls, Tailwind web consistency, and RTL support.",
            "Audit Offline Resilience: Ensure optimistic mutations update WatermelonDB SQLite cache properly.",
        ],
    },
    "ui-ux-designer": {
        "description": "UI/UX Designer & SDUI Specialist: Server-Driven UI AST schemas, visual design tokens, and RTL typography.",
        "default_role": "designer",
        "allowed_paths": [
            "apps/storefront/src/shared/tokens/**",
            "docs/SDUI_AND_LOCALIZATION.md",
            "docs/designs/**",
        ],
        "forbidden_paths": [
            "backend/**",
            "crates/**",
        ],
        "rules": [
            "Enforce WCAG 2.1 AA accessibility standards for all design tokens and color contrasts.",
            "Design bilingual layout parity for Arabic (ar-EG, RTL) and English (en-US, LTR).",
        ],
    },
    "testing-qa-engineer": {
        "description": "Testing & QA Engineer: end-to-end multi-module flows, provider sandboxes, and test coverage verification.",
        "default_role": "tester",
        "allowed_paths": [
            "tests/**",
            "backend/tests/**",
            "apps/storefront/__tests__/**",
            "docs/validation/**",
        ],
        "forbidden_paths": [
            "apps/storefront/src/**",
            "backend/src/**",
            "crates/*/src/**",
        ],
        "rules": [
            "Enforce Gate G1: verify >= 90% line and >= 85% branch coverage in affected packages.",
            "Execute realistic provider sandbox scenarios (Paymob, Stripe, Bosta, Aramex).",
        ],
    },
    "junior-testing-qa-engineer": {
        "description": "Junior QA Test Engineer: Authors property-based tests (proptest), repository integration suites, and RNTL tests.",
        "default_role": "tester",
        "allowed_paths": [
            "backend/tests/**",
            "apps/storefront/__tests__/**",
            "docs/validation/**",
        ],
        "forbidden_paths": [
            "backend/src/**",
            "apps/storefront/src/**",
        ],
        "rules": [
            "Write comprehensive proptest suites verifying mathematical invariants and error bounds.",
            "Author React Native Testing Library tests asserting WCAG 2.1 AA accessibility roles.",
            "Submit test suites to Senior Security QA Auditor for review.",
        ],
    },
    "senior-security-qa-auditor": {
        "description": "Senior Security QA Auditor: Performs fuzzing, multi-tenant breach audits, ASVS L2 verification, and Gate G2 sign-off.",
        "default_role": "auditor",
        "allowed_paths": [
            "docs/validation/**",
            "backend/tests/**",
        ],
        "forbidden_paths": [
            "backend/src/**",
            "apps/storefront/src/**",
        ],
        "rules": [
            "Validate OWASP ASVS v4.0.3 Level 2 security controls across all endpoints.",
            "Perform automated synthetic tenant-leak pentests across DynamoDB PK/SK boundaries.",
            "Certify Gate G2 Security Audit sign-off prior to Tech Lead integration.",
        ],
    },
    "security-engineer": {
        "description": "Security Engineer & Auditor: Security Gateways (G2), OWASP ASVS v4.0.3 L2, STRIDE abuse matrix, and zero-trust tenant pentest.",
        "default_role": "security-auditor",
        "allowed_paths": [
            "docs/validation/**",
            "scripts/ci/**",
            "security/**",
        ],
        "forbidden_paths": [
            "apps/storefront/src/**",
            "backend/src/**",
        ],
        "rules": [
            "Zero Critical/High Vulnerabilities: verify 0 high/critical findings in SAST and dependency audits.",
            "Zero-Trust Tenant Isolation: execute adversarial penetration tests verifying zero cross-tenant data leaks.",
            "Cryptographic Protection: verify AWS KMS envelope encryption for all sensitive payloads and zero PII logging.",
        ],
    },
    "devops-engineer": {
        "description": "DevOps & Cloud Engineer: AWS CDK v2 infrastructure, CI/CD pipelines, Docker containerization, and FTR compliance.",
        "default_role": "devops",
        "allowed_paths": [
            "infra/**",
            "scripts/ci/**",
            ".github/workflows/**",
            "Dockerfile*",
        ],
        "forbidden_paths": [
            "apps/storefront/src/features/**",
            "backend/src/features/**",
        ],
        "rules": [
            "Validate AWS CDK synth and diff cleanly with zero security misconfigurations.",
            "Ensure AWS Marketplace FTR compliance and hourly SaaS metering integration.",
        ],
    },
    "release-gatekeeper": {
        "description": "Release Gatekeeper: Quality Gates enforcement (G0–G4, SG0–SG4, Gate A1, A2, M1) and release certification.",
        "default_role": "gatekeeper",
        "allowed_paths": [
            "docs/QUALITY_GATES.md",
            "GATES.md",
            "docs/validation/**",
        ],
        "forbidden_paths": [
            "apps/storefront/src/**",
            "backend/src/**",
        ],
        "rules": [
            "Block PRs and releases failing any required gate (G0–G4, SG0–SG4, Gate M1, Gate A1, Gate A2).",
            "Validate release candidate builds and verify rollback drill evidence.",
        ],
    },
    "qa-security-auditor": {
        "description": "Combined QA & Security Auditor (Alias): OWASP ASVS L2, tenant pentest, Gate G1/G2 verification, and gatekeeper.",
        "default_role": "auditor",
        "allowed_paths": [
            "docs/validation/**",
            "scripts/ci/**",
            "backend/tests/**",
            "apps/storefront/__tests__/**",
        ],
        "forbidden_paths": [
            "apps/storefront/src/**",
            "backend/src/**",
        ],
        "rules": [
            "Zero Critical/High Vulnerabilities: every PR and story must pass SAST, dependency audits, and secret scanning with 0 critical/high findings.",
            "Zero-Trust Tenant Isolation: verify that every query, cache key, and event payload is strictly partitioned by TenantId.",
            "ASVS L2 Conformance: verify server-side authorization checks on all routes, preventing IDOR, privilege escalation, and parameter tampering.",
            "Gate Certification: enforce strict G0–G4 and SG0–SG4 sign-offs before certifying PR merge readiness.",
        ],
    },
}

PR_SPECS = {
    1: {
        "name": "Microkernel Domain Logic & Invariants",
        "layers": ["crates/kernel-core", "crates/some-*"],
        "summary": "Pure, vendor-agnostic Rust domain rules, trait ports (PaymentGatewayPlugin, ShippingCarrierPlugin), value objects (Money, Locale), and mathematical models with proptest invariants. Zero external cloud dependencies.",
    },
    2: {
        "name": "Polyglot Database Schema Definitions",
        "layers": ["crates/db-schema", "packages/watermelon-db"],
        "summary": "Strongly-typed Rust schema structs, DynamoDB Single-Table keys (PK, SK, GSI1–GSI5), OpenSearch nested property mappings, WatermelonDB SQLite schema, and ts-rs automated TypeScript codegen.",
    },
    3: {
        "name": "Repository Handlers & Caching Tier",
        "layers": ["crates/db-dynamo", "crates/cache-tier", "crates/search-elastic"],
        "summary": "DynamoDB atomic transactions (TransactWriteItems), Moka L1 in-process TinyLFU cache, Redis L2 connection multiplexer, cache eviction channels, and BLAKE3 RFC 9110 ETag generator.",
    },
    4: {
        "name": "Pure Axum Handlers, Auth Guards & WebMCP",
        "layers": ["backend/src/features/..."],
        "summary": "Axum HTTP router functions, Tower middlewares (ETag conditional 304), Cognito JWT authentication guards, WebMCP tool registration endpoints (/v1/mcp/*). Fully decoupled from lambda_http.",
    },
    5: {
        "name": "Client Services & Local Database Models",
        "layers": ["apps/storefront/src/features/.../services/", "packages/api-client"],
        "summary": "Strongly-typed Axios HTTP service with RFC 9110 ETag interceptor, WatermelonDB reactive model classes, delta pull/push sync handlers, and TanStack React Query v5 options.",
    },
    6: {
        "name": "Headless Custom Hooks & Domain Logic",
        "layers": ["apps/storefront/src/features/.../logic/"],
        "summary": "Headless React hooks encapsulating client state machines, form validation, optimistic UI updates, and offline mutation queues.",
    },
    7: {
        "name": "Platform-Adaptive UI & SDUI Renderers",
        "layers": ["apps/storefront/src/features/.../designs/"],
        "summary": "@expo/ui native iOS/Android screens, Tailwind CSS web views, dynamic SDUI component AST renderers, dual-language RTL/LTR layout, and WCAG 2.1 AA accessibility traits.",
    },
}


def find_user_story_file(story_id: str) -> Optional[Path]:
    """Finds user story markdown file by ID (e.g. 'us-1.1.1' or 'US-1.1.1')."""
    normalized = story_id.lower().strip()
    if not normalized.startswith("us-"):
        normalized = f"us-{normalized}"

    stories_dir = REPO_ROOT / "docs" / "user-stories"
    for story_file in stories_dir.rglob("us-*.md"):
        if story_file.name.lower().startswith(normalized):
            return story_file
    return None


def extract_story_details(story_file: Path) -> Dict[str, str]:
    """Extracts narrative, ACs, folder blueprint, and security gateway from story spec."""
    content = story_file.read_text(encoding="utf-8")
    
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else story_file.stem

    def extract_section(section_name: str) -> str:
        pattern = rf"##\s+\d+\.\s+{re.escape(section_name)}.*?(?=(?:\n##\s+\d+|\Z))"
        match = re.search(pattern, content, re.DOTALL)
        return match.group(0).strip() if match else ""

    return {
        "title": title,
        "spec_kit": extract_section("Spec Kit Specification"),
        "architecture": extract_section("Behavior-Centric Architecture & Folder Blueprint"),
        "plan": extract_section("Technical Implementation Plan"),
        "tasks": extract_section("Granular Implementation Tasks"),
        "security": extract_section("Security Gateway (Powered by security-audit)"),
        "gates": extract_section("Validation Gates & Acceptance Sign-Off"),
    }


def generate_agent(
    name: str,
    profile: str,
    role: Optional[str],
    sprint: str,
    story_id: str,
    pr_num: Optional[int],
    custom_workdir: Optional[str] = None,
    create_git_worktree: bool = False,
    seniority: str = "senior",
) -> Tuple[Path, Dict[str, str]]:
    """Generates an agent directory with agent.yaml, context.md, tasks.md, and workdir."""
    if profile not in PROFILES:
        raise ValueError(f"Invalid profile '{profile}'. Must be one of: {list(PROFILES.keys())}")

    story_file = find_user_story_file(story_id)
    if not story_file:
        raise FileNotFoundError(f"User story '{story_id}' not found in docs/user-stories/")

    story_data = extract_story_details(story_file)
    profile_info = PROFILES[profile]
    actual_role = role or profile_info["default_role"]

    # Determine workdir
    if custom_workdir:
        workdir = Path(custom_workdir)
    else:
        workdir = REPO_ROOT / ".agents" / "workspaces" / sprint / name

    workdir.mkdir(parents=True, exist_ok=True)

    # Determine PR details
    pr_info = PR_SPECS.get(pr_num) if pr_num in PR_SPECS else None
    pr_str = f"PR {pr_num}: {pr_info['name']}" if pr_info else "All PRs (1–7)"

    # Build agent.yaml
    agent_yaml_content = f"""name: "{name}"
profile: "{profile}"
role: "{actual_role}"
seniority: "{seniority}"
sprint: "{sprint}"
story_id: "{story_id}"
story_title: "{story_data['title']}"
pr: "{pr_num if pr_num else 'all'}"
workdir: "{workdir.relative_to(REPO_ROOT) if workdir.is_relative_to(REPO_ROOT) else workdir}"

description: "{profile_info['description']}"

allowed_paths:
"""
    for p in profile_info["allowed_paths"]:
        agent_yaml_content += f"  - \"{p}\"\n"

    agent_yaml_content += "\nforbidden_paths:\n"
    for p in profile_info["forbidden_paths"]:
        agent_yaml_content += f"  - \"{p}\"\n"

    agent_yaml_content += "\nrules:\n"
    for r in profile_info["rules"]:
        agent_yaml_content += f"  - \"{r}\"\n"

    agent_yaml_path = workdir / "agent.yaml"
    agent_yaml_path.write_text(agent_yaml_content, encoding="utf-8")

    # Build context.md
    context_md_content = f"""# Agent Context: {name}

## 1. Assignment & Role Metadata
- **Agent Name**: `{name}`
- **Core Profile**: `{profile}`
- **Specialized Role**: `{actual_role}`
- **Seniority Level**: `{seniority.upper()}`
- **Target Sprint**: `{sprint}`
- **Assigned User Story**: `{story_data['title']}` (`{story_file.stem}`)
- **Assigned PR Slice**: `{pr_str}`
- **Working Directory**: `{workdir}`

---

## 2. The 6-Layer Governance Ladder & Your Responsibility
1. **Layer 1 (Junior Author)**: Writes code in isolated workdir; runs local tests, lints, and Gate M1/A1/A2 sanity.
2. **Layer 2 (Senior Reviewer)**: Audits code against Rust Zero-Clone Law, LoB folder layout, microkernel purity, and ASVS L2. Issues formal APPROVE.
3. **Layer 3 (Security & Architect)**: Security Engineer verifies Gate G2; System Architect verifies Gate G3 (Gate A1, A2, M1).
4. **Layer 4 (Tech Lead & Gatekeeper)**: Verifies cross-story integration and Gate G1 coverage (>=90%/85%); executes PR merge.
5. **Layer 5 (Product Manager)**: Verifies 100% Gherkin ACs [AC-US-X.Y.Z-NN]; validates user outcomes & bilingual parity; issues PM Acceptance.
6. **Layer 6 (Chief Technology Officer)**: Executive architectural agreement; verifies crates.io publishability & cloud portability; grants SG4 release agreement.

---

## 3. Non-Negotiable Architectural & Code Laws
"""
    for r in profile_info["rules"]:
        context_md_content += f"- **{r.split(':')[0]}**: {':'.join(r.split(':')[1:]).strip()}\n"

    if pr_info:
        context_md_content += f"""
---

## 3. Assigned PR Scope: PR {pr_num} — {pr_info['name']}
- **Target Code Layers**: `{', '.join(pr_info['layers'])}`
- **Deliverables**: {pr_info['summary']}
- **Quality Gates Checklist**:
  - G1 Coverage: $\ge 90\%$ line and $\ge 85\%$ branch coverage.
  - Zero critical/high vulnerabilities; strict tenant isolation.
  - Passing Gate M1 microkernel purity and zero-clone checks (`python3 scripts/validate_microkernel.py`).
"""

    context_md_content += f"""
---

## 4. User Story Specification & Acceptance Criteria
{story_data['spec_kit']}

---

## 5. Behavior-Centric Architecture Blueprint
{story_data['architecture']}

---

## 6. Security Gateway Controls (Powered by security-audit)
{story_data['security']}

---

## 7. Verification & Quality Gates Commands
Run these commands locally in your worktree before requesting gate sign-off:
```bash
# 1. Microkernel purity and zero-clone borrowing check (Gate M1)
python3 scripts/validate_microkernel.py

# 2. Spec Kit documentation & Security Gateway validation
python3 scripts/validate_docs.py

# 3. Rust test suite (if operating on backend)
cargo test --workspace

# 4. Client test suite (if operating on storefront)
npm test
```
"""
    context_md_path = workdir / "context.md"
    context_md_path.write_text(context_md_content, encoding="utf-8")

    # Build tasks.md
    tasks_md_content = f"""# Execution Tasks: {name} ({pr_str})

## Phase 1: Environment & Context Setup
- [ ] Initialize workspace at `{workdir}`
- [ ] Review assigned PR scope: `{pr_str}`
- [ ] Review Gherkin Acceptance Criteria and ensure stable identifiers are mapped
- [ ] Confirm write-allowed paths: `{', '.join(profile_info['allowed_paths'])}`

## Phase 2: Implementation & Tests
"""
    if pr_num == 1:
        tasks_md_content += """- [ ] Implement pure domain rules and value objects in `crates/kernel-core` or microkernel crate
- [ ] Implement trait ports (ports-and-adapters interfaces)
- [ ] Enforce Rust Zero-Clone borrowing discipline (&T, &mut T, Cow<'a, str>)
- [ ] Write exhaustive proptest property-based unit tests
"""
    elif pr_num == 2:
        tasks_md_content += """- [ ] Define DynamoDB Single-Table schema (PK, SK, GSI keys)
- [ ] Define OpenSearch nested property mappings
- [ ] Define WatermelonDB local table definitions
- [ ] Execute `ts-rs` automated codegen to export TypeScript interfaces
"""
    elif pr_num == 3:
        tasks_md_content += """- [ ] Implement DynamoDB repository queries and `TransactWriteItems` atomic transactions
- [ ] Configure L1 Moka TinyLFU cache and L2 Redis connection multiplexer
- [ ] Implement BLAKE3 RFC 9110 ETag generation
- [ ] Write repository integration tests validating cache eviction channels
"""
    elif pr_num == 4:
        tasks_md_content += """- [ ] Implement pure Axum Router function in `backend/src/features/...`
        - [ ] Ensure ZERO imports from `lambda_http` (verify pure Tower service)
- [ ] Attach Tower ETag 304 conditional middleware
- [ ] Configure Cognito JWT authentication and RBAC/ABAC guards
- [ ] Register WebMCP tool endpoints under `/v1/mcp/*`
"""
    elif pr_num == 5:
        tasks_md_content += """- [ ] Implement strongly-typed Axios API client with ETag interceptor
- [ ] Define WatermelonDB model classes and reactive schema actions
- [ ] Implement delta synchronization handlers (`/v1/sync/pull` and `/v1/sync/push`)
- [ ] Configure TanStack React Query v5 query and mutation options
"""
    elif pr_num == 6:
        tasks_md_content += """- [ ] Implement headless React custom hooks for domain interactions
- [ ] Implement client-side form validation and state machines
- [ ] Configure optimistic UI state updates and rollback handlers
"""
    elif pr_num == 7:
        tasks_md_content += """- [ ] Build platform-adaptive UI using `@expo/ui` for native iOS and Android
- [ ] Build Tailwind CSS responsive layouts for web
- [ ] Implement dynamic SDUI AST widget decoders
- [ ] Validate RTL (`ar-EG`) and LTR (`en-US`) layouts
- [ ] Verify WCAG 2.1 AA accessibility labels and touch target sizes
"""
    else:
        tasks_md_content += """- [ ] Execute end-to-end user story implementation across affected vertical layers
- [ ] Verify non-conflicting directory placement
- [ ] Run automated unit and integration tests
"""

    tasks_md_content += """
## Phase 3: Quality Gates Verification
- [ ] Run `python3 scripts/validate_microkernel.py` (Gate M1)
- [ ] Run test suite and confirm $\ge 90\%$ line and $\ge 85\%$ branch coverage (Gate G1)
- [ ] Perform security threat review and verify zero critical/high findings (Gate G2)
- [ ] Verify framework-scoped LoB folder hierarchy compliance (Gate G3)
- [ ] Verify end-to-end acceptance in sandbox (Gate G4)
- [ ] Submit PR for review
"""
    tasks_md_path = workdir / "tasks.md"
    tasks_md_path.write_text(tasks_md_content, encoding="utf-8")

    # Native Antigravity CLI Agent registration in .agents/agents/<name>/agent.md
    agents_dir = REPO_ROOT / ".agents" / "agents" / name
    agents_dir.mkdir(parents=True, exist_ok=True)
    agent_md_path = agents_dir / "agent.md"
    tools_list = [
        "send_message", "view_file", "read_url_content", "search_web",
        "multi_replace_file_content", "replace_file_content", "write_to_file",
        "run_command", "manage_task"
    ]
    agent_md_content = f"""---
name: {name}
description: Antigravity CLI agent instance '{name}' for sprint '{sprint}', profile '{profile}', story '{story_id}'.
tools:
""" + "\n".join(f"  - {t}" for t in tools_list) + f"""
---

# Agent Instance: {name}

## Context & Assignment
- **Profile**: `{profile}` (`{seniority}` / `{actual_role}`)
- **Sprint**: `{sprint}`
- **Story**: `{story_id}`
- **Assigned PR**: `{pr_str}`
- **Workdir**: `{workdir}`

See detailed instructions and context in:
`{workdir}/context.md`
`{workdir}/tasks.md`
"""
    agent_md_path.write_text(agent_md_content, encoding="utf-8")

    # Isolated agent profile home & env in .agent_profiles/<name>/
    agent_profiles_dir = REPO_ROOT / ".agent_profiles"
    agent_home = agent_profiles_dir / name
    (agent_home / ".gemini" / "antigravity-cli").mkdir(parents=True, exist_ok=True)
    (agent_home / ".gemini" / "antigravity-cli" / "settings.json").write_text('{"modelProvider": "gemini"}\n', encoding="utf-8")
    env_path = agent_profiles_dir / f"{name}.env"
    env_content = f"""# Environment configuration for Antigravity Agent: {name}
MODEL="gemini-3.8-flash-high"
EFFORT="high"
GEMINI_API_KEY=""
SPRINT="{sprint}"
STORY="{story_id}"
PR="{pr_num if pr_num else 'all'}"
WORKDIR="{workdir}"
"""
    env_path.write_text(env_content, encoding="utf-8")

    # One-click runner script in workdir: run.sh
    run_sh_path = workdir / "run.sh"
    run_sh_content = f"""#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
REPO_ROOT="$(cd "${{SCRIPT_DIR}}/../../.." && pwd)"

NAME="$(basename "${{SCRIPT_DIR}}")"
AGENT_ENV="${{REPO_ROOT}}/.agent_profiles/${{NAME}}.env"

if [[ -f "${{AGENT_ENV}}" ]]; then
  # shellcheck disable=SC1090
  source "${{AGENT_ENV}}"
fi

export HOME="${{REPO_ROOT}}/.agent_profiles/${{NAME}}"

AGY_BIN="$(which agy 2>/dev/null || echo "/Users/maheraladdin/.local/bin/agy")"

if [[ ! -x "${{AGY_BIN}}" ]]; then
  echo "Error: Antigravity CLI binary 'agy' not found." >&2
  exit 1
fi

MODEL="${{MODEL:-gemini-3.8-flash-high}}"
EFFORT="${{EFFORT:-high}}"

ARGS=()
HAS_MODEL=false
HAS_EFFORT=false

for arg in "$@"; do
  if [[ "${{arg}}" == "--model" ]]; then HAS_MODEL=true; fi
  if [[ "${{arg}}" == "--effort" ]]; then HAS_EFFORT=true; fi
  ARGS+=("${{arg}}")
done

if [[ "${{HAS_MODEL}}" == false ]]; then
  ARGS+=(--model "${{MODEL}}")
fi

if [[ "${{HAS_EFFORT}}" == false ]]; then
  ARGS+=(--effort "${{EFFORT}}")
fi

TARGET_DIR="${{SCRIPT_DIR}}"
if [[ -d "${{SCRIPT_DIR}}/workspace" ]]; then
  TARGET_DIR="${{SCRIPT_DIR}}/workspace"
fi

cd "${{TARGET_DIR}}"
echo "Launching Antigravity CLI agent '${{NAME}}' in ${{TARGET_DIR}}..."
exec "${{AGY_BIN}}" --agent "${{NAME}}" "${{ARGS[@]}}"
"""
    run_sh_path.write_text(run_sh_content, encoding="utf-8")
    run_sh_path.chmod(0o755)

    # Optional Git Worktree creation
    if create_git_worktree:
        workspace_dir = workdir / "workspace"
        branch_name = f"agent/{sprint}/{name}"
        if not workspace_dir.exists():
            print(f"Creating git worktree at {workspace_dir} on branch {branch_name}...")
            try:
                subprocess.run(
                    ["git", "worktree", "add", "-b", branch_name, str(workspace_dir)],
                    cwd=REPO_ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                # If branch already exists, add without -b
                subprocess.run(
                    ["git", "worktree", "add", str(workspace_dir), branch_name],
                    cwd=REPO_ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                )

    return workdir, {
        "agent_yaml": str(agent_yaml_path),
        "context_md": str(context_md_path),
        "tasks_md": str(tasks_md_path),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate an isolated agent workspace, configuration, and context file."
    )
    parser.add_argument("--name", required=True, help="Unique name for the agent (e.g. s11-us111-be-builder)")
    parser.add_argument("--profile", required=True, choices=list(PROFILES.keys()), help="Agent profile")
    parser.add_argument("--role", default=None, help="Sub-role (builder, tester, auditor, gatekeeper)")
    parser.add_argument("--sprint", required=True, help="Sprint identifier (e.g. sprint-1.1)")
    parser.add_argument("--story", required=True, help="User story ID (e.g. us-1.1.1)")
    parser.add_argument("--pr", type=int, choices=range(1, 8), default=None, help="Assigned PR slice (1 to 7)")
    parser.add_argument("--seniority", choices=["junior", "mid", "senior", "lead", "executive"], default="senior", help="Seniority level")
    parser.add_argument("--workdir", default=None, help="Custom working directory path")
    parser.add_argument("--create-git-worktree", action="store_true", help="Create an isolated git worktree")

    args = parser.parse_args()

    try:
        workdir, files = generate_agent(
            name=args.name,
            profile=args.profile,
            role=args.role,
            sprint=args.sprint,
            story_id=args.story,
            pr_num=args.pr,
            custom_workdir=args.workdir,
            create_git_worktree=args.create_git_worktree,
            seniority=args.seniority,
        )
        print(f"\nSUCCESS: Agent '{args.name}' generated successfully!")
        print(f"  Working Directory: {workdir}")
        print(f"  Config:  {files['agent_yaml']}")
        print(f"  Context: {files['context_md']}")
        print(f"  Tasks:   {files['tasks_md']}")
    except Exception as e:
        print(f"\nERROR: Failed to generate agent: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
