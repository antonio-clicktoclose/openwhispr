#!/usr/bin/env python3
"""Read-only machine setup gate. Exit 0 allows work; exit 1 allows setup only."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import queue
import threading
import sys

PLUGIN='team-config@antonio-claude-skills'


def read(path):
    return json.loads(path.read_text())


def check(home):
    errors=[]
    base=home/'.local/share/c2c-team-config-updates'
    def require(condition,message):
        if not condition:errors.append(message)
    try:
        receipt=read(base/'acceptance.json')
        require(receipt.get('status')=='verified','Local acceptance tests have not passed.')
        require((base/'acceptance.json').stat().st_uid==os.getuid(),'Acceptance receipt belongs to another OS user.')
        for app,helper in [('claude','claude_business_advisor_hook.py'),('codex','update_team_config.py')]:
            require((base/helper).is_file(),app+' updater is missing.')
            settings=read(home/('.'+app)/('settings.json' if app=='claude' else 'hooks.json'))
            require(not settings.get('disableAllHooks'),app+' hooks are disabled.')
            for event in ['SessionStart','UserPromptSubmit']:
                matches=[h for g in settings.get('hooks',{}).get(event,[]) for h in g.get('hooks',[]) if helper in h.get('command','')]
                require(len(matches)==1,app+' needs exactly one '+event+' advisor hook.')
                if len(matches)==1:
                    parts=shlex.split(matches[0]['command'])
                    require(matches[0].get('type')=='command' and len(parts)==(3 if app=='codex' else 2) and parts[1]==str(base/helper) and (app!='codex' or parts[2]=='--hook'),app+' hook points to an unexpected helper.')
            if app=='claude':
                entries=read(home/'.claude/plugins/installed_plugins.json')['plugins'][PLUGIN]
                entry=next(e for e in entries if e.get('scope')=='user')
                package=Path(entry['installPath']);version=entry['version']
                require(settings.get('enabledPlugins',{}).get(PLUGIN) is True,'Claude team-config is disabled.')
                require(settings.get('extraKnownMarketplaces',{}).get('antonio-claude-skills',{}).get('autoUpdate') is True,'Claude marketplace updates are disabled.')
                log=base/'claude/hook-runs.jsonl'
            else:
                entry=read(base/'codex.json');package=Path(entry['installed_path']);version=entry['version'];log=base/'hook-runs.jsonl'
            manifest=read(package/'.claude-plugin/plugin.json')
            require(manifest.get('name')=='team-config' and manifest.get('version')==version,app+' package identity does not match its install record.')
            skill=package/'skills/antonio-business-advisor/SKILL.md'
            require((skill.parent/'scripts/business_advisor.py').is_file(),app+' teaching reader is missing.')
            digest=hashlib.sha256(skill.read_bytes()).hexdigest()
            tests=[r for r in receipt.get('tests',[]) if r.get('app')==app]
            require({r.get('case') for r in tests if r.get('verified')}=={'repo-load','folder-load','automatic-business-query'},app+' needs all three native acceptance tests.')
            require(any(c.get('app')==app and c.get('verified') and c.get('answer_reference_verified') for c in receipt.get('source_checks',[])),app+' timestamp and frame checks have not passed.')
            runs=[json.loads(line) for line in log.read_text().splitlines() if line.strip()]
            for test in tests:
                require(any(r.get('event')=='SessionStart' and r.get('advisor_loaded') and r.get('skill_sha256')==digest and Path(r.get('cwd','.')).resolve()==Path(test['cwd']).resolve() for r in runs),app+' current skill lacks native load evidence for '+test.get('case','unknown')+'.')
    except (OSError,ValueError,KeyError,StopIteration,TypeError,IndexError):
        errors.append('A required setup file, install record or test receipt is missing or invalid.')
    return {'status':'ready' if not errors else 'setup-only','ordinary_work_allowed':not errors,'problems':errors,
            'next_action':None if not errors else 'Read the team setup guide, run scripts/setup_business_advisor.py, review native hook trust and rerun the tests. Do only setup work until this check passes.',
            'scope':'Instruction gate based on local evidence. It does not prevent a person from disabling instructions or hooks.'}


def native_problems(cwd):
    problems=[]
    try:
        auth=subprocess.run(['claude','auth','status'],capture_output=True,text=True,timeout=20)
        if auth.returncode or not json.loads(auth.stdout).get('loggedIn'):problems.append('Claude Code needs its normal account login.')
        auth=subprocess.run(['codex','login','status'],capture_output=True,text=True,timeout=20)
        if auth.returncode:problems.append('Codex needs its normal account login.')
        process=subprocess.Popen(['codex','app-server','--stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
        messages=queue.Queue()
        def reader():
            for line in process.stdout:
                try:messages.put(json.loads(line))
                except ValueError:pass
        threading.Thread(target=reader,daemon=True).start()
        def call(number,method,params):
            process.stdin.write(json.dumps({'id':number,'method':method,'params':params})+'\n');process.stdin.flush()
            while True:
                response=messages.get(timeout=20)
                if response.get('id')==number:
                    if 'error' in response:raise ValueError('Native hook check failed')
                    return response['result']
        try:
            call(1,'initialize',{'clientInfo':{'name':'c2c-machine-setup-gate','version':'1'},'capabilities':{'experimentalApi':True}})
            process.stdin.write('{"method":"initialized","params":{}}\n');process.stdin.flush()
            rows=call(2,'hooks/list',{'cwds':[str(cwd)]})['data']
            hooks=[h for row in rows for h in row.get('hooks',[]) if 'c2c-team-config-updates/update_team_config.py' in h.get('command','')]
            if len(hooks)!=2 or {h.get('eventName') for h in hooks}!={'sessionStart','userPromptSubmit'} or not all(h.get('enabled') and h.get('trustStatus')=='trusted' for h in hooks):
                problems.append('Review and enable the advisor user hooks in Codex /hooks. Setup cannot grant native trust.')
        finally:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait()
    except (OSError,ValueError,KeyError,subprocess.TimeoutExpired,queue.Empty):
        problems.append('Native login or hook checks could not be verified. Repair the app setup first.')
    return problems


if __name__=='__main__':
    if sys.platform=='darwin':
        signed=Path('/Library/Frameworks/Python.framework/Versions/3.13/bin/python3')
        if not signed.is_file():
            print('SETUP ONLY: Install python.org Python 3.13 first.');raise SystemExit(1)
        if Path(sys.executable).resolve()!=signed.resolve():os.execv(str(signed),[str(signed),str(Path(__file__).resolve())])
    result=check(Path.home())
    if result['ordinary_work_allowed']:
        result['problems'].extend(native_problems(Path.cwd()))
        if result['problems']:result.update(status='setup-only',ordinary_work_allowed=False,next_action='Repair login or native hook trust, then rerun this check. Do only setup work until it passes.')
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['ordinary_work_allowed'] else 1)
