---
name: complete-issue
description: Review the changes made for an issue against its acceptance criteria and report what is done and what is left before it can be called finished. Use when the user has finished (or thinks they have finished) work on an issue and wants to confirm it is actually complete. Read-only by default — offers to update the issue's status and tick verified criteria only after the user confirms.
---

# Complete Issue

Check whether the work done for an issue actually satisfies it. Walk each acceptance criterion against the real changes, and report — honestly — what is done, what is partial, and what is still missing. The goal is a trustworthy answer to "is this issue finished?", not a rubber stamp.

This is **read-only by default**. Assess and report first. Do NOT edit the issue, tick criteria, or change its status as part of the assessment. Only after presenting the state and getting the user's confirmation may you record completion (see step 5). Never invent evidence: if you cannot see that a criterion is met, it is not met.

## Process

### 1. Identify the issue

Work out which issue is being verified:

1. If the user names a specific issue file, use it.
2. Otherwise infer it from the conversation, the current changes (`git status` / `git diff`), and the `In progress` issues under `ai/issues/`.
3. If it is still ambiguous — several open issues, no clear signal — ask which one to check rather than guessing.

Read the full issue: `Type`, `What to build`, `Acceptance criteria`, `Blocked by`, and any `Parent`.

### 2. Survey the actual changes

Look at what was really done, not what was intended. Inspect the working tree and diff (`git status`, `git diff`, and the relevant files) to see the changes in scope. Run the tests or the app where that is the only way to confirm a behavioral criterion — but stay within verification; do not fix or extend the implementation here.

### 3. Judge each acceptance criterion

For every criterion in the issue, assign one state and back it with concrete evidence:

- **Met** — the change demonstrably satisfies it. Point to the file, function, or test that proves it.
- **Partial** — started but incomplete, or met only for the happy path. Say exactly what is missing.
- **Not met** — no evidence it was addressed.
- **Unverifiable** — you cannot confirm it from here (needs a manual step, an environment you lack, a human judgment). Say what would verify it.

Also sanity-check beyond the checklist: does the change match `What to build`? Did it stay inside the slice's scope, or drift? Are there obvious regressions, missing tests, or loose ends an implementer would be embarrassed to ship?

### 4. Report the state directly

Present the assessment in the conversation using the format below. Lead with a clear verdict so the answer to "is it done?" is visible immediately.

<output-format>
## Issue check: <filename> — <title>

**Verdict:** Complete / Almost there / Not done — one line.
**Type:** AFK / HITL · **Current status:** In progress

### Acceptance criteria
| Criterion | State | Evidence / what's missing |
| --- | --- | --- |
| Criterion 1 | Met | `path/thing.ts` does X; covered by `thing.test.ts` |
| Criterion 2 | Partial | happy path done; error case in <area> not handled |
| Criterion 3 | Not met | no change addresses this |

### What's left to finish
- The concrete, ordered remaining work — or "Nothing; all criteria met." Frame each as an actionable step.

### Beyond the checklist
- Scope drift, missing tests, regressions, or loose ends — or "None spotted."
</output-format>

### 5. Offer to record completion

After presenting the state, offer to update the issue file — and do it only if the user confirms:

- If every criterion is **Met**, offer to tick the `- [ ]` acceptance boxes and move `## Status` to `Completed`.
- If some criteria are met and others are not, offer to tick only the verified boxes and leave the status as `In progress`.
- If little is done, record nothing — just report.

Apply only the edits the user approves: tick the agreed boxes and set the agreed status. Make no other changes to the issue, and never modify the parent source.
