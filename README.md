# cc-plugins

Personal skills for [Claude Code](https://docs.claude.com/en/docs/claude-code)
and [Codex](https://skills.sh) — installed with bare names (no plugin prefix) via
the [`skills`](https://skills.sh) CLI.

Seventeen skills, grouped by category:

| Category       | Skill              | What you get                                                                                                 |
| -------------- | ------------------ | ------------------------------------------------------------------------------------------------------------ |
| `reasoning`    | `think-like`       | Adopt an expert persona to reason through a problem; editable persona library; authoring workflow built in    |
| `reasoning`    | `grilling`         | The interview primitive — a design tree walked to its frontier, in serial or batch cadence                    |
| `reasoning`    | `grill-me`         | Grilling, one question at a time                                                                              |
| `reasoning`    | `batch-grill-me`   | Grilling, the whole frontier per round                                                                        |
| `reasoning`    | `domain-modeling`  | Sharpen the project's language; maintain a `CONTEXT.md` glossary and ADRs                                     |
| `code-quality` | `review`           | Two axes — standards (scored 0–100) and spec compliance — reviewed by parallel sub-agents, saved to `ai/reviews/` |
| `code-quality` | `code-smells`      | The shared structural baseline `simplify` fixes and `review` flags                                            |
| `code-quality` | `tdd`              | Red → green at pre-agreed seams, vertical slices, behavior-driven tests                                       |
| `code-quality` | `simplify`         | Refine recently changed code for clarity, preserving exact functionality                                      |
| `code-quality` | `zoom-out`         | Map the modules and callers around an unfamiliar area of code                                                 |
| `workflow`     | `implement`        | Build approved work by chaining `tdd` → `simplify` → `review` → `commit`                                      |
| `workflow`     | `commit`           | Imperative-title commits with structured bodies                                                               |
| `planning`     | `to-spec`          | Synthesize the current context into a spec under `ai/specs/`                                                  |
| `planning`     | `to-tickets`       | Break a plan or spec into vertical-slice tickets under `ai/tickets/`, then vet them                           |
| `planning`     | `vet-tickets`      | Pressure-test tickets through an implementer's eyes; findings in-conversation, no files                       |
| `planning`     | `next-ticket`      | Pick up the next open ticket, read it, and plan it before any code                                            |
| `planning`     | `complete-ticket`  | Verify a ticket's acceptance criteria against the real changes                                                |

## Install

These install as **bare-named skills** into both Claude Code (`~/.claude/skills/`)
and Codex (`~/.codex/skills/`) — invoked as `next-ticket`, not `plugin:next-ticket`.

```shell
npx skills add MalasataXD/cc-plugins
```

The installer prompts you to pick which skills and which agents to install into.
Re-run the same command to pull updates.

> **Upgrading from an earlier install?** Five skills were renamed
> (`to-prd` → `to-spec`, `to-issues` → `to-tickets`, `vet-issues` → `vet-tickets`,
> `next-issue` → `next-ticket`, `complete-issue` → `complete-ticket`) and their
> output folders moved (`ai/prds/` → `ai/specs/`, `ai/issues/` → `ai/tickets/`).
> Re-run `npx skills add` to pick up the new names, delete the old skill folders
> from `~/.claude/skills/`, and move any existing `ai/issues/` and `ai/prds/`
> folders yourself — nothing reads the old paths.

> Skills auto-trigger on natural phrasing (e.g. *"think like a security
> engineer…"*, *"grill me on this plan"*, *"what's the next ticket"*) and can also
> be invoked directly by name where your agent supports it.

## The pipeline

Most of these compose into one path from conversation to committed work:

```
conversation → to-spec → to-tickets → next-ticket → implement → complete-ticket
                              │            │            │
                          vet-tickets   grilling      tdd → simplify → review → commit
```

Each stage stops where the next begins. `next-ticket` selects and plans, then
**stops for approval**; `implement` builds; `complete-ticket` judges the result
**cold**. Nothing ever grades its own work.

## `think-like` — expert persona reasoning

Adopt a specific expert's lens to reason through a problem, using that role's
mental models and experience-shaped instincts.

**Auto-triggers** on natural phrasing: *"think like a software architect…"*, *"as
a UX designer, what…"*, *"from the perspective of a security engineer…"*.

Eleven personas are bundled (software-architect, backend-engineer,
frontend-engineer, devops-sre, security-engineer, tech-lead, dba, product-manager,
ux-designer, technical-writer, production-designer), living as editable markdown
files in `skills/reasoning/think-like/personas/` — each file is the source of
truth. To **add** a persona, the skill drafts a spec interactively, shows it to
you, and only writes after you approve (workflow in
`references/adding-a-persona.md`). Commit new personas back to this repo and
re-run `npx skills add` to sync them across machines.

## `grilling` — stress-test a plan

The interview primitive. It maps the work as a **design tree** and walks it to the
**frontier** — every decision whose prerequisites are already settled — offering a
recommended answer for each question and refusing to act until you confirm you've
reached shared understanding. Facts are its job to find; decisions stay yours.

Two cadences over the same tree, exposed as thin wrappers:

- `grill-me` — **serial**: one question at a time, deepest resolution per question.
- `batch-grill-me` — **batch**: the whole frontier in one numbered round, with
  sub-agents dispatched for fact-finding so a lookup never blocks the round.

**Auto-triggers** on phrasing like *"grill me"*, *"stress-test this plan"*, or
*"get me grilled on this design"*. When a `CONTEXT.md` exists it reads it, holds
you to that vocabulary, and offers to bring in `domain-modeling`.

## `domain-modeling` — one term, one meaning

Keeps the project's ubiquitous language sharp: challenges terms that conflict with
the glossary, proposes canonical names for fuzzy ones, stress-tests relationships
with concrete scenarios, and cross-references claims against the code.

Captures as it goes — `CONTEXT.md` updated the moment a term resolves (glossary
only, never implementation detail), and ADRs offered **sparingly**: only when a
decision is hard to reverse, surprising without context, *and* the result of a real
trade-off. Formats in `references/CONTEXT-FORMAT.md` and `references/ADR-FORMAT.md`.
Supports both single-context repos and `CONTEXT-MAP.md` layouts.

## `review` — two-axis code review

Judges code against the **standards** it should meet and the **spec** it was meant
to satisfy. Pins a fixed point first (resolve the ref, require a non-empty diff),
then dispatches **parallel sub-agents over disjoint dimensions** — security and
performance; quality, style, architecture and docs; spec compliance where a spec
exists — so no lens colours another. Findings aggregate verbatim, unreranked.

The standards axis is **scored 0–100** and weighted; spec compliance reports its own
Met / Partial / Not met verdict, deliberately kept out of the score — a change can
be immaculate and still build the wrong thing.

Documented project standards **override** the baseline, and anything a formatter,
linter, or type checker already enforces is skipped. Reports are written to
`ai/reviews/` with a date prefix, so re-reviewing keeps a history.

## `code-smells` — the shared baseline

One list of structural problems, used at two moments: `simplify` **acts** on it,
`review` **flags** what's left. Sharing it is what stops a simplify pass from
leaving behind exactly what the review would reopen. Every entry is a judgement
call, not a violation.

## `tdd` — test-driven development

The **red → green** loop, and the rules that make its tests worth keeping. Tests
live at **seams** — public boundaries where behavior is observable — and no test is
written at a seam you haven't confirmed, which is how testing effort lands on the
critical paths instead of every edge case.

Names three anti-patterns: **implementation-coupled**, **tautological** (the
assertion recomputes the expected value the way the code does, so it can never
disagree with the code), and **horizontal slicing**. Work goes in vertical slices,
one tracer bullet at a time.

Refactoring is deliberately **not** part of the loop — it belongs to `simplify`,
which `implement` chains next. Supporting references (tests, mocking, interface
design, deep modules) live in `skills/code-quality/tdd/references/`.

## `simplify`

Refines recently modified code for clarity, consistency, and maintainability
**without changing what it does**. Defers to the project's `AGENTS.md` or
`CLAUDE.md` and surrounding idioms, prefers explicit readable code over clever or
compact code (no nested ternaries), and stops short of over-simplifying.

Reads comments as a **verdict on the code**: one explaining *how* the code works —
or defending why it's written that way — means the code hasn't earned its place, so
rewrite it and delete the comment. One recording *why* a non-obvious external
constraint exists stays, because no refactor can recover that knowledge.
Doc comments (JSDoc/TSDoc, docstrings) sit outside the rule.

## `zoom-out` — map an unfamiliar area

When you don't know an area of code well, goes up a layer of abstraction and gives
you a map of the relevant modules and callers, named the way `CONTEXT.md` names
them. **Manually invoked only** — it won't auto-trigger.

## `implement` — build the approved work

The chain, not the work: grounds itself in the ticket, builds with `tdd`, tidies
with `simplify`, checks with `review`, runs the full suite, and commits with
`commit`. It holds no selection logic and no acceptance audit, so nothing ever
grades its own work.

Carries an **escape hatch** for the gaps every approved plan still has. A **fact**
(how the code behaves, what an interface accepts) is its job to find. A **decision**
the plan never settled is yours — it stops before writing code that assumes an
answer, and escalates several tangled ones to a `grilling` session.

## `commit`

Invokes automatically when you ask to commit changes. Full style guide at
`skills/workflow/commit/references/commit-style.md`.

## `to-spec` — context to spec

Synthesizes the current conversation and codebase understanding into a spec. It does
**not** interview you — it works from what's already known, sketches the test seams,
then writes using a structured template (Problem Statement, Solution, User Stories,
Implementation Decisions, Testing Decisions, Out of Scope, Further Notes). Written as
a **local markdown file only** under `ai/specs/`.

## `to-tickets` — plan to tickets

Breaks a plan or spec into independently-grabbable tickets using **tracer-bullet
vertical slices** — thin paths cutting through every layer rather than horizontal
slices of one layer. Prefers **self-contained** tickets, declaring a "Blocked by"
dependency only when a slice genuinely can't stand alone. For mechanical changes
whose blast radius rules out any thin path, it sequences **expand → migrate →
contract** instead, one ticket per phase.

Presents the breakdown and iterates with you before writing anything. Each approved
slice becomes a **local markdown file** under `ai/tickets/`, zero-padded by ordinal
(e.g. `01-account-balance-endpoint.md`), carrying a **`Type`** (**RFA**
ready-for-agent, or **RFH** ready-for-human) and a **`Status`** (`Not started` →
`In progress` → `Completed`).

Once written, it **vets its own output**: sub-agents read the files cold — batched
about five at a time, contiguous by ordinal so a ticket and its blocker land
together — plus one pass across the whole set for cycles, coverage holes, overlap,
and granularity drift.

## `vet-tickets` — pressure-test tickets

Reads a set of tickets through the eyes of an implementer picking each one up
**cold** and reports the first question they can't answer. Distinguishes a **genuine
gap** (a decision nobody made) from **healthy exploration** (reading the code),
flagging only the former.

**Read-only**: each ticket gets a verdict (Ready / Needs work / Blocked) and fixes
are framed as questions for the author. Findings are shown **in the conversation** —
nothing is written to disk.

## `next-ticket` — pick up the next open ticket

Selects the next open ticket from `ai/tickets/`, reads it in full, explores the
codebase, and presents an implementation plan — then **stops and waits for
approval** before touching any code. Prefers finishing an `In progress` ticket over
starting a new one, otherwise picks the lowest-ordinal `Not started` ticket whose
blockers are all `Completed`. On approval, offers to flip `Status` to `In progress`
and hands the plan to `implement`.

## `complete-ticket` — verify a ticket is done

Surveys the real changes (`git diff`, the files, the tests) and judges **each
acceptance criterion** as Met / Partial / Not met / Unverifiable, backed by
concrete evidence, then reports a verdict plus what's left and any scope drift.

**Read-only by default**: only after you confirm does it offer to tick the verified
criteria and advance `Status` to `Completed`.

## Layout

Skills use the `skills/<category>/<name>/` catalog layout the `skills` CLI
installs from. Category folders are for organization only — skills install with
bare names regardless.

```
cc-plugins/
├── skills/
│   ├── reasoning/
│   │   ├── think-like/
│   │   ├── grilling/
│   │   ├── grill-me/
│   │   ├── batch-grill-me/
│   │   └── domain-modeling/
│   ├── code-quality/
│   │   ├── review/
│   │   ├── code-smells/
│   │   ├── tdd/
│   │   ├── simplify/
│   │   └── zoom-out/
│   ├── workflow/
│   │   ├── implement/
│   │   └── commit/
│   └── planning/
│       ├── to-spec/
│       ├── to-tickets/
│       ├── vet-tickets/
│       ├── next-ticket/
│       └── complete-ticket/
└── archive/
    ├── gh/               # GitHub CLI workflows
    └── grill-with-docs/  # superseded by grilling + domain-modeling
```

## Archived

Retired skills move to `archive/` rather than being deleted. Nothing here is
installed by the `skills` CLI.

- **`gh`** — GitHub CLI workflows (plate, digest, standup, project status moves,
  issue drafting).
- **`grill-with-docs`** — the docs-aware grilling session, superseded when the
  interview became the `grilling` primitive and the documentation discipline became
  `domain-modeling`.

## Credits

`tdd`, `grilling`, `batch-grill-me`, `domain-modeling`, `implement`, `to-spec`,
`to-tickets`, and parts of `review` are adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) (MIT). The composition —
local-file-only outputs, scored reviews, the RFA/RFH split, and the
`next-ticket` → `implement` → `complete-ticket` pipeline — is this repo's own.
