#!/usr/bin/env python3
"""
Gate A2: Folder Architecture & Locality of Behavior Conformance Validator (docs/FOLDER_ARCHITECTURE.md)
Verifies:
1. Framework Scoping Law: features/ MUST NOT exist at monorepo root. Must be inside apps/storefront/src/ or backend/src/.
2. 4-Tier Hierarchical Structure: features/<feature>/modules/<module>/behaviours/<behaviour>/[services, designs, logic, types, constants].
3. Shared Folder Naming: Feature-level and module-level shared tiers must use '_shared', while framework root uses 'shared'.
4. Client vs Backend Tier Separation: 'designs/' is permitted strictly in client apps, forbidden in backend services.
5. No Cross-Behaviour Sibling Imports: Behaviours must not import from sibling behaviours directly; shared items must be promoted.
6. Documentation Conformance: docs/FOLDER_ARCHITECTURE.md must exist and contain required layout blueprints.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import os
import re
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]

ALLOWED_CLIENT_BEHAVIOUR_DIRS = {"services", "designs", "logic", "types", "constants"}
ALLOWED_BACKEND_BEHAVIOUR_DIRS = {"services", "logic", "types", "constants"}

REQUIRED_FOLDER_DOC_SECTIONS = [
    "## 1. Architectural Philosophy: Locality of Behavior (LoB) Inside Frameworks",
    "## 2. Monorepo Structural Layout",
    "## 3. The 4 Sharing & Promotion Tiers Inside Each Framework",
    "## 4. Framework Anatomy: Frontend vs Backend Colocation",
    "## 5. Master Feature & Module Taxonomy",
]


def validate_folder_arch_doc(doc_path: Path) -> List[str]:
    """Validates docs/FOLDER_ARCHITECTURE.md integrity."""
    errors = []
    if not doc_path.exists():
        return [f"Folder architecture document missing: {doc_path}"]

    content = doc_path.read_text(encoding="utf-8")
    for section_prefix in REQUIRED_FOLDER_DOC_SECTIONS:
        if not any(line.startswith(section_prefix) for line in content.splitlines()):
            errors.append(f"Missing required section in FOLDER_ARCHITECTURE.md: '{section_prefix}'")

    return errors


def validate_framework_scoping(repo_root: Path) -> List[str]:
    """Verifies that features/ does NOT exist at the repository root."""
    errors = []
    root_features = repo_root / "features"
    if root_features.exists():
        errors.append(
            f"Gate A2 violation: 'features/' directory found at repository root ({root_features}). "
            f"Per Framework Scoping Law, features/ must only live inside apps/storefront/src/features/ or backend/src/features/."
        )

    root_shared = repo_root / "shared"
    if root_shared.exists():
        errors.append(
            f"Gate A2 violation: 'shared/' directory found at repository root ({root_shared}). "
            f"Shared folders must be framework-scoped (apps/storefront/src/shared/ or backend/src/shared/)."
        )

    return errors


def validate_behaviour_directory_structure(features_root: Path, is_client: bool) -> List[str]:
    """Validates that a features/ tree adheres to the 4-tier LoB standard."""
    errors = []
    if not features_root.exists():
        return errors

    allowed_behaviour_subdirs = ALLOWED_CLIENT_BEHAVIOUR_DIRS if is_client else ALLOWED_BACKEND_BEHAVIOUR_DIRS
    framework_name = "Client" if is_client else "Backend"

    for feature_dir in features_root.iterdir():
        if not feature_dir.is_dir() or feature_dir.name.startswith("."):
            continue

        # If it's a feature directory, allowed children are '_shared' and 'modules'
        for child in feature_dir.iterdir():
            if not child.is_dir() or child.name.startswith("."):
                continue
            if child.name not in ("_shared", "modules"):
                errors.append(
                    f"{framework_name} Feature '{feature_dir.name}' contains invalid directory '{child.name}'. "
                    f"Expected only '_shared' or 'modules'."
                )

        modules_dir = feature_dir / "modules"
        if not modules_dir.exists():
            continue

        for module_dir in modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith("."):
                continue

            for child in module_dir.iterdir():
                if not child.is_dir() or child.name.startswith("."):
                    continue
                if child.name not in ("_shared", "behaviours"):
                    errors.append(
                        f"{framework_name} Module '{module_dir.name}' contains invalid directory '{child.name}'. "
                        f"Expected only '_shared' or 'behaviours'."
                    )

            behaviours_dir = module_dir / "behaviours"
            if not behaviours_dir.exists():
                continue

            for behaviour_dir in behaviours_dir.iterdir():
                if not behaviour_dir.is_dir() or behaviour_dir.name.startswith("."):
                    continue

                for sub in behaviour_dir.iterdir():
                    if not sub.is_dir() or sub.name.startswith("."):
                        continue
                    if sub.name not in allowed_behaviour_subdirs:
                        if not is_client and sub.name == "designs":
                            errors.append(
                                f"Backend Behaviour '{behaviour_dir.name}' contains 'designs/'. "
                                f"'designs/' is forbidden on backend; UI belongs in client."
                            )
                        else:
                            errors.append(
                                f"{framework_name} Behaviour '{behaviour_dir.name}' contains unapproved folder '{sub.name}'. "
                                f"Allowed folders: {sorted(list(allowed_behaviour_subdirs))}."
                            )

    return errors


def validate_no_sibling_cross_imports(features_root: Path) -> List[str]:
    """Validates that behaviours do not import directly from sibling behaviours."""
    errors = []
    if not features_root.exists():
        return errors

    # Regex detecting traversal up to sibling behaviour: e.g. ../../sibling/ or ../../../other-behaviour/
    # Intra-behaviour imports (e.g. ../services/ or ../constants/ within the same behaviour) are allowed.
    # Traversal to module or feature _shared/ (e.g. ../../_shared/) is allowed.
    sibling_import_regex = re.compile(
        r"""(?:from\s+['"]|import\s+['"]|require\s*\(\s*['"])[.]{2}/[.]{2}/(?:\.\./)*(?!_shared/)[a-zA-Z0-9_-]+"""
    )
    rust_sibling_regex = re.compile(r"""use\s+super::super::(?!_shared)[a-zA-Z0-9_]+""")

    for ext in ("*.ts", "*.tsx", "*.rs", "*.js", "*.jsx"):
        for source_file in features_root.rglob(ext):
            parts = source_file.parts
            if "behaviours" in parts:
                content = source_file.read_text(encoding="utf-8", errors="ignore")
                for line_num, line in enumerate(content.splitlines(), start=1):
                    line_clean = line.strip()
                    if line_clean.startswith("//") or line_clean.startswith("/*") or line_clean.startswith("*"):
                        continue
                    if sibling_import_regex.search(line_clean) or rust_sibling_regex.search(line_clean):
                        errors.append(
                            f"{source_file}:{line_num}: Gate A2 violation: direct sibling behaviour import detected: '{line_clean}'. "
                            f"Cross-behaviour dependencies must be promoted to module '_shared/' or feature '_shared/'."
                        )

    return errors


def run_folder_arch_validation(repo_root: Path) -> Tuple[int, List[str]]:
    """Runs all Gate A2 folder architecture checks across the workspace."""
    all_errors = []

    # 1. Validate docs/FOLDER_ARCHITECTURE.md
    doc_path = repo_root / "docs" / "FOLDER_ARCHITECTURE.md"
    all_errors.extend(validate_folder_arch_doc(doc_path))

    # 2. Validate Framework Scoping Law
    all_errors.extend(validate_framework_scoping(repo_root))

    # 3. Validate Client Features hierarchy (if directory exists)
    client_features = repo_root / "apps" / "storefront" / "src" / "features"
    all_errors.extend(validate_behaviour_directory_structure(client_features, is_client=True))
    all_errors.extend(validate_no_sibling_cross_imports(client_features))

    # 4. Validate Backend Features hierarchy (if directory exists)
    backend_features = repo_root / "backend" / "src" / "features"
    all_errors.extend(validate_behaviour_directory_structure(backend_features, is_client=False))
    all_errors.extend(validate_no_sibling_cross_imports(backend_features))

    return len(all_errors), all_errors


def main():
    print("Running Gate A2: Folder Architecture & Locality of Behavior Conformance Validation...")
    error_count, errors = run_folder_arch_validation(REPO_ROOT)

    if error_count > 0:
        print(f"\nGATE A2 FAILED with {error_count} violation(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\nGATE A2 PASSED: Framework scoping, 4-tier LoB hierarchy, and colocation rules verified.")
        sys.exit(0)


if __name__ == "__main__":
    main()
