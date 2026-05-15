# Python Cheat Sheets — Stage 1 Audit

Source: 4 HTML files in `python/`. Target: a set of `.md` cheat sheets matching the decisions locked in via grilling (aggressive split per data structure, convert-only, type-name filenames, most-specific-type wins, 3-col complexity tables, 3-test anti-pattern rule, canonical 2D gotcha in `list.md`, anchor-level cross-links).

**Heads-up:** `python-str-cheatsheet.html` is misnamed. It actually covers 7+ distinct topics (strings, lists, dicts, type checks, type conversions, regex, sorting, builtins). The split below reflects the real content, not the filename.

---

## 1. File inventory

| source_file | proposed_target | action | rationale |
|---|---|---|---|
| `binary_search_cheatsheet.html` | `binary_search.md` | `rename_to:binary_search.md` | drop verbose `_cheatsheet` suffix; convert PT-BR commentary to English |
| `python-str-cheatsheet.html` | `str.md`, `list.md`, `dict.md`, `conversions.md`, `re.md`, `sorting.md`, `iteration.md` | `split_into:str.md, list.md, dict.md, conversions.md, re.md, sorting.md, iteration.md` | misnamed file; covers 7 topics — split per Q4 canonical-home rule |
| `python_dsa_cheatsheet.html` | `list.md`, `dict.md`, `set.md`, `tuple.md`, `deque.md`, `heapq.md`, `iteration.md` | `split_into:list.md, dict.md, set.md, tuple.md, deque.md, heapq.md, iteration.md` | one file per DS (Q1); tuple unpacking → `iteration.md` per Q4 |
| `python_iteration_cheatsheet.html` | `iteration.md`, `list.md`, `dict.md`, `set.md` | `split_into:iteration.md, list.md, dict.md, set.md` | list/dict/set comprehensions → respective type files (Q4); mechanics stay in `iteration.md`; Java-comparison tabs dropped |

**Final target file set** (12 files): `binary_search.md`, `str.md`, `list.md`, `dict.md`, `set.md`, `tuple.md`, `deque.md`, `heapq.md`, `iteration.md`, `re.md`, `conversions.md`, `sorting.md`.

---

## 2. Concepts inventory per source file

### `binary_search_cheatsheet.html`

- Exact match template (`lo <= hi`, return mid, return -1)
  - mid overflow-safe formula `lo + (hi - lo) // 2`
  - loop invariant rationale (`lo == hi` with one element)
- Lower bound (`arr[i] >= target`, first True)
  - `hi = len(arr)` (out-of-range sentinel)
  - `hi = mid` (not mid-1) rationale
- Upper bound (`arr[i] > target`)
  - relation `count = upper_bound(t) - lower_bound(t)`
  - combined-use range `[lower, upper)`
- Binary search on answer
  - monotonic predicate `f(mid)` requirement
  - Koko Eating Bananas reference
- Comparison table (loop / hi init / movement rules / return / use case)

### `python-str-cheatsheet.html` (misnamed — multi-topic)

- String basics
  - create (single, double, triple-quoted) + concat
  - slicing / indexing including `s[::-1]` reverse
  - f-strings + format spec (`{x:.2f}`)
- String methods
  - case (`upper`, `lower`, `title`)
  - whitespace (`strip`, `lstrip`, `rstrip`)
  - search/replace (`find`, `count`, `replace`, `startswith`, `endswith`, `in`)
  - padding (`zfill`, `center`, `ljust`, `rjust`)
- Split & join
  - `.split(sep)`, `.split(sep, maxsplit)`, `.splitlines()`, default whitespace split
  - `.join(iterable)`
  - `.partition(sep)`
- Type checks
  - `isinstance` (incl. tuple-of-types form), `type() is`
  - character-class checks (`isalpha`, `isdigit`, `isalnum`, `isnumeric`, `isspace`, `istitle`, `isupper`, `islower`)
  - safe number parsing via try/except
- Lists
  - init / mutate (`append`, `insert`, `extend`, `remove`, `pop`)
  - search/sort (`index`, `count`, `in`, `sort`, `reverse`, `sorted`)
  - list comprehensions (basic, filter, nested/flatten)
- Dictionaries
  - create/access (`d[k]`, `.get`, `.get` with default, add/del)
  - iterate / views (`keys`, `values`, `items`)
  - dict comprehension
  - merge (`|` 3.9+, `**unpack`)
