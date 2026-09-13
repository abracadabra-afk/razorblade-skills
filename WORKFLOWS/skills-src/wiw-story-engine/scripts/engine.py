#!/usr/bin/env python3
"""wiw-story-engine mechanical shell.

Deterministic only. No craft lives here; the craft is CRE's and is read by path.

  scaffold-triage   write an empty CANDIDATES/<TITLE>/triage.md (Step 1 bank entry)
  scaffold-spine    write an empty EPISODES/EP NN/spine.md (Steps 2-3 per-piece file)
  check-triage      lint a filled triage.md: frontmatter parses, sections present,
                    premise carries no pattern words ("keeps", "always"), shape is
                    from the ruled list, promise mapping has five lines
  check-spine       lint a filled spine.md: frontmatter parses, sections present in
                    order, every slot filled or [NOT NAMED — CRE], Inescapable names
                    force AND truth, Story has do-this AND or-else, setting is 3-4
                    lines each tied force|truth, every escalation has trigger /
                    therefore / but+denies / penalty+subtracts, penalties are
                    distinct, budgets sum, band verdict matches the sum, promise
                    mapping present, Your notes last below a rule, no placeholders
  budget            deterministic per-section split (Opening / E1..En / Climax /
                    Cut / Pay-off 0) over the band midpoint when CRE gives no
                    numbers; presented for one-tap ratify, his numbers replace it
  bag               print the bag census: live candidates, ages, status, 90-day
                    re-gut flags, count against cap and min-fill

Two result classes, on purpose:
  FAIL  structural — the file is not in the shape the route reads. Exit 1.
  FLAG  content the check can see but CRE rules — dread, band, a thin penalty.
        Exit 0. A flag is never a veto (CRE's gut outranks the check).

Exit codes: 0 = pass (flags allowed), 1 = structural fail, 2 = usage or I/O error.
"""

import argparse
import datetime as _dt
import io
import pathlib
import re
import sys

# console-encoding-safe (DIR-020): the vault's arrows and dashes crash cp1252
for _s in ("stdout", "stderr"):
    _f = getattr(sys, _s)
    if hasattr(_f, "reconfigure"):
        try:
            _f.reconfigure(encoding="utf-8")
        except Exception:  # pragma: no cover
            pass
    elif hasattr(_f, "buffer"):  # pragma: no cover
        setattr(sys, _s, io.TextIOWrapper(_f.buffer, encoding="utf-8"))

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required (DIR-004 serialized frontmatter). pip install pyyaml\n")
    sys.exit(2)

# ---------------------------------------------------------------- constants
NN = "[NOT NAMED — CRE]"
NN_RE = re.compile(r"\[NOT NAMED\s*[—-]\s*CRE\]")
HEADING2_RE = re.compile(r"^##\s+(.+?)\s*$")
HEADING3_RE = re.compile(r"^###\s+(.+?)\s*$")
BUDGET_RE = re.compile(r"\(~\s*(\d[\d,]*)\s*\)")
DIALOGUE_RE = re.compile(r"[\"“]([^\"”]{12,})[\"”]")
PLACEHOLDER_RE = re.compile(r"\[(his (words|sentence|phrase)|one sentence|the (first|last)|what (it|she|he)|CRE's words)[^\]]*\]", re.I)
PATTERN_WORDS_RE = re.compile(r"\b(keeps?|always|every (night|day|morning|time)|each (night|day|time)|has been (hearing|seeing|finding)|used to)\b", re.I)
DECLARED_WANT_RE = re.compile(r"\b(wants? to|wanted to|wishes to|hopes to|needs to)\b", re.I)
ERA_REGION_CLASS_RE = re.compile(r"\b(era|region|class|decade|19\d0s|20\d0s|working-class|middle-class|upper-class|rural|urban|suburban)\b", re.I)

SHAPES = [
    "slow burn", "single incident", "twist/reveal", "twist", "reveal", "circular",
    "frame story", "frame", "epistolary", "cat-and-mouse", "cat and mouse",
    "dread curve", "slow burn to sudden shock", "kishōtenketsu", "kishotenketsu",
]
MAPPING_KEYS = ["dread", "fresh wound", "destruction", "compelled to watch", "no agency"]

TRIAGE_SECTIONS = ["Premise", "Promise", "Shape", "Container", "TOS band / tier", "Promise read", "Variety note"]
TRIAGE_FM = ["type", "working_title", "author", "source", "subgenre", "shape", "format", "triaged", "status", "gut"]

SPINE_SECTIONS = ["Step 2 — Want vs Inescapability", "Step 3 — Escalations", "Checks", "Stamp", "Your notes"]
STEP2_SLOTS = ["Want", "Rationale", "Inescapable", "Story", "Setting"]
SPINE_FM = ["type", "episode", "source_candidate", "shape", "status", "step", "run", "band_low", "band_high",
            "band_source", "budget_total", "band_verdict", "escalation_count", "generated", "tool"]
