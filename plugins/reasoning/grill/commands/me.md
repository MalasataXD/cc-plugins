---
description: Stress-test a plan or design through relentless one-at-a-time interviewing. Usage /grill:me [plan or topic]
---
Invoke the `grill-me` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/grill-me/SKILL.md`) and run the interview against the subject below.

Arguments: `$ARGUMENTS`

Parsing rules:
1. Treat `$ARGUMENTS` as the plan, design, or topic to grill. It may name a file, a feature, or a free-form description.
2. If `$ARGUMENTS` is empty, ask the user what plan they want grilled before starting.
3. Follow the skill exactly: ask one question at a time, walk each branch of the decision tree resolving dependencies one-by-one, and give your recommended answer for each question.
4. When a question can be answered by exploring the codebase, explore the codebase instead of asking.
