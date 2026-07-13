#!/usr/bin/env python3
"""
skill-audit — reconcile a vault's skill SOURCES against the INSTALLED skill cache.

Three layers exist for every Cowork skill:
  1. canonical doc   WORKFLOWS/<name>.md      (source of truth; human-edited)
  2. build artifact  <vault>/WORKFLOWS/skills/<name>.skill (zip, packed on the DESKTOP via pack-skills.ps1)
  3. installed copy  <installed>/<name>/...   (what actually RUNS; app-data, outside the vault)

Drift happens at each manual hop (doc->package, package->install). This tool diagnoses
drift + structural integrity and prints a punch list. It NEVER writes the installed cache
(read-only, behind the install trust boundary) — fixes stay manual: rebuild / reinstall.

TWO THINGS THIS TOOL LEARNED THE HARD WAY (2026-07-13, ^obs-183)
----------------------------------------------------------------
1. THE INSTALLED CACHE MUST NOT BE READ THROUGH A SANDBOX MOUNT.
   Read via the Cowork bash mount (/sessions/<id>/mnt/.claude/skills/), this cache serves
   STALE PARTIALS — it reported a 6,876 B decision-helper/SKILL.md while the desktop held
   the correct 9,568 B copy written minutes earlier, and showed a directory caught
   MID-UPDATE (a fresh references/ file beside a stale SKILL.md). Two false findings were
   filed off that view. The old ^obs-014 double-read "coherence" guard does NOT save you:
   it detects a TORN read, not a STALE one — a stale read is perfectly self-consistent, so
   it reads twice, gets the same wrong bytes, and reports "coherent" with full confidence.
   This script therefore HARD-FAILS on a mounted --installed path (override: --allow-mount,
   which downgrades every drift verdict to UNCERTAIN, because it must).

2. THE AUDIT MUST COMPARE THE WHOLE TREE, NOT JUST SKILL.md.
   Multi-file skills (references/, scripts/, templates/) had their payloads compared
   against NOTHING: the old loader read only SKILL.md at both ends, so a package whose
   references/ never reached the cache read as OK. Now: enumerate both trees, diff the
   relpath sets, and sha every shared file.

A THIRD FAILURE MODE NO FILE CHECK CAN SEE: a freshly Save-skill'd skill is NOT LIVE until
the Cowork session restarts (the skill list is snapshotted at boot). A correct install can
therefore look "not fixed". This script prints that reminder whenever it reports an install
action — see the footer.

Usage:
  skill_audit.py --vault <vault_root> --installed <installed_skills_dir> [--workflows <dir>]
                 [--json] [--allow-mount]

Run it where the installed cache is LOCAL AND REAL — i.e. on the desktop (via windows-cli or
a local python), pointed at the actual AppData path — not from the sandbox.
"""
import argparse, os, sys, glob, zipfile, hashlib, re, json, posixpath

# Path shapes that indicate a sandbox mount rather than a real local filesystem.
MOUNT_MARKERS = (
    re.compile(r"^/sessions/[^/]+/mnt/"),   # Cowork workspace mount
    re.compile(r"^/mnt/(c|d)/", re.I),      # WSL-style passthrough
)

def is_mounted(path):
    p = path.replace("\\", "/")
    return any(m.search(p) for m in MOUNT_MARKERS)

def sha(b):
    return hashlib.sha256(b).hexdigest()[:12]

def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()

def frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        return None, {}
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r'^([A-Za-z0-9_]+):\s*(.*)$', line)
        if mm:
            v = mm.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]            # some skills quote their scalars; unquote for name-matching
            fm[mm.group(1)] = v
    return m.group(1), fm

def sections(text):
    return [l[3:].strip() for l in text.splitlines() if l.startswith("## ")]

def integrity(text, raw):
    """Return (ok, [issues]) for a SKILL.md body."""
    issues = []
    fm_block, fm = frontmatter(text)
    if fm_block is None:
        issues.append("no YAML frontmatter")
    else:
        if not fm.get("name"): issues.append("frontmatter missing name")
        if not fm.get("description"): issues.append("frontmatter missing description")
    if not raw.endswith(b"\n"):
        issues.append("TRUNCATED: no trailing newline")
    last = text.rstrip("\n").splitlines()[-1] if text.strip() else ""
    if re.search(r'[A-Za-z]$', last) and not last.endswith(("notes", "prose")):
        issues.append("WARN: last line ends mid-word/no terminal punctuation")
    return (len([i for i in issues if i.startswith(("TRUNCATED", "no YAML", "frontmatter"))]) == 0), issues

