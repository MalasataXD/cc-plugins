---
description: Build a feature or fix a bug test-first with the red-green-refactor loop. Usage /tdd [optional feature, bug, or behavior]
---
Invoke the `tdd` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/tdd/SKILL.md`) and apply it to the arguments below.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If `$ARGUMENTS` is non-empty, treat it as the feature, bug, or behavior to build test-first.
2. If `$ARGUMENTS` is empty, apply TDD to the work currently in focus in the conversation.
3. Follow the skill exactly: plan and confirm the interface and behaviors with the user first, then work in vertical slices (one test → one implementation → repeat), and refactor only once green.
