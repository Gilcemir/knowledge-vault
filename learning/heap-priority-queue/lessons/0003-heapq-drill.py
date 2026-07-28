"""
Lesson 3 drill — heapq fluency.

HOW TO USE THIS FILE
    1. Part A: fill in the PREDICTIONS dict *from your head*, before running anything.
    2. Parts B and C: implement the two functions.
    3. Run it, from the repo root:
           python3 learning/heap-priority-queue/lessons/0003-heapq-drill.py
    4. The harness gives you immediate pass/fail feedback on every item.

Part A is the important one. Predicting the array before you run the code is
where the learning happens — running first and back-filling the answers teaches
you nothing. You will get some wrong. That is the point.

There are no solutions in this file, and your teacher will not give you one.
If you are stuck, ask for a hint — you will get the smallest hint that unblocks you.
"""

import heapq
import itertools
from typing import Any


# ----------------------------------------------------------------------------
# PART A — predict the internal array
# ----------------------------------------------------------------------------
#
# Four scenarios. Work each one out on paper using the sift rules from Lesson 2,
# then write the answer as a literal below. Leave a value as None to skip it.
#
#   Scenario A:  h = []
#                for x in [18, 23, 3, 19, 2]:
#                    heapq.heappush(h, x)
#                # what is h?
#
#   Scenario B:  h = [18, 23, 3, 19, 2]
#                heapq.heapify(h)
#                # what is h?   (same input as A — same answer?)
#
#   Scenario C:  h = [2, 7, 5]
#                out = heapq.heapreplace(h, 1)
#                # what is out, and what is h?
#
#   Scenario D:  h = [2, 7, 5]
#                out = heapq.heappushpop(h, 1)
#                # what is out, and what is h?

PREDICTIONS: dict[str, Any] = {
    "A_heap": [2, 3, 18, 23, 19],           # list[int]
    "B_heap": [2, 18, 3, 19, 23],           # list[int]
    "C_returned": 2,       # int
    "C_heap": [1, 7, 5],           # list[int]
    "D_returned": 1,       # int
    "D_heap": [2, 7, 5],           # list[int]
}


# ----------------------------------------------------------------------------
# PART B — the max-heap trick
# ----------------------------------------------------------------------------

def descending(nums: list[int]) -> list[int]:
    h = [-x for x in nums]
    heapq.heapify(h)
    r = []
    while h:
        r.append(-heapq.heappop(h))

    return r


# ----------------------------------------------------------------------------
# PART C — tuple priorities that survive a tie
# ----------------------------------------------------------------------------

