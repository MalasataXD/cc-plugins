---
name: vet-issues
description: Pressure-test issues by reading each one through the eyes of an implementer picking it up cold, then report what would block them. Use when the user wants to sanity-check issues before handing them off, find gaps in a breakdown, or ask "would this make sense to whoever grabs it". Read-only — findings are shown directly in the conversation, never written to a file.
---

# Vet Issues

Pressure-test a set of issues by simulating the person who will actually implement them. For each issue, put yourself in the shoes of an implementer who is grabbing it **cold** — no access to the conversation that produced it, only the issue text and the codebase. Ask: *Can I tell what to build? Do I know where to start? Will I have to guess at a decision nobody made?* Then report what would trip them up.

This is **read-only**. Do NOT edit, annotate, or rewrite the issues. Do NOT write a report file. Present every finding directly in the conversation. The user fixes the issues themselves — your job is to surface the gaps, not to paper over them by inventing answers.

## Process

### 1. Locate the issues

Work out which issues to vet:

1. If the user passes a path or glob (a single issue file, a folder, or a pattern), use that.
2. Otherwise default to `ai/issues/` at the repository root.
3. If no issues are found, say so and stop — there is nothing to vet.

Read the full body of every issue in scope before judging any of them. The cross-issue checks in step 4 need the whole set in view.

### 2. Explore the codebase (lightly)

Skim the codebase enough to judge whether an issue's "where do I start" is *answerable from the code* or genuinely *missing*. Use the project's domain glossary vocabulary so your findings speak the same language as the issues. You are not implementing anything — just calibrating what a competent implementer could reasonably figure out on their own.

### 3. Vet each issue through an implementer's eyes

For each issue, walk the checklist below. The goal is to find the moment an implementer would **stall** — the first question they cannot answer from the issue plus the codebase.

<implementer-checklist>
- **Goal clarity** — Can I state, in one sentence, what "done" looks like? Or is the intent ambiguous?
- **Starting point** — Do I know where to begin? The issue need not name files (it shouldn't), but the area should be identifiable from domain vocabulary, existing seams, or the codebase. If I'd have to guess *which* part of the system this even touches, that's a gap.
- **Acceptance criteria** — Are the criteria concrete and verifiable, or vague ("works well", "handles errors")? Could two implementers disagree on whether a criterion is met?
- **Scope boundaries** — Do I know what is explicitly NOT in this slice? Where is the risk of scope creep?
- **Undecided decisions** — Is there a choice the issue assumes is made but never states (a data shape, an edge-case behavior, a UX detail)? These are the dangerous ones: an implementer will silently guess and may guess wrong.
- **Self-containedness & dependencies** — Can this actually be started alone? If it declares a blocker, does the blocker exist and come first? If it declares none, is that true?
- **Verifiability** — Could the implementer demo or test this slice on its own, as the tracer-bullet model intends?
</implementer-checklist>

<signal-vs-noise>
Distinguish a **genuine gap** from **healthy exploration**:

- A genuine gap is a decision nobody made that the implementer must invent to proceed (e.g. "what happens when the balance is negative?" with no answer anywhere). Flag these.
- Healthy exploration is work the implementer is *supposed* to do — reading the code to find the right function, choosing a variable name, picking an obvious idiom. Do NOT flag these. Issues that avoid file paths and code snippets are following the `to-issues` design on purpose; needing to read the code is not a defect.

When in doubt, ask: *would a competent implementer have to guess at something the author actually knew?* If yes, it's a gap. If they'd just have to look, it's fine.
</signal-vs-noise>

Give each issue a one-word **verdict**:

- **Ready** — an implementer could pick this up and start with no clarification.
- **Needs work** — implementable, but they'd hit one or more questions worth resolving first.
- **Blocked** — they could not meaningfully start; a core decision or dependency is missing.

### 4. Check the set as a whole

After the per-issue pass, look across all issues:

- **Dependency sanity** — Are there cycles? Does anything depend on an issue that does not exist? Is the ordering coherent?
- **Coverage gaps** — Does the plan have an obvious hole between issues (a step everyone assumes someone else owns)?
- **Overlap** — Do two issues claim the same work, risking a collision?
- **Granularity drift** — Is one issue a thin slice while another secretly bundles five?

### 5. Report the findings directly

Present everything in the conversation using the format below. Be specific: quote the issue, name the exact question an implementer would ask, and suggest concretely how the author could resolve it — **as a question to answer or a sentence to add, never as a decision you invent for them.** Lead with the verdict so the state of the breakdown is clear at a glance.

<output-format>
## Issue vet: <scope, e.g. ai/issues/ (5 issues)>

| Issue | Verdict |
| --- | --- |
| 01-account-balance-endpoint.md | Ready |
| 02-balance-display.md | Needs work |
| 03-... | Blocked |

### 01-account-balance-endpoint.md — Ready
Brief note on why it holds up. Skip the detail subsections when an issue is clean.

### 02-balance-display.md — Needs work
- **Where they'd stall:** the first question an implementer hits, quoted against the issue.
- **Gap:** what decision is missing or what criterion is too vague.
- **Suggested fix:** the question the author should answer, or the sentence to add. Do not answer it yourself.

### Across the set
- Dependency, coverage, overlap, or granularity findings — or "No cross-issue problems found."

### Bottom line
One or two sentences: is this breakdown ready to hand off, and what is the highest-leverage thing to fix first?
</output-format>

Do NOT modify any issue file. Do NOT write the report to disk.
