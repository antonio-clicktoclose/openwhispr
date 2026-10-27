#!/usr/bin/env python3
"""Refresh team-config through the Codex plugin manager, once per hour per user."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import time

MARKETPLACE = 'antonio-claude-skills'
PLUGIN = 'team-config@' + MARKETPLACE


def refresh(state_dir, runner=subprocess.run, now=None, force=False):
    now = time.time() if now is None else now
    state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (state_dir / 'codex.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'status': 'already-running'}
        receipt = state_dir / 'codex.json'
        try:
            prior = json.loads(receipt.read_text())
        except (OSError, ValueError):
            prior = {}
        if not force and 0 <= now - prior.get('checked_at', 0) < 3600:
            return {'status': 'recently-checked', 'checked_at': prior['checked_at']}
        env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        for args in [
            ['codex', 'plugin', 'marketplace', 'upgrade', MARKETPLACE, '--json'],
            ['codex', 'plugin', 'add', PLUGIN, '--json'],
        ]:
            try:
                result = runner(args, capture_output=True, text=True, timeout=45, env=env)
            except (OSError, subprocess.TimeoutExpired):
                return {'status': 'blocked', 'step': args[2], 'reason': 'CLI unavailable or timed out'}
            if result.returncode:
                # CLI output can contain credential-helper details. Never persist or echo it.
                return {'status': 'blocked', 'step': args[2], 'reason': 'Plugin manager failed; check marketplace registration, GitHub access and workspace trust'}
        data = {'status': 'updated', 'checked_at': now, 'plugin': PLUGIN}
        temporary = receipt.with_suffix('.tmp')
        temporary.write_text(json.dumps(data) + '\n')
        temporary.replace(receipt)
        return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    data = refresh(Path.home() / '.local/share/c2c-team-config-updates', force=args.force)
    print(json.dumps(data))
    if data['status'] == 'blocked':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