STATUSES = {"draft", "stamped"}
VERDICTS = {"IN-BAND", "UNDER-BAND", "OVER-BAND"}
ESC_RE = re.compile(r"^E(\d+)\b")
STOPWORDS = set("the a an of to in on at and or his her he she it its they them their is was be been that this with for from by as not no into out up off".split())


# ---------------------------------------------------------------- helpers
def _split_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return None, text
    body = parts[1]
    if body.startswith("\n"):
        body = body[1:]
    return parts[0][3:], body


def _sections(body, level_re):
    out, current = [], None
    for line in body.splitlines():
        m = level_re.match(line)
        if m:
            current = (BUDGET_RE.sub("", m.group(1)).strip(), [])
            out.append(current)
        elif current is not None:
            current[1].append(line)
    return out


def _int(s):
    return int(str(s).replace(",", ""))


def _content_words(s):
    return {w for w in re.findall(r"[a-zA-Z']+", s.lower()) if w not in STOPWORDS and len(w) > 2}


def _filled(text):
    """Slot has CRE's words (non-empty, not the hand-back, not a placeholder)."""
    t = text.strip()
    return bool(t) and not NN_RE.search(t) and not PLACEHOLDER_RE.search(t)


def _hole_tokens(h):
    """Loose match for a hole on the Checks 'stamp —' line: the runs name holes in
    free form ('E1 denies', 'Setting placing facts', 'Inescapable · truth')."""
    if h == "Setting.placing-facts":
        return ["placing facts"]
    if h == "Setting.detail":
        return ["setting"]
    if "." in h:
        head, tail = h.lower().split(".", 1)
        return [tail] if head in ("inescapable", "story") else [head, tail]
    return [h.lower()]


def _load_fm(text, fails):
    fm_text, body = _split_frontmatter(text)
    fm = {}
    if fm_text is None:
        fails.append("frontmatter: missing")
        return fm, body
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        fails.append(f"frontmatter: does not parse ({e.__class__.__name__})")
    return fm, body


def _dump_fm(fm):
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)
    yaml.safe_load(fm_text)  # parse gate (DIR-004)
    return fm_text


def _report(fails, flags, infos, not_checked):
    for f in fails:
        print(f"FAIL  {f}")
    for f in flags:
        print(f"FLAG  {f}")
    for i in infos:
        print(f"info  {i}")
    print("not checked: " + not_checked + " Those are CRE's gate (DIR-018).")
    if fails:
        print(f"FAILED ({len(fails)} structural) · {len(flags)} flag(s)")
        return 1
    print(f"PASS · {len(flags)} flag(s)")
    return 0


# ---------------------------------------------------------------- scaffold-triage
def cmd_scaffold_triage(a):
    out = pathlib.Path(a.out)
    if out.exists() and not a.force:
        sys.stderr.write(f"refusing to overwrite {out} (use --force)\n")
        return 2
    title = a.title or NN
    fm = {
        "type": "candidate-triage",
        "working_title": title,
        "working_title_placeholder": a.title is None,
        "author": "Chad Ryan",
        "source": f"wiw-story-engine Step 1 ({a.mode}) {_dt.date.today().isoformat()}",
        "subgenre": a.subgenre or NN,
        "shape": a.shape or NN,
        "format": "short-form",
        "triaged": _dt.date.today().isoformat(),
        "gut": a.gut or "SPARK",
        "status": "banked premise — awaiting CRE pick + episode-init gate",
        "model": "wiw-story-engine v1 — premise = witnessed instance, promise = dread compact; no knot field (the wound is the premise)",
    }
    body = f"""---
{_dump_fm(fm)}---
# {title} — forged premise

## Premise
[his words — one witnessed instance, the reader in the room the first time it happens]

## Promise
[his words — the dread compact: the wrongness the reader is now waiting for]

## Shape
{a.shape or NN}

## Container
[why this holds inside 2,000–2,800: one intrusion on the reader's own world, one spine, a bounded span, no mechanism to teach]

## TOS band / tier
[best pre-read: free-tier / age-restricted / never → FULL / SAFE-CUT / TEASE rec — episode-init re-rules at gate]

## Promise read
- dread — [what bad thing the reader feels coming | thin — {NN}]
- fresh wound — [the witnessed instance, on the page in story-present | thin — {NN}]
- destruction — [what the or-else will cost | thin — {NN}]
- compelled to watch — [why the reader stays in the room | thin — {NN}]
- no agency — [what refuses the character | thin — {NN}]

## Variety note
[what this adds against the worked corpus — sub-genre + shape, under the horror promise]
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"scaffolded {out}")
    return 0


# ---------------------------------------------------------------- scaffold-spine
def cmd_scaffold_spine(a):
    out = pathlib.Path(a.out)
    if out.exists() and not a.force:
        sys.stderr.write(f"refusing to overwrite {out} (use --force; a re-run carries ## Your notes verbatim)\n")
        return 2
    fm = {
        "type": "episode-spine",
        "episode": a.episode,
        "source_candidate": a.candidate,
        "shape": a.shape or NN,
        "subgenre": a.subgenre or NN,
        "status": "draft",
        "step": 2,
        "run": 1,
        "band_low": a.band_low,
        "band_high": a.band_high,
        "band_source": a.band_source,
        "budget_total": 0,
        "band_verdict": "UNDER-BAND",
        "escalation_count": a.escalations,
        "checks": {},
        "stamped": "",
        "sources_read": [],
        "generated": _dt.date.today().isoformat(),
        "tool": "wiw-story-engine",
        "note": "Replaces shape.md + blueprint.md on the WIW route. Plan precedes prose; never graded against draft.md (DIR-017, DIR-019). Re-run after S2 carries ## Your notes verbatim.",
    }
    esc = "\n".join(
        f"""### E{i} (~0)
