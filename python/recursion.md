# Recursion & Memoization

`@cache` for DP, the recursion-limit gotcha, and closure capture (`nonlocal`) — the plumbing behind every recursive LeetCode solution.

## `@cache` — memoization in one line

```python
from functools import cache

@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

fib(100)                              # instant — each n computed once
fib.cache_clear()                     # reset between test cases if needed
```

`@cache` (3.9+) is `lru_cache(maxsize=None)` — an unbounded dict keyed by the arguments. It turns exponential naive recursion into O(states) DP with zero bookkeeping.

```python
# don't: hand-rolled memo dict — works, but it's boilerplate @cache replaces
memo = {}
def fib_manual(n):
    if n in memo:
        return memo[n]
    result = n if n < 2 else fib_manual(n - 1) + fib_manual(n - 2)
    memo[n] = result
    return result
```

## Arguments must be hashable

The cache key is the argument tuple — every argument must be hashable:

```python
@cache
def solve(nums, i):                   # TypeError if nums is a list!
    ...

# Fix 1: convert once at the boundary
def solve_list(nums):
    return solve(tuple(nums), 0)      # tuples are hashable — see tuple.md

# Fix 2: close over the data instead of passing it (preferred in LC)
def solve_list(nums):
    @cache
    def dp(i):                        # only the INDEX is a cache key
        ...
    return dp(0)
```

Closing over the input (Fix 2) is the standard LC shape — define the cached helper *inside* the solution function so the cache dies with the call (no state leaking between test cases).

## Recursion limit — the silent TLE/RecursionError

CPython's default recursion limit is ~1000 frames. A DFS over an input of n = 10⁴ (linked lists, deep trees, path-shaped graphs) blows it:

```python
import sys
sys.setrecursionlimit(10**6)          # standard first line in deep-recursion LC solutions
```

Raising the limit fixes `RecursionError`, but each frame still costs memory and time. When depth is a real concern, convert to iteration:

```python
# Recursive DFS → iterative DFS with an explicit stack
def dfs_iter(start, graph):
    visited = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for nbr in graph[node]:
            if nbr not in visited:
                visited.add(nbr)
                stack.append(nbr)
```

## `nonlocal` — mutating an outer variable from a closure

Assigning to a name inside a function makes it local. To rebind a variable of the *enclosing* function, declare it `nonlocal`:

```python
def diameter_of_tree(root):
    best = 0
    def depth(node):
        nonlocal best                 # without this, `best = ...` creates a NEW local
        if not node:
            return 0
        l, r = depth(node.left), depth(node.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    depth(root)
    return best
```

Alternative without `nonlocal` — a single-element list as mutable cell (mutating isn't rebinding, so no declaration needed):

```python
best = [0]
def depth(node):
    ...
    best[0] = max(best[0], l + r)     # see list.md#leetcode-patterns
```

Both are idiomatic; `nonlocal` reads better for scalars, the list cell predates it and still shows up in solutions.

## LeetCode patterns

```python
from functools import cache

# Top-down DP — grid paths (LC 62)
def unique_paths(m, n):
    @cache
    def dp(r, c):
        if r == 0 or c == 0:
            return 1
        return dp(r - 1, c) + dp(r, c - 1)
    return dp(m - 1, n - 1)

# Memoized recursion over two sequences (LC 1143 LCS)
def lcs(s, t):
    @cache
    def dp(i, j):
        if i == len(s) or j == len(t):
            return 0
        if s[i] == t[j]:
            return 1 + dp(i + 1, j + 1)
        return max(dp(i + 1, j), dp(i, j + 1))
    return dp(0, 0)

# Backtracking template — build, recurse, undo
def subsets(nums):
    out, path = [], []
    def bt(i):
        out.append(path[:])           # snapshot — path keeps mutating! (see list.md copy)
        for j in range(i, len(nums)):
            path.append(nums[j])
            bt(j + 1)
            path.pop()                # undo
    bt(0)
    return out
```

**See also:** [tuple.md#hashability--tuples-as-dict-keys](tuple.md) for cache-key hashability, [dict.md](dict.md) for hand-rolled memo tables, [list.md](list.md) for the mutable-cell pattern and `path[:]` snapshots.
