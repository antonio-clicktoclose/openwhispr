# Team setup: automatic business advisor in Claude and Codex

Run this once from a current team repo checkout:

```bash
python3 scripts/setup_business_advisor.py
```

If your checkout does not have that script yet, run this from any local folder. It uses your own GitHub CLI login and fetches a pinned launcher:

```bash
setup_file="$(mktemp)" && \
gh api 'repos/antonio-clicktoclose/antonio-claude-skills/contents/scripts/setup_business_advisor.py?ref=f21f076f535b636c035228d8622f77dab896f459' --jq '.content | @base64d' > "$setup_file" && \
python3 "$setup_file"
```

The command fetches a pinned, reviewed setup from the private skills repo. It installs user hooks for both Claude Code and Codex, turns on plugin updates and runs checks. The user hooks cover repos and local folders, including folders without Git. For business questions, the advisor uses the chat context and searches reviewed training without a keyword or manual skill request.

## Before setup

- Install both Claude Code and Codex and sign in through their normal login flows.
- Use your own existing GitHub access to `antonio-clicktoclose/antonio-claude-skills`. Setup does not grant access. A missing grant remains blocked.
- On macOS, install python.org Python 3.13 at `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`. Linux needs Python 3.10 or later. Windows and custom app config folders are not supported by this installer.
- Use your own approved Obsidian connection. Do not share Antonio's service-account token or copy another person's credentials. If the shared notes cannot be read, retrieval stays incomplete.

## One-time trust and checks

Codex requires a person to review new hook definitions in `/hooks`. Setup does not grant trust or change workspace trust. If the first test reports missing trust, review those hooks in Codex, then run the installed check:

```bash
# macOS
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 ~/.local/share/c2c-team-config-updates/verify.py
```

```bash
# Linux
python3 ~/.local/share/c2c-team-config-updates/verify.py
```

The check uses the person's normal account credits and keeps their selected model. It tests fresh sessions in the current folder and a new non-Git folder. Both apps must load the advisor from a native hook. An ordinary sales question must then trigger a semantic teaching query. The test checks the cited video timestamp against the live source note and fetches its linked JPEG. A JPEG check does not prove visual review.

Read the local result at `~/.local/share/c2c-team-config-updates/acceptance.json`. A machine counts as tested only when `status` is `verified`. The raw logs stay private on that machine. An incomplete result names the failed checks. Do not share raw logs or credentials in team chats.

## Updates and limits

At startup and on each prompt, the hooks check team-config through the native plugin manager. They reuse a successful check for one hour. No manual pull is needed after setup. Existing chats may need a reload. Disabled hooks, missing repo access, expired sign-in and missing Obsidian access remain visible gaps.

Setup backs up changed settings under `~/.local/share/c2c-team-config-updates/backups/`. It preserves other hooks, model settings, credentials and trust choices. Repo permissions remain unchanged. Private book skills may need their own existing library access; reviewed public training does not replace missing books.

This setup covers Claude Code and Codex. It does not claim support for ordinary Claude Desktop chats or Cowork. Each person must run it on each machine. Antonio's successful tests do not prove another computer works.

## Required check before work

Both `AGENTS.md` and `CLAUDE.md` require the agent to run:

```bash
python3 scripts/check_business_advisor_setup.py
```

Exit code 0 and `ordinary_work_allowed: true` allow normal work. Any other result means setup-only mode. The agent must pause the original request and repair setup first. A missing checker also means setup-only mode.

The read-only check verifies both install records, advisor files, user hook definitions, automatic-update settings, passed native tests, current skill load evidence, source checks, app sign-in and native Codex hook trust. It calls no model and changes no settings. A missing login or trust choice needs the person to act. Setup cannot approve trust or grant repo access.

The installer also adds the gate to the user's global Claude and Codex instruction files. In a local folder without a repo, the checker lives at `~/.local/share/c2c-team-config-updates/check_business_advisor_setup.py`.

Use [the ready-to-copy agent prompt](team-business-advisor-agent-prompt.md) for a teammate's setup chat. This is an instruction gate, not an OS security boundary. A person can still disable instructions or hooks.
