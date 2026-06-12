---
name: simplify
description: >
  Simplify and refine code for clarity, consistency, and maintainability while
  preserving exact functionality. Triggers when the user asks to simplify, clean
  up, tidy, refine, or improve the readability of code, or to apply project
  standards to recent changes. Focuses on recently modified code unless told
  otherwise. Prefers explicit, readable code over clever or overly compact code.
---

# Simplify

Refine code to be clearer, more consistent, and more maintainable **without
changing what it does**. Favor readable, explicit code over compact cleverness —
that balance is the whole point of this skill.

## Scope

By default, only touch code that was **recently modified or written in the
current session**. Broaden the scope only when the user explicitly asks for it
(a named file, directory, or "the whole module").

If you can't tell what changed recently, check `git diff` / `git status` first,
or ask the user to point at the target — don't guess and rewrite untouched code.

## Hard rule: preserve functionality

Never change behavior — only *how* the code expresses it. All original features,
outputs, side effects, and public signatures must remain intact. If a "cleanup"
would alter behavior, stop and surface it as a question instead of applying it.

## Apply project standards

Standards apply in layers, highest precedence first:

1. **The project's agent instructions and existing conventions** — read whichever
   of `AGENTS.md` or `CLAUDE.md` the project has (or both); these always win.
2. **The matching language reference** — if `references/<language>.md` exists for
   the file's language (e.g. `typescript-react.md`, `python.md`, `csharp.md`),
   load and apply it. These hold cross-project defaults.
3. **The general clarity principles** below.

Match the surrounding code's idioms over imposing your own, and never let a
language default override an explicit project convention.

## Enhance clarity

- Reduce unnecessary complexity and nesting
- Eliminate redundant code and abstractions
- Improve names so intent is obvious
- Consolidate related logic
- Remove comments that merely restate what the code already says
- **Avoid nested ternaries** — prefer `switch` or `if`/`else` chains for multiple
  conditions
- Choose clarity over brevity — explicit beats dense one-liners

## Maintain balance — don't over-simplify

Stop short of changes that would:

- Reduce clarity or maintainability
- Produce clever solutions that are hard to follow
- Cram too many concerns into one function or component
- Remove helpful abstractions that aid organization
- Trade readability for fewer lines (nested ternaries, dense one-liners)
- Make the code harder to debug or extend

## Process

1. Identify the recently modified sections in scope.
2. Analyze for clarity, consistency, and standards opportunities.
3. Apply project standards and the refinements above.
4. Verify functionality is unchanged (signatures, outputs, side effects).
5. Confirm the result is genuinely simpler and more maintainable — not just
   shorter.
6. Apply the edits directly rather than only describing them, then briefly note
   any significant change that affects how the code is understood.

When invoked, act on the code in scope — make the edits. Only pause to ask when a
simplification would risk changing behavior or when the scope is ambiguous.
