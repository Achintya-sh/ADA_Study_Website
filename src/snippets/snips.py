#@@ merge_intervals
def merge_intervals(intervals):           # sort by start, then one pass
    intervals.sort()
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:       # touches or overlaps the last block
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out

#@@ largest_number
from functools import cmp_to_key

def largest_number(nums):                 # LC 179: which order gives the biggest number?
    def cmp(a, b):                        # a goes first if a+b beats b+a as text
        return -1 if a + b > b + a else (1 if a + b < b + a else 0)
    s = sorted(map(str, nums), key=cmp_to_key(cmp))
    r = "".join(s)
    return "0" if r[0] == "0" else r

#@@ quickselect
import random

def quickselect(a, k):                    # k-th smallest (0-based), expected O(n)
    a = a[:]
    lo, hi = 0, len(a) - 1
    while lo < hi:
        p = a[random.randint(lo, hi)]
        lt, i, gt = lo, lo, hi            # < p | == p | > p, the Dutch flag
        while i <= gt:
            if a[i] < p:
                a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] > p:
                a[i], a[gt] = a[gt], a[i]; gt -= 1
            else:
                i += 1
        if k < lt:
            hi = lt - 1                   # the answer is in the "< p" part
        elif k > gt:
            lo = gt + 1                   # ... or in the "> p" part
        else:
            return p                      # ... or it is p itself
    return a[lo]

#@@ count_inversions
def count_inversions(a):                  # pairs i < j with a[i] > a[j], via merge sort
    def go(a):
        if len(a) <= 1:
            return a, 0
        m = len(a) // 2
        L, x = go(a[:m])
        R, y = go(a[m:])
        out, i, j, c = [], 0, 0, x + y
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                out.append(L[i]); i += 1
            else:
                out.append(R[j]); j += 1
                c += len(L) - i           # R[j] jumps over every remaining element of L
        out += L[i:] + R[j:]
        return out, c
    return go(a)[1]

#@@ quick_sort_safe
import random

def quick_sort_desc(a):                   # Contest 1 Q5: survives reverse-sorted and all-equal input
    stack = [(0, len(a) - 1)]             # explicit stack: no recursion limit problems
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        p = a[random.randint(lo, hi)]     # random pivot: no input is "always bad"
        lt, i, gt = lo, lo, hi            # three zones: bigger | equal | smaller
        while i <= gt:
            if a[i] > p:
                a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] < p:
                a[i], a[gt] = a[gt], a[i]; gt -= 1
            else:
                i += 1
        stack.append((lo, lt - 1))        # the equal zone is finished: skip it
        stack.append((gt + 1, hi))

#@@ bst_validate
class Node:
    def __init__(self, value):
        self.value = value
        self.left = self.right = None

def is_bst_wrong(node):                   # the Contest 1 Q4 trap: compares only with the parent
    if node is None:
        return True
    if node.left and node.left.value >= node.value:
        return False
    if node.right and node.right.value <= node.value:
        return False
    return is_bst_wrong(node.left) and is_bst_wrong(node.right)

def is_bst(node, low=float('-inf'), high=float('inf')):
    if node is None:
        return True
    if not (low < node.value < high):     # every ancestor sets a bound, not just the parent
        return False
    return is_bst(node.left, low, node.value) and is_bst(node.right, node.value, high)

#@@ bst_pre
def bst_from_preorder(pre):               # LC 1008, O(n): each value must stay below a bound
    i = 0
    def build(bound):
        nonlocal i
        if i == len(pre) or pre[i] > bound:
            return None
        node = Node(pre[i]); i += 1
        node.left = build(node.value)     # left subtree: values below this node
        node.right = build(bound)         # right subtree: values below the inherited bound
        return node
    return build(float('inf'))

#@@ bst_recover
def swapped_pair(root):                   # LC 99: two values were swapped; one inorder walk finds them
    first = second = prev = None
    stack, node = [], root
    while stack or node:
        while node:
            stack.append(node); node = node.left
        node = stack.pop()
        if prev and prev.value > node.value:      # a descent in what should be sorted
            if first is None:
                first = prev                      # first descent: its bigger value is misplaced
            second = node                         # last descent: its smaller value is misplaced
        prev, node = node, node.right
    return first.value, second.value

#@@ bisect_bst
from bisect import bisect_left, bisect_right, insort

def floor_(a, x):                         # largest element <= x in a sorted list, or None
    i = bisect_right(a, x)
    return a[i - 1] if i else None

def ceiling(a, x):                        # smallest element >= x, or None
    i = bisect_left(a, x)
    return a[i] if i < len(a) else None

#@@ min_heap_manual
class MinHeap:                            # Contest 1 Q3: heapq is not allowed
    def __init__(self):
        self.a = []
    def push(self, x):                    # O(log n): add at the end, bubble up
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0:
            p = (i - 1) // 2
            if a[p] <= a[i]:
                break
            a[p], a[i] = a[i], a[p]
            i = p
    def pop(self):                        # O(log n): last item to the root, sift down
        a = self.a
        top, last = a[0], a.pop()
        if a:
            a[0] = last
            i, n = 0, len(a)
            while True:
                l, r, m = 2 * i + 1, 2 * i + 2, i
                if l < n and a[l] < a[m]: m = l
                if r < n and a[r] < a[m]: m = r
                if m == i:
                    break
                a[i], a[m] = a[m], a[i]
                i = m
        return top

#@@ kway
import heapq

def merge_k(lists):                       # k sorted lists -> one sorted list, O(N log k)
    heap = [(l[0], i, 0) for i, l in enumerate(lists) if l]
    heapq.heapify(heap)
    out = []
    while heap:
        v, i, j = heapq.heappop(heap)
        out.append(v)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out

#@@ lazy_heap
import heapq
from collections import Counter

class LazyHeap:                           # min-heap with remove(x): mark it dead, clean when it reaches the top
    def __init__(self):
        self.h, self.dead = [], Counter()
    def push(self, x):
        heapq.heappush(self.h, x)
    def remove(self, x):                  # x must be in the heap
        self.dead[x] += 1
    def _clean(self):
        while self.h and self.dead[self.h[0]]:
            self.dead[self.h[0]] -= 1
            heapq.heappop(self.h)
    def top(self):
        self._clean()
        return self.h[0]
    def pop(self):
        self._clean()
        return heapq.heappop(self.h)

#@@ min_rooms
import heapq

def min_rooms(intervals):                 # LC 253: fewest rooms so no two meetings overlap
    heap = []                             # end times of rooms in use
    for s, e in sorted(intervals):
        if heap and heap[0] <= s:
            heapq.heapreplace(heap, e)    # the earliest-ending room is free: reuse it
        else:
            heapq.heappush(heap, e)       # otherwise open a new room
    return len(heap)

#@@ ipo
import heapq

def find_max_capital(k, w, profits, capital):     # LC 502: at most k projects, capital grows
    projects = sorted(zip(capital, profits))
    heap, i = [], 0                       # heap: profits of projects we can afford
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(heap, -projects[i][1]); i += 1
        if not heap:
            break
        w -= heapq.heappop(heap)          # take the most profitable affordable project
    return w

#@@ next_greater
def next_greater(a):                      # index of the next strictly greater element, or -1
    res, st = [-1] * len(a), []           # st: indices whose answer is still unknown
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = i             # x is the first bigger value to the right of st[-1]
        st.append(i)
    return res

#@@ histogram
def largest_rectangle(h):                 # LC 84
    st, best = [], 0                      # st: indices with increasing heights
    for i, x in enumerate(h + [0]):       # the sentinel 0 flushes the stack
        while st and h[st[-1]] >= x:
            height = h[st.pop()]
            left = st[-1] if st else -1   # the bar is the shortest between left and i
            best = max(best, height * (i - left - 1))
        st.append(i)
    return best

#@@ sum_mins
def sum_subarray_mins(a):                 # LC 907: contribution of each element as the minimum
    n = len(a)
    left, right, st = [0] * n, [0] * n, []
    for i in range(n):                    # distance back to the previous STRICTLY smaller element
        while st and a[st[-1]] >= a[i]:
            st.pop()
        left[i] = i - (st[-1] if st else -1)
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):        # distance forward to the next smaller-or-EQUAL element
        while st and a[st[-1]] > a[i]:
            st.pop()
        right[i] = (st[-1] if st else n) - i
        st.append(i)
    return sum(a[i] * left[i] * right[i] for i in range(n))

