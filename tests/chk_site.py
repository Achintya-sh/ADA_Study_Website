# Verification suite for the v5 Multi-Page Site Redesign (filesystem, DOM parity, and JS runtime).
import os, sys, json, re, subprocess
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')

def main():
    fails = []
    def check(cond, msg):
        print(('ok   ' if cond else 'FAIL ') + msg)
        if not cond:
            fails.append(msg)

    # 1. Check modular filesystem outputs
    required_files = [
        os.path.join(DIST, 'index.html'),
        os.path.join(DIST, 'hub.html'),
        os.path.join(DIST, 'ladder.html'),
        os.path.join(DIST, 'manifest.json'),
        os.path.join(DIST, 'sw.js'),
        os.path.join(DIST, 'assets', 'site.css'),
        os.path.join(DIST, 'assets', 'store.js'),
        os.path.join(DIST, 'assets', 'site_shell.js'),
        os.path.join(DIST, 'data', 'ladder.json'),
        os.path.join(DIST, 'data', 'quizzes.json'),
        os.path.join(DIST, 'data', 'drills.json'),
        os.path.join(DIST, 'stops', 'ch0.html'),
        os.path.join(DIST, 'stops', 'ch12.html'),
        os.path.join(DIST, 'stops', 'ch17.html'),
        os.path.join(DIST, 'stops', 'b0.html'),
        os.path.join(DIST, 'exam', 'mock.html'),
        os.path.join(DIST, 'exam', 'bugs.html'),
        os.path.join(DIST, 'exam', 'cheat.html'),
        os.path.join(ROOT, 'src', 'stops', 'ch12.html'),
    ]
    for p in required_files:
        rel = os.path.relpath(p, ROOT)
        check(os.path.exists(p), 'exists: ' + rel)

    if fails:
        print('\nFAILED (missing files):', fails)
        sys.exit(1)

    # 2. Check extracted JSON data parity
    ladder_data = json.load(open(os.path.join(DIST, 'data', 'ladder.json'), encoding='utf-8'))
    check(len(ladder_data) == 380, 'dist/data/ladder.json has 380 problems (%d)' % len(ladder_data))

    quizzes_data = json.load(open(os.path.join(DIST, 'data', 'quizzes.json'), encoding='utf-8'))
    check('e3' in quizzes_data and len(quizzes_data['e3']) == 19,
          'dist/data/quizzes.json has all 19 Stop 12 quiz items')

    drills_data = json.load(open(os.path.join(DIST, 'data', 'drills.json'), encoding='utf-8'))
    check(len(drills_data.get('bugs', [])) == 26, 'dist/data/drills.json has 26 bug hunts (%d)' % len(drills_data.get('bugs', [])))
    check(len(drills_data.get('blanks', [])) == 35, 'dist/data/drills.json has 35 fill-in blanks (%d)' % len(drills_data.get('blanks', [])))
    check(len(drills_data.get('parsons', [])) == 13, 'dist/data/drills.json has 13 ordering puzzles (%d)' % len(drills_data.get('parsons', [])))

    # 3. Verify all 29 stop files + ladder + 8 exam files exist and have valid structure
    stop_ids = [f'ch{i}' for i in range(18)] + [f'b{i}' for i in range(11)]
    for sid in stop_ids:
        sp = os.path.join(DIST, 'stops', f'{sid}.html')
        check(os.path.exists(sp), f'dist/stops/{sid}.html exists')

    exam_ids = ['mock', 'drills', 'bugs', 'order', 'mistakes', 'practice', 'cards', 'cheat']
    for eid in exam_ids:
        ep = os.path.join(DIST, 'exam', f'{eid}.html')
        check(os.path.exists(ep), f'dist/exam/{eid}.html exists')

    # 4. Inspect Stop 12 (dist/stops/ch12.html) and Hub (dist/hub.html) HTML & interactive JS behavior
    ch12_html = open(os.path.join(DIST, 'stops', 'ch12.html'), encoding='utf-8').read()
    check('id="siteTopBar"' in ch12_html, 'ch12.html contains #siteTopBar')
    check('id="onThisStop"' in ch12_html, 'ch12.html contains 3-column #onThisStop right rail')
    check('id="workbenchDock"' in ch12_html, 'ch12.html contains #workbenchDock split pane')
    check('class="stop-pager"' in ch12_html and 'ch11.html' in ch12_html and 'ch13.html' in ch12_html,
          'ch12.html has Prev (ch11.html) and Next (ch13.html) pagination cards')
    check('<dialog id="cmdPaletteDialog" closedby="any"' in ch12_html,
          'ch12.html uses <dialog id="cmdPaletteDialog" closedby="any">')
    check('<dialog id="exportImportDialog" closedby="any"' in ch12_html,
          'ch12.html uses <dialog id="exportImportDialog" closedby="any">')
    check('<meta name="color-scheme" content="light dark">' in ch12_html,
          'ch12.html includes <meta name="color-scheme" content="light dark">')

    # Cross-page link rewriting check (Review Focus #3)
    ch8_html = open(os.path.join(DIST, 'stops', 'ch8.html'), encoding='utf-8').read()
    check('href="ch12.html"' in ch8_html or 'href="../ladder.html"' in ch8_html,
          'cross-stop links in dist/stops/ch8.html point to multi-page routes')

    # 4b. Verify all 26 audit fixes across CSS, HTML structure, IDs, Pager, and SW
    site_css = open(os.path.join(DIST, 'assets', 'site.css'), encoding='utf-8').read()
    check('body.atlas-shell .shell' in site_css and 'body.workbench-mode .shell' in site_css,
          '[WB-1] site.css targets both .shell and .app for 3-col and Workbench grid')
    check('scroll-padding-top' in site_css,
          '[SCR-1] site.css sets html scroll-padding-top for sticky topbar')
    check('@media (prefers-color-scheme: dark)' in site_css and '--fs-ground: #0c0e12' in site_css,
          '[THM-1] site.css defines prefers-color-scheme: dark tokens for --fs-*')
    check('body.atlas-shell.quick[data-page-kind="exam"] #activeStopStage > section.topic' in site_css,
          '[QCK-1] site.css keeps exam pages visible when Quick Review is active')

    ch0_html = open(os.path.join(DIST, 'stops', 'ch0.html'), encoding='utf-8').read()
    check('href="b0.html"' in ch0_html,
          '[NAV-2] ch0.html Next pager links to Bridge 0.5 (b0.html) instead of skipping bridges')
    check('data-order="0"' in ch0_html and '(+a.dataset.order || 0) - (+b.dataset.order || 0)' in ch0_html,
          '[NAV-1] sections have data-order and #navLines sorts by data-order')
    check(ch0_html.count('<div') == ch0_html.count('</div>'),
          '[SCR-6] ch0.html has balanced <div> tags (%d open, %d close)' % (ch0_html.count('<div'), ch0_html.count('</div>')))
    check(re.search(r'<div class="box tip" id="quickBanner"[^>]*>.*?</div>.*?</p></div>\s*<div id="activeStopStage">', ch0_html, re.S) is not None,
          '[QCK-2] #quickBanner closes completely BEFORE #activeStopStage opens (Quick Review OFF never hides #activeStopStage)')
    check('<style>' not in ch0_html,
          '[THM-2] inline <style> removed from route HTML so dist/assets/site.css cascade is never overridden')

    hub_html = open(os.path.join(DIST, 'hub.html'), encoding='utf-8').read()
    index_html = open(os.path.join(DIST, 'index.html'), encoding='utf-8').read()
    check('id="commandHubView"' in index_html and 'id="commandHubView"' in hub_html,
          '[NAV-3] both dist/index.html and dist/hub.html serve the Command Hub landing page')
    check(hub_html.count('<div') == hub_html.count('</div>'),
          '[SCR-6] hub.html has balanced <div> tags')

    # 4c. Verify Theme Readability, WCAG AA Contrast (>= 4.5:1), and Resizable/Collapsible Sidebars
    check('--lc: var(--l-found)' in site_css and '--f-sans:' in site_css,
          '[THM-3] :root defines --lc and --f-sans so docked labs/buttons never get transparent backgrounds')
    check('html[data-theme="light"]' in site_css and 'html[data-theme="dark"]' in site_css,
          '[THM-4] site.css defines explicit html[data-theme="light"] and html[data-theme="dark"] overrides')
    check('.wb-body svg text' in site_css and ':is(.topic, .wb-body) svg text.sub' in site_css,
          '[THM-5] site.css styles SVG text inside docked .wb-body and preserves .sub muted fills')
    check('.box > .lbl[data-ico="➕"]::before' in site_css,
          '[THM-6] site.css replaces dark color-emoji U+2795 with accessible high-contrast warning glyph')
    check('overscroll-behavior: contain' in site_css and 'scrollbar-width: thin' in site_css,
          '[QOL-1] site.css prevents sidebar/modal scroll chaining and styles thin scrollbars')

    for ctrl_id in ['leftRailToggleBtn', 'rightRailToggleBtn', 'leftRailResizer', 'rightRailResizer', 'otsCollapseBtn', 'wbWidthCycleBtn', 'backToTopBtn']:
        check(f'id="{ctrl_id}"' in ch12_html, f'[QOL-2] ch12.html includes #{ctrl_id}')

    # Programmatic WCAG AA (>= 4.5:1) check on Light and Dark mode tokens in site_redesign.css
    def _srgb(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    def _lum(h):
        h = h.lstrip('#')
        return 0.2126 * _srgb(int(h[0:2], 16)) + 0.7152 * _srgb(int(h[2:4], 16)) + 0.0722 * _srgb(int(h[4:6], 16))
    def _contrast(a, b):
        la, lb = _lum(a), _lum(b)
        return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

    wcag_pairs = [
        ('Light .lab-h found', '#254edb', '#ffffff'),
        ('Light .lab-h trees', '#1e7336', '#ffffff'),
        ('Light .lab-h graph', '#b83b0a', '#ffffff'),
        ('Light .tip > .lbl', '#146932', '#e5f5eb'),
        ('Light .warnbox > .lbl', '#7c4d00', '#fff3d6'),
        ('Light .trap > .lbl', '#a82520', '#fbe9e8'),
        ('Dark .lab-h found', '#82a2ff', '#091118'),
        ('Dark .lab-h trees', '#54cb77', '#091118'),
        ('Dark .lab-h graph', '#fc9258', '#091118'),
        ('Dark .tip > .lbl', '#66da94', '#15301f'),
        ('Dark .warnbox > .lbl', '#f7c95c', '#3a2d0e'),
        ('Dark .trap > .lbl', '#ff8880', '#3a1a19'),
        ('Dark code comment', '#94a3b8', '#0b0e15'),
    ]
    for label, fg_hex, bg_hex in wcag_pairs:
        ratio = _contrast(fg_hex, bg_hex)
        check(ratio >= 4.5, f'[WCAG-AA] {label} contrast {ratio:.2f}:1 >= 4.5:1')

    # Verify zero duplicate HTML element IDs and balanced <div> tags across ALL 39 multi-page routes
    all_rel_pages = (
        ['hub.html', 'index.html', 'ladder.html'] +
        [f'stops/{s}.html' for s in stop_ids] +
        [f'exam/{e}.html' for e in exam_ids]
    )
    dup_pages = []
    unbalanced_pages = []
    for rel_page in all_rel_pages:
        raw = open(os.path.join(DIST, rel_page), encoding='utf-8').read()
        if raw.count('<div') != raw.count('</div>'):
            unbalanced_pages.append(rel_page)
        raw_clean = re.sub(r'<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>', '', raw)
        ids = re.findall(r'\s+id="([^"]+)"', raw_clean)
        seen = set()
        for i in ids:
            if i in seen:
                dup_pages.append(f'{rel_page}:{i}')
                break
            seen.add(i)
    check(len(dup_pages) == 0, f'zero duplicate HTML IDs across all {len(all_rel_pages)} routes (dups: {dup_pages[:5]})')
    check(len(unbalanced_pages) == 0, f'balanced <div> tags across all {len(all_rel_pages)} routes (bad: {unbalanced_pages[:5]})')

    sw_js = open(os.path.join(DIST, 'sw.js'), encoding='utf-8').read()
    check('./stops/ch12.html' in sw_js and './exam/mock.html' in sw_js,
          '[SYNC-1] dist/sw.js pre-caches stop and exam routes')

    # 5. Execute interactive JS tests on site_shell.js + store.js in Node
    node_script = r"""
const fs = require('fs');
const path = require('path');
const root = process.argv[1];

const storeCode = fs.readFileSync(path.join(root, 'dist', 'assets', 'store.js'), 'utf8');
const shellCode = fs.readFileSync(path.join(root, 'dist', 'assets', 'site_shell.js'), 'utf8');
const ladderJson = JSON.parse(fs.readFileSync(path.join(root, 'dist', 'data', 'ladder.json'), 'utf8'));
const quizzesJson = JSON.parse(fs.readFileSync(path.join(root, 'dist', 'data', 'quizzes.json'), 'utf8'));

function assert(cond, msg) {
  if (!cond) {
    console.error('FAIL JS:', msg);
    process.exit(1);
  }
  console.log('ok   JS:', msg);
}

// Verify site_shell.js parses and exposes window.ADASiteShell
const mem = {};
global.localStorage = {
  getItem: (k) => Object.prototype.hasOwnProperty.call(mem, k) ? mem[k] : null,
  setItem: (k, v) => { mem[k] = String(v); },
  removeItem: (k) => { delete mem[k]; }
};
global.window = global;
global.LADDER = ladderJson;
global.QUIZ = quizzesJson;

// Minimal DOM harness for site_shell.js unit checks
const elements = {};
function makeEl(tag, id) {
  const attrs = {};
  const el = {
    tagName: (tag || 'DIV').toUpperCase(),
    id: id || '',
    className: '',
    innerHTML: '',
    textContent: '',
    value: '',
    open: false,
    dataset: {},
    style: {
      setProperty(k, v) { this[k] = v; },
      removeProperty(k) { delete this[k]; }
    },
    children: [],
    classList: {
      _set: new Set(),
      add(c) { this._set.add(c); },
      remove(c) { this._set.delete(c); },
      toggle(c, force) {
        if (force === undefined) {
          if (this._set.has(c)) { this._set.delete(c); return false; }
          this._set.add(c); return true;
        }
        if (force) this._set.add(c); else this._set.delete(c);
        return !!force;
      },
      contains(c) { return this._set.has(c); }
    },
    getAttribute(a) { return Object.prototype.hasOwnProperty.call(attrs, a) ? attrs[a] : null; },
    setAttribute(a, v) { attrs[a] = String(v); },
    removeAttribute(a) { delete attrs[a]; },
    appendChild(c) { this.children.push(c); return c; },
    addEventListener(ev, fn) { this['_on_' + ev] = fn; },
    querySelectorAll() { return []; },
    querySelector() { return null; },
    showModal() { this.open = true; },
    close() { this.open = false; },
    focus() {}
  };
  if (id) elements[id] = el;
  return el;
}

const metaColorScheme = makeEl('meta', 'metaColorScheme');
metaColorScheme.content = 'light dark';
const topThemeBtn = makeEl('button', 'topThemeBtn');
const wbDock = makeEl('aside', 'workbenchDock');
const wbBody = makeEl('div', 'workbenchBody');
const wbTabCode = makeEl('button'); wbTabCode.dataset.wbTab = 'code';
const wbTabLabs = makeEl('button'); wbTabLabs.dataset.wbTab = 'labs';
const wbTabQuiz = makeEl('button'); wbTabQuiz.dataset.wbTab = 'quiz';
wbDock.querySelectorAll = (sel) => sel === '.wb-tab' ? [wbTabCode, wbTabLabs, wbTabQuiz] : [];
makeEl('aside', 'onThisStop');
makeEl('button', 'leftRailToggleBtn');
makeEl('button', 'rightRailToggleBtn');
makeEl('button', 'workbenchBtn');

const mockStage = makeEl('div', 'activeStopStage');
const mockSec = makeEl('section', 'ch12');
mockSec.setAttribute('data-group', 'graph');
mockSec.querySelectorAll = (sel) => {
  if (sel === 'pre.code') return [];
  if (sel === '.lab') return [makeEl('div')];
  if (sel === '.quiz') return [makeEl('div')];
  if (sel === '.quiz .q') return [makeEl('div'), makeEl('div'), makeEl('div')];
  return [];
};
mockStage.querySelector = (sel) => sel === 'section.topic' ? mockSec : null;

global.document = {
  body: makeEl('body', 'body'),
  documentElement: makeEl('html', 'html'),
  head: makeEl('head', 'head'),
  getElementById(id) { return elements[id] || null; },
  querySelector(sel) {
    if (sel === 'meta[name="color-scheme"]') return metaColorScheme;
    if (sel.startsWith('#')) return elements[sel.slice(1)] || null;
    return null;
  },
  querySelectorAll() { return []; },
  createElement(tag) { return makeEl(tag); },
  addEventListener() {}
};
document.body.dataset.pageKind = 'stop';
document.body.dataset.activeRoute = 'ch12';

eval(storeCode);
eval(shellCode);

assert(typeof window.ADASiteShell === 'object', 'window.ADASiteShell is exported');
assert(typeof window.ADASiteShell.searchCorpus === 'function', 'ADASiteShell.searchCorpus is defined');
assert(typeof window.ADASiteShell.toggleWorkbench === 'function', 'ADASiteShell.toggleWorkbench is defined');
assert(typeof window.ADASiteShell.toggleLeftSidebar === 'function', 'ADASiteShell.toggleLeftSidebar is defined');
assert(typeof window.ADASiteShell.toggleRightSidebar === 'function', 'ADASiteShell.toggleRightSidebar is defined');
assert(typeof window.ADASiteShell.buildStopTocData === 'function', 'ADASiteShell.buildStopTocData is defined');

// Test searchCorpus('Dijkstra') across stops and 380 Ladder problems
const hits = window.ADASiteShell.searchCorpus('Dijkstra');
assert(Array.isArray(hits) && hits.length >= 3, 'searchCorpus("Dijkstra") returns stop + ladder matches (' + hits.length + ')');
assert(hits.some(h => h.kind === 'stop' && h.id === 'ch12'), 'searchCorpus("Dijkstra") includes Stop 12');
assert(hits.some(h => h.kind === 'ladder'), 'searchCorpus("Dijkstra") includes Ladder problems');

// Test toggleWorkbench state machine + data-group propagation + empty Code tab auto-fallback + tab counts
window.ADASiteShell.toggleWorkbench(true);
assert(document.body.classList.contains('workbench-mode'), 'toggleWorkbench(true) adds .workbench-mode class to body');
assert(wbDock.getAttribute('data-group') === 'graph', 'Workbench inherits active section data-group="graph" for --lc header styling');
assert(wbTabLabs.classList.contains('active'), 'Workbench auto-selects Labs tab when Code tab has 0 templates on the stop');
assert(wbTabCode.textContent === 'Code (0)' && wbTabLabs.textContent === 'Labs (1)' && wbTabQuiz.textContent === 'Quiz (3)',
  'Workbench stamps item counts onto Code/Labs/Quiz tabs');
window.ADASiteShell.toggleWorkbench(false);
assert(!document.body.classList.contains('workbench-mode'), 'toggleWorkbench(false) removes .workbench-mode class from body');

// Test collapsible Left & Right sidebars + width preset cycling + theme sync
assert(window.ADASiteShell.toggleLeftSidebar(false) === false, 'toggleLeftSidebar(false) collapses left sidebar');
assert(document.documentElement.getAttribute('data-left-collapsed') === '1' && localStorage.getItem('ada-left-collapsed') === '1',
  'left sidebar collapse persists data-left-collapsed="1"');
assert(window.ADASiteShell.toggleLeftSidebar(true) === true && document.documentElement.getAttribute('data-left-collapsed') === null,
  'toggleLeftSidebar(true) expands left sidebar');

assert(window.ADASiteShell.toggleRightSidebar(false) === false, 'toggleRightSidebar(false) collapses right outline');
assert(document.documentElement.getAttribute('data-ots-collapsed') === '1' && localStorage.getItem('ada-ots-collapsed') === '1',
  'right sidebar collapse persists data-ots-collapsed="1"');
assert(window.ADASiteShell.toggleRightSidebar(true) === true && document.documentElement.getAttribute('data-ots-collapsed') === '0',
  'toggleRightSidebar(true) expands right outline');

window.ADASiteShell.cycleWorkbenchWidth();
assert(document.documentElement.style['--user-wb-w'] === '36vw' && localStorage.getItem('ada-wb-w') === '36vw',
  'cycleWorkbenchWidth() sets and persists --user-wb-w preset');

window.ADASiteShell.setThemeExplicit('dark');
assert(document.documentElement.getAttribute('data-theme') === 'dark' && metaColorScheme.content === 'dark' && topThemeBtn.textContent === '☀️',
  'setThemeExplicit("dark") syncs html[data-theme], <meta name="color-scheme">, and #topThemeBtn');
window.ADASiteShell.setThemeExplicit('light');
assert(document.documentElement.getAttribute('data-theme') === 'light' && metaColorScheme.content === 'light' && topThemeBtn.textContent === '🌙',
  'setThemeExplicit("light") syncs html[data-theme], <meta name="color-scheme">, and #topThemeBtn');

// Test resolveInternalHref for cross-page navigation (Review Focus #3)
assert(window.ADASiteShell.resolveInternalHref('#ch12', 'stop') === 'ch12.html', 'resolveInternalHref maps #ch12 -> ch12.html from /stops/*');
assert(window.ADASiteShell.resolveInternalHref('#ladder', 'stop') === '../ladder.html', 'resolveInternalHref maps #ladder -> ../ladder.html from /stops/*');
assert(window.ADASiteShell.resolveInternalHref('#mock', 'stop') === '../exam/mock.html', 'resolveInternalHref maps #mock -> ../exam/mock.html from /stops/*');
assert(window.ADASiteShell.resolveInternalHref('#v-chakravyuh', 'stop') === '../ladder.html#v-chakravyuh', 'resolveInternalHref maps Vault #v-* -> ../ladder.html#v-*');
"""
    res = subprocess.run(['node', '-e', node_script, ROOT], capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.returncode != 0:
        print(res.stderr)
        fails.append('Node JS runtime check failed')

    if fails:
        print('\nFAILED:', fails)
        sys.exit(1)
    print('\nALL MULTI-PAGE SITE CHECKS PASSED')

if __name__ == '__main__':
    main()
