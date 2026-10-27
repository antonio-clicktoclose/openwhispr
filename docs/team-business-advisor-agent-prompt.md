# Setup prompt for Claude Code or Codex, from any local folder

Paste this into either agent. No repo clone or plugin install is needed first. The person still needs their own approved access. This setup supports macOS and Linux.

```text
Set up this machine's shared business advisor for both Claude Code and Codex. Work from my current folder. Do not assume I have cloned a team repo or installed the plugin. Until setup passes, do setup work only.

Use my own GitHub access and approved Obsidian connection. Keep repo permissions, credentials, model settings, unrelated hooks and trust choices unchanged. Never copy another person's token or bypass native trust.

1. Check the prerequisites: Git, both app CLIs and normal app sign-ins. On macOS, use the signed python.org interpreter at /Library/Frameworks/Python.framework/Versions/3.13/bin/python3. Linux needs Python 3.10 or later. Help install missing tools through official sources. Ask me to complete any required login or OS approval. Stop and report unsupported platforms or missing access.

2. Fetch this private repo into a new temporary directory outside my current folder:
   https://github.com/antonio-clicktoclose/antonio-claude-skills.git

   Fetch and check out this exact reviewed commit:
   c956fe9b9b9d3525aadae132ec849164c7d60164

   Verify that HEAD matches the full commit before running its code. Stop if any fetch or verification fails. Leave my current folder's files untouched.

3. From that temporary checkout, run plugins/team-config/runtime/advisor/setup.py with the required Python interpreter. Use an absolute script path. Run setup without --verify first, so login and trust can be completed before model tests.

4. Ask me to review any required native Codex /hooks trust or workspace trust. Never approve it yourself. Then run ~/.local/share/c2c-team-config-updates/verify.py with the required interpreter, using the temporary Git checkout as the working directory. These tests use my normal account credits and selected models.

5. Verify both apps load the advisor automatically in a repo and a non-Git folder. Confirm that an ordinary business question triggers semantic search without naming the advisor. Check the cited timestamps and linked frame files against the live reviewed notes. Keep raw logs private.

6. Return to my original folder. Run ~/.local/share/c2c-team-config-updates/check_business_advisor_setup.py with the required interpreter. Resume normal work only when it exits 0 and reports "ordinary_work_allowed": true.

Report installed versions, test results and any exact blocker. Do not claim success from an enabled setting or a package install alone. Keep the temporary checkout until checks pass, then remove only the temporary files you created. Leave user hooks and global instructions installed so this works across repos and local folders with automatic updates.
```

This is an agent instruction gate, not an OS security lock. Missing private-repo access remains a blocker.
