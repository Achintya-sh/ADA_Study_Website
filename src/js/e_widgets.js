/* ===== End-sem line (E0–E4): labs, ladder, mocks, quizzes ===== */
(function () {
  'use strict';
  const INF = Infinity;
  const fmtD = x => x === INF ? '∞' : String(x);
  const cfURL = id => { const m = String(id).match(/^(\d+)([A-Z]\d?)$/); return m ? `https://codeforces.com/problemset/problem/${m[1]}/${m[2]}` : '#'; };

  /* shared SVG graph painter: nodes as .gn circles, edges as .ed lines with optional arrowheads and weights */
  function drawGraph(o) {
    const s = sv('svg', { viewBox: `0 0 ${o.W} ${o.H}`, style: `min-width:${Math.min(o.W, 520)}px`, role: 'img', 'aria-label': o.label || 'Graph drawing' });
    const R = 17;
    if (o.arrows) {
      const defs = sv('defs');
      [['', 'var(--muted)'], ['Hot', 'var(--accent)'], ['Cur', 'var(--cur)']].forEach(([k, col]) => {
        defs.append(sv('marker', { id: o.mid + k, viewBox: '0 0 10 8', refX: 9, refY: 4, markerWidth: 8, markerHeight: 7, orient: 'auto' }, sv('path', { d: 'M0,0 L10,4 L0,8 z', fill: col })));
      });
      s.append(defs);
    }
    o.edges.forEach(e => {
      const a = o.pos[e.u], b = o.pos[e.v], cls = e.cls || '';
      const mk = cls.includes('look') ? 'Cur' : cls.includes('tree') ? 'Hot' : '';
      if (e.u === e.v) {
        s.append(sv('path', { class: 'ed ' + cls, d: `M${a[0] - 8},${a[1] - R + 2} C${a[0] - 26},${a[1] - 52} ${a[0] + 26},${a[1] - 52} ${a[0] + 8},${a[1] - R + 2}`, 'marker-end': o.arrows ? `url(#${o.mid + mk})` : null }));
        return;
      }
      const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
      const x1 = a[0] + ux * R, y1 = a[1] + uy * R, x2 = b[0] - ux * (R + (o.arrows ? 3 : 0)), y2 = b[1] - uy * (R + (o.arrows ? 3 : 0));
      s.append(sv('line', { class: 'ed ' + cls, x1, y1, x2, y2, 'marker-end': o.arrows ? `url(#${o.mid + mk})` : null }));
      if (e.w !== undefined) {
        const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
        s.append(sv('rect', { x: mx - 11, y: my - 10, width: 22, height: 20, rx: 5, fill: 'var(--surface)', stroke: 'var(--line)' }));
        s.append(sv('text', { x: mx, y: my + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 12, 'font-weight': 700 }, e.w));
      }
    });
    o.pos.forEach((p, i) => {
      if (!p) return;
      const g = sv('g', { class: 'gn ' + ((o.nodeCls && o.nodeCls[i]) || ''), 'data-n': i }, sv('circle', { cx: p[0], cy: p[1], r: R }), sv('text', { x: p[0], y: p[1] }, i));
      if (o.onNode) { g.style.cursor = 'pointer'; g.addEventListener('click', () => o.onNode(i)); }
      if (o.sub && o.sub[i] !== undefined && o.sub[i] !== null) g.append(sv('text', { x: p[0], y: p[1] + 31, 'font-size': 12, style: 'fill:var(--muted)' }, o.sub[i]));
      s.append(g);
    });
    return s;
  }

  /* ---------- E0 lab: the Chakravyuh walker ---------- */
  function wChak(b) {
    const PRE = {
      rho: { a: [1, 2, 3, 4, 2, 3, 7, 8, -1, 7], pos: [[50, 55], [150, 55], [260, 55], [350, 115], [260, 175], [460, 115], [50, 250], [190, 250], [330, 250], [90, 175]] },
      tail: { a: [1, 2, 3, 4, 5, 6, 7, 4] },
      self: { a: [0, 0, 1, -1, 3] },
      perm: { a: [2, 0, 1, 4, 3, 5] }
    };
    let a = PRE.rho.a.slice(), pos = PRE.rho.pos;
    const inp = h('input', { type: 'text', value: a.join(', '), 'aria-label': 'Array a', style: 'min-width:16em' });
    const startSel = h('select', { 'aria-label': 'Start node' });
    const viz = h('div', { class: 'viz' }), tbl = h('div'), cap = h('p', { class: 'cap' }), sp = h('div');
    const stp = Stepper(sp, f => paint(f));
    function circlePos(n) {
      const W = 520, H = 280, cx = W / 2, cy = H / 2, r = Math.min(110, 30 + n * 9);
      return Array.from({ length: n }, (_, i) => [cx + r * Math.cos(-Math.PI / 2 + 2 * Math.PI * i / n), cy + r * Math.sin(-Math.PI / 2 + 2 * Math.PI * i / n)]);
    }
    function paint(f) {
      const edges = [];
      a.forEach((v, u) => { if (v !== -1) edges.push({ u, v, cls: (f && f.ecls && f.ecls[u]) || '' }); });
      const W = Math.max(...pos.map(p => p[0])) + 60, H = Math.max(...pos.map(p => p[1])) + 50;
      viz.innerHTML = '';
      viz.append(drawGraph({ W, H, pos, edges, arrows: true, mid: 'ahChak', nodeCls: f ? f.ncls : {}, sub: a.map(v => v === -1 ? '−1' : null), onNode: i => { startSel.value = i; walk(i); }, label: 'Directed graph where every node has at most one outgoing edge' }));
      tbl.innerHTML = '';
      if (f && f.ans) {
        const t = h('table', { class: 'mat dpt' });
        t.append(h('tr', {}, h('th', {}, 'i'), ...a.map((_, i) => h('th', {}, i))));
        t.append(h('tr', {}, h('th', {}, 'a[i]'), ...a.map((v, i) => h('td', { class: 'base' }, v))));
        t.append(h('tr', {}, h('th', {}, 'ans[i]'), ...f.ans.map((v, i) => h('td', { class: f.hot && f.hot.includes(i) ? 'cur' : v ? 'mt' : 'dim' }, v || '?'))));
        tbl.append(h('div', { class: 'tw' }, t));
      }
      if (f) { cap.textContent = f.msg; cap.className = 'cap' + (f.done ? ' good' : ''); }
    }
    function load(arr, p) {
      a = arr; pos = p || circlePos(a.length);
      startSel.innerHTML = ''; a.forEach((_, i) => startSel.append(h('option', { value: i, text: 'node ' + i })));
      stp.set([{ ncls: {}, msg: 'Click any node to walk from it, or run the O(n) algorithm to fill every answer at once. The number under a node marks a[i] = −1 (no outgoing edge).' }]);
    }
    function walk(v) {
      const F = [], seen = [v], ncls = {}, ecls = {};
      ncls[v] = 'cur';
      F.push({ ncls: { ...ncls }, ecls: {}, msg: `Start at ${v}. Seen so far: {${v}}, count 1.` });
      let cur = v;
      while (true) {
        const nx = a[cur];
        if (nx === -1) {
          const fin = {}; seen.forEach(x => fin[x] = 'hb');
          F.push({ ncls: fin, ecls: { ...ecls }, done: true, msg: `a[${cur}] = −1: a dead end, the walk stops. Answer for ${v}: ${seen.length} node${seen.length > 1 ? 's' : ''} (${seen.join(' → ')}). No cycle on this walk.` });
          break;
        }
        ecls[cur] = 'tree';
        if (seen.includes(nx)) {
          const k = seen.indexOf(nx), fin = {};
          seen.forEach((x, i) => fin[x] = i >= k ? 'hg' : 'hb');
          const cyc = seen.slice(k);
          const ec = { ...ecls }; cyc.forEach(x => ec[x] = 'look');
          F.push({ ncls: fin, ecls: ec, done: true, msg: `${cur} → ${nx}, but ${nx} is already seen: the walk would loop forever, so stop. Answer for ${v}: ${seen.length} = tail ${k} (amber) + cycle ${cyc.length} (green: ${cyc.join(' → ')} → ${nx}).` });
          break;
        }
        seen.push(nx); Object.keys(ncls).forEach(x => ncls[x] = 'hl'); ncls[nx] = 'cur'; cur = nx;
        F.push({ ncls: { ...ncls }, ecls: { ...ecls }, msg: `Follow the only edge to ${nx}. Seen: {${seen.join(', ')}}, count ${seen.length}. Each node has at most one way out, so there is never a choice to make.` });
      }
      stp.set(F);
    }
    function algo() {
      const n = a.length, ans = Array(n).fill(0), state = Array(n).fill(0), F = [];
      const snap = (msg, hot, extra) => {
        const ncls = {};
        state.forEach((s, i) => { if (s === 1) ncls[i] = 'gray'; else if (s === 2) ncls[i] = 'dn'; });
        (hot || []).forEach(i => ncls[i] = 'cur');
        F.push(Object.assign({ ncls, ecls: {}, ans: ans.slice(), hot, msg }, extra || {}));
      };
      snap('state: white = new, amber = on the walk in progress, green = finished. ans[] fills in as nodes finish. Total work O(n): every node joins one walk and is finished once.');
      for (let s = 0; s < n; s++) {
        if (state[s]) continue;
        const path = []; let u = s;
        while (u !== -1 && state[u] === 0) { state[u] = 1; path.push(u); snap(`New walk from ${s}: put ${u} on the path [${path.join(', ')}].`, [u]); u = a[u]; }
        if (u !== -1 && state[u] === 1) {
          const k = path.indexOf(u), cyc = path.slice(k);
          cyc.forEach(x => { ans[x] = cyc.length; state[x] = 2; });
          snap(`${path[path.length - 1]} points to ${u}, which is on this very walk: a new cycle [${cyc.join(' → ')}] of length ${cyc.length}. Every cycle node sees exactly the cycle, so each gets ${cyc.length}.`, cyc);
          path.length = k;
        } else if (u === -1) {
          snap(`${path[path.length - 1]} has a[i] = −1: the walk hits a dead end.`, [path[path.length - 1]]);
        } else {
          snap(`${path[path.length - 1]} points to ${u}, already finished with ans = ${ans[u]}. Reuse it: no need to walk on.`, [u]);
        }
        let nxt = u === -1 ? 0 : ans[u];
        for (let i = path.length - 1; i >= 0; i--) {
          const x = path[i]; nxt += 1; ans[x] = nxt; state[x] = 2;
          snap(a[x] === -1 ? `ans[${x}] = 1: it has no way out, so it reaches only itself.` : `Unwind the tail: ans[${x}] = 1 + ans[${a[x]}] = ${nxt}.`, [x]);
        }
      }
      const last = F[F.length - 1]; last.done = true; last.msg += ` Done: ans = [${ans.join(', ')}].`;
      stp.set(F);
    }
    const P = (label, key) => btn(label, () => { inp.value = PRE[key].a.join(', '); load(PRE[key].a.slice(), PRE[key].pos); });
    startSel.addEventListener('change', () => walk(+startSel.value));
    b.append(
      h('div', { class: 'row' }, h('label', {}, 'a = ', inp), btn('Draw', () => {
        const arr = inp.value.split(/[\s,;\[\]]+/).filter(x => x.length).map(Number);
        const n = arr.length;
        if (!n || n > 12 || arr.some(x => !Number.isInteger(x) || x < -1 || x >= n)) { cap.textContent = 'Use 1 to 12 whole numbers, each −1 or a node number from 0 to n − 1.'; cap.className = 'cap bad'; return; }
        load(arr, null);
      }, 'pri')),
      h('div', { class: 'row' }, h('span', { class: 'mini' }, 'Shapes: '), P('Two ρ shapes', 'rho'), P('Long tail', 'tail'), P('Self-loop and dead end', 'self'), P('Only cycles', 'perm')),
      h('div', { class: 'row' }, h('label', {}, 'Walk from ', startSel), btn('Walk', () => walk(+startSel.value)), btn('Run the O(n) algorithm', algo, 'pri')),
      viz, tbl, cap, sp);
    load(a, pos);
  }

  /* ---------- E2 lab: loop direction decides how many copies ---------- */
  function wKnapDir(b) {
    const PRE = {
      one: { items: [[2, 3]], W: 6 },
      two: { items: [[2, 3], [3, 4]], W: 7 },
      q4: { items: [[3, 5], [4, 7]], W: 10 }
    };
    let cfg = PRE.one;
    const mode = h('select', { 'aria-label': 'Variant' },
      h('option', { value: 'down', text: '0/1: capacity downward' }),
      h('option', { value: 'up', text: 'Unbounded: capacity upward' }),
      h('option', { value: 'two', text: '0/1/2 (your Q4): downward, 1 or 2 copies' }));
    const host = h('div'), cap = h('p', { class: 'cap' }), sp = h('div');
    const names = 'ABCDE';
    const comp = c => c.map((k, i) => k ? names[i] + (k > 1 ? '×' + k : '') : '').filter(Boolean).join(' ') || '–';
    const stp = Stepper(sp, f => {
      const t = h('table', { class: 'mat dpt' });
      t.append(h('tr', {}, h('th', {}, 'capacity c'), ...f.dp.map((_, c) => h('th', {}, c))));
      t.append(h('tr', {}, h('th', {}, 'before this item'), ...f.prev.map(v => h('td', { class: 'base' }, v))));
      t.append(h('tr', {}, h('th', {}, 'dp[c] now'), ...f.dp.map((v, c) => h('td', { class: c === f.c ? 'cur' : (f.src || []).includes(c) ? 'src' : f.touched[c] ? 'mt' : '' }, v, h('small', {}, comp(f.cm[c]))))));
      host.innerHTML = '';
      host.append(h('p', { class: 'mini' }, 'Items: ' + cfg.items.map(([w, v], i) => `${names[i]} (w ${w}, v ${v})`).join(', ') + `. W = ${cfg.W}. Green: already updated in this pass. Blue: the cell being read. Small text: the items inside that best value.`), h('div', { class: 'tw' }, t));
      cap.textContent = f.msg; cap.className = 'cap' + (f.done ? ' good' : f.bad ? ' bad' : '');
    });
    function run() {
      const md = mode.value, W = cfg.W, n = cfg.items.length;
      let dp = Array(W + 1).fill(0), cm = Array.from({ length: W + 1 }, () => Array(n).fill(0));
      const F = [];
      F.push({ dp: dp.slice(), prev: dp.slice(), cm: cm.map(x => x.slice()), c: -1, touched: [], msg: 'Every cell starts at 0: with no items, any capacity is worth nothing. Press Next to process the items one at a time.' });
      cfg.items.forEach(([w, v], it) => {
        const prev = dp.slice(), touched = [];
        const order = [];
        if (md === 'up') for (let c = w; c <= W; c++) order.push(c); else for (let c = W; c >= w; c--) order.push(c);
        order.forEach(c => {
          const opts = [[dp[c], null, 0]];
          opts.push([dp[c - w] + v, c - w, 1]);
          if (md === 'two' && c >= 2 * w) opts.push([dp[c - 2 * w] + 2 * v, c - 2 * w, 2]);
          let best = opts[0];
          opts.forEach(o => { if (o[0] > best[0]) best = o; });
          const src = opts.slice(1).map(o => o[1]);
          const reused = src.some(s => touched[s]);
          const parts = opts.slice(1).map(o => `dp[${o[1]}] + ${o[2] * v} = ${o[0]}`).join(', ');
          let msg = `Item ${names[it]}, c = ${c}: keep ${dp[c]}, or ${parts}.`;
          if (best[1] !== null) {
            const nc = cm[best[1]].slice(); nc[it] += best[2];
            dp[c] = best[0]; cm[c] = nc;
            msg += ` New best ${best[0]}.`;
          } else msg += ' Keep it.';
          if (reused) msg += ` dp[${src.find(s => touched[s])}] was already updated in this pass, so it already contains ${names[it]}: this adds another copy.`;
          touched[c] = true;
          F.push({ dp: dp.slice(), prev, cm: cm.map(x => x.slice()), c, src, touched: touched.slice(), bad: reused && md !== 'up', msg });
        });
      });
      const used = cm[W];
      F.push({ dp: dp.slice(), prev: dp.slice(), cm: cm.map(x => x.slice()), c: W, touched: [], done: true,
        msg: `Answer dp[${W}] = ${dp[W]} using ${comp(used)}. ` + (md === 'up' ? 'Upward reads cells this item already improved, so one item can be stacked again and again: unbounded supply.' : md === 'two' ? 'Downward means dp[c − w] and dp[c − 2w] still hold the "before this item" values, so at most 2 copies, exactly as Q4 asked.' : 'Downward means every read sees the row before this item, so each item is used at most once.') });
      stp.set(F);
    }
    mode.addEventListener('change', run);
    const P = (l, k) => btn(l, () => { cfg = PRE[k]; run(); });
    b.append(h('div', { class: 'row' }, h('label', {}, 'Variant: ', mode), btn('Run', run, 'pri')),
      h('div', { class: 'row' }, h('span', { class: 'mini' }, 'Items: '), P('one item (2, 3), W = 6', 'one'), P('two items, W = 7', 'two'), P('Q4-style, W = 10', 'q4')),
      host, cap, sp);
    run();
  }

  /* ---------- E3 lab: Dijkstra with a heap ---------- */
  function wDijk(b) {
    const pos = [[50, 150], [190, 55], [190, 245], [330, 150], [480, 245], [480, 55]];
    const E = [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1], [2, 3, 5], [3, 4, 3], [2, 4, 8], [4, 5, 1], [3, 5, 6]];
    const n = 6, adj = Array.from({ length: n }, () => []);
    E.forEach(([u, v, w]) => { adj[u].push([v, w]); adj[v].push([u, w]); });
    const srcSel = h('select', { 'aria-label': 'Source' }, ...pos.map((_, i) => h('option', { value: i, text: 'from ' + i })));
    const viz = h('div', { class: 'viz' }), info = h('div'), cap = h('p', { class: 'cap' }), sp = h('div');
    const ekey = (u, v) => u < v ? u + '-' + v : v + '-' + u;
    const stp = Stepper(sp, f => {
      const ncls = {};
      f.fin.forEach((x, i) => { if (x) ncls[i] = 'dn'; });
      if (f.u !== null && f.u !== undefined) ncls[f.u] = 'cur';
      if (f.v !== null && f.v !== undefined) ncls[f.v] = 'hl';
      viz.innerHTML = '';
      viz.append(drawGraph({ W: 530, H: 290, pos, mid: 'ahDij', arrows: false,
        edges: E.map(([u, v, w]) => ({ u, v, w, cls: f.look === ekey(u, v) ? 'look' : f.tree && f.tree.includes(ekey(u, v)) ? 'tree' : '' })),
        nodeCls: ncls, sub: f.dist.map(fmtD), label: 'Weighted undirected graph for Dijkstra' }));
      const t = h('table', { class: 'mat dpt' });
      t.append(h('tr', {}, h('th', {}, 'node'), ...f.dist.map((_, i) => h('th', {}, i))));
      t.append(h('tr', {}, h('th', {}, 'dist'), ...f.dist.map((d, i) => h('td', { class: i === f.v ? 'cur' : f.fin[i] ? 'mt' : d === INF ? 'dim' : '' }, fmtD(d)))));
      t.append(h('tr', {}, h('th', {}, 'from'), ...f.par.map(p => h('td', { class: 'base' }, p === null ? '–' : p))));
      info.innerHTML = '';
      info.append(h('div', { class: 'tw' }, t), h('div', { class: 'row' }, h('span', { class: 'mini' }, 'Heap (smallest first): '), ...(f.heap.length ? f.heap.slice().sort((x, y) => x[0] - y[0] || x[1] - y[1]).map(([d, u]) => h('span', { class: 'chip' }, `(${d}, ${u})`)) : [h('span', { class: 'chip z' }, 'empty')])));
      cap.textContent = f.msg; cap.className = 'cap' + (f.done ? ' good' : '');
    });
    function run() {
      const s = +srcSel.value, dist = Array(n).fill(INF), par = Array(n).fill(null), fin = Array(n).fill(false), F = [];
      let heap = [[0, s]]; dist[s] = 0;
      const snap = (msg, extra) => F.push(Object.assign({ dist: dist.slice(), par: par.slice(), fin: fin.slice(), heap: heap.map(x => x.slice()), u: null, v: null, msg }, extra || {}));
      snap(`dist[${s}] = 0, every other distance ∞. The heap holds (distance, node) pairs; we always pop the smallest.`);
      while (heap.length) {
        heap.sort((x, y) => x[0] - y[0] || x[1] - y[1]);
        const [d, u] = heap.shift();
        if (d > dist[u]) { snap(`Pop (${d}, ${u}): stale, because dist[${u}] is already ${dist[u]} < ${d}. Skip it.`, { u }); continue; }
        fin[u] = true;
        snap(`Pop (${d}, ${u}): the closest unfinished node. With no negative edges nothing found later can be cheaper, so dist[${u}] = ${d} is final (green).`, { u });
        adj[u].forEach(([v, w]) => {
          if (fin[v]) return;
          if (d + w < dist[v]) {
            const old = dist[v]; dist[v] = d + w; par[v] = u; heap.push([dist[v], v]);
            snap(`Relax ${u}–${v} (weight ${w}): ${d} + ${w} = ${d + w} < ${fmtD(old)}, so dist[${v}] = ${d + w} and push (${d + w}, ${v}).` + (old !== INF ? ' The old pair for ' + v + ' stays in the heap and will be skipped as stale.' : ''), { u, v, look: ekey(u, v) });
          } else {
            snap(`Relax ${u}–${v} (weight ${w}): ${d} + ${w} = ${d + w} is not better than ${fmtD(dist[v])}. No change.`, { u, v, look: ekey(u, v) });
          }
        });
      }
      const tree = par.map((p, i) => p === null ? null : ekey(p, i)).filter(Boolean);
      snap(`Heap empty: done. Thick edges form the shortest-path tree; follow "from" backwards for any route. Each push and pop costs O(log V), so O((V + E) log V) overall.`, { tree, done: true });
      stp.set(F);
    }
    srcSel.addEventListener('change', run);
    b.append(h('div', { class: 'row' }, h('label', {}, 'Source: ', srcSel), btn('Run', run, 'pri')), viz, info, cap, sp);
    run();
  }

  /* ---------- E1 lab: days to the end-sem and what to do now ---------- */
  function wEndPlan(b) {
    const KEY = 'ada-endsem-date';
    const inp = h('input', { type: 'date', 'aria-label': 'End-sem date', value: ls2Get(KEY, '') || '' });
    const out = h('div');
    const PH = [
      [15, 'Build', 'One stop a day in this order: 10 (DP patterns), 12 (Graphs II), 13 (monotonic stacks), 14 (toolkit). Two Exam-rung Ladder problems a day. One three-rung mock every four days.'],
      [8, 'Climb', 'Three ladder problems a day at 1500–1600. A three-rung mock every two or three days. Twenty minutes of quick review mode on stops 2–5 for any written part.'],
      [3, 'Sharpen', 'A mock every other day. Clear the My mistakes deck daily. Re-code every missed mock problem from a blank file the next day. Read the cheat sheet once.'],
      [1, 'Rest', 'One 1400 warm-up only. Quick review mode, then the routine in stop 14. Sleep a full night: an all-nighter costs more marks than it earns.'],
      [0, 'Exam day', 'Read every problem, then follow the routine: bank the sure ones, brute force before cleverness on the last three, stress test before trusting a fast idea.']
    ];
    function paint() {
      out.innerHTML = '';
      const v = inp.value;
      if (!v) { out.append(h('p', { class: 'cap' }, 'No date set. Until it’s announced, plan as if it is three weeks away: start with the Build phase below.'), table(-1)); return; }
      const today = new Date(); today.setHours(0, 0, 0, 0);
      const d = new Date(v + 'T00:00:00');
      const days = Math.round((d - today) / 86400000);
      if (days < 0) { out.append(h('p', { class: 'cap' }, `That date was ${-days} day${days === -1 ? '' : 's'} ago. Change it if the exam moved.`)); return; }
      const ph = PH.find(p => days >= p[0]);
      out.append(h('div', { class: 'row' }, h('div', { class: 'stat' }, 'Days left ', h('b', {}, days)), h('div', { class: 'stat' }, 'Phase ', h('b', {}, ph[1]))), h('p', { class: 'cap good' }, ph[2]), table(PH.indexOf(ph)));
    }
    function table(on) {
      const t = h('table', {}, h('tr', {}, h('th', {}, 'Days left'), h('th', {}, 'Phase'), h('th', {}, 'Each day')));
      PH.forEach((p, i) => t.append(h('tr', { style: i === on ? 'font-weight:700' : '' }, h('td', {}, i === 0 ? '15 or more' : i === 1 ? '8–14' : i === 2 ? '3–7' : i === 3 ? '1–2' : '0'), h('td', {}, p[1]), h('td', {}, p[2]))));
      return h('div', { class: 'tw' }, t);
    }
    inp.addEventListener('change', () => { ls2Set(KEY, inp.value); paint(); });
    b.append(h('div', { class: 'row' }, h('label', {}, 'End-sem date: ', inp), btn('Clear', () => { inp.value = ''; ls2Set(KEY, ''); paint(); })), out);
    paint();
  }

  Object.assign(WIDGETS, { chak: wChak, knapdir: wKnapDir, dijk: wDijk, endplan: wEndPlan });

  /* ---------- quizzes ---------- */
  QUIZ.e0 = [
    { q: 'Every node has at most one outgoing edge. Starting anywhere and following edges, the walk…', o: ['can branch, so you need BFS', 'either stops at a dead end or runs into exactly one cycle and loops there', 'always visits every node', 'always ends at node 0'], a: 1, why: 'With one way out of each node there is never a choice: a straight tail, then a dead end or a cycle. The ρ shape.' },
    { q: 'a = [1, 2, 0, 2, −1, 4]. How many distinct nodes can you reach from node 3, counting 3?', o: ['3', '4', '5', '6'], a: 1, why: '3 → 2, and 2 sits on the cycle 2 → 0 → 1 → 2 of length 3. Tail 1 + cycle 3 = 4.' },
    { q: 'Subtask 1 has n ≤ 10³. Walking from every node with a seen-set costs about…', o: ['10³ steps', '10⁶ steps: comfortably fast', '10⁹ steps: too slow', 'It never finishes on a cycle'], a: 1, why: 'Each walk is at most n steps and there are n walks: n² = 10⁶. That alone banks the first subtask.' },
    { q: '0/1/2 knapsack with one dp array. Which way does the capacity loop run?', o: ['Upward, so a copy can build on the previous copy', 'Downward, so dp[c − w] and dp[c − 2w] still describe the items before this one', 'Either way gives the same answer', 'It needs a 2D table'], a: 1, why: 'Upward reads cells this item already improved, allowing unlimited copies. Downward caps it at the copies you try explicitly.' },
    { q: 'The quickest correct way to turn 0/1/2 knapsack into a problem you already know:', o: ['Sort by value per weight and take greedily', 'List every item twice, then run plain 0/1 knapsack', 'Run unbounded knapsack', 'Use BFS over capacities'], a: 1, why: 'Two identical copies are just two items. 2n items, same O(nW) table, nothing new to invent.' }
  ];
  QUIZ.e1 = [
    { q: 'The final three end-sem problems are CF 1400, 1500 and 1600. What should you guarantee on the 1600?', o: ['A full solution or nothing', 'At least a correct brute-force submission for the small subtask', 'Skip it entirely', 'Write the clever idea first and test later'], a: 1, why: 'A correct slow solution scores the small tests. Full marks on the 1600 are a bonus; zero is avoidable.' },
    { q: 'A subtask says n ≤ 20. Which brute force fits?', o: ['Try all 2ⁿ subsets', 'Try all n! orders', 'Nothing: it needs O(n log n)', 'Binary search'], a: 0, why: '2²⁰ ≈ 10⁶. 20! is about 2·10¹⁸: far too many.' },
    { q: 'Stress testing means…', o: ['Submitting many times', 'Running your fast solution and a brute force on many tiny random inputs and comparing', 'Testing only the sample input', 'Timing your code on the largest input'], a: 1, why: 'Tiny random inputs find the edge case you didn’t think of, and the brute force tells you the right answer for it.' },
    { q: 'Reading 2·10⁵ numbers in Python on Codeforces, the safest way is…', o: ['input() in a loop', 'sys.stdin.buffer.read().split() once, then walk an index', 'eval(input())', 'One print per number'], a: 1, why: 'One read and one write. Calling input() hundreds of thousands of times can cost a time limit on its own.' },
    { q: 'Fifteen minutes on one problem, no new idea. What now?', o: ['Keep going: you’re close', 'Submit a brute force if you have one, then move to another problem and come back', 'Restart the problem from scratch', 'Stop the exam'], a: 1, why: 'Bank what you can, then spend time where it buys marks. Coming back fresh often shows the observation.' }
  ];
  QUIZ.e2 = [
    { q: 'n gifts, each with a price and a joy value. Budget B. Each gift can be bought once. Maximise joy.', o: ['Unbounded knapsack', '0/1 knapsack', 'Fewest coins', 'Greedy by joy per price'], a: 1, why: 'Items, capacity, maximise value, each once: 0/1 knapsack with a downward capacity loop.' },
    { q: 'Unlimited coins. How many different collections (order ignored) make the amount?', o: ['Coins in the outer loop, amount upward inside', 'Amount in the outer loop, coins inside', 'Downward loop', 'max instead of +'], a: 0, why: 'Coins outside means each collection is built in one fixed coin order, so it is counted once (LC 518).' },
    { q: 'Count ordered sequences of steps from {1, 3, 4} that add up to n.', o: ['Coins outside, amount inside', 'Amount outside, steps inside', 'Subset sum', '0/1 knapsack'], a: 1, why: 'Order matters, so every last step is tried at every total: amount outside (LC 377, Climbing Stairs generalised).' },
    { q: 'Split stones into two groups with the smallest possible difference of sums.', o: ['Sort and alternate', 'Subset sum: which totals up to sum/2 are reachable?', 'Dijkstra', 'Unbounded knapsack'], a: 1, why: 'The best split puts one group as close to half the total as possible: a True/False table over sums (LC 1049).' },
    { q: 'Same 0/1 knapsack code, but the capacity loop runs upward. What does it now solve?', o: ['Still 0/1', 'Unbounded knapsack', 'It crashes', 'Bounded with 2 copies'], a: 1, why: 'Upward lets dp[c − w] already contain this item, so it can be reused without limit. Direction is the whole difference.' },
    { q: 'Sum must be exactly T and you maximise the count of items. How do you start the table?', o: ['All zeros', 'dp[0] = 0 and every other cell −1 (or −∞) for “impossible”', 'All ones', 'dp[T] = 0'], a: 1, why: 'Zeros would treat unreachable sums as free. Mark them impossible and skip them in the transition.' },
    { q: 'Memo best(i, c) reads only best(i + 1, ·). To tabulate it, fill i…', o: ['from 0 up to n − 1', 'from n − 1 down to 0 (row n is the base case)', 'in any order', 'by capacity first'], a: 1, why: 'A cell must be filled after the cells it reads. Then one row is enough, swept downward over c.' }
  ];
  QUIZ.e3 = [
    { q: 'Kahn’s algorithm outputs fewer than n vertices. What does that tell you?', o: ['The graph is disconnected', 'There is a cycle: those vertices never reach in-degree 0', 'The graph is a tree', 'Nothing'], a: 1, why: 'A vertex on a cycle always has an in-edge from the cycle, so it is never queued.' },
    { q: 'Why is BFS wrong for shortest paths with weights?', o: ['It is too slow', 'It minimises the number of edges, and a longer route can weigh less', 'It cannot handle cycles', 'It needs a sorted graph'], a: 1, why: 'Edge 0–1 of weight 4 versus 0–2–1 of weight 1 + 2 = 3: fewer edges, more weight.' },
    { q: 'In heap-based Dijkstra, when is a node’s distance final?', o: ['When it is first pushed', 'When it is popped with d equal to dist[node]', 'When all its neighbours are pushed', 'At the very end only'], a: 1, why: 'A node can be pushed several times as better routes appear. The first pop is the smallest; later pops are stale.' },
    { q: 'You pop (7, u) but dist[u] is already 5. You should…', o: ['Set dist[u] = 7', 'Skip it: it is a stale entry', 'Stop the algorithm', 'Push it back'], a: 1, why: 'Lazy deletion: old pairs stay in the heap and are ignored when they surface.' },
    { q: 'In the Dijkstra lab graph, what is dist from 0 to 3?', o: ['5', '4', '6', '3'], a: 1, why: '0 → 2 (1), 2 → 1 (2), 1 → 3 (1): total 4. The direct-looking 0 → 1 → 3 costs 5.' },
    { q: 'Dijkstra on a graph with one negative edge:', o: ['Always correct', 'Can finalise a node too early and give a wrong distance', 'Loops forever', 'Becomes BFS'], a: 1, why: 'The “closest popped node is final” argument needs every edge ≥ 0.' },
    { q: 'In Kruskal, union(u, v) returns False for the next cheapest edge. You…', o: ['Add it anyway', 'Skip it: u and v are already connected, so it would close a cycle', 'Stop', 'Restart with Prim'], a: 1, why: 'An MST has no cycles; union-find answers “already connected?” in near-constant time.' }
  ];
  

  /* ---------- drills ---------- */
  BLANKS.push(
    { t: 'Graphs II', p: 'Dijkstra with lazy deletion: skip stale pairs, relax with the popped distance.', c: 'while heap:\n    d, u = heapq.{{heappop}}(heap)\n    if d {{>}} dist[u]:\n        continue\n    for v, w in adj[u]:\n        if d + w < dist[v]:\n            dist[v] = {{d + w}}\n            heapq.heappush(heap, ({{dist[v]}}, v))' },
    { t: 'Graphs II', p: 'Kahn: queue a vertex the moment its last prerequisite is done.', c: 'for v in adj[u]:\n    indeg[v] {{-=}} 1\n    if indeg[v] == {{0}}:\n        q.append(v)' },
    { t: 'Knapsack family', p: '0/1 knapsack in one row: the capacity loop runs downward.', c: 'for w, v in zip(weights, values):\n    for c in range({{W}}, {{w - 1}}, {{-1}}):\n        dp[c] = max(dp[c], dp[{{c - w}}] + v)' }
  );
  BUGS.push(
    { t: 'Knapsack family', p: '0/1/2 knapsack with one item (w 2, v 3) and W = 6 returns 9, but only two copies exist (answer 6).', c: ['dp = [0] * (W + 1)', 'for w, v in zip(weights, values):', '    for c in range(w, W + 1):', '        dp[c] = max(dp[c], dp[c - w] + v)', '        if c >= 2 * w:', '            dp[c] = max(dp[c], dp[c - 2 * w] + 2 * v)'], a: [2], e: 'The loop runs upward, so dp[c − w] already contains this item and copies stack: three copies give 9. Sweep capacity downward.', f: '    for c in range(W, w - 1, -1):' },
    { t: 'Graphs II', p: 'Dijkstra gives dist[1] = 4 from node 0, but 0 → 2 → 1 costs 1 + 2 = 3.', c: ['dist = [INF] * n; dist[src] = 0', 'heap, done = [(0, src)], {src}', 'while heap:', '    d, u = heapq.heappop(heap)', '    for v, w in adj[u]:', '        if v not in done:', '            done.add(v)', '            dist[v] = d + w', '            heapq.heappush(heap, (dist[v], v))'], a: [5, 6], e: 'Marking a node done when it is first pushed freezes the first route found. That is right for BFS, wrong with weights. Compare d + w < dist[v] and treat a node as final when it is popped.', f: '        if d + w < dist[v]:\n            dist[v] = d + w\n            heapq.heappush(heap, (dist[v], v))' },
    { t: 'Functional graphs', p: 'brute([0]) never returns: node 0 points to itself.', c: ['def brute(a):', '    ans = []', '    for v in range(len(a)):', '        count, u = 0, v', '        while u != -1:', '            count += 1', '            u = a[u]', '        ans.append(count)', '    return ans'], a: [4], e: 'Following edges until −1 never stops on a cycle. Keep a set of seen nodes, stop on a repeat, and answer with the size of the set.', f: '        seen, u = set(), v\n        while u != -1 and u not in seen:\n            seen.add(u)\n            u = a[u]\n        ans.append(len(seen))' }
  );
})();
