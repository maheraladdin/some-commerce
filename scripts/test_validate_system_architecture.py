#!/usr/bin/env python3
"""
Test suite for Gate A1 validator (validate_system_architecture.py).
Provides negative controls:
1. Detects missing core architecture sections in SYSTEM_ARCHITECTURE.md
2. Detects forbidden lambda_http imports in Axum feature code
3. Detects forbidden root-level features directory
"""

import sys
import unittest
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_system_architecture import (
    validate_system_arch_doc,
    validate_axum_layer_decoupling,
    run_system_arch_validation,
)


class TestGateA1SystemArchitectureValidator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_missing_arch_sections_fails(self):
        # Empty doc should fail
        empty_doc = self.test_dir / "SYSTEM_ARCHITECTURE.md"
        empty_doc.write_text("# Incomplete Arch", encoding="utf-8")
        errors = validate_system_arch_doc(empty_doc)
        self.assertGreater(len(errors), 0, "Expected missing section errors for incomplete doc")

    def test_axum_layer_decoupling_detection(self):
        # Clean Axum router should pass
        features_dir = self.test_dir / "backend" / "src" / "features"
        features_dir.mkdir(parents=True)
        clean_file = features_dir / "clean.rs"
        clean_file.write_text("use axum::Router;\npub fn route() -> Router { Router::new() }", encoding="utf-8")
        errors = validate_axum_layer_decoupling(features_dir)
        self.assertEqual(len(errors), 0, f"Expected 0 errors, got: {errors}")

        # Router with lambda_http import should fail
        dirty_file = features_dir / "dirty.rs"
        dirty_file.write_text("use lambda_http::Request;\nuse axum::Router;", encoding="utf-8")
        errors = validate_axum_layer_decoupling(features_dir)
        self.assertEqual(len(errors), 1, f"Expected 1 error for lambda_http import, got: {errors}")

    def test_forbidden_root_features_detection(self):
        # Creating a root features/ directory should fail run_system_arch_validation
        root_features = self.test_dir / "features"
        root_features.mkdir(parents=True)
        # Create a mock SYSTEM_ARCHITECTURE.md with all sections to isolate root features check
        docs_dir = self.test_dir / "docs"
        docs_dir.mkdir(parents=True)
        arch_file = docs_dir / "SYSTEM_ARCHITECTURE.md"
        arch_file.write_text(
            "## 1. End-to-End System Architecture Overview & Master Diagram\n"
            "## 2. Pillar 1: Microkernel Abstract Logic\n"
            "## 3. Pillar 2: Polyglot Database Schema\n"
            "## 4. Pillar 3: Repository Tools & Monorepo Toolchain\n"
            "## 5. Pillar 4 & Pillar 5: Two-Tier Backend Caching\n"
            "## 6. Pillar 6: HTTP `ETag` & `If-None-Match`\n"
            "## 7. Pillar 7: Frontend Server-State Caching\n"
            "## 8. Pillar 8: Client-First Local Database\n"
            "## 9. Pillar 9: Headless Custom Hooks\n"
            "## 10. Pillar 10: Platform-Adaptive UI Design Layer\n",
            encoding="utf-8",
        )
        error_count, errors = run_system_arch_validation(self.test_dir)
        self.assertTrue(any("root" in e.lower() for e in errors), f"Expected root features error, got: {errors}")


if __name__ == "__main__":
    unittest.main()
