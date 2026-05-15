# Binary Search

Four templates for searching a sorted array (or any monotonic predicate) in O(log n) — pick by what question you're answering.

## Exact match

```python
def exact_match(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:                   # includes lo == hi (one-element case)
        mid = lo + (hi - lo) // 2     # safe form (vs (lo+hi)//2 — habit from other langs)
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1              # mid and left are all smaller — discard
        else:
            hi = mid - 1              # mid and right are all larger — discard
    return -1                         # not found
```

Loop condition is `lo <= hi` because with one element remaining (`lo == hi`) we still need to check it. Returns `-1` if absent. O(log n) time, O(1) space.

## Lower bound — first index with `arr[i] >= target`

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)              # hi = len (one past the end!)
    while lo < hi:                    # lo == hi → converged
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1              # mid is False — discard
        else:
            hi = mid                  # mid might be the answer — keep it
    return lo                         # lo == hi == answer (or len if all < target)
```

`hi = len(arr)` lets the function return `len(arr)` when `target` is greater than every element. `hi = mid` (not `mid - 1`) because `mid` could itself be the first valid index.

## Upper bound — first index with `arr[i] > target`

```python
def upper_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= target:        # only difference from lower_bound
            lo = mid + 1
        else:
            hi = mid
    return lo
```

Combined use: `[lower_bound(t), upper_bound(t))` is the half-open range of all occurrences of `t`. Count: `upper_bound(t) - lower_bound(t)`.

## Pythonic substitute — `bisect`

Don't hand-roll lower/upper bound when the stdlib already has it:

```python
from bisect import bisect_left, bisect_right

bisect_left(arr, target)              # == lower_bound(arr, target)
bisect_right(arr, target)             # == upper_bound(arr, target)

# count occurrences of target in a sorted list
count = bisect_right(arr, target) - bisect_left(arr, target)

# insertion point to keep list sorted
from bisect import insort
insort(arr, x)                        # O(log n) search + O(n) shift
```

Use `bisect_left` for the "first index ≥ target" question, `bisect_right` for "first index > target". Both are O(log n).

## Search on answer — binary search over a value range

```python
def search_on_answer(lo, hi, f):
    # Invariant: answer always in [lo, hi]
    while lo < hi:                    # lo == hi → converged on the boundary
        mid = lo + (hi - lo) // 2
        if f(mid):
            hi = mid                  # mid satisfies; maybe smaller works too
        else:
            lo = mid + 1              # mid doesn't satisfy — discard
    return lo                         # smallest x with f(x) True
```

**Precondition:** `f` must be monotonic — once `f(x)` becomes True, `f(x+1)`, `f(x+2)`, … are all True. Without monotonicity binary search doesn't apply.

### Example: Koko Eating Bananas (LeetCode 875)

```python
# runnable
from math import ceil

def min_eating_speed(piles, h):
    def can_finish(k):                # f(k): can Koko eat all in h hours at speed k?
        return sum(ceil(p / k) for p in piles) <= h

    lo, hi = 1, max(piles)            # speed range: 1 to the largest pile
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_finish(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

assert min_eating_speed([3, 6, 7, 11], 8) == 4
assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
```

## Comparison table

| Technique | Loop | `hi` init | If True | If False | Returns |
|---|---|---|---|---|---|
| Exact match | `lo <= hi` | `len - 1` | return `mid` | `lo=mid+1` or `hi=mid-1` | `-1` if absent |
| Lower bound | `lo < hi` | `len` | `hi = mid` | `lo = mid + 1` | `lo` |
| Upper bound | `lo < hi` | `len` | `hi = mid` | `lo = mid + 1` | `lo` |
| Search on answer | `lo < hi` | problem domain | `hi = mid` | `lo = mid + 1` | `lo` |
