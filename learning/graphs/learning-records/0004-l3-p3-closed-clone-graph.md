# L3+P3 closed — old→new map is genuine; cost counting needs the "how many calls total" reflex; type hints wider than reality

P3 (Clone Graph, LC 133) accepted on LeetCode, first hand-in (2026-08-25). Code clean: guard-inside-clone, register-before-wiring, memo-check first, no stdlib shadowing, naming fine (`nd`, `cp`, `ngb`, `old_to_new`). Both P2 watch items (re-shadowing, `x, y` dims) passed — retire them.

**Register-before-wiring is understood, not copied.** Gil self-reported the solve as "basically copying L3", so the probe mattered: asked what breaks if `old_to_new[nd] = cp` moves after the neighbor loop, he correctly identified the mechanism unaided — an in-progress node is absent from the memo, so the cycle re-enters it and recursion never bottoms out. Only the outcome name was imprecise ("enters a loop" instead of `RecursionError`); supplied, with the connection that late registration ≡ the naive clone from L3.

## Evidence

Accepted LC submission pasted in-session (no file in repo, per standing rule). Probe Q1 answered with the correct causal chain. Cost table: per-call O(1) rows right; "V constructions, one per vertex" right.

## Implications

- **Watch item (cost): never produced the total-call count.** Asked twice how many times `clone` is called in total (1 + 2E — each undirected edge appears in two neighbor lists), he answered per-call costs and the V-constructions count but never the 2E. This is the L2 K5 fact ("each edge examined twice") not yet transferred to counting *calls*. Re-probe at L4 (BFS queue pushes) and at the capstone.
- **Watch item (space): partial regression.** At P2 the space row was unprompted and correct (recursion stack). Here, prompted for three consumers, he named only the cloned nodes (and undersized them: the clone's neighbor lists hold 2E references → O(V+E), not O(V)); missed `old_to_new` (O(V)) and the recursion stack (O(V) worst case, line graph). Keep demanding the space row; name-the-consumers is the scaffold that works.
- **New low-grade watch item: type hints wider than reality.** `dict[Optional['Node'], Optional['Node']]` when no None can ever enter the dict (the guard returns before any dict access; values are always fresh `Node`s). Answered "não sei" when asked — the gap is real, not a slip: he doesn't yet read a hint as a provable claim about what flows. Nudge when it recurs; don't drill.
- **Teaching-design lesson (his feedback, now a standing rule in NOTES.md): leave the last step.** L3 traced the complete Clone Graph algorithm, so P3 had no productive struggle. From L4 on, lessons stop one assembly step short of the target problem. Applies doubly to L8 → Word Ladder.
- L4 (BFS: layers = distance, multi-source seeding) is next, with a drill.
