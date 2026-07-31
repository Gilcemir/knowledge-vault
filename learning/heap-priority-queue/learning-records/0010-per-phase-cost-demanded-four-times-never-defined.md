# "Custo por fase" was demanded four times and never defined

On the P4 debrief (2026-07-31) Gil solved LC 215 with `heapq.nlargest(k, nums)[-1]` and answered the cost question with `n log k` — the correct aggregate. Asked again for the cost **per phase**, he replied: *"Eu estou errando porque não estou entendendo a pergunta. Respondi o tempo que leva. O que faltou?"*

**Root cause: the demand was never operationalised.** `NOTES.md` had carried "ask for complexity per phase, then which dominates" since LR-0006, and it was asked on P1, P2, P3 and P4. It was recorded four times as a *habit gap* — "Gil does not volunteer complexity" — when at least part of it was a **vocabulary gap**. To him, "quanto custa" and "custa quanto por fase" were the same question, so he answered the one he understood and looked like he was skipping the other. Four sessions of friction attributed to motivation instead of definition.

**What fixed it**: showing the shape of the wanted answer with a worked table on a strategy he had already costed correctly (heapify-all + k pops, from L4), explicitly labelled as *the format, not the content*. Plus the pedagogical why: the aggregate can be right while the attribution is wrong (P2), a wrong aggregate can come from a coherent-but-substituted strategy (P3, LR-0009), and decomposition is what exposes that "who dominates" shifts with the parameters.

**Second failure in the same session, mine**: after he asked what was missing, I answered with more prose and four fresh open questions. He came back with *"Seu texto está muito confuso... Só me dê a resposta e o porquê e vamos seguir."* Socratic pressure has a budget, and it was already spent by the third round on the same point. LR-0009 said the same thing one day earlier (*source before prose*) and I still front-loaded prose.

**A real knowledge gap surfaced underneath**: he could not read `zip(range(k), it)` at all — `zip` itself was unknown, which made the whole `nlargest` source unreadable and made "how many elements enter the seed?" unanswerable. He asked for it to be unpacked into primitives, which was the right call. Running it (executable, not prose) settled it: `zip` stops at the shorter side, so exactly `k` pairs come out of a 7-element input, and `it` keeps its position so the following `for elem in it` resumes at element `k+1` — which is *why* the sweep is over `n − k`.

**Bonus finding from my own bug**, worth keeping: unpacking that line as `for elem in it: if i >= k: break` produces an identical seed list but consumes `k + 1` elements, silently eating one candidate. That is the reason `heapq` uses `zip` rather than a guarded loop, and it demonstrated an off-by-one that no amount of reading would have.

**His final answer, corrected**: seed O(k) (he said O(n) — the same `n`/`k` substitution family as [[0009-nk-naming-collision-inverted-nsmallest-cost]]); sweep O((n − k) log k); closing sort O(k log k). Dominance genuinely depends on `k` — sweep for small `k`, closing sort for `k` near `n`, crossover near `k ≈ n/2` — and I had to correct my own framing, which implied it was `k`-independent. `O(n log k)` bounds both regimes, so his opening aggregate was right.

**Implications**:

- **Define a demand before repeating it.** If the same request is skipped twice, the next move is to model the answer format, not to ask a third time. Re-read old "habit gap" notes for other demands that may never have been defined.
- **Show the wanted format on already-mastered content**, labelled as format-not-content, so the modelling costs no new thinking.
- **Ask at most one open question per round** during debriefs. Four stacked questions read as an interrogation and cost him the thread.
- **When he says "just give me the answer"**, give it plainly and move on — the Socratic budget for that point is gone. Re-test cold at L8 instead.
- **Never assume Python built-ins are known** just because the topic is advanced. `zip`, `iter`, iterator position and `next()` were all load-bearing here and none had been taught. Same family as the 2026-07-29 materials gap: leaning on a function whose contract was never stated.
- L8 must re-test the `nlargest` per-phase table cold, including the two dominance regimes.
