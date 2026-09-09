---
name: complete-ticket
description: Check a ticket's changes against its acceptance criteria. Use when the user thinks a ticket is finished and wants to confirm it.
---

# Complete Ticket

Check whether the work done for a ticket actually satisfies it. Walk each acceptance criterion against the real changes and report what is met and what is not. The goal is a trustworthy answer to "is this ticket finished?", not a rubber stamp.

This judges a **ticket** against its criteria; `handoff` transfers a **conversation** to another agent. Reach for that one instead when the work is unfinished and someone else is picking it up.

Never invent evidence: if you cannot see that a criterion is met, it is not met.

## Process

### 1. Identify the ticket

1. If the user names a specific ticket file, use it.
2. Otherwise infer it from the conversation, the current changes (`git status` / `git diff`), and the `In progress` tickets under `<work folder>/tickets/`. The project's `AGENTS.md` or `CLAUDE.md` names the work folder; when it names nothing, use `.ai/` at the repository root.
3. If it is still ambiguous — several open tickets, no clear signal — ask which one to check rather than guessing.

Read the full ticket: the `Type`, `Category`, and `Status` lines under the title, `What to build`, `Acceptance criteria`, `Blocked by`, and the `Parent` spec. The Category names where the evidence lives: a Build ticket's evidence is the diff and tests; a Research ticket's is the findings file under `<work folder>/research/`; a Decision ticket's is the recorded outcome, and the ADR if one was warranted.

### 2. Dispatch a cold read

The judgment itself goes to a sub-agent, not this conversation. This session often *wrote* the changes being judged — the `implement` chain ends here — and an author checking its own work against the criteria reads the ticket through the lens of what it built, not what was asked. The sub-agent gets exactly two things: the ticket file and the scope of the changes (the ref, branch, or list of touched paths). No conversation history, no plan, no explanation of intent.

The sub-agent surveys what was really done, not what was intended: the working tree and diff (`git status`, `git diff`, and the relevant files). It runs the tests or the app where that is the only way to confirm a behavioral criterion — but stays within verification; it does not fix or extend the implementation.

### 3. Judge each acceptance criterion

The sub-agent gives every criterion one of two states, backed with concrete evidence graded on the `prove-it` ladder, the rung stated in the report:

- **Met** — the change demonstrably satisfies it. Point to the file, function, or test that proves it. A behavioral criterion is Met only at **Ran it** or higher.
- **Not met** — anything short of that. Say what is missing: the work itself, the error path, or the proof — when a criterion cannot be verified from here (a manual step, an environment you lack, a human judgment), it is Not met, and the evidence column names what would verify it.

It also sanity-checks beyond the checklist: does the change match `What to build`? Did it stay inside the ticket's scope, or drift? Are there obvious regressions, missing tests, or loose ends an implementer would be embarrassed to ship? For anything risky the criteria don't cover, name the safety fact from `prove-it` — the one fact the change is safe because of — and the rung it reached.

### 4. Report the state

Present the sub-agent's assessment in the conversation using the format below, without softening its verdicts — the cold read is the point.

<output-format>
## Ticket check: <filename> — <title>

**Verdict:** Complete / Not done — one line.
**Type:** RFA / RFH · **Category:** Build / Research / Decision

### Acceptance criteria
| Criterion | State | Evidence / what's missing |
| --- | --- | --- |
| C1 | Met | `path/thing.ts` does X; covered by `thing.test.ts` (Ran it) |
| C2 | Not met | happy path done; error case in <area> not handled |
| C3 | Not met | needs a manual check of <thing>; no change addresses it |

### What's left to finish
- The concrete, ordered remaining work — or "Nothing; all criteria met."

### Beyond the checklist
- Scope drift, missing tests, regressions, or loose ends — or "None spotted."
</output-format>

### 5. Record the verdict

The verdict is **Complete** only when every criterion is Met. Then tick every `- [ ]` acceptance box and set the `Status` line to `Completed` — that records what the report already said, and it is the only edit made to the ticket. The parent spec is never modified.

If the ticket was the last open one in its phase (the `[P<x>]` title prefix; the other tickets of the phase sit beside it), say so and name the phase's verifiable state from the spec's `## Phases` map: this is the moment the user can check the feature end to end.

On **Not done**, change nothing and leave the report as the answer.

### 6. Offer to commit

When the verdict is Complete and the working tree still holds uncommitted changes from the ticket, ask once whether to finish with the `commit` skill. Skip the question when the tree is already clean.
