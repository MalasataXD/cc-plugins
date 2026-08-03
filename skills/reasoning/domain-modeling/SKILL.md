---
name: domain-modeling
description: Sharpen the project's domain language and capture the decisions behind it, maintaining a CONTEXT.md glossary and ADRs. Use when terminology is fuzzy, overloaded, or conflicts with the existing glossary, when a hard-to-reverse decision needs recording, or when another skill needs the project's domain vocabulary.
---

# Domain Modelling

One term, one meaning. This skill keeps the project's **ubiquitous language** sharp — the vocabulary the team, the docs, and the code all share — and records the decisions that shaped it.

## Where the documentation lives

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is warranted.

## Sharpening the language

**Challenge against the glossary.** When a term conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

**Sharpen fuzzy language.** When a term is vague or overloaded, propose a precise canonical one. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

**Discuss concrete scenarios.** Stress-test domain relationships with specific scenarios. Invent ones that probe edge cases and force precision about the boundaries between concepts.

**Cross-reference with code.** When someone states how something works, check whether the code agrees. Surface contradictions: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

## Capturing it

**Update `CONTEXT.md` inline.** The moment a term is resolved, write it down — capture as you go rather than batching. Format in [CONTEXT-FORMAT.md](./references/CONTEXT-FORMAT.md).

`CONTEXT.md` is a glossary and nothing else. It stays free of implementation details, and is not a spec, a scratch pad, or a home for implementation decisions.

**Offer ADRs sparingly.** An ADR is warranted only when all three hold:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and this one won for specific reasons

If any of the three is missing, skip it. Format in [ADR-FORMAT.md](./references/ADR-FORMAT.md).

## Reading it back

When another skill needs the project's vocabulary, `CONTEXT.md` is the source: name things the way the glossary names them, and respect the ADRs covering the area being touched.
