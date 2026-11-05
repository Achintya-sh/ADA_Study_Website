# ADA Exam Notebook v5 — Full-Fledged Multi-Page Site Redesign Spec

## 1. Intent & Why
Transform `ADA_Exam_Notebook_v4.html` (a 986 KB single-file monolith built by regex-splicing `src/original/nb.html`) into a fast, modular, full-fledged multi-page web application (`dist/`) while preserving **100% content, code, interactive widget, quiz, drill, and `localStorage` parity**.

## 2. Goals, Non-Goals, and Anti-Goals
- **Goals:**
  1. **Multi-Page + Instant SPA Router Architecture**:
     - Dedicated static HTML pages generated into `dist/` so every view has its own clean URL and works both via a static server (Cloudflare Pages / GitHub Pages / `python3 -m http.server`) and direct file navigation:
       - `dist/index.html` — **Command Hub Home** (Option C: Interactive 29-stop Transit Map, End-Sem Countdown, Today's Study Queue, Ladder XP/Rank/Streak overview, Mistake Deck summary, and Export/Import JSON progress backup) plus full single-page compatibility mode.
       - `dist/stops/<id>.html` — Dedicated page for each of the 29 stops (`ch0`–`ch17`, bridges `b0`–`b10`), featuring the **3-Column Atlas Shell** (Option A: Left Transit Sidebar, Center Reading + Inline Labs + Code, Right "On This Stop" dynamic TOC + Stop Ladder progress) AND a one-click **"Workbench Split View" toggle** (Option B: 50/50 split pinning Code Templates, Interactive Labs, and Stop Quizzes on the right while scrolling prose on the left).
       - `dist/ladder.html` — Dedicated page for the 380-problem Ladder, 12 topic tabs, Vault originals, and Timed 3-Problem Mocks (Codeforces & LeetCode).
       - `dist/exam/<id>.html` — Dedicated pages for all 8 Exam-Prep tools (`mock`, `drills`, `bugs`, `order`, `mistakes`, `practice`, `cards`, `cheat`).
  2. **Modular Source & Asset Extraction**:
     - Extract CSS into `dist/assets/app.css` (implementing the dealt `framed-sheet` light/dark adaptive design system with `IBM Plex Sans` + `IBM Plex Mono`, 228px sidebar, 48px top bar, 8px inset sheet with 16px corners and 1px border, zero drop-shadow clutter).
     - Extract JS into modular scripts (`dist/assets/store.js`, `dist/assets/router.js`, `dist/assets/search.js`, plus the verified notebook runtime bundles) and structured JSON data (`dist/data/ladder.json`, `dist/data/quizzes.json`, `dist/data/drills.json`).
  3. **Roadmap Platform Features (P0, P1, P2, P4)**:
     - **P1 Export / Import Progress JSON**: Exact schema from `roadmap.md` Appendix A (`app: "ada-notebook"`, `schema: 1`, `exportedAt`, `data`), merge-never-overwrite logic (Section 6), summary preview before/on import, and last-exported indicator.
     - **P2 Split Output & Clean Source Pipeline**: Build script (`build_site.py` + `build.py`) that builds both thegolden `dist/index.html` and the full multi-page site (`dist/stops/*.html`, `dist/ladder.html`, `dist/exam/*.html`, `dist/assets/*`, `dist/data/*`).
     - **P4 Offline PWA Support**: `dist/manifest.json` and `dist/sw.js` service worker caching all pages, scripts, styles, and JSON data for offline study.
  4. **Mathematical Parity Guarantee**:
     - All 5 Python algorithm/quiz test suites (`tests.py`, `t2.py`, `t3.py`, `t4.py`, `t5.py`) and both Playwright browser suites (`chk.py`, `chk4.py`) PLUS a new multi-page & parity verification suite (`tests/chk_site.py`) must pass with zero errors.
- **Non-Goals:**
  - No in-page code judge (explicitly declined in `context.md` §3).
  - No modification to any tested algorithm in `src/snippets/snips.py` or any quiz/bug/blank/Parsons answer key.
- **Anti-Goals:**
  - Never rename or break any `localStorage` key (`ada-done`, `ada-ladder-v2`, `ada-deck`, `ada-mock`, `ada-mock3`, `ada-mock-lc`, `ada-endsem-date`, `ada-quick`, `ada-theme2`).
  - Never lose or alter any of the 29 stops, 147+ code blocks, 380 Ladder rows, 26 bug hunts, 35 fill-in-the-blanks, or 13 ordering puzzles.

## 3. Visual Direction (`framed-sheet` + Dark Mode Adaptive)
From `design-taste-frontend` (`seed 1277094099`):
- **Typography:** `IBM Plex Sans` (400, 500, 600) for prose, headings, and UI; `IBM Plex Mono` (400, 500) for Python code, Big-O complexities, problem IDs, and ratings (`tabular-nums`).
- **Shell:** L-shaped tinted chrome (`#f9fbfc` in light, `#0b0d10` in dark) holding the `228px` Transit Sidebar and `48px` Top Bar (with centered `⌘K` search trigger, Quick Review toggle, Workbench Split toggle, Export/Import button, and Theme switch). Content sits on an inset sheet (`8px` inset, `16px` border-radius, `1px` crisp border, no resting box-shadow).
- **3-Column Atlas & Split Workbench:**
  - On desktop (`>= 1180px`), every stop page shows the Left Transit Sidebar (`228px`), Center Reading/Lab Column (`minmax(0, 1fr)`), and Right "On This Stop" sticky outline + topic Ladder summary (`240px`).
  - Clicking **Workbench Mode** switches the stop page into a 50/50 split where prose scrolls on the left and a tabbed interactive dock (Code Templates, Interactive Labs, Stop Quiz) stays pinned on the right.

