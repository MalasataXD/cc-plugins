---
name: wayfinder
description: Use when an effort is too big for one spec, or to continue an existing wayfinder map.
disable-model-invocation: true
---

# Wayfinder

A loose idea has arrived — too big for one spec, and wrapped in fog: the way from here to the **destination** isn't visible yet, and you can't grasp all of it at once. This skill charts the way as a **route**: an ordered list of specs, each starting life as a short **pitch**. It then grills one pitch at a time into a spec, and **re-charts** the route every time a spec's work lands.

Wayfinder produces specs. `to-tickets` cuts a spec into tickets, as a separate step the user starts.

## The map

One map per effort, at `<work folder>/wayfinder/<effort-slug>.md`. The project's `AGENTS.md` or `CLAUDE.md` names the work folder; when it names nothing, use `.ai/` at the repository root.

The map is an **index**, not a store. Decisions live in the specs (and the ADRs and `CONTEXT.md` they feed); the map only orders the specs and links them.

```markdown
# <Effort>

## Destination

<what is true once this effort is finished — one or two lines; every session orients to it>

## Route

1. **<Spec name>**: Done → [spec](../specs/<slug>.md)
2. **<Spec name>**: Specced → [spec](../specs/<slug>.md)
3. **<Spec name>**: Pitch
   <what it is and why, in a line or two>
   Waits on: <the landed work its decisions depend on, or "Nothing">

## Out of scope

- <gist>: <why it's beyond the destination>
```

### Statuses

`Pitch → Specced → Ticketed → Done`. The first `Pitch` in the route is the next to grill; order carries priority, so there is no `Next` status.

`Ticketed` and `Done` are read from `<work folder>/tickets/<spec-slug>/`: the folder exists → `Ticketed`; every ticket in it `Completed` → `Done`. Refresh them from there whenever you load the map.

### Pitches

A pitch is the fog written down per spec: loose on purpose, a line or two plus **Waits on**. It is the base the deep grill starts from, never a substitute for it. When a pitch outgrows a few lines, it's sharp enough to grill.

When a pitch becomes a spec, its text goes and the entry collapses to name, status and link — the spec now holds it.

### The dependency rule

**A spec ends where a decision can only be made after earlier work has landed.** A question you can't answer until you've seen something built belongs to a later pitch, whose **Waits on** names that work. This is what cuts the route into specs; the ticket count never does.

The rule applies while grilling too. A question that surfaces mid-grill and waits on unlanded work moves to the pitch it belongs to — or a new one — instead of becoming an assumption in the spec or a Decision ticket under it.

### Out of scope

The destination fixes the scope. Work beyond it goes in **Out of scope** with one line on why — not in a pitch. It returns only if the destination is redrawn.

## Invocation

Either mode ends on a written map; neither writes tickets or code.

### Chart the route

User invokes with a loose idea.

1. **Name the destination.** Run `grilling` and `domain-modeling` until the destination is one or two lines the user has accepted. It fixes the scope, so it's settled first.
2. **Cut the route.** Grill **breadth-first** across the whole space, applying the dependency rule, until every part of the destination sits in exactly one pitch or in Out of scope. If the route is a single pitch, the effort doesn't need a map: say so and hand off to `grilling` → `to-spec`.
3. **Write the map** with every stop a `Pitch`, then offer to grill the first one.

### Continue the route

User invokes with an existing map, or asks to redirect the effort.

1. **Load the map** and refresh `Ticketed` and `Done`.
2. **Re-chart** when the refresh moved a stop to `Done`, or when the user has changed direction: rewrite each remaining pitch against what actually landed, drop the ones reality killed, add the ones it revealed, and move anything now past the destination to Out of scope. Confirm the new route with the user. A map that no longer matches the direction misdirects everyone who reads it, so the rewrite happens in this session.
3. **Pick the stop:** the first `Pitch` whose Waits on has landed. If none has, report which work the route waits on and stop — the next move is building, not planning.
4. **Grill it deep** with `grilling` and `domain-modeling`, until every question in the pitch is decided or has moved to a later pitch under the dependency rule.
5. **Write the spec** with `to-spec`, then collapse the stop to `Specced` with its link.

When every stop is `Done`, the destination is reached: report it, and offer to delete the map — a finished map only misdirects.
