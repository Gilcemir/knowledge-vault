"""
Lesson 6 drill — the heap of cursors: merging k sorted sources.

HOW TO USE THIS FILE
    1. Part A: fill in BOUNDS. On paper first, before you touch Part B.
    2. Part B: implement merge_logs(), then first_r().
    3. Part C: fill in PREDICTIONS *before* you run anything.
    4. Run it, from the repo root:
           python3.14 learning/heap-priority-queue/lessons/0006-merge-drill.py
    5. Immediate pass/fail on every item.

The heap in this drill never owns the data. The data lives in lists owned by
a dict; the heap holds POSITIONS into them. Part A's first two answers are
the design; if you have those, Part B is short.

There are no solutions in this file, and your teacher will not give you one.
If you are stuck, ask for a hint — you will get the smallest hint that unblocks
you. If a hint is unclear, say so and ask for the answer instead.
"""

import heapq


# ----------------------------------------------------------------------------
# PART A — the frontier, and what the composition buys
# ----------------------------------------------------------------------------
#
# Notation, so nothing collides (three letters, three different things):
#     k  = the number of sources (services)
#     N  = the TOTAL number of records across all sources
#     r  = the number of records requested by the early-stop variant
#
# N has no relationship to heapq's `n` parameter, nor to the cooldown from
# the last problem. Spell the letters out before writing any cost.
#
# "frontier": mid-merge, what does the heap hold? One of these, spelled exactly:
#
#     "one head per unfinished source"
#     "one record per finished source"
#     "every record of every source"
#     "the r smallest records overall"
#
# "heap_size": what bounds the size of the heap during the whole merge?
# One of: "k", "r", "N", "log N"
#
# The "_cost" keys take one of these labels, spelled exactly:
#
#     O(1)  O(k)  O(N)  O(k log N)  O(N log k)  O(N log N)  O(k + r log k)
#
# Phases of the full merge (assume the seed uses heapify):
#     seed    — put the first record of each non-empty source into the heap
#     loop    — the whole merge loop, all pushes and pops included
#     output  — assembling the merged list you return
#
# "dominant": which phase's cost survives in the total? One of:
#     "seed", "loop", "output", "tie"
#
# "concat_sort_cost": the baseline you are beating — dump all N records into
# one list and comparison-sort it, ignoring that the pieces are sorted.
#
# "first_r_cost": seed the heap, then stop as soon as r records are out.
#
# Leave a value as None to skip it.

BOUNDS: dict[str, str | None] = {
    "frontier": None,
    "heap_size": None,

    "concat_sort_cost": None,
    "seed_cost": None,
    "loop_cost": None,
    "output_cost": None,
    "dominant": None,

    "first_r_cost": None,
}


# ----------------------------------------------------------------------------
# PART B — the merge
# ----------------------------------------------------------------------------

def merge_logs(services: dict[str, list[dict]]) -> list[dict]:
    """Merge every service's log into one timeline.

    `services` maps a service name to its log: a list of records, each a dict
    with at least the keys "t" (an int tick) and "msg" (a string). Within one
    service the records are already in non-decreasing "t" order — that is a
    given of the input, not something you must arrange.

    Return one list containing every record (the dicts themselves), ordered by:
      1. smaller "t" first;
      2. on a "t" tie across services, the smaller service name first;
      3. within one service, original order preserved.

    Rules:
      - Use `import heapq` and qualified calls (`heapq.heappop(...)`), not
        `from heapq import heappop` — the instrumentation cannot see
        unqualified ones.
      - The heap may hold at most ONE entry per service at any moment. The
        harness measures the heap's size while your code runs.
      - Re-arranging the data wholesale is off the table: the pieces already
        come in order, and beating the do-it-all-again baseline is the entire
        point. The harness reads your source.
      - Records are dicts, and dicts cannot be compared. Whatever you push
        must settle every tie before a record would ever be reached.
      - A service's log may be empty; `services` itself may be empty.
    """
    raise NotImplementedError


def first_r(services: dict[str, list[dict]], r: int) -> list[dict]:
    """Return only the FIRST r records of the merged timeline.

    Same input contract and the same ordering rules as merge_logs(). If r is
    larger than the total number of records, return the whole merge; r == 0
    returns [].

    The one extra rule: LAZINESS. Stop as soon as you have r records. The
    harness counts your heap operations on an input with 150,000 records
    while asking for ten — one pop per record returned, plus the seed, and
    nothing beyond that.
    """
    raise NotImplementedError


