<!-- BEGIN:team-advisor-setup -->
## Business advisor setup for the app in use

Claude Code and Codex work independently. Never require a Claude user to install,
sign into, trust or test Codex. Never require a Codex user to set up Claude.
Use `--app claude` in Claude and `--app codex` in Codex for the setup,
checker and verifier. `--app both` is optional and requires an explicit request.

Check only the current app with `python3 scripts/check_business_advisor_setup.py
--app APP` (replace APP with claude or codex). A missing advisor must not be
reported as lost access to Twilio, dialers, transcripts, Metabase or campaigns.
Check each provider through that person's own approved access. Do not alter
credentials, repo permissions, models or native trust to fix advisor setup.

Read `docs/team-setup-business-advisor-and-obsidian-hooks.md` for setup.
Use the advisor automatically for business questions once the current app is ready.
If advisor setup is incomplete, report that limit. Unrelated provider diagnosis
and recovery can continue; the other app is never a prerequisite.
<!-- END:team-advisor-setup -->

<!-- BEGIN:business-advisor-entry -->
## Required business advisor routing

At the start of each chat, keep `team-config` current without asking the user
or requiring a manual pull. Claude uses the repo marketplace setting
`extraKnownMarketplaces.antonio-claude-skills.autoUpdate: true`.
Codex runs `scripts/update_team_config.py --hook` through the repo's
`.codex/hooks.json` at SessionStart and UserPromptSubmit. The startup hook
loads the installed advisor instructions; the prompt hook keeps routing active.
The updater uses a per-user lock and a one-hour success cache. It checks the
installed package and reports failures. Do not run a second manual check when
the hook already succeeded. Native hook trust is still required once on each
machine. Keep unrelated hooks and trust choices. On macOS the hook uses
`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`; on Linux it
uses Python 3.10 or later. Existing chats may need a reload for new hooks.
Never claim that an update succeeded from a setting alone.

For business advice, use the installed `team-config:antonio-business-advisor`
skill automatically before answering. Read `ADVISOR.md` in this repo. Do not
ask the user whether to query the advisor or wait for a creator name or keyword.
Use the current message and recent chat context. Short follow-ups keep the
business context until the task clearly changes.

Read current evidence for this project first. Then run the installed advisor
reader's `teaching` command with a plain-language description of the business
problem. It uses local semantic search over reviewed public teaching notes.
Read the returned passage and its exact source timestamp. Inspect the linked
frame before making a visual claim. Use only sources that change the answer.
If semantic search fails, use the labelled lexical fallback and state the gap.
Never claim a source was checked when retrieval or access failed.

This applies to offers, ads, funnels, sales, retention, delivery, hiring,
operations, growth and business decisions. Skip unrelated coding, security,
legal, tax, health, trading and personal tasks. Keep client records isolated.
Keep Antonio's voice and current evidence ahead of outside teaching. Do not
imitate a creator, invent certainty or force a source into every answer.
Loading advice does not authorize spending, sending or other external actions.

If the skill or its runtime is missing, follow `ADVISOR.md` to install or update
`team-config` through the existing plugin manager. Report access gaps. Never
copy another user's credentials or edit an installed plugin cache by hand.
<!-- END:business-advisor-entry -->

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
