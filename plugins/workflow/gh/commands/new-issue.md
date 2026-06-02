---
description: Draft and create a well-formed GitHub issue with correct labels and template. Usage /gh:new-issue <description> [owner/repo]
---

# New Issue workflow

Arguments: `$ARGUMENTS`

## Step 1 — Parse args

- If the last whitespace-separated token matches `owner/repo` format (e.g. `MalasataXD/cc-plugins`), treat it as the target repo and the remainder as the description.
- Otherwise, the entire argument string is the description; resolve the repo:
  ```bash
  gh repo view --json nameWithOwner -q .nameWithOwner
  ```
- If that also fails, ask the user for the repo.

## Step 2 — Discover repo conventions

Run these in parallel (ignore 404 errors):

```bash
gh label list --repo <owner/repo> --limit 100 --json name,description
```

```bash
gh api repos/<owner>/<repo>/contents/.github/ISSUE_TEMPLATE
```

If template files are found, fetch the one whose filename or title best matches the inferred issue type (Step 3) and use it as the body skeleton. Otherwise fall back to the built-in skeletons below.

## Step 3 — Classify the issue

Pick exactly one type based on the user's description:

| Signals | Type |
|---|---|
| "broken", "crash", "error", "regression", reproduction steps | **Bug** |
| "add", "support", "would be nice", "feature", "enhancement" | **Feature** |
| "refactor", "rename", "cleanup", "chore", "docs", "bump" | **Task** |
| anything else | **Generic** |

## Step 4 — Draft the issue

Use the repo template if one was found. Otherwise use the matching built-in skeleton below.

Sections marked **(required)** must always be present. Sections marked **(optional)** are included only when the user's description supplies real content for them — never emit an empty heading or a placeholder like "N/A". If unsure, omit the section.

### Bug

- Title: `[Bug] <short, specific symptom>`
- Body sections:
  - `## Summary` (required)
  - `## Steps to reproduce` (required)
  - `## Expected` (required)
  - `## Actual` (required)
  - `## Environment` (optional — include when OS/version/browser/commit is known)
  - `## Notes` (optional — logs, links, related issues)
- Suggested label: `bug`

### Feature

- Title: `<verb> <object>` — imperative; skip a `[Feature]` prefix unless the repo convention uses it
- Body sections:
  - `## Problem` (required)
  - `## Proposal` (required)
  - `## Acceptance criteria` (optional but strongly preferred — render as a checklist)
  - `## Out of scope` (optional)
  - `## Open questions` (optional)
- Suggested label: `enhancement`

### Task

- Title: imperative verb + object (e.g. `Bump eslint to v9`, `Refactor auth middleware`)
- Body sections:
  - `## Goal` (required)
  - `## Scope` (optional — include only when a boundary needs calling out explicitly)
  - `## Definition of done` (required — checklist)
  - `## Notes` (optional)
- Suggested label: `chore` (or `refactor` / `docs` if more accurate)

### Generic

- Title: concise descriptor
- Body sections:
  - `## Context` (required)
  - `## What we want` (required)
  - `## Notes` (optional)
- No suggested labels.

### Quality bar — apply to every draft

- Title ≤ 80 chars; no trailing period; no issue number references.
- First line of body is one sentence summarising *what* and *why*.
- Be concrete: name files, functions, commands, or error strings when the user mentioned them.
- Use GitHub task-list checkboxes (`- [ ]`) for any "done when…" criteria.
- Never invent facts the user didn't supply — write `TODO: <what's missing>` instead.

### Label reconciliation

Intersect suggested labels with the real set from Step 2. Drop any that don't exist. If none survive, list the three closest real labels and let the user choose during approval.

## Step 5 — Show draft and wait for approval

Present the draft to the user:

```
**Repo:** <owner/repo>
**Title:** <title>
**Labels:** <comma-separated, or "(none)">
**Template:** <repo template path, or "built-in <type>">

---
<body>
---
Reply `ok` to create, or tell me what to change (title, labels, body, type).
```

Loop — apply requested edits and re-show — until the user explicitly approves. Do **not** call `gh issue create` before approval.

## Step 6 — Create

Write the approved body to a temp file, then run:

```bash
gh issue create \
  --repo <owner/repo> \
  --title "<title>" \
  --body-file <tempfile> \
  [--label "<label>" ...]
```

Using `--body-file` avoids shell-quoting issues with multi-line markdown.

On success: print the returned issue URL on its own line.

On failure: surface stderr verbatim and offer to retry without labels (the most common cause is a label not existing in the repo despite the discovery step).