- Type conversion
  - numeric (`int`, `int(s, base)`, `float`, `round`)
  - collections (`list("abc")`, `tuple`, `set`, `str`, `bool` truthiness)
  - number bases (`bin`, `oct`, `hex`, `ord`, `chr`)
- Regex
  - `search`, `match`, `fullmatch`, `findall`
  - `sub`, `split`
  - `re.compile` for reuse
  - common patterns (email, digits, URL, strip HTML)
- Sorting
  - `sorted` / `.sort` + `reverse=True`
  - `key=` (lambda, `operator.itemgetter`)
  - `min` / `max` / `sum` / mean
- Useful builtins
  - `enumerate` + `start=` argument
  - `zip` for parallel iteration
  - `map` / `filter` (+ chaining)
  - `any` / `all` with generator expressions
  - `collections.Counter`, `collections.defaultdict`
- Wide reference table of all string methods

### `python_dsa_cheatsheet.html`

- List
  - init (`[]`, literal, `list(range)`, `[0] * n`)
  - add/remove (`append`, `insert`, `extend`, `pop`, `pop(i)`, `remove`, `clear`) + complexity
  - access/search (`[i]`, `[-1]`, slice, `index`, `in`, `len`) + complexity
  - sort (`sort`, `sort(reverse)`, `sorted`, `reverse`, `count`)
- Dict
  - init (`{}`, literal, `dict(kw)`, `defaultdict(int)`, `defaultdict(list)`)
  - set/get/delete (`d[k]`, `.get(k, default)`, `del`, `pop(k, default)`, `clear`)
  - iterate (default keys, `.values`, `.items`, `in`, `len`)
  - merge (`update`, `{**d1, **d2}`, `setdefault`)
- Set
  - init (`set()` not `{}`!, literal, dedup from iterable)
  - add/remove (`add`, `update`, `remove` strict, `discard` safe, `pop`, `clear`)
  - operations (`|`, `&`, `-`, `^`, `issubset`, `issuperset`, `in`)
- Stack via list
  - push = `append`, pop = `pop`, peek = `[-1]`, empty check
- Queue via deque
  - `append` / `appendleft`, `popleft` / `pop`, peek front/back, empty check
- Stack via deque
  - same API as list-stack but O(1) on both ends; mentions `list.pop(0)` is O(n)
- Heap / priority queue
  - min-heap (`heappush`, `heappop`, peek `h[0]`, `heapify`)
  - max-heap via value negation
  - tuples as priority (`(priority, value)`)
  - `nlargest` / `nsmallest`
- Tuple
  - init (parens, no parens, single-element `(42,)`)
  - access, unpack (`a, b, c = t`), starred (`a, *rest = t`), swap (`x, y = y, x`)
- Counter
  - construct from iterable / string
  - `.most_common(n)`, `.total()`, addition between Counters
- Bottom complexity reference table (list / dict & set / heap & deque)

### `python_iteration_cheatsheet.html`

- For loops
  - `range(n)`, `range(start, stop, step)`
  - direct iteration over list
- While + loop control
  - basic `while`, `n -= 2` (no `--`)
  - `break` / `continue`
  - `for...else` (runs if not broken)
- Enumerate
  - basic + `start=` argument
- Zip
  - parallel iteration, 3+ iterables, unzip via `zip(*pairs)`
  - shortest-iterable cutoff + `zip_longest` mention
- Map / filter
  - basic, chaining
- Comprehensions
  - list (basic, filter, nested)
  - dict comprehension
  - set comprehension
  - filter-clause-after-for ordering note
- Unpacking / starred assignment
  - tuple unpacking in loop
  - `first, *rest`, `*start, last`, `a, *mid, z`
  - swap without temp
- Iterating dicts
  - keys (default), values, items, sorted by key, sorted by value via lambda
- `itertools.chain` / `chain.from_iterable` / `islice`
- `itertools.combinations` / `permutations` / `combinations_with_replacement` / `product`
- `itertools.groupby` (warns must sort first) / `count` / `cycle`
- Generators
  - generator expressions
  - `yield` functions
  - passing to `sum`/`min`/`max`
- Java comparison tabs in every section (**dropping — out of scope; cheat sheet is Python-only**)

---

## 3. Outdated / incorrect items to fix in Stage 2

### `binary_search_cheatsheet.html`

