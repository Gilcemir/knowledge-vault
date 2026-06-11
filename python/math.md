# math

Integer math in Python is exact and arbitrary-precision — no overflow, ever. The `math` module fills in the number-theory and combinatorics helpers LC problems lean on.

## `gcd` / `lcm`

```python
import math

math.gcd(12, 18)                      # 6
math.gcd(12, 18, 24)                  # 6  — multiple args (3.9+)
math.lcm(4, 6)                        # 12 — (3.9+)
math.lcm(2, 3, 5)                     # 30

# gcd of a whole list
from functools import reduce
reduce(math.gcd, [12, 18, 24])        # 6 — works on any Python version
```

`gcd(0, x) == x`, which makes `reduce(gcd, nums)` safe without an initializer for non-empty lists.

## `isqrt` — exact integer square root

```python
import math

math.isqrt(17)                        # 4 — floor of √17, exact integer arithmetic

# don't: float sqrt loses precision on big ints
n = 10**30 + 1
int(math.sqrt(n))                     # may be off by one — float has 53 bits of mantissa
math.isqrt(n)                         # always exact

# Perfect-square check
def is_square(n):
    r = math.isqrt(n)
    return r * r == n
```

## `comb` / `perm` / `factorial`

```python
import math

math.comb(5, 2)                       # 10  — n choose k, exact
math.perm(5, 2)                       # 20  — ordered arrangements
math.factorial(10)                    # 3628800
```

`comb` is exact for arbitrarily large n — no overflow, no floating point. For answers mod 10⁹+7 on huge n, you still need modular inverses (precomputed factorials), but for direct computation `comb` just works.

## Infinity & extremes

```python
import math

math.inf                              # float('inf') — same object semantics
-math.inf
math.inf > 10**1000                   # True — beats any int

best = math.inf                       # "minimum so far" sentinel
worst = -math.inf

# For pure-int code, None or a problem bound also works as sentinel —
# but inf survives min()/max() arithmetic without special-casing.
```

## Floor, ceil, ceil-division

```python
import math

math.floor(-3.2)                      # -4 — toward -inf (int() truncates toward 0!)
math.ceil(3.01)                       # 4

# Integer ceil-division WITHOUT floats — exact for any size
def ceil_div(a, b):
    return -(-a // b)                 # or (a + b - 1) // b for positive a, b

ceil_div(7, 2)                        # 4
math.ceil(7 / 2)                      # 4 — fine for small numbers, float-rounded for huge ones
```

See [conversions.md](conversions.md) for `int()` truncation vs `floor` and for `divmod`/`pow(a, b, mod)`.

## LeetCode patterns

```python
import math
from functools import reduce

MOD = 10**9 + 7                       # the canonical LC modulus

# Modular arithmetic — reduce as you go
total = 0
for x in nums:
    total = (total + x) % MOD

# Modular exponentiation & inverse (MOD is prime → Fermat)
pow(2, 50, MOD)                       # fast
inv = pow(x, MOD - 2, MOD)            # modular inverse of x

# Simplify a fraction / direction vector (LC 149 Max Points on a Line)
dx, dy = 4, -6
g = math.gcd(dx, dy)                  # gcd ignores signs → 2
slope = (dx // g, dy // g)            # (2, -3) — hashable canonical form

# Primality by trial division up to isqrt
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            return False
    return True
```

**See also:** [conversions.md](conversions.md) for `divmod`, `pow` with modulus, and float division pitfalls; [bits.md](bits.md) for powers of two and bit-level math.
