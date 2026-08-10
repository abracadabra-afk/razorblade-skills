#!/usr/bin/env python3
"""link_audit.py - Obsidian vault reference-integrity auditor (read-only).

Scans notes for [[wikilinks]], ![[embeds]], and [md](links), resolves each against
the real file index using Obsidian's rules (basename match with FOLDER-PROXIMITY
tie-break, or path match), plus heading/block-anchor indices. Reports:
  DANGLING        - target file not found anywhere
  BROKEN-ANCHOR   - file resolves, but ^block-id missing
  BROKEN-HEADING  - file resolves, but #heading missing
  AMBIGUOUS(info) - basename matches >1 file and none in the same folder (Obsidian
                    still resolves to the shortest path; informational, low priority)
  SUSPECT-STALE   - a target file read back TRUNCATED (NUL bytes / partial), so its
                    anchor/heading set can't be trusted; the audit refuses to emit a
                    confident BROKEN-ANCHOR/HEADING off a poisoned read. (^obs-073)
  INTEGRITY       - a scanned note's OWN bytes carry NUL / control / trailing-pad bytes
                    (the ^obs-089/103/129/133 trailing-NUL corruption class). SUSPECT
                    under the disk mount (may be a stale partial -> verify via the file
                    tools, then strip-or-restore). Checked for every .md, incl. the
                    link-quarantined logs (_CHANGELOG / _OBSERVATIONS), since those are
                    exactly what corrupts.

OBS-014 / OBS-073 GUARD: the local bash/Dropbox mount can serve STALE or TRUNCATED
copies of recently-written/moved files (a file-tools write does not heal the bash
view mid-session). Truncated reads are detected (NUL bytes) and downgraded to
SUSPECT-STALE advisories instead of false BROKEN-* findings, and the run prints a
top-level "MOUNT MAY BE STALE" banner so you re-run in a fresh session. Confirm any
surprising DANGLING via the file tools before acting. (The former --rest-base/--rest-key
live-view path was REMOVED 2026-08-10 under DIR-001 - the backing plugin was removed
from the vault 2026-07-13; do not go looking for its key.)

SELF-CHECK (added 2026-08-10, ^backlog-linkaudit-unpack-bug): the run REFUSES to report
if it scanned 0 (or <50%) of the vault's markdown files - the 2026-08-09 scheduled run
printed "0 md scanned ... severity: clean" off a call-site arity bug (^obs-245), and a
clean verdict from an empty scan is worse than a crash.
"""
import argparse, os, re, json, sys, urllib.parse
from collections import Counter

MD = '.md'
WIKILINK = re.compile(r'(!?)\[\[([^\]\n]+?)\]\]')
MDLINK   = re.compile(r'(!?)\[[^\]\n]*?\]\(([^)\n]+?)\)')
HEADING  = re.compile(r'^#{1,6}\s+(.*?)\s*$', re.M)
BLOCKID  = re.compile(r'(?:^|\s)\^([A-Za-z0-9_-]+)\s*$', re.M)
SKIPDIRS = {'.git', '.obsidian', '.smart-env', '.trash'}
QZONES   = ('/GRAVEYARD/', '/evals/', '/SYSTEM/history/')  # history added 2026-08-10 (^backlog-linkaudit-unpack-bug (c)): carved archives hold refs to moved content by design
QFILES   = ('_CHANGELOG.md', '_OBSERVATIONS.md', 'vault-migration-plan.md')

def quarantined(rel):
    if any(z in '/' + rel for z in QZONES): return True
    b = os.path.basename(rel)
    return b in QFILES or b.startswith('_pre-migration') or b.endswith('.bak.md')

def strip_code(txt):
    txt = re.sub(r'```.*?```', '', txt, flags=re.S)
    txt = re.sub(r'~~~.*?~~~', '', txt, flags=re.S)
    txt = re.sub(r'`[^`\n]*`', '', txt)
    return txt

def norm_head(h):
    h = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', h)
    return re.sub(r'[*_`~]', '', h).strip().lower()

def looks_truncated(raw_bytes, text):
    # NUL bytes are the documented signature of a half-written / mount-truncated read
    # (^obs-018/^obs-027). errors='replace' would otherwise hide them as U+FFFD.
    return b'\x00' in raw_bytes or '\x00' in text or '�' in text

def integrity_metrics(raw):
    # ^obs-089/103/129/133: NUL / control / trailing-pad bytes are the documented
    # Dropbox-sync / atomic-write corruption signature. tab/lf/cr are legitimate.
    nul = raw.count(b'\x00')
    ctrl = sum(1 for b in raw if b < 32 and b not in (9, 10, 13))
    trail_nul = len(raw) - len(raw.rstrip(b'\x00'))
    if nul or ctrl or trail_nul:
        return {'nul': nul, 'ctrl': ctrl, 'trail_nul': trail_nul, 'bytes': len(raw)}
    return None

