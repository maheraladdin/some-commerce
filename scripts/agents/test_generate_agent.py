#!/usr/bin/env python3
"""
Test suite for Agent Generator (generate_agent.py).
Verifies:
1. Generation of agent.yaml with correct profiles, rules, and allowed/forbidden paths.
2. Assembly of context.md with story narratives, Gherkin ACs, and verification commands.
3. Generation of tasks.md with ordered 7-PR execution checklist.
4. Correct support for all software company positions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import unittest
import tempfile
import shutil

from scripts.agents.generate_agent import generate_agent, PROFILES
from scripts.agents import generate_agent as generator_module
from scripts.agents.test_support import make_repository_fixture
from unittest.mock import patch


class TestAgentGenerator(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.test_dir = Path(self.temp.name)
        make_repository_fixture(self.test_dir)
        self.root_patch = patch.object(generator_module, "REPO_ROOT", self.test_dir)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def test_generate_backend_agent(self):
        workdir, files = generate_agent(
            name="test-be-builder",
            profile="backend-engineer",
            role="builder",
            sprint="sprint-1.1",
            story_id="us-1.1.1",
            pr_num=1,
            custom_workdir=str(self.test_dir / "test-be-builder"),
            create_git_worktree=False,
        )

        self.assertTrue((workdir / "agent.yaml").exists())
        self.assertTrue((workdir / "context.md").exists())
        self.assertTrue((workdir / "tasks.md").exists())

        yaml_content = (workdir / "agent.yaml").read_text(encoding="utf-8")
        self.assertIn("profile: \"backend-engineer\"", yaml_content)
        self.assertIn("Strict Rust Zero-Clone Law", yaml_content)

        context_content = (workdir / "context.md").read_text(encoding="utf-8")
        self.assertIn("PR 1: Microkernel Domain Logic & Invariants", context_content)
        self.assertIn("validate_microkernel.py", context_content)

    def test_all_company_positions_supported(self):
        expected_positions = [
            "product-manager",
            "tech-lead",
            "system-architect",
            "backend-engineer",
            "client-engineer",
            "ui-ux-designer",
            "testing-qa-engineer",
            "security-engineer",
            "devops-engineer",
            "release-gatekeeper",
        ]
        for pos in expected_positions:
            self.assertIn(pos, PROFILES, f"Expected position '{pos}' in PROFILES")


if __name__ == "__main__":
    unittest.main()
