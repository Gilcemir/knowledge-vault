"""
Lesson 2 drill — build a MinHeap from scratch.

HOW TO USE THIS FILE
    1. Fill in the four TODOs below. Do NOT import heapq in your implementation.
    2. Run it, from the repo root:
           python3 learning/heap-priority-queue/lessons/0002-minheap-drill.py
    3. The test harness at the bottom gives you immediate pass/fail feedback,
       including a random stress test against Python's own heapq.
    4. Only after all tests pass, compare your code with the real thing:
       https://github.com/python/cpython/blob/main/Lib/heapq.py

There are no solutions in this file, and your teacher will not give you one.
If you are stuck, ask for a hint — you will get the smallest hint that unblocks you.
"""


from collections.abc import Iterable


class MinHeap:
    def __init__(self) -> None:
        # The heap is just a flat list. Index math does the rest:
        #   parent(i) = (i - 1) // 2      left(i) = 2*i + 1      right(i) = 2*i + 2
        self._data: list[int] = []

    def __len__(self) -> int:
        return len(self._data)

    def peek(self) -> int:
        if len(self) == 0:
            raise IndexError('peek from empty heap')
        return self._data[0]

    def push(self, item: int) -> None:
        next_idx = len(self)
        self._data.append(item)
        self._sift_up(next_idx)

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent_idx = (idx - 1) // 2
            if self._data[idx] < self._data[parent_idx]:
                self._data[idx], self._data[parent_idx] = self._data[parent_idx], self._data[idx]
            else:
                break

            idx = parent_idx


    def _sift_down(self, idx: int) -> None:
        l = len(self)
        if l == 0:
            return

        while idx < l:
            lc = 2 * idx + 1 if 2 * idx + 1 < l else None
            rc = 2 * idx + 2 if 2 * idx + 2 < l else None

            # No `elif rc is not None` branch: rc == lc + 1, so a node can never
            # have a right child without a left one. The tree fills left-to-right.
            candidate = None
            if lc is not None and rc is not None:
                candidate = lc if self._data[lc] < self._data[rc] else rc
                candidate = candidate if self._data[candidate] < self._data[idx] else None
            elif lc is not None and self._data[lc] < self._data[idx]:
                candidate = lc

            if candidate is None:
                break

            self._data[candidate], self._data[idx] = self._data[idx], self._data[candidate]
            idx = candidate

    
    def pop(self) -> int:
        if len(self) == 0:
            raise IndexError('pop from empty heap')

        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        popped = self._data.pop()

        self._sift_down(0)

        return popped        
    
    @classmethod
    def heapify(cls, items: Iterable[int]) -> "MinHeap":
        pq = cls()
        pq._data = list(items)
        n = len(pq._data) // 2 - 1
        for i in range(n, -1, -1):
            pq._sift_down(i)

        return pq


# ----------------------------------------------------------------------------
# TEST HARNESS — do not edit below this line.
# ----------------------------------------------------------------------------

import heapq
import random


def _is_valid_min_heap(data):
    return all(data[(i - 1) // 2] <= data[i] for i in range(1, len(data)))


def _check(name, fn):
    try:
        fn()
    except NotImplementedError:
        print(f"  ..  {name} — not implemented yet")
        return None
    except AssertionError as e:
        print(f"  FAIL  {name}: {e}")
        return False
    except Exception as e:
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")
        return False
    print(f"  ok    {name}")
    return True


def test_empty_behaviour():
    h = MinHeap()
    assert len(h) == 0, "a fresh heap should have length 0"
    for method in ("peek", "pop"):
        try:
            getattr(h, method)()
        except IndexError:
            pass
        else:
            raise AssertionError(f"{method}() on an empty heap must raise IndexError")


def test_push_keeps_invariant():
    h = MinHeap()
    for x in [4, 8, 2, 6, 1]:
        h.push(x)
        assert _is_valid_min_heap(h._data), f"heap property broken after pushing {x}: {h._data}"
    assert h.peek() == 1, f"peek() should be 1, got {h.peek()}"
    assert len(h) == 5, f"len() should be 5, got {len(h)}"


def test_pop_returns_sorted_order():
    h = MinHeap()
    values = [37, 4, 19, 4, 91, 0, 55, 12, 12, 78]
    for x in values:
        h.push(x)
    out = [h.pop() for _ in range(len(values))]
    assert out == sorted(values), f"pops should come out ascending; got {out}"
    assert len(h) == 0, "heap should be empty after popping everything"


def test_pop_keeps_invariant_midway():
    h = MinHeap()
    for x in random.Random(1).sample(range(200), 40):
        h.push(x)
    for _ in range(20):
        h.pop()
        assert _is_valid_min_heap(h._data), f"heap property broken mid-pop: {h._data}"


def test_heapify_is_valid_and_correct():
    items = [9, 3, 7, 1, 8, 2, 5]
    h = MinHeap.heapify(items)
    assert isinstance(h, MinHeap), "heapify() should return a MinHeap instance"
    assert _is_valid_min_heap(h._data), f"heapify produced an invalid heap: {h._data}"
    assert sorted(h._data) == sorted(items), "heapify must not lose or invent elements"
    out = [h.pop() for _ in range(len(items))]
    assert out == sorted(items), f"popping a heapified heap should be ascending; got {out}"


def test_interleaved_stress_against_heapq():
    rng = random.Random(99)
    for trial in range(300):
        mine, ref = MinHeap(), []
        for _ in range(rng.randint(1, 60)):
            if ref and rng.random() < 0.4:
                got, want = mine.pop(), heapq.heappop(ref)
                assert got == want, f"trial {trial}: pop gave {got}, heapq gave {want}"
            else:
                v = rng.randint(-50, 50)
                mine.push(v)
                heapq.heappush(ref, v)
            assert len(mine) == len(ref), f"trial {trial}: length drifted"
            assert _is_valid_min_heap(mine._data), f"trial {trial}: invalid heap {mine._data}"
            if ref:
                assert mine.peek() == ref[0], f"trial {trial}: peek mismatch"


TESTS = [
    ("empty heap raises properly", test_empty_behaviour),
    ("push keeps the heap property", test_push_keeps_invariant),
    ("pops come out ascending", test_pop_returns_sorted_order),
    ("pop keeps the heap property", test_pop_keeps_invariant_midway),
    ("heapify builds a valid heap", test_heapify_is_valid_and_correct),
    ("stress test vs heapq", test_interleaved_stress_against_heapq),
]

if __name__ == "__main__":
    print("\nMinHeap drill — Lesson 2\n")
    results = [_check(name, fn) for name, fn in TESTS]
    passed = results.count(True)
    todo = results.count(None)
    failed = results.count(False)
    print(f"\n{passed} passed, {failed} failed, {todo} not implemented")
    if failed == 0 and todo == 0:
        print("\nAll green. Now read CPython's heapq.py and see how it differs from yours:")
        print("https://github.com/python/cpython/blob/main/Lib/heapq.py\n")
    else:
        print("\nKeep going. Ask your teacher for a hint if you are stuck.\n")
