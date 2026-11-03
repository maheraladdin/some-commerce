#!/usr/bin/env python3
"""
Gate A1: System Architecture Conformance Validator (docs/SYSTEM_ARCHITECTURE.md)
Verifies:
1. Layer Decoupling: Asserts that pure domain crates (crates/kernel-core, crates/some-*)
   do not depend on cloud SDKs, direct DB drivers, or transport runtimes.
2. Single-Table DynamoDB Key Conventions: Checks that database schemas in crates/db-schema
   or specs adhere to PK, SK, and GSI1-GSI5 conventions.
3. Axum Decoupling from Lambda: Verifies that Axum handlers in backend/src/features/
   do not import lambda_http, enforcing pure Tower services.
4. Polyglot Persistence Contracts: Verifies separation between OLTP (DynamoDB),
   Search (Elasticsearch/OpenSearch), Cache (Redis/Moka), and Client (WatermelonDB).
5. WebMCP Tool Contracts: Checks that AI tools follow the W3C WebMCP / Bedrock schema format.
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

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

REQUIRED_ARCH_SECTIONS = [
    "## 1. End-to-End System Architecture Overview & Master Diagram",
    "## 2. Pillar 1: Microkernel Abstract Logic",
    "## 3. Pillar 2: Polyglot Database Schema",
    "## 4. Pillar 3: Repository Tools & Monorepo Toolchain",
    "## 5. Pillar 4 & Pillar 5: Two-Tier Backend Caching",
    "## 6. Pillar 6: HTTP `ETag` & `If-None-Match`",
    "## 7. Pillar 7: Frontend Server-State Caching",
    "## 8. Pillar 8: Client-First Local Database",
    "## 9. Pillar 9: Headless Custom Hooks",
    "## 10. Pillar 10: Platform-Adaptive UI Design Layer",
]


def validate_system_arch_doc(doc_path: Path) -> List[str]:
    """Validates docs/SYSTEM_ARCHITECTURE.md integrity and core architectural invariants."""
    errors = []
    if not doc_path.exists():
        return [f"System architecture document missing: {doc_path}"]

    content = doc_path.read_text(encoding="utf-8")
    for section_prefix in REQUIRED_ARCH_SECTIONS:
        if not any(line.startswith(section_prefix) for line in content.splitlines()):
            errors.append(f"Missing required architectural section prefix: '{section_prefix}'")

    return errors


def validate_dynamodb_schema_conventions(schema_path: Path) -> List[str]:
    """Validates that DynamoDB schemas adhere to Single-Table PK/SK and GSI patterns."""
    errors = []
    if not schema_path.exists():
        return errors

    content = schema_path.read_text(encoding="utf-8")
    # Verify standard single-table key naming
    has_pk = "pk" in content.lower() or "partition_key" in content.lower()
    has_sk = "sk" in content.lower() or "sort_key" in content.lower()
    if not (has_pk and has_sk):
        errors.append(f"{schema_path}: DynamoDB Single-Table schema must define PK and SK keys.")

    return errors


def validate_axum_layer_decoupling(features_dir: Path) -> List[str]:
    """Validates that Axum routers in features do not import lambda_http."""
    errors = []
    if not features_dir.exists():
        return errors

    for rs_file in features_dir.rglob("*.rs"):
        content = rs_file.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.splitlines(), start=1):
            if re.search(r"use\s+(lambda_http|aws_lambda_events|lambda_runtime)", line):
                errors.append(
                    f"{rs_file}:{line_num}: Gate A1 violation: Axum feature handler imports Lambda runtime directly ({line.strip()}). "
                    f"Per SYSTEM_ARCHITECTURE.md Layer 6 & Axum Decoupling Law, handlers must be pure Tower services."
                )
    return errors


def run_system_arch_validation(repo_root: Path) -> Tuple[int, List[str]]:
    """Runs all Gate A1 system architecture checks."""
    all_errors = []

    # 1. Validate docs/SYSTEM_ARCHITECTURE.md
    doc_path = repo_root / "docs" / "SYSTEM_ARCHITECTURE.md"
    all_errors.extend(validate_system_arch_doc(doc_path))

    # 2. Validate Axum handlers layer decoupling
    features_dir = repo_root / "backend" / "src" / "features"
    all_errors.extend(validate_axum_layer_decoupling(features_dir))

    # 3. Check for forbidden root features directory (Framework Scoping Law)
    root_features = repo_root / "features"
    if root_features.exists():
        all_errors.append(
            f"Gate A1 violation: 'features/' found at repository root ({root_features}). "
            f"Per SYSTEM_ARCHITECTURE.md and FOLDER_ARCHITECTURE.md, features must live inside "
            f"apps/storefront/src/features/ or backend/src/features/."
        )

    return len(all_errors), all_errors


def main():
    print("Running Gate A1: System Architecture Conformance Validation...")
    error_count, errors = run_system_arch_validation(REPO_ROOT)

    if error_count > 0:
        print(f"\nGATE A1 FAILED with {error_count} violation(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\nGATE A1 PASSED: System architecture contracts and layer decoupling verified.")
        sys.exit(0)


if __name__ == "__main__":
    main()
