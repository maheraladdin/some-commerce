#!/usr/bin/env python3
"""Local account usage allocator. Estimates are not provider quota telemetry."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import argparse
from contextlib import contextmanager
import fcntl
import json
import math
import os
import signal
import socket
import subprocess
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
ACCOUNTS = ('agent-a', 'agent-b', 'agent-c')


class Pool:
    def __init__(self, directory=None):
        self.directory = Path(directory or ROOT / '.agent_profiles')

    @contextmanager
    def state(self):
        self.directory.mkdir(parents=True, exist_ok=True)
        with (self.directory / 'quota.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            path = self.directory / 'quota.json'
            data = json.loads(path.read_text()) if path.exists() else {'version': 1, 'accounts': {}, 'reservations': {}}
            if data.get('version') != 1 or not isinstance(data.get('reservations'), dict):
                raise ValueError('Invalid quota ledger; refusing to reset it')
            for account in ACCOUNTS:
                row = data['accounts'].setdefault(account, {'used': 0, 'budget': None, 'weight': 1,
                    'enabled': True, 'cooldown_until': 0, 'max_concurrency': 1, 'last_selected': 0})
                for key in ('used', 'weight', 'cooldown_until', 'last_selected'):
                    value = row[key]
                    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                        raise ValueError('Invalid account numeric value')
                if row['weight'] <= 0 or not isinstance(row['enabled'], bool) or type(row['max_concurrency']) is not int or row['max_concurrency'] < 1:
                    raise ValueError('Invalid account configuration')
                if row['budget'] is not None and (type(row['budget']) not in (int, float) or not math.isfinite(row['budget']) or row['budget'] < 0):
                    raise ValueError('Invalid budget')
            yield data
            temp = self.directory / ('quota-' + uuid.uuid4().hex + '.tmp')
            try:
                with temp.open('x') as output:
                    json.dump(data, output, indent=2)
                    output.flush()
                    os.fsync(output.fileno())
                temp.replace(path)
            finally:
                if temp.exists():
                    temp.unlink()

    def reserve(self, role, account='auto', units=1):
        if account != 'auto' and account not in ACCOUNTS:
            raise ValueError('Unknown account')
        if not math.isfinite(units) or units <= 0:
            raise ValueError('Estimated units must be positive and finite')
        with self.state() as data:
            choices = []
            for name in ACCOUNTS:
                row = data['accounts'][name]
                active = [r for r in data['reservations'].values() if r['account'] == name]
                reserved = sum(r['units'] for r in active)
                if account not in ('auto', name) or not (self.directory / name).is_dir():
                    continue
                if not row['enabled'] or row['cooldown_until'] > time.time() or len(active) >= row['max_concurrency']:
                    continue
                if row['budget'] is not None and row['used'] + reserved + units > row['budget']:
                    continue
                denominator = row['budget'] if row['budget'] is not None else row['weight']
                if denominator <= 0:
                    continue
                score = (row['used'] + reserved) / denominator
                choices.append((score, len(active), row['last_selected'], name))
            if not choices:
                raise ValueError('No account available: initialized pools are busy, disabled, cooling down or over budget. No task was launched.')
            name = min(choices)[-1]
            token = uuid.uuid4().hex
            data['accounts'][name]['last_selected'] = time.time()
            data['reservations'][token] = {'account': name, 'role': role, 'units': units,
                'owner_pid': os.getpid(), 'host': socket.gethostname(), 'child_pid': None, 'started_at': time.time()}
            return name, token

    def finish(self, token):
        with self.state() as data:
            reservation = data['reservations'].pop(token, None)
            if reservation:
                data['accounts'][reservation['account']]['used'] += reservation['units']

    def configure(self, account, **settings):
        if account not in ACCOUNTS:
            raise ValueError('Unknown account')
        with self.state() as data:
            row = data['accounts'][account]
            for key, value in settings.items():
                if key not in ('budget', 'weight', 'max_concurrency', 'enabled', 'cooldown_until', 'used'):
                    raise ValueError('Unknown setting')
                if key in ('budget', 'weight', 'max_concurrency', 'cooldown_until', 'used') and value is not None:
                    if not math.isfinite(value) or value < 0 or (key in ('weight', 'max_concurrency') and value <= 0):
                        raise ValueError('Invalid numeric setting')
                row[key] = value

    def recover(self):
        """Only clear local reservations whose owner process is known dead."""
        with self.state() as data:
            dead = []
            for token, row in data['reservations'].items():
                if row['host'] != socket.gethostname():
                    continue
                if row.get('child_pid') is None:
                    continue  # Ambiguous crash before spawn acknowledgment needs manual reconciliation.
                try:
                    os.kill(row['child_pid'], 0)
                except ProcessLookupError:
                    pass
                except PermissionError:
                    continue
                else:
                    continue
                try:
                    os.kill(row['owner_pid'], 0)
                except ProcessLookupError:
                    dead.append(token)
                except PermissionError:
                    pass
            for token in dead:
                row = data['reservations'].pop(token)
                data['accounts'][row['account']]['used'] += row['units']
            return len(dead)


def run(pool, args):
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        raise ValueError('A command is required')
    account, token = pool.reserve(args.role, args.account, args.units)
    env = os.environ.copy()
    env['AGENT_POOL_ACCOUNT'] = account
    env['AGENT_POOL_RESERVATION'] = token
    print(f'Quota pool selected {account} for {args.role}; estimated units={args.units}', file=sys.stderr)
    process = None
    old_handler = signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        process = subprocess.Popen(command, env=env)
        with pool.state() as data:
            data['reservations'][token]['child_pid'] = process.pid
        return process.wait()
    except KeyboardInterrupt:
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        return 130
    finally:
        signal.signal(signal.SIGTERM, old_handler)
        pool.finish(token)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', type=Path, help='Override ledger/auth directory for isolated tests')
    commands = parser.add_subparsers(dest='operation', required=True)
    launch = commands.add_parser('run')
    launch.add_argument('--role', required=True)
    launch.add_argument('--account', choices=('auto',) + ACCOUNTS, default='auto')
    launch.add_argument('--units', type=float, default=1)
    launch.add_argument('command', nargs=argparse.REMAINDER)
    commands.add_parser('status')
    commands.add_parser('recover')
    config = commands.add_parser('configure')
    config.add_argument('account', choices=ACCOUNTS)
    config.add_argument('--budget', type=float)
    config.add_argument('--clear-budget', action='store_true')
    config.add_argument('--weight', type=float)
    config.add_argument('--max-concurrency', type=int)
    config.add_argument('--cooldown-seconds', type=float)
    config.add_argument('--enabled', choices=('yes', 'no'))
    config.add_argument('--used', type=float, help='Set usage from operator/provider evidence; use zero when the actual quota resets')
    args = parser.parse_args(argv)
    pool = Pool(args.state_dir)
    try:
        if args.operation == 'run':
            result = run(pool, args)
            return result if result >= 0 else 128 - result
        if args.operation == 'status':
            with pool.state() as data:
                print(json.dumps(data, indent=2))
        elif args.operation == 'recover':
            print(f'Recovered {pool.recover()} dead local reservations')
        else:
            settings = {key: getattr(args, key) for key in ('budget', 'weight', 'max_concurrency', 'used') if getattr(args, key) is not None}
            if args.clear_budget:
                settings['budget'] = None
            if args.enabled is not None:
                settings['enabled'] = args.enabled == 'yes'
            if args.cooldown_seconds is not None:
                if not math.isfinite(args.cooldown_seconds) or args.cooldown_seconds < 0:
                    raise ValueError('Cooldown must be finite and non-negative')
                settings['cooldown_until'] = time.time() + args.cooldown_seconds
            pool.configure(args.account, **settings)
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Account allocation failed: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
