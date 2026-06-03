---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable issues using tracer-bullet vertical slices, written as local markdown files under ai/issues/. Use when the user wants to convert a plan into issues, create implementation tickets, or break work down into tasks.
---

# To Issues

Break a plan into independently-grabbable issues using vertical slices (tracer bullets), written as local markdown files. Prefer **self-contained tasks** that can be picked up and completed on their own; fall back to declaring dependencies when a task genuinely cannot stand alone.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a path, a PRD, a spec, or a plan) as an argument, read its full body before slicing. PRDs from this workspace typically live under `ai/prds/`.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

### 3. Draft vertical slices

Break the plan into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Prefer **self-contained** tasks that carry no blockers. Only introduce a "Blocked by" dependency when a slice genuinely cannot be started or verified without another slice landing first
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first — aim for "None"
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the slices as self-contained as they can be? Can any blocker be designed away?
- Are the remaining dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.

### 5. Write the issues as local markdown files

Issues are written as local markdown files only — never published to an external issue tracker.

1. Find the `ai/` folder at the repository root. Reuse it if it exists, otherwise create it.
2. Inside `ai/`, issues always go in `ai/issues/`. Reuse the folder if it exists, otherwise create it.
3. Write one file per approved slice, using the body template below. Name each file with a zero-padded ordinal and a short kebab-case slug so dependency order is visible at a glance, e.g. `ai/issues/01-account-balance-endpoint.md`. If a file with that name already exists, confirm with the user before overwriting.
4. Write files in dependency order (blockers first) so the "Blocked by" field can reference the real filename of the blocking issue.

Report the list of written file paths to the user once done.

<issue-template>

## Parent

A reference to the parent plan, spec, or PRD this slice came from (e.g. `ai/prds/<name>.md`). Omit this section if there is no parent source.

## Type

One of:

- **AFK** — implementable and mergeable with no human interaction during the work; a human only reviews it afterward.
- **HITL** — a human is required *during* implementation (an architectural decision, a design review, a credential).

## Status

`Not started`

One of `Not started` | `In progress` | `Completed`. New issues are always written as `Not started`; downstream skills advance this as the work moves.

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- A reference to the blocking issue file (e.g. `ai/issues/01-...md`)

Or "None — self-contained" if there are no blockers.

</issue-template>

Do NOT close or modify any parent source.
