#!/usr/bin/env python3
"""
Builds the full-fledged multi-page ADA Exam Notebook v5 site into dist/:
- Runs build.py first to assemble the canonical notebook HTML
- Extracts every stop into src/stops/<id>.html
- Extracts structured JSON datasets into dist/data/{ladder,quizzes,drills}.json
- Writes modular assets into dist/assets/{site.css,store.js,site_shell.js}
- Generates multi-page routes:
    dist/hub.html
    dist/ladder.html
    dist/stops/<id>.html  (ch0..ch17, b0..b10)
    dist/exam/<id>.html   (mock, drills, bugs, order, mistakes, practice, cards, cheat)
- Generates PWA manifest (dist/manifest.json) and offline service worker (dist/sw.js)
"""
import os, re, sys, json, shutil, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(ROOT, *a)

STOP_ORDER = [
    ('ch0', '0', 'Prerequisites primer', 'found'),
    ('b0', '0.5', 'Tracing code by hand', 'found'),
    ('ch1', '1', 'Problem-solving foundations', 'found'),
    ('b1', '1.5', 'Growth, limits and induction', 'found'),
    ('ch2', '2', 'Complexity analysis', 'found'),
    ('b2', '2.5', 'Swaps, pointers and partitions', 'trees'),
    ('ch3', '3', 'Quick Sort', 'trees'),
    ('b3', '3.5', 'Names, references, linked lists', 'trees'),
    ('ch4', '4', 'Binary Search Trees', 'trees'),
    ('b4', '4.5', 'Complete trees and priority queues', 'trees'),
    ('ch5', '5', 'Heaps', 'trees'),
    ('b5', '5.5', 'Counting choices', 'bt'),
    ('ch6', '6', 'Backtracking', 'bt'),
    ('b6', '6.5', 'Pairs, sets and grids', 'graph'),
    ('ch7', '7', 'Graphs: concepts and representation', 'graph'),
    ('b7', '7.5', 'One loop, two bags', 'graph'),
    ('ch8', '8', 'DFS and BFS', 'graph'),
    ('b8', '8.5', 'Caches and greedy choices', 'dp'),
    ('ch9', '9', 'Dynamic Programming I', 'dp'),
    ('b9', '9.5', 'Prefixes and 2D tables', 'dp'),
    ('ch10', '10', 'Dynamic Programming II (2D)', 'dp'),
    ('b10', '10.5', 'Choosing the technique', 'exam'),
    ('ch11', '11', 'Greedy algorithms', 'dp'),
    ('ch12', '12', 'Graphs II: order, cycles, weights', 'graph'),
    ('ch13', '13', 'Monotonic stacks and queues', 'trees'),
    ('ch14', '14', 'Contest toolkit', 'found'),
    ('ch15', '15', 'Bridges: tools you know, combined', 'dp'),
    ('ch16', '16', 'Contest readiness', 'found'),
    ('ch17', '17', 'Appendix: beyond the outline', 'found'),
]

EXAM_ORDER = [
    ('mock', 'X1', 'Mock quiz exam', 'exam'),
    ('drills', 'X2', 'Syntax recall drills', 'exam'),
    ('bugs', 'X3', 'Spot the bug', 'exam'),
    ('order', 'X4', 'Put the lines in order', 'exam'),
    ('mistakes', 'X5', 'My mistakes', 'exam'),
    ('practice', 'X6', 'Practice problems', 'exam'),
    ('cards', 'X7', 'Flashcards and glossary', 'exam'),
    ('cheat', 'X8', 'Cheat sheet', 'exam'),
]

ALL_SECTIONS = STOP_ORDER + [('ladder', 'L', 'The Ladder', 'ladder')] + EXAM_ORDER
STOP_IDS = {s[0] for s in STOP_ORDER}
EXAM_IDS = {s[0] for s in EXAM_ORDER}


def extract_sections(html):
    """Extract every <section class="topic"...>...</section> block by id."""
    sections = {}
    pattern = re.compile(
        r'(<section class="topic(?:\s+half)?" id="([^"]+)"[^>]*>.*?\n</section>)',
        re.S
    )
    for m in pattern.finditer(html):
        full_sec, sid = m.group(1), m.group(2)
        sections[sid] = full_sec
    return sections


