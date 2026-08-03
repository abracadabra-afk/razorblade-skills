#!/usr/bin/env python3
"""
task-audit — reconcile each scheduled task's live SKILL.md prompt against its
WORKFLOWS/<name>.md canon doc. The sibling of skill-audit for the SCHEDULED-TASK spine.

skill-audit reconciles the Cowork-skill chain (doc -> .skill build -> installed copy).
This reconciles the OTHER runtime surface: a scheduled task runs a prompt stored at
  C:\\Users\\Chad\\Claude\\Scheduled\\<task>\\SKILL.md
a hand-maintained file that can silently lag its WORKFLOWS/<name>.md doc (^obs-113 / the
2026-06-24 prompt-drift audit). Nothing else reconciles those two.

Three prompt SHAPES, three drift profiles (^obs-124):
  doc-deferring    "Read WORKFLOWS/<name>.md and follow it"   -> drift-RESISTANT
  inline-behavior  procedure baked into the SKILL.md body     -> drift-PRONE  (both real hits)
  runner-staged    logic in runner.py staged each run         -> prompt drift COSMETIC

The scheduler dir is HOST-side and NOT reachable from sandbox bash, so the skill (Stage B)
stages each prompt via the file tools into a scratch dir that THIS script reads (the same
"stage off the mount, read the clean copy" discipline as ^obs-103). Read-only diagnosis:
every fix stays CRE-attended via update_scheduled_task — and per ^obs-138 the prompt is
passed BODY-ONLY (no --- frontmatter) or the frontmatter doubles.

Usage:
  task_audit.py --prompts-dir <scratch> --workflows <VAULT/WORKFLOWS> --map <map.json> [--json]
  task_audit.py --selftest
"""
import argparse, os, sys, glob, json, hashlib, re

def _has(rx, flags=0):
    rgx = re.compile(rx, flags)
    return lambda body: bool(rgx.search(body))

def _writes_changelog(body):
    return "_CHANGELOG" in body

# A corrected prompt still CONTAINS the word "foot-append" (e.g. "never a foot-append"),
# so match only an UN-NEGATED (authorizing) occurrence. ^obs-143.
_NEG = re.compile(r"\b(never|not|rather than|do not|don't|avoid|instead of|no longer)\b", re.I)
_FOOT = re.compile(r"foot-?append|append\s+(?:it\s+)?(?:safely\s+)?(?:at|to)\s+the\s+(?:foot|end|bottom)", re.I)

# STALE-BOOK-NAME had the mirror-image of the ^obs-143 problem, in BOTH directions (2026-08-03):
#   (a) it was CASE-SENSITIVE (`VIBEBOOK|TASKBOOK|DOBOOK|DoBook|LIFEBOOK`, no re.I), so the live
#       drift — "note it for Taskbook", "weave Vibebook's fragments" — was INVISIBLE to it; while
#   (b) it fired on the prompt's own PROHIBITION clause ("do NOT use the old VIBEBOOK/... paths"),
#       i.e. the one sentence that proves the prompt is correct. A false positive on the fix.
# Same shape as _foot_append_authorized: match case-insensitively, then discount any occurrence on
# a line that RETIRES the name rather than using it. Line-scoped, not a 30-char lookbehind, because
# the retirement marker often trails the name ("Vibebook, Taskbook — are dead: never use them").
_BOOKS = re.compile(r"\b(VIBEBOOK|TASKBOOK|DOBOOK|LIFEBOOK)\b", re.I)
_RETIRED_MARKER = re.compile(
    r"\b(never|not|no longer|retired|renamed|the old|old \w+ paths|dead|do not exist|"
    r"deprecated|forbidden|legacy|instead of|→|->)\b|→", re.I)

def _stale_book_name(body):
    for line in body.splitlines():
        if _BOOKS.search(line) and not _RETIRED_MARKER.search(line):
            return True   # a live use of a retired root name, not a prohibition against it
    return False


