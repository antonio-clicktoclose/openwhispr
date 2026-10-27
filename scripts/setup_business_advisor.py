#!/usr/bin/env python3
"""Fetch the reviewed private advisor setup using this person's existing Git access."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

REPO='https://github.com/antonio-clicktoclose/antonio-claude-skills.git'
COMMIT='c956fe9b9b9d3525aadae132ec849164c7d60164'
MAC_PYTHON='/Library/Frameworks/Python.framework/Versions/3.13/bin/python3'


def main():
    python=sys.executable
    if sys.platform=='darwin':
        python=MAC_PYTHON
        if not Path(python).is_file():
            raise RuntimeError('Install python.org Python 3.13 first. The signed Mac runtime is required.')
        if Path(sys.executable).resolve()!=Path(python).resolve():
            os.execv(python,[python,str(Path(__file__).resolve()),*sys.argv[1:]])
    elif not sys.platform.startswith('linux') or sys.version_info<(3,10):
        raise RuntimeError('This setup supports macOS and Linux with Python 3.10 or later.')
    with tempfile.TemporaryDirectory(prefix='c2c-team-advisor-setup-') as folder:
        for command in [['git','init','-q',folder],['git','-C',folder,'fetch','--depth','1',REPO,COMMIT],['git','-C',folder,'checkout','--detach','FETCH_HEAD']]:
            result=subprocess.run(command,capture_output=True,text=True,timeout=120,env=dict(os.environ,GIT_TERMINAL_PROMPT='0'))
            if result.returncode:
                raise RuntimeError('Cannot fetch the reviewed private setup. Check your existing GitHub access. No repo permissions were changed.')
        actual=subprocess.check_output(['git','-C',folder,'rev-parse','HEAD'],text=True).strip()
        if actual!=COMMIT:raise RuntimeError('Setup commit did not match the reviewed pin.')
        return subprocess.call([python,str(Path(folder)/'plugins/team-config/runtime/advisor/setup.py'),'--verify'])


if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,RuntimeError,subprocess.TimeoutExpired) as error:
        print(str(error),file=sys.stderr);raise SystemExit(1)
