"""
L1 drill — Graph anatomy: build the map, walk the grid.

HOW TO USE
    1. Read lesson 0003 (graph anatomy) first.
    2. Implement the two functions below and fill every KNOWLEDGE cell
       with one of its allowed answers, spelled exactly as listed.
    3. Run, from the repo root:
           python3.14 learning/graphs/lessons/0004-graph-anatomy-drill.py
    4. Report the output to your teacher — reds included.

There are no solutions in this file.
"""


# ----------------------------------------------------------------------------
# PART F — two functions
# ----------------------------------------------------------------------------

def build_adj(n: int, edges: list[list[int]], directed: bool) -> dict[int, list[int]]:
    """Build an adjacency list for a graph with vertices 0 .. n-1.

    Rules:
      - EVERY vertex 0 .. n-1 must appear as a key — even a vertex
        with no edges at all.
      - If directed is False, an edge [u, v] must show up in BOTH
        adj[u] and adj[v]. If True, only in adj[u].
      - Neighbor order inside each list does not matter.
    """
    adj: dict[int, list[int]] = {v:[] for v in range(n)}
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)

    return adj


def grid_neighbors(grid: list[list[str]], r: int, c: int) -> list[tuple[int, int]]:
    """Return the 4-directional IN-BOUNDS neighbors of cell (r, c).

    Rules:
      - Up, down, left, right only — no diagonals.
      - Only coordinates that actually exist in the grid.
      - The grid may be non-square (rows != cols).
      - Order does not matter; no duplicates.
    """

    neighbours = []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            neighbours.append((nr, nc))

    return neighbours


# ----------------------------------------------------------------------------
# PART K — six knowledge cells
# ----------------------------------------------------------------------------
#
# K1 "list_space" — total memory of an adjacency LIST for a graph with
#     V vertices and E edges. One of (exactly):
#     "O(V)"   "O(E)"   "O(V + E)"   "O(V^2)"
#
# K2 "matrix_space" — total memory of an adjacency MATRIX. Same options.
#
# K3 "matrix_edge_check" — cost of answering "is (u, v) an edge?" with a
#     MATRIX. One of (exactly):
#     "O(1)"   "O(deg(u))"   "O(V)"   "O(V^2)"
#
# K4 "list_edge_check" — cost of the same question with a LIST.
#     Same four options as K3.
#
# K5 "matrix_iterate" — cost of visiting all neighbors of u with a
#     MATRIX. Same four options as K3.
#
# K6 "matrix_wrong_call" — the matrix is the WRONG representation
#     when... One of (exactly):
#     "the graph is sparse: E is far below V^2"
#     "the graph is directed, so the matrix is asymmetric"
#     "the graph has cycles, so lookups repeat forever"
#     "the graph is weighted, so cells cannot hold booleans"

