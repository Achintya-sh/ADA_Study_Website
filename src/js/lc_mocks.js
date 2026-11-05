/* ===== Three-problem LeetCode mocks: one easy, one medium, one hard ===== */
(function () {
  'use strict';
  const E = 'Easy', M = 'Medium', H = 'Hard';
  const P = (id, s, t, d, topic) => ({ id, s, t, d, topic });
  const MOCKS_LC = {
    'LC1 Graphs: path, delay, colours': [P(1971, 'find-if-path-exists-in-graph', 'Find if Path Exists in Graph', E, 'BFS / DSU'), P(743, 'network-delay-time', 'Network Delay Time', M, 'Dijkstra'), P(1857, 'largest-color-value-in-a-directed-graph', 'Largest Color Value in a Directed Graph', H, 'Kahn + DP')],
    'LC2 Graphs: judge, effort, matrix': [P(997, 'find-the-town-judge', 'Find the Town Judge', E, 'degrees'), P(1631, 'path-with-minimum-effort', 'Path With Minimum Effort', M, 'Dijkstra on the max'), P(329, 'longest-increasing-path-in-a-matrix', 'Longest Increasing Path in a Matrix', H, 'DAG layers')],
    'LC3 Spanning trees and union-find': [P(1791, 'find-center-of-star-graph', 'Find Center of Star Graph', E, 'degrees'), P(1584, 'min-cost-to-connect-all-points', 'Min Cost to Connect All Points', M, 'Prim / Kruskal'), P(1489, 'find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree', 'Find Critical and Pseudo-Critical Edges in MST', H, 'MST variants')],
    'LC4 Shortest paths with limits': [P(733, 'flood-fill', 'Flood Fill', E, 'grid DFS'), P(787, 'cheapest-flights-within-k-stops', 'Cheapest Flights Within K Stops', M, 'Bellman–Ford rounds'), P(2092, 'find-all-people-with-secret', 'Find All People With Secret', H, 'DSU by time')],
    'LC5 Greedy': [P(455, 'assign-cookies', 'Assign Cookies', E, 'sort + two pointers'), P(621, 'task-scheduler', 'Task Scheduler', M, 'greedy frame'), P(135, 'candy', 'Candy', H, 'two passes')],
    'LC6 Dynamic programming II': [P(70, 'climbing-stairs', 'Climbing Stairs', E, '1-D DP'), P(97, 'interleaving-string', 'Interleaving String', M, '2-D DP'), P(115, 'distinct-subsequences', 'Distinct Subsequences', H, '2-D DP counting')],
    'LC7 Trees': [P(543, 'diameter-of-binary-tree', 'Diameter of Binary Tree', E, 'tree DP'), P(337, 'house-robber-iii', 'House Robber III', M, 'tree DP'), P(124, 'binary-tree-maximum-path-sum', 'Binary Tree Maximum Path Sum', H, 'tree DP')],
    'LC8 Heaps': [P(703, 'kth-largest-element-in-a-stream', 'Kth Largest Element in a Stream', E, 'min-heap of size k'), P(347, 'top-k-frequent-elements', 'Top K Frequent Elements', M, 'Counter + heap'), P(295, 'find-median-from-data-stream', 'Find Median from Data Stream', H, 'two heaps')],
    'LC9 Beyond the outline': [P(705, 'design-hashset', 'Design HashSet', E, 'chaining'), P(146, 'lru-cache', 'LRU Cache', M, 'hash + linked list'), P(493, 'reverse-pairs', 'Reverse Pairs', H, 'merge sort counting')]
  };
  const MARKS = { Easy: 40, Medium: 80, Hard: 120 };
  const LV = [['0', 'Nothing yet'], ['1', 'Brute force passed some tests'], ['2', 'Fully accepted']];
  function wMockLC(b) {
    const KEY = 'ada-mock-lc';
    let st = ls2Get(KEY, null);
    if (!st || typeof st !== 'object' || !MOCKS_LC[st.pick]) st = { pick: Object.keys(MOCKS_LC)[0], len: 60, left: null, running: false, at: 0, res: {} };
    st.res = st.res || {};
    const sel = h('select', { 'aria-label': 'Mock' }, ...Object.keys(MOCKS_LC).map(k => h('option', { value: k, text: k, selected: k === st.pick })));
    const lenSel = h('select', { 'aria-label': 'Length' }, ...[45, 60, 75, 90].map(m => h('option', { value: m, text: m + ' minutes', selected: m === st.len })));
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
    function paint() {
      const ps = MOCKS_LC[st.pick], res = st.res[st.pick] || {};
      const t = h('table', {}, h('tr', {}, h('th', {}, 'Q'), h('th', {}, 'Level (marks)'), h('th', {}, 'Problem'), h('th', {}, 'Topic'), h('th', {}, 'Result')));
      ps.forEach((p, i) => {
        const s = h('select', { 'aria-label': 'Result for ' + p.t }, ...LV.map(([v, l]) => h('option', { value: v, text: l, selected: String(res[p.id] || 0) === v })));
        s.addEventListener('change', () => { st.res[st.pick] = st.res[st.pick] || {}; st.res[st.pick][p.id] = +s.value; save(); score(); });
        t.append(h('tr', {}, h('td', {}, 'Q' + (i + 1)), h('td', {}, `${p.d} (${MARKS[p.d]})`),
          h('td', {}, h('a', { href: `https://leetcode.com/problems/${p.s}/`, target: '_blank', rel: 'noopener' }, `${p.id}. ${p.t}`)), h('td', {}, p.topic), h('td', {}, s)));
      });
      list.innerHTML = ''; list.append(h('div', { class: 'tw' }, t)); score(); paintClock();
    }
    function score() {
      const ps = MOCKS_LC[st.pick], res = st.res[st.pick] || {};
      const marks = ps.reduce((a, p) => a + MARKS[p.d] * (res[p.id] === 2 ? 1 : res[p.id] === 1 ? 0.5 : 0), 0);
      const zero = ps.filter(p => !res[p.id]).length, full = ps.filter(p => res[p.id] === 2).length;
      if (!ps.some(p => res[p.id]) && st.left !== 0) { cap.textContent = 'Open all three problems, read them, then press Start. Write the brute force first and submit it.'; cap.className = 'cap'; return; }
      cap.textContent = `${marks} of 240 marks (brute force counts as half). ${full} of 3 fully accepted, ${zero} at zero.` + (zero === 0 ? ' Nothing left at zero: that is the habit the end-sem rewards.' : ' Anything still at zero costs more than a half-correct brute force would have.');
      cap.className = 'cap' + (zero === 0 ? ' good' : '');
    }
    function reset() { clearInterval(tick); tick = null; st.left = null; st.running = false; st.res[st.pick] = {}; save(); paint(); }
    sel.addEventListener('change', () => { if (st.running) toggle(); st.pick = sel.value; st.left = null; save(); paint(); });
    lenSel.addEventListener('change', () => { st.len = +lenSel.value; if (!st.running) st.left = null; save(); paintClock(); });
    b.append(h('div', { class: 'row' }, h('label', {}, 'Mock: ', sel), h('label', {}, 'Length: ', lenSel)), h('div', { class: 'row' }, clock, startBtn, btn('Reset', reset)), list, cap,
      h('p', { class: 'mini' }, 'Levels are LeetCode’s own Easy / Medium / Hard labels, typed from memory and not re-checked; slugs were not opened. Marks are this notebook’s (40 / 80 / 120).'));
    paint();
    if (st.running) tick = setInterval(paintClock, 500);
  }
  Object.assign(WIDGETS, { mocklc: wMockLC });
})();
