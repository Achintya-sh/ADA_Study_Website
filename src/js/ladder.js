/* ===== The Ladder: one list, two rating scales, six tiers ===== */
(function () {
  'use strict';
  const cfURL = id => { const m = String(id).match(/^(\d+)([A-Z]\d?)$/); return m ? `https://codeforces.com/problemset/problem/${m[1]}/${m[2]}` : '#'; };
  const UP = new Set(['i', 'ii', 'iii', 'iv', 'v', 'bst', 'lru', 'dfs', 'bfs']);
  const TT = s => s.split('-').map(w => UP.has(w) ? w.toUpperCase() : w.replace(/^(\d)sum$/, '$1Sum').replace(/^./, c => c.toUpperCase())).join(' ');
  const LAD = [], seen = new Set();
  const add = o => { if (!seen.has(o.k)) { seen.add(o.k); LAD.push(o); } };
  const EST = { e: 900, m: 1300, M: 1500, h: 1750 };

  /* the old LeetCode ladder keeps its keys, so earlier ticks survive */
  Object.entries(LADDER).forEach(([topic, list]) => list.forEach(p => add({ k: String(p.id), t: `${p.id}. ${p.t}`, u: `https://leetcode.com/problems/${p.s}/`, src: 'LC', topic, pat: p.p, lc: p.r || null, est: p.r ? null : 1250 })));
  const L = (id, slug, topic, pat, d, lc) => add({ k: String(id), t: `${id}. ${TT(slug)}`, u: `https://leetcode.com/problems/${slug}/`, src: 'LC', topic, pat, lc: lc || null, est: lc ? null : EST[d] });
  const S = (id, t, topic, pat, est) => add({ k: 'cses:' + id, t: `CSES ${t}`, u: `https://cses.fi/problemset/task/${id}`, src: 'CSES', topic, pat, est });
  const C = (id, t, topic, pat, cf, h, v) => add({ k: 'cf:' + id, t: `CF ${id} ${t}`, u: cfURL(id), src: 'CF', topic, pat, cf, h: h || '', v: v || '' });
  const O = (key, t, topic, pat, est, v) => add({ k: 'orig:' + key, t: t, u: '#v-' + key, src: 'Vault', topic, pat, est, v, orig: true, h: 'Statement, hints and solution are in the Vault below the Ladder.' });

  /* ---- arrays, search, prefix sums, windows ---- */
  L(1, 'two-sum', 'arr', 'hash map', 'e'); L(167, 'two-sum-ii-input-array-is-sorted', 'arr', 'two pointers', 'm'); L(15, '3sum', 'arr', 'sort + two pointers', 'm');
  L(11, 'container-with-most-water', 'arr', 'two pointers', 'm'); L(560, 'subarray-sum-equals-k', 'arr', 'prefix sums + dictionary', 'm'); L(209, 'minimum-size-subarray-sum', 'arr', 'sliding window', 'm');
  L(3, 'longest-substring-without-repeating-characters', 'arr', 'sliding window', 'm'); L(76, 'minimum-window-substring', 'arr', 'sliding window', 'h'); L(875, 'koko-eating-bananas', 'arr', 'binary search on the answer', 'm');
  L(1011, 'capacity-to-ship-packages-within-d-days', 'arr', 'binary search on the answer', 'm'); L(410, 'split-array-largest-sum', 'arr', 'binary search on the answer', 'h'); L(33, 'search-in-rotated-sorted-array', 'arr', 'binary search', 'm');
  L(238, 'product-of-array-except-self', 'arr', 'prefix and suffix products', 'm'); L(53, 'maximum-subarray', 'arr', 'Kadane', 'e');
  S(1640, 'Sum of Two Values', 'arr', 'hash map or two pointers', 1000); S(1643, 'Maximum Subarray Sum', 'arr', 'Kadane', 1000); S(1141, 'Playlist', 'arr', 'sliding window', 1200);
  S(1660, 'Subarray Sums I', 'arr', 'two pointers', 1100); S(1661, 'Subarray Sums II', 'arr', 'prefix sums + dictionary', 1300);
  C('1913C', 'Game with Multiset', 'arr', 'greedy / bitmasks / binary search', 1300);
  C('1431B', 'Polycarp and the Language of Gods', 'arr', 'implementation / two pointers', 1400);
  C('2104D', 'Array and GCD', 'arr', 'binary search / greedy / math', 1400);
  C('2132C2', 'The Cunning Seller (hard version)', 'arr', 'binary search / greedy / math', 1400);
  C('1901D', 'Yet Another Monster Fight', 'arr', 'binary search / dp / greedy', 1700);
  C('1731D', 'Valiant’s New Map', 'arr', 'binary search + 2D prefix sums', 1700, 'Binary search the side length k; a 2D prefix-sum check tests whether some k×k square has every value at least k.');

  /* ---- sorting ---- */
  L(75, 'sort-colors', 'sort', 'Dutch national flag', 'm'); L(215, 'kth-largest-element-in-an-array', 'sort', 'quickselect or heap', 'm'); L(179, 'largest-number', 'sort', 'custom comparator', 'm');
  L(56, 'merge-intervals', 'sort', 'sort, then merge', 'm'); L(912, 'sort-an-array', 'sort', 'implement a sort', 'm'); L(148, 'sort-list', 'sort', 'merge sort on a linked list', 'm');
  L(493, 'reverse-pairs', 'sort', 'merge sort counting', 'h'); L(315, 'count-of-smaller-numbers-after-self', 'sort', 'merge sort or Fenwick', 'h'); L(324, 'wiggle-sort-ii', 'sort', 'quickselect + interleave', 'M');
  L(164, 'maximum-gap', 'sort', 'bucket or radix sort', 'h'); L(969, 'pancake-sorting', 'sort', 'place the maximum, flip', 'm');
  S(1621, 'Distinct Numbers', 'sort', 'sort + scan', 900); S(1074, 'Stick Lengths', 'sort', 'the median minimises', 1000);
  C('733D', 'Kostya the Sculptor', 'sort', 'sorting / hashing', 1600);

  /* ---- BST ---- */
  L(98, 'validate-binary-search-tree', 'bst', 'bounds, not just the parent', 'm'); L(230, 'kth-smallest-element-in-a-bst', 'bst', 'inorder, stop early', 'm'); L(235, 'lowest-common-ancestor-of-a-binary-search-tree', 'bst', 'the split point', 'm');
  L(108, 'convert-sorted-array-to-binary-search-tree', 'bst', 'middle element', 'e'); L(450, 'delete-node-in-a-bst', 'bst', 'three delete cases', 'm'); L(538, 'convert-bst-to-greater-tree', 'bst', 'reverse inorder', 'm');
  L(99, 'recover-binary-search-tree', 'bst', 'inorder descents', 'M'); L(173, 'binary-search-tree-iterator', 'bst', 'controlled inorder', 'm'); L(1008, 'construct-binary-search-tree-from-preorder-traversal', 'bst', 'running upper bound', 'm');
  L(669, 'trim-a-binary-search-tree', 'bst', 'prune by range', 'm'); L(1382, 'balance-a-binary-search-tree', 'bst', 'inorder, rebuild (your Contest 1 Q6)', 'm'); L(530, 'minimum-absolute-difference-in-bst', 'bst', 'neighbours in inorder', 'e');
  L(653, 'two-sum-iv-input-is-a-bst', 'bst', 'inorder + two pointers', 'e'); L(701, 'insert-into-a-binary-search-tree', 'bst', 'walk down', 'm'); L(501, 'find-mode-in-binary-search-tree', 'bst', 'runs in inorder', 'e');

  /* ---- heaps ---- */
  L(703, 'kth-largest-element-in-a-stream', 'heap', 'size-k min-heap', 'e'); L(347, 'top-k-frequent-elements', 'heap', 'Counter + heap', 'm'); L(23, 'merge-k-sorted-lists', 'heap', 'k-way merge', 'h');
  L(295, 'find-median-from-data-stream', 'heap', 'two heaps', 'h'); L(1046, 'last-stone-weight', 'heap', 'max-heap', 'e'); L(2406, 'divide-intervals-into-minimum-number-of-groups', 'heap', 'rooms: heap of end times', 'm');
  L(621, 'task-scheduler', 'heap', 'greedy + heap', 'm'); L(767, 'reorganize-string', 'heap', 'always place the most frequent', 'm'); L(373, 'find-k-pairs-with-smallest-sums', 'heap', 'k-way merge', 'm');
  L(378, 'kth-smallest-element-in-a-sorted-matrix', 'heap', 'k-way merge', 'm'); L(502, 'ipo', 'heap', 'sort by cost + max-heap', 'h'); L(407, 'trapping-rain-water-ii', 'heap', 'Dijkstra-like flood', 'h');
  L(480, 'sliding-window-median', 'heap', 'two heaps + lazy deletion', 'h'); L(1792, 'maximum-average-pass-ratio', 'heap', 'greedy by marginal gain', 'm');
  S(1091, 'Concert Tickets', 'heap', 'sorted list + bisect', 1500); S(1076, 'Sliding Window Median', 'heap', 'two heaps + lazy deletion', 2000);
  C('1418D', 'Trash Problem', 'heap', 'sorted structure + gaps', 2100, 'The answer is the span of all points minus the largest gap between neighbours. Keep the gaps in an ordered multiset, or a heap with lazy deletion.');

  /* ---- monotonic stack ---- */
  L(739, 'daily-temperatures', 'mono', 'next greater', 'm'); L(496, 'next-greater-element-i', 'mono', 'next greater', 'e'); L(503, 'next-greater-element-ii', 'mono', 'circular next greater', 'm');
  L(84, 'largest-rectangle-in-histogram', 'mono', 'histogram stack', 'h'); L(85, 'maximal-rectangle', 'mono', 'histogram per row', 'h'); L(42, 'trapping-rain-water', 'mono', 'two pointers or stack', 'h');
  L(901, 'online-stock-span', 'mono', 'previous greater', 'm'); L(907, 'sum-of-subarray-minimums', 'mono', 'contribution counting', 'M'); L(402, 'remove-k-digits', 'mono', 'pop while bigger', 'm');
  L(316, 'remove-duplicate-letters', 'mono', 'lexicographic stack', 'M'); L(239, 'sliding-window-maximum', 'mono', 'monotonic deque', 'h'); L(862, 'shortest-subarray-with-sum-at-least-k', 'mono', 'prefix sums + deque', 'h');
  L(2104, 'sum-of-subarray-ranges', 'mono', 'contribution counting', 'M'); L(456, '132-pattern', 'mono', 'stack from the right', 'M'); L(1856, 'maximum-subarray-min-product', 'mono', 'boundaries + prefix sums', 'M');
  S(1645, 'Nearest Smaller Values', 'mono', 'previous smaller', 1400); S(1142, 'Advertisement', 'mono', 'histogram stack', 1700);
  C('670E', 'Correct Bracket Sequence Editor', 'mono', 'linked list + bracket matching', 1700);
  O('vis', 'Visible Pairs', 'mono', 'monotonic stack with equal groups', 1800, 'stack of (height, count)');

  /* ---- backtracking ---- */
  L(22, 'generate-parentheses', 'bt', 'open/close counts (your mid-sem Q4)', 'm'); L(131, 'palindrome-partitioning', 'bt', 'palindrome table + backtracking (your mid-sem Q7)', 'M'); L(132, 'palindrome-partitioning-ii', 'bt', 'the same table, as DP', 'h');
  L(46, 'permutations', 'bt', 'used[] array', 'm'); L(47, 'permutations-ii', 'bt', 'skip equal siblings', 'M'); L(78, 'subsets', 'bt', 'include or exclude', 'm'); L(90, 'subsets-ii', 'bt', 'skip equal siblings', 'M');
  L(39, 'combination-sum', 'bt', 'reuse allowed, prune by remainder', 'm'); L(40, 'combination-sum-ii', 'bt', 'no reuse, skip duplicates', 'M'); L(51, 'n-queens', 'bt', 'column and diagonal sets', 'h');
  L(52, 'n-queens-ii', 'bt', 'count only', 'h'); L(79, 'word-search', 'bt', 'grid DFS with undo', 'm'); L(37, 'sudoku-solver', 'bt', 'most constrained cell first', 'h'); L(93, 'restore-ip-addresses', 'bt', 'cut points', 'm');
  L(17, 'letter-combinations-of-a-phone-number', 'bt', 'product of choices', 'm'); L(698, 'partition-to-k-equal-sum-subsets', 'bt', 'big items first, skip equal fills', 'M'); L(473, 'matchsticks-to-square', 'bt', 'k = 4 buckets', 'M');
  L(1593, 'split-a-string-into-the-max-number-of-unique-substrings', 'bt', 'set of used pieces', 'M'); L(1239, 'maximum-length-of-a-concatenated-string-with-unique-characters', 'bt', 'bitmasks', 'M'); L(140, 'word-break-ii', 'bt', 'memoised backtracking', 'h');
  L(282, 'expression-add-operators', 'bt', 'carry the last term', 'h'); L(494, 'target-sum', 'bt', 'signs; or subset-sum DP', 'm'); L(77, 'combinations', 'bt', 'choose k', 'm'); L(216, 'combination-sum-iii', 'bt', 'fixed size and sum', 'm');
  S(1622, 'Creating Strings', 'bt', 'permutations of a multiset', 1200); S(1623, 'Apple Division', 'bt', 'every subset', 1300); S(1624, 'Chessboard and Queens', 'bt', 'N-Queens with blocked cells', 1400);
  S(1628, 'Meet in the Middle', 'bt', 'two halves of 2^(n/2)', 1900); S(1625, 'Grid Paths', 'bt', 'pruned search', 2000);
  O('tre', 'Split the Treasure', 'bt', 'meet in the middle', 2000, 'two halves of 2^(n/2)');

  /* ---- graphs I ---- */
  C('1829E', 'The Lakes', 'graph', 'grid components with sums', 1100);
  C('755C', 'PolandBall and Forest', 'graph', 'components', 1300);
  C('490B', 'Queue', 'graph', 'linked structure', 1500);
  C('659E', 'New Reform', 'graph', 'components: tree or has a cycle', 1600, 'Per component: if it has a cycle (edges ≥ vertices) every city can get an incoming road; a tree leaves exactly one city out. Count the tree components.');
  C('731C', 'Socks', 'graph', 'DSU / components', 1600, 'Socks worn on one day must share a colour: union them. In each component repaint all but the most common colour.');
  C('723D', 'Lakes in Berland', 'graph', 'grid flood fill', 1600, 'Flood from the border to mark the ocean. The remaining water components are lakes; fill the smallest first until exactly k remain.');
  C('763A', 'Timofey and a tree', 'graph', 'tree DFS', 1600);
  C('1702E', 'Split Into Two Sets', 'graph', 'degree 2 means cycles', 1600, 'Numbers are vertices, dominoes are edges. Every vertex has degree 2, so the graph is a set of cycles; the split exists iff every cycle has even length (a 2-colouring).');
  C('1833E', 'Round Dance', 'graph', 'components: cycles versus paths', 1600, 'People are vertices, remembered neighbours are edges. Components are cycles or paths. Maximum dances = all components; minimum = cycles, plus 1 if any path exists.');
  C('939D', 'Love Rescue', 'graph', 'DSU on letters', 1600);
  C('500B', 'New Year Permutation', 'graph', 'components + sort', 1600, 'Positions that can swap form components: sort the values inside each component into its sorted positions.');
  C('1609D', 'Social Network', 'graph', 'DSU / greedy', 1600);
  C('698B', 'Fix a Tree', 'graph', 'functional graph repair', 1700, 'Find every cycle and any existing root (a[i] = i). Each cycle needs exactly one edge changed; if there is no root, one cycle node becomes it.', 'repair a functional graph: one change per cycle');
  C('1594D', 'The Number of Imposters', 'graph', 'DSU with parity / 2-colouring', 1700, 'Each statement says two people are of the same or opposite type: parity edges. Colour each component and take the larger colour class as imposters.', 'DSU with parity');
  C('659F', 'Polycarp and Hay', 'graph', 'sort + grow components', 2000);
  C('723E', 'One-Way Reform', 'graph', 'Euler orientation', 2200, 'Join the odd-degree vertices through a dummy vertex, then orient the edges along an Euler circuit.', 'Euler circuit through a dummy vertex');
  C('652E', 'Pursuit For Artifacts', 'graph', 'bridge tree', 2300);
  C('732F', 'Tourist Reform', 'graph', 'bridges / 2-edge-connected components', 2300, '', 'bridges: orient each 2-edge-connected part as a cycle');
  C('653E', 'Bear and Forgotten Tree 2', 'graph', 'BFS on the complement graph', 2400, 'Keep a set of unvisited vertices. To explore from u, take every unvisited vertex that is NOT forbidden with u: the complement graph is traversed in O(n + m).', 'BFS on the complement graph');
  S(1192, 'Counting Rooms', 'graph', 'grid components', 1100); S(1666, 'Building Roads', 'graph', 'components', 1100); S(1667, 'Message Route', 'graph', 'BFS with parents', 1200);
  S(1193, 'Labyrinth', 'graph', 'BFS path on a grid', 1300); S(1668, 'Building Teams', 'graph', 'bipartite', 1300); S(1669, 'Round Trip', 'graph', 'cycle in an undirected graph', 1500);
  S(1194, 'Monsters', 'graph', 'multi-source BFS', 1700); S(1751, 'Planets Cycles', 'graph', 'functional graph (your Chakravyuh)', 1700); S(1750, 'Planets Queries I', 'graph', 'binary lifting', 1700);
  S(1160, 'Planets Queries II', 'graph', 'functional graph queries', 2200);
  O('rev', 'Chakravyuh Reversed', 'graph', 'functional graph, constructed from the answers', 1900, 'build the graph from the answers');
  O('odd', 'Odd Walk', 'graph', 'BFS on (vertex, parity)', 1700, 'the node is a state');
  O('fro', 'Frozen Middle', 'graph', 'which positions can never move?', 1700, 'find what is frozen');

  /* ---- graphs II ---- */
  L(743, 'network-delay-time', 'g2', 'Dijkstra', 'm'); L(1514, 'path-with-maximum-probability', 'g2', 'Dijkstra on products', 'm'); L(787, 'cheapest-flights-within-k-stops', 'g2', 'Bellman–Ford rounds', 'M');
  L(1631, 'path-with-minimum-effort', 'g2', 'Dijkstra on the maximum edge', 'M', 1948); L(1334, 'find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance', 'g2', 'Floyd–Warshall', 'M');
  L(207, 'course-schedule', 'g2', 'cycle detection with Kahn', 'm'); L(210, 'course-schedule-ii', 'g2', 'Kahn', 'm'); L(802, 'find-eventual-safe-states', 'g2', 'reverse graph + Kahn', 'M');
  L(1584, 'min-cost-to-connect-all-points', 'g2', 'MST', 'M'); L(684, 'redundant-connection', 'g2', 'DSU', 'm'); L(685, 'redundant-connection-ii', 'g2', 'DSU on a directed graph', 'h');
  L(1202, 'smallest-string-with-swaps', 'g2', 'DSU + sort', 'M'); L(721, 'accounts-merge', 'g2', 'DSU', 'M'); L(399, 'evaluate-division', 'g2', 'weighted graph', 'M');
  L(1976, 'number-of-ways-to-arrive-at-destination', 'g2', 'Dijkstra counting paths', 'M'); L(2290, 'minimum-obstacle-removal-to-reach-corner', 'g2', '0-1 BFS', 'h');
  L(1368, 'minimum-cost-to-make-at-least-one-valid-path-in-a-grid', 'g2', '0-1 BFS', 'h'); L(2092, 'find-all-people-with-secret', 'g2', 'DSU by time', 'h');
  S(1671, 'Shortest Routes I', 'g2', 'Dijkstra', 1400); S(1672, 'Shortest Routes II', 'g2', 'Floyd–Warshall', 1500); S(1679, 'Course Schedule', 'g2', 'Kahn', 1300);
  S(1680, 'Longest Flight Route', 'g2', 'DAG DP', 1500); S(1675, 'Road Reparation', 'g2', 'Kruskal', 1500); S(1195, 'Flight Discount', 'g2', 'Dijkstra on (node, pass used)', 1600);
  S(1673, 'High Score', 'g2', 'Bellman–Ford, positive cycle', 1700); S(1682, 'Flight Routes Check', 'g2', 'strongly connected components', 1700); S(1683, 'Planets and Kingdoms', 'g2', 'strongly connected components', 1800);
  C('722C', 'Destroying Array', 'g2', 'DSU run backwards', 1600, 'Removals are hard for DSU, additions are easy: process the removals in reverse as additions and record the best block each time.', 'run time backwards');
  C('472D', 'Design Tutorial: Inverse the Problem', 'g2', 'rebuild an MST, then verify', 1900, 'Build a minimum spanning tree from the distance matrix, then check every pair: the tree distance must equal the given number.', 'rebuild it, then verify');
  C('733F', 'Drivers Dissatisfaction', 'g2', 'MST modification', 2200);
  C('723F', 'st-Spanning Tree', 'g2', 'DSU / spanning tree with degree limits', 2300);
  C('715B', 'Complete The Graph', 'g2', 'Dijkstra twice', 2300, 'Two Dijkstra runs: the first treats unknown edges as 1 to see if the target length can be reached at all; the second raises unknown edges on the way until the shortest path is exactly L.', 'two Dijkstra runs');
  C('1430G', 'Yet Another DAG Problem', 'g2', 'DAG / topological order / bitmask', 2600);
  C('1368E', 'Ski Accidents', 'g2', 'graphs / DAG / greedy construction', 2500);
  O('free', 'Free Passes', 'g2', 'Dijkstra on (node, passes used)', 1900, 'the node is a state');

  /* ---- DP ---- */
  L(300, 'longest-increasing-subsequence', 'dp', 'LIS with bisect', 'm'); L(72, 'edit-distance', 'dp', 'two strings', 'M'); L(322, 'coin-change', 'dp', 'fewest items', 'm'); L(518, 'coin-change-ii', 'dp', 'combinations: coins outside', 'm');
  L(377, 'combination-sum-iv', 'dp', 'orderings: amount outside', 'm'); L(416, 'partition-equal-subset-sum', 'dp', 'subset sum', 'm'); L(474, 'ones-and-zeroes', 'dp', 'two budgets', 'M'); L(1049, 'last-stone-weight-ii', 'dp', 'subset sum, minimum difference', 'M');
  L(309, 'best-time-to-buy-and-sell-stock-with-cooldown', 'dp', 'states', 'M'); L(188, 'best-time-to-buy-and-sell-stock-iv', 'dp', 'states × k', 'h'); L(139, 'word-break', 'dp', 'prefix DP', 'm'); L(91, 'decode-ways', 'dp', '1D counting', 'm');
  L(516, 'longest-palindromic-subsequence', 'dp', 'interval DP', 'M'); L(354, 'russian-doll-envelopes', 'dp', 'sort + LIS', 'h'); L(673, 'number-of-longest-increasing-subsequence', 'dp', 'LIS with counts', 'M'); L(312, 'burst-balloons', 'dp', 'interval DP', 'h');
  S(1633, 'Dice Combinations', 'dp', 'counting', 1000); S(1634, 'Minimizing Coins', 'dp', 'fewest items', 1200); S(1635, 'Coin Combinations I', 'dp', 'orderings', 1300); S(1636, 'Coin Combinations II', 'dp', 'combinations', 1400);
  S(1637, 'Removing Digits', 'dp', 'greedy-looking DP', 1200); S(1638, 'Grid Paths', 'dp', 'grid DP', 1200); S(1158, 'Book Shop', 'dp', '0/1 knapsack', 1400); S(1639, 'Edit Distance', 'dp', 'two strings', 1500);
  S(1145, 'Increasing Subsequence', 'dp', 'LIS with bisect', 1500); S(1745, 'Money Sums', 'dp', 'subset sum', 1400); S(1746, 'Array Description', 'dp', 'DP over values', 1600); S(1744, 'Rectangle Cutting', 'dp', 'interval DP', 1700);
  S(1093, 'Two Sets II', 'dp', 'counting subset sums', 1800); S(1097, 'Removal Game', 'dp', 'interval game DP', 2000);
  C('1418C', 'Mortal Kombat Tower', 'dp', 'dp over (index, whose turn)', 1500, 'State (boss index, whose turn). Each session kills one or two bosses; the friend pays 1 for every hard boss. Minimise the skips.');
  C('1373D', 'Maximum Sum on Even Positions', 'dp', 'dp / Kadane on gains', 1600, 'Reversing an even-length piece swaps neighbours. Build the gain arrays a[2i+1] − a[2i] and a[2i+1] − a[2i+2]; the best gain is a maximum subarray.');
  C('2027D1', 'The Endspeaker (Easy Version)', 'dp', 'dp / binary search / greedy', 1700);
  C('747D', 'Winter Is Coming', 'dp', 'dp / greedy / sorting', 1800);
  C('733C', 'Epidemic in Monstropolis', 'dp', 'constructive / greedy / two pointers', 1800);
  C('730J', 'Bottles', 'dp', 'knapsack with two goals', 1900, 'First the fewest bottles whose capacities hold all the soda (a capacity knapsack), then, among those choices, the most water you can leave untouched.');
  C('750D', 'New Year and Fireworks', 'dp', 'brute force / simulation with a visited set', 1900);
  C('1431G', 'Number Deletion Game', 'dp', 'dp / games / greedy', 2100);
  C('1373E', 'Sum of Digits', 'dp', 'brute force / dp / greedy', 2200);
  C('500E', 'New Year Domino', 'dp', 'offline queries + dsu / dp', 2300);

  /* ---- greedy ---- */
  L(134, 'gas-station', 'greedy', 'restart when the tank goes negative', 'm'); L(135, 'candy', 'greedy', 'two passes', 'h'); L(455, 'assign-cookies', 'greedy', 'sort + two pointers', 'e'); L(860, 'lemonade-change', 'greedy', 'give back the biggest bill', 'e');
  L(605, 'can-place-flowers', 'greedy', 'scan', 'e'); L(121, 'best-time-to-buy-and-sell-stock', 'greedy', 'minimum so far', 'e'); L(122, 'best-time-to-buy-and-sell-stock-ii', 'greedy', 'sum of rises', 'm');
  S(1629, 'Movie Festival', 'greedy', 'sort by end', 1200); S(1630, 'Tasks and Deadlines', 'greedy', 'shortest first', 1100); S(1084, 'Apartments', 'greedy', 'two pointers after sorting', 1200);
  S(1090, 'Ferris Wheel', 'greedy', 'two pointers after sorting', 1200); S(1073, 'Towers', 'greedy', 'bisect on the tops', 1400);
  C('1431D', 'Used Markers', 'greedy', 'greedy', 1500);
  C('750C', 'New Year and Rating', 'greedy', 'binary search / greedy / math', 1600);
  C('1368D', 'AND, OR and Square Sum', 'greedy', 'bitmasks / greedy', 1700);
  C('732D', 'Exams', 'greedy', 'binary search + greedy check', 1700, 'Binary search the number of days. The check scans backwards, taking each subject’s last possible exam day and counting the free days for preparation.');
  C('1431F', 'Neural Network Problem', 'greedy', 'binary search / greedy', 2100);
  C('732E', 'Sockets', 'greedy', 'greedy / sorting', 2100);
  C('1373F', 'Network Coverage', 'greedy', 'binary search / greedy', 2400);
  C('908F', 'New Year and Rainbow Roads', 'greedy', 'graphs / greedy', 2400);

  /* ---- v4 additions: LeetCode problems for the rebuilt Graphs II, greedy, DP-II, tree DP, hashing and the trie.
          Difficulty letters are estimates (shown with ≈); the slugs were typed from memory and not opened. ---- */
  L(329, 'longest-increasing-path-in-a-matrix', 'g2', 'DAG on the grid: Kahn layers', 'h'); L(1857, 'largest-color-value-in-a-directed-graph', 'g2', 'Kahn + colour counts', 'h');
  L(778, 'swim-in-rising-water', 'g2', 'Dijkstra on the maximum, or binary search + BFS', 'M'); L(1135, 'connecting-cities-with-minimum-cost', 'g2', 'Kruskal', 'M');
  L(1489, 'find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree', 'g2', 'MST: ban or force each edge', 'h'); L(1971, 'find-if-path-exists-in-graph', 'g2', 'BFS or union-find', 'e');
  L(1791, 'find-center-of-star-graph', 'g2', 'degrees', 'e'); L(733, 'flood-fill', 'g2', 'grid DFS', 'e'); L(997, 'find-the-town-judge', 'g2', 'in-degree and out-degree', 'e');
  L(435, 'non-overlapping-intervals', 'greedy', 'sort by end', 'm'); L(452, 'minimum-number-of-arrows-to-burst-balloons', 'greedy', 'sort by right end', 'm'); L(763, 'partition-labels', 'greedy', 'last occurrence', 'm');
  L(55, 'jump-game', 'greedy', 'farthest reach', 'm'); L(45, 'jump-game-ii', 'greedy', 'BFS layers without a queue', 'm');
  L(1143, 'longest-common-subsequence', 'dp', 'two strings: memo, table, one row', 'm'); L(97, 'interleaving-string', 'dp', 'two strings, weave', 'M'); L(115, 'distinct-subsequences', 'dp', 'two strings, counting', 'h');
  L(64, 'minimum-path-sum', 'dp', 'grid, one row', 'm'); L(63, 'unique-paths-ii', 'dp', 'grid with obstacles', 'm'); L(221, 'maximal-square', 'dp', 'grid, reads the diagonal', 'M'); L(174, 'dungeon-game', 'dp', 'grid, fill backwards', 'h');
  L(1035, 'uncrossed-lines', 'dp', 'LCS in disguise', 'm'); L(583, 'delete-operation-for-two-strings', 'dp', 'LCS in disguise', 'm'); L(712, 'minimum-ascii-delete-sum-for-two-strings', 'dp', 'two strings', 'M');
  L(647, 'palindromic-substrings', 'dp', 'expand around the centre', 'm'); L(70, 'climbing-stairs', 'dp', '1-D', 'e');
  L(337, 'house-robber-iii', 'dp', 'tree DP: robbed or skipped', 'M'); L(124, 'binary-tree-maximum-path-sum', 'dp', 'tree DP: one branch up, two at the bend', 'h'); L(543, 'diameter-of-binary-tree', 'dp', 'tree DP: heights', 'e');
  L(208, 'implement-trie-prefix-tree', 'bt', 'trie', 'm'); L(212, 'word-search-ii', 'bt', 'trie + grid DFS', 'h');
  L(146, 'lru-cache', 'arr', 'hash map + doubly linked list', 'M'); L(705, 'design-hashset', 'arr', 'chaining', 'e'); L(706, 'design-hashmap', 'arr', 'chaining', 'e');

  /* ---- more Summit and Ego problems (ratings read from the Codeforces problem list) ---- */
  C('1848D', 'Vika and Bonuses', 'arr', 'binary search / math / ternary search', 2200);
  C('1901E', 'Compressed Tree', 'graph', 'tree DP / greedy / sorting', 2200);
  C('2027D2', 'The Endspeaker (Hard Version)', 'dp', 'dp / binary search / data structures', 2200);
  C('1989E', 'Distance to Different', 'dp', 'combinatorics / dp / math', 2300);
  C('1418E', 'Expected Damage', 'arr', 'binary search / combinatorics / probabilities', 2400);
  C('1845E', 'Boxes and Balls', 'dp', 'dp / math', 2500);
  C('1469F', 'Power Sockets', 'greedy', 'binary search / data structures / greedy', 2600);
  C('1431H', 'Rogue-like Game', 'greedy', 'brute force / greedy / two pointers', 2600);
  C('715C', 'Digit Tree', 'graph', 'trees / divide and conquer / dsu', 2700);
  C('938G', 'Shortest Path Queries', 'g2', 'offline queries / dsu / bitmasks', 2900);
  C('750G', 'New Year and Binary Tree Paths', 'dp', 'bitmasks / combinatorics / dp', 3200);

  /* ---- ratings, tiers, XP ---- */
  const eff = p => p.cf != null ? p.cf : p.lc ? p.lc - 400 : (p.est != null ? p.est : 1300);
  const TIERS = [['Warm-up', 0, 1, 'var(--muted)'], ['Foundation', 1200, 2, 'var(--l-found)'], ['Exam rung', 1400, 4, 'var(--l-trees)'], ['Climb', 1700, 8, 'var(--l-graph)'], ['Summit', 1900, 16, 'var(--l-bt)'], ['Ego', 2400, 32, 'var(--l-exam)']];
  const tierOf = p => { const e = eff(p); let t = 0; TIERS.forEach((x, i) => { if (e >= x[1]) t = i; }); return t; };
  LAD.forEach(p => { p.eff = eff(p); p.tier = tierOf(p); });
  const RANKS = [['Newcomer', 0], ['Apprentice', .03], ['Contestant', .08], ['Specialist', .16], ['Expert', .28], ['Candidate Master', .42], ['Master', .58], ['International Master', .75], ['Grandmaster of ADA', .92]];
  const TOPICS = [['all', 'All'], ['arr', 'Arrays and search'], ['sort', 'Sorting'], ['bst', 'BST'], ['heap', 'Heaps'], ['mono', 'Monotonic stack'], ['bt', 'Backtracking'], ['graph', 'Graphs'], ['g2', 'Graphs II'], ['dp', 'DP'], ['greedy', 'Greedy'], ['vault', 'Vault']];
  const ratingText = p => { const parts = []; if (p.cf) parts.push('CF ' + p.cf); if (p.lc) parts.push('LC ' + p.lc); if (!p.cf) parts.push('≈CF ' + (Math.round(p.eff / 50) * 50)); return parts.join(' · '); };

  function wLadder2(b) {
    const KEY = 'ada-ladder-v2';
    let done = ls2Get(KEY, {}); if (!done || typeof done !== 'object') done = {};
    const oldTicks = ls2Get('ada-cf-ticks', {});
    if (oldTicks && typeof oldTicks === 'object') Object.keys(oldTicks).forEach(k => { const m = k.match(/^(cf|cses)(.+)$/); if (m && seen.has(m[1] + ':' + m[2]) && !done[m[1] + ':' + m[2]]) done[m[1] + ':' + m[2]] = 1; });
    let cur = 'all', tierSel = -1, hide = false, q = '';
    const total = LAD.reduce((s, p) => s + TIERS[p.tier][2], 0);
    const xpOf = () => LAD.reduce((s, p) => s + (done[p.k] ? TIERS[p.tier][2] : 0), 0);
    const rankOf = xp => { let r = 0; RANKS.forEach((x, i) => { if (xp >= x[1] * total) r = i; }); return r; };
    const dayKey = ts => { const d = new Date(ts); return d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate(); };
    function streak() {
      const days = new Set(Object.values(done).filter(v => v > 1e9).map(dayKey)); let n = 0; const d = new Date();
      if (!days.has(dayKey(d))) d.setDate(d.getDate() - 1);
      while (days.has(dayKey(d))) { n++; d.setDate(d.getDate() - 1); }
      return n;
    }
    const head = h('div'), ctl = h('div'), host = h('div'), cap = h('p', { class: 'cap' });
    function paintHead() {
      const xp = xpOf(), r = rankOf(xp), next = RANKS[r + 1], base = RANKS[r][1] * total, top = next ? next[1] * total : total;
      const pct = next ? Math.round((xp - base) / (top - base) * 100) : 100;
      head.innerHTML = '';
      head.append(h('div', { class: 'row' },
        h('div', { class: 'stat' }, 'Rank ', h('b', {}, RANKS[r][0])),
        h('div', { class: 'stat' }, 'XP ', h('b', {}, `${xp} / ${total}`)),
        h('div', { class: 'stat' }, 'Streak ', h('b', {}, streak() + (streak() === 1 ? ' day' : ' days'))),
        h('div', { class: 'stat' }, 'Solved ', h('b', {}, `${LAD.filter(p => done[p.k]).length} / ${LAD.length}`))));
      head.append(h('div', { class: 'xpbar', role: 'img', 'aria-label': next ? `${pct}% of the way to ${next[0]}` : 'Top rank reached' }, h('i', { style: `width:${pct}%` })),
        h('p', { class: 'mini' }, next ? `${Math.ceil(top - xp)} XP to ${next[0]}. XP per solve: ${TIERS.map(t => t[0] + ' ' + t[2]).join(', ')}.` : 'Top rank reached.'));
      const bars = h('div', { class: 'tierbars' });
      TIERS.forEach((t, i) => { const all = LAD.filter(p => p.tier === i), n = all.filter(p => done[p.k]).length; bars.append(h('div', { class: 'tb' }, h('span', { class: 'tbn' }, `${t[0]} `, h('b', {}, `${n}/${all.length}`)), h('span', { class: 'tbar' }, h('i', { style: `width:${all.length ? n / all.length * 100 : 0}%;background:${t[3]}` })))); });
      head.append(bars);
    }
    function view() {
      let list = LAD.filter(p => cur === 'all' ? true : cur === 'vault' ? !!p.v : p.topic === cur);
      if (tierSel >= 0) list = list.filter(p => p.tier === tierSel);
      if (hide) list = list.filter(p => !done[p.k]);
      if (q) list = list.filter(p => (p.t + ' ' + p.pat + ' ' + (p.v || '')).toLowerCase().includes(q));
      return list.slice().sort((a, b) => a.eff - b.eff);
    }
    function paintCtl() {
      ctl.innerHTML = '';
      const tabs = h('div', { class: 'tabs' });
      TOPICS.forEach(([k, n]) => tabs.append(btn(n, () => { cur = k; paintCtl(); paintTable(); }, k === cur ? 'on' : '')));
      const tsel = h('select', { 'aria-label': 'Tier' }, h('option', { value: -1, text: 'All tiers' }), ...TIERS.map((t, i) => h('option', { value: i, text: `${t[0]} (${t[1] ? t[1] + '+' : 'below 1200'})`, selected: i === tierSel })));
      tsel.addEventListener('change', () => { tierSel = +tsel.value; paintTable(); });
      const qin = h('input', { type: 'search', placeholder: 'Filter: pattern, title…', value: q, 'aria-label': 'Filter' });
      qin.addEventListener('input', () => { q = qin.value.trim().toLowerCase(); paintTable(); });
      const hid = h('input', { type: 'checkbox' }); hid.checked = hide; hid.addEventListener('change', () => { hide = hid.checked; paintTable(); });
      ctl.append(tabs, h('div', { class: 'row' }, h('label', {}, 'Tier: ', tsel), qin, h('label', {}, hid, ' hide solved'), btn('Surprise me', surprise, 'pri')));
    }
    function surprise() {
      const pool = view().filter(p => !done[p.k]).slice(0, 6);
      if (!pool.length) { cap.textContent = 'Nothing unsolved in this view. Widen the filter or move up a tier.'; cap.className = 'cap good'; return; }
      const p = pool[Math.floor(Math.random() * pool.length)];
      cap.textContent = `Next: ${p.t} (${TIERS[p.tier][0]}, ${ratingText(p)}). Tick it only after it is accepted without reading a solution.`; cap.className = 'cap';
      if (!p.orig) window.open(p.u, '_blank', 'noopener'); else location.hash = p.u.slice(1);
    }
    function paintTable() {
      const list = view();
      const t = h('table', {}, h('tr', {}, h('th', {}, '✓'), h('th', {}, 'Tier'), h('th', {}, 'Rating'), h('th', {}, 'Problem'), h('th', {}, cur === 'vault' ? 'The trick' : 'Pattern'), h('th', {}, 'Hint')));
      list.forEach(p => {
        const cb = h('input', { type: 'checkbox', 'aria-label': 'Solved ' + p.t }); cb.checked = !!done[p.k];
        cb.addEventListener('change', () => {
          const before = rankOf(xpOf());
          if (cb.checked) done[p.k] = Date.now(); else delete done[p.k];
          ls2Set(KEY, done); window.dispatchEvent(new Event('ada-ladder-change'));
          const xp = xpOf(), after = rankOf(xp), gain = TIERS[p.tier][2];
          cap.textContent = cb.checked ? `+${gain} XP · ${TIERS[p.tier][0]} cleared.` + (after > before ? ` Rank up: ${RANKS[after][0]}.` : '') : `Unticked: −${gain} XP.`;
          cap.className = 'cap' + (cb.checked ? ' good' : '');
          paintHead(); if (hide) paintTable();
        });
        const hint = h('span', { class: 'mini', hidden: true }, p.h || ''); let hb = null;
        if (p.h) { hb = btn('Hint', () => { hint.hidden = !hint.hidden; hb.textContent = hint.hidden ? 'Hint' : 'Hide'; }); hb.style.cssText = 'font-size:13px;padding:2px 8px'; }
        const link = p.orig ? h('a', { href: p.u }, p.t) : h('a', { href: p.u, target: '_blank', rel: 'noopener' }, p.t);
        t.append(h('tr', { style: `border-left:4px solid ${TIERS[p.tier][3]}` },
          h('td', {}, cb), h('td', {}, TIERS[p.tier][0]), h('td', { class: 'n' }, ratingText(p)), h('td', {}, link, p.src === 'CF' || p.src === 'LC' ? '' : h('span', { class: 'mini' }, '  ' + p.src)),
          h('td', {}, cur === 'vault' ? (p.v || p.pat) : p.pat), h('td', {}, hb, hint)));
      });
      host.innerHTML = '';
      host.append(h('p', { class: 'mini' }, `${list.length} problem${list.length === 1 ? '' : 's'}, easiest first.`), h('div', { class: 'tw' }, t));
    }
    window.addEventListener('ada-ladder-change', () => { done = ls2Get(KEY, {}); });
    b.append(head, ctl, cap, host, h('p', { class: 'mini' }, 'CF = Codeforces rating, each one read from the Codeforces problem list. LC = community rating of LeetCode contest problems. ≈CF is an estimate: LC rating − 400 for rated LeetCode problems, my judgement for unrated classics and CSES tasks. Ticks and the streak are saved in this browser.'));
    paintHead(); paintCtl(); paintTable();
    cap.textContent = 'Pick a tab, pick a tier, or press Surprise me for something at the easy end of the current view.';
  }

  /* ---- three-rung mocks with subtask scoring ---- */
  const MOCKS3 = {
    'Exam M1 (1400 / 1500 / 1600)': ['2104D', '1431D', '659E'], 'Exam M2': ['2132C2', '1418C', '722C'], 'Exam M3': ['1431B', '490B', '1702E'],
    'Exam M4': ['2104D', '1418C', '731C'], 'Exam M5': ['2132C2', '1431D', '1833E'], 'Exam M6': ['1431B', '1418C', '1373D'],
    'Summit S1 (1700 / 1900 / 2100)': ['698B', '472D', '1431G'], 'Summit S2': ['1594D', '730J', '1418D'], 'Summit S3': ['732D', '750D', '732E'],
    'Ego X1 (1900 / 2300 / 2500)': ['472D', '715B', '1368E'], 'Ego X2': ['730J', '723F', '1430G']
  };
  function wMock3(b) {
    const KEY = 'ada-mock3';
    let st = ls2Get(KEY, null);
    if (!st || typeof st !== 'object' || !MOCKS3[st.pick]) st = { pick: Object.keys(MOCKS3)[0], len: 90, left: null, running: false, at: 0, res: {} };
    st.res = st.res || {};
    const byKey = id => LAD.find(p => p.k === 'cf:' + id);
    const sel = h('select', { 'aria-label': 'Mock' }, ...Object.keys(MOCKS3).map(k => h('option', { value: k, text: k, selected: k === st.pick })));
    const lenSel = h('select', { 'aria-label': 'Length' }, ...[60, 75, 90, 120].map(m => h('option', { value: m, text: m + ' minutes', selected: m === st.len })));
    const clock = h('div', { style: 'font-family:var(--f-mono);font-size:34px;font-weight:700' }), list = h('div'), cap = h('p', { class: 'cap' });
    const startBtn = btn('Start', () => toggle(), 'pri');
    let tick = null;
    const save = () => ls2Set(KEY, st);
    const remaining = () => st.left === null ? st.len * 60 : st.running ? Math.max(0, st.left - (Date.now() - st.at) / 1000) : st.left;
    const fmt = s => { s = Math.ceil(s); return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`; };
    function paintClock() {
      const r = remaining(); clock.textContent = fmt(r);
      clock.style.color = r <= 0 ? 'var(--bad)' : r < 600 ? 'var(--warn)' : 'var(--ink)';
      startBtn.textContent = st.running ? 'Pause' : st.left === null ? 'Start' : r <= 0 ? 'Time is up' : 'Resume';
      startBtn.disabled = r <= 0;
      if (r <= 0 && st.running) { st.running = false; st.left = 0; save(); clearInterval(tick); tick = null; score(); }
    }
    function toggle() {
      if (st.running) { st.left = remaining(); st.running = false; clearInterval(tick); tick = null; }
      else { if (st.left === null) st.left = st.len * 60; st.at = Date.now(); st.running = true; tick = setInterval(paintClock, 500); }
      save(); paintClock();
    }
    const LV = [['0', 'Nothing yet'], ['1', 'Brute force passed some tests'], ['2', 'Fully accepted']];
    function paint() {
      const ids = MOCKS3[st.pick], res = st.res[st.pick] || {};
      const t = h('table', {}, h('tr', {}, h('th', {}, 'Rung'), h('th', {}, 'Rating'), h('th', {}, 'Problem'), h('th', {}, 'Topic'), h('th', {}, 'Result')));
      ids.forEach((id, i) => {
        const p = byKey(id);
        const s = h('select', { 'aria-label': 'Result for ' + id }, ...LV.map(([v, l]) => h('option', { value: v, text: l, selected: String(res[id] || 0) === v })));
        s.addEventListener('change', () => { st.res[st.pick] = st.res[st.pick] || {}; st.res[st.pick][id] = +s.value; save(); score(); });
        t.append(h('tr', {}, h('td', {}, 'Q' + (i + 1)), h('td', { class: 'n' }, 'CF ' + p.cf), h('td', {}, h('a', { href: p.u, target: '_blank', rel: 'noopener' }, p.t.replace(/^CF /, ''))), h('td', {}, p.pat), h('td', {}, s)));
      });
      list.innerHTML = ''; list.append(h('div', { class: 'tw' }, t)); score(); paintClock();
    }
    function score() {
      const ids = MOCKS3[st.pick], res = st.res[st.pick] || {};
      const full = ids.filter(id => res[id] === 2).length, zero = ids.filter(id => !res[id]).length;
      if (!ids.some(id => res[id]) && st.left !== 0) { cap.textContent = 'Open all three problems, then press Start. The timer keeps running if you reload this page.'; cap.className = 'cap'; return; }
      cap.textContent = `${full} of 3 fully accepted, ${3 - full - zero} with partial marks, ${zero} at zero.` + (zero === 0 ? ' Nothing left at zero: that is the habit the end-sem rewards.' : ' Every zero is a problem where a brute force was the missing step: write one for it now, untimed.');
      cap.className = 'cap' + (zero === 0 ? ' good' : '');
    }
    function reset() { clearInterval(tick); tick = null; st.left = null; st.running = false; st.res[st.pick] = {}; save(); paint(); }
    sel.addEventListener('change', () => { if (st.running) toggle(); st.pick = sel.value; st.left = null; save(); paint(); });
    lenSel.addEventListener('change', () => { st.len = +lenSel.value; if (!st.running) st.left = null; save(); paintClock(); });
    b.append(h('div', { class: 'row' }, h('label', {}, 'Mock: ', sel), h('label', {}, 'Length: ', lenSel)), h('div', { class: 'row' }, clock, startBtn, btn('Reset', reset)), list, cap);
    paint();
    if (st.running) tick = setInterval(paintClock, 500);
  }
  Object.assign(WIDGETS, { ladder2: wLadder2, mock3: wMock3 });

  /* ---- monotonic stack quiz and naming ---- */
  QUIZ.m13 = [
    { q: 'Next STRICTLY greater element. Which loop condition is right?', o: ['while st and a[st[-1]] < x', 'while st and a[st[-1]] <= x', 'if st and a[st[-1]] < x', 'while st and a[st[-1]] > x'], a: 0, why: 'Pop everything that x beats, and equal values stay: x is not strictly greater than them. It must be a while loop, because one new value can answer many waiting elements.' },
    { q: 'A monotonic stack handles n elements in…', o: ['O(n²) in the worst case', 'O(n) amortised: each element is pushed once and popped once', 'O(n log n) because of the stack', 'O(n) only if the array is sorted'], a: 1, why: 'The while loop inside the for loop looks quadratic, but every pop removes something pushed earlier: at most n pops in total.' },
    { q: 'Sum of subarray minimums with repeated values. Why is one side strict and the other not?', o: ['Python’s sort is stable', 'So a subarray with equal minimums is credited to exactly one element', 'To save memory', 'It is arbitrary'], a: 1, why: 'If both sides stopped only at strictly smaller values, a subarray with two equal minimums would be counted for both. Making one side stop at equal values assigns it to exactly one.' },
    { q: 'Sliding window maximum with a deque of indices. When do you pop from the front?', o: ['When the front value is the smallest', 'When the front index is at most i − k (it left the window)', 'Every iteration', 'When the new value is bigger'], a: 1, why: 'The back is trimmed by value; the front expires by position. The front is always the maximum of the current window.' },
    { q: 'Daily Temperatures for [73, 74, 75, 71, 69, 72, 76, 73]: days to wait for a warmer day?', o: ['[1, 1, 4, 2, 1, 1, 0, 0]', '[1, 1, 1, 1, 1, 1, 0, 0]', '[1, 1, 4, 2, 1, 1, 0, 1]', '[2, 2, 4, 2, 1, 1, 0, 0]'], a: 0, why: '75 waits 4 days for 76; 71 waits 2 days for 72; 76 and the last 73 never see a warmer day.' }
  ];
  Object.assign(TOPIC_NAMES, { c1: 'Contest toolkit', c2: 'Graph patterns', c3: 'DP patterns', c4: 'Greedy', e0: 'Functional graphs', e1: 'Contest routine', e2: 'Knapsack family', e3: 'Graphs II', m13: 'Monotonic stacks' });
  window.SECMAP = { c1: 'ch14', c2: 'ch8', c3: 'ch10', c4: 'ch11', e0: 'ch8', e1: 'ch14', e2: 'ch10', e3: 'ch12', m13: 'ch13' };
})();
