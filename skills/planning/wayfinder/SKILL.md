---
name: wayfinder
description: Plan a huge chunk of work — more than one grilling session can hold — as a local map of decision tickets under ai/wayfinder/, and resolve them one at a time until the way to the destination is clear.
disable-model-invocation: true
---

# Wayfinder

A loose idea has arrived — too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **map** of local markdown files, then works its **decision tickets** — questions whose resolution is a decision, not slices of a build to execute — one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting — it shapes every ticket. It might be a spec to hand off to `to-spec` → `to-tickets`, a decision to lock before planning starts, or a change made in place like a data-structure migration.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear — nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off — usually to `to-spec`, whose spec `to-tickets` then slices into build tickets. An effort can override this in its **Notes** — carrying execution into the map itself — but absent that, produce decisions, not deliverables.

## Refer by name

Every ticket has a **name** — its title. In everything the human reads — narration, the map's Decisions-so-far — refer to it by that name, never by a bare ordinal or filename. The file path doesn't vanish — a name wraps its link — but it rides _inside_ the name, never stands in for it.

## The Map

The map lives at `ai/wayfinder/map.md` — the canonical artifact. Its tickets live beside it in `ai/wayfinder/tickets/`, one file per ticket, named `<ordinal>-<slug>.md` (zero-padded, e.g. `03-auth-provider.md`). These are **decision tickets**, deliberately kept apart from the build tickets in `ai/tickets/` — those execute a plan; these produce one.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place — its ticket — so the map never restates it, only gists it and links.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed — they are found by reading the ticket folder's statuses.

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index — one line per resolved ticket: enough to judge relevance, then follow the link for the detail the ticket holds -->

- [<resolved ticket title>](tickets/<file>.md) — <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket's body is the question, sized to one agent session:

```markdown
# <Ticket title>

## Category

<research | prototype | decision | task>

## Status

<Not started | In progress | Resolved | Out of scope>

## Question

<the decision or investigation this ticket resolves>

## Blocked by

<references to blocking ticket files, or "None">

## Resolution

<empty until resolved — then the answer, and links to any assets (research files, prototypes) rather than pasted content>
```

A session **claims** a ticket by setting its Status to `In progress`, **first**, before any work, so concurrent sessions skip it. A ticket is **unblocked** when every ticket blocking it is `Resolved`; the **frontier** is the open, unblocked, unclaimed tickets — the edge of the known.

## Ticket Categories

The same `Category` axis the build tickets in `ai/tickets/` carry — `research`, `prototype`, and `decision` mean the same thing in both places; only `build` never appears here, because wayfinder plans rather than builds, and `task` never appears there. Every ticket is either **HITL** — human in the loop, worked _with_ a human who speaks for themselves — or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. Resolved by a `research` **subagent** writing to `ai/research/`, linked from the ticket. Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to — an outline, a rough take, a stub, or UI/logic code via the `prototype` skill. Links the artifact as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Decision** (HITL): Conversation — the choice is put to the human. The default case. Always invoke the `grilling` and `domain-modeling` skills.
- **Task** (HITL or AFK): Manual work that must happen before a _decision_ can be made — nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that _does_ rather than decides — and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist — or, for a dashboard-and-credentials procedure, generates one via the `wizard` skill (HITL). Resolved when the work is done; the resolution records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war** — the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets — one at a time, until the way to the destination is clear and no tickets remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination — everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for anyone reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now — _not_ whether you can answer it now.

- **Ticket when** the question is already sharp — even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope** — it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates — the frontier stops at the destination — so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already exists turns out to sit past the destination — mis-scoped in while charting, or exposed by a resolution — set its Status to `Out of scope` (unambiguously off the frontier) and leave one line in the **Out of scope** section: the gist plus why it's out, linking the ticket. It stays out of **Decisions so far**, which records the route actually walked — a scope boundary isn't a step on it.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session** — with the exception of research tickets.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Run a `grilling` and `domain-modeling` session to pin down what this map is finding its way to — the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** — the way to the destination is already clear, the whole journey small enough for one session — you don't need a map. Stop and ask the user how they'd like to proceed (usually straight to `to-spec`).
3. **Create the map** at `ai/wayfinder/map.md`: Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
4. **Create the tickets you can specify now** under `ai/wayfinder/tickets/` — then wire the **Blocked by** references in a **second pass** (files need names before they can reference each other). Wiring sorts them into the frontier and the blocked; everything you can't yet specify stays in the fog — the **Not yet specified** section.
5. **Fire the research subagents.** For each `research` ticket you just created, spin up a `research` subagent to resolve it in parallel, its findings landing in `ai/research/` with a link from the ticket.
6. Stop — charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with an existing map. A ticket is **optional** — without one, you pick the next decision, not the user.

1. Load the **map** — the low-res view, not every ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in ordinal order. **Claim it**: set its Status to `In progress` before any work.
3. Resolve it — **zoom as needed**: read the full body of any related or resolved ticket on demand; invoke the skills the `## Notes` block names. If in doubt, use `grilling` and `domain-modeling`.
4. Record the resolution: write the answer into the ticket's `## Resolution`, set its Status to `Resolved`, and **append a one-line gist with a link** to the map's Decisions-so-far.
5. Add newly-surfaced tickets (create-then-wire); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. If the answer reveals a ticket — this one or another — sits beyond the destination, **rule it out of scope** rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those tickets.

When the map is done — frontier empty, fog cleared — hand off: run `to-spec` to turn the decisions into a spec, or report the locked decision, whichever the Destination named.
