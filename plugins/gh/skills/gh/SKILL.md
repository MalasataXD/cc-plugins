---
name: gh
description: >
  GitHub CLI workflows for issues and projects. Triggers automatically when
  the user asks about their open issues, upcoming work, what's on their plate,
  moving an issue to a new status, summarizing work done in a period, standup
  prep, drafting a new issue, tagging an issue, writing a well-formed issue,
  or anything phrased as "look at my issues", "what did we ship", "new issue",
  "move #<n> to <status>", "standup", "digest", "triage", or similar.
  Requires the gh-supercharged CLI extension.
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

### New Issue — draft then confirm

**Step 1 — resolve repo:**
- From the user's args (`owner/repo` as last token).
- Fallback: `gh repo view --json nameWithOwner`.
- If neither works, ask.

**Step 2 — preview draft:**
```bash
gh supercharged new-issue "<description>" --repo <owner/repo> --json
```

**Step 3 — show draft and get approval:**
Present the drafted title, labels, template, and body to the user. Say:
"Here's the draft — reply `ok` to create it, or tell me what to change."

**Step 4 — create:**
```bash
gh supercharged new-issue "<description>" --repo <owner/repo> --confirm
```

Confirm with the created issue URL.

---

## 4. Global Flags

| Flag | Description |
|---|---|
| `--json` | Structured JSON output (used internally for preview step) |
| `--repo owner/repo` | Target a specific repository |
| `--owner org` | Filter by organization or owner |
| `--verbose` | Show raw API errors for debugging |