class Task:
    """A payload with no ordering defined. Comparing two Tasks raises TypeError."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Task({self.name!r})"


def dispatch(tasks: list[tuple[int, Task]]) -> list[str]:
    """Return the task *names* in ascending priority order.

    Ties (equal priority) come out in the order they appear in `tasks`: the
    monotonic counter in slot 2 is unique per task, so tuple comparison always
    resolves there and never reaches the Task payload — which has no ordering
    and would raise TypeError if compared.
    """
    counter = itertools.count()
    pq: list[tuple[int, int, Task]] = []
    for priority, task in tasks:
        heapq.heappush(pq, (priority, next(counter), task))

    res: list[str] = []
    while pq:
        _, _, task = heapq.heappop(pq)
        res.append(task.name)

    return res


# ----------------------------------------------------------------------------
# TEST HARNESS — do not edit below this line.
# ----------------------------------------------------------------------------

import inspect
import random


def _check(name, fn):
    try:
        fn()
    except NotImplementedError:
        print(f"  ..  {name} — not implemented yet")
        return None
    except AssertionError as e:
        print(f"  FAIL  {name}: {e}")
        return False
    except Exception as e:
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")
        return False
    print(f"  ok    {name}")
    return True


def _actual_scenarios() -> dict[str, Any]:
    a: list[int] = []
    for x in [18, 23, 3, 19, 2]:
        heapq.heappush(a, x)

    b = [18, 23, 3, 19, 2]
    heapq.heapify(b)

    c = [2, 7, 5]
    c_out = heapq.heapreplace(c, 1)

    d = [2, 7, 5]
    d_out = heapq.heappushpop(d, 1)

    return {
        "A_heap": a,
        "B_heap": b,
        "C_returned": c_out,
        "C_heap": c,
        "D_returned": d_out,
        "D_heap": d,
    }


def _make_prediction_test(key, want):
    def test():
        got = PREDICTIONS.get(key)
        if got is None:
            raise NotImplementedError
        assert got == want, f"you predicted {got}, heapq actually produced {want}"
    return test


def _source_of(fn) -> str:
    """Source of fn with its docstring stripped — the docstring names the banned
    constructs, and we are checking your code, not the instructions."""
    try:
        src = inspect.getsource(fn)
    except OSError:
        return ""
    doc = fn.__doc__
    if doc:
        src = src.replace(doc, "")
    return src


def test_descending_uses_a_heap():
    descending([])  # signals "not implemented yet" instead of a confusing FAIL
    src = _source_of(descending)
    assert "heapq" in src, "descending() must actually use heapq"
    for banned in ("sorted(", ".sort(", "reverse", "[::-1]", "max(", "nlargest"):
        assert banned not in src, f"descending() must not use {banned!r} — the point is the heap"


def test_descending_is_correct():
    cases = [
        [],
        [42],
        [3, 1, 2],
        [5, 5, 5, 1],
        [-7, 0, -7, 12, 3],
    ]
    for nums in cases:
        got = descending(list(nums))
        want = sorted(nums, reverse=True)
        assert got == want, f"descending({nums}) gave {got}, expected {want}"

    rng = random.Random(11)
    for _ in range(200):
        nums = [rng.randint(-40, 40) for _ in range(rng.randint(0, 30))]
        got = descending(list(nums))
        want = sorted(nums, reverse=True)
        assert got == want, f"descending({nums}) gave {got}, expected {want}"


def test_dispatch_orders_by_priority():
    tasks = [(3, Task("c")), (1, Task("a")), (2, Task("b"))]
    got = dispatch(tasks)
    assert got == ["a", "b", "c"], f"expected ['a', 'b', 'c'], got {got}"


def test_dispatch_breaks_ties_by_arrival():
    tasks = [
        (2, Task("second")),
        (1, Task("first")),
        (2, Task("third")),
        (2, Task("fourth")),
        (1, Task("also-first")),
    ]
    got = dispatch(tasks)
    want = ["first", "also-first", "second", "third", "fourth"]
    assert got == want, f"expected {want}, got {got}"


def test_dispatch_never_compares_tasks():
    # Every priority is identical, so any comparison that reaches the payload
    # will raise. A correct tie-breaker makes that impossible.
    tasks = [(0, Task(f"t{i}")) for i in range(50)]
    got = dispatch(tasks)
    want = [f"t{i}" for i in range(50)]
    assert got == want, f"all-equal priorities must stay in arrival order; got {got}"


def test_dispatch_handles_edges():
    assert dispatch([]) == [], "an empty task list should dispatch to []"
    assert dispatch([(9, Task("solo"))]) == ["solo"], "a single task should come straight back"
    src = _source_of(dispatch)
    assert "heapq" in src, "dispatch() must actually use heapq"
    for banned in ("sorted(", ".sort("):
        assert banned not in src, f"dispatch() must not use {banned!r}"


_ACTUAL = _actual_scenarios()

TESTS = [
    ("A — array after five pushes", _make_prediction_test("A_heap", _ACTUAL["A_heap"])),
    ("B — array after heapify", _make_prediction_test("B_heap", _ACTUAL["B_heap"])),
    ("C — heapreplace return value", _make_prediction_test("C_returned", _ACTUAL["C_returned"])),
    ("C — array after heapreplace", _make_prediction_test("C_heap", _ACTUAL["C_heap"])),
    ("D — heappushpop return value", _make_prediction_test("D_returned", _ACTUAL["D_returned"])),
    ("D — array after heappushpop", _make_prediction_test("D_heap", _ACTUAL["D_heap"])),
    ("descending() leans on the heap", test_descending_uses_a_heap),
    ("descending() is correct", test_descending_is_correct),
    ("dispatch() orders by priority", test_dispatch_orders_by_priority),
    ("dispatch() breaks ties by arrival", test_dispatch_breaks_ties_by_arrival),
    ("dispatch() never compares tasks", test_dispatch_never_compares_tasks),
    ("dispatch() handles the edges", test_dispatch_handles_edges),
]

if __name__ == "__main__":
    print("\nheapq fluency drill — Lesson 3\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green. Scenarios A and B started from the same five numbers.")
        print("Did they end up as the same array? Ask your teacher why.\n")
    else:
        print("\nKeep going. Ask your teacher for a hint if you are stuck.\n")
