# Conversions & Type Checks

Converting between numeric types, strings, and collections — plus checking types defensively.

## Numeric conversions

```python
int("42")                # 42
int("  42 ")             # 42 — whitespace OK
int("3.99")              # ValueError — int() does not parse floats from strings
int(3.99)                # 3 — truncates toward zero, NOT round
int(-3.99)               # -3 — truncates toward zero (NOT floor for negatives!)
float("3.14")            # 3.14
float(42)                # 42.0
round(3.14159, 2)        # 3.14 — banker's rounding to N decimals
round(2.5)               # 2 — banker's rounding (round half to even!)
round(3.5)               # 4
```

For floor on negatives, use `math.floor` (not `int`):

```python
import math
math.floor(-3.99)        # -4
math.ceil(3.01)          # 4
math.trunc(-3.99)        # -3 — same as int() for floats
```

## `divmod`, `pow` and infinity

```python
q, r = divmod(17, 5)     # (3, 2) — quotient and remainder in one call
pow(2, 10)               # 1024
pow(2, 10, 1000)         # 24 — modular exponentiation, FAST (O(log b))

# don't: (2 ** huge) % MOD materializes the giant intermediate
MOD = 10**9 + 7
(2 ** 10**6) % MOD       # slow — builds a 300k-digit int first
pow(2, 10**6, MOD)       # fast — reduces mod at every step

float('inf')             # ∞ — compares greater than every number
float('-inf')
import math
math.inf                 # same value; pick one style and stick to it
best = float('inf')      # canonical "minimum so far" sentinel
```

See [math.md](math.md) for `gcd`, `isqrt`, `comb` and friends.

## Bases and `ord`/`chr`

```python
int("FF", 16)            # 255 — parse hex
int("1010", 2)           # 10  — parse binary
int("777", 8)            # 511 — parse octal
int("0xFF", 0)           # 255 — auto-detect from prefix

bin(10)                  # '0b1010'
oct(10)                  # '0o12'
hex(255)                 # '0xff'

f"{255:b}"               # '11111111' — binary without prefix
f"{255:08b}"             # '11111111' — width 8, zero-padded
f"{255:x}"               # 'ff'

ord('A')                 # 65   — char → codepoint
chr(65)                  # 'A'  — codepoint → char
ord('a') - ord('A')      # 32   — case offset in ASCII
```

## String ↔ collection

```python
list("abc")              # ['a', 'b', 'c']
tuple([1, 2, 3])         # (1, 2, 3)
set([1, 2, 2, 3])        # {1, 2, 3} — dedup
"".join(['a', 'b'])      # 'ab' — see str.md for join patterns

str(42)                  # '42'
str([1, 2, 3])           # '[1, 2, 3]' — useful for hashing list-shaped state
```

## Truthiness — falsy values

```python
bool(0)                  # False
bool(0.0)                # False
bool("")                 # False
bool([])                 # False
bool({})                 # False
bool(set())              # False
bool(None)               # False
# Everything else is truthy.

# Idiom: check non-empty container
if nums:                 # equivalent to `if len(nums) > 0`
    pass

# don't: explicit comparison to True/False/None
if x == None: pass       # use `if x is None`
if x == True: pass       # use `if x`
```

## isinstance vs type

```python
isinstance(42, int)              # True
isinstance(3.14, float)          # True
isinstance("hi", str)            # True
isinstance(42, (int, float))     # True — tuple form: any of these
isinstance(True, int)            # True — bool is a subclass of int!

type(42) is int                  # True — strict, ignores subclassing
```

Prefer `isinstance` — it handles subclassing (most LC inputs are fine either way, but `isinstance` is the convention). Note the bool/int subclass relationship: `isinstance(True, int)` is True.

## Safe number parsing

```python
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

is_number("3.14")        # True
is_number("-1e10")       # True
is_number("abc")         # False
is_number("inf")         # True — float("inf") is allowed
```

For "integer only, no signs" prefer `s.isdigit()` (from [str.md](str.md#character-checks)).

## LeetCode patterns

```python
# Digit-by-digit on an int
n = 1234
digits = [int(c) for c in str(n)]      # [1, 2, 3, 4]

# Reverse an integer
n, rev = 1234, 0
while n > 0:
    rev = rev * 10 + n % 10
    n //= 10                            # rev == 4321

# Integer division vs float division
7 / 2                                   # 3.5
7 // 2                                  # 3   — floor division
-7 // 2                                 # -4  — floors toward -inf (not toward 0!)
7 % 2                                   # 1   — modulo follows divisor's sign
-7 % 2                                  # 1   — (not -1)
```

**See also:** [str.md#character-checks](str.md#character-checks) for `isdigit`/`isalpha` predicates on strings.
