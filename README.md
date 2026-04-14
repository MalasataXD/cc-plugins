# cc-plugins

Personal [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace.

Three plugins:

| Plugin   | What you get                                                                                            |
| -------- | ------------------------------------------------------------------------------------------------------- |
| `think`  | `think-like` skill + editable persona library + `/think:like` and `/think:add` commands                 |
| `commit` | `commit` skill — imperative-title commits with structured bodies                                        |
| `review` | `review` skill — security, performance, quality, architecture, docs, with a 0–100 scoring rubric        |

## Install

From any Claude Code session:

```shell
/plugin marketplace add MalasataXD/cc-plugins
/plugin install think@cc-plugins
/plugin install commit@cc-plugins
/plugin install review@cc-plugins
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
    └── review/
        ├── .claude-plugin/plugin.json
        └── skills/review/
```

## License

MIT.
