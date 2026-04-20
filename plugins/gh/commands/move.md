---
description: Move an issue to a new project status. Usage /gh:move <issue-url-or-number> <status> [owner/repo]
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **Move** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. The first token is the issue reference:
   - Full URL: `https://github.com/owner/repo/issues/123` — extract owner, repo, and number.
   - Plain number like `123`: use the third-arg `owner/repo` or infer via `gh repo view --json nameWithOwner`.
2. The second token is the target **status name** (e.g. `"In Progress"`, `done`, `todo`). Matched case-insensitively by the extension.
3. Optional third token: `owner/repo` to disambiguate when a plain number is given.
