# Roadmap v2: one plan for the notebook (content and platform)

> **Status (2026-11-04):** content phases C1–C6 are built in v4 (see `handover.md` §12). Not done: all platform phases after P1 (hosting, Export/Import, sync, offline). You chose to skip P0/P1 before the exam.

Last updated: 2026-11-04. This merges the old roadmap (`roadmap.md`, 2026-11-03: website, sync, offline) with the end-sem content plan (v3 → v4) and what the semester handbook says. Nothing has been built from this yet; v3 is untouched.

> **Rule zero (updated).** The notebook exists to help you pass ADA and solve problems faster. Before the end-sem, spend platform effort on **P0 and P1 only** (about half a day). Everything else on the platform track waits until the exam is over. Every phase below leaves you with something that works, so you can stop after any of them.

---

## 1. Inputs, reconciled

**From v3 (checked in the file on 2026-11-04)**

- 24 sections: stops 0–14, the Ladder, and the exam tools (mock, drills, bugs, order, mistakes, practice, cards, cheat sheet).
- 147 embedded Python sources: all parse, 144 run clean; the other 3 read stdin or are fragments. The 5 JS scripts have no syntax errors.
- Stop quizzes exist for every stop. Counts: Greedy 6, Graphs II 7, Monotonic stacks 5, Toolkit 11 (two quizzes), and 5–10 for the earlier stops. **Correction:** an earlier analysis said stops 11–14 had no quizzes; that came from a partial read of the page and was wrong.
- **The real gap is the exam-practice pool.** The 10 extra mock-exam questions, the 15 spot-the-bug, 9 put-in-order and 22 fill-in-the-blank items cover stops 0–10 only. Nothing there touches Greedy, Graphs II, Monotonic stacks or the Toolkit. Seven questions for the whole Graphs II unit is also thin.
- Graphs II (about 590 words) and Monotonic stacks (about 570) are the thinnest stops; most others run 2,000–3,000 words.
- Already present, so build on it: `merge_sort`, `count_inversions`, `bellman_ford`, a union-find class, a Dijkstra lab, binary-search-on-answer (`first_true`), Fenwick tree, LIS with `bisect`, pointer-jumping (`build_jump`), and `count_sum_k`.
- Missing or very thin: trie (0 mentions), sparse table (0), segment tree (1), tree DP (2), digit DP (1), recursion limit (1), fast input (2), topological sort by DFS (0), hashing internals (0), no Export/Import (0).
- **The pipeline reproduces v3.** From `ada-notebook-source.zip`, `python build.py` produced a file identical to `ADA_Exam_Notebook_v3.html` (`cmp` clean), `tests/tests.py` printed ALL TESTS PASSED and `tests/t2.py` printed `vault ok`. `tests/chk.py` (browser check) was not run.
- Storage keys in use: `ada-done`, `ada-ladder-v2`, `ada-deck`, `ada-mock3`, `ada-endsem-date`, `ada-quick`, `ada-theme2`, plus legacy `ada-cf-ticks` and `ada-todo-newton-v2`. These match the old roadmap's sync table.
- The Mistakes deck stores ids shaped `kind:topic:index`, so inserting questions in the middle of a list would corrupt it.
- The timed-mock code looks problems up as `'cf:' + id` and builds only Codeforces URLs. LeetCode-format mocks need new lookup code.
- The title says "26 stops". That count includes the half stops (0.5, 1.5, …), so it is correct today but must change when stops are added.

**From the handbook (Semester 3, 2026–27)**

