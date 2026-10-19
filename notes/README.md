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
| `projects/` | Optional. One folder per project with an `overview.md`: what it is, where it lives, where it stands. Not a task list. Move it, rename it or delete it as you like. |
| `references/` | Notes on outside material worth coming back to. Nothing decided. |

Add a folder when a note does not fit. Do not create folders ahead of time.

Notes older than 30 days move into an `archive/` folder inside their folder, if a schedule runs `archive_old_notes.py`. They stay searchable.

## Rules

- The vault records; it does not manage. Deadlines and plans are the user's: record the ones they state. A plan the agent made up is shown in chat first and written once the user confirms it. Silence is not approval.
- Read: search when the task may touch something recorded here. At the start of a session, read the newest work log of the current project.
- Write: when a decision is made, a number is measured, a pitfall is hit, or a work session reaches a break or ends (work log; also when the user says "note this and stop"). Tell the user in one line.
- Say how you know: what the user said, what you checked, what is your guess `(my guess)`. Write the user's reasons as given.
- A block (failing check, refused action, guard) is recorded as unsolved; ask the user how to go on.
- File name: `YYYY-MM-DD title.md`, the title states the conclusion, without `# ^ [ ] | : / \`. Work log: `worklog/<project>/<YYYY-MM-DD>/<HHMM> title.md`, where `<project>` is the repository or folder worked on; a new file each time.
- Titles of the user's own decisions end with `(user)`.
- Links: `[[folder/file name]]`, full path from the vault root, without `.md`.
- Commits: none. (Change to, for example: "This vault is in git. Commit after each write, only the files you wrote, message `notes: ...`. Never push.")
