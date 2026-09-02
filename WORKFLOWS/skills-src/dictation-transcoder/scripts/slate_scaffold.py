#!/usr/bin/env python3
"""slate_scaffold.py — the transcoder's mechanical shell (references/slate-contract.md).

Owns everything about a slate run that is bookkeeping, so the model only writes
prose and ledger content:

  new     --chapter DIR [--dictation FILE] [--tense past|present] [--canon WORKFLOWS/transcoder.md]
          sentinel · pick the newest un-slated dictation · read segments from envelope.md
          · allocate slate/YYYY-MM-DD-NN/ · write the four stub files with one serialized
          frontmatter block · print the changelog stubs · WARN if SKILL.md and canon disagree on version
  derive  --chapter DIR --parent NN|PATH
          new run copied from the parent (all four files), derived_from/supersedes stamped,
          status: derived, generated re-stamped
  check   RUNDIR [--against PARENT]
          4/4 files · frontmatter parses with the ruled key set · envelope_segments is a list
          · required ledger sections · <<marker>> census · retired keys · slate-local clean-ledger
          · edited-after-generated · optional paragraph diff vs parent
  --selftest

Exit: 0 clean (INFO/WARN) · 1 ERROR findings · 2 gate failure (sentinel, bad path).
stdlib only (DIR-007). Console forced to UTF-8 (Windows cp1252 crashes on the vault's dashes).
Never writes outside <chapter>/slate/. Never writes prose.
"""
import argparse
import datetime as _dt
import os
import re
import shutil
import sys
import tempfile

FILES = ("clean-draft.md", "cut-log.md", "synthesis-ledger.md", "leaves-left.md")
REQUIRED_KEYS = ("source_dictation", "envelope_segments", "generated", "transcoder_version", "tense", "status")
OPTIONAL_KEYS = ("supersedes", "derived_from")
RETIRED_KEYS = ("segments", "type", "chapter", "file", "run", "word_count", "coverage",
                "register", "floor", "generated_by", "transcoder", "last_updated")
STATUSES = ("floor-draft", "gate-pending", "gated", "derived")
LEDGER_SECTIONS = [
    "## Mic metadata", "## Reconciler restorations", "## Ruled lines — preserved",
    "## Clusters collapsed", "## Floor ledger", "## Heat bank", "## Optioned",
    "## Register repair", "## Contamination check", "## Garbles",
    "## Developmental-seam flags", "## Scene map", "## Continuity touched",
]
MARKER_RE = re.compile(r"<<(GARBLE-UNRESOLVED|OPTIONED-\d+|REGISTER-AMBIGUOUS|AUTHOR-GAP)[^>]*>>")
SEGMENT_RE = re.compile(r"^##\s+Segment\s+\d+\s*[—\-–:]\s*(\S+)", re.M)
VERSION_RE = re.compile(r"\bv(\d+(?:\.\d+)*)\b")
EDIT_WINDOW_MIN = 180  # a run's own writing session; edits after this are "edited in place"


def utf8_console():
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            try:
                s.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


class Findings:
    def __init__(self):
        self.items = []

    def add(self, sev, check, msg):
        self.items.append((sev, check, msg))

    def worst(self):
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        return min((i[0] for i in self.items), key=lambda s: order[s], default=None)

    def render(self, title):
        out = [title]
        for sev in ("ERROR", "WARN", "INFO"):
            rows = [i for i in self.items if i[0] == sev]
            if rows:
                out.append("  %s (%d)" % (sev, len(rows)))
                for _, chk, msg in rows:
                    out.append("    %-14s %s" % (chk, msg))
        return "\n".join(out)


