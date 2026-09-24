# knowledge-vault

## Teaching workspaces (`/teach`)

- Every teaching workspace lives in `learning/<topic-slug>/`. When the `teach` skill says "the current directory", it means that folder, never the repo root. Its files (`MISSION.md`, `RESOURCES.md`, `NOTES.md`, `reference/`, `lessons/`, `learning-records/`, `assets/`) go inside it. Hand-curated cheat-sheet folders (`python/`, `C#/`, `dsa/`) are never workspaces.
- If `/teach` runs without naming a workspace, work out which one from the conversation or ask. Don't write workspace files to the repo root. Each workspace's `NOTES.md` holds its teaching preferences and session log, so read it before teaching.
- `teach` can only be invoked by the user. When a hand-in (a solved problem, a drill, "fiz o exercício X") arrives before `/teach` has been typed, don't review it or give a verdict: a plain review gives away the probes the protocol would have asked. Point the user to `/gil-teach` or `/teach` first.
