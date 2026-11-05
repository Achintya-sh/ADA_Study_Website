import re, sys, os, json
ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(ROOT, *a)
H = open(P('src', 'original', 'nb.html'), encoding='utf-8').read()      # the original notebook
SN = open(P('src', 'snippets', 'snips.py'), encoding='utf-8').read()
CODE = {m.group(1): m.group(2).rstrip() + '\n' for m in re.finditer(r'#@@ (\w+)\n(.*?)(?=\n#@@ |\Z)', SN, re.S)}

def tpl(path):
    s = open(path, encoding='utf-8').read()
    return {m.group(1): m.group(2).strip('\n') for m in re.finditer(r'<!--@@ (\w+) -->\n(.*?)(?=\n<!--@@ |\Z)', s, re.S)}
T = {}
for f in ('templates_a.html', 'templates_b.html', 'templates_c.html', 'templates_d.html'):
    T.update(tpl(P('src', 'templates', f)))

def fill(html):
    def rep(m):
        name = m.group(1)
        if name not in CODE: raise SystemExit('missing code block ' + name)
        return '<script type="text/plain" class="code">\n' + CODE[name] + '</script>'
    return re.sub(r'\{\{code:(\w+)\}\}', rep, html)

def section(id_):
    m = re.search(r'<section class="topic" id="%s"[^>]*>.*?\n</section>' % id_, H, re.S)
    if not m: raise SystemExit('no section ' + id_)
    return m

def body(id_, keep_idea=False):
    s = section(id_).group(0)
    s = re.sub(r'^<section[^>]*>\n', '', s)
    s = re.sub(r'<div class="topic-head">.*?</div></div>\n', '', s, count=1, flags=re.S)
    if not keep_idea:
        s = re.sub(r'<div class="box idea">.*?</div>\n', '', s, count=1, flags=re.S)
    s = re.sub(r'<div class="quiz" data-quiz="\w+"></div>\n?', '', s)
    s = re.sub(r'\n</section>$', '', s)
    return s.strip('\n')

def head(id_, num, title, meta, group):
    return ('<section class="topic" id="%s" data-group="%s" data-num="%s" data-title="%s">\n'
            '<div class="topic-head"><div class="badge">%s</div><div><div class="meta">%s</div><h2>%s</h2></div></div>\n') % (id_, group, num, title, num, meta, title)

# ---------- new stops
c2, c3, c4 = body('c2'), body('c3'), body('c4', keep_idea=True)
ch11 = (head('ch11', '11', 'Greedy algorithms', 'Dynamic programming and greedy line · weeks 1–12', 'dp') + c4 + '\n' + T['ch11_extra'] + '\n' + T['ch11_more'] +
        '\n<div class="quiz" data-quiz="c4"></div>\n</section>')
ch12 = head('ch12', '12', 'Graphs II: order, cycles, weights', 'Graphs line · week 11', 'graph') + T['ch12'] + '\n</section>'
ch13 = head('ch13', '13', 'Monotonic stacks and queues', 'Sorting and trees line · a stop your outline lists', 'trees') + T['ch13'] + '\n</section>'
ch14 = head('ch14', '14', 'Contest toolkit', 'Foundations line · Python, limits, routine, tricks', 'found') + T['ch14'] + '\n</section>'
ch15 = head('ch15', '15', 'Bridges: tools you know, combined', 'Dynamic programming and greedy line · tree DP, DAG DP, binary search, union-find, heaps, trie', 'dp') + T['ch15'] + '\n</section>'
ch16 = head('ch16', '16', 'Contest readiness', 'Foundations line · constraints, Python pitfalls, templates, interview, 3-hour mock', 'found') + T['ch16'] + '\n</section>'
ch17 = head('ch17', '17', 'Appendix: beyond the outline', 'Foundations line · merge sort, amortised analysis, hashing, what comes next', 'found') + T['ch17'] + '\n</section>'
ladder = head('ladder', 'L', 'The Ladder', 'Practise at the edge of your ability', 'ladder') + T['ladder'] + '\n</section>'
new_block = '\n\n'.join([
    '<!-- ===================================================== 11 -->', ch11,
    '<!-- ===================================================== 12 -->', ch12,
    '<!-- ===================================================== 13 -->', ch13,
    '<!-- ===================================================== 14 -->', ch14,
    '<!-- ===================================================== 15 -->', ch15,
    '<!-- ===================================================== 16 -->', ch16,
    '<!-- ===================================================== 17 -->', ch17,
    '<!-- ===================================================== LADDER -->', ladder]) + '\n\n'

