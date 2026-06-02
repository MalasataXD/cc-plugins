---
description: Grill a plan against the domain model, sharpen terminology, and update CONTEXT.md and ADRs inline. Usage /grill:with-docs [plan or topic]
---
Invoke the `grill-with-docs` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/grill-with-docs/SKILL.md`) and run the interview against the subject below.

Arguments: `$ARGUMENTS`

Parsing rules:
1. Treat `$ARGUMENTS` as the plan, design, or topic to grill. It may name a file, a feature, or a free-form description.
2. If `$ARGUMENTS` is empty, ask the user what plan they want grilled before starting.
3. Follow the skill exactly: ask one question at a time, waiting for feedback before continuing, and give your recommended answer for each question.
4. During codebase exploration, also locate existing domain docs (`CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`) as described in the skill, and create them lazily only when there is something to write.
5. Challenge the user's terminology against the glossary, sharpen fuzzy language, cross-reference claims with code, update `CONTEXT.md` inline as terms resolve, and offer ADRs only when the decision is hard to reverse, surprising, and a real trade-off.