def read(p):
    with open(p, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


# ---------- frontmatter: fixed-schema emitter + parser (DIR-004 parse gate) ----------

def yaml_scalar(v):
    s = str(v)
    if s == "" or re.search(r"[:#\[\]{},&*!|>'\"%@`]|^\s|\s$|^-|^\d{4}-\d{2}-\d{2}", s):
        return "'" + s.replace("'", "''") + "'"
    return s


def emit_frontmatter(d):
    lines = ["---"]
    for k in REQUIRED_KEYS + OPTIONAL_KEYS:
        if k not in d:
            continue
        v = d[k]
        if k == "envelope_segments":
            lines.append("%s: [%s]" % (k, ", ".join(yaml_scalar(x) for x in v)))
        else:
            lines.append("%s: %s" % (k, yaml_scalar(v)))
    lines.append("---")
    return "\n".join(lines) + "\n"


def parse_frontmatter(text):
    """Returns (dict, body, error). Strict enough to gate our own emitter and the
    hand-written history; uses PyYAML when present for the real parse."""
    if not text.startswith("---"):
        return None, text, "no opening fence"
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text, "no closing fence"
    block = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1:])
    try:
        import yaml  # type: ignore
        try:
            d = yaml.safe_load(block) or {}
            if not isinstance(d, dict):
                return None, body, "frontmatter is not a mapping"
            return d, body, None
        except Exception as e:  # pragma: no cover
            return None, body, "yaml: %s" % e
    except ImportError:
        pass
    d, key = {}, None
    for raw in block.split("\n"):
        if not raw.strip():
            continue
        if raw[0] in " \t" and key:
            d[key] = (str(d[key]) + " " + raw.strip()).strip()
            continue
        m = re.match(r"^([A-Za-z_][\w\-]*):\s*(.*)$", raw)
        if not m:
            return None, body, "unparseable line: %r" % raw[:60]
        key, val = m.group(1), m.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            d[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()] if inner else []
        elif len(val) >= 2 and val[0] == val[-1] and val[0] in "'\"":
            d[key] = val[1:-1].replace("''", "'")
        else:
            d[key] = val
    return d, body, None


# ---------- discovery ----------

def find_vault_root(start):
    p = os.path.abspath(start)
    for _ in range(12):
        if os.path.isfile(os.path.join(p, "_DIRECTIVES.md")):
            return p
        parent = os.path.dirname(p)
        if parent == p:
            break
        p = parent
    return None


def sentinel(chapter, f):
    root = find_vault_root(chapter)
    if not root:
        f.add("ERROR", "SENTINEL", "no _DIRECTIVES.md above %s — which folder is the vault?" % chapter)
        return None
    fm, _, err = parse_frontmatter(read(os.path.join(root, "_DIRECTIVES.md")))
    if err or not fm or fm.get("type") != "ai-os-brain" or fm.get("file") != "directives":
        f.add("ERROR", "SENTINEL", "_DIRECTIVES.md at %s fails the ai-os-brain/directives check" % root)
        return None
    return root


def existing_runs(chapter):
    sd = os.path.join(chapter, "slate")
    if not os.path.isdir(sd):
        return []
    return sorted(d for d in os.listdir(sd)
                  if re.match(r"^\d{4}-\d{2}-\d{2}-\d{2}$", d) and os.path.isdir(os.path.join(sd, d)))


def allocate_run(chapter, today=None):
    today = today or _dt.date.today().isoformat()
    taken = {r for r in existing_runs(chapter) if r.startswith(today)}
    for n in range(1, 100):
        cand = "%s-%02d" % (today, n)
        if cand not in taken:
            return cand
    raise RuntimeError("99 runs today — stop.")


def slated_dictations(chapter):
    out = set()
    for r in existing_runs(chapter):
        p = os.path.join(chapter, "slate", r, "clean-draft.md")
        if os.path.isfile(p):
            fm, _, _ = parse_frontmatter(read(p))
            if fm and fm.get("source_dictation"):
                out.add(os.path.basename(str(fm["source_dictation"])))
    return out


def pick_dictation(chapter, f):
    dd = os.path.join(chapter, "dictation")
    if not os.path.isdir(dd):
        f.add("ERROR", "DICTATION", "no dictation/ folder")
        return None
    done = slated_dictations(chapter)
    cands = [fn for fn in os.listdir(dd)
             if fn.lower().endswith((".md", ".txt")) and fn.lower() != "readme.md"
             and os.path.isfile(os.path.join(dd, fn))]
    fresh = [fn for fn in cands if fn not in done]
    if not fresh:
        f.add("ERROR", "DICTATION", "no un-slated dictation in dictation/ (%d file(s), all have runs)" % len(cands))
        return None
    fresh.sort(key=lambda fn: os.path.getmtime(os.path.join(dd, fn)), reverse=True)
    if len(fresh) > 1:
        f.add("WARN", "DICTATION", "%d un-slated dictations; picked newest by mtime: %s (others: %s)"
              % (len(fresh), fresh[0], ", ".join(fresh[1:])))
    return fresh[0]


