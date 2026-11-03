#!/usr/bin/env python3
"""
Adds Gate G-Borrow (Rust Zero-Clone Borrowing) and Gate G-UI (UI/UX Platform Presentation)
to all 51 user stories across docs/user-stories/**/us-*.md.
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STORIES_DIR = REPO_ROOT / "docs" / "user-stories"

def update_story_file(file_path: Path) -> bool:
    content = file_path.read_text(encoding="utf-8")
    m_id = re.search(r"#\s+(US-[\d\.]+)", content)
    if not m_id:
        print(f"Skipping {file_path}: No story ID found.")
        return False

    story_id = m_id.group(1)
    modified = False

    # 1. Update intro line in Section 6
    old_intro = "All [G0–G4 quality gates + G-Review + G-Law]"
    new_intro = "All [G0–G4 quality gates + G-Review + G-Borrow + G-UI + G-Law]"
    if old_intro in content:
        content = content.replace(old_intro, new_intro)
        modified = True

    # 2. Add G-Borrow and G-UI subsections if not present
    g_borrow_section = (
        f"### G-Borrow — Rust zero-clone borrowing validation\n"
        f"- [ ] **{story_id}-G-Borrow:** Backend code relies strictly on borrowing (&T, &mut T), "
        f"explicit lifetimes, zero-copy byte buffers (bytes::Bytes), and zero unauthorized deep .clone() "
        f"calls on domain entities and models (Arc::clone and Rc::clone pointer copies permitted only); "
        f"certified by systems reviewer.\n\n"
    )

    g_ui_section = (
        f"### G-UI — UI/UX validation\n"
        f"- [ ] **{story_id}-G-UI:** Pure separation of presentation (designs/, owned by ui-ux-designer) "
        f"and headless hooks (logic/, owned by client-engineer); mobile components use @expo/ui primitives "
        f"and native modules; web components use semantic HTML5 styled with Tailwind CSS; "
        f"WCAG 2.1 AA and Arabic RTL layout parity verified; certified by UI/UX designer.\n\n"
    )

    if f"{story_id}-G-Borrow" not in content and f"{story_id}-G-UI" not in content:
        # Insert before G-Law
        law_header = "### G-Law — Law validation"
        if law_header in content:
            replacement = g_borrow_section + g_ui_section + law_header
            content = content.replace(law_header, replacement, 1)
            modified = True
        else:
            print(f"Warning: {file_path} missing '{law_header}'")

    if modified:
        file_path.write_text(content, encoding="utf-8")
        return True

    return False


def main():
    count = 0
    updated = 0
    for root, dirs, files in os.walk(STORIES_DIR):
        for f in sorted(files):
            if f.startswith("us-") and f.endswith(".md"):
                count += 1
                path = Path(root) / f
                if update_story_file(path):
                    updated += 1

    print(f"Scanned {count} user stories. Updated {updated} files.")

if __name__ == "__main__":
    main()
