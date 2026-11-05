"""
L6 drill — topological order: in-degrees, checking an order, Kahn's loop.

HOW TO USE
    1. Read lesson 0011 (topological sort) first — then CLOSE it, and
       the reference sheet too.
    2. Implement the three functions below and fill every KNOWLEDGE cell
       with one of its allowed answers, spelled exactly as listed.
    3. Run, from the repo root:
           python3.14 learning/graphs/lessons/0012-topo-sort-drill.py
    4. Report the output to your teacher — reds included.

EDGE CONVENTION FOR THIS WHOLE FILE
    Vertices are 0 .. n-1. An edge [u, v] means u -> v: "u must come
    before v". Edges are DIRECTED — [u, v] says nothing about v -> u.

There are no solutions in this file.
"""

from collections import deque, defaultdict


# ----------------------------------------------------------------------------
# PART F — three functions
# ----------------------------------------------------------------------------

def in_degrees(n: int, edges: list[list[int]]) -> list[int]:
    """Return a list `deg` of length n where deg[v] is the in-degree of v:
    the number of edges that point INTO v.

    Rules:
      - Vertices with no incoming edges have in-degree 0 — including
        vertices that appear in no edge at all.
      - Return a list of ints, indexed by vertex.
    """
    deg: list[int] = [0] * n
    for _, v in edges:
        deg[v] += 1

    return deg


def is_topological(n: int, edges: list[list[int]], order: list[int]) -> bool:
    """Return True if `order` is a topological order of the graph, else False.

    A topological order lists EVERY vertex 0 .. n-1 exactly once, and for
    every edge [u, v], u appears somewhere before v.

    Rules:
      - A missing vertex, a repeated vertex, or an out-of-range value
        makes the order invalid.
      - "Before" means anywhere earlier in the list, not necessarily
        right next to it.
      - Return a bool.
    """
    # Fix given by the teacher on 2026-11-05, at Gil's request.
    #
    # Rule 1: every vertex 0..n-1 exactly once. Sorting a valid order gives
    # back exactly [0, 1, ..., n-1]. A missing vertex, an extra copy
    # ([0, 0, 1]) or a stranger (7) all break that equality. A set would
    # merge the extra copy and hide it, so its size proves nothing (F6).
    if sorted(order) != list(range(n)):
        return False

    # Rule 2: every arrow points right. Record each vertex's position in
    # the order, then check each edge [u, v]: u's position must be smaller
    # than v's. In-degrees take no part. They count arrows; they don't say
    # where an arrow starts (F13, F14).
    pos: dict[int, int] = {v: i for i, v in enumerate(order)}
    return all(pos[u] < pos[v] for u, v in edges)


def kahn_order(n: int, edges: list[list[int]]) -> list[int]:
    """Return a topological order of the graph as a list of all n vertices.

    GUARANTEE: the graph given to this function has NO directed cycle —
    an order always exists. (What to do when it doesn't is not this
    function's job.)

    Rules:
      - Any valid topological order is accepted; the harness checks the
        definition, not one fixed answer.
      - Vertices that appear in no edge still belong in the order.
      - No recursion — Kahn's algorithm is a loop and a queue.
      - Return a list of ints.
    """
    adj: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    deg = in_degrees(n, edges)
    q = deque([v for v in range(n) if deg[v] == 0])

    order: list[int] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            deg[v] -= 1
            if deg[v] == 0:
                q.append(v)

    return order



