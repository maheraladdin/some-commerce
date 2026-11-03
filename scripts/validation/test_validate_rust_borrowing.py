#!/usr/bin/env python3
"""
Unit tests and negative controls for validate_rust_borrowing.py (Gate R1).
Verifies that:
- Deep .clone() calls on domain types are caught.
- Permitted patterns (Arc::clone, Rc::clone, derive(Clone), borrowing) pass.
- Missing {story_id}-G-Borrow in user stories is caught.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import tempfile
import unittest
from scripts.validation import validate_rust_borrowing


class TestValidateRustBorrowing(unittest.TestCase):

    def test_deep_clone_violation_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            rs_file = tmp_path / "entity.rs"
            rs_file.write_text(
                "pub fn process(order: Order) -> Order {\n"
                "    let copy = order.clone();\n"
                "    copy\n"
                "}\n",
                encoding="utf-8"
            )
            errors = validate_rust_borrowing.validate_rust_source_borrowing(rs_file)
            self.assertEqual(len(errors), 1)
            self.assertIn("Gate R1 Violation", errors[0])
            self.assertIn("Unauthorized deep .clone()", errors[0])

    def test_permitted_arc_rc_and_derive_clone_pass(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            rs_file = tmp_path / "valid.rs"
            rs_file.write_text(
                "#[derive(Clone, Debug)]\n"
                "pub struct SafeHandle;\n\n"
                "pub fn share(handle: &Arc<SafeHandle>) -> Arc<SafeHandle> {\n"
                "    Arc::clone(handle)\n"
                "}\n\n"
                "pub fn share_rc(handle: &Rc<SafeHandle>) -> Rc<SafeHandle> {\n"
                "    Rc::clone(handle)\n"
                "}\n\n"
                "pub fn borrow_only(data: &SafeHandle) -> &SafeHandle {\n"
                "    data\n"
                "}\n",
                encoding="utf-8"
            )
            errors = validate_rust_borrowing.validate_rust_source_borrowing(rs_file)
            self.assertEqual(len(errors), 0)

    def test_missing_story_g_borrow_gate_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            story_file = tmp_path / "us-1.1.1-auth.md"
            story_file.write_text(
                "# US-1.1.1: Customer Authentication\n"
                "### 6. Validation Gates & Acceptance Sign-Off\n"
                "- [ ] **US-1.1.1-G-Review:** pass\n",
                encoding="utf-8"
            )
            errors = validate_rust_borrowing.validate_stories_borrow_gate(tmp_path)
            self.assertTrue(any("Missing Rust zero-clone gate 'US-1.1.1-G-Borrow'" in e for e in errors))

    def test_valid_story_g_borrow_gate_passes(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # Create dummy 51 stories with valid G-Borrow
            for i in range(1, 52):
                f = tmp_path / f"us-1.1.{i}.md"
                f.write_text(
                    f"# US-1.1.{i}: Story {i}\n"
                    f"### G-Borrow — Rust zero-clone borrowing validation\n"
                    f"- [ ] **US-1.1.{i}-G-Borrow:** Zero deep .clone() calls verified.\n",
                    encoding="utf-8"
                )
            errors = validate_rust_borrowing.validate_stories_borrow_gate(tmp_path)
            self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
