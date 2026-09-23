"""Break ticket-session time down: tickets per session, ticket category, agent vs user time, commits."""
import json, glob, os, re, collections, statistics as st
from datetime import datetime, timedelta, timezone

HOME = os.path.expanduser('~')
HERE = os.path.dirname(__file__)
IDLE = timedelta(minutes=10)
TICKET = re.compile(r'tickets[\\/]+(?:([A-Za-z][A-Za-z0-9_.-]*)[\\/]+)?([0-9][A-Za-z0-9_.-]*\.md)')
CAT = re.compile(r'^\+?Category:\s*(\w+)', re.M)
TYP = re.compile(r'^\+?Type:\s*(\w+)', re.M)
S = json.load(open(os.path.join(HERE, 'sessions.json'), encoding='utf-8'))
PLAN = {'to-spec', 'to-tickets', 'vet-tickets'}
TICK = {'next-ticket', 'implement', 'complete-ticket'}
ts = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))

catalog = {}  # "dir/file" -> dict(cat, type)


def note_ticket(path, text):
    m = TICKET.search(path or '')
    if not m or not text:
        return
    c, t = CAT.search(text), TYP.search(text)
    if c or t:
        catalog[f'{m.group(1)}/{m.group(2)}'] = dict(cat=c.group(1) if c else None, type=t.group(1) if t else None)


def refs(text):
    return {f'{a}/{b}' for a, b in TICKET.findall(text or '')}


def claude_events(path, main=True):
    """Yield (time, kind, payload) for one Claude transcript; kind in user/agent."""
    for line in open(path, encoding='utf-8'):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get('type') not in ('user', 'assistant') or 'timestamp' not in d:
            continue
        t = ts(d['timestamp'])
        msg = d['message']
        if d['type'] == 'assistant':
            for b in msg.get('content', []):
                if isinstance(b, dict) and b.get('type') == 'tool_use':
                    inp = b.get('input') or {}
                    if b['name'] == 'Write':
                        note_ticket(inp.get('file_path'), inp.get('content'))
                    yield t, 'agent', dict(tool=b['name'], inp=inp)
            yield t, 'agent', None
        else:
            c = msg.get('content')
            is_prompt = main and not d.get('isMeta') and (isinstance(c, str) or not any(isinstance(b, dict) and b.get('type') == 'tool_result' for b in c or []))
            txt = c if isinstance(c, str) else ' '.join(b.get('text', '') for b in c or [] if isinstance(b, dict))
            if is_prompt and txt.strip() and not txt.lstrip().startswith(('<local-command', '<system-reminder>', '<task-notification>', 'Caveat:')):
                yield t, 'user', txt
            else:
                yield t, 'tool', None


def codex_events(path):
    born = None
    for line in open(path, encoding='utf-8'):
        d = json.loads(line)
        p = d.get('payload') or {}
        if d.get('type') == 'session_meta':
            born = born or ts(p['timestamp'])
            continue
        if not born or 'timestamp' not in d or ts(d['timestamp']) < born:
            continue
        t = ts(d['timestamp'])
        if d['type'] == 'event_msg' and p.get('type') in ('task_started', 'thread_settings_applied'):
            yield t, 'user', ''
            continue
        if d['type'] == 'event_msg' and p.get('type') == 'item_completed':
            it = p.get('item') or {}
            k = it.get('type')
            if k == 'UserMessage':
                yield t, 'tool',' '.join(c.get('text', '') for c in it.get('content', []) if isinstance(c, dict))
                continue
            if k == 'CommandExecution':
                yield t, 'agent', dict(tool='cmd', inp={'command': ' '.join(it.get('command') or [])})
                continue
            if k == 'FileChange':
                for path_, ch in (it.get('changes') or {}).items():
                    if ch.get('type') == 'add':
                        note_ticket(path_, ch.get('unified_diff') or ch.get('content'))
                    yield t, 'agent', dict(tool='edit', inp={'file_path': path_, 'diff': ch.get('unified_diff') or ''})
                continue
        if d['type'] == 'response_item' and p.get('type') == 'custom_tool_call' and 'rg ' not in (p.get('input') or ''):
            yield t, 'agent', dict(tool='exec', inp={'command': p.get('input') or ''})
            continue
        yield t, 'agent', None


# ---- pass 1: every file, to build the ticket catalog; keep events for ticket sessions
claude_files = {os.path.basename(f)[:-6]: f for f in glob.glob(os.path.join(HOME, '.claude/projects/*/*.jsonl'))}
codex_files = collections.defaultdict(list)
for f in glob.glob(os.path.join(HOME, '.codex/sessions/2026/*/*/*.jsonl')) + glob.glob(os.path.join(HOME, '.codex/archived_sessions/*.jsonl')):
    if os.path.getmtime(f) < 1788000000:
        continue
    with open(f, encoding='utf-8') as fh:
        first = json.loads(fh.readline())
    codex_files[first['payload']['id']].append(f)

