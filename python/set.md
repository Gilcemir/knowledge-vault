# set

Unordered collection of unique, hashable elements — average O(1) membership tests.

## Complexity reference

| Operation | Time | Notes |
|---|---|---|
| `x in s` | O(1) avg | worst O(n) on adversarial hashes |
| `s.add(x)` | O(1) avg | |
| `s.remove(x)` | O(1) avg | raises KeyError if missing |
| `s.discard(x)` | O(1) avg | safe — no error if missing |
| `s.pop()` | O(1) | removes & returns arbitrary element |
| `len(s)` | O(1) | |
| iterate `s` | O(n) | order is not guaranteed |
| `a | b`, `a & b`, `a - b`, `a ^ b` | O(len(a)+len(b)) | union / intersection / diff / symmetric diff |
| `a.issubset(b)` / `a <= b` | O(len(a)) | |

## Initialization

```python
s = set()                             # empty set — NOT {} (that's an empty dict!)
s = {1, 2, 3}                         # literal
s = set([1, 2, 2, 3])                 # {1, 2, 3} — dedups any iterable
s = set("abracadabra")                # {'a', 'b', 'r', 'c', 'd'}
```

The `{}` literal is reserved for empty dict — there's no empty-set literal.

## Add / remove

```python
s = {1, 2, 3}
s.add(4)                              # {1,2,3,4}   O(1)
s.update([5, 6])                      # add many       O(k)
s.update("ab")                        # {..., 'a', 'b'} — also accepts strings
s.remove(4)                           # raises KeyError if absent
s.discard(99)                         # no error if absent
s.pop()                               # remove arbitrary element
s.clear()
```

Use `discard` when "remove if present" — `remove` is the strict version.

## Set operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b                                 # {1,2,3,4,5,6}   union
a & b                                 # {3, 4}          intersection
a - b                                 # {1, 2}          difference
b - a                                 # {5, 6}
a ^ b                                 # {1,2,5,6}       symmetric difference (XOR)

a.issubset(b)                         # False  — a ⊆ b?
a <= b                                # same
a.issuperset(b)                       # False  — a ⊇ b?
a.isdisjoint({99, 100})               # True   — no shared elements

# In-place variants (mutate left side)
a |= b                                # a.update(b)
a &= b                                # a.intersection_update(b)
a -= b                                # a.difference_update(b)
a ^= b                                # a.symmetric_difference_update(b)
```

Set operators accept other sets only with `&`/`|`/etc. The method forms (`a.union(b)`, `a.intersection(b)`) accept any iterable.

## Membership idioms

```python
# Replace O(n) `in list` with O(1) `in set` when checking membership in a hot loop
allowed = {"GET", "POST", "PUT", "DELETE"}
if method in allowed:
    pass

# Deduplicate while preserving order — see dict.md trick
seen = set()
unique = [x for x in items if not (x in seen or seen.add(x))]
# Or use dict.fromkeys (3.7+ insertion order):
unique = list(dict.fromkeys(items))
```

## Set comprehension

```python
unique_lens = {len(w) for w in ["hi", "hey", "yo"]}    # {2, 3}
chars = {ch.lower() for ch in "Hello World" if ch.isalpha()}
```

**See also:** [iteration.md#comprehensions](iteration.md#comprehensions) for general comprehension mechanics.

## `frozenset` — hashable, immutable set

```python
fs = frozenset([1, 2, 3])
fs.add(4)                             # AttributeError — frozenset is immutable

# Use as dict key (regular set is unhashable)
groups = {}
groups[frozenset({"a", "b"})] = "pair"

# Use as element of another set
sets_of_sets = {frozenset([1, 2]), frozenset([3, 4])}
```

Use `frozenset` when you need to key a dict by an unordered collection, or when storing sets-of-sets. Tuples are usually preferred for ordered keys; `frozenset` shines when membership equality matters and order doesn't.

## LeetCode patterns

```python
# Duplicate detection in one pass
def contains_duplicate(nums):
    return len(set(nums)) != len(nums)

# Visited tracking in DFS/BFS — use a set for O(1) lookups
visited = set()
def dfs(node):
    if node in visited:
        return
    visited.add(node)
    # ...

# Intersection of multiple lists
def common(*lists):
    return set(lists[0]).intersection(*lists[1:])

# 2D grid visited — tuples are hashable
visited = set()
visited.add((0, 0))
if (1, 2) in visited:
    pass
```

**See also:** [dict.md](dict.md) for the value-carrying cousin, [list.md#membership-the-set-trick](list.md#membership--the-set-trick) for the O(n²)→O(n) refactor.
