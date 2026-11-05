"""Exam-practice items added in v4 (quiz questions, mock extras, fill-ins, bug hunts, line ordering).
Everything that can be checked by running code IS checked: tests/t5.py executes it.
build.py turns DATA into JSON for the page, so the page and the tests can never drift apart."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, '..', 'snippets', 'snips.py'), encoding='utf-8').read()
_blocks = {m.group(1): m.group(2).rstrip() + '\n' for m in re.finditer(r'#@@ (\w+)\n(.*?)(?=\n#@@ |\Z)', SRC, re.S)}
NS = {}
for _n, _c in _blocks.items():
    if _n not in {'cf_input', 'stress', 'deep_rec', 'stdlib'}:
        exec(_c, NS)

CHECKS = []          # (description, callable) collected for tests/t5.py

def run(expr):
    return eval(expr, NS)

def Q(q, o, a, why):                                  # plain conceptual quiz question: o has 4 options, a = index
    assert len(o) == 4 and 0 <= a < 4 and len(set(o)) == 4, q
    return {'q': q, 'o': o, 'a': a, 'why': why}

def X(topic, q, code, expr, wrongs, pos, e, fmt=repr):
    """Mock extra whose correct option is COMPUTED by running `expr` in the snippet namespace."""
    correct = fmt(run(expr))
    assert correct not in wrongs, (q, correct, wrongs)
    o = list(wrongs); o.insert(pos, correct)
    assert len(o) == 4 and len(set(o)) == 4, q
    return {'t': topic, 'q': q, 'c': code, 'o': o, 'a': pos, 'e': e}

def XC(topic, q, o, a, e, code=None):                  # conceptual mock extra
    assert len(o) == 4 and len(set(o)) == 4 and 0 <= a < 4, q
    d = {'t': topic, 'q': q, 'o': o, 'a': a, 'e': e}
    if code: d['c'] = code
    return d

# ------------------------------------------------------------------ stop quizzes (appended to existing keys)
QUIZ = {
 'e3': [
  Q('Kahn’s algorithm finishes with fewer than n vertices in its output. What does that mean?',
    ['The graph has a directed cycle', 'The graph is disconnected', 'The queue was implemented wrongly', 'The graph has a negative edge'], 0,
    'Vertices on or behind a cycle never reach in-degree 0, so they are never queued. Disconnected pieces are still peeled.'),
  Q('Why can topological DP find a longest path in a DAG when longest path is hard on general graphs?',
    ['A DAG has no cycles, so each vertex is final before its out-edges are used', 'Longest path equals shortest path on a DAG', 'A DAG has at most V edges', 'Heaps work for longest paths'], 0,
    'In topological order every path into a vertex is already counted when you reach it, and no cycle can inflate a path.'),
  Q('In Dijkstra, what does a popped heap entry (d, u) with d > dist[u] mean?',
    ['It is stale: u was already improved, so skip it', 'u has a negative edge', 'u is unreachable', 'The heap is corrupt'], 0,
    'Heaps cannot lower an existing entry, so improved vertices get a new entry and the old one is skipped when it surfaces.'),
  Q('What single assumption does the correctness proof of Dijkstra need?',
    ['Extending a path never makes it cheaper', 'The graph is connected', 'Weights are integers', 'The graph is undirected'], 0,
    'That is why “minimise the largest edge” (max instead of +) still works, and why negative edges break it.'),
  Q('Path With Minimum Effort (LC 1631): what changes from plain Dijkstra?',
    ['The new cost is max(d, step) instead of d + step', 'You must use BFS', 'You must use Bellman–Ford', 'Nothing changes'], 0,
    'The cost of a path is its largest height difference, and max never decreases as the path grows, so Dijkstra still applies.'),
  Q('Bellman–Ford on 6 vertices with no negative cycle: how many rounds are always enough?',
    ['5', '6', '36', '3'], 0,
    'A shortest simple path has at most V − 1 = 5 edges, and round r settles every path of at most r edges.'),
  Q('For “at most k stops” (LC 787) you run Bellman–Ford for k + 1 rounds. Why must each round read the OLD distances?',
    ['Otherwise one round could use several edges and break the limit', 'To save memory', 'To detect negative cycles', 'Python lists are immutable'], 0,
    'Reading values updated earlier in the same round lets a path grow by more than one edge per round.'),
  Q('Floyd–Warshall: which loop must be outermost?',
    ['k, the allowed intermediate vertex', 'i, the source', 'j, the target', 'Any order works'], 0,
    'The table must be complete for intermediate vertices 0..k−1 before k is allowed.'),
  Q('State the cut property of minimum spanning trees.',
    ['A lightest edge crossing any cut is in some MST', 'The heaviest edge overall is never in an MST', 'Every MST has the same edges', 'A lightest edge is in every cycle'], 0,
    'Swap argument: any MST missing that edge can swap it in for another crossing edge without getting heavier.'),
  Q('Kruskal’s running time is dominated by…',
    ['sorting the edges, O(E log E)', 'union-find, O(E²)', 'building the adjacency list', 'the V − 1 merges'], 0,
    'With union by size and path compression each union-find operation is almost constant.'),
  Q('Which MST algorithm suits a complete graph on 2,000 points best?',
    ['Prim without a heap, O(V²)', 'Kruskal with all 2 million edges sorted', 'Bellman–Ford', 'Floyd–Warshall'], 0,
    'V² ≈ E, so the heap-free array version has the lowest overhead.'),
  Q('In LC 1489, an edge is critical when…',
    ['removing it makes the MST weight larger (or disconnects)', 'forcing it in keeps the MST weight', 'it is the heaviest edge', 'it is the lightest edge'], 0,
    'It then belongs to every MST. If forcing it in keeps the weight but removing it does not hurt, it is pseudo-critical.'),
 ],
 'c4': [
  Q('Which sort order makes the greedy for “most non-overlapping intervals” correct?',
    ['By end time, earliest first', 'By start time', 'By length, shortest first', 'By number of overlaps'], 0,
    'The exchange argument swaps the interval that ends first into any optimal schedule without causing a conflict.'),
  Q('Greedy by value-per-weight is optimal for…',
    ['fractional knapsack only', '0/1 knapsack', 'both', 'neither'], 0,
    'With splitting allowed no capacity is ever stranded; in 0/1 knapsack (60,10), (100,20), (120,30), capacity 50 it gives 160 instead of 220.'),
  Q('Coins 1, 3, 4 and amount 6: how do greedy and the DP compare?',
    ['Greedy 3 coins, DP 2 coins', 'Both give 2', 'Both give 3', 'Greedy 2, DP 3'], 0,
    'Greedy takes 4 + 1 + 1; the best is 3 + 3.'),
  Q('Task Scheduler (LC 621): what fixes the minimum length?',
    ['The most frequent task, which forces (top − 1) gaps of width n + 1', 'The number of distinct tasks', 'The cooldown alone', 'The alphabetical order'], 0,
    'The busiest task needs top − 1 full frames of n + 1 slots plus a last row; with more tasks than slots the answer is just the task count.'),
 ],
 'x15': [
  Q('In tree DP, what order must nodes be processed in?',
    ['Children before their parent', 'Parent before children', 'Left to right by value', 'Random'], 0,
    'A node’s answer is built from its children’s answers; reversing a parent-first order gives that order without recursion.'),
  Q('Maximum Path Sum (LC 124): why can a path that goes UP to the parent use only one child branch?',
    ['A path cannot split in two directions when it continues upward', 'Child branches are always negative', 'The root forbids it', 'It can use both'], 0,
    'Only the node where the path bends can use both branches; the value passed upward is the node plus its better branch.'),
  Q('When does “binary search the answer” work?',
    ['When “is x enough?” flips from no to yes exactly once as x grows', 'When the array is sorted', 'When the answer is an integer', 'When the graph is a tree'], 0,
    'A monotone yes/no check is the whole requirement; sortedness of the input is irrelevant.'),
  Q('Evaluate Division (LC 399) uses a weighted union-find. What does each node store?',
    ['The ratio of the node to its parent', 'The size of its set', 'Its depth', 'The edge weight to its neighbour'], 0,
    'A query is then the ratio of the two nodes to the common root, if they share one.'),
  Q('Running median with two heaps: which half goes in the max-heap?',
    ['The smaller half', 'The larger half', 'The odd values', 'The newest values'], 0,
    'The max-heap’s top is the largest of the small half and the min-heap’s top the smallest of the large half; the median sits between them.'),
  Q('Why does Word Search II (LC 212) use a trie?',
    ['One grid walk checks every word at once and cuts paths that match no prefix', 'Tries sort the words', 'It avoids recursion', 'It makes the grid smaller'], 0,
    'Without a trie you would search the grid once per word.'),
 ],
 'x16': [
  Q('n ≤ 100,000 and you need the answer within a few seconds in Python. Which cost class is the target?',
    ['O(n log n)', 'O(n²)', 'O(2ⁿ)', 'O(n!)'], 0, 'About 10⁷ simple operations per second: n² would be 10¹⁰.'),
  Q('n ≤ 20 and “choose any subset”. Which approach fits?',
    ['Bitmask or subset enumeration, O(2ⁿ)', 'O(n log n) sort', 'Floyd–Warshall', 'Binary search'], 0, '2²⁰ ≈ 10⁶ subsets is fine.'),
  Q('V ≤ 400 and all-pairs shortest paths. Which fits?',
    ['Floyd–Warshall, O(V³)', 'V runs of Bellman–Ford', 'Prim', 'Kahn'], 0, '400³ = 6.4 · 10⁷, borderline but standard; Bellman–Ford from every source would be V²E.'),
  Q('n ≤ 5,000 and a table indexed by two positions. Which cost is allowed?',
    ['O(n²) = 25 million cells', 'O(n³)', 'O(2ⁿ)', 'O(n!)'], 0, 'Two-dimensional DP over 5,000 × 5,000 is the usual ceiling.'),
  Q('The answer can be up to 10⁹ and you can check any candidate quickly. Which technique?',
    ['Binary search on the answer', 'DP table over the answer', 'Backtracking', 'Sorting'], 0, 'About 30 checks instead of 10⁹.'),
  Q('Which is the correct way to make a 3×3 grid of zeros in Python?',
    ['[[0] * 3 for _ in range(3)]', '[[0] * 3] * 3', '[0 * 3] * 3', '[[0, 3]] * 3'], 0, 'The second form makes three names for one row.'),
  Q('Why does recursive DFS often fail on a 10⁵-node chain in Python?',
    ['The default recursion limit is about 1,000 frames', 'Python has no recursion', 'Lists are too slow', 'The stack is a heap'], 0, 'Use an explicit stack or a topological peel.'),
  Q('heapq.heappop returns…',
    ['the smallest item', 'the largest item', 'the newest item', 'a random item'], 0, 'For a max-heap push negated values.'),
 ],
 'x17': [
  Q('Merge sort is stable if, on a tie, the item from…',
    ['the left half is taken first', 'the right half is taken first', 'either half, at random', 'neither half, the tie is dropped'], 0, 'Left items came first in the input, so they must stay first.'),
  Q('Merge sort’s extra space is…',
    ['O(n)', 'O(1)', 'O(log n) only', 'O(n²)'], 0, 'The merge needs a buffer for the combined output.'),
  Q('Why is appending to a doubling dynamic array O(1) amortised?',
    ['Copies happen at sizes 1, 2, 4, …, summing to less than 2n over n appends', 'Python never copies', 'The array is a linked list', 'Appending is free'], 0, 'Growing by one instead would copy n(n − 1)/2 elements in total.'),
  Q('In open addressing, why must a deleted slot become a tombstone, not an empty slot?',
    ['An empty slot would end searches early and hide keys placed after it', 'To free memory', 'To keep the table sorted', 'Python requires it'], 0, 'Probing stops at the first empty slot.'),
  Q('The load factor of a hash table is…',
    ['entries divided by slots', 'slots divided by entries', 'the number of collisions', 'the hash of the key'], 0, 'Tables resize when it passes a limit such as 0.75 (chaining) or 0.5 (linear probing).'),
 ],
}

# ------------------------------------------------------------------ extra mock-exam questions (appended)
EXTRA = [
 X('Graphs II', 'What does Kahn’s algorithm return for this graph? (Vertices with in-degree 0 are queued in index order.)',
   'edges = [(0, 2), (1, 2), (2, 3)]\nprint(topo_order(4, edges))', 'topo_order(4, [(0, 2), (1, 2), (2, 3)])',
   ['[1, 0, 2, 3]', '[0, 2, 1, 3]', '[3, 2, 1, 0]'], 0,
   'Vertices 0 and 1 start at in-degree 0 and are popped in that order. Vertex 2 reaches in-degree 0 only after both are gone, then 3.'),
 X('Graphs II', 'What distances does Dijkstra return from vertex 0?',
   'edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2)]\nprint(dijkstra(3, edges, 0)[0])', 'dijkstra(3, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0)[0]',
   ['[0, 4, 1]', '[0, 1, 3]', '[0, 3, 3]'], 1,
   '0 → 2 → 1 costs 1 + 2 = 3, which beats the direct edge 0 → 1 of cost 4.'),
 XC('Graphs II', 'Edge weights are all 0 or 1. Which algorithm runs in O(V + E)?',
    ['Dijkstra with a heap', '0-1 BFS with a deque', 'Bellman–Ford', 'Floyd–Warshall'], 1,
    'Free edges push to the front of the deque and cost-1 edges to the back, so the deque stays sorted by distance without a heap.'),
 XC('Graphs II', 'Why does the textbook Dijkstra fail on a graph with a negative edge?',
    ['A vertex finalised early can later be undercut', 'The heap overflows', 'Python cannot add negatives', 'It finds longest paths instead'], 0,
    'On 0→1 (2), 0→2 (3), 2→1 (−2) the textbook version finalises vertex 1 at 2, but 0→2→1 costs 1.'),
 XC('Graphs II', 'A graph has 6 vertices and no negative cycle. How many rounds of Bellman–Ford are always enough?',
    ['5', '6', '2', '36'], 0, 'A shortest simple path has at most V − 1 = 5 edges.'),
 X('Graphs II', 'What does this “at most k stops” search return (k = 1 stop, so up to 2 edges)?',
   'flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]\nprint(cheapest_flights(3, flights, 0, 2, 1))', 'cheapest_flights(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1)',
   ['500', '100', '-1'], 1, 'One stop allows 0 → 1 → 2 for 100 + 100 = 200, which beats the direct flight at 500.'),
 X('Graphs II', 'What total weight does Kruskal return?',
   'edges = [(5, 0, 1), (3, 1, 2), (4, 0, 2), (1, 2, 3), (6, 1, 3)]   # (weight, u, v)\nprint(kruskal(4, edges))', 'kruskal(4, [(5, 0, 1), (3, 1, 2), (4, 0, 2), (1, 2, 3), (6, 1, 3)])',
   ['9', '14', '13'], 2, 'Kept in order: 1, 3, 4. The edges of weight 5 and 6 would each close a cycle.'),
 XC('Graphs II', 'Why is Kruskal’s running time O(E log E)?',
    ['Sorting the edges dominates; union-find is almost constant per operation', 'Each edge needs a full DFS', 'It runs V Dijkstras', 'It builds an E × E table'], 0,
    'After the sort, each edge costs one find or union, which is near-constant with path compression and union by size.'),
 XC('Graphs II', 'Course Schedule (LC 207): prerequisites [[1, 0]] means…',
    ['take course 0 before course 1, so the edge is 0 → 1', 'take course 1 before course 0', 'the courses are the same', 'there is a cycle'], 0,
    'The pair is [a, b]: to take a you must first take b, so the edge points from b to a.'),
 XC('Graphs II', 'Longest Increasing Path in a Matrix (LC 329) is solved with Kahn’s algorithm by counting…',
    ['the number of BFS layers peeled', 'the number of cells', 'the largest value', 'the number of components'], 0,
    'Each layer adds one more cell to the longest path; peeling avoids the deep recursion the memoised DFS needs.'),
 XC('Graphs II', 'Path With Maximum Probability (LC 1514) with heapq: what do you push?',
    ['the negated probability, because heapq is a min-heap', 'the probability itself', 'the edge weight', 'the vertex only'], 0,
    'Popping the smallest negated value pops the largest probability.'),
 XC('Graphs II', 'Which statement is the cycle property of MSTs?',
    ['An edge strictly heavier than every other edge on some cycle belongs to no MST', 'Every cycle contains an MST edge', 'The lightest edge of a cycle is never in an MST', 'MSTs contain no cycles, so cycles are irrelevant'], 0,
    'Swap it out for the cycle’s lighter edges and the tree gets lighter, so it cannot have been minimum.'),
 XC('Graphs II', 'Which algorithm answers “connect all 3,000 points in the plane at minimum total distance”?',
    ['Prim without a heap, O(n²), on the implicit complete graph', 'Dijkstra from point 0', 'Topological sort', 'Floyd–Warshall'], 0,
    'The graph is complete (about 4.5 million edges), so the array version of Prim beats sorting all edges.'),
 X('Greedy', 'What do greedy and the DP return for coins 1, 3, 4 and amount 6?',
   "print(greedy_coins([1, 3, 4], 6), 'and', dp_coins([1, 3, 4], 6))", "'%d and %d' % (greedy_coins([1, 3, 4], 6), dp_coins([1, 3, 4], 6))",
   ['2 and 2', '3 and 3', '2 and 3'], 0, 'Greedy takes 4 + 1 + 1 = 3 coins; the best is 3 + 3 = 2 coins.', fmt=lambda v: v),
 X('Greedy', 'What does Task Scheduler return?',
   "print(least_interval(list('AAABBB'), 2))", "least_interval(list('AAABBB'), 2)",
   ['6', '7', '9'], 2, 'A B _ A B _ A B: the frame is (3 − 1) · (2 + 1) = 6 plus a final row holding the 2 tasks tied for the highest count.'),
 X('Greedy', 'What does Partition Labels return?',
   "print(partition_labels('ababcbacadefegdehijhklij'))", "partition_labels('ababcbacadefegdehijhklij')",
   ['[8, 8, 8]', '[9, 8, 7]', '[24]'], 0, 'The first piece ends at the last “a” (index 8), the second at the last “e” (index 15), the third is the rest.'),
 X('Greedy', 'What does Jump Game (LC 55) return?',
   'print(can_jump([3, 2, 1, 0, 4]))', 'can_jump([3, 2, 1, 0, 4])',
   ['True', 'it depends on the order of jumps', 'IndexError'], 1, 'Every route lands on index 3, whose jump length is 0, so index 4 is out of reach.'),
 XC('Greedy', 'For which problem is “take the highest value per kilo first” provably optimal?',
    ['fractional knapsack', '0/1 knapsack', 'coin change with coins 1, 3, 4', 'subset sum'], 0,
    'Only when fractions are allowed can no capacity be stranded.'),
 X('Monotonic stacks', 'What does this return? (index of the next strictly greater element, −1 if none)',
   'print(greater_next([2, 1, 2, 4, 3]))', 'greater_next([2, 1, 2, 4, 3])',
   ['[2, 2, 3, -1, -1]', '[3, 2, 3, -1, 4]', '[1, 2, 3, 4, -1]'], 1, 'Both 2s see the 4 at index 3 first as strictly greater; the 1 sees the 2 at index 2.'),
 X('Monotonic stacks', 'The code uses a strict comparison. What does it return when values are equal?',
   'print(greater_next([2, 2, 3]))', 'greater_next([2, 2, 3])',
   ['[1, 2, -1]', '[2, -1, -1]', '[1, 1, -1]'], 1, 'Equal values are not greater, so the first 2 must wait for the 3 at index 2, exactly like the second 2.'),
 XC('Monotonic stacks', 'Why is a monotonic stack pass O(n) even though one step may pop many elements?',
    ['each element is pushed once and popped at most once', 'pops are free', 'the stack is sorted', 'n is small'], 0,
    'The total number of pops cannot exceed the total number of pushes: that is amortised analysis.'),
 X('DP II conversions', 'What does the one-row version return?',
   "print(lcs_row('abcde', 'ace'))", "lcs_row('abcde', 'ace')",
   ['2', '5', '4'], 1, 'The longest common subsequence is “ace”, length 3.'),
 XC('DP II conversions', 'Why does the one-row LCS need a saved “diag” variable?',
    ['The cell diagonal to you is overwritten before you need it', 'Python lists cannot be edited', 'To count matches', 'To store the answer'], 0,
    'dp[i][j] reads dp[i+1][j+1], which lives in the slot that was just overwritten for the previous j.'),
 XC('DP II conversions', 'A table cell reads only the cell above and the cell to its left. Which way do the loops run?',
    ['forwards in both i and j', 'backwards in both', 'diagonally only', 'columns first, backwards'], 0,
    'Both dependencies have smaller indices, so they must be filled first.'),
 X('Bridges', 'What does House Robber III return for the tree [3, 2, 3, null, 3, null, 1]?',
   'print(rob_tree(build_tree([3, 2, 3, None, 3, None, 1])))', 'rob_tree(build_tree([3, 2, 3, None, 3, None, 1]))',
   ['6', '8', '9'], 1, 'Rob the root (3) and the two grandchildren (3 and 1): 3 + 3 + 1 = 7. Robbing the two middle nodes gives 2 + 3 = 5.'),
 X('Bridges', 'After adding 5, 2 and 8 to the two-heap median finder, what is find_median()?',
   'm = MedianFinder()\nfor x in (5, 2, 8):\n    m.add_num(x)\nprint(m.find_median())', '(lambda m: ([m.add_num(x) for x in (5, 2, 8)], m.find_median())[1])(MedianFinder())',
   ['2.0', '8.0', '5.5'], 0, 'Sorted: 2, 5, 8; the middle is 5. The max-heap holds {2, 5} with top 5; the min-heap holds {8}.'),
]

# ------------------------------------------------------------------ fill-in-the-blank code (answers in {{ }})
def L(*lines):
    return '\n'.join(lines)

BLANKS = [
 {'t': 'Graphs II', 'p': 'Kahn’s algorithm: peel every vertex whose prerequisites are all done.',
  'test': "topo_order(4, [(0, 2), (1, 2), (2, 3)]) == [0, 1, 2, 3] and topo_order(2, [(0, 1), (1, 0)]) is None",
  'c': L('def topo_order(n, edges):', '    adj = [[] for _ in range(n)]', '    indeg = [0] * n', '    for u, v in edges:', '        adj[u].append(v)',
         '        indeg[v] {{+=}} 1', '    q = deque(u for u in range(n) if indeg[u] == {{0}})', '    order = []', '    while q:', '        u = q.popleft()',
         '        order.append(u)', '        for v in adj[u]:', '            indeg[v] {{-=}} 1', '            if indeg[v] == 0:', '                q.append(v)',
         '    return order if len(order) == {{n}} else None')},
 {'t': 'Graphs II', 'p': 'Dijkstra with a heap: skip stale entries, relax, push the improvement.',
  'test': "dijkstra(3, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0)[0] == [0, 3, 1]",
  'c': L('def dijkstra(n, edges, src):', '    adj = [[] for _ in range(n)]', '    for u, v, w in edges:', '        adj[u].append((v, w))',
         "    INF = float('inf')", '    dist, par = [INF] * n, [-1] * n', '    dist[src] = 0', '    heap = [(0, src)]', '    while heap:',
         '        d, u = heapq.heappop(heap)', '        if d {{>}} dist[u]:', '            continue', '        for v, w in adj[u]:',
         '            if d + w {{<}} dist[v]:', '                dist[v], par[v] = d + w, u', '                heapq.heappush(heap, ({{dist[v]}}, v))',
         '    return dist, par')},
 {'t': 'Graphs II', 'p': 'Kruskal: lightest edges first, keep an edge only if it joins two components.',
  'test': "kruskal(4, [(5, 0, 1), (3, 1, 2), (4, 0, 2), (1, 2, 3), (6, 1, 3)]) == 8",
  'c': L('def kruskal(n, edges):', '    dsu, total, used = DSU(n), 0, 0', '    for w, u, v in {{sorted}}(edges):', '        if dsu.{{union}}(u, v):',
         '            total += w', '            used += 1', '    return total if used == n {{-}} 1 else None')},
 {'t': 'Graphs II', 'p': 'At most k stops: k + 1 rounds, each reading the OLD distances.',
  'test': "cheapest_flights(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200",
  'c': L('def cheapest_flights(n, flights, src, dst, k):', "    INF = float('inf')", '    dist = [INF] * n', '    dist[src] = 0',
         '    for _ in range({{k + 1}}):', '        nxt = {{dist[:]}}', '        for u, v, w in flights:', '            if dist[u] + w < nxt[v]:',
         '                nxt[v] = dist[u] + w', '        dist = {{nxt}}', '    return -1 if dist[dst] == INF else dist[dst]')},
 {'t': 'Monotonic stacks', 'p': 'Next strictly greater element: pop everything smaller than the newcomer.',
  'test': "greater_next([2, 1, 2, 4, 3]) == [3, 2, 3, -1, -1]",
  'c': L('def greater_next(a):', '    out, stack = [-1] * len(a), []', '    for i, x in enumerate(a):', '        while stack and a[stack[-1]] {{<}} x:',
         '            out[{{stack.pop()}}] = i', '        stack.append({{i}})', '    return out')},
 {'t': 'Greedy', 'p': 'Most non-overlapping intervals: sort by END time, keep what starts after the last kept one ends.',
  'test': "keep_intervals([(1, 10), (2, 3), (4, 5)]) == 2",
  'c': L('def keep_intervals(iv):', "    kept, last_end = 0, -float('inf')", '    for s, e in sorted(iv, key=lambda p: p[{{1}}]):',
         '        if s {{>=}} last_end:', '            kept += 1', '            last_end = {{e}}', '    return kept')},
 {'t': 'DP II conversions', 'p': 'One-row LCS: save the diagonal before it is overwritten.',
  'test': "lcs_row('abcde', 'ace') == 3",
  'c': L('def lcs_row(a, b):', '    n, m = len(a), len(b)', '    row = [0] * (m + 1)', '    for i in range(n - 1, -1, -1):', '        diag = 0',
         '        for j in range(m - 1, -1, -1):', '            old = row[j]', '            row[j] = 1 + diag if a[i] == b[j] else max(old, row[{{j + 1}}])',
         '            diag = {{old}}', '    return row[0]')},
]

# ------------------------------------------------------------------ spot the bug.  'a' = buggy line numbers (0-based);
# 'fix' maps line number -> replacement line ('' deletes it); 'test' is evaluated for the buggy and the fixed version.
BUGS = [
 {'t': 'Graphs II', 'p': 'dijkstra_bad({0: [(1, 5), (2, 1)], 1: [], 2: [(1, 1)]}, 0) gives vertex 1 a distance of 5; the right answer is 2.',
  'c': ['def dijkstra_bad(adj, s):', '    dist = {s: 0}', '    seen = {s}', '    heap = [(0, s)]', '    while heap:', '        d, u = heapq.heappop(heap)',
        '        for v, w in adj[u]:', '            if v not in seen:', '                seen.add(v)', '                dist[v] = d + w', '                heapq.heappush(heap, (d + w, v))', '    return dist'],
  'a': [7, 8], 'fix': {7: '            if v not in dist or d + w < dist[v]:', 8: None},
  'test': "dijkstra_bad({0: [(1, 5), (2, 1)], 1: [], 2: [(1, 1)]}, 0)[1]", 'bad': 5, 'good': 2,
  'e': 'Marking a vertex when it is first pushed is BFS’s rule. In Dijkstra the first route found (cost 5 to vertex 1) can be beaten later (0 → 2 → 1 costs 2), so a vertex is final only when popped. Relax whenever a cheaper route appears.'},
 {'t': 'Graphs II', 'p': 'find_order_bad(3, [[1, 0], [2, 1], [1, 2]]) should return [] because courses 1 and 2 need each other, but it returns [0].',
  'c': ['def find_order_bad(n, pre):', '    adj = [[] for _ in range(n)]', '    indeg = [0] * n', '    for a, b in pre:', '        adj[b].append(a)', '        indeg[a] += 1',
        '    q = deque(i for i in range(n) if indeg[i] == 0)', '    order = []', '    while q:', '        u = q.popleft()', '        order.append(u)', '        for v in adj[u]:',
        '            indeg[v] -= 1', '            if indeg[v] == 0:', '                q.append(v)', '    return order'],
  'a': [15], 'fix': {15: '    return order if len(order) == n else []'},
  'test': "find_order_bad(3, [[1, 0], [2, 1], [1, 2]])", 'bad': [0], 'good': [],
  'e': 'Kahn never queues vertices on a cycle, so a cycle shows up as an order shorter than n. Without the length check the function silently returns a partial order.'},
 {'t': 'Graphs II', 'p': 'cheapest_flights_bad(4, [[0, 1, 100], [1, 2, 100], [2, 3, 100], [0, 3, 1000]], 0, 3, 1) should be 1000 (at most 2 edges) but returns 300.',
  'c': ['def cheapest_flights_bad(n, flights, src, dst, k):', "    INF = float('inf')", '    dist = [INF] * n', '    dist[src] = 0', '    for _ in range(k + 1):',
        '        for u, v, w in flights:', '            if dist[u] + w < dist[v]:', '                dist[v] = dist[u] + w', '    return -1 if dist[dst] == INF else dist[dst]'],
  'a': [5, 6, 7], 'fix': {4: '    for _ in range(k + 1):\n        nxt = dist[:]', 5: '        for u, v, w in flights:', 6: '            if dist[u] + w < nxt[v]:', 7: '                nxt[v] = dist[u] + w\n        dist = nxt'},
  'test': "cheapest_flights_bad(4, [[0, 1, 100], [1, 2, 100], [2, 3, 100], [0, 3, 1000]], 0, 3, 1)", 'bad': 300, 'good': 1000,
  'e': 'Updating dist in place lets a later edge in the same round use a value improved earlier in that round, so one round can add several edges and the stop limit is ignored. Read from the old list and write to a copy.'},
 {'t': 'Graphs II', 'p': 'floyd_bad on the path 0 → 2 → 3 → 1 (all weights 1) leaves the distance from 0 to 1 at infinity; it should be 3.',
  'c': ['def floyd_bad(n, edges):', "    INF = float('inf')", '    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]', '    for u, v, w in edges:', '        d[u][v] = min(d[u][v], w)',
        '    for i in range(n):', '        for j in range(n):', '            for k in range(n):', '                if d[i][k] + d[k][j] < d[i][j]:', '                    d[i][j] = d[i][k] + d[k][j]', '    return d'],
  'a': [5, 6, 7], 'fix': {5: '    for k in range(n):', 6: '        for i in range(n):', 7: '            for j in range(n):'},
  'test': "floyd_bad(4, [(0, 2, 1), (2, 3, 1), (3, 1, 1)])[0][1]", 'bad': float('inf'), 'good': 3,
  'e': 'The loop over the intermediate vertex k must be outermost: the table has to be complete for k − 1 before k is allowed as a stop. With k innermost, d[0][1] is examined, in its one and only visit, before d[0][3] (the first half of the route 0 → 3 → 1) is known.'},
 {'t': 'Graphs II', 'p': 'kruskal_bad(4, [(0, 1, 5), (1, 2, 3), (0, 2, 4), (2, 3, 1), (1, 3, 6)]) returns 15 instead of 8.',
  'c': ['def kruskal_bad(n, edges):', '    dsu, total, used = DSU(n), 0, 0', '    for u, v, w in sorted(edges):', '        if dsu.union(u, v):', '            total += w', '            used += 1', '    return total if used == n - 1 else None'],
  'a': [2], 'fix': {2: '    for u, v, w in sorted(edges, key=lambda e: e[2]):'},
  'test': "kruskal_bad(4, [(0, 1, 5), (1, 2, 3), (0, 2, 4), (2, 3, 1), (1, 3, 6)])", 'bad': 15, 'good': 8,
  'e': 'sorted(edges) sorts tuples by their first item, the vertex u, not the weight. Kruskal needs the lightest edges first: sort by e[2], or store edges as (w, u, v).'},
 {'t': 'Graphs II', 'p': 'has_cycle_bad(4, [[1, 2], [3], [3], []]) says there is a cycle, but the graph is a diamond-shaped DAG.',
  'c': ['def has_cycle_bad(n, adj):', '    WHITE, GREY, BLACK = 0, 1, 2', '    color = [WHITE] * n', '    def dfs(u):', '        color[u] = GREY', '        for v in adj[u]:',
        '            if color[v] != WHITE:', '                return True', '            if dfs(v):', '                return True', '        color[u] = BLACK', '        return False',
        '    return any(color[u] == WHITE and dfs(u) for u in range(n))'],
  'a': [6], 'fix': {6: '            if color[v] == GREY:'},
  'test': "has_cycle_bad(4, [[1, 2], [3], [3], []])", 'bad': True, 'good': False,
  'e': 'Only a vertex on the CURRENT path (grey) proves a cycle. A finished (black) vertex reached again through another route, as vertex 3 is here, is perfectly fine in a DAG.'},
 {'t': 'Greedy', 'p': 'max_meetings_bad([(1, 10), (2, 3), (4, 5)]) returns 1; two meetings fit.',
  'c': ['def max_meetings_bad(iv):', "    kept, last_end = 0, -float('inf')", '    for s, e in sorted(iv):', '        if s >= last_end:', '            kept += 1', '            last_end = e', '    return kept'],
  'a': [2], 'fix': {2: '    for s, e in sorted(iv, key=lambda p: p[1]):'},
  'test': "max_meetings_bad([(1, 10), (2, 3), (4, 5)])", 'bad': 1, 'good': 2,
  'e': 'Sorting by start time lets one long early meeting block everything. The exchange argument works only when you sort by end time.'},
 {'t': 'Monotonic stacks', 'p': 'next_greater_bad([2, 2, 3]) returns [1, 2, -1]; the first 2 should point at the 3, index 2.',
  'c': ['def next_greater_bad(a):', '    out, stack = [-1] * len(a), []', '    for i, x in enumerate(a):', '        while stack and a[stack[-1]] <= x:', '            out[stack.pop()] = i', '        stack.append(i)', '    return out'],
  'a': [3], 'fix': {3: '        while stack and a[stack[-1]] < x:'},
  'test': "next_greater_bad([2, 2, 3])", 'bad': [1, 2, -1], 'good': [2, 2, -1],
  'e': '“Strictly greater” needs <; with <= an equal value pops its twin and is wrongly recorded as its next greater element.'},
]

# ------------------------------------------------------------------ put the lines in order
PARSONS = [
 {'t': 'Kahn’s algorithm', 'p': 'Order the lines of the topological sort that detects cycles.',
  'test': "topo_order(4, [(0, 2), (1, 2), (2, 3)]) == [0, 1, 2, 3] and topo_order(2, [(0, 1), (1, 0)]) is None",
  'c': ['def topo_order(n, edges):', '    adj = [[] for _ in range(n)]', '    indeg = [0] * n', '    for u, v in edges:', '        adj[u].append(v)', '        indeg[v] += 1',
        '    q = deque(u for u in range(n) if indeg[u] == 0)', '    order = []', '    while q:', '        u = q.popleft()', '        order.append(u)', '        for v in adj[u]:',
        '            indeg[v] -= 1', '            if indeg[v] == 0:', '                q.append(v)', '    return order if len(order) == n else None'],
  'why': 'Count in-degrees first, queue the sources, then pop, record, lower the neighbours’ counts and queue those that reach zero. The final length check is what reports a cycle.'},
 {'t': 'Dijkstra with a heap', 'p': 'Order the lines of Dijkstra (stale-entry check included).',
  'test': "dijkstra(3, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0)[0] == [0, 3, 1]",
  'c': ['def dijkstra(n, edges, src):', '    adj = [[] for _ in range(n)]', '    for u, v, w in edges:', '        adj[u].append((v, w))', "    INF = float('inf')", '    dist, par = [INF] * n, [-1] * n',
        '    dist[src] = 0', '    heap = [(0, src)]', '    while heap:', '        d, u = heapq.heappop(heap)', '        if d > dist[u]:', '            continue', '        for v, w in adj[u]:',
        '            if d + w < dist[v]:', '                dist[v], par[v] = d + w, u', '                heapq.heappush(heap, (dist[v], v))', '    return dist, par'],
  'why': 'Pop first, skip the stale entry, and only then relax; a push happens only when a strictly shorter route is found.'},
 {'t': 'Kruskal with union-find', 'p': 'Order the lines of Kruskal’s MST.',
  'test': "kruskal(4, [(5, 0, 1), (3, 1, 2), (4, 0, 2), (1, 2, 3), (6, 1, 3)]) == 8",
  'c': ['def kruskal(n, edges):', '    dsu, total, used = DSU(n), 0, 0', '    for w, u, v in sorted(edges):', '        if dsu.union(u, v):', '            total += w', '            used += 1', '    return total if used == n - 1 else None'],
  'why': 'Sort first so the lightest edge is considered first; add the weight only when union() accepts the edge; check V − 1 edges at the end.'},
 {'t': 'Next greater element', 'p': 'Order the lines of the monotonic-stack scan.',
  'test': "greater_next([2, 1, 2, 4, 3]) == [3, 2, 3, -1, -1]",
  'c': ['def greater_next(a):', '    out, stack = [-1] * len(a), []', '    for i, x in enumerate(a):', '        while stack and a[stack[-1]] < x:', '            out[stack.pop()] = i', '        stack.append(i)', '    return out'],
  'why': 'For each newcomer, first answer everyone on the stack it beats, then push the newcomer itself.'},
]

def _fix_text(b):
    """The corrected code shown after a bug is found: replacement lines, with deletions noted."""
    out = []
    for i in sorted(b['fix']):
        new = b['fix'][i]
        out.append('# remove: ' + b['c'][i].strip() if new is None else new)
    return '\n'.join(out)

def _indent(line):
    return len(line) - len(line.lstrip())

# Alternative valid orders for the ordering puzzles, found by swapping neighbouring lines of equal indentation
# and RUNNING the result against several tests; the page accepts any of them, so a correct answer is never marked wrong.
PARSON_TESTS = {
 'Kahn’s algorithm': ["topo_order(4, [(0, 2), (1, 2), (2, 3)]) == [0, 1, 2, 3]", "topo_order(2, [(0, 1), (1, 0)]) is None",
                      "topo_order(5, [(4, 3), (3, 2), (2, 1), (1, 0)]) == [4, 3, 2, 1, 0]", "topo_order(1, []) == [0]", "topo_order(3, [(0, 1), (1, 2), (2, 1)]) is None"],
 'Dijkstra with a heap': ["dijkstra(3, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0) == ([0, 3, 1], [-1, 2, 0])", "dijkstra(4, [(0, 1, 2), (1, 2, 3)], 0)[0] == [0, 2, 5, float('inf')]",
                         "dijkstra(1, [], 0) == ([0], [-1])"],
 'Kruskal with union-find': ["kruskal(4, [(5, 0, 1), (3, 1, 2), (4, 0, 2), (1, 2, 3), (6, 1, 3)]) == 8", "kruskal(3, [(1, 0, 1)]) is None", "kruskal(1, []) == 0"],
 'Next greater element': ["greater_next([2, 1, 2, 4, 3]) == [3, 2, 3, -1, -1]", "greater_next([2, 2, 3]) == [2, 2, -1]", "greater_next([]) == []", "greater_next([5, 4, 3]) == [-1, -1, -1]"],
}

def _alternatives(item):
    lines, tests = item['c'], PARSON_TESTS[item['t']]
    def passes(order):
        ns = fresh_ns()
        try:
            exec('\n'.join(lines[k] for k in order), ns)
            return all(eval(t, ns) for t in tests)
        except Exception:
            return False
    start = tuple(range(len(lines)))
    assert passes(start), item['t']
    seen, valid, stack = {start}, [start], [start]
    while stack:
        cur = stack.pop()
        for i in range(len(cur) - 1):
            a, b = cur[i], cur[i + 1]
            if _indent(lines[a]) != _indent(lines[b]):
                continue
            nxt = list(cur); nxt[i], nxt[i + 1] = b, a; nxt = tuple(nxt)
            if nxt in seen:
                continue
            seen.add(nxt)
            if passes(nxt):
                valid.append(nxt); stack.append(nxt)
    # equal lines are interchangeable, so drop orders that read identically to the canonical one or to each other
    uniq, texts = [], {tuple(lines[k] for k in start)}
    for o in valid[1:]:
        t = tuple(lines[k] for k in o)
        if t not in texts:
            texts.add(t); uniq.append(list(o))
    return uniq

def fresh_ns():
    from collections import deque
    import heapq
    ns = dict(NS); ns.update({'deque': deque, 'heapq': heapq})
    return ns

for _p in PARSONS:
    _p['ok'] = _alternatives(_p)

def _pub_bug(b):
    return {'t': b['t'], 'p': b['p'], 'c': b['c'], 'a': b['a'], 'e': b['e'], 'f': _fix_text(b)}

DATA = {'quiz': QUIZ, 'extra': EXTRA,
        'blanks': [{'t': b['t'], 'p': b['p'], 'c': b['c']} for b in BLANKS],
        'bugs': [_pub_bug(b) for b in BUGS],
        'parsons': [{'t': b['t'], 'p': b['p'], 'c': b['c'], 'why': b['why'], 'ok': b['ok']} for b in PARSONS],
        'names': {'x15': 'Bridges between the tools', 'x16': 'Contest readiness', 'x17': 'Appendix: merge sort, amortised, hashing'},
        'secmap': {'x15': 'ch15', 'x16': 'ch16', 'x17': 'ch17'}}
