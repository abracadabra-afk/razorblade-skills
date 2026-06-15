#!/usr/bin/env python3
"""
build.py - Git Bridge skill build + audit tool (razorblade-skills)

Runs in the Cowork sandbox against a clone of razorblade-skills (race-free), or
on the desktop. A .skill is a zip whose single top dir is the skill name:
  <name>/SKILL.md  (+ optional scripts/ , templates/ , head.txt ...)

Subcommands:
  verify   every .skill unzips, SKILL.md frontmatter parses (name+description),
           body is non-empty and not obviously truncated. Recomputes zip + content
           SHA-256 and, if skills-manifest.json is present, checks the zip SHA.
  extract  unpack each .skill -> WORKFLOWS/skills-src/<name>/ so SKILL.md becomes a
           diffable, version-controlled source file instead of a binary blob.
  package  re-zip WORKFLOWS/skills-src/<name>/ -> WORKFLOWS/skills/<name>.skill DETERMINISTICALLY
           (sorted entries, fixed timestamp, fixed compression) so a rebuild is
           byte-reproducible; then rewrite skills-manifest.json.
  audit    compare each package's CONTENT hash against the INSTALLED copy in the
           skills cache -> current / STALE / SUSPECT-STALE / not-installed. Answers
           the real question: "is what's actually running the same as the canonical
           package?" A hash mismatch off a TRUNCATED/NUL installed-side read (the
           Dropbox/installed-cache mount staleness, obs-014/obs-070) is downgraded to
           SUSPECT-STALE -- not a confident STALE -- so the sweep stops queuing false
           reinstalls; re-confirm those via the file tools / a fresh session.

content_sha256 = sha256 over the skill's files keyed by path RELATIVE TO THE SKILL
ROOT (leading '<name>/' stripped), sorted, so package(zip) and installed(dir) are
directly comparable regardless of zip metadata.

Typical sandbox use:
  git clone --depth 1 https://github.com/abracadabra-afk/razorblade-skills.git /tmp/rs
  python3 build.py verify --root /tmp/rs
  python3 build.py audit  --root /tmp/rs        # auto-detects the installed cache
"""
import sys, os, io, json, hashlib, zipfile, pathlib, argparse, datetime

def sha256(b): return hashlib.sha256(b).hexdigest()

def pkg_files(skill_path):
    """{relpath_under_skillroot: bytes} for a .skill zip."""
    name = pathlib.Path(skill_path).stem
    out = {}
    with zipfile.ZipFile(skill_path) as z:
        for zi in z.infolist():
            if zi.is_dir(): continue
            rel = zi.filename
            if rel.startswith(name + "/"): rel = rel[len(name)+1:]
            out[rel] = z.read(zi.filename)
    return out

def dir_files(skill_dir):
    """{relpath: bytes} for an installed/extracted skill directory."""
    out = {}
    base = pathlib.Path(skill_dir)
    for p in sorted(base.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(base)).replace(os.sep, "/")] = p.read_bytes()
    return out

def content_hash(files: dict):
    h = hashlib.sha256()
    for rel in sorted(files):
        h.update(rel.encode()); h.update(b"\0")
        h.update(hashlib.sha256(files[rel]).digest())
    return h.hexdigest()

def parse_frontmatter(skill_md: bytes):
    t = skill_md.decode("utf-8", "replace")
    if not t.startswith("---"): return None, "no frontmatter"
    end = t.find("\n---", 3)
    if end < 0: return None, "unterminated frontmatter"
    fm = t[3:end]
    name = desc = None
    for line in fm.splitlines():
        if line.startswith("name:"): name = line[5:].strip()
        if line.startswith("description:"): desc = line[12:].strip()
    body = t[end+4:].strip()
    return {"name": name, "description": desc, "body": body}, None

TRUNC_OK_END = tuple(".!?)\"'`*_:>0123456789")  # 'looks complete' last chars
def looks_truncated(body: str):
    if not body: return True
    s = body.rstrip()
    last = s[-1]
    return (last not in TRUNC_OK_END) and last.islower() and s[-2:].isalpha()

def mount_suspect(pkg_d: dict, inst_d: dict):
    """Detect a poisoned/truncated INSTALLED-side read (obs-014/obs-070/obs-073).
    Signatures: a NUL byte or the UTF-8 replacement char in any installed file, or
    an installed file that is a non-empty proper PREFIX of its package counterpart
    (the classic mount-truncation pattern). Returns (bool, reason) so a content-hash
    mismatch off a bad read is reported SUSPECT-STALE rather than a false STALE."""
    for rel, b in inst_d.items():
        if b"\x00" in b or b"\xef\xbf\xbd" in b:
            return True, f"NUL/replacement byte in installed {rel}"
    for rel, pb in pkg_d.items():
        ib = inst_d.get(rel)
        if ib is None:
            continue
        if ib != pb and 0 < len(ib) < len(pb) and pb[:len(ib)] == ib:
            return True, f"installed {rel} is a truncated prefix ({len(ib)}/{len(pb)}B)"
    return False, ""

def packages(root):
    d = pathlib.Path(root) / "WORKFLOWS" / "skills"
    return sorted(d.glob("*.skill"))

