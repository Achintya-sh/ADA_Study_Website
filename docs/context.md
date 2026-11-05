# Project context: the ADA study notebook

Last updated: 2026-11-04. v4 note: the user says the end-sem is LeetCode-style; the teacher note below said unseen Codeforces problems. v4 serves both.

**What this file is.** A self-contained description of the project, written so that a new person, or a new AI chat with no memory of how it was built, can understand what exists, why, and what rules it follows. It is **project knowledge, not a chat transcript**: nothing here depends on any earlier conversation. Pair it with `handover.md` (how to work on it) and `roadmap.md` (where it's going).

**How to use it with a new AI chat.** Attach this file, `handover.md`, `roadmap.md` and `ada-notebook-source.zip`, then paste the starter prompt at the end of `handover.md`.

---

## 1. The student and the course

- **The user** is a B.Tech CS & AI student at Newton School of Technology (cohort label seen on the platform: NST'25 CS+AI RU), studying for the **end-semester exam** of the algorithms course and wanting to become a genuinely better programmer, not just to pass.
- **Course:** Analysis and Design of Algorithms, code CSA 311, B.Tech CS & AI, 2026–27 Semester 3, core, 4 credits, LTP 2-0-4, regular classroom, 12 weeks.
- **Pre-requisites stated by the course:** one programming language, arrays and trees, recursion. The course is taught in Python.
- **Reading:** *Introduction to Algorithms*, 3rd edition (CLRS).
- **Evaluation (as the course outline's table shows):** Assignments and Contests 30%, Mock AI Interview 10% (conceptual questions plus hands-on coding), Mid-sem 20%, End-sem 40%. The outline carries a note that an earlier draft totalled 90% and needed correction; the table as shown totals 100%.
- **Weekly plan:**

| Weeks | Content |
|---|---|
| 1 | Problem-solving foundations; complexity analysis (time and space, Big-O, best/average/worst case) |
| 2–4 | Advanced sorting (Quick Sort); binary trees and BSTs (insert, delete, search; problem solving) |
| 5–6 | Heaps (min/max heap, priority queues); backtracking |
| 7–8 | Graphs I: representation (adjacency list/matrix), DFS, BFS |
| 9–10 | DP I: memoization; Climbing Stairs, House Robber |
| 11 | Graphs II: shortest paths; minimum spanning tree (optional) |
| 12 | DP II: memoization, tabulation, space optimisation |

Each week has a code-based quiz and a coding assignment. The outline highlights "monotonic stacks" as a modern topic, and its learning outcomes stress dry runs, test cases, debugging and communicating solutions in code and in writing.

### What the teacher said about the end-sem

A note from the teacher, paraphrased: the last problem of Contest 2 was a Codeforces 1600-rated problem (it was Chakravyuh), and **the last three End-sem problems will be unseen Codeforces problems rated 1400, 1500 and 1600**. The end-sem date, duration, number of easier problems and any written section are **not yet known**.

---

## 2. The contest history

Three coding contests have happened on the Newton platform. Scores are per problem; many are marked "Partial" (scored by tests or subtasks). On the platform, an orange **2x** badge appears on problems solved before the deadline; problems without it were solved afterwards ("Solving after deadline" is shown on the contest card). That reading of the badge is an inference from the screenshots, not documented.

**Contest 1, 11 Sep 2026, 85 marks** (BSTs, heaps, Quick Sort)

| Q | Problem | Score | When |
|---|---|---|---|
| 1 | Minimum in BST | 40/40 | in time |
| 2 | Second Minimum in a Heap | 40/40 | in time |
| 3 | Insertion in Min Heap (heapq prohibited, O(log n)) | 20/40 | late |
| 4 | Validate BST | 40/80 | late |
| 5 | Implementing Quick Sort, reverse sorted (descending) | 80/80 | in time |
| 6 | Create a Balanced BST from a Binary Tree | 120/80 | in time |

**Mid-sem contest, 14 Oct 2026, 70 marks**

| Q | Problem | Score | When |
|---|---|---|---|
| 1 | Inorder Traversal of BST | 40/40 | in time |
| 2 | Adjacency Matrix to Edge List | 40/40 | in time |
| 3 | Convert Array to Min Heap | 40/40 | in time |
| 4 | Generate Parentheses | 40/80 | late |
| 5 | Min Cost Climbing Stairs | 40/80 | late |
| 6 | Signal Propagation at Time K (multi-source BFS, exactly at time k) | 120/120 | in time |
| 7 | Palindrome Partitioning | 0/120 | still open |

**Contest 2, 30 Oct 2026, 80 marks**

| Q | Problem | Score | When |
|---|---|---|---|
| 1 | Bag of Coins (at most two coins) | 40/40 | in time |
| 2 | Apple Baskets | 40/40 | in time |
| 3 | Count Graph Components | 80/80 | in time |
| 4 | 0/1/2 Knapsack | 40/80 | late |
| 5 | Chakravyuh (Codeforces 1600 level) | 0/120 | still open |

**What the user said about the late solves:** they came from *not having studied the topic yet* when the contest ran. They are **not** evidence of a recognition weakness. (An earlier analysis suggested "mediums with a trap" were the weakness; the user corrected that, and this document records the corrected reading.)

**The lesson that did hold up:** Chakravyuh scored 0/120 although its first subtask (n ≤ 10³) needed only an eight-line brute force worth roughly half the marks. The notebook now teaches *read the subtasks, write the brute force, submit it, then look for the trick*.

---

## 3. The user's goals and working preferences

Treat these as standing instructions.

**Goals**
1. Do well in the end-sem (40% of the grade) and the Mock AI Interview (10%).
2. "Truly master" the course: go beyond the outline where it helps become a better programmer, but stay inside the course's topic areas (sorting, trees, heaps, backtracking, graphs, DP, greedy and their natural neighbours).
3. Practise at a difficulty **above** the exam's: a pyramid with a wide base at 1200–1800, a Summit tier at 1900–2300, and an **Ego tier** at 2400+ ("for personal ego"). The exam itself is expected to be about 1400–1600; the base of the pyramid is where marks are won.

**How the user likes to work**
- **Plan first, then build.** For a large task, produce a plan, search the web, and ask questions before building. After the user answers, build.
- **Honesty over reassurance.** The user accepted and valued corrections of earlier mistakes, including an overclaim about verified ratings. Say what was checked and what was not.
- **Rewarding and satisfying practice.** The Ladder is preferred over a checklist: XP, ranks, streak, tiers, "surprise me". The old contest to-do checklist was deliberately deleted.
- **Both rating systems.** Codeforces and LeetCode ratings are both shown.
- **No in-page judge.** Links, hints and editorials are enough. (Offered and declined.)
- **Unusual, unpredictable problems** like Chakravyuh: hard because the *pattern* is new, not because the code is long.
- **Ladder placement:** after all the stops and before Exam prep.
- **Everything verifiable.** Prefer tested code and sourced facts.

---

## 4. The product

**Name:** the ADA study notebook ("Algorithms from zero: 26 stops, then the Ladder").
**Current delivered file:** `ADA_Exam_Notebook_v3.html` (about 840 KB, one self-contained file; fonts load from Google Fonts).

### 4.1 Structure

The notebook is a sequence of **stops** (one topic each) shown in a sidebar styled like a transit map. A **half stop** (numbers like 2.5) is a short bridge teaching background the next stop assumes. Every stop follows the same order: Big idea, Teacher's notes, rules then code, worked examples, a Lab (interactive), Exam traps, Added-missing-from-your-notes, Check yourself (quiz), and a "Mark as understood" button.

| id | Stop | Group |
|---|---|---|
| ch0 | 0 Prerequisites primer | Foundations |
| b0 | 0.5 Tracing code by hand | Foundations |
| ch1 | 1 Problem-solving foundations | Foundations |
| b1 | 1.5 Growth, limits and induction | Foundations |
| ch2 | 2 Complexity analysis | Foundations |
| ch14 | 14 **Contest toolkit** | Foundations |
| b2 | 2.5 Swaps, pointers and partitions | Sorting and trees |
| ch3 | 3 Quick Sort | Sorting and trees |
| b3 | 3.5 Names, references, linked lists | Sorting and trees |
| ch4 | 4 Binary Search Trees | Sorting and trees |
| b4 | 4.5 Complete trees and priority queues | Sorting and trees |
| ch5 | 5 Heaps | Sorting and trees |
| ch13 | 13 **Monotonic stacks and queues** | Sorting and trees |
| b5 | 5.5 Counting choices | Backtracking |
| ch6 | 6 Backtracking | Backtracking |
| b6 | 6.5 Pairs, sets and grids | Graphs |
| ch7 | 7 Graphs: concepts and representation | Graphs |
| b7 | 7.5 One loop, two bags | Graphs |
| ch8 | 8 DFS and BFS | Graphs |
| ch12 | 12 **Graphs II: order, cycles, weights** | Graphs |
| b8 | 8.5 Caches and greedy choices | Dynamic programming and greedy |
| ch9 | 9 Dynamic Programming I | Dynamic programming and greedy |
| b9 | 9.5 Prefixes and 2D tables | Dynamic programming and greedy |
| ch10 | 10 Dynamic Programming II (2D) | Dynamic programming and greedy |
| ch11 | 11 **Greedy algorithms** | Dynamic programming and greedy |
| ladder | L **The Ladder** | The Ladder |
| b10 | 10.5 Choosing the technique | Exam prep |
| mock, drills, bugs, order, mistakes, practice, cards, cheat | Mock quiz exam, Syntax recall drills, Spot the bug, Put the lines in order, My mistakes, Practice problems, Flashcards and glossary, Cheat sheet | Exam prep |

Bold = added in v3. The DOM order differs from the sidebar order: stops 11–14 and the Ladder sit after stop 10.5 in the page, and the sidebar groups them by topic.

### 4.2 The "Patterns for contests" sections

Stops 3, 4, 5, 6, 8 and 10 end with a section of that name (and stops 11–14 are built around the same idea). Each has: a table of *words in the statement → tool*, tested templates, traps, and a **"Seen in your contests"** box naming which of the user's contest problems the topic covers. Functional graphs (Chakravyuh) live in stop 8; the knapsack family and the memo → table → one-row conversion live in stop 10; the free-pass Dijkstra, Kahn, 0-1 BFS, Bellman–Ford and union-find live in stop 12.

### 4.3 The Ladder

354 problems in 12 tabs (All, Arrays and search, Sorting, BST, Heaps, Monotonic stack, Backtracking, Graphs, Graphs II, DP, Greedy, Vault).

**Rating system.** Each problem has a Codeforces rating (`cf`), a LeetCode contest rating (`lc`), or an estimate (`est`). Display: `CF 1600`, `LC 2000`, and for anything without a CF rating `≈CF 1600`. The effective rating used for tiers is the CF rating if present, else `LC rating − 400`, else the estimate. The `−400` rule is a heuristic of this project, not an official conversion; it comes from the project's earlier note that CF 1600 corresponds roughly to LC 1900–2100.

**Tiers, XP, ranks**

| Tier | Effective rating | XP per solve | Problems |
|---|---|---|---|
| Warm-up | below 1200 | 1 | 45 |
| Foundation | 1200–1399 | 2 | 117 |
| Exam rung | 1400–1699 | 4 | 97 |
| Climb | 1700–1899 | 8 | 55 |
| Summit | 1900–2399 | 16 | 28 |
| Ego | 2400 and up | 32 | 12 |

Ranks run Newcomer, Apprentice, Contestant, Specialist, Expert, Candidate Master, Master, International Master, Grandmaster of ADA, with thresholds at 0, 3, 8, 16, 28, 42, 58, 75 and 92 percent of the total available XP. A streak counts consecutive days with a dated tick. "Surprise me" picks from the six easiest unsolved problems in the current view.

**Sources of problems:** the original LeetCode ladder (102 problems, ratings from the community LeetCode contest ratings), added LeetCode classics (unrated, estimated), CSES tasks (estimated), Codeforces problems (ratings read from Codeforces), and six original Vault problems.

### 4.4 The Vault

Six original problems written in the style of Chakravyuh, each with a plain statement, two subtasks, one hidden observation, hints, the subtask-1 brute force, and the full solution. Each solution was checked against its brute force.

| Problem | Estimated | Trick |
|---|---|---|
| Chakravyuh Reversed | ≈CF 1900 | build a functional graph from the reachable-node counts |
| Odd Walk | ≈CF 1700 | BFS on (vertex, parity) |
| Free Passes | ≈CF 1900 | Dijkstra on (node, passes used) |
| Visible Pairs | ≈CF 1800 | monotonic stack of (height, count) |
| Split the Treasure | ≈CF 2000 | meet in the middle |
| Frozen Middle | ≈CF 1700 | positions n−k … k−1 can never move |

The Vault tab also lists 8 real Codeforces problems chosen for the same quality, labelled by trick.

### 4.5 Other features

Interactive labs for most stops (BST, heap, DFS/BFS, DP tables, the Chakravyuh walker, the knapsack-direction lab, Dijkstra, and more), stop quizzes, a 20-question mock exam built from all quizzes, syntax recall drills, spot-the-bug, put-the-lines-in-order, a **My mistakes** deck that collects every miss, flashcards and glossary, a cheat sheet, a quick-review mode (about 20 minutes), full-text search, a dark/light theme, a plan-for-today lab keyed to the end-sem date, and timed mocks: three-rung Codeforces mocks (Exam M1–M6, Summit S1–S3, Ego X1–X2) scored "nothing / partial / full", and the older LeetCode mocks A–H.

---

## 5. Technical architecture

### 5.1 The delivered artefact

One HTML file. Inside, in order: `<head>` with a Google Fonts link and one `<style>` block (design tokens as CSS custom properties, light and dark themes, a colour per "line"); `<body>` with a sidebar `nav`, a main column of `section.topic` elements, then script blocks:

1. core helpers, the `Stepper`, `QUIZ` data, the lab widgets, chapter quizzes (global `WIDGETS` registry, `h()`/`sv()` DOM helpers, `ls2Get/ls2Set`);
2. exam data (`TOPIC_NAMES`, `EXTRA_QS`, `BLANKS`, `BUGS`, `LADDER` and `MOCKS` data, contest widgets);
3. **injected by the v3 build:** `e_widgets.js` (labs: Chakravyuh walker, knapsack direction, Dijkstra, plan-for-today; the Vault and stop quizzes; drills) and `ladder.js` (the Ladder, the three-rung mocks, the monotonic-stack quiz, `SECMAP`);
4. the main script: theme, navigation and progress, search, quick-review, quizzes mounting, the mock exam, the mistakes deck, the drills.

Code samples on the pages are written as `<script type="text/plain" class="code">…</script>` and turned into highlighted blocks at load time.

### 5.2 The build pipeline (the real source of truth)

```
src/original/nb.html        the user's original notebook (input; never edited by hand)
src/snippets/snips.py       every code sample, in blocks marked  #@@ name
src/templates/templates_*.html   new and added content, with  {{code:name}}  placeholders
src/js/e_widgets.js, ladder.js   widgets, Ladder data, quizzes
build.py                    assembles dist/index.html from the above
tests/tests.py, t2.py       test every snippet against a brute force
tests/chk.py                loads the built page in a headless browser
dist/index.html             the output
```

`build.py` removes the old contest sections, writes the new stops and the Ladder, injects the pattern sections before each stop's own quiz, rewrites internal links, patches the sidebar groups and the mock-exam section mapping, adds CSS, and inserts the two script files. It is deterministic: rebuilding reproduces the delivered file exactly.

### 5.3 Conventions in the content

- **Box types:** `box idea` (big idea), `box tip`, `box warnbox`, `box trap` (exam trap), `box remember`, `box analogy`.
- **Labs:** `<div class="lab" data-w="name" data-title="…"></div>`, mounted from the `WIDGETS` registry.
- **Quizzes:** `<div class="quiz" data-quiz="key"></div>`, with the questions in the global `QUIZ[key]` and a readable name in `TOPIC_NAMES[key]`.
- **Keys for dissolved material:** the quiz keys `c1` (toolkit), `c2` (graph patterns), `c3` (DP patterns), `c4` (greedy), `e0` (functional graphs), `e1` (routine), `e2` (knapsack), `e3` (Graphs II) and `m13` (monotonic) kept their historical names; `SECMAP` maps them to stop ids so "weak topic" links from the mock exam land correctly.
- **Stop ids:** `chN` main stops, `bN` bridges (`bN` is stop N.5). The id regex that counts progress matches `ch`, `b`, `c` or `e` followed by digits.

### 5.4 State and storage

Everything is in the browser's `localStorage` as JSON, under these keys:

| Key | Content | Notes |
|---|---|---|
| `ada-done` | array of stop ids marked "understood" | |
| `ada-ladder-v2` | map problem-key → tick time in ms (older ticks are `1`) | keys: LeetCode id as a string; `cf:<id>`; `cses:<id>`; `orig:<name>` |
| `ada-deck` | map item-id → `{n, at}` | the My mistakes deck |
| `ada-mock`, `ada-mock3` | mock state, including a running clock | |
| `ada-endsem-date` | date string | |
| `ada-quick`, `ada-theme2` | preferences | per device |
| `ada-cf-ticks`, `ada-todo-newton-v2` | legacy | the first is migrated; the second is dead |

**Compatibility rule:** never rename these keys or change their shapes without a migration; they hold the user's progress.

### 5.5 Technical constraints

- No server and no network calls other than the font stylesheet.
- Dark and light themes via CSS variables; layout is responsive down to a phone; reduced-motion is respected.
- Code samples target Python 3.8+ except where marked: `bit_count` and `pairwise` need 3.10, and `bisect` with `key=` needs 3.10.

---

## 6. Provenance and verification policy

**Code.** Every code block on the new pages lives in `snips.py` and is tested against an independent brute force on random inputs (64 blocks tested at the time of writing). The six Vault problems' solutions are tested against their brute forces; Chakravyuh Reversed against every possible graph for n ≤ 5; Frozen Middle against every permutation for n ≤ 6 with every k (and n ≤ 7 in a separate check).

**Ratings.**
- Codeforces ratings in the Ladder were each read from a Codeforces problem list during this project. Note for anyone parsing those lists: a problem's **rating appears after its tags**, not before its name. One such parse error was caught (New Year and Rating is 1600; its neighbour is 1900).
- LeetCode ratings are the community ratings carried over from the original ladder. New LeetCode classics and all CSES tasks carry **estimates**, shown with ≈.
- The Codeforces public API (`problemset.problems`, `user.status`) exists and is the right way to automate verification; the build sandbox couldn't reach it.

**Not verified.**
- About 128 LeetCode and 54 CSES links were typed from memory and have not been opened.
- About 20 Codeforces hints were written from knowledge of the standard solutions, not read from editorials this session.
- The Contest-1/Contest-2/mid-sem "late" labels rely on the badge inference in section 2.

**An earlier mistake, recorded so it isn't repeated.** A previous version, `ADA_Exam_Notebook_EndSem.html`, claimed "every rating checked on Codeforces" while several ratings were from memory. It is superseded and should not be used.

---

## 7. Known issues

1. The Exam-prep stops are numbered 11–18, which collides with the new stops 11–14 in the sidebar.
2. The hero route map shows dots only for stops 0–10.
3. Quick-review mode was not re-tuned for the new stops.
4. Two labs deliberately show a red "wrong answer" caption (the max-heap checker and the coin-greedy counterexample). They are teaching examples, not failures.
5. Fonts depend on Google Fonts; offline it falls back to system fonts.
6. Progress is per browser until the roadmap's sync phase.

---

## 8. Glossary

- **Stop / half stop:** a topic / a short bridge to the next topic (numbers like 4.5).
- **Lab:** an interactive widget inside a stop.
- **Pattern:** a recurring problem shape with a standard tool (for example, "node is a state").
- **Subtask:** a smaller version of a contest problem (for example, n ≤ 10³) scored separately.
- **Ladder / tier / Vault / Ego:** see section 4.
- **CF, LC, CSES:** Codeforces; LeetCode; the CSES Problem Set. **Newton:** the platform where the course contests run.
- **≈CF:** an estimated Codeforces-equivalent rating.
- **Functional graph:** a directed graph where every node has at most one outgoing edge (Chakravyuh's family).

---

## 9. Rules for anyone editing this project

1. **Edit the sources, then rebuild.** Don't hand-edit `dist/index.html`.
2. **Every new code sample goes into `snips.py` with a test** against a brute force before it appears on a page.
3. **Every Codeforces rating must be read from Codeforces** (or the API). Anything else is an estimate and must show ≈.
4. **Keep storage keys and shapes stable.**
5. **Don't copy problem statements** from Newton, Codeforces, LeetCode or CSES. Link to them; write originals for the Vault.
6. **Say what was and wasn't verified** when you deliver.
7. **Stay inside the course's topic areas**, and keep the pyramid shape: more at the base than at the top.
8. **Respect the preferences in section 3.**