- trigger — {NN}
- therefore — {NN}
- but — {NN} · denies: {NN}
- penalty — {NN} · subtracts: {NN}
"""
        for i in range(1, a.escalations + 1)
    )
    body = f"""---
{_dump_fm(fm)}---
# {a.episode} · spine

**Premise:** [verbatim from triage § Premise]
**Promise:** [verbatim from triage § Promise]
**Shape:** {a.shape or NN}

## Step 2 — Want vs Inescapability

### Want
- first physical move — {NN}

### Rationale
- {NN}

### Inescapable
- force — {NN}
- truth — {NN}

### Story
- must — {NN}
- or else — {NN}

### Setting
- {NN} · force
- {NN} · truth
- {NN} · force
- placing facts — {NN}

## Step 3 — Escalations

### Opening (~0)
- the witnessed instance on the page, the want in the first move

{esc}
### Climax (~0)
- ultimate therefore — {NN}

### Cut (~0)
- last line on the page — {NN}

### Pay-off (~0)
- survives off the page — {NN}

## Checks
- promise mapping (Step 1) — pending
- promise mapping (pre-stamp) — pending
- inescapable names force and truth — pending
- setting 3–4, each tied — pending
- penalties subtract — pending
- budget — 0 · UNDER-BAND
- stamp — pending

## Stamp
status: draft

---

## Your notes
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"scaffolded {out} (band {a.band_low}-{a.band_high}, {a.escalations} escalation slots)")
    return 0


# ---------------------------------------------------------------- check-triage
def cmd_check_triage(a):
    path = pathlib.Path(a.path)
    if not path.exists():
        sys.stderr.write(f"no such file: {path}\n")
        return 2
    text = path.read_text(encoding="utf-8")
    fails, flags, infos = [], [], []
    fm, body = _load_fm(text, fails)
    if fm:
        for k in TRIAGE_FM:
            if k not in fm:
                fails.append(f"frontmatter: missing key {k}")
        if fm.get("type") != "candidate-triage":
            fails.append("frontmatter: type must be candidate-triage (episode-init reads this)")
        if fm.get("format") != "short-form":
            fails.append("frontmatter: format must be short-form (the bag stays shorts-pure)")
        if fm.get("gut") not in {"SPARK", "REWORK", "KILL"}:
            fails.append("frontmatter: gut must be SPARK | REWORK | KILL")
        elif fm.get("gut") != "SPARK":
            fails.append(f"frontmatter: gut is {fm.get('gut')} — only a SPARK banks")
        if fm.get("working_title_placeholder") and not NN_RE.search(str(fm.get("working_title", ""))):
            fails.append("frontmatter: working_title_placeholder true but working_title is not the hand-back")

    secs = _sections(body, HEADING2_RE)
    names = [s[0] for s in secs]
    for want in TRIAGE_SECTIONS:
        if want not in names:
            fails.append(f"section missing: {want}")
    secmap = {n: "\n".join(ls) for n, ls in secs}

    premise = secmap.get("Premise", "")
    promise = secmap.get("Promise", "")
    if not _filled(premise):
        fails.append("Premise: empty or placeholder")
    else:
        m = PATTERN_WORDS_RE.search(premise)
        if m:
            flags.append(f"Premise: pattern word '{m.group(0)}' — a witnessed instance is one moment, not a habit")
        if premise.count(".") >= 4:
            flags.append("Premise: four or more sentences — the instance is one moment")
    if not _filled(promise):
        fails.append("Promise: empty or placeholder")

    shape_raw = (secmap.get("Shape", "") or "").strip()
    shape = shape_raw.lower()
    fm_shape = str(fm.get("shape", "")).lower() if fm else ""
    if not shape or NN_RE.search(shape_raw):
        flags.append("Shape: not named — asked after the gut on SPARKs; a banked candidate can carry the hand-back")
    else:
        parts = [p.strip() for p in re.split(r"[+/,]| and ", shape) if p.strip()]
        unknown = [p for p in parts if p not in SHAPES]
        if unknown:
            flags.append(f"Shape: {unknown} not on the ruled list ({', '.join(SHAPES[:8])}…) — CRE may add a shape; recorded as his")
        if fm_shape and fm_shape != shape:
            fails.append("Shape: frontmatter shape disagrees with § Shape")

    pr = secmap.get("Promise read", "")
    found = {k: None for k in MAPPING_KEYS}
    for ln in pr.splitlines():
        s = ln.strip().lstrip("-* ").lower()
        for k in MAPPING_KEYS:
            if s.startswith(k):
                found[k] = ln
    for k, ln in found.items():
        if ln is None:
            fails.append(f"Promise read: no '{k}' line")
        else:
            rest = re.sub(r"^[-*\s]*" + re.escape(k) + r"\s*[—-]\s*", "", ln.strip(), flags=re.I)
            if not _filled(rest) or rest.lower().startswith("thin"):
                flags.append(f"Promise read: {k} is thin — a dread-less premise banks for Substack/anthology, not the weekly slot")

    for n in ("Container", "TOS band / tier", "Variety note"):
        if n in secmap and not _filled(secmap[n]):
            fails.append(f"{n}: empty or placeholder")
    if DIALOGUE_RE.search(premise + promise):
        flags.append("Premise/Promise: quoted speech — the sentence pre-spends the mic (CDIR-001)")

    return _report(fails, flags, infos,
                   "whether the premise sparks; whether the dread line is really dread or cruelty in an unbent world; "
                   "whether the sentence is CRE's ratified wording.")