#@@ remove_k
def remove_k_digits(num, k):              # LC 402: smallest number after deleting k digits
    st = []
    for ch in num:
        while k and st and st[-1] > ch:   # a bigger digit before a smaller one: delete it
            st.pop(); k -= 1
        st.append(ch)
    if k:
        st = st[:-k]                      # still deleting: take them from the end
    return "".join(st).lstrip("0") or "0"

#@@ sliding_max
from collections import deque

def sliding_max(a, k):                    # LC 239: maximum of every window of size k
    dq, out = deque(), []                 # dq: indices, values decreasing
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()                      # smaller values can never be a window maximum again
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()                  # the front slid out of the window
        if i >= k - 1:
            out.append(a[dq[0]])
    return out

#@@ trap
def trap(h):                              # LC 42: rain water, two pointers
    lo, hi, lmax, rmax, water = 0, len(h) - 1, 0, 0, 0
    while lo < hi:
        if h[lo] < h[hi]:                 # the lower side decides: the other side is at least as tall
            lmax = max(lmax, h[lo]); water += lmax - h[lo]; lo += 1
        else:
            rmax = max(rmax, h[hi]); water += rmax - h[hi]; hi -= 1
    return water

#@@ visible_pairs
def visible_pairs(a):                     # pairs i < j with every element between them <= min(a[i], a[j])
    st, ans = [], 0                       # st: (value, how many equal), values strictly decreasing
    for x in a:
        cnt = 1
        while st and st[-1][0] < x:
            ans += st.pop()[1]            # each smaller person on the stack sees x
        if st and st[-1][0] == x:
            c = st.pop()[1]
            ans += c                      # x sees every equal person too
            cnt = c + 1
            if st:
                ans += 1                  # ... and the first taller one behind them
        elif st:
            ans += 1                      # the taller person on top of the stack
        st.append((x, cnt))
    return ans

#@@ permute_unique
def permute_unique(nums):                 # LC 47: no repeated permutations
    nums.sort()
    res, cur, used = [], [], [False] * len(nums)
    def go():
        if len(cur) == len(nums):
            res.append(cur[:]); return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i and nums[i] == nums[i - 1] and not used[i - 1]:
                continue                  # same value as the sibling branch we just finished
            used[i] = True; cur.append(nums[i])
            go()
            cur.pop(); used[i] = False
    go()
    return res

