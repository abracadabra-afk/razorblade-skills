#!/usr/bin/env python3
"""episode-harden mechanical shell.

Three subcommands, all deterministic, none of them craft:

  scaffold   write an empty shape.md with serialized frontmatter (DIR-004).
             Rung count and anchor are ARGUMENTS the skill read from the
             blueprint; this script carries no story material of its own.
  check      lint a filled shape.md: frontmatter parses, every pillar section
             is present in walk order, rungs run DOWN from the top rung to E1
             with one resistance token each (or the hand-back tag), every entry
             carries exactly one status tag, no bare [recommended] survives on a
             ratified shape, no prose-like lines, no placeholders, the agenda
             is the last section.
  handbacks  print the [... — CRE] hand-back lines from a blueprint.md so the
             skill can seed the brainstorm agenda. Reads blueprint.md only.

Exit codes: 0 = pass / done, 1 = check failed, 2 = usage or I/O error.
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
# Walk order = the Character Arcs chain read from the summit down, then the
# derived sheets, then the agenda. Structure, not craft: craft is read by path.
SECTION_ORDER = [
    "Want",
    "Moment of Truth",
    "Ending",
    "Rungs",
    "Flaw",
    "Cast",
    "Setting",
    "Brainstorm agenda",
]
PILLAR_SECTIONS = ["Want", "Moment of Truth", "Ending", "Rungs", "Flaw"]
SHEET_SECTIONS = ["Cast", "Setting"]
TAGGED_SECTIONS = PILLAR_SECTIONS + SHEET_SECTIONS
REQUIRED_FM = [
    "type", "episode", "anchor_rung", "rung_count", "status", "sources_read", "generated",
]
STATUSES = {"draft", "ratified"}

TAG_RULED = "[ruled]"
TAG_REC = "[recommended]"
TAG_RAT = "[recommended → ratified]"
TAG_NN = "[NOT NAMED — CRE]"
TAGS = (TAG_RULED, TAG_REC, TAG_RAT, TAG_NN)
TAG_RE = re.compile(r"\[(ruled|recommended|recommended → ratified|NOT NAMED — CRE)\]")

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
RUNG_LINE_RE = re.compile(r"^\s*[-*]\s*\*\*E(\d+)\*\*")
BULLET_RE = re.compile(r"^\s*[-*]\s+\S")
DIALOGUE_RE = re.compile(r"[\"“]([^\"”]{12,})[\"”]")
SPEECH_TAG_RE = re.compile(r"\b(said|says|asked|whispered|screamed|muttered|replied)\b", re.I)
MULTI_SENTENCE_RE = re.compile(r"[.!?]\s+[A-Z]")
HANDBACK_RE = re.compile(r"\[[^\]]*CRE\s*\]")
PLACEHOLDER_RE = re.compile(r"\[(one sentence|his phrase|role / name|what she wants|the scope of)[^\]]*\]", re.I)
PROSE_WORD_CEILING = 45  # a one-sentence line plus its tag; longer reads as prose
RESISTANCE_TOKEN = "runs against:"


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
    """Ordered list of (heading, [lines]) for ## headings; text before the first ## is ('_head', [...])."""
    out = [("_head", [])]
    current = out[0]
    for line in body.splitlines():
        m = HEADING_RE.match(line)
        if m:
            current = (m.group(1).strip(), [])
            out.append(current)
        else:
            current[1].append(line)
    return out


def _strip_tags(s):
    return re.sub(r"\[[^\]]*\]", "", s)