# ---------------------------------------------------------------- check-spine
def cmd_check_spine(a):
    path = pathlib.Path(a.path)
    if not path.exists():
        sys.stderr.write(f"no such file: {path}\n")
        return 2
    text = path.read_text(encoding="utf-8")
    fails, flags, infos = [], [], []
    fm, body = _load_fm(text, fails)
    step = 2
    if fm:
        for k in SPINE_FM:
            if k not in fm:
                fails.append(f"frontmatter: missing key {k}")
        if fm.get("type") != "episode-spine":
            fails.append("frontmatter: type must be episode-spine")
        if fm.get("status") not in STATUSES:
            fails.append(f"frontmatter: status must be one of {sorted(STATUSES)}")
        if fm.get("band_verdict") not in VERDICTS:
            fails.append(f"frontmatter: band_verdict must be one of {sorted(VERDICTS)}")
        try:
            step = int(fm.get("step", 2))
        except (TypeError, ValueError):
            fails.append("frontmatter: step must be 2 or 3")
        if step not in (2, 3):
            fails.append("frontmatter: step must be 2 or 3")

    # sections + order
    secs2 = _sections(body, HEADING2_RE)
    names = [s[0] for s in secs2]
    for want in SPINE_SECTIONS:
        if want not in names:
            fails.append(f"section missing: {want}")
    present = [n for n in names if n in SPINE_SECTIONS]
    if present != [s for s in SPINE_SECTIONS if s in present]:
        fails.append(f"section order wrong: {present}")
    if names and names[-1] != "Your notes":
        fails.append("Your notes must be the last section (the tool never writes below it)")
    lines = body.splitlines()
    for i, ln in enumerate(lines):
        if HEADING2_RE.match(ln) and HEADING2_RE.match(ln).group(1).strip() == "Your notes":
            above = [x.strip() for x in lines[:i] if x.strip()]
            if not above or above[-1] != "---":
                fails.append("Your notes must sit below a --- rule")
            break

    sec2 = {n: "\n".join(ls) for n, ls in secs2}
    if "**Premise:**" not in body or "**Promise:**" not in body:
        fails.append("head: **Premise:** / **Promise:** lines missing — the promise is carried from sentence one")
    if re.search(r"\*\*Premise:\*\*\s*\[verbatim", body) or re.search(r"\*\*Promise:\*\*\s*\[verbatim", body):
        fails.append("head: Premise/Promise still the scaffold placeholder — copy from triage verbatim")

    # ---- Step 2
    s2 = _sections(sec2.get("Step 2 — Want vs Inescapability", ""), HEADING3_RE)
    s2map = {n: "\n".join(ls) for n, ls in s2}
    for slot in STEP2_SLOTS:
        if slot not in s2map:
            fails.append(f"Step 2: slot missing: {slot}")
    holes = []

    def _slot_lines(txt):
        return [l.strip().lstrip("-* ") for l in txt.splitlines() if l.strip().startswith(("-", "*"))]

    want = s2map.get("Want", "")
    wl = _slot_lines(want)
    wtext = re.sub(r"^first physical move\s*[—-]\s*", "", wl[0], flags=re.I) if wl else ""
    if not wl:
        fails.append("Want: no line")
    elif not _filled(wtext):
        holes.append("Want")
    elif DECLARED_WANT_RE.search(wtext):
        flags.append(f"Want: reads as a declaration ('{DECLARED_WANT_RE.search(wtext).group(0)}') — the want is shown in the first physical move")

    rl = _slot_lines(s2map.get("Rationale", ""))
    if not rl:
        fails.append("Rationale: no line")
    elif not _filled(rl[0]):
        holes.append("Rationale")

    inesc = s2map.get("Inescapable", "")
    force = truth = None
    for l in _slot_lines(inesc):
        if re.match(r"force\s*[—-]", l, re.I):
            force = re.sub(r"^force\s*[—-]\s*", "", l, flags=re.I)
        if re.match(r"truth\s*[—-]", l, re.I):
            truth = re.sub(r"^truth\s*[—-]\s*", "", l, flags=re.I)
    if force is None or truth is None:
        fails.append("Inescapable: needs a 'force —' line and a 'truth —' line")
    else:
        if not _filled(force):
            holes.append("Inescapable.force")
        if not _filled(truth):
            holes.append("Inescapable.truth")
        if _filled(force) and not _filled(truth):
            flags.append("Inescapable: force alone is a mechanism — the buried truth is not named")
        if _filled(truth) and not _filled(force):
            flags.append("Inescapable: truth alone is literary — the refusing force is not named")
        if _filled(force) and _filled(truth) and _content_words(force) == _content_words(truth):
            flags.append("Inescapable: force and truth are the same words — two halves, not one restated")

    story = s2map.get("Story", "")
    must = orelse = None
    for l in _slot_lines(story):
        if re.match(r"must\s*[—-]", l, re.I):
            must = re.sub(r"^must\s*[—-]\s*", "", l, flags=re.I)
        if re.match(r"or else\s*[—-]", l, re.I):
            orelse = re.sub(r"^or else\s*[—-]\s*", "", l, flags=re.I)
    if must is None or orelse is None:
        fails.append("Story: needs a 'must —' line and an 'or else —' line (do-this / or-else)")
    else:
        if not _filled(must):
            holes.append("Story.must")
        if not _filled(orelse):
            holes.append("Story.or-else")

    setting = s2map.get("Setting", "")
    details, placing = [], None
    for l in _slot_lines(setting):
        if re.match(r"placing facts\s*[—-]", l, re.I):
            placing = re.sub(r"^placing facts\s*[—-]\s*", "", l, flags=re.I)
        else:
            details.append(l)
    real = [d for d in details if _filled(d)]
    if len(details) < 3 or len(details) > 4:
        flags.append(f"Setting: {len(details)} detail line(s) — the model asks 3–4")
    for d in details:
        if _filled(d) and not re.search(r"·\s*(force|truth)\s*$", d, re.I):
            flags.append(f"Setting: detail not tied to force or truth — '{d[:50]}'")
        if not _filled(d):
            holes.append("Setting.detail")
    if placing is None:
        fails.append("Setting: needs a 'placing facts —' line ([NOT NAMED — CRE] until he says none needed or names them)")
    elif NN_RE.search(placing):
        holes.append("Setting.placing-facts")
    elif placing.strip().lower() not in ("none needed", "none") and not fm.get("placing_facts_needed"):
        flags.append("Setting: placing facts named but frontmatter placing_facts_needed is not true — era/region/class only when the premise needs them (DIR-017 §2)")
    for d in real:
        if ERA_REGION_CLASS_RE.search(d):
            flags.append(f"Setting: detail carries an era/region/class word — '{d[:50]}'")

    # ---- Step 3
    s3 = _sections(sec2.get("Step 3 — Escalations", ""), HEADING3_RE)
    s3map = {n: "\n".join(ls) for n, ls in s3}
    s3names = [n for n, _ in s3]
    esc_names = [n for n in s3names if ESC_RE.match(n)]
    budgets = {}
    heading_lines = [ln for ln in lines if HEADING3_RE.match(ln)]

    def _budget_of(name):
        for hl in heading_lines:
            if BUDGET_RE.sub("", HEADING3_RE.match(hl).group(1)).strip() == name:
                m = BUDGET_RE.findall(hl)
                return _int(m[0]) if len(m) == 1 else None
        return None

    if step == 3 or fm.get("status") == "stamped":
        for n in ("Opening", "Climax", "Cut", "Pay-off"):
            if n not in s3map:
                fails.append(f"Step 3: section missing: {n}")
        if not esc_names:
            fails.append("Step 3: no escalation blocks (### E1 (~N) …)")
        nums = [int(ESC_RE.match(n).group(1)) for n in esc_names]
        if nums != list(range(1, len(nums) + 1)):
            fails.append(f"Step 3: escalations must run E1..En contiguous, found {esc_names}")
        if fm and "escalation_count" in fm and _int(fm["escalation_count"]) != len(nums):
            fails.append(f"frontmatter: escalation_count {fm['escalation_count']} but {len(nums)} E blocks")
        order = ["Opening"] + esc_names + ["Climax", "Cut", "Pay-off"]
        if [n for n in s3names if n in order] != order:
            fails.append(f"Step 3: order must be Opening, E1..En, Climax, Cut, Pay-off — found {s3names}")

        penalties = []
        for en in esc_names:
            blk = s3map.get(en, "")
            parts = {}
            for l in _slot_lines(blk):
                m = re.match(r"(trigger|therefore|but|penalty)\s*[—-]\s*(.*)", l, re.I)
                if m:
                    parts[m.group(1).lower()] = m.group(2)
            for k in ("trigger", "therefore", "but", "penalty"):
                if k not in parts:
                    fails.append(f"{en}: no '{k} —' line")
                elif not _filled(parts[k].split("·")[0]):
                    holes.append(f"{en}.{k}")
            if "but" in parts:
                m = re.search(r"·\s*denies:\s*(.*)$", parts["but"], re.I)
                if not m:
                    fails.append(f"{en}: but line needs '· denies: <the assumption>'")
                elif not _filled(m.group(1)):
                    holes.append(f"{en}.denies")
            if "penalty" in parts:
                m = re.search(r"·\s*subtracts:\s*(.*)$", parts["penalty"], re.I)
                if not m:
                    fails.append(f"{en}: penalty line needs '· subtracts: <what is gone>'")
                else:
                    if not _filled(m.group(1)):
                        holes.append(f"{en}.subtracts")
                    else:
                        penalties.append((en, m.group(1).strip()))
            b = _budget_of(en)
            if b is None:
                fails.append(f"{en}: needs exactly one (~N) on its heading")
            else:
                budgets[en] = b
        # penalties subtract something new
        seen = []
        for en, p in penalties:
            cw = _content_words(p)
            for pen, pcw in seen:
                if cw and (cw == pcw or (len(cw & pcw) / max(1, len(cw)) >= 0.75)):
                    flags.append(f"{en}: subtracts the same thing as {pen} ('{p[:40]}') — escalation needs a new loss")
            seen.append((en, cw))

        for n in ("Opening", "Climax", "Cut", "Pay-off"):
            b = _budget_of(n)
            if b is None:
                fails.append(f"{n}: needs exactly one (~N) on its heading")
            else:
                budgets[n] = b
            ls = _slot_lines(s3map.get(n, ""))
            if n != "Opening":
                if not ls:
                    fails.append(f"{n}: no line")
                else:
                    val = re.sub(r"^(ultimate therefore|last line on the page|survives off the page)\s*[—-]\s*", "", ls[0], flags=re.I)
                    if not _filled(val):
                        holes.append(n)
        if budgets.get("Pay-off", 0) != 0:
            flags.append("Pay-off: budget should be (~0) — it survives off the page, it is not written")
        if budgets.get("Cut", 0) > 120:
            flags.append(f"Cut: (~{budgets['Cut']}) — the cut is the last line or two, not a section")

        total = sum(v for k, v in budgets.items() if k != "Pay-off")
        lo, hi = (_int(fm.get("band_low", 0)), _int(fm.get("band_high", 0))) if fm else (0, 0)
        verdict = "IN-BAND" if lo <= total <= hi else ("UNDER-BAND" if total < lo else "OVER-BAND")
        infos.append(f"budgets sum to {total} against band {lo}–{hi} → {verdict}")
        if fm:
            if _int(fm.get("budget_total", 0)) != total:
                fails.append(f"frontmatter: budget_total {fm.get('budget_total')} but sections sum to {total}")
            if fm.get("band_verdict") != verdict:
                fails.append(f"frontmatter: band_verdict {fm.get('band_verdict')} but the sum gives {verdict}")
        if verdict != "IN-BAND":
            flags.append(f"budget: {verdict} ({total}) — the band is prescriptive at plan time; CRE rules reshape or route-out")
        zero = [k for k, v in budgets.items() if v == 0 and k != "Pay-off"]
        if zero:
            fails.append(f"budget: (~0) left on {zero}")
        chk = sec2.get("Checks", "")
        m = re.search(r"budget\s*[—-]\s*(\d[\d,]*)\s*·\s*(IN-BAND|UNDER-BAND|OVER-BAND)", chk)
        if not m:
            fails.append("Checks: budget line must read 'budget — N · VERDICT'")
        elif _int(m.group(1)) != total or m.group(2) != verdict:
            fails.append(f"Checks: budget line says {m.group(1)} · {m.group(2)} but the sum gives {total} · {verdict}")
        if "pending" in re.sub(r"promise mapping \(Step 1\).*", "", chk):
            if fm.get("status") == "stamped":
                fails.append("Checks: a stamped spine cannot carry a pending check")
            else:
                flags.append("Checks: a check is still pending")
    else:
        infos.append("step 2 file: Step 3 blocks not linted (run again with step: 3 once escalations are recorded)")
        chk = sec2.get("Checks", "")

    # ---- Checks section shape
    for label in ("promise mapping (Step 1)", "promise mapping (pre-stamp)", "inescapable names force and truth",
                  "setting 3–4, each tied", "penalties subtract", "budget"):
        if label not in chk:
            fails.append(f"Checks: line missing: {label}")
    for ln in chk.splitlines():
        if re.search(r"\bFLAG\b", ln):
            flags.append(f"Checks (recorded): {ln.strip().lstrip('-* ')[:90]}")

    # ---- stamp
    stamp = sec2.get("Stamp", "")
    if fm.get("status") == "stamped":
        if not re.search(r"status:\s*stamped\s*[—-]\s*CRE,\s*\d{4}-\d{2}-\d{2}", stamp):
            fails.append("Stamp: stamped status needs 'status: stamped — CRE, YYYY-MM-DD'")
        if not fm.get("stamped"):
            fails.append("frontmatter: stamped is empty on a stamped spine")
        if step != 3:
            fails.append("a stamped spine must be at step 3")
        if holes:
            flags.append(f"stamped with {len(holes)} hole(s) — {', '.join(holes[:6])} — CRE's call, recorded")
    else:
        if "status: draft" not in stamp:
            fails.append("Stamp: draft status needs 'status: draft'")
        # a draft with holes must carry them on the Checks 'stamp —' line: the deferral
        # record that routes without CRE remembering it (_ME working rule 1, DIR-012 §4)
        if holes and step == 3:
            stamp_line = next((ln for ln in chk.splitlines() if re.match(r"^\s*[-*]\s*stamp\s*[—-]", ln, re.I)), None)
            if stamp_line is None:
                fails.append("Checks: a draft spine with holes needs a 'stamp —' line listing every [NOT NAMED — CRE] hole by slot")
            else:
                low = stamp_line.lower()
                missing = [h for h in set(holes) if not all(t in low for t in _hole_tokens(h))]
                if missing:
                    flags.append(f"Checks: stamp line does not list hole(s) {sorted(missing)}")

    # ---- prose-like lines
    plan = sec2.get("Step 2 — Want vs Inescapability", "") + "\n" + sec2.get("Step 3 — Escalations", "")
    for ln in plan.splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if DIALOGUE_RE.search(s):
            flags.append(f"prose-like: quoted speech — '{s[:50]}' (the plan pre-spends the mic, CDIR-001)")
        if len(re.sub(r"\[[^\]]*\]", "", s).split()) > 60:
            flags.append(f"prose-like: {len(s.split())} words on one line — '{s[:50]}'")
    if PLACEHOLDER_RE.search(plan):
        fails.append("scaffold placeholders remain in the plan")
    if holes:
        infos.append(f"{len(holes)} hand-back(s) to CRE: " + ", ".join(holes))

    return _report(fails, flags, infos,
                   "whether a slot is CRE's words or an invented beat; whether a Therefore is really forced by its But; "
                   "whether the dread is dread; whether a penalty is a real loss or a restatement.")


