---
description: Draft a new expert persona spec interactively, then save it to the think-like library. Usage /think:add <archetype> <idea>
---
Help the user create a new persona file for the `think-like` skill library shipped with this plugin.

Arguments: `$ARGUMENTS`

Parsing rules:
1. The first whitespace-delimited token is the **archetype alias** (kebab-case, e.g. `data-scientist`).
2. Everything after that token is the **idea** — a free-form description of the role.

Workflow:

1. **Validate the alias.**
   - Must be kebab-case (lowercase letters, digits, hyphens). If not, suggest a corrected alias.
   - Check whether `${CLAUDE_PLUGIN_ROOT}/skills/think-like/personas/<alias>.md` already exists. If it does, stop and tell the user to either edit that file directly or pick a different alias. Do **not** overwrite.

2. **Draft the persona spec** from the idea, following the template used in the existing library:

   ```markdown
   # <Full Name>
   **Alias:** `<alias>` | **Focus:** <3–6 comma-separated focus areas>

   ## Mental Models
   - **<Model 1>** — <one-line explanation>
   - **<Model 2>** — <one-line explanation>
   - (3–6 total)

   ## Key Questions
   - <question 1>
   - <question 2>
   - (3–5 total)

   ## Experience Markers
   <1 short paragraph describing what shapes this role's intuition — what they've seen go wrong, what they respect, what they're skeptical of>
   ```

3. **Ask clarifying questions** only if the idea is too thin to fill the template (e.g. tone, default seniority level, domain boundary vs. an adjacent role). Use the AskUserQuestion tool. Keep it to 1–3 questions max.

4. **Show the drafted markdown to the user** in a code block and ask for approval before writing anything to disk. Offer to revise if they want changes.

5. **On explicit approval**, write the file to `${CLAUDE_PLUGIN_ROOT}/skills/think-like/personas/<alias>.md` using the Write tool.

6. **Confirm** by telling the user:
   - The exact path of the new file.
   - **Caveat:** the plugin cache at that path is refreshed when the marketplace updates. For a persona you want to keep permanently, also commit the new file to your cc-plugins repo under `plugins/think/skills/think-like/personas/`.
   - How to invoke it: `/think:like <alias> <prompt>` — or naturally, e.g. *"think like a <alias>…"*.
