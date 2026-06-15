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

OBS-014 / OBS-073 GUARD: the local bash/Dropbox mount can serve STALE or TRUNCATED
copies of recently-written/moved files (a file-tools write does not heal the bash
view mid-session). Mitigations, in order of strength:
  1. Pass --rest-base http://127.0.0.1:27123 --rest-key <Local REST API key> to read
     every target from Obsidian's LIVE in-memory view (immune to the mount). Falls
     back to disk per-file on any API error. (env: OBSIDIAN_REST_BASE/OBSIDIAN_API_KEY)
  2. Without the API, truncated reads are detected (NUL bytes) and downgraded to
     SUSPECT-STALE advisories instead of false BROKEN-* findings, and the run prints a
     top-level "MOUNT MAY BE STALE" banner so you re-run in a fresh session.
Either way, confirm any surprising DANGLING via the file tools before acting.
"""
import argparse, os, re, json, urllib.parse, urllib.request
from collections import Counter

MD = '.md'
WIKILINK = re.compile(r'(!?)\[\[([^\]\n]+?)\]\]')
MDLINK   = re.compile(r'(!?)\[[^\]\n]*?\]\(([^)\n]+?)\)')
HEADING  = re.compile(r'^#{1,6}\s+(.*?)\s*$', re.M)
BLOCKID  = re.compile(r'(?:^|\s)\^([A-Za-z0-9_-]+)\s*$', re.M)
SKIPDIRS = {'.git', '.obsidian', '.smart-env', '.trash'}
QZONES   = ('/GRAVEYARD/', '/evals/')
QFILES   = ('_CHANGELOG.md', '_OBSERVATIONS.md', 'vault-migration-plan.md')

def quarantined(rel):
    if any(z in '/' + rel for z in QZONES): return True
    b = os.path.basename(rel)
    return b in QFILES or b.startswith('_pre-migration')

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

def read_disk(path):
    with open(path, 'rb') as fh:
        raw = fh.read()
    text = raw.decode('utf-8', errors='replace')
    return text, looks_truncated(raw, text)

def read_rest(base, key, rel):
    url = base.rstrip('/') + '/vault/' + urllib.parse.quote(rel)
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + key,
                                               'Accept': 'text/markdown'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()
    text = raw.decode('utf-8', errors='replace')
    # the live API view is authoritative; only a real NUL would be suspect (shouldn't happen)
    return text, ('\x00' in text)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vault', required=True)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--all', action='store_true', help='include GRAVEYARD/evals/history')
    ap.add_argument('--ambiguous', action='store_true', help='show AMBIGUOUS info findings')
    ap.add_argument('--rest-base', default=os.environ.get('OBSIDIAN_REST_BASE'),
                    help='Obsidian Local REST API base (live view; bypasses the stale mount)')
    ap.add_argument('--rest-key', default=os.environ.get('OBSIDIAN_API_KEY'),
                    help='Obsidian Local REST API bearer key')
    a = ap.parse_args()
    vault = os.path.abspath(a.vault)
    use_rest = bool(a.rest_base and a.rest_key)
    rest_failures = 0

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
    for rel in files:
        if not rel.lower().endswith(MD): continue
        txt, sus = None, False
        if use_rest:
            try:
                txt, sus = read_rest(a.rest_base, a.rest_key, rel)
            except Exception:
                rest_failures += 1
                txt = None
        if txt is None:
            try: txt, sus = read_disk(os.path.join(vault, rel))
            except Exception: continue
        content[rel] = txt
        if sus: suspect.add(rel)
        headings[rel] = {norm_head(h) for h in HEADING.findall(txt)}
        blocks[rel] = set(BLOCKID.findall(txt))

    findings = []
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
    if suspect and not use_rest:
        stale_banner = ("MOUNT MAY BE STALE: %d target(s) read back truncated (NUL bytes). "
                        "Findings off them are downgraded to SUSPECT-STALE. Re-run in a fresh "
                        "session or pass --rest-base/--rest-key to read Obsidian's live view." % len(suspect))
    if a.json:
        print(json.dumps({'shown': show, 'quarantined_count': len(quar),
                          'suspect_count': len(suspect), 'suspect_files': sorted(suspect),
                          'rest': use_rest, 'rest_failures': rest_failures,
                          'stale_banner': stale_banner}, indent=2)); return
    if stale_banner: print("[!] " + stale_banner)
    if use_rest:
        print("read mode: Obsidian Local REST API (live view)%s"
              % (" (%d fell back to disk)" % rest_failures if rest_failures else ""))
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
