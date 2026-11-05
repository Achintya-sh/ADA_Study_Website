# Handover

Last updated: 2026-11-04 (v4). Written for whoever picks this project up next: the user in a new session, a new AI chat, or another developer.

Read `context.md` first (what the project is and the rules it follows). `roadmap.md` says where it's going. This file says **where things stand and how to work on them**.

---

## 1. Status at a glance

| Area | State |
|---|---|
| Notebook content (stops 0–17, Ladder, Vault, drills, mocks) | **v4 built** as `ADA_Exam_Notebook_v4.html`; v3 is kept unchanged |
| Build pipeline | **Done**, tested, reproduces v3 byte for byte |
| Code samples | **Tested** against brute force (64 blocks) |
| Hosting, accounts, sync, offline | **Not started.** Roadmap phases 0–4 |
| Known defects | Listed in section 7; none blocks studying |
| Unverified facts | Listed in section 8 |

**One-line summary:** the study material is finished and working as a single file; turning it into a hosted site with synced progress is the next job, and the very first step (put the source in git and keep a second copy) has not been done yet.

---

## 2. What was delivered

| File | What it is | Keep? |
|---|---|---|
| `ADA_Exam_Notebook_v3.html` | The current notebook. One self-contained file, about 840 KB | **Yes: this is the product** |
| `ada-notebook-source.zip` | The full source pipeline plus these three docs (see section 3) | **Yes: this is the only place the sources live** |
| `notebook_code_snippets.py` | A copy of all tested code samples. Optional; it contains the Vault solutions, so it's a spoiler | Optional |
| `roadmap.md`, `context.md`, `handover.md` | The documents | Yes |
| `ADA_Exam_Notebook_EndSem.html` | An **earlier** version. Superseded. It claims all Codeforces ratings were checked; several were not | **Delete it** |

The original notebook the user supplied is `ADA_Exam_Notebook2222.html`; a copy is inside the zip as `src/original/nb.html`.

### History in one paragraph

The user's original notebook had 22 stops plus a "Contest line" (C1–C5) built for Contest 2. A second version (the EndSem file) added an "End-sem line" (E0–E4); it's superseded. Version 3 dissolved both lines into the topic stops, added four stops (11 Greedy, 12 Graphs II, 13 Monotonic stacks, 14 Contest toolkit), rebuilt the Ladder as a tiered, gamified list rated on both Codeforces and LeetCode scales, and added the Vault of original problems.

---

## 3. Getting running (10 minutes)

**Prerequisites:** Python 3.10 or newer. For the browser check only: `pip install playwright` then `playwright install chromium`.

```bash
unzip ada-notebook-source.zip && cd ada-notebook
python build.py                          # writes dist/index.html
python tests/tests.py                    # ends with: ALL TESTS PASSED
python tests/t2.py                       # prints: vault ok
python tests/chk.py                      # optional: loads the page in a headless browser
```

Expected from `chk.py`: `errors: none`, 7 sidebar groups, 26 stops, 354 Ladder rows, no dead links, no unfilled `{{code:…}}` placeholders. The only "stale" hit it may print is the phrase "Contest line" in the "What changed" box, which is intentional. It also lists two `lab failures`: those are the heap checker and the coin-greedy labs, which **deliberately** show a red wrong-answer caption.

To confirm your build matches the delivered file: `cmp dist/index.html ADA_Exam_Notebook_v3.html` (no output means identical).

### Repository layout

```
ada-notebook/
├── build.py                       assembles dist/index.html
├── src/
│   ├── original/nb.html           the user's original notebook (input, do not edit)
│   ├── snippets/snips.py          every code sample, in blocks marked  #@@ name
│   ├── templates/
│   │   ├── templates_a.html       pattern sections for stops 3, 4, 5, 6
│   │   ├── templates_b.html       graph, DP and greedy patterns; the Graphs II stop
│   │   └── templates_c.html       monotonic stack stop, toolkit stop, the Ladder stop and Vault
│   └── js/
│       ├── e_widgets.js           labs (Chakravyuh, knapsack direction, Dijkstra, plan), quizzes, drills
│       └── ladder.js              the Ladder data and widget, three-rung mocks, monotonic quiz, SECMAP
├── tests/
│   ├── tests.py                   every snippet vs a brute force (about 30 s)
│   ├── t2.py                      Vault brute forces and the Frozen Middle rule
│   └── chk.py                     headless-browser structural check
├── dist/index.html                build output
└── docs/                          roadmap.md, context.md, handover.md
```

