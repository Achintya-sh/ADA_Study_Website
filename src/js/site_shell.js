/* ===== ADASiteShell: Multi-Page Atlas, Workbench Split View, Command Hub & ⌘K Search ===== */
(function () {
  var STOPS_CATALOG = [
    { id: 'ch0', num: '0', title: 'Prerequisites primer', group: 'found', kind: 'stop', ladTopic: 'arr', keywords: 'python arrays loops recursion indexing dicts sets' },
    { id: 'b0', num: '0.5', title: 'Tracing code by hand', group: 'found', kind: 'stop', ladTopic: 'arr', keywords: 'dry run trace invariants table' },
    { id: 'ch1', num: '1', title: 'Problem-solving foundations', group: 'found', kind: 'stop', ladTopic: 'arr', keywords: 'brute force constraints edge cases subtasks' },
    { id: 'b1', num: '1.5', title: 'Growth, limits and induction', group: 'found', kind: 'stop', ladTopic: 'arr', keywords: 'induction logarithms geometric series' },
    { id: 'ch2', num: '2', title: 'Complexity analysis', group: 'found', kind: 'stop', ladTopic: 'arr', keywords: 'big o omega theta recurrence master theorem' },
    { id: 'ch14', num: '14', title: 'Contest toolkit', group: 'found', kind: 'stop', ladTopic: 'arr', keywords: 'prefix sums difference array two pointers sliding window binary search on answer bisect bitmask' },
    { id: 'ch16', num: '16', title: 'Contest readiness', group: 'found', kind: 'stop', ladTopic: 'arr', keywords: 'constraints to algorithm python pitfalls recursion limit template sheet explain aloud mock' },
    { id: 'ch17', num: '17', title: 'Appendix: beyond the outline', group: 'found', kind: 'stop', ladTopic: 'arr', keywords: 'merge sort inversions amortised analysis hashing lca scc bridges segment tree' },
    { id: 'b2', num: '2.5', title: 'Swaps, pointers and partitions', group: 'trees', kind: 'stop', ladTopic: 'sort', keywords: 'partition lomuto hoare two pointers' },
    { id: 'ch3', num: '3', title: 'Quick Sort', group: 'trees', kind: 'stop', ladTopic: 'sort', keywords: 'quicksort pivot partition quickselect dutch national flag' },
    { id: 'b3', num: '3.5', title: 'Names, references, linked lists', group: 'trees', kind: 'stop', ladTopic: 'bst', keywords: 'pointers references nodes recursion' },
    { id: 'ch4', num: '4', title: 'Binary Search Trees', group: 'trees', kind: 'stop', ladTopic: 'bst', keywords: 'bst insert delete validate inorder lca' },
    { id: 'b4', num: '4.5', title: 'Complete trees and priority queues', group: 'trees', kind: 'stop', ladTopic: 'heap', keywords: 'complete binary tree array indexing parent child' },
    { id: 'ch5', num: '5', title: 'Heaps', group: 'trees', kind: 'stop', ladTopic: 'heap', keywords: 'heapq min heap max heap sift up sift down top k median' },
    { id: 'ch13', num: '13', title: 'Monotonic stacks and queues', group: 'trees', kind: 'stop', ladTopic: 'mono', keywords: 'monotonic stack next greater element histogram sliding window deque' },
    { id: 'b5', num: '5.5', title: 'Counting choices', group: 'bt', kind: 'stop', ladTopic: 'bt', keywords: 'permutations subsets decision tree' },
    { id: 'ch6', num: '6', title: 'Backtracking', group: 'bt', kind: 'stop', ladTopic: 'bt', keywords: 'backtracking subsets permutations n queens pruning' },
    { id: 'b6', num: '6.5', title: 'Pairs, sets and grids', group: 'graph', kind: 'stop', ladTopic: 'graph', keywords: 'grid neighbours visited set' },
    { id: 'ch7', num: '7', title: 'Graphs: concepts and representation', group: 'graph', kind: 'stop', ladTopic: 'graph', keywords: 'adjacency list matrix directed undirected degree' },
    { id: 'b7', num: '7.5', title: 'One loop, two bags', group: 'graph', kind: 'stop', ladTopic: 'graph', keywords: 'stack queue lifo fifo' },
    { id: 'ch8', num: '8', title: 'DFS and BFS', group: 'graph', kind: 'stop', ladTopic: 'graph', keywords: 'dfs bfs connected components shortest path bipartite cycle functional graph chakravyuh' },
    { id: 'ch12', num: '12', title: 'Graphs II: order, cycles, weights', group: 'graph', kind: 'stop', ladTopic: 'g2', keywords: 'topological sort kahn dijkstra bellman ford floyd warshall mst kruskal prim union find dsu' },
    { id: 'b8', num: '8.5', title: 'Caches and greedy choices', group: 'dp', kind: 'stop', ladTopic: 'dp', keywords: 'memoization overlapping subproblems optimal substructure' },
    { id: 'ch9', num: '9', title: 'Dynamic Programming I', group: 'dp', kind: 'stop', ladTopic: 'dp', keywords: '1d dp climbing stairs house robber coin change lis' },
    { id: 'b9', num: '9.5', title: 'Prefixes and 2D tables', group: 'dp', kind: 'stop', ladTopic: 'dp', keywords: '2d grid table state transitions' },
    { id: 'ch10', num: '10', title: 'Dynamic Programming II (2D)', group: 'dp', kind: 'stop', ladTopic: 'dp', keywords: 'knapsack 0/1 unbounded lcs edit distance space optimisation' },
    { id: 'ch11', num: '11', title: 'Greedy algorithms', group: 'dp', kind: 'stop', ladTopic: 'greedy', keywords: 'greedy exchange argument intervals scheduling fractional knapsack' },
    { id: 'ch15', num: '15', title: 'Bridges: tools you know, combined', group: 'dp', kind: 'stop', ladTopic: 'dp', keywords: 'tree dp dag dp binary search + graph dsu two heaps trie' },
    { id: 'b10', num: '10.5', title: 'Choosing the technique', group: 'exam', kind: 'stop', ladTopic: 'dp', keywords: 'decision tree complexity table' },
    { id: 'ladder', num: 'L', title: 'The Ladder (380 Problems & Vault)', group: 'ladder', kind: 'ladder', ladTopic: 'all', keywords: 'codeforces leetcode cses vault xp rank mocks' },
    { id: 'mock', num: 'X1', title: 'Mock quiz exam', group: 'exam', kind: 'exam', keywords: '20 question mock test' },
    { id: 'drills', num: 'X2', title: 'Syntax recall drills', group: 'exam', kind: 'exam', keywords: 'fill in the blank python syntax' },
    { id: 'bugs', num: 'X3', title: 'Spot the bug', group: 'exam', kind: 'exam', keywords: 'bug hunt debugging off by one' },
    { id: 'order', num: 'X4', title: 'Put the lines in order', group: 'exam', kind: 'exam', keywords: 'parsons puzzles line ordering' },
    { id: 'mistakes', num: 'X5', title: 'My mistakes', group: 'exam', kind: 'exam', keywords: 'spaced repetition mistake deck' },
    { id: 'practice', num: 'X6', title: 'Practice problems', group: 'exam', kind: 'exam', keywords: 'curated problem list' },
    { id: 'cards', num: 'X7', title: 'Flashcards and glossary', group: 'exam', kind: 'exam', keywords: 'flashcards definitions terms' },
    { id: 'cheat', num: 'X8', title: 'Cheat sheet', group: 'exam', kind: 'exam', keywords: 'templates summary complexities' }
  ];

  var EXAM_IDS = { mock: 1, drills: 1, bugs: 1, order: 1, mistakes: 1, practice: 1, cards: 1, cheat: 1 };
  var CATALOG_BY_ID = {};
  STOPS_CATALOG.forEach(function (it) { CATALOG_BY_ID[it.id] = it; });

  function escHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function detectPageContext() {
    if (typeof document !== 'undefined' && document.body && document.body.dataset && document.body.dataset.pageKind) {
      return document.body.dataset.pageKind; // 'root' | 'stop' | 'exam'
    }
    if (typeof location !== 'undefined' && location.pathname) {
      if (location.pathname.indexOf('/stops/') !== -1) return 'stop';
      if (location.pathname.indexOf('/exam/') !== -1) return 'exam';
    }
    return 'root';
  }

  function resolveInternalHref(hashOrId, fromContext) {
    var ctx = fromContext || detectPageContext();
    var raw = String(hashOrId || '').trim();
    if (!raw) return '#';
    var id = raw.charAt(0) === '#' ? raw.slice(1) : raw;

    // Legacy dissolved stop mapping
    var legacyMap = { c1: 'ch14', c2: 'ch8', c3: 'ch10', c4: 'ch11', c5: 'ladder', e0: 'ch8', e1: 'ch14', e2: 'ch10', e3: 'ch12', e4: 'ladder' };
    if (legacyMap[id]) id = legacyMap[id];

    var prefix = (ctx === 'stop' || ctx === 'exam') ? '../' : '';

    if (id === 'hub' || id === 'top') return prefix + 'hub.html';
    if (id === 'ladder' || id.indexOf('v-') === 0) {
      return prefix + 'ladder.html' + (id.indexOf('v-') === 0 ? '#' + id : '');
    }
    if (EXAM_IDS[id]) {
      return (ctx === 'exam' ? '' : prefix + 'exam/') + id + '.html';
    }
    if (/^(ch\d+|b\d+)$/.test(id)) {
      return (ctx === 'stop' ? '' : prefix + 'stops/') + id + '.html';
    }
    return '#' + id;
  }

  function getLadderArray() {
    if (typeof window === 'undefined') return [];
    if (Array.isArray(window.LADDER2)) return window.LADDER2;
    if (Array.isArray(window.LADDER)) return window.LADDER;
    if (window.LADDER && typeof window.LADDER === 'object') {
      var flat = [];
      Object.keys(window.LADDER).forEach(function (topic) {
        var list = window.LADDER[topic];
        if (Array.isArray(list)) {
          list.forEach(function (p) {
            flat.push({ k: String(p.id), t: p.id + '. ' + p.t, src: 'LC', topic: topic, pat: p.p || '' });
          });
        }
      });
      return flat;
    }
    return [];
  }

  function searchCorpus(query, fromContext) {
    var q = String(query || '').trim().toLowerCase();
    if (!q) return [];
    var ctx = fromContext || detectPageContext();
    var results = [];

    STOPS_CATALOG.forEach(function (item) {
      var hay = (item.num + ' ' + item.title + ' ' + item.keywords + ' ' + item.id).toLowerCase();
      if (hay.indexOf(q) !== -1) {
        results.push({
          kind: item.kind,
          id: item.id,
          badge: item.num,
          title: item.title,
          sub: item.group.toUpperCase(),
          href: resolveInternalHref('#' + item.id, ctx)
        });
      }
    });

    var ladder = getLadderArray();
    ladder.forEach(function (row) {
      var title = row.t || row.name || row.title || row[1] || '';
      var pat = row.pat || row.pattern || row[3] || '';
      var topic = row.topic || row.t || row[2] || '';
      var id = String(row.k || row.id || row.key || row[0] || '');
      var hay = (id + ' ' + title + ' ' + pat + ' ' + topic).toLowerCase();
      if (hay.indexOf(q) !== -1 && results.length < 35) {
        var cleanFilter = title.replace(/^(CF\s+\S+\s+|CSES\s+|\d+\.\s+)/i, '').trim() || title;
        var ladHref = (row.orig && row.u && String(row.u).indexOf('#v-') === 0)
          ? resolveInternalHref(row.u, ctx)
          : (resolveInternalHref('#ladder', ctx) + '?q=' + encodeURIComponent(cleanFilter));
        results.push({
          kind: 'ladder',
          id: id,
          badge: row.src || 'LADDER',
          title: title + (pat ? ' — ' + pat : ''),
          sub: 'Ladder · ' + String(topic).toUpperCase(),
          href: ladHref
        });
      }
    });

    return results;
  }

  function buildStopTocData(sectionEl) {
    if (!sectionEl || typeof sectionEl.querySelectorAll !== 'function') return [];
    var items = [];
    var idx = 0;
    var quizIdx = 0;
    var ideaIdx = 0;
    var nodes = sectionEl.querySelectorAll('h3, .box.idea .lbl, .lab, .quiz');
    Array.prototype.forEach.call(nodes, function (node) {
      idx++;
      var label = '';
      if (node.tagName === 'H3') {
        label = (node.textContent || '').trim();
      } else if (node.classList && node.classList.contains('lbl')) {
        ideaIdx++;
        label = ideaIdx === 1 ? 'Big Idea' : 'Big Idea #' + ideaIdx;
        node = node.parentElement || node;
      } else if (node.classList && node.classList.contains('lab')) {
        var rawLabTitle = node.getAttribute('data-title') || node.getAttribute('data-w') || 'Interactive';
        label = rawLabTitle.indexOf('Lab') === 0 ? rawLabTitle : ('Lab: ' + rawLabTitle);
      } else if (node.classList && node.classList.contains('quiz')) {
        quizIdx++;
        var qHead = node.querySelector && node.querySelector('.qhead strong');
        var qTitle = qHead ? (qHead.textContent || '').trim() : 'Check Yourself Quiz';
        label = quizIdx === 1 ? qTitle : (qTitle + ' #' + quizIdx);
      }
      if (!label) return;
      if (!node.id) {
        node.id = (sectionEl.id || 'sec') + '-sub-' + idx;
      }
      items.push({ id: node.id, label: label });
    });
    return items;
  }

  /* ---------- Live DOM Docking for Split Workbench (Code, Labs, Quiz) ---------- */
  var activeWbTab = 'code';
  var dockedItems = []; // [{ node, placeholder }]

  function restoreDockedNodes() {
    while (dockedItems.length > 0) {
      var entry = dockedItems.pop();
      if (entry && entry.node && entry.placeholder && entry.placeholder.parentNode) {
        entry.placeholder.parentNode.replaceChild(entry.node, entry.placeholder);
      }
    }
  }

  function getActiveStageSection() {
    if (typeof document === 'undefined') return null;
    var stage = document.getElementById('activeStopStage');
    if (stage && typeof stage.querySelector === 'function') {
      return stage.querySelector('section.topic');
    }
    return document.querySelector('main section.topic');
  }

  function inferCodeBlockMeta(pre, index) {
    var detailsParent = pre.closest ? pre.closest('details') : null;
    var summaryText = '';
    if (detailsParent) {
      var sumEl = detailsParent.querySelector('summary');
      if (sumEl) summaryText = (sumEl.textContent || '').trim();
    }
    var headingText = '';
    var cur = detailsParent || pre;
    while (cur && cur.previousElementSibling) {
      cur = cur.previousElementSibling;
      if (cur.tagName === 'H3' || cur.tagName === 'H4') {
        headingText = (cur.textContent || '').trim();
        break;
      }
      if (cur.querySelector) {
        var innerH = cur.querySelector('h3, h4');
        if (innerH) {
          headingText = (innerH.textContent || '').trim();
          break;
        }
      }
    }
    if (!headingText && pre.parentElement) {
      var pH = pre.parentElement.querySelector('h4, h3, .lvl');
      if (pH) headingText = (pH.textContent || '').trim();
    }
    var codeEl = pre.querySelector ? pre.querySelector('code') : null;
    var rawText = codeEl ? (codeEl.textContent || '') : (pre.textContent || '');
    var fnMatch = rawText.match(/^\s*(?:def|class)\s+([A-Za-z_]\w*)/m);
    var title = summaryText || headingText || (fnMatch ? ('def ' + fnMatch[1] + '(…)') : ('Template #' + (index + 1)));
    return {
      title: title,
      isSpoiler: !!detailsParent,
      codeHtml: codeEl ? codeEl.innerHTML : pre.innerHTML,
      rawText: rawText.replace(/\bCopy\s*$/, '').trim()
    };
  }

  function dockElementsIntoWorkbench(elementsList, bodyEl, kindLabel) {
    Array.prototype.forEach.call(elementsList, function (node, idx) {
      if (!node || !node.parentNode) return;
      var title = node.getAttribute('data-title') ||
        (node.querySelector && node.querySelector('.qhead strong') && node.querySelector('.qhead strong').textContent) ||
        (kindLabel + ' #' + (idx + 1));

      var placeholder = document.createElement('div');
      placeholder.className = 'wb-docked-placeholder';
      placeholder.innerHTML = '<span>⚡ <strong>' + escHtml(title) + '</strong> is docked in the Split Workbench →</span>' +
        '<button type="button" class="stb-btn wb-restore-inline-btn">Restore inline</button>';

      node.parentNode.replaceChild(placeholder, node);
      dockedItems.push({ node: node, placeholder: placeholder });

      var restoreBtn = placeholder.querySelector('.wb-restore-inline-btn');
      if (restoreBtn) {
        restoreBtn.addEventListener('click', function () {
          toggleWorkbench(false);
        });
      }

      var wrapper = document.createElement('div');
      wrapper.className = 'wb-item';
      wrapper.appendChild(node);
      bodyEl.appendChild(wrapper);
    });
  }

  function renderWorkbenchTab(tabName) {
    activeWbTab = tabName || activeWbTab || 'code';
    if (typeof document === 'undefined') return;
    var dock = document.getElementById('workbenchDock');
    if (!dock) return;
    var body = document.getElementById('workbenchBody');
    if (!body) return;

    // Always restore any previously docked live DOM nodes before re-rendering
    restoreDockedNodes();

    var tabs = dock.querySelectorAll('.wb-tab');
    Array.prototype.forEach.call(tabs, function (btn) {
      if (btn.dataset && btn.dataset.wbTab === activeWbTab) btn.classList.add('active');
      else btn.classList.remove('active');
    });

    var activeSec = getActiveStageSection();
    if (!activeSec) {
      var ctx = detectPageContext();
      var pfx = (ctx === 'stop' || ctx === 'exam') ? '../' : '';
      body.innerHTML =
        '<div class="wb-item">' +
          '<div class="wb-item-head"><span>🗺️ Command Hub Quick Workbench</span></div>' +
          '<p style="margin:0 0 10px;font-size:13px;color:var(--fs-muted)">Open any Stop to dock its Python templates, interactive step-by-step Labs, and Check-Yourself Quizzes side-by-side.</p>' +
          '<div style="display:flex;flex-direction:column;gap:6px;">' +
            '<a class="stb-btn" href="' + pfx + 'stops/ch12.html">⚡ Stop 12: Graphs II (Topo, Dijkstra, MST)</a>' +
            '<a class="stb-btn" href="' + pfx + 'stops/ch10.html">📐 Stop 10: 2D DP &amp; Knapsack Conversions</a>' +
            '<a class="stb-btn" href="' + pfx + 'stops/ch16.html">🧠 Stop 16: 13 Contest Memory Templates</a>' +
            '<a class="stb-btn" href="' + pfx + 'exam/cheat.html">📋 X8: One-Page Exam Cheat Sheet</a>' +
          '</div>' +
        '</div>';
      return;
    }

    if (activeWbTab === 'code') {
      var pres = activeSec.querySelectorAll('pre.code');
      if (!pres || !pres.length) {
        body.innerHTML = '<div class="wb-item"><strong>No code templates on this stop.</strong><p style="margin:6px 0 0;color:var(--fs-muted)">Switch to the Labs or Quiz tab to practise interactively.</p></div>';
        return;
      }
      body.innerHTML = '';
      Array.prototype.forEach.call(pres, function (pre, i) {
        var meta = inferCodeBlockMeta(pre, i);
        var card = document.createElement('div');
        card.className = 'wb-item';

        var headRow = document.createElement('div');
        headRow.className = 'wb-item-head';
        var titleSpan = document.createElement('span');
        titleSpan.textContent = meta.title;
        var copyBtn = document.createElement('button');
        copyBtn.type = 'button';
        copyBtn.className = 'stb-btn';
        copyBtn.style.height = '24px';
        copyBtn.style.padding = '0 8px';
        copyBtn.style.fontSize = '11.5px';
        copyBtn.textContent = 'Copy';
        copyBtn.addEventListener('click', function () {
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(meta.rawText).then(function () {
              copyBtn.textContent = '✓ Copied';
              setTimeout(function () { copyBtn.textContent = 'Copy'; }, 1400);
            });
          }
        });
        headRow.appendChild(titleSpan);
        headRow.appendChild(copyBtn);

        var codePre = document.createElement('pre');
        codePre.className = 'code wb-code-pre';
        codePre.style.margin = '0';
        codePre.style.overflowX = 'auto';
        var codeNode = document.createElement('code');
        codeNode.innerHTML = meta.codeHtml;
        codePre.appendChild(codeNode);

        if (meta.isSpoiler) {
          var det = document.createElement('details');
          det.style.border = 'none';
          det.style.padding = '0';
          det.style.margin = '0';
          det.style.background = 'transparent';
          var sum = document.createElement('summary');
          sum.style.fontSize = '12.5px';
          sum.style.padding = '2px 0 8px';
          sum.textContent = '🔒 ' + meta.title + ' (Click to reveal solution)';
          det.appendChild(sum);
          det.appendChild(headRow);
          det.appendChild(codePre);
          card.appendChild(det);
        } else {
          card.appendChild(headRow);
          card.appendChild(codePre);
        }
        body.appendChild(card);
      });
    } else if (activeWbTab === 'labs') {
      var labs = activeSec.querySelectorAll('.lab');
      if (!labs || !labs.length) {
        body.innerHTML = '<div class="wb-item"><strong>No interactive lab on this stop.</strong><p style="margin:6px 0 0;color:var(--fs-muted)">Use the Code or Quiz tab to practise this stop.</p></div>';
        return;
      }
      body.innerHTML = '';
      if (document.body && document.body.classList && document.body.classList.contains('workbench-mode') && labs[0] && labs[0].parentNode) {
        dockElementsIntoWorkbench(labs, body, 'Lab');
      } else {
        var lhtml = [];
        Array.prototype.forEach.call(labs, function (lab, i) {
          var title = lab.getAttribute('data-title') || lab.getAttribute('data-w') || ('Lab ' + (i + 1));
          if (!lab.id) lab.id = 'wb-lab-target-' + i;
          lhtml.push('<div class="wb-item"><div style="font-weight:600;margin-bottom:6px;">' + escHtml(title) + '</div><a class="stb-btn" href="#' + lab.id + '">Jump to interactive lab →</a></div>');
        });
        body.innerHTML = lhtml.join('');
      }
    } else {
      var quizzes = activeSec.querySelectorAll('.quiz');
      if (!quizzes || !quizzes.length) {
        body.innerHTML = '<div class="wb-item"><strong>Quick Check</strong><p style="margin:6px 0 0;color:var(--fs-muted)">Trace the worked example on the left by hand, then mark this stop as understood.</p></div>';
        return;
      }
      body.innerHTML = '';
      if (document.body && document.body.classList && document.body.classList.contains('workbench-mode') && quizzes[0] && quizzes[0].parentNode) {
        dockElementsIntoWorkbench(quizzes, body, 'Quiz');
      } else {
        var qCount = activeSec.querySelectorAll('.quiz .q').length;
        var qz = quizzes[0];
        if (!qz.id) qz.id = 'wb-quiz-target';
        body.innerHTML = '<div class="wb-item"><div style="font-weight:600;margin-bottom:6px;">Stop Quiz (' + qCount + ' Questions)</div><a class="stb-btn" href="#' + qz.id + '">Scroll to Stop Quiz (' + qCount + ' Qs) →</a></div>';
      }
    }
  }

  function toggleWorkbench(force) {
    if (typeof document === 'undefined' || !document.body) return false;
    var next = typeof force === 'boolean' ? force : !document.body.classList.contains('workbench-mode');
    if (!next) {
      restoreDockedNodes();
    }
    document.body.classList.toggle('workbench-mode', next);
    var btn = document.getElementById('workbenchBtn');
    if (btn && btn.classList) btn.classList.toggle('active', next);
    try {
      if (typeof sessionStorage !== 'undefined') sessionStorage.setItem('ada-wb-open', next ? '1' : '0');
    } catch (_) {}
    if (next) renderWorkbenchTab(activeWbTab);
    return next;
  }

  function attachDialogLightDismiss(dialog) {
    if (!dialog) return;
    if (typeof HTMLDialogElement !== 'undefined' && !('closedBy' in HTMLDialogElement.prototype)) {
      dialog.addEventListener('click', function (event) {
        if (event.target !== dialog) return;
        var rect = dialog.getBoundingClientRect();
        var isDialogContent = (
          rect.top <= event.clientY &&
          event.clientY <= rect.top + rect.height &&
          rect.left <= event.clientX &&
          event.clientX <= rect.left + rect.width
        );
        if (isDialogContent) return;
        dialog.close();
      });
    }
  }

  /* ---------- Right Rail (#onThisStop): Scroll-Spy, Top Done Toggle & Stop Ladder Links ---------- */
  var tocObserver = null;

  function populateOnThisStop() {
    if (typeof document === 'undefined') return;
    var rail = document.getElementById('onThisStop');
    if (!rail) return;
    var activeSec = getActiveStageSection();
    if (!activeSec) return;

    var items = buildStopTocData(activeSec);
    var listEl = document.getElementById('onThisStopList');
    if (listEl) {
      if (!items.length) {
        listEl.innerHTML = '<li><a class="toc-link active" href="#' + activeSec.id + '">Overview</a></li>';
      } else {
        listEl.innerHTML = items.map(function (it, idx) {
          return '<li><a class="toc-link' + (idx === 0 ? ' active' : '') + '" data-toc-id="' + escHtml(it.id) + '" href="#' + escHtml(it.id) + '">' + escHtml(it.label) + '</a></li>';
        }).join('');
      }

      if (listEl.addEventListener) {
        listEl.addEventListener('click', function (e) {
          var a = e.target && e.target.closest ? e.target.closest('a.toc-link') : null;
          if (!a) return;
          Array.prototype.forEach.call(listEl.querySelectorAll('a.toc-link'), function (lnk) {
            lnk.classList.toggle('active', lnk === a);
          });
        });
      }

      // Attach IntersectionObserver scroll-spy for #onThisStopList
      if (typeof IntersectionObserver !== 'undefined' && items.length > 1) {
        if (tocObserver) tocObserver.disconnect();
        tocObserver = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting && en.target && en.target.id) {
              var links = listEl.querySelectorAll('a.toc-link');
              Array.prototype.forEach.call(links, function (lnk) {
                var match = lnk.getAttribute('href') === '#' + en.target.id;
                lnk.classList.toggle('active', match);
              });
            }
          });
        }, { rootMargin: '-72px 0px -68% 0px', threshold: 0 });

        items.forEach(function (it) {
          var targetNode = document.getElementById(it.id);
          if (targetNode) tocObserver.observe(targetNode);
        });
      }
    }

    // Sync top "Mark Stop Understood" button in #onThisStop
    var otsDoneBtn = document.getElementById('otsDoneBtn');
    var inlineDoneBtn = activeSec.querySelector ? activeSec.querySelector('.done-btn') : null;
    if (otsDoneBtn) {
      if (inlineDoneBtn) {
        var syncDoneState = function () {
          var isOn = inlineDoneBtn.classList && inlineDoneBtn.classList.contains('on');
          otsDoneBtn.classList.toggle('active', isOn);
          otsDoneBtn.textContent = isOn ? '✓ Stop Understood' : '○ Mark Stop Understood';
        };
        syncDoneState();
        otsDoneBtn.onclick = function () {
          inlineDoneBtn.click();
          syncDoneState();
        };
        if (document.addEventListener) {
          document.addEventListener('click', function (ev) {
            if (ev.target && ev.target.classList && ev.target.classList.contains('done-btn')) {
              setTimeout(syncDoneState, 10);
            }
          });
        }
      } else {
        otsDoneBtn.style.display = 'none';
      }
    }

    // Populate related Ladder problems for this stop
    var otsLadBox = document.getElementById('otsLadderList');
    if (otsLadBox) {
      var catItem = CATALOG_BY_ID[activeSec.id];
      var ladTopic = catItem && catItem.ladTopic ? catItem.ladTopic : '';
      var ladder = getLadderArray().filter(function (p) { return p.topic === ladTopic; }).slice(0, 5);
      var ctx = detectPageContext();
      if (ladder.length) {
        otsLadBox.innerHTML = ladder.map(function (p) {
          var cleanQ = (p.t || '').replace(/^(CF\s+\S+\s+|CSES\s+|\d+\.\s+)/i, '').trim() || p.t;
          var href = resolveInternalHref('#ladder', ctx) + '?q=' + encodeURIComponent(cleanQ);
          return '<a class="stb-btn" style="justify-content:space-between;font-size:11.5px;height:28px;" href="' + href + '">' +
            '<span style="overflow:hidden;text-overflow:ellipsis;">' + escHtml(p.t) + '</span>' +
            '<span style="color:var(--fs-muted);font-family:\'IBM Plex Mono\',monospace;">' + escHtml(p.src || 'LC') + '</span></a>';
        }).join('');
      } else {
        otsLadBox.innerHTML = '';
      }
    }
  }

  function refreshHubMetrics() {
    if (typeof document === 'undefined') return;
    var doneEl = document.getElementById('hubKpiStops');
    var ladEl = document.getElementById('hubKpiLadder');
    var deckEl = document.getElementById('hubKpiDeck');
    var syncEl = document.getElementById('hubKpiSync');

    try {
      var done = JSON.parse(localStorage.getItem('ada-done') || '[]');
      var doneSet = new Set(Array.isArray(done) ? done : []);
      var stopDone = Array.isArray(done) ? done.filter(function (k) { return /^(ch|b)\d+$/.test(k); }).length : 0;
      if (doneEl) doneEl.textContent = stopDone + ' / 29';

      var lad = JSON.parse(localStorage.getItem('ada-ladder-v2') || '{}');
      var ladCount = lad && typeof lad === 'object' ? Object.keys(lad).length : 0;
      if (ladEl) ladEl.textContent = ladCount + ' / 380';

      var deck = JSON.parse(localStorage.getItem('ada-deck') || '{}');
      var deckCount = deck && typeof deck === 'object' ? Object.keys(deck).length : 0;
      if (deckEl) deckEl.textContent = String(deckCount);

      if (syncEl && window.ADAStore) {
        var st = window.ADAStore.lastExportStatus();
        syncEl.textContent = st.never ? 'Not exported' : (st.days === 0 ? 'Today' : st.days + 'd ago');
      }

      // Highlight completed .hub-stop-pill items on hub.html
      if (document.querySelectorAll) {
        var pills = document.querySelectorAll('.hub-stop-pill[href^="stops/"]');
        Array.prototype.forEach.call(pills, function (pill) {
          var m = (pill.getAttribute('href') || '').match(/stops\/([^.]+)\.html/);
          if (m && doneSet.has(m[1])) {
            pill.classList.add('done');
          } else {
            pill.classList.remove('done');
          }
        });

        // Update Resume Last Stop CTA on hub.html
        var resumeBtn = document.getElementById('hubResumeBtn');
        var lastStop = localStorage.getItem('ada-last-stop');
        if (resumeBtn && lastStop && CATALOG_BY_ID[lastStop]) {
          var meta = CATALOG_BY_ID[lastStop];
          resumeBtn.setAttribute('href', 'stops/' + lastStop + '.html');
          resumeBtn.textContent = 'Resume Stop ' + meta.num + ': ' + meta.title + ' →';
        }
      }
    } catch (_) {}
  }

  function enhanceNavigationAndSearch() {
    if (typeof document === 'undefined' || !document.body) return;
    var ctx = detectPageContext();
    var activeRoute = (document.body.dataset && document.body.dataset.activeRoute) || 'hub';

    // Track last visited stop for Hub Resume button
    if (ctx === 'stop' && /^(ch|b)\d+$/.test(activeRoute)) {
      try { localStorage.setItem('ada-last-stop', activeRoute); } catch (_) {}
    }

    // 1. Prepend "🗺️ Command Hub" link at top of #navLines & auto-scroll #rail to active link
    var navLines = document.getElementById('navLines');
    if (navLines && navLines.querySelector && !navLines.querySelector('[data-id="hub"]')) {
      var hubWrap = document.createElement('div');
      hubWrap.className = 'line-group';
      hubWrap.style.marginBottom = '10px';
      var isHubActive = (activeRoute === 'hub' || activeRoute === 'index');
      hubWrap.innerHTML = '<ul class="stations" style="padding:0"><li style="list-style:none"><a href="' + resolveInternalHref('#hub', ctx) + '" data-id="hub" class="' + (isHubActive ? 'active' : '') + '"><span class="dot" style="border-color:var(--fs-accent)" aria-hidden="true"></span><span class="num">🗺️</span><span>Command Hub (Overview)</span></a></li></ul>';
      if (navLines.firstChild) navLines.insertBefore(hubWrap, navLines.firstChild);
      else navLines.appendChild(hubWrap);
    }

    var rail = document.getElementById('rail');
    if (rail && rail.querySelector) {
      var activeNav = rail.querySelector('#navLines a.active');
      if (activeNav && typeof activeNav.scrollIntoView === 'function' && activeRoute !== 'hub' && activeRoute !== 'index') {
        setTimeout(function () {
          try { activeNav.scrollIntoView({ block: 'center', behavior: 'instant' }); } catch (_) {}
        }, 30);
      }
    }

    // 2. Rewrite runtime SVG #mapDots links on hub.html
    if (document.querySelectorAll) {
      var mapLinks = document.querySelectorAll('#mapDots a[href^="#"]');
      Array.prototype.forEach.call(mapLinks, function (a) {
        var raw = a.getAttribute('href');
        if (raw) a.setAttribute('href', resolveInternalHref(raw, ctx));
      });
    }

    // 3. Global delegated click interceptor for any runtime <a href="#..."> pointing to offstage stops/exams
    if (document.addEventListener) {
      document.addEventListener('click', function (e) {
        var a = e.target && e.target.closest ? e.target.closest('a[href^="#"]') : null;
        if (!a) return;
        var raw = a.getAttribute('href');
        if (!raw || raw === '#') return;
        var targetId = raw.slice(1);
        var activeSec = getActiveStageSection();
        // If targetId is an in-page element inside #activeStopStage, let native smooth scroll handle it
        var stage = document.getElementById('activeStopStage');
        var targetEl = document.getElementById(targetId);
        if (targetEl && stage && stage.contains && stage.contains(targetEl)) {
          return;
        }
        var mapped = resolveInternalHref(raw, ctx);
        if (mapped && mapped.charAt(0) !== '#') {
          e.preventDefault();
          location.href = mapped;
        }
      });
    }

    // 4. Prevent legacy #searchIn from hiding #activeStopStage on multi-page views and show cross-page matches
    var searchIn = document.getElementById('searchIn');
    var searchMsg = document.getElementById('searchMsg');
    if (searchIn && searchIn.addEventListener) {
      searchIn.addEventListener('input', function () {
        var activeSec = getActiveStageSection();
        if (activeSec) activeSec.hidden = false;
        var intro = document.getElementById('commandHubView');
        if (intro) intro.hidden = false;
        var term = (searchIn.value || '').trim();
        if (term && searchMsg) {
          var hits = searchCorpus(term, ctx).slice(0, 4);
          if (hits.length) {
            searchMsg.innerHTML = hits.map(function (h) {
              return '<a href="' + h.href + '" style="display:block;padding:3px 0;font-size:12.5px;text-decoration:none;">→ <strong>[' + escHtml(h.badge) + ']</strong> ' + escHtml(h.title) + '</a>';
            }).join('');
          }
        }
      });
      searchIn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && (searchIn.value || '').trim()) {
          e.preventDefault();
          var cmdBtn = document.getElementById('cmdSearchBtn');
          var cmdInput = document.getElementById('cmdSearchInput');
          if (cmdInput) cmdInput.value = searchIn.value.trim();
          if (cmdBtn) cmdBtn.click();
        }
      });
    }

    // 5. Support ?q= query parameter and ★ Starred filter on ladder.html
    if (activeRoute === 'ladder' && typeof location !== 'undefined') {
      var ladLab = document.querySelector('.lab[data-w="ladder2"]');
      var qInput = ladLab && ladLab.querySelector ? ladLab.querySelector('input[type="search"]') : null;
      if (qInput && location.search) {
        try {
          var params = new URLSearchParams(location.search);
          var qParam = params.get('q');
          if (qParam) {
            qInput.value = qParam;
            qInput.dispatchEvent(new Event('input', { bubbles: true }));
          }
        } catch (_) {}
      }
    }

    // 6. Keep #onThisStop outline synchronized when Quick Review (#quickBtn) is toggled
    var quickBtn = document.getElementById('quickBtn');
    if (quickBtn && quickBtn.addEventListener) {
      quickBtn.addEventListener('click', function () {
        setTimeout(populateOnThisStop, 10);
      });
    }
  }

  function initDomBindings() {
    if (typeof document === 'undefined') return;
    populateOnThisStop();
    refreshHubMetrics();
    enhanceNavigationAndSearch();

    // Restore Workbench split state if kept open in sessionStorage
    try {
      if (typeof sessionStorage !== 'undefined' && sessionStorage.getItem('ada-wb-open') === '1') {
        toggleWorkbench(true);
      }
    } catch (_) {}

    var wbBtn = document.getElementById('workbenchBtn');
    if (wbBtn) {
      wbBtn.addEventListener('click', function () {
        toggleWorkbench();
      });
    }

    var wbCloseBtn = document.getElementById('workbenchCloseBtn');
    if (wbCloseBtn) {
      wbCloseBtn.addEventListener('click', function () {
        toggleWorkbench(false);
      });
    }

    var topThemeBtn = document.getElementById('topThemeBtn');
    if (topThemeBtn) {
      topThemeBtn.addEventListener('click', function () {
        var railThemeBtn = document.getElementById('themeBtn');
        if (railThemeBtn) {
          railThemeBtn.click();
        }
        var cur = document.documentElement.getAttribute('data-theme');
        var meta = document.querySelector && document.querySelector('meta[name="color-scheme"]');
        if (meta && (cur === 'dark' || cur === 'light')) meta.content = cur;
      });
    }

    var dock = document.getElementById('workbenchDock');
    if (dock && dock.querySelectorAll) {
      Array.prototype.forEach.call(dock.querySelectorAll('.wb-tab'), function (tabBtn) {
        tabBtn.addEventListener('click', function () {
          renderWorkbenchTab(tabBtn.dataset.wbTab);
        });
      });
    }

    var cmdDlg = document.getElementById('cmdPaletteDialog');
    var cmdBtn = document.getElementById('cmdSearchBtn');
    var cmdInput = document.getElementById('cmdSearchInput');
    var cmdResults = document.getElementById('cmdSearchResults');
    attachDialogLightDismiss(cmdDlg);

    function renderSearch(q) {
      if (!cmdResults) return;
      var hits = searchCorpus(q || 'Graph');
      if (!hits.length) {
        cmdResults.innerHTML = '<div style="padding:10px;color:var(--fs-muted);font-size:13px;">No matching stops or Ladder problems found.</div>';
        return;
      }
      cmdResults.innerHTML = hits.slice(0, 18).map(function (h) {
        return '<a class="cmd-item" href="' + h.href + '"><span><strong>[' + escHtml(h.badge) + ']</strong> ' + escHtml(h.title) + '</span><span style="font-size:11.5px;color:var(--fs-muted);white-space:nowrap;">' + escHtml(h.sub) + '</span></a>';
      }).join('');
    }

    if (cmdBtn && cmdDlg) {
      cmdBtn.addEventListener('click', function () {
        if (typeof cmdDlg.showModal === 'function') cmdDlg.showModal();
        else cmdDlg.setAttribute('open', 'open');
        renderSearch(cmdInput ? cmdInput.value : '');
        if (cmdInput && cmdInput.focus) cmdInput.focus();
      });
    }
    if (cmdInput) {
      cmdInput.addEventListener('input', function () {
        renderSearch(cmdInput.value);
      });
    }

    var expDlg = document.getElementById('exportImportDialog');
    var expBtn = document.getElementById('exportImportBtn');
    var dlBtn = document.getElementById('downloadExportBtn');
    var applyBtn = document.getElementById('applyImportBtn');
    var importArea = document.getElementById('importJsonTextarea');
    var importMsg = document.getElementById('importFeedbackMsg');
    attachDialogLightDismiss(expDlg);

    if (expBtn && expDlg) {
      expBtn.addEventListener('click', function () {
        if (typeof expDlg.showModal === 'function') expDlg.showModal();
        else expDlg.setAttribute('open', 'open');
      });
    }
    if (dlBtn && window.ADAStore) {
      dlBtn.addEventListener('click', function () {
        var p = window.ADAStore.downloadExport();
        if (importArea) importArea.value = JSON.stringify(p, null, 2);
        if (importMsg) importMsg.textContent = 'Exported current progress JSON.';
        refreshHubMetrics();
      });
    }
    if (applyBtn && window.ADAStore) {
      applyBtn.addEventListener('click', function () {
        var raw = importArea ? importArea.value : '';
        var res = window.ADAStore.validateImport(raw);
        if (!res.ok) {
          if (importMsg) importMsg.textContent = res.error;
          return;
        }
        var sum = res.summary;
        window.ADAStore.mergeImport(res.payload);
        if (importMsg) {
          importMsg.textContent = 'Merged successfully (+' + sum.newStops + ' stops, +' + sum.newProblems + ' Ladder solves, +' + sum.newMistakes + ' mistakes).';
        }
        refreshHubMetrics();
      });
    }

    // Listen for live progress changes
    if (typeof window !== 'undefined' && window.addEventListener) {
      window.addEventListener('ada-ladder-change', refreshHubMetrics);
      window.addEventListener('ada-store-imported', refreshHubMetrics);
      window.addEventListener('keydown', function (e) {
        if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
          e.preventDefault();
          if (cmdBtn) cmdBtn.click();
        }
      });

      // Register offline Service Worker over HTTP/HTTPS (skip on localhost so dev edits never get stuck in cache)
      if (typeof navigator !== 'undefined' && navigator.serviceWorker && typeof location !== 'undefined' && /^https?:$/.test(location.protocol)) {
        var isLocalDev = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
        if (isLocalDev && navigator.serviceWorker.getRegistrations) {
          navigator.serviceWorker.getRegistrations().then(function (regs) {
            regs.forEach(function (r) { r.unregister(); });
          }).catch(function () {});
        } else {
          var swPrefix = (detectPageContext() === 'stop' || detectPageContext() === 'exam') ? '../' : './';
          navigator.serviceWorker.register(swPrefix + 'sw.js').then(function (reg) {
            if (reg && reg.update) reg.update();
          }).catch(function () {});
        }
      }
    }
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initDomBindings);
    } else {
      initDomBindings();
    }
  }

  window.ADASiteShell = {
    STOPS_CATALOG: STOPS_CATALOG,
    detectPageContext: detectPageContext,
    resolveInternalHref: resolveInternalHref,
    searchCorpus: searchCorpus,
    buildStopTocData: buildStopTocData,
    renderWorkbenchTab: renderWorkbenchTab,
    toggleWorkbench: toggleWorkbench,
    refreshHubMetrics: refreshHubMetrics
  };
})();
