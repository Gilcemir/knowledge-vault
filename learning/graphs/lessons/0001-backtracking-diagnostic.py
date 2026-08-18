"""
D0 — Backtracking cold diagnostic (pre-flight for the Graphs track).

WHY THIS EXISTS
    You finished the Backtracking node via LeetCode's tutorial. DFS on
    graphs — the engine of this whole track — IS backtracking wearing a
    different hat. Before building on it, we measure what actually stuck.
    This is a measurement, not an exam: red cells trigger ONE targeted
    patch lesson, never a redo of the node.

HOW TO USE THIS FILE
    1. CLOSED-BOOK: no tutorial, no old code, no searching. First pass
       on paper. Wrong answers are the data we are here to collect.
    2. Part P: trace the two functions on paper, then fill PREDICTIONS.
    3. Part K: fill every KNOWLEDGE cell with one of its allowed answers,
       spelled exactly as listed in the comment above it.
    4. Run it, from the repo root:
           python3.14 learning/graphs/lessons/0001-backtracking-diagnostic.py
    5. REPORT YOUR FIRST-PASS RESULT VERBATIM to your teacher — reds
       included. (The heap capstone's first-pass reds went unrecorded;
       we are not repeating that.)

There are no solutions in this file.
"""


# ----------------------------------------------------------------------------
# PART P — two traces (paper first)
# ----------------------------------------------------------------------------
#
#   P1: what does f([1, 2]) return? Answer with the full list of lists,
#       in the exact order produced, e.g. [[1], [2]].
#
#       def f(nums):
#           res, path = [], []
#           def dfs(i):
#               if i == len(nums):
#                   res.append(path.copy())
#                   return
#               path.append(nums[i])
#               dfs(i + 1)
#               path.pop()
#               dfs(i + 1)
#           dfs(0)
#           return res
#
#   P2: same function, ONE change — the leaf line is now
#               res.append(path)          # no .copy()
#       What does f([1, 2]) return now? Same answer format.

PREDICTIONS: dict[str, list | None] = {
    "P1": [[1, 2], [1], [2], []],
    "P2": [[], [], [], []],
}


# ----------------------------------------------------------------------------
# PART K — seven knowledge cells
# ----------------------------------------------------------------------------
#
# K1 "subsets_leaves" — the recursion tree of P1 on n DISTINCT items:
#     how many LEAVES does it have? One of (exactly):
#     "2^n"   "n!"   "n^2"   "2*n"
#
# K2 "perms_leaves" — the recursion tree that generates every PERMUTATION
#     of n distinct items: how many leaves? Same four options as K1.
#
# K3 "undo_step" — the `path.pop()` line exists to restore... One of:
#     "the result list, so duplicates are removed at the end"
#     "the input list, so recursion sees the original order"
#     "the shared path, so the next branch starts from the same state"
#     "the call stack, so the function can return early"
#
# K4 "copy_reason" — why the leaf must append `path.copy()`. One of:
#     "copy makes the recursion terminate at the base case"
#     "append stores a reference and the list keeps mutating"
#     "append stores a snapshot but only of the first level"
#     "copy prevents the pop from raising on an empty list"
#
# K5 "prune_rule" — a CORRECT prune may skip only branches that... One of:
#     "look expensive compared to their sibling branches"
#     "have already produced one answer somewhere below"
#     "are deeper than the average depth of the tree"
#     "cannot lead to any valid answer from this state"
#
# K6 "used_marker" — in permutations, what prevents picking the same
#     element twice, and when is it released? One of:
#     "a used flag per element, cleared when the call backtracks"
#     "a used flag per element, cleared only at the base case"
#     "a global counter of choices, reset between siblings"
#     "the recursion depth itself, compared against the index"
#
# K7 "subsets_total_cost" — TOTAL work to generate all subsets of n items,
#     including materializing each one at the leaf. One of (exactly):
#     "O(2^n)"   "O(n * 2^n)"   "O(n^2)"   "O(n!)"

KNOWLEDGE: dict[str, str | None] = {
    "subsets_leaves": "2^n",
    "perms_leaves": "n!",
    "undo_step": "the shared path, so the next branch starts from the same state",
    "copy_reason": "append stores a reference and the list keeps mutating",
    "prune_rule": "cannot lead to any valid answer from this state",
    "used_marker": "a used flag per element, cleared when the call backtracks",
    "subsets_total_cost": "O(n * 2^n)",
}


# ============================================================================
# TEST HARNESS — do not edit below this line.
# ============================================================================

