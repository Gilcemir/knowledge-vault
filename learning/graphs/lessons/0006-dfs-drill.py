"""
L2 drill — DFS with cycles: the visited set, reachability, flood fill.

HOW TO USE
    1. Read lesson 0005 (DFS with cycles) first — then CLOSE it.
    2. Implement the two functions below and fill every KNOWLEDGE cell
       with one of its allowed answers, spelled exactly as listed.
    3. Run, from the repo root:
           python3.14 learning/graphs/lessons/0006-dfs-drill.py
    4. Report the output to your teacher — reds included.

There are no solutions in this file.
"""


# ----------------------------------------------------------------------------
# PART F — two functions
# ----------------------------------------------------------------------------

def reachable(n: int, edges: list[list[int]], start: int) -> set[int]:
    """Return every vertex reachable from `start` in an UNDIRECTED graph.

    Vertices are 0 .. n-1; `edges` is an edge list, exactly as in L1.

    Rules:
      - The graph may contain cycles. Your DFS must survive them.
      - `start` is always reachable from itself — it belongs in the result,
        even when it has no edges at all.
      - Undirected: an edge [u, v] can be walked in both directions,
        no matter which order the pair is written in.
      - Return a set of ints.
    """
    raise NotImplementedError


def region(grid: list[list[str]], r: int, c: int) -> set[tuple[int, int]]:
    """Return the flood-fill region of cell (r, c): every cell connected
    to it through 4-directional steps over cells with the SAME value
    as grid[r][c].

    Rules:
      - (r, c) itself always belongs to the region.
      - 4 directions only, no diagonals; the grid may be non-square.
      - Same-value regions can contain cycles (any 2x2 block is one) —
        your flood must survive them.
      - Return a set of (row, col) tuples.
    """
    raise NotImplementedError


# ----------------------------------------------------------------------------
# PART K — six knowledge cells
# ----------------------------------------------------------------------------
#
# K1 "dfs_total_cost" — total cost of DFS with a visited set over an
#     adjacency list (V vertices, E edges). One of (exactly):
#     "O(V)"   "O(E)"   "O(V + E)"   "O(V * E)"
#
# K2 "visited_why" — the visited set exists because... One of (exactly):
#     "cycles would make the recursion revisit forever"
#     "the adjacency dict raises KeyError on repeats"
#     "neighbors would come back in the wrong order"
#     "isolated vertices would never get reached otherwise"
#
# K3 "visited_mark_moment" — when is u marked visited? One of (exactly):
#     "the moment u is entered, before recursing"
#     "after all of u's neighbors are explored"
#     "only when u has an unvisited neighbor"
#     "when the outer component loop selects u"
#
# K4 "visited_unmark" — in reachability DFS, u is REMOVED from visited...
#     One of (exactly):
#     "never: reachability marks are permanent"
#     "on backtrack, like permutation used flags"
#     "once every neighbor of u is visited"
#     "when a second path reaches u later"
#
# K5 "edge_examinations" — in an undirected adjacency-list DFS, one edge
#     u-v is examined (appears in a neighbor loop)... One of (exactly):
#     "exactly once"   "exactly twice"   "deg(u) times"   "up to V times"
#
# K6 "dfs_launches" — the L1 network (n = 5; edges 0-1, 1-2, 2-0, 1-3;
#     vertex 4 alone) is fed to the components loop:
#         for s in range(n):
#             if s not in visited:
#                 dfs(s)
#     How many times does dfs launch? One of (exactly):
#     "1"   "2"   "3"   "5"