- ADA (CSA 311, 4 credits): Contest 1 was 11 Sep, Contest 2 was 30 Oct, mid-term was 16 Oct (the project notes list the mid-sem contest on 14 Oct). The end-sem (40%) is still ahead.
- **End-sem format (from `docs/context.md`, the teacher's note):** the last three end-sem problems are unseen Codeforces problems rated 1400, 1500 and 1600, on the Newton platform with partial (subtask) scoring. Date, duration, number of easier problems and any written section were unknown. The v3 Ladder already has three-rung Codeforces mocks (Exam M1–M6 at 1400/1500/1600). This conflicts with the earlier "LeetCode-style contest" assumption; see C3 and section 7.
- Evaluation: Assignments and Contests 30%, Mock AI Interview 10%, Mid-sem 20%, End-sem 40%. The outline's note about "90%" refers to an older table.
- Syllabus Graphs-II: shortest-path algorithms, **MST optional**. Topological sort, Dijkstra and MST appear in the learning outcomes. Merge sort is not in the syllabus (only Quick Sort).
- Outcomes that need practice beyond coding: dry-running to validate, debugging, and communicating solutions in code and in writing. This feeds the Mock AI Interview (10%).
- System-based (Athena) exam rules: no AI tools, no external pre-solution libraries, no tab switching, no VPN. **You confirmed `heapq`, `collections` and `bisect` are allowed**, so templates use them directly.

---

## 2. How the old roadmap and the content plan fit together

| Old roadmap item | Content-plan item | Merged decision |
|---|---|---|
| P1: fix stop-number collision (exam stops 11–18 vs stops 11–14) | Update "26 stops" and the hard-coded planner text | One fix in C1: relabel the exam stops X1–X8 (ids unchanged), update the title, the planner and the intro |
| P1: hero map has dots only for stops 0–10; quick-review not tuned for 11–14 | No bug, ordering, fill-in or extra mock items for stops 11–14 | Same gap. C1 makes stops 11–14 first-class: map dots, quick review, plus bug, ordering, fill-in and extra mock items |
| P2: per-stop quizzes for the pattern sections | About 25 new mock questions | Merged into C1 and C3. Append-only, never reorder |
| P2: Ladder data to JSON | New Ladder problems for every Phase 1 topic | Add the new problems in the current format now, behind a clean list so they move to JSON later (P2). Doing the restructure first would delay study |
| P2: link and rating verification scripts | New LeetCode problems with ratings | The build sandbox cannot reach LeetCode or Codeforces, so new LeetCode ratings ship as estimates marked ≈, like v3. P2b verifies them on your machine |
| P6: next-layer topics (SCC, bridges, LCA, tree DP, digit DP, matrix exponentiation) | Appendix reference page (SCC, bridges, LCA, balanced BSTs) | One reference page in C6. **Tree DP moves up into C4** because it joins trees, DP and topological sort. Digit DP and matrix exponentiation stay after the exam |
| P6: more quiz, bug and ordering drills | Same | Merged into C1, C3 and C5 |
| P5: re-solve queue, notes, miss tagging, timers, contest log | Mock contests, My-mistakes deck | Post-exam. If one feature is wanted earlier, make it the re-solve queue |
| P0–P4: git, hosting, sync, offline | Test discipline: every template run and brute-force checked | Same discipline. The source pipeline (`build.py`, `tests/`) would make this automatic, but the zip was not uploaded (see section 7) |
| Appendix D item 7: delete `ADA_Exam_Notebook_EndSem.html` | n/a | Do it in P0 |

---

## 3. Ground rules for all content work

1. v3 stays untouched. v4 is built as a copy.
2. Stop ids (`ch0`…`ch14`, `ladder`, `mock`, `drills`, `bugs`, `order`, `mistakes`, `practice`, `cards`, `cheat`) and storage keys never change, so saved ticks and the Mistakes deck survive.
3. **Append-only data.** New quiz, bug, ordering and fill-in items go at the end of their lists. New Ladder problems get new unique keys. Nothing is reordered or renumbered.
4. Every code template is run before it ships. Graph algorithms also get a brute-force comparison on random inputs (Dijkstra vs Bellman–Ford, Kruskal vs Prim, topological order validity, Floyd vs repeated Dijkstra). Every quiz answer is checked by running or by hand.
5. Templates use `heapq`, `deque` and `bisect`, which you confirmed are allowed in the end-sem. Individual problems can still forbid them (Contest 1 Q3 banned `heapq`), so a short "if a problem forbids it" note covers a hand-written heap and union-find, not a second copy of everything.
5a. **Work through the pipeline, never by hand-editing `dist/index.html`.** Code goes in `src/snippets/snips.py` with a test in `tests/tests.py`; text goes in `src/templates/`; quiz questions are appended to `QUIZ.<key>` in `src/js/`; new bug, ordering, fill-in and extra mock items are appended with `.push(...)` from an injected script (those arrays are defined earlier in the page, so appending cannot reorder anything). Rebuild, run `tests.py`, `t2.py` and `chk.py` before each handoff.
6. Recursion limit: LC 329 and LC 1857 can reach tens of thousands of nodes, so their templates use Kahn peeling or an iterative DFS, never plain recursive DFS.
7. Do not copy problem statements from LeetCode, Codeforces, CSES or Newton. Link to them. Hints and solutions are written fresh.
8. New stops follow the existing format: Big idea, Teacher's notes, Rules and code, Worked examples, Lab, Exam traps, Check yourself, Patterns for contests.
9. After each phase: summarise what was added and what was tested before starting the next.

---

## 4. The merged phase map

Two tracks. **Content** (C) is where the exam marks are. **Platform** (P) is the old roadmap. The order of work is P0, P1, C1…C6, then the rest of P after the exam.

### Platform before the exam

**P0: Safe foundation (1–2 h).** Same as old Phase 0: keep a second copy of everything, `git init`, private repo, tag `v3.0`, delete `ADA_Exam_Notebook_EndSem.html`. Add the CI workflow (Appendix C) only if the source pipeline is available.
*Done when:* a fresh clone gives you the same v3 file.

**P1: Online and portable (2–3 h).** Same as old Phase 1: deploy `dist/index.html` to Cloudflare Pages or GitHub Pages, add **Export / Import progress** buttons (format in Appendix A, merge rules in section 6), and a "last exported N days ago" nudge.
*Done when:* on a second computer you open the URL, import an export, and continue where you stopped.
*Note:* this also protects your mistakes deck while v4 is being built.

### Content track

**C1: Make stops 11–14 first-class (highest priority).**
- Extra mock-exam questions, spot-the-bug, put-the-lines-in-order and fill-in items for stops 11–14, none of which exist today: greedy, topological sort, Dijkstra (stale-entry check, marking on push vs pop), Bellman–Ford, Kruskal and the monotonic-stack template.
- Deepen the Graphs II quiz (7 questions for a whole unit); the other stop quizzes already exist.
- Hero map dots, quick-review mode and topic names for stops 11–14.
- Relabel the exam stops X1–X8; update the title and the end-sem planner widget; extend the syllabus map.

**C2: Graphs II, rebuilt.** Compact core first, full treatment after.
1. DAGs and topological sort: Kahn and DFS versions, cycle detection, DAG shortest and longest path, DP over a DAG. LC 207, 210, 329, 1857.
2. Dijkstra: `heapq` template with the stale-entry check, grids as graphs, "minimise the maximum" variants, why negatives break it. LC 743, 1631, 1514, 778.
3. Bellman–Ford and Floyd–Warshall: why V−1 rounds suffice, negative-cycle detection, the "at most k edges" form. LC 787, 1334.
4. MST in full (syllabus calls it optional, you asked for full): cut and cycle properties, Kruskal with tested union-find, Prim with a heap, when to prefer which. LC 1584, 684, 1135, 1489.
5. One decision page: BFS, 0-1 BFS, Dijkstra, Bellman–Ford, Floyd, topological DP; linked to the existing table in stop 12.
6. Hand-traced exercises stay: topological order, Dijkstra table, Bellman–Ford rounds, Kruskal.

**C3: Contest-style practice.**
- About 25 new mock-exam questions across Graphs II, greedy and monotonic stacks.
- New Ladder problems with difficulty ratings (estimates marked ≈) for every C2 topic.
- Timed 3-problem mocks. **Format needs your decision** (section 7): the teacher's note says Codeforces-style 1400/1500/1600, and Exam M1–M6 already exist, so more Codeforces-rung mocks plus a few easier warm-up problems fit with no new code. LeetCode-format mocks (easy, medium, hard) need a LeetCode URL builder, a lookup that accepts LeetCode ids, and mock names that do not clash with `ada-mock3` state.
- New bug and ordering items for the new algorithms.

**C4: Greedy, DP-II and the bridges between course tools.**
- Greedy extension (stop 11 already has the exchange argument and seven patterns): fractional knapsack proof, counterexamples (coin change, 0/1 knapsack), a "greedy or DP?" decision drill, LC 621 and 763, plus 55 and 45 where missing.
- DP-II: three full memo → table → one-row conversions, "convert this code" drills, LC 97 (missing), and harder grid and string DP.
- **Tree DP and DAG DP** (LC 337, 124, 543): trees, DP and topological sort together.
- **Binary search on the answer with a graph check:** BFS, DSU or Dijkstra as the feasibility test (second solution to LC 1631 and 778).
- **Union-find beyond MST:** components, accounts merging, weighted DSU (LC 721, 399).
- **Heap plus greedy scheduling:** meeting rooms, k-way merge, two-heaps median. First check what stop 5 already covers.
- A small **trie** page, tied to backtracking (Word Search II).

**C5: Contest readiness.**
- A full 3-hour ADA-weighted mock contest with answers, in whichever format you confirm for the end-sem, with the subtask habit built in (read the subtasks, submit the brute force first; Chakravyuh scored 0/120 although its brute force was worth about half).
- A "constraints → algorithm" drill.
- A Python-pitfalls page: recursion limit, fast input, `heapq` quirks (min-heap only, tuple tie-breaks), mutable defaults, copying lists, slicing cost.
- A final template sheet: about 12 algorithms to type from memory, each with an edge-case checklist.
- **Explain-it-aloud drills** for the Mock AI Interview: for each algorithm, state the invariant, justify the complexity, name edge cases, dry-run a tiny input.
- Updated intro, syllabus map and five-session plan.

**C6: Appendix and next layer (last).** Clearly marked as beyond the core outline.
- Merge sort: build on the existing `merge_sort` and `count_inversions`: stability, O(n) space, inversion counting in the merge (LC 912, 315, 493).
- Amortised analysis: dynamic-array doubling, why union-find and heap-build costs are what they are.
- Hashing basics: collisions, chaining vs open addressing, load factor (LC 146, 705, 706).
- One reference page: SCC, bridges, LCA with binary lifting, balanced BSTs, digit DP, matrix exponentiation, sparse table and segment tree, with pointers only.

### Platform after the exam

| Phase | What | Notes |
|---|---|---|
| P2 | Split output (HTML, CSS, JS, `ladder.json`, `quiz.json`), one file per stop, content-hashed asset names | Do this before the content files multiply further |
| P2b | `verify_cf.py`, `check_links.py`, `verify_lc_ratings.py`, weekly CI | Replaces ≈ estimates with checked ratings. Run on your own machine |
| P3 | Single `Store` module, sync with tombstones, Worker + token (personal) or Supabase (multi-user), nightly backup | Design in section 6 and Appendices A–B |
| P4 | PWA, service worker, self-hosted fonts, print stylesheet, accessibility pass | |
| P5 | Re-solve queue first; then notes, miss tagging, problem timers, contest log (record the end-sem too), stats, Codeforces auto-tick, weekly review | Pick by value; each is independent |
| P7 | Share with classmates, other courses, analytics, licensing | Mind spoilers: the Vault contains full solutions |

---

## 5. Schedule and effort

| Step | Rough effort | Marks relevance |
|---|---|---|
| P0 + P1 | half a day | protects progress |
| C1 | 1–2 days | high: fills the biggest testing gap |
| C2 | 3–4 days | high: Graphs-II is a named syllabus unit |
| C3 | 2–3 days | high |
| C4 | 2–3 days | medium–high |
| C5 | 2 days | high |
| C6 | 2 days | low for the exam; do only if time remains |

The content work is mostly mine; the plan is only useful if you spend most of your time solving problems, not reading. After each phase, solve at least two of its Ladder problems before moving on. If a new page is annoying to use, fix that before building the next one.

---

## 6. Sync design notes (unchanged from the old roadmap)

Everything the notebook stores is one of three shapes, so the merge is simple.

1. **Set of ticks** (`ada-done`, `ada-ladder-v2`): an item is a record `{key, value, updated_at}` where `value` is a timestamp when ticked and `null` when unticked. Merge per key by newest `updated_at`.
2. **Counter map** (`ada-deck`): per key, newest `at` wins.
3. **Single value** (`ada-endsem-date`): newest wins.

Edge cases to test on purpose:
- The same problem ticked on two devices a minute apart (keep either, but XP must not double-count; XP is computed from the set, so it can't).
- Unticked on A while offline, ticked on B: newest change wins, and the user sees the result.
- A device with the wrong clock: use the server's time for `updated_at` on push where possible.
- A legacy tick (`1`): treat its time as 0 so any dated change beats it.

---

## 7. Open items and risks

**Needed from you**

1. **End-sem format.** Is it Codeforces-style (unseen 1400/1500/1600 problems with subtasks, as the teacher's note in `context.md` says), LeetCode-style (as the earlier plan assumed), or has the format been announced differently since? This decides C3 and the C5 mock.
2. Whether the added LeetCode problems may carry estimated ratings (≈) until you run the verification scripts. Codeforces ratings are never added from memory, per the project rules.
3. Hosting and repo visibility for P0 and P1 (the old roadmap's decisions 1 and 4).
4. Agreement that P2 onward waits until after the end-sem.

**Resolved:** the source zip was received; it builds byte-identical to v3 and its tests pass. In the repo, replace `docs/roadmap.md` with this file and update `docs/handover.md` section 6 to match.

**Not re-verified:** the Cloudflare, GitHub and Supabase limits in the old roadmap's facts section were dated 2026-11-03 and carried over unchanged. Re-check them before relying on them.

**New risks**

| Risk | Mitigation |
|---|---|
| Inserting questions in the middle shifts the `kind:topic:index` ids and corrupts the Mistakes deck | Append-only rule (section 3) |
| LeetCode-format mocks break because lookup and URLs assume Codeforces | Add LeetCode support in C3 and test with one mock before writing more |
| Recursive DFS fails on large LeetCode tests in Python | Iterative templates; Python-pitfalls page (C5) |
| Estimated ratings mislead the Ladder | Keep the ≈ marker; verify in P2b |
| Platform work eats study time | Rule zero; P2 onward after the exam |
| Content is added but never used | Each phase ends with timed use, not reading |

The old roadmap's risk register still applies to the platform track and follows in full.

### Platform risk register (from the old roadmap)

Phase numbers in this table are the old roadmap's. Old Phases 0, 1, 3 and 4 are P0, P1, P3 and P4 here; the old Phase 2 verification scripts are P2b.

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Free-tier limits or policies change | medium | medium | Facts dated above; Export/Import means no lock-in; keep sync behind a thin adapter so the backend can be swapped |
| Supabase free project pauses after 7 days idle | high (if used) | medium | Worker route for personal use; or a weekly cron ping; or accept manual restore |
| Browser storage cleared, progress lost | medium | high before Phase 3 | Phase 1 export reminder; Phase 3 sync and nightly backup |
| Source lost with this chat or sandbox | high if nothing is done | high | Phase 0 today: zip, git, second copy |
| Sync bug overwrites good data | low | high | Tombstones, merge-not-overwrite, nightly backups, a "restore from backup" button |
| Sync token leaks | low | medium | Rotate the secret on the Worker; the token only reads and writes your own progress |
| Wrong ratings or dead links mislead the Ladder | medium | medium | Phase 2 verification scripts on a weekly schedule; estimated ratings stay marked with ≈ |
| Scope creep eats study time | high | high | Rule zero; the schedule above; features judged by "does this make me solve more, or better?" |
| Hint or fact is wrong | medium | low–medium | Hints written from memory of editorials are listed in Appendix D; re-verify against editorials |

---

## Appendix E: Hosting and sync decisions, and the facts behind them (from the old roadmap)


| Decision | Recommendation | Why | Alternatives | Revisit when |
|---|---|---|---|---|
| Source of truth | A git repository (GitHub, private is fine) | History, backup, free CI | Plain folder + zip | never |
| Hosting | **Cloudflare Pages**, serving the committed `dist/` folder | Free, unmetered static requests, deploys from git, no build step needed on their side | GitHub Pages (fewest accounts), Netlify | you want a feature they lack |
| Build | Keep the Python pipeline. Commit `dist/` | It works, it is tested, and a Python build step on the host would be one more thing to break | Move to Astro or Vite later | Phase 2 is done and the content files multiply |
| Sync, personal use | **A tiny Cloudflare Worker + KV or D1**, protected by a secret token | Same vendor as hosting, no inactivity pause, no accounts to manage for one user | Supabase | friends will use it |
| Sync, if others join | **Supabase** (login + Postgres with row-level security) | Ready-made auth | Firebase, a Worker with its own auth | you outgrow one user |
| Zero-backend fallback | Export/Import JSON file | Works today, works forever | none | never; keep it even after sync exists |

### Facts behind the hosting and sync choices (checked 2026-11-03; re-check before relying on them)

- **Cloudflare Pages, free plan:** 500 builds per month, one build at a time, 20-minute build timeout, 20,000 files per site, 25 MiB per file, 100 custom domains per project. Static requests are unmetered. Pages Functions use the Workers free allowance of 100,000 requests per day. Source: Cloudflare's Pages limits page, `developers.cloudflare.com/pages/platform/limits`.
- **GitHub Pages:** 1 GB published site, about 100 GB per month soft bandwidth, 10 builds per hour soft limit. Check whether your plan allows Pages from a *private* repository; if not, make the repo public or use Cloudflare Pages.
- **Supabase, free plan:** two active projects, 500 MB database, 50,000 monthly active users, **projects pause after 7 days of inactivity** and must be restored by hand, and there are no automatic backups. A pause is a real risk for a student who may skip a week during exams. Mitigation: a scheduled ping (a GitHub Actions cron job), or choose the Worker route.
- **Not verified:** Cloudflare D1 and KV free-tier numbers beyond "KV reads capped at 100,000 per day". Look them up before choosing between KV and D1. One user's progress is a few kilobytes, so either will fit.

---

## Appendix A: Export file format

```json
{
  "app": "ada-notebook",
  "schema": 1,
  "exportedAt": "2026-11-03T10:00:00.000Z",
  "data": {
    "ada-done": ["ch0", "ch1", "b0"],
    "ada-ladder-v2": { "98": 1762147200000, "cf:659E": 1762233600000 },
    "ada-deck": { "q:s4:2": { "n": 1, "at": 1762147200000 } },
    "ada-mock3": { "pick": "Exam M1 (1400 / 1500 / 1600)", "res": {} },
    "ada-endsem-date": "2026-11-28"
  }
}
```

Import rules: refuse files whose `app` or `schema` doesn't match; merge, never replace; show a summary ("+12 ticks, 2 mistakes") before applying.

## Appendix B: Supabase schema (multi-user mode only)

```sql
create table progress (
  user_id    uuid not null default auth.uid() references auth.users on delete cascade,
  key        text not null,
  value      jsonb,                         -- null = tombstone (unticked)
  updated_at timestamptz not null default now(),
  primary key (user_id, key)
);

alter table progress enable row level security;

create policy "own rows only" on progress
  for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

The browser uses the project's public anon key; the row-level-security policy is what keeps users out of each other's rows. Never put a service-role key in the page.

## Appendix C: CI workflow (GitHub Actions)

Check the action versions when you add it; they change.

```yaml
name: build
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python tests/tests.py
      - run: python tests/t2.py
      - run: python build.py
      - run: git diff --exit-code dist/   # fails if dist/ was not rebuilt and committed
```


## Appendix D: Known debt, updated

| # | Item | Status / where it is fixed |
|---|---|---|
| 1 | Exam stops numbered 11–18 collide with stops 11–14 (confirmed in the file) | C1: relabel X1–X8, ids unchanged |
| 2 | Hero map has dots only for stops 0–10 (topic names stop at `s10`) | C1 |
| 3 | Quick-review mode not tuned for stops 11–14 | C1 |
| 4 | About 128 LeetCode and 54 CSES links added from memory, not opened; ratings are estimates (≈) | P2b scripts |
| 5 | About 20 Codeforces hints written from memory of standard solutions | After the exam; re-verify against editorials |
| 6 | Ladder Codeforces ratings read once from a problem list; nothing re-checks them | P2b `verify_cf.py` |
| 7 | `ADA_Exam_Notebook_EndSem.html` claims every rating was checked but several were not | P0: delete it |
| 8 | Fonts load from Google | P4 |
| 9 | No extra mock, bug, ordering or fill-in items for stops 11–14; Graphs II quiz has 7 questions (corrected finding; the stop quizzes themselves exist) | C1 |
| 10 | Title ("26 stops", includes half stops), planner widget ("stop 10, 12, 13, 14") and syllabus map are hard-coded | C1 and C5 |
| 11 | Mock lookup and URL builder assume Codeforces ids (only matters if LeetCode-format mocks are chosen) | C3 |
| 12 | No Export/Import exists yet | P1 |