#@@ subsets_dup
def subsets_dup(nums):                    # LC 90
    nums.sort()
    res, cur = [], []
    def go(start):
        res.append(cur[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue                  # skip an equal sibling at the same depth
            cur.append(nums[i]); go(i + 1); cur.pop()
    go(0)
    return res

#@@ pal_part
def palindrome_partitions(s):             # mid-sem Q7 / LC 131
    n = len(s)
    pal = [[False] * n for _ in range(n)] # pal[i][j]: is s[i..j] a palindrome?
    for i in range(n - 1, -1, -1):        # pal[i][j] needs pal[i+1][j-1]: fill i downward
        for j in range(i, n):
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
    res, cur = [], []
    def go(i):
        if i == n:
            res.append(cur[:]); return
        for j in range(i, n):
            if pal[i][j]:                 # cut only where the piece is a palindrome: prunes dead branches
                cur.append(s[i:j + 1]); go(j + 1); cur.pop()
    go(0)
    return res

def min_cuts(s):                          # LC 132: same table, DP instead of listing everything
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
    cuts = [0] * n                        # cuts[j]: fewest cuts for the prefix s[0..j]
    for j in range(n):
        cuts[j] = 0 if pal[0][j] else min(cuts[i - 1] + 1 for i in range(1, j + 1) if pal[i][j])
    return cuts[-1]

#@@ partition_k
def can_partition_k(nums, k):             # LC 698: k buckets with equal sums
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    nums.sort(reverse=True)               # big items first: dead ends show up early
    if nums[0] > target:
        return False
    buckets = [0] * k
    def go(i):
        if i == len(nums):
            return True
        seen = set()
        for b in range(k):
            if buckets[b] + nums[i] > target or buckets[b] in seen:
                continue                  # two buckets with the same fill are the same situation
            seen.add(buckets[b])
            buckets[b] += nums[i]
            if go(i + 1):
                return True
            buckets[b] -= nums[i]
        return False
    return go(0)

#@@ mitm
from collections import Counter

def count_subsets(a, T):                  # subsets with sum exactly T, n up to about 40
    def sums(part):
        res = [0]
        for x in part:
            res += [s + x for s in res]   # every old sum, with and without x
        return res
    mid = len(a) // 2
    left = Counter(sums(a[:mid]))         # 2^(n/2) sums instead of 2^n
    return sum(left[T - s] for s in sums(a[mid:]))

#@@ chak
def chak_brute(a):                        # subtask 1 (n <= 10^3): walk from every node
    ans = []
    for v in range(len(a)):
        seen, u = set(), v
        while u != -1 and u not in seen:
            seen.add(u)
            u = a[u]
        ans.append(len(seen))
    return ans

def chak_solve(a):                        # O(n), no recursion
    n = len(a)
    ans = [0] * n
    state = [0] * n                       # 0 new, 1 on the current walk, 2 finished
    for s in range(n):
        if state[s]:
            continue
        path, u = [], s
        while u != -1 and state[u] == 0:
            state[u] = 1
            path.append(u)
            u = a[u]
        if u != -1 and state[u] == 1:     # walked into our own path: a new cycle
            k = path.index(u)
            for x in path[k:]:
                ans[x] = len(path) - k
                state[x] = 2
            path = path[:k]               # what is left is the tail
        nxt = 0 if u == -1 else ans[u]    # what the end of the tail already knows
        for x in reversed(path):          # unwind the tail backwards
            nxt += 1
            ans[x] = nxt
            state[x] = 2
    return ans

#@@ chak_peel
from collections import deque

def chak_peel(a):                         # the same answer by peeling in-degree-0 nodes
    n = len(a)
    indeg = [0] * n
    for x in a:
        if x != -1:
            indeg[x] += 1
    q = deque(u for u in range(n) if indeg[u] == 0)
    peeled = []
    while q:
        u = q.popleft()
        peeled.append(u)
        if a[u] != -1:
            indeg[a[u]] -= 1
            if indeg[a[u]] == 0:
                q.append(a[u])
    ans = [0] * n
    for s in range(n):                    # survivors lie on cycles: measure each cycle once
        if indeg[s] > 0 and ans[s] == 0:
            cyc, u = [s], a[s]
            while u != s:
                cyc.append(u)
                u = a[u]
            for x in cyc:
                ans[x] = len(cyc)
    for u in reversed(peeled):            # a[u] was peeled after u, so its answer is known
        ans[u] = 1 if a[u] == -1 else 1 + ans[a[u]]
    return ans

#@@ floyd
def rho(a, s):                            # Floyd: (tail length, cycle length) from s; every node has a[i] != -1
    slow, fast = a[s], a[a[s]]
    while slow != fast:                   # the hare laps the tortoise inside the cycle
        slow, fast = a[slow], a[a[fast]]
    lam, fast = 1, a[slow]                # measure the cycle
    while fast != slow:
        fast = a[fast]; lam += 1
    mu, slow, fast = 0, s, s              # find where the cycle starts
    for _ in range(lam):
        fast = a[fast]
    while slow != fast:
        slow, fast = a[slow], a[fast]; mu += 1
    return mu, lam

#@@ binary_lifting
def build_jump(a, LOG=20):                # a[i]: the single successor of i
    up = [a[:]]
    for _ in range(LOG - 1):
        prev = up[-1]
        up.append([prev[x] for x in prev])    # 2^b steps = two jumps of 2^(b-1)
    return up

def kth_successor(up, v, k):              # k < 2^LOG: O(log k) per query
    for b in range(len(up)):
        if k >> b & 1:
            v = up[b][v]
    return v

#@@ rev_chak
def reverse_chak(c):                      # given c[i] = nodes reachable from i, build a (or None)
    n = len(c)
    first = {}                            # a node holding each value, for tails to attach to
    members = {}
    for i, v in enumerate(c):
        members.setdefault(v, []).append(i)
        first.setdefault(v, i)
    a = [-1] * n
    for v, idx in members.items():
        if v == 1:
            continue                      # dead ends: a[i] = -1
        if v - 1 in first:
            for i in idx:
                a[i] = first[v - 1]       # a tail: one step before a node that reaches v - 1
        elif len(idx) % v == 0:
            for g in range(0, len(idx), v):   # no v-1 anywhere: they must form cycles of length v
                grp = idx[g:g + v]
                for t in range(v):
                    a[grp[t]] = grp[(t + 1) % v]
        else:
            return None
    return a

#@@ is_bip
from collections import deque

def two_colour(n, edges):                 # None if an odd cycle exists
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    colour = [-1] * n
    for s in range(n):
        if colour[s] != -1:
            continue
        colour[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if colour[v] == -1:
                    colour[v] = colour[u] ^ 1; q.append(v)
                elif colour[v] == colour[u]:
                    return None           # an edge inside one colour: odd cycle
    return colour

#@@ odd_walk
from collections import deque

def shortest_odd_walk(n, edges, s, t):    # fewest edges in a walk (repeats allowed) of odd length
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    dist = [[-1, -1] for _ in range(n)]   # dist[v][p]: fewest edges to reach v with parity p
    dist[s][0] = 0
    q = deque([(s, 0)])
    while q:
        u, p = q.popleft()
        for v in adj[u]:
            if dist[v][p ^ 1] == -1:
                dist[v][p ^ 1] = dist[u][p] + 1
                q.append((v, p ^ 1))
    return dist[t][1]                     # -1 if no odd walk exists

#@@ topo
from collections import deque

def topo_order(n, edges):                 # Kahn: edges (u, v) mean u before v
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(u for u in range(n) if indeg[u] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:             # its last prerequisite is done
                q.append(v)
    return order if len(order) == n else None     # None: a cycle

def longest_path_dag(n, edges):           # most edges on any path
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    best = [0] * n
    for u in topo_order(n, edges):        # u is final before its out-edges are used
        for v in adj[u]:
            best[v] = max(best[v], best[u] + 1)
    return max(best)

#@@ dijkstra
import heapq

def dijkstra(n, edges, src):              # edges (u, v, w), w >= 0, directed; returns dist and parent
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist, par = [INF] * n, [-1] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                   # stale pair: u was already finished with a smaller d
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:           # relax
                dist[v], par[v] = d + w, u
                heapq.heappush(heap, (dist[v], v))
    return dist, par

def path_to(par, t):                      # follow parents backwards
    out = []
    while t != -1:
        out.append(t); t = par[t]
    return out[::-1]

#@@ zero_one
from collections import deque

def zero_one_bfs(n, edges, s):            # every weight is 0 or 1: a deque replaces the heap, O(V + E)
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    dq = deque([s])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)      # free edge: same level, go first
                else:
                    dq.append(v)
    return dist

#@@ free_edges
import heapq

def min_cost_k_free(n, edges, s, t, k):   # up to k edges on the path cost nothing (CSES Flight Discount)
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [[INF] * (k + 1) for _ in range(n)]     # state = (node, free edges used)
    dist[s][0] = 0
    heap = [(0, s, 0)]
    while heap:
        d, u, j = heapq.heappop(heap)
        if d > dist[u][j]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v][j]:
                dist[v][j] = d + w
                heapq.heappush(heap, (d + w, v, j))
            if j < k and d < dist[v][j + 1]:       # use a free pass on this edge
                dist[v][j + 1] = d
                heapq.heappush(heap, (d, v, j + 1))
    return min(dist[t])

#@@ bellman
def bellman_ford(n, edges, s):            # handles negative edges; None if a negative cycle is reachable
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:                 # one more pass: any improvement means a negative cycle
        if dist[u] + w < dist[v]:
            return None
    return dist

def floyd_warshall(n, edges):             # all pairs, O(n^3): only for n up to a few hundred
    INF = float('inf')
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):                    # allow k as an intermediate stop, one k at a time
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d

#@@ dsu
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False                  # already connected: this edge would close a cycle
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

def kruskal(n, edges):                    # edges (w, u, v), undirected
    dsu, total, used = DSU(n), 0, 0
    for w, u, v in sorted(edges):         # lightest first
        if dsu.union(u, v):
            total += w
            used += 1
    return total if used == n - 1 else None       # None: disconnected

#@@ dsu_reverse
def best_after_removals(a, order):        # CF 722C: remove a[order[0]], a[order[1]], ...; best block sum after each
    n = len(a)
    dsu = DSU(n)
    tot, alive = a[:], [False] * n        # tot[root]: sum of its block
    ans, best = [0] * n, 0
    for step in range(n - 1, -1, -1):     # run time backwards: removals become additions
        ans[step] = best                  # the answer AFTER removal `step` is the state before adding it back
        i = order[step]
        alive[i] = True
        for j in (i - 1, i + 1):
            if 0 <= j < n and alive[j]:
                ri, rj = dsu.find(i), dsu.find(j)
                if ri != rj:
                    dsu.union(ri, rj)
                    r = dsu.find(ri)
                    tot[r] = tot[ri] + tot[rj]
        best = max(best, tot[dsu.find(i)])
    return ans

#@@ knap
def knap01(w, v, W):                      # each item at most once: capacity DOWNWARD
    dp = [0] * (W + 1)
    for wi, vi in zip(w, v):
        for c in range(W, wi - 1, -1):
            dp[c] = max(dp[c], dp[c - wi] + vi)
    return dp[W]

def unbounded(w, v, W):                   # any number of copies: capacity UPWARD
    dp = [0] * (W + 1)
    for wi, vi in zip(w, v):
        for c in range(wi, W + 1):
            dp[c] = max(dp[c], dp[c - wi] + vi)
    return dp[W]

def knap012(w, v, W):                     # Contest 2 Q4: each item 0, 1 or 2 times
    dp = [0] * (W + 1)
    for wi, vi in zip(w, v):
        for c in range(W, wi - 1, -1):    # downward: dp[c - wi], dp[c - 2wi] are still "before this item"
            dp[c] = max(dp[c], dp[c - wi] + vi)
            if c >= 2 * wi:
                dp[c] = max(dp[c], dp[c - 2 * wi] + 2 * vi)
    return dp[W]

#@@ knap_more
def can_make(nums, T):                    # subset sum, each number once
    ok = [True] + [False] * T
    for x in nums:
        for t in range(T, x - 1, -1):
            ok[t] = ok[t] or ok[t - x]
    return ok[T]

def combos(coins, amount):                # LC 518: {1,2} and {2,1} count once
    ways = [1] + [0] * amount
    for c in coins:                       # coins OUTSIDE
        for x in range(c, amount + 1):
            ways[x] += ways[x - c]
    return ways[amount]

def orderings(nums, target):              # LC 377: 1+2 and 2+1 count twice
    ways = [1] + [0] * target
    for x in range(1, target + 1):        # amount OUTSIDE
        for c in nums:
            if c <= x:
                ways[x] += ways[x - c]
    return ways[target]

def min_coins(coins, amount):             # fewest coins, unlimited supply
    INF = float('inf')
    dp = [0] + [INF] * amount
    for c in coins:
        for x in range(c, amount + 1):
            dp[x] = min(dp[x], dp[x - c] + 1)
    return dp[amount] if dp[amount] < INF else -1

#@@ knap_memo
from functools import cache

def k_memo(w, v, W):                      # 1. top-down: write the recurrence, cache it
    @cache
    def best(i, c):
        if i == len(w):
            return 0
        skip = best(i + 1, c)
        take = best(i + 1, c - w[i]) + v[i] if w[i] <= c else 0
        return max(skip, take)
    return best(0, W)

def k_table(w, v, W):                     # 2. bottom-up: row i reads only row i + 1
    n = len(w)
    dp = [[0] * (W + 1) for _ in range(n + 1)]     # row n is the base case: all 0
    for i in range(n - 1, -1, -1):
        for c in range(W + 1):
            dp[i][c] = dp[i + 1][c]
            if w[i] <= c:
                dp[i][c] = max(dp[i][c], dp[i + 1][c - w[i]] + v[i])
    return dp[0][W]

def k_row(w, v, W):                       # 3. one row: overwrite in place, sweep c downward
    dp = [0] * (W + 1)
    for i in range(len(w) - 1, -1, -1):
        for c in range(W, w[i] - 1, -1):
            dp[c] = max(dp[c], dp[c - w[i]] + v[i])
    return dp[W]

#@@ lis
from bisect import bisect_left

def lis_length(a):                        # strictly increasing, O(n log n)
    tails = []                            # tails[i]: smallest possible last value of an increasing run of length i + 1
    for x in a:
        i = bisect_left(tails, x)         # use bisect_right for "non-decreasing"
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

#@@ edit
def edit_distance(s, t):                  # LC 72, one row of memory
    m, n = len(s), len(t)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])   # delete, insert, replace
        prev = cur
    return prev[n]

