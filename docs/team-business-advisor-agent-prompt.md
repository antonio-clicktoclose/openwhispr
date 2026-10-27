# Prompt for a teammate's Claude Code or Codex agent

Copy the block below into the agent chat while working in a team repo:

```text
Before working on my request, check this machine's required team setup.

Run `python3 scripts/check_business_advisor_setup.py`. Continue only if it exits 0 and reports `ordinary_work_allowed: true`.

If the checker is missing or fails, pause my original request and do setup work only. Read `docs/team-setup-business-advisor-and-obsidian-hooks.md`, then run `python3 scripts/setup_business_advisor.py` as needed. If these files are missing, fetch the reviewed setup files from this repo without overwriting unrelated work.

Use my own existing GitHub and approved Obsidian access. Keep repo permissions, credentials, model settings and unrelated hooks unchanged. Do not copy anyone else's token or bypass native hook trust. Ask me to complete any required app login or Codex /hooks review.

Finish the fresh-session and training-reference checks in both Claude Code and Codex. Confirm automatic advisor loading in a repo and a local non-Git folder. Test a normal business question without naming an advisor or creator. Check the returned timestamps and linked frame files against the live reviewed notes. Keep raw logs private.

Rerun the machine check. Report the result, installed versions and any exact blocker. Resume my original request only after the check passes. Do not call setup complete from an enabled setting, a package install or a copied receipt alone.
```

The gate guides agent behavior. It cannot stop someone from disabling instructions or hooks. Each machine needs its own setup and checks.
