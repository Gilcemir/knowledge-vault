"""
Lesson 7 drill — two heaps, one boundary: the build farm.

HOW TO USE THIS FILE
    1. Part A: fill in BOUNDS. On paper first, before you touch Part B.
    2. Part B: implement the BuildFarm class.
    3. Part C: fill in PREDICTIONS *before* you run anything.
    4. Run it, from the repo root:
           python3.14 learning/heap-priority-queue/lessons/0007-boundary-drill.py
    5. Immediate pass/fail on every item.

Two heaps facing each other across one cut. Part A's direction answers ARE
the design; if you have those, Part B is choreography.

There are no solutions in this file, and your teacher will not give you one.
If you are stuck, ask for a hint — you will get the smallest hint that unblocks
you. If a hint is unclear, say so and ask for the answer instead.
"""

import heapq
import itertools


# ----------------------------------------------------------------------------
# PART A — the invariant, the directions, and what each move costs
# ----------------------------------------------------------------------------
#
# Notation (two letters, two different things — spell them before any cost):
#     n = jobs currently in the farm, both groups together
#     s = slots (machines); small, and it moves by one at a time
#
# "invariant": what is ALWAYS true after every operation? One of, exactly:
#
#     "every running job outranks every waiting job"
#     "the running heap stores its jobs in sorted order"
#     "the strongest waiting job outranks the weakest running job"
#     "a job that reaches the running side stays there"
#
# "running_heap" / "waiting_heap": the direction each side needs.
# One of: "min-heap", "max-heap"
#
# "crossing": what happens when a job changes sides? One of, exactly:
#
#     "only a root ever crosses, re-encoded for the other side"
#     "the whole weaker half is rebuilt on every submit"
#     "any job may cross whenever the two heaps disagree"
#     "a crossing job keeps the tuple it already carried"
#
# The "_cost" keys take one of these labels, spelled exactly:
#
#     O(1)  O(log n)  O(n)  O(n log n)
#
#     peek_cost           — weakest_running() / strongest_waiting(), one call
#     submit_cost         — one submit, worst case
#     reslot_cost         — one add_slot or remove_slot, worst case
#     total_submits_cost  — n submits, all together
#
# Leave a value as None to skip it.

BOUNDS: dict[str, str | None] = {
    "invariant": "every running job outranks every waiting job",
    "running_heap": "min-heap",
    "waiting_heap": "max-heap",
    "crossing": "only a root ever crosses, re-encoded for the other side",

    "peek_cost": "O(1)",
    "submit_cost": "O(log n)",
    "reslot_cost": "O(log n)",
    "total_submits_cost": "O(n log n)",
}


# ----------------------------------------------------------------------------
# PART B — the farm
# ----------------------------------------------------------------------------

