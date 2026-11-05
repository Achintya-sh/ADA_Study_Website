# ADA Field Station v5.1 — Persona Audit & Improvement Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve all 12 findings uncovered by the 4 parallel user-persona subagent audits across layout/CSS grid selectors, dark/light theme synchronization, mobile responsiveness (`390px`), multi-page search and runtime anchor routing, live Split Workbench DOM docking, right-rail scroll-spy, JSON sync re-rendering, and offline Service Worker precaching.

**Architecture:** All edits happen in the source and build pipeline ([`src/css/site_redesign.css`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/css/site_redesign.css), [`src/js/site_shell.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/site_shell.js), [`src/js/store.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/store.js), [`src/js/ladder.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/ladder.js), and [`build_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/build_site.py)), keeping `python3 build.py` (`dist/index.html` = `ADA_Exam_Notebook_v4.html`) 100% untouched and extending [`tests/chk_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/chk_site.py) + [`tests/test_store.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/test_store.py) to lock in every fix.

**Tech Stack:** Vanilla HTML5, CSS3, ES6 JavaScript, Python 3 build pipeline, Node.js test harness.

---

## Summary of the 4 Persona Subagent Audits

1. **[Night-Before-Exam Crammer](conversation://6d3e0065-3e63-4444-a77e-777aa1a4b2d6)** — Tested `dist/hub.html` and all 8 `dist/exam/*.html` tools (`mock`, `drills`, `bugs`, `order`, `mistakes`, `practice`, `cards`, `cheat`), Quick Review mode (`body.quick`), and `ada-deck` persistence.
2. **[Deep-Study Chapter Learner](conversation://beff0df6-3eca-457c-8d18-92dbea4881b8)** — Tested `dist/stops/ch0.html`..`ch17.html` and `b0.html`..`b10.html`, interactive visualizers/labs, inline quizzes, the right-rail *On This Stop* drawer (`#onThisStop`), and the *Split Workbench* (`#workbenchDock`).
3. **[Competitive Programming / Contest Grinder](conversation://aa28840e-4f04-443d-9862-908d85c83478)** — Tested `dist/ladder.html` (413 problems), filters, `ada-ladder-v2` persistence, `⌘K` Command Palette (`#cmdkModal`), legacy sidebar search (`#searchIn`), and `ADAStore` JSON Export/Import round-trip.
4. **[Mobile, Theme, Accessibility & Offline PWA Auditor](conversation://0522ba2f-91f7-4ee3-84ab-8fd3cbbf2f3a)** — Tested `390×844` mobile & `768×1024` tablet viewports, dark/light theme variables (`ada-theme2`), keyboard navigation/ARIA roles, and `dist/sw.js` + `dist/manifest.json`.

---

## Phase 1: Critical Layout, Theme & Mobile Fixes

### Task 1: Fix 3-Column Atlas & Split Workbench Grid Selector (`.shell`) + `<div class="col">` Wrapper

**Files:**
- Modify: [`src/css/site_redesign.css`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/css/site_redesign.css#L170-L255)
- Modify: [`build_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/build_site.py#L369-L418)
- Test: [`tests/chk_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/chk_site.py)

**Why (Found by Personas 2 & 4):**
- [`src/css/site_redesign.css`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/css/site_redesign.css#L172-L176) styles `body.atlas-shell .app` and `body.workbench-mode .app`, whereas the actual HTML container is `<div class="shell">`. As a result, `.shell` stays on the 2-column grid (`290px minmax(0,1fr)`) and pushes `<aside id="onThisStop">` and `<aside id="workbenchDock">` onto **Row 2, Column 1** underneath `#rail`.
- In [`build_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/build_site.py#L369-L414), `header_block` opens `<div class="col">` and `footer_block` closes `</div>`. Wrapping `header_block` inside `<div id="adaOffstagePool">` on stop/exam pages splits `<div class="col">` across two parents and strips `.col` styling from `<main id="main">`.

- [ ] **Step 1: Update `src/css/site_redesign.css` grid selectors to target `.shell`**
  - Replace `body.atlas-shell .app` and `body.workbench-mode .app` (including `@media` breakpoints at lines 172, 248, 525, 534) with `body.atlas-shell .shell, body.atlas-shell .app` and `body.workbench-mode .shell, body.workbench-mode .app`.
  - Ensure `#onThisStop` is hidden when `body.workbench-mode` is active (`body.workbench-mode #onThisStop { display: none !important; }`) and `#workbenchDock` occupies the 3rd grid column (`minmax(360px, 44vw)`).

- [ ] **Step 2: Keep `<div class="col">` balanced in `build_site.py`**
  - In [`build_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/build_site.py), keep `<div class="col">` outside `#adaOffstagePool` wrapping `#activeStopStage`, `#adaOffstagePool`, and `footer_block` cleanly so DOM nesting is 100% balanced on every page.

- [ ] **Step 3: Add regression assertions to `tests/chk_site.py`**
  - Assert `body.atlas-shell .shell` and `body.workbench-mode .shell` exist in `dist/assets/site.css` and that `<div class="col">` wraps `<main class="main" id="main">` directly on `dist/stops/ch0.html` and `dist/hub.html`.

---

### Task 2: Unify Dark/Light Theme Synchronization & Add Top-Bar Theme Toggle

**Files:**
- Modify: [`src/css/site_redesign.css`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/css/site_redesign.css#L4-L46)
- Modify: [`build_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/build_site.py#L220-L246)
- Modify: [`src/js/site_shell.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/site_shell.js#L260-L310)
- Test: [`tests/chk_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/chk_site.py)

**Why (Found by Persona 4):**
- Base CSS activates dark mode via `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }`, whereas `site_redesign.css` only activates dark `--fs-*` tokens under `html[data-theme="dark"]`. When OS dark mode is active and `ada-theme2` is unset, `--fs-text` is `#131416` on `--surface` `#171C25` (`1.12:1` contrast).
- The `<head>` script in `build_site.py` checks `localStorage.getItem("color-scheme")` instead of `localStorage.getItem("ada-theme2")`.

- [ ] **Step 1: Add `@media (prefers-color-scheme: dark)` fallback in `src/css/site_redesign.css`**
  - Apply dark `--fs-*` tokens both under `html[data-theme="dark"], body[data-theme="dark"]` AND under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }`.
  - Replace hardcoded light hex colors on `.hub-card-num`, `.hub-stat-card`, `.hub-stop-pill`, and `.hub-banner` with `var(--fs-surface)`, `var(--fs-surface-2)`, and `var(--fs-text)`.

- [ ] **Step 2: Fix `<head>` inline theme bootstrap in `build_site.py` and add `#topThemeBtn` in `#siteTopBar`**
  - Read `localStorage.getItem("ada-theme2") || localStorage.getItem("color-scheme")` in the `<head>` inline script so `document.documentElement.dataset.theme` is set before first paint.
  - Add a compact theme toggle button (`#topThemeBtn`) in `.top-bar-actions` inside `top_bar_html()` and wire it in `site_shell.js` to click `#themeBtn` (or toggle `data-theme` + `ada-theme2` directly) so theme switching is always 1 click away even when `#rail` is collapsed on mobile.

---

### Task 3: Fix `390px` Mobile Viewport Overflow & Sticky `#siteTopBar` / `.rail` Overlap

**Files:**
- Modify: [`src/css/site_redesign.css`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/css/site_redesign.css#L60-L195)
- Test: [`tests/chk_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/chk_site.py)

**Why (Found by Persona 4):**
- On a `390×844` mobile screen, `#siteTopBar` overflows horizontally (~805px) because `.top-bar-links` and button labels do not wrap or condense.
- `#siteTopBar` (`position: sticky; top: 0; height: 48px; z-index: 60`) overlaps the top 48px of `.rail` (`top: 0; height: 100vh; z-index: 50`), covering `.rail-head` and `#themeBtn`.

- [ ] **Step 1: Offset `.rail` by `top: 48px; height: calc(100vh - 48px)`**
  - Update `body.atlas-shell .rail` on desktop and mobile drawer so it starts at `top: 48px` with `height: calc(100vh - 48px)` and never collides with `#siteTopBar`.

- [ ] **Step 2: Make `#siteTopBar` responsive at `<= 900px` and `<= 520px`**
  - At `<= 900px`, allow horizontal scroll or compact pills in `.top-bar-links`, hide `.cmdk-trigger kbd` and secondary text labels (`Export`, `Import`, `Split Workbench`), and ensure `max-width: 100vw; overflow-x: hidden` on `#siteTopBar`.

---

## Phase 2: Multi-Page Navigation, Search & Quick Review Fixes

### Task 4: Fix `⌘K` Command Palette (`window.LADDER`) & Sidebar Search (`#searchIn`)

**Files:**
- Modify: [`build_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/build_site.py#L485-L505)
- Modify: [`src/js/site_shell.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/site_shell.js#L100-L150)
- Test: [`tests/chk_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/chk_site.py)

**Why (Found by Persona 3):**
- `window.LADDER` is never populated (`ladder.js` uses `const LAD = []` inside an IIFE), and `LAD` items use `{ k, t, u, src, topic, pat, orig }` rather than `{ id, title }`. Thus `ADASiteShell.searchCorpus('Edit Distance')` returns **0** ladder problems.
- When `ladder.html?q=<query>` is opened from `⌘K`, `ladder.js` doesn't read `?q=` to pre-populate `#lad2Search`.
- Typing in the legacy sidebar `#searchIn` hides the active stop (`s.hidden = true`) when the query matches an offstage stop, leaving a blank page.

- [ ] **Step 1: Expose `window.LADDER = LAD;` in `build_site.py` and support `row.t` / `row.k` in `site_shell.js`**
  - In `build_site.py` when extracting `ladder.json` (or patching `src/js/ladder.js`), also expose `window.LADDER = LAD;` on `window`.
  - In `src/js/site_shell.js`, update `buildCorpus()` to read `const title = row.t || row.name || row.title || ''; const id = row.k || row.id || row.key || '';` and link each ladder item to `relHref('ladder.html?q=' + encodeURIComponent(title))`.
  - On `ladder.html` load in `site_shell.js`, if `URLSearchParams(location.search).get('q')` is present, set `#lad2Search.value = q` and dispatch `new Event('input', { bubbles: true })`.

- [ ] **Step 2: Bridge legacy `#searchIn` to `⌘K` on multi-page views**
  - In `site_shell.js`, attach a focus/input capture listener on `#searchIn` on multi-page routes (`body.atlas-shell`) that opens the `⌘K` Command Palette (`openCmdk()`) pre-filled with the typed character so `#searchIn` searches across all 38 pages + 413 problems without hiding `#activeStopStage`.

---

### Task 5: Intercept Runtime-Generated `#...` Anchor Links (`#mockResult`, `#mapDots`) & Fix Quick Review Mode (`body.quick`)

**Files:**
- Modify: [`src/js/site_shell.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/site_shell.js#L290-L335)
- Modify: [`src/css/site_redesign.css`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/css/site_redesign.css)
- Test: [`tests/chk_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/chk_site.py)

**Why (Found by Persona 1):**
- Finishing the Mock Exam (`dist/exam/mock.html`) dynamically injects `<a href="#ch12">` into `#mockResult`, and `dist/hub.html` dynamically injects `<a href="#ch0">` into `#mapDots`. Clicking those runtime anchors points into `#adaOffstagePool` instead of navigating to `../stops/ch12.html`.
- Toggling Quick Review (`body.quick`) hides `#mock, #drills, #bugs, #order, #mistakes, #practice, #cards` via base CSS, blanking out `dist/exam/*.html`, while `#quickBanner` is trapped inside `#adaOffstagePool`.

- [ ] **Step 1: Add delegated click interceptor in `site_shell.js` for any `a[href^="#"]` matching a stop/exam ID**
  - In `site_shell.js`, add a document-level click listener: if a clicked `<a href="#...">` has a hash matching one of the 38 stop/exam section IDs (`ch0`..`ch17`, `b0`..`b10`, `mock`, `drills`, etc.) and is not the current page's active stop, navigate to its multi-page URL (`stops/<id>.html` or `exam/<id>.html`).

- [ ] **Step 2: Override `body.quick` hiding on `#activeStopStage` and hoist `#quickBanner`**
  - In `src/css/site_redesign.css`, add `body.atlas-shell.quick #activeStopStage > section { display: block !important; }` so visiting an exam page while Quick Review is active never renders a blank page.
  - In `site_shell.js`, move `#quickBanner` into `<main id="main">` above `#activeStopStage` so users can see and exit Quick Review mode from any page.

---

## Phase 3: True Workbench Docking & Context-Aware Right Rail

### Task 6: Live DOM Reparenting & Interactive Copy in Split Workbench (`#workbenchDock`)

**Files:**
- Modify: [`src/js/site_shell.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/site_shell.js#L180-L245)
- Test: [`tests/chk_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/chk_site.py)

**Why (Found by Persona 2):**
- Currently, the Workbench `Code` tab clones `pre.innerHTML` without copy listeners and labels every snippet `Template #1..#22` without extracting its title/function name.
- The `Labs` and `Quiz` tabs only render `<a href="#...">` anchor jumps instead of letting the learner interact with the live `.lab` visualizer or `.quiz` widget side-by-side while reading the prose.

- [ ] **Step 1: Extract descriptive C++ snippet titles & wire working Copy buttons in the Workbench `Code` tab**
  - Infer each `<pre>` block's title from its preceding heading (`h3`/`h4`), `.card` title, or first C++ function signature / comment, and attach a working Copy button handler (`navigator.clipboard.writeText(pre.innerText)`).

- [ ] **Step 2: Reparent live `.lab` and `.quiz` nodes into `#workbenchBody` with placeholder restoration**
  - When the user selects the `Labs` or `Quiz` tab while `body.workbench-mode` is open, move the active stop's `.lab` / `.quiz` elements into `#workbenchBody` (leaving a lightweight `<div class="wb-placeholder">` in the main prose with a *"Docked in Split Workbench →"* badge), and restore them to their exact placeholders when switching tabs or closing the Workbench.

---

### Task 7: Enhance `#onThisStop` Right Rail (Scroll-Spy, Related Ladder Problems, Top `.done-btn`, Context-Aware Non-Stop Views)

**Files:**
- Modify: [`src/js/site_shell.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/site_shell.js#L150-L185)
- Modify: [`src/css/site_redesign.css`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/css/site_redesign.css#L210-L245)
- Test: [`tests/chk_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/chk_site.py)

**Why (Found by Personas 1, 2 & 3):**
- `#onThisStop` never updates `.active` on scroll (`IntersectionObserver` missing), doesn't surface a top "Mark Understood" button, and doesn't list Ladder problems for the active stop.
- On `hub.html`, `ladder.html`, and `exam/*.html`, `#onThisStop` either scrapes hidden `#ch0` headings or shows a single empty `Overview` item.

- [ ] **Step 1: Add `IntersectionObserver` scroll-spy, top Mark-Done toggle, and Stop Ladder problems to `#onThisStop`**
  - Observe headings inside `#activeStopStage` to highlight the current `.ots-list a.active` link as the user scrolls.
  - Add a synchronized "✓ Mark Stop Understood" button inside `#onThisStop` (mirroring `.done-btn`) and a compact **Practice on Ladder** list showing up to 5 matching problems from `window.LADDER` (`row.orig === stopId`).

- [ ] **Step 2: Context-aware `#onThisStop` on `hub.html`, `ladder.html`, and `exam/*.html`**
  - On `hub.html` and `ladder.html`, collapse `#onThisStop` (`body.page-hub .shell, body.page-ladder .shell { grid-template-columns: 272px minmax(0, 1fr); }`) so the Hub dashboard and 413-problem Ladder table get the full width.

---

## Phase 4: Live Sync Re-render, Hub Command Center & Offline PWA Completeness

### Task 8: Live Re-Render on JSON Import, Smart Mock Score Merge & Ladder ★ Re-Solve Queue

**Files:**
- Modify: [`src/js/store.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/store.js#L70-L120)
- Modify: [`src/js/site_shell.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/site_shell.js#L250-L285)
- Modify: [`tests/test_store.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/test_store.py)

**Why (Found by Persona 3):**
- Importing a JSON backup updates `localStorage`, but `ADAStore.mergeImport` doesn't dispatch `ada-ladder-change` or refresh the current page's UI, and `ada-mock3` / `ada-mock-lc` are skipped if the local browser has an initialized empty object `{}`.
- Contest grinders requested a lightweight ★ Bookmark ("Re-solve Queue" `ada-ladder-star`) filter on `ladder.html`.

- [ ] **Step 1: Upgrade `ADAStore.mergeImport` in `src/js/store.js` and test in `tests/test_store.py`**
  - Merge `ada-mock3` and `ada-mock-lc` per-key (keeping the higher `best` score and union of `attempts` / `solved` arrays).
  - Add `'ada-ladder-star'` to `KNOWN_KEYS` (union of starred problem IDs).
  - Dispatch `window.dispatchEvent(new Event('ada-ladder-change'))` and reload/re-paint active widgets after import in `site_shell.js`.

- [ ] **Step 2: Inject ★ Star toggle & "★ Starred" filter chip on `ladder.html`**
  - In `site_shell.js` on `ladder.html`, add a `★ Starred` filter chip and per-row star toggle backed by `localStorage['ada-ladder-star']`.

---

### Task 9: Hub Live Readiness Enhancements & Full Offline Service Worker Precaching

**Files:**
- Modify: [`build_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/build_site.py#L420-L595)
- Modify: [`src/js/site_shell.js`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/src/js/site_shell.js)
- Test: [`tests/chk_site.py`](file:///Users/achintyasharma/Desktop/GOD%20OF%20ADA/files/tests/chk_site.py)

**Why (Found by Personas 1 & 4):**
- `dist/hub.html` has a hardcoded `Resume: Ch 0` CTA, doesn't mark completed `.hub-stop-pill` pills with `.done`, and doesn't display the live `ada-deck` count on the Mistakes Deck link.
- `dist/sw.js` is never registered via `navigator.serviceWorker.register`, only precaches 8 files (omitting the 29 `./stops/*.html` and 8 `./exam/*.html` pages), and can resolve with `undefined` when offline.

- [ ] **Step 1: Enhance `hub.html` live telemetry in `site_shell.js`**
  - Track `localStorage.setItem('ada-last-stop', stopId)` when visiting any stop page, update the Hub's primary CTA to `Resume: <Last Stop>` dynamically, mark completed `.hub-stop-pill` items with `.done` (green check styling), and show live Mistakes count (`🎯 Mistakes (N)`) on `hub.html` and `#siteTopBar`.

- [ ] **Step 2: Precache all 29 stops + 8 exam pages in `dist/sw.js` and register Service Worker in `site_shell.js`**
  - Update `write_pwa_files()` in `build_site.py` so `CORE_ASSETS` includes all `./stops/*.html` and `./exam/*.html` routes and falls back to `caches.match('./hub.html')` if an uncached document request fails offline.
  - Register `sw.js` on `window.load` in `site_shell.js` when `location.protocol.startsWith('http')`.

---

### Task 10: Full Verification Suite (`build.py`, `build_site.py`, `test_store.py`, `chk_site.py`, `tests.py`..`t5.py`)

- [ ] **Step 1: Rebuild both targets and run all verification suites**
  - Run `python3 build.py && python3 build_site.py`
  - Run `python3 tests/test_store.py && python3 tests/chk_site.py`
  - Run `python3 tests/tests.py && python3 tests/t2.py && python3 tests/t3.py && python3 tests/t4.py && python3 tests/t5.py`
  - Commit all changes cleanly to `main`.

