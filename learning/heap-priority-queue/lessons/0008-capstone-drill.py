"""
Lesson 8 drill — the capstone: everything, cold.

HOW TO USE THIS FILE
    1. CLOSED-BOOK: no cheat sheet, no old lessons, no old code on the
       first pass. Wrong answers are measurements, not failures.
    2. Part P: predict the three traces on paper, then fill PREDICTIONS.
    3. Part K: fill every KNOWLEDGE cell with one of its allowed answers,
       spelled exactly as listed in the comment above it.
    4. Run it, from the repo root:
           python3.14 learning/heap-priority-queue/lessons/0008-capstone-drill.py
    5. Whatever comes back red names the cheat-sheet section to re-read.

There are no solutions in this file. This is the last drill of the track.
"""

import heapq
import itertools


# ----------------------------------------------------------------------------
# PART P — three traces, cold (paper first, as always)
# ----------------------------------------------------------------------------
#
#   P1 (heap mechanics): the INTERNAL ARRAY, not the sorted order.
#       h: list[int] = []
#       heapq.heappush(h, 7); heapq.heappush(h, 2)
#       heapq.heappush(h, 9); heapq.heappush(h, 4)
#       heapq.heappop(h)
#       What list is h now? Answer as a list of ints, e.g. [1, 2, 3].
#
#   P2 (heap of cursors): merge these two sorted logs; smaller t first,
#       on a t tie the smaller SOURCE NAME first. Answer with the msg
#       strings in output order.
#       "api": [ (t=1, "api-1"), (t=3, "api-2") ]
#       "web": [ (t=1, "web-1") ]
#
#   P3 (two heaps, one boundary): a build farm, slots=1.
#       submit(5, "x"); submit(9, "y"); submit(7, "z")
#       Q1: weakest_running()   Q2: strongest_waiting()
#       Answer with the two query results in order.

PREDICTIONS: dict[str, list | None] = {
    "P1": [4, 7, 9],
    "P2": ["api-1","web-1" , "api-2"],
    "P3": ['y', 'z'],
}


# ----------------------------------------------------------------------------
# PART K — fourteen knowledge cells
# ----------------------------------------------------------------------------
#
# Cost cells take one of (exactly):
#
#     O(1)  O(k)  O(n)  O(log n)  O(k log n)  O(n log k)  O(n log n)
#     O(k + r log k)
#
# K1  "build_heap_cost"   — heapq.heapify on n items.
# K2  "pops_phase_cost"   — AFTER heapify-all: the k pops, that phase alone.
# K3  "nsmallest_cost"    — heapq.nsmallest(k, data), len(data) = n.
# K4  "first_r_cost"      — k-way merge, seeded, stopped after r records.
#
# K5  "stream_survivor"   — n = 1e6 arrives as a STREAM; which strategy is
#                           the only one still available?
# K6  "time_winner_small_k" — n = 1e6 as a finished array, k = 10; which
#                           strategy wins on pure TIME?
#     For K5/K6, one of:  "bounded heap"  "heapify all"  "sort all"
#
# K7  "bounded_heap_breaker" — a size-k min-heap holds the k largest seen so
#     far. One heapq call, if used unconditionally on each newcomer, corrupts
#     the heap's CONTENT while leaving it a perfectly valid heap. Which?
#     One of:  "heappush"  "heappushpop"  "heapreplace"
#
# K8  "breaker_reason" — why K7 corrupts. One of, exactly:
#     "it evicts the root even when the newcomer loses"
#     "it pushes first and pops the wrong element"
#     "it skips the sift and breaks heap order"
#     "it compares against children instead of the root"
#
# K9  "q_metric" — Last Stone Weight: pop two, push at most one, repeat
#     while two stones remain. A VALID termination metric Q is, exactly:
#     "stones still in the heap"
#     "ticks elapsed since the start"
#     "stones already smashed so far"
#     "the weight of the heaviest stone"
#
# K10 "alias_bug" — classify the defect, one of the four sentences below:
#         def strongest_member(self, uid):
#             members = self.teams[uid] if uid in self.teams else set()
#             members.add(uid)
#             return max(members)
#     "the query mutates shared state through an alias"
#     "the query returns a copy instead of the object"
#     "the set discards duplicates the caller still needs"
#     "the guard should test length, not membership"
#
# K11 "reencode_314" — mirrored two-heap tuples under min-only heapq flip
#     every sign at a crossing. Using 3.14's heappush_max/heappop_max for
#     the max side instead, what happens at the border? One of:
#     "the same tuple serves both sides"
#     "every sign still flips at the border"
#     "only the arrival field still flips"
#     "the crossing now needs a fresh counter"
#
# K12–K14 "failure_f1/f2/f3" — name each failure class. One of:
#     "syntax error"  "runtime error"  "wrong output"
#
#     F1: the run completes and prints — but the list is ordered
#         alphabetically instead of by priority.
#     F2: Python exits instantly pointing at line 12; not one of your
#         print statements ever appears.
#     F3: the run starts, prints twice, then dies with
#         "TypeError: '<' not supported between instances of 'dict' and 'dict'".

