#!/usr/bin/env python3
"""register_scaffold.py — the register pass's mechanical shell (references/rev-contract.md).

Owns everything about a revision that is bookkeeping, so the model only runs the
register and writes the note:

  resolve --chapter DIR [--slate NN|RUN]
          sentinel · project root · REFERENCE/register.md (+ its title) · working text
          (draft.md if real content, else newest slate) · mode (execute-only when a ready
          verdicts.md matches the run; on a no-slate chapter the run is the sheet's minted
          id — spec-check.md 2026-08-24 rule, RP-P3) · slate ledgers present · protected-span census
          · prints a JSON block the model reads instead of re-deriving any of it
  new     --chapter DIR [--slate NN|RUN] [--sweep] [--date YYYY-MM-DD]
          resolve, then allocate YYYY-MM-DD-<slug>-rev<N> (or -sweep<N>) and write the
          rev + note stubs (note only for --sweep) with one serialized frontmatter block
          each · parse-gate what was written · print the changelog stubs
  check   FILE            a rev file, a note file, or either half of a pair
          frontmatter parses with the ruled key set · retired keys · source_slate is the
          bare form · mode/verdicts agree · <<FILL>> residue · rev body non-empty ·
          protected_spans_touched: every chapter span accounted, `kept` byte-verified,
          `reworded` needs new: (verified), `dropped` needs ruled:
  --selftest

Exit: 0 clean (INFO/WARN) · 1 ERROR findings · 2 gate failure (sentinel, bad path).
stdlib only (DIR-007). Console forced to UTF-8. Never writes outside <chapter>/revisions/.
Never writes prose. Never decides reworded-vs-dropped (DIR-014 corollary) — it only says
whether a `kept` claim is true.
"""
import argparse
import datetime as _dt
import json
import os
import re
import sys
import tempfile

REV_KEYS = ("type", "chapter", "project", "rev", "kind", "source_slate", "working_text",
            "register", "register_title", "mode", "verdicts", "maturity_gear", "generated")
REV_REQUIRED = tuple(k for k in REV_KEYS if k != "verdicts")
NOTE_KEYS = ("type", "pairs_with", "protected_spans_touched", "drift")
RETIRED_REV_KEYS = ("status", "source", "rulings", "sheet", "ledger", "explains", "segments", "date")
RETIRED_NOTE_KEYS = ("explains", "source_slate", "register", "mode", "verdicts", "rev", "date")
MODES = ("full", "execute-only")
STATES = ("kept", "reworded", "dropped")
FILL = "<<FILL"
FILL_RE = re.compile(r"<<FILL[^>]*>>")
RUN_RE = re.compile(r"(\d{4}-\d{2}-\d{2}-\d{2})")
VERSION_RE = re.compile(r"\bv(\d+(?:\.\d+)*)\b")
SPAN_LINE_RE = re.compile(r"^\s*-\s+span:\s*(.+?)\s*$")
PLACEHOLDER_BODY_RE = re.compile(r"^\s*(>.*)?\s*$")


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

    def has(self, sev, check):
        return any(s == sev and c == check for s, c, _ in self.items)

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


# ---------- frontmatter: fixed-shape emitter + parser (DIR-004 parse gate) ----------

def yaml_scalar(v):
    s = str(v)
    if s == "" or re.search(r"[:#\[\]{},&*!|>'\"%@`]|^\s|\s$|^-|^\d{4}-\d{2}-\d{2}", s):
        return "'" + s.replace("'", "''") + "'"
    return s


def emit_rev_frontmatter(d):
    lines = ["---"]
    for k in REV_KEYS:
        if k not in d or d[k] is None:
            continue
        v = d[k]
        if k == "rev":
            lines.append("%s: %d" % (k, int(v)))
        else:
            lines.append("%s: %s" % (k, yaml_scalar(v)))
    lines.append("---")
    return "\n".join(lines) + "\n"


def emit_note_frontmatter(d):
    lines = ["---", "type: revision-note", "pairs_with: %s" % yaml_scalar(d["pairs_with"])]
    rows = d.get("protected_spans_touched") or []
    if not rows:
        lines.append("protected_spans_touched: []")
    else:
        lines.append("protected_spans_touched:")
        for r in rows:
            lines.append("- span: %s" % yaml_scalar(r["span"]))
            lines.append("  state: %s" % yaml_scalar(r.get("state", "")))
            if r.get("new") is not None:
                lines.append("  new: %s" % yaml_scalar(r["new"]))
            if r.get("ruled") is not None:
                lines.append("  ruled: %s" % yaml_scalar(r["ruled"]))
    drift = d.get("drift") or {}
    lines.append("drift:")
    lines.append("  voice_spec: %s" % yaml_scalar(drift.get("voice_spec", "")))
    lines.append("  contamination: %s" % yaml_scalar(drift.get("contamination", "")))
    lines.append("---")
    return "\n".join(lines) + "\n"


def split_frontmatter(text):
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
    return "\n".join(lines[1:end]), "\n".join(lines[end + 1:]), None


def _unquote(val):
    if len(val) >= 2 and val[0] == val[-1] and val[0] in "'\"":
        return val[1:-1].replace("''", "'")
    return val


