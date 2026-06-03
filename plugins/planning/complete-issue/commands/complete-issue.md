---
description: Review your changes against an issue's acceptance criteria and report what's done and what's left. Usage /complete-issue [issue file]
---
Invoke the `complete-issue` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/complete-issue/SKILL.md`) and verify the work done for an issue against its acceptance criteria.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If `$ARGUMENTS` names a specific issue file, verify against that issue.
2. If `$ARGUMENTS` is empty, infer which issue is being worked on from the conversation, the current changes (git status/diff), and the `In progress` issues under `ai/issues/`. If it is ambiguous, ask which issue to check.
3. Follow the skill exactly: assess each acceptance criterion against the actual changes, report what is done and what is left, and present the state directly in the conversation. This is read-only — only after the user confirms may you tick verified criteria or update the issue's status.
