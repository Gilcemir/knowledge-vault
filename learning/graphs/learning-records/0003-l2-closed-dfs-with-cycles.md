# L2 closed 13/13 — visited-set DFS and flood fill are genuine; watch the vertex/edge vocabulary in code

L2 (DFS with cycles) drill passed 13/13 on the first reported run (2026-08-19). Both functions are structurally correct and idiomatic in the ways that matter: mark-on-entry in both DFSes, guard before recursing, bounds check rejects negatives explicitly, isolated start handled. All six K-cells green, including K1 (O(V + E) — the D0 watch item "counts by guess, not structure" was probed and passed) and K5 (each undirected edge examined exactly twice).

**The L1 misconception is verifiably gone.** LR-0002 predicted he would fuse the flood-fill guard's three questions (exists? / new? / allowed?); he did not. His `region` compares the neighbor's value against the stored start label (`grid[nr][nc] == t`) — an explicit label match, no truthiness filter. The vertex-label vs edge-flag correction held cold, one day later, closed-book.

## Evidence

Verbatim harness output: `13 passed, 0 failed, 0 not attempted`. Reference: `lessons/0006-dfs-drill.py` as submitted.

## Implications

- Cycle-safe DFS (list and grid) is now a floor. P1 (Number of Islands, LC 200) is unlocked — his first roadmap problem in this track. At hand-in: demand the empty per-phase cost table (standing watch item — never volunteers complexity).
- New low-grade watch item, vocabulary in code: he wrote `{edge: [] for edge in range(n)}` — the loop variable iterates **vertices** but is named `edge`. Given the vocabulary-zero baseline (2026-08-17), check whether it was a typo or a real conflation before letting it pass. Also partial drift from the L1 naming convention: kept `nr/nc` but used `i, j` for the direction deltas (not `dr, dc`) and `x, y` for grid dimensions (not `rows, cols` / `R, C`). Convention nudges land in one pass for him — one mention should suffice; don't drill it.
