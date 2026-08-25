"""
L4 drill — BFS: layers are distances, the snapshot loop, multi-source seeding.

HOW TO USE
    1. Read lesson 0008 (BFS: layers are distances) first — then CLOSE it.
    2. Implement the three functions below and fill every KNOWLEDGE cell
       with one of its allowed answers, spelled exactly as listed.
    3. Run, from the repo root:
           python3.14 learning/graphs/lessons/0009-bfs-drill.py
    4. Report the output to your teacher — reds included.

There are no solutions in this file.
"""

from collections import deque


# ----------------------------------------------------------------------------
# PART F — three functions
# ----------------------------------------------------------------------------

def bfs_dist(n: int, edges: list[list[int]], start: int) -> dict[int, int]:
    """Return {vertex: distance from `start`} for every REACHABLE vertex
    of an UNDIRECTED graph. Distance = minimum number of edges.

    Vertices are 0 .. n-1; `edges` is an edge list, exactly as in L1.

    Rules:
      - Unreachable vertices must NOT appear in the result at all.
      - `start` is always reachable from itself, at distance 0 —
        even when it has no edges.
      - The graph may contain cycles; there may be several routes to a
        vertex — report the SHORTEST one.
      - No recursion: BFS is a loop and a queue.
      - Return a dict mapping int to int.
    """
    raise NotImplementedError


def steps(grid: list[list[str]], start: tuple[int, int],
          target: tuple[int, int]) -> int:
    """Return the minimum number of 4-directional steps from `start` to
    `target` over OPEN cells, or -1 if `target` cannot be reached.

    Cells hold "." (open — may be stepped on) or "#" (wall — may not).
    `start` and `target` are (row, col) tuples and are always open cells.

    Rules:
      - 4 directions only, no diagonals; the grid may be non-square.
      - Standing on `start` costs 0 steps; if start == target, answer 0.
      - Walls block: a path must consist of open cells only.
      - Return an int (a plain count, or -1).
    """
    raise NotImplementedError


def nearest(n: int, edges: list[list[int]],
            sources: list[int]) -> dict[int, int]:
    """Return {vertex: distance to its NEAREST source} for every vertex
    of an UNDIRECTED graph reachable from at least one source.

    Vertices are 0 .. n-1; `edges` is an edge list; `sources` is a
    non-empty list of distinct vertices.

    Rules:
      - Every source is at distance 0 from itself.
      - All sources spread SIMULTANEOUSLY — one traversal, not one
        traversal per source.
      - Vertices unreachable from every source must not appear.
      - No recursion. Return a dict mapping int to int.
    """
    raise NotImplementedError


# ----------------------------------------------------------------------------
# PART K — six knowledge cells
# ----------------------------------------------------------------------------
#
# K1 "bfs_total_cost" — total cost of BFS with a seen set over an
#     adjacency list (V vertices, E edges). One of (exactly):
#     "O(V)"   "O(E)"   "O(V + E)"   "O(V * E)"
#
# K2 "queue_append_count" — over one whole BFS run (counting the seed),
#     queue.append executes... One of (exactly):
#     "at most V times"
#     "exactly 2E times"
#     "once per edge walked"
#     "up to V * V times"
#
# K3 "seen_check_count" — with every vertex reachable, the check
#     `v not in seen` executes in total... One of (exactly):
#     "exactly V"   "exactly E"   "exactly 2E"   "exactly V * E"
#
# K4 "mark_moment" — a vertex v is marked seen... One of (exactly):
#     "the moment v is appended to the queue"
#     "the moment v is popped from the queue"
#     "after the neighbor loop of v finishes"
#     "when the layer holding v is complete"
#
# K5 "layer_order_why" — layers are served in distance order because...
#     One of (exactly):
#     "older discoveries are always served before newer ones"
#     "newer discoveries are always served before older ones"
#     "each vertex is discovered from its farthest neighbor"
#     "each layer is sorted by label before being served"
#
# K6 "snapshot_why" — `for _ in range(len(queue))` serves exactly one
#     layer because... One of (exactly):
#     "range evaluates len once, when the for begins"
#     "range re-evaluates len after every single turn"
#     "append during the loop goes to a hidden buffer"
#     "popleft shrinks it as fast as append grows it"

