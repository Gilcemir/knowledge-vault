# str

Immutable sequence of characters — every "mutation" returns a new string.

## Complexity reference

| Operation | Time | Notes |
|---|---|---|
| `s[i]` | O(1) | random access |
| `len(s)` | O(1) | |
| `s[i:j]` | O(j−i) | creates a copy, O(j−i) space |
| `s + t` | O(len(s)+len(t)) | new string; in a loop use `"".join(parts)` |
| `sub in s` | O(n·m) | substring search (n=len(s), m=len(sub)) |
| `s.find(sub)` / `s.index(sub)` | O(n·m) | `find` returns -1, `index` raises |
| `s.replace(a, b)` | O(n) | |
| `s.split(sep)` | O(n) | |
| `sep.join(iter)` | O(total) | single allocation; preferred over `+=` in loops |
| `s.startswith(p)` / `endswith(p)` | O(len(p)) | |
| `s == t` | O(n) | char-by-char |

## Create, concat, slice

```python
s = "Hello, World!"
s2 = 'single quotes'
multi = """multi
line"""

joined = "Hello" + " World"          # O(n+m) — avoid `+=` in loops, use join()

s = "Python"
s[0]       # 'P'
s[-1]      # 'n'
s[1:4]     # 'yth'
s[::-1]    # 'nohtyP' — reverse via slicing (O(n))
```

## f-strings

```python
name = "Alice"
age = 30
print(f"{name} is {age} years old")
print(f"Pi = {3.14159:.2f}")          # 'Pi = 3.14'
print(f"{42:05d}")                    # '00042' — width 5, zero-pad
print(f"{0.5:.1%}")                   # '50.0%'

# Debug form (Python 3.8+) — prints both the expression and its value
x, y = 3, 4
print(f"{x=}, {y=}, {x+y=}")          # 'x=3, y=4, x+y=7'
```

## Case & whitespace

```python
s = "  Hello World  "
s.upper()       # '  HELLO WORLD  '
s.lower()       # '  hello world  '
s.title()       # '  Hello World  '
s.strip()       # 'Hello World'
s.lstrip()      # 'Hello World  '
s.rstrip()      # '  Hello World'
s.strip(",.!")  # also strips listed chars from both ends
```

## `removeprefix` / `removesuffix` (3.9+)

```python
"img_photo.png".removeprefix("img_")  # 'photo.png'
"test_name.py".removesuffix(".py")    # 'test_name'
"hello".removeprefix("xyz")           # 'hello' — no error if absent

# don't: strip removes a CHARACTER SET, not a literal prefix/suffix
"file.pyp".rstrip(".py")              # 'file' — strips ANY trailing '.', 'p' or 'y'!
"file.pyp".removesuffix(".py")        # 'file.pyp' — correct: suffix doesn't match
```

The `strip("...")` char-set misuse is a classic silent-wrong bug — use `removeprefix`/`removesuffix` for literal affixes.

## Search & replace

```python
s = "banana"
s.find("an")            # 1 — first occurrence, -1 if absent
s.rfind("an")           # 3 — last occurrence, -1 if absent
s.index("an")           # 1 — same as find but raises ValueError if absent
s.count("a")            # 3 — non-overlapping
s.replace("a", "o")     # 'bonono'
s.replace("a", "o", 1)  # 'bonana' — only first occurrence
s.startswith("ban")     # True
s.endswith(("a", "z"))  # True — accepts a tuple of suffixes
"an" in s               # True
```

## Padding

```python
"42".zfill(5)           # '00042'
"hi".center(10, "-")    # '----hi----'
"hi".ljust(10, ".")     # 'hi........'
"hi".rjust(10, ".")     # '........hi'
```

## Split & join

```python
s = "one,two,three"
s.split(",")            # ['one', 'two', 'three']
s.split(",", 1)         # ['one', 'two,three'] — maxsplit

"  a  b  c  ".split()   # ['a', 'b', 'c'] — no-arg split collapses any whitespace
"a\nb\nc".splitlines()  # ['a', 'b', 'c']

words = ["Hello", "World"]
" ".join(words)         # 'Hello World'
"-".join(words)         # 'Hello-World'
"".join(words)          # 'HelloWorld'

# don't: build strings with += in a loop (O(n²) total)
parts = []
for w in words:
    parts.append(w.upper())
result = "".join(parts)               # O(n) total
```

## Partition — split into 3 parts on first separator

```python
"user@example.com".partition("@")     # ('user', '@', 'example.com')
"no-sep".partition("@")               # ('no-sep', '', '')   ← keeps tuple shape
"key=value".partition("=")            # ('key', '=', 'value')
```

Useful when you want the separator preserved or need a clean fallback when it's absent.

## Character checks

```python
"abc123".isalnum()      # True  — letters + digits
"abc".isalpha()         # True  — letters only
"123".isdigit()         # True  — ASCII digits
"½".isnumeric()         # True  — broader: fractions, superscripts, etc.
"  ".isspace()          # True  — all whitespace
"Hello".istitle()       # True  — title case
"ABC".isupper()         # True
"abc".islower()         # True
```

For "is this string a number including signs and decimals?" use a try/except — see [conversions.md#safe-number-parsing](conversions.md#safe-number-parsing).

## LeetCode patterns

```python
# Palindrome check via slicing
def is_palindrome(s):
    return s == s[::-1]               # O(n) time, O(n) space

# Anagram check — see dict.md for Counter approach
# Substring search — use s.find() or implement KMP if asked

# Char ↔ int conversions (see conversions.md#bases-and-ord-chr)
ord('A')                # 65
chr(65)                 # 'A'

# Iterate with index over string
word = "leetcode"
for i, ch in enumerate(word):         # see iteration.md#enumerate
    pass
```

**See also:** [conversions.md](conversions.md) for `int`/`float` parsing and `ord`/`chr`, [re.md](re.md) for pattern matching, [iteration.md#comprehensions](iteration.md#comprehensions) for string-building via comprehensions.