class BuildFarm:
    """A CI cluster: the s strongest jobs run, everyone else waits.

    Ranking ("outranks"): higher priority wins; on a priority tie, the job
    submitted EARLIER outranks. Job names are unique, but the name must never
    be what settles an order — the submission order must (the harness has two
    tests where names and arrival order deliberately disagree).

    Contract, holding after every public call returns:
      - exactly min(slots, total jobs) jobs are running, and they are the
        strongest ones in the whole farm;
      - slots may be 0 (init or via remove_slot): then everything waits.

    Methods:
      __init__(slots)      — slots >= 0; the farm starts empty.
      submit(priority, name)
                           — a new job arrives. Runs if a machine is free;
                             preempts the weakest running job if it outranks
                             it; otherwise waits.
      weakest_running()    — name of the running job a newcomer would have to
                             beat, or None if nothing runs.
      strongest_waiting()  — name of the waiting job a freed machine would
                             take, or None if nothing waits.
      add_slot()           — one machine comes online; if anyone waits, the
                             strongest waiting job is promoted immediately.
      remove_slot()        — one machine goes down (no-op if slots == 0); if
                             the farm is now over capacity, the weakest
                             running job is demoted immediately.

    Rules:
      - Use `import heapq` and qualified calls (`heapq.heappop(...)`), not
        `from heapq import heappop` — the instrumentation cannot see
        unqualified ones.
      - The two queries are READS. They must not change any state — the
        harness interleaves repeated calls and the farm must behave as if
        they never happened. A peek is not a pop.
      - Re-ranking a group wholesale is off the table: every operation must
        be a constant number of heap moves. The harness reads your source
        and counts your heap operations across 1500 submits.
    """

    def __init__(self, slots: int) -> None:
        self.counter = itertools.count()
        self.slots = slots
        self.running = []
        self.waiting = []

    def submit(self, priority: int, name: str) -> None:
        job = (priority, -next(self.counter), name)
        if len(self.running) < self.slots:
            heapq.heappush(self.running, job)
            return

        if self.running and job > self.running[0]:
            weakest_job = heapq.heappop(self.running)
            heapq.heappush(self.running, job)
            heapq.heappush_max(self.waiting, (weakest_job[0], weakest_job[1], weakest_job[2]))
        else:
            heapq.heappush_max(self.waiting, (job[0], job[1], job[2]))

    def weakest_running(self) -> str | None:
        return self.running[0][2] if self.running else None

    def strongest_waiting(self) -> str | None:
        return self.waiting[0][2] if self.waiting else None

    def add_slot(self) -> None:
        self.slots += 1
        if self.waiting:
            priority, arr, name = heapq.heappop_max(self.waiting)
            heapq.heappush(self.running, (priority, arr, name))

    def remove_slot(self) -> None:
        if self.slots == 0:
            return
        if self.running and len(self.running) == self.slots:
            priority, arr, name = heapq.heappop(self.running)
            heapq.heappush_max(self.waiting, (priority, arr, name))
        self.slots -= 1


# ----------------------------------------------------------------------------
# PART C — predict the trace
# ----------------------------------------------------------------------------
#
# Write down what each QUERY returns, BEFORE running. Answer with the job
# names, in query order — and bare None (no quotes) for a query that returns
# None. Each scenario is small enough to trace on paper with the section 3
# table from the lesson.
#
#   C1: farm = BuildFarm(slots=2)
#       farm.submit(5, "a"); farm.submit(3, "b"); farm.submit(4, "c")
#       Q1: farm.weakest_running()
#       Q2: farm.strongest_waiting()
#
#   C2: farm = BuildFarm(slots=1)
#       farm.submit(7, "x"); farm.submit(7, "y")
#       Q1: farm.weakest_running()
#       farm.add_slot()
#       Q2: farm.weakest_running()
#       Q3: farm.strongest_waiting()
#
#   C3: farm = BuildFarm(slots=2)
#       farm.submit(9, "p"); farm.submit(1, "q"); farm.submit(5, "r")
#       farm.remove_slot()
#       Q1: farm.weakest_running()
#       Q2: farm.strongest_waiting()
#
# C1 has one preemption.
# C2 has a priority tie, then the boundary moves right.
# C3 has a preemption, then the boundary moves left.
#
# Write real lists of real values, e.g. ["a", None] — not "[a, None]".

