# P4 closed — and a teacher error: the hand-in probes were front-run

P4 (Rotting Oranges, LC 994) accepted 2026-09-17, closing the P4–P5 pair out of order (P5 first, [[0006-p5-closed-walls-and-gates]]). The code is clean. The teaching around it was not: **the teacher answered the planned probes before the protocol was loaded**, so this hand-in produced far less evidence than it should have.

## Evidence

Accepted on LeetCode (no file in repo, per standing rule). Final version: single `fresh` counter up front, `while q and fresh`, grid itself as the visited mark (`== 1` tests, `= 2` marks — no `seen` set), `-1 if fresh else t`.

Gil also volunteered his **first version**, unprompted, with the judgement "ficou mais verboso e mais difícil de entender":

- v1 used `while q:` with no `fresh` guard, a `seen` set, a `rotten_count`, a trailing full-grid scan for leftover `1`s, and `return t - 1 if rotten_count > 0 else 0`.
- Both versions are correct. v1 is the off-by-one **discovered empirically and patched** (`t - 1`) plus a guard for the no-sources case; v2 is the same insight moved into the loop condition, where it costs nothing.

## Implications

- **The P4 probes are burned — do not count them.** Before `/teach` was invoked, the teacher gave away, unprompted: the correctness verdict, the whole `and fresh` off-by-one analysis with edge cases, and the full time/space answer. Only the third followed anything Gil produced. The two clean probes that survived (two-scans-vs-one; construct the counterexample for dropping `and fresh`) were **never answered** — he moved to the next lesson instead. Re-probe both cold at L9.
- **He volunteered complexity unasked, for the first time.** "Todos os dois tem o mesmo tempo/espaço O(m·n)" — the heap-track watch item ("never volunteers per-phase complexity") is finally moving on its own. Partial credit only: a lump total rather than per phase, and wrong twice in the justification — called it "pior caso" (the seeding scan alone forces Θ(m·n) on every input; there is no cheaper case) and treated the two solutions' space as identical (P5 pays `seen` unconditionally; P4 has no `seen`, so its O(m·n) is a worst-case frontier only). **Keep pasting the empty per-phase table; stop treating silence as the default.**
- **v1 → v2 is the real result of this problem.** He shipped a correct solution, disliked it, and rewrote it — trading a trailing scan for an up-front counter and a compensating `t - 1` for an honest loop condition. Nobody asked him to. That is taste developing, and it is worth more than the probes that were lost. Name it back to him.
- **Open, unbilled: both versions make two full passes over the grid** (v2: `sum(...)` then the deque comprehension; v1: seeding scan then the trailing leftover scan). One pass can do both jobs with an `elif`. He has not seen this. It is a per-phase-granularity observation — good material for the L9 capstone, or a throwaway nudge if a future grid problem repeats the pattern.
- **Type hints inconsistent across the two files handed in the same day**: P5 annotates its locals, P4 annotates none. The mission says type hints everywhere. Low-grade; flag on recurrence.
- Sentinel-vs-data ([[0006-p5-closed-walls-and-gates]]) did not recur — P4 had no sentinel to confuse.
- **Next: L5** (thinking from the boundary inward), delivered same day → unlocks P6 (Pacific Atlantic) and P7 (Surrounded Regions).

## Process note

`/teach` is user-invocation-only; the skill tool refuses it. When Gil pastes a hand-in cold, the protocol is **not** loaded, and reviewing "helpfully" in that state destroys the session's evidence. Correct move next time: answer nothing of substance, say the protocol needs `/teach`, and wait.
