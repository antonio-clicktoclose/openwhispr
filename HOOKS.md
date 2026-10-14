# Check your Claude and Codex setup

Run this from the repo root before agent work:

```bash
python3 scripts/check-agent-setup.py
```

If setup is missing or outdated, run:

```bash
python3 scripts/check-agent-setup.py --install
```

The install command downloads one approved commit, checks every file against its SHA-256 hash, and then runs the installer. It needs Python 3, Git, and GitHub read access to [antonio-claude-skills](https://github.com/antonio-clicktoclose/antonio-claude-skills). It uses your existing Git login. If access fails, ask the repo owner for access; do not paste a token into a command or chat.

The source commit and file hashes are in `.agent-setup.json`. No moving branch or unverified download is executed. The installer backs up changed files and keeps unrelated settings and your main model. Run it again safely to repair drift. It installs both client profiles even if you currently use only one client.

## Finish setup

1. In Codex, open `/hooks` and review any new or changed hook definitions. The installer cannot grant trust. Run the check again after review.
2. Start a fresh Claude or Codex session. Existing chats may retain old guidance.
3. In Claude, inspect `/hooks` for the shared `SessionStart` and `SubagentStart` entries. A user-file check cannot prove that managed or project settings allow them to run.

Exit code `0` means the pinned files and user settings match, and the Codex CLI reports both hooks enabled and trusted for this repo. It does not prove that Claude ran them or that either model follows every rule. Exit code `1` means setup is missing, outdated, invalid, or could not be installed. Exit code `2` means the files match but Codex trust could not be verified, including when the CLI is absent. Follow the printed repair step. Disabled hooks and instruction overrides need manual review; reinstalling does not remove them. Do not report full runtime health from a file check.

This setup uses all five local Karpathy sections, full-request checks, and evidence-based pushback. Jev stays disabled. Exact searches and checks use code. A narrow, independent reading task may use `c2c-light-reader`: Luna with high reasoning in Codex or Haiku in Claude. The main model keeps edits, decisions, and final checks. Token savings are not guaranteed.

## Limits and recovery

Only `--install` downloads the package or changes user files. The default check starts the Codex app server only to inspect hook status; it does not run a model task. Both clients use their standard home directories. Custom `CODEX_HOME` or `CLAUDE_CONFIG_DIR` locations need a separate setup and are reported as unsupported.

Backups live under `~/.local/share/c2c-agent-policy/backups/`. Restore only the needed files, preserving later edits. Keep trust review in the native client. A repo file is a setup aid, not an admin policy or a security boundary. New teammates must pull the repo and run the command. Required installation across devices needs managed deployment.

Maintainers: update the canonical template in `antonio-claude-skills/scripts/agent-setup-template`, test it, and distribute it to enrolled repos. Update the pinned commit and all package hashes together. Keep the short setup block near the top of both `AGENTS.md` and `CLAUDE.md` so long instruction files do not hide it.
