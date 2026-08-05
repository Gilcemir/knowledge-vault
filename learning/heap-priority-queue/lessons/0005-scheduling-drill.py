"""
Lesson 5 drill — greedy under an eligibility gate.

HOW TO USE THIS FILE
    1. Part A: fill in BOUNDS. On paper first, before you touch Part B.
    2. Part B: implement processing_order().
    3. Part C: fill in PREDICTIONS *before* you run anything.
    4. Run it, from the repo root:
           python3.14 learning/heap-priority-queue/lessons/0005-scheduling-drill.py
    5. Immediate pass/fail on every item.

Part A is not bookkeeping this time — it decides Part B. One test feeds you
arrival times in the billions with five orders in total. If your loop advances
the clock one tick at a time it will not finish, and no amount of correct
heap code will save it. Name the shrinking quantity first and the shape of
the loop follows.

There are no solutions in this file, and your teacher will not give you one.
If you are stuck, ask for a hint — you will get the smallest hint that unblocks
you. If a hint is unclear, say so and ask for the answer instead.
"""

import heapq
from collections import deque


# ----------------------------------------------------------------------------
# PART A — bounding a loop whose length depends on the data
# ----------------------------------------------------------------------------
#
# The loop under discussion is the one from section 4 of the lesson:
#
#     while work remains:
#         release everything now eligible into the heap
#         if the heap is empty: move the clock forward
#         pop the best, handle it, advance the clock by one tick
#
# Notation, so nothing is ambiguous:
#     n  = the number of orders
#     T  = the largest arrival time in the input  (a number that arrives with
#          the data — it has no relationship to n at all)
#
# "shrinking_quantity": which quantity shrinks by at least 1 on EVERY
# iteration, once the clock jumps straight to the next arrival? Answer with
# one of these strings, spelled exactly:
#
#     "ticks elapsed"
#     "orders already processed"
#     "orders not yet processed"
#     "orders not yet arrived"
#
# "iterations_jump" / "iterations_tick": how many times does the loop body run,
# for each clock policy? Answer with one of: "n", "2n", "T", "n log n"
#
# The three "_cost" keys take one of these labels, spelled exactly:
#
#     O(1)  O(n)  O(log n)  O(n log n)  O(T)  O(n * T)
#
# "dominant": which phase's cost survives in the total? One of:
#     "prepare", "loop", "output", "tie"
#
# Leave a value as None to skip it.

BOUNDS: dict[str, str | None] = {
    "shrinking_quantity": "orders not yet processed",
    "iterations_jump": "n",
    "iterations_tick": "T",

    # Phases of the clock-jumping version:
    #   prepare — put the orders in arrival order before the loop starts
    #   loop    — the whole loop, all iterations together, pushes and pops included
    #   output  — assembling the list of names you return
    "prepare_cost": "O(n log n)",
    "loop_cost": "O(n log n)",
    "output_cost": "O(n)",
    "dominant": "tie",
}


# ----------------------------------------------------------------------------
# PART B — the two containers
# ----------------------------------------------------------------------------

def processing_order(orders: list[tuple[int, int, str]]) -> list[str]:
    """Return the names of the orders in the order a single worker handles them.

    Each order is a tuple `(arrival, priority, name)`. One worker handles one
    order per tick, and every order takes exactly one tick. The worker is idle
    and waiting at tick 0.

    The policy, at every step:
      - Consider only orders that have arrived (arrival <= now) and are not
        yet handled.
      - Handle the one with the HIGHEST priority.
      - If nothing has arrived yet, the worker waits until something does.

    Ties, in this order: higher priority wins; then earlier arrival wins; then
    the smaller name wins (plain string comparison). Getting this right is
    about what you compare, not which heapq function you call.

    Rules:
      - Your heap must hold only orders that are eligible right now. The
        harness does not measure this directly — it measures its consequences.
      - Use `import heapq` and qualified calls (`heapq.heappop(...)`), not
        `from heapq import heappop` — the instrumentation cannot see
        unqualified ones.
      - Sorting the input by arrival up front is allowed and expected.
      - One test uses arrival times in the billions. Part A tells you what
        that test is checking.
      - Empty input returns [].

    Not required: handling two orders with the same name.
    """
    res = []
    now = 0
    pq = []
    orders.sort(key= lambda o: o[0])
    queue = deque(orders)
    while queue or pq:
        while queue and queue[0][0] <= now:
            arr, pr, name = queue.popleft()
            heapq.heappush(pq, (-pr, arr, name))
        if not pq:
            now = queue[0][0]
            continue
        _, _ , name = heapq.heappop(pq)
        res.append(name)
        now += 1

    return res


