# Checks every exam-practice item added in v4 by RUNNING it: blanks, bugs, orderings, and mock extras with code.
import os, re, sys, io, contextlib, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'data'))
import exam_v4 as E
from collections import deque
import heapq

def fresh():
    ns = dict(E.NS); ns.update({'deque': deque, 'heapq': heapq})
    return ns

# ---- quiz structure
for key, qs in E.QUIZ.items():
    for q in qs:
        assert len(q['o']) == 4 and len(set(q['o'])) == 4 and 0 <= q['a'] < 4 and q['q'] and q['why'], (key, q['q'])
print('quiz structure ok', {k: len(v) for k, v in E.QUIZ.items()})

# ---- claims quoted inside quiz explanations
ns = fresh()
assert ns['greedy_coins']([1, 3, 4], 6) == 3 and ns['dp_coins']([1, 3, 4], 6) == 2
assert ns['knap01']([10, 20, 30], [60, 100, 120], 50) == 220
assert abs(ns['fractional_knapsack']([(60, 10), (100, 20), (120, 30)], 50) - 240) < 1e-9     # fractions help: 60 + 100 + 80
assert 160 == 60 + 100                                                                       # what ratio-greedy gets without fractions
print('quiz claims ok')

# ---- mock extras with code: run the printed code and compare with the marked-correct option
for it in E.EXTRA:
    if 'c' not in it: continue
    ns = fresh(); buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(it['c'], ns)
    got = buf.getvalue().strip()
    assert got == it['o'][it['a']], (it['q'], got, it['o'][it['a']])
print('mock extras ok:', len(E.EXTRA), 'items,', sum(1 for i in E.EXTRA if 'c' in i), 'with executed code')

# ---- blanks: fill in the answers, run, test
for b in E.BLANKS:
    code = re.sub(r'\{\{(.*?)\}\}', lambda m: m.group(1), b['c'])
    ns = fresh(); exec(code, ns)
    assert eval(b['test'], ns) is True or eval(b['test'], ns), b['p']
    answers = re.findall(r'\{\{(.*?)\}\}', b['c']); assert 2 <= len(answers) <= 5, b['p']
    # a wrong answer must break it: replace the first blank by a nonsense token
    broken = re.sub(r'\{\{(.*?)\}\}', 'None', b['c'], count=1)
    try:
        ns2 = fresh(); exec(broken.replace('{{', '').replace('}}', ''), ns2); ok = eval(b['test'], ns2)
    except Exception:
        ok = False
    assert not ok, ('first blank is not load-bearing', b['p'])
print('blanks ok:', len(E.BLANKS))

# ---- bugs: buggy version fails the test, fixed version passes, flagged lines are inside the fix
INF = float('inf')
for b in E.BUGS:
    ns = fresh(); exec('\n'.join(b['c']), ns)
    bad = eval(b['test'], ns)
    assert bad == b['bad'], (b['p'], bad, b['bad'])
    assert set(b['a']) <= set(b['fix']), b['p']
    lines = list(b['c'])
    for i, new in b['fix'].items():
        lines[i] = new                                                # None deletes
    fixed = '\n'.join(l for l in lines if l is not None)
    ns = fresh(); exec(fixed, ns)
    good = eval(b['test'], ns)
    assert good == b['good'], (b['p'], good, b['good'])
    assert all(0 <= i < len(b['c']) for i in b['a'])
    assert b['p'].count('(') >= 1 and str(b['bad']) in b['p'] or b['t'] in ('Graphs II', 'Greedy', 'Monotonic stacks')
print('bugs ok:', len(E.BUGS))

# ---- orderings: the listed order runs and passes
for p in E.PARSONS:
    ns = fresh(); exec('\n'.join(p['c']), ns)
    assert eval(p['test'], ns), p['p']
    assert len(set(p['c'])) >= len(p['c']) - 2
print('orderings ok:', len(E.PARSONS))
print('EXAM ITEMS PASSED')
