# Setup prompt for either Claude Code or Codex

Paste this into the app you use, from any local folder:

```text
Set up the shared business advisor for THIS app only. If you are Claude Code, use --app claude. If you are Codex, use --app codex. Do not install, sign into, trust or test the other app. Do not change repo permissions, credentials, models, unrelated hooks or native trust.

Use my own existing GitHub and Obsidian access. Fetch https://github.com/antonio-clicktoclose/antonio-claude-skills.git into a new temporary folder. Check out reviewed commit 7164e4771f9053d786b7a5356d296e0433f6c596 and verify HEAD exactly before running code. Leave my current folder unchanged.

Use python.org Python 3.13 at /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 on macOS, or Python 3.10 or later on Linux. Run plugins/team-config/runtime/advisor/setup.py --app APP from the temporary checkout, replacing APP with this app. Ask me to complete any required login or native hook review in this app. Never approve trust yourself.

Then run ~/.local/share/c2c-team-config-updates/verify.py --app APP from that checkout. Verify native advisor loading in the repo and a plain local folder. Test an ordinary business question and check its training timestamps and linked frames against the live notes. Report any untested limit. Keep raw logs private.

Run ~/.local/share/c2c-team-config-updates/check_business_advisor_setup.py --app APP. Report the chosen app, installed version, test results and exact blockers. The other app is never a prerequisite. A missing advisor must not be called lost access to business providers. Provider diagnosis can continue through my approved access while advisor setup is repaired.
```
