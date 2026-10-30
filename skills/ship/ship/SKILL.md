---
name: ship
description: Use when deciding whether finished work is ready to ship.
---

# Ship

A **gate** for finished work. `review` and `complete-ticket` judge the work; this skill reads their results and derives **Ready** or **Not ready**. Each gate is a yes or no read from the record, so two runs reach the same verdict. The score stays out of it, because a weighted average can hide a critical finding.

This skill ends at the verdict, so the user decides what happens next.

## Process

### 1. Pin the branch

Take `HEAD` as the head, and the merge base with the target branch as the base. The target is the branch the user names, otherwise the default branch. If the diff is empty, say so and stop.

Only committed work is judged. Note any uncommitted files for the report.

### 2. Find a current review

Look in `<work folder>/reviews/` for the newest report whose **Scope** shows this base and head. The project's `AGENTS.md` or `CLAUDE.md` names the work folder; when it names nothing, use `.ai/` at the repository root.

When no report matches, run `review` on the pinned range. A working-tree report or an older head doesn't count, because the code it judged may not be the code being shipped.

### 3. Apply the gates

Read the report and apply every gate. A gate passes only on what the record states, so a missing or unclear line fails it.

| Gate | Passes when | When it fails |
| --- | --- | --- |
| **Findings** | The report has no `## Act on first` section. | Fix the findings, commit, and run `ship` again. |
| **Checks** | **Coverage** shows that every check the project has ran and passed. | Fix the failure, commit, and run `ship` again. |
| **Coverage** | **Coverage** records no dimension as not assessed. | Run `review` again. |
| **Spec** | **Spec compliance** is **Met**, or "Not assessed". | Close the gap, commit, and run `ship` again. |
| **Tickets** | Every ticket **Spec compliance** names has the `Status` `Completed`. With no ticket named, this passes. | Run `complete-ticket`. |

This step is done when every gate has a result.

### 4. Report the verdict

The verdict is **Ready** only when every gate passes. Present it in the conversation:

<output-format>
## Ship check: <branch> (<short base>..<short head>)

**Verdict:** Ready / Not ready

**Review:** `<report path>`

| Gate | Result | Evidence |
| --- | --- | --- |
| Findings | Pass / Fail | The titles of the **Act on** findings, or "None". |
| Checks | Pass / Fail | Each check and its result. |
| Coverage | Pass / Fail | The dimensions not assessed, or "All assessed". |
| Spec | Pass / Fail | The verdict, or why it was not assessed. |
| Tickets | Pass / Fail | Each ticket and its status, or "None named". |

**Next:** `file-pr` when **Ready**. Otherwise, the fix for each failed gate, in table order.

**Uncommitted:** The files left out of this check. Omit the line when there are none.
</output-format>
