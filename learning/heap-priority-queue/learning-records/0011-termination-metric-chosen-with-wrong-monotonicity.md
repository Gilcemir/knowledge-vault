# Termination metric chosen with the wrong monotonicity

On the L5 drill (2026-08-04/05), Part A asked for the **shrinking quantity** that bounds the scheduling loop. Gil answered `"ticks elapsed"` — a quantity that only ever **increases** — and held it through the harness hint, whose first two sentences literally say a valid Q "drops by at least 1 every time the body runs" and "ticks elapsed goes UP".

**Root cause: "tracks progress" was conflated with "shrinks".** A progress bar and a termination metric are mirror images (Q = total − progress), and he reached for the progress-bar side. The harness hint failed because it corrected the *choice* without restating the *purpose*; what fixed it was re-anchoring what Q is for — proving the loop ends — plus one discriminating scenario: **all n orders arrive at tick 0**. After the first release, "orders not yet arrived" is 0 and frozen for n iterations (violating "decreases every iteration"), while "orders not yet processed" keeps falling by 1 at every `res.append` until the loop exits. He fixed it from that alone; the correct answer was never stated.

**Second bug, same session, different family**: the tie rule in the docstring names **three** levels (priority, arrival, name) and his heap tuple carried **two** (`(-priority, name)`), silently substituting name-order for arrival-order on priority ties. Two tests failed from this one omission (the targeted tie case and the 300-case oracle stress — first divergence at two equal-priority orders where the earlier arrival had the later name). The tell was already on his screen: Pylance's *`"arr" is not accessed`* on the unpacking line. An unused-variable warning on **unpacked domain data** is a policy bug, not lint noise — the spec said three fields decide, the code used two.

**What went right**: every other Part A cell — both iteration bounds (n vs T), all three phase costs, and `"tie"` for dominance — was correct on the first pass, unprompted. The per-phase format modelled in [[0010-per-phase-cost-demanded-four-times-never-defined]] appears to have transferred, at least on a lesson-scaffolded surface.

**Implications**:

- P5 needs the shrinking-quantity argument again, on a loop whose natural "progress" metrics also go up. Watch for the same inversion; the "mirror image" framing (Q = total − progress) is the repair that worked.
- L8 re-test cold: given a data-dependent loop, name a valid Q — including at least one distractor quantity that increases.
- When a harness hint is read but not absorbed, the missing piece is usually the *purpose* of the concept, not more detail about the choice. Restate what the thing is for, then let the hint land.
- Teaching move worth reusing: a **discriminating scenario** ("all arrive at tick 0") beats naming the answer — it let him reject one candidate and earn the other in a single step.
