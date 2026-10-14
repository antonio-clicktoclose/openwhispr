#!/usr/bin/env python3
"""Check the pinned agent setup. Network and writes require --install."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://github.com/antonio-clicktoclose/antonio-claude-skills.git'
FILES = ('install.py', 'execution-context.py', 'policy.md', 'karpathy-guidelines.md',
         'c2c-light-reader.toml', 'c2c-light-reader.md')
TARGETS = {
    'execution-context.py': '.local/share/c2c-agent-policy/execution-context.py',
    'policy.md': '.local/share/c2c-agent-policy/policy.md',
    'karpathy-guidelines.md': '.local/share/c2c-agent-policy/karpathy-guidelines.md',
    'c2c-light-reader.toml': '.codex/agents/c2c-light-reader.toml',
    'c2c-light-reader.md': '.claude/agents/c2c-light-reader.md',
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def manifest():
    data = json.loads((ROOT / '.agent-setup.json').read_text())
    if data.get('source') != SOURCE or not re.fullmatch('[0-9a-f]{40}', data.get('commit', '')):
        raise ValueError('Invalid source or commit in .agent-setup.json')
    if set(data.get('sha256', {})) != set(FILES):
        raise ValueError('Unexpected package file list')
    if any(not re.fullmatch('[0-9a-f]{64}', x) for x in data['sha256'].values()):
        raise ValueError('Invalid package hash')
    return data


def check(home, data):
    errors = []
    for name, rel in TARGETS.items():
        path = home / rel
        if not path.is_file() or digest(path.read_bytes()) != data['sha256'][name]:
            errors.append('Missing or outdated: ' + rel)
    for rel in ('.claude/settings.json', '.claude/settings.local.json'):
        path = ROOT / rel
        if path.exists():
            try:
                if json.loads(path.read_text()).get('disableAllHooks') is True:
                    errors.append('Project disables Claude hooks: ' + rel)
            except (OSError, ValueError, AttributeError):
                errors.append('Invalid project Claude settings: ' + rel)
    expected = 'python3 "' + str(home / TARGETS['execution-context.py']) + '"'
    for rel in ('.codex/hooks.json', '.claude/settings.json'):
        try:
            cfg = json.loads((home / rel).read_text())
            if cfg.get('disableAllHooks') is True:
                errors.append('Hooks disabled in ' + rel)
            hooks = cfg.get('hooks', {})
            for event in ('SessionStart', 'SubagentStart'):
                matches = [(g, h) for g in hooks.get(event, []) for h in g.get('hooks', [])
                           if h.get('command') == expected]
                if len(matches) != 1 or matches[0][0].get('matcher') not in (None, '', '*'):
                    errors.append('Missing, duplicate, or restricted ' + event + ' hook: ' + rel)
            for groups in hooks.values():
                if any('jev-routing-context.py' in h.get('command', '')
                       for g in groups for h in g.get('hooks', [])):
                    errors.append('Old Jev hook remains in ' + rel)
        except (OSError, ValueError, TypeError, AttributeError):
            errors.append('Missing or invalid hook file: ' + rel)
    for rel in ('.codex/AGENTS.md', '.claude/CLAUDE.md'):
        try:
            text = (home / rel).read_text()
            policy = (home / TARGETS['policy.md']).read_text()
            if '<!-- BEGIN:c2c-execution-policy -->' not in text or policy not in text:
                errors.append('Missing shared execution rules: ' + rel)
            if '<!-- BEGIN:jev-decision-routing -->' in text:
                errors.append('Old Jev instructions remain: ' + rel)
        except OSError:
            errors.append('Missing shared execution rules: ' + rel)
    override = home / '.codex/AGENTS.override.md'
    if override.exists() and override.read_text().strip():
        errors.append('Codex AGENTS.override.md hides the shared user rules; review it manually')
    if (home / '.codex/tools/jev-router/router.py').exists():
        errors.append('Old Jev entry point is still active')
    return errors


def install(home, data):
    if not shutil.which('git'):
        raise RuntimeError('Git is required. Install Git, then run this command again.')
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    with tempfile.TemporaryDirectory(prefix='c2c-agent-setup-') as tmp:
        def git(*args):
            result = subprocess.run(['git', '-C', tmp, *args], capture_output=True, env=env, timeout=180)
            if result.returncode:
                raise RuntimeError('Cannot fetch the approved package. Check GitHub access to antonio-clicktoclose/antonio-claude-skills. No credentials were printed.')
            return result.stdout
        git('init', '-q')
        git('fetch', '--quiet', '--depth=1', SOURCE, data['commit'])
        if git('rev-parse', 'FETCH_HEAD').decode().strip() != data['commit']:
            raise RuntimeError('Downloaded commit does not match the approved version')
        package = Path(tmp) / 'package'
        package.mkdir()
        # Verify every file before executing any downloaded code.
        for name in FILES:
            content = git('show', data['commit'] + ':plugins/team-config/runtime/' + name)
            if digest(content) != data['sha256'][name]:
                raise RuntimeError('Package checksum failed: ' + name)
            (package / name).write_bytes(content)
        result = subprocess.run([sys.executable, str(package / 'install.py'), '--home', str(home)],
                                capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise RuntimeError('Installer failed. Review the local config files; no trust settings were changed by this checker.')
        receipt = json.loads(result.stdout)
        print('Installer changed %s files. Backups: %s' % (len(receipt['changed']), receipt['backup_root']))


def codex_trust(cwd):
    """Ask the installed client which hooks it will accept; never edit trust."""
    if not shutil.which('codex'):
        return False, 'Codex CLI is not on PATH; use /hooks in Codex to check trust.'
    proc = subprocess.Popen(['codex', 'app-server', '--stdio'], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    messages = queue.Queue()
    def read():
        for line in proc.stdout:
            try:
                messages.put(json.loads(line))
            except ValueError:
                pass
        messages.put({'closed': True})
    threading.Thread(target=read, daemon=True).start()
    def call(i, method, params):
        proc.stdin.write(json.dumps({'id': i, 'method': method, 'params': params}) + '\n')
        proc.stdin.flush()
        import time
        until = time.monotonic() + 20
        while time.monotonic() < until:
            msg = messages.get(timeout=max(.01, until-time.monotonic()))
            if msg.get('closed'):
                raise RuntimeError('Codex closed before replying')
            if msg.get('id') == i:
                if 'error' in msg:
                    raise RuntimeError('Hook inspection is not supported by this Codex version')
                return msg.get('result', {})
        raise RuntimeError('Codex hook inspection timed out')
    try:
        call(1, 'initialize', {'clientInfo': {'name': 'c2c-setup-check', 'version': '1.0'},
                               'capabilities': {'experimentalApi': True}})
        proc.stdin.write('{"method":"initialized","params":{}}\n'); proc.stdin.flush()
        result = call(2, 'hooks/list', {'cwds': [str(cwd)]})
        rows = result.get('data', [])
        hooks = [h for row in rows for h in row.get('hooks', [])
                 if 'c2c-agent-policy/execution-context.py' in json.dumps(h)]
        errors = any(row.get('errors') for row in rows)
        okay = (not errors and len(hooks) == 2 and
                {h.get('eventName') for h in hooks} == {'sessionStart', 'subagentStart'} and
                all(h.get('enabled') and h.get('trustStatus') == 'trusted' for h in hooks))
        return okay, ('Codex reports both hooks enabled and trusted.' if okay else
                      'Codex hooks need review or are disabled. Open /hooks and review them.')
    except (OSError, RuntimeError, queue.Empty, BrokenPipeError):
        return False, 'Could not verify Codex hook trust. Open /hooks or update the Codex CLI.'
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill(); proc.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true', help='Fetch, verify, and install the pinned package')
    args = parser.parse_args()
    print('REQUIRED SETUP REQUESTED BY ANTONIO')
    print('Everyone using Claude Code or Codex in this repo must complete this setup before coding.')
    try:
        data = manifest()
        home = Path.home()
        for var, standard in [('CODEX_HOME', home/'.codex'), ('CLAUDE_CONFIG_DIR', home/'.claude')]:
            if os.environ.get(var) and Path(os.environ[var]).expanduser().resolve() != standard.resolve():
                raise RuntimeError(var + ' uses a custom location. This installer supports standard user locations only.')
        if args.install:
            install(home, data)
        errors = check(home, data)
        if errors:
            print('SETUP INCOMPLETE')
            for error in errors:
                print('- ' + error)
            print('Repair files: python3 scripts/check-agent-setup.py --install')
            print('Disabled hooks or instruction overrides need review in the client; see HOOKS.md.')
            return 1
        print('PINNED FILES AND USER SETTINGS: PASS (' + data['version'] + ')')
        trusted, message = codex_trust(ROOT)
        print(message)
        print('CLAUDE RUNTIME: not verified by this check. Start a fresh session and inspect /hooks.')
        print('This check does not prove model behavior or a completed task.')
        return 0 if trusted else 2
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print('SETUP CHECK FAILED: ' + str(exc))
        return 1


if __name__ == '__main__':
    sys.exit(main())
