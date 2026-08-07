# Shrinking-quantity argument transferred; pairing argument produced unprompted

On P5 (LC 621, solved solo 2026-08-07 with only the standard handover briefing), Gil chose a correctly-monotone Q on the first attempt — "tasks not yet executed" — the exact skill that needed a discriminating scenario to repair on L5 (see [[0011-termination-metric-chosen-with-wrong-monotonicity]], whose implication predicted this might not transfer). Better: his loop has jump-the-clock iterations where Q freezes, and he defended the bound with the **pairing argument** ("every jump lands on an instant where a task is guaranteed eligible, so the next iteration executes") without the argument being named or hinted. The name was given only after he produced the reasoning.

**Evidence**: full per-phase cost table (T + m + T·log m + O(1)) with one self-corrected slip (phase 2 first given as T, recounted to m in one round); the log m = log 26 → O(T) bounded-alphabet collapse volunteered unprompted; jump-the-clock chosen in his own code without the tick-by-tick trap ever being mentioned for this problem; "queue sorted by construction — n fixed, time monotone, so appends arrive in order" earned in a single question round.

**Implications**:

- The L5→P5 chain (scaffolded drill → unscaffolded problem) worked end to end; keep the lesson-then-problem spoiler discipline for L6→P6 and L7→P7.
- His code carried **zero defensive hedges** — `if not pq: time = queue[0][0]` trusts the loop invariant with no extra guard. First clean counter-instance to [[0008-hedges-against-invariants-he-established]].
- L8 can lighten the Q re-test: still include one distractor quantity that increases (per LR-0011), but the pairing case can be a recall question rather than a re-derivation.