def cmd_verify(root):
    man = {}
    mpath = pathlib.Path(root) / "skills-manifest.json"
    if mpath.exists():
        man = {s["name"]: s for s in json.loads(mpath.read_text(encoding="utf-8-sig")).get("skills", [])}
    pk = packages(root)
    bad = 0
    print(f"verify: {len(pk)} package(s)")
    for sp in pk:
        name = sp.stem
        try:
            files = pkg_files(sp)
        except Exception as e:
            print(f"  FAIL  {name}: not a valid zip ({e})"); bad += 1; continue
        if "SKILL.md" not in files:
            print(f"  FAIL  {name}: no SKILL.md"); bad += 1; continue
        fm, err = parse_frontmatter(files["SKILL.md"])
        if err: print(f"  FAIL  {name}: {err}"); bad += 1; continue
        if fm["name"] != name:
            print(f"  WARN  {name}: frontmatter name='{fm['name']}' != filename")
        body = fm["body"]
        flags = []
        if looks_truncated(body): flags.append("BODY-MAYBE-TRUNCATED")
        zsha = sha256(sp.read_bytes())
        if name in man and man[name].get("sha256") and man[name]["sha256"] != zsha:
            flags.append("MANIFEST-SHA-MISMATCH")
        print(f"  {'ok  ' if not flags else 'FLAG'}  {name:<20} files={len(files)} body={len(body)}B  {' '.join(flags)}")
        if "BODY-MAYBE-TRUNCATED" in flags: bad += 1
    print(f"verify: {'OK' if bad==0 else str(bad)+' problem(s)'}")
    return bad

def cmd_extract(root):
    src = pathlib.Path(root) / "WORKFLOWS" / "skills-src"
    for sp in packages(root):
        name = sp.stem
        for rel, data in pkg_files(sp).items():
            dst = src / name / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
        print(f"  extracted {name} -> skills-src/{name}/")
    print(f"extract: wrote sources for {len(packages(root))} skill(s) to {src}")

FIXED_DT = (1980, 1, 1, 0, 0, 0)
def cmd_package(root):
    src = pathlib.Path(root) / "WORKFLOWS" / "skills-src"
    outdir = pathlib.Path(root) / "WORKFLOWS" / "skills"
    outdir.mkdir(parents=True, exist_ok=True)
    names = sorted(p.name for p in src.iterdir() if p.is_dir()) if src.exists() else []
    skills = []
    for name in names:
        sdir = src / name
        rels = sorted(str(p.relative_to(sdir)).replace(os.sep, "/") for p in sdir.rglob("*") if p.is_file())
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for rel in rels:
                zi = zipfile.ZipInfo(f"{name}/{rel}", date_time=FIXED_DT)
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                z.writestr(zi, (sdir / rel).read_bytes())
        data = buf.getvalue()
        (outdir / f"{name}.skill").write_bytes(data)
        skills.append({"name": name, "package": f"WORKFLOWS/skills/{name}.skill",
                       "sha256": sha256(data), "content_sha256": content_hash(dir_files(sdir)),
                       "bytes": len(data)})
        print(f"  packaged {name} ({len(data)}B)")
    man = {"generated": datetime.datetime.now().astimezone().isoformat(),
           "note": "sha256=zip; content_sha256=SKILL.md+assets (installed-comparable). Built by build.py.",
           "skills": skills}
    (pathlib.Path(root) / "skills-manifest.json").write_text(json.dumps(man, indent=2) + "\n", encoding="utf-8")
    print(f"package: {len(skills)} skill(s); manifest rewritten")

def cmd_audit(root, installed_root):
    inst = pathlib.Path(installed_root)
    print(f"audit: packages in {root}  vs installed cache {installed_root}\n")
    cur = stale = suspect = missing = 0
    for sp in packages(root):
        name = sp.stem
        pkg_d = pkg_files(sp)
        pkg_h = content_hash(pkg_d)
        idir = inst / name
        if not idir.exists():
            print(f"  NOT-INSTALLED  {name}"); missing += 1; continue
        inst_d = dir_files(idir)
        inst_h = content_hash(inst_d)
        if inst_h == pkg_h:
            print(f"  current        {name}"); cur += 1; continue
        bad, why = mount_suspect(pkg_d, inst_d)
        if bad:
            print(f"  SUSPECT-STALE  {name}   {why} - re-confirm via file tools / fresh session"); suspect += 1
        else:
            print(f"  STALE          {name}   installed != package (reinstall to sync)"); stale += 1
    print(f"\naudit: {cur} current, {stale} STALE, {suspect} SUSPECT-STALE, {missing} not-installed (of {len(packages(root))} packaged)")
    if suspect:
        print(f"MOUNT MAY BE STALE: {suspect} skill(s) had a truncated/NUL installed-side read (obs-014/obs-070).")
        print("  -> NOT confirmed stale; verify the installed SKILL.md via the file tools or re-run in a fresh session before queuing a reinstall.")
    if stale:
        print("note: confirm any STALE via the file tools before acting (obs-014 installed-cache mount can read stale).")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["verify", "extract", "package", "audit"])
    ap.add_argument("--root", default=".")
    ap.add_argument("--installed", default=None, help="installed skills cache (auto-detected if omitted)")
    a = ap.parse_args()
    if a.installed is None:
        import glob
        hits = sorted(p for p in glob.glob("/sessions/*/mnt/.claude/skills") if pathlib.Path(p).is_dir())
        a.installed = hits[0] if hits else "/sessions/*/mnt/.claude/skills"
    if a.cmd == "verify":  sys.exit(1 if cmd_verify(a.root) else 0)
    if a.cmd == "extract": cmd_extract(a.root)
    if a.cmd == "package": cmd_package(a.root)
    if a.cmd == "audit":   cmd_audit(a.root, a.installed)