#@@ cooldown
def max_profit_cooldown(prices):          # LC 309: states instead of a table
    hold, sold, rest = float('-inf'), 0, 0       # at the end of the day: holding / just sold / free to buy
    for x in prices:
        hold, sold, rest = max(hold, rest - x), hold + x, max(rest, sold)
    return max(sold, rest)

#@@ bitdp
def min_assignment(cost):                 # n workers to n jobs, n <= 15
    n = len(cost)
    INF = float('inf')
    dp = [INF] * (1 << n)                 # dp[mask]: cheapest way to give the jobs in mask to the first popcount(mask) workers
    dp[0] = 0
    for mask in range(1 << n):
        i = mask.bit_count()              # Python 3.10+; otherwise bin(mask).count("1")
        if i == n:
            continue
        for j in range(n):
            if not mask >> j & 1:
                nm = mask | 1 << j
                dp[nm] = min(dp[nm], dp[mask] + cost[i][j])
    return dp[-1]

#@@ deadlines
import heapq

def max_profit_deadlines(jobs):           # jobs (deadline, profit), each takes one time slot
    heap = []                             # profits of the jobs we currently plan to do
    for d, p in sorted(jobs):
        heapq.heappush(heap, p)
        if len(heap) > d:                 # more jobs than slots before deadline d: drop the least profitable
            heapq.heappop(heap)
    return sum(heap)

#@@ gas
def start_station(gas, cost):              # LC 134
    if sum(gas) < sum(cost):
        return -1
    tank = start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                      # nothing in [start, i] can work as a start
            start, tank = i + 1, 0
    return start

#@@ candy
def candy(r):                             # LC 135: two passes, one for each neighbour
    n = len(r)
    c = [1] * n
    for i in range(1, n):
        if r[i] > r[i - 1]:
            c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if r[i] > r[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)
    return sum(c)

#@@ huffman
import heapq

def merge_cost(w):                        # join all pieces; a join costs the sum of the two (ropes, Huffman)
    w = w[:]
    heapq.heapify(w)
    total = 0
    while len(w) > 1:
        a, b = heapq.heappop(w), heapq.heappop(w)
        total += a + b
        heapq.heappush(w, a + b)
    return total

#@@ first_true
def first_true(lo, hi, ok):               # smallest x in [lo, hi] with ok(x) True; ok must be False..False True..True
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def ship_days(weights, days):             # LC 1011: smallest capacity that ships everything in `days`
    def ok(cap):
        need, load = 1, 0
        for x in weights:
            if load + x > cap:
                need += 1; load = 0
            load += x
        return need <= days
    return first_true(max(weights), sum(weights), ok)

#@@ prefix
def count_sum_k(a, k):                    # LC 560: subarrays with sum k, negatives allowed
    seen, s, cnt = {0: 1}, 0, 0           # seen[p]: how many prefixes had sum p
    for x in a:
        s += x
        cnt += seen.get(s - k, 0)         # a prefix k less than now closes a subarray of sum k
        seen[s] = seen.get(s, 0) + 1
    return cnt

def apply_ranges(n, ops):                 # difference array: add v to a[l..r] for each op, O(n + ops)
    diff = [0] * (n + 1)
    for l, r, v in ops:
        diff[l] += v
        diff[r + 1] -= v
    out, run = [], 0
    for i in range(n):
        run += diff[i]
        out.append(run)
    return out

def shortest_at_least(a, S):              # LC 209: shortest subarray with sum >= S, positives only
    best, lo, run = float('inf'), 0, 0
    for hi, x in enumerate(a):
        run += x
        while run >= S:                   # shrink while still valid: lo never moves back
            best = min(best, hi - lo + 1)
            run -= a[lo]; lo += 1
    return 0 if best == float('inf') else best

#@@ cf_input
import sys

def main():
    data = sys.stdin.buffer.read().split()     # read everything once
    pos = 0
    def nxt():
        nonlocal pos
        pos += 1
        return int(data[pos - 1])
    t = nxt()
    out = []
    for _ in range(t):
        n = nxt()
        a = [nxt() for _ in range(n)]
        out.append(str(sum(a)))                # your answer for this test
    sys.stdout.write("\n".join(out) + "\n")    # print once at the end

main()

#@@ stress
import random
from itertools import combinations

def brute(c):                             # "at most two coins": try every choice of 0, 1 or 2 coins
    best = 0
    for k in range(3):
        for pick in combinations(c, k):
            best = max(best, sum(pick))
    return best

def fast(c):                              # the quick idea you want to trust
    return sum(sorted(c)[-2:])            # top two... but what if a value is negative?

for it in range(2000):                    # tiny random inputs find bugs fastest
    c = [random.randint(-5, 5) for _ in range(random.randint(1, 5))]
    if brute(c) != fast(c):
        print("MISMATCH on", c, "brute", brute(c), "fast", fast(c))
        break
else:
    print("all 2000 tests agree")

#@@ deep_rec
import sys, threading

def solve():
    def depth(n):                         # recursion 10^5 deep: crashes without the two lines below
        return 0 if n == 0 else 1 + depth(n - 1)
    print(depth(100000))

sys.setrecursionlimit(1 << 20)            # allow deep calls...
threading.stack_size(1 << 27)             # ...and give the thread a stack big enough for them
t = threading.Thread(target=solve)
t.start()
t.join()

#@@ stdlib
from bisect import bisect_left, bisect_right, insort
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from itertools import accumulate, combinations, groupby, pairwise, permutations, product
from math import comb, gcd, inf, isqrt, lcm

a = [1, 3, 3, 7]
print(bisect_left(a, 3), bisect_right(a, 3))       # 1 3: first and one-past-last position of 3
print(list(accumulate([1, 2, 3, 4])))              # [1, 3, 6, 10]: prefix sums
print(list(pairwise([1, 4, 9])))                   # [(1, 4), (4, 9)]: neighbours
print(comb(5, 2), gcd(12, 18), lcm(4, 6), isqrt(99))   # 10 6 12 9
print(pow(3, -1, 7))                               # 5: modular inverse (Python 3.8+)
print((13).bit_count(), 13 & -13)                  # 3 1: ones in 13, lowest set bit (Python 3.10+)
print(sorted(["bb", "a", "ccc"], key=lambda s: (-len(s), s)))   # longest first, ties alphabetical
print(Counter("abracadabra").most_common(2))       # [('a', 5), ('b', 2)]

#@@ rev_brute
import itertools

def rev_brute(c):                         # Chakravyuh Reversed, subtask 1 (n <= 6): try every graph
    n = len(c)
    for a in itertools.product(range(-1, n), repeat=n):
        if chak_brute(list(a)) == c:
            return list(a)
    return None

#@@ odd_walk_brute
def odd_walk_brute(n, edges, s, t):       # Odd Walk, subtask 1: which vertices can a walk of exactly L edges reach?
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    here = {s}
    for L in range(1, 2 * n + 3):
        here = {v for u in here for v in adj[u]}
        if L % 2 == 1 and t in here:
            return L
    return -1

#@@ free_brute
def free_brute(n, edges, s, t, k):        # Free Passes, subtask 1: every simple path, free the k heaviest edges
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = float('inf')
    def go(u, seen, ws):
        nonlocal best
        if u == t:
            best = min(best, sum(sorted(ws)[:max(0, len(ws) - k)]))
            return
        for v, w in adj[u]:
            if v not in seen:
                go(v, seen | {v}, ws + [w])
    go(s, {s}, [])
    return best

#@@ visible_brute
def visible_brute(a):                     # Visible Pairs, subtask 1: O(n^2) with a running maximum
    n, ans = len(a), 0
    for i in range(n):
        mx = 0                            # tallest person strictly between i and j
        for j in range(i + 1, n):
            if mx <= min(a[i], a[j]):
                ans += 1
            mx = max(mx, a[j])
    return ans

#@@ subsets_brute
def subsets_brute(a, T):                  # Split the Treasure, subtask 1: n <= 20, every subset
    n, cnt = len(a), 0
    for mask in range(1 << n):
        if sum(a[i] for i in range(n) if mask >> i & 1) == T:
            cnt += 1
    return cnt

#@@ frozen
import itertools
from collections import deque

