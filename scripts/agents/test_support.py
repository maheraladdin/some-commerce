"""Disposable source fixtures for launcher tests; no live credentials or provider calls."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]


def make_repository_fixture(target):
    target = Path(target)
    shutil.copytree(ROOT / 'scripts/agents', target / 'scripts/agents', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy2(ROOT / 'scripts/__init__.py', target / 'scripts/__init__.py')
    shutil.copytree(ROOT / '.agents/profiles', target / '.agents/profiles')
    shutil.copytree(ROOT / '.agents/agents', target / '.agents/agents')
    source = next((ROOT / 'docs/user-stories').glob('*/us-1.1.1-*.md'))
    destination = target / source.relative_to(ROOT)
    destination.parent.mkdir(parents=True)
    shutil.copy2(source, destination)
    for account in ('agent-a', 'agent-b', 'agent-c'):
        (target / '.agent_profiles' / account).mkdir(parents=True)
    return target