- `binary_search_cheatsheet.html` → all comments and prose in Portuguese (`não encontrado`, `convergiu`, `descarta`, `Achou!`) → translate to English
- `binary_search_cheatsheet.html` → variable `arr` everywhere → keep `arr` for binary-search context (signals "any sorted sequence"); add `nums`-flavored LeetCode-style example for Search-on-Answer card
- `binary_search_cheatsheet.html` → Koko reference in a trailing comment only → promote to a full runnable example (`# runnable` tag for Stage 2 validation)

### `python-str-cheatsheet.html`

- `python-str-cheatsheet.html` → footer claims "python 3.9+" but f-strings shown are 3.6+; dict-merge `|` is 3.9+. Pin everything to target 3.10+ per project rule
- `python-str-cheatsheet.html` → `map`/`filter` shown with `lambda` → note that list comprehensions are preferred (already implied in tip; surface it as an anti-pattern block satisfying the Q8 "complexity-equivalent but clearer Pythonic" test? — borderline; **skip** under the 3-test rule (no asymptotic / no silent-wrong / not a trap))
- `python-str-cheatsheet.html` → no mention of f-string `=` debug form (`f"{x=}"`) → add to `str.md` f-string section (idiom application — within existing file)
- `python-str-cheatsheet.html` → type-conversion `int(3.99) → 3` truncates (not rounds) → add explicit note + contrast with `round()` and `math.floor` for negatives
- `python-str-cheatsheet.html` → `isinstance` vs `type() is` shown without guidance → annotate `isinstance` as the LeetCode default (handles subclassing; matches duck-typed input)

### `python_dsa_cheatsheet.html`

- `python_dsa_cheatsheet.html` → no mention of the 2D-array aliasing gotcha (`[[0] * n] * m`) → add canonical entry to `list.md` per plan (qualifies under the 3-test rule: silently wrong)
- `python_dsa_cheatsheet.html` → dict tagged "ORDERED*" with no footnote → add note: insertion-ordered since Python 3.7
- `python_dsa_cheatsheet.html` → tuple shown without `frozenset` analogy or hashability note → add brief note: tuples of hashables are hashable → usable as dict keys / set elements
- `python_dsa_cheatsheet.html` → bottom complexity table merges dict & set into one column with "O(1) avg" → split: in per-DS files note dict/set worst-case O(n) on adversarial hashes (Notes column)
- `python_dsa_cheatsheet.html` → "Stack (list)" and "Stack (deque)" both shown; recommendation is fuzzy → resolve in `list.md` and `deque.md` (deque preferred for performance-critical; list is fine for typical DFS stack of bounded depth)
- `python_dsa_cheatsheet.html` → heap section has no mention of `(priority, tiebreak, value)` pattern for non-comparable values → add to `heapq.md` (idiom)
- `python_dsa_cheatsheet.html` → no `frozenset` as dict key → add brief mention in `set.md` (idiom application within existing file)

### `python_iteration_cheatsheet.html`

- `python_iteration_cheatsheet.html` → every card has a Java comparison tab → **drop entirely** (cheat sheet is Python-only)
- `python_iteration_cheatsheet.html` → no `itertools.pairwise` (3.10+) → add to `iteration.md` itertools section (idiom application)
- `python_iteration_cheatsheet.html` → no `itertools.accumulate` → add to `iteration.md` itertools section (idiom application)
- `python_iteration_cheatsheet.html` → no walrus `:=` examples → add to `iteration.md` (idiom application — common in `while (chunk := f.read())`, filtering comprehensions)
- `python_iteration_cheatsheet.html` → no `range(len(...))` anti-pattern → add as an anti-pattern block under `enumerate` (qualifies under 3-test rule: universal beginner trap with one-liner fix)
- `python_iteration_cheatsheet.html` → comprehensions example uses `[1,2]` / `[3,4]` (generic) → swap to LeetCode-flavored variants (`nums`, `intervals`, `grid`)

---

## 4. Cross-file redundancy report

Concept appears in 2+ HTML sources → canonical home below. Other sources contribute only via cross-link in the final `.md`.