def read_segments(chapter, f):
    p = os.path.join(chapter, "envelope.md")
    if not os.path.isfile(p):
        f.add("ERROR", "ENVELOPE", "envelope.md missing — halt and ask (or standalone-mode derivation, model's call)")
        return None
    text = read(p)
    fm, body, _ = parse_frontmatter(text)
    segs = SEGMENT_RE.findall(body if fm is not None else text)
    if not segs:
        f.add("ERROR", "ENVELOPE", "envelope.md has no '## Segment N — slug' headings — unfilled envelope")
        return None
    return [s.strip("*` ") for s in segs]


def canon_version(canon_path):
    if not canon_path or not os.path.isfile(canon_path):
        return None
    for ln in read(canon_path).split("\n")[:40]:
        if ln.startswith("# "):
            m = VERSION_RE.search(ln)
            if m:
                return "v" + m.group(1)
    return None


def skill_version(skill_md):
    if not skill_md or not os.path.isfile(skill_md):
        return None
    for ln in read(skill_md).split("\n")[:20]:
        if ln.startswith("# "):
            m = VERSION_RE.search(ln)
            if m:
                return "v" + m.group(1)
    return None


# ---------- stubs ----------

def stub_files(chapter_name, run, fm):
    head = emit_frontmatter(fm)
    segs = fm["envelope_segments"]
    clean = head + "\n# Floor draft — %s (slate %s)\n\n" % (chapter_name, run)
    cut = head + "\n# Cut log — slate %s\n\nReasons: unperceived · too-fine · narrator-injection · modifier · frame · mechanical\n\n" % run
    ledger = head + "\n# Synthesis ledger — slate %s\n\n" % run
    for sec in LEDGER_SECTIONS:
        ledger += sec + "\n\n_nothing recorded_\n\n"
    leaves = head + "\n# Leaves left — slate %s\n\nVerdicts: incidental · dialogue · floored · optioned · repaired · dilution\n\n" % run
    for s in segs:
        leaves += "## Segment — %s\n\n_none listed — re-read before trusting_\n\n" % s
    return {"clean-draft.md": clean, "cut-log.md": cut, "synthesis-ledger.md": ledger, "leaves-left.md": leaves}


def changelog_stubs(chapter_name, run, fm):
    segs = "+".join(fm["envelope_segments"])
    date = run[:10]
    vault = ("## %s — [fiction] transcoder run on %s\n"
             "**Ran:** Transcoder %s on %s · segments: %s · dictation: %s\n"
             "**Shipped:** slate/%s/ (4 files) · N floor normalizations · N heat-bank entries · N optioned · N garbles open\n"
             "**Gate:** open: N markers, N seam flags\n"
             "**Open loops:** <pointers into the synthesis ledger>\n"
             % (date, chapter_name, fm["transcoder_version"], chapter_name, segs, fm["source_dictation"], run))
    chap = ("## %s — transcoder %s — slate run %s\n"
            "**Ran:** %s\n**Slate run:** `slate/%s/`\n**Open loops:** <pointers>\n**Notes:**\n"
            % (date, fm["transcoder_version"], run[-2:], segs, run))
    return vault, chap


# ---------- commands ----------

