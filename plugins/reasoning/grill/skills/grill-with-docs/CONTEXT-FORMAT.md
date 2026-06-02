# CONTEXT.md format

`CONTEXT.md` is a **glossary** of the ubiquitous language for a single bounded context. It records what each term *means* — not how it is implemented. Keep it free of code, data shapes, APIs, and design decisions (those belong in ADRs).

## Document header

Start the file with a one-line statement of which context it covers:

```markdown
# Ordering — Context Glossary

The shared language for the ordering context. Each term below means exactly
one thing here; the same word may mean something different in another context.
```

## Term entries

One `##` heading per term. Terms are nouns from the domain, written in the casing the team speaks them in (e.g. `Order`, `Line Item`). Keep entries alphabetical.

```markdown
## Order

A customer's confirmed request to purchase one or more items. An Order exists
only after checkout completes; before that it is a Cart.

- **Synonyms:** Purchase (deprecated — prefer "Order")
- **Not to be confused with:** Cart (pre-checkout), Shipment (fulfilment unit)
- **States:** Placed → Paid → Fulfilled → Closed; may be Cancelled before Fulfilled
```

### Fields

Only the definition sentence is required. Add the optional bullets when they remove ambiguity:

- **Definition** — one or two present-tense sentences in plain domain language.
- **Synonyms** — words the team also uses for this concept; mark the canonical one.
- **Not to be confused with** — sibling terms people conflate with this one.
- **States** — the lifecycle, when the term has meaningful states.

## Rules

- **Glossary only.** No implementation details, schemas, file paths, or rationale.
- **One meaning per term.** If a word means two things, that is two terms — split and rename until each is unambiguous.
- **Define in domain language**, not in terms of the code that realises it.
- **Capture inline.** Add or sharpen an entry the moment a term is resolved, not in a later batch.
- **Cross-link** related terms by name so a reader can follow the language.
