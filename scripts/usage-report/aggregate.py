"""Aggregate sessions.json into the figures the report page needs (data.json)."""
import json, os, re, collections, statistics as st
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(__file__)
S = json.load(open(os.path.join(HERE, 'sessions.json'), encoding='utf-8'))
PLAN = {'to-spec', 'to-tickets', 'vet-tickets'}
TICK = {'next-ticket', 'implement', 'complete-ticket'}
NOISE = {'i', 'i-1', 'index', 'packageName', 'next-issue'}
CPH = timezone(timedelta(hours=2))
MODEL_NAMES = {'claude-fable-5-1': 'Fable 5.1', 'claude-fable-5': 'Fable 5', 'claude-opus-5': 'Opus 5', 'claude-opus-5-5': 'Opus 5.5',
               'claude-sonnet-5': 'Sonnet 5', 'claude-haiku-4-5-20251001': 'Haiku 4.5'}


def model_name(m):
    if m is None:
        return 'unknown'
    base = m.split(' (')[0]
    return MODEL_NAMES.get(base, base.replace('gpt-', 'GPT-').replace('-astra', ' Astra').replace('-sol', ' Sol'))


def cls(s):
    n = {k['skill'] for k in s['skills']}
    return 'planning' if n & PLAN else 'ticket' if n & TICK else 'other'


def main_model(s):
    return model_name(max(s['models'], key=s['models'].get)) if s['models'] else 'unknown'


def q(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo = int(k)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (k - lo)


for s in S:
    s['cls'] = cls(s)
    s['skills'] = [k for k in s['skills'] if k['skill'] not in NOISE]
    s['main_model'] = main_model(s)

out = {}

# -- per-session rows for the strip chart
out['sessions'] = [dict(tool=s['tool'], window=s['window'], cls=s['cls'], active=round(s['active_min'], 1), prompts=len(s['prompts']),
                        subagents=s['subagents'], created=len(s['ticket_files']), model=s['main_model'], project=s['project'],
                        day=datetime.fromisoformat(s['start']).astimezone(CPH).strftime('%Y-%m-%d'),
                        loaded=len({k['skill'] for k in s['skills'] if k['how'] != 'user'})) for s in S]

# -- workflow summary per tool x window x class
summary = []
for c in ('planning', 'ticket', 'other'):
    for tool in ('claude', 'codex'):
        for w in ('before', 'nightly'):
            x = [s for s in S if s['tool'] == tool and s['window'] == w and s['cls'] == c]
            if not x:
                continue
            act = [s['active_min'] for s in x]
            created = sum(len(s['ticket_files']) for s in x)
            touched = sum(len(s['touched']) for s in x)
            summary.append(dict(cls=c, tool=tool, window=w, n=len(x), hours=round(sum(act) / 60, 1),
                                med_active=round(st.median(act)), p25=round(q(act, .25)), p75=round(q(act, .75)),
                                med_prompts=st.median(len(s['prompts']) for s in x),
                                med_sub=st.median(s['subagents'] for s in x),
                                med_vet=st.median(s['vet_agents'] for s in x),
                                created=created, touched=touched,
                                min_per_created=round(sum(act) / created, 1) if created and c == 'planning' else None,
                                min_per_touched=round(sum(act) / touched, 1) if touched and c == 'ticket' else None,
                                med_loaded=st.median(len({k['skill'] for k in s['skills'] if k['how'] != 'user'}) for s in x)))
out['summary'] = summary

# -- totals per tool x window
out['totals'] = [dict(tool=t, window=w, n=len(x), hours=round(sum(s['active_min'] for s in x) / 60, 1),
                      prompts=sum(len(s['prompts']) for s in x))
                 for t in ('claude', 'codex') for w in ('before', 'nightly')
                 for x in [[s for s in S if s['tool'] == t and s['window'] == w]]]

# -- skill usage: sessions that used a skill, by tool/window, split by who triggered it
sk = collections.defaultdict(lambda: collections.Counter())
for s in S:
    seen = set()
    for k in s['skills']:
        key = (k['skill'], 'user' if k['how'] == 'user' else 'agent')
        if key in seen:
            continue
        seen.add(key)
        sk[k['skill']][f"{s['tool']}_{s['window']}_{key[1]}"] += 1
    for name in {k['skill'] for k in s['skills']}:
        sk[name][f"{s['tool']}_{s['window']}"] += 1
out['skills'] = sorted(({'skill': n, **c} for n, c in sk.items()), key=lambda r: -(r.get('claude_nightly', 0) + r.get('codex_nightly', 0) + r.get('claude_before', 0) + r.get('codex_before', 0)))

# -- skill x model per window: sessions where the skill ran under the model
sm = collections.defaultdict(collections.Counter)
for s in S:
    for name in {k['skill'] for k in s['skills']}:
        sm[(s['window'], name)][s['main_model']] += 1
out['skill_model'] = [dict(window=w, skill=n, **c) for (w, n), c in sm.items()]

# -- model mix per tool/window (main-thread sessions) and subagent models
mm = collections.Counter((s['tool'], s['window'], s['main_model']) for s in S)
out['models'] = [dict(tool=t, window=w, model=m, n=n) for (t, w, m), n in mm.items()]
sub = collections.Counter()
for s in S:
    for m, n in (s.get('sub_models') or {}).items():
        sub[(s['tool'], s['window'], model_name(m))] += n
out['sub_models'] = [dict(tool=t, window=w, model=m, turns=n) for (t, w, m), n in sub.items()]

# -- daily active hours per tool
daily = collections.Counter()
for s in S:
    daily[(out_day := datetime.fromisoformat(s['start']).astimezone(CPH).strftime('%Y-%m-%d'), s['tool'], s['cls'])] += s['active_min'] / 60
out['daily'] = [dict(day=d, tool=t, cls=c, hours=round(h, 2)) for (d, t, c), h in sorted(daily.items())]

# -- prompt patterns in ticket sessions
PAT = {
    'chain': re.compile(r'\b(grab|start on|continue with|do|kick ?off on|and then)\s+#?\d-\d', re.I),
    'handoff': re.compile(r'handoff', re.I),
    'subagents': re.compile(r'sub-?agents?', re.I),
}
pat = []
for tool in ('claude', 'codex'):
    for w in ('before', 'nightly'):
        x = [s for s in S if s['tool'] == tool and s['window'] == w and s['cls'] == 'ticket']
        prompts = [p['text'] for s in x for p in s['prompts']]
        row = dict(tool=tool, window=w, sessions=len(x), prompts=len(prompts))
        for k, rx in PAT.items():
            row[k] = sum(1 for p in prompts if rx.search(p))
        pat.append(row)
out['patterns'] = pat

json.dump(out, open(os.path.join(HERE, 'data.json'), 'w', encoding='utf-8'), indent=1)
for r in summary:
    print(r)
for r in pat:
    print(r)
print(out['totals'])
print(sorted(out['models'], key=lambda r: (r['tool'], r['window'])))
print(sorted(out['sub_models'], key=lambda r: (r['tool'], r['window'])))