# ---------------------------------------------------------------- budget
def derive_budget(n_esc, band_low, band_high):
    """Deterministic split when CRE gives no numbers. Arithmetic, not story.

    Template over the band midpoint: Opening 14% · escalations 62% (rising, each
    E 50 words more than the last) · Climax 20% · Cut 4% · Pay-off 0. Every figure
    rounds to 50; the rounding remainder lands on Climax so the sum is exact and
    inside the band. Two runs on the same inputs return the same split.
    """
    mid = (band_low + band_high) // 2
    r50 = lambda x: int(round(x / 50.0)) * 50
    opening = r50(mid * 0.14)
    cut = max(50, r50(mid * 0.04))
    esc_total = mid * 0.62
    base = r50((esc_total - 50 * n_esc * (n_esc - 1) / 2) / n_esc) if n_esc else 0
    escs = [base + 50 * i for i in range(n_esc)]
    climax = r50(mid * 0.20)
    total = opening + sum(escs) + climax + cut
    # exact-sum + band guard: push the remainder onto Climax
    target = r50(mid)
    climax += target - total
    if climax < 50:
        climax = 50
    out = {"Opening": opening}
    out.update({f"E{i + 1}": v for i, v in enumerate(escs)})
    out.update({"Climax": climax, "Cut": cut, "Pay-off": 0})
    return out


