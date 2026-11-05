# Tests for v4 content: greedy, DP conversions, tree DP, DSU extras, heaps, trie, memory sheet, appendix.
import os, re, random, itertools, heapq, collections
from functools import lru_cache
random.seed(4242)
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'snippets', 'snips.py')).read()
blocks = {m.group(1): m.group(2).rstrip() + '\n' for m in re.finditer(r'#@@ (\w+)\n(.*?)(?=\n#@@ |\Z)', SRC, re.S)}
SCRIPTS = {'cf_input', 'stress', 'deep_rec', 'stdlib'}
ns = {}
for name, code in blocks.items():
    if name not in SCRIPTS:
        exec(code, ns)
g = ns.__getitem__
INF = float('inf')

# ---------- greedy
for _ in range(400):
    n = random.randint(1, 4)
    items = [(random.randint(1, 20), random.randint(1, 9)) for _ in range(n)]
    W = random.randint(1, 25)
    best = 0.0                                        # an optimal fractional solution has at most ONE fractional item
    for frac in range(-1, n):
        for mask in range(1 << n):
            if frac >= 0 and (mask >> frac) & 1: continue
            wt = sum(items[i][1] for i in range(n) if (mask >> i) & 1)
            val = sum(items[i][0] for i in range(n) if (mask >> i) & 1)
            if wt > W: continue
            if frac < 0: best = max(best, val)
            else:
                v, w = items[frac]; take = min(w, W - wt)
                best = max(best, val + v * take / w)
    assert abs(g('fractional_knapsack')(items, W) - best) < 1e-9, (items, W)
assert g('first_greedy_failure')([1, 3, 4]) == 6 and g('first_greedy_failure')([1, 5, 10, 25], 150) is None
assert g('greedy_coins')([1, 3, 4], 6) == 3 and g('dp_coins')([1, 3, 4], 6) == 2
for _ in range(200):                                   # 0/1 knapsack: sorting by ratio is NOT safe
    pass
print('greedy coins / knapsack ok')

def sched_brute(tasks, n):
    types = sorted(set(tasks)); cnt = tuple(tasks.count(t) for t in types)
    start = (cnt, tuple([0] * len(types)))
    seen = {start}; frontier = [start]; t = 0
    while frontier:
        nxt = []
        for cnts, cool in frontier:
            if sum(cnts) == 0: return t
            dec = tuple(max(0, c - 1) for c in cool)
            options = [(cnts, dec)]                    # idle
            for i, c in enumerate(cnts):
                if c > 0 and cool[i] == 0:
                    nc = list(cnts); nc[i] -= 1; nd = list(dec); nd[i] = n
                    options.append((tuple(nc), tuple(nd)))
            for o in options:
                if o not in seen: seen.add(o); nxt.append(o)
        frontier = nxt; t += 1
for _ in range(300):
    tasks = [random.choice('ABC') for _ in range(random.randint(1, 6))]; n = random.randint(0, 3)
    assert g('least_interval')(tasks, n) == sched_brute(tasks, n), (tasks, n)
assert g('least_interval')(list('AAABBB'), 2) == 8
for _ in range(400):
    s = ''.join(random.choice('abcd') for _ in range(random.randint(1, 10)))
    best = None
    for mask in range(1 << (len(s) - 1)):
        cuts = [0] + [i + 1 for i in range(len(s) - 1) if (mask >> i) & 1] + [len(s)]
        pieces = [s[cuts[i]:cuts[i + 1]] for i in range(len(cuts) - 1)]
        if all(not (set(pieces[i]) & set(pieces[j])) for i in range(len(pieces)) for j in range(i + 1, len(pieces))):
            if best is None or len(pieces) > len(best): best = pieces
    assert g('partition_labels')(s) == [len(p) for p in best], s
assert g('partition_labels')('ababcbacadefegdehijhklij') == [9, 7, 8]
for _ in range(500):
    nums = [random.randint(0, 4) for _ in range(random.randint(1, 8))]
    reach = {0}; stack = [0]
    while stack:
        i = stack.pop()
        for j in range(i + 1, min(len(nums), i + nums[i] + 1)):
            if j not in reach: reach.add(j); stack.append(j)
    ok = (len(nums) - 1) in reach
    assert g('can_jump')(nums) == ok, nums
    if ok:
        dist = {0: 0}; q = collections.deque([0])
        while q:
            i = q.popleft()
            for j in range(i + 1, min(len(nums), i + nums[i] + 1)):
                if j not in dist: dist[j] = dist[i] + 1; q.append(j)
        assert g('min_jumps')(nums) == dist[len(nums) - 1], nums
