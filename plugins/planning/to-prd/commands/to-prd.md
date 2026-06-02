---
description: Turn the current conversation context into a PRD and save it under ai/prds/. Usage /to-prd [optional focus or feature name]
---
Invoke the `to-prd` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/to-prd/SKILL.md`) and produce a PRD from the current context.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If `$ARGUMENTS` is non-empty, treat it as the feature name or focus for the PRD and use it to scope the synthesis and the output filename.
2. If `$ARGUMENTS` is empty, synthesize the PRD from the current conversation context and codebase understanding.
3. Do NOT interview the user — synthesize what you already know, following the skill exactly.
4. Confirm the proposed test seams with the user, then write the PRD as a local markdown file under `ai/prds/` (reusing or creating the `ai/` folder as described in the skill) and report the path.
