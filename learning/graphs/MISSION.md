# Mission: Graphs (NeetCode roadmap track)

## Why
Gil is working through the NeetCode DSA roadmap (goal: finish every remaining node by end of 2026) and reached the Graphs node — the largest remaining node and the highest-yield interview topic. Same parent mission as the heap track: durable CS fundamentals plus readiness for a future interview cycle. Graphs also unlocks the Advanced Graphs node, the only real dependency chain left on his map.

## Success looks like
- Can build a graph representation (adjacency list from an edge list; a grid treated as an implicit graph) without hesitation, and say when a matrix would be the wrong call.
- Can write BFS (queue + visited) and DFS (recursion or stack + visited) on a graph **with cycles**, cold — knowing exactly why `visited` exists and where it is marked.
- Can implement topological sort (cycle detection in a directed graph included) and a basic union-find (path compression + union by size) from scratch.
- Solves all 13 NeetCode Graphs problems **independently** (hints allowed, solutions never), recognizing the pattern (grid flood, multi-source BFS, boundary-inward thinking, topo sort, DSU) on sight.

## Constraints
- ~30 min per study session, daily-ish → small lessons; one concept or one problem per session.
- Python only, targeting 3.14; type hints everywhere.
- Conversation in Portuguese; all written materials in English.
- **Never give the answer/solution to the 13 roadmap problems.** Hints only when asked, escalating gradually.
- LeetCode-premium problems in the node (e.g. Walls and Gates) are solved on neetcode.io's free judge instead.
- Year-end deadline pressure: prefer lean lessons over exhaustive ones; cut scope before cutting problems.

## Out of scope
- The Advanced Graphs node (Dijkstra, MST, Bellman-Ford, A*, Eulerian paths) — its own workspace later.
- Strongly connected components / bridges / articulation points — mention only if a problem brushes against them.
- Redoing the Backtracking node. One cold diagnostic in session 1 (agreed 2026-08-14); red cells get a single targeted lesson, never a track.