# ----------------------------------------------------------------------------
# PART C — predict the trace
# ----------------------------------------------------------------------------
#
# Write down what each call returns, BEFORE running. Answer with the "msg"
# strings only, in order. Each is small enough to trace on paper.
#
#   C1: merge_logs({
#           "api": [{"t": 1, "msg": "api-1"}, {"t": 3, "msg": "api-2"}],
#           "web": [{"t": 1, "msg": "web-1"}],
#       })
#
#   C2: merge_logs({
#           "db":  [],
#           "api": [{"t": 2, "msg": "api-1"}, {"t": 2, "msg": "api-2"}],
#           "web": [{"t": 1, "msg": "web-1"}, {"t": 9, "msg": "web-2"}],
#       })
#
#   C3: first_r({
#           "a": [{"t": 1, "msg": "a-1"}, {"t": 5, "msg": "a-2"}],
#           "b": [{"t": 2, "msg": "b-1"}, {"t": 3, "msg": "b-2"}],
#       }, 3)
#
# C1 has a tie that crosses services.
# C2 has an empty source and a tie inside one service.
# C3 stops the merge while both sources still hold records.
#
# Write real lists of real strings, e.g. ["a-1", "b-1"] — not "[a-1, b-1]".

PREDICTIONS: dict[str, list[str] | None] = {
    "C1": None,
    "C2": None,
    "C3": None,
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

import inspect
import random

_FRONTIERS = {"one head per unfinished source", "one record per finished source",
              "every record of every source", "the r smallest records overall"}
_SIZES = {"k", "r", "N", "log N"}
_LABELS = {"O(1)", "O(k)", "O(N)", "O(k log N)", "O(N log k)", "O(N log N)",
           "O(k + r log k)"}
_PHASES = {"seed", "loop", "output", "tie"}

_BOUND_ANSWERS = {
    "frontier": "one head per unfinished source",
    "heap_size": "k",
    "concat_sort_cost": "O(N log N)",
    "seed_cost": "O(k)",
    "loop_cost": "O(N log k)",
    "output_cost": "O(N)",
    "dominant": "loop",
    "first_r_cost": "O(k + r log k)",
}

_BOUND_HINTS = {
    "frontier": (
        "The heap never owns the data. At any moment, each source has exactly "
        "one record that could possibly be next — the earliest one it still "
        "holds. Finished sources have nothing left to offer."
    ),
    "heap_size": (
        "One entry per source still holding records, never more. How many "
        "sources are there?"
    ),
    "concat_sort_cost": (
        "N records, one comparison sort, the sortedness of the pieces thrown "
        "away. This is the number the merge must beat."
    ),
    "seed_cost": (
        "heapify of one head per source — and heapify of j items is O(j), "
        "not O(j log j). Lesson 4 earned this."
    ),
    "loop_cost": (
        "Count per RECORD, not per iteration: each record enters the heap "
        "once and leaves it once, and the heap never grows past the size you "
        "named in heap_size."
    ),
    "output_cost": "N records appended to a list. Nothing is compared.",
    "dominant": (
        "Compare the three phase costs. k <= N, so one of them contains the "
        "others. Exactly one winner this time."
    ),
    "first_r_cost": (
        "Seed the k heads, then r pops, each followed by at most one push — "
        "and the other N - r records are never touched. The label is the only "
        "one with both letters in it."
    ),
}

_PRED_INPUTS: dict[str, tuple] = {
    "C1": ({
        "api": [{"t": 1, "msg": "api-1"}, {"t": 3, "msg": "api-2"}],
        "web": [{"t": 1, "msg": "web-1"}],
    }, None),
    "C2": ({
        "db":  [],
        "api": [{"t": 2, "msg": "api-1"}, {"t": 2, "msg": "api-2"}],
        "web": [{"t": 1, "msg": "web-1"}, {"t": 9, "msg": "web-2"}],
    }, None),
    "C3": ({
        "a": [{"t": 1, "msg": "a-1"}, {"t": 5, "msg": "a-2"}],
        "b": [{"t": 2, "msg": "b-1"}, {"t": 3, "msg": "b-2"}],
    }, 3),
}

_PRED_LABELS = {
    "C1": "a tie that crosses services",
    "C2": "an empty source, a tie inside one",
    "C3": "the merge stops early",
}


def _oracle(services: dict[str, list[dict]]) -> list[dict]:
    """Decorate-sort-undecorate over everything. O(N log N) — exactly the
    baseline the student's merge is supposed to beat, which is why it is safe
    to have here."""
    rows = []
    for name, recs in services.items():
        for i, rec in enumerate(recs):
            rows.append((rec["t"], name, i, rec))
    rows.sort(key=lambda row: row[:3])
    return [row[3] for row in rows]


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


def _run_counted(fn, *args):
    """Call fn with heapq instrumented. Returns (result, op_counts, max_heap_size)."""
    counts: dict[str, int] = {}
    max_size = 0
    names = ("heappush", "heappop", "heappushpop", "heapreplace", "heapify")
    originals = {n: getattr(heapq, n) for n in names}

    def wrap(name, real):
        def wrapper(*a, **kw):
            nonlocal max_size
            counts[name] = counts.get(name, 0) + 1
            out = real(*a, **kw)
            if a and isinstance(a[0], list):
                max_size = max(max_size, len(a[0]))
            return out
        return wrapper

    for n, f in originals.items():
        setattr(heapq, n, wrap(n, f))
    try:
        result = fn(*args)
    finally:
        for n, f in originals.items():
            setattr(heapq, n, f)
    return result, counts, max_size


def _pops(counts: dict[str, int]) -> int:
    return (counts.get("heappop", 0) + counts.get("heappushpop", 0)
            + counts.get("heapreplace", 0))


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
        if key == "frontier":
            allowed, what = _FRONTIERS, "one of the four frontier descriptions"
        elif key == "heap_size":
            allowed, what = _SIZES, "one of: k, r, N, log N"
        elif key == "dominant":
            allowed, what = _PHASES, "one of: seed, loop, output, tie"
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
            'Write the literal itself: ["a-1", "b-1"]'
        )
        assert isinstance(got, list), f"{got!r} is a {type(got).__name__}, not a list"
        for item in got:
            assert isinstance(item, str), (
                f"{item!r} inside your prediction is a {type(item).__name__}, "
                "not a string — answer with the msg strings"
            )
        services, r = _PRED_INPUTS[key]
        want_recs = _oracle(services)
        want = [rec["msg"] for rec in (want_recs if r is None else want_recs[:r])]
        assert got == want, f"you predicted {got!r}, the merge produces {want!r}"
    return test


