# L6 closed: Kahn's built unaided; "sorted by in-degree" taken for "topological"

The L6 drill was handed in on 2026-11-05, six weeks after the lesson. `in_degrees` and `kahn_order` were correct and idiomatic on the first try: he reused `in_degrees`, used `deque` + `popleft`, and enqueued when the count hit zero. So the core mechanism of L6 has storage strength. `is_topological` was wrong in two ways. It replaced the edge check with a proxy (in-degrees must never decrease along the order, i.e. "sorted by in-degree"). Its duplicate check was `n == len(set(order))`, which a padded list like `[0, 0, 1]` passes. After counterexamples he could say WHY the proxy fails, but he could not write the fix. He asked for the answer, and the teacher gave it (positions dict + every edge points right).

## Evidence

- First run was 19/19 green. That was a harness gap: no test separated the definition from the in-degree proxy. F13 (chain 0→1→2, order `[0, 2, 1]`, wrongly accepted) and F14 (0→1 plus loner 2, `[0, 1, 2]`, wrongly rejected) were added and validated against reference + variants. His code then ran 18/21.
- Ask 1 (why isn't Kahn just a `sorted()`?): "o simples fato do tamanho do indeg não garante a ordem, porque tem a correlação de dependência — 2 e 1 têm indeg = 1, porém 2 depende de 1". Right, and unaided.
- Ask 2 (cold: why `deg[v]` and not `deg[u]`?): "porque é v quem depende de u". The direction is his own reading, not a copied pattern.
- He still could not picture the failing cases, even with ASCII arc diagrams and one hint ("which line of the drawing did your eye use?"). He then said: "não sei corrigir… já estou travado há muito tempo nessa lição".
- The K cells are not evidence. `_K_ANSWERS` sits in plaintext in the file.

## Implications

- **P8/P9 risk.** P9 must return a valid order. If he reasons about the order through in-degree values rather than edges, the same proxy can come back. For his own checks, point him to "every arrow points right" (now in `reference/topological-sort.html`).
- **Re-test cold at L9:** write the order checker from scratch (positions + every edge), and explain why a set's size doesn't prove "exactly once".
- **Pacing.** He is frustrated by time spent in drills relative to roadmap progress (deadline: end of 2026). A drill function that isn't on the path to the next problem should not become a multi-round gate. Offer the fix after one hint round.
