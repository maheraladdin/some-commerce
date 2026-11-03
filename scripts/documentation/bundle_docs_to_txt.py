#!/usr/bin/env python3
"""
Bundle Docs to Text Script
Consolidates all markdown documentation from the docs/ directory into a single,
well-organized, searchable text file with a Table of Contents and document delimiters.

Usage:
    python3 scripts/documentation/bundle_docs_to_txt.py [--output docs/SOME_COMMERCE_FULL_DOCS.txt]
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import os
import argparse
from datetime import datetime

DOCS_DIR = 'docs'
DEFAULT_OUTPUT = os.path.join(DOCS_DIR, 'SOME_COMMERCE_FULL_DOCS.txt')

def sprint_sort_key(filename):
    """Sort sprints like sprint-1.1.md, sprint-1.2.md, ..., sprint-6.3.md"""
    base = os.path.basename(filename)
    if 'README' in base:
        return (0, 0, 0)
    match = re.search(r'sprint-(\d+)\.(\d+)', base)
    if match:
        return (1, int(match.group(1)), int(match.group(2)))
    return (2, 0, base)

import re

def get_ordered_doc_files(docs_root):
    """
    Returns a logically ordered list of relative paths for all markdown files in docs/
    """
    all_files = []
    for root, _, files in os.walk(docs_root):
        for f in files:
            if f.endswith('.md'):
                rel_path = os.path.relpath(os.path.join(root, f), '.')
                all_files.append(rel_path)

    # Ordering categories
    core_specs = [
        'docs/SYSTEM_ARCHITECTURE.md',
        'docs/SDUI_AND_LOCALIZATION.md',
        'docs/PAYMENTS_SHIPPING_AND_LICENSING.md',
        'docs/DEPLOYMENT_AND_AWS_MARKETPLACE.md',
    ]

    # Collect user-stories files
    us_master = ['docs/user-stories/README.md']
    us_module_readmes = []
    us_story_files = []

    # Collect sprints files
    sprints_master = ['docs/sprints/README.md']
    sprint_files = []

    remaining_files = []

    for f in all_files:
        if f in core_specs:
            continue
        elif f == 'docs/user-stories/README.md':
            continue
        elif f == 'docs/sprints/README.md':
            continue
        elif f.startswith('docs/user-stories/'):
            base = os.path.basename(f)
            if base == 'README.md':
                us_module_readmes.append(f)
            else:
                us_story_files.append(f)
        elif f.startswith('docs/sprints/'):
            sprint_files.append(f)
        else:
            remaining_files.append(f)

    # Sort module readmes by module directory name
    us_module_readmes.sort()
    
    # Sort user stories by module and story ID
    us_story_files.sort()

    # Sort sprint files in numeric order
    sprint_files.sort(key=sprint_sort_key)

    remaining_files.sort()

    ordered = []
    # 1. Existing core specs in order
    for spec in core_specs:
        if spec in all_files:
            ordered.append(spec)

    # 2. Master User Stories Index
    if 'docs/user-stories/README.md' in all_files:
        ordered.append('docs/user-stories/README.md')

    # 3. User Stories by Module: Module README followed by its story files
    modules = sorted(list(set(os.path.dirname(f) for f in us_module_readmes + us_story_files)))
    for mod in modules:
        mod_readme = os.path.join(mod, 'README.md')
        if mod_readme in us_module_readmes:
            ordered.append(mod_readme)
        mod_stories = sorted([f for f in us_story_files if os.path.dirname(f) == mod])
        ordered.extend(mod_stories)

    # 4. Master Sprints Index
    if 'docs/sprints/README.md' in all_files:
        ordered.append('docs/sprints/README.md')
    ordered.extend(sprint_files)

    # 5. Remaining
    ordered.extend(remaining_files)

    return ordered

def compile_docs(output_file):
    docs_files = get_ordered_doc_files(DOCS_DIR)
    
    total_docs = len(docs_files)
    if total_docs == 0:
        print("No markdown documentation files found in docs/")
        return

    print(f"Discovered {total_docs} documentation files in {DOCS_DIR}/")

    # Read all files into memory
    file_contents = []
    total_chars = 0
    total_words = 0
    total_raw_lines = 0

    for rel_path in docs_files:
        with open(rel_path, 'r', encoding='utf-8') as f:
            text = f.read()
        file_contents.append((rel_path, text))
        total_chars += len(text)
        total_words += len(text.split())
        total_raw_lines += text.count('\n') + 1

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    # Build Header and Table of Contents
    header_lines = [
        "================================================================================",
        "                        SOME-COMMERCE CONSOLIDATED DOCUMENTATION                ",
        "================================================================================",
        f"Project: some-commerce",
        f"Compiled: {timestamp}",
        f"Total Documents: {total_docs}",
        f"Total Raw Lines: {total_raw_lines:,}",
        f"Total Words: {total_words:,}",
        f"Output Destination: {output_file}",
        "================================================================================",
        "",
        "TABLE OF CONTENTS",
        "--------------------------------------------------------------------------------",
    ]

    for idx, (rel_path, _) in enumerate(file_contents, start=1):
        header_lines.append(f"{idx:02d}. {rel_path}")

    header_lines.extend([
        "--------------------------------------------------------------------------------",
        "",
        ""
    ])

    # Now write the combined output file
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write('\n'.join(header_lines))

        for idx, (rel_path, content) in enumerate(file_contents, start=1):
            banner = [
                "================================================================================",
                f"DOCUMENT [{idx}/{total_docs}]: {rel_path}",
                "================================================================================",
                ""
            ]
            out.write('\n'.join(banner))
            out.write(content.rstrip())
            out.write("\n\n")
            footer = [
                "--------------------------------------------------------------------------------",
                f"END OF DOCUMENT [{idx}/{total_docs}]: {rel_path}",
                "================================================================================",
                "",
                ""
            ]
            out.write('\n'.join(footer))

    file_size_kb = os.path.getsize(output_file) / 1024
    print(f"Successfully compiled {total_docs} files into: {output_file}")
    print(f"Output File Size: {file_size_kb:.1f} KB")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compile all documentation in docs/ into a single text file.")
    parser.add_argument(
        '-o', '--output',
        default=DEFAULT_OUTPUT,
        help=f"Path to output text file (default: {DEFAULT_OUTPUT})"
    )
    args = parser.parse_args()
    compile_docs(args.output)
