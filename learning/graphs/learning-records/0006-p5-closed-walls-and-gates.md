# P5 closed — multi-source BFS assembled unaided; the total-count watch item is retired

P5 (Walls and Gates / Islands and Treasures, LC 286 on neetcode.io) accepted first hand-in (2026-09-01), taken out of order (neetcode's list order) with P4 still owed. The assembly was entirely his: collect all sources, seed `seen` AND the queue with them, snapshot layer loop, write `d` on pop. Leave-the-last-step is vindicated — the lesson stopped one step short and he built the rest.

## Evidence

Accepted on the neetcode.io judge (no file in repo, per standing rule). Cost table: time column right unaided (scan O(m·n), BFS O(m·n) via "each cell enqueued at most once × 4 checks"). Total append count produced by counting: m·n, "seen evita que seja mais que isso" — the production form of the 1+2E watch item from [[0004-l3-p3-closed-clone-graph]], finally out of his own mouth. **Retire the total-count watch item** (recognition passed at L4 K2/K3, production passed here).

## Implications

- **Retire mark-the-seed** ([[0005-l4-closed-bfs-drill]]): produced in production, multi-source, unaided — `set(treasures)` + `deque(treasures)` on the first try.
- **Space row still scaffold-dependent.** Volunteered nothing; with the name-the-consumers scaffold he justified `treasures` (all-zeros grid) and the O(m·n) total, but `seen`/`queue` worst cases were completed by the teacher. Keep pasting the empty space column at every hand-in.
- **Recursion-stack-gone probe: passed on the second nudge.** First answer reached for surface differences (in-place output; "no adjacency needed" — wrong differentiator, P1/P2 grids were implicit too). Got the call stack once pointed at "what Python allocates per nested call". The stack→queue trade (LIFO→FIFO = depth-order→distance-order) was then named by the teacher. Half-credit: re-probe cold at capstone (L9).
- **New micro-lesson, worth remembering: sentinel-vs-data.** He tried `grid[u] != float('inf')` and couldn't see why it failed — the problem's "INF" is the int 2147483647, and `2147483647 == float('inf')` is False. The habit to build: check what value is actually IN the data before comparing against what the name suggests. Low-grade; nudge if it recurs.
- P4 (Rotting Oranges, LC 994) is now the open problem — same pieces plus the accounting question the lesson deliberately never named. Expect the assembly to be fast; the probe-worthy part is the final answer's edge cases.
