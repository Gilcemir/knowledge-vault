# Bit manipulation

Operators, single-bit surgery, and the XOR/lowbit tricks behind an entire LC topic. Python ints are arbitrary-precision — no 32-bit wraparound unless you mask for it.

## Operators

| Operator | Meaning | Example |
|---|---|---|
| `a & b` | AND | `0b1100 & 0b1010 == 0b1000` |
| `a \| b` | OR | `0b1100 \| 0b1010 == 0b1110` |
| `a ^ b` | XOR | `0b1100 ^ 0b1010 == 0b0110` |
| `~a` | NOT | `~x == -x - 1` (infinite sign extension) |
| `a << k` | shift left | `1 << 3 == 8` — multiply by 2ᵏ |
| `a >> k` | shift right | `8 >> 2 == 2` — floor-divide by 2ᵏ |

```python
bin(10)                               # '0b1010'
int("1010", 2)                        # 10
f"{10:08b}"                           # '00001010' — fixed width, no prefix

(10).bit_count()                      # 2 — number of set bits (3.10+)
bin(10).count("1")                    # 2 — pre-3.10 equivalent
(10).bit_length()                     # 4 — bits needed to represent
```

## Single-bit surgery

```python
x = 0b1010

x & (1 << i)                          # test bit i  (truthy if set)
x | (1 << i)                          # set bit i
x & ~(1 << i)                         # clear bit i
x ^ (1 << i)                          # toggle bit i
```

## Classic tricks

```python
x & (x - 1)                           # drop the LOWEST set bit  (0b1100 → 0b1000)
x & -x                                # isolate the lowest set bit (0b1100 → 0b0100)

# Power of two — exactly one set bit
def is_power_of_two(n):
    return n > 0 and n & (n - 1) == 0

# Even/odd without %
x & 1                                 # 1 if odd

# Count set bits by repeatedly dropping the lowest (Kernighan)
def popcount(x):
    c = 0
    while x:
        x &= x - 1                    # one iteration PER SET BIT, not per bit
        c += 1
    return c                          # or just x.bit_count() on 3.10+
```

## XOR identities

```python
a ^ a == 0                            # self-cancels
a ^ 0 == a                            # identity
# XOR is commutative & associative → order never matters

# Single number — every element appears twice except one (LC 136)
from functools import reduce
from operator import xor
def single_number(nums):
    return reduce(xor, nums)          # pairs cancel, the loner survives

# Missing number in 0..n (LC 268) — XOR indices against values
def missing_number(nums):
    res = len(nums)
    for i, x in enumerate(nums):
        res ^= i ^ x
    return res
```

## Bitmasks as sets

An int is a set of small integers: bit i set ⇔ element i present. O(1) copy, hashable → perfect DP state.

```python
mask = 0
mask |= 1 << 3                        # add 3
mask & (1 << 3)                       # contains 3?
mask &= ~(1 << 3)                     # remove 3

# All subsets of n elements
n = 3
for mask in range(1 << n):            # 0b000 .. 0b111
    subset = [i for i in range(n) if mask & (1 << i)]

# Iterate SUBMASKS of a given mask — the O(3ⁿ) DP idiom
sub = mask
while sub:
    process(sub)
    sub = (sub - 1) & mask            # next smaller submask
```

## Negative numbers — Python vs 32-bit

Python ints have no fixed width, so `~x` and negative results don't wrap like in C/Java. To simulate 32-bit (LC 190/191-style problems):

```python
MASK = 0xFFFFFFFF
x & MASK                              # truncate to unsigned 32-bit

# Interpret a 32-bit unsigned value as signed
def to_signed(x):
    x &= MASK
    return x if x < 0x80000000 else x - (1 << 32)
```

## LeetCode patterns

```python
# Counting bits DP (LC 338) — dp[x] from dp[x with lowest bit dropped]
def count_bits(n):
    dp = [0] * (n + 1)
    for x in range(1, n + 1):
        dp[x] = dp[x & (x - 1)] + 1
    return dp

# Subsets via bitmask (alternative to backtracking)
def subsets(nums):
    n = len(nums)
    return [[nums[i] for i in range(n) if mask & (1 << i)]
            for mask in range(1 << n)]

# Bitmask DP state — "which elements are used"
from functools import cache
@cache
def dp(mask):
    if mask == (1 << n) - 1:          # all used
        return 0
    ...
```

**See also:** [math.md](math.md) for powers and number theory, [recursion.md](recursion.md) for `@cache` with bitmask states, [conversions.md](conversions.md) for `bin`/`int(s, 2)` formatting.