PREDICTIONS: dict[str, list[str | None] | None] = {
    "C1": ["c", "b"],
    "C2": ["x", "y", None],
    "C3": ["p", "r"],
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

import inspect
import random

_INVARIANTS = {
    "every running job outranks every waiting job",
    "the running heap stores its jobs in sorted order",
    "the strongest waiting job outranks the weakest running job",
    "a job that reaches the running side stays there",
}
_DIRECTIONS = {"min-heap", "max-heap"}
_CROSSINGS = {
    "only a root ever crosses, re-encoded for the other side",
    "the whole weaker half is rebuilt on every submit",
    "any job may cross whenever the two heaps disagree",
    "a crossing job keeps the tuple it already carried",
}
_LABELS = {"O(1)", "O(log n)", "O(n)", "O(n log n)"}

_BOUND_ANSWERS = {
    "invariant": "every running job outranks every waiting job",
    "running_heap": "min-heap",
    "waiting_heap": "max-heap",
    "crossing": "only a root ever crosses, re-encoded for the other side",
    "peek_cost": "O(1)",
    "submit_cost": "O(log n)",
    "reslot_cost": "O(log n)",
    "total_submits_cost": "O(n log n)",
}

_BOUND_HINTS = {
    "invariant": (
        "The two groups are not independent piles — the rule that defines "
        "them compares ACROSS the cut. State the relationship between any "
        "running job and any waiting job."
    ),
    "running_heap": (
        "Which running job must be visible in O(1)? The one a newcomer would "
        "preempt. Point the root at it."
    ),
    "waiting_heap": (
        "Which waiting job must be visible in O(1)? The one a freed machine "
        "would take. Point the root at it."
    ),
    "crossing": (
        "A submit changes the population by one, so the boundary moves by at "
        "most one position — and the invariant guarantees the job at that "
        "position is sitting at a root. Remember that each side encodes "
        "strength in its own direction."
    ),
    "peek_cost": "heap[0]. No walk, no pop, no loop.",
    "submit_cost": (
        "Worst case is the preemption path: one pop and two pushes — a "
        "constant count of root moves on heaps never bigger than n."
    ),
    "reslot_cost": "Promote or demote: one pop from one root, one push to the other.",
    "total_submits_cost": (
        "n submits, each a constant number of O(log n) moves. Same per-item "
        "accounting as Lessons 5 and 6."
    ),
}


class _Oracle:
    """Snapshot semantics: re-rank everything on every question. O(n log n)
    per query — exactly the wasteful total order the student's farm is
    supposed to avoid maintaining, which is why it is safe to have here."""

    def __init__(self, slots: int) -> None:
        self.slots = slots
        self.jobs: list[tuple[int, int, str]] = []  # (priority, arrival, name)
        self._arrivals = itertools.count()

    def submit(self, priority: int, name: str) -> None:
        self.jobs.append((priority, next(self._arrivals), name))

    def _ranked(self) -> list[tuple[int, int, str]]:
        return sorted(self.jobs, key=lambda j: (-j[0], j[1]))

    def weakest_running(self) -> str | None:
        running = self._ranked()[: self.slots]
        return running[-1][2] if running else None

    def strongest_waiting(self) -> str | None:
        waiting = self._ranked()[self.slots:]
        return waiting[0][2] if waiting else None

    def add_slot(self) -> None:
        self.slots += 1

    def remove_slot(self) -> None:
        self.slots = max(0, self.slots - 1)


_PRED_SCRIPTS: dict[str, tuple[int, list[tuple]]] = {
    "C1": (2, [("submit", 5, "a"), ("submit", 3, "b"), ("submit", 4, "c"),
               ("q_weak",), ("q_strong",)]),
    "C2": (1, [("submit", 7, "x"), ("submit", 7, "y"), ("q_weak",),
               ("add",), ("q_weak",), ("q_strong",)]),
    "C3": (2, [("submit", 9, "p"), ("submit", 1, "q"), ("submit", 5, "r"),
               ("remove",), ("q_weak",), ("q_strong",)]),
}

_PRED_LABELS = {
    "C1": "fill, then one preemption",
    "C2": "a tie, then the boundary moves right",
    "C3": "a preemption, then the boundary moves left",
}


def _apply(target, op: tuple):
    """Apply one script op to a farm or oracle; return the answer for queries."""
    kind = op[0]
    if kind == "submit":
        target.submit(op[1], op[2])
    elif kind == "add":
        target.add_slot()
    elif kind == "remove":
        target.remove_slot()
    elif kind == "q_weak":
        return target.weakest_running()
    elif kind == "q_strong":
        return target.strongest_waiting()
    return None


def _source_of(obj) -> str:
    """Source of obj with every triple-quoted block cut out — docstrings state
    the rules and would trip the token checks below. Cut textually, not via
    __doc__: since Python 3.13 the compiler dedents docstrings, so __doc__ no
    longer matches the source text."""
    try:
        src = inspect.getsource(obj)
    except OSError:
        return ""
    for quote in ('"""', "'''"):
        while True:
            start = src.find(quote)
            if start == -1:
                break
            end = src.find(quote, start + 3)
            if end == -1:
                break
            src = src[:start] + src[end + 3:]
    return src


def _run_counted(fn, *args):
    """Call fn with heapq instrumented. Returns (result, op_counts, max_heap_size)."""
    counts: dict[str, int] = {}
    max_size = 0
    names = ("heappush", "heappop", "heappushpop", "heapreplace", "heapify",
             "heappush_max", "heappop_max", "heappushpop_max",
             "heapreplace_max", "heapify_max")
    originals = {n: getattr(heapq, n) for n in names if hasattr(heapq, n)}

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


def _total_ops(counts: dict[str, int]) -> int:
    return sum(counts.values())


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
        if key == "invariant":
            allowed, what = _INVARIANTS, "one of the four invariant sentences"
        elif key in ("running_heap", "waiting_heap"):
            allowed, what = _DIRECTIONS, 'one of: "min-heap", "max-heap"'
        elif key == "crossing":
            allowed, what = _CROSSINGS, "one of the four crossing descriptions"
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
            'Write the literal itself: ["a", None]'
        )
        assert isinstance(got, list), f"{got!r} is a {type(got).__name__}, not a list"
        for item in got:
            assert item is None or isinstance(item, str), (
                f"{item!r} inside your prediction is a {type(item).__name__} — "
                "answer with job-name strings, or bare None for an empty side"
            )
        slots, script = _PRED_SCRIPTS[key]
        oracle = _Oracle(slots)
        want: list[str | None] = []
        for op in script:
            ans = _apply(oracle, op)
            if op[0].startswith("q"):
                want.append(ans)
        assert got == want, f"you predicted {got!r}, the farm produces {want!r}"
    return test


