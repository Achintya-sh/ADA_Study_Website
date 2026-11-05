import os
import re, random, itertools, heapq, subprocess, sys, time
from collections import Counter
random.seed(7)

SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'snippets', 'snips.py')).read()
blocks = {}
for m in re.finditer(r'#@@ (\w+)\n(.*?)(?=\n#@@ |\Z)', SRC, re.S):
    blocks[m.group(1)] = m.group(2).rstrip() + '\n'
SCRIPTS = {'cf_input', 'stress', 'deep_rec', 'stdlib'}
ns = {}
for name, code in blocks.items():
    if name not in SCRIPTS:
        exec(code, ns)
g = ns.__getitem__
print('loaded', len(blocks), 'blocks')

def rnd(n, lo=-5, hi=9): return [random.randint(lo, hi) for _ in range(n)]

# ---------- sorting
for _ in range(500):
    iv = [[random.randint(0, 12), 0] for _ in range(random.randint(0, 6))]
    for x in iv: x[1] = x[0] + random.randint(0, 5)
    got = g('merge_intervals')([x[:] for x in iv])
    pts = set()
    for s, e in iv:
        pts |= set(range(s, e + 1))
    # brute: merged blocks must cover exactly the union of closed integer ranges, with touching merged
    cover = sorted(pts); exp = []
    for s, e in sorted(iv):
        pass
    for s, e in got:
        assert s <= e
    for (s1, e1), (s2, e2) in zip(got, got[1:]):
        assert e1 < s2
    assert set(x for s, e in got for x in range(s, e + 1)) == pts
for _ in range(300):
    nums = [random.choice([0, 1, 3, 9, 10, 30, 34, 5, 12, 121, 12]) for _ in range(random.randint(1, 6))]
    best = max("".join(map(str, p)) for p in itertools.permutations(nums))
    best = "0" if int(best) == 0 else best
    best = str(max(int("".join(map(str, p))) for p in itertools.permutations(nums)))
    assert g('largest_number')(nums) == best, (nums,)
for _ in range(500):
    a = rnd(random.randint(1, 15)); k = random.randrange(len(a))
    assert g('quickselect')(a, k) == sorted(a)[k]
    assert g('count_inversions')(a) == sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])
    b = a[:]; g('quick_sort_desc')(b); assert b == sorted(a, reverse=True)
big = list(range(100000)); t = time.time(); g('quick_sort_desc')(big); assert big == sorted(range(100000), reverse=True)
big = [5] * 100000; g('quick_sort_desc')(big)
rev = list(range(100000, 0, -1)); g('quick_sort_desc')(rev); assert rev == sorted(rev, reverse=True)
print('sorting ok', round(time.time() - t, 2), 's')

# ---------- BST
Node = g('Node')
def insert(r, v):
    if r is None: return Node(v)
    if v < r.value: r.left = insert(r.left, v)
    else: r.right = insert(r.right, v)
    return r
def pre(r): return [] if r is None else [r.value] + pre(r.left) + pre(r.right)
def ino(r): return [] if r is None else ino(r.left) + [r.value] + ino(r.right)
def nodes(r): return [] if r is None else [r] + nodes(r.left) + nodes(r.right)
t = Node(5); t.left = Node(1); t.right = Node(6); t.right.left = Node(3); t.right.right = Node(7)
assert g('is_bst_wrong')(t) is True and g('is_bst')(t) is False
for _ in range(300):
    vals = random.sample(range(100), random.randint(1, 12)); r = None
    for v in vals: r = insert(r, v)
    assert g('is_bst')(r)
    b = g('bst_from_preorder')(pre(r)); assert pre(b) == pre(r) and ino(b) == sorted(vals)
    if len(vals) >= 2:
        ns_ = nodes(r); x, y = random.sample(ns_, 2)
        x.value, y.value = y.value, x.value
        assert set(g('swapped_pair')(r)) == {x.value, y.value}
for _ in range(300):
    a = sorted(rnd(random.randint(0, 8))); x = random.randint(-7, 11)
    f = max([v for v in a if v <= x], default=None); c = min([v for v in a if v >= x], default=None)
    assert g('floor_')(a, x) == f and g('ceiling')(a, x) == c
print('bst ok')

