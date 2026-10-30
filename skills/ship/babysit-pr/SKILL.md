---
name: babysit-pr
description: Carry an open pull request to green CI, pushing the fixes and merges it needs.
disable-model-invocation: true
---

# Babysit PR

Carry an open pull request to green CI. Invoking this skill is the user's go-ahead to push to the pull request's branch. Merging the pull request stays with the user.

Fix the **cause** of each failure, and keep every test and check as strong as it was. When a test itself looks wrong, stop and report it.

## Process

### 1. Pin the PR

Resolve the pull request's number, base, head branch, head SHA, and author:

```bash
gh pr view <n> --json number,baseRefName,headRefName,headRefOid,mergeable,author
```

Work on the head branch. With no pull request, point to `file-pr` and stop. With uncommitted changes, stop and offer `commit`. Confirm before pushing to a pull request the user didn't open.

### 2. Clear conflicts

When the pull request conflicts with its base, merge the base into the branch, resolve the conflicts, run the project's checks, and push. A rebase rewrites history, so it waits for the user. Stop and report a conflict that needs a decision about which behaviour wins.

### 3. Wait for CI

Wait for the checks on the head SHA with the harness's watcher (`watch_pull_request` in T3), and end the turn until it reports. When the pull request has no checks, report that and stop.

When every check is green, go to step 5. A new conflict goes back to step 2, and a red check goes to step 4.

### 4. Fix a red check

When the failure has nothing to do with the diff and looks flaky, re-run it once with `gh run rerun <run id> --failed`, then go back to step 3. This costs no round.

Otherwise, find the cause through the `diagnosing-bugs` skill, fix it, run the project's checks, commit with the `commit` skill, and push. Each pushed fix is one round. Go back to step 3.

Two rounds is the cap. When CI is still red after the second, stop. Stop sooner when a fix needs a design decision.

### 5. Report

Stop watching the pull request, then report in the conversation, omitting any line with nothing to say:

<output-format>
## Babysit PR: <pull request URL>

**CI:** Green / Red at `<short sha>`

**Fixes:** Each fix and its `<short sha>`, with the rounds used.

**Left for you:** What is still red or undecided, and why it stopped.

**Review comments:** Any that arrived, listed without action.

**Ship:** Pushed changes moved the head, so an earlier `ship` verdict no longer covers this branch.
</output-format>
