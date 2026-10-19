# Decision log (compact rules)

For agents that read a rules file but not skills. Paste this into your project's `AGENTS.md` (or `CLAUDE.md`), and set the vault path.

Notes vault: `~/notes` (its `README.md` wins over these rules; change them there).

- The vault records; it does not manage. Deadlines, priorities and plans are the user's: record the ones they state. Do not write "if there is no answer by X, do Y": silence is not approval. A plan can be suggested in chat; it goes into the vault once the user settles it, even when they ask you to write it down.
- Say how you know: what the user told you, what you checked, what is your guess (mark it `(my guess)`). Write the user's reasons as given. Failed and unfinished are fine to write down.
- A block (failing check, refused action, guard) is recorded as unsolved; ask the user how to go on. Do not work out a way around it on your own. When unsure, ask.
- Read: when the task may touch something recorded before, search the vault by words from the task. At the start of a session, read the newest work log of the current project.
- Write: `decisions/` (what and why), `measurements/` (number, reproduce command, commit), `pitfalls/` (mistake, trap or block, and how to avoid it or that it is unsolved), `map/` (where things are), `worklog/` (done, left, next step; also when the user says "note this and stop"), `references/` (outside material), `projects/` (optional overview per project, not a task list). Add folders when needed.
- File name `YYYY-MM-DD title.md`, the title states the conclusion, without `# ^ [ ] | : / \`. Work log: `worklog/<project>/<YYYY-MM-DD>/<HHMM> title.md` (`<project>` = the repo or folder worked on), a new file each time.
- Get the date from the system. A decision the user made gets `(user)` at the end of its title. Withdrawn decisions: append, do not delete. No secrets.
- Links: `[[folder/file name]]`, full path from the vault root, without `.md`.
- After writing, tell the user in one line. Commit only if the vault README asks, and only your files. Pushing is up to the user.
