---
name: next-ticket
description: Pick the next open ticket. Use when the user wants to pick up the next piece of work or asks "what's next".
---

# Next Ticket

Pick up the next open ticket from a local breakdown, understand it, and present a concrete plan — then **stop and wait for approval** before touching any code. The plan is the user's chance to catch a mistake on the way out the door, so selection and planning are the whole job.

## Process

### 1. Locate the ticket set

1. If the user passes a specific ticket file, use it and skip to step 3.
2. If the user passes a folder or glob, search there.
3. Otherwise look in `<work folder>/tickets/`. The project's `AGENTS.md` or `CLAUDE.md` names the work folder; when it names nothing, use `.ai/` at the repository root. Each breakdown is a subfolder named after its spec; with one subfolder use it, with several ask which.
4. If nothing is found, say so and stop.

### 2. Select the next open ticket

Survey the set by headers only: the `[P<x>]` phase in each title, the `Type`, `Category`, and `Status` lines under it, and the `## Blocked by` section. A ticket is **open** when its Status is `Not started` or `In progress`.

1. Prefer an `In progress` ticket if one exists — finishing started work beats starting new work. Surface it and confirm the user wants to continue it.
2. Otherwise stay in the **lowest phase with an open ticket**; phases complete in order, so a later phase waits until every ticket in the current one is `Completed`. Within that phase, pick the lowest-ordinal `Not started` ticket whose blockers are all `Completed`.
3. If every open ticket in the phase is blocked by unfinished work, name what must complete first and stop.

State which ticket you picked and why.

### 3. Read the ticket in full

Read the whole ticket, and skim its `Parent` spec for the context the ticket assumes.

The `Type` decides where the user is needed. **RFA** runs end to end with no human during the work. **RFH** needs the user at a specific point — a decision, a design review, a credential — so the plan names exactly where; when the human-only steps are a manual procedure (credentials, dashboards, provisioning), plan to generate a walkthrough via the `wizard` skill.

The `Category` decides what the plan is and who takes it on approval:

- **Build** — an implementation plan; on approval it goes to `implement`.
- **Research** — no code. The plan is the question, the primary sources to check, and what the findings must settle; on approval it goes to the `research` skill.
- **Decision** — no code. The plan is the question, the realistic options, and your recommended answer; on approval it becomes a `grilling` session, the outcome recorded in the ticket, with an ADR via `domain-modeling` if hard to reverse.

### 4. Explore the codebase

Ground the plan in the actual code: the modules, seams, and existing patterns, so the plan names real integration points rather than guesses. Name things the way `CONTEXT.md` names them and respect ADRs in the area you're touching — see the `domain-modeling` skill. Run anything the plan adds — a new module, dependency, or special case — through the ledger in the `complexity` skill.

### 5. Present the plan and wait

Present the plan in the conversation using the format below: each step tied to the acceptance criteria it satisfies, the real parts of the codebase it touches, and every point where an RFH ticket needs the user. Then **stop**.

<output-format>
## Next ticket: <filename> — <title>

**Type:** RFA / RFH · **Category:** Build / Research / Decision

**Goal:** one sentence on what "done" looks like, drawn from the acceptance criteria.

### Plan
1. Step tied to an integration point — *covers: acceptance criterion X*
2. ...

### Where I'll need you (RFH only)
- The specific decision or review point, and why it can't be automated. Omit for RFA tickets.

### Verification
How the finished ticket will be demoed or tested on its own, mapped to the acceptance criteria.

### Open questions
Anything ambiguous in the ticket worth resolving before starting — or "None." Ask; never silently guess.
</output-format>

Wait for the user to approve, adjust, or redirect.

### 6. On approval

Approval is the go-ahead: set the ticket's `Status` line to `In progress` and hand the plan to the skill its Category names. That status line is the only edit made here — acceptance criteria are marked by `complete-ticket`, never by this skill.
