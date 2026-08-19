---
name: complexity
description: A ledger for weighing complexity against value. Use when planning or specing a new solution, when a plan element feels like a shortcut or special case, or when another skill needs the complexity vocabulary.
---

# Complexity

**Complexity is anything about a system's structure that makes it hard to understand or modify.** Not size, not sophistication — difficulty of change. Use this vocabulary when planning a solution, so complexity is spent deliberately instead of accumulated by accident.

## The three symptoms

How complexity is felt by whoever works on the system next:

**Change amplification** — one conceptual change forcing edits in many places. In existing code, `code-smells` calls this shotgun surgery; here it is judged before the code exists.

**Cognitive load** — how much a developer must hold in their head to complete a task correctly. A shorter solution that demands more knowledge is the *more* complex one.

**Unknown unknowns** — the worst of the three: it is not obvious which code must change, or what you must know to change it safely. You find out via the bug report.

## The two causes

Every symptom traces back to one of these:

**Dependencies** — code that cannot be understood or changed in isolation, because other code relies on it or shapes it. Dependencies can't be eliminated, only made fewer, simpler, and more obvious.

**Obscurity** — important information that is not evident from the code: an unstated invariant, a unit hidden in an int, a name that reveals nothing. Obscurity is the cheaper cause to fix and the easier one to plan away.

## The two mindsets

How complexity gets in — or gets kept out — is a way of working, not a single decision:

**Tactical programming** — optimising for the next milestone: the shortcut, the special case, "just this once." Each increment is small; the sum is where complexity comes from.

**Strategic programming** — optimising for the structure that makes future change cheap; treating working code as not enough. The investment is continuous and small, not a big-bang redesign.

## Principles

- **Complexity is incremental.** No single decision makes a system complex; hundreds of small ones do. That is why "it's only a little hack" is not an argument — the ledger below applies to small things too.
- **Complexity is what the reader experiences, not the writer.** The author's familiarity is not evidence of simplicity. Judge from the position of someone arriving cold.
- **Pull complexity downwards.** When complexity is unavoidable, the implementer should absorb it rather than the caller — a module with a simple interface and a hard implementation beats the reverse. The deepening moves live in `codebase-design`.
- **Somewhat general-purpose.** The interface serves more than today's exact need, while the implementation does only what today needs. Guards against both special-casing and speculative generality.

## The complexity ledger

When planning, run each element of the proposed solution through this — every new module, dependency, config option, and special case is accounted for before the plan is approved:

1. **What does it cost?** Which dependencies does it create, and what will be obscure to a cold reader?
2. **Which symptom will that cost show up as** — change amplification, cognitive load, or unknown unknowns?
3. **What pays for it?** A benefit named in the plan, not "we might need it."
4. **Can the same benefit be bought cheaper** — fewer dependencies, less obscurity, complexity pulled downwards?

An element that can't answer 3 is tactical programming; cut it or say explicitly that the debt is being taken on purpose.

## Relationships

- **Dependencies** and **obscurity** cause complexity; **change amplification**, **cognitive load**, and **unknown unknowns** are how it is felt.
- **Tactical programming** is how complexity gets in; **strategic programming** plus the **ledger** is how it is kept out of a plan.
- In existing code, symptoms surface as entries in `code-smells`; the structural cure is a deeper module — vocabulary and moves in `codebase-design`.

## Rejected framings

- **Complexity as size or line count**: a 50-line clever solution can be more complex than a 200-line obvious one. Judge by cost of change, not volume.
- **"Technical debt"** as the umbrella term: debt implies a repayment plan; most tactical complexity has none. Name the cause (dependency, obscurity) instead.
- **"Keep it simple" as a rule**: without the causes and symptoms it's a vibe, not a test. The ledger replaces it.
