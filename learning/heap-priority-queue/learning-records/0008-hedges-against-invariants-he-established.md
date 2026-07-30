# Gil hedges against invariants he himself established

Third instance, so this graduates from a watch-item in [[NOTES.md]] to a record. He writes defensive code against properties his own structure already guarantees:

1. **P2** — `abs()` over `x - y` where max-heap pop order already guarantees `x >= y`. Provably dead.
2. **P2** — `pq.append(0)` to dodge an empty-heap check, breaking the heap invariant (harmlessly, by luck).
3. **L4 Part B (2026-07-30)** — `next(counter)` called once before the loop to "pular o zero, caso esse caso de borda aconteça no primeiro caso". There is no such edge case: `-0 == 0`, and `0` already outranks every later `-1, -2, …`. He had *just* used the fact that only relative order matters.

**The shape**: each hedge guards a case he could rule out by reading the invariant he just wrote. It is not a knowledge gap — in all three he could state the guarantee when asked. It is a **trust gap**: structural guarantees do not yet feel load-bearing enough to build on without a belt-and-braces check.

**Why it matters beyond style**: the cost is not the wasted line, it is that hedging *suppresses the derivation*. Instance 3 is the clearest case — had he asked "does the starting value of the counter matter?", the answer (no, only monotonicity) is the same reasoning that fixes the sign bug he was about to hit two lines later. The hedge let him skip the question.

**Implications**:

- When he hands in code, ask him to **name the invariant a defensive line is protecting against**, and whether the surrounding code can already violate it. Do not just delete the line — the derivation is the lesson.
- Expect this in L7 (two heaps): the balance invariant is precisely the kind of guarantee he will want to re-check defensively inside the loop instead of relying on. Good place to make the habit visible.
- Separate, opposite-facing observation from the same session, not yet a pattern: when the drill harness rejected his Part C answers, his first read was that the harness had misjudged him rather than that his input was wrong (they were strings, not lists — identical on screen under `str()`, different types). Trusting his own output over the mechanism, while distrusting his own invariants. Watch whether either recurs.