# STALE-SNAPSHOT (2026-08-03). A prompt that measures or decides off a DATED artifact — a
# SYSTEM/reports/*.json size stamp, a cached scan, any "report written by <the desktop sync>" —
# is reading a claim, not probing a state (DIR-010). The live instance: vault-health measured off
# `brain-doc-sizes.json` 43 min old, inside its documented <=36h window and fully compliant, yet
# already ~13.5K stale on _CHANGELOG because ONE session had written to all three brain docs in
# between. An age window is necessary and NOT sufficient: it cannot see intra-window writes.
# So the lint asks for BOTH — some age/freshness notion AND some has-anything-changed notion.
_SNAPSHOT_RX = re.compile(
    r"SYSTEM/reports/\S+\.json|brain-doc-sizes|size stamp|pre-computed|cached (?:report|scan)"
    r"|snapshot(?:ted)?\b", re.I)
_AGE_RX = re.compile(
    r"\bfresh(?:ness)?\b|\bgenerated\b|timestamp|\bstale\b|\bage\b|hours? old|h old|"
    r"\bre-?measure\b|written (?:since|after)|newest entry|has (?:anything|written)", re.I)

def _reads_snapshot(body):
    return bool(_SNAPSHOT_RX.search(body))

def _tests_snapshot_age(body):
    return bool(_AGE_RX.search(body))


# A doc-deferring prompt is supposed to be a LOADER — the doc is the behavior and the prompt
# carries no procedure of its own. In practice they all ship an "In brief:" / "Summary of what to
# do:" block, and THAT block silently goes stale while the shape verdict stays CLEAN. This is the
# hole the 2026-08-03 audit fell into: vault-health was the only deterministically-CLEAN row, so
# it never went to Stage B, and its summary was instructing an in-sandbox _CHANGELOG carve that
# the doc explicitly forbids (^obs-083/^obs-084). CLEAN is a SHAPE verdict, not a CONTENT verdict.
# Fix: an unstamped summary block routes to REVIEW. A `tracks:` stamp clears it, because a stamp
# turns doc movement into an exact DRIFT-EXACT signal — which is the whole point of stamping.
SUMMARY_RX = re.compile(
    r"in brief\b|summary of (?:what|that|the)|the outline below|steps? summar|"
    r"summary only, the doc wins|orientation only", re.I)


def _foot_append_authorized(body):
    if not _writes_changelog(body):
        return False
    for m in _FOOT.finditer(body):
        pre = body[max(0, m.start() - 30):m.start()]
        if not _NEG.search(pre):
            return True   # an authorizing (non-forbidden) foot-append instruction
    return False

# ---------------------------------------------------------------------------
# Convention lint signals. severity HIGH/MED flips a verdict to DRIFT-MECH;
# ADVISORY only annotates. Extend this list as retired conventions appear.
# ---------------------------------------------------------------------------
LINT = [
    dict(id="STALE-BOOK-NAME", sev="HIGH",
         test=_stale_book_name,
         blurb="live use of a pre-2026-06-14 book name (VIBES/TASKS/WORKFLOWS/LIFE now) — the books-daily HIGH hit; a line that RETIRES the name doesn't count"),
    dict(id="STALE-SCHED-PATH", sev="HIGH",
         test=_has(r"OneDrive[\\/]+Documents[\\/]+Claude[\\/]+Scheduled"),
         blurb="wrong scheduler path — real path is C:\\Users\\Chad\\Claude\\Scheduled (an edit there silently no-ops)"),
    dict(id="CHANGELOG-FOOT-APPEND", sev="MED",
         test=_foot_append_authorized,
         blurb="authorizes a _CHANGELOG foot-append — the inversion bug vault-health repairs; the research-runner MED hit"),
    dict(id="MISSING-NUL-GUARD", sev="ADVISORY",
         test=lambda b: _writes_changelog(b) and not re.search(r"\^obs-084|NUL", b),
         blurb="writes _CHANGELOG but names no ^obs-084 NUL-mount guard (the convention every sibling carries)"),
    dict(id="STALE-SNAPSHOT", sev="MED",
         test=lambda b: _reads_snapshot(b) and not _tests_snapshot_age(b),
         blurb="measures/decides off a dated report or snapshot with no freshness test — an age window alone cannot see writes made after the stamp (the 2026-08-03 vault-health instance)"),
]

