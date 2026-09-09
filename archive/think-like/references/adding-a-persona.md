# Adding a Persona

Author a new persona into `personas/` when the user wants one that does not yet
exist (e.g. "add a data-scientist persona", or after a failed resolution).

1. **Resolve the alias.** Take a kebab-case alias (lowercase letters, digits,
   hyphens); correct it if malformed. If `personas/<alias>.md` already exists,
   stop and tell the user to edit that file or pick a different alias — never
   overwrite.

2. **Draft the spec** from the user's idea, following the library template:

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
   <1 short paragraph on what shapes this role's intuition — what they've seen
   go wrong, what they respect, what they're skeptical of>
   ```

3. **Ask clarifying questions** only if the idea is too thin to fill the template
   (tone, default seniority, domain boundary vs. an adjacent role). 1–3 max.

4. **Show the draft** in a code block and wait for explicit approval before
   writing anything to disk. Offer to revise.

5. **On approval**, write `personas/<alias>.md`.

6. **Confirm** the path, and remind the user: a persona added to the installed
   skill lives only in that install. To keep it permanently and sync it to other
   machines, also add the file to the cc-plugins repo under
   `skills/reasoning/think-like/personas/` and re-run `npx skills add`.