# ----------------------------------------------------------------------------
# PART K — six knowledge cells
# ----------------------------------------------------------------------------
#
# K1 "kahn_total_cost" — total cost of Kahn's algorithm over an adjacency
#     list (V vertices, E edges), in-degree setup included. One of (exactly):
#     "O(V)"   "O(E)"   "O(V + E)"   "O(V * E)"
#
# K2 "decrement_count" — over one whole run on a DAG, the line
#     `indeg[v] -= 1` executes... One of (exactly):
#     "exactly V times"
#     "exactly E times"
#     "exactly 2E times"
#     "up to V * V times"
#
# K3 "enqueue_moment" — a vertex with predecessors joins the queue...
#     One of (exactly):
#     "the moment its first predecessor is popped"
#     "the moment its last predecessor is popped"
#     "the moment it is first reached as a neighbor"
#     "the moment the layer holding it is served"
#
# K4 "cycle_symptom" — run Kahn's loop on a graph that HAS a directed
#     cycle. The loop... One of (exactly):
#     "ends with some vertices never popped at all"
#     "runs forever, re-enqueuing the cycle's vertices"
#     "raises an error when it reaches the cycle"
#     "pops every vertex, but the cycle out of order"
#
# K5 "leftover_set" — in that run, the vertices never popped are...
#     One of (exactly):
#     "exactly the vertices that lie on a cycle"
#     "the cycle's vertices plus everything they point to, transitively"
#     "the vertices whose starting in-degree was the largest"
#     "the vertices whose starting in-degree was zero"
#
# K6 "reverse_postorder_reverses" — the DFS route to a topological order
#     is called "reverse postorder". What gets reversed? One of (exactly):
#     "the list of vertices in the order DFS finished them"
#     "the direction of every edge, as in the transpose graph"
#     "the order in which each vertex's neighbors are visited"
#     "the in-degree counts, which then count down to zero"

