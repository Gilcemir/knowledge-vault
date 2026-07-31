# The `n`/`k` naming collision inverted the `nsmallest` cost

On the P3 debrief (2026-07-31) Gil solved LC 973 with `heapq.nsmallest(k, pq)` and stated its cost as **`k log n`** — exactly inverted from the correct `O(n log k)`. He held that answer across one full Socratic round, restating it as "n + k log n (n para montar heap internamente, k para o motivo que eu disse antes)" after being pointed at L4's three-strategy table.

**Root cause, which he confirmed the moment it was named**: `heapq`'s signature is `nsmallest(n, iterable)`, where heapq's `n` is *the caller's `k`*. L4 §5 and the cheat sheet both quote the stdlib naming. With the two `n`s crossed, `O(n log k)` reads as `O(k log n)` — the inversion is not a slip, it is the mechanical consequence of the collision.

**Why this is not noise**: what he described — `O(n)` to heapify internally, then `k` pops at `log n` each — is a *coherent and correct* algorithm. It is the heapify-all-then-pop-k strategy from L4's own cost table, which he got fully right at the L4 debrief (11/11 cells). So he substituted a strategy he knows well for the one he actually called. Same failure family as [[0006-heapify-cost-misattributed-under-composition]]: under composition he reaches for the most memorable named cost instead of tracing the phases in front of him.

**What makes it sharper**: the *contract* half of L4 §5 landed cleanly — asked whether `pq` was a heap, he said no and correctly invoked that `nsmallest` builds its own rather than consuming one. So API fluency and the mutation contract are solid while the cost model is not. The "materials gap" fix from 2026-07-29 taught the contract and left the cost under-anchored.

**What actually fixed it**: reading the CPython source, specifically `result = [(elem, i) for i, elem in zip(range(n), it)]` followed by `heapify_max(result)` and a `for elem in it` loop over the remainder. Two rounds of prose plus a pointer to the cheat-sheet table failed; one look at `zip(range(n), it)` closed it in a single round, and he generalised unprompted to `nlargest` as well.

**Residual imprecisions in his final answer** (minor, corrected in place): he named the per-element operation `heappushpop` where the source uses `heapreplace_max` behind an `if elem < top` guard, so the `log k` is paid only by elements that actually qualify; and he omitted `heapify_max` on the first `k` (`O(k)`) and the closing `result.sort()` (`O(k log k)`), neither of which changes the dominant term.

**Implications**:

- **Never write `n` for the count** when discussing `nlargest`/`nsmallest` in this workspace. Always the caller's `k`, and say "heapq spells this parameter `n`" explicitly as a warning. Audit L4 §5 and the cheat sheet for bare stdlib naming.
- **For stdlib cost questions, show the source before writing prose.** Three rounds of explanation lost to one `inspect.getsource`. This generalises beyond `heapq`.
- L8 must re-test `nlargest`/`nsmallest` cost **cold**, with the caller's variable named `k`, and must not accept the aggregate alone — ask which phase the `log` lives in.
- Third consecutive problem (P1, P2, P3) where per-phase costs were requested explicitly and only the middle phase came back. See [[NOTES.md]].
