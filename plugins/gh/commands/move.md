---
description: Move an issue to a new project status. Usage /gh:move <issue-url-or-number> <status> [owner/repo]
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **Move** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. The first token is the issue reference:
   - Full URL: `https://github.com/owner/repo/issues/123` — extract owner, repo, and number.
   - Plain number like `123`: require a `owner/repo` token (third argument) or infer from CWD via `gh repo view --json nameWithOwner`.
2. The second token (everything between the issue ref and an optional repo) is the target **status name** (e.g. `"In Progress"`, `done`, `todo`). Match case-insensitively against the project's option names.
3. Optional third token: `owner/repo` to disambiguate when a plain issue number is given without a git context.
4. If the issue belongs to multiple projects, list them and ask which one to update.
5. Prefer cached project field/option IDs. Populate cache on first use per project.