# ---------- heaps
for _ in range(200):
    h, ref = g('MinHeap')(), []
    for _ in range(random.randint(1, 40)):
        if ref and random.random() < 0.4:
            assert h.pop() == heapq.heappop(ref)
        else:
            x = random.randint(-20, 20); h.push(x); heapq.heappush(ref, x)
    assert h.a == h.a  # structure sanity: heap property
    assert all(h.a[(i - 1) // 2] <= h.a[i] for i in range(1, len(h.a)))
for _ in range(300):
    ls = [sorted(rnd(random.randint(0, 5))) for _ in range(random.randint(1, 5))]
    assert g('merge_k')(ls) == sorted(x for l in ls for x in l)
for _ in range(300):
    lh, ref = g('LazyHeap')(), []
    for _ in range(random.randint(1, 40)):
        r = random.random()
        if ref and r < 0.3:
            x = random.choice(ref); ref.remove(x); lh.remove(x)
        elif ref and r < 0.5:
            x = min(ref); ref.remove(x); assert lh.pop() == x
        else:
            x = random.randint(0, 6); ref.append(x); lh.push(x)
        if ref: assert lh.top() == min(ref)
for _ in range(300):
    iv = []
    for _ in range(random.randint(0, 7)):
        s = random.randint(0, 10); iv.append((s, s + random.randint(1, 5)))
    brute = max([sum(1 for s, e in iv if s <= t0 < e) for t0 in range(0, 20)] or [0])
    assert g('min_rooms')(iv) == brute
def ipo_brute(k, w, P, C):
    best = w
    def go(w, used, left):
        nonlocal best
        best = max(best, w)
        if left == 0: return
        for i in range(len(P)):
            if i not in used and C[i] <= w: go(w + P[i], used | {i}, left - 1)
    go(w, frozenset(), k); return best
for _ in range(300):
    n = random.randint(1, 6); P = [random.randint(0, 6) for _ in range(n)]; C = [random.randint(0, 8) for _ in range(n)]
    k, w = random.randint(1, 4), random.randint(0, 5)
    assert g('find_max_capital')(k, w, P, C) == ipo_brute(k, w, P, C)
print('heaps ok')

# ---------- monotonic
for _ in range(500):
    a = rnd(random.randint(1, 12), 0, 6); n = len(a)
    ng = [next((j for j in range(i + 1, n) if a[j] > a[i]), -1) for i in range(n)]
    assert g('next_greater')(a) == ng
    best = max(a[i] * 0 + min(a[i:j + 1]) * (j - i + 1) for i in range(n) for j in range(i, n))
    assert g('largest_rectangle')(a[:]) == best
    assert g('sum_subarray_mins')(a) == sum(min(a[i:j + 1]) for i in range(n) for j in range(i, n))
    k = random.randint(1, n)
    assert g('sliding_max')(a, k) == [max(a[i:i + k]) for i in range(n - k + 1)]
    assert g('trap')(a) == sum(max(0, min(max(a[:i + 1]), max(a[i:])) - a[i]) for i in range(n))
    assert g('visible_pairs')(a) == sum(1 for i in range(n) for j in range(i + 1, n) if max(a[i + 1:j], default=0) <= min(a[i], a[j]))
for _ in range(300):
    num = "".join(random.choice("0123456789") for _ in range(random.randint(1, 7))); k = random.randint(0, len(num))
    exp = min((int("".join(c) or "0") for c in itertools.combinations(num, len(num) - k)), default=0)
    assert g('remove_k_digits')(num, k) == str(exp), (num, k)
print('mono ok')

# ---------- backtracking
for _ in range(200):
    nums = [random.randint(0, 3) for _ in range(random.randint(0, 6))]
    assert sorted(map(tuple, g('permute_unique')(nums[:]))) == sorted(set(itertools.permutations(nums))) or not nums
    ss = g('subsets_dup')(nums[:]); exp = sorted(set(tuple(sorted(c)) for k in range(len(nums) + 1) for c in itertools.combinations(nums, k)))
    assert sorted(map(tuple, ss)) == exp
for _ in range(200):
    s = "".join(random.choice("ab") for _ in range(random.randint(1, 8)))
    n = len(s); exp = []
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i + 1 for i in range(n - 1) if mask >> i & 1] + [n]
        parts = [s[cuts[i]:cuts[i + 1]] for i in range(len(cuts) - 1)]
        if all(p == p[::-1] for p in parts): exp.append(parts)
    assert sorted(g('palindrome_partitions')(s)) == sorted(exp)
    assert g('min_cuts')(s) == min(len(p) - 1 for p in exp)
def part_brute(nums, k):
    total = sum(nums)
    if total % k: return False
    for assign in itertools.product(range(k), repeat=len(nums)):
        sums = [0] * k
        for x, b in zip(nums, assign): sums[b] += x
        if len(set(sums)) == 1: return True
    return False
for _ in range(300):
    nums = [random.randint(1, 6) for _ in range(random.randint(1, 7))]; k = random.randint(1, 3)
    assert g('can_partition_k')(nums[:], k) == part_brute(nums, k)
for _ in range(300):
    a = rnd(random.randint(0, 12)); T = random.randint(-5, 12)
    exp = sum(1 for m in range(1 << len(a)) if sum(a[i] for i in range(len(a)) if m >> i & 1) == T)
    assert g('count_subsets')(a, T) == exp
print('backtracking ok')

# ---------- graphs I
def all_graphs(n):
    for a in itertools.product(range(-1, n), repeat=n): yield list(a)
for _ in range(2000):
    n = random.randint(1, 9); a = [random.choice([-1] + list(range(n))) for _ in range(n)]
    b = g('chak_brute')(a); assert g('chak_solve')(a) == b == g('chak_peel')(a)
big = list(range(1, 100000)) + [-1]; assert g('chak_solve')(big)[0] == 100000
big = list(range(1, 100000)) + [0]; assert g('chak_peel')(big)[5] == 100000
for _ in range(500):
    n = random.randint(1, 9); a = [random.randrange(n) for _ in range(n)]
    s = random.randrange(n); seen = []; u = s
    while u not in seen: seen.append(u); u = a[u]
    mu = seen.index(u); lam = len(seen) - mu
    assert g('rho')(a, s) == (mu, lam)
    up = g('build_jump')(a, 6)
    k = random.randint(0, 63); u = s
    for _ in range(k): u = a[u]
    assert g('kth_successor')(up, s, k) == u
# reverse chakravyuh vs all graphs, n <= 5
for n in range(1, 6):
    achievable = set(tuple(g('chak_brute')(a)) for a in all_graphs(n))
    for c in itertools.product(range(1, n + 1), repeat=n):
        res = g('reverse_chak')(list(c))
        if res is None: assert c not in achievable, (c,)
        else: assert tuple(g('chak_brute')(res)) == c and all(x == -1 or 0 <= x < n for x in res), (c, res)
        if res is not None: assert c in achievable
for _ in range(500):
    n = random.randint(1, 7); E = [(u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.35]
    col = g('two_colour')(n, E)
    ok = any(all((m >> u & 1) != (m >> v & 1) for u, v in E) for m in range(1 << n))
    assert (col is not None) == ok
    if col: assert all(col[u] != col[v] for u, v in E)
    s, t = random.randrange(n), random.randrange(n)
    reach = [{s}]; adj = {i: [] for i in range(n)}
    for u, v in E: adj[u].append(v); adj[v].append(u)
    for L in range(1, 2 * n + 3): reach.append({v for u in reach[-1] for v in adj[u]})
    exp = next((L for L in range(1, 2 * n + 3, 2) if t in reach[L]), -1)
    assert g('shortest_odd_walk')(n, E, s, t) == exp
print('graphs I ok')

# ---------- graphs II
for _ in range(500):
    n = random.randint(1, 7); E = [(u, v) for u in range(n) for v in range(n) if u < v and random.random() < 0.4]
    perm = list(range(n)); random.shuffle(perm); E2 = [(perm[u], perm[v]) for u, v in E]
    order = g('topo_order')(n, E2); pos = {v: i for i, v in enumerate(order)}
    assert order is not None and all(pos[u] < pos[v] for u, v in E2)
    # longest path brute
    best = 0
    def dfs(u, d):
        global best
        best = max(best, d)
        for x, y in E2:
            if x == u: dfs(y, d + 1)
    for s in range(n): dfs(s, 0)
    assert g('longest_path_dag')(n, E2) == best
assert g('topo_order')(3, [(0, 1), (1, 2), (2, 0)]) is None
for _ in range(500):
    n = random.randint(1, 7); E = [(random.randrange(n), random.randrange(n), random.randint(0, 9)) for _ in range(random.randint(0, 14))]
    s = 0; d, par = g('dijkstra')(n, E, s)
    bf = g('bellman_ford')(n, E, s); assert bf == d
    fw = g('floyd_warshall')(n, E); assert fw[s] == d
    for t in range(n):
        if d[t] < float('inf'):
            p = g('path_to')(par, t); assert p[0] == s and p[-1] == t
    E01 = [(u, v, w % 2) for u, v, w in E]; assert g('zero_one_bfs')(n, E01, s) == g('dijkstra')(n, E01, s)[0]
neg = [(0, 1, 2), (1, 2, -5), (2, 1, 1)]; assert g('bellman_ford')(3, neg, 0) is None
assert g('bellman_ford')(3, [(0, 1, 4), (1, 2, -2)], 0) == [0, 4, 2]
def free_brute(n, E, s, t, k):
    adj = {i: [] for i in range(n)}
    for u, v, w in E: adj[u].append((v, w))
    best = float('inf')
    def go(u, seen, ws):
        nonlocal best
        if u == t:
            best = min(best, sum(sorted(ws)[:max(0, len(ws) - k)])); return
        for v, w in adj[u]:
            if v not in seen: go(v, seen | {v}, ws + [w])
    go(s, {s}, []); return best
for _ in range(500):
    n = random.randint(2, 6); E = [(random.randrange(n), random.randrange(n), random.randint(1, 9)) for _ in range(random.randint(1, 12))]
    k = random.randint(0, 3); s, t = 0, n - 1
    assert g('min_cost_k_free')(n, E, s, t, k) == free_brute(n, E, s, t, k)
for _ in range(500):
    n = random.randint(1, 6); E = [(random.randint(1, 9), u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.7]
    k = g('kruskal')(n, E); best = None
    for sub in itertools.combinations(E, n - 1):
        d = g('DSU')(n)
        if all(d.union(u, v) for _, u, v in sub):
            s_ = sum(w for w, _, _ in sub); best = s_ if best is None else min(best, s_)
    if n == 1: best = 0
    assert k == best
for _ in range(500):
    n = random.randint(1, 8); a = [random.randint(1, 9) for _ in range(n)]; order = list(range(n)); random.shuffle(order)
    got = g('best_after_removals')(a, order)
    exp = []; alive = [True] * n
    for i in order:
        alive[i] = False; b = 0; cur = 0
        for j in range(n):
            cur = cur + a[j] if alive[j] else 0; b = max(b, cur)
        exp.append(b)
    assert got == exp, (a, order, got, exp)
print('graphs II ok')

# ---------- DP
for _ in range(500):
    n = random.randint(1, 5); W = random.randint(0, 20)
    w = [random.randint(1, 8) for _ in range(n)]; v = [random.randint(0, 20) for _ in range(n)]
    def bf(limit):
        best = 0
        for ks in itertools.product(range(limit + 1), repeat=n):
            if sum(k * x for k, x in zip(ks, w)) <= W: best = max(best, sum(k * x for k, x in zip(ks, v)))
        return best
    assert g('knap01')(w, v, W) == bf(1) == g('k_memo')(w, v, W) == g('k_table')(w, v, W) == g('k_row')(w, v, W)
    assert g('knap012')(w, v, W) == bf(2) == g('knap01')(w * 2, v * 2, W)
    assert g('unbounded')(w, v, W) == bf(W)
assert (g('combos')([1, 2, 5], 5), g('orderings')([1, 2, 3], 4), g('min_coins')([1, 3, 4], 6), g('can_make')([1, 5, 11, 5], 11)) == (4, 7, 2, True)
assert g('min_coins')([2], 3) == -1
for _ in range(500):
    a = rnd(random.randint(0, 10)); n = len(a); L = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i]: L[i] = max(L[i], L[j] + 1)
    assert g('lis_length')(a) == max(L, default=0)
from functools import lru_cache
for _ in range(300):
    s = "".join(random.choice("abc") for _ in range(random.randint(0, 6))); t = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
    @lru_cache(None)
    def ed(i, j):
        if i == 0: return j
        if j == 0: return i
        if s[i - 1] == t[j - 1]: return ed(i - 1, j - 1)
        return 1 + min(ed(i - 1, j), ed(i, j - 1), ed(i - 1, j - 1))
    assert g('edit_distance')(s, t) == ed(len(s), len(t))
def cool_brute(p):
    best = 0
    def go(i, holding, cool, profit):
        nonlocal best
        if i == len(p): best = max(best, profit); return
        go(i + 1, holding, False, profit)
        if holding: go(i + 1, False, True, profit + p[i])
        elif not cool: go(i + 1, True, False, profit - p[i])
    go(0, False, False, 0); return best
for _ in range(300):
    p = [random.randint(1, 9) for _ in range(random.randint(0, 8))]
    assert g('max_profit_cooldown')(p) == cool_brute(p)
for _ in range(100):
    n = random.randint(1, 6); c = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
    assert g('min_assignment')(c) == min(sum(c[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
print('dp ok')

# ---------- greedy
for _ in range(500):
    jobs = [(random.randint(1, 4), random.randint(1, 9)) for _ in range(random.randint(0, 7))]
    best = 0
    for m in range(1 << len(jobs)):
        sel = [jobs[i] for i in range(len(jobs)) if m >> i & 1]
        if all(sum(1 for d, _ in sel if d <= t0) <= t0 for t0 in range(1, 5)): best = max(best, sum(p for _, p in sel))
    assert g('max_profit_deadlines')(jobs) == best
for _ in range(500):
    n = random.randint(1, 6); gas = [random.randint(0, 5) for _ in range(n)]; cost = [random.randint(0, 5) for _ in range(n)]
    ok = [s for s in range(n) if all(sum(gas[(s + i) % n] - cost[(s + i) % n] for i in range(k + 1)) >= 0 for k in range(n))]
    got = g('start_station')(gas, cost)
    assert (got == -1 and not ok) or got in ok
    r = [random.randint(1, 4) for _ in range(random.randint(1, 7))]; m = len(r)
    @lru_cache(None)
    def cn(i):
        v = 1
        if i and r[i - 1] < r[i]: v = max(v, cn(i - 1) + 1)
        if i + 1 < m and r[i + 1] < r[i]: v = max(v, cn(i + 1) + 1)
        return v
    assert g('candy')(r) == sum(cn(i) for i in range(m))
def hb(w):
    w = tuple(sorted(w))
    if len(w) == 1: return 0
    best = float('inf')
    for i in range(len(w)):
        for j in range(i + 1, len(w)):
            rest = [w[k] for k in range(len(w)) if k not in (i, j)] + [w[i] + w[j]]
            best = min(best, w[i] + w[j] + hb(rest))
    return best
for _ in range(200):
    w = [random.randint(1, 9) for _ in range(random.randint(1, 6))]; assert g('merge_cost')(w) == hb(w)
print('greedy ok')

# ---------- toolkit
for _ in range(300):
    ws = [random.randint(1, 9) for _ in range(random.randint(1, 8))]; d = random.randint(1, len(ws))
    def okc(cap):
        need, load = 1, 0
        for x in ws:
            if load + x > cap: need += 1; load = 0
            load += x
        return need <= d
    assert g('ship_days')(ws, d) == next(c for c in range(max(ws), sum(ws) + 1) if okc(c))
    a = rnd(random.randint(0, 10)); k = random.randint(-4, 6)
    assert g('count_sum_k')(a, k) == sum(1 for i in range(len(a)) for j in range(i, len(a)) if sum(a[i:j + 1]) == k)
    n = random.randint(1, 8); ops = [(l, r, random.randint(-3, 3)) for l, r in [sorted((random.randrange(n), random.randrange(n))) for _ in range(random.randint(0, 5))]]
    exp = [0] * n
    for l, r, v in ops:
        for i in range(l, r + 1): exp[i] += v
    assert g('apply_ranges')(n, ops) == exp
    p = [random.randint(1, 5) for _ in range(random.randint(0, 9))]; S = random.randint(1, 12)
    exp = min([j - i + 1 for i in range(len(p)) for j in range(i, len(p)) if sum(p[i:j + 1]) >= S], default=0)
    assert g('shortest_at_least')(p, S) == exp
print('toolkit ok')

# ---------- scripts
r = subprocess.run([sys.executable, '-c', blocks['cf_input']], input=b"2\n3\n1 2 3\n2\n5 -1\n", capture_output=True); assert r.stdout == b"6\n4\n", r
r = subprocess.run([sys.executable, '-c', blocks['stress']], capture_output=True, text=True); print(r.stdout.strip()); assert 'MISMATCH on' in r.stdout
r = subprocess.run([sys.executable, '-c', blocks['deep_rec']], capture_output=True, text=True); assert r.stdout.strip() == '100000', r
r = subprocess.run([sys.executable, '-c', blocks['stdlib']], capture_output=True, text=True); print(r.stdout); assert r.returncode == 0, r.stderr
print('ALL TESTS PASSED')
