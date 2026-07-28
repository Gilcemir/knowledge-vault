# Working Notes — Heap / Priority Queue

## User preferences
- Conversation in **Portuguese (BR)**; all materials (lessons, reference, records) in **English**.
- **NEVER give solutions** to the 7 NeetCode problems. When stuck, give escalating hints: (1) restate/reframe the problem, (2) point to the pattern, (3) suggest the data-structure shape, (4) discuss a subproblem — never full code.
- Python only. ~30 min per session → one lesson OR one problem attempt per session.
- Baseline (2026-07-24): uses `heapq` push/pop mechanically; near zero on internals. Comfortable with earlier roadmap topics (arrays, binary search, trees, backtracking).

## Track plan

Lessons lead up to problems; problems are solved solo on LeetCode. Order within the problem set follows NeetCode's.

| # | Session | Type | Status |
|---|---------|------|--------|
| L1 | The array that thinks it's a tree (heap anatomy, index math) | lesson | ✅ delivered |
| L2 | Sift-down + build your own MinHeap (skeleton `lessons/0002-minheap-drill.py` + test harness) | lesson + coding drill | ✅ delivered |
| L3 | `heapq` fluency: min-only, negation trick, tuples, pushpop vs replace (drill `lessons/0003-heapq-drill.py`) | lesson + drill | ✅ delivered |
| P1 | Kth Largest Element in a Stream (LC 703, Easy) | problem | ✅ solved solo, no hints |
| P2 | Last Stone Weight (LC 1046, Easy) | problem | ✅ solved solo, no hints |
| L4 | ~~Top-K pattern~~ → **rescoped** (LR-0005): `nlargest`/`nsmallest` + custom priorities only; size-k heap already known | lesson | ⬜ |
| P3 | K Closest Points to Origin (LC 973, Medium) | problem | ⬜ |
| P4 | Kth Largest Element in an Array (LC 215, Medium) | problem | ⬜ |
| L5 | Greedy + heap: scheduling with priorities and cooldowns | lesson | ⬜ |
| P5 | Task Scheduler (LC 621, Medium) | problem | ⬜ |
| L6 | Composing heaps with other structures (heap + hashmap + lists) | lesson | ⬜ |
| P6 | Design Twitter (LC 355, Medium) | problem | ⬜ |
| L7 | The two-heaps pattern (balance invariant) | lesson | ⬜ |
| P7 | Find Median from Data Stream (LC 295, Hard) | problem | ⬜ |
| L8 | Capstone review: spaced retrieval quiz across everything | lesson | ⬜ |

Plan is adaptive — reorder/merge if Gil moves faster or slower than expected. Update Status column as sessions complete.

## Teaching notes
- Gil learns well by tracing on paper and asks cost questions unprompted — lean into hand-traces + complexity reasoning. He got sift-up right cold on the first try (LR-0002).
- Drills should ship with a runnable test harness (immediate automatic feedback). Validate the harness against a reference impl **in the scratchpad**, never in the workspace.
- Verified 2026-07-24: textbook sift-down pop vs `heapq.heappop` — popped value and multiset always match, array arrangement differs in ~10% of random cases, both always valid heaps. Don't let him think that's a bug.
- Quizzes: keep all options the same word count (skill rule).
- After each solved problem, debrief: complexity achieved, pattern named, add learning record if insight is non-obvious.
- Encourage predicting `heapq` internal array states before running code — cheap desirable difficulty. L3's drill formalises this as a `PREDICTIONS` dict checked by the harness; reuse the pattern.
- L3 deliberately teaches `heappushpop`/`heapreplace` as *API mechanics only*, with no top-k framing — the size-k-heap pattern is L4's job and would spoil P1 (LC 703). Keep it that way if L3 is ever revised.
- Verified 2026-07-27: local Python is **3.9.6**. `list[int]` annotations are fine; `X | Y` unions are not (3.10+). No 3.14 max-heap functions available.
- L4 can skip the "why not just sort" motivation — Gil raised the `heapify` vs push-loop build-cost question himself at the end of L3 (LR-0004). Open L4 directly at the size-k heap, and fold in `nlargest`/`nsmallest` (the last unmet `heapq` success criterion).
- **L8 must re-test cold**: `heappushpop` vs `heapreplace` — Gil named the right one on P1 but skipped deriving why `heapreplace` breaks a size-k heap, so it was given, not earned (LR-0005). Fluency only; no evidence of storage strength.
- **Ask for complexity per phase, then which dominates** — never one aggregate number (LR-0006). On P2 the aggregate was right while the underlying attribution was wrong (`heapify` blamed for the log factor), and separating the phases is the only thing that surfaces it.
- **Teach the shrinking-quantity argument explicitly in L5** — bounding a loop whose iteration count depends on the data. P2 needed it (2 popped / ≤1 returned ⇒ ≤ n−1 iterations); Gil didn't attempt it. P5 (Task Scheduler) needs it again. Don't assume it transferred.
- **Recurring habit gap**: Gil does not volunteer complexity when handing in a solution — asked for it explicitly in the P1 and P2 briefings, skipped both times, and answers correctly only when pressed. Not a knowledge gap (P1 answers were right, cold). Keep demanding it *before* the code review, every problem, until it's automatic — it's the first interview follow-up question.
- P2 style signals worth watching (not yet a learning record — application of an already-recorded pattern): he wrote a provably-dead `abs()` over `x - y` where max-heap pop order already guarantees `x >= y`, and hacked `pq.append(0)` to dodge an empty check, breaking the heap invariant harmlessly. Both are hedges against invariants *he himself established*. If this recurs, it becomes a record: he trusts structural guarantees less than he should.
- Pattern for problem handovers that worked well on P1: no pattern name, no structure name — just "what does the shape of the API tell you about where cost can live" plus one crux question. He needed zero hints. Keep briefings that thin.
- Watch for Python-level slips distinct from topic misconceptions — L3's only bug was storing an `itertools.count()` object instead of `next(counter)`. Naming the symptom ("this output is alphabetical") was enough; no explanation needed.
- Verified 2026-07-27: L3 drill scenarios A/B — pushing `[18, 23, 3, 19, 2]` one at a time gives `[2, 3, 18, 23, 19]`, while `heapify` on the same list gives `[2, 18, 3, 19, 23]`. Both valid; textbook sift-down agrees with CPython on both. Roughly 47% of random 5–7 element lists show this divergence.
