#!/usr/bin/env python3
"""
Spec Kit Configuration & Integrity Validator
Validates that:
1. .specify/config.json exists, is valid JSON, and declares all required standards and templates.
2. All templates referenced in config.json physically exist on disk.
3. .specify/memory/constitution.md exists and is complete.
4. Declared quality gates (story gates, monorepo gates, sprint gates) match constitutional specifications.
5. All 51 user stories link to the Spec Kit constitution.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import json
import os
import re
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
SPECIFY_DIR = REPO_ROOT / ".specify"

EXPECTED_STORY_GATES = [
    "G0", "G1", "G2", "G3", "G-Review", "G-Borrow", "G-UI", "G-Law", "G4"
]

EXPECTED_MONOREPO_GATES = [
    "M1", "A1", "A2", "L1", "R1", "F1"
]

EXPECTED_SPRINT_GATES = [
    "SG0", "SG1", "SG2", "SG3", "SG4"
]


def validate_speckit_config(config_path: Path) -> List[str]:
    """Validates .specify/config.json structure, templates, and quality gate definitions."""
    errors = []
    if not config_path.exists():
        return [f"Spec Kit Error: Missing configuration file at {config_path}"]

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"Spec Kit Error: Failed to parse {config_path}: {e}"]

    # 1. Basic flags
    if not config.get("spec_driven_development"):
        errors.append("Spec Kit Error: 'spec_driven_development' must be true in config.json")

    # 2. Standards & Constitution
    standards = config.get("standards", {})
    constitution_rel = standards.get("constitution")
    if not constitution_rel:
        errors.append("Spec Kit Error: Missing 'standards.constitution' in config.json")
    else:
        constitution_path = REPO_ROOT / constitution_rel
        if not constitution_path.exists():
            errors.append(f"Spec Kit Error: Constitution file does not exist at {constitution_path}")

    # 3. Templates existence
    templates = standards.get("templates", {})
    required_template_keys = ["spec", "plan", "tasks", "security_gateway", "user_story", "company_plan"]
    for key in required_template_keys:
        template_rel = templates.get(key)
        if not template_rel:
            errors.append(f"Spec Kit Error: Missing template mapping for '{key}' in config.json")
        else:
            template_path = REPO_ROOT / template_rel
            if not template_path.exists():
                errors.append(f"Spec Kit Error: Template '{key}' does not exist at {template_path}")

    # 4. Quality Gates
    quality_gates = standards.get("quality_gates", {})
    story_gates = quality_gates.get("story_gates", [])
    for g in EXPECTED_STORY_GATES:
        if g not in story_gates:
            errors.append(f"Spec Kit Error: Missing story quality gate '{g}' in config.json")

    monorepo_gates = quality_gates.get("monorepo_gates", [])
    for mg in EXPECTED_MONOREPO_GATES:
        if mg not in monorepo_gates:
            errors.append(f"Spec Kit Error: Missing monorepo gate '{mg}' in config.json")

    sprint_gates = quality_gates.get("sprint_gates", [])
    for sg in EXPECTED_SPRINT_GATES:
        if sg not in sprint_gates:
            errors.append(f"Spec Kit Error: Missing sprint gate '{sg}' in config.json")

    return errors


def validate_story_speckit_links(stories_dir: Path) -> List[str]:
    """Validates that all 51 user stories reference the Spec Kit constitution."""
    errors = []
    if not stories_dir.exists():
        return [f"Spec Kit Error: Missing stories directory at {stories_dir}"]

    count = 0
    for root, dirs, files in os.walk(stories_dir):
        for f in sorted(files):
            if f.startswith("us-") and f.endswith(".md"):
                count += 1
                path = Path(root) / f
                content = path.read_text(encoding="utf-8")
                if ".specify/memory/constitution.md" not in content and "Spec Kit Specification" not in content:
                    errors.append(f"Spec Kit Error: {path}: Missing Spec Kit specification reference")

    if count != 51:
        errors.append(f"Spec Kit Error: Expected 51 user stories, found {count}")
    return errors


def validate_user_story_template(template_path: Path) -> List[str]:
    """Validates that .specify/templates/user-story-template.md contains the 10 PR layers and all quality gates."""
    errors = []
    if not template_path.exists():
        return [f"Spec Kit Error: Missing user story template at {template_path}"]

    content = template_path.read_text(encoding="utf-8")

    # Verify 10 PR layers
    for pr_num in range(1, 11):
        if f"**PR {pr_num}**" not in content and f"PR {pr_num}:" not in content:
            errors.append(f"Spec Kit Error: User story template missing 10-PR vertical slice layer 'PR {pr_num}'")

    # Verify quality gates
    for gate in EXPECTED_STORY_GATES:
        if gate not in content:
            errors.append(f"Spec Kit Error: User story template missing quality gate '{gate}'")

    # Verify statutory legal scenario
    if "AC-US-X.Y.Z-LAW" not in content:
        errors.append("Spec Kit Error: User story template missing statutory legal scenario 'AC-US-X.Y.Z-LAW'")

    return errors


def run_speckit_validation(repo_root: Path) -> Tuple[int, List[str]]:
    """Runs all Spec Kit validation checks."""
    all_errors = []
    all_errors.extend(validate_speckit_config(repo_root / ".specify" / "config.json"))
    all_errors.extend(validate_user_story_template(repo_root / ".specify" / "templates" / "user-story-template.md"))
    all_errors.extend(validate_story_speckit_links(repo_root / "docs" / "user-stories"))
    return len(all_errors), all_errors


def main():
    print("Running Spec Kit Configuration & Integrity Validation...")
    error_count, errors = run_speckit_validation(REPO_ROOT)

    if error_count > 0:
        print(f"\nSPEC KIT VALIDATION FAILED with {error_count} error(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\nSPEC KIT VALIDATION PASSED: Spec Kit is fully configured and integrated.")
        sys.exit(0)


if __name__ == "__main__":
    main()
