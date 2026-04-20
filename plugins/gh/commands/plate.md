---
description: Show open GitHub issues assigned to you, grouped by repo. Usage /gh:plate [owner/repo]
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **Plate** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If an argument is provided in `owner/repo` format, pass it as `--repo`.
2. If a bare owner (no slash) is provided, pass it as `--owner`.
3. If no argument is given, or the user says "everywhere" / "all repos", add `--full`.
4. Group output by repo, sorted by last updated descending.