for f in glob.glob(os.path.join(HOME, '.claude/projects/*/*.jsonl')) + glob.glob(os.path.join(HOME, '.claude/projects/*/*/subagents/*.jsonl')):
    if os.path.getmtime(f) > 1788000000:
        for _ in claude_events(f):
            pass
for fs in codex_files.values():
    for f in fs:
        for _ in codex_events(f):
            pass

rows = []
for s in S:
    names = {k['skill'] for k in s['skills']}
    if names & PLAN or not names & TICK:
        continue
    if s['tool'] == 'claude':
        ev = list(claude_events(claude_files[s['id']]))
        sub = glob.glob(os.path.join(os.path.dirname(claude_files[s['id']]), s['id'], 'subagents', '*.jsonl'))
    else:
        ev = sorted((e for f in codex_files[s['id']] for e in codex_events(f)), key=lambda e: e[0])
        sub = []
    ev.sort(key=lambda e: e[0])
    agent = user = 0.0
    for (t0, k0, _), (t1, k1, _) in zip(ev, ev[1:]):
        gap = min(t1 - t0, IDLE).total_seconds() / 60
        if k1 == 'user':
            user += gap
        else:
            agent += gap
    touched, done, commits = set(), set(), 0
    for _, k, p in ev:
        if k == 'user':
            continue
        if isinstance(p, dict):
            blob = json.dumps(p['inp'])
            r_ = refs(blob.replace('\\\\', '\\'))
            touched |= r_
            if len(r_) == 1 and re.search(r'\bCompleted\b', blob):
                done |= r_
            if re.search(r'\bgit\s+(?:-C\s+\S+\s+)?commit\b', blob):
                commits += 1
    rows.append(dict(tool=s['tool'], window=s['window'], project=s['project'], start=s['start'][:16], active=s['active_min'],
                     agent=agent, user=user, prompts=len(s['prompts']), commits=commits, subagents=s['subagents'],
                     tickets=sorted(touched), done=sorted(done), cats=[(catalog.get(x) or {}).get('cat') for x in sorted(done)]))

json.dump(dict(rows=rows, catalog=catalog), open(os.path.join(HERE, 'tickets.json'), 'w'), indent=1)
print('catalog', len(catalog), collections.Counter(v['cat'] for v in catalog.values()))
med = lambda xs: round(st.median(xs), 1) if xs else '-'
for tool in ('claude', 'codex'):
    for w in ('before', 'nightly'):
        x = [r for r in rows if r['tool'] == tool and r['window'] == w]
        nt = [len(r['done']) for r in x]
        tot_t = sum(nt)
        print(f"{tool:6} {w:7} n={len(x):3} med_active={med([r['active'] for r in x])} med_agent={med([r['agent'] for r in x])} med_user={med([r['user'] for r in x])} "
              f"agent_h={sum(r['agent'] for r in x)/60:.1f} user_h={sum(r['user'] for r in x)/60:.1f} med_tickets={med(nt)} tickets={tot_t} commits={sum(r['commits'] for r in x)} "
              f"min/ticket={sum(r['active'] for r in x)/tot_t if tot_t else 0:.1f} min/commit={sum(r['active'] for r in x)/max(1,sum(r['commits'] for r in x)):.1f} "
              f"cats={dict(collections.Counter(c for r in x for c in r['cats']))}")

# ---- per-ticket figures for the report (per_ticket.json): real ticket sessions only
MANUAL_TEST = re.compile(r'\[Image|clipboard|test(ed)? it|works nicely|it works|try (it )?now|I can see|doesn.t work|I don.t see', re.I)
by_key = {s['start'][:16] + s['tool']: s for s in S}


def worked_tickets(r):
    """A session counts when you invoked next-ticket or it marked a ticket Completed."""
    return r['done'] or any(k['skill'] == 'next-ticket' and k['how'] == 'user' for k in by_key[r['start'] + r['tool']]['skills'])


per_ticket = {}
for tool in ('claude', 'codex', 'all'):
    per_ticket[tool] = {}
    for w in ('before', 'nightly'):
        x = [r for r in rows if (tool == 'all' or r['tool'] == tool) and r['window'] == w and worked_tickets(r)]
        done = sum(len(r['done']) for r in x)
        active = sum(r['active'] for r in x)
        tests = sum(1 for r in x for p in by_key[r['start'] + r['tool']]['prompts'] if MANUAL_TEST.search(p['text']))
        per_ticket[tool][w] = dict(sessions=len(x), done=done, perSession=round(done / len(x), 2), minPer=round(active / done),
                                   userShare=round(100 * sum(r['user'] for r in x) / active), testPer=round(tests / done, 2))
json.dump(per_ticket, open(os.path.join(HERE, 'per_ticket.json'), 'w'), indent=1)
print(json.dumps(per_ticket))
