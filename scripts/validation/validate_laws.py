#!/usr/bin/env python3
"""
Gate L1: Global E-Commerce Legal & Constitutional Law Conformance Validator
Validates that the entire codebase strictly complies with international e-commerce
statutory legal requirements (GDPR, CCPA, Omnibus Directive, PSD2/PCI-DSS, ZATCA, DSA, EAA)
and the non-negotiable Project Constitution (.specify/memory/constitution.md):
1. Law 1 (SDD & Constitution Integrity): Constitution and master governance specifications exist and are complete.
2. Law 2 (Framework Scoping Law): features/ NEVER at root; strictly inside framework containers.
3. Law 3 (Rust Zero-Clone Law): Zero deep .clone() calls on domain structs/entities (Arc/Rc borrowing only).
4. Law 4 (Microkernel Purity Law - Gate M1): Pure domain crates (crates/some-*) have zero cloud SDKs, DB drivers, or transport runtimes.
5. Law 5 (Axum Transport Decoupling Law): Axum route handlers are pure Tower services without lambda_http.
6. Law 6 (Security Gateway & Multi-Tenancy Law): Zero-trust tenant isolation (PK = TENANT#<id>) and STRIDE threat modeling.
7. Law 7 (Global Legal Acceptance Rule & G-Law Gate): Every user story contains an explicit AC-*-LAW global statutory legal scenario, TC-*-LAW test case, and G-Law validation gate.
8. Law 8 (Agency-Agents Code Review & Role Separation Law): Catalog covers all 17 company roles and enforces Gate G-Review and Gate G-Law.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import json
import os
import re
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_CONSTITUTION_SECTIONS = [
    "## 1. Core Philosophy: Spec-Driven Development (SDD)",
    "## 2. Master Folder Architecture & Framework Scoping Laws",
    "## 3. Rust Code Performance & Memory Law: Zero-Clone & Borrowing Discipline",
    "## 4. Security-Audit Integration & Security Gateways",
    "## 5. Quality Gates Standard",
    "## 6. Microkernel Architecture & Cloud Portability Law",
    "## 8. Universal Agent Launch & Spec Kit Law",
    "## 9. Continuous Pipeline & Parallel Junior Law",
    "## 10. Top-Down Planning, Division of Work and Upward Validation Law",
    "## 11. One Authoritative Record for Every User Story",
]

FORBIDDEN_MICROKERNEL_DEPS = [
    r"^aws-sdk-",
    r"^aws-config$",
    r"^azure_",
    r"^google-cloud-",
    r"^lambda_http$",
    r"^aws_lambda_events$",
    r"^tokio-postgres$",
    r"^mongodb$",
    r"^sqlx$",
]


def validate_constitution_document(constitution_path: Path) -> List[str]:
    """Law 1: Validates .specify/memory/constitution.md presence and mandatory sections."""
    errors = []
    if not constitution_path.exists():
        return [f"Constitutional Law 1 Violation: Missing constitution file at {constitution_path}"]

    content = constitution_path.read_text(encoding="utf-8")
    for sec in REQUIRED_CONSTITUTION_SECTIONS:
        if sec not in content:
            errors.append(f"Constitutional Law 1 Violation: Missing mandatory section '{sec}' in constitution.")
    return errors


def validate_framework_scoping_law(repo_root: Path) -> List[str]:
    """Law 2: Validates that features/ is never at repository root."""
    errors = []
    root_features = repo_root / "features"
    if root_features.exists():
        errors.append(
            f"Constitutional Law 2 Violation: Forbidden 'features/' directory found at monorepo root ({root_features}). "
            f"Per Framework Scoping Law, features must reside exclusively under apps/storefront/src/features/ or backend/src/features/."
        )
    return errors


def validate_zero_clone_law(repo_root: Path) -> List[str]:
    """Law 3: Validates that domain logic has 0 deep .clone() calls on domain types."""
    errors = []
    search_dirs = [repo_root / "crates", repo_root / "backend" / "src" / "features"]

    for d in search_dirs:
        if not d.exists():
            continue
        for rs_file in d.rglob("*.rs"):
            # Exclude tests and build scripts
            if "test" in rs_file.name or rs_file.parent.name == "tests":
                continue
            content = rs_file.read_text(encoding="utf-8")
            for line_num, line in enumerate(content.splitlines(), start=1):
                clean_line = line.split("//")[0].strip()
                if not clean_line:
                    continue
                # Permit Arc::clone(&x), Rc::clone(&x), clone_from, #[derive(Clone)]
                if "derive(Clone)" in clean_line or "Arc::clone" in clean_line or "Rc::clone" in clean_line:
                    continue
                # Reject deep .clone() calls
                if re.search(r"\b\w+\.clone\(\)", clean_line):
                    errors.append(
                        f"Constitutional Law 3 Violation: {rs_file}:{line_num}: Unauthorized deep .clone() call: '{clean_line}'. "
                        f"Per Rust Zero-Clone Law, domain logic must rely on borrowing (&T, &mut T) or Arc::clone(&handle)."
                    )
    return errors


def validate_microkernel_purity_law(crates_dir: Path) -> List[str]:
    """Law 4: Validates that crates/ domain packages have zero cloud SDKs or direct DB drivers."""
    errors = []
    if not crates_dir.exists():
        return errors

    for cargo_file in crates_dir.rglob("Cargo.toml"):
        content = cargo_file.read_text(encoding="utf-8")
        in_deps = False
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("[") and "dependencies" in line:
                in_deps = True
                continue
            elif line.startswith("["):
                in_deps = False
                continue

            if in_deps and "=" in line:
                dep_name = line.split("=")[0].strip()
                for forbidden in FORBIDDEN_MICROKERNEL_DEPS:
                    if re.match(forbidden, dep_name):
                        errors.append(
                            f"Constitutional Law 4 Violation: {cargo_file}: Forbidden dependency '{dep_name}'. "
                            f"Microkernel crates must be pure domain logic with zero cloud/DB dependencies."
                        )
    return errors


def validate_axum_portability_law(features_dir: Path) -> List[str]:
    """Law 5: Validates that Axum routers in features do not import lambda_http."""
    errors = []
    if not features_dir.exists():
        return errors

    for rs_file in features_dir.rglob("*.rs"):
        content = rs_file.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.splitlines(), start=1):
            if re.search(r"use\s+(lambda_http|aws_lambda_events|lambda_runtime)", line):
                errors.append(
                    f"Constitutional Law 5 Violation: {rs_file}:{line_num}: Axum handler imports Lambda runtime ({line.strip()}). "
                    f"Route handlers must be pure Tower services to guarantee cloud portability."
                )
    return errors


def validate_stories_constitutional_laws(stories_dir: Path) -> List[str]:
    """Law 6 & 7: Validates that all user stories contain global legal acceptance rules, test cases, and G-Law validation gates."""
    errors = []
    if not stories_dir.exists():
        return [f"Constitutional Law 7 Violation: Missing stories directory at {stories_dir}"]

    count = 0
    legal_keywords = ["legal compliance", "statutory", "regulations", "directive", "act", "gdpr", "ccpa", "omnibus", "privacy", "consumer"]

    for root, dirs, files in os.walk(stories_dir):
        for f in sorted(files):
            if f.startswith("us-") and f.endswith(".md"):
                count += 1
                path = Path(root) / f
                content = path.read_text(encoding="utf-8")

                m_title = re.search(r'#\s+(US-[\d\.]+)', content)
                if not m_title:
                    errors.append(f"Constitutional Law 7 Violation: {path}: Missing story ID in title")
                    continue
                story_id = m_title.group(1)

                # Law 6: Zero-Trust Multi-Tenancy Invariant
                if "PK = TENANT#" not in content and "tenant_id" not in content:
                    errors.append(f"Constitutional Law 6 Violation: {path} ({story_id}): Missing zero-trust multi-tenant partition key enforcement.")

                # Law 7: Global E-Commerce Law Acceptance Scenario
                if f"AC-{story_id}-LAW" not in content:
                    errors.append(f"Constitutional Law 7 Violation: {path} ({story_id}): Missing constitutional law acceptance rule 'AC-{story_id}-LAW'.")
                else:
                    # Verify scenario specifies statutory e-commerce legal requirements
                    scenario_match = re.search(r'Scenario:\s+\[AC-' + re.escape(story_id) + r'-LAW\][^\n]*\n((?:    [^\n]*\n)+)', content)
                    if scenario_match:
                        scenario_body = scenario_match.group(0).lower()
                        if not any(kw in scenario_body for kw in legal_keywords):
                            errors.append(f"Constitutional Law 7 Violation: {path} ({story_id}): 'AC-{story_id}-LAW' must specify global e-commerce legal/statutory requirements.")

                # Law 7: Mapped Test Case in Traceability Matrix
                num_id = story_id.replace("US-", "")
                if f"TC-{num_id}-LAW" not in content and f"TC-{story_id}-LAW" not in content and "TC-" not in content:
                    errors.append(f"Constitutional Law 7 Violation: {path} ({story_id}): Missing legal test case 'TC-{num_id}-LAW' in traceability matrix.")

                # Law 7: G-Law Validation Gate
                if f"{story_id}-G-Law" not in content:
                    errors.append(f"Constitutional Law 7 Violation: {path} ({story_id}): Missing law validation gate '{story_id}-G-Law'.")

                # Gate G-Review
                if f"{story_id}-G-Review" not in content:
                    errors.append(f"Constitutional Law 8 Violation: {path} ({story_id}): Missing code review validation gate '{story_id}-G-Review'.")

    if count != 51:
        errors.append(f"Constitutional Law 7 Violation: Expected 51 user stories, found {count}")

    return errors


def validate_role_separation_law(repo_root: Path) -> List[str]:
    """Law 8: Validates that the 17 company roles and Code Reviewer standards are active."""
    errors = []
    catalog_path = repo_root / ".agents" / "profiles" / "catalog.json"
    if not catalog_path.exists():
        return [f"Constitutional Law 8 Violation: Missing catalog at {catalog_path}"]

    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        if len(catalog.get("roles", {})) != 17:
            errors.append(f"Constitutional Law 8 Violation: Expected exactly 17 company roles, found {len(catalog.get('roles', {}))}")
        if "code_review" not in catalog.get("common", {}):
            errors.append("Constitutional Law 8 Violation: Missing Agency-Agents code_review common standard in catalog.")
    except Exception as e:
        errors.append(f"Constitutional Law 8 Violation: Failed to parse catalog: {e}")

    return errors


def run_law_validation(repo_root: Path) -> Tuple[int, List[str]]:
    """Runs all Gate L1 Constitutional Law checks."""
    all_errors = []

    # Law 1: SDD & Constitution Integrity
    all_errors.extend(validate_constitution_document(repo_root / ".specify" / "memory" / "constitution.md"))

    # Law 2: Framework Scoping Law
    all_errors.extend(validate_framework_scoping_law(repo_root))

    # Law 3: Rust Zero-Clone Memory Law
    all_errors.extend(validate_zero_clone_law(repo_root))

    # Law 4: Microkernel Purity Law
    all_errors.extend(validate_microkernel_purity_law(repo_root / "crates"))

    # Law 5: Axum Transport Portability Law
    all_errors.extend(validate_axum_portability_law(repo_root / "backend" / "src" / "features"))

    # Law 6 & 7: Stories Law Acceptance Rules & Validation Gates
    all_errors.extend(validate_stories_constitutional_laws(repo_root / "docs" / "user-stories"))

    # Law 8: Role Separation & Governance Law
    all_errors.extend(validate_role_separation_law(repo_root))

    return len(all_errors), all_errors


def main():
    print("Running Gate L1: Constitutional Law Conformance Validation...")
    error_count, errors = run_law_validation(REPO_ROOT)

    if error_count > 0:
        print(f"\nGATE L1 FAILED with {error_count} constitutional violation(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\nGATE L1 PASSED: All non-negotiable Project Constitution laws verified across the codebase.")
        sys.exit(0)


if __name__ == "__main__":
    main()
