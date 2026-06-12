# cc-plugins

Personal skills for [Claude Code](https://docs.claude.com/en/docs/claude-code)
and [Codex](https://skills.sh) — installed with bare names (no plugin prefix) via
the [`skills`](https://skills.sh) CLI.

Thirteen skills, grouped by category:

| Category       | Skill              | What you get                                                                                                |
| -------------- | ------------------ | ----------------------------------------------------------------------------------------------------------- |
| `reasoning`    | `think-like`       | Adopt an expert persona to reason through a problem; editable persona library; authoring workflow built in   |
| `reasoning`    | `grill-me`         | Lean interview-style plan stress-testing, one question at a time, no side effects                            |
| `reasoning`    | `grill-with-docs`  | Docs-aware grilling — challenges terminology against the domain model, updates `CONTEXT.md` and offers ADRs   |
| `code-quality` | `review`           | Security, performance, quality, architecture, docs — scored 0–100, written to `ai/reviews/`                  |
| `code-quality` | `zoom-out`         | Map the modules and callers around an unfamiliar area of code                                                |
| `code-quality` | `tdd`              | Red-green-refactor, vertical slices, behavior-driven tests                                                   |
| `code-quality` | `simplify`         | Simplify recently changed code for clarity and consistency, preserving exact functionality                   |
| `workflow`     | `commit`           | Imperative-title commits with structured bodies                                                              |
| `planning`     | `to-prd`           | Synthesize the current context into a PRD under `ai/prds/`                                                    |
| `planning`     | `to-issues`        | Break a plan/spec/PRD into self-contained issues under `ai/issues/`                                           |
| `planning`     | `vet-issues`       | Pressure-test issues through an implementer's eyes; findings shown in-conversation, no files                 |
| `planning`     | `next-issue`       | Pick up the next open issue, read it, and plan it before any code                                            |
| `planning`     | `complete-issue`   | Verify an issue's acceptance criteria against the real changes                                               |

## Install

These install as **bare-named skills** into both Claude Code (`~/.claude/skills/`)
and Codex (`~/.codex/skills/`) — invoked as `next-issue`, not `plugin:next-issue`.

```shell
npx skills add MalasataXD/cc-plugins
```

The installer prompts you to pick which skills and which agents to install into.
Re-run the same command to pull updates.

> Skills auto-trigger on natural phrasing (e.g. *"think like a security
> engineer…"*, *"grill me on this plan"*, *"what's the next issue"*) and can also
> be invoked directly by name where your agent supports it.

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

## `grill-me` / `grill-with-docs` — stress-test a plan

Interview you relentlessly about a plan or design, one question at a time, walking
each branch of the decision tree until you reach shared understanding. For each
question they offer a recommended answer, and explore the codebase whenever a
question can be answered from the code.

**Auto-triggers** on phrasing like *"grill me"*, *"stress-test this plan"*, or
*"get me grilled on this design"*.

- `grill-me` — the lean version: pure interview, no side effects.
- `grill-with-docs` — challenges your plan against the project's domain language,
  sharpens fuzzy terminology, and captures decisions inline: maintains a
  `CONTEXT.md` glossary and offers ADRs sparingly (only for hard-to-reverse,
  surprising, genuine trade-offs). Formats live in `references/CONTEXT-FORMAT.md`
  and `references/ADR-FORMAT.md` beside the skill.

## `review`

Invokes when you ask for a code review. Produces scored feedback across security,
performance, quality, style, architecture, and documentation, then writes it as a
**local markdown file** under `ai/reviews/` at the repo root (reused if present,
created otherwise). Files are date-prefixed (e.g.
`ai/reviews/2026-06-02-auth-service.md`) so re-reviewing keeps a history. Rubric
and checklists in `skills/code-quality/review/references/`.

## `zoom-out` — map an unfamiliar area

When you don't know an area of code well, goes up a layer of abstraction and gives
you a map of the relevant modules and callers, using the project's domain glossary
vocabulary. **Manually invoked only** — it won't auto-trigger.

## `tdd` — test-driven development

Guides feature work and bug fixes through the **red-green-refactor** loop. Tests
verify behavior through public interfaces, not implementation details. Works in
**vertical slices** (one test → one implementation → repeat) rather than writing
all tests up front, and refactors only once green.

**Auto-triggers** on phrasing like *"build this test-first"*, *"red-green-refactor"*,
or *"let's TDD this"*. Supporting references (tests, mocking, interface design,
deep modules, refactoring) live in `skills/code-quality/tdd/references/`. Adapted
from [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd).

## `simplify`

Refines recently modified code for clarity, consistency, and maintainability
**without changing what it does**. Defers to the project's `AGENTS.md` or
`CLAUDE.md` and surrounding idioms, prefers explicit readable code over clever or
compact code
(no nested ternaries), and stops short of over-simplifying. Scoped to recent
changes by default; applies edits directly, pausing only when a change would risk
behavior or the scope is ambiguous.

**Auto-triggers** on phrasing like *"simplify this"*, *"clean up what I just
wrote"*, or *"tidy up these changes"*.

## `commit`

Invokes automatically when you ask to commit changes. Full style guide at
`skills/workflow/commit/references/commit-style.md`.

## `to-prd` — context to PRD

Synthesizes the current conversation and codebase understanding into a Product
Requirements Document. It does **not** interview you — it works from what's already
known, sketches the test seams, then writes the PRD using a structured template
(Problem Statement, Solution, User Stories, Implementation Decisions, Testing
Decisions, Out of Scope, Further Notes). Written as a **local markdown file only**
under `ai/prds/` at the repo root.

## `to-issues` — plan to issues

Breaks a plan, spec, or PRD into independently-grabbable issues using
**tracer-bullet vertical slices** — thin paths that cut through every layer rather
than horizontal slices of one layer. Prefers **self-contained tasks**, declaring a
"Blocked by" dependency only when a slice genuinely can't stand alone. Presents the
numbered breakdown and iterates with you before writing anything.

Each approved slice is a **local markdown file only** under `ai/issues/`, named
with a zero-padded ordinal (e.g. `01-account-balance-endpoint.md`). Each issue
carries a **`Type`** (`AFK` — review only; or `HITL` — human needed during work)
and a **`Status`** (`Not started` → `In progress` → `Completed`).

## `vet-issues` — pressure-test issues

Reads a set of issues through the eyes of an implementer picking each one up
**cold** and reports the first question they can't answer. It distinguishes a
**genuine gap** (a decision nobody made) from **healthy exploration** (reading the
code), flagging only the former, and checks the set for dependency cycles, coverage
holes, overlap, and granularity drift.

**Read-only**: each issue gets a verdict (Ready / Needs work / Blocked) and fixes
are framed as questions for the author. Findings are shown **in the conversation**
— nothing is written to disk.

## `next-issue` — pick up the next open issue

Selects the next open issue from `ai/issues/`, reads it in full, explores the
codebase, and presents an implementation plan — then **stops and waits for
approval** before touching any code. Prefers finishing an `In progress` issue over
starting a new one, otherwise picks the lowest-ordinal `Not started` issue whose
blockers are all `Completed`. On approval, offers to flip `Status` to `In progress`.

## `complete-issue` — verify an issue is done

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
│   │   ├── grill-me/
│   │   └── grill-with-docs/
│   ├── code-quality/
│   │   ├── review/
│   │   ├── zoom-out/
│   │   ├── tdd/
│   │   └── simplify/
│   ├── workflow/
│   │   └── commit/
│   └── planning/
│       ├── to-prd/
│       ├── to-issues/
│       ├── vet-issues/
│       ├── next-issue/
│       └── complete-issue/
└── archive/
    └── gh/          # GitHub CLI workflows — archived, not installed
```

## Archived

- **`gh`** — GitHub CLI workflows (plate, digest, standup, project status moves,
  issue drafting). Kept under `archive/` for reference; not installed by the
  `skills` CLI.
