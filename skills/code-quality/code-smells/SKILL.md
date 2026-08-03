---
name: code-smells
description: The shared baseline of structural problems to look for in code — naming, abstraction, structure, and change patterns. Use when reviewing or refining code, or when another skill needs the smell baseline.
---

# Code Smells

The one list of structural problems this workspace looks for. Two skills reach for it at different moments:

- **`simplify`** acts on it — rewriting the code while preserving behavior.
- **`review`** flags what is left — reporting rather than fixing.

Same list, so a `simplify` pass doesn't leave behind exactly what the review will reopen.

Every entry is a **judgement call, not a violation**. A smell is a reason to look
closer; the code may still be right. Documented project standards override anything
here, and anything a formatter, linter, or type checker already enforces is out of
scope for both skills.

## Naming and abstraction

- **Mysterious name** — a name that doesn't say what the thing is or does. Rename until it does.
- **Primitive obsession** — a domain concept carried as a string, int, or map. Give it a type, named the way `CONTEXT.md` names it.
- **Data clumps** — the same few fields or parameters travelling together everywhere. Bundle them into one type.
- **Speculative generality** — an abstraction, hook, or parameter with no present caller. Remove it until something needs it.

## Structure

- **Duplicated code** — the same logic in more than one place. Extract it once the third instance appears, or sooner if the copies must change together.
- **Long method** — a function doing several things at several levels of abstraction. Break it up, keeping tests on the public interface.
- **Shallow module** — an interface nearly as wide as the implementation behind it, so callers carry the complexity. Deepen it or fold it into its caller.
- **Feature envy** — a method reaching repeatedly into another object's data. Move it to the data.
- **Middle man** — a class that only delegates. Let callers talk to the real thing.
- **Message chains** — `a.getB().getC().getD()`. Ask the first object for what you actually want.

## Change patterns

- **Divergent change** — one module changed for unrelated reasons. Split it along those reasons.
- **Shotgun surgery** — one conceptual change forcing edits across many modules. Consolidate what belongs together.
- **Repeated switches** — the same conditional cascade in several places. Replace with polymorphism or a shared map.
- **Refused bequest** — a subclass inheriting things it doesn't want. Prefer composition.

## Revealed by new code

- **Existing code the new code exposes** — a change that makes a nearby shape obviously wrong. Worth flagging even when it predates the work under review.