# ---------------------------------------------------------------- scaffold
def cmd_scaffold(a):
    out = pathlib.Path(a.out)
    if out.exists() and not a.force:
        sys.stderr.write(f"refusing to overwrite {out} (use --force; a ratified shape is a ruling, amend it by hand)\n")
        return 2
    if a.rungs < 1:
        sys.stderr.write("--rungs must be at least 1\n")
        return 2
    fm = {
        "type": "episode-shape",
        "episode": a.episode,
        "anchor_rung": a.anchor or "",
        "rung_count": a.rungs,
        "curve": a.curve or "",
        "status": "draft",
        "ratified": "",
        "blueprint_run_read": a.blueprint_run,
        "sources_read": [],
        "generated": _dt.date.today().isoformat(),
        "tool": "episode-harden",
        "note": "structural commitment, not a spec. The brainstorm may wander from it; collisions surface via episode-feedback GATE COLLISION. Never regenerated — amended by CRE's ruling only.",
    }
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)
    yaml.safe_load(fm_text)  # parse gate
    rungs = "\n".join(
        f"- **E{n}** — [one sentence — the rung as the blueprint states it] · runs against: [one sentence — what her intentions, obfuscations, flaw meet here]  {TAG_NN}"
        for n in range(a.rungs, 0, -1)
    )
    body = f"""---
{fm_text}---
# {a.episode} · shape

**Knot:** [his phrase — premise § a]
**Anchor rung:** [En — his phrase]  {TAG_REC}

## Want
[one sentence — what she wants in her heart of hearts]  {TAG_NN}

## Moment of Truth
- **Question** — [one sentence — the scope of what she is building to ask]  {TAG_NN}
- **Answer** — [one sentence — the scope of what she gets]  {TAG_NN}

## Ending
- **Gained** — [one sentence]  {TAG_NN}
- **Lost** — [one sentence]  {TAG_NN}
- **Mode** — [stated | inferred]  {TAG_NN}

## Rungs
{rungs}

## Flaw
[one sentence — what will not be surrendered]  {TAG_NN}

## Cast
- **[role / name]** — age [n] · social status [x] · personality [x] · living conditions [x] · mental state [x]  {TAG_REC}
- **The instrument** — job: [one sentence] · arc: [one sentence]  {TAG_REC}

## Setting
- **Era** — [x]  {TAG_REC}
- **Region** — [x]  {TAG_REC}
- **Class** — [x]  {TAG_REC}
- **Living conditions** — [x]  {TAG_REC}

## Brainstorm agenda
- [open item, or: none — the spine is committed; aim the mic at the aesthetic layer]
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"scaffolded {out} ({a.rungs} rungs, anchor {a.anchor or 'unset'})")
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
    status = None
    if fm:
        for k in REQUIRED_FM:
            if k not in fm:
                fails.append(f"frontmatter: missing key {k}")
        if fm.get("type") != "episode-shape":
            fails.append("frontmatter: type must be episode-shape")
        status = fm.get("status")
        if status not in STATUSES:
            fails.append(f"frontmatter: status must be one of {sorted(STATUSES)}")
        if status == "ratified" and not str(fm.get("ratified") or "").strip():
            fails.append("frontmatter: status ratified needs a ratified stamp (CRE, YYYY-MM-DD)")
        if not str(fm.get("anchor_rung") or "").strip():
            fails.append("frontmatter: anchor_rung is empty (the anchor is named at the top of the session)")

    # 2. sections + walk order
    secs = _sections(body)
    names = [s[0] for s in secs if s[0] != "_head"]
    for want in SECTION_ORDER:
        if want not in names:
            fails.append(f"section missing: {want}")
    present = [n for n in names if n in SECTION_ORDER]
    if present != [s for s in SECTION_ORDER if s in present]:
        fails.append(f"walk order wrong: {present} (want → MoT → ending → rungs → flaw → cast → setting → agenda)")
    if names and names[-1] != "Brainstorm agenda":
        fails.append("Brainstorm agenda must be the last section")
    secmap = {n: ls for n, ls in secs}

    # 3. head lines: knot + anchor
    head = "\n".join(secmap.get("_head", []))
    if "**Knot:**" not in head:
        fails.append("head: no **Knot:** line")
    anchor_lines = [ln for ln in secmap.get("_head", []) if ln.strip().startswith("**Anchor rung:**")]
    if not anchor_lines:
        fails.append("head: no **Anchor rung:** line")
    else:
        if len(TAG_RE.findall(anchor_lines[0])) != 1:
            fails.append("head: Anchor rung line needs exactly one status tag")
        elif status == "ratified" and TAG_REC in anchor_lines[0] and TAG_RAT not in anchor_lines[0]:
            fails.append("head: Anchor rung is a bare [recommended] on a ratified shape")

    # 4. tagging — every entry line in a tagged section carries exactly one tag
    tag_counts = {t: 0 for t in TAGS}
    for n in TAGGED_SECTIONS:
        lines = secmap.get(n, [])
        entry_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("<!--")]
        if n in ("Want", "Flaw"):
            # single-line pillars: exactly one non-empty entry line
            if len(entry_lines) != 1:
                fails.append(f"{n}: needs exactly one entry line, found {len(entry_lines)}")
        else:
            entry_lines = [ln for ln in entry_lines if BULLET_RE.match(ln)]
            if not entry_lines:
                fails.append(f"{n}: no entry lines (- **…** — …)")
        for ln in entry_lines:
            found = TAG_RE.findall(ln)
            if len(found) != 1:
                fails.append(f"{n}: entry needs exactly one status tag, found {len(found)} — {ln.strip()[:60]}")
                continue
            tag = f"[{found[0]}]"
            tag_counts[tag] += 1
            if status == "ratified" and tag == TAG_REC:
                fails.append(f"{n}: bare [recommended] on a ratified shape (ratify it, or mark NOT NAMED) — {ln.strip()[:60]}")
            # an untagged empty field: tag present but nothing before it
            if not _strip_tags(ln).replace("-", "").replace("*", "").replace("·", "").replace("—", "").strip():
                fails.append(f"{n}: empty entry — {ln.strip()[:60]}")

    # 5. Moment of Truth + Ending sub-entries
    mot = "\n".join(secmap.get("Moment of Truth", []))
    for token in ("**Question**", "**Answer**"):
        if token not in mot:
            fails.append(f"Moment of Truth: missing {token} entry")
    end = "\n".join(secmap.get("Ending", []))
    for token in ("**Gained**", "**Lost**", "**Mode**"):
        if token not in end:
            fails.append(f"Ending: missing {token} entry")
    mode_line = next((ln for ln in secmap.get("Ending", []) if "**Mode**" in ln), "")
    if mode_line and not re.search(r"\b(stated|inferred)\b", mode_line) and TAG_NN not in mode_line:
        fails.append("Ending: Mode must say stated or inferred (or carry the hand-back tag)")

    # 6. rungs: descending, contiguous to E1, resistance token each
    rung_lines = [ln for ln in secmap.get("Rungs", []) if RUNG_LINE_RE.match(ln)]
    nums = [int(RUNG_LINE_RE.match(ln).group(1)) for ln in rung_lines]
    if not nums:
        fails.append("Rungs: no E lines")
    else:
        if nums != sorted(nums, reverse=True):
            fails.append(f"Rungs: must be walked DOWN (descending), found {nums}")
        if nums and (nums[-1] != 1 or nums != list(range(nums[0], 0, -1))):
            fails.append(f"Rungs: must run contiguously from the top rung to E1, found {nums}")
        if fm and "rung_count" in fm:
            try:
                if int(fm["rung_count"]) != len(nums):
                    fails.append(f"Rungs: frontmatter rung_count {fm['rung_count']} but {len(nums)} E lines")
            except (TypeError, ValueError):
                fails.append("frontmatter: rung_count must be an integer")
        for ln in rung_lines:
            k = f"E{RUNG_LINE_RE.match(ln).group(1)}"
            if RESISTANCE_TOKEN not in ln and TAG_NN not in ln:
                fails.append(f"{k}: no '{RESISTANCE_TOKEN}' token and no [NOT NAMED — CRE] tag")
            if RESISTANCE_TOKEN in ln:
                rest = ln.split(RESISTANCE_TOKEN, 1)[1]
                if not _strip_tags(rest).strip() and TAG_NN not in rest:
                    fails.append(f"{k}: '{RESISTANCE_TOKEN}' is empty and carries no hand-back tag")

    # 7. cast + setting shape
    cast = secmap.get("Cast", [])
    inst = [ln for ln in cast if BULLET_RE.match(ln) and ("job:" in ln or re.search(r"instrument|obstacle", ln, re.I))]
    if not inst:
        fails.append("Cast: no instrument / obstacle line (a cast line carrying job: … · arc: …)")
    else:
        for ln in inst:
            if "arc:" not in ln and TAG_NN not in ln:
                fails.append(f"Cast: instrument line has job: but no arc: — {ln.strip()[:60]}")
    setting = "\n".join(secmap.get("Setting", []))
    for token in ("**Era**", "**Region**", "**Class**", "**Living conditions**"):
        if token not in setting:
            fails.append(f"Setting: missing {token} placing fact")

    # 8. prose-like lines (heuristic; see the not-checked line)
    for n in TAGGED_SECTIONS + ["_head"]:
        for ln in secmap.get(n, []):
            s = ln.strip()
            if not s or s.startswith("<!--"):
                continue
            label = "head" if n == "_head" else n
            if DIALOGUE_RE.search(s) and not s.startswith("**Knot:**"):
                fails.append(f"prose-like ({label}): quoted speech — {s[:60]}…")
            if SPEECH_TAG_RE.search(s) and ("\"" in s or "“" in s):
                fails.append(f"prose-like ({label}): speech tag with quote — {s[:60]}…")
            core = _strip_tags(s)
            words = len(core.split())
            if words > PROSE_WORD_CEILING and not s.startswith("**Knot:**"):
                fails.append(f"prose-like ({label}): {words} words, ceiling {PROSE_WORD_CEILING} — {s[:60]}…")
            if MULTI_SENTENCE_RE.search(core) and not s.startswith("**Knot:**"):
                fails.append(f"prose-like ({label}): more than one sentence on a line — {s[:60]}…")

    # 9. placeholders left from the scaffold
    ph = [ln.strip()[:50] for ln in body.splitlines() if PLACEHOLDER_RE.search(ln) or re.search(r"\[(n|x|En — his phrase|open item)\b[^\]]*\]", ln)]
    if ph:
        fails.append("scaffold placeholders remain: " + " | ".join(ph[:4]))

    # 10. agenda
    agenda = [ln for ln in secmap.get("Brainstorm agenda", []) if BULLET_RE.match(ln)]
    if "Brainstorm agenda" in secmap and not agenda:
        fails.append("Brainstorm agenda: needs at least one line (open items, hand-backs, or the explicit none line)")
    nn_total = tag_counts[TAG_NN]
    if nn_total and agenda and not any(TAG_NN in ln or "NOT NAMED" in ln or "open" in ln.lower() for ln in agenda):
        infos.append(f"{nn_total} [NOT NAMED — CRE] entr{'y' if nn_total == 1 else 'ies'} above but the agenda names no open item — check the agenda lists them")

    # 11. hand-backs carried from the blueprint (informational)
    hb = [ln.strip() for ln in agenda if HANDBACK_RE.search(ln) and TAG_NN not in ln]
    if hb:
        infos.append(f"{len(hb)} blueprint hand-back(s) carried on the agenda")

    infos.append("tags: " + " · ".join(f"{t} {c}" for t, c in tag_counts.items()))

    for f in fails:
        print(f"FAIL  {f}")
    for i in infos:
        print(f"info  {i}")
    print("not checked: whether a line is CRE's material or an invented beat; whether a rung's resistance line "
          "is really different from its neighbour's; whether a default was derived from the shape or from imagination; "
          "whether the anchor is the right rung. Those are the attended gate's job (DIR-018).")
    print("PASS" if not fails else f"FAILED ({len(fails)})")
    return 0 if not fails else 1


# ---------------------------------------------------------------- handbacks
def cmd_handbacks(a):
    path = pathlib.Path(a.blueprint)
    if not path.exists():
        sys.stderr.write(f"no such file: {path}\n")
        return 2
    text = path.read_text(encoding="utf-8", errors="replace")
    fm_text, body = _split_frontmatter(text)
    hits = []
    for ln in body.splitlines():
        if HEADING_RE.match(ln) and ln.strip().endswith("Your notes"):
            break  # never read CRE's notes as hand-backs
        for m in HANDBACK_RE.finditer(ln):
            hits.append((m.group(0), ln.strip()[:90]))
    curve = ""
    if fm_text:
        try:
            curve = str((yaml.safe_load(fm_text) or {}).get("curve", "") or "")
        except yaml.YAMLError:
            curve = ""
    print(f"blueprint hand-backs in {path.name}: {len(hits)}")
    for tag, ln in hits:
        print(f"  {tag}  ←  {ln}")
    print(f"curve (frontmatter): {curve or 'not named — an agenda item, never asked here (blueprint field)'}")
    print("not read: draft.md, WRITING/SHORTS/DEV/, ## Your notes")
    return 0


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(prog="shape.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scaffold", help="write an empty shape.md with serialized frontmatter")
    s.add_argument("--episode", required=True, help='e.g. "EP 04 - TITLE"')
    s.add_argument("--out", required=True, help="path to shape.md")
    s.add_argument("--rungs", type=int, required=True, help="escalation count read from the blueprint")
    s.add_argument("--anchor", default="", help='the anchor rung as CRE named it, e.g. "E3 — the big question"')
    s.add_argument("--curve", default="", help="curve as read from blueprint frontmatter (never ruled here)")
    s.add_argument("--blueprint-run", type=int, default=1)
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_scaffold)

    c = sub.add_parser("check", help="lint a filled shape.md")
    c.add_argument("path")
    c.set_defaults(fn=cmd_check)

    h = sub.add_parser("handbacks", help="print the [... — CRE] hand-backs from a blueprint.md for the agenda")
    h.add_argument("blueprint")
    h.set_defaults(fn=cmd_handbacks)

    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