# A loader is "<verb> [`|'|"]WORKFLOWS/<doc>.md". The original pattern matched only a BARE
# `Read WORKFLOWS/x.md` — no quoting, one verb — and the house convention had since drifted to
# BACKTICKED paths and other verbs (run / open / execute / at). Result (2026-08-03 audit): five
# doc-deferring prompts misfiled as inline-behavior, producing 5 spurious REVIEW/NO-DOC rows and
# 3 bogus SHAPE-CHANGED notes; only the two unbackticked prompts classified correctly.
#
# Per DIR-014's corollary this widens the EXACT layer only — the path still has to match
# literally, so there is no new false-positive surface. Never widen a fuzzy threshold to catch
# a semantic miss.
LOADER_VERBS = r"read|run|open|execute|follow|at|per|in|doc|workflow"
LOADER_RX = re.compile(
    r"(?:%s)\s+(?:the\s+(?:workflow\s+)?(?:doc\s+)?)?[`'\"\[(]{0,2}"
    r"(?:\$?VAULT[\\/]+|\.?[\\/])?WORKFLOWS[\\/]+(\S+?\.md)\b" % LOADER_VERBS, re.I)
# Phrases that mark the prompt as SUBORDINATE to its doc. Extended 2026-08-03 with the house
# phrasings actually in use ("the doc is the behavior", "the doc wins", "this prompt is a loader")
# — same exact-layer widening as LOADER_RX; these are literal conventions, not fuzzy signals.
SUBORDINATE_RX = re.compile(
    r"follow (?:it|its steps|the doc)(?: exactly)?|source of truth|in brief|summary only"
    r"|see the doc|doc is the behavio|the doc wins|is a loader, not a summary"
    r"|execute it exactly as written|do not improvise beyond it", re.I)
RUNNER_RX = re.compile(r"(runner|scaffold_ingest)\.py", re.I)
STAMP_RX = re.compile(r"<!--\s*tracks:\s*(\S+\.md)\s+sha:([0-9a-f]+)", re.I)


def sha12(b):
    return hashlib.sha256(b).hexdigest()[:12]


def strip_frontmatter(text):
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


def classify_shape(body):
    """doc-deferring | inline-behavior | runner-staged (best-effort; Stage B confirms)."""
    if RUNNER_RX.search(body):
        return "runner-staged"
    loaders = LOADER_RX.findall(body)
    if loaders:
        steps = len(re.findall(r"^\s*\d+\.\s", body, re.M))
        if SUBORDINATE_RX.search(body) and steps <= 5:
            return "doc-deferring"
        return "inline-behavior"
    return "inline-behavior"


def lint(body):
    return [(s["id"], s["sev"], s["blurb"]) for s in LINT if s["test"](body)]


def doc_sha(workflows, doc):
    p = os.path.join(workflows, doc)
    if not os.path.isfile(p):
        return None
    with open(p, "rb") as f:
        return sha12(f.read())


