---
name: review
description: Use when reviewing a change or an area of code, or asked for a quality check.
---

# Code Review

Judge code on two axes:
- The **standards** it should meet, scored with the [scoring-rubric](references/scoring-rubric.md)
- The **spec** it is meant to satisfy, settled as a verdict

## Workflow

### 1. Pin the target

Settle exactly what you are reviewing before reading anything: a ref (commit, branch, tag, pull request), a path, a directory, a named function, or the working tree. Confirm that it resolves, then fix what it means:

- **A ref**: resolve it to a base SHA and a head SHA. The base is the parent for a commit or tag, and the merge base with the target branch for a branch or pull request. Review a ref that isn't checked out from a worktree at its head, so callers and line numbers match.
- **The working tree**: HEAD plus staged, unstaged, and untracked files.
- **A path, directory, or function**: the code as it stands at the current head SHA.

If a ref or the working tree has an empty diff, say so and stop, so the review stays inside its target.

State the pinned target and its SHAs in the report, so the review is repeatable against the same code.

### 2. Gather the **standards**

Standards apply in 3 layers, highest precedence first:

1. **The project's own**: Look for `CODING_STANDARDS.md`, `AGENTS.md` / `CLAUDE.md`, `CONTRIBUTING.md`, style guides, and the ADRs covering the area. Documented project standards **override** the layers below.
2. **The baseline**: Use the `code-smells` skill for structure, the `complexity` skill for symptoms and causes, the [security-checklist](references/security-checklist.md) for vulnerabilities.
3. **Language and community idioms**, plus the conventions of the surrounding code.

Skip anything a tool already enforces: a finding the formatter, linter, or type checker would fix belongs in the pipeline, not the report.

Read the project glossary, so findings can use the project's own vocabulary (see the `domain-modeling` skill).

### 3. Run the project's checks

Run the project's tests, linter, and type checker once, before any sub-agent starts, and keep the output for the brief. Record any check that can't run and why.

### 4. Review in parallel

Use one sub-agent per dimension, so one lens cannot colour another:

1. **Bugs**: find inputs or states where the code does the wrong thing, judged against what its names, types, tests, and callers promise. Read the callers and failure paths, not only the diff. Check that tests cover the changed behaviour and weren't weakened to pass, and check the effect on existing data, consumers outside the repository, and rollback. Name the `prove-it` safety fact and its rung. Every finding names the scenario: what goes in, what happens, and what should happen.
2. **Security and Performance**: the [security-checklist](references/security-checklist.md), algorithm cost, resource handling, N+1s, caching that is missing or wrong.
3. **Quality, Style and Documentation**: the `code-smells` baseline, naming, project conventions, and whether public interfaces are documented.
4. **Architecture and Complexity**: the `complexity` skill and its references, separation of concerns, dependency direction, change amplification, cognitive load, unknown unknowns.
5. **Spec compliance** (*Optional*): Only when a spec or plan exists for the change (`<work folder>/specs/`, a plan in the conversation, a commit message naming one) and no ticket does. Does the change do what was specified, no less and no more? A ticket's verdict belongs to `complete-ticket`.

Give every sub-agent the same brief, built from the written record so the author's reasoning can't anchor it:

- The pinned target and the output of the project's checks.
- The gathered standards and the glossary.
- The stated intent: commit messages, the pull request description, and any spec or plan.
- Its dimension, plus the rubric's opening rules and the sections for its categories.
- All of [finding-format](references/finding-format.md), pasted verbatim, so all dimensions come back in one shape.
- These rules: work read-only, treat a baseline entry as a reason to look closer, and say why this instance matters, with evidence a reader can check (file, line, and what makes it a problem). Evidence states the rung it reached on the `prove-it` ladder; a review reports the rung and enforces none.

Dispatch every dimension that applies in parallel. Re-dispatch a sub-agent once if it fails or returns a malformed envelope. If it fails again, mark its categories `Not assessed` and record that under Coverage. This step is done when every dimension has an envelope or is recorded as not assessed.

### 5. Aggregate the results

Copy each finding through verbatim, then give it one verdict in place of the reviewer's **Recommendation**: **Act on**, **Consider**, or **Noted**, as defined in [finding-format](references/finding-format.md), or **Dismissed**.

**Dismissed** means wrong, out of scope, or a duplicate. Keep it as one line with the reason, backed by evidence at **Cited** or better. When findings share a root cause, keep the strongest and dismiss the rest as `duplicate of <title>`.

This step is done when every returned finding has a verdict.

### 6. Score the **standards** axis

Apply the [scoring-rubric](references/scoring-rubric.md) to the sub-agents' scores to get the overall score. When a dismissed finding cost a category points, first re-score that category from its surviving findings.

### 7. Settle the **spec** axis

When the spec compliance sub-agent ran, report the verdict from its envelope.

The spec axis stays out of the score, because a change can be immaculate and still build the wrong thing.

### 8. Write the review

Save the report as a local markdown file at `<work folder>/reviews/YYYY-MM-DD-<slug>.md`, creating the folder if it is missing and confirming before overwriting a file. The project's `AGENTS.md` or `CLAUDE.md` names the work folder; when it names nothing, use `.ai/` at the repository root.

Pass the connective prose through the `unslop` skill before saving, leaving each finding in its reviewer's wording. Then report the path and overall score to the user.

<output-format>
# Code Review: <what was reviewed>

> <date and time of the review> · <model slug>

**Scope:** the pinned target and its SHAs.

## Overall: X/100

| Category | Score | Weight |
| --- | --- | --- |
| Security | X | 25% |
| Performance | X | 15% |
| Quality & Maintainability | X | 20% |
| Complexity | X | 10% |
| Style & Standards | X | 10% |
| Architecture & Design | X | 10% |
| Documentation | X | 10% |

**Spec compliance:** Met / Partial / Not met, with one line of reasoning. Or "Not assessed: no spec found." Or "Not assessed: a ticket exists (<ticket paths>), see `complete-ticket`."

**Coverage:** the checks that ran and their results, what the sub-agents could not assess, and any dimension recorded as not assessed.

## Summary

Two or three sentences: the state of the code, the safety fact and its rung, and the highest-leverage next step.

## Strengths and Weaknesses

**Strengths**
- Up to five specific things the code does well.

**Weaknesses**
- Up to five patterns that span several findings, each pointing at those findings by number.

## Act on first

- The number and title of each **Act on** finding. Omit the section when there are none.

## Findings

Each finding not dismissed is its reviewer's block from [finding-format](references/finding-format.md), with **Recommendation** replaced by **Verdict**. Order them Act on, Consider, Noted, keeping each reviewer's order within a verdict, and number them from 1 in that order as `### <n>. <title>`.

## Dismissed

- One line per dismissed finding: what was raised, and why it doesn't apply. Omit the section when nothing was dismissed.
</output-format>