# ---------- cut the old contest line (c1..c5) and drop in the new stops
a = H.index('<!-- ===================================================== C1 -->')
mock = H.index('<section class="topic" id="mock"')
H = H[:a] + new_block + H[mock:]

# ---------- patterns appended to existing stops (before each stop's own quiz)
def inject(stop_quiz, html, after=''):
    global H
    marker = '<div class="quiz" data-quiz="%s"></div>' % stop_quiz
    assert H.count(marker) == 1, (marker, H.count(marker))
    H = H.replace(marker, html + '\n' + marker + after)

inject('s3', T['ch3']); inject('s4', T['ch4']); inject('s5', T['ch5']); inject('s6', T['ch6'])
inject('s8', T['ch8_head'] + '\n' + c2 + '\n' + T['ch8_func'], '\n<div class="quiz" data-quiz="c2"></div>\n<div class="quiz" data-quiz="e0"></div>')
inject('s10', T['ch10_head'] + '\n' + c3 + '\n' + T['ch10_knap'] + '\n' + T['ch10_conv'], '\n<div class="quiz" data-quiz="c3"></div>\n<div class="quiz" data-quiz="e2"></div>')

H = fill(H)

# ---------- internal links from the dissolved lines
LINK = {'c1': 'ch14', 'c2': 'ch8', 'c3': 'ch10', 'c4': 'ch11', 'c5': 'ladder', 'e0': 'ch8', 'e1': 'ch14', 'e2': 'ch10', 'e3': 'ch12', 'e4': 'ladder'}
H = re.sub(r'href="#(c[1-5]|e[0-4])"', lambda m: 'href="#%s"' % LINK[m.group(1)], H)
H = H.replace('<a href="#ch9">stop 9</a></td></tr>\n<tr><td>Signal Propagation', '<a href="#ch10">stop 10</a></td></tr>\n<tr><td>Signal Propagation')

# ---------- intro, title, plan
H = H.replace('<h1>Algorithms from zero: 22 stops to exam day</h1>', '<h1>Algorithms from zero: 29 stops, then the Ladder</h1>')
old_p = re.search(r'<p><b>Coding contest coming up\?</b>.*?</p>', H, re.S).group(0)
H = H.replace(old_p, '<p><b>Coding contests and the end-sem?</b> Every topic ends with a <i>Patterns for contests</i> section: the words that give a problem away, tested Python templates, and the twists, with the problems from your own contests marked. Stops 11–17 add greedy, Graphs II, monotonic stacks, the contest toolkit, tools combined, contest readiness and an appendix beyond the outline. <b>The Ladder</b> (last stop before Exam prep) holds the practice problems for every topic, rated on both Codeforces and LeetCode scales.</p>')
H = H.replace('<li><b>Session 5, 1½ h</b>', '<li><b>Session 5, 3 h</b> Stops 11 to 14: greedy, Graphs II, monotonic stacks and the toolkit, then your first Ladder problems at the Foundation tier</li>\n    <li><b>Session 6, 3 h</b> Stops 15 to 17: tools combined, contest readiness (type the template sheet from memory), then the three-hour mock contest</li>\n    <li><b>Session 7, 1½ h</b>', 1)
box = '''</header>

<section class="box tip" style="margin-top:28px">
  <div class="lbl" data-ico="🧭">What changed</div>
  <p>The separate Contest line is gone: its templates now sit inside the topic that owns them, under <i>Patterns for contests</i>. New stops: <a href="#ch11">11 Greedy</a>, <a href="#ch12">12 Graphs II</a>, <a href="#ch13">13 Monotonic stacks</a>, <a href="#ch14">14 Contest toolkit</a>. <a href="#ladder">The Ladder</a> holds every practice problem, from warm-ups to the Ego tier, with XP, ranks and a streak.</p>
  <p><b>Version 4:</b> a rebuilt <a href="#ch12">Graphs II</a> (topological sort, Dijkstra, Bellman–Ford, Floyd–Warshall and spanning trees in full), greedy exchange arguments, memo → table → one-row conversions in <a href="#ch10">stop 10</a>, new stops <a href="#ch15">15 Bridges</a>, <a href="#ch16">16 Contest readiness</a> and <a href="#ch17">17 Appendix</a>, three-problem LeetCode mocks on the Ladder, and new quiz, spot-the-bug, fill-in and ordering items. The exam-prep stops are now labelled X1 to X8.</p>
</section>'''
assert H.count('</header>') == 1
H = H.replace('</header>', box)

