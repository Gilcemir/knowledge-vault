# Baseline: mechanical heapq user, no internals

Gil (2026-07-24) reports he can use `heapq.heappush`/`heappop` in problems but describes his conceptual understanding as "near zero" — he does not know the array representation, the heap property, or why operations cost O(log n). He has completed earlier NeetCode roadmap nodes (arrays, binary search, trees, backtracking), so binary-tree vocabulary, recursion, and big-O reasoning can be assumed.

**Implications**: Start at heap anatomy, not at "what is big-O". The `heapq` API itself needs polish (max-heap trick, tuples, heapify) but not introduction. The from-scratch MinHeap drill (L2) is the highest-value early target since it directly attacks the stated gap.
