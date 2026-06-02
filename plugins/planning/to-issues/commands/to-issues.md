---
description: Break a plan, spec, or PRD into self-contained issues written under ai/issues/. Usage /to-issues [plan, spec, PRD path, or free-form description]
---
Invoke the `to-issues` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/to-issues/SKILL.md`) and break the subject below into tracer-bullet vertical slices.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If `$ARGUMENTS` names a file (e.g. a PRD under `ai/prds/`, a spec, or a plan), read its full body first and use it as the source material.
2. If `$ARGUMENTS` is free-form text, treat it as the plan to break down.
3. If `$ARGUMENTS` is empty, work from the current conversation context.
4. Follow the skill exactly: prefer self-contained slices, present the numbered breakdown and iterate with the user until approved, then write one local markdown file per slice under `ai/issues/` (reusing or creating the `ai/` folder) in dependency order, and report the written paths.
