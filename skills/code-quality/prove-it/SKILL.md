---
name: prove-it
description: The certainty ladder for evidence — name the fact a change is safe because of, and how far up the ladder it was pushed. Use when judging whether work is complete, backing a review finding with evidence, or when another skill needs the ladder.
---

# Prove It

The one ladder this workspace uses to grade evidence. Two skills reach for it at different moments:

- **`review`** reports it — each finding states the rung its evidence reached.
- **`complete-ticket`** enforces it — a behavioral criterion below **Ran it** is not Met.

Same ladder, so a review's "verified" and a ticket check's "verified" mean the same thing.

## The safety fact

Before grading anything, name **the one fact the change is safe because of** — the single claim that, if false, breaks the change. "The migration is idempotent." "No caller passes null here." "The old endpoint has no remaining consumers." A change without a nameable safety fact hasn't been understood yet; naming it is the first rung's price of entry.

## The ladder

Each rung is the same claim, held with more proof than the one below it:

1. **Asserted** — the claim was stated. Nothing backs it.
2. **Cited** — a specific line, config, or doc was pointed at. `path/file.ts:42` says so.
3. **Walked through** — the logic was traced end to end: this input takes this path and produces this result, shown step by step.
4. **Ran it** — a test, script, or command was executed and its output captured. The output is quoted, not summarized.
5. **Reproduced live** — the real surface was driven: the app launched, the endpoint called, the page rendered, and the behavior observed there.

State the rung by name. "Verified" without a rung is rung 1 wearing a costume.

## Which rung is enough

The riskier the claim, the higher the required rung. Rungs 1–3 are reasoning; rungs 4–5 are evidence. Reasoning is enough for claims the type checker or a cited line settles outright; anything **behavioral** — the code does X when Y happens — needs rung 4 or better, because walked-through logic is exactly where hidden assumptions hide. Rung 5 is for claims that only the real surface can settle: rendering, integration, environment.
