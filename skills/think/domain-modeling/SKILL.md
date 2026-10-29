---
name: domain-modeling
description: Use when a term is fuzzy or clashes with the glossary, or a hard-to-reverse decision needs recording.
---

# Domain Modeling

One term, one meaning. This skill keeps the project's **ubiquitous language** sharp (the vocabulary the team, the docs, and the code all share) and records the decisions that shaped it.

## Where the documentation lives

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

In a mapped repo, **the glossary** means the one the map lists for the context you are working in. A term from a context the map doesn't cover gets a new glossary beside the map's existing ones, and its own row in the map.

Create files lazily, only when you have something to write. If the repo has no glossary yet, create `GLOSSARY.md` when the first term is resolved; in a mapped repo, follow the rule above. If no `docs/adr/` exists, create it when the first ADR is warranted.

## Sharpening the language

**Challenge against the glossary.** When a term conflicts with the existing language in the glossary, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

**Sharpen fuzzy language.** When a term is vague or overloaded, propose a precise canonical one. "You're saying 'account'. Do you mean the Customer or the User? Those are different things."

**Discuss concrete scenarios.** Stress-test domain relationships with specific scenarios. Invent ones that probe edge cases and force precision about the boundaries between concepts.

**Cross-reference with code.** When someone states how something works, check whether the code agrees. Surface contradictions: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

## Capturing it

**Update the glossary inline.** The moment a term is resolved, write it down. Capture as you go rather than batching. Format in [GLOSSARY-FORMAT.md](./references/GLOSSARY-FORMAT.md).

The glossary is a glossary and nothing else. It stays free of implementation details, and is not a spec, a scratch pad, or a home for implementation decisions.

**Offer ADRs sparingly.** An ADR is warranted only when all three hold:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and this one won for specific reasons

If any of the three is missing, skip it. Format in [ADR-FORMAT.md](./references/ADR-FORMAT.md).

## Reading it back

When another skill needs the project's vocabulary, the glossary is the source: name things the way the glossary names them, and respect the ADRs covering the area being touched.