def test_farm_uses_a_heap():
    BuildFarm(1)  # signals "not attempted" instead of a confusing FAIL
    src = _source_of(BuildFarm)
    assert "heapq" in src, "BuildFarm must actually use heapq"
    assert "from heapq import" not in src, \
        "use qualified heapq.* calls — the instrumentation cannot see unqualified ones"

    def driver():
        farm = BuildFarm(1)
        farm.submit(1, "a")
        farm.submit(2, "b")   # must preempt a
        return farm
    _, counts, _ = _run_counted(driver)
    pushes = sum(counts.get(n, 0) for n in
                 ("heappush", "heappushpop", "heappush_max", "heappushpop_max"))
    assert pushes >= 3, (
        f"only {pushes} heap pushes for a fill plus a preemption — the heaps "
        "have to be what holds the jobs, not a list you scan"
    )


def test_farm_does_not_resort():
    BuildFarm(1)  # signals "not attempted" instead of a premature ok
    src = _source_of(BuildFarm)
    for token in ("sorted(", ".sort(", "bisect"):
        assert token not in src, (
            f"BuildFarm uses {token!r}. Re-ranking a group wholesale is the "
            "baseline this design beats — the boundary only ever moves by "
            "one root. Part A, crossing + total_submits_cost."
        )


def test_empty_and_trivial():
    farm = BuildFarm(3)
    assert farm.weakest_running() is None, (
        f"empty farm: weakest_running() must be None, got {farm.weakest_running()!r}"
    )
    assert farm.strongest_waiting() is None, (
        f"empty farm: strongest_waiting() must be None, got {farm.strongest_waiting()!r}"
    )
    farm = BuildFarm(0)
    farm.submit(4, "solo")
    assert farm.weakest_running() is None, (
        "slots == 0: nothing can run — weakest_running() must be None, got "
        f"{farm.weakest_running()!r}"
    )
    assert farm.strongest_waiting() == "solo", (
        f"slots == 0: the job waits — expected 'solo', got {farm.strongest_waiting()!r}"
    )
    farm.add_slot()
    assert farm.weakest_running() == "solo", (
        "add_slot must promote the strongest waiting job immediately — "
        f"expected 'solo' running, got {farm.weakest_running()!r}"
    )
    assert farm.strongest_waiting() is None, (
        f"after the promotion nothing waits — got {farm.strongest_waiting()!r}"
    )


