<!-- BEGIN:c2c-agent-setup-check -->
## Required agent setup check

Antonio requires this setup for everyone using Claude Code or Codex in this repo.

Before edits or commands that change project state, run `python3 scripts/check-agent-setup.py` from the repo root. Read `HOOKS.md` for setup, download sources, and repair steps. If setup is missing or outdated, run `python3 scripts/check-agent-setup.py --install`, then check again. Preserve native hook trust review. Report any failed check; do not claim that installed files prove runtime health. When setup is blocked, continue safe read-only work and report the exact setup gap. Do not repeat this check on every message after it passes unless setup files change.
<!-- END:c2c-agent-setup-check -->
