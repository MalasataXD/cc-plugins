---
name: health-check
description: Check the codebase's health and suggest the few places where reducing complexity would pay off most.
disable-model-invocation: true
---

The user has asked for a **health check**: a short, ranked list of the places where reducing complexity would pay off most, backed by evidence from the codebase's history. You suggest; you do not refactor and you write no files.

## Steps

1. Load the `complexity` skill and read both of its references, then load `code-smells`. Read `GLOSSARY.md` and any ADRs in `docs/adr/` if they exist (see the `domain-modeling` skill), so findings use the project's names and don't re-suggest what an ADR settled.

2. Find the **hot spots**. If the user named an area, that area is the scope; go to step 3. Otherwise read the recent history (`git log --name-only`, a few hundred commits or the last few months, whichever is shorter) for:

   - **Churn**: the files that change most often.
   - **Co-change**: files that keep changing in the same commits. This is change amplification in the wild.
   - **Fix clusters**: fix commits concentrated in one area.

   Keep the handful of areas with the strongest signal. A problem in code nobody changes is not a finding.

3. Read each hot spot through these lenses:

   - **Shallow modules**: apply the deletion test. Does the module concentrate complexity, or just move it?
   - **Scattered concepts**: one concept spread across modules that always change together.
   - **Unreachable behaviour**: logic no seam can reach without mocking internals or testing past the interface.
   - **Smells**: structural entries from the `code-smells` baseline.

   The step is done when every hot spot has either produced a candidate or been dropped for a stated reason.

4. Present 3 to 5 candidates in chat, most severe first. For each:

   - **Area**: the modules involved, named as `GLOSSARY.md` names them.
   - **Evidence**: the churn, co-change, or fix commits that put it on the list.
   - **Problem**: one sentence naming the symptom (change amplification, cognitive load, or unknown unknowns).
   - **Move**: one sentence: deepen, fold into its caller, or move the seam.
   - **Strength**: `Strong`, `Worth exploring`, or `Speculative`.

   A candidate that contradicts an ADR appears only when the friction is real enough to reopen it, and says which ADR.

   End with the candidate you would tackle first and why, and offer to run `to-spec` on it.
