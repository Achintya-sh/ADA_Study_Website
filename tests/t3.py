# Tests for the v4 content: Graphs II rebuild, contest-readiness and bridge topics.
import os, re, random, itertools, heapq, subprocess, sys
from functools import lru_cache
random.seed(2026)
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'snippets', 'snips.py')).read()
blocks = {m.group(1): m.group(2).rstrip() + '\n' for m in re.finditer(r'#@@ (\w+)\n(.*?)(?=\n#@@ |\Z)', SRC, re.S)}
SCRIPTS = {'cf_input', 'stress', 'deep_rec', 'stdlib'} | {n for n in blocks if n.startswith('script_')}
ns = {}
for name, code in blocks.items():
    if name not in SCRIPTS:
        exec(code, ns)
g = ns.__getitem__
INF = float('inf')

def rand_digraph(n, p):
    return [(u, v) for u in range(n) for v in range(n) if u != v and random.random() < p]

def reach_closure(n, edges):
    r = [[i == j for j in range(n)] for i in range(n)]
    for u, v in edges: r[u][v] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if r[i][k] and r[k][j]: r[i][j] = True
    return r

def has_cycle(n, edges):
    r = reach_closure(n, edges)
    return any(r[v][u] for u, v in edges) or any(u == v for u, v in edges)

# ---------- topological sort (DFS and Kahn), cycle detection
for _ in range(600):
    n = random.randint(1, 7)
    E = rand_digraph(n, random.choice([.1, .2, .35]))
    if random.random() < .1: E.append((0, 0))
    adj = [[] for _ in range(n)]
    for u, v in E: adj[u].append(v)
    cyc = has_cycle(n, E)
    o1 = g('topo_dfs')(n, adj)
    o2 = g('topo_order')(n, E)
    if cyc:
        assert o1 is None and o2 is None, (n, E)
    else:
        for o in (o1, o2):
            assert o is not None and sorted(o) == list(range(n))
            pos = {v: i for i, v in enumerate(o)}
            assert all(pos[u] < pos[v] for u, v in E)
# deep chain: the iterative DFS must not hit the recursion limit
n = 200000
adj = [[i + 1] if i + 1 < n else [] for i in range(n)]
assert g('topo_dfs')(n, adj) == list(range(n))
print('topo ok')

# ---------- LC 207 / 210
for _ in range(500):
    n = random.randint(1, 6)
    pre = [[b, a] for a, b in rand_digraph(n, random.choice([.1, .25]))]   # [a, b]: b before a
    E = [(b, a) for a, b in pre]
    ok = not has_cycle(n, E)
    assert g('can_finish')(n, pre) == ok
    o = g('find_order')(n, pre)
    if ok:
        pos = {v: i for i, v in enumerate(o)}
        assert sorted(o) == list(range(n)) and all(pos[b] < pos[a] for a, b in pre)
    else:
        assert o == []
assert g('find_order')(1, []) == [0] and g('can_finish')(2, [[1, 0], [0, 1]]) is False
print('207/210 ok')

# ---------- DAG shortest and longest path
for _ in range(500):
    n = random.randint(1, 7)
    perm = list(range(n)); random.shuffle(perm)
    E = [(perm[i], perm[j], random.randint(-4, 6)) for i in range(n) for j in range(i + 1, n) if random.random() < .4]
    s = random.randrange(n)
    sh, lo = g('dag_shortest_longest')(n, E, s)
    adj = [[] for _ in range(n)]
    for u, v, w in E: adj[u].append((v, w))
    best_s, best_l = [INF] * n, [-INF] * n
    def walk(u, tot):
        best_s[u] = min(best_s[u], tot); best_l[u] = max(best_l[u], tot)
        for v, w in adj[u]: walk(v, tot + w)
    walk(s, 0)
    assert sh == best_s and lo == best_l, (n, E, s)
assert g('dag_shortest_longest')(2, [(0, 1, 1), (1, 0, 1)], 0) is None
print('dag paths ok')

# ---------- LC 329
for _ in range(500):
    R, C = random.randint(1, 4), random.randint(1, 4)
    M = [[random.randint(0, 5) for _ in range(C)] for _ in range(R)]
    @lru_cache(None)
    def f(r, c):
        b = 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and M[nr][nc] > M[r][c]: b = max(b, 1 + f(nr, nc))
        return b
    assert g('longest_increasing_path')(M) == max(f(r, c) for r in range(R) for c in range(C)), M
