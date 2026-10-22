"""branch-writing-expert plan tool (plotting mode; carried over from interlock-plotter): every write to an Interlocking Arc Model plan goes through here, so the JSON block stays
valid and the readable table above it is always regenerated from it (never hand-edited, so the two can't drift).

    python -I plan_tool.py new    <plan.md> --board-path <path> --title <t> [--copy-of <path>] [--vault V]
    python -I plan_tool.py set    <plan.md> --json-file <part.json>                merge top-level keys (a FILE, never a shell
                                                                                   argument: PowerShell 5.1 strips the quotes, ^obs-444)
    python -I plan_tool.py set    <plan.md> --json '<partial plan JSON>'          the same from Git Bash only; merge top-level keys (cast, roles, switches,
                                                                                   plotting, structure, external) — CRE's words only
    python -I plan_tool.py beat   <plan.md> --n 17 --spine external [--cast key] [--sub a|b] (--text "<CRE's words>" | --open)
                                  [--who k1,k2] [--at "seq:Title"] [--src "dictation 2026-10-18 ¶12"]
    python -I plan_tool.py walk   <plan.md> --beats 16-20 [--vault V]             the walk sheet for one model group
    python -I plan_tool.py render <plan.md> [--vault V]                           regenerate the readable part
    python -I plan_tool.py approve <plan.md> --phrase "<CRE's exact words>"        refuses anything but "approve the plan"
    python -I plan_tool.py walked <plan.md> --beats 16-20                         record a round as walked (answered or skipped)
    python -I plan_tool.py status <plan.md> [--vault V]                           what is filled, which rounds are walked, where to resume

Spine sets (0.65): a plan may carry extra full spine sets beside the main one — one character leading two stories (the
Woodsgirl interludes beside the woodswoman's present day). Add or change one with `set --json-file` holding
    {"spines": [{"key": "woodsgirl", "name": "The Woodsgirl", "lead": "<cast key>", "antagonist": "<cast key>",
                 "era": "<era name on the board, or null>", "switches": {"K1": null, ...}, "external": {"label": "..."}}]}
(merged by key: a set already there keeps its beats and walked rounds; a set is never dropped by `set`). Its beats, walk and
rounds take `--set <key>`: `beat --set woodsgirl --n 6 --spine lead --text "…"`, `walk --set woodsgirl --beats 6-10`,
`walked --set woodsgirl --beats 6-10`. A set has three columns: antagonist, external, lead. No --set is the main set,
exactly as before, and a plan without `spines` is unchanged.

A beat CRE skips needs no call: a beat the plan doesn't list is an open, labelled blank. `beat` with only --at / --who places
or tags a beat without retyping its words. A beat number means what the builder reads (stepAtBeat): the step at that beat,
else the compressed step whose rows span it, else the one step carrying that model beat.

Never invents a value: every text it writes arrives on the command line, from CRE. A beat given --open is an open,
labelled blank (text null), a valid state. Console output is forced to UTF-8 (DIR-020).
"""
import argparse, datetime, hashlib, json, os, re, sys

for st in (sys.stdout, sys.stderr):
    try:
        st.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEFAULT_VAULT = r"C:\Users\Chad\Dropbox\razorblade_mermaid" if os.name == "nt" else os.path.expanduser("~/Dropbox/razorblade_mermaid")
