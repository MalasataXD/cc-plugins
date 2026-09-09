---
name: implement
description: Build an approved ticket or plan end to end. Use when the user approves a plan and wants it built, or asks to implement a ticket.
---

# Implement

Build the approved work. This skill is the chain — each stage belongs to another skill, and this one runs them in order and keeps the suite honest between them. `simplify` always runs; `tdd` runs where the code has a seam to test at; `review` runs when the change is big.

It starts from work that is already understood and agreed: a ticket with a plan the user approved, or a plan from the conversation. Selecting what to work on is `next-ticket`'s job; judging whether it is finished is `complete-ticket`'s. Coming straight from `next-ticket`, the ticket, its parent spec, and the codebase are already in context; when they are not, read the ticket and the plan before building.

## When the plan runs out

Plans are approved with gaps in them, and the gaps surface at every stage below — mid-build, mid-tidy, mid-review. Whenever one does, sort it into one of two kinds:

- **A fact** — how the existing code behaves, what an interface accepts, which pattern the project already uses. Finding it is your job: read the code, run the tests, check the docs, then carry on.
- **A decision** — anything with more than one defensible answer that the plan did not settle. That one is the user's.

On a decision, stop before writing code that assumes an answer, and put it to them: what you hit, the options, and your recommendation. One decision is a question; several tangled ones are a `grilling` session. Resume from where you stopped once it is settled.

Capture what comes back where it belongs: a resolved term or a hard-to-reverse choice goes to `domain-modeling`, and anything that moves the acceptance criteria gets flagged for `complete-ticket` rather than quietly absorbed.

## The chain

### 1. Build it

For a `RFH` ticket, bring the user in at the points the plan identified. For `RFA`, drive it through.

`tdd` is the default where the code has a seam the project already tests at — a service, a handler, a reducer, a pure function. Run the `tdd` skill: confirm the seams before the first test, then red → green, minimal code per test, the affected test file after every cycle and the type checker as you go.

Where there is no such seam — UI components, styling, wiring, configuration, a rename — build it directly and verify it the way the project verifies that kind of change (the type checker, a lint pass, running the app). Say in one line which path was taken and why.

### 2. Tidy it with `simplify`

Once the build is green, run the `simplify` skill over the code written in this session. This is the refactor step that `tdd` deliberately leaves out, and it runs every time.

Re-run the tests and the type checker afterwards. Green again before moving on.

### 3. Review it when the change is big

Run the `review` skill when any of these hold, and skip it with a one-line note otherwise:

- The change touches more than five files, or crosses a module boundary.
- It changes a schema, a public interface, or an API contract.
- The ticket is `RFH`, or a decision came up during the build.

The user can ask for a review at any size. When it runs, act on what it raises, or say plainly why a finding is being left.

## Done

The chain is complete when the stages that apply have run and the full suite passes — the full suite, not just the affected files. Continue straight into `complete-ticket` — the approval that started this chain covers the whole run through it, and the only stops along the way are the decisions described in [When the plan runs out](#when-the-plan-runs-out). Do **not** commit here — the work has not been judged yet. `complete-ticket` verifies the acceptance criteria against what was actually built and offers the `commit` once they hold. Leave the criteria unticked and the status alone here.
