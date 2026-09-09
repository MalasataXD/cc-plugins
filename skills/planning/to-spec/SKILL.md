---
name: to-spec
description: Turn the current conversation context into a compact spec. Use when the user wants to create a spec.
---

This skill takes the current conversation context and codebase understanding and produces a spec as a local markdown file. Do NOT interview the user — just synthesize what you already know.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Name things the way `CONTEXT.md` names them throughout the spec, and respect any ADRs in the area you're touching — see the `domain-modeling` skill.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can.

   Check with the user that these seams match their expectations.

3. Run each implementation decision through the ledger in the `complexity` skill — every new module, dependency, config option, and special case must name what pays for it before it goes in the spec.

4. Write the spec using the template below and pass its prose through the `unslop` skill, then save it to `<work folder>/specs/<slug>.md`. The project's `AGENTS.md` or `CLAUDE.md` names the work folder; when it names nothing, use `.ai/` at the repository root. The slug is short kebab-case derived from the feature, e.g. `specs/account-balance-display.md`; if that file already exists, confirm with the user before overwriting. Confirm the path to the user once written.

## Spec template

The spec is read by agents building the feature, so it carries decisions, not narrative. Every section is a short paragraph or a bullet list; a spec that runs past a screen or two is carrying something the tickets should carry instead.

<spec-template>

## Goal

One paragraph: what is wrong or missing today, and what is true once this ships.

## Decisions

One bullet per decision, stating the decision and why it beat the alternative. Cover the modules built or modified and their interfaces, schema changes, API contracts, architectural choices, and any clarification the developer gave. Each new module, dependency, config option, or special case names what pays for it.

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing

The seam the feature is tested at, what a good test there looks like (external behavior only, never implementation details), and prior art for such tests in the codebase.

## Required Research

Questions that must be answered from primary sources — official docs, third-party APIs, specs — before dependent work can be built. One bullet per question, each naming the decision that waits on its answer. When the spec is broken down, `to-tickets` turns each into a **Research**-category ticket resolved by the `research` skill. Omit this section when there is none.

## Out of Scope

Bullets naming what this spec deliberately leaves out.

</spec-template>
