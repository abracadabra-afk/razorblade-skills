#!/usr/bin/env python3
"""episode-blueprint mechanical shell.

Three subcommands, all deterministic, none of them craft:

  scaffold  write an empty blueprint.md with serialized frontmatter (DIR-004).
            The ruled container numbers are ARGUMENTS, read from the strategy
            doc at run time by the skill; this script carries none of its own.
  check     lint a filled blueprint.md: frontmatter parses, every section is
            present in the ruled order, budgets sum to the target, the band
            verdict is consistent with the numbers, no prose-like lines, the
            notes section is last and below a rule.
  shape     read EPISODES/*/premise.md + blueprint.md frontmatter only and
            print the prior-episode shape table for the cross-episode read.
            Never reads triage.md or draft.md (corpus variety is premise-forge's;
            drafts are Pass 3 / scene-intensity territory).

Exit codes: 0 = pass / done, 1 = check failed, 2 = usage or I/O error.
"""

import argparse
import datetime as _dt
import pathlib
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required (DIR-004 serialized frontmatter). pip install pyyaml\n")
    sys.exit(2)

# ---------------------------------------------------------------- constants
# Section order = CRAFT BELIEFS "Character Arcs" chain, with Cast in front,
# Climax inserted before Outcome, and the three tool lines + notes at the foot.
# The order is structure, not craft: the craft text is read by path at run time.
SECTION_ORDER = [
    "Cast",
    "Flaw",
    "Incident",
    "Choice",
    "Escalations",
    "Moment of Truth",
    "Climax",
    "Outcome",
    "Variance",
    "Scope",
    "Recommendation",
    "Your notes",
]
BUDGETED_SECTIONS = ["Flaw", "Incident", "Choice", "Moment of Truth", "Climax", "Outcome"]
REQUIRED_FM = [
    "type", "episode", "target_words", "band_low", "band_high", "route_out_at",
    "natural_estimate", "scope_verdict", "recommendation", "ruling", "generated",
]
VERDICTS = {"SHORT-FORM", "OVER-BAND"}
RECS = {"GO", "RESHAPE", "ROUTE-OUT"}

BUDGET_RE = re.compile(r"\(~\s*(\d[\d,]*)\s*\)")
ESC_LINE_RE = re.compile(r"^\s*[-*]\s*\*\*E(\d+)\*\*")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
DIALOGUE_RE = re.compile(r"[\"“]([^\"”]{12,})[\"”]")
SPEECH_TAG_RE = re.compile(r"\b(said|says|asked|whispered|screamed|muttered|replied)\b", re.I)
HANDBACK_RE = re.compile(r"\[[^\]]*CRE\s*\]")  # a hand-back ends in CRE: [ANGLE MISSING — CRE]; a provenance note does not
PROSE_WORD_CEILING = 45  # a memorizable sentence plus its tags; longer reads as prose


# ---------------------------------------------------------------- helpers
def _split_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return None, text
    fm_text = parts[0][3:]
    body = parts[1]
    if body.startswith("\n"):
        body = body[1:]
    return fm_text, body


def _sections(body):
    """Return ordered list of (heading, [lines]) for ## headings."""
    out = []
    current = None
    for line in body.splitlines():
        m = HEADING_RE.match(line)
        if m:
            name = BUDGET_RE.sub("", m.group(1)).strip()  # "Flaw (~250)" -> "Flaw"
            current = (name, [])
            out.append(current)
        elif current is not None:
            current[1].append(line)
    return out


def _int(s):
    return int(str(s).replace(",", ""))


