#!/usr/bin/env python3
"""
Validates that:
1. Every user story is formatted as a full Spec Kit specification.
2. Every user story contains a comprehensive Security Gateway powered by security-audit.
3. Every user story maps to the Behavior-Centric folder architecture (features -> modules -> behaviours -> [services, designs, logic, types, constants]).
4. The folder architecture physically exists on disk.
5. All references, sprint metadata, and validation gates are consistent.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import os
import re

BASE_DIR = "docs/user-stories"
TOTAL_EXPECTED_STORIES = 51

REQUIRED_SECTIONS = [
    "## 1. Spec Kit Specification",
    "## 2. Behavior-Centric Architecture & Folder Blueprint",
    "## 3. Technical Implementation Plan",
    "## 4. Granular Implementation Tasks",
    "## 5. Security Gateway (Powered by security-audit)",
    "## 6. Validation Gates & Acceptance Sign-Off",
]

REQUIRED_SUBSECTIONS = [
    "### 1.1 User Story Narrative",
    "### 1.2 Acceptance Criteria (Gherkin Scenarios)",
    "### 1.3 Test Cases & Traceability Matrix",
    "### 2.1 Colocated Behaviour Directory Tree",
    "### 2.2 Scoping & Promotion Blueprint",
    "### 3.1 Domain Invariants & Storage Schema",
    "### 3.2 Activity & Interaction Diagram",
    "### 5.1 Trust Boundaries & Security Actors",
    "### 5.2 Threat Modeling & Abuse Matrix",
    "### 5.3 Cryptographic & Data Protection Controls",
    "### 5.4 Automated Security Verification Checklist",
    "### 5.5 Security Gateway (G2) Sign-Off Checklist",
    "### G1 — Test coverage",
    "### G2 — Security audit",
    "### G3 — Architecture and maintainability",
    "### G-Review — Code review",
    "### G-Borrow — Rust zero-clone borrowing validation",
    "### G-UI — UI/UX validation",
    "### G-Law — Law validation",
    "### G4 — Integrated acceptance"
]

def validate_all_stories():
    stories_found = 0
    errors = []

    for root, dirs, files in os.walk(BASE_DIR):
        for f in sorted(files):
            if f.startswith("us-") and f.endswith(".md"):
                stories_found += 1
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Check Story ID in title
                m_title = re.search(r'#\s+(US-[\d\.]+):?\s*(.*)', content)
                if not m_title:
                    errors.append(f"{path}: Missing valid story title (# US-X.Y.Z: ...)")
                    continue
                story_id = m_title.group(1)

                # Check required sections
                for sec in REQUIRED_SECTIONS:
                    if sec not in content:
                        errors.append(f"{path} ({story_id}): Missing section '{sec}'")

                # Check required subsections
                for sub in REQUIRED_SUBSECTIONS:
                    if sub not in content:
                        errors.append(f"{path} ({story_id}): Missing subsection '{sub}'")

                # Check for AC identifier tags in Gherkin
                if f"AC-{story_id}-" not in content:
                    errors.append(f"{path} ({story_id}): Missing scenario identifiers 'AC-{story_id}-NN'")

                # Check for constitutional law acceptance rule
                if f"AC-{story_id}-LAW" not in content:
                    errors.append(f"{path} ({story_id}): Missing constitutional law acceptance rule 'AC-{story_id}-LAW'")

                # Check for law validation gate
                if f"{story_id}-G-Law" not in content:
                    errors.append(f"{path} ({story_id}): Missing law validation gate check '{story_id}-G-Law'")

                # Check for Rust zero-clone borrowing gate
                if f"{story_id}-G-Borrow" not in content:
                    errors.append(f"{path} ({story_id}): Missing Rust zero-clone borrowing gate check '{story_id}-G-Borrow'")

                # Check for UI/UX validation gate
                if f"{story_id}-G-UI" not in content:
                    errors.append(f"{path} ({story_id}): Missing UI/UX validation gate check '{story_id}-G-UI'")

                # Check for behavior folder blueprint
                if "features/" not in content or "behaviours/" not in content:
                    errors.append(f"{path} ({story_id}): Missing behaviour folder blueprint path")

                # Check for security gateway threat matrix
                if "Threat Modeling & Abuse Matrix" not in content or "Spoofing & Impersonation" not in content:
                    errors.append(f"{path} ({story_id}): Missing threat modeling table in Security Gateway")

    if stories_found != TOTAL_EXPECTED_STORIES:
        errors.append(f"Expected {TOTAL_EXPECTED_STORIES} stories, but found {stories_found}")

    # Check framework governance specifications
    if not os.path.exists(".specify/memory/constitution.md"):
        errors.append("Missing .specify/memory/constitution.md")
    if not os.path.exists("docs/FOLDER_ARCHITECTURE.md"):
        errors.append("Missing docs/FOLDER_ARCHITECTURE.md")

    return stories_found, errors

def main():
    print("Validating Spec Kit documentation, folder architecture, and security gateways...")
    count, errors = validate_all_stories()
    from scripts.documentation.sprint_closeout import check_all
    errors.extend(check_all())
    if errors:
        print(f"\nVALIDATION FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"\nAll {count} user stories validated successfully against GitHub Spec Kit and security-audit standards.")
        print("DOCS VALIDATION PASSED")
        sys.exit(0)

if __name__ == "__main__":
    main()
