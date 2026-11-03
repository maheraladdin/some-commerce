#!/usr/bin/env python3
"""
Test suite for Gate A2 validator (validate_folder_architecture.py).
Provides negative controls:
1. Detects forbidden root-level features/ or shared/ directories.
2. Detects invalid subdirectories in 4-tier LoB hierarchy.
3. Detects 'designs/' directory inside backend features.
4. Detects direct sibling behaviour imports.
"""

import sys
import unittest
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_folder_architecture import (
    validate_framework_scoping,
    validate_behaviour_directory_structure,
    validate_no_sibling_cross_imports,
    run_folder_arch_validation,
)


class TestGateA2FolderArchitectureValidator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_framework_scoping_violation(self):
        # Root features/ must fail
        root_features = self.test_dir / "features"
        root_features.mkdir()
        errors = validate_framework_scoping(self.test_dir)
        self.assertEqual(len(errors), 1)
        self.assertIn("root", errors[0].lower())

    def test_backend_designs_forbidden(self):
        # Backend behaviour having 'designs' must fail
        backend_dir = self.test_dir / "features" / "auth" / "modules" / "otp" / "behaviours" / "send-otp" / "designs"
        backend_dir.mkdir(parents=True)
        errors = validate_behaviour_directory_structure(self.test_dir / "features", is_client=False)
        self.assertTrue(any("designs" in e.lower() for e in errors))

    def test_client_valid_structure_passes(self):
        # Client behaviour with standard folders should pass
        client_dir = self.test_dir / "features" / "catalog" / "modules" / "search" / "behaviours" / "facet-filter"
        for sub in ("services", "designs", "logic", "types", "constants"):
            (client_dir / sub).mkdir(parents=True)
        errors = validate_behaviour_directory_structure(self.test_dir / "features", is_client=True)
        self.assertEqual(len(errors), 0, f"Expected 0 errors, got: {errors}")

    def test_sibling_cross_import_detection(self):
        # Sibling import without _shared should fail
        b1_dir = self.test_dir / "features" / "auth" / "modules" / "otp" / "behaviours" / "verify-otp" / "logic"
        b1_dir.mkdir(parents=True)
        bad_file = b1_dir / "bad.ts"
        bad_file.write_text("import { sendOtp } from '../../send-otp/services/api';", encoding="utf-8")
        errors = validate_no_sibling_cross_imports(self.test_dir / "features")
        self.assertEqual(len(errors), 1)
        self.assertIn("direct sibling behaviour import", errors[0].lower())


if __name__ == "__main__":
    unittest.main()
