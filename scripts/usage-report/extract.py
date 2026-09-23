"""Extract per-session facts from Claude Code transcripts and Codex rollouts into sessions.json."""
import json, glob, os, re, collections
from datetime import datetime, timezone, timedelta

HOME = os.path.expanduser('~')
START = datetime(2026, 8, 26, tzinfo=timezone.utc)
SPLIT = datetime(2026, 9, 9, 13, 35, tzinfo=timezone.utc)  # cd07f68, first nightly commit
END = datetime(2026, 9, 23, 23, 59, tzinfo=timezone.utc)
IDLE_CAP = timedelta(minutes=10)
CPH = timezone(timedelta(hours=2))

REPO_SKILLS = {os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(HOME, 'sandbox/cc-plugins/skills/*/*/SKILL.md'))}
INSTALLED = {os.path.basename(p) for p in glob.glob(os.path.join(HOME, '.agents/skills/*'))} | {os.path.basename(p) for p in glob.glob(os.path.join(HOME, '.claude/skills/*'))}
KNOWN = REPO_SKILLS | INSTALLED | {'handoff', 'wait-what', 'teach', 'batch-grill-me'}


def ts(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def active_minutes(times):
    times = sorted(times)
    return sum(min(b - a, IDLE_CAP).total_seconds() for a, b in zip(times, times[1:])) / 60


def new_session(tool, sid, project):
    return dict(tool=tool, id=sid, project=project, times=[], prompts=[], skills=[], models=collections.Counter(),
                subagents=0, vet_agents=0, ticket_files=set(), touched=set(), compactions=0)


def finish(s):
    t = s.pop('times')
    if not t:
        return None
    s['start'] = min(t).isoformat()
    s['end'] = max(t).isoformat()
    s['wall_min'] = (max(t) - min(t)).total_seconds() / 60
    s['active_min'] = active_minutes(t)
    s['window'] = 'before' if min(t) < SPLIT else 'nightly'
    s['ticket_files'] = sorted(s['ticket_files'])
    s['touched'] = sorted(s['touched'])
    # a /skill invocation is logged twice (command + expansion); keep one
    s['prompts'] = [p for i, p in enumerate(s['prompts']) if i == 0 or p['text'] != s['prompts'][i - 1]['text']]
    s['models'] = dict(s['models'])
    return s


# ---------------- Claude Code ----------------
def claude_text(content):
    if isinstance(content, str):
        return content
    if any(isinstance(b, dict) and b.get('type') == 'tool_result' for b in content):
        return None
    return '\n'.join(b.get('text', '') for b in content if isinstance(b, dict) and b.get('type') == 'text')


def is_ticket_path(p):
    return bool(re.search(r'[\\/]tickets[\\/].+\.md$', p or ''))


def scan_claude_file(path, s, main):
    model = None
    for line in open(path, encoding='utf-8'):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if 'timestamp' not in d or d.get('type') not in ('user', 'assistant', 'system'):
            continue
        t = ts(d['timestamp'])
        if not (START <= t <= END):
            continue
        s['times'].append(t)
        if d['type'] == 'assistant':
            m = d['message'].get('model')
            if m and m != '<synthetic>':
                model = m
                s['models'][m] += 1
            for b in d['message'].get('content', []):
                if not isinstance(b, dict) or b.get('type') != 'tool_use':
                    continue
                inp = b.get('input') or {}
                if b['name'] == 'Skill':
                    s['skills'].append(dict(skill=inp.get('skill', '').split(':')[-1], how='agent' if main else 'subagent', model=model, t=t.isoformat()))
                elif b['name'] in ('Agent', 'Task') and main:
                    s['subagents'] += 1
                    if re.search(r'vet', (inp.get('prompt', '') + inp.get('description', '')), re.I):
                        s['vet_agents'] += 1
                elif b['name'] in ('Write', 'Edit', 'MultiEdit') and is_ticket_path(inp.get('file_path')):
                    name = os.path.basename(inp['file_path'])
                    if name.upper() != 'LATER.MD':
                        s['touched'].add(name)
                        if b['name'] == 'Write':
                            s['ticket_files'].add(name)
        elif d['type'] == 'user' and main and not d.get('isMeta') and not d.get('isSidechain'):
            txt = claude_text(d['message'].get('content'))
            if not txt or not txt.strip():
                continue
            cmd = re.search(r'<command-name>/?([^<]+)</command-name>', txt)
            if cmd:
                name = cmd.group(1).split(':')[-1]
                if name in KNOWN:
                    s['skills'].append(dict(skill=name, how='user', model=model, t=t.isoformat()))
                    s['prompts'].append(dict(t=t.isoformat(), text='/' + name))
                continue
            if txt.lstrip().startswith(('<local-command', '<system-reminder>', '<task-notification>', '[Request interrupted', 'Caveat:', '<command-message>')):
                continue
            s['prompts'].append(dict(t=t.isoformat(), text=txt.strip()[:400]))
            if 'compact' in txt[:40].lower():
                s['compactions'] += 1


def claude_sessions():
    out = []
    for f in glob.glob(os.path.join(HOME, '.claude/projects/*/*.jsonl')):
        if datetime.fromtimestamp(os.path.getmtime(f), timezone.utc) < START:
            continue
        project = os.path.basename(os.path.dirname(f)).split('-')[-1]
        sid = os.path.basename(f)[:-6]
        s = new_session('claude', sid, project)
        scan_claude_file(f, s, True)
        for sub in glob.glob(os.path.join(os.path.dirname(f), sid, 'subagents', '*.jsonl')):
            sub_s = new_session('claude', sid, project)
            scan_claude_file(sub, sub_s, False)
            s['skills'] += sub_s['skills']
            s['ticket_files'] |= sub_s['ticket_files']
            s['touched'] |= sub_s['touched']
            for m, n in sub_s['models'].items():
                s.setdefault('sub_models', collections.Counter())[m] += n
        if 'sub_models' in s:
            s['sub_models'] = dict(s['sub_models'])
        if s['prompts']:
            out.append(finish(s))
    return [s for s in out if s]


# ---------------- Codex ----------------
SKILL_READ = re.compile(r'skills[\\/]+(?:\.system[\\/]+)?([A-Za-z0-9_-]+)[\\/]+SKILL\.md')
SKILL_MENTION = re.compile(r'\[\$([A-Za-z0-9_:-]+)\]')


def codex_sessions():
    files = {}
    for f in glob.glob(os.path.join(HOME, '.codex/sessions/2026/*/*/*.jsonl')) + glob.glob(os.path.join(HOME, '.codex/archived_sessions/*.jsonl')):
        files.setdefault(os.path.basename(f), f)
    threads = {}
    seen = set()
    for f in files.values():
        if datetime.fromtimestamp(os.path.getmtime(f), timezone.utc) < START:
            continue
        meta = None
        model = None
        for line in open(f, encoding='utf-8'):
            d = json.loads(line)
            p = d.get('payload') or {}
            if d.get('type') == 'session_meta':
                if meta is None:
                    meta = p
                    tid = p['id']
                    root = p.get('session_id', tid)
                    th = threads.get(tid)
                    if th is None:
                        th = threads[tid] = new_session('codex', tid, os.path.basename(p.get('cwd', '')))
                        th['root'] = root
                        th['source'] = p.get('thread_source')
                        th['parent'] = p.get('parent_thread_id')
                        th['agent_path'] = ((p.get('source') or {}).get('subagent', {}) if isinstance(p.get('source'), dict) else {}).get('thread_spawn', {}).get('agent_path') if isinstance(p.get('source'), dict) else None
                    born = ts(p['timestamp'])
                continue
            if meta is None or 'timestamp' not in d:
                continue
            t = ts(d['timestamp'])
            if t < born or not (START <= t <= END):
                continue
            key = (tid, d.get('ordinal'), d.get('type'), p.get('type'))
            if key in seen:
                continue
            seen.add(key)
            th['times'].append(t)
            if d['type'] == 'turn_context' and p.get('model'):
                model = p['model']
                eff = p.get('effort') or p.get('reasoning_effort') or (p.get('collaboration_mode') or {}).get('settings', {}).get('reasoning_effort')
                th['models'][model + (f' ({eff})' if eff else '')] += 1
            if d['type'] == 'event_msg' and p.get('type') == 'item_completed':
                it = p.get('item') or {}
                k = it.get('type')
                if k == 'UserMessage':
                    txt = '\n'.join(c.get('text', '') for c in it.get('content', []) if isinstance(c, dict))
                    for m in SKILL_MENTION.findall(txt):
                        th['skills'].append(dict(skill=m.split(':')[-1], how='user', model=model, t=t.isoformat()))
                    if not txt.lstrip().startswith(('<heartbeat>', '<send_user_message')):
                        th['prompts'].append(dict(t=t.isoformat(), text=txt.strip()[:400]))
                elif k == 'CommandExecution':
                    cmd = ' '.join(it.get('command') or [])
                    for m in set(SKILL_READ.findall(cmd)):
                        th['skills'].append(dict(skill=m, how='agent', model=model, t=t.isoformat()))
                elif k == 'FileChange':
                    for path, ch in (it.get('changes') or {}).items():
                        name = os.path.basename(path)
                        if is_ticket_path(path) and name.upper() != 'LATER.MD':
                            th['touched'].add(name)
                            if ch.get('type') == 'add':
                                th['ticket_files'].add(name)
                elif k == 'ContextCompaction':
                    th['compactions'] += 1
                elif k == 'SubAgentActivity' and it.get('kind') == 'started':
                    th['subagents'] += 1
                    if re.search(r'vet', it.get('agent_path') or '', re.I):
                        th['vet_agents'] += 1
    # fold subagent threads into their user-facing root
    roots = {tid: th for tid, th in threads.items() if th['source'] == 'user'}
    for tid, th in threads.items():
        if th['source'] == 'user':
            continue
        r = roots.get(th['root'])
        if not r:
            continue
        if th['source'] == 'subagent':
            for sk in th['skills']:
                r['skills'].append(dict(sk, how='subagent'))
            r['ticket_files'] |= th['ticket_files']
            r['touched'] |= th['touched']
            r.setdefault('sub_models', collections.Counter()).update(th['models'])
    out = []
    for th in roots.values():
        for k in ('root', 'source', 'parent', 'agent_path'):
            th.pop(k, None)
        if 'sub_models' in th:
            th['sub_models'] = dict(th['sub_models'])
        if th['prompts']:
            s = finish(th)
            if s:
                out.append(s)
    return out


if __name__ == '__main__':
    sessions = claude_sessions() + codex_sessions()
    for s in sessions:
        # collapse repeated SKILL.md reads: one "agent" load per skill per session is what matters
        seen, uniq = set(), []
        for sk in sorted(s['skills'], key=lambda x: x['t']):
            k = (sk['skill'], sk['how'])
            if sk['how'] != 'user' and k in seen:
                continue
            seen.add(k)
            uniq.append(sk)
        s['skill_reads'] = len(s['skills'])
        s['skills'] = uniq
    json.dump(sessions, open(os.path.join(os.path.dirname(__file__), 'sessions.json'), 'w'), indent=1, default=str)
    c = collections.Counter((s['tool'], s['window']) for s in sessions)
    print(c)
