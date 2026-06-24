#!/usr/bin/env python3
"""dev-capture-audit — deterministic capture-integrity checker for a project's DEV/ tree.

Read-only. Reports a severity-ranked punch list (ERROR / WARN / INFO) of structural
defects the dev-capture mechanism can leave behind — duplicate poetics anchors, broken
graduation-loop parity (_POETICS <-> _DEV_MAP), a routed transcript left in _intake/, a
missing audit floor, placeholder leakage, invalid frontmatter, missing boundary tags,
dangling DEV wikilinks, thin stubs. It NEVER edits the tree; fixes are gated and manual
(the skill-audit philosophy).

This is the DETERMINISTIC layer only. Judgment checks (preserve-the-kind, taste-drift,
routing sanity) are an LLM pass run by the skill, not this script.

Usage:
  python3 audit_dev.py --project <path-to-project-root> [--json] [--strict]

--project is the project root (the folder with CHAPTERS/ and/or REFERENCE/, DEV/ a
sibling). Exit codes: 0 clean · 1 ERROR findings (or any WARN under --strict) · 2 gate
failure (sentinel / no DEV tree; message on stderr).

Freshness: this reads the filesystem it is given. On a sync-lagged vault (e.g. Dropbox)
the disk view can trail the cloud-latest, so ensure the tree is synced — or cross-check
the flagged anchors via the file tools — before trusting anchor/graduation findings
(^obs-122).
"""
import argparse, json, re, sys
from pathlib import Path

THIN_CHARS = 400  # entry body shorter than this => possible thin stub
ALLOWED_INTAKE_FILES = {"README.md", "_LEDGER.md"}
BOUNDARY_VALUES = {"cued", "inferred", "per-entry"}


def die(msg):
    print(f"GATE: {msg}", file=sys.stderr)
    sys.exit(2)


def split_frontmatter(text):
    """Return (frontmatter_dict, body). Minimal key: value parser (no nested YAML)."""
    fm = {}
    body = text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if m:
        block, body = m.group(1), m.group(2)
        for line in block.splitlines():
            s = line.strip()
            if not s or s.startswith("#") or ":" not in line:
                continue
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body


def parse_list(val):
    """Parse a frontmatter inline list like '[a, b, c]' -> ['a','b','c']."""
    val = val.strip()
    if val.startswith("[") and val.endswith("]"):
        val = val[1:-1]
    return [x.strip().strip("'\"") for x in val.split(",") if x.strip()]


def classify(dev, p):
    rel = p.relative_to(dev).as_posix()
    if p.name == "README.md":
        return "skip"
    if rel in ("_DEV.md", "project.md"):
        return "derived"
    if rel == "registry/items.md":
        return "bucket"
    if rel.startswith(("registry/", "sequences/", "scenes/")):
        return "standard"
    if rel in ("_POETICS.md", "_DEV_MAP.md"):
        return "engine"
    if rel.startswith("_intake/_audit/"):
        return "floor"
    if rel.startswith("_intake/"):
        return "intake"
    return "other"