| Concept | Sources | Canonical target | Rule applied |
|---|---|---|---|
| `enumerate` | `python-str` (Useful Builtins), `python_iteration` (enumerate card) | `iteration.md` | mechanic → iteration |
| `zip` | `python-str` (Useful Builtins), `python_iteration` (zip card) | `iteration.md` | mechanic → iteration |
| `map` / `filter` | `python-str` (Useful Builtins), `python_iteration` (map-filter card) | `iteration.md` | mechanic → iteration |
| `any` / `all` | `python-str` (Useful Builtins) | `iteration.md` | mechanic → iteration |
| `Counter` | `python-str` (Useful Builtins), `python_dsa` (Counter card) | `dict.md` | most-specific type wins (Counter IS a dict) |
| `defaultdict` | `python-str` (Useful Builtins), `python_dsa` (Dict init) | `dict.md` | most-specific type wins |
| List comprehension | `python-str` (Lists card), `python_iteration` (list-comp card) | `list.md` | type-specific → produces list |
| Dict comprehension | `python-str` (Dictionaries card), `python_iteration` (list-comp card) | `dict.md` | type-specific → produces dict |
| Set comprehension | `python_iteration` (list-comp card) | `set.md` | type-specific → produces set |
| List operations (`append`, `insert`, `pop`, `in`, `index`, `count`) | `python-str` (Lists card), `python_dsa` (List card) | `list.md` | type ops → type file (DSA card is the richer source; str-cheat additions merge in) |
| Dict operations (`get`, `items`, `keys`, `values`, merge) | `python-str` (Dictionaries card), `python_dsa` (Dict card), `python_iteration` (dict-iter card) | `dict.md` | type ops → type file |
| Dict iteration patterns (sort by key / by value) | `python-str`, `python_iteration` (dict-iter card) | `dict.md` | type-specific iteration patterns stay with type |
| Tuple unpacking / `a, *rest` / swap | `python_dsa` (Tuple card), `python_iteration` (unpacking card) | `iteration.md` | mechanic → iteration (per Q4); `tuple.md` retains only init + single-element trailing-comma trap |
| Sorting (`sorted`, `sort`, `key=`) | `python-str` (Sorting card), `python_dsa` (List "Sort/Other") | `sorting.md` | cross-type concept earns its own file (already a section in the source) |
| List initialization (`[0] * n`, `list(range)`) | `python-str` (Lists), `python_dsa` (List Init) | `list.md` | type-specific |
| Falsy values (`bool(0)`, `bool("")`, `bool([])`) | `python-str` (Type Conversion) | `conversions.md` | cross-type concept; lives with conversions |
| String slicing including `s[::-1]` | `python-str` (String Basics) | `str.md` | type-specific |
| Generator expressions | `python-str` (`any`/`all` examples), `python_iteration` (generators card) | `iteration.md` | mechanic → iteration |

---

## 5. Gaps — LeetCode-relevant idioms absent from sources

**Not implementing in Stage 2.** Surfaced for follow-up: greenlight any item to add it in a separate turn.

These are concepts from the plan's Pythonic-idioms list (or universally common in LeetCode) that have **no natural home in the existing source content** — adding them would mean creating a new `.md`, which Q2(a) disallowed.

- **`functools.lru_cache` / `@cache` for DP memoization** — no DP/recursion cheat sheet exists. Would need `dp.md` or `recursion.md`. Common enough in LC that a dedicated cheat sheet would pay off.
- **`match/case` structural pattern matching (3.10+)** — no clear existing home. Useful for state machines, tree-shape dispatch, and some graph problems. Would need its own section or a new `pattern_matching.md`.
- **`bisect.bisect_left` / `bisect_right`** — borderline: I'm proposing to *briefly* mention these inside `binary_search.md` as the Pythonic substitute for hand-rolled lower/upper-bound loops. That's idiom application within an existing file (allowed). If you want a fuller `bisect.md` with insertion (`insort`) and key-function patterns, flag this entry.
- **Single-element list as mutable cell** (`res = [0]` backtracking pattern, alternative to `nonlocal`) — plan calls this out as a Pythonic idiom for LC. No natural home in current sources; would warrant a section in a future `recursion.md` or under a "closures" subsection somewhere.
- **`nonlocal` / closure capture semantics** — same as above; ties to backtracking.

The following idioms from the plan list are **NOT gaps** — they apply within existing target files and are already enumerated in Section 3:

- 2D array `[[0]*n]*m` gotcha → `list.md`
- f-string `=` debug form → `str.md`
- walrus `:=` → `iteration.md`
- `itertools.pairwise` / `accumulate` → `iteration.md`
- `frozenset` as dict key → `set.md`
- Tuple unpacking idioms → `iteration.md`
- `(priority, tiebreak, value)` heap pattern → `heapq.md`

---

**Stage 1 complete. Awaiting approval to proceed with Stage 2.**
