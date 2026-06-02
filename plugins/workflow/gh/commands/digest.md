---
description: Summarize issues closed and PRs merged in a time period. Usage /gh:digest [<since>] [owner/repo or owner]
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **Digest** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. The first token is the `<since>` window. Accept:
   - Relative: `7d`, `2w`, `1m`, `last monday`
   - ISO date: `2026-04-10`
   - Omitted: extension uses `digest_window_days` from its config.
2. If a second token matches `owner/repo`, pass it as `--repo`.
3. If a second token matches a bare owner (no slash), pass it as `--owner`.
4. If no repo/owner is given, add `--full` for a cross-repo digest.
