---
name: github-attribution
description: The attribution note that closes every write to GitHub — a PR body, a PR or issue comment, a review, an issue. Use before running any `gh` command that creates or edits text on GitHub, or when another skill needs the note.
---

# GitHub attribution

Anything the agent writes to GitHub is read by people who cannot see this session, so every write closes with a note saying which model wrote it and for whom. The note is the default for every `gh` write; leave it out only when the user says so for that write.

## The note

The last thing in the body, after a blank line, as a GitHub alert:

```markdown
> [!NOTE]
> Filed by <model name> on behalf of <name>.
```

- **`<model name>`** is the running model's display name — Fable 5.1, Opus 5, GPT-5 Codex — not the API slug and not the vendor alone.
- **`<name>`** is `git config user.name`. Outside a repository, ask.

The note applies to every write: `gh pr create`, `gh pr comment`, `gh pr review`, `gh issue create`, `gh issue comment`, and any `--edit` of those bodies. Edits keep the note of the body they edit. Pass a body with `--body-file` so the blank line and the `>` survive the shell.

The note covers GitHub only. Commit messages carry no attribution; the `commit` skill owns that rule.
