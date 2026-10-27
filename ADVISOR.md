<!-- BEGIN:advisor-semantic-routing -->
# Business advisor setup and automatic use

Use `team-config:antonio-business-advisor` from the private marketplace
`antonio-clicktoclose/antonio-claude-skills`, version 0.8.2 or later. The package
contains the complete reader, training skills and source routes. Every user
needs their own GitHub access and their existing authorized Obsidian connection.
Never share personal credentials or copy Antonio's service-account token.

Claude Code installation:

```bash
claude plugin marketplace add antonio-clicktoclose/antonio-claude-skills
claude plugin install team-config@antonio-claude-skills -s user
claude plugin update team-config@antonio-claude-skills -s user
```

For Codex, use its plugin manager to add the same marketplace and install or
update `team-config`. Use the installed skill path returned by that manager.
Do not assume another person's home path exists. Both tools must trust and
load the package through their normal approval flow.

Before business advice, read the installed skill. Run its reader by absolute
path from any repository:

```text
python3 <installed-skill>/scripts/business_advisor.py teaching "business problem"
```

The default route uses a local embedding model and a local relevance model.
On first use it installs the pinned Python runtime and downloads public model
files into that user's cache. Chat text stays local. There is no paid embedding
API. Python 3.10 or later and network access are needed for initial setup.
Use `OBSIDIAN_API_KEY` from the user's existing authorized connection, or the
approved local SDK credential reader. Do not print or store a key in this repo.

Search only the reviewed public teaching manifest and shared semantic index.
The reader checks each selected passage against the current source note.
Results carry source links, timestamps and frames when the original review has
them. Older text-only sections must stay labelled as such. Do not invent a
missing frame. For a visual claim, inspect the actual returned image.

The agent must infer the business problem from the chat, including short
follow-ups. It must not ask for permission to query the advisor. It must still
read current project facts, keep clients separate and select only useful
sources. Keep the user's voice; do not impersonate a teacher or turn outside
benchmarks into facts. Advice does not authorize external actions.

When the semantic model, index or source is unavailable, the reader reports a
lexical fallback. State that limit and continue with the best verified sources.
Do not call a fallback result semantic. A skill instruction guides the agent;
it does not prove that every future model response will comply.

Shared operating record:
https://obsidian.clicktoclose.ai/?note=C2C%2FProcesses%2FBusiness-Advisor-Training-Sources-And-Maintenance
<!-- END:advisor-semantic-routing -->


