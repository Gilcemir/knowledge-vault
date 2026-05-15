# heapq

Min-heap operations on a plain `list` — O(log n) push/pop, O(1) peek-min. The module is functions-on-a-list, not a class.

## Complexity reference

| Operation | Time | Notes |
|---|---|---|
| `heappush(h, x)` | O(log n) | |
| `heappop(h)` | O(log n) | pops min |
| `h[0]` (peek min) | O(1) | h is just a list |
| `heapify(lst)` | O(n) | turn an arbitrary list into a heap, in place |
| `heapreplace(h, x)` | O(log n) | pop min + push x (one pass) |
| `heappushpop(h, x)` | O(log n) | push x + pop min (pushed item may be the popped) |
| `nlargest(k, iter)` | O(n log k) | beats `sorted(iter)[-k:]` (O(n log n)) when k ≪ n |
| `nsmallest(k, iter)` | O(n log k) | |

## Min-heap

```python
import heapq

h = []
heapq.heappush(h, 3)                  # O(log n)
heapq.heappush(h, 1)
heapq.heappush(h, 2)

top = h[0]                            # 1    peek min   O(1)
val = heapq.heappop(h)                # 1    pop min    O(log n)
```

The underlying list is *not* sorted — only the heap invariant holds (parent ≤ children). Don't iterate `h` expecting sorted order.

## Heapify an existing list

```python
import heapq

nums = [5, 3, 8, 1, 4]
heapq.heapify(nums)                   # O(n) — faster than n pushes (O(n log n))
heapq.heappop(nums)                   # 1
```

`heapify` is in-place. Always preferred over repeated `heappush` when you already have the data.

## Max-heap — negate values

`heapq` is min-only. For max-heap behavior, store negatives:

```python
import heapq

h = []
heapq.heappush(h, -3)                 # push -value
heapq.heappush(h, -1)
heapq.heappush(h, -5)
max_val = -h[0]                       # 5      peek max
val = -heapq.heappop(h)               # 5      pop max
```

For object payloads, see the tiebreak pattern below.

## Tuples as priority — with a tiebreaker

```python
import heapq

# (priority, value) — Python compares tuples lexicographically
pq = []
heapq.heappush(pq, (3, "low"))
heapq.heappush(pq, (1, "urgent"))
priority, task = heapq.heappop(pq)    # (1, "urgent")

# Problem: when priorities tie, Python tries to compare the values.
# If the values aren't comparable (e.g., custom objects), this errors.
# Solution: insert a unique tiebreaker.
import itertools
counter = itertools.count()           # 0, 1, 2, ...

heapq.heappush(pq, (priority, next(counter), task_obj))
# Tuples: (priority, sequence_num, value)
# - Sequence_num breaks priority ties.
# - task_obj is never compared (sequence_num is always unique).
```

The `(priority, tiebreak, value)` pattern is essential when `value` isn't comparable (e.g., dicts, custom objects). It also makes the order deterministic (FIFO within a priority).

## `nlargest` / `nsmallest`

```python
import heapq

nums = [5, 2, 8, 1, 9, 3]
heapq.nlargest(3, nums)               # [9, 8, 5]
heapq.nsmallest(3, nums)              # [1, 2, 3]

# With key=
words = ["apple", "kiwi", "banana"]
heapq.nlargest(2, words, key=len)     # ['banana', 'apple']
```

For small k relative to n (k ≪ n), `nlargest(k, ...)` is O(n log k) — faster than `sorted(...)[-k:]` (O(n log n)).

## LeetCode patterns

```python
import heapq

# K-th largest element — running min-heap of size k
def find_kth_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)          # drop smallest; root is always the k-th largest seen
    return h[0]
# O(n log k) time, O(k) space

# Dijkstra's algorithm
def dijkstra(graph, src):
    dist = {src: 0}
    pq = [(0, src)]                   # (distance, node)
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float('inf')):
            continue                  # stale entry
        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

# Merge k sorted lists — one entry per list in the heap
def merge_k_sorted(lists):
    h = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(h, (lst[0], i, 0))
    out = []
    while h:
        val, i, j = heapq.heappop(h)
        out.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(h, (lists[i][j + 1], i, j + 1))
    return out
# O(N log k) where N is total elements
```

**See also:** [sorting.md](sorting.md) for full sorts (heaps win when you only need top-k or partial ordering), [deque.md](deque.md) for non-priority queues.
