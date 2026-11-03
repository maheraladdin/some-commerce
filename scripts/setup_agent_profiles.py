#!/usr/bin/env python3
"""
setup_agent_profiles.py - Populates the 3 Google AI Pro Account profiles (.agent_profiles/agent-[a,b,c]),
the master Agent Profiles catalog (.agents/profiles/), and native Antigravity CLI agents (.agents/agents/).
"""

import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
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
        "account": "agent-a",
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
        "account": "agent-a",
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
        "account": "agent-a",
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
        "account": "agent-b",
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
        "account": "agent-b",
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
        "account": "agent-b",
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
        "account": "agent-c",
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
        "account": "agent-c",
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
        "account": "agent-c",
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
        "account": "agent-c",
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
        "account": "agent-c",
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
        "account": "agent-a",
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
        "account": "agent-b",
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
        "account": "agent-c",
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
        "account": "agent-a",
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
        "account": "agent-c",
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
        "account": "agent-c",
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
# If left empty, running './scripts/agy_agent.sh {data['account_id']}' launches browser OAuth
# sign-in to authenticate {data['account_label']}.
GEMINI_API_KEY=""

MODEL="{data['model']}"
EFFORT="{data['effort']}"
ACCOUNT_ID="{data['account_id']}"
ACCOUNT_LABEL="{data['account_label']}"
TRACK="{data['track']}"
"""
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
        mapped_acc = data["account"]
        role_dir = PROFILES_DIR / role_id
        role_dir.mkdir(parents=True, exist_ok=True)

        profile_yaml = f"""name: {role_id}
title: "{data['title']}"
auth_account: {mapped_acc}
role: {data['role']}
seniority: {data['seniority']}
description: "{data['description']}"
model: {data['model']}
effort: {data['effort']}
governing_rules:
""" + "\n".join(f"  - \"{rule}\"" for rule in data['governing_rules']) + """
allowed_paths:
""" + "\n".join(f"  - \"{p}\"" for p in data['allowed_paths']) + """
forbidden_paths:
""" + "\n".join(f"  - \"{p}\"" for p in data['forbidden_paths']) + """
tools:
""" + "\n".join(f"  - {t}" for t in data['tools']) + "\n"

        (role_dir / "profile.yaml").write_text(profile_yaml, encoding="utf-8")

        system_prompt = f"""# {data['title']} (`{role_id}`) - System Instructions

## 1. Authentication & Identity
* **Operating Account**: `{mapped_acc}` ({AUTH_ACCOUNTS[mapped_acc]['account_label']})
* **Identity**: You are the **{data['title']}** for `some-commerce`.
{data['description']}

## 2. Seniority & Validation Ladder Tier
* **Seniority Tier**: `{data['seniority']}`
* **Role Function**: `{data['role']}`

## 3. Mandatory Governing Invariants
""" + "\n".join(f"* **{rule.split(':')[0]}**: {rule.split(':')[1] if ':' in rule else rule}" for rule in data['governing_rules']) + """

## 4. Allowed Working Boundaries
* **Whitelisted Write Paths**:
""" + "\n".join(f"  - `{p}`" for p in data['allowed_paths']) + """
* **Blacklisted / Forbidden Paths**:
""" + "\n".join(f"  - `{p}`" for p in data['forbidden_paths']) + """
"""
        (role_dir / "system_prompt.md").write_text(system_prompt, encoding="utf-8")

        # Also register in .agents/agents/<role_id>/agent.md for agy CLI discovery
        cli_agent_dir = AGENTS_DIR / role_id
        cli_agent_dir.mkdir(parents=True, exist_ok=True)
        agent_md = f"""---
name: {role_id}
description: "{data['description']}"
tools:
""" + "\n".join(f"  - {t}" for t in data['tools']) + f"""
---

{system_prompt}
"""
        (cli_agent_dir / "agent.md").write_text(agent_md, encoding="utf-8")

        # In .agent_profiles/<role_id>, symlink to the appropriate account home so NO repeated sign-ins!
        role_profile_home = AGENT_PROFILES_DIR / role_id
        if role_profile_home.exists():
            if role_profile_home.is_symlink() or role_profile_home.is_dir():
                shutil.rmtree(role_profile_home) if not role_profile_home.is_symlink() else role_profile_home.unlink()
        
        # Create relative symlink to agent-a, agent-b, or agent-c
        role_profile_home.symlink_to(mapped_acc, target_is_directory=True)

        # Create env file that sources the parent account env
        role_env_file = AGENT_PROFILES_DIR / f"{role_id}.env"
        role_env_content = f"""# Inherits credentials from {mapped_acc}
source "${{REPO_ROOT}}/.agent_profiles/{mapped_acc}.env"
ROLE="{role_id}"
"""
        role_env_file.write_text(role_env_content, encoding="utf-8")
        print(f"  [OK] {role_id} -> {mapped_acc} ({AUTH_ACCOUNTS[mapped_acc]['account_label']})")

    print("\nSUCCESS: Configured exactly 3 Google AI Pro Account authentication homes and mapped all roles.")


if __name__ == "__main__":
    setup_all()
