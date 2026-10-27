#!/usr/bin/env python3
"""Refresh team-config through the Codex plugin manager, once per hour per user."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
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
        if not force and prior.get('installed_path') and 0 <= now - prior.get('checked_at', 0) < 3600:
            return dict(prior, status='recently-checked')
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
        try:
            installed = json.loads(result.stdout)
            path = Path(installed['installedPath']).resolve()
            manifest = json.loads((path / '.claude-plugin/plugin.json').read_text())
            if installed['pluginId'] != PLUGIN or manifest['name'] != 'team-config' or manifest['version'] != installed['version']:
                raise ValueError('Plugin identity mismatch')
            if not (path / 'skills/antonio-business-advisor/SKILL.md').is_file():
                raise ValueError('Advisor missing')
        except (OSError, ValueError, KeyError, TypeError):
            return {'status': 'blocked', 'reason': 'Plugin manager install readback failed'}
        data = {'status': 'updated', 'checked_at': now, 'plugin': PLUGIN,
                'installed_path': str(path), 'version': installed['version']}
        temporary = receipt.with_suffix('.tmp')
        temporary.write_text(json.dumps(data) + '\n')
        temporary.replace(receipt)
        return data


def hook(state_dir, event, result):
    """Load the installed skill as hook context. Never store the prompt."""
    event_name = event.get('hook_event_name', 'SessionStart')
    if event_name not in ('SessionStart', 'UserPromptSubmit'):
        raise ValueError('Unsupported hook event')
    context = 'Team-config update check: ' + result['status'] + '. '
    skill = Path(result.get('installed_path', '')) / 'skills/antonio-business-advisor/SKILL.md'
    loaded = False
    if result['status'] in ('updated', 'recently-checked') and skill.is_file():
        context += 'Installed advisor: ' + str(skill) + '. '
        if event_name == 'SessionStart':
            context += ('Business advisor loaded automatically by the Codex startup hook. '
                        'Apply it only to relevant business conversations. Resolve relative '
                        'source paths against this skill directory. Use the reader by absolute '
                        'path: ' + str(skill.parent / 'scripts/business_advisor.py') +
                        '. The current request may be unrelated; do not force advice into it.\n\n' + skill.read_text())
        else:
            context += ('For business advice, infer the problem from this chat and query the '
                        'installed teaching reader automatically. Check exact timestamps and '
                        'frames. Skip unrelated work. Never ask whether to query the advisor.')
        loaded = True
    else:
        context += ('Advisor was not loaded by this hook. Report the update or access gap; '
                    'do not claim automatic advisor setup succeeded.')
    receipt = {'event': event_name, 'at': time.time(), 'update_status': result['status'],
               'advisor_loaded': loaded, 'version': result.get('version'),
               'skill_sha256': hashlib.sha256(skill.read_bytes()).hexdigest() if loaded else None}
    with (state_dir / 'hook-runs.jsonl').open('a') as stream:
        stream.write(json.dumps(receipt) + '\n')
    return {'hookSpecificOutput': {'hookEventName': event_name, 'additionalContext': context}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--hook', action='store_true')
    args = parser.parse_args()
    data = refresh(Path.home() / '.local/share/c2c-team-config-updates', force=args.force)
    if args.hook:
        event = json.load(sys.stdin)
        print(json.dumps(hook(Path.home() / '.local/share/c2c-team-config-updates', event, data)))
    else:
        print(json.dumps(data))
    if data['status'] == 'blocked':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