---

## 4. How to do the common jobs

### Add a Ladder problem
1. Open `src/js/ladder.js` and find the topic's section.
2. Add one line with the right helper:
   - Codeforces: `C('1418C', 'Mortal Kombat Tower', 'dp', 'pattern text', 1500, 'optional hint')`. The **rating must be read from Codeforces**; otherwise use an estimate helper.
   - LeetCode: `L(98, 'validate-binary-search-tree', 'bst', 'pattern text', 'm')`, where the last letter is `e`, `m`, `M` or `h` (easy 900, medium 1300, medium-hard 1500, hard 1750 estimated), or pass a real rating as the 6th argument.
   - CSES: `S(1645, 'Nearest Smaller Values', 'mono', 'pattern text', 1400)`. The last number is an estimate.
   - Original Vault problem: `O('key', 'Title', 'topic', 'pattern', estimate, 'trick')` plus a matching `<div class="prob" id="v-key">` in `templates_c.html`.
3. Topic keys: `arr sort bst heap mono bt graph g2 dp greedy`. Give a hint or trick (the 7th and 8th arguments) to make the problem appear in the Vault tab.
4. Duplicates are ignored by key, so adding the same problem twice is harmless.
5. `python build.py && python tests/chk.py`.

### Add a tested code sample to a page
1. Add a block to `src/snippets/snips.py`: a line `#@@ my_name`, then self-contained code (its own imports at the top).
2. **Add a test** in `tests/tests.py` (or `t2.py`) comparing it with a brute force on random small inputs.
3. In a template, write `{{code:my_name}}` where the code should appear.
4. Build. The build fails loudly (`missing code block my_name`) if the name doesn't match.

### Edit text on a page
Edit the matching block in `src/templates/templates_*.html`. Blocks are separated by `<!--@@ name -->` lines: `ch3 ch4 ch5 ch6` (A); `ch8_head ch8_func ch10_head ch10_knap ch11_extra ch12` (B); `ch13 ch14 ladder` (C). Content for stops 0–2 and 7–10 that came from the original notebook lives in `src/original/nb.html`; the build pulls the old contest-line bodies (`c2`, `c3`, `c4`) from there.

### Add a quiz question
Append to `QUIZ.<key>` in `ladder.js` or `e_widgets.js`: `{ q, o: [4 options], a: indexOfCorrect, why }`. Quiz keys and their stops are listed in `context.md` §5.3. Register a new key's readable name in `TOPIC_NAMES` and, if it is not a plain `sN` key, in `SECMAP`, so the mock exam's "weak topic" link works.

### Add a lab (interactive widget)
Write `function wMyLab(b) { … }` using the helpers `h()`, `sv()`, `btn()`, `Stepper()`, and register it: `Object.assign(WIDGETS, { mylab: wMyLab })`. Place `<div class="lab" data-w="mylab" data-title="…"></div>` in a template.

### Add a whole new stop
Copy `head(...)` usage in `build.py` (see `ch11`–`ch14`), add the new template block, add it to `new_block` in the right DOM position, set its `data-group` to one of `found trees bt graph dp ladder exam`, and make its id match `ch<number>` so progress counting includes it.

### Change tiers, XP or ranks
`TIERS`, `RANKS` and the thresholds are near the end of the data section in `ladder.js`. Ranks use fractions of the total available XP, so adding problems rescales them automatically.

---

## 5. Gotchas learned the hard way

**Build and structure**
- `inject()` in `build.py` asserts that each stop's own quiz marker (`<div class="quiz" data-quiz="s3"></div>` and so on) appears exactly once in the original. Changing that markup breaks the build, by design.
- The build removes the sections `c1…c5` from the original by position and recovers `c2`, `c3`, `c4` bodies by regex. Don't reorder or rename those sections in `nb.html`.
- Internal links of the form `#c1…#c5`, `#e0…#e4` are rewritten by `build.py` using a map; a new link to a removed id would be a dead link. `chk.py` lists dead links.
- Python code in HTML must not contain the text `</script>`.