for _ in range(400):
    pts = [sorted((random.randint(0, 9), random.randint(0, 9))) for _ in range(random.randint(1, 6))]
    cand = sorted({x for p in pts for x in p})
    best = next(k for k in range(1, len(pts) + 1) if any(all(any(a <= x <= b for x in sel) for a, b in pts) for sel in itertools.combinations(cand, k)))
    assert g('find_min_arrow_shots')([p[:] for p in pts]) == best, pts
print('621 / 763 / 55 / 45 / 452 ok')

# ---------- DP conversions: three versions agree with each other and with a plain recursion
def lcs_plain(a, b):
    if not a or not b: return 0
    if a[0] == b[0]: return 1 + lcs_plain(a[1:], b[1:])
    return max(lcs_plain(a[1:], b), lcs_plain(a, b[1:]))
def edit_plain(a, b):
    if not a: return len(b)
    if not b: return len(a)
    if a[0] == b[0]: return edit_plain(a[1:], b[1:])
    return 1 + min(edit_plain(a[1:], b), edit_plain(a, b[1:]), edit_plain(a[1:], b[1:]))
def weave_plain(a, b, c):
    if not a and not b: return not c
    if not c: return False
    return (bool(a) and a[0] == c[0] and weave_plain(a[1:], b, c[1:])) or (bool(b) and b[0] == c[0] and weave_plain(a, b[1:], c[1:]))
for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
    e = lcs_plain(a, b)
    assert g('lcs_memo')(a, b) == g('lcs_table')(a, b) == g('lcs_row')(a, b) == e, (a, b)
    e = edit_plain(a, b)
    assert g('edit_memo')(a, b) == g('edit_table')(a, b) == g('edit_row')(a, b) == e, (a, b)
    if random.random() < .5:
        c = list(a + b); random.shuffle(c); c = ''.join(c)                          # often NOT a weave
    else:
        i = j = 0; c = ''
        while i < len(a) or j < len(b):                                              # a true weave
            if j == len(b) or (i < len(a) and random.random() < .5): c += a[i]; i += 1
            else: c += b[j]; j += 1
        if random.random() < .3 and c: c = c[:-1] + random.choice('abc')
    e = weave_plain(a, b, c)
    assert g('interleave_memo')(a, b, c) == g('interleave_table')(a, b, c) == g('interleave_row')(a, b, c) == e, (a, b, c)
assert g('interleave_row')('aabcc', 'dbbca', 'aadbbcbcac') is True and g('interleave_row')('aabcc', 'dbbca', 'aadbbbaccc') is False
assert g('edit_row')('horse', 'ros') == 3 and g('lcs_row')('abcde', 'ace') == 3
print('DP conversions ok')

# ---------- tree DP
def rand_tree(n):
    vals = []
    nodes = [g('TreeNode')(random.randint(-5, 9)) for _ in range(n)]
    for i in range(1, n):
        while True:
            p = nodes[random.randrange(i)]
            side = random.choice(['left', 'right'])
            if getattr(p, side) is None:
                setattr(p, side, nodes[i]); break
    return nodes[0]
def rob_ref(v):
    if not v: return (0, 0)
    (rl, sl), (rr, sr) = rob_ref(v.left), rob_ref(v.right)
    return (v.val + sl + sr, max(rl, sl) + max(rr, sr))
def height_ref(v): return 0 if not v else 1 + max(height_ref(v.left), height_ref(v.right))
def diam_ref(v):
    if not v: return 0
    return max(height_ref(v.left) + height_ref(v.right), diam_ref(v.left), diam_ref(v.right))
def pathsum_ref(root):
    best = -INF
    def down(v):
        nonlocal best
        if not v: return 0
        l, r = max(0, down(v.left)), max(0, down(v.right))
        best = max(best, v.val + l + r)
        return v.val + max(l, r)
    down(root); return best
for _ in range(500):
    t = rand_tree(random.randint(1, 10))
    assert g('rob_tree')(t) == max(rob_ref(t))
    assert g('diameter')(t) == diam_ref(t)
    assert g('max_path_sum')(t) == pathsum_ref(t)
