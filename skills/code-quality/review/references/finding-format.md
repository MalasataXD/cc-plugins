# Finding Format

The return contract for the dimension reviewers. Paste the finding block and the return envelope into every sub-agent prompt verbatim: the structure is fixed, the wording inside it is the reviewer's own.

## Finding block

```markdown
### <title — name the problem, not the category>

**Recommendation:** Act on / Consider / Noted · **Category:** <rubric category> · **Where:** `path/file.cs:42` · **Evidence rung:** <prove-it rung>

Why it matters, then the current shape and the suggested one — code snippets only where prose is less precise.
```

- **Recommendation** is a proposal. The orchestrator assigns the final **Verdict** when aggregating ("tag, don't rerank"); the wording of the finding is never edited in the process.
- **Where** lists every implicated `file:line`, comma-separated.
- **Evidence rung** names the rung the evidence reached on the `prove-it` ladder.

## Return envelope

Each sub-agent returns exactly this shape:

```markdown
## Findings

<finding blocks, or the single line "No findings.">

## Scores

- <Category>: X/100

## Strengths

- Specific strengths, each with `file:line` where applicable.

<closing line: what was and wasn't run, e.g. "Read-only review; no tests were run.">
```

Scores are 0–100 — the rubric's scale — one line per category the dimension covers, and nothing else is scored.
