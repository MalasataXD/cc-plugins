# Finding Format

The return contract for the dimension reviewers. Paste this whole file into every sub-agent prompt verbatim: the structure is fixed, the wording inside it is the reviewer's own.

## Finding block

```markdown
### <title: name the problem, not the category>

**Recommendation:** Act on / Consider / Noted · **Category:** <rubric category, Bugs, or Spec> · **Where:** `path/file.cs:42` · **Evidence rung:** <prove-it rung>

Why it matters, then the current shape and the suggested one, with code snippets only where prose is less precise.
```

- **Recommendation** is a proposal. The orchestrator assigns the final **Verdict** when aggregating; the wording of the finding is never edited in the process.
- **Where** lists every implicated `file:line`, comma-separated.
- **Evidence rung** names the rung the evidence reached on the `prove-it` ladder.
- A secret is cited by its location, never its value.
- A problem the change neither caused nor worsened is pre-existing. Start its title with `Pre-existing:`, recommend **Noted** or **Consider**, and leave it out of your scores.

## Recommendations

- **Act on**: fix before this ships.
- **Consider**: worth doing, can wait.
- **Noted**: an observation, no action expected.

## Return envelope

Each sub-agent returns exactly this shape:

```markdown
## Findings

<finding blocks, or the single line "No findings.">

## Scores

- <Category>: X/100 or N/A, plus the findings that cost it

## Strengths

- Specific strengths, each with `file:line` where applicable.

<closing line: what was and wasn't run, and anything you could not assess, e.g. "Read-only review; no tests were run.">
```

Scores are 0–100 or `N/A` (the rubric's scale), one line per category the dimension covers, and nothing else is scored. A dimension with no rubric category returns no `## Scores` section.

## Spec verdict

The spec compliance reviewer adds a `## Spec verdict` section to its envelope, with one verdict and one line of reasoning:

- **Met**: It does everything specified and nothing outside it.
- **Partial**: It reaches the goal, with gaps or unrequested additions.
- **Not met**: It misses the goal or builds something else.