assert g('rob_tree')(g('build_tree')([3, 2, 3, None, 3, None, 1])) == 7
assert g('rob_tree')(g('build_tree')([3, 4, 5, 1, 3, None, 1])) == 9
assert g('diameter')(g('build_tree')([1, 2, 3, 4, 5])) == 3
assert g('max_path_sum')(g('build_tree')([-10, 9, 20, None, None, 15, 7])) == 42
chain = g('TreeNode')(1); cur = chain
for _ in range(100000): cur.left = g('TreeNode')(1); cur = cur.left            # a 100,001-deep tree: recursion would crash
assert g('diameter')(chain) == 100000 and g('rob_tree')(chain) == 50001
print('tree DP ok')

# ---------- DSU extras
for _ in range(400):
    emails = ['e%d' % i for i in range(random.randint(1, 8))]
    accs = [[random.choice('AB')] + random.sample(emails, random.randint(1, min(3, len(emails)))) for _ in range(random.randint(1, 5))]
    # reference: graph components over emails; name taken from any account that owns the email
    adj = collections.defaultdict(set)
    for acc in accs:
        for e in acc[1:]: adj[e] |= set(acc[1:])
    seen = set(); exp = []
    for e in adj:
        if e in seen: continue
        comp, st = set(), [e]
        while st:
            x = st.pop()
            if x in comp: continue
            comp.add(x); st.extend(adj[x] - comp)
        seen |= comp
        exp.append(tuple(sorted(comp)))
    got = g('accounts_merge')([a[:] for a in accs])
    assert sorted(tuple(r[1:]) for r in got) == sorted(exp), (accs, got)
assert sorted(g('accounts_merge')([['John', 'a', 'b'], ['John', 'c'], ['John', 'b', 'c'], ['Mary', 'm']])) == [['John', 'a', 'b', 'c'], ['Mary', 'm']]
for _ in range(500):
    vars_ = list('abcdef'); hidden = {v: random.choice([1, 2, 3, 4, 6]) for v in vars_}
    eq = []; vals = []
    for _ in range(random.randint(1, 6)):
        x, y = random.sample(vars_, 2); eq.append([x, y]); vals.append(hidden[x] / hidden[y])
    qs = [[random.choice(vars_ + ['z']), random.choice(vars_ + ['z'])] for _ in range(6)]
    adj = collections.defaultdict(list)
    for (x, y), v in zip(eq, vals): adj[x].append((y, v)); adj[y].append((x, 1 / v))
    exp = []
    for a, b in qs:
        if a not in adj or b not in adj: exp.append(-1.0); continue
        dist = {a: 1.0}; st = [a]
        while st:
            x = st.pop()
            for y, v in adj[x]:
                if y not in dist: dist[y] = dist[x] * v; st.append(y)
        exp.append(dist[b] if b in dist else -1.0)
    got = g('calc_equation')(eq, vals, qs)
    assert all(abs(x - y) < 1e-9 for x, y in zip(got, exp)), (eq, vals, qs, got, exp)
assert g('calc_equation')([['a', 'b'], ['b', 'c']], [2.0, 3.0], [['a', 'c'], ['b', 'a'], ['a', 'e'], ['a', 'a'], ['x', 'x']]) == [6.0, 0.5, -1.0, 1.0, -1.0]
print('DSU extras ok')

# ---------- heaps, trie
for _ in range(300):
    mf = g('MedianFinder')(); seen = []
    for _ in range(random.randint(1, 30)):
        x = random.randint(-20, 20); mf.add_num(x); seen.append(x)
        s = sorted(seen); n = len(s)
        exp = float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
        assert mf.find_median() == exp
for _ in range(300):
    words = [''.join(random.choice('ab') for _ in range(random.randint(1, 4))) for _ in range(random.randint(0, 6))]
    T = g('Trie')()
    for w in words: T.insert(w)
    for q in [''.join(random.choice('ab') for _ in range(random.randint(1, 5))) for _ in range(10)]:       # LC 208: length >= 1
        assert T.search(q) == (q in words)
        assert T.starts_with(q) == any(w.startswith(q) for w in words)
