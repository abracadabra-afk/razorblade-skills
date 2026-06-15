#!/usr/bin/env python3
"""book-ingest scaffolder: drop a published chapter's prose into the per-chapter
folder convention at the LANDED stage (status: ingested). Writes prose verbatim;
never reflows. Refuses to overwrite an existing chapter folder.

Usage:
  scaffold_ingest.py --project-root <PROJECT_DIR> --n <N> --source <CHAPTER_MD> [--title TITLE]

PROJECT_DIR is e.g. ".../WRITING/PROJECTS/GHOST RIVER". Source is the published
prose .md (copied byte-for-byte after a frontmatter block). On the first chapter
it also creates REFERENCE/ scaffolds + intensity_config.json + project README.
"""
import argparse, os, sys, datetime, json, re

def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(text)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--n", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--source-label", default="published First-Edition prose")
    a = ap.parse_args()
    today = datetime.date.today().isoformat()
    proj = os.path.basename(a.project_root.rstrip("/"))
    folder = f"CHAPTER {a.n}" + (f" - {a.title}" if a.title else "")
    chap = os.path.join(a.project_root, "CHAPTERS", folder)
    if os.path.exists(os.path.join(chap, "draft.md")):
        print(f"REFUSE: {chap}/draft.md already exists — not overwriting."); sys.exit(2)
    if not os.path.isfile(a.source):
        print(f"ERROR: source not found: {a.source}"); sys.exit(3)
    prose = open(a.source, encoding="utf-8").read()

    import yaml as _yaml  # emit frontmatter via safe_dump so values with ': ' / backticks stay valid YAML (^obs-026)
    _front = {
        "type": "chapter-draft", "chapter": folder, "project": proj, "status": "ingested",
        "source": f"{a.source_label}. Ingested verbatim from \"{a.source}\".",
        "ingest_note": ("No dictation lineage. Published book entering the per-chapter pipeline at the LANDED "
                        "stage; dictation/slate/revisions are N/A, brief.md/envelope.md are N/A stubs. canon-sync "
                        "and storyline-sync treat status: ingested like a landed draft. Provenance tag for derived "
                        f"canon = (CH{a.n} ingested)."),
        "last_updated": today,
    }
    fm = "---\n" + _yaml.safe_dump(_front, sort_keys=False, allow_unicode=True, width=100000) + "---\n\n"
    body = prose if prose.endswith("\n") else prose + "\n"
    w(os.path.join(chap, "draft.md"), fm + body)

    na = lambda kind, body: f"---\ntype: {kind}\nchapter: {folder}\nproject: {proj}\nstatus: not-applicable\nlast_updated: {today}\n---\n\n{body}\n"
    w(os.path.join(chap, "brief.md"), na("chapter-brief",
        "# Brief — "+folder+"\n\n> **N/A — ingested published work.** Forward intent (job/beats/setups/payoffs) is authored before drafting; a published book has none, and reverse-deriving it would be AI-inferred intent. Author by hand only to enable spec-check on this chapter."))
    w(os.path.join(chap, "envelope.md"), na("chapter-envelope",
        "# Envelope — "+folder+"\n\n> **N/A — ingested published work.** The perceptual envelope is the Transcoder's dictation input; this book was not dictated. Stub for structural parity."))
    for d, label in [("dictation","No dictation lineage."),("slate","No Transcoder slates."),("revisions","No register-pass revisions.")]:
        w(os.path.join(chap, d, "README.md"), f"# {d}/ — N/A (ingested published book)\n\n{label} The published prose is the draft (`status: ingested`).\n")
    w(os.path.join(chap, "_status.md"),
        f"---\ntype: chapter-meta\nchapter: {folder}\nproject: {proj}\nfile: status\nlast_updated: {today}\n---\n\n# Status — {folder}\n\n> Ingested published chapter; enters at landed/ingested.\n\n| Stage | State | Date |\n|---|---|---|\n| Ingest (draft.md) | done | {today} |\n| canon-sync | pending | — |\n| storyline-sync | pending | — |\n")
    w(os.path.join(chap, "changelog.md"),
        f"---\ntype: chapter-meta\nchapter: {folder}\nproject: {proj}\nfile: changelog\nlast_updated: {today}\n---\n\n# Changelog — {folder}\n\n## {today} — Ingest\n- Scaffolded (ingested-published variant); loaded published prose into draft.md verbatim (status: ingested).\n")
    w(os.path.join(chap, "notes.md"), f"---\ntype: chapter-meta\nchapter: {folder}\nproject: {proj}\nfile: notes\nlast_updated: {today}\n---\n\n# Notes — {folder}\n")
    w(os.path.join(chap, "open-loops.md"), f"---\ntype: chapter-meta\nchapter: {folder}\nproject: {proj}\nfile: open-loops\nlast_updated: {today}\n---\n\n# Open Loops — {folder}\n\n## Deferred for CRE\n- _(none yet)_\n")
    w(os.path.join(chap, "continuity.md"), f"---\ntype: chapter-meta\nchapter: {folder}\nproject: {proj}\nfile: continuity\nlast_updated: {today}\n---\n\n# Continuity — {folder}\n\n> End-state filled by canon-sync from the landed draft.\n\n## Entities / objects in play\n## Physical state\n## Knowledge state\n## Time / place\n## Conflicts gated for CRE\n")

    # ---- first-chapter REFERENCE scaffolds ----
    ref = os.path.join(a.project_root, "REFERENCE")
    if not os.path.exists(os.path.join(ref, "bible.md")):
        w(os.path.join(ref, "bible.md"), f"---\ntype: project-state\nproject: {proj}\nfile: bible\nmaintained_by: canon-sync\nlast_updated: {today}\n---\n\n# Bible — {proj}\n\n> Derived + curated. canon-sync adds facts tagged `(CH<N> ingested)`.\n\n## Characters\n## Places\n## Objects\n## Lore & rules / terms\n")
        w(os.path.join(ref, "threads.md"), f"---\ntype: project-state\nproject: {proj}\nfile: threads\nmaintained_by: canon-sync\nspec_material: true\nlast_updated: {today}\n---\n\n# Threads — {proj}\n\n> Open promises. canon-sync adds `(CH<N> ingested)` thread events. blind-read must never load this file.\n\n## Open\n\n## Settled\n")
        w(os.path.join(ref, "story-so-far.md"), f"---\ntype: project-state\nproject: {proj}\nfile: story-so-far\nmaintained_by: canon-sync\nlast_updated: {today}\n---\n\n# Story So Far — {proj}\n\n<!-- canon-sync: sections in reading order. -->\n")
        cfg = {"_note": f"{proj} — uncalibrated; inherits engine project-agnostic DEFAULTS. Recalibrate once several chapters are scored.",
               "weights":{"D1":2,"D2":2,"D3":1,"D4":2,"D5":1,"D6":1},"band_edges":[30.5,55.5,75.5],
               "band_names":["REST","BUILD","HIGH","PEAK"],"seam_distance":4.0,"fragment_max_words":4,
               "d5_bins":[[2.0,1],[4.5,2]],"d6_bins":[[0.1,1],[0.3,2]],"d6_long_zero":[0.03,16.0],
               "somatic_extra":[],"dread_cap":2,"dread_lift_bands":1,"dread_floor":{},"dialogue_dominated_frac":0.6}
        w(os.path.join(ref, "intensity_config.json"), json.dumps(cfg, indent=2))
    if not os.path.exists(os.path.join(a.project_root, "README.md")):
        w(os.path.join(a.project_root, "README.md"),
          f"---\ntype: project-root\nproject: {proj}\nconvention: per-chapter folder (ingested-published variant)\nlast_updated: {today}\n---\n\n# {proj} — project root\n\n> **Ingested published book.** Each chapter's draft.md holds the published prose verbatim (`status: ingested`); dictation/slate/revisions + brief/envelope are N/A. REFERENCE + StoryLine are derived by canon-sync / storyline-sync. Provenance = `(CH<N> ingested)`.\n\n## Ingest status\n\n| Chapter | Scaffolded | canon-sync | storyline-sync |\n|---|---|---|---|\n")

    nwords = len(re.findall(r"\w+", prose))
    print(f"OK: scaffolded {chap}  (draft words: {nwords})")

if __name__ == "__main__":
    main()
