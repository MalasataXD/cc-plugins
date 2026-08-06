---
name: next-ticket
description: Find the next open ticket under ai/tickets/, read it in full, and present an implementation plan for approval before writing any code. Use when the user wants to pick up the next piece of work, asks "what's next", or wants to start the next ticket in a breakdown.
---

# Next Ticket

Pick up the next open ticket from a local breakdown, understand it, and present a concrete implementation plan — then **stop and wait for approval** before touching any code. The point is to start work deliberately: the right ticket, fully understood, with a plan the user has signed off on.

Selection and planning are the whole job. Do NOT begin implementing until the user approves the plan.

## Process

### 1. Locate the tickets

Work out where the tickets live:

1. If the user passes a specific ticket file, use it directly and skip to step 3.
2. If the user passes a folder or glob, search there.
3. Otherwise default to `ai/tickets/` at the repository root.
4. If the folder is missing or empty, say so and stop — there is nothing to pick up.

### 2. Select the next open ticket

Run the bundled selector instead of reading every file for its fields:

```bash
bash <path-to-this-skill>/scripts/next-ticket.sh [tickets-dir]
```

It prints every ticket's Type, Category, Status, and blockers in one table, plus a `NEXT:` line computed by the same rules below. Trust the survey, but sanity-check the pick — and fall back to reading the files yourself if bash is unavailable or the tickets deviate from the template.

A ticket is **open** when its status is `Not started` or `In progress`; `Completed` is closed. The selection rules:

1. Prefer an `In progress` ticket if one exists — finishing started work beats starting new work. Surface it and confirm the user wants to continue it rather than start something fresh.
2. Otherwise pick the **lowest-ordinal** `Not started` ticket whose blockers are all `Completed`. Read each candidate's `## Blocked by`; skip any ticket whose blocking ticket is not yet `Completed`.
3. If every open ticket is blocked by unfinished work, report the dependency wall — name what must complete first — and stop.

State which ticket you picked and why (ordinal order, blockers satisfied) so the choice is transparent.

### 3. Read the ticket in full

Read the entire selected ticket — `Type`, `Category`, `What to build`, `Acceptance criteria`, `Blocked by`, and any `Parent` reference. If a parent spec or spec is linked, skim it for context the ticket assumes.

Note the `## Type`:

- **RFA** (ready-for-agent) — implementable and mergeable with no human interaction during the work; the human only reviews afterward. Plan to drive it end-to-end.
- **RFH** (ready-for-human) — a human is needed *during* implementation (an architectural call, a design review, a credential). Identify in your plan exactly where you will need the user, so they know what they're signing up for. When the human-only steps are a manual procedure (credentials, dashboards, provisioning), plan to generate them a walkthrough via the `wizard` skill.

And the `## Category` (tickets without one are **Build**):

- **Build** — a vertical slice; the plan below is an implementation plan.
- **Research** — no code will be written. The plan is the question, the primary sources to check, and what the findings must settle; on approval it goes to the `research` skill, not `implement`.
- **Decision** — no code will be written. The plan is the question, the realistic options, and your recommended answer; on approval it becomes a `grilling` session, the outcome recorded in the ticket (an ADR via `domain-modeling` if hard to reverse).
- **Prototype** — throwaway code only. The plan is the question and which prototype branch fits (logic demo or UI variations); on approval it goes to the `prototype` skill, and the ticket completes when the verdict and prototype pointer are recorded.

### 4. Explore the codebase

Ground the plan in the actual code. Find the relevant modules, seams, and existing patterns so the plan names real integration points rather than guesses. Name things the way `CONTEXT.md` names them and respect ADRs in the area you're touching — see the `domain-modeling` skill. This is the homework that makes the plan trustworthy.

### 5. Present the plan and wait

Present the plan directly in the conversation using the format below. Be concrete: tie each step to the acceptance criteria it satisfies, name the real parts of the codebase you'll touch, and call out every point where an RFH ticket needs the user. Then **stop**.

<output-format>
## Next ticket: <filename> — <title>

**Status:** Not started → (proposing to start) · **Type:** RFA / RFH · **Category:** Build / Research

**Goal:** one sentence on what "done" looks like, drawn from the acceptance criteria.

### Plan
1. Step tied to an integration point — *covers: acceptance criterion X*
2. ...
3. ...

### Where I'll need you (RFH only)
- The specific decision or review point, and why it can't be automated. Omit this section entirely for RFA tickets.

### Verification
How the finished slice will be demoed or tested on its own, mapped to the acceptance criteria.

### Open questions
Anything ambiguous in the ticket worth resolving before starting — or "None." Frame these as questions, do not silently guess.
</output-format>

Wait for the user to approve, adjust, or redirect. Do not start editing until they give the go-ahead.

### 6. On approval

Once the user approves, you may offer to set the ticket's `## Status` to `In progress` so the breakdown reflects that the work has started — a one-line edit, only after they confirm. Then hand the approved plan to the skill its Category names: **Build** goes to `implement`; **Research** to the `research` skill (done when the findings file exists under `ai/research/` and is linked from the ticket); **Decision** to a `grilling` session (done when the outcome is recorded in the ticket); **Prototype** to the `prototype` skill (done when the verdict and prototype pointer are recorded).

Do NOT modify any ticket file before approval, and never mark acceptance criteria complete here — that is `complete-ticket`'s job.