SPEC = "WORKFLOWS/interlocking-arc-model.md"
TDIR = "WRITING/BOARD TEMPLATES/Arcs"
FENCE = re.compile(r"```json\r?\n(.*?)\r?\n```", re.S)
GROUPS = [(1, "Setup: Introduction"), (6, "Incident: Change Event"), (11, "Trials: Hairlines"), (16, "Pinch 1: Fractures"), (21, "Mid-Point: Cracks"), (26, "Pinch 2: Shattering"), (31, "Final Showdown: Change Vs. Failure")]
SPINES = ["antagonist", "external", "lead"]
ROLES = ["lead", "antagonist", "deuteragonist", "X1", "X2", "X3", "X4", "AM1", "AM2", "AM3", "AM4", "AM5"]
PLAN_KEYS = {"cast", "roles", "switches", "plotting", "structure", "external", "board", "spines", "subplots"}
# Subplots (CRE, 2026-10-21): plot arcs with no model role — "the subplot beats would hit the scenes and lines like the others,
# so each unit holds the entirety of narrative needs - plus they are linked to larger arcs". Each carries its own `status`
# (pilot / ruled), so setting them leaves the grid's approval alone: the approval covers the model cells, not the subplots.
SUBPLOT_STEP_KEYS = {"label", "text", "src", "from", "via", "renamed", "cards", "parts", "seq", "ch", "unplaced", "ruling"}
SET_KEYS = {"key", "name", "lead", "antagonist", "era", "switches", "external"}
K_OPTIONS = {
    "K1": ["Changed", "Not changed"], "K2": ["V1", "V2", "V3"], "K3": ["None", "PH1", "PH2", "PH3 leading", "PH3 trailing"],
    "K4": ["Evil", "Force of resistance, with intent", "Force of resistance, without intent"], "K5": ["Unchanged", "Redeemed"], "K6": ["False victory", "False defeat"],
}


def die(msg):
    print("REFUSED: " + msg, file=sys.stderr)
    sys.exit(2)


def read_plan(path):
    text = open(path, encoding="utf-8").read()
    m = FENCE.search(text)
    if not m:
        die(f"{path} has no ```json block")
    return text, json.loads(m.group(1))


def model_sha(vault):
    raw = open(os.path.join(vault, SPEC), encoding="utf-8").read()
    cut = raw.find("\n\n---\n\n<!-- SYSTEM WIRING FOOTER")
    return hashlib.sha256(raw[:cut].encode("utf-8")).hexdigest()


def templates(vault):
    out = {}
    d = os.path.join(vault, TDIR)
    for f in sorted(os.listdir(d)):
        if not (f.startswith("IAM — ") and f.endswith(".md")):
            continue
        j = json.loads(FENCE.search(open(os.path.join(d, f), encoding="utf-8").read()).group(1))
        if j.get("iam", {}).get("role"):
            out[j["iam"]["role"]] = {"name": f[:-3], "steps": j["steps"], "sha": j["iam"].get("sha256", "")}
    return out


def effective_steps(t, role=None):
    """A template's steps with the plan's picks applied: an open anchor beat ("29 lost, or 31 if they survive") takes the
    beat the role's `beats` sets for it ("resolves" / "enters" / the step's label)."""
    out = []
    picks = (role or {}).get("beats") or {}
    for s in (t["steps"] if t else []):
        s = dict(s)
        if not s.get("beat") and s.get("beatOptions"):
            key = "resolves" if s["label"].startswith("Resolves") else "enters" if s["label"].startswith("Enters") else s["label"]
            if picks.get(key) in s["beatOptions"]:
                s["beat"] = picks[key]
        out.append(s)
    return out


def step_at(steps, n, carried=True):
    """The step a beat number means — the builder's rule (stepAtBeat in the plugin core): the step that sits at that beat;
    else a compressed step whose rows span it (a step at 21 with the next at 23 spans 21–22); else the one step that carries
    that model beat in its `beats` range. Two carriers → None (asked, never guessed)."""
    for s in steps:
        if s.get("beat") == n:
            return s
    for i, s in enumerate(steps):
        if s.get("beat") and s.get("beats"):
            nxt = next((x["beat"] for x in steps[i + 1:] if x.get("beat")), None)
            if s["beat"] <= n <= (nxt - 1 if nxt else s["beat"]):
                return s
    if not carried:
        return None
    carriers = [s for s in steps if s.get("beats") and s["beats"][0] <= n <= s["beats"][1]]
    return carriers[0] if len(carriers) == 1 else None


