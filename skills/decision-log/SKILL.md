---
name: decision-log
description: >
  Keep a folder of Markdown notes the agent can look up later: decisions and
  why, measured numbers, pitfalls hit, where things are, and a work log per
  session. Use when a decision is made, a number is measured, a pitfall is hit,
  a work session reaches a break or ends, or when the current task may touch
  something recorded before. Works as an Obsidian vault, but Obsidian is not
  required.
license: MIT
---

# Decision log

A notes folder ("vault") the agent writes to and searches. Plain Markdown files, so any agent and any editor can use it. Obsidian is optional: it makes the links clickable for the human.

This needs an agent that can read and write local files and run commands, such as a CLI coding agent.

## Find the vault

The user names the vault in their rules file (`CLAUDE.md`, `AGENTS.md` or similar), for example: `Notes vault: ~/notes (see its README.md)`. If no vault is named, ask the user where it is. Do not create one without asking.

The vault's own `README.md` is the source of truth for that vault. Read it before the first write in a session. Where it differs from this skill, it wins.

## Ground rules

These come from a first version that went wrong: tight management and deadlines pushed the agent into routing around guards, ignoring instructions and stating things that were not true.

- The vault records; it does not manage. Do not create deadlines, priorities or schedules the user did not state, and never write "if there is no answer by X, do Y". A date the user gave is information, not a reason to hurry.
- Write only what you checked. Mark guesses and unchecked points as such. A claim you cannot trace to a command, a file or the user's words does not go in as fact.
- Failed and unfinished are fine to write down. Do not word a note so the work looks done.
- When something goes wrong, write it as a pitfall. Do not add a rule, folder or field each time; change the rules only with the user.
- When a note records a block, a guard or a restriction, do not plan a way around it. Stop and ask the user.
- When unsure, ask the user. Do not decide on your own and record it as settled.

## When to read

Search the vault when the current task may touch something recorded before: a decision, a measured number, a known pitfall, where a file lives. Search by words from the task (file names, tool names, error text). Do not read the whole vault every session.

## When to write

| Folder | Write when |
|---|---|
| `decisions/` | A decision is made: what, and why. |
| `measurements/` | A number is measured. Include the command to reproduce it and the commit or version. |
| `pitfalls/` | A mistake, a trap or a block was hit (a failing check, a refused action). Include how to avoid it, or say it is unsolved. For a block, write only that it is unsolved, never a way around it. |
| `map/` | Where something is: repos, files, folders, services. |
| `worklog/` | A work session reaches a break or ends: what was done, what is left, the next step. |
| `references/` | Notes on outside material worth coming back to. Nothing decided. |

Add a folder only when a note does not fit any existing one. Do not create folders ahead of time.

After writing, tell the user in one line which note was written.

## One note

- Before writing any date or time, get it from the system (for example `date '+%F %H:%M'`). Do not guess; dates go wrong around midnight.
- File name: `YYYY-MM-DD title.md`. The title states the conclusion, not the topic. Keep `# ^ [ ] | : / \` out of titles; they break links or file names.
- Work log: `worklog/<project>/<YYYY-MM-DD>/<HHMM> title.md`. `<project>` is the name of the repository or folder being worked on; if there is none, ask the user. Add a new file each time; never append to an old one. Put decisions and pitfalls in their own folders and link to them from the log.
- Keep what the user told you apart from what you checked yourself, and say which is which. Do not write "checked" or "confirmed" for something you only heard.
- Write the reasons the user gave, in their words where you can. Do not fill in reasons they did not give. If you add your own reading, mark it `(my guess)`.
- If the user made the decision, end the title with `(user)`. Otherwise the reader cannot tell the user's call from the agent's.
- Start with a small header, then the conclusion first, then short supporting points:

```markdown
---
type: decision
date: 2026-10-19
---

# Use SQLite for the cache, not Redis (user)

Conclusion: SQLite. The user's reason: "one file, no server to babysit".

- Not given: why Redis was ruled out beyond that. Left open.
```

- When a decision is withdrawn, append the withdrawal and its reason to the same note. Do not delete it.
- Never write secrets: tokens, passwords, private keys, webhook URLs.

## Links

Link to another note with its full path from the vault root, without `.md`:

```markdown
See [[pitfalls/2026-10-15 the build fails if the cache dir is missing]].
```

Obsidian makes this a clickable link. Without Obsidian, add `.md` to the path inside the brackets and open it from the vault root.

## Old notes

Notes older than 30 days may sit in an `archive/` folder inside their folder (for example `decisions/archive/`), moved there by `scripts/archive_old_notes.py` on a schedule the user sets up. They are not out of date by default. Search them like any other note. An archive folder's `README.md` may list the old notes used most in the last week; check it first when looking for something older. Do not move notes into an archive yourself unless the user asks.

## Version control

If the vault's `README.md` says the vault is in git and asks for commits, commit after each write. Add only the files you wrote. Never push unless the user asks. If the README says nothing, do not commit.
