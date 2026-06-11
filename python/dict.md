# dict

Hash map — average O(1) lookups, insertion-ordered since Python 3.7.

## Complexity reference

| Operation | Time | Notes |
|---|---|---|
| `d[k]` (get) | O(1) avg | O(n) worst case on adversarial hashes |
| `d[k] = v` (set) | O(1) avg | |
| `del d[k]` | O(1) avg | |
| `k in d` | O(1) avg | use this for membership, not `k in d.keys()` |
| `d.get(k, default)` | O(1) avg | no exception on missing key |
| `len(d)` | O(1) | |
| iterate `d` / `d.items()` | O(n) | |
| `d.update(other)` | O(k) | k = len(other) |
| `{**d1, **d2}` | O(n+m) | merge into new dict |

## Create & access

```python
d = {}
d = {"a": 1, "b": 2}
d = dict(a=1, b=2)                    # keyword form — keys must be valid identifiers
d = dict([("a", 1), ("b", 2)])        # from pairs

d["a"]                                # 1     — raises KeyError if missing
d.get("c")                            # None  — returns None if missing
d.get("c", 0)                         # 0     — default if missing

d["c"] = 3                            # add/update
del d["a"]                            # remove (KeyError if missing)
d.pop("b")                            # remove + return value (KeyError if missing)
d.pop("zzz", None)                    # remove + return value, None if missing
d.clear()                             # empty in-place
```

## Iterate

```python
d = {"a": 1, "b": 2, "c": 3}

for k in d:                           # default iteration yields KEYS
    pass
for v in d.values():
    pass
for k, v in d.items():                # most common form
    pass

"a" in d                              # True — O(1) membership
len(d)                                # 3
```

`d.keys()`, `d.values()`, and `d.items()` return **view objects** — they reflect later mutations to the dict and are O(1) to construct. Wrap in `list()` if you need a snapshot.

## Sorted iteration

```python
d = {"banana": 3, "apple": 5, "cherry": 1}

for k in sorted(d):                                   # by key asc
    pass
for k, v in sorted(d.items(), key=lambda kv: kv[1]):  # by value asc
    pass
for k, v in sorted(d.items(), key=lambda kv: -kv[1]): # by value desc
    pass
```

See [sorting.md](sorting.md) for multi-key sorting patterns.

## Merge

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 99, "c": 3}

merged = d1 | d2                      # {'a': 1, 'b': 99, 'c': 3}   — 3.9+, right wins
d1 |= d2                              # in-place merge — d1 == merged
merged = {**d1, **d2}                 # equivalent, works on older Pythons

d1.update(d2)                         # in-place, right wins
d1.setdefault("k", [])                # set k to [] only if k not already in d1; returns d1["k"]
```

## Comprehension

```python
sq = {x: x * x for x in range(5)}     # {0:0, 1:1, 2:4, 3:9, 4:16}

# Invert {value: key} — assumes unique values
d = {"a": 1, "b": 2}
inv = {v: k for k, v in d.items()}    # {1: 'a', 2: 'b'}

# Group nums by parity (using comprehension would lose multiples — see defaultdict below)
```

## `Counter` — frequency map

```python
from collections import Counter

c = Counter([1, 2, 2, 3, 3, 3])       # Counter({3: 3, 2: 2, 1: 1})
c = Counter("abracadabra")            # Counter({'a': 5, 'b': 2, 'r': 2, ...})

c["a"]                                # 5
c["zzz"]                              # 0 — missing keys return 0 (not KeyError!)
c.most_common(3)                      # [('a', 5), ('b', 2), ('r', 2)]
c.most_common()[-1]                   # least common element
c.total()                             # 11 (3.10+) — sum of counts
c.elements()                          # iterator: 'a','a','a','a','a','b','b',...