def test_merge_uses_a_heap():
    merge_logs({})  # signals "not attempted" instead of a confusing FAIL
    src = _source_of(merge_logs)
    assert "heapq" in src, "merge_logs() must actually use heapq"
    assert "from heapq import" not in src, \
        "use qualified heapq.* calls — the instrumentation cannot see unqualified ones"
    services = {"a": [{"t": 1, "msg": "a-1"}, {"t": 4, "msg": "a-2"}],
                "b": [{"t": 2, "msg": "b-1"}]}
    _, counts, _ = _run_counted(merge_logs, services)
    assert _pops(counts) >= 3, (
        f"only {_pops(counts)} heap pops for 3 records — the heap has to be what "
        "selects each record, not a scan over the lists"
    )


def test_merge_does_not_resort():
    merge_logs({})  # signals "not attempted" instead of a premature ok
    for fn in (merge_logs, first_r):
        src = _source_of(fn)
        assert "sorted(" not in src and ".sort(" not in src, (
            f"{fn.__name__}() calls a sort. The sources are ALREADY sorted — "
            "merging them is cheaper than re-sorting everything, and that gap "
            "is the whole lesson. Part A, concat_sort_cost vs loop_cost."
        )


def test_merge_empty_and_trivial():
    assert merge_logs({}) == [], "no services → []"
    assert merge_logs({"a": []}) == [], "one service, empty log → []"
    solo = {"a": [{"t": 3, "msg": "a-1"}]}
    got = merge_logs(solo)
    assert got == [{"t": 3, "msg": "a-1"}], f"one record in, one record out; got {got!r}"
    assert got[0] is solo["a"][0], (
        "return the record dicts THEMSELVES, not copies — downstream code "
        "holds references to them"
    )


