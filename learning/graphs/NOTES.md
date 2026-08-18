# Working Notes — Graphs

## User preferences (carried over from the heap track)
- Conversation in **Portuguese (BR)**; all materials (lessons, reference, records) in **English**.
- **NEVER give solutions** to the 13 roadmap problems. Escalating hints on request: (1) restate/reframe, (2) point to the pattern, (3) suggest the structure shape, (4) discuss a subproblem — never full code.
- Python only, `python3.14` in all run lines; type hints everywhere. ~30 min per session → one lesson OR one problem per session.
- Gil learns best by **tracing on paper**; every new loop/pattern gets a full state-table trace on a small input. Lessons state the concrete problem FIRST — abstractions enter only as the fix to a failure he just watched (L5 post-mortem rule, heap track).
- Premium problems: solved on neetcode.io's free judge (his choice, 2026-08-14).
- **Vocabulary is truly zero on graphs** (2026-08-17, his own report after the L1 cold open failed): 12-year-old college theory did NOT survive. Every lesson must define its new nouns (vertex, edge, neighbor, degree, directed/undirected, traversal, ...) at first use, anchored to a concrete picture — before any code snippet, quiz, or Big-O expression that uses them. Never lean on the reference glossary or assumed recall for a first encounter.

## Baseline (2026-08-14)
- Graphs proper: **near zero by his own report** — has never written BFS or DFS on a graph with cycles, never built an adjacency list, no contact with topological sort or union-find.
- Strong adjacent ground: Trees (roadmap ✅), Backtracking (roadmap ✅ via LeetCode's official tutorial — NOT this teach flow), Heap track closed 2026-08-14 with capstone 17/17.
- **Watch item inherited from heap track**: never volunteers per-phase complexity unasked. Demand it at every hand-in, empty table skeleton pasted, boring phases by name.

## Track plan (adaptive — reorder/merge freely)

Problem order follows NeetCode's Graphs list (verified 2026-08-14 vs the NeetCode 150 list: 12 Medium + 1 Hard).

| # | Session | Type | Status |
|---|---------|------|--------|
| D0 | Backtracking cold diagnostic (`lessons/0001-backtracking-diagnostic.py`) — the agreed insurance before building on DFS | drill | ✅ first pass 5/9 → 9/9 after patch (2026-08-17, LR-0001) |
| P0 | Patch: recursion-tree size & cost (`lessons/0002-recursion-tree-patch.html`) — leaves = 2^n, cost = leaves × per-leaf work | patch lesson | ✅ closed 2026-08-17 — D0 re-ran 9/9 same day |
| L1 | Graph anatomy: edge list → adjacency list; the grid as an implicit graph; matrix vs list cost | lesson + drill | ✅ closed 2026-08-18 — drill 13/13 (LR-0002) |
| L2 | DFS on a graph WITH cycles: visited, components, flood fill | lesson + drill | 🔵 delivered 2026-08-18 (`0005-dfs-with-cycles.html` + `0006-dfs-drill.py`) |
| P1–P2 | Number of Islands (LC 200), Max Area of Island (LC 695) | problems | planned |
| L3 | Graph copies and identity: hashmap old→new (leads to Clone Graph) | lesson | planned |
| P3 | Clone Graph (LC 133) | problem | planned |
| L4 | BFS: layers = distance; multi-source seeding | lesson + drill | planned |
| P4–P5 | Rotting Oranges (LC 994), Walls and Gates (LC 286, on neetcode.io) | problems | planned |
| L5 | Thinking from the boundary inward (reverse flood) | lesson | planned |
| P6–P7 | Pacific Atlantic (LC 417), Surrounded Regions (LC 130) | problems | planned |
| L6 | Topological sort + cycle detection in digraphs | lesson + drill | planned |
| P8–P9 | Course Schedule (LC 207), Course Schedule II (LC 210) | problems | planned |
| L7 | Union-Find from scratch (path compression, union by size) | lesson + drill | planned |
| P10–P12 | Graph Valid Tree (LC 261, neetcode.io), Connected Components (LC 323, neetcode.io), Redundant Connection (LC 684) | problems | planned |
| L8 | Implicit graphs of states (words as nodes) → P13 Word Ladder (LC 127, Hard) | lesson + problem | planned |
| L9 | Capstone: everything, cold | drill | planned |

Deadline note: Gil wants ALL remaining roadmap nodes done by end of 2026 — keep lessons lean, merge sessions when he's fast, and never add scope the 13 problems don't demand.

## Harness & teaching rules inherited from the heap track (apply from day one)
- Validate every drill harness **in the scratchpad** against a reference solution PLUS deliberately wrong variants; every wrong variant must fail a targeted small test with a readable message.
- Assertion messages are teaching surface: always `{got!r}`, assert type before value (the str-of-list trap cost two rounds once).
- Docstring-dedent gotcha (3.13+): cut banned-token docstrings textually, never `src.replace(fn.__doc__, "")` — copy L4's `_source_of`.
- Cost rejection by **op counts**, never wall-clock (3.14 is too fast); SIGALRM `_with_time_limit` helper from heap L5 if a hard stop is needed.
- Quizzes: equal word counts per option, vary `data-answer` position.
- Per-phase cost demand at every problem hand-in: paste the EMPTY table, rows = phases of HIS code, boring phases by name.
- When he says "just give me the answer", give it — Socratic budget spent; re-test cold at the capstone instead.
- Never assume a Python built-in is known (zip was unknown once); when a lesson leans on a stdlib function, state its input/output/mutation contract before reasoning with it.
- Stdlib cost questions: show `inspect.getsource` before prose.

## Session log
- **2026-08-18 — L1 closed 13/13, L2 delivered.** Drill 0004 passed 13/13 first run; review found two issues he then fixed himself: idiomatic `dr/dc`–`nr/nc` naming (one explanation sufficed) and a truthiness filter on grid cells rooted in a real misconception — he treated the grid like an adjacency matrix (cell value as edge flag). Corrected: cell value = vertex LABEL; edges are implicit. LR-0002 written. Also clarified in conversation: sparse-vs-dense with worked examples (flight network vs round-robin tournament); he answered the closing transfer question correctly. L2 delivered: lesson `0005-dfs-with-cycles.html` (naive tree-DFS crashes on the L1 triangle → visited set → mark-on-entry trace → backtracking-template contrast table → O(V + E) counted not guessed (D0 watch item probed again in K1/K5/K6) → components loop → flood fill with the exists/new/allowed three-question split aimed straight at his L1 misconception), drill `0006-dfs-drill.py` (closed-book; harness validated in scratchpad: reference 13/13; 12 wrong variants — no visited, mark-after-loop, directed-only build, list return, label-leak, negative-wrap, diagonals, region-no-visited, wrong/off-menu K cells — each fails its targeted test; RecursionError gets a dedicated teaching message), reference `reference/dfs-traversal.html`. All-green on drill 0006 → P1 (Number of Islands, LC 200) — first roadmap problem; remember the per-phase cost table demand at hand-in.
- **2026-08-17 (feedback) — L1 opening rewritten.** Gil reported the L1 cold open unreadable: the first quiz and the `edges` snippet used vertex/edge/mutual/deg(u)/V/E with zero definitions. Fix shipped in place (`0003-graph-anatomy.html`): lesson now opens with the 5-person network drawn as an SVG, a vocabulary table where every term points at the picture, the edge-list format decoded pair by pair (incl. why vertex 4 is invisible in `edges`), and "traversal" defined before DFS/BFS are name-dropped. Reference glossary expanded (graph, neighbors, undirected/directed, traversal). New standing rule recorded under preferences: define every new noun against a picture before any code/quiz/Big-O uses it. Drill 0004 unchanged — it depends only on the lesson.
- **2026-08-17 (close) — patch closed, L1 delivered.** D0 re-run: **9/9 green**, cells verified genuine (correct tree order, `2^n`, `O(n * 2^n)`). LR-0001 updated with closure. L1 delivered: lesson `0003-graph-anatomy.html`, drill `0004-graph-anatomy-drill.py` (harness validated in scratchpad: reference 13/13 green; 9 wrong variants — missing isolated keys, missing/extra reverse edge, wrong return type, diagonals, no bounds check, swapped r/c bounds, wrong K cell, off-menu K answer — each fails its targeted test), reference sheet `reference/graph-representations.html` started. Drill is closed-book. All-green on drill 0004 → L2 (DFS with cycles).
- **2026-08-17 (follow-up) — misconception source identified.** His Backtracking-node subsets template was the for-loop version (single recursive call, results appended at every node), NOT the take/skip two-call version — the unfamiliar shape explains part of the D0 P1 red. He correctly re-derived take/skip in his own words; one imprecision corrected: believed the two calls advance `i` differently (both call `dfs(i+1)`; only path membership differs). When introducing DFS templates in L2+, expect the same friction whenever a template differs from the one he first memorized — always map new template ↔ known template explicitly. He also flagged difficulty holding recursion trees mentally → reinforced: the tool is paper, not visualization.
- **2026-08-17 — D0 graded, patch delivered.** First pass 5/9, reported honestly with reds visible (good faith — reinforce this habit). Reds P1/P2/K1/K7 share one root cause: never drew the recursion tree (predicted 3 leaves on a power-of-2 tree; missed leaves × copy-cost multiplication). Greens K2–K6: choose/explore/unchoose mechanics are load-bearing — do NOT re-teach. LR-0001 written. Patch lesson `0002-recursion-tree-patch.html` delivered; closes when he fixes the four D0 cells from his own paper trace and re-runs to 9/9, then L1. **New watch item:** counts trees by guess, not by structure — re-probe leaf/cost counting cold at L2 (DFS cost = V × work + E) and at the capstone.
- **2026-08-14 — workspace opened.** Mission written (inherits the roadmap parent mission), resources verified (Erickson ch. 2/5/6, MIT 6.006 L9/L10, CP-Algorithms DSU, graphlib, VisuAlgo), assets copied from heap track (course.css, quiz.js). D0 backtracking diagnostic delivered — closed-book, first-pass result to be reported verbatim (the heap capstone's first-pass reds went unrecorded; don't repeat that). Branch rule: any red K-cell in D0 → one targeted patch lesson before L1; all green → straight to L1.