def open_at(steps, n):
    """Open anchor steps that could land at n (their beat not yet picked)."""
    return [s for s in steps if not s.get("beat") and n in (s.get("beatOptions") or [])]


def group_of(n):
    g = [x for x in GROUPS if x[0] <= n][-1]
    return g[1]


def spine_set(plan, key):
    """An extra spine set by key (0.65), or None."""
    return next((s for s in plan.get("spines") or [] if s.get("key") == key), None)


def beats_of(plan, key=None):
    """The beat list of the main set (key None) or of an extra set."""
    return plan.get("beats", []) if not key else (spine_set(plan, key) or {}).get("beats", [])


def beat_entry(plan, n, spine, cast=None, sub=None, beats=None):
    for b in (plan.get("beats", []) if beats is None else beats):
        if b.get("n") == n and b.get("spine") == spine and (b.get("cast") or None) == (cast or None) and (b.get("sub") or None) == (sub or None):
            return b
    return None


def entry_for(plan, spine, cast, steps, step, sub=None, beats=None):
    """The plan's entry for a step, whichever of its beat numbers CRE used (B21 or B22 for a step spanning 21–22)."""
    for b in (plan.get("beats", []) if beats is None else beats):
        if b.get("spine") == spine and (b.get("cast") or None) == (cast or None) and (b.get("sub") or None) == (sub or None):
            if step_at(steps, b["n"]) is step:
                return b
    return None


def render(path, plan, vault):
    """Regenerate everything above the JSON block from the JSON (the JSON is the record)."""
    T = templates(vault)
    cast = {c["key"]: c["name"] for c in plan.get("cast", [])}
    roles = plan.get("roles", [])
    sw = plan.get("switches", {})
    lines = ["---", "type: iam-plan", f"board: \"{plan['board'].get('path', '')}\"", f"status: {plan.get('status', 'draft')}", "---", "",
             f"# {plan['board'].get('title') or 'Board'} — arc plan", "",
             "Interlocking Arc Model plan, written by the branch-writing-expert skill (plotting mode). **The JSON block at the bottom is the record**; this summary and table are regenerated from it by `plan_tool.py render` and are never hand-edited. Every filled cell is CRE's words (its `src` says where they came from); an open cell is a valid, labelled blank.", ""]
    ap = plan.get("approved")
    lines += [f"**Approved:** {ap['date']} (\"{ap['phrase']}\")" if ap else "**Approved:** not yet — the builder refuses an unapproved plan. CRE approves with \"approve the plan\".", ""]
    lines += ["**Switches:** " + " · ".join(f"{k}: {sw.get(k) or 'open'}" for k in ["K1", "K2", "K3", "K4", "K5", "K6"]) + " · K7/K8: derived from the roles", ""]
    lines += ["**Cast and roles:** " + ("; ".join(f"{cast.get(r['cast'], r['cast'])} — {r['role']}" + (f" (faces {cast.get(r['against'], r['against'])})" if r.get("against") else "") for r in roles) or "none yet"), ""]
    pl = plan.get("plotting") or {}
    lines += [f"**Statement Plotting:** {'on' if pl.get('on') else 'off'}" + (f" · roster: {', '.join(cast.get(k, k) for k in pl.get('leads', []))}" if pl.get("leads") else ""), ""]
    if plan.get("structure"):
        lines += ["**Containers (only those CRE named):** " + "; ".join(f"{s['kind']} {s['title']}" + (f" under {s['under']}" if s.get("under") else "") for s in plan["structure"]), ""]
    # Columns: the three spines, then every other role in use.
    cols = [("antagonist", None), ("external", None), ("lead", None)] + [(r["role"], r["cast"]) for r in roles if r["role"] not in ("lead", "antagonist")]
    head = ["#"] + [("external" if c == "external" else f"{c} · {cast.get(k, '') if k else next((cast.get(r['cast'], '') for r in roles if r['role'] == c), '')}").strip(" ·") for c, k in cols]
    lines += ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    colsteps = []
    for c, k in cols:
        role = next((r for r in roles if r["role"] == c and (k is None or r["cast"] == k)), None)
        colsteps.append(effective_steps(T.get(c), role))
    esc = lambda x: x.replace("|", "/")
    last_group = None
    for n in range(1, 36):
        g = group_of(n)
        if g != last_group:
            lines.append("| | **" + g + "** |" + " |" * (len(head) - 2))
            last_group = g
        row = [f"B{n}"]
        for (c, k), steps in zip(cols, colsteps):
            ck = k if c not in SPINES else None
            st = step_at(steps, n, carried=False)  # the table shows a step on the rows it sits on, never on the beats it carries
            if not st:
                op = open_at(steps, n)
                row.append("; ".join("*beat not picked:* " + esc(s["label"]) for s in op))
                continue
            b = entry_for(plan, c, ck, steps, st)
            words = (b or {}).get("text")
            cell = esc(words) if words else "*open:* " + esc(st["label"])
            cell += layers(b, esc)
            if st.get("beat") != n:
                cell = "↑ " + cell  # the same step as the row it sits at (a compressed range)
            subs = [(x, beat_entry(plan, n, c, ck, x)) for x in ("a", "b")]
            if n == 34 and c == "deuteragonist":
                e = subs[1][1]  # V2/V3: the deuteragonist's Moment of Truth at 34b is its own B34
                if e and e.get("text") and not words:
                    cell = esc(e["text"]) + " (34b)"
            elif n == 34 and any(e for _, e in subs):
                cell += "".join(f" · 34{x}: " + (esc(e["text"]) if e and e.get("text") else "*open*") for x, e in subs)
            row.append(cell)
        lines.append("| " + " | ".join(row) + " |")
    for sp in plan.get("spines") or []:
        lines += render_set(plan, sp, T, cast, esc)
    for sp in plan.get("subplots") or []:
        lines += render_subplot(sp, esc)
    lines += ["", "```json", json.dumps(plan, indent=2, ensure_ascii=False), "```", ""]
    out = "\n".join(lines)
    json.loads(FENCE.search(out).group(1))  # parse gate
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    back = json.loads(FENCE.search(open(path, encoding="utf-8").read()).group(1))
    if back != plan:
        die("parse gate: the plan did not read back identical")