def extract_json_datasets(html):
    """Evaluate the notebook's data script blocks in Node to dump clean JSON files."""
    os.makedirs(P('dist', 'data'), exist_ok=True)
    # Find script blocks that define QUIZ, BUGS, BLANKS, PARSONS, LADDER, etc.
    scripts = re.findall(r'<script>\n?(.*?)</script>', html, re.S)
    # Scripts 0..5 are:
    # 0: core helpers + QUIZ + chapter widgets
    # 1: TOPIC_NAMES, EXTRA_QS, BLANKS, BUGS, PARSONS, old LADDER/MOCKS
    # 2: e_widgets.js
    # 3: ladder.js
    # 4: c_extra.js
    # 5: lc_mocks.js
    data_js = '\n;\n'.join(scripts[:6])
    extractor = r"""
const fs = require('fs');
global.window = global;
global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
global.document = {
  querySelectorAll: () => [],
  querySelector: () => null,
  getElementById: () => null,
  createElement: () => ({ style: {}, classList: { add: () => {} }, appendChild: () => {}, addEventListener: () => {}, setAttribute: () => {} }),
  addEventListener: () => {},
  body: { appendChild: () => {}, classList: { toggle: () => {}, add: () => {} } },
  documentElement: { setAttribute: () => {}, getAttribute: () => 'dark' }
};
global.matchMedia = () => ({ matches: false, addEventListener: () => {} });
""" + data_js + r"""
;
const outDir = process.argv[1];
const path = require('path');
fs.writeFileSync(path.join(outDir, 'ladder.json'), JSON.stringify(window.LADDER2 || LADDER, null, 2));
fs.writeFileSync(path.join(outDir, 'quizzes.json'), JSON.stringify(QUIZ, null, 2));
fs.writeFileSync(path.join(outDir, 'drills.json'), JSON.stringify({
  topic_names: TOPIC_NAMES,
  extra_qs: EXTRA_QS,
  blanks: BLANKS,
  bugs: BUGS,
  parsons: PARSONS
}, null, 2));
"""
    # Expose LAD inside ladder.js IIFE so we capture all 380 rows
    patched_extractor = extractor.replace('const LAD = [], seen = new Set();', 'const LAD = [], seen = new Set(); window.LADDER2 = LAD;')
    res = subprocess.run(['node', '-e', patched_extractor, P('dist', 'data')], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError('JSON extraction failed:\n' + res.stderr)


def rewrite_links_for_context(fragment_html, page_kind):
    """Rewrite href="#ch12", href="#ladder", href="#mock", href="#v-..." for multi-page routes."""
    prefix = '../' if page_kind in ('stop', 'exam') else ''

    def repl(m):
        target = m.group(1)
        if target in STOP_IDS:
            return f'href="{"" if page_kind == "stop" else prefix + "stops/"}{target}.html"'
        if target == 'ladder':
            return f'href="{prefix}ladder.html"'
        if target.startswith('v-'):
            return f'href="{prefix}ladder.html#{target}"'
        if target in EXAM_IDS:
            return f'href="{"" if page_kind == "exam" else prefix + "exam/"}{target}.html"'
        return m.group(0)

    return re.sub(r'href="#([^"]+)"', repl, fragment_html)


def build_top_bar_html(page_kind, active_num, active_title):
    prefix = '../' if page_kind in ('stop', 'exam') else ''
    return f'''<div id="siteTopBar" role="banner">
  <div style="display:flex;align-items:center;gap:12px;min-width:0;">
    <a class="stb-brand" href="{prefix}hub.html">
      <span class="stb-mark">ADA</span>
      <span>GOD OF ADA</span>
    </a>
    <span class="stb-breadcrumb">/ [{active_num}] {active_title}</span>
  </div>
  <button type="button" id="cmdSearchBtn" class="stb-search-btn" aria-label="Search stops and problems">
    <span>Search 29 stops, 380 problems &amp; templates…</span>
    <span class="stb-kbd">⌘K</span>
  </button>
  <div class="stb-actions">
    <a class="stb-btn" href="{prefix}hub.html">🗺️ Hub</a>
    <a class="stb-btn" href="{prefix}ladder.html">🪜 Ladder (380)</a>
    <button type="button" id="workbenchBtn" class="stb-btn" title="Toggle 50/50 Split Workbench">⧉ Workbench Split</button>
    <button type="button" id="exportImportBtn" class="stb-btn" title="Export or Import Progress JSON">⇅ Backup / Sync</button>
  </div>
</div>'''


def build_dialogs_html():
    return '''<dialog id="cmdPaletteDialog" closedby="any" class="ada-dialog" aria-labelledby="cmdDlgTitle">
  <div class="ada-dlg-head">
    <strong id="cmdDlgTitle">Jump to Stop, Algorithm, or Ladder Problem</strong>
    <form method="dialog" style="margin:0"><button type="submit" class="stb-btn">Esc</button></form>
  </div>
  <div class="ada-dlg-body">
    <input type="search" id="cmdSearchInput" placeholder="Type e.g. Dijkstra, Kahn, Tree DP, Chakravyuh, LC 743…" style="width:100%;padding:9px 12px;border-radius:6px;border:1px solid var(--fs-border);background:var(--fs-raised);color:var(--fs-text);font-size:14px;" />
    <div id="cmdSearchResults" class="cmd-results"></div>
  </div>
</dialog>

<dialog id="exportImportDialog" closedby="any" class="ada-dialog" aria-labelledby="expDlgTitle">
  <div class="ada-dlg-head">
    <strong id="expDlgTitle">Portable Progress — Export / Import JSON (Roadmap P1)</strong>
    <form method="dialog" style="margin:0"><button type="submit" class="stb-btn">Close</button></form>
  </div>
  <div class="ada-dlg-body">
    <p style="margin:0 0 12px;font-size:13px;color:var(--fs-muted);">Export your understood stops, 380-problem Ladder ticks, and Mistakes Deck to a JSON file, or paste/import an export from another device. Merging never overwrites newer progress.</p>
    <div style="display:flex;gap:8px;margin-bottom:12px;">
      <button type="button" id="downloadExportBtn" class="stb-btn">⬇ Download Progress (.json)</button>
      <button type="button" id="applyImportBtn" class="stb-btn">⬆ Merge Imported JSON</button>
    </div>
    <textarea id="importJsonTextarea" rows="7" placeholder=\'{"app":"ada-notebook","schema":1,"data":{...}}\' style="width:100%;font-family:\'IBM Plex Mono\',monospace;font-size:12px;padding:10px;border-radius:6px;border:1px solid var(--fs-border);background:var(--fs-raised);color:var(--fs-text);"></textarea>
    <div id="importFeedbackMsg" style="margin-top:8px;font-size:13px;font-weight:500;"></div>
  </div>
</dialog>'''


def build_right_rails_html(page_kind):
    prefix = '../' if page_kind in ('stop', 'exam') else ''
    return f'''<aside id="onThisStop" aria-label="On this stop">
  <div class="ots-card">
    <div class="ots-title">
      <span>On This Stop</span>
      <span>Outline</span>
    </div>
    <ul id="onThisStopList" class="ots-list"></ul>
  </div>
  <div class="ots-card">
    <div class="ots-title">
      <span>Study Shortcuts</span>
    </div>
    <div style="display:flex;flex-direction:column;gap:6px;">
      <a class="stb-btn" href="{prefix}ladder.html">🪜 Open The Ladder (380)</a>
      <a class="stb-btn" href="{prefix}exam/mock.html">⚡ Take 20-Q Mock Exam</a>
      <a class="stb-btn" href="{prefix}exam/mistakes.html">🎯 Review Mistakes Deck</a>
      <a class="stb-btn" href="{prefix}exam/cheat.html">📋 Final Template Sheet</a>
    </div>
  </div>
</aside>

<aside id="workbenchDock" aria-label="Interactive Workbench Split Pane">
  <div class="wb-header">
    <strong style="font-size:13px;">Interactive Workbench</strong>
    <div class="wb-tabs">
      <button type="button" class="wb-tab active" data-wb-tab="code">Code</button>
      <button type="button" class="wb-tab" data-wb-tab="labs">Labs</button>
      <button type="button" class="wb-tab" data-wb-tab="quiz">Quiz</button>
    </div>
  </div>
  <div id="workbenchBody" class="wb-body"></div>
</aside>'''


def build_stop_pager_html(active_id, page_kind):
    order = STOP_ORDER if page_kind == 'stop' else (EXAM_ORDER if page_kind == 'exam' else ALL_SECTIONS)
    idx = next((i for i, item in enumerate(order) if item[0] == active_id), -1)
    if idx == -1:
        return ''
    prev_item = order[idx - 1] if idx > 0 else None
    next_item = order[idx + 1] if idx + 1 < len(order) else None

    # Also ensure direct numeric chapter neighbors (e.g. ch11 <-> ch12 <-> ch13) are linked cleanly
    m_ch = re.match(r'^ch(\d+)$', active_id)
    if m_ch:
        n = int(m_ch.group(1))
        by_id = {item[0]: item for item in STOP_ORDER}
        if f'ch{n-1}' in by_id:
            prev_item = by_id[f'ch{n-1}']
        if f'ch{n+1}' in by_id:
            next_item = by_id[f'ch{n+1}']

    cards = []
    if prev_item:
        cards.append(f'<a href="{prev_item[0]}.html"><span class="sp-dir">← Previous Stop [{prev_item[1]}]</span><span class="sp-name">{prev_item[2]}</span></a>')
    else:
        prefix = '../' if page_kind in ('stop', 'exam') else ''
        cards.append(f'<a href="{prefix}hub.html"><span class="sp-dir">← Command Hub</span><span class="sp-name">Course Transit Map &amp; Overview</span></a>')

    if next_item:
        cards.append(f'<a href="{next_item[0]}.html" style="text-align:right"><span class="sp-dir">Next Stop [{next_item[1]}] →</span><span class="sp-name">{next_item[2]}</span></a>')
    else:
        prefix = '../' if page_kind in ('stop', 'exam') else ''
        cards.append(f'<a href="{prefix}ladder.html" style="text-align:right"><span class="sp-dir">Up Next →</span><span class="sp-name">The Ladder (380 Problems)</span></a>')

    return '<nav class="stop-pager" aria-label="Stop pagination">' + ''.join(cards) + '</nav>'


def build_command_hub_html():
    groups = [
        ('Foundations & Contest Readiness', [('ch0', '0'), ('b0', '0.5'), ('ch1', '1'), ('b1', '1.5'), ('ch2', '2'), ('ch14', '14'), ('ch16', '16'), ('ch17', '17')]),
        ('Sorting, Trees, Heaps & Monotonic', [('b2', '2.5'), ('ch3', '3'), ('b3', '3.5'), ('ch4', '4'), ('b4', '4.5'), ('ch5', '5'), ('ch13', '13')]),
        ('Backtracking & Combinatorics', [('b5', '5.5'), ('ch6', '6')]),
        ('Graphs I & Graphs II (Topo, Shortest Paths, MST)', [('b6', '6.5'), ('ch7', '7'), ('b7', '7.5'), ('ch8', '8'), ('ch12', '12')]),
        ('Dynamic Programming, Greedy & Combined Bridges', [('b8', '8.5'), ('ch9', '9'), ('b9', '9.5'), ('ch10', '10'), ('ch11', '11'), ('ch15', '15'), ('b10', '10.5')]),
    ]
    title_map = {s[0]: s[2] for s in ALL_SECTIONS}
    rows_html = []
    for gname, items in groups:
        pills = []
        for sid, snum in items:
            pills.append(f'<a class="hub-stop-pill" href="stops/{sid}.html"><strong>{snum}</strong> {title_map[sid]}</a>')
        rows_html.append(f'<div class="hub-line-row"><div class="hub-line-head"><span>{gname}</span><span style="color:var(--fs-muted);font-size:12px;">{len(items)} stops</span></div><div class="hub-stop-pills">{"".join(pills)}</div></div>')

    exam_pills = [f'<a class="hub-stop-pill" href="exam/{eid}.html"><strong>{enum}</strong> {etitle}</a>' for eid, enum, etitle, _ in EXAM_ORDER]

    return f'''<section id="commandHubView">
  <div style="display:flex;align-items:baseline;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
    <div>
      <h1 style="font-size:24px;font-weight:600;margin:0;">ADA Study Command Center</h1>
      <p style="margin:4px 0 0;font-size:14px;color:var(--fs-muted);">29 course stops, 147+ brute-force-verified Python templates, 380 rated Ladder problems, and 8 interactive exam tools.</p>
    </div>
    <div style="display:flex;gap:8px;">
      <a class="stb-btn" href="stops/ch12.html">Resume Stop 12: Graphs II →</a>
      <a class="stb-btn" href="ladder.html">Open The Ladder →</a>
    </div>
  </div>

  <div id="hubKpiStrip" class="hub-kpi-strip">
    <div class="hub-kpi">
      <div class="hub-kpi-lbl">Stops understood</div>
      <div class="hub-kpi-val" id="hubKpiStops">0 / 29</div>
      <div class="hub-kpi-sub">Across 5 transit lines</div>
    </div>
    <div class="hub-kpi">
      <div class="hub-kpi-lbl">Ladder solved</div>
      <div class="hub-kpi-val" id="hubKpiLadder">0 / 380</div>
      <div class="hub-kpi-sub">Warm-up → Exam → Ego tier</div>
    </div>
    <div class="hub-kpi">
      <div class="hub-kpi-lbl">Mistakes deck</div>
      <div class="hub-kpi-val" id="hubKpiDeck">0</div>
      <div class="hub-kpi-sub">Queued for spaced review</div>
    </div>
    <div class="hub-kpi">
      <div class="hub-kpi-lbl">Backup status</div>
      <div class="hub-kpi-val" id="hubKpiSync">Ready</div>
      <div class="hub-kpi-sub">JSON Export / Import</div>
    </div>
  </div>

  <div class="hub-grid">
    <div class="hub-panel">
      <h3>Interactive Course Transit Lines (Click any stop to open its dedicated page)</h3>
      <div class="hub-line-list">
        {''.join(rows_html)}
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:16px;">
      <div class="hub-panel">
        <h3>Exam Prep &amp; Drill Suite (X1–X8)</h3>
        <div class="hub-stop-pills">
          {''.join(exam_pills)}
        </div>
      </div>
      <div class="hub-panel">
        <h3>High-Yield End-Sem Priority Path</h3>
        <ol style="margin:0;padding-left:18px;font-size:13.5px;line-height:1.6;">
          <li><a href="stops/ch12.html"><strong>Stop 12: Graphs II</strong></a> — Topo sort, Dijkstra stale-entry proof, Bellman-Ford, MST</li>
          <li><a href="stops/ch10.html"><strong>Stop 10: DP II</strong></a> &amp; <a href="stops/ch11.html"><strong>Stop 11: Greedy</strong></a> — Knapsack family &amp; exchange proofs</li>
          <li><a href="stops/ch15.html"><strong>Stop 15: Bridges</strong></a> — Tree DP, DAG DP, Binary Search + Graph check</li>
          <li><a href="stops/ch16.html"><strong>Stop 16: Contest Readiness</strong></a> — 13 memory templates &amp; 3-hour mock</li>
          <li><a href="ladder.html"><strong>The Ladder</strong></a> — Timed 3-problem Codeforces &amp; LeetCode mocks</li>
        </ol>
      </div>
    </div>
  </div>
</section>'''


def render_route_page(base_html, sections_map, active_ids, page_kind, page_title, badge_num, is_hub=False):
    """Assemble a standalone multi-page HTML document for a specific route."""
    prefix = '../' if page_kind in ('stop', 'exam') else ''

    # 1. Inject <meta name="color-scheme" content="light dark">, IBM Plex fonts, and site.css link in <head>
    head_inject = f'''<meta name="color-scheme" content="light dark">
<script>try{{document.querySelector('meta[name="color-scheme"]').content=localStorage.getItem("color-scheme")||"light dark";}}catch(_){{}}</script>
<link rel="manifest" href="{prefix}manifest.json">
<link rel="stylesheet" href="{prefix}assets/site.css">'''

    h = re.sub(r'<title>.*?</title>',
               f'<title>{page_title} — GOD OF ADA</title>\n' + head_inject, base_html, count=1)

    # 2. Add body class and data-page-kind
    h = h.replace('<body>', f'<body class="atlas-shell" data-page-kind="{page_kind}" data-active-route="{active_ids[0] if active_ids else "hub"}">', 1)

    # 3. Extract the header + intro boxes and the sections block inside <main class="main" id="main">
    main_tag = '<main class="main" id="main">'
    main_start = h.index(main_tag) + len(main_tag)
    first_sec = h.index('<section class="topic" id="ch0"')
    last_sec_m = list(re.finditer(r'</section>', h[:h.index('</main>')]))[-1]
    last_sec_end = last_sec_m.end()

    header_block = h[main_start:first_sec]
    footer_block = h[last_sec_end:h.index('</main>')]

    active_html_parts = []
    offstage_html_parts = []

    if is_hub:
        active_html_parts.append(build_command_hub_html())
        active_html_parts.append(rewrite_links_for_context(header_block, page_kind))

    for sid, _, _, _ in ALL_SECTIONS:
        sec_raw = sections_map[sid]
        if sid in active_ids and not is_hub:
            rewritten = rewrite_links_for_context(sec_raw, page_kind)
            active_html_parts.append(rewritten)
            if page_kind in ('stop', 'exam'):
                active_html_parts.append(build_stop_pager_html(sid, page_kind))
        else:
            offstage_html_parts.append(sec_raw)

    if is_hub:
        # Keep header outside offstage so #mapDots works in hub view
        new_main_inner = (
            '\n<div id="activeStopStage">\n' +
            '\n'.join(active_html_parts) +
            '\n</div>\n<div id="adaOffstagePool" hidden style="display:none!important" aria-hidden="true">\n' +
            '\n'.join(offstage_html_parts) +
            '\n</div>\n' + footer_block
        )
    else:
        new_main_inner = (
            '\n<div id="activeStopStage">\n' +
            '\n'.join(active_html_parts) +
            '\n</div>\n<div id="adaOffstagePool" hidden style="display:none!important" aria-hidden="true">\n' +
            header_block + '\n' +
            '\n'.join(offstage_html_parts) +
            '\n</div>\n' + footer_block
        )

    h = h[:main_start] + new_main_inner + h[h.index('</main>'):]

    # 4. Inject Top Bar right after <body ...> and Right Rails right after </main>
    body_tag_end = h.index('>', h.index('<body')) + 1
    top_bar = build_top_bar_html(page_kind, badge_num, page_title)
    h = h[:body_tag_end] + '\n' + top_bar + '\n' + h[body_tag_end:]

    main_close = h.index('</main>') + len('</main>')
    right_rails = build_right_rails_html(page_kind)
    h = h[:main_close] + '\n' + right_rails + '\n' + h[main_close:]

    # 5. Inject dialogs and store.js + site_shell.js + sidebar multi-page link enhancer before </body>
    nav_rewrite_js = f'''<script src="{prefix}assets/store.js"></script>
<script src="{prefix}assets/site_shell.js"></script>
<script>
(function(){{
  var ctx = "{page_kind}";
  var activeId = "{active_ids[0] if active_ids else 'hub'}";
  var navLinks = document.querySelectorAll('#navLines a[href^="#"]');
  Array.prototype.forEach.call(navLinks, function(a){{
    var raw = a.getAttribute('href');
    if (window.ADASiteShell && window.ADASiteShell.resolveInternalHref) {{
      a.setAttribute('href', window.ADASiteShell.resolveInternalHref(raw, ctx));
    }}
    if (raw === '#' + activeId) {{
      a.classList.add('active');
    }} else {{
      a.classList.remove('active');
    }}
  }});
}})();
</script>'''

    dialogs = build_dialogs_html()
    h = h.replace('</body>', dialogs + '\n' + nav_rewrite_js + '\n</body>', 1)
    return h


def write_pwa_files():
    manifest = {
        "name": "GOD OF ADA — Interactive Algorithms & Exam Prep Atlas",
        "short_name": "GOD OF ADA",
        "start_url": "./hub.html",
        "display": "standalone",
        "background_color": "#0c0e12",
        "theme_color": "#1b6c80",
        "description": "29 interactive stops, 147+ brute-force-tested Python templates, 380 rated Ladder problems, and 8 exam tools."
    }
    open(P('dist', 'manifest.json'), 'w', encoding='utf-8').write(json.dumps(manifest, indent=2))

    sw_code = """const CACHE_NAME = 'ada-atlas-v5';
const CORE_ASSETS = [
  './',
  './index.html',
  './hub.html',
  './ladder.html',
  './manifest.json',
  './assets/site.css',
  './assets/store.js',
  './assets/site_shell.js',
  './data/ladder.json',
  './data/quizzes.json',
  './data/drills.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cached) => {
      return cached || fetch(event.request).then((res) => {
        const clone = res.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone)).catch(() => {});
        return res;
      }).catch(() => cached);
    })
  );
});
"""
    open(P('dist', 'sw.js'), 'w', encoding='utf-8').write(sw_code)


def main():
    # 1. Run build.py to produce canonical dist/index.html
    subprocess.run([sys.executable, P('build.py')], check=True)
    base_html = open(P('dist', 'index.html'), encoding='utf-8').read()

    # 2. Extract all 38 sections into src/stops/<id>.html
    os.makedirs(P('src', 'stops'), exist_ok=True)
    sections_map = extract_sections(base_html)
    assert len(sections_map) == 38, f'Expected 38 sections, got {len(sections_map)}'
    for sid, sec_html in sections_map.items():
        open(P('src', 'stops', f'{sid}.html'), 'w', encoding='utf-8').write(sec_html + '\n')

    # 3. Extract structured JSON files into dist/data/
    extract_json_datasets(base_html)

    # 4. Write modular assets into dist/assets/
    os.makedirs(P('dist', 'assets'), exist_ok=True)
    style_m = re.search(r'<style>(.*?)</style>', base_html, re.S)
    base_css = style_m.group(1) if style_m else ''
    redesign_css = open(P('src', 'css', 'site_redesign.css'), encoding='utf-8').read()
    open(P('dist', 'assets', 'site.css'), 'w', encoding='utf-8').write(base_css + '\n\n' + redesign_css)
    shutil.copyfile(P('src', 'js', 'store.js'), P('dist', 'assets', 'store.js'))
    shutil.copyfile(P('src', 'js', 'site_shell.js'), P('dist', 'assets', 'site_shell.js'))

    # 5. Generate multi-page routes: dist/hub.html, dist/ladder.html, dist/stops/*.html, dist/exam/*.html
    # Also save byte-identical v4 single file at dist/v4-classic.html and upgrade dist/index.html with the v5 shell
    shutil.copyfile(P('dist', 'index.html'), P('dist', 'v4-classic.html'))

    head_inject_root = '''<meta name="color-scheme" content="light dark">
<script>try{document.querySelector('meta[name="color-scheme"]').content=localStorage.getItem("color-scheme")||"light dark";}catch(_){}</script>
<link rel="manifest" href="manifest.json">
<link rel="stylesheet" href="assets/site.css">'''
    idx_html = re.sub(r'<title>.*?</title>',
                      '<title>GOD OF ADA — Interactive Algorithms & Exam Prep Atlas</title>\n' + head_inject_root,
                      base_html, count=1)
    idx_html = idx_html.replace('<body>', '<body class="atlas-shell" data-page-kind="root" data-active-route="index">', 1)
    body_end = idx_html.index('>', idx_html.index('<body')) + 1
    idx_html = idx_html[:body_end] + '\n' + build_top_bar_html('root', 'ALL', '29 Stops + Ladder + Exam Suite') + '\n' + idx_html[body_end:]
    main_close = idx_html.index('</main>') + len('</main>')
    idx_html = idx_html[:main_close] + '\n' + build_right_rails_html('root') + '\n' + idx_html[main_close:]
    idx_html = idx_html.replace(
        '</body>',
        build_dialogs_html() + '\n<script src="assets/store.js"></script>\n<script src="assets/site_shell.js"></script>\n</body>',
        1
    )
    open(P('dist', 'index.html'), 'w', encoding='utf-8').write(idx_html)

    os.makedirs(P('dist', 'stops'), exist_ok=True)
    os.makedirs(P('dist', 'exam'), exist_ok=True)

    hub_html = render_route_page(base_html, sections_map, [], 'root', 'Command Hub', 'HUB', is_hub=True)
    open(P('dist', 'hub.html'), 'w', encoding='utf-8').write(hub_html)

    ladder_html = render_route_page(base_html, sections_map, ['ladder'], 'root', 'The Ladder (380 Problems & Vault)', 'L')
    open(P('dist', 'ladder.html'), 'w', encoding='utf-8').write(ladder_html)

    for sid, snum, stitle, _ in STOP_ORDER:
        stop_page = render_route_page(base_html, sections_map, [sid], 'stop', stitle, f'Stop {snum}')
        open(P('dist', 'stops', f'{sid}.html'), 'w', encoding='utf-8').write(stop_page)

    for eid, enum, etitle, _ in EXAM_ORDER:
        exam_page = render_route_page(base_html, sections_map, [eid], 'exam', etitle, enum)
        open(P('dist', 'exam', f'{eid}.html'), 'w', encoding='utf-8').write(exam_page)

    # 6. Write PWA manifest.json and sw.js
    write_pwa_files()

    print(f'built multi-page site: 38 extracted stops in src/stops/, 29 dist/stops/*.html, 8 dist/exam/*.html, dist/hub.html, dist/ladder.html, dist/data/*.json, dist/assets/*')


if __name__ == '__main__':
    main()
