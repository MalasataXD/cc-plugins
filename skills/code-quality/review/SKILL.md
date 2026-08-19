---
name: review
description: Multi-dimension code review written to ai/reviews/. Use when the user asks for a code review, a quality check, or how a change could be improved.
---

# Code Review

Judge code on two axes: against the **standards** it should meet, and against the **spec** it was meant to satisfy. The standards axis is scored; the spec axis is a verdict.

## 1. Pin a fixed point

Settle exactly what is under review before reading anything: a ref (commit, branch, tag), a path, a directory, a named function, or the working tree. Confirm it resolves and that the diff is non-empty — an empty diff means say so and stop, rather than reviewing the whole repository by accident.

State the pinned scope in the report so the review can be repeated against the same thing.

## 2. Gather the standards

Standards apply in layers, highest precedence first:

1. **The project's own** — `AGENTS.md` / `CLAUDE.md`, `CONTRIBUTING.md`, style guides, and the ADRs covering the area. Documented project standards **override** everything below.
2. **The baseline** — the `code-smells` skill for structure, the `complexity` skill for the symptoms-and-causes lens, [security-checklist.md](references/security-checklist.md) for vulnerabilities.
3. **Language and community idioms**, plus the conventions of the surrounding code.

Skip anything a tool already enforces. A finding the formatter, linter, or type checker would fix is noise in a review — it belongs in the pipeline, not the report.

Read `CONTEXT.md` so findings use the project's own vocabulary (see `domain-modeling`).

## 3. Review in parallel

Dispatch sub-agents over **disjoint** dimensions, so one lens cannot colour another:

- **Security and performance** — the `security-checklist.md` sweep, algorithmic cost, resource handling, N+1s, caching that is missing or wrong.
- **Quality, style and documentation** — the code-level lens: the `code-smells` baseline, naming, project conventions, and whether public interfaces are documented.
- **Architecture and complexity** — the design-level lens: separation of concerns, dependency direction, and the `complexity` skill's vocabulary: interfaces whose obscurity or dependencies will surface as change amplification, cognitive load, or unknown unknowns for the next maintainer; complexity pushed onto callers that the implementation should absorb.
- **Spec compliance** — only when a spec or plan exists for this change (`ai/specs/`, a plan in the conversation, a commit message naming one) **and no ticket does**. Does the change do what was specified, no less and no more? When a ticket exists, skip this dimension: `complete-ticket` owns that verdict, and two verdicts on the same question can disagree.

Each sub-agent returns findings with concrete evidence — file, line, and what makes it a problem — plus a score per category it covered. Evidence states the rung it reached on the `prove-it` ladder; a review reports the rung, it does not enforce one.

Dispatch the three dimension agents in parallel. When spec compliance applies, dispatch it as soon as a slot frees if the environment caps concurrent sub-agents — it is the lightest of the four and never blocks the review.

**Aggregate verbatim.** Present each sub-agent's findings under its own heading without reranking or merging them. Cross-contamination is the thing the split exists to prevent.

## 4. Score the standards axis

Apply [scoring-rubric.md](references/scoring-rubric.md): score each category 0–100, weight them, round to a whole number.

Security 25% · Performance 15% · Quality & Maintainability 20% · Complexity 10% · Style & Standards 10% · Architecture & Design 10% · Documentation 10%

The spec axis stays out of the score. It reports its own verdict — **Met**, **Partial**, or **Not met** — because a change can be immaculate and still build the wrong thing.

## 5. Write the review

Write the report to a local markdown file — never to an external tracker.

1. Find `ai/` at the repository root; reuse it or create it.
2. Reviews go in `ai/reviews/`; reuse or create.
3. Name it with the date and a kebab-case slug of what was reviewed, e.g. `ai/reviews/2026-06-02-auth-service.md`. The date prefix keeps a history across re-reviews. Confirm before overwriting an existing file.

Report the path and the overall score to the user, so the result is both saved and visible at a glance.

<output-format>
# Code Review: <what was reviewed>

**Scope:** the pinned ref, path, or diff · **Date:** YYYY-MM-DD

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

**Spec compliance:** Met / Partial / Not met — one line, or "No spec found for this change."

## Strengths

- What the code does well, specifically.

## Priority issues

### 1. <title>

**Category:** … · **Where:** `path/file.ts:42`

Why it matters, then the current shape and the suggested one — code snippets only where prose is less precise.

### 2. …

## Remaining findings

Grouped under the dimension that raised them, verbatim from each reviewer.

## Summary

Two or three sentences: the state of the code and the highest-leverage next step.
</output-format>

## Judgement, not enforcement

Every entry in the baseline is a reason to look closer, not a rule that has been broken — say why *this* instance matters rather than citing the smell by name. Back every finding with evidence a reader can go and check, and report the strengths as specifically as the problems.