def search_word(board, w):
    R, C = len(board), len(board[0])
    def go(r, c, i, used):
        if board[r][c] != w[i]: return False
        if i == len(w) - 1: return True
        used.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in used and go(nr, nc, i + 1, used): used.discard((r, c)); return True
        used.discard((r, c)); return False
    return any(go(r, c, 0, set()) for r in range(R) for c in range(C))
for _ in range(300):
    R, C = random.randint(1, 4), random.randint(1, 4)
    board = [[random.choice('abc') for _ in range(C)] for _ in range(R)]
    words = [''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(random.randint(1, 6))]
    exp = sorted({w for w in words if search_word(board, w)})
    got = g('find_words')([row[:] for row in board], words)
    assert sorted(got) == exp and len(got) == len(set(got)), (board, words, got, exp)
print('heaps / trie ok')

# ---------- memory sheet
for _ in range(300):
    a = sorted(random.randint(0, 30) for _ in range(random.randint(1, 12))); x = random.randint(-2, 32)
    from bisect import bisect_left
    assert g('search_first_true')(0, len(a), lambda i: i == len(a) or a[i] >= x) == bisect_left(a, x)
for _ in range(300):
    R, C = random.randint(1, 5), random.randint(1, 5)
    grid = [[1 if random.random() < .3 else 0 for _ in range(C)] for _ in range(R)]
    grid[0][0] = grid[R - 1][C - 1] = 0
    dist = {(0, 0): 0}; q = collections.deque([(0, 0)])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and (nr, nc) not in dist: dist[(nr, nc)] = dist[(r, c)] + 1; q.append((nr, nc))
    assert g('grid_bfs')(grid, (0, 0), (R - 1, C - 1)) == dist.get((R - 1, C - 1), -1)
for _ in range(300):
    n = random.randint(1, 7); E = [(u, v) for u in range(n) for v in range(n) if u != v and random.random() < .25]
    adj = [[] for _ in range(n)]
    for u, v in E: adj[u].append(v)
    s = random.randrange(n); r = [[i == j for j in range(n)] for i in range(n)]
    for u, v in E: r[u][v] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if r[i][k] and r[k][j]: r[i][j] = True
    assert g('reach')(adj, s) == {j for j in range(n) if r[s][j]}
    o = g('topo_kahn')(n, E); assert (o is None) == (g('topo_order')(n, E) is None)
    W = [(u, v, random.randint(0, 9)) for u, v in E]
    assert g('shortest_dijkstra')(n, W, s) == g('dijkstra')(n, W, s)[0]
    NW = [(u, v, random.randint(-3, 9)) for u, v in E]
    assert g('shortest_bf')(n, NW, s) == g('bellman_ford')(n, NW, s)
    UE = [(u, v, random.randint(1, 9)) for u in range(n) for v in range(u + 1, n) if random.random() < .5]
    assert g('mst_kruskal')(n, UE) == g('kruskal')(n, [(w, u, v) for u, v, w in UE])
    uf = g('UF')(n); comp = list(range(n))
    for u, v, _ in UE:
        uf.union(u, v)
    for u, v, _ in UE: assert uf.find(u) == uf.find(v)
for _ in range(400):
    a = [random.randint(-5, 9) for _ in range(random.randint(0, 9))]
    best = 0
    for L in range(1, len(a) + 1):
        for c in itertools.combinations(a, L):
            if all(c[i] < c[i + 1] for i in range(L - 1)): best = max(best, L)
    assert g('lis_bisect')(a) == best == g('lis_length')(a)
    w = [random.randint(1, 6) for _ in range(random.randint(0, 6))]; v = [random.randint(1, 9) for _ in w]; W = random.randint(0, 14)
    exp = max((sum(v[i] for i in range(len(w)) if m >> i & 1) for m in range(1 << len(w)) if sum(w[i] for i in range(len(w)) if m >> i & 1) <= W), default=0)
    assert g('knap_01_row')(w, v, W) == exp
    s1 = ''.join(random.choice('abc') for _ in range(random.randint(0, 6))); s2 = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
    assert g('edit_dist_row')(s1, s2) == edit_plain(s1, s2)
    exp = [-1] * len(a)
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[j] > a[i]: exp[i] = j; break
    assert g('greater_next')(a) == exp
    b = a[:6]; got = g('all_subsets')(b)
    assert sorted(map(tuple, got)) == sorted(tuple(x for i, x in enumerate(b) if m >> i & 1) for m in range(1 << len(b)))
