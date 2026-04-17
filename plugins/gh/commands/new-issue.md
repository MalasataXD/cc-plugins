---
description: Draft and create a well-formed GitHub issue with correct labels and template. Usage /gh:new-issue <description> [owner/repo]
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **New Issue** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If the last token matches `owner/repo` format, treat it as the target repo and the rest as the description.
2. Otherwise the entire argument string is the description; infer the repo from CWD via `gh repo view --json nameWithOwner`. If that fails, ask the user.
3. Read the repo's label taxonomy (`gh label list`) and available issue templates before drafting.
4. Always show the full draft (title + labels + body) to the user and wait for approval before calling `gh issue create`.
5. After creation, output the new issue URL.
