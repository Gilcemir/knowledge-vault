# L4 closed — BFS mechanics are genuine; knowledge cells right but the code contradicts two of them

Drill 0009 handed in all green, 18/18 (2026-09-01). All three functions loop+queue (no recursion), deque discipline respected, snapshot layer loop used in all three, multi-source seeding in `nearest` correct on the first try (`seen = set(sources)`, all sources enqueued together). All six knowledge cells right — including K2 ("append runs at most V times") and K3 ("2E seen-checks"), the recognition form of the total-call-count watch item from [[0004-l3-p3-closed-clone-graph]].

## Evidence

Teacher re-ran the drill: 18 passed, 0 failed. K-cells verified against the menu.

## Implications

- **Knowledge outruns code — two review findings show K-cells not yet transferred to fingers:**
  1. `bfs_dist` never marks the seed (`seen = set()` but `deque([start])`), so on the triangle vertex 0 re-enters the queue; the answer survives only because of a value-guard (`if v not in distances`) that silently absorbs the double claim. In `nearest` he seeded `seen` correctly — the inconsistency says mark-the-seed isn't automatic yet.
  2. `steps` marks the WRONG vertex: `seen.add(cell)` (the parent being served) instead of `seen.add(new_cell)` (the discovered neighbor) — directly contradicting his own correct K4 answer ("marked the moment v is appended"). Tests pass because the first pop still arrives via a shortest path, but cells can enqueue up to 4×, violating his own K2 on paper. Both handed back as questions; on follow-up he saw the double entry but misgeneralized ("2× per vertex") and never named the saving line, then invoked the give-me-the-answer rule (out of time) — answers and both one-line fixes supplied. **Mark-the-seed is now a watch item**: never produced by him; re-probe cold at P4 (multi-source seeding setup must be his own) and at the capstone.
- **`x, y` for grid dimensions recurred** (`x, y = len(grid), len(grid[0])`) — the item retired at P3 came back in its original habitat, grids. Re-flag; don't retire again until a grid problem comes back clean.
- Production form of the total-count watch item (produce 1+2E / "at most V appends" unprompted) still untested — probe at P4 hand-in per plan, plus the where-did-the-recursion-stack-go space question.
- P4 (Rotting Oranges, LC 994) unlocked once the two fixes re-run green.
