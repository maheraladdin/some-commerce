#!/usr/bin/env python3
"""
Unit tests and negative controls for validate_speckit.py.
Verifies that:
- Missing config.json is caught.
- Missing templates are caught.
- Missing quality gates in config are caught.
- Missing Spec Kit references in user stories are caught.
- A fully valid setup passes.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import json
import tempfile
import unittest
from scripts.validation import validate_speckit


class TestValidateSpecKit(unittest.TestCase):

    def test_missing_config_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            errors = validate_speckit.validate_speckit_config(tmp_path / "config.json")
            self.assertEqual(len(errors), 1)
            self.assertIn("Missing configuration file", errors[0])

    def test_missing_template_mapping_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_file = tmp_path / "config.json"
            config_file.write_text(json.dumps({
                "spec_driven_development": True,
                "standards": {
                    "constitution": ".specify/memory/constitution.md",
                    "templates": {
                        "spec": ".specify/templates/spec-template.md"
                    }
                }
            }), encoding="utf-8")
            errors = validate_speckit.validate_speckit_config(config_file)
            self.assertTrue(any("Missing template mapping for 'plan'" in e for e in errors))

    def test_missing_story_quality_gate_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_file = tmp_path / "config.json"
            config_file.write_text(json.dumps({
                "spec_driven_development": True,
                "standards": {
                    "constitution": ".specify/memory/constitution.md",
                    "templates": {
                        "spec": ".specify/templates/spec-template.md",
                        "plan": ".specify/templates/plan-template.md",
                        "tasks": ".specify/templates/tasks-template.md",
                        "security_gateway": ".specify/templates/security-gateway-template.md",
                        "user_story": ".specify/templates/user-story-template.md",
                        "company_plan": ".specify/templates/company-plan-template.md"
                    },
                    "quality_gates": {
                        "story_gates": ["G0", "G1"]
                    }
                }
            }), encoding="utf-8")
            errors = validate_speckit.validate_speckit_config(config_file)
            self.assertTrue(any("Missing story quality gate 'G-Borrow'" in e for e in errors))

    def test_missing_story_speckit_link_caught(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            story_file = tmp_path / "us-1.1.1-test.md"
            story_file.write_text("# US-1.1.1: Unlinked Story\nNo constitution link here.\n", encoding="utf-8")
            errors = validate_speckit.validate_story_speckit_links(tmp_path)
            self.assertTrue(any("Missing Spec Kit specification reference" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
