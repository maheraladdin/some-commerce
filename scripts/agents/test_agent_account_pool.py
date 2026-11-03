#!/usr/bin/env python3
"""Bounded local negative controls; no provider calls or real authentication."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import concurrent.futures
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from scripts.agents.agent_account_pool import ACCOUNTS, Pool

ROOT = Path(__file__).resolve().parents[2]

class AccountPoolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)
        self.pool = Pool(self.path)
        for name in ACCOUNTS:
            (self.path / name).mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_every_role_balances_across_all_accounts(self):
        catalog = json.loads((ROOT / '.agents/profiles/catalog.json').read_text())
        for role in catalog['roles']:
            picks = []
            for _ in range(3):
                account, token = self.pool.reserve(role)
                picks.append(account)
                self.pool.finish(token)
            self.assertEqual(set(picks), set(ACCOUNTS), role)

    def test_parallel_reservations_are_atomic(self):
        def reserve(_):
            try: return self.pool.reserve('same-role')
            except ValueError: return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            results = [r for r in executor.map(reserve, range(8)) if r]
        self.assertEqual(len(results), 3)
        self.assertEqual({r[0] for r in results}, set(ACCOUNTS))

    def test_budget_cooldown_disable_and_no_available(self):
        self.pool.configure('agent-a', budget=1, used=1)
        self.pool.configure('agent-b', enabled=False)
        self.pool.configure('agent-c', cooldown_until=10**12)
        with self.assertRaisesRegex(ValueError, 'No account available'):
            self.pool.reserve('cto')
        self.pool.configure('agent-c', cooldown_until=0)
        account, token = self.pool.reserve('cto')
        self.assertEqual(account, 'agent-c')
        self.pool.finish(token)
        self.pool.finish(token)
        with self.pool.state() as state:
            self.assertEqual(state['accounts']['agent-c']['used'], 1)

    def test_explicit_pin_and_invalid_units(self):
        for role in ('junior-backend-engineer', 'chief-technology-officer'):
            account, token = self.pool.reserve(role, 'agent-b')
            self.assertEqual(account, 'agent-b')
            self.pool.finish(token)
        for value in (0, -1, float('nan'), float('inf')):
            with self.assertRaises(ValueError): self.pool.reserve('test', units=value)

    def test_corrupt_ledger_is_not_reset(self):
        (self.path / 'quota.json').write_text('{bad data')
        with self.assertRaises(ValueError): self.pool.reserve('test')
        self.assertEqual((self.path / 'quota.json').read_text(), '{bad data')

    def test_failed_command_charged_once_and_releases_reservation(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/agents/agent_account_pool.py'),
            '--state-dir', str(self.path), 'run', '--role', 'test', '--',
            sys.executable, '-c', 'import sys; sys.exit(7)'], capture_output=True)
        self.assertEqual(result.returncode, 7)
        with self.pool.state() as state:
            self.assertFalse(state['reservations'])
            self.assertEqual(sum(r['used'] for r in state['accounts'].values()), 1)

    def test_recovery_preserves_live_or_ambiguous_reservations(self):
        _, token = self.pool.reserve('live')
        self.assertEqual(self.pool.recover(), 0)
        with self.pool.state() as state:
            state['reservations'][token]['child_pid'] = os.getpid()
        self.assertEqual(self.pool.recover(), 0)

    def test_launcher_roles_ignore_legacy_account_binding(self):
        # Disposable repository, synthetic auth homes, and a fake CLI.
        repo = self.path / 'repo'
        (repo / 'scripts/agents').mkdir(parents=True)
        for name in ('agy_agent.sh', 'agent_account_pool.py'):
            shutil.copy2(ROOT / 'scripts/agents' / name, repo / 'scripts/agents' / name)
        for account in ACCOUNTS:
            (repo / '.agent_profiles' / account).mkdir(parents=True)
        name = 'chief-technology-officer'
        (repo / '.agents/agents' / name).mkdir(parents=True)
        (repo / '.agent_profiles' / (name + '.env')).write_text('ACCOUNT="agent-c"\n')
        fake = repo / 'fake-agy'
        fake.write_text('#!/bin/sh\nprintf "%s" "$AGENT_POOL_ACCOUNT"\n')
        fake.chmod(0o755)
        env = {'PATH': os.environ['PATH'], 'AGY_BIN': str(fake), 'PYTHONDONTWRITEBYTECODE': '1'}
        picks = []
        for _ in range(3):
            run = subprocess.run(['bash', str(repo / 'scripts/agents/agy_agent.sh'), name, '-p', 'synthetic'],
                                 env=env, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            picks.append(run.stdout.strip().splitlines()[-1])
        self.assertEqual(set(picks), set(ACCOUNTS))
        run = subprocess.run(['bash', str(repo / 'scripts/agents/agy_agent.sh'), '--account', 'b', name],
                             env=env, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.strip().splitlines()[-1], 'agent-b')

class ProfileRenderingTests(unittest.TestCase):
    def test_refresh_renders_detailed_profiles_without_touching_auth(self):
        spec = importlib.util.spec_from_file_location('setup_profiles', ROOT / 'scripts/agents/setup_agent_profiles.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            module.PROFILES_DIR = base / 'profiles'
            module.AGENTS_DIR = base / 'agents'
            module.AGENT_PROFILES_DIR = base / 'auth'
            module.PROFILES_DIR.mkdir()
            shutil.copy2(ROOT / '.agents/profiles/catalog.json', module.PROFILES_DIR / 'catalog.json')
            module.refresh_descriptions()
            self.assertFalse(module.AGENT_PROFILES_DIR.exists())
            catalog = module.role_catalog()
            for role in module.COMPANY_ROLES:
                metadata = (module.PROFILES_DIR / role / 'profile.yaml').read_text()
                prompt = (module.PROFILES_DIR / role / 'system_prompt.md').read_text()
                self.assertIn('auth_account: auto', metadata)
                self.assertIn(catalog['roles'][role]['description'], prompt)
                self.assertIn('Spec Kit', prompt)
                self.assertIn('non-contributing reviewer', prompt)
                self.assertIn(catalog['common']['planning'], prompt)
                self.assertIn(catalog['common']['story_record'], prompt)
                self.assertIn(catalog['roles'][role]['planning_duties'], prompt)
                self.assertIn(catalog['roles'][role]['collection_duties'], prompt)
                self.assertIn('Planning-only assignments use approved upstream direction', prompt)
                self.assertIn(prompt, (module.AGENTS_DIR / role / 'agent.md').read_text())
            for account in ACCOUNTS:
                text = (module.AGENTS_DIR / account / 'agent.md').read_text()
                for role in module.COMPANY_ROLES: self.assertIn('`'+role+'`', text)

    def test_instance_generation_embeds_profile_and_balanced_runner(self):
        spec = importlib.util.spec_from_file_location('generator', ROOT / 'scripts/agents/generate_agent.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            module.REPO_ROOT = base
            shutil.copytree(ROOT / '.agents/profiles', base / '.agents/profiles')
            source = next((ROOT / 'docs/user-stories').glob('*/us-1.1.1-*.md'))
            target = base / source.relative_to(ROOT)
            target.parent.mkdir(parents=True)
            shutil.copy2(source, target)
            workdir, files = module.generate_agent('synthetic-instance', 'junior-backend-engineer',
                'builder', 'sprint-1.1', 'us-1.1.1', 1, custom_workdir=str(base / 'work'))
            self.assertIn('auth_account: auto', (workdir / 'agent.yaml').read_text())
            self.assertIn('Required job context and Spec Kit inputs', (workdir / 'context.md').read_text())
            runner = (workdir / 'run.sh').read_text()
            self.assertIn(str(base / 'scripts/agents/agy_agent.sh'), runner)
            self.assertNotIn('export HOME=', runner)

if __name__ == '__main__':
    unittest.main()
