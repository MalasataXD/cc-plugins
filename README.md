# cc-plugins

Personal [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace.

Four plugins:

| Plugin   | What you get                                                                                            |
| -------- | ------------------------------------------------------------------------------------------------------- |
| `think`  | `think-like` skill + editable persona library + `/think:like` and `/think:add` commands                 |
| `commit` | `commit` skill — imperative-title commits with structured bodies                                        |
| `review` | `review` skill — security, performance, quality, architecture, docs, with a 0–100 scoring rubric        |
| `gh`     | GitHub CLI workflows — plate, digest, standup, project status moves, and well-formed issue drafting     |

## Install

From any Claude Code session:

```shell
/plugin marketplace add MalasataXD/cc-plugins
/plugin install think@cc-plugins
/plugin install commit@cc-plugins
/plugin install review@cc-plugins
/plugin install gh@cc-plugins
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

Personas live as editable markdown files at `plugins/think/skills/think-like/personas/`. Eleven are bundled (software-architect, backend-engineer, frontend-engineer, devops-sre, security-engineer, tech-lead, dba, product-manager, ux-designer, technical-writer, production-designer). Edit or add your own — each file is the source of truth.

`/think:add` drafts a new persona interactively, shows you the spec, and only writes to disk after you approve. Commit the resulting file back to this repo to sync it across machines.

## `commit`

Invokes automatically when you ask Claude to commit changes. Full style guide at `plugins/commit/skills/commit/references/commit-style.md`.

## `review`

Invokes when you ask for a code review. Returns scored feedback across security, performance, quality, style, architecture, and documentation. Rubric and checklists in `plugins/review/skills/review/references/`.

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

**First-time setup:** after installing, copy `plugins/gh/skills/gh/config.example.json` to `config.json` in the same folder and set `github_handle` to your GitHub username. The skill will prompt you if the file is missing.

Requires `gh auth refresh -s project` for project board commands (`/gh:move`).

## Layout

```
cc-plugins/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    ├── think/
    │   ├── .claude-plugin/plugin.json
    │   ├── skills/think-like/
    │   │   ├── SKILL.md
    │   │   └── personas/*.md
    │   └── commands/
    │       ├── like.md
    │       └── add.md
    ├── commit/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/commit/
    ├── review/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/review/
    └── gh/
        ├── .claude-plugin/plugin.json
        ├── skills/gh/
        │   ├── SKILL.md
        │   ├── config.example.json   # committed — copy to config.json and fill in
        │   ├── config.json           # gitignored — your personal settings
        │   ├── cache.json            # gitignored — auto-managed project ID cache
        │   └── references/
        │       ├── gh-cheatsheet.md
        │       └── project-ids.md
        └── commands/
            ├── plate.md
            ├── digest.md
            ├── standup.md
            ├── move.md
            └── new-issue.md
```

## License

MIT.
