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

The user names the vault in their rules file (`CLAUDE.md`, `AGENTS.md` or similar), for example: `Notes vault: ~/notes (see its README.md)`. If no vault is named, ask the user where it is rather than creating one.

The vault's own `README.md` describes how this vault is used. Read it before the first write in a session. Where it differs from this skill, follow the README: everything below is a starting point that the user is expected to change.

## Ground rules

These come from a first version that went wrong: tight management and deadlines pushed the agent into routing around guards, ignoring instructions and stating things that were not true. An agent under pressure gets less reliable, so these keep the vault calm.

- The vault records; it does not manage. Deadlines, priorities and plans belong to the user: record the ones they state, and leave the rest to them. Do not write "if there is no answer by X, do Y": silence is not approval. A date the user gave is information, not a reason to hurry. If they ask for a plan, you can suggest one in chat, but it goes into the vault only once they settle it.
- Write what you know and say how you know it: what the user told you, what you checked yourself, and what is your guess. Failed and unfinished are fine to write down as they are.
- When something is blocked (a failing check, a refused action, a guard), record it as unsolved and ask the user how to proceed. Do not work out a way around it on your own.
- When something goes wrong, a pitfall note is usually enough. Change the vault's rules together with the user, not on the spot.
- When unsure, ask.

## When to read

Search the vault when the task may touch something recorded before: a decision, a measured number, a known pitfall, where a file lives. Search by words from the task (file names, tool names, error text). There is no need to read the whole vault every session.

## When to write

| Folder | Write when |
|---|---|
| `decisions/` | A decision is made: what, and why. |
| `measurements/` | A number is measured: the number, how to reproduce it, and the commit or version. |
| `pitfalls/` | A mistake, trap or block was hit: what happened, and how to avoid it or that it is unsolved. |
| `map/` | Where something is: repos, files, folders, services. |
| `worklog/` | A work session reaches a break or ends, or the user asks where things stand: what was done, what is left, the next step. |
| `references/` | Outside material worth coming back to. Nothing decided. |

Add a folder when a note does not fit the ones there. After writing, tell the user in a line which note was written.

## Defaults for one note

Change any of these in the vault's README.

- Get the date and time from the system (for example `date '+%F %H:%M'`) instead of guessing; dates go wrong around midnight.
- File name `YYYY-MM-DD title.md`, with a title that states the conclusion. Characters such as `# ^ [ ] | : / \` break links or file names, so leave them out.
- Work log: `worklog/<project>/<YYYY-MM-DD>/<HHMM> title.md`, a new file each time. `<project>` is the repository or folder being worked on.
- A decision the user made gets `(user)` at the end of its title, so the user's calls stand apart from the agent's.
- Keep the user's reasons in their words. If you add your own reading, mark it `(my guess)`.
- A small header, the conclusion first, then short points:

```markdown
---
type: decision
date: 2026-10-19
---

# Use SQLite for the cache, not Redis (user)

Conclusion: SQLite. The user's reason: "one file, no server to babysit".

- Not given: why Redis was ruled out beyond that.
```

- A withdrawn decision keeps its note; append the withdrawal and why.
- Leave secrets out: tokens, passwords, private keys, webhook URLs.

## Links

Link to another note with its full path from the vault root, without `.md`:

```markdown
See [[pitfalls/2026-10-15 the build fails if the cache dir is missing]].
```

Obsidian makes this a clickable link. Without Obsidian, add `.md` to the path and open it from the vault root.

## Old notes

If the user runs `scripts/archive_old_notes.py` on a schedule, notes older than 30 days sit in an `archive/` folder inside their folder (for example `decisions/archive/`). Old does not mean wrong; search them like any other note. An archive folder's `README.md` may list the old notes used most in the last week. Moving notes is the script's job, not the agent's.

## Version control

Commit only if the vault's README asks for it, and then only the files you wrote. Pushing is up to the user.