def load_installed(installed_dir):
    """Enumerate the ENTIRE installed tree per skill, not just SKILL.md (^obs-183)."""
    out = {}
    for d in sorted(glob.glob(os.path.join(installed_dir, "*"))):
        if not os.path.isdir(d):
            continue
        sk = os.path.join(d, "SKILL.md")
        if not os.path.isfile(sk):
            continue
        payload = {}
        for root, _dirs, files in os.walk(d):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, d).replace(os.sep, "/")
                try:
                    payload[rel] = sha(read_bytes(full))
                except OSError as e:
                    payload[rel] = "ERR:%s" % e.__class__.__name__
        raw = read_bytes(sk)
        text = raw.decode("utf-8", "replace")
        _, fm = frontmatter(text)
        name = fm.get("name") or os.path.basename(d)
        out[name] = dict(path=sk, raw=raw, text=text, sha=sha(raw),
                         sections=sections(text), payload=payload,
                         mtime=os.path.getmtime(sk))
    return out

def load_packages(vault):
    """Enumerate every zip entry, not just the inner SKILL.md (^obs-183)."""
    out = {}
    candidates = sorted(glob.glob(os.path.join(vault, "WORKFLOWS", "skills", "*.skill"))) + \
                 sorted(glob.glob(os.path.join(vault, "skills", "*.skill"))) + \
                 sorted(glob.glob(os.path.join(vault, "*.skill")))
    for z in candidates:
        try:
            with zipfile.ZipFile(z) as zf:
                names = [n for n in zf.namelist() if not n.endswith("/")]
                inner = [n for n in names if n.endswith("SKILL.md")]
                if not inner:
                    continue
                skill_md = sorted(inner, key=len)[0]     # the top-level <name>/SKILL.md
                base = posixpath.dirname(skill_md)       # strip the "<name>/" package root
                raw = zf.read(skill_md)
                payload = {}
                for n in names:
                    rel = posixpath.relpath(n, base) if base else n
                    payload[rel] = sha(zf.read(n))
        except Exception as e:
            out[os.path.basename(z)] = dict(path=z, error=str(e))
            continue
        text = raw.decode("utf-8", "replace")
        _, fm = frontmatter(text)
        name = fm.get("name") or os.path.basename(z)[:-6]
        if name in out:           # skills/ wins over a root-level duplicate
            continue
        out[name] = dict(path=z, raw=raw, text=text, sha=sha(raw),
                         sections=sections(text), payload=payload,
                         mtime=os.path.getmtime(z), source_sha=fm.get("source_sha"))
    return out

def load_docs(wf):
    out = {}
    for m in sorted(glob.glob(os.path.join(wf, "*.md"))):
        raw = read_bytes(m); text = raw.decode("utf-8", "replace")
        _, fm = frontmatter(text)
        name = fm.get("name")
        if not name:
            continue
        out[name] = dict(path=m, sha=sha(raw), mtime=os.path.getmtime(m),
                         last_updated=fm.get("last_updated"))
    return out