def cmd_new(a, f):
    chapter = os.path.abspath(a.chapter)
    if not os.path.isdir(chapter):
        f.add("ERROR", "CHAPTER", "not a folder: %s" % chapter)
        return None
    root = sentinel(chapter, f)
    if not root:
        return None
    segs = read_segments(chapter, f)
    dictation = a.dictation or pick_dictation(chapter, f)
    if segs is None or dictation is None:
        return None
    canon = a.canon or os.path.join(root, "WORKFLOWS", "transcoder.md")
    cver = canon_version(canon)
    sver = skill_version(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL.md"))
    version = cver or sver or "v?"
    if cver and sver and cver != sver:
        f.add("WARN", "VERSION", "canon %s is %s, this skill's SKILL.md is %s — run from the canon doc; announce the gap (DIR-009)"
              % (os.path.basename(canon), cver, sver))
    if not cver:
        f.add("WARN", "VERSION", "could not read a version from %s; stamped %s" % (canon, version))
    run = allocate_run(chapter, a.date)
    fm = {
        "source_dictation": "dictation/" + dictation,
        "envelope_segments": segs,
        "generated": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "transcoder_version": version,
        "tense": a.tense or "past",
        "status": "floor-draft",
    }
    rundir = os.path.join(chapter, "slate", run)
    if os.path.exists(rundir):
        f.add("ERROR", "ALLOC", "run dir already exists: %s" % rundir)
        return None
    files = stub_files(os.path.basename(chapter), run, fm)
    for name, text in files.items():
        write(os.path.join(rundir, name), text)
    # parse gate on what we just wrote
    for name in FILES:
        d, _, err = parse_frontmatter(read(os.path.join(rundir, name)))
        if err or not d or not isinstance(d.get("envelope_segments"), list):
            f.add("ERROR", "PARSE-GATE", "%s frontmatter failed to parse back: %s" % (name, err))
    f.add("INFO", "NEW", "slate/%s written (4 stubs) · dictation %s · %d segment(s) · %s" % (run, dictation, len(segs), version))
    v, c = changelog_stubs(os.path.basename(chapter), run, fm)
    return {"rundir": rundir, "run": run, "vault_stub": v, "chapter_stub": c}


def resolve_parent(chapter, parent):
    if os.path.isdir(parent):
        return os.path.abspath(parent)
    runs = existing_runs(chapter)
    if re.match(r"^\d{2}$", parent):
        hits = [r for r in runs if r.endswith("-" + parent)]
        if len(hits) == 1:
            return os.path.join(chapter, "slate", hits[0])
        if len(hits) > 1:
            return os.path.join(chapter, "slate", hits[-1])
    if parent in runs:
        return os.path.join(chapter, "slate", parent)
    return None


def cmd_derive(a, f):
    chapter = os.path.abspath(a.chapter)
    if not sentinel(chapter, f):
        return None
    parent = resolve_parent(chapter, a.parent)
    if not parent:
        f.add("ERROR", "PARENT", "parent run not found: %s" % a.parent)
        return None
    missing = [n for n in FILES if not os.path.isfile(os.path.join(parent, n))]
    if missing:
        f.add("ERROR", "PARENT", "parent lacks %s — derive requires 4/4 (copy what exists by hand, then check)" % ", ".join(missing))
        return None
    pfm, _, err = parse_frontmatter(read(os.path.join(parent, "clean-draft.md")))
    if err or not pfm:
        f.add("ERROR", "PARENT", "parent clean-draft frontmatter unparseable: %s" % err)
        return None
    run = allocate_run(chapter, a.date)
    rundir = os.path.join(chapter, "slate", run)
    prel = "slate/" + os.path.basename(parent)
    fm = {k: pfm.get(k) for k in REQUIRED_KEYS if k in pfm}
    # normalize legacy parents onto the ruled schema where we can
    if "envelope_segments" not in fm:
        legacy = pfm.get("segments")
        if isinstance(legacy, list):
            fm["envelope_segments"] = legacy
            f.add("WARN", "LEGACY", "parent used retired key `segments`; carried as envelope_segments")
        elif isinstance(legacy, str) and "," in legacy:
            fm["envelope_segments"] = [s.strip() for s in legacy.split(",")]
            f.add("WARN", "LEGACY", "parent `segments` was a string; split into a list — confirm")
        else:
            fm["envelope_segments"] = []
            f.add("ERROR", "LEGACY", "parent has no usable envelope_segments; fill by hand before check")
    for k in ("source_dictation", "tense"):
        fm.setdefault(k, pfm.get("source_dictation" if k == "source_dictation" else "tense") or "?")
    fm["generated"] = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    fm["transcoder_version"] = pfm.get("transcoder_version") or "v?"
    fm["status"] = "derived"
    fm["derived_from"] = prel
    fm["supersedes"] = prel
    head = emit_frontmatter(fm)
    for name in FILES:
        _, body, _ = parse_frontmatter(read(os.path.join(parent, name)))
        write(os.path.join(rundir, name), head + body)
    for name in FILES:
        d, _, err = parse_frontmatter(read(os.path.join(rundir, name)))
        if err or not d:
            f.add("ERROR", "PARSE-GATE", "%s failed to parse back: %s" % (name, err))
    f.add("INFO", "DERIVE", "slate/%s derived from %s (4 files copied; edit the new run only, then `check --against %s`)"
          % (run, prel, os.path.basename(parent)))
    return {"rundir": rundir, "run": run, "parent": parent}


def paragraphs(text):
    _, body, _ = parse_frontmatter(text)
    return [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]


def cmd_check(a, f):
    rundir = os.path.abspath(a.rundir)
    if not os.path.isdir(rundir):
        f.add("ERROR", "RUNDIR", "not a folder: %s" % rundir)
        return None
    present = [n for n in FILES if os.path.isfile(os.path.join(rundir, n))]
    missing = [n for n in FILES if n not in present]
    if missing:
        f.add("ERROR", "FILES", "%d/4 files — missing %s (derived runs included: Q3)" % (len(present), ", ".join(missing)))
    else:
        f.add("INFO", "FILES", "4/4 files present")
    extras = [n for n in os.listdir(rundir) if n not in FILES and os.path.isfile(os.path.join(rundir, n))]
    if "clean-ledger.md" in extras:
        f.add("WARN", "PLACEMENT", "clean-ledger.md is slate-local; the ruled home is <chapter>/clean-ledger.md — append it there at the gate")
        extras.remove("clean-ledger.md")
    if extras:
        f.add("WARN", "FILES", "unexpected file(s) in run: %s" % ", ".join(extras))

    fms = {}
    for n in present:
        d, _, err = parse_frontmatter(read(os.path.join(rundir, n)))
        if err or d is None:
            f.add("ERROR", "FRONTMATTER", "%s: %s" % (n, err or "empty"))
            continue
        fms[n] = d
    if "clean-draft.md" in fms:
        d = fms["clean-draft.md"]
        for k in REQUIRED_KEYS:
            if k not in d:
                f.add("ERROR", "SCHEMA", "clean-draft.md missing `%s`" % k)
        if "envelope_segments" in d and not isinstance(d["envelope_segments"], list):
            f.add("ERROR", "SCHEMA", "envelope_segments is %s, must be a list (register-pass slug derivation reads it)"
                  % type(d["envelope_segments"]).__name__)
        retired = [k for k in RETIRED_KEYS if k in d]
        if retired:
            f.add("WARN", "SCHEMA", "retired key(s) present: %s" % ", ".join(retired))
        if d.get("status") not in STATUSES:
            f.add("WARN", "SCHEMA", "status %r not in %s" % (d.get("status"), "/".join(STATUSES)))
        # edited-after-generated (Q4 guard)
        gen = str(d.get("generated", ""))
        try:
            g = _dt.datetime.strptime(gen[:16], "%Y-%m-%d %H:%M")
            m = _dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(rundir, "clean-draft.md")))
            if (m - g).total_seconds() > EDIT_WINDOW_MIN * 60:
                f.add("WARN", "IMMUTABLE", "clean-draft.md modified %s, %.1f h after generated — edits belong in a derived run"
                      % (m.strftime("%Y-%m-%d %H:%M"), (m - g).total_seconds() / 3600))
        except ValueError:
            f.add("WARN", "SCHEMA", "generated %r is not 'YYYY-MM-DD HH:MM'" % gen)
        # sibling blocks should match
        for n in present:
            if n != "clean-draft.md" and n in fms:
                for k in ("source_dictation", "generated", "derived_from"):
                    if fms[n].get(k) != d.get(k):
                        f.add("WARN", "SCHEMA", "%s `%s` differs from clean-draft.md" % (n, k))
                        break
    # markers
    if "clean-draft.md" in present:
        text = read(os.path.join(rundir, "clean-draft.md"))
        markers = [(text[:m.start()].count("\n") + 1, m.group(0)) for m in MARKER_RE.finditer(text)]
        if markers:
            f.add("INFO", "MARKERS", "%d open marker(s) — gate OPEN: %s"
                  % (len(markers), "; ".join("L%d %s" % (ln, mk[:48]) for ln, mk in markers[:12])))
        else:
            f.add("INFO", "MARKERS", "0 markers — gate clearable (seams + scene map still CRE's)")
    # ledger sections
    if "synthesis-ledger.md" in present:
        lt = read(os.path.join(rundir, "synthesis-ledger.md"))
        absent = [s for s in LEDGER_SECTIONS if s not in lt]
        if absent:
            f.add("WARN", "LEDGER", "section(s) absent (absent reads as not-checked): %s" % ", ".join(absent))
        else:
            f.add("INFO", "LEDGER", "all %d sections present" % len(LEDGER_SECTIONS))
    # leaves per segment
    if "leaves-left.md" in present and "clean-draft.md" in fms:
        lt = read(os.path.join(rundir, "leaves-left.md"))
        segs = fms["clean-draft.md"].get("envelope_segments") or []
        if isinstance(segs, list):
            miss = [s for s in segs if s not in lt]
            if miss:
                f.add("WARN", "LEAVES", "segment(s) with no leaves entry: %s" % ", ".join(miss))
    # diff against parent
    if a.against:
        chapter = os.path.dirname(os.path.dirname(rundir))
        parent = resolve_parent(chapter, a.against)
        if not parent or not os.path.isfile(os.path.join(parent, "clean-draft.md")):
            f.add("ERROR", "DIFF", "parent not found: %s" % a.against)
        else:
            A = paragraphs(read(os.path.join(parent, "clean-draft.md")))
            B = paragraphs(read(os.path.join(rundir, "clean-draft.md")))
            same = sum(1 for p in B if p in set(A))
            f.add("INFO", "DIFF", "vs %s: %d¶ in / %d¶ out · %d identical · %d differing"
                  % (os.path.basename(parent), len(A), len(B), same, len(B) - same))
    return {"rundir": rundir}


