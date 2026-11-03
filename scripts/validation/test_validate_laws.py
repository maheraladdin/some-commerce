#!/usr/bin/env python3
"""
Unit tests and negative controls for validate_laws.py (Gate L1).
Verifies that violations of the non-negotiable Project Constitution laws are caught:
- Framework Scoping Law (features/ at root)
- Zero-Clone Law (unauthorized .clone())
- Microkernel Purity Law (cloud SDKs in crates/)
- Axum Decoupling Law (lambda_http in features/)
- Spec Kit Law Acceptance Rule (missing AC-*-LAW)
- Law Validation Gate (missing G-Law)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import tempfile
import unittest
from scripts.validation import validate_laws


class TestValidateLaws(unittest.TestCase):

    def test_framework_scoping_negative_control(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            root_features = tmp_path / "features"
            root_features.mkdir()
            errors = validate_laws.validate_framework_scoping_law(tmp_path)
            self.assertTrue(any("Constitutional Law 2 Violation" in e for e in errors))

    def test_zero_clone_negative_control(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            crates_dir = tmp_path / "crates" / "some-kernel" / "src"
            crates_dir.mkdir(parents=True)
            bad_file = crates_dir / "lib.rs"
            bad_file.write_text("pub fn process(data: DomainModel) -> DomainModel { data.clone() }\n", encoding="utf-8")
            errors = validate_laws.validate_zero_clone_law(tmp_path)
            self.assertTrue(any("Constitutional Law 3 Violation" in e for e in errors))

    def test_microkernel_purity_negative_control(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            crate_dir = tmp_path / "crates" / "some-kernel"
            crate_dir.mkdir(parents=True)
            bad_cargo = crate_dir / "Cargo.toml"
            bad_cargo.write_text("[dependencies]\naws-sdk-dynamodb = \"1.0\"\n", encoding="utf-8")
            errors = validate_laws.validate_microkernel_purity_law(tmp_path / "crates")
            self.assertTrue(any("Constitutional Law 4 Violation" in e for e in errors))

    def test_axum_decoupling_negative_control(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            feature_dir = tmp_path / "features" / "auth"
            feature_dir.mkdir(parents=True)
            bad_handler = feature_dir / "routes.rs"
            bad_handler.write_text("use lambda_http::Request;\npub async fn handler() {}\n", encoding="utf-8")
            errors = validate_laws.validate_axum_portability_law(tmp_path / "features")
            self.assertTrue(any("Constitutional Law 5 Violation" in e for e in errors))

    def test_missing_law_acceptance_rule_negative_control(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            stories_dir = tmp_path / "user-stories"
            stories_dir.mkdir(parents=True)
            bad_story = stories_dir / "us-1.1.1-test.md"
            bad_story.write_text(
                "# US-1.1.1: Test Story\n"
                "PK = TENANT#123\n"
                "Scenario: [AC-US-1.1.1-01] Valid scenario\n"
                "### G-Law — Law validation\n"
                "- [ ] **US-1.1.1-G-Law:** pass\n"
                "- [ ] **US-1.1.1-G-Review:** pass\n",
                encoding="utf-8"
            )
            errors = validate_laws.validate_stories_constitutional_laws(stories_dir)
            self.assertTrue(any("Missing constitutional law acceptance rule 'AC-US-1.1.1-LAW'" in e for e in errors))

    def test_missing_law_gate_negative_control(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            stories_dir = tmp_path / "user-stories"
            stories_dir.mkdir(parents=True)
            bad_story = stories_dir / "us-1.1.1-test.md"
            bad_story.write_text(
                "# US-1.1.1: Test Story\n"
                "PK = TENANT#123\n"
                "Scenario: [AC-US-1.1.1-01] Valid scenario\n"
                "Scenario: [AC-US-1.1.1-LAW] Law scenario\n"
                "- [ ] **US-1.1.1-G-Review:** pass\n",
                encoding="utf-8"
            )
            errors = validate_laws.validate_stories_constitutional_laws(stories_dir)
            self.assertTrue(any("Missing law validation gate 'US-1.1.1-G-Law'" in e for e in errors))

    def test_catalog_role_separation_negative_control(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            profiles_dir = tmp_path / ".agents" / "profiles"
            profiles_dir.mkdir(parents=True)
            bad_catalog = profiles_dir / "catalog.json"
            bad_catalog.write_text('{"roles": {"only-one": {}}, "common": {}}\n', encoding="utf-8")
            errors = validate_laws.validate_role_separation_law(tmp_path)
            self.assertTrue(any("Expected exactly 17 company roles" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
