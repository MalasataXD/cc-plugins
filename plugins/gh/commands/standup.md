---
description: Generate a standup report: yesterday's closes and today's open plate. Usage /gh:standup
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **Standup** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. No arguments expected. Ignore any provided.
2. Add `--full` if the user asks for all repos or says "everywhere".
3. Output format is controlled by `standup_format` in the extension's config.
