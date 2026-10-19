# decision-log-skill

A skill that gives your AI agent a notes folder it writes to and looks things up in: decisions and why, measured numbers, pitfalls it hit, where things are, and a log of each work session.

The notes are plain Markdown files, so any agent and any editor can use them. Opening the folder in [Obsidian](https://obsidian.md) is recommended, since links become clickable and you get backlinks and search, but nothing depends on it.

## Why

Agents forget between sessions. Rules files say how to work; they are a poor place for "we tried X on the 15th and it was 30% slower". This skill keeps that kind of record in small, dated, searchable notes, and has the agent look it up only when the task touches it.

## What's in here

| Path | What it is |
|---|---|
| `skills/decision-log/SKILL.md` | The skill: when to read, when to write, what one note looks like. |
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

## Using it with Obsidian

Open the vault folder as a vault in Obsidian. Notes link to each other as `[[folder/file name]]`, with the full path from the vault root, so Obsidian resolves them exactly and the agent can follow them as file paths without Obsidian.

## License

[MIT](LICENSE)
