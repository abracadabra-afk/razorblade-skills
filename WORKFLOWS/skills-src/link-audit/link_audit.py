#!/usr/bin/env python3
"""link_audit.py - Obsidian vault reference-integrity auditor (read-only).

Scans notes for [[wikilinks]], ![[embeds]], and [md](links), resolves each against
the real file index using Obsidian's rules, plus heading/block-anchor indices.

PATH RESOLUTION (rebuilt 2026-09-11, ^obs-287 / ^backlog-linkaudit-path-resolution).
A link containing "/" is tried against FOUR layers, in Obsidian's own order, not one:
  1. vault-root-relative   ("DEV/registry/items")
  2. source-relative       (the same link written from inside WRITING/PROJECTS/X/)
  3. unique path SUFFIX    (Obsidian's shortest-path-when-possible rule)
  4. suffix matching >1 file -> AMBIGUOUS (resolves to shortest), never DANGLING
Only layer 1 existed before. Its absence produced ~1,600 phantom DANGLING findings
per run - about 95% of all output - and three independent skill-test runs disagreed
by two orders of magnitude (~15 / ~40 / ~1,430) because each one improvised a
different amount of distrust toward it. A link that points at a DIRECTORY resolves
to FOLDER-LINK (the vault's navigational convention), not to breakage.
Wikilink targets are unescaped ("\\|" -> "|") before the alias split: 99 links live
inside markdown tables, where the pipe must be escaped, and splitting the raw text
left a trailing backslash on every one of them.

Reports:
  DANGLING        - target file not found anywhere
  BROKEN-ANCHOR   - file resolves, but ^block-id missing
  BROKEN-HEADING  - file resolves, but #heading missing
  AMBIGUOUS(info) - basename or path-suffix matches >1 file and none in the same
                    folder (Obsidian still resolves to the shortest path; low priority)
  FOLDER-LINK     - benign: the target is a real DIRECTORY, not a note. The vault
                    links at folders as navigation on purpose. Never actionable.
  HOUSE-PREFIX    - benign: a heading cite on _DIRECTIVES / _SKILLS MAP written as a
                    stable identifier PREFIX rather than full heading text. CRE ruled
                    this house style 2026-08-19 (^backlog-heading-prefix-cites); the
                    resolver accepts it so the 32 closed items cannot return as
                    findings. Reason the ruling stands: those headings get amended
                    (DIR-005's four times), so pinning cites to full text guarantees
                    re-breakage. DIR-014's own logic - widen the exact layer.
  CLIPPING        - benign: a Web Clipper artifact under Clippings/ (author bylines,
                    javascript: nav stubs). Never authored as vault links.
  TEMPLATE        - benign: a placeholder in a template/prompt asset (<NAME>, {{var}}).
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
# history added 2026-08-10 (^backlog-linkaudit-unpack-bug (c)): carved archives hold refs
# to moved content by design. skill-tests added 2026-09-11: `skill-test` copies real notes
# into per-run fixture trees, so every link in them double-counts a link already scanned
# at its real path - and the count moves whenever a test runs, which is the one thing the
# baseline must not do.
QZONES   = ('/GRAVEYARD/', '/evals/', '/SYSTEM/history/', '/SYSTEM/skill-tests/')
QFILES   = ('_CHANGELOG.md', '_OBSERVATIONS.md', 'vault-migration-plan.md')

# --- benign classes: real unresolved links that are NOT breakage ------------------
# Every class below was a judgment call an agent re-made from scratch on each run.
# They are mechanical now, because that improvisation is where the run-to-run
# inconsistency lived, not in the resolver's arithmetic.
CLIPPING_ZONES = ('Clippings/', 'COMP LISTINGS/')  # Web Clipper output: author bylines, nav stubs
TEMPLATE_HINTS = ('_TEMPLATE', '/templates/', '/prompts/')
PLACEHOLDER    = re.compile(r'[<>{}]|^javascript:|\$\{|\.\.\.|…')
# Documented metavariables: tokens the OS docs use as STAND-INS inside example link
# syntax ("resolved against [[Entry]] — confirm", "[[X]]", "[[SEQ NN]]"). A stoplist,
# deliberately - DIR-014 says widen the EXACT layer, never loosen the matcher. Adding
# a token here is a one-line, reviewable change; a heuristic over doc paths would
# swallow real breakage in WORKFLOWS/ canon, which is where link rot actually hurts.
METAVARS = {'x', 'n', 'nn', 'entry', 'note', 'file', 'title', 'link', 'links',
            'wikilinks', 'embeds', 'seq nn', 'date', 'name', 'slug', 'project'}
# Heading cites by stable identifier PREFIX are house style on exactly these two
# files (CRE-ruled 2026-08-19, ^backlog-heading-prefix-cites). Accept, don't flag.
HOUSE_ANCHORS  = {'_directives', '_skills map'}

def quarantined(rel):
    if any(z in '/' + rel for z in QZONES): return True
    b = os.path.basename(rel)
    return b in QFILES or b.startswith('_pre-migration') or b.endswith('.bak.md')

def strip_code(txt):
    txt = re.sub(r'```.*?```', '', txt, flags=re.S)
    txt = re.sub(r'~~~.*?~~~', '', txt, flags=re.S)
    txt = re.sub(r'`[^`\n]*`', '', txt)
    return txt

# DO NOT strip a heading's trailing provenance stamp ("## Sanctuaries along the
# trail *(CRE, 2026-06-29)*") to match a cite that omits it. Tried 2026-09-11 and
# REVERTED: the heading renders fine but Obsidian anchors on the FULL text, so the
# cite genuinely will not navigate - and the 2026-09-06 run already ruled exactly
# these two cites real (^backlog-linkaudit-fixlist-2026-09-06). They sit outside
# the 08-19 prefix ruling, which is scoped to _DIRECTIVES / _SKILLS MAP only.
# Suppressing them would re-open a settled call as a silent non-finding.
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
    ap.add_argument('--benign', action='store_true',
                    help='show the benign classes (FOLDER-LINK / HOUSE-PREFIX / CLIPPING / TEMPLATE)')
    a = ap.parse_args()
    vault = os.path.abspath(a.vault)
    read_failures = []

    files = []
    for root, dirs, fs in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIPDIRS]
        for f in fs:
            files.append(os.path.relpath(os.path.join(root, f), vault).replace('\\', '/'))

    by_rel, by_base, by_base_ext, by_suffix = {}, {}, {}, {}
    dirset = set()
    for rel in files:
        rl = rel.lower(); by_rel[rl] = rel
        if rl.endswith(MD): by_rel[rl[:-3]] = rel
        base = os.path.basename(rel); stem, ext = os.path.splitext(base)
        by_base.setdefault(stem.lower(), []).append(rel)
        by_base_ext.setdefault(base.lower(), []).append(rel)
        # Obsidian's shortest-path-when-possible rule: a link may name any unique
        # trailing slice of a path. Indexed once here; a per-link scan of by_rel
        # would be O(links x files) and this vault has ~7k files.
        parts = rl.split('/')
        for i in range(1, len(parts)):
            suf = '/'.join(parts[i:])
            by_suffix.setdefault(suf, []).append(rel)
            if suf.endswith(MD): by_suffix.setdefault(suf[:-3], []).append(rel)
        # every ancestor directory, so a link at a folder is classified, not flagged
        p = os.path.dirname(rl)
        while p:
            dirset.add(p); p = os.path.dirname(p)

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

    def benign_class(src, tgt):
        """Name the benign class of an unresolved link, or None if it is real breakage."""
        s = '/' + src
        if any(z in s for z in CLIPPING_ZONES): return 'CLIPPING'
        if any(h in s for h in TEMPLATE_HINTS) or PLACEHOLDER.search(tgt): return 'TEMPLATE'
        if tgt.strip().lower() in METAVARS: return 'TEMPLATE'
        return None

    def house_prefix(target_rel, frag):
        """True if frag cites a heading on an OS anchor by its stable identifier.

        Prefix match covers "DIR-005" and "Cowork skills"; a contained match covers
        "_SKILLS MAP#Fiction" against "Lane 1: Fiction Writing". Bounded to the two
        files CRE ruled on - never widened to the vault (DIR-014: widen the exact
        layer, never chase the drift).
        """
        stem = os.path.splitext(os.path.basename(target_rel))[0].lower()
        if stem not in HOUSE_ANCHORS: return False
        f = norm_head(frag)
        return bool(f) and any(h.startswith(f) or f in h for h in headings.get(target_rel, set()))

    def resolve(target, ext_hint, src):
        """Four-layer path resolution + basename resolution. See module docstring.

        Layer order is Obsidian's, and the order matters: a link that resolves
        source-relative must not be reported because it failed root-relative.
        """
        t = target.strip()
        if not t: return ('self', src)
        tl = t.lower()
        if '/' in t:
            # 1. vault-root-relative
            for c in (tl, tl + MD):
                if c in by_rel: return ('ok', by_rel[c])
            # 2. source-relative to the linking note's folder
            # NOTE: src carries the real casing; by_rel is keyed lowercase. Joining
            # without lowering silently skips this layer, and the link then falls
            # through to the suffix layer and matches the WRONG project's file -
            # which is worse than a miss, because the heading check then runs
            # against a file the author never linked. (Caught 2026-09-11 by the
            # closing self-check on its own first run: 327 phantom BROKEN-HEADINGs.)
            sdir = os.path.dirname(src).lower()
            if sdir:
                rp = os.path.normpath(os.path.join(sdir, tl)).replace('\\', '/')
                for c in (rp, rp + MD):
                    if c in by_rel: return ('ok', by_rel[c])
            # 3/4. unique path suffix, else shortest-path among several
            sufhits = by_suffix.get(tl) or by_suffix.get(tl + MD) or []
            if len(sufhits) == 1: return ('ok', sufhits[0])
            if len(sufhits) > 1:
                pick = sorted(sufhits, key=lambda h: (h.count('/'), len(h)))[0]
                return ('ambiguous', pick)
            if tl in dirset: return ('folder', t)
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
        if tl in dirset: return ('folder', t)
        return ('dangling', None)

    def check(src, embed, inner):
        # A wikilink inside a markdown TABLE must escape its alias pipe as "\|".
        # Splitting the raw text left a trailing backslash on the target and made
        # all 99 of them phantom-DANGLING. Unescape before the alias split.
        part = inner.replace('\\|', '|').split('|', 1)[0]
        tgt, frag = part.split('#', 1) if '#' in part else (part, None)
        status, rel = resolve(tgt, embed, src)
        if status == 'dangling' and "''" in tgt:
            # ^obs-064: a wikilink inside a YAML single-quoted frontmatter scalar escapes an
            # apostrophe by doubling it ('[[Pig''s Box]]'); Obsidian unescapes before resolving.
            status, rel = resolve(tgt.replace("''", "'"), embed, src)
        kind = 'embed' if embed else 'link'
        if status == 'folder':
            findings.append(('FOLDER-LINK', src, inner.strip(),
                             'target is a directory (%s) - vault navigation convention, not breakage' % rel)); return
        if status == 'dangling':
            findings.append((benign_class(src, tgt) or 'DANGLING', src, inner.strip(),
                             'target not found')); return
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
                if house_prefix(target_rel, f):
                    findings.append(('HOUSE-PREFIX', src, inner.strip(),
                                     'identifier-prefix cite on %s - house style, CRE-ruled 2026-08-19' % target_rel))
                else:
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
            if not ok:
                sufhits = by_suffix.get(href.lower()) or by_suffix.get(href.lower() + MD) or []
                ok = bool(sufhits)
            if not ok and (href.lower().rstrip('/') in dirset or cr.rstrip('/') in dirset):
                findings.append(('FOLDER-LINK', rel, href, 'md-link target is a directory')); continue
            if not ok:
                findings.append((benign_class(rel, href) or 'DANGLING', rel, href,
                                 'md-link target not found'))

    BENIGN = ('FOLDER-LINK', 'HOUSE-PREFIX', 'CLIPPING', 'TEMPLATE', 'AMBIGUOUS')
    show = [f for f in findings if not quarantined(f[1])]
    quar = [f for f in findings if quarantined(f[1])]
    benign = [f for f in show if f[0] in BENIGN]
    if not a.benign:
        show = [f for f in show if f[0] not in BENIGN]
    elif not a.ambiguous:
        show = [f for f in show if f[0] != 'AMBIGUOUS']

    # --- CLOSING SELF-CHECK (DIR-018) -------------------------------------------
    # Apply the resolver's own known limitations to its own actionable section
    # before printing. Every remaining DANGLING is re-resolved through all four
    # path layers plus the directory index; anything that resolves on the second
    # pass is a resolver bug, not a finding, and is pulled out LOUDLY rather than
    # shipped. Three test runs put four such false positives in section A.
    caught = []       # a finding the resolver itself can overturn -> its own BUG, print loud
    ambig_frag = []   # target matched several files; fragment lives in one of the others.
                      # Not a bug and not confident breakage - the link is genuinely
                      # ambiguous. Counted, never listed, never actionable.
    for f in list(show):
        part = f[2].replace('\\|', '|').split('|', 1)[0]
        raw, frag = part.split('#', 1) if '#' in part else (part, None)
        raw = raw.strip()
        if not raw: continue
        if f[0] == 'DANGLING':
            st, _rel = resolve(raw, False, f[1])
            if st in ('ok', 'ambiguous', 'folder', 'self'):
                show.remove(f); caught.append((f, 're-resolves as ' + st))
        elif f[0] in ('BROKEN-HEADING', 'BROKEN-ANCHOR') and frag:
            # A fragment finding is only confident if the FILE was unambiguous.
            # Where several files match the link, Obsidian picks one and we may
            # have picked another; if the fragment exists in ANY candidate the
            # finding is a resolver artifact, not breakage.
            tl = raw.lower()
            cands = (by_suffix.get(tl) or by_suffix.get(tl + MD) or
                     by_base.get(os.path.basename(tl), []))
            if len(cands) > 1:
                ff = frag.strip()
                hit = any((ff[1:] in blocks.get(c, set())) if ff.startswith('^')
                          else (norm_head(ff) in headings.get(c, set())) for c in cands)
                if hit:
                    show.remove(f); ambig_frag.append(f)

    stale_banner = None
    if suspect:
        stale_banner = ("MOUNT MAY BE STALE: %d target(s) read back truncated (NUL bytes). "
                        "Findings off them are downgraded to SUSPECT-STALE. Re-run in a fresh "
                        "session and confirm surprising findings via the file tools." % len(suspect))
    benign_counts = dict(Counter(f[0] for f in benign))
    if a.json:
        print(json.dumps({'shown': show, 'actionable_count': len(show),
                          'benign': benign if a.benign else [], 'benign_counts': benign_counts,
                          'self_check_caught': [[list(f), st] for f, st in caught],
                          'ambiguous_fragment_count': len(ambig_frag),
                          'quarantined_count': len(quar),
                          'suspect_count': len(suspect), 'suspect_files': sorted(suspect),
                          'md_scanned': len(content), 'md_total': md_total,
                          'read_failures': read_failures,
                          'stale_banner': stale_banner}, indent=2)); return
    if stale_banner: print("[!] " + stale_banner)
    if read_failures:
        print("[!] %d file(s) could not be read (excluded from scan, NOT evidence of absence):" % len(read_failures))
        for rf in read_failures[:10]: print("      %s: %s" % rf)
    print("LINK AUDIT  vault=%s" % vault)
    print("%d md scanned (of %d files)" % (len(content), len(files)))
    # The suppression arithmetic, printed - not left to the reader to re-derive.
    print("net ACTIONABLE: %d   (benign suppressed: %s | quarantined: %d | "
          "ambiguous-fragment: %d | self-check caught: %d)"
          % (len(show), benign_counts or '{}', len(quar), len(ambig_frag), len(caught)))
    print("severity:", dict(Counter(f[0] for f in show)) or "clean")
    for sev, src, raw, detail in sorted(show):
        print("  [%s] %s\n       %s  ->  %s" % (sev, src, raw[:80], detail[:120]))
    if caught:
        print("\n[!] SELF-CHECK caught %d item(s) that would have shipped as false positives\n"
              "    (re-resolved on the second pass -> resolver bug, report it, do NOT list them):" % len(caught))
        for f, st in caught[:10]: print("      %s  %s  -> %s" % (f[1], f[2][:60], st))
    if a.benign and benign:
        print("\n-- benign, not actionable (%d) --" % len(benign))
        for sev, src, raw, detail in sorted(benign):
            print("  [%s] %s  %s" % (sev, src, raw[:60]))
    if a.all and quar:
        print("\n-- quarantined (%d) --" % len(quar))
        for sev, src, raw, detail in sorted(quar):
            print("  [%s] %s  %s" % (sev, src, raw[:60]))

if __name__ == '__main__': main()
