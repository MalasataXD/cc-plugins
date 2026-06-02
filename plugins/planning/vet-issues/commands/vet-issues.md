---
description: Pressure-test issues through an implementer's eyes and report what would block them. Usage /vet-issues [issue file, folder, or glob]
---
Invoke the `vet-issues` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/vet-issues/SKILL.md`) and pressure-test the issues below by reading each one as an implementer picking it up cold.

Arguments: `$ARGUMENTS`

Parsing rules:
1. If `$ARGUMENTS` names an issue file, a folder, or a glob, vet exactly those issues.
2. If `$ARGUMENTS` is empty, default to the issues under `ai/issues/`.
3. Follow the skill exactly: read every issue in scope, vet each against the implementer checklist, run the cross-issue checks, and present all findings directly in the conversation. This is read-only — do NOT edit the issues and do NOT write a report file.