# ---------- v4: relabel the exam-prep stops X1..X8 (ids and storage keys are untouched)
for k, (id_, old) in enumerate([('mock', 11), ('drills', 12), ('bugs', 13), ('order', 14), ('mistakes', 15), ('practice', 16), ('cards', 17), ('cheat', 18)], 1):
    m = re.search(r'(<section class="topic" id="%s"[^>]*data-num=")%d(".*?<div class="badge">)%d(</div>)' % (id_, old, old), H, re.S)
    assert m, id_
    H = H[:m.start()] + m.group(1) + 'X%d' % k + m.group(2) + 'X%d' % k + m.group(3) + H[m.end():]

# ---------- v4: hero map gets a second row for the stops added after the original route (11-17)
assert H.count('viewBox="0 0 940 170" width="940" height="170"') == 1
H = H.replace('viewBox="0 0 940 170" width="940" height="170"', 'viewBox="0 0 940 200" width="940" height="200"')
assert H.count('<g id="mapDots"></g>') == 1
H = H.replace('<g id="mapDots"></g>', '<path d="M45 148 H375" stroke="var(--line)" stroke-width="4" stroke-linecap="round"/><text x="30" y="122" font-size="12" font-weight="700" style="fill:var(--muted)">Added stops</text><g id="mapDots"></g>')
assert H.count('ch10:[870,60]};') == 1
H = H.replace('ch10:[870,60]};', 'ch10:[870,60],ch11:[60,148],ch12:[110,148],ch13:[160,148],ch14:[210,148],ch15:[260,148],ch16:[310,148],ch17:[360,148]};')

# ---------- CSS
css = '''
/* ---------- patterns, ladder ---------- */
[data-group=ladder]{--lc:var(--l-contest)}
.pat-head{margin:38px 0 12px;padding:10px 14px;border-left:6px solid var(--lc);background:var(--surface-2);border-radius:0 10px 10px 0;font-size:21px}
.xpbar{height:10px;border-radius:99px;background:var(--surface-2);border:1px solid var(--line);overflow:hidden;margin:2px 0}
.xpbar i{display:block;height:100%;background:var(--l-contest);transition:width .4s}
.tierbars{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px 14px;margin:6px 0 2px}
.tb{display:flex;flex-direction:column;gap:3px;font-size:13.5px;color:var(--muted)}
.tb b{color:var(--ink);font-family:var(--f-mono)}
.tbar{height:7px;border-radius:99px;background:var(--surface-2);border:1px solid var(--line);overflow:hidden}
.tbar i{display:block;height:100%}
.tabs{display:flex;flex-wrap:wrap;gap:6px}
.lab[data-w=ladder2] table td:nth-child(3){white-space:nowrap}
.prob details > p{margin:8px 0}
</style>'''
i = H.index('</style>'); H = H[:i] + css + H[i + len('</style>'):]

# ---------- JS
H = re.sub(r'const GROUPS = \[.*?\];', 'const GROUPS = [["found","Foundations"],["trees","Sorting and trees"],["bt","Backtracking"],["graph","Graphs"],["dp","Dynamic programming and greedy"],["ladder","The Ladder"],["exam","Exam prep"]];', H, count=1, flags=re.S)
n_before = H.count('sec: k.startsWith("s") ? "ch" + k.slice(1) : k')
H = H.replace('sec: k.startsWith("s") ? "ch" + k.slice(1) : k', 'sec: (window.SECMAP || {})[k] || (k.startsWith("s") ? "ch" + k.slice(1) : k)')
assert n_before == 1, n_before
ew, lj = open(P('src', 'js', 'e_widgets.js'), encoding='utf-8').read(), open(P('src', 'js', 'ladder.js'), encoding='utf-8').read()
sys.path.insert(0, P('src', 'data'))
import exam_v4
cx = open(P('src', 'js', 'c_extra.js'), encoding='utf-8').read().replace('__V4_DATA__', json.dumps(exam_v4.DATA, ensure_ascii=False))
assert '</script>' not in cx
lm = open(P('src', 'js', 'lc_mocks.js'), encoding='utf-8').read()
core = H.index('/* ===== core helpers')
ends = [m.start() + core for m in re.finditer('</script>', H[core:])]
pos = ends[1] + len('</script>')
H = H[:pos] + '\n<script>\n' + ew + '\n</script>\n<script>\n' + lj + '\n</script>\n<script>\n' + cx + '\n</script>\n<script>\n' + lm + '\n</script>' + H[pos:]

open(P('dist', 'index.html'), 'w', encoding='utf-8').write(H)
print('built', len(H), 'bytes')
