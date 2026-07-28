# Size-k heap pattern derived independently, before being taught

Gil solved P1 (LC 703, Kth Largest in a Stream) unaided and arrived at the canonical bounded min-heap on the first attempt — no hints requested at any level. This matters because L4 was scheduled to *teach* this pattern; it now only needs to generalise it.

**Evidence**: solution verified 2026-07-27 against the official LeetCode example plus 3000 randomised trials against a brute-force oracle — all matched, heap size never exceeded `k`, and no crash when `nums` is shorter than `k`. Beyond correctness:

- He reused `self.add` inside `__init__` rather than duplicating the trim logic, keeping the size invariant in one place.
- Asked afterwards, he stated all three complexities cold and correctly: `add` O(log k), memory O(k), `__init__` O(n log k).
- Asked which L3 primitive collapses the steady-state `heappush`+`heappop` into a single sift, he named `heappushpop` correctly.

**The gap, recorded deliberately**: he named `heappushpop` but did **not** work through why `heapreplace` is wrong here (it replaces the root unconditionally, so a value below the k-th largest evicts a larger element). He chose to move on, so this was given rather than derived. Treat the pushpop-vs-replace *distinction* as fluency-only, not storage-strength — re-test it cold in L8 rather than assuming it.

**Implications**: L4 ("The Top-K pattern") loses most of its original purpose. Do not re-teach the size-k heap — he has it. Repoint L4 at what he has *not* met:

- size-k heap vs `heapify`-all-then-pop as an explicit cost comparison (he already reasoned correctly that O(n log k) beats O(n) + (n−k) log n for small k, so this is confirmation, not instruction)
- `nlargest`/`nsmallest` — the last unmet `heapq` criterion in [[MISSION.md]]
- custom priorities via `key`, building on the `(priority, counter, payload)` tuple from [[0004-heapq-api-fluent-tuple-priorities-solid]]

Consider merging L4 into the P3/P4 debriefs if it shrinks to less than a session's worth.
