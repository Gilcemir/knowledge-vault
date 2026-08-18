# D0 diagnostic: backtracking mechanics green, recursion-tree counting red

First pass on the D0 cold diagnostic (2026-08-17, closed-book, honest reds): **5/9**. The four reds — P1, P2, K1, K7 — share one root cause: Gil cannot yet *see* the recursion tree. He predicted 3 leaves for the subsets tree on 2 items (it has 4; a full binary decision tree always has a power-of-2 leaf count), answered `n^2` for leaf count and `O(n^2)` for total subsets cost (missing the leaves × per-leaf-copy multiplication).

The five greens matter just as much: K3 (what `pop` restores), K4 (why `copy` at the leaf), K5 (when a prune is legal), K6 (used flag released on backtrack), K2 (n! permutation leaves). The choose/explore/unchoose *mechanics* stuck from the Backtracking node — even P2's wrong answer contained the right deep insight (all appends alias one list that ends empty); only the leaf *count* was wrong.

## Evidence

Verbatim harness output: `5 passed, 4 failed, 0 not attempted` — FAIL on "P1 — subsets, traced" (predicted `[[1, 2], [1, 2], [1, 2]]`), "P2 — the missing copy, traced" (predicted `[[], [], []]`), "K1 — subsets tree: leaves" (`n^2`), "K7 — total subsets cost" (`O(n^2)`).

## Closure (2026-08-17, same day)

After the patch lesson (`0002-recursion-tree-patch.html`) he corrected all four red cells from his own paper trace and re-ran D0 to **9/9**. He also re-derived the take/skip template in his own words after learning subsets via the for-loop template — evidence the correction is conceptual, not memorized. The watch item below stays active regardless: one green re-run is fluency, not storage.

## Implications

- Per the D0 branch rule: ONE targeted patch lesson (`lessons/0002-recursion-tree-patch.html`) on drawing/counting the recursion tree and its total cost — then straight to L1. No redo of the Backtracking node.
- **Watch item**: tree-size and cost-by-multiplication reasoning is fragile. Re-probe leaf/node counting cold at L2 (DFS visits × edge cost) and at the capstone.
- Do not re-teach undo/copy/prune/used-flag mechanics — they are load-bearing.
