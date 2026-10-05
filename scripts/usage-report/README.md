# Usage report

These scripts measure how skills are used across Claude Code (`~/.claude/projects`) and Codex (`~/.codex/sessions`, `archived_sessions`). They were written for the nightly trial readout.

Run them in order from this folder. Each one writes JSON next to itself (gitignored):

1. `python extract.py` writes `sessions.json`, one record per session.
2. `python aggregate.py` writes `data.json`, the figures behind the charts.
3. `python tickets.py` writes `tickets.json` and `per_ticket.json`, the per-ticket breakdown.

The windows are hardcoded at the top of `extract.py` (`START`, `SPLIT`, `END`). `SPLIT` is the first nightly commit, `cd07f68`. Change all three before measuring a new period.

`baseline-sessions-2026-09-30.json` (gitignored, local only) is the `sessions.json` from the 30 September run, windowed before / nightly / now at 9 Sep 13:35 and 23 Sep 07:45 UTC. Claude Code deleted transcripts after 30 days until `cleanupPeriodDays` was raised to 365 on 5 Oct 2026, so from then on it is the only complete record of the pre-nightly Claude sessions (40, where a fresh extract finds 28).