# ----------------------------------------------------------------------------
# PART C — predict the trace
# ----------------------------------------------------------------------------
#
# Write down what processing_order() returns for each of these, BEFORE running.
# Each is small enough to trace on paper in under a minute.
#
#   C1:  [(0, 5, "a"), (0, 5, "b"), (0, 9, "c")]
#   C2:  [(0, 1, "a"), (10, 9, "b"), (10, 1, "c")]
#   C3:  [(0, 1, "a"), (0, 1, "b"), (1, 9, "c")]
#
# C1 has a tie that the priority alone cannot settle.
# C2 has a gap where the worker has nothing to do.
# C3 is the one worth thinking about: something better shows up while the
# worker is busy. Trace it tick by tick and do not guess.
#
# Write real lists of real strings, e.g. ["a", "b", "c"] — not "[a, b, c]".

PREDICTIONS: dict[str, list[str] | None] = {
    "C1": ["c", "a", "b"],
    "C2": ["a", "b", "c"],
    "C3": ["a", "c", "b"],
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

import inspect
import random
import time

_LABELS = {"O(1)", "O(n)", "O(log n)", "O(n log n)", "O(T)", "O(n * T)"}
_QUANTITIES = {"ticks elapsed", "orders already processed",
               "orders not yet processed", "orders not yet arrived"}
_ITER_LABELS = {"n", "2n", "T", "n log n"}
_PHASES = {"prepare", "loop", "output", "tie"}

_BOUND_ANSWERS = {
    "shrinking_quantity": "orders not yet processed",
    "iterations_jump": "n",
    "iterations_tick": "T",
    "prepare_cost": "O(n log n)",
    "loop_cost": "O(n log n)",
    "output_cost": "O(n)",
    "dominant": "tie",
}

_BOUND_HINTS = {
    "shrinking_quantity": (
        "It must be a non-negative integer that drops by at least 1 every time "
        "the body runs. Ticks elapsed goes UP. A count of things already done "
        "also goes up. That leaves two counts of things not done — and only one "
        "of them changes on the iteration where the worker handles an order."
    ),
    "iterations_jump": (
        "If the clock jumps straight to the next arrival, an idle jump is "
        "followed by handling an order in the same iteration. So every "
        "iteration handles exactly one order. How many orders are there?"
    ),
    "iterations_tick": (
        "One iteration per tick, and the clock has to walk all the way to the "
        "last arrival before that order can be handled. Which of the two "
        "letters describes that number?"
    ),
    "prepare_cost": "Putting n items in arrival order, by comparison.",
    "loop_cost": (
        "Do not count per iteration and multiply. Count per ITEM: each order "
        "is pushed exactly once and popped exactly once, and each of those "
        "costs log of the heap size, which is at most n."
    ),
    "output_cost": "n names appended to a list. Nothing is compared.",
    "dominant": (
        "Compare your three phase costs. Two of them are the same, and that "
        "same value is the largest. Section 5 of the lesson says what to answer "
        "when there is not exactly one winner."
    ),
}

_PRED_INPUTS = {
    "C1": [(0, 5, "a"), (0, 5, "b"), (0, 9, "c")],
    "C2": [(0, 1, "a"), (10, 9, "b"), (10, 1, "c")],
    "C3": [(0, 1, "a"), (0, 1, "b"), (1, 9, "c")],
}

_PRED_LABELS = {
    "C1": "a tie the priority cannot settle",
    "C2": "a gap with nothing to do",
    "C3": "something better arrives mid-tick",
}


def _oracle(orders: list[tuple[int, int, str]]) -> list[str]:
    """Brute force, no heap: rescan every remaining order at every step.

    O(n^2), which is exactly why it is safe to have here.
    """
    remaining = list(orders)
    out: list[str] = []
    now = 0
    while remaining:
        arrived = [o for o in remaining if o[0] <= now]
        if not arrived:
            now = min(o[0] for o in remaining)
            continue
        # highest priority, then earliest arrival, then smallest name
        best = min(arrived, key=lambda o: (-o[1], o[0], o[2]))
        remaining.remove(best)
        out.append(best[2])
        now += 1
    return out


def _source_of(fn) -> str:
    """Source of fn with its docstring cut out — the docstring states the rules
    and would trip the checks below.

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


def _run_counted(orders):
    """Call processing_order with heapq instrumented, returning (result, counts)."""
    counts: dict[str, int] = {}
    names = ("heappush", "heappop", "heappushpop", "heapreplace", "heapify")
    originals = {n: getattr(heapq, n) for n in names}

    def wrap(name, real):
        def wrapper(*a, **kw):
            counts[name] = counts.get(name, 0) + 1
            return real(*a, **kw)
        return wrapper

    for n, f in originals.items():
        setattr(heapq, n, wrap(n, f))
    try:
        result = processing_order(orders)
    finally:
        for n, f in originals.items():
            setattr(heapq, n, f)
    return result, counts


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


def _make_bound_test(key):
    def test():
        got = BOUNDS.get(key)
        if got is None:
            raise NotImplementedError
        assert isinstance(got, str), f"{got!r} is not a string — answer with one of the labels"
        if key == "shrinking_quantity":
            allowed, what = _QUANTITIES, "one of the four quantities listed"
        elif key.startswith("iterations_"):
            allowed, what = _ITER_LABELS, "one of: n, 2n, T, n log n"
        elif key == "dominant":
            allowed, what = _PHASES, "one of: prepare, loop, output, tie"
        else:
            allowed, what = _LABELS, "one of the cost labels"
        assert got in allowed, f"{got!r} is not {what} — check the spelling"
        assert got == _BOUND_ANSWERS[key], f"you said {got!r}. Hint: {_BOUND_HINTS[key]}"
    return test


def _make_prediction_test(key):
    def test():
        got = PREDICTIONS.get(key)
        if got is None:
            raise NotImplementedError
        assert not isinstance(got, str), (
            f"{got!r} is a string, not a list — drop the outer quotes. "
            'Write the literal itself: ["a", "b", "c"]'
        )
        assert isinstance(got, list), f"{got!r} is a {type(got).__name__}, not a list"
        for item in got:
            assert isinstance(item, str), (
                f"{item!r} inside your prediction is a {type(item).__name__}, "
                "not a string — the function returns names"
            )
        want = _oracle(_PRED_INPUTS[key])
        assert got == want, f"you predicted {got!r}, the policy produces {want!r}"
    return test


def test_uses_a_heap():
    processing_order([])  # signals "not attempted" instead of a confusing FAIL
    src = _source_of(processing_order)
    assert "heapq" in src, "processing_order() must actually use heapq"
    assert "from heapq import" not in src, \
        "use qualified heapq.* calls — the instrumentation cannot see unqualified ones"
    orders = [(0, 3, "a"), (0, 1, "b"), (2, 9, "c"), (2, 2, "d")]
    _, counts = _run_counted(list(orders))
    pops = counts.get("heappop", 0) + counts.get("heappushpop", 0) + counts.get("heapreplace", 0)
    assert pops >= len(orders), (
        f"only {pops} heap pops for {len(orders)} orders — the heap has to be what "
        "selects each order, not a scan over a list"
    )


def test_empty_and_single():
    assert processing_order([]) == [], "no orders → []"
    assert processing_order([(0, 1, "solo")]) == ["solo"], "one order at tick 0"
    assert processing_order([(7, 1, "late")]) == ["late"], \
        "one order arriving at tick 7 — the worker waits, then handles it"


def test_matches_the_policy_on_small_cases():
    cases = [
        [(0, 1, "a"), (0, 2, "b")],
        [(0, 2, "a"), (0, 1, "b")],
        [(0, 1, "a"), (5, 9, "b")],
        [(3, 1, "a"), (3, 1, "b"), (3, 1, "c")],
        [(0, 1, "a"), (1, 5, "b"), (2, 9, "c")],
        [(0, 9, "a"), (0, 8, "b"), (0, 7, "c"), (0, 6, "d")],
    ]
    for orders in cases:
        got = processing_order(list(orders))
        want = _oracle(orders)
        assert got == want, f"processing_order({orders}) gave {got!r}, expected {want!r}"


def test_ties_compare_the_key_not_the_whole_tuple():
    # same priority, same arrival: the smaller name wins
    got = processing_order([(0, 5, "b"), (0, 5, "a")])
    assert got == ["a", "b"], f"expected ['a', 'b'], got {got!r}"

    # same priority, different arrival: the earlier arrival wins, and note that
    # the later one has the alphabetically smaller name
    got = processing_order([(0, 5, "z"), (0, 5, "y")])
    assert got == ["y", "z"], f"expected ['y', 'z'], got {got!r}"

    # priority must outrank arrival: 'b' arrives later but is more important
    got = processing_order([(0, 1, "a"), (0, 9, "b")])
    assert got == ["b", "a"], f"expected ['b', 'a'] — priority outranks arrival; got {got!r}"

    # arrival must outrank the name. 'x' takes tick 0. Then 'z' (arrived at 0)
    # and 'a' (arrived at 1) both wait at priority 5, and 'a' has the smaller
    # name — but 'z' has been waiting longer, so 'z' goes first.
    got = processing_order([(0, 9, "x"), (0, 5, "z"), (1, 5, "a")])
    assert got == ["x", "z", "a"], (
        f"expected ['x', 'z', 'a'], got {got!r} — on equal priority the earlier "
        "arrival wins, and the name only breaks a tie the arrival could not. "
        "Check the ORDER of the fields in the tuple you push."
    )


def test_something_better_can_arrive_mid_run():
    # 'a' is handled at tick 0 because it is all there is. 'c' arrives at tick 1
    # and outranks 'b', which was already waiting.
    orders = [(0, 1, "a"), (0, 1, "b"), (1, 9, "c")]
    got = processing_order(list(orders))
    assert got == ["a", "c", "b"], (
        f"expected ['a', 'c', 'b'], got {got!r} — orders that arrive later still "
        "compete for the next tick"
    )


def _with_time_limit(seconds: float, message: str, fn):
    """Run fn, failing with `message` if it takes longer than `seconds`.

    Uses a real timer so a loop bounded by T fails in a couple of seconds
    instead of appearing to hang. Falls back to measuring afterwards on
    platforms without SIGALRM.
    """
    try:
        import signal
        alarm = signal.SIGALRM
    except (ImportError, AttributeError):
        start = time.perf_counter()
        out = fn()
        assert time.perf_counter() - start < seconds * 10, message
        return out

    def _blow_up(signum, frame):
        raise AssertionError(message)

    previous = signal.signal(alarm, _blow_up)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        return fn()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(alarm, previous)


def test_survives_huge_arrival_times():
    orders = [(0, 1, "a"), (700_000_000, 5, "b"), (700_000_000, 9, "c"),
              (2_000_000_000, 2, "d"), (2_000_000_001, 7, "e")]
    got = _with_time_limit(
        2.0,
        "gave up after 2s on five orders. Your loop is walking the clock one tick "
        "at a time, so it runs T times instead of n times — and here T is two "
        "billion. Part A, 'iterations_tick': that is this test. The fix is in the "
        "branch that runs when the heap is empty.",
        lambda: processing_order(list(orders)),
    )
    want = _oracle(orders)
    assert got == want, f"gave {got!r}, expected {want!r}"


def test_input_is_not_sorted_by_arrival():
    # 'c' arrives at tick 0 but is listed last. If your release step walks the
    # list in the order given, it stops at 'b' (arrival 9) and never sees 'c'.
    orders = [(0, 1, "a"), (9, 1, "b"), (0, 9, "c")]
    got = processing_order(list(orders))
    assert got == ["c", "a", "b"], (
        f"expected ['c', 'a', 'b'], got {got!r} — the input is in no particular "
        "order. Your release step needs the waiting orders in arrival order "
        "before it can stop early at the first one that has not arrived."
    )


def test_stress_against_the_oracle():
    rng = random.Random(11)
    for case in range(300):
        n = rng.randint(0, 30)
        orders = []
        for i in range(n):
            orders.append((rng.randint(0, 12), rng.randint(0, 5), f"o{i:02d}"))
        got = processing_order(list(orders))
        want = _oracle(orders)
        assert got == want, f"case {case}: processing_order({orders}) gave {got!r}, expected {want!r}"


def test_stress_with_sparse_arrivals():
    """Arrivals spread far apart, so idle gaps are the norm rather than the exception."""
    rng = random.Random(23)
    for case in range(120):
        n = rng.randint(1, 12)
        orders = [(rng.randrange(0, 4000, 40), rng.randint(0, 3), f"s{i:02d}")
                  for i in range(n)]
        got = processing_order(list(orders))
        want = _oracle(orders)
        assert got == want, f"sparse case {case}: {orders} gave {got!r}, expected {want!r}"


TESTS = (
    [(f"A — {key}", _make_bound_test(key)) for key in _BOUND_ANSWERS]
    + [
        ("B — the heap is what selects", test_uses_a_heap),
        ("B — empty and single order", test_empty_and_single),
        ("B — matches the policy on small cases", test_matches_the_policy_on_small_cases),
        ("B — ties compare the key, not the tuple", test_ties_compare_the_key_not_the_whole_tuple),
        ("B — a better order can arrive mid-run", test_something_better_can_arrive_mid_run),
        ("B — the input is not sorted by arrival", test_input_is_not_sorted_by_arrival),
        ("B — survives arrival times in the billions", test_survives_huge_arrival_times),
        ("B — 300 random cases against an oracle", test_stress_against_the_oracle),
        ("B — 120 sparse-arrival cases", test_stress_with_sparse_arrivals),
    ]
    + [(f"C — {_PRED_LABELS[key]}", _make_prediction_test(key)) for key in _PRED_LABELS]
)

if __name__ == "__main__":
    print("\nscheduling drill — Lesson 5\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green. The gate you just handled was one-way: once an order has")
        print("arrived it stays arrived. Ask your teacher what changes when an item")
        print("becomes ineligible AGAIN every time you use it — that is the next problem.\n")
    else:
        print("\nKeep going. Ask your teacher for a hint if you are stuck.\n")
