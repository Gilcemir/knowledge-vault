# re

Pattern matching against strings — reach for it when string methods aren't expressive enough (variable separators, classes of characters, validation).

## Search & match

```python
import re

re.search(r"\d+", "abc123")           # <Match 'span=(3,6), match='123'>  — anywhere
re.match(r"\d+", "123abc")            # match — only at start of string
re.fullmatch(r"\d+", "123")           # match — must cover the whole string
re.findall(r"\d+", "a1b22c333")       # ['1', '22', '333'] — all non-overlapping
re.finditer(r"\d+", "a1b22c333")      # iterator of Match objects (lazy)

m = re.search(r"(\w+)@(\w+)", "name@host")
if m:
    m.group(0)                        # 'name@host'
    m.group(1)                        # 'name'      ← first capture group
    m.group(2)                        # 'host'
    m.groups()                        # ('name', 'host')
```

`search` returns `None` if no match — always check before `.group()`.

## Substitute & split

```python
re.sub(r"\s+", "-", "a b  c")         # 'a-b-c' — collapse whitespace
re.sub(r"(\w+)@", r"X@", "a@b.com")   # backreferences in replacement
re.split(r"[,;]", "a,b;c")            # ['a', 'b', 'c'] — split on any of , or ;

# Replacement function — runs for every match
re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "a1b22")    # 'a2b44'
```

## Compile for reuse

```python
pat = re.compile(r"[A-Z]\w+")
pat.findall("Hello World")            # ['Hello', 'World']
pat.search("the Quick fox")           # match on 'Quick'
```

Compile when reusing the same pattern many times (e.g., inside a loop over inputs) — Python caches recently-used regexes but explicit compile is clearer.

## Common patterns

```python
EMAIL = r"[\w.+-]+@[\w-]+\.[\w.-]+"
DIGITS_ONLY = r"^\d+$"                # whole string is digits
URL = r"https?://[^\s]+"
HEX_COLOR = r"#[0-9a-fA-F]{6}"
INTEGER_OR_FLOAT = r"-?\d+(?:\.\d+)?"
WORD = r"\b\w+\b"                     # word boundary

# Strip HTML tags (naive — fine for cheat-sheet sketches, NOT for real HTML)
re.sub(r"<[^>]+>", "", "<b>bold</b>")  # 'bold'
```

## Character class cheat

| Pattern | Matches |
|---|---|
| `\d` | digit (`[0-9]`) |
| `\D` | non-digit |
| `\w` | word char (`[A-Za-z0-9_]`) |
| `\W` | non-word |
| `\s` | whitespace |
| `\S` | non-whitespace |
| `.` | any char except newline (use `re.DOTALL` to include newline) |
| `^` / `$` | start / end of string (or line with `re.MULTILINE`) |
| `\b` | word boundary |
| `[abc]` | one of a/b/c |
| `[^abc]` | not a/b/c |
| `a*` / `a+` / `a?` | 0+ / 1+ / 0-or-1 |
| `a{n}` / `a{n,m}` | exactly n / between n and m |
| `(?:...)` | non-capturing group |
| `(?=...)` / `(?!...)` | lookahead / negative lookahead |

Always use raw strings (`r"..."`) for patterns so `\d`, `\b`, etc. aren't interpreted as escape sequences by Python before they reach `re`.

**See also:** [str.md](str.md) for non-regex string methods (often faster and simpler when the pattern is fixed).