def read_disk(path):
    with open(path, 'rb') as fh:
        raw = fh.read()
    text = raw.decode('utf-8', errors='replace')
    return text, looks_truncated(raw, text), integrity_metrics(raw)

# NOTE (2026-08-10, ^backlog-linkaudit-dead-rest-flags): the --rest-base/--rest-key
# path was REMOVED. The Obsidian Local REST API plugin was removed from the vault
# 2026-07-13 under DIR-001 (its data.json held an apiKey + TLS private key); the
# flags had no live backend and invited a future reader to go looking for that key.

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vault', required=True)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--all', action='store_true', help='include GRAVEYARD/evals/history')
    ap.add_argument('--ambiguous', action='store_true', help='show AMBIGUOUS info findings')
    a = ap.parse_args()
    vault = os.path.abspath(a.vault)
    read_failures = []

    files = []
    for root, dirs, fs in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIPDIRS]
        for f in fs:
            files.append(os.path.relpath(os.path.join(root, f), vault).replace('\\', '/'))

    by_rel, by_base, by_base_ext = {}, {}, {}
    for rel in files:
        rl = rel.lower(); by_rel[rl] = rel
        if rl.endswith(MD): by_rel[rl[:-3]] = rel
        base = os.path.basename(rel); stem, ext = os.path.splitext(base)
        by_base.setdefault(stem.lower(), []).append(rel)
        by_base_ext.setdefault(base.lower(), []).append(rel)

    headings, blocks, content, suspect = {}, {}, {}, set()
    integrity_findings = []
    for rel in files:
        if not rel.lower().endswith(MD): continue
        # read_disk returns a 3-tuple (text, truncated, integrity) — the 2026-08-09
        # scheduled run proved a 2-var unpack here raises ValueError on EVERY file,
        # silently skipping the whole vault and printing "0 md scanned ... clean"
        # (^obs-245 / ^backlog-linkaudit-unpack-bug). Keep the arity in sync with
        # read_disk, and never blanket-continue: count what could not be read.
        try:
            txt, sus, integ = read_disk(os.path.join(vault, rel))
        except Exception as e:
            read_failures.append((rel, repr(e)))
            continue
        content[rel] = txt
        if sus: suspect.add(rel)
        if integ:
            integrity_findings.append(('INTEGRITY', rel, '',
                'own bytes suspect: %d NUL, %d control, %d trailing-pad (of %d)' %
                (integ['nul'], integ['ctrl'], integ['trail_nul'], integ['bytes'])))
        headings[rel] = {norm_head(h) for h in HEADING.findall(txt)}
        blocks[rel] = set(BLOCKID.findall(txt))

    # Signature self-check (DIR-013: verify by signature, not absence of error;
    # DIR-018: a pass-condition must name its blind spot). A run that scanned
    # nothing or almost nothing must REFUSE to report — "clean" off an empty
    # scan is the confident-negative failure that shipped 2026-08-09.
    md_total = sum(1 for r in files if r.lower().endswith(MD))
    if md_total and (len(content) == 0 or len(content) < md_total * 0.5):
        sys.stderr.write(
            "FATAL: scanned %d of %d markdown files - refusing to report.\n"
            "A scan this incomplete cannot support any verdict, least of all 'clean'.\n"
            "First read failures (of %d):\n%s\n" % (
                len(content), md_total, len(read_failures),
                '\n'.join('  %s: %s' % rf for rf in read_failures[:10])))
        sys.exit(2)

    findings = list(integrity_findings)
    def resolve(target, ext_hint, src):
        t = target.strip()
        if not t: return ('self', src)
        tl = t.lower()
        if '/' in t:
            for c in (tl, tl + MD):
                if c in by_rel: return ('ok', by_rel[c])
            return ('dangling', None)
        stem, ext = os.path.splitext(t)
        hits = by_base_ext.get(tl, []) if ext else by_base.get(tl, [])
        if len(hits) == 1: return ('ok', hits[0])
        if len(hits) > 1:
            sdir = os.path.dirname(src)
            same = [h for h in hits if os.path.dirname(h) == sdir]
            if len(same) == 1: return ('ok', same[0])          # Obsidian: same-folder wins
            pick = sorted(hits, key=lambda h: (h.count('/'), len(h)))[0]  # else shortest path
            return ('ambiguous', pick)
        return ('dangling', None)

    def check(src, embed, inner):
        part = inner.split('|', 1)[0]
        tgt, frag = part.split('#', 1) if '#' in part else (part, None)
        status, rel = resolve(tgt, embed, src)
        if status == 'dangling' and "''" in tgt:
            # ^obs-064: a wikilink inside a YAML single-quoted frontmatter scalar escapes an
            # apostrophe by doubling it ('[[Pig''s Box]]'); Obsidian unescapes before resolving.
            status, rel = resolve(tgt.replace("''", "'"), embed, src)
        kind = 'embed' if embed else 'link'
        if status == 'dangling':
            findings.append(('DANGLING', src, inner.strip(), 'target not found')); return
        if status == 'ambiguous':
            findings.append(('AMBIGUOUS', src, inner.strip(), 'basename matches multiple; resolves to ' + rel))
        target_rel = rel
        if frag and target_rel and target_rel.lower().endswith(MD) and target_rel in content:
            f = frag.strip()
            if target_rel in suspect:
                # ^obs-073: the target read back truncated; its anchor/heading set is not
                # trustworthy. Refuse to emit a confident BROKEN-* off a poisoned read.
                findings.append(('SUSPECT-STALE', src, inner.strip(),
                                 'target %s read truncated; #%s unverifiable - re-run fresh/with --rest-base' % (target_rel, f)))
                return
            if f.startswith('^'):
                if f[1:] not in blocks.get(target_rel, set()):
                    findings.append(('BROKEN-ANCHOR', src, inner.strip(), 'no ^%s in %s' % (f[1:], target_rel)))
            elif norm_head(f) not in headings.get(target_rel, set()):
                findings.append(('BROKEN-HEADING', src, inner.strip(), 'no heading "%s" in %s' % (f, target_rel)))

    for rel in files:
        if rel not in content: continue
        scan = strip_code(content[rel])
        for m in WIKILINK.finditer(scan): check(rel, m.group(1) == '!', m.group(2))
        for m in MDLINK.finditer(scan):
            href = m.group(2).strip()
            if href.startswith('<') and href.endswith('>'): href = href[1:-1]
            href = href.split(' ')[0]
            if re.match(r'^[a-z]+://', href) or href.startswith(('mailto:', '#', 'data:', 'tel:')): continue
            href = urllib.parse.unquote(href).split('#', 1)[0]
            if not href: continue
            cr = os.path.normpath(os.path.join(os.path.dirname(rel), href)).replace('\\', '/').lower()
            ok = any(c in by_rel for c in (href.lower(), href.lower()+MD, cr, cr+MD))
            if not ok:
                b = os.path.basename(href).lower()
                ok = b in by_base_ext or os.path.splitext(b)[0] in by_base
            if not ok: findings.append(('DANGLING', rel, href, 'md-link target not found'))

    show = [f for f in findings if not quarantined(f[1])]
    quar = [f for f in findings if quarantined(f[1])]
    if not a.ambiguous:
        show = [f for f in show if f[0] != 'AMBIGUOUS']
    stale_banner = None
    if suspect:
        stale_banner = ("MOUNT MAY BE STALE: %d target(s) read back truncated (NUL bytes). "
                        "Findings off them are downgraded to SUSPECT-STALE. Re-run in a fresh "
                        "session and confirm surprising findings via the file tools." % len(suspect))
    if a.json:
        print(json.dumps({'shown': show, 'quarantined_count': len(quar),
                          'suspect_count': len(suspect), 'suspect_files': sorted(suspect),
                          'md_scanned': len(content), 'md_total': md_total,
                          'read_failures': read_failures,
                          'stale_banner': stale_banner}, indent=2)); return
    if stale_banner: print("[!] " + stale_banner)
    if read_failures:
        print("[!] %d file(s) could not be read (excluded from scan, NOT evidence of absence):" % len(read_failures))
        for rf in read_failures[:10]: print("      %s: %s" % rf)
    print("LINK AUDIT  vault=%s\n%d md scanned (of %d files) | %d findings shown, %d quarantined, %d ambiguous-suppressed"
          % (vault, len(content), len(files), len(show),
             len([f for f in findings if quarantined(f[1])]),
             len([f for f in findings if f[0]=='AMBIGUOUS' and not quarantined(f[1])]) if not a.ambiguous else 0))
    print("severity:", dict(Counter(f[0] for f in show)) or "clean")
    for sev, src, raw, detail in sorted(show):
        print("  [%s] %s\n       %s  ->  %s" % (sev, src, raw[:80], detail[:120]))
    if a.all and quar:
        print("\n-- quarantined (%d) --" % len(quar))
        for sev, src, raw, detail in sorted(quar):
            print("  [%s] %s  %s" % (sev, src, raw[:60]))

if __name__ == '__main__': main()
