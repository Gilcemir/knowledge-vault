# Tie-break counters need a *sign*, derived from the heap's direction

On L4's Part B (2026-07-30) Gil reached for an `itertools.count()` tiebreaker **unprompted** — the decorated-tuple pattern is his now — but signed it wrong: a positive counter in a min-heap of size k makes the *earliest* arrival the smallest, and the smallest is exactly what `heappushpop` evicts. The drill's tie test failed with `['b', 'c']` where `{'a', 'b'}` was required. One hand-trace of three equal-`ms` pushes was enough; he fixed it to `-next(counter)` and then generalised correctly on his own ("só a ordem relativa importa").

**Why this is worth recording**: the missing step was not the counter, it was *choosing the direction of the comparison from the direction of the heap*. He knew ties needed breaking and knew how to encode a tiebreaker — but treated the counter as a symmetric "desempate" rather than as a policy with a winner and a loser. The generalisation he needs, and now has: **make the item you want evicted the extreme your heap discards.** Same shape as the direction table he already had for the key (min-heap to select the k largest); he had not connected the two.

**Evidence it stuck**: asked to explain Part C afterwards, he did not need the `nlargest`/`nsmallest` sign difference explained twice — the opposite signs (`0, -1, -2…` vs `0, 1, 2…`) read as a consequence of min-vs-max rather than as two arbitrary facts to memorise.

**Implications**:

- L7 (two heaps) is direction reasoning end to end — two heaps pointing opposite ways, with an invariant across them. This record is the prerequisite; open L7 by having him re-derive the sign rule cold rather than restating it.
- Pair with [[0005-size-k-heap-pattern-derived-independently]]: he derives *which* structure, and now *which direction*, but both times the derivation appeared only after a concrete failing case. Keep making the failing case cheap and immediate — the drill harness did the teaching here, not the lesson prose.
- He hedged against `-0` being a special case before the tie test even ran (see [[0008-hedges-against-invariants-he-established]]).