def _fallback_parse(block):
    """Handles the two shapes this skill emits (flat scalars; a list of flat mappings under
    one key; a one-level mapping) plus the flat-scalar frontmatter of drafts and slates.
    Nested lists of mappings under `protected_patterns` are read separately by spans_in()."""
    d, key, cur_list, cur_map = {}, None, None, None
    for raw in block.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        s = raw.strip()
        if indent == 0 and s.startswith("- "):
            # top-level list item under the last key
            if key is None:
                return None, "list item before any key"
            if not isinstance(d.get(key), list):
                d[key] = []
            m = re.match(r"^-\s+([A-Za-z_][\w\-]*):\s*(.*)$", s)
            if m:
                cur_map = {m.group(1): _unquote(m.group(2).strip())}
                d[key].append(cur_map)
            else:
                d[key].append(_unquote(s[2:].strip()))
                cur_map = None
            continue
        if indent > 0:
            m = re.match(r"^([A-Za-z_][\w\-]*):\s*(.*)$", s)
            if m and cur_map is not None:
                cur_map[m.group(1)] = _unquote(m.group(2).strip())
                continue
            if m and isinstance(d.get(key), dict):
                d[key][m.group(1)] = _unquote(m.group(2).strip())
                continue
            if key is not None and not isinstance(d.get(key), (list, dict)):
                d[key] = (str(d.get(key) or "") + " " + s).strip()
                continue
            return None, "unparseable indented line: %r" % raw[:60]
        m = re.match(r"^([A-Za-z_][\w\-]*):\s*(.*)$", s)
        if not m:
            return None, "unparseable line: %r" % raw[:60]
        key, val = m.group(1), m.group(2).strip()
        cur_map = None
        if val == "":
            d[key] = {}  # becomes a list on the first "- " line, a mapping on the first indented k: v
            continue
        if val == "[]":
            d[key] = []
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            d[key] = [_unquote(x.strip()) for x in inner.split(",") if x.strip()] if inner else []
        else:
            d[key] = _unquote(val)
    # a key that got `{}` and then "- " items was converted; a key left as {} with no children is empty
    return d, None


def parse_frontmatter(text):
    block, body, err = split_frontmatter(text)
    if err:
        return None, text, err
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
    d, err = _fallback_parse(block)
    if err:
        return None, body, err
    return d, body, None


def spans_in(text):
    """Chapter-level protected spans: every `- span:` row inside the frontmatter block.
    Regex on purpose — the shape is fixed and the fallback parser must not guess at nesting."""
    block, _, err = split_frontmatter(text)
    if err or block is None:
        return []
    out = []
    for ln in block.split("\n"):
        m = SPAN_LINE_RE.match(ln)
        if m:
            out.append(_unquote(m.group(1)))
    return out


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


def project_root(chapter):
    """The folder whose CHAPTERS/ contains this chapter; else the nearest ancestor with REFERENCE/register.md."""
    p = os.path.abspath(chapter)
    parent = os.path.dirname(p)
    if os.path.basename(parent).upper() == "CHAPTERS":
        return os.path.dirname(parent)
    q = p
    for _ in range(8):
        if os.path.isfile(os.path.join(q, "REFERENCE", "register.md")):
            return q
        nq = os.path.dirname(q)
        if nq == q:
            break
        q = nq
    return None


def title_of(md_path):
    for ln in read(md_path).split("\n")[:60]:
        if ln.startswith("# "):
            return ln[2:].strip()
    return None


def version_in(md_path, head_lines=40):
    if not md_path or not os.path.isfile(md_path):
        return None
    for ln in read(md_path).split("\n")[:head_lines]:
        if ln.startswith("# "):
            m = VERSION_RE.search(ln)
            if m:
                return "v" + m.group(1)
    return None


def bare_run(v):
    """'slate/2026-08-05-01/clean-draft.md' → '2026-08-05-01'; already-bare passes through."""
    if v is None:
        return None
    m = RUN_RE.search(str(v))
    return m.group(1) if m else str(v)


def existing_runs(chapter):
    sd = os.path.join(chapter, "slate")
    if not os.path.isdir(sd):
        return []
    return sorted(d for d in os.listdir(sd)
                  if re.match(r"^\d{4}-\d{2}-\d{2}-\d{2}$", d) and os.path.isdir(os.path.join(sd, d)))


def resolve_run(chapter, want):
    runs = existing_runs(chapter)
    if not want:
        return runs[-1] if runs else None
    if want in runs:
        return want
    if re.match(r"^\d{2}$", want):
        hits = [r for r in runs if r.endswith("-" + want)]
        return hits[-1] if hits else None
    return bare_run(want) if bare_run(want) in runs else None


def draft_is_real(draft_path):
    """Scaffold = status starts with not-yet-migrated, or the body is empty / placeholder-only."""
    if not os.path.isfile(draft_path):
        return False, None
    text = read(draft_path)
    fm, body, _ = parse_frontmatter(text)
    fm = fm or {}
    status = str(fm.get("status", ""))
    if status.startswith("not-yet-migrated") or status.startswith("scaffold"):
        return False, fm
    prose = [ln for ln in body.split("\n") if ln.strip() and not ln.lstrip().startswith(("#", ">", "<!--"))]
    return (len(prose) > 0), fm


def no_slate_sheet(chapter):
    """No-slate route (spec-check.md 2026-08-24 rule; RP-P3, 2026-09-02): a chapter whose draft.md
    carries no source_slate keys its verdict sheet on a MINTED run id — spec-check/<YYYY-MM-DD-NN>/
    verdicts.md with `slate_run: none — …` and the sheet naming draft.md as its text. Returns the
    newest such run id that is `status: ready`, else None. A sheet keyed to a real slate run is
    never picked here (that is select_mode's job)."""
    sd = os.path.join(chapter, "spec-check")
    if not os.path.isdir(sd):
        return None
    hits = []
    for d in sorted(os.listdir(sd)):
        vp = os.path.join(sd, d, "verdicts.md")
        if not re.match(r"^\d{4}-\d{2}-\d{2}-\d{2}$", d) or not os.path.isfile(vp):
            continue
        fm, _, err = parse_frontmatter(read(vp))
        if err or not fm:
            continue
        sr = str(fm.get("slate_run", "")).strip().lower()
        names_draft = "draft.md" in (str(fm.get("working_text", "")) + " " + str(fm.get("source", "")))
        if sr.startswith("none") and names_draft and str(fm.get("status", "")).strip() == "ready":
            hits.append(d)
    return hits[-1] if hits else None


