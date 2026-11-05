/* ===== ADASiteShell: Multi-Page Atlas, Workbench Split View, Command Hub & ⌘K Search ===== */
(function () {
  var STOPS_CATALOG = [
    { id: 'ch0', num: '0', title: 'Prerequisites primer', group: 'found', kind: 'stop', keywords: 'python arrays loops recursion indexing dicts sets' },
    { id: 'b0', num: '0.5', title: 'Tracing code by hand', group: 'found', kind: 'stop', keywords: 'dry run trace invariants table' },
    { id: 'ch1', num: '1', title: 'Problem-solving foundations', group: 'found', kind: 'stop', keywords: 'brute force constraints edge cases subtasks' },
    { id: 'b1', num: '1.5', title: 'Growth, limits and induction', group: 'found', kind: 'stop', keywords: 'induction logarithms geometric series' },
    { id: 'ch2', num: '2', title: 'Complexity analysis', group: 'found', kind: 'stop', keywords: 'big o omega theta recurrence master theorem' },
    { id: 'ch14', num: '14', title: 'Contest toolkit', group: 'found', kind: 'stop', keywords: 'prefix sums difference array two pointers sliding window binary search on answer bisect bitmask' },
    { id: 'ch16', num: '16', title: 'Contest readiness', group: 'found', kind: 'stop', keywords: 'constraints to algorithm python pitfalls recursion limit template sheet explain aloud mock' },
    { id: 'ch17', num: '17', title: 'Appendix: beyond the outline', group: 'found', kind: 'stop', keywords: 'merge sort inversions amortised analysis hashing lca scc bridges segment tree' },
    { id: 'b2', num: '2.5', title: 'Swaps, pointers and partitions', group: 'trees', kind: 'stop', keywords: 'partition lomuto hoare two pointers' },
    { id: 'ch3', num: '3', title: 'Quick Sort', group: 'trees', kind: 'stop', keywords: 'quicksort pivot partition quickselect dutch national flag' },
    { id: 'b3', num: '3.5', title: 'Names, references, linked lists', group: 'trees', kind: 'stop', keywords: 'pointers references nodes recursion' },
    { id: 'ch4', num: '4', title: 'Binary Search Trees', group: 'trees', kind: 'stop', keywords: 'bst insert delete validate inorder lca' },
    { id: 'b4', num: '4.5', title: 'Complete trees and priority queues', group: 'trees', kind: 'stop', keywords: 'complete binary tree array indexing parent child' },
    { id: 'ch5', num: '5', title: 'Heaps', group: 'trees', kind: 'stop', keywords: 'heapq min heap max heap sift up sift down top k median' },
    { id: 'ch13', num: '13', title: 'Monotonic stacks and queues', group: 'trees', kind: 'stop', keywords: 'monotonic stack next greater element histogram sliding window deque' },
    { id: 'b5', num: '5.5', title: 'Counting choices', group: 'bt', kind: 'stop', keywords: 'permutations subsets decision tree' },
    { id: 'ch6', num: '6', title: 'Backtracking', group: 'bt', kind: 'stop', keywords: 'backtracking subsets permutations n queens pruning' },
    { id: 'b6', num: '6.5', title: 'Pairs, sets and grids', group: 'graph', kind: 'stop', keywords: 'grid neighbours visited set' },
    { id: 'ch7', num: '7', title: 'Graphs: concepts and representation', group: 'graph', kind: 'stop', keywords: 'adjacency list matrix directed undirected degree' },
    { id: 'b7', num: '7.5', title: 'One loop, two bags', group: 'graph', kind: 'stop', keywords: 'stack queue lifo fifo' },
    { id: 'ch8', num: '8', title: 'DFS and BFS', group: 'graph', kind: 'stop', keywords: 'dfs bfs connected components shortest path bipartite cycle functional graph chakravyuh' },
    { id: 'ch12', num: '12', title: 'Graphs II: order, cycles, weights', group: 'graph', kind: 'stop', keywords: 'topological sort kahn dijkstra bellman ford floyd warshall mst kruskal prim union find dsu' },
    { id: 'b8', num: '8.5', title: 'Caches and greedy choices', group: 'dp', kind: 'stop', keywords: 'memoization overlapping subproblems optimal substructure' },
    { id: 'ch9', num: '9', title: 'Dynamic Programming I', group: 'dp', kind: 'stop', keywords: '1d dp climbing stairs house robber coin change lis' },
    { id: 'b9', num: '9.5', title: 'Prefixes and 2D tables', group: 'dp', kind: 'stop', keywords: '2d grid table state transitions' },
    { id: 'ch10', num: '10', title: 'Dynamic Programming II (2D)', group: 'dp', kind: 'stop', keywords: 'knapsack 0/1 unbounded lcs edit distance space optimisation' },
    { id: 'ch11', num: '11', title: 'Greedy algorithms', group: 'dp', kind: 'stop', keywords: 'greedy exchange argument intervals scheduling fractional knapsack' },
    { id: 'ch15', num: '15', title: 'Bridges: tools you know, combined', group: 'dp', kind: 'stop', keywords: 'tree dp dag dp binary search + graph dsu two heaps trie' },
    { id: 'b10', num: '10.5', title: 'Choosing the technique', group: 'exam', kind: 'stop', keywords: 'decision tree complexity table' },
    { id: 'ladder', num: 'L', title: 'The Ladder (380 Problems & Vault)', group: 'ladder', kind: 'ladder', keywords: 'codeforces leetcode cses vault xp rank mocks' },
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

    if (id === 'hub') return prefix + 'hub.html';
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

    var ladder = (typeof window !== 'undefined' && Array.isArray(window.LADDER)) ? window.LADDER : [];
    ladder.forEach(function (row) {
      // row shape in ladder.js or ladder.json: object or array
      var title = row.name || row.title || row[1] || '';
      var pat = row.pat || row.pattern || row[3] || '';
      var topic = row.t || row.topic || row[2] || '';
      var id = String(row.id || row.key || row[0] || '');
      var hay = (id + ' ' + title + ' ' + pat + ' ' + topic).toLowerCase();
      if (hay.indexOf(q) !== -1 && results.length < 30) {
        results.push({
          kind: 'ladder',
          id: id,
          badge: row.src || 'LADDER',
          title: title + (pat ? ' — ' + pat : ''),
          sub: 'Ladder · ' + topic,
          href: resolveInternalHref('#ladder', ctx)
        });
      }
    });

    return results;
  }

  function buildStopTocData(sectionEl) {
    if (!sectionEl || typeof sectionEl.querySelectorAll !== 'function') return [];
    var items = [];
    var idx = 0;
    var nodes = sectionEl.querySelectorAll('h3, .box.idea .lbl, .lab, .quiz');
    Array.prototype.forEach.call(nodes, function (node) {
      idx++;
      var label = '';
      if (node.tagName === 'H3') {
        label = (node.textContent || '').trim();
      } else if (node.classList && node.classList.contains('lbl')) {
        label = 'Big Idea';
        node = node.parentElement || node;
      } else if (node.classList && node.classList.contains('lab')) {
        label = 'Lab: ' + (node.getAttribute('data-title') || node.getAttribute('data-w') || 'Interactive');
      } else if (node.classList && node.classList.contains('quiz')) {
        label = 'Check Yourself Quiz';
      }
      if (!label) return;
      if (!node.id) {
        node.id = (sectionEl.id || 'sec') + '-sub-' + idx;
      }
      items.push({ id: node.id, label: label });
    });
    return items;
  }

  var activeWbTab = 'code';

  function renderWorkbenchTab(tabName) {
    activeWbTab = tabName || activeWbTab || 'code';
    if (typeof document === 'undefined') return;
    var dock = document.getElementById('workbenchDock');
    if (!dock) return;
    var body = document.getElementById('workbenchBody');
    if (!body) return;

    var tabs = dock.querySelectorAll('.wb-tab');
    Array.prototype.forEach.call(tabs, function (btn) {
      if (btn.dataset && btn.dataset.wbTab === activeWbTab) btn.classList.add('active');
      else btn.classList.remove('active');
    });

    var activeSec = document.querySelector('#activeStopStage section.topic') || document.querySelector('main section.topic');
    if (!activeSec) {
      body.innerHTML = '<div class="wb-item">Select any stop to inspect its code templates, interactive labs, and quiz side-by-side.</div>';
      return;
    }

    if (activeWbTab === 'code') {
      var pres = activeSec.querySelectorAll('pre.code');
      if (!pres || !pres.length) {
        body.innerHTML = '<div class="wb-item"><strong>No code blocks on this bridge stop.</strong><p style="margin:6px 0 0;color:var(--fs-muted)">Switch to the Quiz tab or continue to the next full stop.</p></div>';
        return;
      }
      var html = [];
      Array.prototype.forEach.call(pres, function (pre, i) {
        html.push('<div class="wb-item"><div style="font-size:11.5px;color:var(--fs-muted);margin-bottom:6px;font-weight:600;">Template #' + (i + 1) + '</div><pre class="code wb-code-pre" style="margin:0;overflow-x:auto;">' + pre.innerHTML + '</pre></div>');
      });
      body.innerHTML = html.join('');
    } else if (activeWbTab === 'labs') {
      var labs = activeSec.querySelectorAll('.lab');
      if (!labs || !labs.length) {
        body.innerHTML = '<div class="wb-item"><strong>No interactive lab on this stop.</strong><p style="margin:6px 0 0;color:var(--fs-muted)">Use the Code or Quiz tab to practise this stop.</p></div>';
        return;
      }
      var lhtml = [];
      Array.prototype.forEach.call(labs, function (lab, i) {
        var title = lab.getAttribute('data-title') || lab.getAttribute('data-w') || ('Lab ' + (i + 1));
        if (!lab.id) lab.id = 'wb-lab-target-' + i;
        lhtml.push('<div class="wb-item"><div style="font-weight:600;margin-bottom:6px;">' + title + '</div><p style="font-size:12.5px;color:var(--fs-muted);margin:0 0 8px;">Interactive widget mounted inline in the stop:</p><a class="stb-btn" href="#' + lab.id + '">Jump to interactive lab →</a></div>');
      });
      body.innerHTML = lhtml.join('');
    } else {
      var quizzes = activeSec.querySelectorAll('.quiz');
      if (!quizzes || !quizzes.length) {
        body.innerHTML = '<div class="wb-item"><strong>Quick Check</strong><p style="margin:6px 0 0;color:var(--fs-muted)">Trace the worked example on the left by hand, then mark this stop as understood.</p></div>';
        return;
      }
      var qCount = activeSec.querySelectorAll('.quiz .q').length;
      var qz = quizzes[0];
      if (!qz.id) qz.id = 'wb-quiz-target';
      body.innerHTML = '<div class="wb-item"><div style="font-weight:600;margin-bottom:6px;">Stop Quiz (' + qCount + ' Questions)</div><p style="font-size:12.5px;color:var(--fs-muted);margin:0 0 10px;">Every wrong answer is automatically queued into your Mistakes Deck.</p><a class="stb-btn" href="#' + qz.id + '">Scroll to Stop Quiz (' + qCount + ' Qs) →</a></div>';
    }
  }

  function toggleWorkbench(force) {
    if (typeof document === 'undefined' || !document.body) return false;
    var next = typeof force === 'boolean' ? force : !document.body.classList.contains('workbench-mode');
    document.body.classList.toggle('workbench-mode', next);
    var btn = document.getElementById('workbenchBtn');
    if (btn && btn.classList) btn.classList.toggle('active', next);
    if (next) renderWorkbenchTab(activeWbTab);
    return next;
  }

  function attachDialogLightDismiss(dialog) {
    if (!dialog) return;
    // Fallback per modern-web-guidance: light-dismiss-a-dialog
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

  function populateOnThisStop() {
    if (typeof document === 'undefined') return;
    var rail = document.getElementById('onThisStop');
    if (!rail) return;
    var activeSec = document.querySelector('#activeStopStage section.topic') || document.querySelector('main section.topic');
    if (!activeSec) return;

    var items = buildStopTocData(activeSec);
    var listEl = document.getElementById('onThisStopList');
    if (listEl) {
      if (!items.length) {
        listEl.innerHTML = '<li><a class="toc-link" href="#' + activeSec.id + '">Overview</a></li>';
      } else {
        listEl.innerHTML = items.map(function (it, idx) {
          return '<li><a class="toc-link' + (idx === 0 ? ' active' : '') + '" href="#' + it.id + '">' + it.label + '</a></li>';
        }).join('');
      }
    }
  }

  function refreshHubMetrics() {
    if (typeof document === 'undefined') return;
    var doneEl = document.getElementById('hubKpiStops');
    var ladEl = document.getElementById('hubKpiLadder');
    var deckEl = document.getElementById('hubKpiDeck');
    var syncEl = document.getElementById('hubKpiSync');
    if (!doneEl) return;

    try {
      var done = JSON.parse(localStorage.getItem('ada-done') || '[]');
      var stopDone = Array.isArray(done) ? done.filter(function (k) { return /^(ch|b)\d+$/.test(k); }).length : 0;
      doneEl.textContent = stopDone + ' / 29';

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
    } catch (_) {}
  }

  function initDomBindings() {
    if (typeof document === 'undefined') return;
    populateOnThisStop();
    refreshHubMetrics();

    var wbBtn = document.getElementById('workbenchBtn');
    if (wbBtn) {
      wbBtn.addEventListener('click', function () {
        toggleWorkbench();
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
      cmdResults.innerHTML = hits.slice(0, 14).map(function (h) {
        return '<a class="cmd-item" href="' + h.href + '"><span><strong>[' + h.badge + ']</strong> ' + h.title + '</span><span style="font-size:11.5px;color:var(--fs-muted)">' + h.sub + '</span></a>';
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

    // Global ⌘K / Ctrl+K shortcut
    if (typeof window !== 'undefined' && window.addEventListener) {
      window.addEventListener('keydown', function (e) {
        if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
          e.preventDefault();
          if (cmdBtn) cmdBtn.click();
        }
      });
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
    searchCorpus: searchCorpus,
    toggleWorkbench: toggleWorkbench,
    buildStopTocData: buildStopTocData,
    resolveInternalHref: resolveInternalHref,
    refreshHubMetrics: refreshHubMetrics
  };
})();
