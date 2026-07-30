"""
Lesson 4 drill — choosing the key, choosing the direction.

HOW TO USE THIS FILE
    1. Part A: fill in COSTS. Per phase, then which phase dominates. On paper.
    2. Part B: implement top_k_slowest().
    3. Part C: fill in PREDICTIONS *before* you run anything.
    4. Run it, from the repo root:
           python3.14 learning/heap-priority-queue/lessons/0004-topk-drill.py
    5. Immediate pass/fail on every item.

Part A is the one that matters. On P2 you gave the right total with the wrong
story underneath — heapify blamed for a log factor it does not have. The cure is
mechanical: write each phase down separately, then compare. Never one number.

There are no solutions in this file, and your teacher will not give you one.
If you are stuck, ask for a hint — you will get the smallest hint that unblocks you.
"""

import heapq
import itertools

# ----------------------------------------------------------------------------
# PART A — cost accounting, one phase at a time
# ----------------------------------------------------------------------------
#
# The task: given `requests`, a list of n (endpoint, ms) pairs, return the k
# slowest. Three strategies. For each one, cost the two phases separately.
#
# Throughout Part A, "small k" means these concrete numbers, so nothing is
# ambiguous:                     n = 1_000_000        k = 10
#
#   sort_all     p1: sort all n by ms
#                p2: take the last k of the sorted list
#
#   heapify_all  p1: negate all n into a list and heapify it (a max-heap)
#                p2: pop k times
#
#   bounded      p1: one pass over all n, keeping a heap that never holds
#                    more than k entries
#                p2: drain the k survivors out of that heap
#
# Write each phase cost as one of these labels, spelled exactly:
#
#   O(1)  O(k)  O(n)  O(log k)  O(log n)  O(k log k)  O(k log n)  O(n log k)  O(n log n)
#
# For each "_dominant" key, answer "p1" or "p2" — which phase's cost survives
# when you add the two and drop the smaller term, at n = 1e6 and k = 10.
#
# For the last two keys, answer with a strategy name: "sort_all",
# "heapify_all" or "bounded".
#
# Leave a value as None to skip it.

COSTS: dict[str, str | None] = {
    "sort_all_p1": "O(n log n)",
    "sort_all_p2": "O(k)",
    "sort_all_dominant": "p1",

    "heapify_all_p1": "O(n)",
    "heapify_all_p2": "O(k log n)",
    "heapify_all_dominant": "p1",

    "bounded_p1": "O(n log k)",
    "bounded_p2": "O(k log k)",
    "bounded_dominant": "p1",

    # Add each strategy's two phases and compare the totals, at n = 1e6, k = 10.
    "best_time_small_k": "heapify_all",
    # Now ignore time. How much memory does each one need *beyond* the input?
    "best_memory_small_k": "bounded",
}


# ----------------------------------------------------------------------------
# PART B — the bounded heap, with a key you have to choose
# ----------------------------------------------------------------------------

def top_k_slowest(requests: list[tuple[str, int]], k: int) -> list[tuple[str, int]]:
    """Return the k slowest requests, ascending by ms.

    `requests` is in arrival order. Return the k pairs with the largest ms,
    ordered ascending by ms — the order a heap hands you for free, so you need
    no sort at the end.

    Rules:
      - Your heap must NEVER hold more than k entries. The harness watches.
      - Use `import heapq` and qualified calls (`heapq.heappush(...)`), not
        `from heapq import heappush` — the size check cannot see unqualified ones.
      - Banned: sorted(), .sort(), reverse, [::-1], nlargest, nsmallest.
      - k <= 0 returns []. k >= len(requests) returns everything, still ascending.

    Ties: if a later request has exactly the same ms as one already held, the
    earlier arrival keeps its slot. Getting this right is about *what you
    compare*, not about which heapq function you call.
    """
    pq = []
    counter = itertools.count()

    for request, ms in requests:
        item = (ms, -next(counter), request)
        if len(pq) < k:
            heapq.heappush(pq, item)
        else:
            heapq.heappushpop(pq, item)
    res = []
    while pq:
        ms, _, request = heapq.heappop(pq)
        res.append((request, ms))

    return res


# ----------------------------------------------------------------------------
# PART C — predict nlargest / nsmallest
# ----------------------------------------------------------------------------
#
# LATENCIES = [("a", 5), ("b", 5), ("c", 1), ("d", 9), ("e", 5)]
# ms = lambda r: r[1]
#
#   C1:  heapq.nlargest(3, LATENCIES, key=ms)          → ?
#   C2:  heapq.nsmallest(2, LATENCIES, key=ms)         → ?
#   C3:  heapq.nlargest(9, [("x", 1), ("y", 2)], key=ms)  → ?   (only 2 items!)
#
# Three ties at ms=5 in C1. Something has to decide their order. Predict what,
# then check the docs line for nlargest -- or sections 5 and 6 of the lesson --
# if you want to reason it out rather than guess.
#
# C3 is not a trick question: read the contract in section 5 and note what
# happens when n is larger than the input.
#
# Write full literals, e.g. [("a", 5), ("b", 5)].

