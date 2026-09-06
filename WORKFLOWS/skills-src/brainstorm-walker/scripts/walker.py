#!/usr/bin/env python3
"""brainstorm-walker mechanical shell.

Three subcommands, all deterministic, none of them craft:

  derive     read a ratified shape.md (+ premise.md, blueprint.md, the candidate's
             ## Arc chain, WRITING/SHORTS/DEV/registry/) and write walker.md into the
             episode folder: refresher head, four episode-level slots, one block per
             shape entry (verbatim reminder lines + seven lens questions + an empty
             notes slot), cast, setting, agenda last. Every question is a fixed
             template parameterised only by the entry's own label — the script
             carries no story material. An existing walker.md is regenerated with
             every filled notes slot carried forward verbatim; unmatched notes go to
             a Carried notes section, never dropped.
  check      lint a walker.md: frontmatter parses, sections in order, four
             episode-level slots, every block carries the seven lenses (cue-grammar
             heads, question form) and a notes slot, no quoted speech in a question,
             no word in a question that is not template vocabulary or already on the
             block's reminder lines (the no-proposed-content floor), and — with
             --shape — every tagged shape entry appears verbatim as a reminder line.
  supersede  stamp superseded_by: on a walker.md once the brainstorm sheet ratifies.

Never reads draft.md. Never reads WRITING/SHORTS/DEV/scenes/. Never reads a
blueprint below its ## Your notes rule. Writes only walker.md.

Exit codes: 0 = pass / done, 1 = check failed, 2 = usage or I/O error, 3 = stop
condition (shape missing or not ratified, S2 already banked, nothing moved).
"""

import argparse
import datetime as _dt
import hashlib
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
TOOL = "brainstorm-walker"
EPISODES_DIR = pathlib.Path("WRITING/SHORTS/EPISODES")
REGISTRY_DIR = pathlib.Path("WRITING/SHORTS/DEV/registry")
AUDIT_DIR = pathlib.Path("WRITING/SHORTS/DEV/_intake/_audit")

# Shape sections in walk order (episode-harden's SECTION_ORDER); the walker mirrors it.
SHAPE_WALK = ["Want", "Moment of Truth", "Ending", "Rungs", "Flaw"]
SHAPE_SHEETS = ["Cast", "Setting"]
SHAPE_AGENDA = "Brainstorm agenda"

# Walker sections, in order. "Your notes" sits after a --- rule, last.
WALKER_SECTIONS = ["Refresher", "Episode-level cues", "The walk", "Cast", "Setting", "Brainstorm agenda"]
NOTES_HEADING = "Your notes"
CARRIED_HEADING = "Carried notes"

# The seven lenses, in the order every block prints them.
LENSES = ["dialogue", "imagery", "action", "reflection", "setting", "character", "feel"]

# Block classes that live under ## The walk (the shape's walk order).
WALK_CLASSES = ("moment", "pillar")

# S2 cue grammar (WRITING/SHORTS/DEV/_DEV_MAP.md cue table). The spoken head routes
# in dev-capture's deterministic layer; these are the only heads a question may carry.
CUE_HEADS = ("scene —", "character —", "place —", "what I love about this —", "project level —")

# lens -> cue head. Uniform on purpose: the same lens always speaks the same head.
LENS_HEAD = {
    "dialogue": "scene —",
    "imagery": "scene —",
    "action": "scene —",
    "reflection": "character —",
    "setting": "place —",
    "character": "character —",
    "feel": "what I love about this —",
}

# Question templates, by block class. {X} = the block's own label, lifted from the
# shape. Plain-speech questions about a committed entry; no beat, image, line or
# option. Change a template here, never in a generated file.
TEMPLATES = {
    "moment": {
        "dialogue": "What gets said out loud at {X}, and what stays unsaid?",
        "imagery": "What does the reader see at {X}? Is there one image that carries it?",
        "action": "What do they physically do at {X}? What moves, what is touched, what is refused?",
        "reflection": "What does she think or realise at {X}, and how much of that reaches the page?",
        "setting": "Where does {X} happen, and what does the place do to it?",
        "character": "Who is each of them at {X}, and what does it cost them?",
        "feel": "What is the feel of {X}? What do you love about it, and what interests you here?",
    },
    "pillar": {
        "dialogue": "Where does {X} get said out loud, if anywhere, and where does it stay unsaid?",
        "imagery": "What does the reader see that shows {X} without it being said?",
        "action": "What does she do because of {X}? What does she refuse to do?",
        "reflection": "How much of {X} does she know about herself, and when?",
        "setting": "Where in the place does {X} show? What does the place hold that says it?",
        "character": "Who else sees {X} in her, and who pushes on it?",
        "feel": "What is the feel of {X} on the page? What do you love about it?",
    },
    "person": {
        "dialogue": "How does {X} talk? What is a conversation with {X} like?",
        "imagery": "What does {X} look like, and what does the reader notice first?",
        "action": "What does {X} do with their hands, their body, their time?",
        "reflection": "What is {X} thinking that never gets said?",
        "setting": "Where does {X} belong, and where is {X} out of place?",
        "character": "What do you know about {X} that the shape does not say?",
        "feel": "What do you love about {X}? What does {X} feel like on the page?",
    },
    "place": {
        "dialogue": "How does {X} sound in their mouths? What words, names, or ways of talking does it bring?",
        "imagery": "What does {X} put in front of the reader? What is seen because of it?",
        "action": "What do they do that only {X} makes possible, or impossible?",
        "reflection": "What does {X} make them think about, or avoid thinking about?",
        "setting": "What else is true of {X} that the line does not say?",
        "character": "Who does {X} press on hardest, and how does that show?",
        "feel": "What is the feel of {X}? What do you love about it?",
    },
    "open": {
        "dialogue": "If {X} were named, what would get said about it, and by whom?",
        "imagery": "Is there an image that sits where {X} is not named?",
        "action": "What would happen on the page if {X} were named, and what happens because it is not?",
        "reflection": "What does she think about {X}, named or not?",
        "setting": "Does {X} live anywhere in the place, or stay out of it?",
        "character": "Whose is {X}? Who carries it, and who never learns it?",
        "feel": "What do you love about leaving {X} open, or about closing it?",
    },
}

