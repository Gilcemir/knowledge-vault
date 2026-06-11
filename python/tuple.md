# tuple

Immutable ordered sequence — hashable if its elements are, which makes it the go-to type for composite keys and grid coordinates.

## Complexity reference

| Operation | Time | Notes |
|---|---|---|
| `t[i]` | O(1) | random access |
| `len(t)` | O(1) | |
| `t1 + t2` | O(n+m) | new tuple |
| `x in t` | O(n) | linear scan |
| `hash(t)` | O(n) | only if all elements are hashable |

## Initialization

```python
t = (1, 2, 3)
t = 1, 2, 3                           # parens optional — comma makes the tuple
t = ()                                # empty tuple
t = (42,)                             # single element — comma required!
t = 42,                               # also a 1-tuple
bad = (42)                            # NOT a tuple — just int 42 in parens
```

The single-element trailing comma is the most common tuple gotcha. `(42)` is parenthesized int; `(42,)` is a 1-tuple.

## Access

```python
t = (1, 2, 3)
t[0]                                  # 1
t[-1]                                 # 3
t[1:]                                 # (2, 3) — slicing returns a new tuple
len(t)                                # 3

# Tuples are immutable
t[0] = 99                             # TypeError
# But elements can be mutable — a tuple of lists is "mutable inside"
mixed = ([1, 2], [3, 4])
mixed[0].append(99)                   # OK — list inside the tuple is mutated
```

## Unpacking

See [iteration.md#unpacking](iteration.md#unpacking) for the full catalog — basic unpack, starred, swap, dict-items, nested. Quick taste:

```python
a, b, c = (1, 2, 3)
x, y = y, x                           # swap without temp
first, *rest = (1, 2, 3, 4)           # first=1, rest=[2,3,4]
```

## Hashability — tuples as dict keys

```python
# Grid coordinates as dict keys / set elements
visited = set()
visited.add((0, 0))
visited.add((1, 2))
(1, 2) in visited                     # True — tuple hash from its elements

# State vectors as memoization keys
from functools import cache

@cache
def solve(i, j, remaining):
    # cache key is (i, j, remaining) — a tuple
    pass

# Counter and freq maps keyed by composite
from collections import Counter
edges = [(0, 1), (1, 2), (0, 1)]
freq = Counter(edges)                 # Counter({(0, 1): 2, (1, 2): 1})
```

A tuple is hashable iff all its elements are. `(1, 2, 3)` is hashable; `(1, [2, 3])` is not (because the inner list isn't).

For unordered composite keys where order shouldn't matter (`{a, b} == {b, a}`), use [set.md#frozenset](set.md#frozenset) instead.

## `namedtuple` — readable composite values

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
p.x, p.y                              # 1, 2 — field access by name
p[0]                                  # 1 — still a tuple (unpacking, hashing all work)
x, y = p                              # unpacks like any tuple

# Typed version — better for non-throwaway code
from typing import NamedTuple

class Event(NamedTuple):
    time: int
    kind: str

e = Event(5, "start")
e.time                                # 5
```

Use it when a bare tuple's positional fields start needing comments (`iv[0]` vs `iv.start`). Immutable and hashable like any tuple — works as dict key.

## LeetCode patterns

```python
# Return multiple values
def divmod_(a, b):
    return a // b, a % b              # implicit tuple
q, r = divmod_(17, 5)                 # q=3, r=2

# Iterate (index, value) — tuple unpacking from enumerate
for i, val in enumerate(nums):
    pass

# Priority queue with (priority, value) tuples — see heapq.md
import heapq
pq = []
heapq.heappush(pq, (3, "task"))
heapq.heappush(pq, (1, "urgent"))
priority, task = heapq.heappop(pq)    # (1, "urgent")
```

**See also:** [iteration.md#unpacking](iteration.md#unpacking) for unpacking idioms, [heapq.md](heapq.md) for tuple-keyed priority queues, [dict.md](dict.md) for hashable-tuple-keyed dicts.
