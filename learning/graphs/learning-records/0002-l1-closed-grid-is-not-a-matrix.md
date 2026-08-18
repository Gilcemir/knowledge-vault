# L1 closed 13/13 — but the grid was mistaken for an adjacency matrix

L1 (graph anatomy) drill passed 13/13 first run (2026-08-18), both parts genuine: adjacency-list build handled isolated vertices and the directed/undirected split cleanly, and all six K-cells (space/time trade-offs, sparse-graph judgement) were correct. Representation-building is now a floor, not a target.

One misconception surfaced and was corrected in review: his `grid_neighbors` filtered neighbors by cell **truthiness** (`and grid[nr][nc]`), because he assumed a grid works like the adjacency matrix from the lesson — cell value as an edge flag ("only add if the relation exists"). Corrected framing, in his own words accepted: **in a grid each cell is a vertex and its value is a vertex label; edges are implicit in adjacency.** The anatomy layer answers "which neighbors exist" (bounds only); the traversal layer decides "where may I step" (reading labels).

## Evidence

Verbatim harness output: `13 passed, 0 failed, 0 not attempted`, twice — original version and after he applied the review fixes himself (idiomatic `dr, dc` / `nr, nc` naming, truthiness filter removed). His stated reason for the filter confirmed the matrix analogy was the source, not carelessness.

## Implications

- L2 (DFS with cycles / flood fill) must make the vertex-label vs edge-flag distinction explicit: the flood-fill condition is three separate questions — exists? (bounds), new? (visited), allowed? (label match) — and he has already shown he will fuse them.
- He self-corrected naming to the `dr/dc`, `nr/nc` convention after one explanation — convention nudges land in one pass; don't over-drill them.