def sortable_brute(p, k):                 # subtask 1 (n <= 7): BFS over every arrangement reachable by legal swaps
    n = len(p)
    start, goal = tuple(p), tuple(range(n))
    seen = {start}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == goal:
            return True
        for i in range(n):
            for j in range(i + k, n):         # legal swaps only: distance at least k
                nxt = list(cur)
                nxt[i], nxt[j] = nxt[j], nxt[i]
                nxt = tuple(nxt)
                if nxt not in seen:
                    seen.add(nxt); q.append(nxt)
    return False

def sortable(p, k):                       # positions n-k .. k-1 have no legal partner: they must already be right
    n = len(p)
    return all(p[i] == i for i in range(max(0, n - k), min(n, k)))

#@@ fenwick
class Fenwick:                            # prefix sums with point updates, O(log n) each
    def __init__(self, n):
        self.t = [0] * (n + 1)
    def add(self, i, v):                  # a[i] += v (0-based)
        i += 1
        while i < len(self.t):
            self.t[i] += v
            i += i & -i                   # jump to the next block that covers i
    def prefix(self, i):                  # sum of a[0 .. i-1]
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i                   # drop the lowest set bit
        return s

#@@ topo_dfs
def topo_dfs(n, adj):                     # iterative DFS (no recursion limit); order, or None if there is a cycle
    WHITE, GREY, BLACK = 0, 1, 2
    color = [WHITE] * n
    post = []
    for s in range(n):
        if color[s] != WHITE:
            continue
        color[s] = GREY
        stack = [(s, 0)]                  # (node, index of the next neighbour to try)
        while stack:
            u, i = stack.pop()
            if i < len(adj[u]):
                stack.append((u, i + 1))
                v = adj[u][i]
                if color[v] == GREY:      # v is still on the current path: a back edge, so a cycle
                    return None
                if color[v] == WHITE:
                    color[v] = GREY
                    stack.append((v, 0))
            else:
                color[u] = BLACK          # everything reachable from u is finished
                post.append(u)
    return post[::-1]                     # reverse finishing order is a topological order

#@@ course_schedule
from collections import deque

def find_order(num_courses, prerequisites):   # LC 210: [a, b] means take b before a; [] if impossible
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == num_courses else []

def can_finish(num_courses, prerequisites):   # LC 207: the same peel, only the count matters
    return len(find_order(num_courses, prerequisites)) == num_courses

#@@ dag_paths
from collections import deque

def dag_shortest_longest(n, edges, s):    # weighted DAG, negative weights allowed; None if there is a cycle
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, w in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) < n:
        return None
    INF = float('inf')
    short, long_ = [INF] * n, [-INF] * n
    short[s] = long_[s] = 0
    for u in order:                       # u is final before its out-edges are used: no heap needed
        if short[u] == INF:
            continue                      # not reachable from s
        for v, w in adj[u]:
            short[v] = min(short[v], short[u] + w)
            long_[v] = max(long_[v], long_[u] + w)
    return short, long_

#@@ longest_increasing_path
from collections import deque

def longest_increasing_path(matrix):      # LC 329: peel the DAG "step to a bigger neighbour" layer by layer
    R, C = len(matrix), len(matrix[0])
    D = ((1, 0), (-1, 0), (0, 1), (0, -1))
    indeg = [[0] * C for _ in range(R)]   # how many smaller neighbours can step INTO this cell
    for r in range(R):
        for c in range(C):
            for dr, dc in D:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and matrix[nr][nc] < matrix[r][c]:
                    indeg[r][c] += 1
    q = deque((r, c) for r in range(R) for c in range(C) if indeg[r][c] == 0)
    layers = 0
    while q:
        layers += 1                       # one BFS layer = one more cell on the longest path
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in D:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and matrix[nr][nc] > matrix[r][c]:
                    indeg[nr][nc] -= 1
                    if indeg[nr][nc] == 0:
                        q.append((nr, nc))
    return layers

#@@ largest_color_value
from collections import deque

def largest_path_value(colors, edges):    # LC 1857: most frequent colour on some path; -1 if there is a cycle
    n = len(colors)
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1                     # a self-loop gives indeg[u] >= 1 forever: caught as a cycle
    cnt = [[0] * 26 for _ in range(n)]    # cnt[u][c]: best count of colour c on a path that ENDS at u
    q = deque(i for i in range(n) if indeg[i] == 0)
    seen = best = 0
    while q:
        u = q.popleft()
        seen += 1
        cnt[u][ord(colors[u]) - 97] += 1  # add u itself
        best = max(best, max(cnt[u]))
        for v in adj[u]:
            for c in range(26):           # push the best counts forward
                if cnt[u][c] > cnt[v][c]:
                    cnt[v][c] = cnt[u][c]
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return best if seen == n else -1

#@@ network_delay
import heapq

def network_delay(times, n, k):           # LC 743: nodes 1..n, edges (u, v, w); -1 if someone is never reached
    adj = [[] for _ in range(n + 1)]
    for u, v, w in times:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[k] = 0
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                   # stale entry
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    worst = max(dist[1:])
    return -1 if worst == INF else worst

#@@ max_probability
import heapq

def max_probability(n, edges, succ_prob, start, end):    # LC 1514: maximise a product, so pop the LARGEST
    adj = [[] for _ in range(n)]
    for (a, b), p in zip(edges, succ_prob):
        adj[a].append((b, p))
        adj[b].append((a, p))
    best = [0.0] * n
    best[start] = 1.0
    heap = [(-1.0, start)]                # heapq is a min-heap: store the negative
    while heap:
        p, u = heapq.heappop(heap)
        p = -p
        if p < best[u]:                   # stale
            continue
        if u == end:
            return p
        for v, w in adj[u]:
            if p * w > best[v]:           # probabilities are <= 1, so a path never improves by getting longer
                best[v] = p * w
                heapq.heappush(heap, (-best[v], v))
    return 0.0

#@@ minimax_grid
import heapq

def min_effort(heights):                  # LC 1631: minimise the LARGEST height difference on the path
    R, C = len(heights), len(heights[0])
    INF = float('inf')
    best = [[INF] * C for _ in range(R)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        d, r, c = heapq.heappop(heap)
        if d > best[r][c]:
            continue
        if (r, c) == (R - 1, C - 1):
            return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                nd = max(d, abs(heights[nr][nc] - heights[r][c]))     # "sum" becomes "max"
                if nd < best[nr][nc]:
                    best[nr][nc] = nd
                    heapq.heappush(heap, (nd, nr, nc))
    return 0

def swim_in_water(grid):                  # LC 778: the cost of a path is the tallest cell on it
    n = len(grid)
    INF = float('inf')
    best = [[INF] * n for _ in range(n)]
    best[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        d, r, c = heapq.heappop(heap)
        if d > best[r][c]:
            continue
        if (r, c) == (n - 1, n - 1):
            return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                nd = max(d, grid[nr][nc])
                if nd < best[nr][nc]:
                    best[nr][nc] = nd
                    heapq.heappush(heap, (nd, nr, nc))
    return -1

#@@ minimax_bs
from collections import deque

def min_effort_bs(heights):               # LC 1631 again: binary search the answer, BFS answers "can we do it with limit x?"
    R, C = len(heights), len(heights[0])
    def reachable(limit):
        seen = [[False] * C for _ in range(R)]
        seen[0][0] = True
        q = deque([(0, 0)])
        while q:
            r, c = q.popleft()
            if (r, c) == (R - 1, C - 1):
                return True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and not seen[nr][nc] and abs(heights[nr][nc] - heights[r][c]) <= limit:
                    seen[nr][nc] = True
                    q.append((nr, nc))
        return False
    lo, hi = 0, max(max(row) for row in heights) - min(min(row) for row in heights)
    while lo < hi:                        # smallest limit for which reachable() is True
        mid = (lo + hi) // 2
        if reachable(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

#@@ cheapest_flights
def cheapest_flights(n, flights, src, dst, k):   # LC 787: at most k stops = at most k + 1 edges
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):                # round r: best cost using at most r edges
        nxt = dist[:]                     # read OLD values, write NEW: each round adds exactly one edge
        for u, v, w in flights:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == INF else dist[dst]

#@@ city_threshold
def find_the_city(n, edges, distance_threshold):  # LC 1334: fewest cities within the threshold; ties: the larger number
    INF = float('inf')
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[u][v] = d[v][u] = min(d[u][v], w)
    for k in range(n):                    # k outermost: "allow k as a stop"
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    best_city, best_cnt = -1, n + 1
    for i in range(n):
        cnt = sum(1 for j in range(n) if j != i and d[i][j] <= distance_threshold)
        if cnt <= best_cnt:               # <= so that a later (larger) city wins ties
            best_cnt, best_city = cnt, i
    return best_city

#@@ prim
import heapq

def prim(n, edges):                       # edges (u, v, w), undirected; returns (total, tree edges) or None if disconnected
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    seen = [False] * n
    heap = [(0, 0, -1)]                   # (weight of the edge that enters the tree, vertex, parent)
    total, used = 0, []
    while heap:
        w, u, p = heapq.heappop(heap)
        if seen[u]:                       # already in the tree: stale
            continue
        seen[u] = True
        total += w
        if p != -1:
            used.append((p, u, w))
        for v, x in adj[u]:
            if not seen[v]:
                heapq.heappush(heap, (x, v, u))
    return (total, used) if len(used) == n - 1 else None

#@@ mst_problems
def min_cost_connect_points(points):      # LC 1584: complete graph, so Prim WITHOUT a heap, O(n^2)
    n = len(points)
    INF = float('inf')
    dist = [INF] * n                      # cheapest edge from the tree to each outside point
    in_tree = [False] * n
    dist[0] = 0
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not in_tree[i]), key=dist.__getitem__)
        in_tree[u] = True
        total += dist[u]
        for v in range(n):
            if not in_tree[v]:
                d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                if d < dist[v]:
                    dist[v] = d
    return total

