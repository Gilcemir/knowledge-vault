# deque

Double-ended queue — O(1) append and pop on **both** ends. Reach for it whenever you need a queue, a sliding window, or a stack that you'll push/pop from either side.

## Complexity reference

| Operation | Time | Notes |
|---|---|---|
| `q.append(x)` | O(1) | right end |
| `q.appendleft(x)` | O(1) | left end |
| `q.pop()` | O(1) | right end |
| `q.popleft()` | O(1) | left end — the BFS workhorse |
| `q[0]` / `q[-1]` | O(1) | peek front/back |
| `q[i]` (middle) | O(n) | NOT random-access optimal — use `list` if you need that |
| `x in q` | O(n) | |
| `len(q)` | O(1) | |
| `q.rotate(k)` | O(k) | shift k positions; negative k rotates left |
| `q.extend(iter)` / `q.extendleft(iter)` | O(k) | `extendleft` reverses element order! |

## Initialization

```python
from collections import deque

q = deque()
q = deque([1, 2, 3])
q = deque("abc")                      # deque(['a', 'b', 'c'])
q = deque(maxlen=3)                   # bounded — see Sliding window below
```

## Basic operations

```python
from collections import deque

q = deque()
q.append(1)           # right          deque([1])
q.append(2)           #                deque([1, 2])
q.appendleft(0)       # left           deque([0, 1, 2])
q.popleft()           # → 0            deque([1, 2])    O(1)
q.pop()               # → 2            deque([1])       O(1)

q[0]                  # peek front
q[-1]                 # peek back
not q                 # is-empty check (False if any elements)
len(q) == 0           # explicit empty check
```

## Why deque beats `list` for queues

```python
# don't: O(n) per dequeue → O(n²) total for BFS
queue = []
queue.append(x)
queue.pop(0)                          # O(n) — shifts every remaining element

# do: O(1) per dequeue → O(n) total
from collections import deque
queue = deque()
queue.append(x)
queue.popleft()                       # O(1)
```

This is the single biggest reason BFS solutions written with a plain list TLE on large inputs.

## Bounded deque — sliding window

```python
# maxlen drops elements from the OPPOSITE end when full
window = deque(maxlen=3)
for x in [1, 2, 3, 4, 5]:
    window.append(x)
# window == deque([3, 4, 5], maxlen=3)

# Combine with iteration for a "last k values" view
last_3 = deque(maxlen=3)
for x in nums:
    last_3.append(x)
    if len(last_3) == 3:
        process(list(last_3))
```

## Rotate

```python
q = deque([1, 2, 3, 4, 5])
q.rotate(2)                           # deque([4, 5, 1, 2, 3])   — right
q.rotate(-1)                          # deque([5, 1, 2, 3, 4])   — left
```

## LeetCode patterns

```python
# BFS — the canonical use
from collections import deque

def bfs(start, graph):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()        # O(1) — critical
        for nbr in graph[node]:
            if nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)

# Level-order traversal with sentinel-by-size
def level_order(root):
    if not root:
        return []
    levels = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):       # process exactly one level
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        levels.append(level)
    return levels

# Monotonic deque — sliding window maximum (LC 239)
def max_sliding_window(nums, k):
    q = deque()                       # stores INDICES, values decreasing
    out = []
    for i, x in enumerate(nums):
        while q and nums[q[-1]] <= x:
            q.pop()                   # drop smaller values from the back
        q.append(i)
        if q[0] <= i - k:
            q.popleft()               # drop indices outside the window
        if i >= k - 1:
            out.append(nums[q[0]])
    return out
```

**See also:** [list.md#stack-via-list](list.md#stack-via-list) for stack patterns (list is fine for typical depths; deque is the choice when you push/pop from both ends).
