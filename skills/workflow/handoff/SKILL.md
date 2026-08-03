---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section naming the skills the next agent should reach for, and where in the pipeline the work sits — `next-ticket` when a ticket is chosen but unplanned, `implement` when a plan is approved and the build is underway, `complete-ticket` when the work looks finished, `diagnosing-bugs` when the session was chasing a symptom. Name the specific ticket or spec file where one exists.

This transfers a **conversation**; `complete-ticket` judges a **ticket**. Reach for that one instead when the question is whether the work is done.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
