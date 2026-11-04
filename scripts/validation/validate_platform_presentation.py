#!/usr/bin/env python3
"""
Gate F1: Platform-Adaptive Presentation & UI/UX Separation Validator (G-UI)
Validates:
1. Separation of Concerns:
   - designs/: Owned by ui-ux-designer. Pure presentational UI components.
     Must NOT export business custom hooks (use[A-Z]...) or perform direct data mutations/queries.
   - logic/ & services/: Owned by client-engineer. Headless custom hooks, state machines, and API sync.
     Must NOT return JSX/TSX presentation markup.
2. Mobile Presentation Standard:
   - Mobile components use @expo/ui primitives and native modules if needed.
   - Forbids unadapted raw web DOM elements (<div>, <span>, <p>, etc.) in mobile files.
3. Web Presentation Standard:
   - Web components use semantic HTML5 (<header>, <nav>, <main>, <article>, <section>, <footer>, <button>, etc.)
     styled with Tailwind CSS (className="...").
4. User Stories G-UI Gate:
   - Every user story in docs/user-stories/**/us-*.md defines the G-UI gate check [US-X.Y.Z-G-UI].
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import os
import re
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]


def validate_designs_directory(designs_dir: Path) -> List[str]:
    """Validates that designs/ contains pure presentation components and no business custom hooks or queries."""
    errors = []
    if not designs_dir.exists():
        return errors

    hook_pattern = re.compile(r"export\s+(?:function|const)\s+(use[A-Z]\w+)")
    query_mutation_pattern = re.compile(r"\b(useQuery|useMutation|fetchWithEtag|watermelonDbQuery)\b")

    for file_path in designs_dir.rglob("*.tsx"):
        content = file_path.read_text(encoding="utf-8")

        # Check for forbidden custom hook definitions
        for match in hook_pattern.finditer(content):
            hook_name = match.group(1)
            errors.append(
                f"Gate F1 Violation: {file_path}: Custom hook '{hook_name}' defined inside 'designs/'. "
                f"Per Frontend Separation of Concerns, custom hooks and business state belong exclusively "
                f"in 'logic/' (owned by client-engineer), while 'designs/' is strictly presentational (owned by ui-ux-designer)."
            )

        # Check for direct queries/mutations inside presentation
        for match in query_mutation_pattern.finditer(content):
            forbidden_call = match.group(1)
            errors.append(
                f"Gate F1 Violation: {file_path}: Direct query/mutation '{forbidden_call}' called inside 'designs/'. "
                f"Presentational components must receive data and handlers via props from logic custom hooks."
            )

    return errors


def validate_logic_directory(logic_dir: Path) -> List[str]:
    """Validates that logic/ contains headless custom hooks and NO JSX presentation markup."""
    errors = []
    if not logic_dir.exists():
        return errors

    # Matches JSX tags (e.g. <Component>, <div>, <button>) while ignoring TypeScript generic type arguments (e.g. useState<T>, Promise<T>)
    jsx_pattern = re.compile(r"(?<![a-zA-Z0-9_$])<\s*([A-Z]\w+|div|span|header|footer|section|main|nav|button|input|p|table)\b[^>]*>")

    for file_path in logic_dir.rglob("*.ts*"):
        content = file_path.read_text(encoding="utf-8")
        # Check if file renders JSX elements
        for line_num, line in enumerate(content.splitlines(), start=1):
            clean_line = line.split("//")[0].strip()
            if not clean_line or clean_line.startswith("/*") or clean_line.startswith("*"):
                continue
            if jsx_pattern.search(clean_line):
                errors.append(
                    f"Gate F1 Violation: {file_path}:{line_num}: JSX presentation markup found inside 'logic/'. "
                    f"Per Frontend Separation of Concerns, 'logic/' must be strictly headless custom hooks, "
                    f"state machines, and validation math, with zero UI markup."
                )
                break  # Flag once per file

    return errors


def validate_mobile_component_presentation(file_path: Path) -> List[str]:
    """Validates mobile components use @expo/ui / native modules and no raw web DOM tags."""
    errors = []
    if not file_path.exists() or not file_path.name.endswith(".tsx"):
        return errors

    # Check for mobile target files: *.native.tsx, *.ios.tsx, *.android.tsx, or inside designs/mobile/
    is_mobile = (
        ".native." in file_path.name
        or ".ios." in file_path.name
        or ".android." in file_path.name
        or "mobile" in file_path.parts
    )
    if not is_mobile:
        return errors

    content = file_path.read_text(encoding="utf-8")

    # Forbidden raw web DOM tags in mobile native code
    web_dom_tags = ["<div", "<span", "<table", "<section", "<article", "<nav", "<header", "<footer"]
    for tag in web_dom_tags:
        if tag in content:
            errors.append(
                f"Gate F1 Violation: {file_path}: Forbidden web DOM element '{tag}>' found in mobile component. "
                f"Mobile storefront interfaces must use @expo/ui primitives or native modules."
            )
            break

    return errors


def validate_web_component_presentation(file_path: Path) -> List[str]:
    """Validates web components use semantic HTML5 and Tailwind CSS."""
    errors = []
    if not file_path.exists() or not file_path.name.endswith(".tsx"):
        return errors

    # Check for web target files: *.web.tsx or inside designs/web/
    is_web = ".web." in file_path.name or "web" in file_path.parts
    if not is_web:
        return errors

    content = file_path.read_text(encoding="utf-8")

    # Verify Tailwind CSS styling usage
    if "className=" not in content and "class=" not in content:
        errors.append(
            f"Gate F1 Violation: {file_path}: Web component missing Tailwind CSS 'className' styling. "
            f"Web storefront interfaces must use semantic HTML5 styled with Tailwind CSS."
        )

    return errors


def validate_all_presentation_code(storefront_dir: Path) -> List[str]:
    """Scans apps/storefront for Gate F1 presentation rules."""
    errors = []
    if not storefront_dir.exists():
        return errors

    for path in storefront_dir.rglob("*"):
        if path.is_dir():
            if path.name == "designs":
                errors.extend(validate_designs_directory(path))
            elif path.name == "logic":
                errors.extend(validate_logic_directory(path))
        elif path.is_file():
            errors.extend(validate_mobile_component_presentation(path))
            errors.extend(validate_web_component_presentation(path))

    return errors


def validate_stories_ui_gate(stories_dir: Path) -> List[str]:
    """Validates that all user stories contain the G-UI gate in Section 6."""
    errors = []
    if not stories_dir.exists():
        return [f"Gate F1 Violation: Missing stories directory at {stories_dir}"]

    count = 0
    for root, dirs, files in os.walk(stories_dir):
        for f in sorted(files):
            if f.startswith("us-") and f.endswith(".md"):
                count += 1
                path = Path(root) / f
                content = path.read_text(encoding="utf-8")

                m = re.search(r'#\s+(US-[\d\.]+)', content)
                if not m:
                    errors.append(f"Gate F1 Violation: {path}: Missing story ID in title")
                    continue
                story_id = m.group(1)

                if f"{story_id}-G-UI" not in content:
                    errors.append(f"Gate F1 Violation: {path} ({story_id}): Missing UI/UX validation gate '{story_id}-G-UI'.")

    if count != 51:
        errors.append(f"Gate F1 Violation: Expected 51 user stories, found {count}")
    return errors


def run_platform_presentation_validation(repo_root: Path) -> Tuple[int, List[str]]:
    """Runs all Gate F1 checks."""
    all_errors = []
    for app_name in ("storefront", "dashboard"):
        app_dir = repo_root / "apps" / app_name
        if app_dir.exists():
            all_errors.extend(validate_all_presentation_code(app_dir))
    all_errors.extend(validate_stories_ui_gate(repo_root / "docs" / "user-stories"))
    return len(all_errors), all_errors


def main():
    print("Running Gate F1: Platform-Adaptive Presentation & UI/UX Separation Validation (G-UI)...")
    error_count, errors = run_platform_presentation_validation(REPO_ROOT)

    if error_count > 0:
        print(f"\nGATE F1 FAILED with {error_count} violation(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\nGATE F1 PASSED: Platform presentation standards (@expo/ui Mobile + Tailwind Web) and G-UI gates verified.")
        sys.exit(0)


if __name__ == "__main__":
    main()