def compare_payloads(i, p):
    """Whole-tree diff: files only in the package, only installed, and sha-divergent."""
    ip, pp = i["payload"], p["payload"]
    missing = sorted(set(pp) - set(ip))          # packaged but never installed
    extra   = sorted(set(ip) - set(pp))          # installed but not in the package
    changed = sorted(k for k in (set(ip) & set(pp)) if ip[k] != pp[k])
    return missing, extra, changed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--installed", required=True)
    ap.add_argument("--workflows", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-mount", action="store_true",
                    help="audit a mounted installed-cache anyway; ALL drift verdicts become UNCERTAIN")
    a = ap.parse_args()
    wf = a.workflows or os.path.join(a.vault, "WORKFLOWS")

    # --- Freshness gate (^obs-183) ---------------------------------------------------
    mounted = is_mounted(a.installed)
    if mounted and not a.allow_mount:
        sys.stderr.write(
            "REFUSING TO AUDIT A MOUNTED INSTALLED CACHE.\n\n"
            "  --installed resolves to a sandbox mount:\n    %s\n\n"
            "A Cowork/WSL mount serves STALE PARTIALS of this cache. It has already produced\n"
            "false 'stale install' findings (^obs-183) — and the double-read coherence guard\n"
            "cannot catch it, because a stale read is self-consistent.\n\n"
            "Run this on the DESKTOP against the real AppData path, e.g.:\n"
            "  python skill_audit.py --vault <vault> --installed \\\n"
            "    \"C:/Users/<you>/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/.../skills\"\n\n"
            "To audit through the mount anyway (results are advisory only):  --allow-mount\n"
            % a.installed)
        return 2
    # ---------------------------------------------------------------------------------

    inst = load_installed(a.installed)
    pkgs = load_packages(a.vault)
    docs = load_docs(wf)

    names = sorted(set(inst) | set(pkgs) | set(docs))
    rows = []
    for n in names:
        i, p, d = inst.get(n), pkgs.get(n), docs.get(n)
        verdict, actions, notes = "OK", [], []

        if p and "error" in p:
            verdict = "BROKEN-PKG"; notes.append("package unreadable: " + p["error"])
            rows.append((n, i, p, d, verdict, actions, notes)); continue

        if not p and not d:
            verdict = "EXTERNAL"; notes.append("no vault package or doc — not vault-managed")
            rows.append((n, i, p, d, verdict, actions, notes)); continue

        # integrity of installed + package
        if i:
            ok, iss = integrity(i["text"], i["raw"])
            if not ok:
                verdict = "REINSTALL"; actions.append("reinstall (installed copy is broken: %s)" % "; ".join(iss))
        if p:
            ok, iss = integrity(p["text"], p["raw"])
            if not ok:
                verdict = "REBUILD"; actions.append("rebuild (package is broken: %s)" % "; ".join(iss))

        # installed vs package — SKILL.md
        if i and p and i["sha"] != p["sha"]:
            if verdict == "OK": verdict = "REINSTALL"
            actions.append("reinstall (SKILL.md: installed %s != package %s)" % (i["sha"], p["sha"]))
            miss = set(p["sections"]) - set(i["sections"])
            if miss: notes.append("installed missing sections: " + ", ".join(sorted(miss)))

        # installed vs package — THE WHOLE PAYLOAD (^obs-183)
        if i and p:
            missing, extra, changed = compare_payloads(i, p)
            payload_drift = [x for x in missing + changed if x != "SKILL.md"]
            if payload_drift:
                if verdict == "OK": verdict = "REINSTALL"
                if missing:
                    actions.append("reinstall (packaged but NOT installed: %s)" % ", ".join(missing))
                if [c for c in changed if c != "SKILL.md"]:
                    actions.append("reinstall (installed payload differs: %s)"
                                   % ", ".join(c for c in changed if c != "SKILL.md"))
            if extra:
                notes.append("installed-only files (stale leftovers?): " + ", ".join(extra))
            notes.append("payload: %d file(s) packaged, %d installed" % (len(p["payload"]), len(i["payload"])))

        if i and not p:
            notes.append("installed but no vault package (orphan, or the raw-doc install bypass — DIR-009)")
        if p and not i:
            if verdict == "OK": verdict = "REINSTALL"
            actions.append("install (package exists, not installed)")

        # doc vs package
        if d and p:
            if p.get("source_sha"):
                if p["source_sha"] != d["sha"]:
                    if verdict in ("OK", "REINSTALL"): verdict = "REBUILD"
                    actions.append("rebuild (doc sha %s != package source_sha %s)" % (d["sha"], p["source_sha"]))
            elif d["mtime"] > p["mtime"] + 1:
                if verdict in ("OK", "REINSTALL"): verdict = "REBUILD"
                actions.append("rebuild? doc edited after last build (heuristic — add source_sha to confirm)")
        if d and not p:
            verdict = "UNBUILT"; actions.append("pack the .skill on the DESKTOP via pack-skills.ps1 (DIR-009)")

        # A mounted read cannot justify a drift verdict — downgrade, don't assert.
        if mounted and verdict in ("REINSTALL", "REBUILD"):
            notes.append("UNCERTAIN: read through a sandbox mount (^obs-183) — confirm on the desktop before acting")
            verdict = "UNCERTAIN"

        rows.append((n, i, p, d, verdict, actions, notes))

    if a.json:
        print(json.dumps([dict(name=n, installed=bool(i), package=bool(p), doc=bool(d),
                               verdict=v, actions=acts, notes=nts)
                          for n, i, p, d, v, acts, nts in rows], indent=2))
        return 1 if any(v not in ("OK", "EXTERNAL") for _, _, _, _, v, _, _ in rows) else 0

    print("SKILL AUDIT — %d skills (vault=%s)" % (len(rows), a.vault))
    if mounted:
        print("!! MOUNTED INSTALLED CACHE (--allow-mount): every drift verdict is ADVISORY (^obs-183).")
    print("=" * 78)
    print("%-26s %-5s %-4s %-4s %-12s" % ("skill", "inst", "pkg", "doc", "verdict"))
    print("-" * 78)
    flagged = []
    for n, i, p, d, verdict, actions, notes in rows:
        print("%-26s %-5s %-4s %-4s %-12s" % (
            n[:26], "yes" if i else "-", "yes" if p else "-", "yes" if d else "-", verdict))
        for a2 in actions: print("      -> " + a2)
        for nt in notes:   print("      .  " + nt)
        if verdict not in ("OK", "EXTERNAL"): flagged.append((n, verdict))
    print("-" * 78)
    if flagged:
        print("PUNCH LIST:")
        for n, v in flagged: print("  [%s] %s" % (v, n))
        if any(v in ("REINSTALL", "UNCERTAIN") for _, v in flagged):
            print("\nNOTE: a Save-skill does NOT go live until the Cowork session RESTARTS —")
            print("      the skill list is snapshotted at boot. A correct install can still")
            print("      look 'not fixed' in the session that performed it (^obs-183).")
    else:
        print("All vault-managed skills in sync.")
    return 1 if any(v not in ("OK", "EXTERNAL") for _, _, _, _, v, _, _ in rows) else 0

if __name__ == "__main__":
    sys.exit(main())
