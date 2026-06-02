# ADR format

An **Architecture Decision Record** captures one significant decision: the context that forced it, the choice made, and the consequences accepted. One decision per file. Records are immutable — when a decision changes, write a new ADR that supersedes the old one rather than editing history.

## File location and naming

- System-wide decisions: `docs/adr/`
- Context-specific decisions: the context's own `docs/adr/` (see the file structure in the skill)
- Filename: `NNNN-short-kebab-title.md`, where `NNNN` is the next zero-padded sequential number (`0001`, `0002`, …).

## Template

```markdown
# NNNN. Short title in the imperative ("Use Postgres for the write model")

- **Status:** Proposed | Accepted | Superseded by [NNNN](NNNN-....md) | Deprecated
- **Date:** YYYY-MM-DD

## Context

The forces at play: the problem, the constraints, the requirements, and the
relevant facts. Written so a future reader who wasn't in the room understands
*why a decision was needed*. State the genuine alternatives that were on the table.

## Decision

The choice that was made, stated plainly and actively: "We will …". Include the
key reasons this option won over the alternatives.

## Consequences

What becomes easier and what becomes harder as a result. Capture the trade-off
honestly — the costs accepted, new constraints introduced, and follow-on work
created — not just the benefits.
```

## Rules

- **One decision per record.** If you're documenting two choices, write two ADRs.
- **Immutable.** Don't rewrite an accepted ADR; supersede it and flip the old one's status to `Superseded by …`.
- **Only when it earns its place.** An ADR is warranted only when the decision is hard to reverse, surprising without context, and the result of a real trade-off. If any of those is missing, skip it.
- **Imperative title** naming the decision, not the problem ("Use event sourcing for orders", not "How to store orders").
- **Date in `YYYY-MM-DD`.**
