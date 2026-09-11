# cc-plugins

Personal skills for [Claude Code](https://docs.claude.com/en/docs/claude-code) and
[Codex](https://skills.sh), installed with bare names via the `skills` CLI.

```shell
# install everything, no prompts
npx skills add MalasataXD/cc-plugins --all -g -y

# or one category, by passing its skills (see the tables below)
npx skills add MalasataXD/cc-plugins -g -y -s grilling grill-me batch-grill-me

# refresh everything already installed
npx skills update -g -y
```

The interactive picker groups skills by category (driven by
`.claude-plugin/marketplace.json`), and a category heading toggles its whole
group. Skills trigger on natural phrasing
(*"grill me on this plan"*, *"what's the next ticket"*) or by name. Each skill's
`SKILL.md` is its full documentation — this README is just the map.

## The pipeline

```
grilling ──┬→ to-spec → to-tickets → next-ticket → implement → complete-ticket → commit → file-pr
wayfinder ─┘                 │                          │
                        vet-tickets           tdd → simplify → review
```

Each stage stops where the next begins, and nothing grades its own work:
`implement` builds but never commits; `complete-ticket` judges the result cold
and gates the commit. Two ideas run through it:

- **Two front doors.** `grilling` stress-tests an idea that fits one session;
  `wayfinder` charts one that doesn't, then hands the cleared route to `to-spec`.
- **Every ticket has a Category** — `Build` (default), `Research`, or
  `Decision`. The last two are open questions split out of the build,
  resolved by the `research` and `grilling` skills.

## Skills

Categories are folders only — skills install with bare names regardless.

| `reasoning` — resolve uncertainty | |
| --- | --- |
| `grilling` | The interview primitive — walk a design tree to its frontier |
| `grill-me` | Grilling, one question at a time |
| `batch-grill-me` | Grilling, rounds of 3–5 questions |
| `domain-modeling` | One term, one meaning — `CONTEXT.md` and ADRs |
| `research` | Background agent reads primary sources → `<work folder>/research/` |
| `prototype` | Throwaway code that answers a design question |
| `complexity` | Ousterhout's complexity model — the ledger plans answer to |

| `planning` — produce the breakdown | |
| --- | --- |
| `wayfinder` | Chart a big effort as decision tickets → `<work folder>/wayfinder/` |
| `to-spec` | Current context → compact spec → `<work folder>/specs/` |
| `to-tickets` | Spec → phases of compact tickets → `<work folder>/tickets/` |
| `vet-tickets` | Read tickets cold; report only what would stall an implementer |

| `code-quality` — judge and refine code | |
| --- | --- |
| `review` | Two-axis review, scored 0–100 → `<work folder>/reviews/` |
| `code-smells` | The shared baseline `simplify` fixes and `review` flags |
| `prove-it` | The certainty ladder `review` reports and `complete-ticket` enforces |
| `codebase-design` | Deep-module vocabulary — interfaces, seams, adapters, depth |
| `improve-codebase-architecture` | Find deepening candidates → HTML report → `<work folder>/architecture/` |
| `tdd` | Red → green at pre-agreed seams, vertical slices |
| `simplify` | Refine recent code without changing what it does |
| `diagnosing-bugs` | Feedback loop first; then reproduce, hypothesise, fix |

| `learning` — learn beyond the codebase | |
| --- | --- |
| `teach` | Stateful tutor: mission, HTML lessons, learning records, glossary — the invocation directory is the workspace |

| `utility` — maintain the toolset | |
| --- | --- |
| `writing-for-agents` | Reference for writing any document an agent consumes — skills, `CLAUDE.md`, pointed-at docs |
| `unslop` | Final prose pass for anything a human reads — specs, reviews, PR bodies |
| `wait-what` | Re-pitch the last message, simply |
| `wizard` | Interactive bash walkthrough for steps only a human can do |

| `workflow` — move the work | |
| --- | --- |
| `next-ticket` | Pick and plan the next open ticket, then wait for approval |
| `implement` | Build approved work: `tdd` where a seam exists → `simplify` → `review` when big |
| `complete-ticket` | Judge a ticket against its criteria; offer the `commit` |
| `handoff` | Compact the session for the next agent → `<work folder>/handoff.md` |

| `git` — ship the work | |
| --- | --- |
| `commit` | Structured commits with imperative titles |
| `file-pr` | Open a PR with a changelog body written from the diff |
| `github-attribution` | The "Filed by <model name> on behalf of <name>" note that closes every GitHub write |

## Archived

Retired skills live in `archive/`, uninstalled: `gh` (GitHub CLI workflows),
`grill-with-docs` (superseded by `grilling` + `domain-modeling`), `think-like`,
`zoom-out` and `to-questionnaire` (unused).

## Credits

Several skills are taken or adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) (MIT) — see each
skill's history. The composition — local-file outputs under a project work folder, scored
reviews, the RFA/RFH and Category axes, and the ticket pipeline — is this
repo's own.
