# cc-plugins

Personal [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace.

Seven plugins, grouped by category:

| Category       | Plugin   | What you get                                                                                            |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------- |
| `reasoning`    | `think`  | `think-like` skill + editable persona library + `/think:like` and `/think:add` commands                 |
| `reasoning`    | `grill`  | `grill-me` and `grill-with-docs` skills — interview-style plan stress-testing, optionally docs-aware     |
| `code-quality` | `review` | `review` skill — security, performance, quality, architecture, docs, with a 0–100 scoring rubric        |
| `workflow`     | `commit` | `commit` skill — imperative-title commits with structured bodies                                        |
| `workflow`     | `gh`     | GitHub CLI workflows — plate, digest, standup, project status moves, and well-formed issue drafting     |
| `planning`     | `to-prd` | `to-prd` skill — synthesize the current context into a PRD, written to a local `ai/prds/` markdown file  |
| `planning`     | `to-issues` | `to-issues` skill — break a plan/spec/PRD into self-contained issues, written to local `ai/issues/` files |

## Install

From any Claude Code session:

```shell
/plugin marketplace add MalasataXD/cc-plugins
/plugin install think@cc-plugins
/plugin install grill@cc-plugins
/plugin install review@cc-plugins
/plugin install commit@cc-plugins
/plugin install gh@cc-plugins
/plugin install to-prd@cc-plugins
/plugin install to-issues@cc-plugins
```

Pull updates later with `/plugin marketplace update cc-plugins`.

## `think` — expert persona reasoning

Adopt a specific expert's lens to reason through a problem.

**Auto-triggers** on natural phrasing: *"think like a software architect…"*, *"as a UX designer, what…"*, *"from the perspective of a security engineer…"*.

**Slash commands:**

```shell
/think:like <archetype> <prompt>
/think:add  <archetype> <idea>
```

Personas live as editable markdown files at `plugins/reasoning/think/skills/think-like/personas/`. Eleven are bundled (software-architect, backend-engineer, frontend-engineer, devops-sre, security-engineer, tech-lead, dba, product-manager, ux-designer, technical-writer, production-designer). Edit or add your own — each file is the source of truth.

`/think:add` drafts a new persona interactively, shows you the spec, and only writes to disk after you approve. Commit the resulting file back to this repo to sync it across machines.

## `grill` — stress-test a plan

Interviews you relentlessly about a plan or design, one question at a time, walking each branch of the decision tree until you reach shared understanding. For each question it offers its own recommended answer, and explores the codebase whenever a question can be answered from the code.

**Auto-triggers** on phrasing like *"grill me"*, *"stress-test this plan"*, or *"get me grilled on this design"*.

**Slash commands:**

```shell
/grill:me        [plan or topic]   # lean interview, no side effects
/grill:with-docs [plan or topic]   # docs-aware: updates CONTEXT.md and offers ADRs
```

Two skills:

- `grill-me` — the lean version: pure interview, no side effects.
- `grill-with-docs` — challenges your plan against the project's domain language, sharpens fuzzy terminology, and captures decisions inline: it maintains a `CONTEXT.md` glossary and offers ADRs sparingly (only for hard-to-reverse, surprising, genuine trade-offs). Formats live in `CONTEXT-FORMAT.md` and `ADR-FORMAT.md` beside the skill.

## `review`

Invokes when you ask for a code review. Returns scored feedback across security, performance, quality, style, architecture, and documentation. Rubric and checklists in `plugins/code-quality/review/skills/review/references/`.

## `commit`

Invokes automatically when you ask Claude to commit changes. Full style guide at `plugins/workflow/commit/skills/commit/references/commit-style.md`.

## `gh` — GitHub CLI workflows

**Auto-triggers** when you ask about issues, project statuses, weekly summaries, or drafting a new issue.

**Slash commands:**

```shell
/gh:plate [owner/repo]               # open issues assigned to you, grouped by repo
/gh:digest [<since>] [owner/repo]    # closed issues + merged PRs for a period
/gh:standup                          # yesterday's closes + today's plate, formatted for standup
/gh:move <issue-url> <status>        # move an issue to a new project board status
/gh:new-issue <description> [repo]   # draft and create a well-formed issue with correct labels
```

**First-time setup:** after installing, copy `plugins/workflow/gh/skills/gh/config.example.json` to `config.json` in the same folder and set `github_handle` to your GitHub username. The skill will prompt you if the file is missing.

Requires `gh auth refresh -s project` for project board commands (`/gh:move`).

## `to-prd` — context to PRD

Synthesizes the current conversation and codebase understanding into a Product Requirements Document. It does **not** interview you — it works from what's already known, sketches the test seams (checking they match your expectations), then writes the PRD using a structured template (Problem Statement, Solution, User Stories, Implementation Decisions, Testing Decisions, Out of Scope, Further Notes).

The PRD is written as a **local markdown file only** — never published to an external tracker. It lands under an `ai/prds/` folder at the repo root (reused if present, created otherwise).

**Slash command:**

```shell
/to-prd:to-prd [optional focus or feature name]
```

## `to-issues` — plan to issues

Breaks a plan, spec, or PRD into independently-grabbable issues using **tracer-bullet vertical slices** — thin paths that cut through every layer (schema, API, UI, tests) rather than horizontal slices of one layer. It prefers **self-contained tasks** with no blockers, declaring a "Blocked by" dependency only when a slice genuinely can't stand alone. It presents the numbered breakdown and iterates with you (granularity, HITL/AFK, dependencies) before writing anything.

Each approved slice is written as a **local markdown file only** — never published to an external tracker — under an `ai/issues/` folder at the repo root, named with a zero-padded ordinal so dependency order is visible (e.g. `01-account-balance-endpoint.md`).

**Slash command:**

```shell
/to-issues:to-issues [plan, spec, PRD path, or free-form description]
```

## Layout

Plugins are grouped into category folders. The `category` field in `marketplace.json` and the folder each plugin lives in are kept in sync.

```
cc-plugins/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    ├── reasoning/
    │   ├── think/
    │   └── grill/
    ├── code-quality/
    │   └── review/
    ├── workflow/
    │   ├── commit/
    │   └── gh/
    └── planning/
        ├── to-prd/
        └── to-issues/
```

## License

MIT.