def pick_working_text(chapter, want_run, f):
    """Returns dict(kind, path, rel, run, fm, no_slate) or None."""
    draft = os.path.join(chapter, "draft.md")
    if not want_run:
        real, dfm = draft_is_real(draft)
        if real:
            run = bare_run(dfm.get("source_slate"))
            no_slate = False
            if not run:
                run = no_slate_sheet(chapter)
                if run:
                    no_slate = True
                    f.add("INFO", "NO-SLATE", "draft.md has no source_slate — no-slate route: keyed on spec-check/%s (minted run id); "
                          "rev source_slate carries it (RP-P3)" % run)
                else:
                    f.add("WARN", "WORKING", "draft.md has no source_slate and no ready no-slate verdict sheet; slate ledgers cannot be located")
            return {"kind": "draft", "path": draft, "rel": "draft.md", "run": run, "fm": dfm, "no_slate": no_slate}
    run = resolve_run(chapter, want_run)
    if not run:
        if want_run:
            f.add("ERROR", "WORKING", "named slate run not found: %s" % want_run)
        else:
            f.add("ERROR", "WORKING", "no real draft.md and no slate run — nothing to revise (run the Transcoder first)")
        return None
    cd = os.path.join(chapter, "slate", run, "clean-draft.md")
    if not os.path.isfile(cd):
        f.add("ERROR", "WORKING", "slate/%s has no clean-draft.md" % run)
        return None
    fm, _, err = parse_frontmatter(read(cd))
    if err:
        f.add("WARN", "WORKING", "slate/%s/clean-draft.md frontmatter: %s" % (run, err))
    return {"kind": "slate", "path": cd, "rel": "slate/%s/clean-draft.md" % run, "run": run, "fm": fm or {}, "no_slate": False}


def select_mode(chapter, run, f, no_slate=False):
    if not run:
        return "full", None
    if no_slate:
        # no_slate_sheet already proved: ready, slate_run none, names draft.md (RP-P3)
        return "execute-only", "spec-check/%s/verdicts.md" % run
    vp = os.path.join(chapter, "spec-check", run, "verdicts.md")
    if not os.path.isfile(vp):
        return "full", None
    fm, _, err = parse_frontmatter(read(vp))
    if err or not fm:
        f.add("WARN", "MODE", "verdicts.md present but unparseable (%s) — running full" % err)
        return "full", None
    if str(fm.get("status", "")).strip() != "ready":
        f.add("INFO", "MODE", "verdicts.md status %r — not ready; running full" % fm.get("status"))
        return "full", None
    if bare_run(fm.get("slate_run")) != run:
        f.add("WARN", "MODE", "verdicts.md slate_run %r != working run %s — treated as absent (stale rulings)"
              % (fm.get("slate_run"), run))
        return "full", None
    return "execute-only", "spec-check/%s/verdicts.md" % run


def slug_for(chapter, wt):
    segs = wt["fm"].get("envelope_segments") if wt else None
    if (not isinstance(segs, list) or not segs) and wt and wt["run"]:
        cd = os.path.join(chapter, "slate", wt["run"], "clean-draft.md")
        if os.path.isfile(cd):
            sfm, _, _ = parse_frontmatter(read(cd))
            segs = (sfm or {}).get("envelope_segments")
    if isinstance(segs, list) and segs:
        return "+".join(str(s).strip() for s in segs if str(s).strip())
    return "full-chapter"


def allocate(chapter, slug, kind, today):
    rd = os.path.join(chapter, "revisions")
    pat = re.compile(r"^\d{4}-\d{2}-\d{2}-%s-%s(\d+)(-note)?\.md$" % (re.escape(slug), kind))
    n = 0
    if os.path.isdir(rd):
        for fn in os.listdir(rd):
            m = pat.match(fn)
            if m:
                n = max(n, int(m.group(1)))
    return n + 1, "%s-%s-%s%d" % (today, slug, kind, n + 1)


def protected_census(root, project, wt, f):
    spans = spans_in(read(wt["path"])) if wt else []
    ref = os.path.join(project, "REFERENCE", "protected-patterns.md") if project else None
    rules = 0
    if ref and os.path.isfile(ref):
        rules = len(re.findall(r"^\|\s*P\d+\s*\|", read(ref), re.M))
    f.add("INFO", "PROTECTED", "%d chapter span(s) to account for · %d project P-rule(s) to consult (rules, not spans — not byte-verifiable)"
          % (len(spans), rules))
    return spans, rules


# ---------- commands ----------

