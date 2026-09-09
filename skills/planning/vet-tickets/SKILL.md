---
name: vet-tickets
description: Read tickets cold as an implementer and report only what would stall them. Use when the user wants to sanity-check tickets before handing them off or find gaps in a breakdown.
---

# Vet Tickets

Read a set of tickets as the implementer who will pick them up **cold** — no access to the conversation that produced them, only the ticket text, what it points at, and the codebase. The one question per ticket: *where would I stall?* A **stall** is the moment the implementer must guess at a decision the author knew. Everything else is healthy exploration, and healthy exploration is not a finding.

This is **read-only**. Do NOT edit or annotate the tickets. Do NOT write a report file. Present the findings directly in the conversation; the caller decides what to do with them.

## Process

### 1. Locate the tickets

1. If the user passes a path or glob (a single ticket file, a folder, or a pattern), use that.
2. Otherwise use `<work folder>/tickets/`. The project's `AGENTS.md` or `CLAUDE.md` names the work folder; when it names nothing, use `.ai/` at the repository root.
3. If no tickets are found, say so and stop.

Tickets carry their phase as a `[P<x>]` title prefix and their Type, Category, and Status as header lines under the title.

### 2. Find the stall, one ticket at a time

Take the tickets **one by one**, the way an implementer picks them up. For each: read the ticket, follow only what it points at — its `Blocked by` tickets and its `Parent` spec — walk the checklist, and write the verdict down before opening the next ticket. A ticket is judged on what it and its references say, never on what a sibling you happened to read earlier said.

Skim the codebase only far enough to answer one question per ticket: is the area this touches identifiable from the ticket's vocabulary and the existing seams? Stop there. Quoting file paths and line numbers back means the implementer would have found them too.

Stop at the **first** stall. One finding per ticket; a second stall is found by the implementer once the first is fixed.

<stall-checklist>
- **Done** — can I state in one sentence what "done" looks like? A `What to build` of a single sentence that names a feature but not its end-to-end behavior is a stall.
- **Start** — can I tell which part of the system this touches? Naming files is not the ticket's job; naming the area is.
- **Criteria** — could two implementers disagree on whether an acceptance criterion is met?
- **Decisions** — is there a choice the ticket assumes is made but never states — a data shape, an edge-case behavior, a UX detail — that I would have to invent?
- **Verification** — could I test or demo this ticket on its own?
</stall-checklist>

<not-a-finding>
Report a stall only when the implementer would have to **guess**. When they would only have to **look** or **read**, the ticket holds:

- Wording you would have phrased differently, or a sentence that would be nice to add.
- A term defined in another ticket of the set, in the spec, or in `CONTEXT.md`.
- Anything answerable by reading the code: the right function, an idiom, a name.
- A question that a Research or Decision ticket in the set already owns, when this ticket is blocked by it.
</not-a-finding>

Verdict per ticket, one of two:

- **Ready** — no stall. Ready tickets get their table row and nothing else.
- **Blocked** — one stall, quoted against the ticket, with the question whose answer removes it. Pose the question; never answer it.

### 3. Check the set

With every verdict recorded, read the whole set together and check the breakdown as a whole:

- **Phases** — does each phase end in a state that can be verified or demoed once its tickets complete?
- **Blockers** — does every `Blocked by` name a ticket that exists in the same phase? Do two unblocked tickets in one phase touch the same code?
- **Coverage** — is there a step between tickets that nobody owns?
- **Overlap** — do two tickets claim the same work?

### 4. Report

Lead with the table so the state of the set is clear at a glance. Be specific: quote the ticket and name the exact question.

<output-format>
## Ticket vet: <scope> (<n> tickets)

| Ticket | Verdict |
| --- | --- |
| 1-1-account-balance-endpoint.md | Ready |
| 1-2-balance-display.md | Blocked |

### 1-2-balance-display.md — Blocked
- **Stall:** the first question the implementer hits, quoted against the ticket.
- **Question for the author:** the decision that removes it.

### Across the set
Phase, blocker, coverage, or overlap findings — or "No cross-ticket problems found."

### Bottom line
One sentence: ready to hand off, or the one thing to fix first.
</output-format>