_COUNTS = {"2^n", "n!", "n^2", "2*n"}
_UNDO = {
    "the result list, so duplicates are removed at the end",
    "the input list, so recursion sees the original order",
    "the shared path, so the next branch starts from the same state",
    "the call stack, so the function can return early",
}
_COPY = {
    "copy makes the recursion terminate at the base case",
    "append stores a reference and the list keeps mutating",
    "append stores a snapshot but only of the first level",
    "copy prevents the pop from raising on an empty list",
}
_PRUNE = {
    "look expensive compared to their sibling branches",
    "have already produced one answer somewhere below",
    "are deeper than the average depth of the tree",
    "cannot lead to any valid answer from this state",
}
_USED = {
    "a used flag per element, cleared when the call backtracks",
    "a used flag per element, cleared only at the base case",
    "a global counter of choices, reset between siblings",
    "the recursion depth itself, compared against the index",
}
_COSTS = {"O(2^n)", "O(n * 2^n)", "O(n^2)", "O(n!)"}

_K_ALLOWED = {
    "subsets_leaves": _COUNTS, "perms_leaves": _COUNTS,
    "undo_step": _UNDO, "copy_reason": _COPY, "prune_rule": _PRUNE,
    "used_marker": _USED, "subsets_total_cost": _COSTS,
}

_K_ANSWERS = {
    "subsets_leaves": "2^n",
    "perms_leaves": "n!",
    "undo_step": "the shared path, so the next branch starts from the same state",
    "copy_reason": "append stores a reference and the list keeps mutating",
    "prune_rule": "cannot lead to any valid answer from this state",
    "used_marker": "a used flag per element, cleared when the call backtracks",
    "subsets_total_cost": "O(n * 2^n)",
}

_K_HINTS = {
    "subsets_leaves": (
        "Each element makes one binary decision — in or out. Count the "
        "leaves, not the internal nodes."
    ),
    "perms_leaves": (
        "First slot: n choices. Second: n - 1. Keep going, then multiply."
    ),
    "undo_step": (
        "path is ONE list shared by every call in the tree. What must be "
        "true of it at the moment the exclude-branch begins?"
    ),
    "copy_reason": (
        "P2 is this cell, demonstrated live. Look at what res actually "
        "held when the run ended."
    ),
    "prune_rule": (
        "A prune is a proof, not a preference: skipping is legal only when "
        "no valid answer can exist below the skipped branch."
    ),
    "used_marker": (
        "If the flag is not released on the way back UP, the sibling branch "
        "never gets to use that element at all."
    ),
    "subsets_total_cost": (
        "How many leaves, and how much copying does EACH leaf pay? "
        "Multiply — the copies are not free."
    ),
}

_K_LABELS = {
    "subsets_leaves": "K1 — subsets tree: leaves",
    "perms_leaves": "K2 — permutations tree: leaves",
    "undo_step": "K3 — what the pop restores",
    "copy_reason": "K4 — why copy at the leaf",
    "prune_rule": "K5 — when a prune is legal",
    "used_marker": "K6 — the used flag and its release",
    "subsets_total_cost": "K7 — total subsets cost",
}


def _subsets(nums: list[int], snapshot: bool) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []

    def dfs(i: int) -> None:
        if i == len(nums):
            res.append(path.copy() if snapshot else path)
            return
        path.append(nums[i])
        dfs(i + 1)
        path.pop()
        dfs(i + 1)

    dfs(0)
    return res


_P_ORACLES = {
    "P1": lambda: _subsets([1, 2], snapshot=True),
    "P2": lambda: _subsets([1, 2], snapshot=False),
}
_P_LABELS = {
    "P1": "P1 — subsets, traced",
    "P2": "P2 — the missing copy, traced",
}
_P_HINTS = {
    "P1": (
        "Follow the code's order, not sorted order: the include-branch "
        "recurses BEFORE the exclude-branch."
    ),
    "P2": (
        "Every append stored the SAME list object. What does that one "
        "object contain after the last pop has run?"
    ),
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
        assert got == want, (
            f"you predicted {got!r}; the code produces {want!r}. "
            f"Hint: {_P_HINTS[key]}"
        )
    return test


def _make_knowledge_test(key):
    def test():
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


TESTS = (
    [(_P_LABELS[key], _make_prediction_test(key)) for key in _P_ORACLES]
    + [(_K_LABELS[key], _make_knowledge_test(key)) for key in _K_ANSWERS]
)

if __name__ == "__main__":
    print("\nbacktracking cold diagnostic — D0\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not attempted")
    if failed == 0 and todo == 0:
        print("\nAll green — backtracking is load-bearing. Tell your teacher:")
        print("L1 (graph anatomy) is next, no patch lesson needed.\n")
    else:
        print("\nReport this output to your teacher VERBATIM, reds included.")
        print("Each red names exactly what the one patch lesson will cover;")
        print("primary source meanwhile: Erickson, Algorithms, ch. 2.\n")