KNOWLEDGE: dict[str, str | None] = {
    "build_heap_cost": "O(n)",
    "pops_phase_cost": "O(k log n)",
    "nsmallest_cost": "O(n log k)",
    "first_r_cost": "O(k + r log k)",

    "stream_survivor": "bounded heap",
    "time_winner_small_k": "heapify all",

    "bounded_heap_breaker": "heapreplace",
    "breaker_reason": "it evicts the root even when the newcomer loses",

    "q_metric": "stones still in the heap",
    "alias_bug": "the query mutates shared state through an alias",
    "reencode_314": "the same tuple serves both sides",

    "failure_f1": "wrong output",
    "failure_f2": "syntax error",
    "failure_f3": "runtime error",
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

_COSTS = {"O(1)", "O(k)", "O(n)", "O(log n)", "O(k log n)", "O(n log k)",
          "O(n log n)", "O(k + r log k)"}
_STRATEGIES = {"bounded heap", "heapify all", "sort all"}
_OPS = {"heappush", "heappushpop", "heapreplace"}
_REASONS = {
    "it evicts the root even when the newcomer loses",
    "it pushes first and pops the wrong element",
    "it skips the sift and breaks heap order",
    "it compares against children instead of the root",
}
_QS = {
    "stones still in the heap",
    "ticks elapsed since the start",
    "stones already smashed so far",
    "the weight of the heaviest stone",
}
_ALIAS = {
    "the query mutates shared state through an alias",
    "the query returns a copy instead of the object",
    "the set discards duplicates the caller still needs",
    "the guard should test length, not membership",
}
_REENC = {
    "the same tuple serves both sides",
    "every sign still flips at the border",
    "only the arrival field still flips",
    "the crossing now needs a fresh counter",
}
_CLASSES = {"syntax error", "runtime error", "wrong output"}

_K_ALLOWED = {
    "build_heap_cost": _COSTS, "pops_phase_cost": _COSTS,
    "nsmallest_cost": _COSTS, "first_r_cost": _COSTS,
    "stream_survivor": _STRATEGIES, "time_winner_small_k": _STRATEGIES,
    "bounded_heap_breaker": _OPS, "breaker_reason": _REASONS,
    "q_metric": _QS, "alias_bug": _ALIAS, "reencode_314": _REENC,
    "failure_f1": _CLASSES, "failure_f2": _CLASSES, "failure_f3": _CLASSES,
}

_K_ANSWERS = {
    "build_heap_cost": "O(n)",
    "pops_phase_cost": "O(k log n)",
    "nsmallest_cost": "O(n log k)",
    "first_r_cost": "O(k + r log k)",
    "stream_survivor": "bounded heap",
    "time_winner_small_k": "heapify all",
    "bounded_heap_breaker": "heapreplace",
    "breaker_reason": "it evicts the root even when the newcomer loses",
    "q_metric": "stones still in the heap",
    "alias_bug": "the query mutates shared state through an alias",
    "reencode_314": "the same tuple serves both sides",
    "failure_f1": "wrong output",
    "failure_f2": "syntax error",
    "failure_f3": "runtime error",
}

_K_HINTS = {
    "build_heap_cost": "Lesson 4 earned this: heapify of n items is NOT n pushes.",
    "pops_phase_cost": (
        "Attribute the log to the right owner: each pop sifts a heap whose "
        "size is still n — the k out front only counts the pops."
    ),
    "nsmallest_cost": (
        "The n that is not your n: heapq seeds a heap of k (zip with range(k)) "
        "and sweeps the remaining n - k items against it."
    ),
    "first_r_cost": (
        "Seed the k heads, then r pops with at most one push each — everything "
        "past the r-th record is never touched."
    ),
    "stream_survivor": (
        "heapify and sort both need the whole collection in hand at once. "
        "Only one strategy never holds more than k."
    ),
    "time_winner_small_k": (
        "O(n) build + O(k log n) pops vs O(n log k) arrivals. At k = 10, "
        "which total is linear? Winning on the wrong axis is not winning — "
        "but this question asked about exactly one axis."
    ),
    "bounded_heap_breaker": (
        "Two calls combine push and pop. One of them pops FIRST, "
        "unconditionally — before knowing whether the newcomer even belongs."
    ),
    "breaker_reason": (
        "The heap stays structurally valid; what breaks is WHICH k items it "
        "holds. The root — a rightful member — is gone, and a weaker "
        "newcomer sits in its place."
    ),
    "q_metric": (
        "Q must be a non-negative integer that every iteration DECREASES. "
        "Progress bars go up — they are the mirror image of a Q."
    ),
    "alias_bug": (
        "Follow the reference: when uid IS in teams, what does `members` "
        "name? Then .add() writes through it. A certain P6 review found "
        "this exact shape."
    ),
    "reencode_314": (
        "The flip was never part of the pattern — it was the price of "
        "simulating a max-heap inside a min-heap. Native max-heaps stop "
        "charging it."
    ),
    "failure_f1": "It ran. It finished. The answer was wrong. Which class is that?",
    "failure_f2": "Nothing of yours ever executed — the file was rejected before running.",
    "failure_f3": "It was running fine until an operation blew up mid-flight.",
}

_K_LABELS = {
    "build_heap_cost": "K1 — heapify cost",
    "pops_phase_cost": "K2 — the pops phase, attributed",
    "nsmallest_cost": "K3 — the n that is not your n",
    "first_r_cost": "K4 — lazy merge cost",
    "stream_survivor": "K5 — who survives a stream",
    "time_winner_small_k": "K6 — who wins pure time",
    "bounded_heap_breaker": "K7 — the bounded-heap breaker",
    "breaker_reason": "K8 — why it breaks",
    "q_metric": "K9 — a valid Q",
    "alias_bug": "K10 — classify the query bug",
    "reencode_314": "K11 — the border under 3.14",
    "failure_f1": "K12 — failure class: F1",
    "failure_f2": "K13 — failure class: F2",
    "failure_f3": "K14 — failure class: F3",
}


def _p1_oracle() -> list[int]:
    h: list[int] = []
    for x in (7, 2, 9, 4):
        heapq.heappush(h, x)
    heapq.heappop(h)
    return h


def _p2_oracle() -> list[str]:
    logs = {"api": [(1, "api-1"), (3, "api-2")], "web": [(1, "web-1")]}
    rows = [(t, name, i, msg) for name, recs in logs.items()
            for i, (t, msg) in enumerate(recs)]
    rows.sort(key=lambda r: r[:3])
    return [r[3] for r in rows]


def _p3_oracle() -> list[str | None]:
    # snapshot semantics, as in the Lesson 7 harness
    slots = 1
    jobs: list[tuple[int, int, str]] = []
    counter = itertools.count()
    for p, name in ((5, "x"), (9, "y"), (7, "z")):
        jobs.append((p, next(counter), name))
    ranked = sorted(jobs, key=lambda j: (-j[0], j[1]))
    running, waiting = ranked[:slots], ranked[slots:]
    return [running[-1][2] if running else None,
            waiting[0][2] if waiting else None]


_P_ORACLES = {"P1": _p1_oracle, "P2": _p2_oracle, "P3": _p3_oracle}
_P_LABELS = {
    "P1": "P1 — the internal array, traced",
    "P2": "P2 — the merge, traced",
    "P3": "P3 — the boundary, traced",
}


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


def _make_prediction_test(key):
    def test():
        got = PREDICTIONS.get(key)
        if got is None:
            raise NotImplementedError
        assert not isinstance(got, str), (
            f"{got!r} is a string, not a list — drop the outer quotes and "
            "write the literal itself"
        )
        assert isinstance(got, list), f"{got!r} is a {type(got).__name__}, not a list"
        want = _P_ORACLES[key]()
        assert got == want, f"you predicted {got!r}; the trace produces {want!r}"
    return test


def _make_knowledge_test(key):
    def test():
        got = KNOWLEDGE.get(key)
        if got is None:
            raise NotImplementedError
        assert isinstance(got, str), f"{got!r} is not a string — answer with one of the listed options"
        allowed = _K_ALLOWED[key]
        assert got in allowed, (
            f"{got!r} is not one of the allowed answers for this cell — "
            "copy the option exactly as spelled in the comment"
        )
        assert got == _K_ANSWERS[key], f"you said {got!r}. Hint: {_K_HINTS[key]}"
    return test


TESTS = (
    [(_P_LABELS[key], _make_prediction_test(key)) for key in _P_ORACLES]
    + [(_K_LABELS[key], _make_knowledge_test(key)) for key in _K_ANSWERS]
)

if __name__ == "__main__":
    print("\ncapstone drill — Lesson 8\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green — the track is complete: 7 problems, 8 lessons, one")
        print("cheat sheet that is now yours. Ask your teacher for the closing")
        print("debrief: what to re-test in a month, and what comes after heaps.\n")
    else:
        print("\nEvery red line names a cheat-sheet section to re-read.")
        print("Review it, come back tomorrow, run again — spacing is the point.\n")
