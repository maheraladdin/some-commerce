#!/usr/bin/env python3
"""
test_make_agy_agent.py - Unit test suite for Antigravity CLI Agent creation and profile discovery.
"""

import os
import shutil
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = REPO_ROOT / ".agents" / "profiles"
AGENTS_DIR = REPO_ROOT / ".agents" / "agents"
AGENT_PROFILES_DIR = REPO_ROOT / ".agent_profiles"
MAKE_SCRIPT = REPO_ROOT / "scripts" / "make_agy_agent.sh"
AGY_AGENT_SCRIPT = REPO_ROOT / "scripts" / "agy_agent.sh"
AGY_BIN = Path("/Users/maheraladdin/.local/bin/agy")


class TestMakeAgyAgent(unittest.TestCase):
    def setUp(self):
        self.test_agent_name = "test-agent-junit-1"
        self.test_sprint = "sprint-1.1"
        self.test_story = "us-1.1.1"
        self.cleanup_test_agent()

    def tearDown(self):
        self.cleanup_test_agent()

    def cleanup_test_agent(self):
        agent_dir = AGENTS_DIR / self.test_agent_name
        if agent_dir.exists():
            shutil.rmtree(agent_dir)
        profile_home = AGENT_PROFILES_DIR / self.test_agent_name
        if profile_home.exists():
            shutil.rmtree(profile_home)
        env_file = AGENT_PROFILES_DIR / f"{self.test_agent_name}.env"
        if env_file.exists():
            env_file.unlink()
        workdir = REPO_ROOT / ".agents" / "workspaces" / self.test_sprint / self.test_agent_name
        if workdir.exists():
            shutil.rmtree(workdir)

    def test_01_profile_directory_structure(self):
        """Verifies that .agents/profiles contains all company role profiles with required files."""
        self.assertTrue(PROFILES_DIR.is_dir(), f"{PROFILES_DIR} must exist")
        expected_profiles = [
            "backend-engineer",
            "junior-backend-engineer",
            "senior-backend-engineer",
            "client-engineer",
            "junior-client-engineer",
            "senior-client-engineer",
            "testing-qa-engineer",
            "junior-testing-qa-engineer",
            "senior-security-qa-auditor",
            "product-manager",
            "tech-lead",
            "system-architect",
            "ui-ux-designer",
            "security-engineer",
            "devops-engineer",
            "release-gatekeeper",
            "chief-technology-officer",
        ]
        for prof in expected_profiles:
            p_dir = PROFILES_DIR / prof
            self.assertTrue(p_dir.is_dir(), f"Profile dir {p_dir} missing")
            self.assertTrue((p_dir / "profile.yaml").is_file(), f"profile.yaml missing in {prof}")
            self.assertTrue((p_dir / "system_prompt.md").is_file(), f"system_prompt.md missing in {prof}")
            self.assertTrue((p_dir / "env.template").is_file(), f"env.template missing in {prof}")

    def test_02_antigravity_cli_agent_discovery(self):
        """Verifies that agy agents dynamically discovers all registered profiles."""
        if not AGY_BIN.is_file():
            self.skipTest(f"{AGY_BIN} not found")

        res = subprocess.run(
            [str(AGY_BIN), "agents"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=True
        )
        output = res.stdout
        self.assertIn("backend-engineer", output)
        self.assertIn("client-engineer", output)
        self.assertIn("testing-qa-engineer", output)
        self.assertIn("product-manager", output)
        self.assertIn("chief-technology-officer", output)

    def test_03_make_agy_agent_execution(self):
        """Tests scripts/make_agy_agent.sh creates complete agent workspace, agent.md, and run.sh."""
        cmd = [
            str(MAKE_SCRIPT),
            "-n", self.test_agent_name,
            "-p", "backend-engineer",
            "-s", "junior",
            "-r", "builder",
            "--sprint", self.test_sprint,
            "--story", self.test_story,
            "--pr", "1"
        ]
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"make_agy_agent.sh failed: {res.stderr}")

        # Check agent.md
        agent_md = AGENTS_DIR / self.test_agent_name / "agent.md"
        self.assertTrue(agent_md.is_file(), f"Expected {agent_md} to exist")
        agent_content = agent_md.read_text(encoding="utf-8")
        self.assertIn(f"name: {self.test_agent_name}", agent_content)
        self.assertIn("tools:", agent_content)

        # Check isolated profile home & env
        self.assertTrue((AGENT_PROFILES_DIR / self.test_agent_name).is_dir())
        self.assertTrue((AGENT_PROFILES_DIR / f"{self.test_agent_name}.env").is_file())

        # Check sprint workdir artifacts
        workdir = REPO_ROOT / ".agents" / "workspaces" / self.test_sprint / self.test_agent_name
        self.assertTrue((workdir / "agent.yaml").is_file())
        self.assertTrue((workdir / "context.md").is_file())
        self.assertTrue((workdir / "tasks.md").is_file())
        self.assertTrue((workdir / "run.sh").is_file())
        self.assertTrue(os.access(str(workdir / "run.sh"), os.X_OK))

    def test_04_negative_controls(self):
        """Negative controls: missing arguments or invalid profile must fail."""
        # Missing name
        res = subprocess.run([str(MAKE_SCRIPT), "-p", "backend-engineer"], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("--name", res.stderr)

        # Missing profile
        res = subprocess.run([str(MAKE_SCRIPT), "-n", "agent-x"], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("--profile", res.stderr)

        # Invalid profile
        res = subprocess.run([str(MAKE_SCRIPT), "-n", "agent-x", "-p", "nonexistent-profile"], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("not found in", res.stderr)

    def test_05_three_google_ai_pro_accounts(self):
        """Verifies exactly 3 physical Google AI Pro Account authentication homes exist."""
        for acc in ["agent-a", "agent-b", "agent-c"]:
            acc_home = AGENT_PROFILES_DIR / acc
            self.assertTrue(acc_home.is_dir(), f"Physical auth home {acc_home} missing")
            self.assertTrue((AGENT_PROFILES_DIR / f"{acc}.env").is_file(), f"{acc}.env missing")
            self.assertTrue((acc_home / ".gemini" / "antigravity-cli" / "settings.json").is_file())

        # Test agy_agent.sh status command
        res = subprocess.run([str(AGY_AGENT_SCRIPT), "--status"], capture_output=True, text=True, check=True)
        self.assertIn("Account A (agent-a)", res.stdout)
        self.assertIn("Account B (agent-b)", res.stdout)
        self.assertIn("Account C (agent-c)", res.stdout)

    def test_06_manage_worktrees(self):
        """Verifies scripts/manage_agent_worktrees.sh manages isolated worktrees."""
        worktree_script = REPO_ROOT / "scripts" / "manage_agent_worktrees.sh"
        self.assertTrue(worktree_script.is_file())
        self.assertTrue(os.access(str(worktree_script), os.X_OK))

        res = subprocess.run([str(worktree_script), "status"], capture_output=True, text=True, check=True)
        self.assertIn("Active Git Worktrees in .worktrees/", res.stdout)


if __name__ == "__main__":
    unittest.main()
