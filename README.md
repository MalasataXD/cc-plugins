# cc-plugins

Personal skills for [Claude Code](https://docs.claude.com/en/docs/claude-code) and
[Codex](https://skills.sh), installed with bare names via the `skills` CLI.

```shell
# a new machine: the main tier, no prompts
npx skills add MalasataXD/cc-plugins -g -y -s grilling domain-modeling research prototype complexity to-spec to-tickets vet-tickets next-ticket implement tdd diagnosing-bugs simplify handoff review complete-ticket code-smells prove-it commit file-pr github-attribution unslop health-check retro writing-for-agents

# everything, including the extras tier
npx skills add MalasataXD/cc-plugins --all -g -y

# refresh everything already installed
npx skills update -g -y
```

Skills come in two tiers, which are the groups in the interactive picker
(driven by `.claude-plugin/marketplace.json`). **Main** is the working set:
the pipeline, every skill it loads, and the tools for maintaining the skills.
**Extras** is everything outside day-to-day work, marked *(extras)* below. Skills trigger on natural
phrasing (*"grill me on this plan"*, *"what's the next ticket"*) or by name.
Each skill's `SKILL.md` is its full documentation. This README is just the map.

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
  `wayfinder` charts one that doesn't as a route of pitches, grilling each into a spec in turn.
- **Tickets are only build work.** `to-tickets` settles every open question
  before writing one (facts through `research`, choices through `grilling`),
  so no ticket carries a guess.

## Skills

Folders follow the stage of work you are in. Skills install with bare names regardless.

| `think`: resolve uncertainty | |
| --- | --- |
| `grilling` | Interview in rounds of 3–5 questions, walking a design tree to its frontier |
| `research` | Background agent reads primary sources → `<work folder>/research/` |
| `prototype` | Throwaway code that answers a design question |
| `domain-modeling` | One term, one meaning: `GLOSSARY.md` and ADRs |
| `complexity` | Ousterhout's complexity model: the ledger plans answer to, plus deep modules and seams |

| `plan`: produce the breakdown | |
| --- | --- |
| `wayfinder` *(extras)* | Chart a big effort as a route of pitches → specs → `<work folder>/wayfinder/` |
| `to-spec` | Current context → compact spec → `<work folder>/specs/` |
| `to-tickets` | Spec → phases of compact tickets → `<work folder>/tickets/` |
| `vet-tickets` | Read tickets cold; report only what would stall an implementer |

| `build`: make the change | |
| --- | --- |
| `next-ticket` | Pick and plan the next open ticket, then build it unless the plan has open questions |
| `implement` | Build approved work: `tdd` where a seam exists → `simplify` → `review` when big |
| `tdd` | Red → green at pre-agreed seams, vertical slices |
| `diagnosing-bugs` | Feedback loop first; then reproduce, hypothesise, fix |
| `simplify` | Refine recent code without changing what it does |
| `handoff` | Compact the session for the next agent → `<work folder>/handoff.md` |

| `check`: judge the work | |
| --- | --- |
| `review` | Two-axis review, scored 0–100 → `<work folder>/reviews/` |
| `complete-ticket` | Judge a ticket against its criteria; commit and name the next ticket |
| `code-smells` | The shared baseline `simplify` fixes and `review` flags |
| `prove-it` | The certainty ladder `review` reports and `complete-ticket` enforces |
| `health-check` | Rank the codebase's hot spots from git history; hand the top one to `to-spec` |

| `ship`: get it out | |
| --- | --- |
| `commit` | Structured commits with imperative titles |
| `file-pr` | Open a PR with a changelog body written from the diff |
| `github-attribution` | The "Filed by <model name> on behalf of <name>" note that opens every GitHub write |

| `toolbox`: helpers for any stage | |
| --- | --- |
| `unslop` | Final prose pass for anything a human reads: specs, reviews, PR bodies |
| `wizard` *(extras)* | Interactive bash walkthrough for steps only a human can do |
| `wait-what` *(extras)* | Re-pitch the last message, simply |
| `teach` *(extras)* | Stateful tutor: mission, HTML lessons, learning records, glossary. The invocation directory is the workspace |

| `meta`: maintain the skills themselves | |
| --- | --- |
| `writing-for-agents` | Reference for writing any document an agent consumes: skills, `CLAUDE.md`, pointed-at docs |
| `retro` | Review a session and suggest changes to the agent's setup, not the code |

## Archived

Retired skills live in `archive/`, uninstalled: `gh` (GitHub CLI workflows),
`grill-with-docs` (superseded by `grilling` + `domain-modeling`), `think-like`,
`zoom-out` and `to-questionnaire` (unused), `codebase-design` (merged into
`complexity`), and `improve-codebase-architecture` (superseded by `health-check`).

## Credits

Several skills are taken or adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) (MIT); see each
skill's history. The composition is this repo's own: local-file outputs under a
project work folder, scored reviews, the RFA/RFH axis, and the ticket pipeline.
