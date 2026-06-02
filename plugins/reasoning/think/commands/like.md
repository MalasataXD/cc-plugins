---
description: Reason through a prompt from a specific expert role's perspective. Usage /think:like <archetype> <prompt>
---
Invoke the `think-like` skill shipped with this plugin (`${CLAUDE_PLUGIN_ROOT}/skills/think-like/SKILL.md`) and apply it to the arguments below.

Arguments: `$ARGUMENTS`

Parsing rules:
1. The first whitespace-delimited token is the **archetype** (e.g. `software-architect`, `ux-designer`).
2. Everything after that token is the **prompt** to reason about.
3. Resolve the archetype against `${CLAUDE_PLUGIN_ROOT}/skills/think-like/personas/` — first by filename (minus `.md`), then by `**Alias:**` value inside each file.
4. If no match, list the available personas in that directory and suggest `/think:add <archetype> <idea>` so the user can define it.
5. On a match, read only the matching persona file, then apply the skill's response structure (Header, Gut Reaction, Structured Analysis, Recommendation, optional Diagnostic Questions).
