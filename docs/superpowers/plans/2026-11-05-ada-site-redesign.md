# ADA Exam Notebook v5 Full-Fledged Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Unpack `ada-notebook-source-v4.zip` into a git-backed project and build a modular, multi-page static site (`dist/`) with a Command Hub dashboard, 3-Column Atlas & Split-Workbench stop pages, Export/Import progress backup, global `⌘K` search, and PWA offline support while maintaining 100% parity with all v4 content, code blocks, widgets, and tests.

**Architecture:** We preserve the deterministic `build.py` pipeline that produces `dist/index.html` (passing `chk.py` and `chk4.py` unmodified) and extend it with `build_site.py`, which extracts each stop (`src/stops/<id>.html`), JSON data files (`dist/data/*.json`), modular CSS/JS (`dist/assets/site.css`, `dist/assets/store.js`, `dist/assets/site-shell.js`), and generates dedicated multi-page routes (`dist/hub.html`, `dist/stops/<id>.html`, `dist/ladder.html`, `dist/exam/<id>.html`) plus a View-Controller mode inside `dist/index.html` so both single-page anchors (`#ch12`) and multi-page URLs (`/stops/ch12.html`) work seamlessly.

**Tech Stack:** Python 3.10+ (build & test pipeline), Vanilla HTML5 / CSS3 (`framed-sheet` design tokens, `IBM Plex Sans` + `IBM Plex Mono`), Vanilla ES6+ JavaScript (`localStorage` sync/merge, `⌘K` modal, 3-Column TOC + Split Workbench), Service Worker (`sw.js`), Playwright + Chromium (automated verification).

**Spec:** `docs/superpowers/specs/2026-11-05-ada-site-redesign-design.md`

## Global Constraints

- Never rename or alter the schema of `localStorage` keys: `ada-done`, `ada-ladder-v2`, `ada-deck`, `ada-mock`, `ada-mock3`, `ada-mock-lc`, `ada-endsem-date`, `ada-quick`, `ada-theme2`.
- Every Python code snippet in `src/snippets/snips.py` and exam item in `src/data/exam_v4.py` remains untouched and must pass `tests/tests.py`, `tests/t2.py`, `tests/t3.py`, `tests/t4.py`, and `tests/t5.py`.
- All existing browser assertions in `tests/chk.py` and `tests/chk4.py` must continue to pass with 0 failures.
- Export/Import JSON must use `{"app": "ada-notebook", "schema": 1, "exportedAt": "<ISO>", "data": {...}}` and merge without overwriting newer progress.

## Review Focus

1. **Legacy `1` ticks in `ada-ladder-v2` during Export/Import merge:** A legacy tick stored as `1` must be treated as timestamp `0` so any dated timestamp (`> 0`) wins, and unticking deletes the key cleanly without double-counting XP.
2. **Invalid or mismatched JSON uploaded to Import:** Importing a non-JSON file or a JSON file where `app !== "ada-notebook"` or `schema !== 1` must be rejected with a clear user-facing error message without mutating `localStorage`.
3. **Cross-page internal anchor links (`href="#ch12"`, `href="#v-key"`):** On a dedicated stop page (`dist/stops/ch8.html`), clicking a link to `#ch12` or `#ladder` must navigate to the target stop (`ch12.html` or `../ladder.html`) rather than failing to find `#ch12` on the current page.
4. **Interactive lab & quiz mounting on standalone stop pages:** Scripts that expect all stops to exist in the DOM must guard missing elements cleanly so opening `/stops/ch12.html` or `/exam/mock.html` directly produces zero `TypeError` console errors.
5. **Workbench Split View toggle with empty labs/code:** Toggling Split Workbench on a bridge stop (`b0`–`b10`) that has no `<pre class="code">` or `.lab` must still display its quiz/exercises cleanly without leaving a broken empty right pane.

---

### Task 1: Unpack v4 Source Pipeline, Initialize Git (P0), and Verify Baseline Suites

**Files:**
- Extract: `ada-notebook-source-v4.zip` into workspace root (`src/`, `tests/`, `docs/`, `build.py`)
- Create: `.gitignore`

**Interfaces:**
- Consumes: `ada-notebook-source-v4.zip`, `ADA_Exam_Notebook_v4.html`
- Produces: Working repository with `src/`, `tests/`, `build.py`, `dist/index.html` byte-identical to `ADA_Exam_Notebook_v4.html`

- [ ] **Step 1: Unpack `ada-notebook-source-v4.zip` into the workspace and initialize git**

 Extract `ada-notebook/*` into `/Users/achintyasharma/Desktop/GOD OF ADA/files/` (preserving `roadmap.md` and `docs/superpowers/`), create `.gitignore` ignoring `.superpowers/`, `.taste-skill/`, `__pycache__/`, and `/tmp/`, and initialize git with tag `v4.0-baseline`.

- [ ] **Step 2: Run `build.py` and verify byte-for-byte identity with `ADA_Exam_Notebook_v4.html`**

Run: `python3 build.py && cmp -s dist/index.html ADA_Exam_Notebook_v4.html && echo "BYTE_IDENTICAL"`
Expected: `BYTE_IDENTICAL`

- [ ] **Step 3: Run all 5 Python algorithm and exam verification suites**

Run: `python3 tests/tests.py && python3 tests/t2.py && python3 tests/t3.py && python3 tests/t4.py && python3 tests/t5.py`
Expected: `ALL TESTS PASSED`, `vault ok`, `Graphs II: all tests passed`, `t4: all tests passed`, `t5: all exam items verified`

- [ ] **Step 4: Commit P0 baseline**

```bash
git add .gitignore build.py README.md src/ tests/ docs/
git commit -m "chore(p0): initialize repository from v4 source pipeline"
```

