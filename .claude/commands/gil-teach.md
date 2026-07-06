---
description: Start or resume a learning roadmap using the teach skill, in learning/<topic>/
argument-hint: "What would you like to learn about? (or leave empty to resume)"
---

You are orchestrating a teaching session in this knowledge vault. Follow these steps:

1. **Resolve the topic.**
   - If the user provided a topic in `$ARGUMENTS`, convert it to a dash-case slug (e.g. "Rust ownership" → `rust-ownership`).
   - If no topic was provided, list the existing workspaces under `learning/` and ask the user which one to resume (or whether to start a new one).

2. **Locate or create the workspace.**
   - All teaching workspaces live under `learning/<topic-slug>/` at the root of this repository — never at the repo root itself, and never inside the hand-curated cheat-sheet folders (e.g. `python/`, `C#/`).
   - Before creating a new workspace, check whether an existing `learning/*/` directory already covers this topic (a broader topic may subsume it). Prefer resuming/extending an existing workspace over creating near-duplicates.
   - Create the directory if it does not exist.

3. **Invoke the teach skill** (Skill tool, skill: `teach`) and follow its instructions with one override: wherever the skill says "the current directory", use `learning/<topic-slug>/` as the teaching workspace instead. All workspace files (`MISSION.md`, `RESOURCES.md`, `NOTES.md`, `reference/`, `lessons/`, `learning-records/`, `assets/`) belong inside that directory.

4. **Ground new workspaces in the mission.** For a brand-new topic, your first job (per the skill) is to interview the user about *why* they want to learn this before producing any lessons.
