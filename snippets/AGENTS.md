# Decision log (compact rules)

For agents that read a rules file but not skills. Paste this into your project's `AGENTS.md` (or `CLAUDE.md`), and set the vault path.

Notes vault: `~/notes` (its `README.md` is the source of truth and wins over these rules).

- The vault records, it does not manage: no deadlines, priorities or "if no answer by X, do Y" the user did not state. Write only what you checked; failed and unfinished are fine to write. Do not add rules each time something goes wrong. Do not plan around a block or guard; ask. When unsure, ask.
- Read: when the task may touch something recorded before, search the vault by words from the task. Do not read it all every session.
- Write: `decisions/` (what and why), `measurements/` (number + reproduce command + commit), `pitfalls/` (trap + how to avoid), `map/` (where things are), `worklog/` (done, left, next step), `references/` (outside material, nothing decided). Add folders only when needed.
- File name `YYYY-MM-DD title.md`, title states the conclusion. Work log: `worklog/<project>/<YYYY-MM-DD>/<HHMM> title.md`, a new file each time.
- Get the date from the system before writing it. End the title with `(user)` if the user made the decision.
- Conclusion first, short. Withdrawn decisions: append, do not delete. No secrets.
- Links: `[[folder/file name]]`, full path from the vault root, no `.md`.
- After writing, tell the user in one line. Commit only if the vault README asks; add only your files; never push unless asked.
