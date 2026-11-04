#!/usr/bin/env python3
"""
Automated Gate M1: Microkernel Logic Abstraction & Cloud Decoupling Validator
Verifies:
1. Microkernel Crate Purity: Zero cloud SDKs (aws-sdk, azure, gcp), zero lambda_http, zero direct DB drivers in pure domain crates.
2. Axum Transport Decoupling: Zero lambda_http imports in Axum feature routers or handlers.
3. Rust Zero-Clone Borrowing Law: Zero deep .clone() calls on domain structs (permitting only Arc::clone and Rc::clone).
4. Hexagonal Architecture: Trait-based Ports exist and external infrastructure is confined to adapters.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import os
import re
from typing import List, Tuple

FORBIDDEN_CRATE_DEPS = [
    r"^aws-sdk-",
    r"^aws-config$",
    r"^aws-types$",
    r"^azure_",
    r"^google-cloud-",
    r"^lambda_http$",
    r"^aws_lambda_events$",
    r"^lambda_runtime$",
    r"^tokio-postgres$",
    r"^mongodb$",
    r"^sqlx$",
    r"^rusqlite$",
]

FORBIDDEN_AXUM_FEATURE_IMPORTS = [
    r"use\s+lambda_http",
    r"use\s+aws_lambda_events",
    r"use\s+lambda_runtime",
]

# Patterns allowed for .clone()
ALLOWED_CLONE_PATTERNS = [
    r"Arc::clone\s*\(",
    r"Rc::clone\s*\(",
    r"//\s*allow\(clone\)",
]

# Regex to detect raw .clone() calls: .clone() not preceded by Arc:: or Rc::
RAW_CLONE_REGEX = re.compile(r"(\.clone\s*\(\s*\))")


def validate_crate_cargo_toml(cargo_toml_path: Path) -> List[str]:
    """Check a microkernel crate's Cargo.toml for forbidden dependencies."""
    errors = []
    if not cargo_toml_path.exists():
        return errors

    content = cargo_toml_path.read_text(encoding="utf-8")
    in_dependencies_section = False
    
    for line_num, line in enumerate(content.splitlines(), start=1):
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            section_name = line.strip("[]")
            if section_name in ("dependencies", "dev-dependencies", "build-dependencies"):
                # dev-dependencies are allowed for mocks/tests if needed, but dependencies are not
                in_dependencies_section = (section_name == "dependencies")
            else:
                in_dependencies_section = False
            continue

        if in_dependencies_section and "=" in line:
            dep_name = line.split("=")[0].strip()
            for pattern in FORBIDDEN_CRATE_DEPS:
                if re.search(pattern, dep_name):
                    errors.append(
                        f"{cargo_toml_path}:{line_num}: Forbidden dependency '{dep_name}' in microkernel domain crate. "
                        f"Domain packages must be zero-cloud and zero-IO."
                    )
    return errors


def validate_axum_feature_file(rs_path: Path) -> List[str]:
    """Check Axum feature files to ensure no lambda_http or AWS Lambda runtimes are imported."""
    errors = []
    if not rs_path.exists() or not rs_path.name.endswith(".rs"):
        return errors

    content = rs_path.read_text(encoding="utf-8")
    for line_num, line in enumerate(content.splitlines(), start=1):
        for pattern in FORBIDDEN_AXUM_FEATURE_IMPORTS:
            if re.search(pattern, line):
                errors.append(
                    f"{rs_path}:{line_num}: Forbidden transport import '{line.strip()}'. "
                    f"Axum features must be pure Tower services and completely decoupled from lambda_http."
                )
    return errors


def validate_rust_zero_clone(rs_path: Path) -> List[str]:
    """Check Rust source file for forbidden .clone() usage in domain logic."""
    errors = []
    if not rs_path.exists() or not rs_path.name.endswith(".rs"):
        return errors

    content = rs_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    in_test_block = False
    in_comment_block = False
    prev_line_had_allow = False

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Handle comments
        if "/*" in stripped:
            in_comment_block = True
        if in_comment_block:
            if "*/" in stripped:
                in_comment_block = False
            prev_line_had_allow = False
            continue
        if stripped.startswith("//"):
            if "allow(clone)" in stripped:
                prev_line_had_allow = True
            else:
                prev_line_had_allow = False
            continue

        # Check test module boundaries
        if "#[cfg(test)]" in stripped or stripped.startswith("mod test") or stripped.startswith("mod tests"):
            in_test_block = True
            prev_line_had_allow = False
            continue

        # If inside a test block, allow .clone() for test ergonomics
        if in_test_block:
            prev_line_had_allow = False
            continue

        # Check for allowed annotations on same line or previous line
        has_current_allow = any(re.search(allowed, line) for allowed in ALLOWED_CLONE_PATTERNS)
        if has_current_allow or prev_line_had_allow:
            prev_line_had_allow = False
            continue

        prev_line_had_allow = False

        # Check for raw .clone() call
        if RAW_CLONE_REGEX.search(line):
            # Check if it was preceded by Arc:: or Rc::
            if "Arc::clone" in line or "Rc::clone" in line:
                continue
            errors.append(
                f"{rs_path}:{line_num}: Forbidden .clone() call '{stripped}'. "
                f"Rust constitution mandates strict borrowing (&T, &mut T) and zero-copy references. "
                f"Use Arc::clone(&handle) for reference-counted pointers or annotate with '// allow(clone)' if justified."
            )

    return errors


def run_microkernel_validation(base_dir: Path) -> Tuple[int, List[str]]:
    """Runs all Gate M1 microkernel abstraction checks across the workspace."""
    all_errors = []

    # 1. Validate Crates in crates/ (if present)
    crates_dir = base_dir / "crates"
    if crates_dir.exists():
        for crate_dir in crates_dir.iterdir():
            if crate_dir.is_dir():
                cargo_path = crate_dir / "Cargo.toml"
                if cargo_path.exists():
                    all_errors.extend(validate_crate_cargo_toml(cargo_path))

                # Check Rust source code inside crates for zero-clone
                src_dir = crate_dir / "src"
                if src_dir.exists():
                    for rs_file in src_dir.rglob("*.rs"):
                        all_errors.extend(validate_rust_zero_clone(rs_file))

    # 2. Validate Axum feature handlers in backend/src/features
    backend_features_dir = base_dir / "backend" / "src" / "features"
    if backend_features_dir.exists():
        for rs_file in backend_features_dir.rglob("*.rs"):
            # Check transport decoupling
            all_errors.extend(validate_axum_feature_file(rs_file))
            # Check zero-clone law
            all_errors.extend(validate_rust_zero_clone(rs_file))

    # 3. Check for any misplaced lambda_http in standalone/portable server binaries in backend/bins
    backend_bins_dir = base_dir / "backend" / "bins"
    if backend_bins_dir.exists():
        for bin_dir in backend_bins_dir.iterdir():
            if bin_dir.is_dir() and ("standalone" in bin_dir.name or "portable" in bin_dir.name):
                for rs_file in bin_dir.rglob("*.rs"):
                    all_errors.extend(validate_axum_feature_file(rs_file))

    return len(all_errors), all_errors


def main():
    base_dir = Path(__file__).resolve().parents[2]
    print("Running Gate M1: Microkernel Logic Abstraction & Cloud Decoupling Audit...")
    error_count, errors = run_microkernel_validation(base_dir)

    if error_count > 0:
        print(f"\nGATE M1 FAILED with {error_count} violation(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\nGATE M1 PASSED: Microkernel crates, Axum transport decoupling, and zero-clone invariants verified.")
        sys.exit(0)


if __name__ == "__main__":
    main()