KNOWLEDGE: dict[str, str | None] = {
    "bfs_total_cost": None,
    "queue_append_count": None,
    "seen_check_count": None,
    "mark_moment": None,
    "layer_order_why": None,
    "snapshot_why": None,
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

import inspect
import signal

_K_ALLOWED: dict[str, set[str]] = {
    "bfs_total_cost": {"O(V)", "O(E)", "O(V + E)", "O(V * E)"},
    "queue_append_count": {
        "at most V times",
        "exactly 2E times",
        "once per edge walked",
        "up to V * V times",
    },
    "seen_check_count": {"exactly V", "exactly E", "exactly 2E", "exactly V * E"},
    "mark_moment": {
        "the moment v is appended to the queue",
        "the moment v is popped from the queue",
        "after the neighbor loop of v finishes",
        "when the layer holding v is complete",
    },
    "layer_order_why": {
        "older discoveries are always served before newer ones",
        "newer discoveries are always served before older ones",
        "each vertex is discovered from its farthest neighbor",
        "each layer is sorted by label before being served",
    },
    "snapshot_why": {
        "range evaluates len once, when the for begins",
        "range re-evaluates len after every single turn",
        "append during the loop goes to a hidden buffer",
        "popleft shrinks it as fast as append grows it",
    },
}

_K_ANSWERS: dict[str, str] = {
    "bfs_total_cost": "O(V + E)",
    "queue_append_count": "at most V times",
    "seen_check_count": "exactly 2E",
    "mark_moment": "the moment v is appended to the queue",
    "layer_order_why": "older discoveries are always served before newer ones",
    "snapshot_why": "range evaluates len once, when the for begins",
}

_K_HINTS: dict[str, str] = {
    "bfs_total_cost": (
        "Count, don't guess: at most V appends + V pops (seen caps each "
        "vertex at one claim), PLUS one check per neighbor-list entry — "
        "2E entries total. Added, not multiplied."
    ),
    "queue_append_count": (
        "Every append is guarded by `v not in seen`, and marks are "
        "permanent — a vertex can be claimed how many times?"
    ),
    "seen_check_count": (
        "One check per neighbor-list entry, each list read exactly once. "
        "An undirected edge is stored in BOTH endpoints' lists — the same "
        "2 + 2 + 2 = 6 you counted on the Clone Graph triangle."
    ),
    "mark_moment": (
        "Between append and popleft a vertex just WAITS in the queue. If "
        "it is not yet marked while waiting, a second neighbor discovers "
        "it and enqueues another copy."
    ),
    "layer_order_why": (
        "FIFO: whoever joined the line first is served first — and "
        "serving distance-d vertices only ever discovers vertices at "
        "distance d + 1 or less."
    ),
    "snapshot_why": (
        "The appends made DURING the inner loop grow the queue — but not "
        "the range, which was computed from len(queue) exactly once, at "
        "the top."
    ),
}

_K_LABELS: dict[str, str] = {
    "bfs_total_cost": "K1 — BFS total cost",
    "queue_append_count": "K2 — how often append runs",
    "seen_check_count": "K3 — how many seen-checks",
    "mark_moment": "K4 — when to mark",
    "layer_order_why": "K5 — why layers are distances",
    "snapshot_why": "K6 — why the snapshot loop works",
}


class _Timeout(Exception):
    pass


def _with_time_limit(seconds: int, fn):
    def _handler(signum, frame):
        raise _Timeout()
    old = signal.signal(signal.SIGALRM, _handler)
    signal.alarm(seconds)
    try:
        return fn()
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def _source_of(fn) -> str:
    src = inspect.getsource(fn)
    for quote in ('"""', "'''"):
        i = src.find(quote)
        if i != -1:
            j = src.find(quote, i + 3)
            if j != -1:
                return src[:i] + src[j + 3:]
    return src


def _assert_dist_dict(got: object, fn_name: str) -> dict[int, int]:
    assert isinstance(got, dict), (
        f"{got!r} is a {type(got).__name__}, not a dict — {fn_name} must "
        "return a dict mapping vertex to distance"
    )
    for k, v in got.items():
        assert isinstance(k, int) and not isinstance(k, bool), (
            f"key {k!r} is a {type(k).__name__}, not an int"
        )
        assert isinstance(v, int) and not isinstance(v, bool), (
            f"value {v!r} is a {type(v).__name__}, not an int"
        )
    return got


def _assert_step_count(got: object) -> int:
    assert isinstance(got, int) and not isinstance(got, bool), (
        f"{got!r} is a {type(got).__name__}, not an int — steps must "
        "return a plain count, or -1"
    )
    return got


def _test_queue_discipline() -> None:
    fns = [bfs_dist, steps, nearest]
    sources = [(f.__name__, _source_of(f)) for f in fns]
    implemented = [(n, s) for n, s in sources if "NotImplementedError" not in s]
    if not implemented:
        raise NotImplementedError
    for name, src in implemented:
        for banned in (".pop(0)", ".insert(0"):
            assert banned not in src, (
                f"{name} uses {banned!r} on a list — the docs: lists "
                '"incur O(n) memory movement costs for pop(0) and '
                'insert(0, v)". V pops of O(n) each and your O(V + E) '
                "quietly becomes O(V**2). The queue is deque: append + "
                "popleft, both O(1)."
            )


# The opening square of L4: 0-1-2-3-0. DFS reaches 3 at depth 3; truth is 1.
_SQUARE: list[list[int]] = [[0, 1], [1, 2], [2, 3], [3, 0]]

# Triangle: vertex 2 is discovered twice in the same wave.
_TRIANGLE: list[list[int]] = [[0, 1], [1, 2], [2, 0]]

# The L1 network: triangle 0-1-2, tail 1-3, isolated 4.
_NETWORK: list[list[int]] = [[0, 1], [1, 2], [2, 0], [1, 3]]


def _test_dist_square() -> None:
    got = _assert_dist_dict(bfs_dist(4, _SQUARE, 0), "bfs_dist")
    want = {0: 0, 1: 1, 3: 1, 2: 2}
    assert got == want, (
        f"bfs_dist on the square 0-1-2-3-0 from 0: got {got!r}, expected "
        f"{want!r} — vertex 3 is a DIRECT neighbor of 0. Distance 3 for "
        "it is the DFS route's depth, not the shortest path; the first "
        "time BFS reaches a vertex must be via a shortest path"
    )


def _test_dist_triangle_rediscovery() -> None:
    got = _assert_dist_dict(bfs_dist(3, _TRIANGLE, 0), "bfs_dist")
    want = {0: 0, 1: 1, 2: 1}
    assert got == want, (
        f"bfs_dist on the triangle from 0: got {got!r}, expected {want!r} "
        "— both 1 and 2 are at distance 1. If 2 came out farther, it "
        "entered the queue more than once and a LATER copy overwrote its "
        "distance: mark on ENQUEUE, and claim each vertex exactly once"
    )


def _test_dist_unreachable_excluded() -> None:
    got = _assert_dist_dict(bfs_dist(5, _NETWORK, 0), "bfs_dist")
    want = {0: 0, 1: 1, 2: 1, 3: 2}
    assert got == want, (
        f"bfs_dist on the L1 network from 0: got {got!r}, expected "
        f"{want!r} — vertex 4 is on its own island: unreachable vertices "
        "must not appear in the result at all"
    )


def _test_dist_isolated_start() -> None:
    got = _assert_dist_dict(bfs_dist(5, _NETWORK, 4), "bfs_dist")
    assert got == {4: 0}, (
        f"bfs_dist from the isolated vertex 4: got {got!r}, expected "
        "{{4: 0}} — a vertex is always at distance 0 from itself, "
        "edges or not"
    )


def _test_dist_long_line_no_recursion() -> None:
    n = 1500
    line = [[i, i + 1] for i in range(n - 1)]
    got = _assert_dist_dict(bfs_dist(n, line, 0), "bfs_dist")
    assert len(got) == n and got[n - 1] == n - 1, (
        f"bfs_dist on a {n}-vertex line from 0: expected every vertex "
        f"present with dist[{n - 1}] == {n - 1}; got {len(got)} vertices "
        f"and dist[{n - 1}] == {got.get(n - 1)!r}"
    )


_MAZE_DETOUR: list[list[str]] = [
    [".", ".", "."],
    ["#", "#", "."],
    [".", ".", "."],
]

_MAZE_WALLED: list[list[str]] = [
    [".", "#", "."],
]

_MAZE_CORNER: list[list[str]] = [
    [".", "#"],
    ["#", "."],
]


def _test_steps_detour() -> None:
    got = _assert_step_count(steps(_MAZE_DETOUR, (0, 0), (2, 0)))
    assert got == 6, (
        f"steps around the wall bar: got {got!r}, expected 6 — the wall "
        "row blocks the 2-step straight drop; the only path swings right "
        "and around: walls may never be stepped on"
    )


def _test_steps_unreachable() -> None:
    got = _assert_step_count(steps(_MAZE_WALLED, (0, 0), (0, 2)))
    assert got == -1, (
        f"steps across a full wall: got {got!r}, expected -1 — no open "
        "path exists, and 'no path' is an answer, not an error"
    )


def _test_steps_no_diagonals() -> None:
    got = _assert_step_count(steps(_MAZE_CORNER, (0, 0), (1, 1)))
    assert got == -1, (
        f"steps to the diagonal cell: got {got!r}, expected -1 — the "
        "target touches the start only at a corner, and diagonals are "
        "not edges"
    )


def _test_steps_start_is_target() -> None:
    got = _assert_step_count(steps(_MAZE_DETOUR, (1, 2), (1, 2)))
    assert got == 0, (
        f"steps from a cell to itself: got {got!r}, expected 0 — the "
        "seed IS the target, at distance 0, before any step is taken"
    )


# The lesson's closing picture: a 7-vertex line with sources at 0 and 5.
_LINE7: list[list[int]] = [[i, i + 1] for i in range(6)]


def _test_nearest_two_waves() -> None:
    got = _assert_dist_dict(nearest(7, _LINE7, [0, 5]), "nearest")
    want = {0: 0, 1: 1, 2: 2, 3: 2, 4: 1, 5: 0, 6: 1}
    assert got == want, (
        f"nearest on the 7-line with sources [0, 5]: got {got!r}, "
        f"expected {want!r} — both waves start on day 0 and ripple "
        "simultaneously; vertex 4 hears it from source 5 on day 1, not "
        "from source 0 on day 4"
    )


def _test_nearest_sources_at_zero() -> None:
    got = _assert_dist_dict(nearest(4, [[0, 1], [1, 2], [2, 3]], [0, 3]),
                            "nearest")
    want = {0: 0, 1: 1, 2: 1, 3: 0}
    assert got == want, (
        f"nearest on the 4-line with sources [0, 3]: got {got!r}, "
        f"expected {want!r} — every source is at distance 0 from itself, "
        "and the middle splits between the two nearest sources"
    )


def _check(name: str, fn) -> bool | None:
    try:
        _with_time_limit(5, fn)
    except NotImplementedError:
        print(f"  ..  {name} — not attempted yet")
        return None
    except _Timeout:
        print(
            f"  FAIL  {name}: never finished (5s limit) — the queue is "
            "being refilled forever. On a cycle, an unmarked waiting "
            "vertex gets re-enqueued endlessly. WHERE does the mark "
            "happen — on enqueue, or too late?"
        )
        return False
    except RecursionError:
        print(
            f"  FAIL  {name}: RecursionError — BFS is a LOOP and a "
            "queue, not recursion. The call stack is LIFO; distances "
            "need FIFO."
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
    ("F0 — queue discipline: no list.pop(0)", _test_queue_discipline),
    ("F1 — bfs_dist: the square (shortest, not DFS depth)", _test_dist_square),
    ("F2 — bfs_dist: triangle (no double claim)", _test_dist_triangle_rediscovery),
    ("F3 — bfs_dist: unreachable stay out", _test_dist_unreachable_excluded),
    ("F4 — bfs_dist: isolated start is at 0", _test_dist_isolated_start),
    ("F5 — bfs_dist: 1500-line (loop, not recursion)", _test_dist_long_line_no_recursion),
    ("F6 — steps: forced detour around walls", _test_steps_detour),
    ("F7 — steps: unreachable answers -1", _test_steps_unreachable),
    ("F8 — steps: corners are not edges", _test_steps_no_diagonals),
    ("F9 — steps: start equals target", _test_steps_start_is_target),
    ("F10 — nearest: two waves meet in the middle", _test_nearest_two_waves),
    ("F11 — nearest: sources sit at distance 0", _test_nearest_sources_at_zero),
] + [(_K_LABELS[key], _make_knowledge_test(key)) for key in _K_ANSWERS]

if __name__ == "__main__":
    print("\nBFS drill — L4\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green — you can measure a graph, not just walk it. Tell")
        print("your teacher: P4 (Rotting Oranges, LC 994) is next — the")
        print("assembly is yours.\n")
    else:
        print("\nReport this output to your teacher, reds included.\n")
