# P9 closed: pair direction read from the statement, with the reason written in the code

Course Schedule II (LC 210) was handed in on 2026-11-05 and is correct. It uses Kahn's loop plus `return order if len(order) == numCourses else []`, and agreed with an order validator and a 3-color-DFS oracle on 20 000 random inputs. The direction is right this time, and he wrote down why: `# A dependência é do segundo para o primeiro, por isso é v, u e não u, v` over `for v, u in prerequisites`. This fixes the P8 slip from [[0010-p8-closed-pair-convention-copied-from-drill]]. But the teacher had flagged that P9's direction mattered right before, so this is not yet evidence that he checks conventions unprompted. That stays a probe for L8 and L9.

## Implications

- The topological-sort part of the roadmap (L6, P8, P9) is done. Kahn's, cycle detection by leftover count, and order output are all his.
- He closed with no asks: nothing new to probe, and space is already owed at L9. Type hints, present in P8, were dropped here (`deg`, `adj`, `order`), which is a minor nit.
- Next is L7 (Union-Find), the first undirected-only structure since L4. There is no pair-direction question, so the convention probe moves to L8.