KNOWLEDGE: dict[str, str | None] = {
    "kahn_total_cost": "O(V + E)",
    "decrement_count": "exactly E times",
    "enqueue_moment": "the moment its last predecessor is popped",
    "cycle_symptom": "ends with some vertices never popped at all",
    "leftover_set": "the cycle's vertices plus everything they point to, transitively",
    "reverse_postorder_reverses": "the list of vertices in the order DFS finished them",
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

import inspect
import signal

_K_ALLOWED: dict[str, set[str]] = {
    "kahn_total_cost": {"O(V)", "O(E)", "O(V + E)", "O(V * E)"},
    "decrement_count": {
        "exactly V times",
        "exactly E times",
        "exactly 2E times",
        "up to V * V times",
    },
    "enqueue_moment": {
        "the moment its first predecessor is popped",
        "the moment its last predecessor is popped",
        "the moment it is first reached as a neighbor",
        "the moment the layer holding it is served",
    },
    "cycle_symptom": {
        "ends with some vertices never popped at all",
        "runs forever, re-enqueuing the cycle's vertices",
        "raises an error when it reaches the cycle",
        "pops every vertex, but the cycle out of order",
    },
    "leftover_set": {
        "exactly the vertices that lie on a cycle",
        "the cycle's vertices plus everything they point to, transitively",
        "the vertices whose starting in-degree was the largest",
        "the vertices whose starting in-degree was zero",
    },
    "reverse_postorder_reverses": {
        "the list of vertices in the order DFS finished them",
        "the direction of every edge, as in the transpose graph",
        "the order in which each vertex's neighbors are visited",
        "the in-degree counts, which then count down to zero",
    },
}

_K_ANSWERS: dict[str, str] = {
    "kahn_total_cost": "O(V + E)",
    "decrement_count": "exactly E times",
    "enqueue_moment": "the moment its last predecessor is popped",
    "cycle_symptom": "ends with some vertices never popped at all",
    "leftover_set": "the cycle's vertices plus everything they point to, transitively",
    "reverse_postorder_reverses": "the list of vertices in the order DFS finished them",
}

_K_HINTS: dict[str, str] = {
    "kahn_total_cost": (
        "Count, don't guess: the in-degree pass reads each edge once, "
        "every vertex is popped at most once, and each pop reads its own "
        "out-list once. Added, not multiplied."
    ),
    "decrement_count": (
        "A directed edge u -> v is stored ONCE, in adj[u] only — unlike "
        "the undirected lists of L2/L4, which stored every edge twice. "
        "Each out-list is read once, when its owner is popped."
    ),
    "enqueue_moment": (
        "Shoes must wait for pants AND socks. Enqueuing at the first "
        "arrival was exactly your BFS's mistake in the lesson — the count "
        "hits zero only when the LAST missing predecessor is done."
    ),
    "cycle_symptom": (
        "Counts only go down, and a vertex joins the queue only when its "
        "count hits zero. On a cycle, each vertex waits for the one "
        "before it — nobody goes first, the queue simply runs dry."
    ),
    "leftover_set": (
        "In the lesson, the belt was not on the pants <-> shoes cycle, "
        "yet it was never popped. Why? One of its predecessors was stuck."
    ),
    "reverse_postorder_reverses": (
        "Name the SUBJECT of each reversal. L5's transpose reversed the "
        "EDGES. Reverse postorder touches no edge at all: it takes a "
        "LIST DFS produced and reads it backwards."
    ),
}

_K_LABELS: dict[str, str] = {
    "kahn_total_cost": "K1 — Kahn total cost",
    "decrement_count": "K2 — how often the decrement runs",
    "enqueue_moment": "K3 — when a vertex joins the queue",
    "cycle_symptom": "K4 — what a cycle does to the loop",
    "leftover_set": "K5 — who is left over",
    "reverse_postorder_reverses": "K6 — which 'reverse' is reverse postorder",
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


def _valid(n: int, edges: list[list[int]], order: list[int]) -> bool:
    if sorted(order) != list(range(n)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[u] < pos[v] for u, v in edges)


def _first_violation(edges: list[list[int]], order: list[int]) -> str:
    pos = {v: i for i, v in enumerate(order)}
    for u, v in edges:
        if u in pos and v in pos and pos[u] > pos[v]:
            return f"edge [{u}, {v}] says {u} before {v}, but {v} came first"
    return ""


def _assert_int_list(got: object, fn_name: str) -> list[int]:
    assert isinstance(got, list), (
        f"{got!r} is a {type(got).__name__}, not a list — {fn_name} must "
        "return a list of ints"
    )
    for x in got:
        assert isinstance(x, int) and not isinstance(x, bool), (
            f"element {x!r} is a {type(x).__name__}, not an int"
        )
    return got


def _assert_order(n: int, edges: list[list[int]], got: object, story: str) -> None:
    order = _assert_int_list(got, "kahn_order")
    assert sorted(order) == list(range(n)), (
        f"{story}: got {order!r} — that is not every vertex 0..{n - 1} "
        "exactly once. Vertices missing? Every vertex belongs in the order, "
        "including those that appear in no edge"
    )
    bad = _first_violation(edges, order)
    assert not bad, f"{story}: got {order!r} — {bad}"


def _assert_bool(got: object) -> bool:
    assert isinstance(got, bool), (
        f"{got!r} is a {type(got).__name__}, not a bool — is_topological "
        "answers True or False"
    )
    return got


# The lesson's dressing graph, numbered so the lesson's BFS trap fires:
#   0 socks   1 underwear   2 shirt   3 pants   4 shoes   5 belt
_DRESS: list[list[int]] = [[1, 3], [3, 4], [0, 4], [3, 5], [2, 5]]

# One long route and one shortcut to the same vertex: 0->1->2->3 and 0->3.
# Every plain BFS, whatever the seed order, reaches 3 before 2.
_SHORTCUT: list[list[int]] = [[0, 1], [1, 2], [2, 3], [0, 3]]


def _test_queue_discipline() -> None:
    src = _source_of(kahn_order)
    if "NotImplementedError" in src:
        raise NotImplementedError
    for banned in (".pop(0)", ".insert(0"):
        assert banned not in src, (
            f"kahn_order uses {banned!r} on a list — lists "
            '"incur O(n) memory movement costs for pop(0) and insert(0, v)"'
            ". V pops of O(n) each and O(V + E) quietly becomes O(V**2). "
            "The queue is deque: append + popleft."
        )


def _test_deg_dress() -> None:
    got = _assert_int_list(in_degrees(6, _DRESS), "in_degrees")
    want = [0, 0, 0, 1, 2, 2]
    assert got == want, (
        f"in_degrees on the dressing graph: got {got!r}, expected {want!r} "
        "— shoes (4) has TWO arrows coming in (pants, socks); socks (0) "
        "has none. If the counts look mirrored, you counted arrows going "
        "OUT: in [u, v] the arrow lands on v"
    )


def _test_deg_isolated() -> None:
    got = _assert_int_list(in_degrees(4, [[0, 1]]), "in_degrees")
    want = [0, 1, 0, 0]
    assert got == want, (
        f"in_degrees(4, [[0, 1]]): got {got!r}, expected {want!r} — one "
        "entry per vertex 0..n-1; vertices 2 and 3 appear in no edge and "
        "have in-degree 0. An edge is directed: [0, 1] adds nothing to 0"
    )


def _test_check_valid() -> None:
    got = _assert_bool(is_topological(6, _DRESS, [0, 1, 2, 3, 4, 5]))
    assert got is True, (
        "is_topological on the lesson's Kahn output [0, 1, 2, 3, 4, 5]: got "
        "False, expected True — every edge's left end comes earlier"
    )


def _test_check_bfs_trap() -> None:
    got = _assert_bool(is_topological(6, _DRESS, [0, 1, 2, 4, 3, 5]))
    assert got is False, (
        "is_topological on the lesson's BFS output [0, 1, 2, 4, 3, 5]: got "
        "True, expected False — shoes (4) comes before pants (3), and "
        "edge [3, 4] says pants first. Check every EDGE, not just "
        "neighbours in the list"
    )
    far = _assert_bool(is_topological(6, _DRESS, [4, 1, 3, 0, 2, 5]))
    assert far is False, (
        "is_topological on [4, 1, 3, 0, 2, 5]: got True, expected False — "
        "shoes (4) is FIRST, yet pants (3) and socks (0) must precede it. "
        "No two neighbours in this list break an edge; the violations "
        "are between positions far apart. Check every EDGE"
    )


def _test_check_far_apart() -> None:
    got = _assert_bool(is_topological(3, [[0, 2]], [0, 1, 2]))
    assert got is True, (
        "is_topological(3, [[0, 2]], [0, 1, 2]): got False, expected True — "
        "0 is before 2; they need not be adjacent in the list"
    )


def _test_check_missing_and_repeats() -> None:
    missing = _assert_bool(is_topological(3, [[0, 1]], [0, 1]))
    assert missing is False, (
        "is_topological(3, [[0, 1]], [0, 1]): got True, expected False — "
        "vertex 2 is missing. An order lists EVERY vertex"
    )
    repeat = _assert_bool(is_topological(3, [[0, 1]], [0, 1, 1]))
    assert repeat is False, (
        "is_topological(3, [[0, 1]], [0, 1, 1]): got True, expected False — "
        "1 appears twice and 2 never. Exactly once each"
    )
    stranger = _assert_bool(is_topological(2, [], [0, 7]))
    assert stranger is False, (
        "is_topological(2, [], [0, 7]): got True, expected False — 7 is not "
        "a vertex of a 2-vertex graph, and vertex 1 is missing"
    )
    padded = _assert_bool(is_topological(2, [], [0, 0, 1]))
    assert padded is False, (
        "is_topological(2, [], [0, 0, 1]): got True, expected False — "
        "nothing is missing, yet 0 appears twice: the list is longer than n. "
        "Exactly once each means no extras either"
    )


# Added 2026-11-05 after the first hand-in: F3-F6 never separated "every
# edge's left end comes first" from "in-degrees never go down along the
# list". These two cases do — one in each direction.

def _test_check_equal_counts() -> None:
    got = _assert_bool(is_topological(3, [[0, 1], [1, 2]], [0, 2, 1]))
    assert got is False, (
        "is_topological(3, [[0, 1], [1, 2]], [0, 2, 1]): got True, expected "
        "False — edge [1, 2] says 1 before 2, but 2 came first. 1 and 2 both "
        "have in-degree 1: a count of incoming arrows can't tell you WHERE "
        "an arrow comes from"
    )


def _test_check_loner_last() -> None:
    got = _assert_bool(is_topological(3, [[0, 1]], [0, 1, 2]))
    assert got is True, (
        "is_topological(3, [[0, 1]], [0, 1, 2]): got False, expected True — "
        "the only edge [0, 1] is respected. 2 touches no edge, so it may sit "
        "anywhere, even right after a vertex with a larger in-degree"
    )


def _test_kahn_dress() -> None:
    _assert_order(6, _DRESS, kahn_order(6, _DRESS), "kahn_order on the dressing graph")


def _test_kahn_shortcut() -> None:
    got = kahn_order(4, _SHORTCUT)
    _assert_order(
        4, _SHORTCUT, got,
        "kahn_order on 0->1->2->3 plus the shortcut 0->3 (if 3 came before "
        "2: it was queued on its FIRST arrival, the way BFS does — it must "
        "wait for its LAST)"
    )


def _test_kahn_isolated() -> None:
    edges = [[2, 0]]
    _assert_order(4, edges, kahn_order(4, edges),
                  "kahn_order(4, [[2, 0]]) — vertices 1 and 3 sit in no edge")


def _test_kahn_many_sources() -> None:
    # Three independent chains merging into 9.
    edges = [[0, 3], [3, 6], [1, 4], [4, 7], [2, 5], [5, 8],
             [6, 9], [7, 9], [8, 9]]
    _assert_order(10, edges, kahn_order(10, edges),
                  "kahn_order on three chains merging into 9 (three sources "
                  "at the start — seed ALL of them)")


def _test_kahn_long_line() -> None:
    n = 1500
    line = [[i, i + 1] for i in range(n - 1)]
    got = _assert_int_list(kahn_order(n, line), "kahn_order")
    assert got == list(range(n)), (
        f"kahn_order on a {n}-vertex line 0->1->...: the only valid order is "
        f"0, 1, ..., {n - 1}; got a list of length {len(got)} starting "
        f"{got[:5]!r}"
    )


def _test_kahn_big_line() -> None:
    # Hard stop for the round-by-round rescan: V rounds x V scans on 100 000
    # vertices is ~5e9 steps and will not finish inside the 5s limit.
    n = 100_000
    line = [[i, i + 1] for i in range(n - 1)]
    got = _assert_int_list(kahn_order(n, line), "kahn_order")
    assert got == list(range(n)), (
        f"kahn_order on a {n}-vertex line: expected 0..{n - 1} in order"
    )


_TIMEOUT_HINTS: dict[str, str] = {
    "F11": (
        "never finished (5s limit) on 100 000 vertices. Linear work here is "
        "~200 000 steps. Are you RESCANNING all vertices each round for "
        "in-degree 0? That is V rounds x V = V**2. The queue exists so "
        "that newly-ready vertices are handed to you, never searched for"
    ),
}


def _check(name: str, fn) -> bool | None:
    try:
        _with_time_limit(5, fn)
    except NotImplementedError:
        print(f"  ..  {name} — not attempted yet")
        return None
    except _Timeout:
        key = name.split(" ", 1)[0]
        hint = _TIMEOUT_HINTS.get(key, (
            "never finished (5s limit) — something is being enqueued "
            "forever. Kahn's needs no seen set: a count only goes DOWN, so "
            "it hits zero at most once. Is a vertex queued every time its "
            "count is touched?"
        ))
        print(f"  FAIL  {name}: {hint}")
        return False
    except RecursionError:
        print(
            f"  FAIL  {name}: RecursionError — Kahn's algorithm is a LOOP "
            "and a queue. A long chain overflows Python's call stack (default limit ~1000 frames)."
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
    ("F1 — in_degrees: the dressing graph", _test_deg_dress),
    ("F2 — in_degrees: isolated vertices, one direction", _test_deg_isolated),
    ("F3 — is_topological: a valid order", _test_check_valid),
    ("F4 — is_topological: the lesson's BFS trap", _test_check_bfs_trap),
    ("F5 — is_topological: 'before' is not 'next to'", _test_check_far_apart),
    ("F6 — is_topological: missing / repeated / stranger", _test_check_missing_and_repeats),
    ("F13 — is_topological: equal in-degrees, the edge still decides", _test_check_equal_counts),
    ("F14 — is_topological: a vertex in no edge may sit last", _test_check_loner_last),
    ("F7 — kahn_order: the dressing graph", _test_kahn_dress),
    ("F8 — kahn_order: the shortcut (wait for the LAST arrival)", _test_kahn_shortcut),
    ("F9 — kahn_order: isolated vertices belong too", _test_kahn_isolated),
    ("F10 — kahn_order: several sources", _test_kahn_many_sources),
    ("F11 — kahn_order: 100 000-line (linear, not V**2)", _test_kahn_big_line),
    ("F12 — kahn_order: 1500-line (loop, not recursion)", _test_kahn_long_line),
] + [(_K_LABELS[key], _make_knowledge_test(key)) for key in _K_ANSWERS]

if __name__ == "__main__":
    print("\nTopological sort drill — L6\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green — you can order a DAG and say why a cycle can't be")
        print("ordered. Tell your teacher: P8 (Course Schedule, LC 207) is")
        print("next — the assembly is yours.\n")
    else:
        print("\nReport this output to your teacher, reds included.\n")