**Storage**
- Don't rename or reshape the `ada-*` keys (see `context.md` §5.4): they hold the user's progress.
- Unticking a problem **deletes** its key. A future sync layer must use tombstones (see `roadmap.md` §5).

**Facts**
- When reading Codeforces problem lists, the **rating follows the tags**: the order is id, name, tags, rating, solved-count. Reading it as "rating then name" attributes a neighbour's rating to the wrong problem. This happened once during the build and was caught.
- Python 3.10 features appear in a few samples (`int.bit_count`, `itertools.pairwise`, `bisect` with `key`); they're marked in the text where it matters.

**Tooling**
- Headless screenshots can hang if the page uses smooth scrolling. Inject `html{scroll-behavior:auto!important}` before capturing.
- A sandbox with no outside network cannot reach Codeforces, so rating checks must be run on a machine that can (the roadmap's `verify_cf.py`).
- The original working folder used while building was `/home/claude/site` and is **temporary**. Only the zip is durable.

---

## 6. Prioritised open items

**P0: do these first**
1. **Put the source under version control and make a second copy** (`roadmap.md` Phase 0). Acceptance: a fresh clone builds a file identical to v3.
2. **Delete `ADA_Exam_Notebook_EndSem.html`** and anything linking to it.
3. **Fix the stop-number collision** (known issue 1). Where: Exam-prep sections in `nb.html` have `data-num` 11 to 18 and matching badge text. Add a post-processing step in `build.py` that renames them (for example `X1`…`X8`) in both the `data-num` attribute and the `<div class="badge">`. Acceptance: no two sidebar entries share a number.

**P1**
4. **Export / Import progress** (roadmap Phase 1; format in roadmap Appendix A). Acceptance: export on one browser, import on another, same stops understood and Ladder ticks.
5. **Host it** (Cloudflare Pages serving `dist/`).
6. **Verification scripts**: `verify_cf.py`, `check_links.py`, `verify_lc_ratings.py` (roadmap Phase 2). Run them once and fix whatever they find.
7. **Hero map dots for stops 11–14** and a quick-review pass over the new stops.

**P2**
8. Move the Ladder data to JSON and split content into one file per stop (roadmap Phase 2).
9. The sync layer (Phase 3), PWA (Phase 4), then the Phase 5 features.
10. Next-layer topic pages (SCC, bridges, LCA, tree DP, digit DP, matrix exponentiation) if the user asks for them.

---

## 7. Known defects

| # | Defect | Severity |
|---|---|---|
| 1 | Exam-prep stops numbered 11–18 collide with new stops 11–14 | cosmetic |
| 2 | The hero route map has no dots for stops 11–14 or the Ladder | cosmetic |
| 3 | Quick-review mode wasn't re-tuned for the new stops | minor |
| 4 | Progress is per browser | the reason for the roadmap |
| 5 | Fonts load from Google; offline falls back to system fonts | minor |

---

## 8. What is and isn't verified

**Verified**
- Every code sample: tested against brute force or known answers.
- Vault solutions: tested against their brute forces (Chakravyuh Reversed over every possible graph for n ≤ 5; Frozen Middle over every permutation for n ≤ 6 and every k).
- The page loads with no script errors; all labs step through; no dead internal links; it renders on a phone-width dark screen.
- Codeforces ratings: each was read from a Codeforces problem list.

**Not verified**
- About 128 LeetCode and 54 CSES links were typed from memory; none were opened. A wrong slug gives a 404.
- Ratings for those problems are **estimates** (shown with ≈).
- About 20 Codeforces hints came from memory of the standard solutions.
- The "late" labels on contest problems rest on the reading of the orange 2x badge.

If you deliver changes, say plainly which of these categories each new fact falls into.

---

## 9. Decisions waiting for the user

1. Hosting: Cloudflare Pages (recommended) or GitHub Pages.
2. Sync: just the user (Worker and a token) or others too (Supabase and login).
3. Repository public or private.
4. Domain: free `*.pages.dev`, or paid.
5. Which Phase 5 features are worth building.
6. The end-sem date and format, once announced (it changes how much website work is sensible; see roadmap §6).

---

## 10. Ready-to-paste starter prompt for a new AI chat

> I'm continuing a project. I've attached `context.md`, `handover.md`, `roadmap.md` and `ada-notebook-source.zip`. Read the three documents first, then unzip the source and run `python build.py`, `python tests/tests.py` and `python tests/t2.py` to confirm the project builds and the tests pass; tell me what you see.
>
> Follow the working preferences in `context.md` §3 (plan first and ask me questions before anything large; be honest about what you verified and what you didn't; never put an unverified Codeforces rating on the Ladder). Don't edit `dist/index.html` by hand.
>
> My end-sem date is **[fill in, or "not announced"]**. Today I want to work on: **[choose from handover §6, for example "P0 items 1–3" or "roadmap Phase 1"]**.

---

## 11. Before you hand work back

- [ ] `python tests/tests.py`, `python tests/t2.py`, `python build.py`, `python tests/chk.py` all clean.
- [ ] `dist/index.html` was rebuilt, not hand-edited.
- [ ] New code samples have tests; new Codeforces ratings were read from Codeforces; estimates are marked ≈.
- [ ] Storage keys unchanged, or a migration written.
- [ ] The zip and the three docs are regenerated and the version noted.
- [ ] The final message states what changed, what was checked, and what wasn't.


---

## 12. What v4 changed (2026-11-04)

**New and rebuilt content**
- **Stop 12 Graphs II** rebuilt: topological sort (Kahn and iterative DFS), DAG DP, LC 207/210/329/1857, Dijkstra with the stale-entry proof and why negatives break it, minimise-the-maximum (LC 1631/778/1514), Bellman–Ford (why V − 1 rounds; at most k edges, LC 787), Floyd–Warshall (LC 1334), MST in full (cut and cycle properties, Kruskal, Prim, LC 1584/684/1135/1489), a decision page, and four hand-trace exercises.
- **Stop 11** gains two written-out exchange arguments, the standard counterexamples and tested LC 621/763/55/45/452 code. **Stop 10** gains three memo → table → one-row conversions (LCS, edit distance, LC 97) and drills.
- **New stops:** 15 Bridges (tree DP, DAG DP, binary search + check, union-find extras, two heaps, trie), 16 Contest readiness (constraints, Python pitfalls, 13-template sheet, explain-it-aloud, a 3-hour LeetCode mock with answers, syllabus map), 17 Appendix (merge sort, amortised analysis, hashing, what comes next).
- **Practice items appended** (never inserted, so saved ids stay valid): 26 mock extras, quiz questions for stops 11, 12, 15, 16, 17, 7 fill-ins, 8 bug hunts, 4 ordering puzzles. Source of truth: `src/data/exam_v4.py`, turned into JSON by `build.py`.
- **Ladder:** 26 new LeetCode problems (380 rows). **Mocks:** nine three-problem LeetCode mocks (`src/js/lc_mocks.js`, storage key `ada-mock-lc`).
- **Defects 1–3 fixed:** exam-prep stops relabelled X1–X8, hero map second row for stops 11–17, quick review checked on the new stops.

**New files:** `src/templates/templates_d.html`, `src/js/c_extra.js`, `src/js/lc_mocks.js`, `src/data/exam_v4.py`, `tests/t3.py` (Graphs II), `t4.py` (all other new code), `t5.py` (exam items run for real), `chk4.py` (browser test of every new interactive item).

**Release routine now:** `python build.py`, then `tests/tests.py`, `t2.py`, `t3.py`, `t4.py`, `t5.py` (all must pass), then `python tests/chk.py` and `python tests/chk4.py` (browser).

**Not verified in v4**
- The new LeetCode slugs and Easy/Medium/Hard labels were typed from memory and never opened; Ladder ratings for them are estimates (shown with ≈).
- No new interactive labs were built (stop 12 reuses the Dijkstra lab).
- End-sem format: `context.md` §1 records a teacher note (unseen Codeforces 1400/1500/1600); the user later said the end-sem is LeetCode-style. v4 supports both: the Codeforces rungs (Exam M1–M6) and the LeetCode mocks.
- `heapq`, `collections` and `bisect` are allowed in the end-sem (user, 2026-11-04); individual problems can still forbid them (Contest 1 Q3 did).
