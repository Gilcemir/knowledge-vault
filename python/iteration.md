# Iteration

For/while loops, enumeration, zip, comprehensions, unpacking, walrus, generators, and `itertools` — the syntactic backbone of every LeetCode solution.

## For loops & `range`

```python
for i in range(5):                    # 0, 1, 2, 3, 4
    pass

for i in range(2, 10, 2):             # 2, 4, 6, 8 — start, stop, step
    pass

for i in range(10, 0, -1):            # 10..1 — countdown
    pass

# Iterate directly — preferred when you don't need the index
for x in nums:
    pass
```

`range` is lazy — it doesn't allocate a list. `range(10**9)` is fine.

## `while` & loop control

```python
n = 10
while n > 0:
    n -= 2                            # no `n--` in Python

# break / continue
for i in range(10):
    if i == 3:
        continue                      # skip to next iteration
    if i == 7:
        break                         # exit loop

# for…else — runs only if the loop didn't break
for x in nums:
    if x == target:
        print("found")
        break
else:
    print("not found")                # runs when no break fired
```

`for…else` is rarely needed in LC — most use cases are clearer with an explicit flag or wrapping the search in a function. Know it exists.

## `enumerate`

```python
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):    # (0, 'apple'), (1, 'banana'), ...
    pass

for i, fruit in enumerate(fruits, start=1):
    pass                              # (1, 'apple'), (2, 'banana'), ...
```

```python
# don't: index-based loop with manual indexing (universal beginner trap)
for i in range(len(nums)):
    x = nums[i]
    print(i, x)

# do:
for i, x in enumerate(nums):
    print(i, x)
```

`range(len(...))` is the single most replaceable pattern in beginner Python — switch to `enumerate` whenever you need both index and value.

## `zip` — parallel iteration

```python
names = ["Alice", "Bob", "Carol"]
scores = [90, 85, 92]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# 3+ iterables
for a, b, c in zip([1, 2], [3, 4], [5, 6]):
    pass

# Unzip (transpose) via star
pairs = [(1, "a"), (2, "b"), (3, "c")]
nums, letters = zip(*pairs)           # nums=(1,2,3), letters=('a','b','c')
```

`zip` stops at the shortest iterable. For padding with a fill value, use `itertools.zip_longest(a, b, fillvalue=0)`.

In Python 3.10+, pass `strict=True` to require equal lengths — raises `ValueError` instead of silently truncating:

```python
for a, b in zip(names, scores, strict=True):
    pass                              # ValueError if lengths differ
```

## `reversed` & `next(iter(...))`

```python
for x in reversed(nums):              # lazy — no copy, unlike nums[::-1]
    pass

for i in reversed(range(n)):          # n-1 .. 0 — clearer than range(n-1, -1, -1)
    pass

# Grab an arbitrary element from a set/dict WITHOUT removing it
s = {1, 2, 3}
x = next(iter(s))                     # any element — s.pop() would remove it

# First match with a default
first_even = next((x for x in nums if x % 2 == 0), None)
```

## Unpacking

```python
# Basic
a, b, c = (1, 2, 3)
a, b, c = [1, 2, 3]                   # works on any iterable

# Swap without temp
x, y = 10, 20
x, y = y, x                           # x=20, y=10

# Starred — absorbs everything else into a list
first, *rest = [1, 2, 3, 4, 5]        # first=1, rest=[2, 3, 4, 5]
*head, last = [1, 2, 3, 4, 5]         # head=[1, 2, 3, 4], last=5
a, *middle, z = [1, 2, 3, 4, 5]       # a=1, middle=[2, 3, 4], z=5

# Nested unpacking
points = [(1, 2), (3, 4)]
for (x, y) in points:
    pass

# Unpacking with dict.items()
d = {"a": 1, "b": 2}
for key, val in d.items():
    pass
```

Starred unpacking absorbs everything between the named names. `a=1`, `z=5`, the rest goes to `middle`.

## Walrus `:=` — assignment expression

```python
# Read until empty (3.8+)
import sys
while (line := sys.stdin.readline()):
    process(line)

# Filter and use the computed value in a comprehension
nums = [1, 4, 9, 16, 25]
results = [y for x in nums if (y := x // 2) > 2]    # [4, 8, 12] — assigns y once per x

# Cap repeated computation in conditions
if (n := len(nums)) > 1000:
    print(f"big input: {n}")
```

Best used to **avoid double computation** in `while` conditions and comprehensions. Don't reach for it when a plain assignment one line above is clearer.

## Comprehensions

The general form: `[expr for item in iterable if condition]` — note the `if` comes **after** the `for`.

```python
# List comprehension — see list.md for type-specific examples
squares = [x * x for x in range(10)]
evens = [x for x in nums if x % 2 == 0]
pairs = [(x, y) for x in [1, 2] for y in [3, 4]]            # nested loops

# Dict comprehension — see dict.md
sq = {x: x * x for x in range(5)}
inv = {v: k for k, v in d.items()}

# Set comprehension — see set.md
unique_lens = {len(w) for w in words}

# Generator expression — lazy, parens not brackets
gen = (x * x for x in range(1_000_000))
sum(x * x for x in range(100))        # parens implied inside sum/min/max/any/all
```

