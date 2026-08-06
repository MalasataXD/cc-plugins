---
name: to-tickets
description: Break a plan or spec into independently-grabbable tickets using tracer-bullet vertical slices, written as local markdown files under ai/tickets/. Use when the user wants to break work down into tickets or tasks.
---

# To Tickets

Break a plan into independently-grabbable tickets using vertical slices (tracer bullets), written as local markdown files. Prefer **self-contained tasks** that can be picked up and completed on their own; fall back to declaring dependencies when a task genuinely cannot stand alone.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a path, a spec, or a plan) as an argument, read its full body before slicing. Specs from this workspace typically live under `ai/specs/`.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should name things the way `CONTEXT.md` names them, and respect ADRs in the area you're touching — see the `domain-modeling` skill.

### 3. Draft vertical slices

Break the plan into **tracer bullet** tickets. Each ticket is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Every slice is either **RFA** (ready-for-agent) or **RFH** (ready-for-human). RFH slices need a human during the work — an architectural decision, a design review. RFA slices can be implemented and merged without one. Prefer RFA where possible.

Orthogonal to Type, every ticket has a **Category** — what kind of work resolves it. **Build** is the default: a vertical slice of the plan. The other three are not slices at all; they are questions that must be resolved before dependent slices can be built, and any slice waiting on one lists it in its "Blocked by":

- **Research** — a fact answered from primary sources. Resolved by the `research` skill; almost always Type RFA. If the spec carries a `## Required Research` section, emit one Research ticket per question.
- **Decision** — a choice nobody has made yet that the plan can't proceed without. Resolved through a `grilling` session with the user; Type RFH by nature — the human makes the call.
- **Prototype** — a design question best answered by reacting to throwaway code. Resolved by the `prototype` skill; Type RFH — the human reacts to the artifact.

Never bury one of these inside a Build slice as a silent assumption — split it out so the breakdown shows what is still open.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Prefer **self-contained** tasks that carry no blockers. Only introduce a "Blocked by" dependency when a slice genuinely cannot be started or verified without another slice landing first
</vertical-slice-rules>

<expand-contract-exception>
Some work resists thin slicing: a mechanical change with a wide blast radius — renaming a concept used in two hundred places, swapping a library, changing a shared signature. There is no narrow path through it, because touching one layer breaks every caller at once.

Sequence those as **expand → migrate → contract**:

1. **Expand** — add the new form alongside the old one. Nothing breaks; nothing has moved yet.
2. **Migrate** — move call sites over in batches, keeping CI green after each batch. Large migrations split into several tickets here.
3. **Contract** — delete the old form once nothing references it.

Each phase is its own ticket, and the migrate tickets block the contract ticket. Reach for this only when the blast radius genuinely forces it — a feature that can be sliced vertically still should be.
</expand-contract-exception>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: RFA / RFH
- **Category**: Build / Research / Decision / Prototype
- **Blocked by**: which other slices (if any) must complete first — aim for "None"
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the slices as self-contained as they can be? Can any blocker be designed away?
- Are the remaining dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as RFH and RFA, and every open question split out as a Research, Decision, or Prototype ticket rather than buried in a slice?

Iterate until the user approves the breakdown.

### 5. Write the tickets as local markdown files

Tickets are written as local markdown files only — never published to an external tracker.

1. Find the `ai/` folder at the repository root. Reuse it if it exists, otherwise create it.
2. Inside `ai/`, tickets always go in `ai/tickets/`. Reuse the folder if it exists, otherwise create it.
3. Write one file per approved slice, using the body template below. Name each file with a zero-padded ordinal and a short kebab-case slug so dependency order is visible at a glance, e.g. `ai/tickets/01-account-balance-endpoint.md`. If a file with that name already exists, confirm with the user before overwriting.
4. Write files in dependency order (blockers first) so the "Blocked by" field can reference the real filename of the blocking ticket.

Report the list of written file paths to the user once done.

### 6. Vet the written tickets

The files are what an implementer actually picks up, so vet the files rather than the breakdown you just presented. Read them back cold, through sub-agents — they carry none of the context that produced the tickets, which is exactly the reading that matters.

Dispatch them over the `vet-tickets` skill:

- **Batch contiguously by ordinal**, about five tickets per sub-agent, so a ticket and its blocker land in the same window.
- **One further sub-agent over the whole set** for the cross-cutting checks: dependency cycles, coverage holes, overlap, granularity drift.
- **Under five tickets**, one sub-agent covers everything and the cross-cutting pass is redundant — skip it.

Aggregate the verdicts and present them with the file paths. Findings stay findings: surface each gap as a question for the author, and leave the ticket files as they are unless the user asks for an edit.

<ticket-template>

## Parent

A reference to the parent plan, spec, or spec this slice came from (e.g. `ai/specs/<name>.md`). Omit this section if there is no parent source.

## Type

One of:

- **RFA** (ready-for-agent) — implementable and mergeable with no human interaction during the work; a human only reviews it afterward.
- **RFH** (ready-for-human) — a human is required *during* implementation (an architectural decision, a design review, a credential).

## Category

One of:

- **Build** — a vertical slice of the plan; the default.
- **Research** — a question answered from primary sources, not a slice of the build. Resolved by the `research` skill writing its findings to `ai/research/`; the acceptance criteria name what the findings must settle.
- **Decision** — a choice nobody has made yet. Resolved through a `grilling` session; the acceptance criteria name what must be decided. The outcome is recorded in the ticket, and a hard-to-reverse decision earns an ADR via `domain-modeling`.
- **Prototype** — a design question answered with throwaway code via the `prototype` skill. The acceptance criteria name the question the prototype must settle; the verdict and a pointer to the captured prototype are recorded in the ticket.

## Status

`Not started`

One of `Not started` | `In progress` | `Completed`. New tickets are always written as `Not started`; downstream skills advance this as the work moves.

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- A reference to the blocking ticket file (e.g. `ai/tickets/01-...md`)

Or "None — self-contained" if there are no blockers.

</ticket-template>

Do NOT close or modify any parent source.
