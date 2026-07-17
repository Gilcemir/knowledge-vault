# Backtracking

Notes and gotchas collected while studying backtracking. Language-agnostic pattern; examples in Python. Grows as I go.

## Mental model — reason about the current call, before recursing

Trying to picture the whole recursion tree at once is what makes backtracking feel hard. Instead, reason locally about *one call*: "I just arrived at a node — what must happen **here**, before I recurse?" Everything interesting happens at the top of the function, before the loop over children:

1. **Is this node an answer?** Subsets: yes, always → `res.append(path[:])` unconditionally, first line.
2. **Is this node a dead end?** Combination Sum: the running total overshot the target → no descendant can fix it → `return`. Subsets has no such check *precisely because* every node is an answer — there is nothing to short-circuit.
3. **Which children do I even generate?** Skip a duplicate sibling (`i > start and nums[i] == nums[i - 1]`), or `break` a sorted tail that can't fit.

Once the current node is handled, the recursive call takes care of the entire subtree below — you don't have to think about it. If you find yourself mentally simulating three levels deep, come back to the node in front of you and ask those three questions.

## The start-index decision — `i` vs `i + 1`

In combination-style backtracking, the single parameter that controls "can I reuse an element?" is what you pass as `start` in the recursive call:

| Problem allows...                       | Recursive call     | Why                                                       |
|-----------------------------------------|--------------------|-----------------------------------------------------------|
| Reusing the same element many times     | `solve(..., i)`    | The next level may pick index `i` again                   |
| Each element used at most once          | `solve(..., i + 1)`| The next level starts *after* the current index           |

### Combination Sum (LC 39) — unlimited reuse → recurse with `i`

```python
class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        res = []

        def solve(l: List[int], start: int, target: int) -> None:
            if target < 0:
                return
            if target == 0:
                res.append(l[:])
                return

            for i in range(start, len(nums)):
                l.append(nums[i])
                solve(l, i, target - nums[i])   # i, NOT i + 1 — current element may repeat
                l.pop()

        solve([], 0, target)
        return res
```

Passing `i` (not `i + 1`) is what lets `[2, 2, 3]` emerge from a single `2` in the input. Passing `start` at all (instead of always `0`) is what prevents permutation duplicates like `[2, 3, 2]` — combinations only ever look forward.

## Duplicates in the input — skip siblings, keep children

Combination Sum II (LC 40): each element used at most once, but the *input* may contain duplicates (e.g. `[1, 1, 6]`). Two copies of `1` are legitimately usable together — yet two *sibling* branches starting with `1` at the same level would produce identical result sets.

The fix: at each level, skip an element equal to its left neighbor **unless it's the first choice of that level**:

```python
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []

        candidates.sort()                 # REQUIRED — see below

        def solve(l: list[int], start: int, target: int) -> None:
            if target == 0:
                res.append(l[:])
                return

            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue              # duplicate SIBLING at this level — already explored
                if candidates[i] > target:
                    break                 # sorted → everything to the right is too big

                l.append(candidates[i])
                solve(l, i + 1, target - candidates[i])   # i + 1 — no reuse
                l.pop()

        solve([], 0, target)
        return res
```

### Why `i > start` and not `i > 0`

`i > 0` is not merely wasteful — it is **wrong**. Trace `[1, 1, 6]`, target 8:

1. Level 0 picks `i = 0` (first `1`). Recurse with `start = 1`, target 7.
2. Level 1 reaches `i = 1` (second `1`). Here `i == start`, so `i > start` is false → **not skipped**, and `[1, 1, 6]` is found. ✓
3. With `i > 0` instead: `1 > 0` is true and `candidates[1] == candidates[0]` → the second `1` is skipped → `[1, 1, 6]` is never produced. ✗

`start` is what distinguishes the two cases:

- `i == start` → first choice of this level = the *continuation* of the previous copy (deeper in the tree). Duplicate allowed.
- `i > start` → a *sibling* branch at the same level that would rebuild an already-explored subtree. Skip it.

## Subsets — no base case with `return`; every node is an answer

Subsets / Subsets II (LC 78/90): the instinct, by analogy with other backtracking problems, is to look for a short-circuit condition (`if ...: return`) as the base case. Here there isn't one. Unlike Combination Sum (which returns when the sum overshoots the target) or constrained permutations, in subsets **every node of the recursion tree is already a valid subset**. That's why the first line of the function is `res.append(path[:])` — the current state always counts as an answer; there is nothing to prune.

Why an explicit `return` is redundant: `if start == len(nums): return` breaks nothing, but does nothing — when `start == len(nums)`, `range(start, len(nums))` is already empty, the `for` doesn't iterate, and the function returns on its own after the append. Placing the `return` *before* the append would be worse: it would drop the full subset.

**Rule of thumb:** the base case is implicit in the `for` that runs dry. If every node is an answer → append at the top of the function, no `return`. Only use a pruning `return` when there is a state from which continuing is provably useless (sum overshot, constraint violated).

### Subsets II (LC 90) — minimal example

```python
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res = []

        nums.sort()                       # required for the sibling-dedup skip

        def solve(path: list[int], start: int) -> None:
            res.append(path[:])           # every node is valid — no return

            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:
                    continue              # duplicate SIBLING at this level — already explored

                path.append(nums[i])
                solve(path, i + 1)
                path.pop()

        solve([], 0)
        return res
```

Contrast — when the `return` *does* exist: Combination Sum → `if total > target: return`. There, continuing past the overshoot is provably useless, so pruning applies.

## Sorting — correctness prerequisite vs pruning bonus

Two distinct reasons to sort, easy to conflate:

1. **Correctness (CS II):** the `candidates[i] == candidates[i - 1]` skip only works if duplicates are *adjacent*. Without sorting, the dedup silently fails and duplicated results come back. Sorting here is not optional.
2. **Pruning (both problems):** once sorted, `candidates[i] > target` means every later candidate is also too big → `break` short-circuits the whole rest of the level. Nice speedup, but the solution would still be correct without it (the `target < 0` guard catches overshoot).