def test_fill_then_preempt():
    farm = BuildFarm(2)
    farm.submit(10, "t1")
    assert farm.weakest_running() == "t1", (
        f"one job, one machine in use: weakest is 't1', got {farm.weakest_running()!r}"
    )
    farm.submit(20, "t2")
    assert farm.weakest_running() == "t1", (
        f"t1(10) is weaker than t2(20): expected 't1', got {farm.weakest_running()!r}"
    )
    farm.submit(15, "t3")
    assert farm.weakest_running() == "t3", (
        "t3(15) outranks t1(10): t1 is preempted, and t3(15) is now the "
        f"weakest runner (vs t2(20)) — got {farm.weakest_running()!r}"
    )
    assert farm.strongest_waiting() == "t1", (
        f"the preempted t1 waits — got {farm.strongest_waiting()!r}"
    )
    farm.submit(1, "t4")
    assert farm.strongest_waiting() == "t1", (
        "t4(1) goes straight to waiting and does not outrank t1(10) — "
        f"expected 't1', got {farm.strongest_waiting()!r}"
    )


def test_ties_settled_by_arrival_not_name():
    farm = BuildFarm(2)
    farm.submit(5, "alpha")
    farm.submit(5, "zulu")
    assert farm.weakest_running() == "zulu", (
        f"equal priority: the LATER submission is the weaker job — expected "
        f"'zulu' (submitted second), got {farm.weakest_running()!r}. If you got "
        "'alpha', a name is deciding an order that belongs to arrival."
    )
    farm = BuildFarm(1)
    farm.submit(9, "m")
    farm.submit(5, "zulu")
    farm.submit(5, "alpha")
    assert farm.strongest_waiting() == "zulu", (
        f"equal priority in waiting: the EARLIER submission outranks — expected "
        f"'zulu' (submitted first), got {farm.strongest_waiting()!r}. If you got "
        "'alpha', a name is deciding an order that belongs to arrival."
    )


def test_crossing_reencodes_the_tuple():
    # A job that crosses the boundary lands in a heap with the OPPOSITE
    # direction. If it carries its old tuple, nothing crashes — the answers
    # just come out wrong.
    farm = BuildFarm(1)
    farm.submit(1, "a")
    farm.submit(5, "b")   # preempts a → a crosses to waiting
    farm.submit(9, "c")   # preempts b → b crosses to waiting
    got = farm.strongest_waiting()
    assert got == "b", (
        f"waiting holds a(1) and b(5); the strongest is 'b', got {got!r}. "
        "If you got 'a', a tuple crossed the boundary without being "
        "re-encoded — every sign flips when a job changes sides."
    )
    assert farm.weakest_running() == "c", (
        f"only c(9) runs — got {farm.weakest_running()!r}"
    )


def test_boundary_moves():
    farm = BuildFarm(1)
    farm.submit(3, "a")
    farm.submit(7, "b")   # preempts a
    farm.add_slot()
    assert farm.weakest_running() == "a", (
        f"add_slot promotes the strongest waiting job (a) — weakest running is "
        f"then 'a'(3), got {farm.weakest_running()!r}"
    )
    assert farm.strongest_waiting() is None, (
        f"nothing waits after the promotion — got {farm.strongest_waiting()!r}"
    )
    farm.remove_slot()
    assert farm.strongest_waiting() == "a", (
        f"remove_slot demotes the weakest running job (a) — got {farm.strongest_waiting()!r}"
    )
    farm.remove_slot()
    assert farm.weakest_running() is None, (
        "slots is now 0: everything is demoted — weakest_running() must be "
        f"None, got {farm.weakest_running()!r}"
    )
    assert farm.strongest_waiting() == "b", (
        f"b(7) outranks a(3) in waiting — got {farm.strongest_waiting()!r}"
    )
    farm.remove_slot()  # already 0: must be a no-op, not an error
    assert farm.strongest_waiting() == "b", (
        f"remove_slot at 0 slots is a no-op — got {farm.strongest_waiting()!r}"
    )
    farm.add_slot()
    assert farm.weakest_running() == "b", (
        f"the freed machine takes the strongest waiter (b) — got {farm.weakest_running()!r}"
    )


