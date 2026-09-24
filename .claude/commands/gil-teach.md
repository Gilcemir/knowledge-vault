---
description: Route a learning request to its learning/<topic>/ workspace and hand off to /teach. Use when the user wants to start or resume a learning track, or reports/pastes work for one ("fiz o P6", a solved roadmap problem, a drill result, "próxima lição") — before any review, so the teach protocol's probes are not front-run.
argument-hint: "Topic, or what you want to do in a track (or leave empty to resume)"
---

You are routing a teaching request in this knowledge vault. You don't teach here: the `teach` skill does that, and only the user can invoke it (the Skill tool refuses it). Your job is to find the right workspace and give the user a `/teach` line that carries everything the teaching session needs.

1. **Match the request to a workspace.** `$ARGUMENTS` (and the recent conversation) is usually a request *inside* a track, not a new topic name — e.g. "P6 e P7 resolvidos" belongs to `learning/graphs/`. Before treating anything as a new topic, check the existing `learning/*/` workspaces: their folder names, `MISSION.md`, and the track plan or session log in `NOTES.md` (problem names, lesson numbers). A broader existing workspace that subsumes the request wins over a new near-duplicate.
   - No arguments and nothing in the conversation: list the workspaces, each with its next step (the track plan's first open row, or else the latest session-log entry), and ask which one to resume or whether to start a new one.
   - Clearly a new topic: propose a dash-case slug (e.g. "Rust ownership" → `rust-ownership`) and confirm it before creating `learning/<slug>/` — a wrong slug means a stray workspace.

2. **Don't act on the request.** If the user pasted a solution, drill result, or answers, do not review, grade, or comment on them — not even a verdict. A review done before the teach protocol loads gives away the probes it would have asked, and that evidence can't be recovered. Just acknowledge that the hand-in will be handled inside `/teach`.

3. **Hand off.** Tell the user, in the language their workspace's `NOTES.md` records (Portuguese by default), to type `/teach` themselves, and give a ready-to-paste line that is self-contained — naming the workspace, restating their request, and pointing at any material already in the conversation:

   ```
   /teach workspace learning/<slug>/ — <their request, e.g. "fechar P6+P7 (códigos acima na conversa)" or the next step from NOTES.md>
   ```

   For a brand-new topic, mention that `/teach` will open by interviewing them about why they want to learn it.
