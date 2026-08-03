---
name: implement
description: Build an approved issue or plan end to end, chaining tdd, simplify, review and commit. Use when the user approves a plan and wants it built, or asks to implement an issue.
---

# Implement

Build the approved work. This skill is the chain — each stage belongs to another skill, and this one runs them in order and keeps the suite honest between them.

It starts from work that is already understood and agreed: an issue with a plan the user approved, or a plan from the conversation. Selecting what to work on is `next-issue`'s job; judging whether it is finished is `complete-issue`'s.

## The chain

### 1. Ground the work

Read the issue in full — `What to build`, `Acceptance criteria`, `Type`, and any `Parent` spec — plus the approved plan. Read `CONTEXT.md` and the ADRs covering the area, so names match the project's language (see `domain-modeling`).

For a `HITL` issue, bring the user in at the points the plan identified. For `AFK`, drive it through.

### 2. Build it with `tdd`

Run the `tdd` skill. Confirm the seams before the first test, then work one vertical slice at a time: red → green, minimal code per test.

Run the affected test file after every slice, and the type checker as you go. Stay on red → green here — the tidying comes next.

### 3. Tidy it with `simplify`

Once the last slice is green, run the `simplify` skill over the code written in this session. This is the refactor step that `tdd` deliberately leaves out.

Re-run the tests and the type checker afterwards. Green again before moving on.

### 4. Check it with `review`

Run the `review` skill over the changes. Act on what it raises, or say plainly why a finding is being left — then run the full suite, not just the affected files.

### 5. Commit

Run the `commit` skill on the current branch.

## Done

The chain is complete when every stage has run, the full suite passes, and the work is committed. Hand off to `complete-issue` to judge the acceptance criteria against what was actually built — leave the criteria unticked and the status alone here.
