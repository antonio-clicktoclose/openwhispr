<!-- BEGIN:shared-slack-communication -->
## Shared Slack communication guide

Before drafting or editing Slack messages, read the shared guide: https://obsidian.clicktoclose.ai/C2C/Processes/Slack-Communication-Guidelines. Use the Obsidian API when available. Canonical GitHub copy: https://github.com/antonio-clicktoclose/c2c-monorepo/blob/main/docs/slack-communication-guidelines.md. On Antonio's Mac, the local copy is `/Users/antoniomonteiro/Developer/Coding Projects/C2C System Monorepo/docs/slack-communication-guidelines.md`.

Apply its tone, owner requests, estimate labels and review checks to the active client. Preserve the user's wording and each project's specific channels, reviewers, Slack formatting tools and send permissions. Do not copy another client's people or facts. For PG, also read `slackmessage.md`. Reading this guide or preparing a draft does not authorize sending.
<!-- END:shared-slack-communication -->

<!-- BEGIN:c2c-agent-setup-check -->
## Required agent setup check

Antonio requires this setup for everyone using Claude Code or Codex in this repo.

Before edits or commands that change project state, run `python3 scripts/check-agent-setup.py` from the repo root. Read `HOOKS.md` for setup, download sources, and repair steps. If setup is missing or outdated, run `python3 scripts/check-agent-setup.py --install`, then check again. Preserve native hook trust review. Report any failed check; do not claim that installed files prove runtime health. When setup is blocked, continue safe read-only work and report the exact setup gap. Do not repeat this check on every message after it passes unless setup files change.
<!-- END:c2c-agent-setup-check -->
