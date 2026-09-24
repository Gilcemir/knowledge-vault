# P6+P7 closed — "reverse the question" conflated with "flip the comparison"

Pacific Atlantic (LC 417) and Surrounded Regions (LC 130) both accepted on 2026-09-24. P6 was assembled unaided, with the reversed condition correct. P7 needed NeetCode hints (not the video). His own diagnosis of the P7 block: "fiquei enviesado com o problema passado, tentando inverter alguma coisa". The misconception under it: he took the L5 inversion to mean *flip the inequality*. The inversion that transfers is *flip the question* (start from the target). Flipping the comparison is only a consequence of directed edges. P7's O–O adjacency is symmetric (G^T = G), so the question flips and the edge test stays the same. His P7 code does flip the question: it floods from the border, then the final sweep takes the complement. But he credited the solve to "just marking visited", which every traversal since L2 has done.

## Evidence

- Probe "smallest grid where `>` breaks P6": he gave the right mechanism (equal heights, an edge in both directions, which `>` drops) but did not build the grid. The teacher supplied it: `[[1,1],[1,1]]`, where (0,0) and (1,1) vanish.
- Probe "why no flipped comparison in P7": he answered "o que foi usado para não revisitar foi marcar os visitados". That is the wrong axis: visited-marking prevents revisits, it does not decide direction. The teacher corrected it directly.
- Complexity: he gave totals unasked for the second hand-in running (O(m·n) for both), but refused the per-phase table ("já me tomou muito tempo"). His justification, "lista adicional com cada vértice", holds for P6 (two sets of up to m·n) and is false for P7. There, `borders` is O(m+n), the grid is the visited mark (as in his P4), and O(m·n) comes only from the worst-case queue. This is the same error class as [[0007-p4-closed-rotting-oranges]]: he assumes two solutions share the same space consumers without naming them. Second occurrence.
- Naming: P6 uses `nr, nc` for deltas and `dr, dc` for the new cell, the opposite of P7 written the same day. He said "usei de forma aleatória". This is a regression of the convention fixed at L1 ([[0002-l1-closed-grid-is-not-a-matrix]]).

## Implications

- **L6 (topological sort) is the first fully directed track.** Watch whether "reverse" gets pattern-matched again: reverse postorder and the reversed graph are different reversals. Name the subject of each reversal explicitly.
- **Space-consumer conflation: second occurrence.** Re-probe cold at L9 with two solutions that differ only in their visited structure (seen set vs in-grid mark).
- **He pushed back on hand-in length.** Keep hand-ins to at most 2 asks per problem. The per-phase table is now a request, not a gate, and becomes a gate only when his total is wrong.
- Re-probe at L9: build the `>` counterexample himself; state why an undirected flood needs no flip.
