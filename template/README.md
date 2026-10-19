---
type: entry
updated: YYYY-MM-DD
---

# Notes vault

A place the agent writes to and looks things up in. This file is the source of truth for this vault; edit it to fit how you work.

## Folders

| Folder | What goes in |
|---|---|
| `decisions/` | What was decided and why. Withdrawn decisions are appended to, not deleted. |
| `measurements/` | Measured numbers, with the command to reproduce them and the commit or version. |
| `pitfalls/` | Mistakes and traps actually hit, and how to avoid them. |
| `map/` | Where things are: repos, files, folders, services. |
| `worklog/` | Per project and date: what was done, what is left, the next step. |
| `references/` | Notes on outside material worth coming back to. Nothing decided. |

Add a folder when a note does not fit. Do not create folders ahead of time.

## Rules

- Read: search when the task may touch something recorded here. Not every session.
- Write: when a decision is made, a number is measured, or a pitfall is hit. Tell the user in one line.
- File name: `YYYY-MM-DD title.md`. Work log: `worklog/<project>/<YYYY-MM-DD>/<HHMM> title.md`, a new file each time.
- Conclusion first, short. Titles of the user's own decisions end with `(user)`.
- Links: `[[folder/file name]]`, full path from the vault root, without `.md`.
- Commits: none. (Change to, for example: "This vault is in git. Commit after each write, only the files you wrote, message `notes: ...`. Never push.")