EPISODE_CUES = [
    ("opening", "scene — the opening", "The opening line or image. What is it?"),
    ("closing", "scene — the closing", "The closing line or image. What is it?"),
    ("during", "project level — the reader, during", "What is the reader meant to feel while reading this?"),
    ("after", "project level — the reader, after", "What is the reader meant to be left with after reading this?"),
]

AGENDA_QUESTION = "What do you want to say to this? Take it, or leave it open."

TAG_RE = re.compile(r"\[(ruled|recommended|recommended → ratified|NOT NAMED — CRE)\]")
TAG_NN = "[NOT NAMED — CRE]"
HEADING2_RE = re.compile(r"^##\s+(.+?)\s*$")
HEADING3_RE = re.compile(r"^###\s+(.+?)\s*$")
BULLET_LABEL_RE = re.compile(r"^\s*[-*]\s*\*\*(.+?)\*\*\s*—\s*(.*)$")
BULLET_RE = re.compile(r"^\s*[-*]\s+\S")
RUNG_LABEL_RE = re.compile(r"^E(\d+)\b")
DIALOGUE_RE = re.compile(r"[\"“]([^\"”]{12,})[\"”]")
SPEECH_TAG_RE = re.compile(r"\b(said|says|asked|whispered|screamed|muttered|replied)\b", re.I)
QUESTION_LINE_RE = re.compile(r"^\s*-\s+\*\*(.+?)\*\*\s*·\s*(\w+)\s*—\s*(.+?)\s*$")
NOTES_LINE = "**Your notes:**"
OPEN_FLAG = "⚑ open"

STOPWORDS = set("""
a an the and or but if of to in on at by for from with without into onto over under
about as is are was were be been being do does did done has have had it its this that
these those there here where when what which who whom whose why how than then them they
their there's he she his her hers him you your yours we our us i me my mine one ones
not no nor so such very just also only even still yet both each any all some more most
other another same own out up down off across along around between before after during
while because once again further ever never always often
""".split())

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]{2,}")


# ---------------------------------------------------------------- helpers
def _read(path):
    return pathlib.Path(path).read_text(encoding="utf-8", errors="replace")


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


def _load_fm(text):
    fm_text, body = _split_frontmatter(text)
    fm = {}
    if fm_text is not None:
        try:
            fm = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            fm = {}
    return fm, body


def _sections(body, level_re=HEADING2_RE, stop_at_rule=False):
    """Ordered list of (heading, [lines]); text before the first heading is ('_head', [...])."""
    out = [("_head", [])]
    current = out[0]
    for line in body.splitlines():
        if stop_at_rule and line.strip() == "---":
            break
        m = level_re.match(line)
        if m:
            current = (m.group(1).strip(), [])
            out.append(current)
        else:
            current[1].append(line)
    return out


def _norm(s):
    return re.sub(r"\s+", " ", s.strip())


def _words(s):
    return {w.lower().strip("'’-") for w in WORD_RE.findall(s)}


