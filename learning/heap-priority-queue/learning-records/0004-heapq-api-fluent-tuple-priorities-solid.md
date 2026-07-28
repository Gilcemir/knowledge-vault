# `heapq` API fluent; tuple priorities understood, including the tie-break slot

Gil completed the Lesson 3 drill (`lessons/0003-heapq-drill.py`) with all 12 harness checks green. He predicted all six Part A array states correctly on paper before running — including the A-vs-B divergence, where five `heappush` calls and one `heapify` on the same input produce different valid arrays. The `heapq` API layer needs no further teaching; the `(priority, counter, payload)` pattern is now his.

**Evidence** (verified by running the file on 2026-07-27):

- Part A: 6/6 predictions correct cold, no back-filling.
- `descending()`: reached for the negation trick without prompting.
- `dispatch()`: reached for `itertools.count()` as a tie-breaker *unprompted* — the counter was his own idea, not a hint. He had not been told the canonical three-slot tuple pattern.

**The one bug, and why it matters.** He wrote `(priority, counter, task.name)` — storing the *iterator object* rather than `next(counter)`. Because the same object sat in every tuple, slot 2 compared equal and tuple comparison silently fell through to slot 3, sorting by name. Two tests failed with alphabetical output (`t0, t1, t10, t2, ...`). Given only the observation "this output is alphabetical, look at what's actually in slot 2", he fixed it immediately. This is an *iterator-vs-value* slip, not a heap misconception — worth remembering as a Python-level blind spot, not a topic blind spot.

**Two things he asked unprompted**, both of which show he is reasoning past the exercise:

1. Whether the `int` in `list[tuple[int, Task]]` was a priority or an enumerator — i.e. he wanted the *contract*, not just a passing test.
2. Whether `heapify` could replace the `heappush` loop. Answered: same O(n log n) total once the n pops dominate, and the real distinction is availability (batch vs streaming), not speed.

**Implications**: That second question is L4's material arriving early. He is already thinking about build-cost trade-offs, so **L4 can skip re-motivating "why not just sort" and open directly at the size-k heap**. The mission's `heapq`-fluency success criterion is met except for `nlargest`/`nsmallest`, which L4 should absorb.

P1 (LC 703) is next and is deliberately unspoiled — L3 taught `heappushpop`/`heapreplace` as bare API mechanics with no top-k framing (see [[NOTES.md]]), so the size-k insight is still his to discover. See [[0003-minheap-implemented-from-scratch]] for the internals half of the mission, now complete.