def cmd_budget(a):
    b = derive_budget(a.escalations, a.band_low, a.band_high)
    total = sum(v for k, v in b.items() if k != "Pay-off")
    verdict = "IN-BAND" if a.band_low <= total <= a.band_high else ("UNDER-BAND" if total < a.band_low else "OVER-BAND")
    for k, v in b.items():
        print(f"{k:<8} (~{v})")
    print(f"total    {total} · {verdict} · band {a.band_low}–{a.band_high} · derived, one-tap ratify (CRE's numbers replace these)")
    return 0


# ---------------------------------------------------------------- bag
def cmd_bag(a):
    root = pathlib.Path(a.candidates_dir)
    if not root.is_dir():
        sys.stderr.write(f"not a directory: {root}\n")
        return 2
    today = _dt.date.today()
    live, spent = [], []
    for c in sorted(p for p in root.iterdir() if p.is_dir()):
        t = c / "triage.md"
        if not t.exists():
            live.append((c.name, "?", "no triage.md", None, ""))
            continue
        fm_text, _ = _split_frontmatter(t.read_text(encoding="utf-8", errors="replace"))
        try:
            fm = yaml.safe_load(fm_text) or {} if fm_text else {}
        except yaml.YAMLError:
            fm = {"status": "frontmatter does not parse"}
        status = str(fm.get("status", ""))
        age = None
        for key in ("triaged", "created"):
            v = fm.get(key)
            if v:
                try:
                    age = (today - _dt.date.fromisoformat(str(v)[:10])).days
                except ValueError:
                    pass
                break
        model = "engine" if "wiw-story-engine" in str(fm.get("model", "")) + str(fm.get("source", "")) else "legacy"
        row = (c.name, str(fm.get("shape", fm.get("subgenre", "?"))), status, age, model)
        (spent if "promoted" in status else live).append(row)
    print(f"bag: {len(live)} live · {len(spent)} promoted (spent)")
    for name, shape, status, age, model in live:
        flag = ""
        if age is not None and age >= a.regut_days:
            flag = f"  [RE-GUT — {age}d, peg is a dated claim]"
        if model == "legacy":
            flag += "  [legacy triage — knot/what-if shape; engine reads Premise/Promise]"
        print(f"  {name:<28} {shape:<22} {age if age is not None else '?':>4}d  {status[:48]}{flag}")
    if len(live) >= a.cap:
        print(f"AT CAP ({a.cap}): lead with hygiene — retire or promote before forging")
    if len(live) < a.min_fill:
        print(f"BELOW MIN-FILL ({a.min_fill}): surface 'forge the story' to TASKS/TASKS.md so week-shape serves it")
    print("not read: triage bodies, EPISODES/, draft.md, SHORTS/DEV/")
    return 0


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(prog="engine.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scaffold-triage")
    s.add_argument("--out", required=True)
    s.add_argument("--title", default=None, help="CRE's working title; omit → [NOT NAMED — CRE] + placeholder flag")
    s.add_argument("--mode", default="FILL", choices=["FILL", "BRING"])
    s.add_argument("--subgenre", default=None)
    s.add_argument("--shape", default=None)
    s.add_argument("--gut", default="SPARK", choices=["SPARK", "REWORK", "KILL"])
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_scaffold_triage)

    s = sub.add_parser("scaffold-spine")
    s.add_argument("--out", required=True)
    s.add_argument("--episode", required=True, help='e.g. "EP 05 - TITLE"')
    s.add_argument("--candidate", required=True, help="path to the source triage.md")
    s.add_argument("--shape", default=None)
    s.add_argument("--subgenre", default=None)
    s.add_argument("--escalations", type=int, default=3)
    s.add_argument("--band-low", type=int, default=2000)
    s.add_argument("--band-high", type=int, default=2800)
    s.add_argument("--band-source", default="BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY §3b (2,000–2,800)")
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_scaffold_spine)

    c = sub.add_parser("check-triage")
    c.add_argument("path")
    c.set_defaults(fn=cmd_check_triage)

    c = sub.add_parser("check-spine")
    c.add_argument("path")
    c.set_defaults(fn=cmd_check_spine)

    g = sub.add_parser("budget", help="deterministic per-section split when CRE gives no numbers")
    g.add_argument("--escalations", type=int, default=3)
    g.add_argument("--band-low", type=int, default=2000)
    g.add_argument("--band-high", type=int, default=2800)
    g.set_defaults(fn=cmd_budget)

    b = sub.add_parser("bag")
    b.add_argument("candidates_dir")
    b.add_argument("--cap", type=int, default=12)
    b.add_argument("--min-fill", type=int, default=4)
    b.add_argument("--regut-days", type=int, default=90)
    b.set_defaults(fn=cmd_bag)

    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
