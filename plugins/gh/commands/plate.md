---
description: Show open GitHub issues assigned to you, grouped by repo. Usage /gh:plate [owner/repo]
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **Plate** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If an argument is provided in `owner/repo` format, restrict results to that repo using `--repo`.
2. If an `owner` (no slash) is provided, restrict to that owner using `--owner`.
3. If no argument is given, search across all repos the user has access to.
4. Sort by last updated descending. Group by repo in the output.
