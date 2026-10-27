# Business advisor setup for Claude Code or Codex

Use only the app you work in. Claude does not require Codex. Codex does not require Claude. Their installs, logins, native trust and acceptance tests are separate. Repo permissions stay unchanged.

From a current team checkout, run one command:

```bash
# Claude Code
python3 scripts/setup_business_advisor.py --app claude
# Codex
python3 scripts/setup_business_advisor.py --app codex
```

Use `--app both` only when you choose to set up both apps. On macOS the launcher uses the signed python.org Python 3.13 interpreter. Linux needs Python 3.10 or later. Use your own existing GitHub and Obsidian access. Setup cannot grant access or native trust.

The setup installs and updates team-config through the chosen app's plugin manager. It preserves unrelated settings, hooks and models. Its user hooks cover repos and plain local folders. An existing chat may need a reload to read updated instructions.

Run the installed verifier with `--app claude` or `--app codex`. Tests use normal account credits. They check native loading in a repo and a plain folder, automatic teaching search, source timestamps and linked frame files. A fetched frame is not proof that a person viewed it. Results for a single app are saved in `~/.local/share/c2c-team-config-updates/acceptance-APP.json`.

The machine checker also accepts `--app claude` or `--app codex`. It checks only that app. The other CLI may be absent, signed out or untrusted. Missing advisor setup does not prove loss of provider credentials. Continue provider diagnosis through the user's own approved access and state the advisor gap separately.

This supports Claude Code and Codex, not ordinary Claude Desktop chats or Cowork. Setup must run once per user and machine. A passed test on Antonio's Mac does not prove a teammate's machine works.

See [the copy-ready prompt](team-business-advisor-agent-prompt.md) for setup from any folder.
