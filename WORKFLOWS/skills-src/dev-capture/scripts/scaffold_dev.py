#!/usr/bin/env python3
"""dev-capture DEV/ scaffold — creates a project's DEV/ tree with correctly stamped frontmatter.

Deterministic on purpose (mirrors chapter-init's scaffold.py): the DEV/ tree is written from
canonical templates with the right project name, profile, and date every time — never by copying
a sibling project, which is exactly how stale frontmatter ships (the ^obs-005 template-copy trap).

The engine is scale-free; only the spine flexes by --profile:
  short    scenes/ + registry/ + _DEV.md  (taste anchor IS the macro read; no sequences/, no project.md)
  novella  + movements/ (lighter mid-rung)            (no sequences/, no project.md)
  novel    + sequences/ + project.md  (the full tree)            [default]
The engine files (_DEV_MAP, _POETICS, _intake/ + _audit/ + _LEDGER) are present in every profile.

Usage:
  python3 scaffold_dev.py --project <path-to-project-root> [--profile novel] [--dry-run]

The project root is the folder containing CHAPTERS/ and/or REFERENCE/ (DEV/ is their sibling).
Exit codes: 0 ok · 2 gate failure (message on stderr, nothing written).
"""
import argparse, datetime, sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

# template filename -> destination relative path (inside DEV/)
COMMON = {
    "_DEV.md": "_DEV.md",
    "_DEV_MAP.md": "_DEV_MAP.md",
    "_POETICS.md": "_POETICS.md",
    "scenes-README.md": "scenes/README.md",
    "registry-README.md": "registry/README.md",
    "registry-characters-README.md": "registry/characters/README.md",
    "registry-locations-README.md": "registry/locations/README.md",
    "registry-lore-README.md": "registry/lore/README.md",
    "items.md": "registry/items.md",
    "intake-README.md": "_intake/README.md",
    "_LEDGER.md": "_intake/_LEDGER.md",
    "audit-README.md": "_intake/_audit/README.md",
}
PROFILES = {
    "short": dict(COMMON),
    "novella": {**COMMON, "movements-README.md": "movements/README.md"},
    "novel": {**COMMON, "project.md": "project.md", "sequences-README.md": "sequences/README.md"},
}


def die(msg):
    print(f"GATE: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--profile", choices=sorted(PROFILES), default="novel")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    project = Path(args.project).resolve()
    if not project.is_dir():
        die(f"{project} is not a directory.")

    # Project gate: a real per-chapter / referenced project (DEV/ is sibling to these).
    if not (project / "CHAPTERS").is_dir() and not (project / "REFERENCE").is_dir():
        die(f"{project} has neither CHAPTERS/ nor REFERENCE/ — doesn't look like a project root. Ask CRE.")

    # Vault sentinel (^obs-004): walk up for _DIRECTIVES.md with the right frontmatter.
    sentinel_ok = False
    for parent in [project, *project.parents]:
        d = parent / "_DIRECTIVES.md"
        if d.is_file():
            head = d.read_text(encoding="utf-8")[:400]
            sentinel_ok = "type: ai-os-brain" in head and "file: directives" in head
            break
    if not sentinel_ok:
        die("vault sentinel failed — no _DIRECTIVES.md with `type: ai-os-brain` / `file: directives` above the project. Halt and ask which folder is the vault.")

    dev = project / "DEV"
    # Never overwrite: an existing DEV/ halts (repair is a separate, manual conversation).
    if dev.exists():
        die(f"{dev.relative_to(project)}/ already exists — dev-capture scaffold never overwrites or back-fills.")

    project_name = project.name
    today = datetime.date.today().isoformat()
    subs = {"{{PROJECT}}": project_name, "{{DATE}}": today, "{{PROFILE}}": args.profile}

    files = PROFILES[args.profile]
    written = []
    for tpl, rel in files.items():
        src = TEMPLATES / tpl
        if not src.is_file():
            die(f"missing template {tpl} — refusing to write a partial tree.")
        text = src.read_text(encoding="utf-8")
        for k, v in subs.items():
            text = text.replace(k, v)
        if any(tok in text for tok in ("{{PROJECT}}", "{{DATE}}", "{{PROFILE}}")):
            die(f"unsubstituted placeholder left in {tpl} — refusing to write.")
        out = dev / rel
        written.append(str(out.relative_to(project)))
        if not args.dry_run:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")

    verb = "would write" if args.dry_run else "wrote"
    print(f"dev-capture scaffold ({args.profile}): {verb} {len(written)} files under DEV/")
    for w in sorted(written):
        print(f"  {w}")
    print(f"stamped: project: {project_name} · profile: {args.profile} · last_updated: {today}")
    print("next: scene-capture path — drop a cleaned transcript and run dev-capture.")


if __name__ == "__main__":
    main()
