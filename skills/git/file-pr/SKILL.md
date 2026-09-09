---
name: file-pr
description: Open a pull request in the house style, with a changelog body written from the branch's real diff. Use when the user asks to file, open, or raise a PR.
---

# File PR

Open a pull request for the current branch against the branch the user names, with a body that is a changelog of what actually changed: grouped entries, one per change, written from the diff. The body is written from the diff, never from memory of the conversation; the commit skill's rule applies here too — no "Generated with" or "Co-Authored-By" lines anywhere.

## Process

### 1. Gather the branch state

Run these together:

```bash
git status -sb                       # branch, upstream, anything uncommitted
git log --format="%h %s" <base>..HEAD # the commits this PR carries
git diff --stat <base>...HEAD         # the files it touches
gh pr list --state open --json number,headRefName,baseRefName,title
```

The **base** is the branch the user named. Without one, use the repository's integration branch (`dev` where it exists, otherwise the default branch).

Uncommitted changes stop the skill: say so and offer the `commit` skill. Do not push or open anything with a dirty tree.

### 2. Detect stacking

If an open PR's head branch is an ancestor of `HEAD` and is not yet merged into the base, this PR is **stacked** on it: use that head as the base, so the diff shows only the commits on top, and open the body with the stacked note from the template. Say which PR it stacks on when reporting.

### 3. Read the diff, not the log

Read the full diff against the base — `git diff <base>...HEAD` — plus the files it touches where the diff alone does not explain the change. Commit messages are a guide to grouping, not a source: a commit can describe an intent the final diff no longer matches, and squashed or reverted work must not appear in the body.

Group the changes by the **thing they change** — a rule, a seam, a tool, a contract, a setup step — not by file or by commit. Each group becomes a bold heading in the body, and each change inside it one entry.

### 4. Establish verification

The Verification section states only what was actually run at the branch head, with the command and the result. Reuse results from this session when they came from the branch head; otherwise run the project's checks now (test suite, type checker, lint, build — whatever the project has). Name what was **not** exercised, such as a UI that was never clicked through, so the reviewer knows where to look. Never claim a pass you did not see.

### 5. Draft the title and body

**Title:** imperative mood, under 70 characters, capitalized, no period — `Add purchasing foundation`, `Add Expo purchasing tools`, `Fix stale basket id across unit switch`.

**Body:** a changelog, not an essay. Follow the template:

- An opening paragraph of two or three sentences on what the PR establishes, in present tense ("This pull request adds…"), closing with "The most important changes are:".
- Groups as bold headings, named by the thing they change — a rule, a seam, a tool, a contract, a setup step.
- Each bullet is one **entry**: it opens with a past-tense verb (Added, Routed, Removed, Replaced, Migrated, Extended, Regenerated), names the real identifier in backticks, and ends with the reason or the consequence when either is not obvious. One change per entry; a change that needs a paragraph is two entries.
- Renames as `old` → `new`. Numbers where they change what the reviewer does: test counts, caps, line reductions.
- **Testing** lists the coverage the PR adds; **Verification** lists what was run and its result. They are different sections. **Breaking changes for clients** appears only when there are some.

<pr-template>

> Stacked on #<n> (`<head of #n>`). Merge that first; this PR only contains the commits on top of it.

_(Blockquote only when stacked or blocked; a blocked PR names what it waits on and why merging early would break.)_

This pull request <establishes / adds / replaces> … . <Second sentence: the shape of the change or what it removes.> The most important changes are:

**<Group>**
- Added `NewSeam` in `src/area` and routed `CallerA`, `CallerB`, and `CallerC` through it; the private copies are removed.
- Removed the `PrimaryUnitId` fallback. Missing unit context now fails explicitly.

**<Group>**
- ...

**Breaking changes for clients**
- `old` → `new`, and what a client must do about it.

**Testing**
- The coverage added, by kind and area: contract, handler, authorization, fixture.

**Verification**
- `<command>` at the branch head: <result, with counts>.
- What was not exercised, and what a reviewer should click through.

</pr-template>

Pass the body through the `unslop` skill — a PR body is read by people, and every one goes through that pass. Then show the title and body in the conversation and wait for the go-ahead. A PR is visible to the whole team, so this is the one confirmation the skill takes.

### 6. Open it

Push the branch with `-u` if it has no upstream. Write the body to a temporary file and pass it with `--body-file` so quoting survives every shell:

```bash
gh pr create --base <base> --head <branch> --title "<title>" --body-file <path>
```

Report the PR URL, the base it targets, and the number it stacks on, if any.