def cmd_resolve(a, f, quiet=False):
    chapter = os.path.abspath(a.chapter)
    if not os.path.isdir(chapter):
        f.add("ERROR", "CHAPTER", "not a folder: %s" % chapter)
        return None
    root = sentinel(chapter, f)
    if not root:
        return None
    if not os.path.isdir(os.path.join(chapter, "slate")) and not os.path.isdir(os.path.join(chapter, "revisions")):
        f.add("ERROR", "CONVENTION", "no slate/ and no revisions/ — this chapter does not use the per-chapter folder convention")
        return None
    project = project_root(chapter)
    reg = os.path.join(project, "REFERENCE", "register.md") if project else None
    if not reg or not os.path.isfile(reg):
        f.add("ERROR", "REGISTER", "no REFERENCE/register.md above %s — halt and ask; never substitute a generic prompt" % chapter)
        return None
    wt = pick_working_text(chapter, getattr(a, "slate", None), f)
    if not wt:
        return None
    mode, verdicts = select_mode(chapter, wt["run"], f, wt.get("no_slate", False))
    ledgers = {}
    if wt["run"] and not wt.get("no_slate"):
        for n in ("synthesis-ledger.md", "leaves-left.md"):
            ledgers[n] = os.path.isfile(os.path.join(chapter, "slate", wt["run"], n))
    spans, rules = protected_census(root, project, wt, f)
    canon = os.path.join(root, "WORKFLOWS", "register-pass.md")
    cver = version_in(canon)
    sver = version_in(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL.md"), 20)
    if cver and sver and cver != sver:
        f.add("WARN", "VERSION", "canon register-pass.md is %s, this SKILL.md is %s — run from the canon doc; announce the gap (DIR-009)" % (cver, sver))
    soft = {n: os.path.isfile(os.path.join(project, "REFERENCE", n)) for n in ("voice-spec.md", "contamination-checklist.md")}
    r = {
        "chapter": chapter, "chapter_name": os.path.basename(chapter), "project": project,
        "project_name": os.path.basename(project), "register": reg,
        "register_rel": "REFERENCE/register.md", "register_title": title_of(reg) or "?",
        "working_text": wt["rel"], "working_kind": wt["kind"], "source_slate": wt["run"],
        "mode": mode, "verdicts": verdicts, "ledgers": ledgers, "protected_spans": spans,
        "protected_rules": rules, "soft_checks": soft, "canon_version": cver, "skill_version": sver,
        "slug": slug_for(chapter, wt),
    }
    f.add("INFO", "RESOLVE", "working text %s · source_slate %s · mode %s · register %r"
          % (wt["rel"], wt["run"], mode, r["register_title"]))
    if not quiet:
        r["_json"] = json.dumps({k: v for k, v in r.items() if not k.startswith("_")}, indent=2, ensure_ascii=False)
    return r


def stub_rev(r, n, today):
    fm = {
        "type": "chapter-revision", "chapter": r["chapter_name"], "project": r["project_name"], "rev": n,
        "kind": "register", "source_slate": r["source_slate"] or "<<FILL: run id>>",
        "working_text": r["working_text"], "register": r["register_rel"], "register_title": r["register_title"],
        "mode": r["mode"], "verdicts": r["verdicts"] if r["mode"] == "execute-only" else None,
        "maturity_gear": "<<FILL: gear the register chose>>",
        "generated": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    return emit_rev_frontmatter(fm) + "\n<<FILL: the revised passage — clean prose only; keep the register's [unclear: …] marks>>\n"


def stub_note(r, pairs_with, sweep):
    rows = [{"span": s, "state": "<<FILL: kept|reworded|dropped>>"} for s in r["protected_spans"]]
    drift = {}
    for k, n in (("voice_spec", "voice-spec.md"), ("contamination", "contamination-checklist.md")):
        drift[k] = "<<FILL: in band | drift lines>>" if r["soft_checks"].get(n) else "n/a — REFERENCE/%s absent" % n
    head = emit_note_frontmatter({"pairs_with": pairs_with, "protected_spans_touched": rows, "drift": drift})
    if sweep:
        body = ("\n# Register sweep — %s\n\nWorking text: %s · source_slate: %s · mode: sweep (no passage produced)\n\n"
                "## Unrecoverable breaks\n\n_none_\n\n## Checked\n\n<<FILL: what the register checked>>\n\n"
                "## Would have been an edit — not earned\n\n<<FILL>>\n\n## Protected spans\n\n_accounted in frontmatter_\n"
                % (r["chapter_name"], r["working_text"], r["source_slate"]))
    else:
        body = ("\n# Editorial note — %s\n\n## Unrecoverable breaks\n\n<<FILL: list first, or _none_>>\n\n"
                "## Diagnosis\n\n<<FILL>>\n\n## Craft changes\n\n<<FILL>>\n\n## Mechanical corrections\n\n<<FILL>>\n\n"
                "## Considered and rejected\n\n<<FILL>>\n\n## Counts\n\n<<FILL>>\n\n"
                "## Verdict rows applied (execute-only)\n\n<<FILL or _n/a — full mode_>>\n\n"
                "## Prior-pass context acted on\n\n<<FILL: left-for-later items, [REGISTER-REPAIR] flags, or _none_>>\n"
                % pairs_with)
    return head + body


def changelog_stubs(r, names, today):
    files = " + ".join("revisions/%s" % n for n in names)
    vault = ("## %s — [fiction] register pass — %s (%s)\n"
             "**Ran:** register %r on %s · source_slate %s · mode %s\n"
             "**Shipped:** %s · N craft changes · N mechanical · N protected spans accounted (N kept / N reworded / N dropped)\n"
             "**Unrecoverable breaks:** N (listed first in the note)\n"
             % (today, r["chapter_name"], r["mode"], r["register_title"], r["working_text"], r["source_slate"], r["mode"], files))
    chap = ("## %s — register pass (%s) — %s\n**Working text:** %s · **source_slate:** %s\n**Files:** %s\n**Breaks:** N\n"
            % (today, r["mode"], names[0], r["working_text"], r["source_slate"], files))
    return vault, chap


def cmd_new(a, f):
    r = cmd_resolve(a, f, quiet=True)
    if not r:
        return None
    today = a.date or _dt.date.today().isoformat()
    sweep = bool(getattr(a, "sweep", False))
    rd = os.path.join(r["chapter"], "revisions")
    names = []
    if sweep:
        r["mode"] = "sweep"
        f.add("INFO", "RESOLVE", "mode → sweep (--sweep: note only, no rev<N> consumed; the line above shows what a rev run would have been)")
        n, base = allocate(r["chapter"], r["slug"], "sweep", today)
        note = base + "-note.md"
        pairs = "%s (sweep — no passage produced)" % r["working_text"]
        write(os.path.join(rd, note), stub_note(r, pairs, True))
        names.append(note)
    else:
        n, base = allocate(r["chapter"], r["slug"], "rev", today)
        rev, note = base + ".md", base + "-note.md"
        write(os.path.join(rd, rev), stub_rev(r, n, today))
        write(os.path.join(rd, note), stub_note(r, "revisions/" + rev, False))
        names.extend([rev, note])
    for nme in names:
        d, _, err = parse_frontmatter(read(os.path.join(rd, nme)))
        if err or not d:
            f.add("ERROR", "PARSE-GATE", "%s frontmatter failed to parse back: %s" % (nme, err))
    f.add("INFO", "NEW", "%s written (%d stub%s) · slug %s · %s"
          % (", ".join(names), len(names), "" if len(names) == 1 else "s", r["slug"], r["mode"]))
    v, c = changelog_stubs(r, names, today)
    return {"files": [os.path.join(rd, n) for n in names], "vault_stub": v, "chapter_stub": c, "resolve": r}


def _pair_of(path):
    """Given a rev or note path, return (rev_path or None, note_path or None)."""
    d, fn = os.path.dirname(path), os.path.basename(path)
    if fn.endswith("-note.md"):
        rev = os.path.join(d, fn[:-len("-note.md")] + ".md")
        return (rev if os.path.isfile(rev) else None), path
    note = os.path.join(d, fn[:-3] + "-note.md")
    return path, (note if os.path.isfile(note) else None)


def check_rev(path, f):
    text = read(path)
    d, body, err = parse_frontmatter(text)
    n = os.path.basename(path)
    if err or d is None:
        f.add("ERROR", "FRONTMATTER", "%s: %s" % (n, err or "empty"))
        return None, ""
    for k in REV_REQUIRED:
        if k not in d:
            f.add("ERROR", "SCHEMA", "%s missing `%s`" % (n, k))
    if d.get("type") != "chapter-revision" or d.get("kind") != "register":
        f.add("WARN", "SCHEMA", "%s type/kind %r/%r — expected chapter-revision/register" % (n, d.get("type"), d.get("kind")))
    retired = [k for k in RETIRED_REV_KEYS if k in d]
    if retired:
        f.add("WARN", "SCHEMA", "%s retired key(s): %s" % (n, ", ".join(retired)))
    ss = str(d.get("source_slate", ""))
    if ss and not re.match(r"^\d{4}-\d{2}-\d{2}-\d{2}$", ss):
        f.add("WARN" if bare_run(ss) != ss else "ERROR", "SOURCE-SLATE",
              "%s source_slate %r is not the bare run id (dec-033) — bare form: %s" % (n, ss, bare_run(ss)))
    mode = d.get("mode")
    if mode not in MODES:
        f.add("ERROR", "MODE", "%s mode %r — a rev file is full or execute-only (sweep writes no rev)" % (n, mode))
    if mode == "execute-only" and not d.get("verdicts"):
        f.add("ERROR", "MODE", "%s execute-only without `verdicts`" % n)
    if mode == "full" and d.get("verdicts"):
        f.add("WARN", "MODE", "%s full mode carries `verdicts` — drop it" % n)
    m = re.search(r"-rev(\d+)\.md$", n)
    if m and str(d.get("rev")) != m.group(1):
        f.add("ERROR", "SCHEMA", "%s rev: %r != filename rev%s" % (n, d.get("rev"), m.group(1)))
    fills = FILL_RE.findall(text)
    if fills:
        f.add("ERROR", "FILL", "%s has %d <<FILL>> marker(s) left" % (n, len(fills)))
    if not [ln for ln in body.split("\n") if ln.strip()]:
        f.add("ERROR", "BODY", "%s body is empty" % n)
    return d, body


def check_note(path, f, rev_body, chapter_spans, label="rev"):
    """`rev_body` is the text every `kept` / `new:` claim is verified against — the rev body for a
    rev+note pair, the working text for a sweep note (RP-P1, 2026-09-02). `label` names which."""
    text = read(path)
    d, body, err = parse_frontmatter(text)
    n = os.path.basename(path)
    if err or d is None:
        f.add("ERROR", "FRONTMATTER", "%s: %s" % (n, err or "empty"))
        return None
    for k in NOTE_KEYS:
        if k not in d:
            f.add("ERROR", "SCHEMA", "%s missing `%s`" % (n, k))
    retired = [k for k in RETIRED_NOTE_KEYS if k in d]
    if retired:
        f.add("WARN", "SCHEMA", "%s retired key(s): %s (keyed provenance lives on the rev file)" % (n, ", ".join(retired)))
    fills = FILL_RE.findall(text)
    if fills:
        f.add("ERROR", "FILL", "%s has %d <<FILL>> marker(s) left" % (n, len(fills)))
    rows = d.get("protected_spans_touched")
    if rows is None:
        return d
    if isinstance(rows, dict) and not rows:
        rows = []
    if not isinstance(rows, list):
        f.add("ERROR", "SPANS", "%s protected_spans_touched must be a list (use [] for none)" % n)
        return d
    seen = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or "span" not in row:
            f.add("ERROR", "SPANS", "%s row %d is not a span mapping" % (n, i + 1))
            continue
        span, state = str(row["span"]), str(row.get("state", ""))
        seen.add(span)
        if state not in STATES:
            f.add("ERROR", "SPANS", "%s row %d state %r not in %s" % (n, i + 1, state, "/".join(STATES)))
            continue
        if state == "kept":
            if rev_body is None:
                f.add("WARN", "SPANS", "%s row %d kept — no %s body to verify against (missing pair)" % (n, i + 1, label))
            elif span not in rev_body:
                f.add("ERROR", "KEPT", "row %d claims kept but the span is not in the %s verbatim: %r — QUERY for the reasoning stage (reworded or dropped is not the script's call)"
                      % (i + 1, label, span[:70]))
        elif state == "reworded":
            new = row.get("new")
            if not new:
                f.add("ERROR", "SPANS", "%s row %d reworded without `new:`" % (n, i + 1))
            elif rev_body is not None and str(new) not in rev_body:
                f.add("ERROR", "SPANS", "%s row %d `new:` witness not in the %s verbatim: %r" % (n, i + 1, label, str(new)[:70]))
        elif state == "dropped" and not row.get("ruled"):
            f.add("ERROR", "SPANS", "%s row %d dropped without `ruled:` — an unaccounted drop is a defect (revert, don't rationalize)" % (n, i + 1))
    if chapter_spans is not None:
        missing = [s for s in chapter_spans if s not in seen]
        if missing:
            f.add("ERROR", "SPANS", "%d chapter span(s) unaccounted in %s: %s" % (len(missing), n, "; ".join(x[:50] for x in missing[:6])))
        else:
            f.add("INFO", "SPANS", "%d chapter span(s) accounted · %d row(s)" % (len(chapter_spans), len(rows)))
    return d


def cmd_check(a, f):
    path = os.path.abspath(a.file)
    if not os.path.isfile(path):
        f.add("ERROR", "FILE", "not a file: %s" % path)
        return None
    rev, note = _pair_of(path)
    chapter = os.path.dirname(os.path.dirname(path))
    rev_body, spans = None, None
    if rev:
        d, rev_body = check_rev(rev, f)
        wt = (d or {}).get("working_text")
        if wt:
            wp = os.path.join(chapter, str(wt))
            if os.path.isfile(wp):
                spans = spans_in(read(wp))
            else:
                f.add("WARN", "SPANS", "working_text %s not found — chapter spans not enumerated" % wt)
    if note:
        label, sweep = "rev", False
        if not rev:
            # No rev beside the note: either a sweep (verify every claim against the WORKING TEXT the
            # note names — RP-P1, 2026-09-02) or a broken pair.
            nd0, _, _ = parse_frontmatter(read(note))
            pw = str((nd0 or {}).get("pairs_with", ""))
            if "sweep" in pw:
                sweep = True
                m = re.match(r"^(\S+)", pw)
                wp = os.path.join(chapter, m.group(1)) if m else None
                if wp and os.path.isfile(wp):
                    wtext = read(wp)
                    _, rev_body, _ = parse_frontmatter(wtext)
                    spans, label = spans_in(wtext), "working text"
                else:
                    f.add("WARN", "SPANS", "sweep note names %r but it is not on disk — spans not verified" % pw)
        nd = check_note(note, f, rev_body, spans, label)
        if nd and not rev:
            if sweep:
                f.add("INFO", "SWEEP", "sweep note — no rev expected; span claims verified against the working text")
            else:
                f.add("ERROR", "PAIR", "note has no rev file beside it: %s" % nd.get("pairs_with"))
    elif rev:
        f.add("ERROR", "PAIR", "rev has no -note.md sidecar")
    return {"rev": rev, "note": note}


# ---------- selftest ----------

def selftest():
    tmp = tempfile.mkdtemp(prefix="regpass-")
    vault = os.path.join(tmp, "vault")
    write(os.path.join(vault, "_DIRECTIVES.md"), "---\ntype: ai-os-brain\nfile: directives\n---\n# D\n")
    write(os.path.join(vault, "WORKFLOWS", "register-pass.md"), "---\ntype: workflow\n---\n\n# WORKFLOW: Register Pass (v2)\n")
    proj = os.path.join(vault, "WRITING", "PROJECTS", "FIX")
    write(os.path.join(proj, "REFERENCE", "register.md"), "# Braided-Register Literary Fantasy (v3)\n\nrules\n")
    write(os.path.join(proj, "REFERENCE", "protected-patterns.md"), "| # | Scope |\n|---|---|\n| P1 | project |\n| P2 | project |\n")
    write(os.path.join(proj, "REFERENCE", "voice-spec.md"), "# v\n")
    ch = os.path.join(proj, "CHAPTERS", "CHAPTER 9 - TEST")
    run = "2026-08-05-01"
    write(os.path.join(ch, "slate", run, "clean-draft.md"),
          "---\nsource_dictation: dictation/a.md\nenvelope_segments: [the-road, the-hut]\ngenerated: '2026-08-05 10:00'\n"
          "transcoder_version: v6.1\ntense: past\nstatus: gated\n---\n# Floor\n\nShe walked.\n")
    write(os.path.join(ch, "slate", run, "leaves-left.md"), "---\nsource_dictation: dictation/a.md\n---\n# l\n")
    write(os.path.join(ch, "revisions", "README.md"), "# revisions/\n")
    fails = []

    class A:
        pass

    def args(**kw):
        a = A(); a.chapter = ch; a.slate = None; a.sweep = False; a.date = "2026-09-02"
        for k, v in kw.items():
            setattr(a, k, v)
        return a

    # 1. scaffold draft → falls back to the slate; full mode; slug from segments
    write(os.path.join(ch, "draft.md"), "---\ntype: chapter-draft\nstatus: not-yet-migrated\n---\n\n> placeholder\n")
    f = Findings(); r = cmd_resolve(args(), f, quiet=True)
    if not r or f.worst() == "ERROR":
        fails.append("resolve#1: %s" % f.items)
    else:
        if r["working_text"] != "slate/%s/clean-draft.md" % run or r["mode"] != "full" or r["slug"] != "the-road+the-hut":
            fails.append("resolve#1: %r / %r / %r" % (r["working_text"], r["mode"], r["slug"]))
        if r["register_title"] != "Braided-Register Literary Fantasy (v3)":
            fails.append("resolve#1: title %r" % r["register_title"])
    # 2. real draft with path-form source_slate + protected spans → draft wins; run normalized; spans counted
    write(os.path.join(ch, "draft.md"),
          "---\ntype: chapter-draft\nstatus: 'author-cut — LANDED'\nsource_slate: slate/%s/clean-draft.md\nprotected_patterns:\n"
          "- span: the pillow of her tongue\n  ruled: '2026-08-03'\n- span: Been through worse\n  ruled: '2026-08-03'\n---\n\n"
          "She walked and the pillow of her tongue was dry. Been through worse, she said.\n" % run)
    f = Findings(); r = cmd_resolve(args(), f, quiet=True)
    if not r or f.worst() == "ERROR":
        fails.append("resolve#2: %s" % f.items)
    else:
        if r["working_text"] != "draft.md" or r["source_slate"] != run or len(r["protected_spans"]) != 2 or r["protected_rules"] != 2:
            fails.append("resolve#2: %r %r %r %r" % (r["working_text"], r["source_slate"], r["protected_spans"], r["protected_rules"]))
    # 3. ready verdicts for the run → execute-only; mismatched slate_run → full
    vp = os.path.join(ch, "spec-check", run, "verdicts.md")
    write(vp, "---\nstatus: ready\nslate_run: %s\n---\n# v\n" % run)
    f = Findings(); r = cmd_resolve(args(), f, quiet=True)
    if not r or r["mode"] != "execute-only" or r["verdicts"] != "spec-check/%s/verdicts.md" % run:
        fails.append("resolve#3: mode %r" % (r and r["mode"]))
    write(vp, "---\nstatus: ready\nslate_run: 2026-08-04-01\n---\n# v\n")
    f = Findings(); r = cmd_resolve(args(), f, quiet=True)
    if not r or r["mode"] != "full" or not f.has("WARN", "MODE"):
        fails.append("resolve#3b: stale verdicts should be treated as absent")
    write(vp, "---\nstatus: ready\nslate_run: %s\n---\n# v\n" % run)
    # 3c. NO-SLATE route (RP-P3): draft.md without source_slate + a minted-run sheet
    #     (slate_run: none, working_text: draft.md, ready) → execute-only keyed on the minted id;
    #     the slate-keyed sheet for `run` is NOT picked. 3d: same sheet not ready → full + WARN.
    draft_keep = read(os.path.join(ch, "draft.md"))
    write(os.path.join(ch, "draft.md"), "---\ntype: chapter-draft\nstatus: author-pass\n---\n\nShe walked.\n")
    ns = "2026-09-02-01"
    nvp = os.path.join(ch, "spec-check", ns, "verdicts.md")
    write(nvp, "---\nslate_run: none — no slate leg\nrun_id: %s\nsource: draft.md (author-pass)\nworking_text: draft.md\nstatus: ready\n---\n# v\n" % ns)
    f = Findings(); r = cmd_resolve(args(), f, quiet=True)
    if (not r or r["mode"] != "execute-only" or r["source_slate"] != ns or r["verdicts"] != "spec-check/%s/verdicts.md" % ns
            or not f.has("INFO", "NO-SLATE") or f.has("WARN", "WORKING")):
        fails.append("resolve#3c (no-slate): %r %r %s" % (r and r["mode"], r and r["source_slate"], f.items))
    write(nvp, "---\nslate_run: none — no slate leg\nsource: draft.md\nworking_text: draft.md\nstatus: draft\n---\n# v\n")
    f = Findings(); r = cmd_resolve(args(), f, quiet=True)
    if not r or r["mode"] != "full" or r["source_slate"] is not None or not f.has("WARN", "WORKING"):
        fails.append("resolve#3d (no-slate, not ready): %r %r" % (r and r["mode"], r and r["source_slate"]))
    os.remove(nvp); os.rmdir(os.path.dirname(nvp))
    write(os.path.join(ch, "draft.md"), draft_keep)
    # 4. new → rev1 + note, parse back, key set, fills present, spans pre-enumerated
    f = Findings(); r = cmd_new(args(), f)
    if not r or f.worst() == "ERROR":
        fails.append("new: %s" % f.items)
    else:
        rev, note = r["files"]
        if not rev.endswith("2026-09-02-the-road+the-hut-rev1.md"):
            fails.append("new: rev name %s (segments are reachable through draft.md's source_slate)" % os.path.basename(rev))
        d, _, err = parse_frontmatter(read(rev))
        if err or [k for k in REV_KEYS if k not in d] or d.get("source_slate") != run or d.get("mode") != "execute-only":
            fails.append("new: rev fm %r %r" % (err, d))
        nd, _, err = parse_frontmatter(read(note))
        rows = (nd or {}).get("protected_spans_touched")
        if err or not isinstance(rows, list) or len(rows) != 2 or rows[0].get("span") != "the pillow of her tongue":
            fails.append("new: note rows %r %r" % (err, rows))
        if (nd or {}).get("drift", {}).get("contamination", "").startswith("n/a") is False:
            fails.append("new: contamination should be n/a (no checklist in fixture): %r" % (nd or {}).get("drift"))
        # 5. check on stubs → FILL errors, then fill and pass; then a false kept
        f2 = Findings(); cmd_check(type("A", (), {"file": rev})(), f2)
        if not f2.has("ERROR", "FILL"):
            fails.append("check(stub): FILL residue not flagged")
        write(rev, read(rev).replace("<<FILL: gear the register chose>>", "POLISHED")
              .replace("<<FILL: the revised passage — clean prose only; keep the register's [unclear: …] marks>>",
                       "She walked and the wet pillow of her tongue was dry."))
        body_note = read(note)
        body_note = re.sub(r"'?<<FILL[^>]*>>'?", "x", body_note)
        if "  state: x" not in body_note:
            fails.append("fixture: placeholder substitution missed: %r" % body_note[:300])
        body_note = body_note.replace("- span: the pillow of her tongue\n  state: x", "- span: the pillow of her tongue\n  state: reworded\n  new: the wet pillow of her tongue")
        body_note = body_note.replace("- span: Been through worse\n  state: x", "- span: Been through worse\n  state: dropped\n  ruled: '2026-09-02'")
        write(note, body_note)
        f3 = Findings(); cmd_check(type("A", (), {"file": note})(), f3)
        if f3.worst() == "ERROR":
            fails.append("check(filled): %s" % [i for i in f3.items if i[0] == "ERROR"])
        # false kept: claim the dropped span was kept
        write(note, read(note).replace("  state: dropped\n  ruled: '2026-09-02'", "  state: kept"))
        f4 = Findings(); cmd_check(type("A", (), {"file": rev})(), f4)
        if not f4.has("ERROR", "KEPT"):
            fails.append("check(false kept): KEPT error not raised: %s" % f4.items)
        # unaccounted span: remove a row entirely
        write(note, read(note).replace("- span: Been through worse\n  state: kept\n", ""))
        f5 = Findings(); cmd_check(type("A", (), {"file": rev})(), f5)
        if not any(c == "SPANS" and "unaccounted" in m for s, c, m in f5.items if s == "ERROR"):
            fails.append("check(unaccounted): not raised: %s" % f5.items)
    # 6. second new same slug → rev2; sweep → sweep1 note only, rev counter untouched
    f = Findings(); r2 = cmd_new(args(), f)
    if not r2 or not r2["files"][0].endswith("-rev2.md"):
        fails.append("new#2: %r" % (r2 and r2["files"]))
    f = Findings(); r3 = cmd_new(args(sweep=True), f)
    if not r3 or len(r3["files"]) != 1 or not r3["files"][0].endswith("-sweep1-note.md"):
        fails.append("sweep: %r" % (r3 and r3["files"]))
    else:
        sn = r3["files"][0]
        f6 = Findings(); cmd_check(type("A", (), {"file": sn})(), f6)
        if not f6.has("INFO", "SWEEP") or f6.has("ERROR", "PAIR"):
            fails.append("check(sweep): %s" % f6.items)
        # 6b. sweep claims are verified against the WORKING TEXT (RP-P1): both spans kept → clean;
        #     a kept span that is not in draft.md → KEPT error; a missing row → unaccounted error
        st = re.sub(r"'?<<FILL[^>]*>>'?", "kept", read(sn))
        st = st.replace("## Checked\n\nkept", "## Checked\n\nall").replace("not earned\n\nkept", "not earned\n\nnone")
        write(sn, st)
        f6b = Findings(); cmd_check(type("A", (), {"file": sn})(), f6b)
        if f6b.worst() == "ERROR" or f6b.has("WARN", "SPANS"):
            fails.append("check(sweep filled): %s" % [i for i in f6b.items if i[0] != "INFO"])
        write(sn, read(sn).replace("- span: Been through worse\n  state: kept", "- span: Been through better\n  state: kept"))
        f6c = Findings(); cmd_check(type("A", (), {"file": sn})(), f6c)
        if not f6c.has("ERROR", "KEPT") or not any(c == "SPANS" and "unaccounted" in m for s, c, m in f6c.items if s == "ERROR"):
            fails.append("check(sweep false kept): %s" % f6c.items)
        write(sn, read(sn).replace("- span: Been through better\n  state: kept\n", ""))
        f6d = Findings(); cmd_check(type("A", (), {"file": sn})(), f6d)
        if not any(c == "SPANS" and "unaccounted" in m for s, c, m in f6d.items if s == "ERROR"):
            fails.append("check(sweep 1-of-2): not raised: %s" % f6d.items)
    f = Findings(); r4 = cmd_new(args(), f)
    if not r4 or not r4["files"][0].endswith("-rev3.md"):
        fails.append("new#3 after sweep: rev counter should be 3, got %r" % (r4 and r4["files"]))
    # 7. legacy path-form rev flags SOURCE-SLATE; legacy explains: key flagged on note
    leg = os.path.join(ch, "revisions", "2026-06-03-the-road+the-hut-rev1.md")
    write(leg, "---\ntype: chapter-revision\nchapter: CHAPTER 9 - TEST\nproject: FIX\nrev: 1\nkind: register\n"
               "source_slate: slate/%s/clean-draft.md\nworking_text: draft.md\nregister: REFERENCE/register.md\n"
               "register_title: X\nmode: full\nmaturity_gear: ROUGH\ngenerated: '2026-06-03 10:00'\n---\n\nprose\n" % run)
    write(leg[:-3] + "-note.md", "---\ntype: revision-note\nexplains: x\npairs_with: revisions/2026-06-03-the-road+the-hut-rev1.md\n"
                                  "protected_spans_touched: []\ndrift:\n  voice_spec: n/a\n  contamination: n/a\n---\n\nnote\n")
    f7 = Findings(); cmd_check(type("A", (), {"file": leg})(), f7)
    if not f7.has("WARN", "SOURCE-SLATE") or not any(c == "SCHEMA" and "explains" in m for _, c, m in f7.items):
        fails.append("check(legacy): %s" % f7.items)
    # 8. sentinel / register halts
    nov = os.path.join(tmp, "novault", "CHAPTERS", "CH")
    write(os.path.join(nov, "slate", "x.md"), "x")
    f8 = Findings()
    if cmd_resolve(args(chapter=nov), f8, quiet=True) is not None or not f8.has("ERROR", "SENTINEL"):
        fails.append("sentinel: should halt without _DIRECTIVES.md")
    noreg = os.path.join(vault, "WRITING", "PROJECTS", "BARE", "CHAPTERS", "CH")
    write(os.path.join(noreg, "slate", run, "clean-draft.md"), "---\nenvelope_segments: [a]\n---\nx\n")
    f9 = Findings()
    if cmd_resolve(args(chapter=noreg), f9, quiet=True) is not None or not f9.has("ERROR", "REGISTER"):
        fails.append("register: should halt without REFERENCE/register.md")

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
    r = sub.add_parser("resolve"); r.add_argument("--chapter", required=True); r.add_argument("--slate")
    n = sub.add_parser("new"); n.add_argument("--chapter", required=True); n.add_argument("--slate")
    n.add_argument("--sweep", action="store_true"); n.add_argument("--date", help="YYYY-MM-DD override (tests)")
    c = sub.add_parser("check"); c.add_argument("file")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.cmd:
        ap.error("one of: resolve / new / check / --selftest")
    f = Findings()
    out = {"resolve": cmd_resolve, "new": cmd_new, "check": cmd_check}[a.cmd](a, f)
    print(f.render("register_scaffold %s" % a.cmd))
    if out and a.cmd == "resolve":
        print("\n--- resolve ---\n" + out["_json"])
    if out and a.cmd == "new":
        print("\n--- _CHANGELOG stub ---\n" + out["vault_stub"] + "\n--- chapter changelog.md stub ---\n" + out["chapter_stub"])
    gate = any(c in ("SENTINEL", "CHAPTER", "FILE", "CONVENTION") for s, c, _ in f.items if s == "ERROR")
    if out is None and gate:
        sys.exit(2)
    sys.exit(1 if f.worst() == "ERROR" else 0)


if __name__ == "__main__":
    main()