def main():
    ap = argparse.ArgumentParser(description="Deterministic capture-integrity audit of a DEV/ tree.")
    ap.add_argument("--project", required=True, help="project root (folder with CHAPTERS/ or REFERENCE/, DEV/ sibling)")
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    ap.add_argument("--strict", action="store_true", help="exit 1 on WARN as well as ERROR")
    args = ap.parse_args()

    project = Path(args.project).resolve()
    if not project.is_dir():
        die(f"{project} is not a directory.")
    if not (project / "CHAPTERS").is_dir() and not (project / "REFERENCE").is_dir():
        die(f"{project} has neither CHAPTERS/ nor REFERENCE/ — doesn't look like a project root.")

    # Vault sentinel (^obs-004): walk up for _DIRECTIVES.md with the right frontmatter.
    sentinel_ok = False
    for parent in [project, *project.parents]:
        d = parent / "_DIRECTIVES.md"
        if d.is_file():
            head = d.read_text(encoding="utf-8", errors="replace")[:400]
            sentinel_ok = "type: ai-os-brain" in head and "file: directives" in head
            break
    if not sentinel_ok:
        die("vault sentinel failed — no _DIRECTIVES.md with `type: ai-os-brain` / `file: directives` above the project.")

    dev = project / "DEV"
    if not dev.is_dir():
        die(f"{project.name}/DEV/ does not exist — this skill audits, it does not scaffold. Run dev-capture's scaffolder first.")

    findings = []  # (severity, relpath, message)

    def add(sev, path, msg):
        rel = path.relative_to(dev).as_posix() if isinstance(path, Path) else path
        findings.append((sev, rel, msg))

    # Gather all markdown, classified.
    all_md = [p for p in dev.rglob("*.md")]
    by_class = {}
    for p in all_md:
        by_class.setdefault(classify(dev, p), []).append(p)
    standard = by_class.get("standard", [])
    derived = by_class.get("derived", [])
    bucket = by_class.get("bucket", [])
    content = standard + derived + bucket  # entries that USE wikilinks (engine files only discuss them)

    # Read text + frontmatter once.
    texts, fms = {}, {}
    for p in all_md:
        t = p.read_text(encoding="utf-8", errors="replace")
        texts[p] = t
        fms[p], _ = split_frontmatter(t)

    tree_project = (fms.get(dev / "_DEV.md", {}) or {}).get("project") \
        or (fms.get(dev / "_DEV_MAP.md", {}) or {}).get("project")

    # -- 1. Anchor uniqueness (^poe in _POETICS) --
    poe_path = dev / "_POETICS.md"
    poe_defs = {}
    if poe_path.is_file():
        for n in re.findall(r"(?m)^###\s+\^poe-(\d+)\b", texts[poe_path]):
            poe_defs[n] = poe_defs.get(n, 0) + 1
        for n, c in sorted(poe_defs.items(), key=lambda x: int(x[0])):
            if c > 1:
                add("ERROR", poe_path, f"duplicate poetics anchor ^poe-{n} defined {c}x — renumber the unreferenced one (scan whole file for max+1).")
    else:
        add("WARN", "_POETICS.md", "missing _POETICS.md.")

    # -- 2. Graduation parity (_POETICS promoted <-> _DEV_MAP binding) --
    promoted = set()
    if poe_path.is_file():
        for m in re.finditer(r"(?ms)^###\s+\^poe-(\d+)\b.*?(?=^###\s+\^poe-|\Z)", texts[poe_path]):
            if "promoted → _DEV_MAP" in m.group(0) or re.search(r"\*\*Status:\*\*\s*promoted", m.group(0)):
                promoted.add(m.group(1))
    map_path = dev / "_DEV_MAP.md"
    bound = set()
    if map_path.is_file():
        for n in re.findall(r"(?m)^-\s*\^poe-(\d+)\b", texts[map_path]):
            bound.add(n)
    else:
        add("WARN", "_DEV_MAP.md", "missing _DEV_MAP.md.")
    for n in sorted(promoted - bound, key=int):
        add("ERROR", "_POETICS.md", f"^poe-{n} is 'promoted → _DEV_MAP' but has NO binding line in _DEV_MAP § Graduated patterns.")
    for n in sorted(bound - promoted, key=int):
        add("ERROR", "_DEV_MAP.md", f"_DEV_MAP binds ^poe-{n} but its _POETICS entry is not marked 'promoted → _DEV_MAP'.")

    # -- 3. Intake invariant --
    intake = dev / "_intake"
    if intake.is_dir():
        for child in sorted(intake.iterdir()):
            if child.is_dir():
                if child.name != "_audit":
                    add("WARN", child, f"unexpected directory in _intake/ — expected only _audit/.")
            else:
                if child.name in ALLOWED_INTAKE_FILES or child.name.startswith("HOLD-"):
                    continue
                add("ERROR", child, "stray file in _intake/ — a routed transcript was not swept+removed (intake holds only README, _LEDGER, _audit/, HOLD-*).")
    else:
        add("WARN", "_intake/", "missing _intake/ folder.")

    # -- 4. Floor pointers (standard entries) --
    audit_dir = dev / "_intake" / "_audit"
    floor_names = {p.name for p in audit_dir.glob("*.md")} if audit_dir.is_dir() else set()
    for p in standard:
        links = re.findall(r"\[\[_intake/_audit/([^\]\|#]+)", texts[p])
        if not links:
            add("INFO", p, "no _audit/ floor pointer in the entry footer.")
            continue
        for slug in links:
            fname = slug.split("/")[-1].strip() + ".md"
            if fname not in floor_names:
                add("ERROR", p, f"floor pointer → _audit/{fname} but that audit file does not exist.")

    # -- 5. Frontmatter / DIR-004 (+ 6 placeholder, + 9 project) --
    for p in all_md:
        if p.name == "README.md":
            continue
        if "{{" in texts[p]:
            add("ERROR", p, "unsubstituted placeholder ({{…}}) survived routing.")
        cl = classify(dev, p)
        # Floors are raw verbatim transcripts — not entries — so they are NOT required to carry
        # frontmatter (early floors are plain prose). Entries + engine files are.
        if cl in ("standard", "derived", "bucket", "engine"):
            if not fms[p]:
                add("ERROR", p, "missing or unparseable frontmatter (DIR-004).")
                continue
            if cl in ("standard", "derived", "bucket"):
                for key in ("type", "project"):
                    if key not in fms[p]:
                        add("ERROR", p, f"frontmatter missing required key '{key}'.")
                if tree_project and fms[p].get("project") and fms[p]["project"] != tree_project:
                    add("WARN", p, f"project '{fms[p]['project']}' != tree project '{tree_project}'.")

    # -- 7. Boundary tags --
    for p in standard:
        b = fms[p].get("boundary")
        if not b:
            add("WARN", p, "no boundary tag (expected cued|inferred).")
        elif b not in BOUNDARY_VALUES:
            add("WARN", p, f"boundary '{b}' not one of cued|inferred|per-entry.")
    for p in bucket:
        if not fms[p].get("boundary"):
            add("WARN", p, "bucket file has no boundary tag (expected per-entry).")

    # -- 8. Ledger form --
    led = dev / "_intake" / "_LEDGER.md"
    if led.is_file():
        if "surface_trigger" not in fms[led]:
            add("WARN", led, "ledger frontmatter missing surface_trigger.")
        for line in texts[led].splitlines():
            if re.match(r"^\s*-\s*\[[ xX]\]", line) and "[source:" not in line:
                add("WARN", led, f"collision line missing [source:…] pointer: {line.strip()[:70]}")

    # -- 10. Dangling wikilinks (DEV-scoped) --
    names = {p.stem.lower() for p in dev.rglob("*.md") if p.name != "README.md"}
    headings = set()
    aliases = set()
    for p in all_md:
        for h in re.findall(r"(?m)^###\s+(.+?)\s*$", texts[p]):
            headings.add(h.strip().lower())
        if "aliases" in fms.get(p, {}):
            for a in parse_list(fms[p]["aliases"]):
                aliases.add(a.lower())
    resolvable = names | headings | aliases
    for p in content:
        for raw in re.findall(r"\[\[([^\]]+)\]\]", texts[p]):
            tgt = raw.lstrip("!").split("|")[0].split("#")[0].strip()
            if not tgt or tgt.startswith("_intake/_audit/") or "..." in tgt:
                continue
            base = tgt.split("/")[-1].strip().lower()
            if base and re.search(r"[a-z0-9]", base) and base not in resolvable:
                add("WARN", p, f"dangling wikilink [[{raw}]] — no DEV file/heading/alias '{base}' (or an intentional future-entry candidate).")

    # -- 11. Thin stubs + 12. Provenance footer (standard entries) --
    for p in standard:
        _, body = split_frontmatter(texts[p])
        if len(body.strip()) < THIN_CHARS:
            add("WARN", p, f"thin entry ({len(body.strip())} chars) — possible empty/fabricated stub or missing taste.")
        if "Routed (" not in texts[p] and "*Routed" not in texts[p]:
            add("INFO", p, "no 'Routed (…)' provenance footer.")

    # ---- Report ----
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda f: (order[f[0]], f[1]))
    counts = {s: sum(1 for f in findings if f[0] == s) for s in ("ERROR", "WARN", "INFO")}

    if args.json:
        print(json.dumps({
            "project": project.name,
            "counts": counts,
            "findings": [{"severity": s, "path": pth, "message": m} for s, pth, m in findings],
        }, indent=2))
    else:
        print(f"dev-capture-audit — {project.name}/DEV/")
        print(f"  {counts['ERROR']} ERROR · {counts['WARN']} WARN · {counts['INFO']} INFO\n")
        if not findings:
            print("  clean — no findings.")
        for s, pth, m in findings:
            print(f"  [{s:<5}] {pth}\n           {m}")

    errors = counts["ERROR"]
    warns = counts["WARN"]
    sys.exit(1 if (errors or (args.strict and warns)) else 0)


if __name__ == "__main__":
    main()
