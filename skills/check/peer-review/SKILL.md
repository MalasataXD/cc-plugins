---
name: peer-review
description: Ask a model from the other provider for a cold read, fix what is clear, and present the rest.
disable-model-invocation: true
---

# Peer Review

An unanchored second opinion. A **peer** from the other provider reads the target cold. This session judges what comes back, fixes the clear findings, and hands the rest to the user.

## Process

### 1. Pin the target

Settle what the peer reads: a ref, a pull request, a path, a document, or the working tree. Take the question from the user, or ask "Is anything wrong or missing?" when they gave none.

### 2. Dispatch the peer

Use the model the user named, otherwise the other provider's strongest: Sol from Claude, Opus from Codex. Set its effort to `high`, and dispatch one read-only reviewer without sub-agents through the harness's delegation tool (`delegate_task` in T3). When the harness can't reach another provider, say so and stop.

The brief carries only:

- The target and the question.
- The finding block and recommendation definitions from the `review` skill's `references/finding-format.md`, with no scores.
- A request for real problems only, ranked by impact, stating which ones it is less sure of.

Leave out the conversation history, the author's reasoning, and any earlier version of the target, because the peer's value is that it starts unanchored.

If the peer fails or returns nothing usable, re-dispatch it once. If it fails again, say so and stop. This step is done when the peer has returned its findings.

### 3. Look over the findings

Check each finding against the target, then give it one verdict: **Act on**, **Consider**, or **Noted**, as defined in `finding-format.md`, or **Dismissed**. **Dismissed** means wrong or out of scope, backed by evidence at **Cited** or better on the `prove-it` ladder. Keep the peer's wording and its order.

This step is done when every finding has a verdict.

### 4. Fix what is clear

Fix each **Act on** finding that has one obvious fix, run the project's checks, and commit with the `commit` skill. Leave pushing to the user. A finding that needs a design choice goes to the user instead.

Fix only the user's own work in this checkout. On anything else, such as a teammate's pull request, present every finding and change nothing.

### 5. Present the rest

Report in the conversation, omitting any section with nothing in it:

<output-format>
## Peer review: <target>

**Peer:** <model and effort> · **Question:** <the question>

### Fixed

The peer has not read these fixes.

- <title>: what changed, in `<short sha>`.

### For you to decide

Each remaining **Act on** and **Consider** finding in the peer's wording, with its verdict and your recommendation.

### Noted

- One line per finding.

### Dismissed

- One line per finding: what was raised, and the evidence against it.
</output-format>
