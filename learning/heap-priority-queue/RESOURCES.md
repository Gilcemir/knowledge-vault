# Heap / Priority Queue Resources

## Knowledge

- [Docs: `heapq` — Heap queue algorithm (Python official docs)](https://docs.python.org/3/library/heapq.html)
  The canonical API reference, plus a superb "Theory" essay at the bottom explaining why heaps are useful and how the array representation works. Use for: API details, priority-queue implementation notes (tuples, tie-breaking, entry invalidation).
- [Lecture: MIT 6.006 (Spring 2020) — Lecture 8: Binary Heaps](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-8-binary-heaps/)
  Rigorous but accessible derivation of heap structure, sift operations, and the O(n) build-heap argument. Use for: the "why" behind complexities; watch when a lesson's claim needs deeper grounding.
- [Book: _Introduction to Algorithms_ (CLRS), Chapter 6 — Heapsort](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
  The formal treatment: max-heapify, build-max-heap, heapsort, priority queues. Use for: precise pseudocode and proofs when the interactive material feels hand-wavy.
- [Tool: VisuAlgo — Binary Heap visualization](https://visualgo.net/en/heap)
  Animated insert/extract on a binary heap, showing tree and array views side by side. Use for: watching sift-up/sift-down happen before implementing them.
- [Tool: USFCA — Interactive heap visualization (David Galles)](https://www.cs.usfca.edu/~galles/visualization/Heap.html)
  Simpler alternative visualizer; lets you drive operations step by step. Use for: hand-tracing practice checks.
- [Code: CPython `heapq` source](https://github.com/python/cpython/blob/main/Lib/heapq.py)
  The real implementation of `_siftup`/`_siftdown`, heavily commented. Use for: comparing your from-scratch heap against production code (after writing your own — not before).
- [Videos: NeetCode YouTube channel](https://www.youtube.com/@NeetCode)
  Per-problem walkthroughs for all 7 roadmap problems. **Use only AFTER an honest solo attempt** — these contain full solutions, which violates the mission if watched early.

## Wisdom (Communities)

- [r/leetcode](https://www.reddit.com/r/leetcode/)
  Active community for interview prep; good for pattern discussions and "am I ready?" calibration. Use for: comparing approaches after solving, prep-strategy questions.
- [LeetCode problem discussion tabs](https://leetcode.com/problemset/)
  Each problem's Discuss tab has idiomatic Python solutions and complexity debates. Use for: post-solve comparison — how did others do it, and is my complexity optimal?
- [NeetCode Discord](https://discord.gg/ddjKRXPqtk)
  The community around the roadmap itself. Use for: asking about problem variants and roadmap sequencing.

## Gaps

- No single high-trust source covers the **two-heaps pattern** (needed for Find Median from Data Stream) at tutorial depth without spoiling the problem — lesson for that will need to be built carefully from first principles.