def audit_one(name, body, mapinfo, workflows):
    shape = classify_shape(body)
    flags = lint(body)
    hard = [f for f in flags if f[1] in ("HIGH", "MED")]
    advisory = [f for f in flags if f[1] == "ADVISORY"]
    docs = (mapinfo or {}).get("docs", [])
    expect = (mapinfo or {}).get("shape_expect")
    notes, actions = [], []
    verdict = "CLEAN"

    if expect and expect != shape:
        notes.append("SHAPE-CHANGED: expected %s, prompt classifies %s" % (expect, shape))

    for d in LOADER_RX.findall(body):
        if workflows and not os.path.isfile(os.path.join(workflows, d)):
            verdict = "BROKEN-REF"
            actions.append("loader reads WORKFLOWS/%s which does not exist" % d)

    stamp = STAMP_RX.search(body)
    stamped_exact = None
    if stamp and workflows:
        sdoc, ssha = stamp.group(1), stamp.group(2)
        cur = doc_sha(workflows, os.path.basename(sdoc))
        if cur is None:
            notes.append("stamp tracks %s but doc not found" % sdoc)
        elif not cur.startswith(ssha) and not ssha.startswith(cur):
            stamped_exact = (sdoc, ssha, cur)

    if verdict != "BROKEN-REF":
        if hard:
            verdict = "DRIFT-MECH"
            for fid, sev, blurb in hard:
                actions.append("[%s/%s] %s" % (fid, sev, blurb))
        elif stamped_exact:
            verdict = "DRIFT-EXACT"
            actions.append("stamp sha:%s != current %s (doc %s changed since last sync)"
                           % (stamped_exact[1], stamped_exact[2], stamped_exact[0]))
        elif shape == "runner-staged":
            verdict = "INFO"
            notes.append("logic lives in runner.py (staged each run) — prompt drift is cosmetic")
        elif shape == "doc-deferring":
            # CLEAN is a SHAPE verdict. If the loader also carries a summary block and has no
            # tracks: stamp, the summary can be stale with nothing to catch it — route to Stage B.
            if SUMMARY_RX.search(body) and not stamp:
                verdict = "REVIEW"
                notes.append("doc-deferring BUT carries an unstamped summary block — the summary "
                             "can drift from %s with no signal; semantic read needed (Stage B), "
                             "or add a tracks: stamp, or delete the summary" % ", ".join(docs or ["its doc"]))
            else:
                verdict = "CLEAN"
        elif not docs:
            verdict = "NO-DOC"
            notes.append("inline prompt with no mapped doc — author a doc before it can defer (option a)")
        elif not stamp:
            verdict = "REVIEW"
            notes.append("inline prompt, no tracks: stamp — needs a semantic read vs %s (Stage B)" % ", ".join(docs))

    for fid, sev, blurb in advisory:
        notes.append("advisory [%s] %s" % (fid, blurb))
    if shape == "inline-behavior" and docs:
        notes.append("option (a): convert to the doc-deferring loader over %s" % ", ".join(docs))
    return dict(name=name, shape=shape, verdict=verdict, actions=actions, notes=notes,
                flags=[f[0] for f in flags])


def run(prompts_dir, workflows, mapfile, as_json):
    amap = {}
    if mapfile and os.path.isfile(mapfile):
        with open(mapfile) as f:
            amap = json.load(f)
    rows = []
    for p in sorted(glob.glob(os.path.join(prompts_dir, "*.md"))):
        name = os.path.splitext(os.path.basename(p))[0]
        with open(p, "rb") as f:
            text = f.read().decode("utf-8", "replace")
        body = strip_frontmatter(text)
        rows.append(audit_one(name, body, amap.get(name), workflows))

    if as_json:
        print(json.dumps(rows, indent=2))
        return 1 if any(r["verdict"] in ("DRIFT-MECH", "DRIFT-EXACT", "BROKEN-REF") for r in rows) else 0

    print("TASK AUDIT — %d task prompts (workflows=%s)" % (len(rows), workflows))
    print("=" * 80)
    print("%-28s %-15s %-12s" % ("task", "shape", "verdict")); print("-" * 80)
    flagged = []
    for r in rows:
        print("%-28s %-15s %-12s" % (r["name"][:28], r["shape"], r["verdict"]))
        for a in r["actions"]:
            print("      -> " + a)
        for n in r["notes"]:
            print("      .  " + n)
        if r["verdict"] in ("DRIFT-MECH", "DRIFT-EXACT", "BROKEN-REF", "REVIEW", "NO-DOC"):
            flagged.append((r["name"], r["verdict"]))
    print("-" * 80)
    if flagged:
        print("PUNCH LIST:")
        for n, v in flagged:
            print("  [%s] %s" % (v, n))
    else:
        print("All task prompts in sync / accounted for.")
    return 1 if any(r["verdict"] in ("DRIFT-MECH", "DRIFT-EXACT", "BROKEN-REF") for r in rows) else 0


