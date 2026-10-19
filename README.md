# decision-log-skill

A skill that gives your AI agent a notes folder it writes to and looks things up in: decisions and why, measured numbers, pitfalls it hit, where things are, and a log of each work session.

It is made for CLI coding agents such as Claude Code and OpenCode: the agent reads and writes the notes as local files and runs a few commands (`date`, `grep`, optionally `git`). Chat apps without file access get little out of it.

The notes are plain Markdown files, so any such agent and any editor can use them. Opening the folder in [Obsidian](https://obsidian.md) is recommended, since links become clickable and you get backlinks and search, but nothing depends on it.

## Why

This comes out of one person's daily use of Claude Code. Two things pushed it.

**Context that loads every session is paid for on every turn.** From 2026-10-14 to 2026-10-19, across 9,244 responses in the author's session logs, 98.4% of tokens were context read back from the cache, 1.2% was new context, and 0.4% was output. Rules files and auto-loaded memory sit in that context. Every fact added to them is read again on every turn, whether the task needs it or not.

**Notes the agent is told not to read do not get used.** Before this, failure write-ups went to a folder the agent was told not to read by default, so what went in there was not used again.

So the notes sit in between: outside the context that loads every session, and read only when the agent goes looking because the task touches something recorded before.

## In use

- First version: 2026-08-25. It grew to 1,243 notes in seven weeks.
- Rebuilt on 2026-10-14 as a smaller vault. Old notes were moved over only after checking they were still true; for example, 6 of 9 pitfalls were moved.
- After six days of the rebuilt vault (2026-10-14 to 10-19): 271 notes. That is 100 work logs, 57 measurements, 49 pitfalls, 42 decisions (19 of them the user's own call, marked `(user)`), 9 references, 8 map notes and 6 in two other folders, plus 215 commits.
- The author's tool logs show the agent read, searched or wrote the vault in 44 of 59 sessions over those six days.

## What went wrong in the first version

The first vault was used for seven weeks, but parts of its design did not hold up. Counted from its files:

- **A status field nobody kept up.** Every note was meant to carry `status: valid | superseded | withdrawn`. By the end there were 107 different status values, many of them free-text remarks, and only 1 of 1,243 notes was ever marked superseded. In the same period, a number measured on 08-12 had been replaced by a newer measurement but was still quoted in a published document until it was caught. The rebuilt vault drops the field: the title states the conclusion, and a withdrawn decision gets the withdrawal appended to the note itself.
- **Structure that kept growing.** It grew to 12 folders, 14 note types, an index tool with a dozen subcommands, and a 6 KB rulebook as its README; the last folder was added the day before the rebuild. In seven weeks it collected 575 measurements and 377 pitfalls. The rebuilt vault starts small and adds a folder only when a note does not fit.
- **Old notes are not carried over blindly.** When rebuilding, nothing was copied over as is. Each note was checked against the current state first, and only the ones that still held were rewritten into the new vault (6 of 9 shared pitfalls).

These are counts from one setup, not a benchmark, and they do not show that the notes made the work better or cheaper. The rules in the skill come from that setup. For example, "get the date from the system before writing it" is there because dates went wrong around midnight. So far it has been used with Claude Code. OpenCode is being tested.

## What's in here

| Path | What it is |
|---|---|
| `skills/decision-log/SKILL.md` | The skill: when to read, when to write, what one note looks like. |
| `skills/decision-log/scripts/archive_old_notes.py` | Optional: moves notes older than 30 days into `archive/` folders and fixes links to them. |
| `snippets/AGENTS.md` | A compact version for agents that read a rules file but not skills. |
| `template/` | An empty vault: a `README.md` with the vault's own rules, and the folders. |

## Install

1. Copy `template/` to where you want your notes, for example `~/notes`.
2. Install the skill:
   - **Claude Code:** copy `skills/decision-log/` to `~/.claude/skills/decision-log/`.
   - **OpenCode:** the same folder works (OpenCode also reads `~/.claude/skills/`), or use `~/.config/opencode/skills/decision-log/`.
   - **Other agents with skill support:** put `skills/decision-log/` wherever the agent looks for skills.
   - **Agents without skills:** paste `snippets/AGENTS.md` into your project's rules file instead.
3. Tell the agent where the vault is, in your rules file (`CLAUDE.md`, `AGENTS.md`, ...):

   ```markdown
   Notes vault: ~/notes (see its README.md)
   ```

4. Edit `~/notes/README.md` to fit how you work. It wins over the skill where they differ. For example, it decides whether the agent commits notes to git.

## Moving old notes (optional)

`archive_old_notes.py` (Python 3, standard library only) moves every note or dated folder whose name starts with a date older than 30 days into an `archive/` folder next to it, for example `decisions/archive/` or `worklog/<project>/archive/`, and rewrites `[[...]]` links to match. Without `--apply` it only prints what it would do.

```bash
python3 skills/decision-log/scripts/archive_old_notes.py ~/notes            # show the plan
python3 skills/decision-log/scripts/archive_old_notes.py ~/notes --apply    # do it
```

Options: `--days` (default 30), `--archive-name`, `--commit "message"` (commits only the files it changed, and refuses if something else is already staged), and `--usage-log '<glob>'`. With `--usage-log`, it counts how often each archived note appears in those logs over the last 7 days (`--usage-days`) and writes the list to each archive folder's `README.md`, so old notes that are still in use are easy to find. For Claude Code, the session logs work: `--usage-log '~/.claude/projects/*/*.jsonl'`.

Run it weekly with cron or a systemd user timer. The agent itself does not need to do anything.

## Using it with Obsidian

Open the vault folder as a vault in Obsidian. Notes link to each other as `[[folder/file name]]`, with the full path from the vault root, so Obsidian resolves them exactly and the agent can follow them as file paths without Obsidian.

## Make it yours

The folders and rules here fit one person's work. Start with them, and change them as you use it until they fit yours.

## License

[MIT](LICENSE)
