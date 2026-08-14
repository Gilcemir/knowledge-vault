# Graphs Resources

## Knowledge

- [Book: Jeff Erickson, _Algorithms_ — Chapter 5: Basic Graph Algorithms](https://jeffe.cs.illinois.edu/teaching/algorithms/book/05-graphs.pdf)
  Free and complete (38 pp.). Representations (adjacency list/matrix), reachability, whatever-first search as the unifying frame for BFS/DFS. Use for: grounding any claim about representations and traversal cost. Verified 2026-08-14 (chapter listing on the book page).
- [Book: Jeff Erickson, _Algorithms_ — Chapter 6: Depth-First Search](https://jeffe.cs.illinois.edu/teaching/algorithms/book/06-dfs.pdf)
  32 pp. DFS in directed graphs, preorder/postorder, topological sort. Use for: the "why" behind topo sort and cycle detection. Verified 2026-08-14 (opened pp. 225–226).
- [Book: Jeff Erickson, _Algorithms_ — Chapter 2: Backtracking](https://jeffe.cs.illinois.edu/teaching/algorithms/book/02-backtracking.pdf)
  Primary source for the session-1 cold diagnostic and any patch lesson it triggers. Use for: the recursion-tree cost argument and the choose/explore/unchoose frame.
- [Lecture: MIT 6.006 (Spring 2020) — Lecture 9: Breadth-First Search](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-9-breadth-first-search/)
  Graph definitions, adjacency, representations, shortest-path trees, BFS. Use for: rigorous grounding of BFS layers = distance. Verified 2026-08-14.
- [Lecture: MIT 6.006 (Spring 2020) — Lecture 10: Depth-First Search](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-10-depth-first-search/)
  DFS, full-DFS/full-BFS, topological sort, cycle detection. Use for: the same lecture series the heap track leaned on. Verified 2026-08-14.
- [Article: CP-Algorithms — Disjoint Set Union](https://cp-algorithms.com/data_structures/disjoint_set_union.html)
  DSU with path compression and union by size/rank, O(α(n)) amortized, with implementations. Use for: the union-find lessons (Redundant Connection, Connected Components). Verified 2026-08-14.
- [Docs: `graphlib` — Python official docs](https://docs.python.org/3/library/graphlib.html)
  Stdlib `TopologicalSorter` (3.9+). Use for: the "the stdlib already ships this" moment after topo sort is earned by hand — same role `heapq`'s source played in the heap track.
- [Docs: `collections.deque` — Python official docs](https://docs.python.org/3/library/collections.html#collections.deque)
  O(1) `popleft` — the BFS queue. Use for: why `list.pop(0)` is the wrong queue.
- [Tool: VisuAlgo — Graph Traversal (DFS/BFS)](https://visualgo.net/en/dfsbfs)
  Animated DFS/BFS plus topological sort (both DFS-based and Kahn's). Use for: watching a traversal before hand-tracing one. Verified 2026-08-14.
- [Videos: NeetCode YouTube channel](https://www.youtube.com/@NeetCode)
  Per-problem walkthroughs for all 13 roadmap problems. **Use only AFTER an honest solo attempt** — full solutions; watching early violates the mission.

## Wisdom (Communities)

- [r/leetcode](https://www.reddit.com/r/leetcode/)
  Pattern discussions and calibration. Use for: comparing approaches after solving.
- [LeetCode problem discussion tabs](https://leetcode.com/problemset/)
  Post-solve comparison: idiomatic Python solutions, complexity debates. Same embargo as the videos.
- [NeetCode Discord](https://discord.gg/ddjKRXPqtk)
  The roadmap's own community. Use for: problem variants and sequencing questions.

## Gaps

- No verified visualizer for **union-find** yet (VisuAlgo has `/ufds`, unverified) — check before the DSU lesson.
- Multi-source BFS (Rotting Oranges, Walls and Gates) rarely gets standalone high-trust treatment without spoiling those exact problems — the lesson will need first-principles construction, like the heap track's two-heaps lesson.
