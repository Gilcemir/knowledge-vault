# Working Notes — Graphs

## User preferences (carried over from the heap track)
- Conversation in **Portuguese (BR)**; all materials (lessons, reference, records) in **English**.
- **NEVER give solutions** to the 13 roadmap problems. Escalating hints on request: (1) restate/reframe, (2) point to the pattern, (3) suggest the structure shape, (4) discuss a subproblem — never full code.
- Python only, `python3.14` in all run lines; type hints everywhere. ~30 min per session → one lesson OR one problem per session.
- Gil learns best by **tracing on paper**; every new loop/pattern gets a full state-table trace on a small input. Lessons state the concrete problem FIRST — abstractions enter only as the fix to a failure he just watched (L5 post-mortem rule, heap track).
- Premium problems: solved on neetcode.io's free judge (his choice, 2026-08-14).

## Baseline (2026-08-14)
- Graphs proper: **near zero by his own report** — has never written BFS or DFS on a graph with cycles, never built an adjacency list, no contact with topological sort or union-find.
- Strong adjacent ground: Trees (roadmap ✅), Backtracking (roadmap ✅ via LeetCode's official tutorial — NOT this teach flow), Heap track closed 2026-08-14 with capstone 17/17.
- **Watch item inherited from heap track**: never volunteers per-phase complexity unasked. Demand it at every hand-in, empty table skeleton pasted, boring phases by name.

## Track plan (adaptive — reorder/merge freely)

Problem order follows NeetCode's Graphs list (verified 2026-08-14 vs the NeetCode 150 list: 12 Medium + 1 Hard).

| # | Session | Type | Status |
|---|---------|------|--------|
| D0 | Backtracking cold diagnostic (`lessons/0001-backtracking-diagnostic.py`) — the agreed insurance before building on DFS | drill | 🔵 delivered 2026-08-14 |
| L1 | Graph anatomy: edge list → adjacency list; the grid as an implicit graph; matrix vs list cost | lesson + drill | planned (branch: if D0 red, a targeted backtracking patch slots in first) |
| L2 | DFS on a graph WITH cycles: visited, components, flood fill | lesson + drill | planned |
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
- **2026-08-14 — workspace opened.** Mission written (inherits the roadmap parent mission), resources verified (Erickson ch. 2/5/6, MIT 6.006 L9/L10, CP-Algorithms DSU, graphlib, VisuAlgo), assets copied from heap track (course.css, quiz.js). D0 backtracking diagnostic delivered — closed-book, first-pass result to be reported verbatim (the heap capstone's first-pass reds went unrecorded; don't repeat that). Branch rule: any red K-cell in D0 → one targeted patch lesson before L1; all green → straight to L1.
