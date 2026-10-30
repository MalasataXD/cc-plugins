# cc-plugins

Personal skills for [Claude Code](https://docs.claude.com/en/docs/claude-code) and
[Codex](https://skills.sh), installed with bare names via the `skills` CLI.

```shell
# a new machine: the main tier
npx skills add MalasataXD/cc-plugins -g -s grilling domain-modeling research prototype complexity to-spec to-tickets vet-tickets next-ticket implement tdd diagnosing-bugs simplify handoff review complete-ticket code-smells prove-it ship commit file-pr github-attribution unslop

# the extras tier, on top
npx skills add MalasataXD/cc-plugins -g -s health-check retro writing-for-agents wait-what

# refresh everything already installed
npx skills update -g -y

# refresh one skill in a project, from nightly
npx skills add "MalasataXD/cc-plugins#nightly" -s <skill> -a universal -y
```

In a project, use `add -a universal` rather than `update`: `update` targets
every agent folder it finds and can create unwanted ones, such as `.grok/skills`.

Skills come in two tiers, which are the groups in the interactive picker
(driven by `.claude-plugin/marketplace.json`). **Main** is the working set:
the pipeline and every skill it loads. **Extras** is everything outside
day-to-day work, marked *(extras)* below.
The install commands prompt for which agents to install to.

Name skills explicitly rather than using `--all`: it installs every
`SKILL.md` in the repo, `archive/` included, for every agent the CLI knows.

Skills trigger on natural
phrasing (*"grill me on this plan"*, *"what's the next ticket"*) or by name.
Each skill's `SKILL.md` is its full documentation. This README is just the map.

## The pipeline

```
grilling → to-spec → to-tickets → next-ticket → implement → complete-ticket → commit → ship → file-pr
                          │                          │
                     vet-tickets           tdd → simplify → review
```

Each stage stops where the next begins, and nothing grades its own work:
`implement` builds but never commits; `complete-ticket` judges the result cold
and gates the commit.

**Tickets are only build work.** `to-tickets` settles every open question
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
| `health-check` *(extras)* | Rank the codebase's hot spots from git history; hand the top one to `to-spec` |

| `ship`: get it out | |
| --- | --- |
| `ship` | Gate finished work on its review, checks, spec and tickets: Ready or Not ready |
| `commit` | Structured commits with imperative titles |
| `file-pr` | Open a PR with a changelog body written from the diff |
| `github-attribution` | The "Filed by <model name> on behalf of <name>" note that opens every GitHub write |

| `toolbox`: helpers for any stage | |
| --- | --- |
| `unslop` | Final prose pass for anything a human reads: specs, reviews, PR bodies |
| `wait-what` *(extras)* | Re-pitch the last message, simply |

| `meta`: maintain the skills themselves | |
| --- | --- |
| `writing-for-agents` *(extras)* | Reference for writing any document an agent consumes: skills, `CLAUDE.md`, pointed-at docs |
| `retro` *(extras)* | Review a session and suggest changes to the agent's setup, not the code |

## Archived

Retired skills live in `archive/`, uninstalled: `gh` (GitHub CLI workflows),
`grill-me` and `batch-grill-me` (superseded by `grilling`), `grill-with-docs`
(superseded by `grilling` + `domain-modeling`), `think-like`,
`zoom-out`, `to-questionnaire`, `wayfinder`, `wizard` and `teach` (unused),
`codebase-design` (merged into `complexity`), and
`improve-codebase-architecture` (superseded by `health-check`).

## Credits

Several skills are taken or adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) (MIT); see each
skill's history. The composition is this repo's own: local-file outputs under a
project work folder, scored reviews, the RFA/RFH axis, and the ticket pipeline.
