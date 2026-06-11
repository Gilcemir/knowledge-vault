# Sorting

Stable Timsort under the hood — O(n log n) time, O(n) space for `sorted`, O(1) extra for `.sort()`.

## `sorted` vs `.sort()`

```python
nums = [3, 1, 4, 1, 5, 9]
sorted(nums)                          # [1, 1, 3, 4, 5, 9] — returns NEW list, original untouched
sorted(nums, reverse=True)            # [9, 5, 4, 3, 1, 1]
nums.sort()                           # mutates nums in place, returns None
nums.sort(reverse=True)
```

Use `sorted()` when you need the original preserved or are sorting a non-list iterable (it accepts any iterable and returns a list).

## `key=` — sort by computed value

```python
words = ["banana", "fig", "apple"]
sorted(words)                         # alphabetic
sorted(words, key=len)                # ['fig', 'apple', 'banana'] — by length

points = [(1, 4), (3, 1), (2, 2)]
sorted(points, key=lambda p: p[1])    # by y-coordinate

from operator import itemgetter
sorted(points, key=itemgetter(1))     # same, faster than lambda for the simple case

people = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]
sorted(people, key=lambda x: x["age"])
sorted(people, key=itemgetter("name"))
```

The `key` function is called **once per element** — O(n) calls, not O(n log n). Cache derived values inside the key if expensive.

## Multi-key sort with tuples

```python
intervals = [(1, 5), (1, 3), (2, 4)]
sorted(intervals, key=lambda x: (x[0], x[1]))      # by start asc, then end asc
sorted(intervals, key=lambda x: (x[0], -x[1]))     # by start asc, then end DESC
```

Tuple sorting is lexicographic — left-to-right, element by element. Negate a numeric field for descending order within a single `key`.

For mixed ascending/descending on non-numeric fields, do two stable sorts back-to-back (Timsort is stable):

```python
data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}, {"name": "Alice", "age": 25}]
data.sort(key=lambda x: x["age"], reverse=True)    # age DESC (secondary)
data.sort(key=lambda x: x["name"])                 # name ASC (primary) — stable, preserves age order within ties
```

## `cmp_to_key` — when the order isn't a `key=`

Some orderings compare *pairs* and can't be expressed as a per-element key. Classic case: LC 179 Largest Number — "a before b if `a+b > b+a` as strings":

```python
from functools import cmp_to_key

def largest_number(nums):
    s = list(map(str, nums))
    s.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else 1))
    return str(int("".join(s)))       # int() collapses "00" → "0"

# Comparator contract: return negative (a first), positive (b first), or 0 (tie)
```

Reach for `cmp_to_key` only when you genuinely can't derive a key — `key=` is faster (one call per element vs O(n log n) comparator calls) and clearer.

## `min` / `max` with `key=`

```python
data = [3, 1, 4, 1, 5]
min(data)                             # 1
max(data)                             # 5
max(data, default=None)               # 5 — `default` avoids ValueError on empty iterable
max([], default=0)                    # 0

words = ["fig", "apple", "banana"]
max(words, key=len)                   # 'banana'

# Multiple args (not iterable)
max(3, 7, 2)                          # 7
```

`min`/`max` are O(n) — use them instead of `sorted(...)[0]` (which is O(n log n)).

## `sum`, `len` and averages

```python
data = [3, 1, 4, 1, 5]
sum(data)                             # 14
sum(data) / len(data)                 # 2.8 — average
sum(x * x for x in data)              # 52  — sum over a generator expression

from statistics import mean, median
mean(data)                            # 2.8
median(data)                          # 3
```

## LeetCode patterns

```python
# Sort by frequency then by value (e.g., LC 1636)
from collections import Counter
nums = [1, 1, 2, 2, 2, 3]
cnt = Counter(nums)
nums.sort(key=lambda x: (cnt[x], -x))  # less frequent first, then larger value first

# Sort intervals for merge / sweep
intervals = [[1, 3], [2, 6], [8, 10]]
intervals.sort(key=lambda iv: iv[0])

# K-th largest — DON'T sort the whole array
# heapq.nlargest(k, nums) is O(n log k) — see heapq.md
```

**See also:** [heapq.md](heapq.md) for `nlargest`/`nsmallest` (better than sorting when k ≪ n), [list.md](list.md) for list-specific operations.
