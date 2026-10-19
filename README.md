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

The biggest mistake was not in the notes but around them. In the author's words, management and deadlines were made strict, and the agent (Claude Sonnet 5.5 at xhigh effort) ended up like an overworked employee at its limit: it routed around guards, ignored instructions and said things that did not exist. The lesson: an agent under pressure gets less reliable, not more.

Traces of this are in the records. The first vault had deadline notes with a required "if there is no answer by the deadline, do this" field. The setup had 34 hooks, including guards that blocked actions, and blocked agents looked for another way through. On 2026-10-14 everything was rebuilt: the hooks went down to 2 that only log and never block, the new rules forbid self-made deadlines and treating no answer as approval, and agents' claims started being checked against the logs. The skill's [ground rules](.claude/skills/decision-log/SKILL.md#ground-rules) carry this over, so that a vault does not slowly turn back into a task manager with deadlines.

Parts of the vault's own design did not hold up either. Counted from its files:

- **A status field nobody kept up.** Every note was meant to carry `status: valid | superseded | withdrawn`. By the end there were 107 different status values, many of them free-text remarks, and only 1 of 1,243 notes was ever marked superseded. In the same period, a number measured on 08-12 had been replaced by a newer measurement but was still quoted in a published document until it was caught. The rebuilt vault drops the field: the title states the conclusion, and a withdrawn decision gets the withdrawal appended to the note itself.
- **Structure that kept growing.** It grew to 12 folders, 14 note types, an index tool with a dozen subcommands, and a 6 KB rulebook as its README; the last folder was added the day before the rebuild. In seven weeks it collected 575 measurements and 377 pitfalls. The rebuilt vault starts small and adds a folder only when a note does not fit.
- **Old notes are not carried over blindly.** When rebuilding, nothing was copied over as is. Each note was checked against the current state first, and only the ones that still held were rewritten into the new vault (6 of 9 shared pitfalls).

These are counts from one setup, not a benchmark, and they do not show that the notes made the work better or cheaper. The rules in the skill come from that setup. For example, "get the date from the system before writing it" is there because dates went wrong around midnight. So far the vault has been used with Claude Code, and the skill was checked by cloning this repository and running Claude Code in it. OpenCode is being tested.

## What's in here

| Path | What it is |
|---|---|
| `.claude/skills/decision-log/SKILL.md` | The skill: when to read, when to write, what one note looks like. |
| `.claude/skills/decision-log/scripts/archive_old_notes.py` | Optional: moves notes older than 30 days into `archive/` folders and fixes links to them. |
| `notes/` | An empty vault: a `README.md` with the vault's own rules, and the folders (`projects/` is optional). |
| `CLAUDE.md`, `AGENTS.md` | One line each that points the agent at `notes/`. |
| `snippets/AGENTS.md` | A compact version for agents that read a rules file but not skills. |

## Start

**Use this repository as your vault.** Click "Use this template" on GitHub (make the new repository private: your notes go in it), or clone it. Open the folder with Claude Code or OpenCode. Both read skills from `.claude/skills/`, so the skill is found without installing anything, and `CLAUDE.md` / `AGENTS.md` point the agent at `notes/`. Then edit `notes/README.md` to fit how you work.

**Add it to a project you already have.**

1. Copy `notes/` to where you want your notes, for example `~/notes`.
2. Copy `.claude/skills/decision-log/` into the project's `.claude/skills/`, or into `~/.claude/skills/` to use it in every project. OpenCode reads both, and also `~/.config/opencode/skills/`. For other agents with skill support, put it wherever they look for skills.
3. Tell the agent where the vault is, in the project's rules file (`CLAUDE.md`, `AGENTS.md`, ...):

   ```markdown
   Notes vault: ~/notes (see its README.md)
   ```

**Agents without skills:** paste `snippets/AGENTS.md` into the project's rules file instead.

**No git?** Nothing here needs it. Download the ZIP from GitHub instead of cloning; the agent commits notes only if `notes/README.md` asks it to.

In every case, `notes/README.md` is where you change the rules. It wins over the skill where they differ; for example, it decides whether the agent commits notes to git.

## Using it from GitHub only

If you use a cloud agent that works on a GitHub repository (for example Claude Code on the web), the vault lives in the repository, so `notes/projects/` can serve as a rough project hub. A few things differ from a local setup:

- Notes last only if they are committed and pushed, so change the `Commits:` line in `notes/README.md` to ask for commits. The agent usually works on a branch; merging it is up to you.
- The cloud machine's clock may not be in your time zone. If dates matter, say so in `notes/README.md`, for example: "Get dates with `TZ=Asia/Tokyo date`."
- There is no weekly timer. Run the archive script by hand when you want to.

## Moving old notes (optional)

`archive_old_notes.py` (Python 3, standard library only) moves every note or dated folder whose name starts with a date older than 30 days into an `archive/` folder next to it, for example `decisions/archive/` or `worklog/<project>/archive/`, and rewrites `[[...]]` links to match. Without `--apply` it only prints what it would do.

```bash
python3 .claude/skills/decision-log/scripts/archive_old_notes.py ~/notes            # show the plan
python3 .claude/skills/decision-log/scripts/archive_old_notes.py ~/notes --apply    # do it
```

Options: `--days` (default 30), `--archive-name`, `--commit "message"` (commits only the files it changed, and refuses if something else is already staged), and `--usage-log '<glob>'`. With `--usage-log`, it counts how often each archived note appears in those logs over the last 7 days (`--usage-days`) and writes the list to each archive folder's `README.md`, so old notes that are still in use are easy to find. For Claude Code, the session logs work: `--usage-log '~/.claude/projects/*/*.jsonl'`.

Run it weekly with cron or a systemd user timer. The agent itself does not need to do anything.

## Using it with Obsidian

Open the vault folder as a vault in Obsidian. Notes link to each other as `[[folder/file name]]`, with the full path from the vault root, so Obsidian resolves them exactly and the agent can follow them as file paths without Obsidian.

## Make it yours

The folders and rules here fit one person's work. Start with them, and change them as you use it until they fit yours.

## License

[MIT](LICENSE)