def _fingerprint(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _entries(lines):
    """Bullet entries of a shape section as (label, rest, raw) — raw keeps the tag."""
    out = []
    for ln in lines:
        m = BULLET_LABEL_RE.match(ln)
        if m:
            out.append((m.group(1).strip(), m.group(2).strip(), ln.strip()))
        elif BULLET_RE.match(ln):
            out.append(("", ln.strip().lstrip("-* ").strip(), ln.strip()))
    return out


def _single(lines):
    entry = [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("<!--")]
    return entry[0] if entry else ""


def _is_open(raw):
    return TAG_NN in raw


# ---------------------------------------------------------------- sources
class Sources:
    def __init__(self, root):
        self.root = pathlib.Path(root).resolve()
        self.read = []
        self.not_read = ["draft.md (plan-only, CRE 2026-09-03)", "WRITING/SHORTS/DEV/scenes/ (S2 not run; other episodes' scenes are noise)"]

    def rel(self, p):
        try:
            return pathlib.Path(p).resolve().relative_to(self.root).as_posix()
        except ValueError:
            return pathlib.Path(p).as_posix()


def read_shape(folder, src):
    p = folder / "shape.md"
    if not p.exists():
        return None, "no shape.md — not hardened; route to episode-harden"
    text = _read(p)
    fm, body = _load_fm(text)
    if fm.get("type") != "episode-shape":
        return None, "shape.md is not type episode-shape"
    if fm.get("status") != "ratified":
        return None, f"shape.md status is {fm.get('status')!r} — the walker mirrors a ratified shape only; stamp it first"
    secs = _sections(body)
    secmap = {n: ls for n, ls in secs}
    head = secmap.get("_head", [])
    knot = next((ln.strip() for ln in head if ln.strip().startswith("**Knot:**")), "")
    anchor = next((ln.strip() for ln in head if ln.strip().startswith("**Anchor rung:**")), "")
    shape = {
        "fm": fm,
        "fingerprint": _fingerprint(text),
        "knot": knot,
        "anchor": anchor,
        "want": _single(secmap.get("Want", [])),
        "mot": _entries(secmap.get("Moment of Truth", [])),
        "ending": _entries(secmap.get("Ending", [])),
        "rungs": _entries(secmap.get("Rungs", [])),
        "flaw": _single(secmap.get("Flaw", [])),
        "cast": _entries(secmap.get("Cast", [])),
        "setting": _entries(secmap.get("Setting", [])),
        "agenda": _entries(secmap.get(SHAPE_AGENDA, [])),
    }
    src.read.append(f"{src.rel(p)} (ratified {fm.get('ratified', '')}; every tagged entry lifted verbatim)")
    return shape, ""


def read_premise(folder, src):
    p = folder / "premise.md"
    if not p.exists():
        src.not_read.append("premise.md (absent)")
        return {}
    text = _read(p)
    fm, body = _load_fm(text)
    secs = _sections(body)
    secmap = {n: ls for n, ls in secs}
    quote = []
    for n, ls in secs:
        if n.lower().startswith("the premise"):
            quote = [ln.strip()[1:].strip() for ln in ls if ln.strip().startswith(">")]
            break
    src.read.append(f"{src.rel(p)} (frontmatter: title, tier, container, pov; § The premise verbatim)")
    return {"fm": fm, "premise_quote": " ".join(q for q in quote if q)}


def read_blueprint(folder, src):
    p = folder / "blueprint.md"
    if not p.exists():
        src.not_read.append("blueprint.md (absent)")
        return {}
    text = _read(p)
    fm, body = _load_fm(text)
    secs = _sections(body, stop_at_rule=True)  # never below the rule: ## Your notes is CRE's
    secmap = {n: ls for n, ls in secs}

    def first_line(name):
        for n, ls in secmap.items():
            if n.split(" (")[0].strip().lower() == name.lower():
                return _single(ls)
        return ""

    src.read.append(f"{src.rel(p)} (frontmatter curve + ruling; § Incident, § Choice; not below the ## Your notes rule)")
    return {"fm": fm, "incident": first_line("Incident"), "choice": first_line("Choice")}


def read_arc_chain(root, premise, src):
    sc = str((premise.get("fm") or {}).get("source_candidate") or "")
    m = re.search(r"((?:[A-Za-z_]+/)+[^'\"\n(]*?triage\.md)", sc)
    if not m:
        src.not_read.append("## Arc chain (premise.md carries no source_candidate path)")
        return {}
    p = root / m.group(1)
    if not p.exists():
        src.not_read.append(f"## Arc chain ({src.rel(p)} not found)")
        return {}
    text = _read(p)
    _, body = _load_fm(text)
    secs = _sections(body)
    chain_lines = []
    for n, ls in secs:
        if n.strip().lower() == "arc chain":
            chain_lines = ls
            break
    if not chain_lines:
        src.not_read.append(f"## Arc chain ({p.name} has no such section)")
        return {}
    out = {}
    for ln in chain_lines:
        s = ln.strip()
        mm = re.match(r"^\*\*(Choice|Mirror|Moment of Truth|Ending stance)\*\*\s*—\s*(.*)$", s)
        if mm:
            out[mm.group(1).lower()] = s
    src.read.append(f"{src.rel(p)} (## Arc chain: Choice, Mirror lines lifted; the rest read as known)")
    return out


def read_registry(root, src):
    reg = root / REGISTRY_DIR
    banked = []
    if not reg.exists():
        src.not_read.append("WRITING/SHORTS/DEV/registry/ (absent)")
        return banked
    for bucket in ("characters", "locations", "lore"):
        d = reg / bucket
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            if f.name.lower().startswith(("readme", "_")):
                continue
            fm, body = _load_fm(_read(f))
            first = next((ln.strip().lstrip("# ").strip() for ln in body.splitlines() if ln.strip() and not ln.strip().startswith(("<!--", ">"))), "")
            banked.append((bucket, f.stem, first[:120]))
    items = reg / "items.md"
    if items.exists():
        _, body = _load_fm(_read(items))
        fenced = False
        for ln in body.splitlines():
            if ln.strip().startswith("```"):
                fenced = not fenced
                continue
            if fenced or not ln.strip().startswith("### "):
                continue
            h = ln.strip().lstrip("# ").strip()
            if "<" in h or ">" in h:  # the README's format example, not an item
                continue
            banked.append(("items", h, ""))
    src.read.append("WRITING/SHORTS/DEV/registry/ (characters, locations, lore, items — names + first line only)")
    return banked


def s2_banked(root, episode):
    """Has S2 already swept a brainstorm floor naming this episode? Probes _audit/ only — never scenes/."""
    d = root / AUDIT_DIR
    if not d.exists():
        return []
    key = episode.lower()
    hits = []
    for f in d.glob("*.md"):
        if f.name.lower().startswith("readme"):
            continue
        if key in f.name.lower():
            hits.append(f.name)
            continue
        try:
            head = _read(f)[:2000].lower()
        except OSError:
            continue
        if key in head:
            hits.append(f.name)
    return hits


# ---------------------------------------------------------------- notes carry
def parse_notes(walker_text):
    """Map block key -> notes text (verbatim) from an existing walker.md; plus the tail ## Your notes."""
    _, body = _load_fm(walker_text)
    notes = {}
    lines = body.splitlines()
    key = None
    collecting = False
    buf = []
    tail = None

    def flush():
        nonlocal buf, key, collecting
        if key is not None and collecting:
            txt = "\n".join(buf).strip("\n")
            if txt.strip():
                notes[key] = txt
        buf, collecting = [], False

    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and HEADING2_RE.match(lines[j]) and lines[j].strip().endswith(NOTES_HEADING):
                flush()
                tail = "\n".join(lines[j + 1:]).strip("\n")
                break
        m3 = HEADING3_RE.match(ln)
        m2 = HEADING2_RE.match(ln)
        if m3 or m2:
            flush()
            key = (m3 or m2).group(1).replace(OPEN_FLAG, "").strip() if m3 else None
            continue
        if ln.strip() == NOTES_LINE:
            flush()
            collecting = True
            continue
        if collecting:
            buf.append(ln)
    flush()
    return notes, tail


# ---------------------------------------------------------------- blocks
def _label_for(kind, label):
    if kind == "moment":
        return label
    return label


def build_blocks(shape):
    """Return ordered list of block dicts: key, heading, cls, label, reminders (raw lines), open."""
    blocks = []

    def add(key, cls, label, reminders):
        blocks.append({
            "key": key, "cls": cls, "label": label,
            "reminders": [r for r in reminders if r],
            "open": any(_is_open(r) for r in reminders if r),
        })

    add("Want", "pillar", "the want", [shape["want"]])
    add("Moment of Truth", "moment", "the Moment of Truth", [e[2] for e in shape["mot"]])
    add("Ending", "moment", "the ending", [e[2] for e in shape["ending"]])

    # rungs: each E line a block; its sub-lines ("E3, the flip") ride with it; other lines own blocks
    rung_blocks = {}
    order = []
    for label, rest, raw in shape["rungs"]:
        m = RUNG_LABEL_RE.match(label)
        if m:
            k = f"E{m.group(1)}"
            if k not in rung_blocks:
                rung_blocks[k] = []
                order.append(k)
            rung_blocks[k].append(raw)
        else:
            order.append(("_other", label or rest[:40], raw))
    for item in order:
        if isinstance(item, tuple):
            _, lab, raw = item
            add(lab, "pillar", "this", [raw])
        else:
            add(item, "moment", item, rung_blocks[item])

    add("Flaw", "pillar", "the flaw", [shape["flaw"]])

    # cast: group sub-lines under their member by name match
    members = []  # (name_display, key, [raws])
    for label, rest, raw in shape["cast"]:
        name_part = label.split(",")[0].strip()
        matched = None
        for mem in members:
            disp = mem[0]
            tokens = [t for t in re.split(r"[\s/()]+", disp) if t]
            if name_part == disp or name_part in tokens or any(name_part == t for t in tokens) or (len(name_part) > 2 and name_part in disp):
                matched = mem
                break
        if matched:
            matched[2].append(raw)
        else:
            display = label.split(",")[0].strip()
            short = display.split("/")[-1].strip() if "/" in display else display
            short = re.sub(r"\s*\([^)]*\)", "", short).strip()  # "The mother (off-page)" -> "The mother"
            if short.startswith("The "):
                short = "the " + short[4:]
            members.append((display, short, [raw]))
    for display, short, raws in members:
        add(f"Cast — {display}", "person", short, raws)

    for label, rest, raw in shape["setting"]:
        x = "the " + (label[:1].lower() + label[1:]) if label and not label.lower().startswith("the ") else label
        add(f"Setting — {label}", "place", x, [raw])

    return blocks


def render_questions(block):
    X = block["label"]
    cls = block["cls"]
    out = []
    for lens in LENSES:
        tmpl = TEMPLATES["open" if (block["open"] and cls in WALK_CLASSES) else cls][lens]
        head = LENS_HEAD[lens]
        if cls == "person":
            target = X
        elif cls == "place":
            target = block["key"].replace("Setting — ", "")
        else:
            target = block["key"]
        q = tmpl.replace("{X}", X)
        out.append(f"- **{head} {target}** · {lens} — {q}")
    return out


def render_block(block, notes):
    h = f"### {block['key']}" + (f"  {OPEN_FLAG}" if block["open"] else "")
    lines = [h, ""]
    for r in block["reminders"]:
        lines.append(r if r.startswith(("-", "*")) else f"- {r}")
    lines.append("")
    lines.extend(render_questions(block))
    lines.append("")
    lines.append(NOTES_LINE)
    lines.append("")
    carried = notes.get(block["key"])
    if carried:
        lines.append(carried)
        lines.append("")
    return lines


# ---------------------------------------------------------------- derive
def cmd_derive(a):
    root = pathlib.Path(a.root).resolve()
    folder = root / EPISODES_DIR / a.episode if not a.folder else pathlib.Path(a.folder).resolve()
    if not folder.exists():
        sys.stderr.write(f"no such episode folder: {folder}\n")
        return 2
    out = pathlib.Path(a.out) if a.out else folder / "walker.md"
    src = Sources(root)

    shape, why = read_shape(folder, src)
    if shape is None:
        sys.stderr.write(f"stop: {why}\n")
        return 3

    hits = s2_banked(root, a.episode)
    if hits and not a.force:
        sys.stderr.write("stop: S2 appears to have run for this episode (brainstorm floor in DEV/_intake/_audit/: "
                         + ", ".join(hits[:3]) + "). The walker's job is done; supersede it instead, or --force to regenerate.\n")
        return 3

    old_notes, old_tail = {}, None
    if out.exists():
        old_text = _read(out)
        old_fm, _ = _load_fm(old_text)
        if old_fm.get("shape_fingerprint") == shape["fingerprint"] and not a.force:
            print(f"nothing moved: {out.name} already mirrors this shape (fingerprint {shape['fingerprint']}). --force to regenerate anyway.")
            return 3
        old_notes, old_tail = parse_notes(old_text)
        # an orphan whose block has come back goes home under its own name
        for k in list(old_notes):
            if k.startswith("was: ") and k[5:] not in old_notes:
                old_notes[k[5:]] = old_notes.pop(k)

    premise = read_premise(folder, src)
    blueprint = read_blueprint(folder, src)
    chain = read_arc_chain(root, premise, src)
    banked = read_registry(root, src)

    blocks = build_blocks(shape)
    pfm = premise.get("fm") or {}
    bfm = blueprint.get("fm") or {}

    fm = {
        "type": TOOL,
        "episode": a.episode,
        "shape_ratified": str(shape["fm"].get("ratified") or ""),
        "shape_fingerprint": shape["fingerprint"],
        "status": "current",
        "superseded_by": "",
        "block_count": len(blocks),
        "sources_read": src.read + [f"not read: {'; '.join(src.not_read)}"],
        "generated": _dt.date.today().isoformat(),
        "tool": TOOL,
        "note": "coverage, not obligation. A derived mirror of the ratified shape (DIR-019 §1): regenerated when shape.md is "
                "re-ratified, notes slots carried verbatim, never ruled on. Skipping a cue is legal; nothing downstream grades "
                "the brainstorm against this (DIR-017 §2). Speak the bold head before you answer — dev-capture routes on it.",
    }
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100)
    yaml.safe_load(fm_text)  # parse gate (DIR-004)

    L = []
    L.append(f"# {a.episode} · walker")
    L.append("")
    L.append("> Coverage, not a checklist. Read the refresher, then speak or type to whatever you want. Say the bold head first ("
             "*scene —*, *character —*, *place —*, *what I love about this —*) so the capture routes itself. Skip anything; "
             "nothing grades you against this.")
    L.append("")
    # ---- Refresher
    L.append("## Refresher")
    L.append("")
    if shape["knot"]:
        L.append(shape["knot"])
    if shape["anchor"]:
        L.append(shape["anchor"])
    curve = shape["fm"].get("curve") or bfm.get("curve") or ""
    if curve:
        L.append(f"**Curve:** {_norm(str(curve))}  (blueprint)")
    if pfm:
        bits = []
        for k, lab in (("tier", "tier"), ("container", "container"), ("pov", "POV")):
            v = pfm.get(k)
            if v:
                bits.append(f"{lab}: {_norm(str(v))}")
        if bits:
            L.append("**Gate:** " + " · ".join(bits) + "  (premise frontmatter)")
    if premise.get("premise_quote"):
        L.append("")
        L.append("> [!quote]- The premise, verbatim (premise.md § The premise)")
        L.append(f"> {premise['premise_quote']}")
    L.append("")
    L.append("**Mechanics**")
    if chain.get("choice"):
        L.append(f"- {chain['choice']}  (arc chain)")
    elif blueprint.get("choice"):
        L.append(f"- **Choice** — {blueprint['choice']}  (blueprint § Choice)")
    if blueprint.get("incident"):
        L.append(f"- **Incident** — {blueprint['incident']}  (blueprint § Incident)")
    if chain.get("mirror"):
        L.append(f"- {chain['mirror']}  (arc chain)")
    if shape["want"]:
        L.append(f"- **Want** — {shape['want']}")
    for e in shape["mot"]:
        L.append(f"- **MoT, {e[0]}** — {e[1]}" if e[0] else f"- {e[2]}")
    for e in shape["ending"]:
        L.append(f"- **Ending, {e[0]}** — {e[1]}" if e[0] else f"- {e[2]}")
    if shape["flaw"]:
        L.append(f"- **Flaw** — {shape['flaw']}")
    L.append("")
    L.append("**Cast**")
    seen_members = set()
    for b in blocks:
        if b["cls"] == "person":
            L.append(b["reminders"][0])
    L.append("")
    L.append("**Setting**")
    for e in shape["setting"]:
        L.append(e[2])
    L.append("")
    L.append("**Agenda (from the shape)**")
    for e in shape["agenda"]:
        L.append(e[2])
    L.append("")
    L.append("**Banked in the registry (shared across episodes)**")
    if banked:
        for bucket, name, first in banked:
            L.append(f"- {bucket}: [[{name}]]" + (f" — {first}" if first else ""))
    else:
        L.append("- nothing banked yet")
    L.append("")

    # ---- Episode-level cues
    L.append("## Episode-level cues")
    L.append("")
    for key, head, q in EPISODE_CUES:
        hk = f"Cue — {key}"
        L.append(f"### {hk}")
        L.append("")
        L.append(f"- **{head}** — {q}")
        L.append("")
        L.append(NOTES_LINE)
        L.append("")
        if old_notes.get(hk):
            L.append(old_notes[hk])
            L.append("")

    # ---- The walk (shape walk order), then cast, then setting
    L.append("## The walk")
    L.append("")
    L.append("Walk order is the shape's: want, Moment of Truth, ending, rungs from the anchor down, flaw. Every committed line is here verbatim, with its tag.")
    L.append("")
    used = set()
    for b in blocks:
        if b["cls"] in WALK_CLASSES:
            L.extend(render_block(b, old_notes))
            used.add(b["key"])
    L.append("## Cast")
    L.append("")
    for b in blocks:
        if b["cls"] == "person":
            L.extend(render_block(b, old_notes))
            used.add(b["key"])
    L.append("## Setting")
    L.append("")
    for b in blocks:
        if b["cls"] == "place":
            L.extend(render_block(b, old_notes))
            used.add(b["key"])

    # ---- Agenda, last
    L.append(f"## {SHAPE_AGENDA}")
    L.append("")
    L.append("Carried whole from the shape. Open items are the holes S2 exists to fill; take them or leave them.")
    L.append("")
    open_blocks = [b for b in blocks if b["open"]]
    if open_blocks:
        L.append(f"- **{OPEN_FLAG}** in the walk: " + " · ".join(b["key"] for b in open_blocks) + " — each block above carries the flag")
    for i, e in enumerate(shape["agenda"], 1):
        hk = f"Agenda {i}"
        used.add(hk)
        L.append(f"### {hk}")
        L.append("")
        L.append(e[2])
        L.append("")
        L.append(f"- **project level — agenda {i}** · open — {AGENDA_QUESTION}")
        L.append("")
        L.append(NOTES_LINE)
        L.append("")
        if old_notes.get(hk):
            L.append(old_notes[hk])
            L.append("")
    if not shape["agenda"]:
        L.append("- none carried — the shape's agenda was empty")
        L.append("")

    # ---- Carried notes that matched no block (never dropped)
    for k in ("Cue — opening", "Cue — closing", "Cue — during", "Cue — after"):
        used.add(k)
    orphans = {k: v for k, v in old_notes.items() if k not in used}
    if orphans:
        L.append(f"## {CARRIED_HEADING}")
        L.append("")
        L.append("Notes whose block no longer exists after the shape moved. Yours; carried verbatim, never dropped.")
        L.append("")
        for k, v in orphans.items():
            L.append(f"### was: {k}")
            L.append("")
            L.append(NOTES_LINE)
            L.append("")
            L.append(v)
            L.append("")

    # ---- Your notes (the tail, after the rule)
    L.append("---")
    L.append("")
    L.append(f"## {NOTES_HEADING}")
    L.append("")
    if old_tail:
        L.append(old_tail)
        L.append("")

    text = f"---\n{fm_text}---\n" + "\n".join(L).rstrip("\n") + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    carried = sum(1 for k in old_notes if k in used) + (1 if old_tail else 0)
    print(f"derived {out} — {len(blocks)} blocks ({sum(b['cls'] in WALK_CLASSES for b in blocks)} walk · "
          f"{sum(b['cls']=='person' for b in blocks)} cast · {sum(b['cls']=='place' for b in blocks)} setting), "
          f"{len(open_blocks)} flagged open, {len(shape['agenda'])} agenda items"
          + (f", {carried} notes slot(s) carried, {len(orphans)} orphaned into Carried notes" if old_notes or old_tail else ""))
    print("not read: " + "; ".join(src.not_read))
    return 0


