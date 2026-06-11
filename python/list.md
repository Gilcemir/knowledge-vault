# list

Ordered, mutable, contiguous sequence — the default LeetCode container.

## Complexity reference

| Operation | Time | Notes |
|---|---|---|
| `nums[i]` | O(1) | random access |
| `nums[-1]` | O(1) | |
| `len(nums)` | O(1) | |
| `nums.append(x)` | O(1) | amortized — occasional resize |
| `nums.pop()` | O(1) | from the end |
| `nums.insert(0, x)` | O(n) | shifts everything right; use [deque.md](deque.md) for front-ops |
| `nums.pop(0)` | O(n) | same — use `deque.popleft()` |
| `nums.pop(i)` | O(n) | shifts tail left |
| `nums.remove(x)` | O(n) | linear scan + shift |
| `x in nums` | O(n) | for membership use a `set` (see [set.md](set.md)) |
| `nums.index(x)` | O(n) | |
| `nums.count(x)` | O(n) | |
| `nums[i:j]` | O(j−i) | copy, O(j−i) space |
| `nums + other` | O(n+k) | new list — see Concatenate & repeat |
| `nums.extend(other)` | O(k) | in-place |
| `nums.copy()` | O(n) | shallow copy |
| `nums.sort()` | O(n log n) | Timsort, in-place — see [sorting.md](sorting.md) |
| `sorted(nums)` | O(n log n) | returns new list, O(n) extra space |
| `nums.reverse()` | O(n) | in-place |
| `nums[::-1]` | O(n) | new reversed list |

## Initialization

```python
nums = []
nums = [1, 2, 3]
nums = list(range(5))                 # [0, 1, 2, 3, 4]
nums = [0] * n                        # n zeros — common for DP 1D arrays
seen = [False] * len(grid)
```

## Concatenate & repeat

```python
a = [1, 2, 3]
b = [4, 5, 6]

c = a + b                             # [1,2,3,4,5,6] — NEW list, a/b untouched   O(n+k)
a += b                                # same as a.extend(b) — mutates a in place
a.extend(b)                           # in-place, O(k)
[0, 1] * 3                            # [0, 1, 0, 1, 0, 1] — repetition
```

`+` vs `extend`:

```python
# extend mutates and returns None — classic trap:
x = a.extend(b)                       # x is None, NOT the list!

# + builds a new list — fine for small data, wasteful in a loop:
# don't: O(n²) — each + recopies everything accumulated so far
res = []
for chunk in chunks:
    res = res + chunk

# do: O(total) amortized
res = []
for chunk in chunks:
    res.extend(chunk)
```

Note `a += b` is `extend` (in-place), not `a = a + b` (rebind to a new list) — the difference is visible when another variable aliases `a`.

## Copy & aliasing

```python
a = [1, 2, 3]

b = a                                 # NO copy — both names point to the same list
b.append(4)                           # a is now [1, 2, 3, 4] too

b = a.copy()                          # shallow copy — independent top level
b = a[:]                              # same
b = list(a)                           # same

# Shallow means nested objects are still shared:
grid = [[1, 2], [3, 4]]
g2 = grid.copy()
g2[0].append(9)                       # grid[0] is now [1, 2, 9] — inner lists shared!

import copy
g3 = copy.deepcopy(grid)              # fully independent — O(total elements)
```

Rule of thumb: copies of flat lists of ints/strs are safe with `.copy()`/`[:]`; anything nested (matrices, lists of lists in backtracking) needs `deepcopy` or a per-row copy like `[row[:] for row in grid]`.

## 2D arrays — row aliasing trap

```python
# don't: all rows alias the SAME list — assigning to dp[0][0] mutates every row
m, n = 3, 4
dp = [[0] * n] * m
dp[0][0] = 1
# now dp == [[1,0,0,0], [1,0,0,0], [1,0,0,0]]   ← silent bug

# do: build independent rows
dp = [[0] * n for _ in range(m)]
dp[0][0] = 1
# dp == [[1,0,0,0], [0,0,0,0], [0,0,0,0]]       ← correct
```

This is the single most common silent-wrong bug in LC matrix problems. The list comprehension creates a fresh inner list per iteration; the `*` operator copies the same reference `m` times.

## Mutate

