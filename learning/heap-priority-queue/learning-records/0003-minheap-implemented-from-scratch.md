# MinHeap implemented from scratch — all tests green

Gil completed the Lesson 2 drill (`lessons/0002-minheap-drill.py`). All six harness tests pass, including the 300-trial randomised stress test that interleaves pushes and pops against `heapq`.

**Evidence**: verified by running the file on 2026-07-27 — `6 passed, 0 failed, 0 not implemented`. Beyond passing, the implementation shows understanding rather than pattern-matching:

- `_sift_down` avoids both traps named in the lesson: it selects the smaller child, and it bounds-checks both child indices.
- He wrote his own comment justifying the absence of an `elif rc is not None` branch — "rc == lc + 1, so a node can never have a right child without a left one. The tree fills left-to-right." That is the completeness invariant, re-derived unprompted and used to *eliminate* a branch. He is reasoning about the structure, not transcribing an algorithm.
- `heapify` starts at `len // 2 - 1` and walks backwards — the O(n) construction, correct on the first attempt.

**Implications**: The internals half of the mission ("implement a min-heap from scratch in an interview setting") is essentially met. Sift-up, sift-down, pop and bottom-up heapify need no re-teaching — only spaced retrieval, so later lessons should keep one recall question about mechanics rather than re-explaining them.

Teaching should now move from *how a heap works* to *how to wield one fast*: `heapq` API fluency (L3), then straight into problems. Because he re-derives invariants on his own, lessons can state a rule once and ask him to justify it rather than proving it for him. Prediction-before-execution drills are a good fit for this — see [[0002-insertion-mechanics-internalized]] for the earlier evidence that he traces accurately on paper.