# ---------------------------------------------------------------- check
def cmd_check(a):
    path = pathlib.Path(a.path)
    if not path.exists():
        sys.stderr.write(f"no such file: {path}\n")
        return 2
    text = _read(path)
    fails, infos = [], []

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
        for k in ("type", "episode", "shape_ratified", "shape_fingerprint", "status", "superseded_by", "sources_read", "generated"):
            if k not in fm:
                fails.append(f"frontmatter: missing key {k}")
        if fm.get("type") != TOOL:
            fails.append(f"frontmatter: type must be {TOOL}")
        if fm.get("status") not in ("current", "superseded"):
            fails.append("frontmatter: status must be current or superseded")
        if fm.get("status") == "superseded" and not str(fm.get("superseded_by") or "").strip():
            fails.append("frontmatter: status superseded needs superseded_by")
        sr = " ".join(str(x) for x in (fm.get("sources_read") or []))
        if "draft.md" not in sr or "scenes" not in sr:
            fails.append("frontmatter: sources_read must carry the not-read line naming draft.md and DEV/scenes/")

    # sections
    pre_rule = body.split("\n---", 1)[0]
    secs = _sections(pre_rule)
    names = [n for n, _ in secs if n != "_head"]
    for want in WALKER_SECTIONS:
        if want not in names:
            fails.append(f"section missing: {want}")
    present = [n for n in names if n in WALKER_SECTIONS]
    if present != [s for s in WALKER_SECTIONS if s in present]:
        fails.append(f"section order wrong: {present}")
    core = [n for n in names if n != CARRIED_HEADING]
    if core and core[-1] != SHAPE_AGENDA:
        fails.append(f"{SHAPE_AGENDA} must be the last section before the notes rule (found {core[-1]!r})")
    if not re.search(r"\n---\n\s*## " + re.escape(NOTES_HEADING), body):
        fails.append(f"no closing --- rule + ## {NOTES_HEADING}")

    secmap = {n: ls for n, ls in secs}

    # episode-level cues
    cue_text = "\n".join(secmap.get("Episode-level cues", []))
    for key, head, _q in EPISODE_CUES:
        if f"### Cue — {key}" not in cue_text:
            fails.append(f"Episode-level cues: missing slot {key}")
        if f"**{head}**" not in cue_text:
            fails.append(f"Episode-level cues: slot {key} lacks its head {head!r}")
    if cue_text.count(NOTES_LINE) < 4:
        fails.append("Episode-level cues: fewer than four notes slots")

    # refresher
    ref = "\n".join(secmap.get("Refresher", []))
    for token in ("**Knot:**", "**Mechanics**", "**Cast**", "**Setting**", "**Agenda (from the shape)**", "**Banked in the registry"):
        if token not in ref:
            fails.append(f"Refresher: missing {token}")

    # blocks
    template_vocab = set()
    for cls in TEMPLATES.values():
        for t in cls.values():
            template_vocab |= _words(t)
    for _k, head, q in EPISODE_CUES:
        template_vocab |= _words(head) | _words(q)
    template_vocab |= _words(AGENDA_QUESTION) | _words(" ".join(CUE_HEADS)) | set(LENSES) | {"open"}
    refresher_words = _words(ref)

    block_count = 0
    reminders_all = []
    for sec in ("The walk", "Cast", "Setting"):
        sub = _sections("\n".join(secmap.get(sec, [])), level_re=HEADING3_RE)
        for h, ls in sub:
            if h == "_head":
                continue
            block_count += 1
            blk = "\n".join(ls)
            key = h.replace(OPEN_FLAG, "").strip()
            reminders = [ln.strip() for ln in ls if BULLET_RE.match(ln) and TAG_RE.search(ln) and not QUESTION_LINE_RE.match(ln)]
            reminders_all.extend(reminders)
            if not reminders:
                fails.append(f"{sec} › {key}: no tagged reminder line lifted from the shape")
            if any(TAG_NN in r for r in reminders) and OPEN_FLAG not in h:
                fails.append(f"{sec} › {key}: carries a [NOT NAMED — CRE] line but the heading lacks {OPEN_FLAG}")
            qs = [QUESTION_LINE_RE.match(ln.strip()) for ln in ls]
            qs = [m for m in qs if m]
            lenses_seen = [m.group(2) for m in qs]
            for lens in LENSES:
                if lens not in lenses_seen:
                    fails.append(f"{sec} › {key}: missing lens {lens}")
            if len(qs) != len(LENSES):
                fails.append(f"{sec} › {key}: expected {len(LENSES)} lens lines, found {len(qs)}")
            allowed = template_vocab | refresher_words | _words(" ".join(reminders)) | _words(key)
            for m in qs:
                head, lens, q = m.group(1), m.group(2), m.group(3)
                if not any(head.startswith(c) for c in CUE_HEADS):
                    fails.append(f"{sec} › {key}: {lens} head is not S2 cue grammar — {head!r}")
                if lens in LENS_HEAD and not head.startswith(LENS_HEAD[lens]):
                    fails.append(f"{sec} › {key}: {lens} should speak {LENS_HEAD[lens]!r}, speaks {head.split(' —')[0]!r} —")
                if not q.rstrip().endswith("?"):
                    fails.append(f"{sec} › {key}: {lens} is not a question — {q[:60]}")
                if DIALOGUE_RE.search(q) or (SPEECH_TAG_RE.search(q) and ("\"" in q or "“" in q)):
                    fails.append(f"{sec} › {key}: {lens} carries quoted speech — {q[:60]}")
                novel = sorted(w for w in _words(q) - allowed if w not in STOPWORDS)
                if novel:
                    fails.append(f"{sec} › {key}: {lens} introduces words not on the reminder or in the template vocabulary (proposed content?): {', '.join(novel)}")
            if NOTES_LINE not in blk:
                fails.append(f"{sec} › {key}: no {NOTES_LINE} slot")

    if fm and "block_count" in fm:
        try:
            if int(fm["block_count"]) != block_count:
                fails.append(f"frontmatter block_count {fm['block_count']} but {block_count} blocks found")
        except (TypeError, ValueError):
            fails.append("frontmatter: block_count must be an integer")

    # agenda
    ag = "\n".join(secmap.get(SHAPE_AGENDA, []))
    ag_sub = [h for h, _ in _sections(ag, level_re=HEADING3_RE) if h != "_head"]
    if ag_sub and ag.count(NOTES_LINE) < len(ag_sub):
        fails.append("Brainstorm agenda: an agenda item lacks its notes slot")

    # --shape: coverage by construction
    if a.shape:
        sp = pathlib.Path(a.shape)
        if not sp.exists():
            fails.append(f"--shape: no such file {sp}")
        else:
            _, sbody = _load_fm(_read(sp))
            ssecs = {n: ls for n, ls in _sections(sbody)}
            walker_norm = _norm(body)
            missing = []
            for n in SHAPE_WALK + SHAPE_SHEETS:
                for ln in ssecs.get(n, []):
                    s = ln.strip()
                    if not s or s.startswith("<!--"):
                        continue
                    if n in ("Want", "Flaw") or BULLET_RE.match(s):
                        if _norm(s) not in walker_norm and _norm(s.lstrip("-* ")) not in walker_norm:
                            missing.append(f"{n}: {s[:50]}")
            for ln in ssecs.get(SHAPE_AGENDA, []):
                s = ln.strip()
                if BULLET_RE.match(s) and _norm(s) not in walker_norm:
                    missing.append(f"agenda: {s[:50]}")
            if missing:
                fails.append("shape entries without a verbatim reminder line: " + " | ".join(missing[:6]) + (" …" if len(missing) > 6 else ""))
            else:
                infos.append("every tagged shape entry and agenda line appears verbatim in the walker")

    infos.append(f"blocks: {block_count} · notes slots: {body.count(NOTES_LINE)}")
    for f in fails:
        print(f"FAIL  {f}")
    for i in infos:
        print(f"info  {i}")
    print("not checked: whether a question is really a question about the committed entry or a beat wearing a question mark; "
          "whether a lifted line is still what the shape says today (regenerate on re-ratify); whether a carried note is complete. "
          "Those are CRE's at the mic and the desk (DIR-018).")
    print("PASS" if not fails else f"FAILED ({len(fails)})")
    return 0 if not fails else 1


