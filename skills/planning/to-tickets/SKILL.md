---
name: to-tickets
description: Break a plan or spec into phases of compact tickets. Use when the user wants to break work down into tickets.
---

# To Tickets

Break a plan into **phases** of tickets. A phase is a group of tickets that, once all complete, leaves the feature in a state the user can verify or demo. Phases run in order; the tickets inside a phase are independent unless one says otherwise, so an agent can pick up every unblocked ticket in the current phase at once.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a path, a spec, or a plan) as an argument, read its full body before grouping. Specs live under `<work folder>/specs/`; the project's `AGENTS.md` or `CLAUDE.md` names the work folder, and when it names nothing, use `.ai/` at the repository root.

If you have not already explored the codebase, do so. Name things the way `CONTEXT.md` names them and respect ADRs in the area you're touching — see the `domain-modeling` skill. If a ticket introduces a new module, dependency, or special case the plan didn't account for, run it through the ledger in the `complexity` skill before writing it.

### 2. Group the work into phases

Draft the phases first, then the tickets inside each:

- Each phase ends in a **verifiable state** — something that can be demoed, tested, or checked end to end. Name the phase by that state.
- A ticket is the unit of work one agent completes in one session. Prefer several small tickets over one large one, and keep tickets in a phase from touching the same code where a different split avoids it.
- A ticket that touches the same code as another in its phase is **blocked by** it. Block only within a phase — phase order already orders the phases.
- Any open question — a fact to look up, a choice nobody has made, a design best judged from throwaway code — becomes its own Research or Decision ticket in the earliest phase it fits, and the tickets waiting on it are blocked by it. Never bury one inside a Build ticket as a silent assumption. If the spec carries a `## Required Research` section, emit one Research ticket per question.

### 3. Confirm with the user

Present the phases as a list: phase number, name and verifiable state, then each ticket's title, Type, Category, and blockers. Ask one question: approve, or what to move, merge, or split. Iterate until approved.

### 4. Write the tickets

Tickets are local markdown files only — never published to an external tracker.

1. Tickets go in `<work folder>/tickets/<spec-slug>/`. Create the folder if it is missing.
2. Write one file per ticket using the template below, named `<phase>-<n>-<slug>.md`, e.g. `1-2-stock-lists-hook.md`, so phase and order are visible at a glance. If a file with that name already exists, confirm with the user before overwriting.
3. Write blockers first so `Blocked by` can name the real filename.
4. Append a `## Phases` section to the parent spec as a map of the breakdown: one heading per phase with its verifiable state, then its ticket files as a list. This is the only edit ever made to the spec.

Report the written file paths.

### 5. Vet once

The files are what an implementer picks up, so vet the files, cold, through sub-agents running the `vet-tickets` skill — about five contiguous tickets per sub-agent, plus one over the whole set for cross-ticket checks when there are more than five.

Then triage every finding yourself:
- If the answer exists in the spec or the conversation, edit the ticket and list the edit.
- Only a finding that needs a decision nobody has made becomes a question for the user.

Re-vet at most once, only the tickets you edited, and only if one was verdict **Blocked** (`vet-tickets` reports nothing else). After that, remaining findings are reported, not looped. Two rounds is the cap.

## Ticket template

Type, Category, and Status are read by `next-ticket` and `complete-ticket`; keep them on one line each.

<ticket-template>

# [P<x>] <title>

Parent: specs/<slug>.md
Type: RFA
Category: Build
Status: Not started

## What to build

Two to five sentences of end-to-end behavior. No file paths or code snippets — they go stale fast. Exception: a snippet from a prototype that encodes a decision more precisely than prose (state machine, reducer, schema, type shape), trimmed to the decision-rich parts and marked as coming from the prototype.

## Acceptance criteria

- [ ] Concrete, verifiable criterion

## Blocked by

- 1-1-<slug>.md, or `None`

</ticket-template>

## Field values

- **Type** — `RFA` (ready-for-agent): implementable and mergeable with no human during the work. `RFH` (ready-for-human): a human is required during implementation — a decision, a design review, a credential. Prefer RFA.
- **Category** — `Build` is the default. `Research`: a fact from primary sources, resolved by the `research` skill, almost always RFA. `Decision`: a choice nobody has made, resolved in a `grilling` session, RFH by nature; a hard-to-reverse outcome earns an ADR via `domain-modeling`. For the last two, the acceptance criteria name what the outcome must settle, and the outcome is recorded in the ticket.
- **Status** — `Not started` | `In progress` | `Completed`. New tickets are always `Not started`; downstream skills advance it.

Beyond the `## Phases` map, do NOT close or modify any parent source.