def test_merge_small_cases():
    cases = [
        {"a": [{"t": 1, "msg": "a-1"}], "b": [{"t": 2, "msg": "b-1"}]},
        {"a": [{"t": 2, "msg": "a-1"}], "b": [{"t": 1, "msg": "b-1"}]},
        {"a": [{"t": 1, "msg": "a-1"}, {"t": 3, "msg": "a-2"}],
         "b": [{"t": 2, "msg": "b-1"}, {"t": 4, "msg": "b-2"}]},
        {"a": [{"t": 1, "msg": "a-1"}, {"t": 2, "msg": "a-2"}],
         "b": [{"t": 5, "msg": "b-1"}], "c": [{"t": 0, "msg": "c-1"}]},
    ]
    for services in cases:
        got = merge_logs(services)
        want = _oracle(services)
        assert got == want, (
            f"merge_logs({services}) gave "
            f"{[r['msg'] for r in got]!r}, expected {[r['msg'] for r in want]!r}"
        )


def test_ties_never_reach_the_records():
    # Same "t" in two different services, and the records are dicts. If your
    # heap entries can reach the record when the prefix ties, this raises
    # TypeError instead of merging.
    services = {"web": [{"t": 7, "msg": "web-1"}],
                "api": [{"t": 7, "msg": "api-1"}]}
    try:
        got = merge_logs(services)
    except TypeError:
        raise AssertionError(
            "two records reached the comparison (TypeError: dicts cannot be "
            "ordered). Whatever you push must settle every tie BEFORE the "
            "record would be compared — make the comparable prefix unique."
        )
    msgs = [r["msg"] for r in got]
    assert msgs == ["api-1", "web-1"], (
        f"expected ['api-1', 'web-1'], got {msgs!r} — on a t tie the smaller "
        "service name goes first"
    )


def test_tie_order_name_before_position():
    # At t=5 the heads are: "a" at position 2, "b" at position 0. The service
    # name settles the tie — a position number must not outrank it.
    services = {"a": [{"t": 1, "msg": "a-1"}, {"t": 2, "msg": "a-2"},
                      {"t": 5, "msg": "a-3"}],
                "b": [{"t": 5, "msg": "b-1"}]}
    got = [r["msg"] for r in merge_logs(services)]
    assert got == ["a-1", "a-2", "a-3", "b-1"], (
        f"expected ['a-1', 'a-2', 'a-3', 'b-1'], got {got!r} — on a t tie the "
        "service NAME decides, before any position or counter you carry. "
        "Check the ORDER of the fields in the tuple you push."
    )


def test_merge_heap_stays_a_frontier():
    # 4 services, 60 records. The heap must never hold more than one entry
    # per service, whatever the interleaving.
    rng = random.Random(7)
    services: dict[str, list[dict]] = {}
    for name in ("a", "b", "c", "d"):
        ticks = sorted(rng.randint(0, 40) for _ in range(15))
        services[name] = [{"t": t, "msg": f"{name}-{i}"} for i, t in enumerate(ticks)]
    got, _, max_size = _run_counted(merge_logs, services)
    assert [r["msg"] for r in got] == [r["msg"] for r in _oracle(services)], \
        "output wrong on the 4x15 case — fix correctness first"
    assert max_size <= 4, (
        f"your heap reached size {max_size} with only 4 services. The heap "
        "holds one head per unfinished source — never the whole data. If you "
        "pushed everything, you rebuilt the concat-and-sort baseline with "
        "extra steps (Part A, frontier)."
    )


def test_merge_stress_against_the_oracle():
    rng = random.Random(11)
    for case in range(300):
        k = rng.randint(0, 5)
        services = {}
        for s in range(k):
            count = rng.randint(0, 8)
            ticks = sorted(rng.randint(0, 10) for _ in range(count))
            services[f"s{s}"] = [{"t": t, "msg": f"s{s}-{i}"}
                                 for i, t in enumerate(ticks)]
        got = merge_logs(services)
        want = _oracle(services)
        assert got == want, (
            f"case {case}: merge_logs({services}) gave "
            f"{[r['msg'] for r in got]!r}, expected {[r['msg'] for r in want]!r}"
        )