```python
nums = [3, 1, 4, 1, 5]
nums.append(9)                        # [3,1,4,1,5,9]      O(1) amortized
nums.extend([7, 8])                   # [3,1,4,1,5,9,7,8]  O(k)
nums.insert(0, 99)                    # O(n) — prefer deque for front-ops
nums.pop()                            # 8, list now ends 9,7         O(1)
nums.pop(0)                           # 99 — costs O(n) shift
nums.remove(1)                        # removes FIRST occurrence     O(n)
nums.clear()                          # []

del nums[0]                           # remove by index, no return   O(n)
del nums[1:3]                         # remove a slice in place
```

`pop(i)` returns the removed value; `del nums[i]` doesn't — use `del` when you don't need it, and `remove(x)` when you know the value but not the index.

## Access & search

```python
nums = [3, 1, 4, 1, 5]
nums[0]                               # 3            — first
nums[-1]                              # 5            — last
nums[1:3]                             # [1, 4]       — slice (new list)
nums.index(4)                         # 2            — position; raises if absent
nums.count(1)                         # 2            — occurrences
4 in nums                             # True         — O(n); use a set if hot
```

## Aggregations

```python
nums = [3, 1, 4, 1, 5]
sum(nums)                             # 14                           O(n)
min(nums)                             # 1   — raises on empty list; min(nums, default=0)
max(nums)                             # 5
max(nums, key=abs)                    # element with largest |x|

any(x > 4 for x in nums)              # True  — short-circuits
all(x > 0 for x in nums)              # True

# argmax — index of the largest element
i = max(range(len(nums)), key=nums.__getitem__)   # 4
```

## Membership — the set trick

```python
# don't: O(n) lookup inside a loop → O(n²) total
def has_duplicate_slow(nums):
    seen = []
    for x in nums:
        if x in seen:                 # O(n) per check
            return True
        seen.append(x)
    return False

# do: O(1) lookup → O(n) total
def has_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:                 # O(1) avg
            return True
        seen.add(x)
    return False
```

## Slicing

```python
nums = [0, 1, 2, 3, 4, 5]
nums[2:5]        # [2, 3, 4]
nums[:3]         # [0, 1, 2]
nums[3:]         # [3, 4, 5]
nums[::2]        # [0, 2, 4]    — every other element
nums[::-1]       # [5,4,3,2,1,0] — reversed copy

# Assign to a slice (replaces the slice in place)
nums[1:3] = [9, 9, 9]                 # nums == [0, 9, 9, 9, 3, 4, 5]
nums[:] = []                          # clears in place (preserves identity)
```

## List comprehension

```python
squares = [x * x for x in range(5)]                           # [0, 1, 4, 9, 16]
evens = [x for x in nums if x % 2 == 0]                       # filter
matrix = [[r * c for c in range(3)] for r in range(3)]        # nested → 2D

# Flatten one level
nested = [[1, 2], [3, 4], [5]]
flat = [x for row in nested for x in row]                     # [1, 2, 3, 4, 5]
```

**See also:** [iteration.md#comprehensions](iteration.md#comprehensions) for comprehension mechanics across all container types (dict, set, generator).

## Stack via list

```python
stack = []
stack.append(1)                       # push   O(1)
stack.append(2)
top = stack[-1]                       # peek   O(1)
val = stack.pop()                     # pop    O(1)
if not stack:                         # empty check
    pass
```

A plain list is fine for typical DFS/parsing stacks. For performance-critical or unbounded-depth stacks, [deque.md](deque.md) is slightly more consistent.

## LeetCode patterns

```python
# Backtracking — single-element list as mutable cell
def count_paths(grid):
    res = [0]
    def dfs(r, c):
        if (r, c) == (len(grid) - 1, len(grid[0]) - 1):
            res[0] += 1               # mutate inner element — no `nonlocal` needed
            return
        # ...
    dfs(0, 0)
    return res[0]

# Prefix sums
nums = [1, 2, 3, 4]
prefix = [0] * (len(nums) + 1)
for i, x in enumerate(nums):
    prefix[i + 1] = prefix[i] + x     # prefix[i+1] = sum(nums[:i+1])

# In-place reverse a portion (LC 189-style rotations)
def reverse(nums, lo, hi):
    while lo < hi:
        nums[lo], nums[hi] = nums[hi], nums[lo]
        lo += 1
        hi -= 1
```

**See also:** [sorting.md](sorting.md) for `key=` patterns, [iteration.md](iteration.md) for `enumerate`/`zip`/unpacking, [deque.md](deque.md) for O(1) front-ops.
