# Sift-up / insertion mechanics internalized

Gil traced inserting `4, 8, 2, 6, 1` into an empty min-heap on paper and produced `[1, 2, 4, 8, 6]` — correct on the first attempt, without running code. Before that, he asked a sharp unprompted question ("if I pop 3 times, do I get the 3 smallest?") and correctly intuited the `3 × O(log n)` cost, showing he was reasoning about the structure rather than memorizing steps.

**Evidence**: correct final array from a cold paper trace; correct cost estimate for k pops volunteered before being taught.

**Implications**: Sift-up needs no re-teaching. Lesson 2 can go straight to sift-down (with heavy emphasis on the *smaller-child* rule, the classic bug) and then to the from-scratch `MinHeap` implementation drill. He has also already been told the pop procedure verbally in conversation, so the lesson should treat pop as consolidation + implementation, not first exposure. His instinct to ask "how does this cost out?" suggests complexity reasoning can be pushed harder — the O(n) heapify argument is in range.
