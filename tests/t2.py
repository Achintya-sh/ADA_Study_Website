import os
import re, random, itertools
random.seed(11)
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'snippets', 'snips.py')).read()
blocks = {m.group(1): m.group(2).rstrip() + '\n' for m in re.finditer(r'#@@ (\w+)\n(.*?)(?=\n#@@ |\Z)', SRC, re.S)}
ns = {}
for name in ['chak', 'rev_chak', 'odd_walk', 'free_edges', 'visible_pairs', 'mitm', 'rev_brute','odd_walk_brute','free_brute','visible_brute','subsets_brute', 'frozen']:
    exec(blocks[name], ns)
g = ns.__getitem__
for n in range(1, 5):
    for c in itertools.product(range(1, n + 1), repeat=n):
        b = g('rev_brute')(list(c)); f = g('reverse_chak')(list(c))
        assert (b is None) == (f is None), c
for _ in range(400):
    n = random.randint(1, 6); E = [(u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.35]
    s, t = random.randrange(n), random.randrange(n)
    assert g('odd_walk_brute')(n, E, s, t) == g('shortest_odd_walk')(n, E, s, t)
    E3 = [(random.randrange(n), random.randrange(n), random.randint(1, 9)) for _ in range(random.randint(1, 10))]
    k = random.randint(0, 3)
    assert g('free_brute')(n, E3, 0, n - 1, k) == g('min_cost_k_free')(n, E3, 0, n - 1, k)
    a = [random.randint(1, 5) for _ in range(random.randint(1, 12))]
    assert g('visible_brute')(a) == g('visible_pairs')(a)
    b = [random.randint(-4, 6) for _ in range(random.randint(0, 12))]; T = random.randint(-5, 10)
    assert g('subsets_brute')(b, T) == g('count_subsets')(b, T)
for n in range(1, 7):
    for k in range(1, n + 2):
        for p in itertools.permutations(range(n)):
            assert g('sortable_brute')(p, k) == g('sortable')(p, k), (n, k, p)
print('vault ok')
