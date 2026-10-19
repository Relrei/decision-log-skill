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
| `pitfalls/` | Mistakes, traps and blocks actually hit, and how to avoid them (or that they are unsolved). |
| `map/` | Where things are: repos, files, folders, services. |
| `worklog/` | Per project and date: what was done, what is left, the next step. |
| `references/` | Notes on outside material worth coming back to. Nothing decided. |

Add a folder when a note does not fit. Do not create folders ahead of time.

Notes older than 30 days move into an `archive/` folder inside their folder, if a schedule runs `archive_old_notes.py`. They stay searchable.

## Rules

- Read: search when the task may touch something recorded here. Not every session.
- Write: when a decision is made, a number is measured, a pitfall is hit, or a work session reaches a break or ends (work log). Tell the user in one line.
- Keep what the user said apart from what the agent checked. A block gets "unsolved", never a way around it.
- File name: `YYYY-MM-DD title.md`, without `# ^ [ ] | : / \` in the title. Work log: `worklog/<project>/<YYYY-MM-DD>/<HHMM> title.md`, where `<project>` is the repository or folder worked on; a new file each time.
- Write the user's reasons as given. Do not fill in reasons they did not give; mark your own reading `(my guess)`.
- Conclusion first, short. Titles of the user's own decisions end with `(user)`.
- Links: `[[folder/file name]]`, full path from the vault root, without `.md`.
- Commits: none. (Change to, for example: "This vault is in git. Commit after each write, only the files you wrote, message `notes: ...`. Never push.")