assert g('longest_increasing_path')([[9, 9, 4], [6, 6, 8], [2, 1, 1]]) == 4
assert g('longest_increasing_path')([[3, 4, 5], [3, 2, 6], [2, 2, 1]]) == 4
big = [[r * 200 + c for c in range(200)] for r in range(200)]      # a 40,000-step staircase would kill recursive DFS
assert g('longest_increasing_path')(big) == 399
print('329 ok')

# ---------- LC 1857
for _ in range(600):
    n = random.randint(1, 6)
    colors = ''.join(random.choice('abc') for _ in range(n))
    E = rand_digraph(n, random.choice([.15, .3]))
    if random.random() < .1: E.append((random.randrange(n), 0))
    got = g('largest_path_value')(colors, E)
    if has_cycle(n, E):
        assert got == -1, (colors, E)
        continue
    adj = [[] for _ in range(n)]
    for u, v in E: adj[u].append(v)
    best = 0
    def walk(u, cnt):
        global best
        cnt[colors[u]] = cnt.get(colors[u], 0) + 1
        best = max(best, max(cnt.values()))
        for v in adj[u]: walk(v, cnt)
        cnt[colors[u]] -= 1
    for s in range(n): walk(s, {})
    assert got == best, (colors, E, got, best)
assert g('largest_path_value')('abaca', [[0, 1], [0, 2], [2, 3], [3, 4]]) == 3
assert g('largest_path_value')('a', [[0, 0]]) == -1
print('1857 ok')

# ---------- Dijkstra family
def bf_dist(n, E, s):
    d = [INF] * n; d[s] = 0
    for _ in range(n):
        for u, v, w in E:
            if d[u] + w < d[v]: d[v] = d[u] + w
    return d
for _ in range(500):
    n = random.randint(1, 7); k = random.randint(1, n)
    T = [[u, v, random.randint(1, 9)] for u in range(1, n + 1) for v in range(1, n + 1) if u != v and random.random() < .3]
    d = bf_dist(n + 1, [(u, v, w) for u, v, w in T], k)
    exp = max(d[1:]); exp = -1 if exp == INF else exp
    assert g('network_delay')(T, n, k) == exp
for _ in range(500):
    n = random.randint(2, 7)
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if random.random() < .45]
    pr = [random.choice([.1, .25, .5, .8, 1.0]) for _ in pairs]
    s, t = random.sample(range(n), 2)
    best = [0.0] * n; best[s] = 1.0
    for _ in range(n + 1):
        for (a, b), p in zip(pairs, pr):
            for x, y in ((a, b), (b, a)):
                best[y] = max(best[y], best[x] * p)
    assert abs(g('max_probability')(n, [list(e) for e in pairs], pr, s, t) - best[t]) < 1e-9
def minimax_brute(R, C, cost):          # cost(r1, c1, r2, c2) of stepping; path cost = max of steps (+ start cell for 778)
    pass
for _ in range(500):
    R, C = random.randint(1, 4), random.randint(1, 4)
    H = [[random.randint(1, 9) for _ in range(C)] for _ in range(R)]
    d = [[INF] * C for _ in range(R)]; d[0][0] = 0
    for _ in range(R * C + 2):
        for r in range(R):
            for c in range(C):
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C:
                        d[nr][nc] = min(d[nr][nc], max(d[r][c], abs(H[nr][nc] - H[r][c])))
    exp = d[R - 1][C - 1]
    assert g('min_effort')(H) == exp == g('min_effort_bs')(H), (H, exp)
for _ in range(400):
    n = random.randint(1, 4)
    perm = random.sample(range(n * n), n * n)
    Gd = [perm[i * n:(i + 1) * n] for i in range(n)]
    d = [[INF] * n for _ in range(n)]; d[0][0] = Gd[0][0]
    for _ in range(n * n + 2):
        for r in range(n):
            for c in range(n):
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        d[nr][nc] = min(d[nr][nc], max(d[r][c], Gd[nr][nc]))
    assert g('swim_in_water')(Gd) == d[n - 1][n - 1], Gd
assert g('min_effort')([[1, 2, 2], [3, 8, 2], [5, 3, 5]]) == 2
assert g('swim_in_water')([[0, 2], [1, 3]]) == 3
print('dijkstra family ok')

