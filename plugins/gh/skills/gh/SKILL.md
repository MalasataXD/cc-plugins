---
name: gh
description: >
  GitHub CLI workflows for issues and projects. Triggers automatically when
  the user asks about their open issues, upcoming work, what's on their plate,
  moving an issue to a new status, summarizing work done in a period, standup
  prep, drafting a new issue, tagging an issue, writing a well-formed issue,
  or anything phrased as "look at my issues", "what did we ship", "new issue",
  "move #<n> to <status>", "standup", "digest", "triage", or similar.
  Requires the gh-supercharged CLI extension for plate/digest/standup/move.
---

# gh — GitHub CLI Skill

Orchestrate GitHub issue and project workflows via the `gh supercharged`
extension. Every workflow first checks the extension is installed and
configured, then delegates to the appropriate subcommand.

## 1. Bootstrap

### Check extension

Run:
```bash
gh extension list
```

If the output does not contain `supercharged`, tell the user:

> The `gh-supercharged` extension is required. Install it with:
> ```
> gh extension install MalasataXD/gh-supercharged
> ```

Then stop.

### Check config

Run:
```bash
gh supercharged config show
```

If `github_handle` is empty or `""`, tell the user:

> Your GitHub handle is not set. Open the config file:
> ```
> gh supercharged config path
> ```
> Set `github_handle` to your GitHub username, then re-run.

Then stop.

---

## 2. Intent Detection

Map the user's request to exactly one workflow:

| User says | Workflow |
|---|---|
| "what's on my plate", "my open issues", "upcoming work" | **Plate** |
| "digest", "what did we ship", "summarize last week / since <date>" | **Digest** |
| "standup", "what to report" | **Standup** |
| "move #<n> to <status>", "set status to", "mark as done/in progress" | **Move** |
| "new issue", "draft issue", "create issue", "open an issue", "write issue" | **New Issue** |

If the intent is ambiguous, state your interpretation and proceed. Do not ask
for confirmation unless there is a genuine fork (e.g., the user mentions both
"digest" and "move" — ask which one to do first).

---

## 3. Workflows

### Plate — open work assigned to me

```bash
gh supercharged plate              # current repo (default)
gh supercharged plate --full       # all repos (user says "everywhere" / "all repos")
gh supercharged plate --owner <o>  # filtered by org
gh supercharged plate --repo <owner/repo>
```

Use `--full` when the user asks for all repos or does not specify a repo
context. Use `--repo` or `--owner` when the user provides an explicit scope.

---

### Digest — period summary

```bash
gh supercharged digest [<since>] [--full] [--repo <owner/repo>]
```

Pass the user's `<since>` token verbatim. Accepted formats: `7d`, `2w`,
`last monday`, ISO date (`2026-04-10`). If omitted, the extension uses
`digest_window_days` from its own config.

Use `--full` for cross-repo digests; `--repo` to restrict to one repo.

---

### Standup — yesterday / today / blockers

```bash
gh supercharged standup            # current repo
gh supercharged standup --full     # all repos
```

Output format is driven by `standup_format` in the extension's config.

---

### Move — change a project status field

```bash
gh supercharged move <issue> "<status>" --repo <owner/repo>
```

Resolve `<owner/repo>`:
1. From the user's input (URL or explicit `owner/repo` arg).
2. Fallback: `gh repo view --json nameWithOwner`.

Status matching is case-insensitive; the extension handles Projects v2 ID
resolution and caches field metadata internally.

On error (stale cache / option not found): offer to run
`gh supercharged cache clear` and retry.

On success: confirm with "Moved #<n> → **<status>**."

---

### New Issue — draft then create

Does **not** use `gh supercharged`. Uses plain `gh issue create`.

**Step 1 — resolve repo**
- From the user's input (`owner/repo` as the last token).
- Fallback: `gh repo view --json nameWithOwner -q .nameWithOwner`.
- If neither works, ask the user.

**Step 2 — discover repo conventions** (run in parallel, ignore 404)
```bash
gh label list --repo <owner/repo> --limit 100 --json name,description
gh api repos/<owner>/<repo>/contents/.github/ISSUE_TEMPLATE
```
Use a matching repo template as the body skeleton if one exists; otherwise use the built-in skeleton for the inferred type.

**Step 3 — classify the issue**

| Signals | Type |
|---|---|
| "broken", "crash", "error", "regression", repro steps | **Bug** |
| "add", "support", "feature", "enhancement" | **Feature** |
| "refactor", "cleanup", "chore", "docs", "bump" | **Task** |
| anything else | **Generic** |

**Step 4 — built-in skeletons**

Sections marked **(optional)** are included only when the user's description supplies real content — never emit an empty heading or a placeholder like "N/A".

- **Bug** — Title: `[Bug] <symptom>` · Sections: `## Summary`, `## Steps to reproduce`, `## Expected`, `## Actual` (all required); `## Environment`, `## Notes` (optional) · Label: `bug`
- **Feature** — Title: imperative verb + object · Sections: `## Problem`, `## Proposal` (required); `## Acceptance criteria` (optional, checklist preferred), `## Out of scope`, `## Open questions` (optional) · Label: `enhancement`
- **Task** — Title: imperative verb + object · Sections: `## Goal`, `## Definition of done` (required, checklist); `## Scope`, `## Notes` (optional) · Label: `chore`
- **Generic** — Sections: `## Context`, `## What we want` (required); `## Notes` (optional) · No labels

Quality bar: title ≤ 80 chars, no trailing period, concrete over vague (name files/commands/errors), never invent facts (write `TODO:` instead).

Label reconciliation: intersect suggested labels with the real set from Step 2. If none match, list the three closest real labels and let the user choose.

**Step 5 — show draft and wait for approval**

```
**Repo:** <owner/repo>
**Title:** <title>
**Labels:** <labels, or "(none)">
**Template:** <repo template path, or "built-in <type>">

---
<body>
---
Reply `ok` to create, or tell me what to change.
```

Loop on edits until explicit approval. Do **not** run `gh issue create` before approval.

**Step 6 — create**
```bash
gh issue create \
  --repo <owner/repo> \
  --title "<title>" \
  --body-file <tempfile> \
  [--label "<label>" ...]
```

On success: print the issue URL. On failure: surface stderr and offer to retry without labels.

---

## 4. Global Flags

| Flag | Description |
|---|---|
| `--json` | Structured JSON output (used internally for preview step) |
| `--repo owner/repo` | Target a specific repository |
| `--owner org` | Filter by organization or owner |
| `--verbose` | Show raw API errors for debugging |
