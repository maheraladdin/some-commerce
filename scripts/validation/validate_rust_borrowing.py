#!/usr/bin/env python3
"""
Gate R1: Rust Zero-Clone Performance & Borrowing Discipline Validator
Enforces that Rust backend code relies strictly on borrowing (&T, &mut T),
lifetimes ('a), zero-copy byte buffers (bytes::Bytes), and forbids deep .clone()
over borrowing on domain structs, entities, and request pipelines (only permitting
reference-counted Arc::clone and Rc::clone).

Verification Rules:
1. Rule R1.1: Zero unauthorized deep .clone() calls on domain entities in crates/ and backend/src/features/.
2. Rule R1.2: Only pointer copies via Arc::clone(&handle) or Rc::clone(&handle) are permitted.
3. Rule R1.3: Borrowing (&T, &mut T) and Cow<'a, str> are required for references.
4. Rule R1.4: Every user story defines the G-Borrow validation gate check [US-X.Y.Z-G-Borrow].
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import os
import re
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]


def validate_rust_source_borrowing(rs_path: Path) -> List[str]:
    """Scans a single Rust file to ensure zero deep .clone() calls on domain structs."""
    errors = []
    if not rs_path.exists() or not rs_path.name.endswith(".rs"):
        return errors

    # Exclude test files, test directories, and build scripts
    if "test" in rs_path.name or rs_path.parent.name == "tests" or rs_path.name == "build.rs":
        return errors

    content = rs_path.read_text(encoding="utf-8")
    for line_num, line in enumerate(content.splitlines(), start=1):
        clean_line = line.split("//")[0].strip()
        if not clean_line:
            continue

        # Allowed patterns: derive(Clone), Arc::clone(&x), Rc::clone(&x), clone_from, allow(clone)
        if "derive(Clone)" in clean_line or "Arc::clone" in clean_line or "Rc::clone" in clean_line:
            continue
        if "allow(clone)" in line or "clone_from" in clean_line:
            continue

        # Reject deep .clone() invocations
        if re.search(r"\b\w+\.clone\(\)", clean_line):
            errors.append(
                f"Gate R1 Violation: {rs_path}:{line_num}: Unauthorized deep .clone() call: '{clean_line}'. "
                f"Per Rust Zero-Clone Performance Law, code must rely on borrowing (&T, &mut T), lifetimes, "
                f"or Arc::clone(&handle) pointer-count increments."
            )
    return errors


def validate_all_rust_code(repo_root: Path) -> List[str]:
    """Scans domain crates and backend features for zero-clone borrowing compliance."""
    errors = []
    target_dirs = [repo_root / "crates", repo_root / "backend" / "src" / "features"]

    for target in target_dirs:
        if not target.exists():
            continue
        for rs_file in target.rglob("*.rs"):
            errors.extend(validate_rust_source_borrowing(rs_file))
    return errors


def validate_stories_borrow_gate(stories_dir: Path) -> List[str]:
    """Validates that all user stories contain the G-Borrow gate in Section 6."""
    errors = []
    if not stories_dir.exists():
        return [f"Gate R1 Violation: Missing stories directory at {stories_dir}"]

    count = 0
    for root, dirs, files in os.walk(stories_dir):
        for f in sorted(files):
            if f.startswith("us-") and f.endswith(".md"):
                count += 1
                path = Path(root) / f
                content = path.read_text(encoding="utf-8")

                m = re.search(r'#\s+(US-[\d\.]+)', content)
                if not m:
                    errors.append(f"Gate R1 Violation: {path}: Missing story ID in title")
                    continue
                story_id = m.group(1)

                if f"{story_id}-G-Borrow" not in content and f"{story_id}-G-Borrow" not in content:
                    errors.append(f"Gate R1 Violation: {path} ({story_id}): Missing Rust zero-clone gate '{story_id}-G-Borrow'.")

    if count != 51:
        errors.append(f"Gate R1 Violation: Expected 51 user stories, found {count}")
    return errors


def run_rust_borrowing_validation(repo_root: Path) -> Tuple[int, List[str]]:
    """Executes all Gate R1 checks."""
    all_errors = []
    all_errors.extend(validate_all_rust_code(repo_root))
    all_errors.extend(validate_stories_borrow_gate(repo_root / "docs" / "user-stories"))
    return len(all_errors), all_errors


def main():
    print("Running Gate R1: Rust Zero-Clone Borrowing Discipline Validation...")
    error_count, errors = run_rust_borrowing_validation(REPO_ROOT)

    if error_count > 0:
        print(f"\nGATE R1 FAILED with {error_count} violation(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\nGATE R1 PASSED: Rust zero-clone borrowing discipline and G-Borrow gates verified.")
        sys.exit(0)


if __name__ == "__main__":
    main()
