"""
L7 drill — union-find: parent links, union by size, path compression.

HOW TO USE
    1. Read lesson 0013 (union-find) first — then CLOSE it, and the
       reference sheet too.
    2. Implement the four methods of UnionFind below and fill every
       KNOWLEDGE cell with one of its allowed answers, spelled exactly
       as listed.
    3. Run, from the repo root:
           python3.14 learning/graphs/lessons/0014-union-find-drill.py
    4. Report the output to your teacher — reds included.

CONVENTIONS FOR THIS WHOLE FILE
    Vertices are 0 .. n-1. A cable between a and b is UNDIRECTED:
    union(a, b) and union(b, a) mean the same thing.
    The harness reads two attributes directly, so keep these names:
        self.parent: list[int]   parent[x] is x's parent; a root is its own parent
        self.size:   list[int]   size[r] is the number of vertices in r's tree,
                                 for every ROOT r

There are no solutions in this file.
"""


# ----------------------------------------------------------------------------
# PART F — one class, four methods
# ----------------------------------------------------------------------------

class UnionFind:
    def __init__(self, n: int) -> None:
        """Start with n groups of one: every vertex is its own root, and
        every tree has size 1."""
        raise NotImplementedError

    def find(self, x: int) -> int:
        """Return the root of x's tree.

        Path compression: when find(x) returns, EVERY vertex on the path
        from x up to the root has the root as its parent.
        """
        raise NotImplementedError

    def union(self, a: int, b: int) -> None:
        """Merge the group of a with the group of b.

        Rules:
          - Link ROOTS, never the vertices themselves.
          - Union by size: the root of the SMALLER tree gets the root of
            the bigger tree as its parent. On a tie, either way is fine.
          - Keep `size` correct at the new root.
          - If a and b are already in one group, nothing changes.
        """
        raise NotImplementedError

    def connected(self, a: int, b: int) -> bool:
        """Return True if a and b are in the same group, else False."""
        raise NotImplementedError


# ----------------------------------------------------------------------------
# PART K — four knowledge cells
# ----------------------------------------------------------------------------
#
# K1 "bfs_per_ask_cost" — cables keep arriving, and every "ask a b" is
#     answered with a fresh BFS from a. With V vertices and E cables so far,
#     ONE ask costs, worst case... One of (exactly):
#     "O(1)"   "O(log V)"   "O(V + E)"   "O(V * E)"
#
# K2 "naive_find_cost" — parent links WITHOUT union by size (always hang
#     a's root under b's root) and WITHOUT path compression. Worst case
#     for ONE find on n vertices... One of (exactly):
#     "O(1)"   "O(log n)"   "O(n)"   "O(n log n)"
#
# K3 "by_size_depth" — with union by size, the depth of any vertex in a
#     forest of n vertices is... One of (exactly):
#     "at most 1"
#     "at most lg n"
#     "at most n / 2"
#     "at most n - 1"
#
# K4 "size_trusted_at" — size[x] is guaranteed to be the size of x's
#     group... One of (exactly):
#     "only at a root"
#     "only at a leaf"
#     "at every vertex"
#     "right after find(x)"

