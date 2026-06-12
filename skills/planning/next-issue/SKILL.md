---
name: next-issue
description: Find the next open issue under ai/issues/, read it in full, and present an implementation plan for approval before writing any code. Use when the user wants to pick up the next piece of work, asks "what's next", or wants to start the next issue in a breakdown.
---

# Next Issue

Pick up the next open issue from a local breakdown, understand it, and present a concrete implementation plan — then **stop and wait for approval** before touching any code. The point is to start work deliberately: the right issue, fully understood, with a plan the user has signed off on.

Selection and planning are the whole job. Do NOT begin implementing until the user approves the plan.

## Process

### 1. Locate the issues

Work out where the issues live:

1. If the user passes a specific issue file, use it directly and skip to step 3.
2. If the user passes a folder or glob, search there.
3. Otherwise default to `ai/issues/` at the repository root.
4. If the folder is missing or empty, say so and stop — there is nothing to pick up.

### 2. Select the next open issue

Read the `## Status` of every issue in scope. An issue is **open** when its status is `Not started` or `In progress`; `Completed` is closed.

Choose the next one to work on:

1. Prefer an `In progress` issue if one exists — finishing started work beats starting new work. Surface it and confirm the user wants to continue it rather than start something fresh.
2. Otherwise pick the **lowest-ordinal** `Not started` issue whose blockers are all `Completed`. Read each candidate's `## Blocked by`; skip any issue whose blocking issue is not yet `Completed`.
3. If every open issue is blocked by unfinished work, report the dependency wall — name what must complete first — and stop.

State which issue you picked and why (ordinal order, blockers satisfied) so the choice is transparent.

### 3. Read the issue in full

Read the entire selected issue — `Type`, `What to build`, `Acceptance criteria`, `Blocked by`, and any `Parent` reference. If a parent PRD or spec is linked, skim it for context the issue assumes.

Note the `## Type`:

- **AFK** — implementable and mergeable with no human interaction during the work; the human only reviews afterward. Plan to drive it end-to-end.
- **HITL** — a human is needed *during* implementation (an architectural call, a design review, a credential). Identify in your plan exactly where you will need the user, so they know what they're signing up for.

### 4. Explore the codebase

Ground the plan in the actual code. Find the relevant modules, seams, and existing patterns so the plan names real integration points rather than guesses. Use the project's domain glossary vocabulary and respect ADRs in the area you're touching. This is the homework that makes the plan trustworthy.

### 5. Present the plan and wait

Present the plan directly in the conversation using the format below. Be concrete: tie each step to the acceptance criteria it satisfies, name the real parts of the codebase you'll touch, and call out every point where a HITL issue needs the user. Then **stop**.

<output-format>
## Next issue: <filename> — <title>

**Status:** Not started → (proposing to start) · **Type:** AFK / HITL

**Goal:** one sentence on what "done" looks like, drawn from the acceptance criteria.

### Plan
1. Step tied to an integration point — *covers: acceptance criterion X*
2. ...
3. ...

### Where I'll need you (HITL only)
- The specific decision or review point, and why it can't be automated. Omit this section entirely for AFK issues.

### Verification
How the finished slice will be demoed or tested on its own, mapped to the acceptance criteria.

### Open questions
Anything ambiguous in the issue worth resolving before starting — or "None." Frame these as questions, do not silently guess.
</output-format>

Wait for the user to approve, adjust, or redirect. Do not start editing until they give the go-ahead.

### 6. On approval

Once the user approves, you may offer to set the issue's `## Status` to `In progress` so the breakdown reflects that the work has started — a one-line edit, only after they confirm. Then begin implementing the approved plan.

Do NOT modify any issue file before approval, and never mark acceptance criteria complete here — that is `complete-issue`'s job.
