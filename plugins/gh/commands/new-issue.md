---
description: Draft and create a well-formed GitHub issue with correct labels and template. Usage /gh:new-issue <description> [owner/repo]
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **New Issue** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If the last token matches `owner/repo` format, treat it as the target repo and the rest as the description.
2. Otherwise the entire argument string is the description; infer the repo from CWD via `gh repo view --json nameWithOwner`. If that fails, ask the user.
3. Run a `--json` preview first, show the draft to the user, wait for approval, then re-run with `--confirm` to create.
4. After creation, output the new issue URL.