def _find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]     # path halving
        x = parent[x]
    return x

def find_redundant_connection(edges):     # LC 684: nodes 1..n, one extra edge; the edge that closes the cycle
    parent = list(range(len(edges) + 1))
    for a, b in edges:
        ra, rb = _find(parent, a), _find(parent, b)
        if ra == rb:
            return [a, b]                 # already connected: this edge is the extra one
        parent[ra] = rb
    return []

def minimum_cost(n, connections):         # LC 1135: cities 1..n, edges (a, b, cost); -1 if not connectable
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    total = used = 0
    for a, b, w in sorted(connections, key=lambda e: e[2]):
        ra, rb = _find(parent, a), _find(parent, b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            total += w
            used += 1
    return total if used == n - 1 else -1

#@@ critical_edges
def _find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def find_critical_and_pseudo(n, edges):   # LC 1489: edges (a, b, w) on nodes 0..n-1; returns [critical ids, pseudo ids]
    m = len(edges)
    order = sorted(range(m), key=lambda i: edges[i][2])
    INF = float('inf')
    def mst(skip=-1, force=-1):           # MST weight with edge `force` required and edge `skip` banned
        parent = list(range(n))
        total = used = 0
        if force != -1:
            a, b, w = edges[force]
            parent[_find(parent, a)] = _find(parent, b)
            total, used = w, 1
        for i in order:
            if i == skip:
                continue
            a, b, w = edges[i]
            ra, rb = _find(parent, a), _find(parent, b)
            if ra != rb:
                parent[ra] = rb
                total += w
                used += 1
        return total if used == n - 1 else INF
    base = mst()
    critical, pseudo = [], []
    for i in range(m):
        if mst(skip=i) > base:            # without it the best tree gets heavier (or disconnects): in EVERY MST
            critical.append(i)
        elif mst(force=i) == base:        # forcing it still gives an MST: in SOME MST
            pseudo.append(i)
    return [critical, pseudo]

#@@ fractional_knapsack
def fractional_knapsack(items, W):         # items (value, weight), weight > 0; fractions of an item are allowed
    total = 0.0
    for v, w in sorted(items, key=lambda it: it[0] / it[1], reverse=True):     # best value per kilo first
        if W <= 0:
            break
        take = min(w, W)                   # all of it, or whatever still fits
        total += v * take / w
        W -= take
    return total

#@@ greedy_vs_dp_coins
def greedy_coins(coins, amount):           # always take the biggest coin that still fits
    count = 0
    for c in sorted(coins, reverse=True):
        count += amount // c
        amount %= c
    return count if amount == 0 else -1

def dp_coins(coins, amount):               # LC 322: always correct
    INF = float('inf')
    best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return -1 if best[amount] == INF else best[amount]

def first_greedy_failure(coins, limit=100):    # smallest amount where greedy loses, or None
    for a in range(1, limit + 1):
        if greedy_coins(coins, a) != dp_coins(coins, a):
            return a
    return None

#@@ task_scheduler
from collections import Counter

def least_interval(tasks, n):              # LC 621: the busiest task decides the frame
    cnt = Counter(tasks)
    top = max(cnt.values())
    num_top = sum(1 for v in cnt.values() if v == top)
    return max(len(tasks), (top - 1) * (n + 1) + num_top)

#@@ partition_labels
def partition_labels(s):                   # LC 763: cut as soon as the farthest "last occurrence" is behind us
    last = {ch: i for i, ch in enumerate(s)}
    out, start, end = [], 0, 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            out.append(end - start + 1)
            start = i + 1
    return out

#@@ jump_game
def can_jump(nums):                        # LC 55: track the farthest index reachable so far
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True

def min_jumps(nums):                       # LC 45 (the end is always reachable): BFS by layers, no queue
    jumps = cur_end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == cur_end:                   # the current layer is exhausted: one more jump
            jumps += 1
            cur_end = far
    return jumps

#@@ min_arrows
def find_min_arrow_shots(points):          # LC 452: sort by right end, shoot there, skip everything it bursts
    arrows, pos = 0, -float('inf')
    for a, b in sorted(points, key=lambda p: p[1]):
        if a > pos:
            arrows += 1
            pos = b
    return arrows

#@@ conv_lcs
from functools import cache

def lcs_memo(a, b):                        # step 1: the recursion, with a cache
    @cache
    def f(i, j):                           # LCS of a[i:] and b[j:]
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

def lcs_table(a, b):                       # step 2: the same cells, filled from the base cases outward
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            dp[i][j] = 1 + dp[i + 1][j + 1] if a[i] == b[j] else max(dp[i + 1][j], dp[i][j + 1])
    return dp[0][0]

def lcs_row(a, b):                         # step 3: row i only needs row i + 1, so keep one row
    n, m = len(a), len(b)
    row = [0] * (m + 1)
    for i in range(n - 1, -1, -1):
        diag = 0                           # dp[i + 1][j + 1], saved before it is overwritten
        for j in range(m - 1, -1, -1):
            old = row[j]                   # dp[i + 1][j]
            row[j] = 1 + diag if a[i] == b[j] else max(old, row[j + 1])
            diag = old
    return row[0]

#@@ conv_edit
from functools import cache

def edit_memo(a, b):
    @cache
    def f(i, j):                           # edits to turn a[i:] into b[j:]
        if i == len(a):
            return len(b) - j              # insert the rest
        if j == len(b):
            return len(a) - i              # delete the rest
        if a[i] == b[j]:
            return f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1), f(i + 1, j + 1))     # delete, insert, replace
    return f(0, 0)

def edit_table(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][m] = n - i
    for j in range(m + 1):
        dp[n][j] = m - j
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = dp[i + 1][j + 1]
            else:
                dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j + 1], dp[i + 1][j + 1])
    return dp[0][0]

def edit_row(a, b):
    n, m = len(a), len(b)
    row = [m - j for j in range(m + 1)]    # the base row dp[n][j]
    for i in range(n - 1, -1, -1):
        diag = row[m]                      # dp[i + 1][m]
        row[m] = n - i                     # dp[i][m]
        for j in range(m - 1, -1, -1):
            old = row[j]
            row[j] = diag if a[i] == b[j] else 1 + min(old, row[j + 1], diag)
            diag = old
    return row[0]

#@@ conv_interleave
from functools import cache

def interleave_memo(s1, s2, s3):           # LC 97: can s3 be woven from s1 and s2, keeping each one's order?
    if len(s1) + len(s2) != len(s3):
        return False
    @cache
    def f(i, j):                           # s1[i:] and s2[j:] must weave into s3[i + j:]
        if i == len(s1) and j == len(s2):
            return True
        k = i + j
        if i < len(s1) and s1[i] == s3[k] and f(i + 1, j):
            return True
        return j < len(s2) and s2[j] == s3[k] and f(i, j + 1)
    return f(0, 0)

def interleave_table(s1, s2, s3):
    n, m = len(s1), len(s2)
    if n + m != len(s3):
        return False
    dp = [[False] * (m + 1) for _ in range(n + 1)]     # dp[i][j]: s1[:i] and s2[:j] weave into s3[:i + j]
    dp[0][0] = True
    for i in range(n + 1):
        for j in range(m + 1):
            if i > 0 and dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]:
                dp[i][j] = True
            if j > 0 and dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]:
                dp[i][j] = True
    return dp[n][m]

