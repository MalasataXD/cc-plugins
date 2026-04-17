---
description: Summarize issues closed and PRs merged in a time period. Usage /gh:digest [<since>] [owner/repo or owner]
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **Digest** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. The first token is the `<since>` window. Accept:
   - Relative: `7d`, `2w`, `1m`, `last-monday`
   - ISO date: `2026-04-10`
   - Omitted: use `config.digest_window_days` days as the default window.
2. If a second token matches `owner/repo`, restrict both issue and PR searches to that repo.
3. If a second token matches an owner (no slash), restrict to that owner.
4. Group output by repo. Include totals at the end.