# ---------------------------------------------------------------- scaffold
def cmd_scaffold(a):
    out = pathlib.Path(a.out)
    if out.exists() and not a.force:
        sys.stderr.write(f"refusing to overwrite {out} (use --force)\n")
        return 2
    fm = {
        "type": "episode-blueprint",
        "episode": a.episode,
        "target_words": a.target,
        "band_low": a.band_low,
        "band_high": a.band_high,
        "route_out_at": a.route_out,
        "band_source": a.band_source,
        "natural_estimate": 0,
        "natural_weights": {},
        "scope_verdict": "SHORT-FORM",
        "recommendation": "GO",
        "ruling": "pending",
        "arc_class": "",
        "curve": "",
        "escalation_count": 0,
        "ending_mode": "",
        "sources_read": [],
        "prior_shape_read": [],
        "generated": _dt.date.today().isoformat(),
        "tool": "episode-blueprint",
        "note": "flow-kickstarter, not a spec (DIR-017 §2). Regenerate when premise.md moves (DIR-019 §1). No pass grades the draft against this.",
    }
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)
    # parse gate
    yaml.safe_load(fm_text)
    t = a.target
    body = f"""---
{fm_text}---
# {a.episode} · blueprint

**Knot:** [from premise § a — CRE's phrase]

## Cast
- [Name] — [knot-carrier | mirror | pressure | instrument]

## Flaw (~0)
[one sentence — what will not be surrendered]  [FAULT LINE]

## Incident (~0)
[one sentence — the event that opens the fault line]

## Choice (~0)
[one sentence — the decision that commits]

## Escalations
- **E1** (~0) — [one sentence] · angle: [angle on the flaw] · fails as: [false victory | fail forward]  [CURVE]
- **E2** (~0) — [one sentence] · angle: [angle] · fails as: [mode]  [CURVE]

## Moment of Truth (~0)
[one sentence — the choice the story cannot defer]

## Climax (~0)
[one sentence — the gated event]

## Outcome (~0)
inferred

## Variance
Within: [none | E_n and E_m share angle X] · Across: [none | matches EP NN shape: ...]

## Scope
cast [n] · conflict: [one phrase] · span: [bounded | stretches] · spines [n] · natural ~[n] → verdict [SHORT-FORM | OVER-BAND]

## Recommendation
[GO | RESHAPE | ROUTE-OUT] — [one-line basis]. Ruling: pending

---

## Your notes
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"scaffolded {out} (target {t}, band {a.band_low}-{a.band_high}, route-out {a.route_out})")
    return 0


# ---------------------------------------------------------------- check
def cmd_check(a):
    path = pathlib.Path(a.path)
    if not path.exists():
        sys.stderr.write(f"no such file: {path}\n")
        return 2
    text = path.read_text(encoding="utf-8")
    fails, infos = [], []

    # 1. frontmatter
    fm_text, body = _split_frontmatter(text)
    fm = {}
    if fm_text is None:
        fails.append("frontmatter: missing")
    else:
        try:
            fm = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError as e:
            fails.append(f"frontmatter: does not parse ({e.__class__.__name__})")
    if fm:
        for k in REQUIRED_FM:
            if k not in fm:
                fails.append(f"frontmatter: missing key {k}")
        if fm.get("type") != "episode-blueprint":
            fails.append("frontmatter: type must be episode-blueprint")
        if fm.get("scope_verdict") not in VERDICTS:
            fails.append(f"frontmatter: scope_verdict must be one of {sorted(VERDICTS)}")
        if fm.get("recommendation") not in RECS:
            fails.append(f"frontmatter: recommendation must be one of {sorted(RECS)}")

    # 2. sections + order
    secs = _sections(body)
    names = [s[0] for s in secs]
    for want in SECTION_ORDER:
        if want not in names:
            fails.append(f"section missing: {want}")
    present = [n for n in names if n in SECTION_ORDER]
    if present != [s for s in SECTION_ORDER if s in present]:
        fails.append(f"section order wrong: {present}")
    if names and names[-1] != "Your notes":
        fails.append("Your notes must be the last section (the tool never writes below it)")

    # rule before Your notes
    lines = body.splitlines()
    def _hname(ln):
        m = HEADING_RE.match(ln)
        return BUDGET_RE.sub("", m.group(1)).strip() if m else None

    for i, ln in enumerate(lines):
        if _hname(ln) == "Your notes":
            above = [x.strip() for x in lines[:i] if x.strip()]
            if not above or above[-1] != "---":
                fails.append("Your notes must sit below a --- rule")
            break

    # 3. budgets
    secmap = {n: ls for n, ls in secs}
    budgets = {}
    for n in BUDGETED_SECTIONS:
        heading_line = next((ln for ln in lines if _hname(ln) == n), "")
        m = BUDGET_RE.findall(heading_line)
        if len(m) != 1:
            fails.append(f"budget: {n} needs exactly one (~N) on its heading, found {len(m)}")
        else:
            budgets[n] = _int(m[0])
    esc_lines = [ln for ln in secmap.get("Escalations", []) if ESC_LINE_RE.match(ln)]
    if not esc_lines:
        fails.append("Escalations: no E lines (- **E1** (~N) — ...)")
    for ln in esc_lines:
        k = f"E{ESC_LINE_RE.match(ln).group(1)}"
        m = BUDGET_RE.findall(ln)
        if len(m) != 1:
            fails.append(f"budget: {k} needs exactly one (~N)")
        else:
            budgets[k] = _int(m[0])
        if "angle:" not in ln and not re.search(r"ANGLE MISSING", ln):
            fails.append(f"{k}: no angle: token and no [ANGLE MISSING — CRE] hand-back tag")
    total = sum(budgets.values())
    target = _int(fm.get("target_words", 0)) if fm else 0
    if fm and abs(total - target) > a.tolerance:
        fails.append(f"budgets sum to {total}, target is {target} (tolerance ±{a.tolerance})")
    else:
        infos.append(f"budgets sum to {total} against target {target}")

    # 4. band consistency (numbers come from frontmatter, never from here)
    if fm and all(k in fm for k in ("natural_estimate", "band_high", "route_out_at", "band_low")):
        nat = _int(fm["natural_estimate"])
        hi, ro, lo = _int(fm["band_high"]), _int(fm["route_out_at"]), _int(fm["band_low"])
        verdict, rec = fm.get("scope_verdict"), fm.get("recommendation")
        if nat >= ro:
            if verdict != "OVER-BAND":
                fails.append(f"natural {nat} ≥ route-out {ro}: scope_verdict must be OVER-BAND")
            if rec != "ROUTE-OUT":
                fails.append(f"natural {nat} ≥ route-out {ro}: recommendation must be ROUTE-OUT (CRE may rule otherwise; the tool recommends per §3b)")
        elif nat > hi:
            if verdict != "OVER-BAND":
                fails.append(f"natural {nat} > band_high {hi}: scope_verdict must be OVER-BAND")
            if rec not in ("RESHAPE", "ROUTE-OUT"):
                fails.append(f"natural {nat} > band_high {hi}: recommendation must be RESHAPE or ROUTE-OUT")
        else:
            if verdict == "OVER-BAND":
                fails.append(f"natural {nat} ≤ band_high {hi} but scope_verdict is OVER-BAND")
            if nat < lo:
                infos.append(f"natural {nat} < band_low {lo}: under band (informational; under is not gated at plan time)")
        if nat == 0:
            fails.append("natural_estimate is 0 (unfilled)")
        nw = fm.get("natural_weights")
        if isinstance(nw, dict) and nw:
            try:
                nws = sum(_int(v) for v in nw.values())
                if nws != nat:
                    fails.append(f"natural_weights sum to {nws} but natural_estimate is {nat}")
                else:
                    infos.append(f"natural_weights sum to {nws} (= natural_estimate)")
            except (TypeError, ValueError):
                fails.append("natural_weights must be a mapping of section -> integer")
        else:
            infos.append("natural_weights not recorded; natural_estimate is unaudited (record the per-section weights so the verdict can be traced)")
        m = re.search(r"natural\s*~\s*(\d[\d,]*)", "\n".join(secmap.get("Scope", [])))
        if m and _int(m.group(1)) != nat:
            fails.append(f"Scope line natural ~{m.group(1)} disagrees with frontmatter natural_estimate {nat}")
        if verdict and verdict not in "\n".join(secmap.get("Scope", [])):
            fails.append("Scope line does not carry the frontmatter scope_verdict")
        if rec and not "\n".join(secmap.get("Recommendation", [])).lstrip().startswith(rec):
            fails.append("Recommendation line does not start with the frontmatter recommendation")

    # 5. prose-like lines (heuristic; see the not-checked line below)
    movement_secs = ["Flaw", "Incident", "Choice", "Escalations", "Moment of Truth", "Climax", "Outcome"]
    for n in movement_secs:
        for ln in secmap.get(n, []):
            s = ln.strip()
            if not s:
                continue
            if DIALOGUE_RE.search(s):
                fails.append(f"prose-like ({n}): quoted speech — {s[:60]}…")
            if SPEECH_TAG_RE.search(s) and ("\"" in s or "“" in s):
                fails.append(f"prose-like ({n}): speech tag with quote — {s[:60]}…")
            words = len(re.sub(r"\[[^\]]*\]", "", s).split())
            if words > PROSE_WORD_CEILING:
                fails.append(f"prose-like ({n}): {words} words, ceiling {PROSE_WORD_CEILING} — {s[:60]}…")
            if s.count(".") >= 3:
                fails.append(f"prose-like ({n}): several sentences on one movement — {s[:60]}…")

    # 6. hand-backs (informational: these are the sections the tool returned to CRE)
    hb = [ln.strip() for ln in body.splitlines() if HANDBACK_RE.search(ln)]
    if hb:
        infos.append(f"{len(hb)} hand-back tag(s) to CRE: " + " | ".join(h[:50] for h in hb))

    # 7. placeholders left from the scaffold
    zero_budgets = [ln.strip()[:40] for ln in lines if "(~0)" in ln and _hname(ln) != "Outcome"]
    if re.search(r"\[one sentence", body) or zero_budgets:
        fails.append("scaffold placeholders remain ([one sentence …] or a (~0) outside Outcome): " + " | ".join(zero_budgets))

    # report
    for f in fails:
        print(f"FAIL  {f}")
    for i in infos:
        print(f"info  {i}")
    print("not checked: whether a sentence is CRE's articulated material or an invented beat; "
          "whether two angles are the same angle (a reasoning call); whether the natural weights are honest. "
          "Those are the attended gate's job (DIR-018).")
    print("PASS" if not fails else f"FAILED ({len(fails)})")
    return 0 if not fails else 1


# ---------------------------------------------------------------- shape
def cmd_shape(a):
    root = pathlib.Path(a.episodes_dir)
    if not root.is_dir():
        sys.stderr.write(f"not a directory: {root}\n")
        return 2
    rows = []
    for ep in sorted(p for p in root.iterdir() if p.is_dir()):
        row = {"episode": ep.name}
        for fname in ("premise.md", "blueprint.md"):
            f = ep / fname
            if not f.exists():
                row[fname] = None
                continue
            fm_text, _ = _split_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
            try:
                row[fname] = yaml.safe_load(fm_text) or {} if fm_text else {}
            except yaml.YAMLError:
                row[fname] = {"_error": "frontmatter does not parse"}
        rows.append(row)
    if not rows:
        print("no episode folders found")
        return 0
    print("prior-episode shape (frontmatter of premise.md + blueprint.md only)")
    for r in rows:
        p, b = r.get("premise.md"), r.get("blueprint.md")
        print(f"\n{r['episode']}")
        if p is None:
            print("  premise.md: none")
        else:
            keys = [k for k in ("knot", "condition", "structural_model", "antagonist", "container", "tier") if k in p]
            if not keys:
                print("  premise.md: frontmatter carries none of the shape keys — read § a by hand")
            for k in keys:
                print(f"  premise.{k}: {str(p[k])[:110]}")
        if b is None:
            print("  blueprint.md: none — shape (arc class, curve, escalation count, ending mode) not derivable "
                  "from frontmatter; read premise.md § a by hand for the cross-episode comparison")
        else:
            for k in ("arc_class", "curve", "escalation_count", "ending_mode", "scope_verdict", "recommendation", "ruling"):
                if k in b:
                    print(f"  blueprint.{k}: {b[k]}")
    print("\nnot read: triage.md (premise-forge's corpus), draft.md (Pass 3 / scene-intensity), notes.md")
    return 0


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(prog="blueprint.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scaffold", help="write an empty blueprint.md with serialized frontmatter")
    s.add_argument("--episode", required=True, help='e.g. "EP 04 - TITLE"')
    s.add_argument("--out", required=True, help="path to blueprint.md")
    s.add_argument("--target", type=int, required=True, help="center target words (from strategy §3b)")
    s.add_argument("--band-low", type=int, required=True)
    s.add_argument("--band-high", type=int, required=True)
    s.add_argument("--route-out", type=int, required=True, help="the routes-out-at-conception threshold")
    s.add_argument("--band-source", default="BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY §3b")
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_scaffold)

    c = sub.add_parser("check", help="lint a filled blueprint.md")
    c.add_argument("path")
    c.add_argument("--tolerance", type=int, default=25, help="allowed |sum - target| (rounding slack)")
    c.set_defaults(fn=cmd_check)

    h = sub.add_parser("shape", help="print prior-episode shape from premise.md + blueprint.md frontmatter")
    h.add_argument("episodes_dir")
    h.set_defaults(fn=cmd_shape)

    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