# Arithmetic between Counters
c1 = Counter("aab")                   # Counter({'a': 2, 'b': 1})
c2 = Counter("abc")                   # Counter({'a': 1, 'b': 1, 'c': 1})
c1 + c2                               # Counter({'a': 3, 'b': 2, 'c': 1})
c1 - c2                               # Counter({'a': 1})  — negative counts dropped
c1 & c2                               # Counter({'a': 1, 'b': 1})  — min of counts
c1 | c2                               # Counter({'a': 2, 'b': 1, 'c': 1})  — max of counts
```

`Counter` IS a dict — every dict operation works on it. The `-` operator drops zero and negative counts, which is handy for "what's left after removing X from Y" without manual filtering.

## `defaultdict` — auto-create missing keys

```python
from collections import defaultdict

# don't: manual missing-key dance — verbose and error-prone in LC
groups = {}
for word in words:
    key = "".join(sorted(word))
    if key not in groups:
        groups[key] = []
    groups[key].append(word)

# do: defaultdict provides the empty container on access
groups = defaultdict(list)
for word in words:
    key = "".join(sorted(word))
    groups[key].append(word)          # creates [] on first access

# Counts as defaultdict(int)
freq = defaultdict(int)
for x in nums:
    freq[x] += 1
# (or just use Counter)
```

`defaultdict(callable)` calls the factory on missing-key **access** (any access — including `dd[k]` and `dd[k].append(...)`). Note this means `dd[k]` may *create* the key as a side effect:

```python
dd = defaultdict(list)
dd["x"]                               # returns [] AND creates the key
"x" in dd                             # True now
```

If you don't want creation-on-read, use `.get(k, [])` instead.

## Mutation during iteration — trap

```python
# don't: adding/removing keys while iterating raises RuntimeError
d = {"a": 1, "b": 2, "c": 3}
for k in d:
    if d[k] > 1:
        del d[k]                      # RuntimeError: dictionary changed size during iteration

# do: iterate over a snapshot of the keys
for k in list(d):
    if d[k] > 1:
        del d[k]

# or build a new dict
d = {k: v for k, v in d.items() if v <= 1}
```

Mutating **values** of existing keys during iteration is fine — only adding/removing keys breaks.

## `dict.fromkeys`

```python
d = dict.fromkeys(["a", "b", "c"])        # {'a': None, 'b': None, 'c': None}
d = dict.fromkeys(["a", "b", "c"], 0)     # {'a': 0, 'b': 0, 'c': 0}

# Ordered dedup — keys are unique and insertion-ordered (3.7+)
unique = list(dict.fromkeys([3, 1, 3, 2, 1]))    # [3, 1, 2]
```

Careful with a mutable default: `dict.fromkeys(keys, [])` shares ONE list across all keys — same aliasing trap as `[[0] * n] * m` (see [list.md](list.md#2d-arrays--row-aliasing-trap)).

## `OrderedDict` — LRU cache (LC 146)

A plain dict is insertion-ordered but can't cheaply *reorder*. `OrderedDict` adds `move_to_end` and `popitem(last=False)` — exactly the two operations an LRU cache needs:

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.od = OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)          # mark as most-recently-used   O(1)
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)   # evict least-recently-used    O(1)
```

## LeetCode patterns

```python
# Two-sum — index lookup table
def two_sum(nums, target):
    seen = {}                         # {value: index}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i

# Anagram grouping — sorted-string key
def group_anagrams(strs):
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        groups["".join(sorted(s))].append(s)
    return list(groups.values())

# Tuple keys — hashable composite keys (great for grid coords, state vectors)
visited = {(0, 0), (1, 2)}            # this is a set; same idea for dicts:
dist = {(0, 0): 0, (1, 2): 5}

# First/last occurrence — exploit insertion order (3.7+)
seen = {}
for i, x in enumerate(nums):
    if x not in seen:
        seen[x] = i                   # first index
# vs.
for i, x in enumerate(nums):
    seen[x] = i                       # last index (overwrites)
```

**See also:** [set.md](set.md) for sets (dict's value-less cousin), [iteration.md#dict-iteration](iteration.md#dict-iteration) for iteration patterns, [sorting.md](sorting.md) for sorting `.items()`.