---

### Task 2: Portable Progress Store & Export/Import Module (P1)

**Files:**
- Create: `src/js/store.js`
- Create: `tests/test_store.py`

**Interfaces:**
- Consumes: `localStorage` keys (`ada-done`, `ada-ladder-v2`, `ada-deck`, `ada-mock`, `ada-mock3`, `ada-mock-lc`, `ada-endsem-date`, `ada-quick`, `ada-theme2`, `ada-last-export`)
- Produces: `window.ADAStore = { exportPayload(), validateImport(rawJson), mergeImport(payload), downloadExport(), promptImport() }`

- [ ] **Step 1: Write `tests/test_store.py` testing Export/Import schema validation, legacy tick (`1`) merging, mistake deck (`{n, at}`) newest-timestamp merging, and invalid file rejection**

```python
# Verifies window.ADAStore in node/python via JS evaluation:
# 1. exportPayload() returns app='ada-notebook', schema=1, exportedAt, data
# 2. validateImport() rejects wrong app/schema or malformed JSON
# 3. mergeImport() unions ada-done, picks max timestamp for ada-ladder-v2 (treating 1 as 0),
#    and picks newest 'at' for ada-deck without overwriting newer local records
```

- [ ] **Step 2: Run `python3 tests/test_store.py` to confirm it fails before implementation**

Run: `python3 tests/test_store.py`
Expected: FAIL (`src/js/store.js` not found)

- [ ] **Step 3: Implement `src/js/store.js` with `window.ADAStore` and top-bar Export/Import modal UI**

Implement `exportPayload()`, `validateImport(text)`, `computeDiffSummary(incoming)`, `mergeImport(payload)`, `downloadExport()`, and the Export/Import modal with last-exported badge.

- [ ] **Step 4: Run `python3 tests/test_store.py` to verify all store & merge tests pass**

Run: `python3 tests/test_store.py`
Expected: PASS (`ALL STORE TESTS PASSED`)

- [ ] **Step 5: Commit P1 Store module**

```bash
git add src/js/store.js tests/test_store.py
git commit -m "feat(p1): add ADAStore export/import JSON with merge rules"
```

---

### Task 3: UI Redesign Shell (`framed-sheet` Theme, 3-Column Atlas, Split Workbench, Command Hub & `⌘K` Search)

**Files:**
- Create: `src/css/site_redesign.css`
- Create: `src/js/site_shell.js`
- Test: `tests/chk_site.py`

**Interfaces:**
- Consumes: `window.ADAStore`, existing DOM sections (`section.topic`), `#navLines`, `QUIZ`, `LADDER`
- Produces:
  - `src/css/site_redesign.css`: `IBM Plex Sans` + `IBM Plex Mono` typography, `framed-sheet` light/dark tokens (`--ground`, `--surface`, `--raised`, `--border`, `--accent: #1b6c80`), 48px top utility bar, 228px transit sidebar, 8px inset sheet with 16px radius, 3-Column Atlas layout (with right-hand `#onThisStop` sticky outline & stop Ladder card), and `.workbench-mode` 50/50 split layout.
  - `src/js/site_shell.js`:
    - Top bar with `⌘K` Command Palette search across all 29 stops & 380 Ladder problems, View Mode switcher (`Hub`, `Atlas 3-Col`, `Workbench Split`, `All-Scroll`), Export/Import button, Quick Review button, and Theme toggle.
    - Dynamic Right Rail (`#onThisStop`) that extracts `h3` headings, interactive labs, code templates, and quiz links for the active stop and highlights on scroll.
    - Workbench Split View mode that pins a tabbed interactive pane (`Code Templates`, `Interactive Labs`, `Stop Quiz`) on the right while scrolling prose on the left.
    - Cross-page & single-page router supporting both standalone multi-page files (`/stops/ch12.html`, `/ladder.html`, `/exam/mock.html`, `/hub.html`) and `#hash` navigation.

- [ ] **Step 1: Write `tests/chk_site.py` to test the redesigned UI shell, 3-Column TOC, Workbench Split View, Command Hub, `⌘K` search, and multi-page routes**

- [ ] **Step 2: Run `python3 tests/chk_site.py` to confirm it fails before implementation**

Run: `python3 tests/chk_site.py`
Expected: FAIL

- [ ] **Step 3: Implement `src/css/site_redesign.css` and `src/js/site_shell.js`**

- [ ] **Step 4: Update `build.py` and create `build_site.py` to output modular assets (`dist/assets/site.css`, `dist/assets/store.js`, `dist/assets/site_shell.js`), structured JSON (`dist/data/ladder.json`, `dist/data/quizzes.json`, `dist/data/drills.json`), extracted stop fragments (`src/stops/<id>.html`), multi-page routes (`dist/hub.html`, `dist/stops/<id>.html`, `dist/ladder.html`, `dist/exam/<id>.html`), and PWA offline files (`dist/manifest.json`, `dist/sw.js`)**

- [ ] **Step 5: Run all Python tests and browser checks (`chk.py`, `chk4.py`, `chk_site.py`)**

Run: `python3 build_site.py && python3 tests/tests.py && python3 tests/t2.py && python3 tests/t3.py && python3 tests/t4.py && python3 tests/t5.py && python3 tests/test_store.py && python3 tests/chk.py && python3 tests/chk4.py && python3 tests/chk_site.py`
Expected: All pass with 0 failures.

- [ ] **Step 6: Commit the full multi-page site redesign and build pipeline**

```bash
git add build.py build_site.py src/ tests/ dist/
git commit -m "feat(site): build v5 multi-page site with Atlas, Workbench, Hub, Export/Import, and PWA"
```