def render_subplot(sp, esc):
    """A subplot (a plot arc with no model role): its fields, then its steps in story order with where each one lands."""
    out = ["", f"## Subplot: {sp['label']}" + (" *(working label — his call)*" if sp.get("labelOpen") else "") + f" — {sp.get('status', 'pilot')}", ""]
    for k in ("goal_holder", "goal", "stakes", "planned_outcome"):
        out.append(f"- **{k.replace('_', ' ')}:** " + (esc(str(sp[k])) if sp.get(k) else "*open — his call*"))
    if sp.get("sources"):
        out.append("- **sources:** " + "; ".join(sp["sources"]))
    out += ["", "| # | step | his words | lands |", "|---|---|---|---|"]
    for i, st in enumerate(sp.get("steps") or [], 1):
        if st.get("parts"):
            lands = "sub-steps: " + "; ".join(f"{esc(p['text'][:40])} → [{p.get('card') or p.get('via') or '?'}]" for p in st["parts"])
        elif st.get("cards"):
            lands = "line of the Beat carrying [" + st["cards"][0] + "]"
        elif st.get("via"):
            # the subplot builder's `via` (a Beat, a micro-beat or a scene ref) — 2026-10-22, the second board audit
            lands = "line of [" + esc(str(st["via"])) + "]"
        elif st.get("ruling"):
            lands = "*ruling:* " + esc(st["ruling"])
        else:
            lands = "unplaced — " + esc(st.get("unplaced") or "no board card yet")
        out.append(f"| {i} | {esc(st.get('label', ''))} | {esc(st['text'])}" + (f"<br>*{esc(st['src'])}*" if st.get("src") else "") + f" | {lands} |")
    return out