PREDICTIONS: dict[str, list[tuple[str, int]] | None] = {
    "C1": [('d', 9), ('a', 5), ('b', 5)],
    "C2": [('c', 1), ('a', 5)],
    "C3": [('y', 2), ('x', 1)],
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

import inspect
import random

LATENCIES = [("a", 5), ("b", 5), ("c", 1), ("d", 9), ("e", 5)]
_ms = lambda r: r[1]

_LABELS = {"O(1)", "O(k)", "O(n)", "O(log k)", "O(log n)",
           "O(k log k)", "O(k log n)", "O(n log k)", "O(n log n)"}

_COST_ANSWERS = {
    "sort_all_p1": "O(n log n)",
    "sort_all_p2": "O(k)",
    "sort_all_dominant": "p1",
    "heapify_all_p1": "O(n)",
    "heapify_all_p2": "O(k log n)",
    "heapify_all_dominant": "p1",
    "bounded_p1": "O(n log k)",
    "bounded_p2": "O(k log k)",
    "bounded_dominant": "p1",
    "best_time_small_k": "heapify_all",
    "best_memory_small_k": "bounded",
}

_COST_HINTS = {
    "sort_all_p1": "Sorting n items by a key is the standard comparison-sort bound.",
    "sort_all_p2": "Slicing k items off the end copies k items. Nothing is compared.",
    "sort_all_dominant": "1e6 log(1e6) against 10. Not close.",
    "heapify_all_p1": "You proved this at the end of Lesson 3 — and then blamed it for a log factor on P2. It has none.",
    "heapify_all_p2": "k pops, and the heap still holds all n items during them, so each sift walks a tree of height log n.",
    "heapify_all_dominant": "1e6 against 10 x 20. The build swamps the pops — and that is what makes this strategy O(n).",
    "bounded_p1": "n arrivals, each one sifting a heap capped at k. What is the height of a heap of k items?",
    "bounded_p2": "k pops from a heap of size k, shrinking as you go.",
    "bounded_dominant": "1e6 x 3.3 against 10 x 3.3.",
    "best_time_small_k": "Add each strategy's phases first: O(n log n)+O(k), O(n)+O(k log n), O(n log k)+O(k log k). At k=10 one of those totals collapses to something strictly smaller than the other two.",
    "best_memory_small_k": "Which one never holds more than k entries at once?",
}

_PRED_LABELS = {"C1": "nlargest(3) with three ties",
                "C2": "nsmallest(2)",
                "C3": "nlargest(9) over 2 items"}


def _check(name, fn):
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


def _make_cost_test(key):
    def test():
        got = COSTS.get(key)
        if got is None:
            raise NotImplementedError
        want = _COST_ANSWERS[key]
        if key.endswith("_dominant"):
            assert got in ("p1", "p2"), f"{got!r} is not 'p1' or 'p2'"
        elif key.startswith("best_"):
            assert got in ("sort_all", "heapify_all", "bounded"), \
                f"{got!r} is not a strategy name"
        else:
            assert got in _LABELS, \
                f"{got!r} is not one of the allowed labels — check the spelling"
        assert got == want, f"you said {got!r}. Hint: {_COST_HINTS[key]}"
    return test


def _make_prediction_test(key):
    def test():
        got = PREDICTIONS.get(key)
        if got is None:
            raise NotImplementedError
        want = _ACTUAL_PREDICTIONS[key]
        assert not isinstance(got, str), (
            f"{got!r} is a string, not a list — drop the outer quotes. "
            "Write the literal itself: [(\"a\", 5), (\"b\", 5)]"
        )
        assert [tuple(x) for x in got] == want, f"you predicted {got!r}, heapq produced {want!r}"
    return test


def _actual_predictions():
    return {
        "C1": heapq.nlargest(3, LATENCIES, key=_ms),
        "C2": heapq.nsmallest(2, LATENCIES, key=_ms),
        "C3": heapq.nlargest(9, [("x", 1), ("y", 2)], key=_ms),
    }


def _source_of(fn) -> str:
    """Source of fn with its docstring cut out — the docstring names the banned
    constructs, and we are checking your code, not the instructions.

    Cuts the first triple-quoted block textually rather than via fn.__doc__:
    since Python 3.13 the compiler dedents docstrings, so __doc__ no longer
    matches the source text and replace() would silently strip nothing.
    """
    try:
        src = inspect.getsource(fn)
    except OSError:
        return ""
    for quote in ('"""', "'''"):
        start = src.find(quote)
        if start == -1:
            continue
        end = src.find(quote, start + 3)
        if end != -1:
            return src[:start] + src[end + 3:]
    return src


def _oracle(requests, k):
    """Only ever called with distinct ms values, so the answer is unambiguous."""
    if k <= 0:
        return []
    return sorted(requests, key=_ms)[-k:]


def _run_watched(requests, k):
    """Call top_k_slowest with heapq instrumented, returning (result, max_heap_len)."""
    sizes: list[int] = []
    names = ("heappush", "heappop", "heappushpop", "heapreplace", "heapify")
    originals = {n: getattr(heapq, n) for n in names}

    def wrap(real):
        def wrapper(h, *a, **kw):
            out = real(h, *a, **kw)
            try:
                sizes.append(len(h))
            except TypeError:
                pass
            return out
        return wrapper

    for n, f in originals.items():
        setattr(heapq, n, wrap(f))
    try:
        result = top_k_slowest(requests, k)
    finally:
        for n, f in originals.items():
            setattr(heapq, n, f)
    return result, (max(sizes) if sizes else 0)


def test_top_k_plays_by_the_rules():
    top_k_slowest([], 1)  # signals "not attempted" instead of a confusing FAIL
    src = _source_of(top_k_slowest)
    assert "heapq" in src, "top_k_slowest() must actually use heapq"
    for banned in ("sorted(", ".sort(", "reverse", "[::-1]", "nlargest", "nsmallest"):
        assert banned not in src, f"must not use {banned!r} — the point is the bounded heap"
    assert "from heapq import" not in src, \
        "use qualified heapq.* calls — the size check cannot see unqualified ones"


def test_top_k_is_correct():
    cases = [
        ([("a", 3), ("b", 1), ("c", 2)], 2),
        ([("a", 3), ("b", 1), ("c", 2)], 1),
        ([("solo", 7)], 1),
        ([("a", 1), ("b", 2), ("c", 3), ("d", 4)], 4),
        ([("a", 1), ("b", 2)], 5),
    ]
    for requests, k in cases:
        got = top_k_slowest(list(requests), k)
        want = _oracle(requests, k)
        assert [tuple(x) for x in got] == want, f"top_k_slowest({requests}, {k}) gave {got}, expected {want}"


def test_top_k_handles_the_edges():
    assert top_k_slowest([], 3) == [], "no requests → []"
    assert top_k_slowest([("a", 1)], 0) == [], "k = 0 → []"
    assert top_k_slowest([("a", 1)], -2) == [], "k < 0 → []"


def test_top_k_never_exceeds_k():
    rng = random.Random(4)
    for _ in range(60):
        n = rng.randint(1, 40)
        k = rng.randint(1, 12)
        requests = [(f"e{i}", v) for i, v in enumerate(rng.sample(range(1000), n))]
        _, peak = _run_watched(list(requests), k)
        assert peak <= k, (
            f"your heap grew to {peak} entries with k={k} (n={n}). "
            "A bounded heap must evict as it goes, not collect first."
        )


def test_top_k_keeps_the_earlier_arrival_on_a_tie():
    got = top_k_slowest([("a", 10), ("b", 10), ("c", 10)], 2)
    assert {e for e, _ in got} == {"a", "b"}, \
        f"expected the two earliest arrivals {{'a', 'b'}}, got {sorted(e for e, _ in got)}"

    got = top_k_slowest([("a", 5), ("b", 10), ("c", 10), ("d", 10)], 2)
    assert {e for e, _ in got} == {"b", "c"}, \
        f"expected {{'b', 'c'}}, got {sorted(e for e, _ in got)}"

    # aaa arrives first and must survive, even though 'zzz' > 'aaa' as a string.
    got = top_k_slowest([("aaa", 8), ("zzz", 8)], 1)
    assert {e for e, _ in got} == {"aaa"}, \
        f"expected {{'aaa'}} — compare the ms, not the whole tuple; got {sorted(e for e, _ in got)}"


def test_top_k_survives_the_stress_test():
    rng = random.Random(99)
    for _ in range(300):
        n = rng.randint(0, 50)
        k = rng.randint(0, 20)
        requests = [(f"e{i}", v) for i, v in enumerate(rng.sample(range(10_000), n))]
        got = top_k_slowest(list(requests), k)
        want = _oracle(requests, k)
        assert [tuple(x) for x in got] == want, f"top_k_slowest({requests}, {k}) gave {got}, expected {want}"


_ACTUAL_PREDICTIONS = _actual_predictions()

TESTS = (
    [(f"A — {key}", _make_cost_test(key)) for key in _COST_ANSWERS]
    + [
        ("B — top_k_slowest() plays by the rules", test_top_k_plays_by_the_rules),
        ("B — top_k_slowest() is correct", test_top_k_is_correct),
        ("B — top_k_slowest() handles the edges", test_top_k_handles_the_edges),
        ("B — the heap never exceeds k", test_top_k_never_exceeds_k),
        ("B — ties keep the earlier arrival", test_top_k_keeps_the_earlier_arrival_on_a_tie),
        ("B — 300 random cases against an oracle", test_top_k_survives_the_stress_test),
    ]
    + [(f"C — {_PRED_LABELS[key]}", _make_prediction_test(key)) for key in _PRED_LABELS]
)

if __name__ == "__main__":
    print("\ntop-k drill — Lesson 4\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green. Part A says heapify-all is the fastest of the three for")
        print("small k — yet the bounded heap is the one you will reach for in an")
        print("interview. Ask your teacher why that is not a contradiction.\n")
    else:
        print("\nKeep going. Ask your teacher for a hint if you are stuck.\n")