def test_queries_do_not_mutate():
    # The same script twice: once clean, once with every query asked four
    # extra times at every step. All answers must match — observing the farm
    # must not change it. (A certain Lesson 6 code review is the reason this
    # test exists.)
    script: list[tuple] = [
        ("submit", 5, "a"), ("submit", 8, "b"), ("submit", 5, "c"),
        ("add",), ("submit", 2, "d"), ("remove",), ("remove",),
        ("submit", 8, "e"), ("add",),
    ]

    def run(extra_peeks: int) -> list[str | None]:
        farm = BuildFarm(2)
        answers: list[str | None] = []
        for op in script:
            _apply(farm, op)
            for _ in range(extra_peeks):
                farm.weakest_running()
                farm.strongest_waiting()
            answers.append(farm.weakest_running())
            answers.append(farm.strongest_waiting())
        return answers

    clean = run(0)
    peeked = run(4)
    assert clean == peeked, (
        "asking the two queries repeatedly changed later answers — a query "
        f"mutated the farm. Clean run: {clean!r}; with extra peeks: {peeked!r}. "
        "A peek reads heap[0] and touches nothing."
    )


def test_constant_heap_ops_per_call():
    # 1500 submits + 60 slot changes. Budget: a preemption is 3 moves, a slot
    # change is 2 — so anything near 3 per submit is fine and anything that
    # rebuilds or drains a heap inside one call is not.
    rng = random.Random(42)
    prios = [rng.randint(0, 1000) for _ in range(1500)]

    def driver():
        farm = BuildFarm(40)
        for i, p in enumerate(prios):
            farm.submit(p, f"b{i}")
        for _ in range(30):
            farm.add_slot()
        for _ in range(30):
            farm.remove_slot()

    _, counts, _ = _run_counted(driver)
    total = _total_ops(counts)
    assert total <= 3 * 1500 + 2 * 60 + 5, (
        f"{total} heap operations for 1500 submits and 60 slot changes — the "
        "contract is a constant few per call (worst case 3 for a preemption, "
        "2 for a slot change). If you emptied, rebuilt, or re-heapified a "
        "heap inside one call, the boundary design is gone."
    )


def test_stress_against_the_oracle():
    rng = random.Random(17)
    for case in range(300):
        slots = rng.randint(0, 3)
        farm = BuildFarm(slots)
        oracle = _Oracle(slots)
        history: list[tuple] = []
        job_id = 0
        for _ in range(25):
            roll = rng.random()
            if roll < 0.55:
                op: tuple = ("submit", rng.randint(0, 5), f"j{job_id}")
                job_id += 1
            elif roll < 0.75:
                op = ("add",)
            else:
                op = ("remove",)
            history.append(op)
            _apply(farm, op)
            _apply(oracle, op)
            for q in (("q_weak",), ("q_strong",)):
                got, want = _apply(farm, q), _apply(oracle, q)
                assert got == want, (
                    f"case {case} (slots={slots}), after {len(history)} ops "
                    f"{history!r}: {q[0]} gave {got!r}, expected {want!r}"
                )


TESTS = (
    [(f"A — {key}", _make_bound_test(key)) for key in _BOUND_ANSWERS]
    + [
        ("B — the heaps are what hold the jobs", test_farm_uses_a_heap),
        ("B — no wholesale re-ranking", test_farm_does_not_resort),
        ("B — empty farm, zero slots", test_empty_and_trivial),
        ("B — fill, preempt, straight-to-waiting", test_fill_then_preempt),
        ("B — ties: arrival decides, never the name", test_ties_settled_by_arrival_not_name),
        ("B — a crossing re-encodes the tuple", test_crossing_reencodes_the_tuple),
        ("B — the boundary moves both ways", test_boundary_moves),
        ("B — queries do not mutate", test_queries_do_not_mutate),
        ("B — constant heap ops per call (1500 submits)", test_constant_heap_ops_per_call),
        ("B — 300 random cases against an oracle", test_stress_against_the_oracle),
    ]
    + [(f"C — {_PRED_LABELS[key]}", _make_prediction_test(key)) for key in _PRED_LABELS]
)

if __name__ == "__main__":
    print("\nboundary drill — Lesson 7\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green. Here, someone handed you `slots` — the hardware set the")
        print("boundary's position. Ask your teacher what changes when nothing does:")
        print("when the boundary must sit exactly in the middle of the population,")
        print("wherever it grows. That is the last problem, and the only Hard one.\n")
    else:
        print("\nKeep going. Ask your teacher for a hint if you are stuck.\n")
