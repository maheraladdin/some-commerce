#!/usr/bin/env python3
"""Launcher/generator integration checks in disposable repositories with a fake CLI."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import json
import os
import subprocess
import tempfile
import unittest
from scripts.agents.test_support import make_repository_fixture


class TestMakeAgyAgent(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = make_repository_fixture(self.temp.name)
        self.fake = self.root / 'fake-agy'
        self.fake.write_text('#!/bin/sh\nprintf "FAKE_CLI %s\\n" "$*"\n')
        self.fake.chmod(0o755)
        self.env = {'PATH': os.environ['PATH'], 'AGY_BIN': str(self.fake), 'PYTHONDONTWRITEBYTECODE': '1'}
        self.make = self.root / 'scripts/agents/make_agy_agent.sh'

    def command(self, *args):
        return subprocess.run(args, cwd=self.root, env=self.env, capture_output=True, text=True)

    def test_every_role_has_profile_prompt_and_environment_template(self):
        catalog = json.loads((self.root / '.agents/profiles/catalog.json').read_text())
        self.assertEqual(len(catalog['roles']), 17)
        for role in catalog['roles']:
            for file in ('profile.yaml', 'system_prompt.md', 'env.template'):
                self.assertTrue((self.root / '.agents/profiles' / role / file).is_file())

    def test_generation_and_one_click_runner_use_shared_pool(self):
        result = self.command('bash', str(self.make), '-n', 'fixture-junior', '-p', 'junior-backend-engineer', '--pr', '1')
        self.assertEqual(result.returncode, 0, result.stderr)
        workdir = self.root / '.agents/workspaces/sprint-1.1/fixture-junior'
        for file in ('agent.yaml', 'context.md', 'tasks.md', 'run.sh'):
            self.assertTrue((workdir / file).is_file())
        self.assertIn('Spec Kit', (workdir / 'context.md').read_text())
        run = self.command('bash', str(workdir / 'run.sh'), '-p', 'synthetic task')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn('FAKE_CLI --agent fixture-junior', run.stdout)
        ledger = json.loads((self.root / '.agent_profiles/quota.json').read_text())
        self.assertFalse(ledger['reservations'])
        self.assertEqual(sum(row['used'] for row in ledger['accounts'].values()), 1)

    def test_missing_name_profile_and_unknown_profile_fail(self):
        for args, expected in ((['-p', 'backend-engineer'], '--name'),
                               (['-n', 'fixture'], '--profile'),
                               (['-n', 'fixture', '-p', 'does-not-exist'], 'not found')):
            result = self.command('bash', str(self.make), *args)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(expected, result.stderr)

    def test_status_and_listing_do_not_call_live_provider(self):
        script = self.root / 'scripts/agents/agy_agent.sh'
        status = self.command('bash', str(script), '--status')
        self.assertEqual(status.returncode, 0, status.stderr)
        for account in ('A', 'B', 'C'):
            self.assertIn('Account '+account, status.stdout)
        listing = self.command('bash', str(script), '--list')
        self.assertEqual(listing.returncode, 0, listing.stderr)
        self.assertIn('FAKE_CLI agents', listing.stdout)

    def test_worktree_status_uses_the_fixture_repository(self):
        init = self.command('git', 'init', str(self.root))
        self.assertEqual(init.returncode, 0, init.stderr)
        status = self.command('bash', str(self.root / 'scripts/agents/manage_agent_worktrees.sh'), 'status')
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertIn('Active Git Worktrees in .worktrees/', status.stdout)
        self.assertIn(str(self.root), status.stdout)


if __name__ == '__main__':
    unittest.main()
