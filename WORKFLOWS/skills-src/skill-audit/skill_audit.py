#!/usr/bin/env python3
"""
skill-audit — reconcile a vault's skill SOURCES against the INSTALLED skill cache.

Three layers exist for every Cowork skill:
  1. canonical doc   WORKFLOWS/<name>.md      (source of truth; human-edited)
  2. build artifact  <vault>/WORKFLOWS/skills/<name>.skill (zip, built from the doc via skill-creator)
  3. installed copy  <installed>/<name>/SKILL.md  (what actually RUNS; app-data, outside the vault)

Drift happens at each manual hop (doc->package, package->install). This tool diagnoses
drift + structural integrity and prints a punch list. It NEVER writes the installed cache
(read-only, behind the install trust boundary) — fixes stay manual: rebuild / reinstall.

Usage:
  skill_audit.py --vault <vault_root> --installed <installed_skills_dir> [--workflows <dir>] [--json]
"""
import argparse, os, sys, glob, zipfile, hashlib, re, io

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
            fm[mm.group(1)] = mm.group(2).strip()
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
        # ends on a bare word with no terminal punctuation/backtick — likely a mid-sentence cut
        issues.append("WARN: last line ends mid-word/no terminal punctuation")
    return (len([i for i in issues if i.startswith(("TRUNCATED", "no YAML", "frontmatter"))]) == 0), issues

def load_installed(installed_dir):
    out = {}
    for d in sorted(glob.glob(os.path.join(installed_dir, "*"))):
        sk = os.path.join(d, "SKILL.md")
        if not os.path.isfile(sk):
            continue
        # obs-014 coherence guard: read twice, compare size+linecount
        raw1 = read_bytes(sk); raw2 = read_bytes(sk)
        coherent = (len(raw1) == len(raw2) and raw1.count(b"\n") == raw2.count(b"\n"))
        text = raw1.decode("utf-8", "replace")
        _, fm = frontmatter(text)
        name = fm.get("name") or os.path.basename(d)
        out[name] = dict(path=sk, raw=raw1, text=text, sha=sha(raw1),
                         sections=sections(text), coherent=coherent,
                         mtime=os.path.getmtime(sk))
    return out

def load_packages(vault):
    out = {}
    # Packages live in <vault>/WORKFLOWS/skills/<name>.skill (canonical home, 2026-06-10);
    # the vault root is searched only as a fallback for stray/legacy builds.
    candidates = sorted(glob.glob(os.path.join(vault, "WORKFLOWS", "skills", "*.skill"))) + sorted(glob.glob(os.path.join(vault, "skills", "*.skill"))) + \
                 sorted(glob.glob(os.path.join(vault, "*.skill")))
    for z in candidates:
        try:
            with zipfile.ZipFile(z) as zf:
                inner = [n for n in zf.namelist() if n.endswith("SKILL.md")]
                if not inner:
                    continue
                raw = zf.read(inner[0])
        except Exception as e:
            out[os.path.basename(z)] = dict(path=z, error=str(e))
            continue
        text = raw.decode("utf-8", "replace")
        _, fm = frontmatter(text)
        name = fm.get("name") or os.path.basename(z)[:-6]
        if name in out:           # skills/ wins over a root-level duplicate
            continue
        out[name] = dict(path=z, raw=raw, text=text, sha=sha(raw),
                         sections=sections(text), mtime=os.path.getmtime(z),
                         source_sha=fm.get("source_sha"))
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--installed", required=True)
    ap.add_argument("--workflows", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    wf = a.workflows or os.path.join(a.vault, "WORKFLOWS")

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

        # external / not vault-managed
        if not p and not d:
            verdict = "EXTERNAL"; notes.append("no vault package or doc — not vault-managed")
            rows.append((n, i, p, d, verdict, actions, notes)); continue

        # integrity of installed + package
        if i:
            if not i["coherent"]:
                notes.append("UNCERTAIN: bash read incoherent (^obs-014) — re-read via file tools")
            ok, iss = integrity(i["text"], i["raw"])
            if not ok:
                verdict = "REINSTALL"; actions.append("reinstall (installed copy is broken: %s)" % "; ".join(iss))
        if p:
            ok, iss = integrity(p["text"], p["raw"])
            if not ok:
                verdict = "REBUILD"; actions.append("rebuild (package is broken: %s)" % "; ".join(iss))

        # installed vs package
        if i and p and i["sha"] != p["sha"]:
            if verdict == "OK": verdict = "REINSTALL"
            actions.append("reinstall (installed %s != package %s)" % (i["sha"], p["sha"]))
            miss = set(p["sections"]) - set(i["sections"])
            if miss: notes.append("installed missing sections: " + ", ".join(sorted(miss)))
        if i and not p:
            notes.append("installed but no vault package (orphan or built elsewhere)")
        if p and not i:
            if verdict == "OK": verdict = "REINSTALL"
            actions.append("install (package exists, not installed)")

        # doc vs package (heuristic: mtime; exact if source_sha present)
        if d and p:
            if p.get("source_sha"):
                if p["source_sha"] != d["sha"]:
                    if verdict in ("OK","REINSTALL"): verdict = "REBUILD"
                    actions.append("rebuild (doc sha %s != package source_sha %s)" % (d["sha"], p["source_sha"]))
            elif d["mtime"] > p["mtime"] + 1:
                if verdict in ("OK","REINSTALL"): verdict = "REBUILD"
                actions.append("rebuild? doc edited after last build (heuristic — add source_sha to confirm)")
        if d and not p:
            verdict = "UNBUILT"; actions.append("build .skill from the doc via skill-creator")

        rows.append((n, i, p, d, verdict, actions, notes))

    # render
    print("SKILL AUDIT — %d skills (vault=%s)" % (len(rows), a.vault))
    print("=" * 78)
    hdr = "%-26s %-5s %-4s %-4s %-12s" % ("skill", "inst", "pkg", "doc", "verdict")
    print(hdr); print("-" * 78)
    flagged = []
    for n, i, p, d, verdict, actions, notes in rows:
        print("%-26s %-5s %-4s %-4s %-12s" % (
            n[:26], "yes" if i else "-", "yes" if p else "-", "yes" if d else "-", verdict))
        for a2 in actions: print("      -> " + a2)
        for nt in notes:  print("      .  " + nt)
        if verdict not in ("OK", "EXTERNAL"): flagged.append((n, verdict))
    print("-" * 78)
    if flagged:
        print("PUNCH LIST:")
        for n, v in flagged: print("  [%s] %s" % (v, n))
    else:
        print("All vault-managed skills in sync.")
    return 1 if any(v not in ("OK","EXTERNAL") for _,_,_,_,v,_,_ in rows) else 0

if __name__ == "__main__":
    sys.exit(main())
