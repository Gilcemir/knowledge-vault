# `heapify` cost misattributed when two phases compose

On the P2 debrief (2026-07-28) Gil gave the right total — O(n log n) time, O(n) space — but credited the log factor to `heapify`, saying "tempo é n log n, do heapify". `heapify` is O(n). The log factor comes from the `while` loop's up-to-n−1 iterations at O(log n) each.

**Why this is not simply forgotten knowledge**: he stated `heapify` is O(n) correctly at the end of L3, and *used* that fact correctly one problem earlier — on P1 he reasoned unprompted that heapify-all-then-trim loses to a size-k heap precisely because O(n) + (n−k) log n exceeds O(n log k) for small k (see [[0005-size-k-heap-pattern-derived-independently]]). So the isolated fact is solid. It broke down when **two phases had to be composed and the dominant one identified** — he reached for the most memorable named operation as the source of the cost instead of adding the phases and comparing.

**The step he actually skipped**: counting the loop's iterations. The loop bound is data-dependent (a stone is sometimes pushed back, sometimes not), so it needs the shrinking-quantity argument — 2 popped, at most 1 returned, therefore at least one stone consumed per iteration, therefore at most n−1 iterations. He did not attempt this and did not flag it as the hard part.

**Implications**:

- Future debriefs must ask for complexity **per phase**, then which dominates — not one aggregate number. The aggregate can be right while the model underneath is wrong, and that is invisible unless the phases are separated.
- L5 (greedy + heap scheduling) and P5 (Task Scheduler) both hinge on bounding data-dependent loops. Teach the monotonically-decreasing-quantity argument explicitly there rather than assuming it transfers from here.
- Pair this with the habit gap in [[NOTES.md]]: he does not volunteer complexity unprompted. Both point the same way — analysis is being treated as an afterthought to the code rather than part of it.