# ---------- LC 787 and LC 1334
for _ in range(600):
    n = random.randint(2, 5)
    F = [[u, v, random.randint(1, 8)] for u in range(n) for v in range(n) if u != v and random.random() < .45]
    s, t = random.sample(range(n), 2); k = random.randint(0, 3)
    best = INF
    def walk(u, edges_left, tot):
        global best
        if u == t: best = min(best, tot)
        if edges_left == 0: return
        for a, b, w in F:
            if a == u: walk(b, edges_left - 1, tot + w)
    walk(s, k + 1, 0)
    assert g('cheapest_flights')(n, F, s, t, k) == (-1 if best == INF else best), (n, F, s, t, k)
assert g('cheapest_flights')(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1) == 700
for _ in range(500):
    n = random.randint(2, 6)
    E = [(u, v, random.randint(1, 9)) for u in range(n) for v in range(u + 1, n) if random.random() < .5]
    T = random.randint(1, 15)
    both = E + [(v, u, w) for u, v, w in E]
    cnts = []
    for i in range(n):
        d = bf_dist(n, both, i)
        cnts.append(sum(1 for j in range(n) if j != i and d[j] <= T))
    exp = max(i for i in range(n) if cnts[i] == min(cnts))
    assert g('find_the_city')(n, [list(e) for e in E], T) == exp, (n, E, T)
assert g('find_the_city')(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4) == 3
print('787 / 1334 ok')

# ---------- MST: Kruskal vs Prim vs every spanning tree
def all_tree_weights(n, E):
    out = []
    for comb in itertools.combinations(range(len(E)), n - 1):
        parent = list(range(n))
        def fd(x):
            while parent[x] != x: x = parent[x]
            return x
        ok = True
        for i in comb:
            a, b = fd(E[i][0]), fd(E[i][1])
            if a == b: ok = False; break
            parent[a] = b
        if ok: out.append((sum(E[i][2] for i in comb), comb))
    return out
for _ in range(500):
    n = random.randint(1, 6)
    E = [(u, v, random.randint(1, 6)) for u in range(n) for v in range(u + 1, n) if random.random() < .55]
    trees = all_tree_weights(n, E)
    exp = min((w for w, _ in trees), default=None)
    kr = g('kruskal')(n, [(w, u, v) for u, v, w in E])
    pr = g('prim')(n, E)
    assert kr == exp, (n, E, kr, exp)
    assert (pr[0] if pr else None) == exp, (n, E, pr, exp)
    if pr: assert len(pr[1]) == n - 1
    assert g('minimum_cost')(n, [[u + 1, v + 1, w] for u, v, w in E]) == (-1 if exp is None else exp)
for _ in range(300):
    n = random.randint(1, 7)
    pts = [[random.randint(-6, 6), random.randint(-6, 6)] for _ in range(n)]
    E = [(i, j, abs(pts[i][0] - pts[j][0]) + abs(pts[i][1] - pts[j][1])) for i in range(n) for j in range(i + 1, n)]
    assert g('min_cost_connect_points')(pts) == g('kruskal')(n, [(w, u, v) for u, v, w in E]) if n > 1 else g('min_cost_connect_points')(pts) == 0
