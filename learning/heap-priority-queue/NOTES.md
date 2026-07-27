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
| L3 | `heapq` fluency: min-only, negation trick, tuples, heapify O(n) | lesson | ⬜ |
| P1 | Kth Largest Element in a Stream (LC 703, Easy) | problem | ⬜ |
| P2 | Last Stone Weight (LC 1046, Easy) | problem | ⬜ |
| L4 | The Top-K pattern: size-k heap vs heapify-all, custom priorities | lesson | ⬜ |
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
- Encourage predicting `heapq` internal array states before running code — cheap desirable difficulty.