KNOWLEDGE: dict[str, str | None] = {
    "bfs_per_ask_cost": None,
    "naive_find_cost": None,
    "by_size_depth": None,
    "size_trusted_at": None,
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

import hashlib
import signal

_K_ALLOWED: dict[str, set[str]] = {
    "bfs_per_ask_cost": {"O(1)", "O(log V)", "O(V + E)", "O(V * E)"},
    "naive_find_cost": {"O(1)", "O(log n)", "O(n)", "O(n log n)"},
    "by_size_depth": {"at most 1", "at most lg n", "at most n / 2", "at most n - 1"},
    "size_trusted_at": {"only at a root", "only at a leaf", "at every vertex", "right after find(x)"},
}

# SHA-256 of the right answer, so the answers can't be read off this file.
_K_DIGESTS: dict[str, str] = {
    "bfs_per_ask_cost": "2f838c97687d059844587abb2d7c9e4d98b7b1f7b0719bf3f577b5dd1df8cfdb",
    "naive_find_cost": "387008096a415eb2a5c95f1d7d9d7d5ec8c6a3b2f1f2fe7a2f7cc0f27c6f38fb",
    "by_size_depth": "0fe8a1b6bae9b094188f9bab355303a87beb3a2dbb0bbe93e9387cc1c26b0830",
    "size_trusted_at": "11d0aa49b4ab68d8d5ff71288a91ef538d326ff555ad7e50f33830eabc04a6f7",
}

_K_HINTS: dict[str, str] = {
    "bfs_per_ask_cost": (
        "The graph changes between asks, so nothing from the last BFS can be "
        "reused. Each ask starts from scratch: how much of the graph can one "
        "BFS touch?"
    ),
    "naive_find_cost": (
        "In the lesson, connecting 0 with 1, then 2, then 3, ... built a "
        "chain. How many parent links does find(0) follow on a chain of n?"
    ),
    "by_size_depth": (
        "A vertex gets one level deeper only when its tree is hung under a "
        "tree at least as big, so its tree at least DOUBLES. How many times "
        "can a group of 1 double before it holds all n?"
    ),
    "size_trusted_at": (
        "union adds to the size of the NEW root only. When a root gets a "
        "parent, nobody updates its size again."
    ),
}

_K_LABELS: dict[str, str] = {
    "bfs_per_ask_cost": "K1 — cost of one ask answered by BFS",
    "naive_find_cost": "K2 — one find without either fix",
    "by_size_depth": "K3 — depth bound under union by size",
    "size_trusted_at": "K4 — where size can be trusted",
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


def _new(n: int) -> UnionFind:
    uf = UnionFind(n)
    assert isinstance(getattr(uf, "parent", None), list), (
        f"UnionFind({n}).parent is {getattr(uf, 'parent', None)!r} — "
        "__init__ must create self.parent as a list"
    )
    assert isinstance(getattr(uf, "size", None), list), (
        f"UnionFind({n}).size is {getattr(uf, 'size', None)!r} — "
        "__init__ must create self.size as a list"
    )
    return uf


def _find(uf: UnionFind, x: int) -> int:
    got = uf.find(x)
    assert isinstance(got, int) and not isinstance(got, bool), (
        f"find({x}) returned {got!r}, a {type(got).__name__} — find returns "
        "the root, an int"
    )
    return got


def _connected(uf: UnionFind, a: int, b: int) -> bool:
    got = uf.connected(a, b)
    assert isinstance(got, bool), (
        f"connected({a}, {b}) returned {got!r}, a {type(got).__name__}, not "
        "a bool — answer True or False"
    )
    return got


def _test_init() -> None:
    uf = _new(5)
    assert uf.parent == [0, 1, 2, 3, 4], (
        f"UnionFind(5).parent: got {uf.parent!r}, expected [0, 1, 2, 3, 4] — "
        "at the start every vertex is its own root, so parent[x] == x"
    )
    assert uf.size == [1, 1, 1, 1, 1], (
        f"UnionFind(5).size: got {uf.size!r}, expected [1, 1, 1, 1, 1] — "
        "every tree starts with one vertex in it"
    )


def _test_find_fresh() -> None:
    uf = _new(4)
    for x in range(4):
        got = _find(uf, x)
        assert got == x, (
            f"find({x}) on a fresh UnionFind(4): got {got!r}, expected {x} — "
            "nothing is merged yet, so every vertex is its own root"
        )


def _test_union_connected() -> None:
    uf = _new(3)
    assert _connected(uf, 0, 1) is False, (
        "connected(0, 1) on a fresh UnionFind(3): got True, expected False — "
        "no union has run yet"
    )
    uf.union(0, 1)
    assert _connected(uf, 0, 1) is True, (
        "after union(0, 1): connected(0, 1) is False, expected True"
    )
    assert _connected(uf, 1, 0) is True, (
        "after union(0, 1): connected(1, 0) is False, expected True — a "
        "cable has no direction"
    )
    assert _connected(uf, 0, 2) is False, (
        "after union(0, 1): connected(0, 2) is True, expected False — 2 "
        "was never merged with anything"
    )


def _test_link_roots() -> None:
    uf = _new(3)
    uf.union(0, 1)
    uf.union(0, 2)
    assert _connected(uf, 1, 2) is True, (
        f"after union(0, 1) then union(0, 2): connected(1, 2) is False, "
        f"expected True. parent is now {uf.parent!r}. Did union overwrite "
        "parent[0] a second time? That cuts 0 off from its first group. "
        "Link the two ROOTS, never a and b themselves"
    )


def _test_by_size_order() -> None:
    for first, second in ((3, 0), (0, 3)):
        uf = _new(4)
        uf.union(0, 1)
        uf.union(1, 2)
        big = _find(uf, 0)
        uf.union(first, second)
        root = _find(uf, 3)
        assert root == big, (
            f"group {{0, 1, 2}} has root {big}; after union({first}, "
            f"{second}) the root of 3's group is {root!r}, expected {big}. "
            "The smaller tree (just 3) must hang under the bigger root, "
            "whatever the argument order"
        )
        assert uf.size[big] == 4, (
            f"after union({first}, {second}): size[{big}] is "
            f"{uf.size[big]!r}, expected 4 — the new root's size is the sum "
            "of both trees"
        )


def _test_by_size_at_roots() -> None:
    uf = _new(5)
    uf.union(0, 1)
    uf.union(0, 2)          # group A = {0, 1, 2}, size 3
    uf.union(3, 4)          # group B = {3, 4}, size 2
    r_a = _find(uf, 0)
    r_b = _find(uf, 3)
    leaf = next(v for v in (0, 1, 2) if v != r_a)
    uf.union(leaf, r_b)
    root = _find(uf, 4)
    assert root == r_a, (
        f"A = {{0, 1, 2}} (root {r_a}, size 3), B = {{3, 4}} (root {r_b}, "
        f"size 2). After union({leaf}, {r_b}) the root is {root!r}, expected "
        f"{r_a}: the bigger group A must stay on top. {leaf} is not a root, "
        f"and size[{leaf}] is stale. Compare the sizes of the ROOTS"
    )
    assert uf.size[r_a] == 5, (
        f"after merging A and B: size[{r_a}] is {uf.size[r_a]!r}, expected 5"
    )


def _test_same_group_noop() -> None:
    uf = _new(3)
    uf.union(0, 1)
    r = _find(uf, 0)
    uf.union(1, 0)
    uf.union(0, 1)
    assert uf.size[r] == 2, (
        f"union(0, 1), then union(1, 0) and union(0, 1) again: size[{r}] is "
        f"{uf.size[r]!r}, expected 2. When a and b already share a root "
        "there is nothing to merge, and size must not grow"
    )
    assert uf.parent[r] == r, (
        f"after repeating unions inside one group, parent[{r}] is "
        f"{uf.parent[r]!r} — the root must still be its own parent"
    )


def _test_path_compression() -> None:
    uf = _new(5)
    uf.parent = [1, 2, 3, 4, 4]       # a chain: 0 -> 1 -> 2 -> 3 -> 4 (root)
    uf.size = [1, 1, 1, 1, 5]
    got = _find(uf, 0)
    assert got == 4, (
        f"find(0) on the chain 0 -> 1 -> 2 -> 3 -> 4: got {got!r}, expected 4"
    )
    assert uf.parent == [4, 4, 4, 4, 4], (
        f"after find(0) on the chain 0 -> 1 -> 2 -> 3 -> 4, parent is "
        f"{uf.parent!r}, expected [4, 4, 4, 4, 4]. Path compression points "
        "EVERY vertex on the path (0, 1, 2 and 3) straight at the root, not "
        "only the vertex you started from"
    )


def _test_big_chain() -> None:
    # The lesson's chain stream: connect 0 with 1, then 2, then 3, ...
    n = 100_000
    uf = _new(n)
    for k in range(1, n):
        uf.union(0, k)
    for k in range(0, n, 7):
        assert _connected(uf, k, n - 1) is True, (
            f"after union(0, k) for every k: connected({k}, {n - 1}) is False"
        )
    root = _find(uf, 0)
    assert uf.size[root] == n, (
        f"after union(0, k) for every k: size[{root}] is {uf.size[root]!r}, "
        f"expected {n}"
    )


def _check(name: str, fn) -> bool | None:
    try:
        _with_time_limit(5, fn)
    except NotImplementedError:
        print(f"  ..  {name} — not attempted yet")
        return None
    except _Timeout:
        print(
            f"  FAIL  {name}: never finished (5s limit). With both fixes "
            "this is ~200 000 nearly-constant steps. Is a find walking a "
            "long chain again and again? Check union by size, and that find "
            "compresses the path it walked"
        )
        return False
    except RecursionError:
        print(
            f"  FAIL  {name}: RecursionError — find went 1000+ levels deep, "
            "so your trees are chains. Union by size keeps every depth at "
            "most lg n (about 17 at 100 000)"
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
        digest = hashlib.sha256(got.encode("utf-8")).hexdigest()
        assert digest == _K_DIGESTS[key], f"you said {got!r}. Hint: {_K_HINTS[key]}"
    return test


TESTS = [
    ("F1 — __init__: everyone is their own root", _test_init),
    ("F2 — find on a fresh structure", _test_find_fresh),
    ("F3 — union + connected", _test_union_connected),
    ("F4 — union links roots, not vertices", _test_link_roots),
    ("F5 — union by size, either argument order", _test_by_size_order),
    ("F6 — union by size compares ROOT sizes", _test_by_size_at_roots),
    ("F7 — union inside one group changes nothing", _test_same_group_noop),
    ("F8 — find compresses the whole path", _test_path_compression),
    ("F9 — 100 000-vertex chain stream (both fixes)", _test_big_chain),
] + [(_K_LABELS[key], _make_knowledge_test(key)) for key in _K_DIGESTS]

if __name__ == "__main__":
    print("\nUnion-find drill — L7\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green — you can merge groups in nearly constant time and")
        print("say why both fixes matter. Tell your teacher: P10-P12 are next")
        print("— the assembly is yours.\n")
    else:
        print("\nReport this output to your teacher, reds included.\n")