def selftest():
    RUNNER = "STEP 2 — Stage the runner off the mount... run runner.py from the clean copy (^obs-103)."
    DEFER = ("BOOTSTRAP... TASK: Read WORKFLOWS/log-rotate.md and follow its steps exactly. "
             "In brief:\n1. MEASURE...\n2. REPORT...\n3. ROTATE...\n4. GATE...")
    INLINE_LOADER = ("2. LOAD THE WORKFLOW: Read WORKFLOWS/research-briefing.md and follow it in SCHEDULED MODE.\n"
                     "3. PICK ONE: ...\n4. CLASSIFY: ...\n5. RESEARCH: ...\n6. WRITE: ...\n"
                     "7. CLOSE OUT: ...\n8. LOG: append to _CHANGELOG.md ...\n9. DIR-001: ...")
    RR_PRE = "8. LOG: append to _CHANGELOG.md ... a foot-append is acceptable; note placement."
    RR_POST = ("8. LOG: Add a dated entry to _CHANGELOG.md ... INSERT IT AT THE TOP via the FILE TOOLS, "
               "never a foot-append; CHANGELOG MOUNT-ARTIFACT GUARD (^obs-084): trailing NUL bytes...")
    BOOKS_PRE = "STEP 1: Vibebook=VIBEBOOK/CAPTURE.md, Taskbook=TASKBOOK/TASKS.md, DoBook=WORKFLOWS/_DOBOOK.md."
    ONEDRIVE = "edit the prompt at C:\\Users\\Chad\\OneDrive\\Documents\\Claude\\Scheduled\\x\\SKILL.md"
    CLEAN = "Do a thing. Write nothing important. The end."

    # ^obs-NNN (2026-08-03): the loader regex matched only a BARE `Read WORKFLOWS/x.md`, so every
    # backticked or non-"Read"-verb loader read as inline-behavior. These five guard that fix.
    TICK_READ = ("Read `WORKFLOWS/day-launch.md` and execute it exactly as written. "
                 "The doc is the behavior; do not improvise beyond it.\n1. a\n2. b")
    TICK_RUN = ("THEN run `WORKFLOWS/skills-manager.md` — that doc is the source of truth.\n"
                "1. a\n2. b\n3. c")
    TICK_OPEN = ("open `WORKFLOWS/week-shape.md` with the file tools and execute it exactly as "
                 "written (the doc wins if they differ).")
    TICK_AT = "run the workflow at `WORKFLOWS/backlog-sweep.md` — follow the doc.\n1. a\n2. b"
    VERB_EXEC = "STEP 1 — INGEST. Execute WORKFLOWS/inbox-router.md against INBOX.md."
    VAULTVAR = "canonical doc $VAULT/WORKFLOWS/dev-capture.md — follow its steps exactly.\n1. a"

    checks = [
        ("shape runner", classify_shape(RUNNER) == "runner-staged"),
        ("shape defer", classify_shape(DEFER) == "doc-deferring"),
        ("shape inline-loader", classify_shape(INLINE_LOADER) == "inline-behavior"),
        ("shape inline-bare", classify_shape(CLEAN) == "inline-behavior"),
        ("loader backtick Read", LOADER_RX.findall(TICK_READ) == ["day-launch.md"]),
        ("loader backtick run", LOADER_RX.findall(TICK_RUN) == ["skills-manager.md"]),
        ("loader backtick open", LOADER_RX.findall(TICK_OPEN) == ["week-shape.md"]),
        ("loader backtick at", LOADER_RX.findall(TICK_AT) == ["backlog-sweep.md"]),
        ("loader verb Execute", LOADER_RX.findall(VERB_EXEC) == ["inbox-router.md"]),
        ("loader $VAULT prefix", LOADER_RX.findall(VAULTVAR) == ["dev-capture.md"]),
        ("backtick loader classifies defer", classify_shape(TICK_READ) == "doc-deferring"),
        ("no loader stays inline", LOADER_RX.findall(CLEAN) == []),
        ("hit research pre", "CHANGELOG-FOOT-APPEND" in [f[0] for f in lint(RR_PRE)]),
        ("research post clean", "CHANGELOG-FOOT-APPEND" not in [f[0] for f in lint(RR_POST)]),
        ("hit books pre", "STALE-BOOK-NAME" in [f[0] for f in lint(BOOKS_PRE)]),
        # ^obs-143-shaped pair for STALE-BOOK-NAME (2026-08-03): mixed case must HIT, and the
        # prompt's own prohibition clause must NOT.
        ("books mixed-case hits",
         "STALE-BOOK-NAME" in [f[0] for f in lint("Task-guard: pull it out and note it for Taskbook.")]),
        ("books prohibition clears",
         "STALE-BOOK-NAME" not in [f[0] for f in lint(
             "The retired names - Vibebook, Taskbook, LifeBook, DoBook - are dead: never use them.\n"
             "(The restructure renamed Vibebook to VIBES; the old VIBEBOOK/TASKBOOK paths do not exist.)")]),
        ("hit onedrive", "STALE-SCHED-PATH" in [f[0] for f in lint(ONEDRIVE)]),
        ("nul-guard advisory fires", "MISSING-NUL-GUARD" in [f[0] for f in lint(RR_PRE)]),
        ("nul-guard clears post", "MISSING-NUL-GUARD" not in [f[0] for f in lint(RR_POST)]),
        # STALE-SNAPSHOT pair (2026-08-03): reading a dated stamp with no freshness notion HITS;
        # reading it with an age gate AND a has-anything-written-since gate CLEARS.
        ("stale-snapshot fires",
         "STALE-SNAPSHOT" in [f[0] for f in lint(
             "MEASURE from SYSTEM/reports/brain-doc-sizes.json (byte-exact, desktop-written).")]),
        ("stale-snapshot clears",
         "STALE-SNAPSHOT" not in [f[0] for f in lint(
             "MEASURE from SYSTEM/reports/brain-doc-sizes.json. Use it when its generated "
             "timestamp is <=36h old AND nothing has written since — check _CHANGELOG's newest "
             "entry against it; if stale, re-measure with the file tools.")]),
        # CLEAN-is-a-shape-verdict pair: an unstamped doc-deferring summary must route to REVIEW,
        # a stamped one must not. This is the vault-health hole the 2026-08-03 audit missed.
        ("summary block routes to REVIEW",
         audit_one("t", DEFER, {"docs": ["log-rotate.md"], "shape_expect": "doc-deferring"},
                   None)["verdict"] == "REVIEW"),
        ("stamped summary stays CLEAN",
         audit_one("t", DEFER + "\n<!-- tracks: WORKFLOWS/log-rotate.md sha:abc123abc123 -->",
                   {"docs": ["log-rotate.md"], "shape_expect": "doc-deferring"},
                   None)["verdict"] == "CLEAN"),
        ("clean is clean", lint(CLEAN) == []),
    ]
    ok = True
    for label, res in checks:
        print(("PASS " if res else "FAIL ") + label)
        ok = ok and res
    print("-" * 40)
    print("SELFTEST: " + ("ALL PASS (%d)" % len(checks) if ok else "FAILURES PRESENT"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts-dir")
    ap.add_argument("--workflows")
    ap.add_argument("--map")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.prompts_dir or not a.workflows:
        ap.error("--prompts-dir and --workflows are required (or use --selftest)")
    return run(a.prompts_dir, a.workflows, a.map, a.json)


if __name__ == "__main__":
    sys.exit(main())
