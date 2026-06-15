#!/usr/bin/env python3
"""chapter-init scaffold — creates a per-chapter folder with correctly stamped frontmatter.

Deterministic on purpose: hand-copying a sibling chapter's files is exactly how stale
`chapter:` frontmatter ships (the ^obs-005 template-copy trap). This script writes every
file from canonical templates with the right chapter name and date, every time.

Usage:
  python3 scaffold.py --project <path-to-project-root> --number 4 --title "THE HERMIT'S DUE" [--allow-gap] [--dry-run]

The project root is the folder containing CHAPTERS/ and REFERENCE/.
Exit codes: 0 ok · 2 gate failure (message on stderr, nothing written).
"""
import argparse, datetime, re, sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

FILES = {  # template filename -> destination relative path
    "brief.md": "brief.md",
    "envelope.md": "envelope.md",
    "changelog.md": "changelog.md",
    "draft.md": "draft.md",
    "open-loops.md": "open-loops.md",
    "continuity.md": "continuity.md",
    "notes.md": "notes.md",
    "_status.md": "_status.md",
    "dictation-README.md": "dictation/README.md",
    "slate-README.md": "slate/README.md",
    "revisions-README.md": "revisions/README.md",
}

def die(msg):
    print(f"GATE: {msg}", file=sys.stderr)
    sys.exit(2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--number", required=True, type=int)
    ap.add_argument("--title", required=True)
    ap.add_argument("--allow-gap", action="store_true",
                    help="proceed even if --number is not (highest existing chapter + 1)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    project = Path(args.project).resolve()
    chapters = project / "CHAPTERS"
    if not chapters.is_dir():
        die(f"{project} has no CHAPTERS/ — per-chapter convention not adopted here. Ask the author.")

    # Vault sentinel (^obs-004): walk up looking for _DIRECTIVES.md with the right frontmatter.
    sentinel_ok = False
    for parent in [project, *project.parents]:
        d = parent / "_DIRECTIVES.md"
        if d.is_file():
            head = d.read_text(encoding="utf-8")[:400]
            if "type: ai-os-brain" in head and "file: directives" in head:
                sentinel_ok = True
            break
    if not sentinel_ok:
        die("vault sentinel failed — no _DIRECTIVES.md with `type: ai-os-brain` / `file: directives` above the project. Halt and ask which folder is the vault.")

    title = args.title.upper().strip()
    chapter = f"CHAPTER {args.number} - {title}"
    dest = chapters / chapter

    # Exists gate: never overwrite, including a same-number folder with a different title.
    clash = [p.name for p in chapters.iterdir()
             if p.is_dir() and re.match(rf"CHAPTER {args.number}\b", p.name)]
    if clash:
        die(f"chapter {args.number} already exists: {clash[0]} — chapter-init never overwrites or back-fills.")

    # Sequence gate.
    nums = [int(m.group(1)) for p in chapters.iterdir() if p.is_dir()
            and (m := re.match(r"CHAPTER (\d+)\b", p.name))]
    expected = (max(nums) + 1) if nums else 1
    if args.number != expected and not args.allow_gap:
        die(f"expected next chapter {expected}, got {args.number}. Confirm with the author, then re-run with --allow-gap.")

    today = datetime.date.today().isoformat()
    seed_marker = "<!-- {{THREAD-SEED}}: chapter-init lists open threads from REFERENCE/threads.md here, each tagged <<PROPOSED — CRE to rule>>. -->"
    subs = {
        "{{CHAPTER}}": chapter,
        "{{DATE}}": today,
        "{{THREAD_SEED}}": seed_marker,
        "{{SEED_NOTE}}": "",  # filled by the skill after the thread harvest
    }

    written = []
    for tpl, rel in FILES.items():
        text = (TEMPLATES / tpl).read_text(encoding="utf-8")
        for k, v in subs.items():
            text = text.replace(k, v)
        if any(tok in text for tok in ("{{CHAPTER}}", "{{DATE}}")):
            die(f"unsubstituted placeholder left in {tpl} — refusing to write.")
        out = dest / rel
        written.append(str(out.relative_to(project)))
        if not args.dry_run:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")

    verb = "would write" if args.dry_run else "wrote"
    print(f"chapter-init: {verb} {len(written)} files under CHAPTERS/{chapter}/")
    for w in written:
        print(f"  {w}")
    print(f"stamped: chapter: {chapter} · last_updated: {today}")
    print("next: harvest REFERENCE/threads.md into brief.md §Payoffs (skill step), then S2 with the author.")

if __name__ == "__main__":
    main()