def test_first_r_small_cases():
    services = {"a": [{"t": 1, "msg": "a-1"}, {"t": 5, "msg": "a-2"}],
                "b": [{"t": 2, "msg": "b-1"}]}
    assert first_r(services, 0) == [], "r == 0 → []"
    got = [r["msg"] for r in first_r(services, 2)]
    assert got == ["a-1", "b-1"], f"first 2 of the merge: expected ['a-1', 'b-1'], got {got!r}"
    got = [r["msg"] for r in first_r(services, 99)]
    assert got == ["a-1", "b-1", "a-2"], (
        f"r beyond the total returns the whole merge; got {got!r}"
    )


def test_first_r_is_lazy():
    # 3 services, 150,000 records, ten requested. Laziness is measured by
    # counting, not by timing: one pop per record returned, plus the seed.
    per, r = 50_000, 10
    services = {
        name: [{"t": base + 3 * i, "msg": f"{name}-{i}"} for i in range(per)]
        for base, name in ((0, "a"), (1, "b"), (2, "c"))
    }
    got, counts, max_size = _run_counted(first_r, services, r)
    want = _oracle(services)[:r]
    assert [rec["msg"] for rec in got] == [rec["msg"] for rec in want], \
        f"wrong records: got {[rec['msg'] for rec in got]!r}"
    pops = _pops(counts)
    assert pops <= r, (
        f"{pops} heap pops to return {r} records. Every pop emits exactly one "
        "record; if you popped more, you merged more than you returned. Stop "
        "when you have r."
    )
    pushes = counts.get("heappush", 0)
    assert pushes <= 3 + r, (
        f"{pushes} pushes to return {r} records from 3 services. Seed the "
        "heads (3), then at most one push per pop — records beyond the r-th "
        "must never enter the heap."
    )
    assert max_size <= 3, (
        f"your heap reached size {max_size} with only 3 services — the "
        "frontier invariant applies here too."
    )


def test_first_r_stress_against_the_oracle():
    rng = random.Random(23)
    for case in range(200):
        k = rng.randint(0, 4)
        services = {}
        for s in range(k):
            count = rng.randint(0, 6)
            ticks = sorted(rng.randint(0, 9) for _ in range(count))
            services[f"s{s}"] = [{"t": t, "msg": f"s{s}-{i}"}
                                 for i, t in enumerate(ticks)]
        r = rng.randint(0, 8)
        got = first_r(services, r)
        want = _oracle(services)[:r]
        assert got == want, (
            f"case {case}: first_r({services}, {r}) gave "
            f"{[rec['msg'] for rec in got]!r}, expected {[rec['msg'] for rec in want]!r}"
        )


TESTS = (
    [(f"A — {key}", _make_bound_test(key)) for key in _BOUND_ANSWERS]
    + [
        ("B — the heap is what selects", test_merge_uses_a_heap),
        ("B — no re-sorting", test_merge_does_not_resort),
        ("B — empty and trivial inputs", test_merge_empty_and_trivial),
        ("B — small cases", test_merge_small_cases),
        ("B — ties never reach the records", test_ties_never_reach_the_records),
        ("B — name outranks position on ties", test_tie_order_name_before_position),
        ("B — the heap stays a frontier", test_merge_heap_stays_a_frontier),
        ("B — 300 random cases against an oracle", test_merge_stress_against_the_oracle),
        ("B — first_r small cases", test_first_r_small_cases),
        ("B — first_r is lazy (150k records, 10 asked)", test_first_r_is_lazy),
        ("B — first_r, 200 random cases", test_first_r_stress_against_the_oracle),
    ]
    + [(f"C — {_PRED_LABELS[key]}", _make_prediction_test(key)) for key in _PRED_LABELS]
)

if __name__ == "__main__":
    print("\nmerge drill — Lesson 6\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green. Here the sources sat still in a dict someone handed you.")
        print("Ask your teacher what changes when the sources must be MAINTAINED —")
        print("records appended, sources added and removed — while merged views are")
        print("being requested. That is the next problem.\n")
    else:
        print("\nKeep going. Ask your teacher for a hint if you are stuck.\n")
