# Usage report

These scripts measure how skills are used across Claude Code (`~/.claude/projects`) and Codex (`~/.codex/sessions`, `archived_sessions`). They were written for the nightly trial readout.

Run them in order from this folder. Each one writes JSON next to itself (gitignored):

1. `python extract.py` writes `sessions.json`, one record per session.
2. `python aggregate.py` writes `data.json`, the figures behind the charts.
3. `python tickets.py` writes `tickets.json` and `per_ticket.json`, the per-ticket breakdown.

The windows are hardcoded at the top of `extract.py` (`START`, `SPLIT`, `END`). `SPLIT` is the first nightly commit, `cd07f68`. Change all three before measuring a new period.
