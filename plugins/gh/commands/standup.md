---
description: Generate a standup report: yesterday's closes and today's open plate. Usage /gh:standup
---
Invoke the `gh` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/gh/SKILL.md`) and run the **Standup** workflow.

Arguments: `$ARGUMENTS`

Parsing rules:
1. No arguments expected. Ignore any provided.
2. "Yesterday" means the calendar day before today in the user's local timezone — use the ISO date of yesterday as the `--closed ">=<date>"` filter.
3. Format output using `config.standup_format`. Leave the `{blockers}` section blank with a placeholder: _(fill in manually)_.
4. Keep the list short: max 10 items per section.