# ---------------------------------------------------------------- supersede
def cmd_supersede(a):
    path = pathlib.Path(a.path)
    if not path.exists():
        sys.stderr.write(f"no such file: {path}\n")
        return 2
    text = _read(path)
    fm_text, body = _split_frontmatter(text)
    if fm_text is None:
        sys.stderr.write("walker.md has no frontmatter\n")
        return 2
    fm = yaml.safe_load(fm_text) or {}
    fm["status"] = "superseded"
    fm["superseded_by"] = a.by
    fm["superseded_on"] = _dt.date.today().isoformat()
    new_fm = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100)
    yaml.safe_load(new_fm)
    path.write_text(f"---\n{new_fm}---\n{body}", encoding="utf-8")
    print(f"stamped {path.name}: status superseded, superseded_by {a.by!r}. Body untouched; notes stay where they are.")
    return 0


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(prog="walker.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("derive", help="derive walker.md from a ratified shape.md")
    d.add_argument("--root", default=".", help="vault root (resolves WRITING/SHORTS/… and the registry)")
    d.add_argument("--episode", required=True, help='e.g. "EP 04 - A GOOD DEATH"')
    d.add_argument("--folder", default="", help="episode folder path if not under WRITING/SHORTS/EPISODES/<episode>")
    d.add_argument("--out", default="", help="output path (default <folder>/walker.md)")
    d.add_argument("--force", action="store_true", help="regenerate even if the shape has not moved / S2 appears banked")
    d.set_defaults(fn=cmd_derive)

    c = sub.add_parser("check", help="lint a walker.md")
    c.add_argument("path")
    c.add_argument("--shape", default="", help="the shape.md it mirrors — enables the coverage check")
    c.set_defaults(fn=cmd_check)

    s = sub.add_parser("supersede", help="stamp superseded_by once the brainstorm sheet ratifies")
    s.add_argument("path")
    s.add_argument("--by", required=True, help='e.g. "WRITING/SHORTS/DEV/_intake/2026-09-07 brainstorm - EP 04.md"')
    s.set_defaults(fn=cmd_supersede)

    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