assert g('min_cost_connect_points')([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
print('MST ok')

# ---------- LC 684
for _ in range(500):
    n = random.randint(3, 7)
    nodes = list(range(1, n + 1)); random.shuffle(nodes)
    E = [[nodes[random.randrange(i)], nodes[i]] for i in range(1, n)]          # a random tree
    while True:
        a, b = random.sample(range(1, n + 1), 2)
        if [a, b] not in E and [b, a] not in E: break
    E.append([a, b]); random.shuffle(E)
    exp = None
    for i in range(len(E) - 1, -1, -1):                                         # last edge whose removal leaves a tree
        rest = E[:i] + E[i + 1:]
        parent = list(range(n + 1))
        def fd(x):
            while parent[x] != x: x = parent[x]
            return x
        ok = True
        for x, y in rest:
            rx, ry = fd(x), fd(y)
            if rx == ry: ok = False; break
            parent[rx] = ry
        if ok: exp = E[i]; break
    assert g('find_redundant_connection')(E) == exp, E
assert g('find_redundant_connection')([[1, 2], [1, 3], [2, 3]]) == [2, 3]
print('684 ok')

# ---------- LC 1489
for _ in range(400):
    n = random.randint(2, 5)
    nodes = list(range(n)); random.shuffle(nodes)
    pairs = {(min(nodes[random.randrange(i)], nodes[i]), max(nodes[random.randrange(i)], nodes[i])) for i in range(1, n)}
    pairs = set()
    for i in range(1, n):
        j = random.randrange(i); pairs.add((min(nodes[i], nodes[j]), max(nodes[i], nodes[j])))
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < .35: pairs.add((u, v))
    E = [[u, v, random.randint(1, 3)] for u, v in sorted(pairs)]
    random.shuffle(E)
    trees = all_tree_weights(n, E)
    best = min(w for w, _ in trees)
    msts = [set(c) for w, c in trees if w == best]
    inter = set.intersection(*msts); union = set.union(*msts)
    crit, pseudo = g('find_critical_and_pseudo')(n, E)
    assert sorted(crit) == sorted(inter) and sorted(pseudo) == sorted(union - inter), (n, E)
assert g('find_critical_and_pseudo')(5, [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]]) == [[0, 1], [2, 3, 4, 5]]
print('1489 ok')


# ---------- facts quoted on the Graphs II page (hand traces and counterexamples)
dd, _ = g('dijkstra')(3, [(0, 1, 2), (0, 2, 3), (2, 1, -2)], 0)
NEG = [(0, 1, 2), (0, 2, 3), (2, 1, -2)]
assert g('dijkstra_done')(3, NEG, 0)[1] == 2            # WRONG: vertex 1 was finalised at 2, but 0 -> 2 -> 1 costs 1
assert g('bellman_ford')(3, NEG, 0)[1] == 1
assert dd[1] == 1                                             # the stale-check template re-expands vertex 1 and recovers here...
# ...but only by re-expanding vertices, which voids the O((V+E) log V) guarantee (it can go exponential), so never rely on it
assert g('topo_order')(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]) == [4, 5, 2, 0, 3, 1]
d5, par5 = g('dijkstra')(5, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)], 0)
assert d5 == [0, 3, 1, 4, 7] and par5 == [-1, 2, 0, 1, 3]
CLRS = [(0, 1, 6), (0, 2, 7), (1, 2, 8), (1, 3, 5), (1, 4, -4), (2, 3, -3), (2, 4, 9), (3, 1, -2), (4, 3, 7), (4, 0, 2)]
assert g('bellman_ford')(5, CLRS, 0) == [0, 2, 7, 4, -2]
d = [INF] * 5; d[0] = 0; rows = []
for _ in range(4):
    for u, v, w in CLRS:
        if d[u] + w < d[v]: d[v] = d[u] + w
    rows.append(d[:])
assert rows == [[0, 2, 7, 4, 2], [0, 2, 7, 4, -2], [0, 2, 7, 4, -2], [0, 2, 7, 4, -2]]
KR = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (3, 4, 2), (4, 5, 6), (3, 5, 7)]
assert g('kruskal')(6, [(w, u, v) for u, v, w in KR]) == 14 and g('prim')(6, KR)[0] == 14
assert g('knap01')([10, 20, 30], [60, 100, 120], 50) == 220                       # but ratio-greedy takes 60 + 100 = 160
for _ in range(300):                                                                # last stone weight vs a plain simulation
    st = [random.randint(1, 12) for _ in range(random.randint(0, 8))]
    cur = sorted(st)
    while len(cur) > 1:
        a, b = cur.pop(), cur.pop()
        if a != b: cur.append(a - b); cur.sort()
    assert g('last_stone_weight')(st) == (cur[0] if cur else 0)
for _ in range(300):
    n = random.randint(1, 7); E = [(u, v, random.randint(0, 9)) for u in range(n) for v in range(n) if u != v and random.random() < .3]
    assert g('dijkstra_done')(n, E, 0) == g('dijkstra')(n, E, 0)[0]
assert g('topo_order')(5, [(0, 2), (1, 2), (2, 3), (1, 3), (3, 4)]) == [0, 1, 2, 3, 4]
assert g('dijkstra')(4, [(0, 1, 2), (0, 2, 5), (1, 2, 1), (1, 3, 7), (2, 3, 2)], 0) == ([0, 2, 3, 5], [-1, 0, 1, 2])
EB = [(2, 3, -2), (1, 2, 3), (0, 1, 4), (0, 3, 9)]
d = [INF] * 4; d[0] = 0; rr = []
for _ in range(3):
    for u, v, w in EB:
        if d[u] + w < d[v]: d[v] = d[u] + w
    rr.append(d[:])
assert rr == [[0, 4, INF, 9], [0, 4, 7, 9], [0, 4, 7, 5]] and g('bellman_ford')(4, EB, 0) == [0, 4, 7, 5]
assert g('kruskal')(4, [(5, 0, 1), (3, 1, 2), (4, 0, 2), (1, 2, 3), (6, 1, 3)]) == 8
print('page facts ok')
print('GRAPHS II TESTS PASSED')