def layers(b, esc):
    """The two layers beneath a beat statement (2026-10-20, CRE: the cell is the beat; the scene beats carry it; the
    quote proves it): rendered under the text in the same cell. Both optional; the builder ignores them."""
    out = ""
    for s in (b or {}).get("support") or []:
        out += "<br>▸ " + esc(s)
    q = (b or {}).get("quote")
    if q:
        out += "<br>‹" + esc(q) + "›"
    return out


def render_set(plan, sp, T, cast, esc):
    """An extra spine set's section (0.65): its switches, lead and antagonist, and its own three-column table."""
    sw = sp.get("switches") or {}
    beats = sp.get("beats", [])
    out = ["", f"## Spine set: {sp.get('name') or sp['key']}" + (f" — told in {sp['era']}" if sp.get("era") else ""), "",
           f"Key `{sp['key']}` · lead: {cast.get(sp.get('lead'), sp.get('lead') or 'open')} · antagonist: {cast.get(sp.get('antagonist'), sp.get('antagonist') or 'open')}" + (f" · external: {sp['external']['label']}" if (sp.get("external") or {}).get("label") else ""), "",
           "**Switches:** " + " · ".join(f"{k}: {sw.get(k) or 'open'}" for k in ["K1", "K2", "K3", "K4", "K5", "K6"]), ""]
    head = ["#", f"antagonist · {cast.get(sp.get('antagonist'), '')}".strip(" ·"), "external", f"lead · {cast.get(sp.get('lead'), '')}".strip(" ·")]
    out += ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    cols = [(c, effective_steps(T.get(c))) for c in SPINES]
    last_group = None
    for n in range(1, 36):
        g = group_of(n)
        if g != last_group:
            out.append("| | **" + g + "** |" + " |" * (len(head) - 2))
            last_group = g
        row = [f"B{n}"]
        for c, steps in cols:
            st = step_at(steps, n, carried=False)
            if not st:
                row.append("")
                continue
            b = entry_for(plan, c, None, steps, st, beats=beats)
            words = (b or {}).get("text")
            cell = esc(words) if words else "*open:* " + esc(st["label"])
            cell += layers(b, esc)
            subs = [(x, beat_entry(plan, n, c, None, x, beats=beats)) for x in ("a", "b")]
            if n == 34 and any(e for _, e in subs):
                cell += "".join(f" · 34{x}: " + (esc(e["text"]) if e and e.get("text") else "*open*") for x, e in subs)
            row.append(cell)
        out.append("| " + " | ".join(row) + " |")
    return out


