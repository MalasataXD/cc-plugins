---
description: Find the next open issue, read it, and present a plan for approval. Usage /next-issue [issue file or folder]
---
Invoke the `next-issue` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/next-issue/SKILL.md`) and pick up the next open issue.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If `$ARGUMENTS` names a specific issue file, use that issue directly (skip selection).
2. If `$ARGUMENTS` names a folder, search for the next open issue there instead of the default.
3. If `$ARGUMENTS` is empty, default to the issues under `ai/issues/`.
4. Follow the skill exactly: select the next open issue, read it in full, present an implementation plan, and wait for approval. Do NOT start editing code until the user approves.