Comprehensions with one `for` and at most one `if` are idiomatic. Past that, switch to a regular for-loop for readability.

## `any` / `all`

```python
nums = [1, 2, 3, 4]
any(x > 3 for x in nums)              # True
all(x > 0 for x in nums)              # True
all(nums)                             # True — all truthy?  (false if any 0)
any(nums)                             # True — any truthy?

# Short-circuits — stops at the first True (any) or first False (all)
any(expensive_check(x) for x in big_list)
```

Use generator expressions (no `[]`) inside `any`/`all` to keep short-circuiting cheap.

## `map` / `filter`

```python
nums = [1, 2, 3, 4]
list(map(str, nums))                  # ['1', '2', '3', '4']
list(map(lambda x: x * 2, nums))      # [2, 4, 6, 8]
list(filter(lambda x: x % 2 == 0, nums))  # [2, 4]
```

Both return lazy iterators. List comprehensions are usually clearer; reach for `map`/`filter` mainly when the function is already named:

```python
list(map(str, nums))                  # cleaner than [str(x) for x in nums]? barely — pick what reads better
```

## Generators

```python
# Generator expression — lazy, memory-efficient
gen = (x * x for x in range(1_000_000))
next(gen)                             # 0     — computed on demand
next(gen)                             # 1

# Generator function — yield instead of return
def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1

for val in count_up(5):
    pass

# Infinite generators — combine with islice or break
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

import itertools
list(itertools.islice(fib(), 10))     # first 10 fibonacci numbers
```

Generators are essential when the full sequence is too big to materialize (`range(10**9)`, infinite streams, lazy pipelines).

## `itertools`

```python
import itertools

# chain — concatenate iterables
list(itertools.chain([1, 2], [3, 4]))                  # [1, 2, 3, 4]

# chain.from_iterable — flatten one level
list(itertools.chain.from_iterable([[1, 2], [3, 4]]))  # [1, 2, 3, 4]

# islice — lazy slicing (works on infinite/generator sources where [a:b] doesn't)
list(itertools.islice(fib(), 5))                       # [0, 1, 1, 2, 3]

# combinations — unordered, no repeats
list(itertools.combinations([1, 2, 3], 2))             # [(1,2),(1,3),(2,3)]

# permutations — ordered arrangements
list(itertools.permutations([1, 2, 3], 2))             # [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]

# combinations_with_replacement
list(itertools.combinations_with_replacement([1, 2, 3], 2))
# [(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]

# product — cartesian product (replaces nested for-loops)
list(itertools.product([0, 1], repeat=3))              # all 3-bit binary patterns

# groupby — group CONSECUTIVE identical keys (sort first if you want full grouping!)
data = [("a", 1), ("a", 2), ("b", 3), ("a", 4)]
for k, group in itertools.groupby(data, key=lambda x: x[0]):
    print(k, list(group))
# a [('a', 1), ('a', 2)]
# b [('b', 3)]
# a [('a', 4)]      ← because original is not sorted by key

# count — infinite counter
counter = itertools.count(start=0, step=2)             # 0, 2, 4, 6, ...

# cycle — infinite cycling
for i, val in zip(range(7), itertools.cycle([1, 2, 3])):
    pass                              # 1 2 3 1 2 3 1
```

### `pairwise` (3.10+) and `accumulate`

```python
import itertools

# pairwise — consecutive pairs (3.10+)
list(itertools.pairwise([1, 2, 3, 4]))                 # [(1,2),(2,3),(3,4)]
# Use case: differences between consecutive elements
diffs = [b - a for a, b in itertools.pairwise(nums)]

# accumulate — running totals / running ops
list(itertools.accumulate([1, 2, 3, 4]))               # [1, 3, 6, 10] — running sum
list(itertools.accumulate([1, 2, 3, 4], initial=100))  # [100, 101, 103, 106, 110]
list(itertools.accumulate([3, 1, 4, 1, 5], max))       # [3, 3, 4, 4, 5] — running max

import operator
list(itertools.accumulate([1, 2, 3, 4], operator.mul)) # [1, 2, 6, 24] — running product
```

## Dict iteration patterns

See [dict.md](dict.md) for the canonical home — `for k in d`, `for v in d.values()`, `for k, v in d.items()`, sorted-by-key, sorted-by-value.

## LeetCode patterns

```python
# Iterate two pointers from opposite ends
lo, hi = 0, len(nums) - 1
while lo < hi:
    if nums[lo] + nums[hi] == target:
        break
    elif nums[lo] + nums[hi] < target:
        lo += 1
    else:
        hi -= 1

# Run-length encoding via groupby
from itertools import groupby
def rle(s):
    return [(ch, sum(1 for _ in g)) for ch, g in groupby(s)]
# rle("aaabbc") → [('a', 3), ('b', 2), ('c', 1)]

# All 4 grid neighbors
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
for dr, dc in directions:
    nr, nc = r + dr, c + dc

# Bitmask enumeration over subsets (k bits, n total)
import itertools
for combo in itertools.combinations(range(n), k):
    mask = sum(1 << i for i in combo)
```

**See also:** [list.md](list.md), [dict.md](dict.md), [set.md](set.md) for type-specific comprehension examples; [tuple.md](tuple.md) for unpacking with composite keys.