def interleave_row(s1, s2, s3):
    n, m = len(s1), len(s2)
    if n + m != len(s3):
        return False
    row = [False] * (m + 1)
    row[0] = True
    for i in range(n + 1):
        for j in range(m + 1):
            if i > 0 and j == 0:
                row[0] = row[0] and s1[i - 1] == s3[i - 1]
            elif i > 0 or j > 0:
                up = i > 0 and row[j] and s1[i - 1] == s3[i + j - 1]       # row[j] still holds dp[i - 1][j]
                left = j > 0 and row[j - 1] and s2[j - 1] == s3[i + j - 1]
                row[j] = up or left
    return row[m]

#@@ tree_dp
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(vals):                      # LeetCode's level-order list with None for missing children
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q, i = [root], 1
    for node in q:
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i]); q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i]); q.append(node.right)
        i += 1
    return root

def children_first(root):                  # iterative: no recursion limit on a 10^5-deep tree
    order, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        order.append(node)
        if node.left: stack.append(node.left)
        if node.right: stack.append(node.right)
    return order[::-1]                     # reversed "parent first" means every child comes before its parent

def rob_tree(root):                        # LC 337: two numbers per node, "robbed" and "skipped"
    rob, skip = {}, {}
    for v in children_first(root):
        l, r = v.left, v.right
        rob[v] = v.val + (skip[l] if l else 0) + (skip[r] if r else 0)
        skip[v] = (max(rob[l], skip[l]) if l else 0) + (max(rob[r], skip[r]) if r else 0)
    return max(rob[root], skip[root]) if root else 0

def diameter(root):                        # LC 543: edges on the longest path; the bend sits at some node
    h, best = {}, 0
    for v in children_first(root):
        hl = h[v.left] if v.left else 0
        hr = h[v.right] if v.right else 0
        h[v] = 1 + max(hl, hr)             # height in nodes
        best = max(best, hl + hr)
    return best

def max_path_sum(root):                    # LC 124: values may be negative; a path may start and end anywhere
    gain, best = {}, -float('inf')
    for v in children_first(root):
        gl = max(0, gain[v.left]) if v.left else 0      # a negative branch is simply not taken
        gr = max(0, gain[v.right]) if v.right else 0
        gain[v] = v.val + max(gl, gr)      # going UP, a path can use only one branch
        best = max(best, v.val + gl + gr)  # a path that bends here uses both
    return best

#@@ dsu_extras
def accounts_merge(accounts):              # LC 721: accounts are [name, email, email, ...]
    parent, owner = {}, {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for acc in accounts:
        first = acc[1]
        for e in acc[1:]:
            parent.setdefault(e, e)
            owner[e] = acc[0]
            parent[find(e)] = find(first)  # every email of one account joins the first one's set
    groups = {}
    for e in parent:
        groups.setdefault(find(e), []).append(e)
    return [[owner[root]] + sorted(es) for root, es in groups.items()]

def calc_equation(equations, values, queries):    # LC 399: weighted union-find, ratio[x] = x / parent[x]
    parent, ratio = {}, {}
    def find(x):
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        root = x
        for node in reversed(path):        # the node nearest the root first
            p = parent[node]
            if p != root:
                ratio[node] *= ratio[p]    # node/root = (node/p) * (p/root)
            parent[node] = root
        return root
    for (a, b), v in zip(equations, values):
        for x in (a, b):
            if x not in parent:
                parent[x], ratio[x] = x, 1.0
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            ratio[ra] = v * ratio[b] / ratio[a]       # from a = v * b
    out = []
    for a, b in queries:
        if a not in parent or b not in parent or find(a) != find(b):
            out.append(-1.0)
        else:
            out.append(ratio[a] / ratio[b])
    return out

#@@ median_finder
import heapq

class MedianFinder:                        # LC 295: two heaps meet at the middle
    def __init__(self):
        self.lo = []                       # max-heap (stored negated): the smaller half
        self.hi = []                       # min-heap: the larger half
    def add_num(self, x):
        heapq.heappush(self.lo, -x)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))       # the largest small one crosses over
        if len(self.hi) > len(self.lo):                        # keep lo the same size or one bigger
            heapq.heappush(self.lo, -heapq.heappop(self.hi))
    def find_median(self):
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2

#@@ trie
class Trie:                                # LC 208: a tree with one child per letter
    def __init__(self):
        self.root = {}
    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node['$'] = True                   # a word ends here
    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node
    def search(self, word):
        node = self._walk(word)
        return node is not None and '$' in node
    def starts_with(self, prefix):
        return self._walk(prefix) is not None

def find_words(board, words):              # LC 212: one DFS over the grid, steered by a trie of all the words
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node['$'] = w
    R, C = len(board), len(board[0])
    found = []
    def dfs(r, c, node):
        ch = board[r][c]
        nxt = node.get(ch)
        if nxt is None:
            return
        if '$' in nxt:
            found.append(nxt.pop('$'))     # report each word once
        board[r][c] = '#'                  # mark used
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] != '#':
                dfs(nr, nc, nxt)
        board[r][c] = ch                   # undo
        if not nxt:
            node.pop(ch)                   # prune a branch that has nothing left to find
    for r in range(R):
        for c in range(C):
            dfs(r, c, root)
    return found

#@@ memory_sheet
import heapq
from collections import deque

def search_first_true(lo, hi, ok):         # 1. binary search: smallest x in [lo, hi] with ok(x); ok is F..F T..T
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def grid_bfs(grid, start, goal):           # 2. fewest steps on a grid (1 = wall), -1 if unreachable
    R, C = len(grid), len(grid[0])
    dist = {start: 0}
    q = deque([start])
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return dist[(r, c)]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1       # mark when PUSHED
                q.append((nr, nc))
    return -1

def reach(adj, s):                         # 3. iterative DFS: which vertices can s reach?
    seen = {s}
    stack = [s]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen

def topo_kahn(n, edges):                   # 4. Kahn: order, or None on a cycle
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out if len(out) == n else None

def shortest_dijkstra(n, edges, s):        # 5. non-negative weights; finalised when POPPED
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [float('inf')] * n
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist

class UF:                                  # 6. union-find: halving + union by size
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a
        self.sz[a] += self.sz[b]
        return True

def mst_kruskal(n, edges):                 # 7. edges (u, v, w); total weight or None
    uf, total, used = UF(n), 0, 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(u, v):
            total += w
            used += 1
    return total if used == n - 1 else None

def shortest_bf(n, edges, s):              # 8. Bellman-Ford; None on a reachable negative cycle
    dist = [float('inf')] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    if any(dist[u] + w < dist[v] for u, v, w in edges):
        return None
    return dist

def lis_bisect(a):                         # 9. LIS length, strictly increasing, O(n log n)
    from bisect import bisect_left
    tails = []
    for x in a:
        i = bisect_left(tails, x)          # bisect_right would allow equal values
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

def knap_01_row(w, v, W):                  # 10. 0/1 knapsack, one row: capacity goes DOWNWARD
    best = [0] * (W + 1)
    for wi, vi in zip(w, v):
        for c in range(W, wi - 1, -1):
            best[c] = max(best[c], best[c - wi] + vi)
    return best[W]

def edit_dist_row(a, b):                   # 11. edit distance, forward, one row
    row = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        diag, row[0] = row[0], i
        for j in range(1, len(b) + 1):
            old = row[j]
            row[j] = diag if a[i - 1] == b[j - 1] else 1 + min(old, row[j - 1], diag)
            diag = old
    return row[-1]

def greater_next(a):                       # 12. index of the next strictly greater element, -1 if none
    out, stack = [-1] * len(a), []
    for i, x in enumerate(a):
        while stack and a[stack[-1]] < x:
            out[stack.pop()] = i
        stack.append(i)
    return out

def all_subsets(a):                        # 13. backtracking: include or skip each element
    out, cur = [], []
    def go(i):
        if i == len(a):
            out.append(cur[:])             # copy: cur keeps changing
            return
        go(i + 1)
        cur.append(a[i])
        go(i + 1)
        cur.pop()                          # undo
    go(0)
    return out

#@@ pitfalls_demo
import heapq

