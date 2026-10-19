#!/usr/bin/env python3
"""Move dated notes older than N days into an archive folder next to them.

A note or folder whose name starts with YYYY-MM-DD and is older than the cutoff
moves into `<its folder>/<archive>/`. Wiki links to it ([[path]]) are rewritten
across the vault. Without --apply it only prints the plan.

Optional: --usage-log counts, per archive folder, how often each archived note
appeared in the given logs over the last few days, and writes that to the
archive folder's README.md, so old notes that are still used are easy to find.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

DATE = re.compile(r'^(\d{4}-\d{2}-\d{2})')
LINK = re.compile(r'\[\[([^\]|#]+)')
TEXT = {
    'en': {
        'title': 'Archive',
        'about': 'Notes older than {days} days, moved here by archive_old_notes.py. They are still searchable.',
        'used': 'Used in the last {n} days (counted {today})',
        'note': 'Note', 'times': 'Times',
        'none': 'None.',
    },
    'ja': {
        'title': '古い',
        'about': '{days} 日より古いノート。archive_old_notes.py が移した。検索には今まで通り出てくる。',
        'used': '直近 {n} 日に使われた物({today} に集計)',
        'note': 'ノート', 'times': '回数',
        'none': '無し。',
    },
}


def plan_moves(vault, archive, cutoff):
    moves = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.') and d != archive)
        if root == vault:
            continue
        for name in dirs + sorted(f for f in files if f.endswith('.md')):
            m = DATE.match(name)
            if not m:
                continue
            try:
                day = dt.date.fromisoformat(m.group(1))
            except ValueError:
                continue
            if day < cutoff:
                moves.append((os.path.join(root, name), os.path.join(root, archive, name)))
        dirs[:] = [d for d in dirs if not (DATE.match(d) and (os.path.join(root, d), os.path.join(root, archive, d)) in moves)]
    return moves


def link_key(vault, path):
    rel = os.path.relpath(path, vault).replace(os.sep, '/')
    return rel[:-3] if rel.endswith('.md') else rel


def rewrite_links(vault, moves, apply):
    files, dirs = {}, []
    for src, dst in moves:
        if os.path.isdir(src) or (apply and os.path.isdir(dst)):
            dirs.append((link_key(vault, src) + '/', link_key(vault, dst) + '/'))
        else:
            files[link_key(vault, src)] = link_key(vault, dst)

    def fix(m):
        target = m.group(1)
        key, md = (target[:-3], '.md') if target.endswith('.md') else (target, '')
        key = key.strip()
        if key in files:
            return '[[' + files[key] + md
        for old, new in dirs:
            if key.startswith(old):
                return '[[' + new + key[len(old):] + md
        return m.group(0)

    changed = []
    for root, ds, fs in os.walk(vault):
        ds[:] = [d for d in ds if not d.startswith('.')]
        for f in fs:
            if not f.endswith('.md'):
                continue
            p = os.path.join(root, f)
            with open(p, encoding='utf-8') as fh:
                text = fh.read()
            new = LINK.sub(fix, text)
            if new != text:
                changed.append(p)
                if apply:
                    with open(p, 'w', encoding='utf-8') as fh:
                        fh.write(new)
    return changed


def count_usage(patterns, since, stems):
    """Count log lines since `since` that mention each stem, streaming the logs."""
    counts = dict.fromkeys(stems, 0)
    for pat in patterns:
        for f in glob.glob(os.path.expanduser(pat)):
            if dt.date.fromtimestamp(os.path.getmtime(f)) < since:
                continue
            with open(f, encoding='utf-8', errors='replace') as fh:
                for line in fh:
                    try:
                        obj = json.loads(line)
                    except ValueError:
                        obj = None
                    if isinstance(obj, dict):
                        when = obj.get('time') or obj.get('timestamp')
                        if isinstance(when, str) and when[:10] < since.isoformat():
                            continue
                        line = json.dumps(obj, ensure_ascii=False)
                    for s in stems:
                        if s in line:
                            counts[s] += 1
    return counts


def archive_dirs(vault, archive):
    for root, dirs, _ in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if os.path.basename(root) == archive:
            notes = [os.path.join(r, f[:-3]) for r, _, fs in os.walk(root)
                     for f in fs if f.endswith('.md') and f != 'README.md']
            yield root, notes


def write_indexes(vault, archive, patterns, n_days, days, lang, today):
    t = TEXT[lang]
    found = list(archive_dirs(vault, archive))
    usage = count_usage(patterns, today - dt.timedelta(days=n_days),
                        {os.path.basename(p) for _, notes in found for p in notes})
    written = []
    for root, notes in found:
        counts = sorted(((usage[os.path.basename(p)], link_key(vault, p)) for p in notes
                         if usage[os.path.basename(p)]), key=lambda c: (-c[0], c[1]))
        body = [f'# {t["title"]}', '', t['about'].format(days=days), '',
                f'## {t["used"].format(n=n_days, today=today)}', '']
        if counts:
            body += [f'| {t["note"]} | {t["times"]} |', '|---|---|']
            body += [f'| [[{k}]] | {n} |' for n, k in counts]
        else:
            body.append(t['none'])
        p = os.path.join(root, 'README.md')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(body) + '\n')
        written.append(p)
    return written


def commit(vault, paths, message):
    top = subprocess.run(['git', '-C', vault, 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True)
    if top.returncode:
        sys.exit('commit: the vault is not in a git repository')
    git = ['git', '-C', top.stdout.strip()]
    if subprocess.run(git + ['diff', '--cached', '--quiet']).returncode:
        sys.exit('commit: other changes are already staged; left the moves uncommitted')
    subprocess.run(git + ['add', '-A', '--'] + paths, check=True)
    if subprocess.run(git + ['diff', '--cached', '--quiet']).returncode:
        subprocess.run(git + ['commit', '-q', '-m', message], check=True)
        print('committed')


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('vault')
    ap.add_argument('--days', type=int, default=30, help='age in days before a note moves (default 30)')
    ap.add_argument('--archive-name', default='archive', help='folder name for old notes (default archive)')
    ap.add_argument('--apply', action='store_true', help='move files; without it, only print the plan')
    ap.add_argument('--usage-log', action='append', default=[], help='glob of log files to count uses in (repeatable)')
    ap.add_argument('--usage-days', type=int, default=7, help='days of logs to count (default 7)')
    ap.add_argument('--lang', choices=sorted(TEXT), default='en', help='language of the archive README')
    ap.add_argument('--commit', metavar='MESSAGE', help='with --apply: commit the changed files with this message')
    a = ap.parse_args()

    vault = os.path.abspath(os.path.expanduser(a.vault))
    today = dt.date.today()
    moves = plan_moves(vault, a.archive_name, today - dt.timedelta(days=a.days))
    ok = []
    for src, dst in moves:
        if os.path.exists(dst):
            print(f'skip (already there): {os.path.relpath(dst, vault)}')
        else:
            ok.append((src, dst))
            print(f'move: {os.path.relpath(src, vault)} -> {os.path.relpath(dst, vault)}')
    if a.apply:
        for src, dst in ok:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.rename(src, dst)
    changed = rewrite_links(vault, ok, a.apply)
    for p in changed:
        print(f'links: {os.path.relpath(p, vault)}')

    indexes = []
    if a.usage_log and a.apply:
        indexes = write_indexes(vault, a.archive_name, a.usage_log, a.usage_days, a.days, a.lang, today)
        for p in indexes:
            print(f'index: {os.path.relpath(p, vault)}')

    if not a.apply:
        print('(dry run: nothing changed; add --apply to do it)')
    elif a.commit:
        paths = [p for pair in ok for p in pair] + changed + indexes
        if paths:
            commit(vault, paths, a.commit)


if __name__ == '__main__':
    main()