def check_spines(plan, part):
    """Validate and merge `spines` by key: a set already there keeps its beats and walked rounds; none is dropped."""
    keys = {c["key"] for c in plan.get("cast", [])} | {c["key"] for c in part.get("cast") or []}
    cur = [dict(s) for s in plan.get("spines") or []]
    for s in part["spines"]:
        if not isinstance(s, dict) or not isinstance(s.get("key"), str) or not s["key"].strip() or s["key"].strip() in ("main", ""):
            die("each spine set needs a \"key\" of its own (not \"main\")")
        bad = set(s) - SET_KEYS
        if bad:
            die(f"a spine set takes only {sorted(SET_KEYS)}; not {sorted(bad)} (its beats go through 'beat --set {s['key']}')")
        for k, v in (s.get("switches") or {}).items():
            if k not in K_OPTIONS or (v is not None and v not in K_OPTIONS[k]):
                die(f"spine set {s['key']} {k}: {v!r} is not one of the model's options {K_OPTIONS.get(k)}")
        for r in ("lead", "antagonist"):
            if s.get(r) is not None and s[r] not in keys:
                die(f"spine set {s['key']}: {r} {s[r]!r} is not a cast key in the plan ({sorted(keys)})")
        old = next((x for x in cur if x["key"] == s["key"]), None)
        if old:
            for k, v in s.items():
                old[k] = {**(old.get(k) or {}), **v} if isinstance(v, dict) and k in ("switches", "external") else v
        else:
            new = {"key": s["key"].strip(), "name": s.get("name") or s["key"].strip(), "lead": s.get("lead"), "antagonist": s.get("antagonist"), "era": s.get("era"),
                   "switches": {k: (s.get("switches") or {}).get(k) for k in K_OPTIONS}, "beats": [], "walked": []}
            if s.get("external"):
                new["external"] = s["external"]
            cur.append(new)
    return cur


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", help="new | set | beat | walk | walked | render | approve | status")
    ap.add_argument("plan")
    ap.add_argument("--vault", default=DEFAULT_VAULT)
    ap.add_argument("--board-path"); ap.add_argument("--title"); ap.add_argument("--copy-of")
    ap.add_argument("--json"); ap.add_argument("--json-file")
    ap.add_argument("--n", type=int); ap.add_argument("--spine"); ap.add_argument("--cast"); ap.add_argument("--sub")
    ap.add_argument("--text"); ap.add_argument("--open", action="store_true")
    ap.add_argument("--who"); ap.add_argument("--at"); ap.add_argument("--src")
    ap.add_argument("--support", help="the scene beats that carry this model beat, '||'-separated (board beat titles with ids, SEQ beat numbers); administrative, never CRE's words")
    ap.add_argument("--quote", help="the execution line: CRE's prose verbatim (or a dev-summary line, prefixed 'dev summary: ')")
    ap.add_argument("--beats"); ap.add_argument("--phrase")
    ap.add_argument("--set", dest="spine_set", help="an extra spine set's key (0.65); none = the main set")
    a = ap.parse_args()
    V = a.vault

    if a.cmd == "new":
        if os.path.exists(a.plan):
            die(f"{a.plan} exists; open it with status instead of starting over")
        if not a.board_path:
            die("--board-path is required")
        sha = model_sha(V)
        plan = {"v": 1, "type": "iam-plan", "status": "draft", "spec": {"file": SPEC, "sha256": sha},
                "board": {"target": "copy" if a.copy_of else "new", "path": a.board_path, "title": a.title or "", "copyOf": a.copy_of or None},
                "plotting": {"on": False, "leads": []}, "switches": {k: None for k in K_OPTIONS}, "cast": [], "roles": [], "beats": [], "structure": [], "approved": None}
        os.makedirs(os.path.dirname(os.path.abspath(a.plan)), exist_ok=True)
        render(a.plan, plan, V)
        print(f"new plan {a.plan} (model {sha[:8]}…)")
        return

    text, plan = read_plan(a.plan)
    part = None
    if a.cmd == "set":
        if a.json_file:
            part = json.loads(open(a.json_file, encoding="utf-8").read())
        elif a.json:
            part = json.loads(a.json)
        else:
            die("set takes --json-file <part.json> (or --json from Git Bash)")
    only_subplots = part is not None and set(part) == {"subplots"}
    if a.cmd in ("set", "beat") and plan.get("approved") and not only_subplots:
        # Any change after approval takes the approval off: CRE approves what will be built.
        plan["approved"] = None
        plan["status"] = "draft"
        print("note: the plan was approved; this change takes the approval off (CRE approves again with \"approve the plan\")")

    if a.cmd == "set":
        bad = set(part) - PLAN_KEYS
        if bad:
            die(f"set takes only {sorted(PLAN_KEYS)}; not {sorted(bad)} (beats go through 'beat', approval through 'approve')")
        for k, v in (part.get("switches") or {}).items():
            if k not in K_OPTIONS or (v is not None and v not in K_OPTIONS[k]):
                die(f"{k}: {v!r} is not one of the model's options {K_OPTIONS.get(k)}")
        for r in part.get("roles") or []:
            if r.get("role") not in ROLES:
                die(f"role {r.get('role')!r} is not a model role {ROLES}")
        for sp in part.get("subplots") or []:
            if not sp.get("key") or not sp.get("label"):
                die("a subplot needs key and label (a working label he rules is fine; it is marked as such)")
            if sp.get("model") or sp.get("role"):
                die(f"subplot {sp['key']}: subplots carry no model role (only the external spine does)")
            for i, st in enumerate(sp.get("steps") or []):
                extra = set(st) - SUBPLOT_STEP_KEYS
                if extra:
                    die(f"subplot {sp['key']} step {i + 1}: unknown keys {sorted(extra)}")
                if not (st.get("text") or "").strip():
                    die(f"subplot {sp['key']} step {i + 1}: text is required — his words, from a ruling or his prose")
        if "spines" in part:
            if not isinstance(part["spines"], list):
                die("spines is a list of spine sets")
            part = {**part, "spines": check_spines(plan, part)}
        for k, v in part.items():
            plan[k] = {**plan.get(k, {}), **v} if isinstance(v, dict) and k in ("switches", "plotting", "board", "external") else v
        render(a.plan, plan, V)
        print("set " + ", ".join(part))
    elif a.cmd == "beat":
        if not a.n or not a.spine:
            die("--n and --spine are required")
        if a.text is None and not a.open and a.at is None and a.who is None and a.support is None and a.quote is None:
            die("give the beat with --text, --open for an open blank, --support / --quote for the layers beneath it, or --at / --who to place or tag a beat")
        if a.spine_set:
            sp = spine_set(plan, a.spine_set)
            if not sp:
                die(f"no spine set {a.spine_set!r} in the plan ({', '.join(s['key'] for s in plan.get('spines') or []) or 'none yet'}); add it with set --json-file")
            if a.spine not in SPINES or a.cast:
                die(f"a spine set has three columns: {', '.join(SPINES)} (no --cast)")
            beats = sp.setdefault("beats", [])
        else:
            beats = plan.setdefault("beats", [])
        b = beat_entry(plan, a.n, a.spine, a.cast, a.sub, beats=beats)
        if not b:
            b = {"n": a.n, "spine": a.spine}
            if a.cast:
                b["cast"] = a.cast
            if a.sub:
                b["sub"] = a.sub
            beats.append(b)
        if a.open:
            b["text"] = None
        elif a.text is not None:
            b["text"] = a.text
        if a.who is not None:
            b["who"] = [x.strip() for x in a.who.split(",") if x.strip()]
        if a.at is not None:
            b["at"] = a.at or None
        if a.src:
            b["src"] = a.src
        if a.support is not None:
            b["support"] = [s.strip() for s in a.support.split("||") if s.strip()]
        if a.quote is not None:
            b["quote"] = a.quote or None
        beats.sort(key=lambda x: (x["n"], x.get("sub") or "", SPINES.index(x["spine"]) if x["spine"] in SPINES else 9, x.get("cast") or ""))
        render(a.plan, plan, V)
        print(f"{a.spine_set + ' ' if a.spine_set else ''}B{a.n}{a.sub or ''} {a.spine}{' (' + a.cast + ')' if a.cast else ''}: {'open' if a.open else 'set' if a.text is not None else 'placed/tagged'}")
    elif a.cmd == "render":
        render(a.plan, plan, V)
        print("rendered")
    elif a.cmd == "approve":
        if (a.phrase or "").strip().lower().rstrip(".!") != "approve the plan":
            die("only CRE's phrase \"approve the plan\" approves a plan")
        if plan.get("spec", {}).get("sha256") and plan["spec"]["sha256"] != model_sha(V):
            die("the model changed since this plan was started; regenerate the templates and re-walk the changed beats first")
        plan["approved"] = {"date": datetime.date.today().isoformat(), "phrase": "approve the plan"}
        plan["status"] = "approved"
        render(a.plan, plan, V)
        print("approved " + plan["approved"]["date"])
    elif a.cmd == "walk":
        T = templates(V)
        lo, hi = (int(x) for x in (a.beats or "1-5").split("-"))
        cast = {c["key"]: c["name"] for c in plan.get("cast", [])}
        ss = None
        if a.spine_set:
            ss = spine_set(plan, a.spine_set)
            if not ss:
                die(f"no spine set {a.spine_set!r} in the plan")
        print(f"## {(ss.get('name') or ss['key']) + ' — ' if ss else ''}{group_of(lo)} — beats {lo}–{hi}\n")
        for n in range(lo, hi + 1):
            print(f"### B{n}")
            for sp in SPINES:
                steps = effective_steps(T.get(sp))
                st = step_at(steps, n)
                b = entry_for(plan, sp, None, steps, st, beats=beats_of(plan, a.spine_set)) if st else None
                who = cast.get((ss or {}).get(sp), "") if ss and sp != "external" else ""
                print(f"- **{sp}{' · ' + who if who else ''}** — {st['label'] if st else '?'}: {(b or {}).get('text') or 'open'}")
                if st and st.get("hint"):
                    print(f"  - asks: {st['hint']}")
            for r in ([] if ss else plan.get("roles", [])):
                if r["role"] in ("lead", "antagonist"):
                    continue
                steps = effective_steps(T.get(r["role"]), r)
                hit = step_at(steps, n)
                for st in ([hit] if hit else []) + open_at(steps, n):
                    if True:
                        b = entry_for(plan, r["role"], r["cast"], steps, st) if st.get("beat") else None
                        opened = "" if st.get("beat") == n else f" (one step for beats {st['beats'][0]}–{st['beats'][1]}, sitting at B{st['beat']})" if st.get("beats") else f" (beat open: {', '.join(map(str, st['beatOptions']))})" if not st.get("beat") else ""
                        print(f"- **{r['role']} · {cast.get(r['cast'], r['cast'])}** — {st['label']}{opened}: {(b or {}).get('text') or 'open'}")
                        if st.get("hint"):
                            print(f"  - asks: {st['hint']}")
            print()
    elif a.cmd == "walked":
        # A round is walked when CRE has been through it (answered or skipped); recorded so a stopped run resumes there.
        lo = int((a.beats or "").split("-")[0] or 0)
        if lo not in [g for g, _ in GROUPS]:
            die("--beats must start a model group: " + ", ".join(str(g) for g, _ in GROUPS))
        tgt = plan
        if a.spine_set:
            tgt = spine_set(plan, a.spine_set)
            if not tgt:
                die(f"no spine set {a.spine_set!r} in the plan")
        tgt["walked"] = sorted(set(tgt.get("walked", [])) | {lo})
        render(a.plan, plan, V)
        print(f"{a.spine_set + ' ' if a.spine_set else ''}round {group_of(lo)} walked")
    elif a.cmd == "status":
        filled = [b for b in plan.get("beats", []) if b.get("text")]
        walked = set(plan.get("walked", []))
        nxt = next((g for g, _ in GROUPS if g not in walked), None)
        print(f"plan {a.plan}: {len(plan.get('cast', []))} cast, {len(plan.get('roles', []))} roles, {len(filled)} beats in CRE's words (every other beat is an open blank); rounds walked: {len(walked)} of 7; next round starts at {'B' + str(nxt) + ' (' + group_of(nxt) + ')' if nxt else '— (walk complete)'}; approved: {bool(plan.get('approved'))}")
        for sp in plan.get("spines") or []:
            f2 = [b for b in sp.get("beats", []) if b.get("text")]
            w2 = set(sp.get("walked", []))
            n2 = next((g for g, _ in GROUPS if g not in w2), None)
            print(f"  spine set {sp.get('name') or sp['key']} (--set {sp['key']}): {len(f2)} beats in CRE's words; rounds walked: {len(w2)} of 7; next round starts at {'B' + str(n2) + ' (' + group_of(n2) + ')' if n2 else '— (walk complete)'}")
    else:
        die("unknown command " + a.cmd)


if __name__ == "__main__":
    main()