def pitfalls_demo():
    out = {}
    def bad_append(x, acc=[]):             # 1. a mutable default is created ONCE and shared by every call
        acc.append(x)
        return acc
    bad_append(1)
    out['mutable_default'] = bad_append(2)                     # [1, 2], not [2]
    grid_bad = [[0] * 3] * 3               # 2. three names for ONE row
    grid_bad[0][0] = 7
    grid_good = [[0] * 3 for _ in range(3)]
    grid_good[0][0] = 7
    out['alias_grid'] = (grid_bad[2][0], grid_good[2][0])      # (7, 0)
    a = [3, 1, 2]                          # 3. b = a is a second name; a[:] is a copy (and costs O(n))
    b, c = a, a[:]
    a.sort()
    out['alias_list'] = (b, c)                                 # ([1, 2, 3], [3, 1, 2])
    h = []                                 # 4. heapq is a MIN-heap; for the max, push the negative
    for x in (5, 1, 9):
        heapq.heappush(h, -x)
    out['max_heap'] = -heapq.heappop(h)                        # 9
    h2 = [(1, 'b'), (1, 'a')]              # 5. equal first items: Python compares the second ones
    heapq.heapify(h2)
    out['tie_break'] = heapq.heappop(h2)                       # (1, 'a')
    out['floor_div'] = (-7 // 2, -7 % 2, int(-7 / 2))          # (-4, 1, -3): // floors, int() truncates
    out['sort_stable'] = sorted([(1, 'x'), (0, 'y'), (1, 'a')], key=lambda t: t[0])    # equal keys keep their order
    return out


#@@ merge_sort_stable
def merge_sort(a):                         # LC 912: new sorted list; stable; O(n log n) time, O(n) extra space
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:            # <=, not <: on a tie the LEFT item goes first, and that is stability
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])                   # one side is empty; the other is already sorted
    out.extend(right[j:])
    return out

#@@ merge_counting
def count_smaller(nums):                   # LC 315: for each i, how many later elements are smaller?
    n = len(nums)
    idx = list(range(n))                   # sort the INDICES by value, so we remember who is who
    res = [0] * n
    def sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        tmp, i, j = [], lo, mid
        while i < mid or j < hi:
            if j == hi or (i < mid and nums[idx[i]] <= nums[idx[j]]):
                res[idx[i]] += j - mid     # the j - mid right-half items already taken were strictly smaller
                tmp.append(idx[i])
                i += 1
            else:
                tmp.append(idx[j])
                j += 1
        idx[lo:hi] = tmp
    sort(0, n)
    return res

def reverse_pairs(nums):                   # LC 493: pairs i < j with nums[i] > 2 * nums[j]
    a = nums[:]
    def sort(lo, hi):
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        cnt = sort(lo, mid) + sort(mid, hi)
        j = mid
        for i in range(lo, mid):           # both halves are sorted, so j only moves forward
            while j < hi and a[i] > 2 * a[j]:
                j += 1
            cnt += j - mid
        a[lo:hi] = sorted(a[lo:hi])        # merging two sorted runs is linear; write the manual merge on an exam
        return cnt
    return sort(0, len(a))

#@@ amortised
class DynArray:                            # what list.append does underneath, with the copies counted
    def __init__(self, grow=2):
        self.cap, self.n, self.copies, self.grow = 1, 0, 0, grow
        self.data = [None]
    def append(self, x):
        if self.n == self.cap:             # full: allocate bigger and copy everything over
            self.cap = self.cap * 2 if self.grow == 2 else self.cap + 1
            new = [None] * self.cap
            for i in range(self.n):
                new[i] = self.data[i]
                self.copies += 1
            self.data = new
        self.data[self.n] = x
        self.n += 1

#@@ hashing
class ChainedMap:                          # buckets are small lists; the table doubles when the load factor passes 0.75
    def __init__(self):
        self.buckets = [[] for _ in range(8)]
        self.n = 0
    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]
    def put(self, key, val):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, val)
                return
        b.append((key, val))
        self.n += 1
        if self.n / len(self.buckets) > 0.75:
            self._grow()
    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default
    def remove(self, key):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b.pop(i)
                self.n -= 1
                return True
        return False
    def _grow(self):
        old = [kv for b in self.buckets for kv in b]
        self.buckets = [[] for _ in range(2 * len(self.buckets))]
        for k, v in old:                   # every key moves: hash % newsize changed
            self.buckets[hash(k) % len(self.buckets)].append((k, v))

_EMPTY, _TOMB = object(), object()

class ProbeMap:                            # open addressing, linear probing, tombstones for deletes
    def __init__(self):
        self.slots = [_EMPTY] * 8
        self.n = self.used = 0             # n live keys; used = live + tombstones
    def _find(self, key):                  # (slot of key or None, first free slot to insert into)
        cap = len(self.slots)
        i, first_free = hash(key) % cap, None
        while True:
            s = self.slots[i]
            if s is _EMPTY:
                return None, (first_free if first_free is not None else i)
            if s is _TOMB:
                if first_free is None:
                    first_free = i         # a deleted slot can be reused, but keep looking: the key may be further on
            elif s[0] == key:
                return i, None
            i = (i + 1) % cap
    def put(self, key, val):
        at, free = self._find(key)
        if at is not None:
            self.slots[at] = (key, val)
            return
        if self.slots[free] is _EMPTY:
            self.used += 1
        self.slots[free] = (key, val)
        self.n += 1
        if self.used / len(self.slots) > 0.5:      # linear probing degrades fast above one half
            self._rebuild()
    def get(self, key, default=None):
        at, _ = self._find(key)
        return default if at is None else self.slots[at][1]
    def remove(self, key):
        at, _ = self._find(key)
        if at is None:
            return False
        self.slots[at] = _TOMB                     # not EMPTY: that would cut the probe chain of other keys
        self.n -= 1
        return True
    def _rebuild(self):
        live = [s for s in self.slots if s is not _EMPTY and s is not _TOMB]
        self.slots = [_EMPTY] * (2 * len(self.slots))
        self.n = self.used = 0
        for k, v in live:
            self.put(k, v)

class LRUCache:                            # LC 146: dict for O(1) lookup, doubly linked list for O(1) reordering
    class _N:
        __slots__ = ('k', 'v', 'prev', 'next')
        def __init__(self, k=0, v=0):
            self.k, self.v, self.prev, self.next = k, v, None, None
    def __init__(self, capacity):
        self.cap, self.map = capacity, {}
        self.head, self.tail = self._N(), self._N()     # sentinels: no edge cases at the ends
        self.head.next, self.tail.prev = self.tail, self.head
    def _unlink(self, x):
        x.prev.next, x.next.prev = x.next, x.prev
    def _push_front(self, x):
        x.next, x.prev = self.head.next, self.head
        self.head.next.prev = x
        self.head.next = x
    def get(self, key):
        if key not in self.map:
            return -1
        x = self.map[key]
        self._unlink(x)
        self._push_front(x)                # most recently used goes to the front
        return x.v
    def put(self, key, value):
        if key in self.map:
            x = self.map[key]
            x.v = value
            self._unlink(x)
            self._push_front(x)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev           # least recently used sits at the back
            self._unlink(lru)
            del self.map[lru.k]
        x = self._N(key, value)
        self.map[key] = x
        self._push_front(x)

class MyHashMap:                           # LC 706 (and LC 705 with the value dropped): fixed buckets, chaining
    def __init__(self):
        self.B = [[] for _ in range(769)]  # a prime number of buckets spreads keys better
    def put(self, key, value):
        b = self.B[key % 769]
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, value)
                return
        b.append((key, value))
    def get(self, key):
        for k, v in self.B[key % 769]:
            if k == key:
                return v
        return -1
    def remove(self, key):
        b = self.B[key % 769]
        for i, (k, _) in enumerate(b):
            if k == key:
                b.pop(i)
                return

#@@ last_stone
import heapq

def last_stone_weight(stones):             # LC 1046: always smash the two heaviest
    h = [-s for s in stones]               # max-heap by negating
    heapq.heapify(h)
    while len(h) > 1:
        a = -heapq.heappop(h)
        b = -heapq.heappop(h)
        if a != b:
            heapq.heappush(h, -(a - b))    # what is left of the heavier stone
    return -h[0] if h else 0

#@@ dijkstra_done
import heapq

def dijkstra_done(n, edges, s):           # the textbook version: a vertex is FINAL the first time it is popped
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    done = [False] * n
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True                    # from here on, dist[u] is never touched again
        for v, w in adj[u]:
            if not done[v] and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist
