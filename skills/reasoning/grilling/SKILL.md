---
name: grilling
description: Interview the user relentlessly about a plan, decision, or design until you reach shared understanding. Use when the user wants to stress-test their thinking, or uses any "grill" trigger phrase.
---

# Grilling

Interview the user relentlessly about every aspect of this until you reach a shared understanding.

Map the work as a **design tree**: every decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are already settled — the questions answerable *now*, without guessing at answers you have not heard yet. Each answer settles a decision, pushes the frontier outward, and unblocks the questions that depended on it.

For every question, give your recommended answer.

The session is done when the frontier is empty: every branch visited, nothing left silently assumed. Hold off on acting until the user confirms you have reached that shared understanding.

## Cadence

Two ways to walk the tree. **Serial** is the default; use **batch** when the caller asks for it.

- **Serial** — one question at a time, waiting for the answer before the next. Deepest resolution per question, and the user can redirect at any point.
- **Batch** — the whole frontier in one round: number each question, give each a recommended answer, then wait for the round's answers before recomputing the frontier. Fewer turns over a wide tree. A question that depends on another still open in this round belongs to a *later* round.

## Facts are yours, decisions are theirs

When a question needs a fact from the environment, find it — explore the codebase, read the files, run the tools — rather than asking the user for something you could look up.

In batch cadence, dispatch a sub-agent for the lookup and keep going: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait. Ask the rest of the frontier now.

The decisions stay the user's. Put each one to them and wait.

## Domain language

When `CONTEXT.md` or `CONTEXT-MAP.md` exists, read it, hold the user to the vocabulary it defines, and offer to bring in the `domain-modeling` skill so resolved terms and hard-to-reverse decisions get captured as you go.