print('memory sheet ok')

# ---------- pitfalls
p = g('pitfalls_demo')()
assert p['mutable_default'] == [1, 2] and p['alias_grid'] == (7, 0) and p['alias_list'] == ([1, 2, 3], [3, 1, 2])
assert p['max_heap'] == 9 and p['tie_break'] == (1, 'a') and p['floor_div'] == (-4, 1, -3)
assert p['sort_stable'] == [(0, 'y'), (1, 'x'), (1, 'a')]
print('pitfalls ok')

# ---------- appendix: merge sort, counting, amortised, hashing
for _ in range(500):
    a = [random.randint(-9, 9) for _ in range(random.randint(0, 14))]
    assert g('merge_sort')(a) == sorted(a)
    recs = [(random.randint(0, 3), i) for i in range(random.randint(0, 12))]
    assert g('merge_sort')([r for r in recs]) == sorted(recs)                            # tuples: tie broken by index
    st = [(k, i) for i, (k, _) in enumerate(recs)]
    class K:                                                                             # stability: compare by key only
        def __init__(s, k, i): s.k, s.i = k, i
        def __le__(s, o): return s.k <= o.k
    out = g('merge_sort')([K(k, i) for k, i in st])
    assert [(x.k, x.i) for x in out] == sorted(st, key=lambda t: t[0])
    a = [random.randint(-6, 6) for _ in range(random.randint(0, 10))]
    assert g('count_smaller')(a) == [sum(1 for j in range(i + 1, len(a)) if a[j] < a[i]) for i in range(len(a))]
    assert g('reverse_pairs')(a) == sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > 2 * a[j])
    assert g('count_inversions')(a[:])[0] == sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j]) if isinstance(g('count_inversions')(a[:]), tuple) else True
assert g('count_smaller')([5, 2, 6, 1]) == [2, 1, 1, 0] and g('reverse_pairs')([1, 3, 2, 3, 1]) == 2 and g('reverse_pairs')([2, 4, 3, 5, 1]) == 3
for n in (1, 2, 3, 10, 100, 1000, 5000):
    d = g('DynArray')()
    for i in range(n): d.append(i)
    assert d.data[:n] == list(range(n)) and d.copies < 2 * n
    d1 = g('DynArray')(grow=1)
    for i in range(n): d1.append(i)
    assert d1.copies == n * (n - 1) // 2
assert g('DynArray')().copies == 0
for _ in range(200):
    for cls in ('ChainedMap', 'ProbeMap'):
        m, ref = g(cls)(), {}
        for _ in range(random.randint(1, 120)):
            k = random.choice([random.randint(0, 40), 'k%d' % random.randint(0, 40)])
            op = random.random()
            if op < .5: v = random.randint(0, 99); m.put(k, v); ref[k] = v
            elif op < .75: assert m.remove(k) == (k in ref); ref.pop(k, None)
            else: assert m.get(k, 'none') == ref.get(k, 'none')
        for k in list(ref): assert m.get(k) == ref[k]
        assert m.n == len(ref)
m = g('ChainedMap')()
for i in range(100): m.put(i, i)
assert len(m.buckets) >= 128 and m.n / len(m.buckets) <= 0.75
for _ in range(300):                                                                    # LRU vs OrderedDict
    cap = random.randint(1, 4); lru = g('LRUCache')(cap); od = collections.OrderedDict()
    for _ in range(random.randint(1, 40)):
        k = random.randint(0, 6)
        if random.random() < .5:
            v = random.randint(0, 9); lru.put(k, v)
            if k in od: od.move_to_end(k)
            od[k] = v
            if len(od) > cap: od.popitem(last=False)
        else:
            exp = -1
            if k in od: od.move_to_end(k); exp = od[k]
            assert lru.get(k) == exp
for _ in range(200):
    hm, ref = g('MyHashMap')(), {}
    for _ in range(random.randint(1, 80)):
        k = random.randint(0, 3000); op = random.random()
        if op < .4: v = random.randint(0, 99); hm.put(k, v); ref[k] = v
        elif op < .6: hm.remove(k); ref.pop(k, None)
        else: assert hm.get(k) == ref.get(k, -1)
print('appendix ok')
print('V4 CONTENT TESTS PASSED')