# ---------- selftest ----------

def selftest():
    tmp = tempfile.mkdtemp(prefix="slate-")
    vault = os.path.join(tmp, "vault")
    write(os.path.join(vault, "_DIRECTIVES.md"), "---\ntype: ai-os-brain\nfile: directives\n---\n# D\n")
    write(os.path.join(vault, "WORKFLOWS", "transcoder.md"), "---\ntype: workflow\n---\n\n# WORKFLOW: Dictation Transcoder (v6.1)\n")
    ch = os.path.join(vault, "WRITING", "PROJECTS", "FIX", "CHAPTERS", "CHAPTER 9 - TEST")
    write(os.path.join(ch, "envelope.md"),
          "---\ntype: chapter-meta\n---\n# Envelopes\n\n## Segment 1 — the-road\n- x\n\n## Segment 2 — the-hut\n- y\n")
    write(os.path.join(ch, "dictation", "README.md"), "# readme\n")
    write(os.path.join(ch, "dictation", "clip-a.md"), "words\n")
    fails = []

    class A:  # argparse stand-in
        pass

    # new
    a = A(); a.chapter = ch; a.dictation = None; a.tense = None; a.canon = None; a.date = "2026-09-02"
    f = Findings(); r = cmd_new(a, f)
    if not r or f.worst() == "ERROR":
        fails.append("new: %s" % f.items)
    else:
        for n in FILES:
            if not os.path.isfile(os.path.join(r["rundir"], n)):
                fails.append("new: %s not written" % n)
        d, _, _ = parse_frontmatter(read(os.path.join(r["rundir"], "clean-draft.md")))
        if d.get("envelope_segments") != ["the-road", "the-hut"]:
            fails.append("new: segments %r" % d.get("envelope_segments"))
        if d.get("source_dictation") != "dictation/clip-a.md":
            fails.append("new: picked %r (README must be skipped)" % d.get("source_dictation"))
        if d.get("transcoder_version") != "v6.1":
            fails.append("new: version %r" % d.get("transcoder_version"))
        if r["run"] != "2026-09-02-01":
            fails.append("new: run %r" % r["run"])
    # second new same day -> -02; and the dictation is now slated -> ERROR (no fresh dictation)
    f2 = Findings(); r2 = cmd_new(a, f2)
    if r2 is not None or not any(c == "DICTATION" and s == "ERROR" for s, c, _ in f2.items):
        fails.append("new#2: should refuse — dictation already slated")
    # check the fresh run
    a3 = A(); a3.rundir = r["rundir"]; a3.against = None
    f3 = Findings(); cmd_check(a3, f3)
    if f3.worst() == "ERROR":
        fails.append("check(new): %s" % [i for i in f3.items if i[0] == "ERROR"])
    # marker census
    cd = os.path.join(r["rundir"], "clean-draft.md")
    write(cd, read(cd) + "She asked. <<GARBLE-UNRESOLVED: G1>> Keep going.\n\n<<OPTIONED-1>>\n")
    f4 = Findings(); cmd_check(a3, f4)
    if not any("2 open marker" in m for _, c, m in f4.items if c == "MARKERS"):
        fails.append("check: marker census missed 2 markers: %s" % [m for _, c, m in f4.items if c == "MARKERS"])
    # derive
    a5 = A(); a5.chapter = ch; a5.parent = "01"; a5.date = "2026-09-02"
    f5 = Findings(); r5 = cmd_derive(a5, f5)
    if not r5 or f5.worst() == "ERROR":
        fails.append("derive: %s" % f5.items)
    else:
        d5, _, _ = parse_frontmatter(read(os.path.join(r5["rundir"], "clean-draft.md")))
        if d5.get("derived_from") != "slate/2026-09-02-01" or d5.get("status") != "derived":
            fails.append("derive: stamps %r" % d5)
        if r5["run"] != "2026-09-02-02":
            fails.append("derive: run %r" % r5["run"])
        # zero-edit diff → 0 differing
        a6 = A(); a6.rundir = r5["rundir"]; a6.against = "01"
        f6 = Findings(); cmd_check(a6, f6)
        dm = [m for _, c, m in f6.items if c == "DIFF"]
        if not dm or "0 differing" not in dm[0]:
            fails.append("check --against: %s" % dm)
    # 2/4 run must fail; retired key + string segments must flag
    bad = os.path.join(ch, "slate", "2026-09-01-01")
    write(os.path.join(bad, "clean-draft.md"),
          "---\ntype: slate-output\nsegments: a, b\nsource_dictation: dictation/x.md\ngenerated: '2026-09-01 10:00'\ntranscoder_version: v6.1\ntense: past\nstatus: gated\n---\n# x\n")
    write(os.path.join(bad, "synthesis-ledger.md"), "---\nsource_dictation: dictation/x.md\n---\n# l\n")
    write(os.path.join(bad, "clean-ledger.md"), "x\n")
    a7 = A(); a7.rundir = bad; a7.against = None
    f7 = Findings(); cmd_check(a7, f7)
    chk = {(s, c) for s, c, _ in f7.items}
    for want in [("ERROR", "FILES"), ("ERROR", "SCHEMA"), ("WARN", "SCHEMA"), ("WARN", "PLACEMENT")]:
        if want not in chk:
            fails.append("check(bad): expected %s in %s" % (want, sorted(chk)))
    # sentinel
    nov = os.path.join(tmp, "novault", "CHAPTERS", "CH")
    write(os.path.join(nov, "envelope.md"), "## Segment 1 — a\n")
    a8 = A(); a8.chapter = nov; a8.dictation = None; a8.tense = None; a8.canon = None; a8.date = None
    f8 = Findings()
    if cmd_new(a8, f8) is not None or not any(c == "SENTINEL" for _, c, _ in f8.items):
        fails.append("sentinel: should halt without _DIRECTIVES.md")

    if fails:
        print("SELFTEST FAIL")
        for x in fails:
            print("  - " + x)
        return 1
    print("SELFTEST PASS (fixtures in %s)" % tmp)
    return 0