KNOWLEDGE: dict[str, str | None] = {
    "dfs_total_cost": None,
    "visited_why": None,
    "visited_mark_moment": None,
    "visited_unmark": None,
    "edge_examinations": None,
    "dfs_launches": None,
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

_K_ALLOWED: dict[str, set[str]] = {
    "dfs_total_cost": {"O(V)", "O(E)", "O(V + E)", "O(V * E)"},
    "visited_why": {
        "cycles would make the recursion revisit forever",
        "the adjacency dict raises KeyError on repeats",
        "neighbors would come back in the wrong order",
        "isolated vertices would never get reached otherwise",
    },
    "visited_mark_moment": {
        "the moment u is entered, before recursing",
        "after all of u's neighbors are explored",
        "only when u has an unvisited neighbor",
        "when the outer component loop selects u",
    },
    "visited_unmark": {
        "never: reachability marks are permanent",
        "on backtrack, like permutation used flags",
        "once every neighbor of u is visited",
        "when a second path reaches u later",
    },
    "edge_examinations": {
        "exactly once", "exactly twice", "deg(u) times", "up to V times",
    },
    "dfs_launches": {"1", "2", "3", "5"},
}

_K_ANSWERS: dict[str, str] = {
    "dfs_total_cost": "O(V + E)",
    "visited_why": "cycles would make the recursion revisit forever",
    "visited_mark_moment": "the moment u is entered, before recursing",
    "visited_unmark": "never: reachability marks are permanent",
    "edge_examinations": "exactly twice",
    "dfs_launches": "2",
}

_K_HINTS: dict[str, str] = {
    "dfs_total_cost": (
        "Count, don't guess: at most V calls (visited caps each vertex "
        "at one) PLUS every adjacency list read once — 2E entries total. "
        "Added, not multiplied."
    ),
    "visited_why": (
        "Replay the paper trace of the triangle 0-1-2-0 without the set: "
        "what do rows 3 and 4 look like?"
    ),
    "visited_mark_moment": (
        "A mark that lands after the neighbor loop arrives too late — "
        "the cycle re-enters u while it is still unmarked."
    ),
    "visited_unmark": (
        "Un-marking is backtracking's move, for enumerating every path. "
        "Reachability asks 'can I get there at all' — one visit answers "
        "it forever."
    ),
    "edge_examinations": (
        "Edge u-v is stored in adj[u] AND in adj[v] (L1), and each list "
        "is read exactly once."
    ),
    "dfs_launches": (
        "One launch paints one whole component. Count the islands in the "
        "drawing, not the vertices."
    ),
}

_K_LABELS: dict[str, str] = {
    "dfs_total_cost": "K1 — DFS total cost",
    "visited_why": "K2 — why visited exists",
    "visited_mark_moment": "K3 — when to mark",
    "visited_unmark": "K4 — when to un-mark",
    "edge_examinations": "K5 — how often one edge is seen",
    "dfs_launches": "K6 — component launches",
}


def _assert_int_set(got: object, fn_name: str) -> set[int]:
    assert isinstance(got, set), (
        f"{got!r} is a {type(got).__name__}, not a set — {fn_name} must "
        "return a set"
    )
    for item in got:
        assert isinstance(item, int), (
            f"{item!r} is a {type(item).__name__}, not an int"
        )
    return got


def _assert_cell_set(got: object) -> set[tuple[int, int]]:
    assert isinstance(got, set), (
        f"{got!r} is a {type(got).__name__}, not a set — region must "
        "return a set"
    )
    for item in got:
        assert isinstance(item, tuple), (
            f"{item!r} is a {type(item).__name__}, not a tuple — cells "
            "are (row, col) tuples"
        )
    return got


# The L1 network: triangle 0-1-2 (a cycle!), tail 1-3, isolated 4.
_NETWORK: list[list[int]] = [[0, 1], [1, 2], [2, 0], [1, 3]]


def _test_reach_cycle() -> None:
    got = _assert_int_set(reachable(5, _NETWORK, 0), "reachable")
    want = {0, 1, 2, 3}
    assert got == want, (
        f"reachable from 0 in the L1 network: got {sorted(got)!r}, "
        f"expected {sorted(want)!r} — the triangle 0-1-2 is a cycle; "
        "vertex 4 is on its own island"
    )


def _test_reach_isolated_start() -> None:
    got = _assert_int_set(reachable(5, _NETWORK, 4), "reachable")
    assert got == {4}, (
        f"reachable from the isolated vertex 4: got {sorted(got)!r}, "
        "expected [4] — a vertex always reaches itself, edges or not"
    )


def _test_reach_undirected_both_ways() -> None:
    got = _assert_int_set(reachable(3, [[1, 0], [2, 1]], 0), "reachable")
    want = {0, 1, 2}
    assert got == want, (
        f"edges [[1, 0], [2, 1]], start 0: got {sorted(got)!r}, expected "
        f"{sorted(want)!r} — undirected edges walk BOTH ways, whichever "
        "order the pair is written in"
    )


# 3x4 grid. The A-region is a 2x2 block — a cycle in disguise.
_GRID_MIXED: list[list[str]] = [
    ["A", "A", "B", "B"],
    ["A", "A", "B", "C"],
    ["C", "C", "C", "C"],
]

# The top and bottom rows share a value: negative-index wrap glues them.
_GRID_WRAP: list[list[str]] = [
    ["A", "A", "B"],
    ["B", "B", "B"],
    ["A", "A", "B"],
]

_GRID_DIAG: list[list[str]] = [
    ["A", "B"],
    ["B", "A"],
]


def _test_region_block_cycle() -> None:
    got = _assert_cell_set(region(_GRID_MIXED, 0, 0))
    want = {(0, 0), (0, 1), (1, 0), (1, 1)}
    assert got == want, (
        f"the A-region of (0, 0): got {sorted(got)!r}, expected "
        f"{sorted(want)!r} — a 2x2 block is already a cycle: "
        "(0,0)->(0,1)->(1,1)->(1,0)->(0,0)"
    )


def _test_region_fenced_by_labels() -> None:
    got = _assert_cell_set(region(_GRID_MIXED, 0, 2))
    want = {(0, 2), (0, 3), (1, 2)}
    assert got == want, (
        f"the B-region of (0, 2): got {sorted(got)!r}, expected "
        f"{sorted(want)!r} — the flood may only step on cells whose "
        "value equals grid[r][c]; other labels are fences"
    )


def _test_region_negative_wrap() -> None:
    got = _assert_cell_set(region(_GRID_WRAP, 0, 0))
    want = {(0, 0), (0, 1)}
    assert got == want, (
        f"the top-left A-region: got {sorted(got)!r}, expected "
        f"{sorted(want)!r} — if bottom-row cells (or negative "
        "coordinates) appear, grid[-1] wrapped around: the bounds check "
        "must reject negatives explicitly"
    )


def _test_region_no_diagonals() -> None:
    got = _assert_cell_set(region(_GRID_DIAG, 0, 0))
    assert got == {(0, 0)}, (
        f"region of (0, 0) in [[A, B], [B, A]]: got {sorted(got)!r}, "
        "expected [(0, 0)] alone — the other A touches only at a "
        "corner, and diagonals are not edges"
    )


def _check(name: str, fn) -> bool | None:
    try:
        fn()
    except NotImplementedError:
        print(f"  ..  {name} — not attempted yet")
        return None
    except RecursionError:
        print(
            f"  FAIL  {name}: RecursionError — your DFS never finished. "
            "On a cycle, an unguarded traversal re-enters vertices "
            "forever. Where (and WHEN) is visited marked?"
        )
        return False
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
    ("F1 — reachable: survives the cycle", _test_reach_cycle),
    ("F2 — reachable: isolated start reaches itself", _test_reach_isolated_start),
    ("F3 — reachable: undirected walks both ways", _test_reach_undirected_both_ways),
    ("F4 — region: 2x2 block (cycle in disguise)", _test_region_block_cycle),
    ("F5 — region: labels are fences", _test_region_fenced_by_labels),
    ("F6 — region: negative wrap trap", _test_region_negative_wrap),
    ("F7 — region: corners are not edges", _test_region_no_diagonals),
] + [(_K_LABELS[key], _make_knowledge_test(key)) for key in _K_ANSWERS]

if __name__ == "__main__":
    print("\nDFS drill — L2\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green — you can walk a graph with cycles. Tell your")
        print("teacher: P1 (Number of Islands, LC 200) is next.\n")
    else:
        print("\nReport this output to your teacher, reds included.\n")
