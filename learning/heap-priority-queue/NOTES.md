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
| L4 | ~~Top-K pattern~~ → **rescoped** (LR-0005) → delivered as *Choosing the key, choosing the direction* (drill `lessons/0004-topk-drill.py`) | lesson + drill | ✅ completed 2026-07-30 — 20/20 checks green, debrief done |
| P3 | K Closest Points to Origin (LC 973, Medium) | problem | 🔵 handed over 2026-07-30 |
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
- **Correction (2026-07-28)**: `python3` on PATH is 3.9.6, but **`python3.14` (3.14.6) is installed** at `/opt/homebrew/bin/python3.14` and is what drills should run under (L3's `__pycache__` is already cpython-314). `X | Y` unions and 3.14 max-heap functions *are* available there. Supersedes the 2026-07-27 note that said otherwise. Drill run lines should say `python3.14`.
- **Harness gotcha, cost me a debug cycle**: since Python 3.13 the compiler **dedents docstrings**, so `src.replace(fn.__doc__, "")` silently strips nothing and every banned token named in the docstring gets flagged in the student's code. L4's `_source_of` now cuts the first triple-quoted block textually instead — copy that version into future drills. (L3 is unaffected only by luck: its docstrings never name a banned token.)
- **Quiz answers leaked position**: L1–L3 used `data-answer="0"` for *every* quiz — correct option always first. L4 varies it. Keep varying it.
- Validate every drill harness in the scratchpad against a reference solution **plus deliberately wrong variants**, not just a correct one. L4's harness was proved to catch: whole-tuple comparison on ties, collect-then-trim (unbounded), unguarded `heapreplace`, and a `sorted()` one-liner.
- L4 can skip the "why not just sort" motivation — Gil raised the `heapify` vs push-loop build-cost question himself at the end of L3 (LR-0004). Open L4 directly at the size-k heap, and fold in `nlargest`/`nsmallest` (the last unmet `heapq` success criterion).
- **L8 must re-test cold**: `heappushpop` vs `heapreplace` — Gil named the right one on P1 but skipped deriving why `heapreplace` breaks a size-k heap, so it was given, not earned (LR-0005). Fluency only; no evidence of storage strength.
- **Ask for complexity per phase, then which dominates** — never one aggregate number (LR-0006). On P2 the aggregate was right while the underlying attribution was wrong (`heapify` blamed for the log factor), and separating the phases is the only thing that surfaces it.
- **Teach the shrinking-quantity argument explicitly in L5** — bounding a loop whose iteration count depends on the data. P2 needed it (2 popped / ≤1 returned ⇒ ≤ n−1 iterations); Gil didn't attempt it. P5 (Task Scheduler) needs it again. Don't assume it transferred.
- **Recurring habit gap**: Gil does not volunteer complexity when handing in a solution — asked for it explicitly in the P1 and P2 briefings, skipped both times, and answers correctly only when pressed. Not a knowledge gap (P1 answers were right, cold). Keep demanding it *before* the code review, every problem, until it's automatic — it's the first interview follow-up question.
- **Graduated to LR-0008 (2026-07-30)**: the hedging-against-his-own-invariants pattern recurred a third time (`next(counter)` to "skip the zero"). See `learning-records/0008-hedges-against-invariants-he-established.md` — when he hands in code, ask him to name the invariant a defensive line protects against instead of just deleting it.
- **Done 2026-07-30**: the withheld Part A cost table is now in `reference/heap-cheat-sheet.html` ("Three strategies, costed per phase"), added at the debrief as planned. The sign-of-the-tiebreaker table went into the same file under "Tie order".
- **L4's designed payoff — delivered at the 2026-07-30 debrief**: he got all 11 cost cells right first pass, including `heapify_all` being O(n) and therefore the time winner over the bounded heap for small k. He did *not* conclude "so the bounded heap is pointless" — but he also did not raise the tension himself; the harness's closing question prompted it. Framing that landed: "ganhar no eixo errado não é ganhar" (memory + streaming are different axes, `heapify_all` doesn't get slower under a memory constraint, it stops being available). Re-test cold at L8.
- Pattern for problem handovers that worked well on P1: no pattern name, no structure name — just "what does the shape of the API tell you about where cost can live" plus one crux question. He needed zero hints. Keep briefings that thin.
- Watch for Python-level slips distinct from topic misconceptions — L3's only bug was storing an `itertools.count()` object instead of `next(counter)`. Naming the symptom ("this output is alphabetical") was enough; no explanation needed. **Second instance (L4 Part C, 2026-07-30)**: he filled `PREDICTIONS` with *string literals of* the lists (`"[('d', 9), ...]"`) instead of the lists. Same family — writing something that renders like the value instead of the value. It cost two rounds because the harness prints with `str()`, so `you predicted [('d', 9)…], heapq produced [('d', 9)…]` looked identical; he reasonably concluded the harness was broken. **Two fixes for future drills: use `{got!r}` in every assertion message, and assert the type before the value.** He waved off the distinction as unimportant ("tanto faz") — worth one calibration pass later, since str-vs-list is the exact class of bug that eats a debug cycle.
- Harness authoring rule earned the hard way (2026-07-30): a drill's assertion messages are teaching surface, not diagnostics. Any message that can print two different objects identically will be read as a harness bug — and the student will stop trusting the feedback loop, which is the whole mechanism.
- **Materials gap Gil reported (2026-07-29)**: `nlargest`/`nsmallest` were *used* heavily in L4 (§1 table, §4 docs quote, §5 ties, Part C) on the strength of two lines in L3 §5 that gave only the signature and O(n log k). He could not tell whether they operate on a heap or on a plain list, what they return, or whether they are Python-specific — and §5's tie discussion was therefore unreadable. Fixed by adding L4 §5 "`nlargest`/`nsmallest`, defined" (contract table, "they build a heap, they do not consume one", the three cost paths incl. the `n==1` and `n>=len` shortcuts, cross-language note), a contract paragraph in L3 §5, and a cheat-sheet subsection. **Lesson for future sessions: when a lesson leans on a stdlib function for a whole section, state its input/output/mutation contract explicitly before reasoning about its behaviour.** A signature plus a complexity is not an introduction.
- Verified 2026-07-27: L3 drill scenarios A/B — pushing `[18, 23, 3, 19, 2]` one at a time gives `[2, 3, 18, 23, 19]`, while `heapify` on the same list gives `[2, 18, 3, 19, 23]`. Both valid; textbook sift-down agrees with CPython on both. Roughly 47% of random 5–7 element lists show this divergence.