def main():
    utf8_console()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    n = sub.add_parser("new"); n.add_argument("--chapter", required=True); n.add_argument("--dictation")
    n.add_argument("--tense"); n.add_argument("--canon"); n.add_argument("--date", help="YYYY-MM-DD override (tests)")
    d = sub.add_parser("derive"); d.add_argument("--chapter", required=True); d.add_argument("--parent", required=True)
    d.add_argument("--date")
    c = sub.add_parser("check"); c.add_argument("rundir"); c.add_argument("--against")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.cmd:
        ap.error("one of: new / derive / check / --selftest")
    f = Findings()
    r = {"new": cmd_new, "derive": cmd_derive, "check": cmd_check}[a.cmd](a, f)
    print(f.render("slate_scaffold %s" % a.cmd))
    if r and a.cmd == "new":
        print("\n--- _CHANGELOG stub ---\n" + r["vault_stub"] + "\n--- chapter changelog.md stub ---\n" + r["chapter_stub"])
    if r is None or any(c == "SENTINEL" for _, c, _ in f.items):
        sys.exit(2 if (r is None and f.worst() == "ERROR" and any(c in ("SENTINEL", "CHAPTER", "RUNDIR") for _, c, _ in f.items)) else 1)
    sys.exit(1 if f.worst() == "ERROR" else 0)


if __name__ == "__main__":
    main()