KNOWLEDGE: dict[str, str | None] = {
    "list_space": "O(V + E)",
    "matrix_space": "O(V^2)",
    "matrix_edge_check": "O(1)",
    "list_edge_check": "O(deg(u))",
    "matrix_iterate": "O(V)",
    "matrix_wrong_call": "the graph is sparse: E is far below V^2",
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

_SPACE = {"O(V)", "O(E)", "O(V + E)", "O(V^2)"}
_TIME = {"O(1)", "O(deg(u))", "O(V)", "O(V^2)"}
_WRONG = {
    "the graph is sparse: E is far below V^2",
    "the graph is directed, so the matrix is asymmetric",
    "the graph has cycles, so lookups repeat forever",
    "the graph is weighted, so cells cannot hold booleans",
}

_K_ALLOWED = {
    "list_space": _SPACE, "matrix_space": _SPACE,
    "matrix_edge_check": _TIME, "list_edge_check": _TIME,
    "matrix_iterate": _TIME, "matrix_wrong_call": _WRONG,
}

_K_ANSWERS = {
    "list_space": "O(V + E)",
    "matrix_space": "O(V^2)",
    "matrix_edge_check": "O(1)",
    "list_edge_check": "O(deg(u))",
    "matrix_iterate": "O(V)",
    "matrix_wrong_call": "the graph is sparse: E is far below V^2",
}

_K_HINTS = {
    "list_space": (
        "One dict slot per vertex, plus one list entry per edge "
        "endpoint stored. Add the two."
    ),
    "matrix_space": (
        "A full V-by-V table exists whether or not the edges do."
    ),
    "matrix_edge_check": (
        "It is a single cell lookup: matrix[u][v]."
    ),
    "list_edge_check": (
        "You must scan u's neighbor list; how long can it be?"
    ),
    "matrix_iterate": (
        "You must walk u's ENTIRE row — zeros included — even if u "
        "has one neighbor."
    ),
    "matrix_wrong_call": (
        "The matrix pays O(V^2) memory and O(V) per neighbor scan no "
        "matter how few edges exist. When does that overhead dwarf "
        "the real data?"
    ),
}

_K_LABELS = {
    "list_space": "K1 — adjacency list: space",
    "matrix_space": "K2 — adjacency matrix: space",
    "matrix_edge_check": "K3 — matrix: is (u,v) an edge?",
    "list_edge_check": "K4 — list: is (u,v) an edge?",
    "matrix_iterate": "K5 — matrix: visit u's neighbors",
    "matrix_wrong_call": "K6 — when the matrix is the wrong call",
}


def _assert_adj_shape(got: object) -> dict[int, list[int]]:
    assert isinstance(got, dict), (
        f"{got!r} is a {type(got).__name__}, not a dict — build_adj must "
        "return a dict mapping vertex -> neighbor list"
    )
    for k, v in got.items():
        assert isinstance(v, list), (
            f"adj[{k!r}] is {v!r} ({type(v).__name__}), not a list"
        )
    return got


def _test_adj_all_vertices_present() -> None:
    got = _assert_adj_shape(build_adj(4, [[0, 1]], directed=False))
    assert set(got.keys()) == {0, 1, 2, 3}, (
        f"keys are {sorted(got.keys())!r}, expected [0, 1, 2, 3] — "
        "vertices 2 and 3 have no edges but still exist. Hint: create "
        "every key BEFORE walking the edge list."
    )
    assert got[2] == [] and got[3] == [], (
        f"adj[2]={got[2]!r}, adj[3]={got[3]!r} — isolated vertices must "
        "map to an empty list"
    )


def _test_adj_undirected_both_ways() -> None:
    got = _assert_adj_shape(build_adj(3, [[0, 1], [1, 2]], directed=False))
    assert sorted(got[1]) == [0, 2], (
        f"adj[1] is {got[1]!r}, expected [0, 2] in some order — an "
        "undirected edge [u, v] must be stored in BOTH directions"
    )
    assert got[0] == [1] and got[2] == [1], (
        f"adj[0]={got[0]!r}, adj[2]={got[2]!r}, expected [1] and [1]"
    )


def _test_adj_directed_one_way() -> None:
    got = _assert_adj_shape(build_adj(3, [[0, 1], [1, 2]], directed=True))
    assert got[0] == [1] and got[1] == [2], (
        f"adj[0]={got[0]!r}, adj[1]={got[1]!r}, expected [1] and [2]"
    )
    assert got[2] == [], (
        f"adj[2] is {got[2]!r}, expected [] — directed means [1, 2] "
        "creates NO reverse entry 2 -> 1"
    )


def _test_adj_empty_graph() -> None:
    got = _assert_adj_shape(build_adj(1, [], directed=False))
    assert got == {0: []}, f"got {got!r}, expected {{0: []}}"


_GRID_2X3: list[list[str]] = [
    [".", ".", "."],
    [".", ".", "."],
]


def _assert_nbr_shape(got: object) -> list[tuple[int, int]]:
    assert isinstance(got, list), (
        f"{got!r} is a {type(got).__name__}, not a list"
    )
    for item in got:
        assert isinstance(item, tuple), (
            f"{item!r} is a {type(item).__name__}, not a tuple — return "
            "coordinates as (row, col) tuples"
        )
    assert len(got) == len(set(got)), f"{got!r} contains duplicates"
    return got


def _test_grid_middle() -> None:
    got = _assert_nbr_shape(grid_neighbors(_GRID_2X3, 0, 1))
    want = {(0, 0), (0, 2), (1, 1)}
    assert set(got) == want, (
        f"neighbors of (0, 1) in a 2x3 grid: got {sorted(got)!r}, "
        f"expected {sorted(want)!r} — up/down/left/right only, and "
        "(−1, 1) is out of bounds"
    )


def _test_grid_corner() -> None:
    got = _assert_nbr_shape(grid_neighbors(_GRID_2X3, 0, 0))
    want = {(0, 1), (1, 0)}
    assert set(got) == want, (
        f"neighbors of the (0, 0) corner: got {sorted(got)!r}, expected "
        f"{sorted(want)!r}. Hint: in Python, grid[-1] does NOT raise — "
        "it wraps around. Negative coordinates must be rejected "
        "explicitly."
    )


def _test_grid_nonsquare_bounds() -> None:
    got = _assert_nbr_shape(grid_neighbors(_GRID_2X3, 1, 2))
    want = {(0, 2), (1, 1)}
    assert set(got) == want, (
        f"neighbors of (1, 2) in a 2x3 grid (2 rows, 3 cols): got "
        f"{sorted(got)!r}, expected {sorted(want)!r}. Hint: rows are "
        "bounded by len(grid), cols by len(grid[0]) — a non-square "
        "grid punishes swapping them."
    )


def _check(name: str, fn) -> bool | None:
    try:
        fn()
    except NotImplementedError:
        print(f"  ..  {name} — not attempted yet")
        return None
    except AssertionError as e:
        print(f"  FAIL  {name}: {e}")
        return False
    except Exception as e:
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")
        return False
    print(f"  ok    {name}")
    return True


def _make_knowledge_test(key: str):
    def test() -> None:
        got = KNOWLEDGE.get(key)
        if got is None:
            raise NotImplementedError
        assert isinstance(got, str), (
            f"{got!r} is not a string — answer with one of the listed options"
        )
        assert got in _K_ALLOWED[key], (
            f"{got!r} is not one of the allowed answers for this cell — "
            "copy the option exactly as spelled in the comment"
        )
        assert got == _K_ANSWERS[key], f"you said {got!r}. Hint: {_K_HINTS[key]}"
    return test


TESTS = [
    ("F1 — adjacency: every vertex present", _test_adj_all_vertices_present),
    ("F2 — adjacency: undirected goes both ways", _test_adj_undirected_both_ways),
    ("F3 — adjacency: directed goes one way", _test_adj_directed_one_way),
    ("F4 — adjacency: empty graph", _test_adj_empty_graph),
    ("F5 — grid: middle cell", _test_grid_middle),
    ("F6 — grid: corner (negative wrap trap)", _test_grid_corner),
    ("F7 — grid: non-square bounds", _test_grid_nonsquare_bounds),
] + [(_K_LABELS[key], _make_knowledge_test(key)) for key in _K_ANSWERS]

if __name__ == "__main__":
    print("\ngraph anatomy drill — L1\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green — you can build the map. Tell your teacher:")
        print("L2 (DFS on a graph with cycles) is next.\n")
    else:
        print("\nReport this output to your teacher, reds included.\n")
