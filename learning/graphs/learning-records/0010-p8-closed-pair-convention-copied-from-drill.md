# P8 closed: Kahn's transferred unaided, but the pair direction was copied from the drill

Course Schedule (LC 207) was handed in on 2026-11-05 and is correct: Kahn's loop with a counter of popped courses, `return visited == numCourses`. The cycle check was his own idea, proposed before he coded it ("se sobrou alguém com deg != 0, houve um ciclo"). Teacher's one nudge was that the leftover set is the never-popped set. He did not read LC's pair convention, though. `for u, v in prerequisites: adj[u].append(v)` reuses the drill's "[u, v] = u before v", so `[a, b]` became a→b while the statement means b→a. He built the transpose G^T. LC accepted it only because a graph and its transpose are either both cyclic or both acyclic.

## Evidence

- His code agreed with an independent 3-color-DFS oracle on 20 000 random inputs (scratchpad).
- Probe "draw Example 1's `[1, 0]` per the statement and per your `adj`": he first answered "não entendi". Once prompted, he guessed "estou usando a seta ao contrário?". The teacher confirmed it with the drawing.
- Probe "why was it accepted?": "porque esse problema só precisa de identificar o ciclo". That is the right reason, but the explicit invariant was not stated: reversing every arrow keeps every cycle. The teacher completed it (0→1→2→0 reversed is 0→2→1→0) and tied it to L5's transpose.
- Cost: time column all right, unasked total O(V + E). The space column was left blank, the third time (P5, P6/P7). The teacher supplied it: O(V + E).

## Implications

- **P9 (Course Schedule II):** the direction now matters, because the order would come out reversed. The risk is flagged to him. Don't re-hint it; check it at the hand-in.
- **Pattern:** he carries the last input convention he used into the next problem without reading the new statement. At L8 (Word Ladder) and L9, give inputs whose convention differs from the previous drill, and see if he checks unprompted.
- **Space is still never volunteered.** Re-probe cold at L9 (already owed from [[0008-p6-p7-closed-reverse-question-vs-flip-comparison]]).
