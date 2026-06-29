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
         test=_has(r"\b(VIBEBOOK|TASKBOOK|DOBOOK|DoBook|LIFEBOOK)\b"),
         blurb="pre-2026-06-14 book/path name (VIBES/TASKS/WORKFLOWS/LIFE now) — the books-daily HIGH hit"),
    dict(id="STALE-SCHED-PATH", sev="HIGH",
         test=_has(r"OneDrive[\\/]+Documents[\\/]+Claude[\\/]+Scheduled"),
         blurb="wrong scheduler path — real path is C:\\Users\\Chad\\Claude\\Scheduled (an edit there silently no-ops)"),
    dict(id="CHANGELOG-FOOT-APPEND", sev="MED",
         test=_foot_append_authorized,
         blurb="authorizes a _CHANGELOG foot-append — the inversion bug vault-health repairs; the research-runner MED hit"),
    dict(id="MISSING-NUL-GUARD", sev="ADVISORY",
         test=lambda b: _writes_changelog(b) and not re.search(r"\^obs-084|NUL", b),
         blurb="writes _CHANGELOG but names no ^obs-084 NUL-mount guard (the convention every sibling carries)"),
]

LOADER_RX = re.compile(r"Read\s+WORKFLOWS/(\S+?\.md)\b", re.I)
SUBORDINATE_RX = re.compile(
    r"follow (?:it|its steps)(?: exactly)?|source of truth|in brief|summary only|see the doc", re.I)
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

    checks = [
        ("shape runner", classify_shape(RUNNER) == "runner-staged"),
        ("shape defer", classify_shape(DEFER) == "doc-deferring"),
        ("shape inline-loader", classify_shape(INLINE_LOADER) == "inline-behavior"),
        ("shape inline-bare", classify_shape(CLEAN) == "inline-behavior"),
        ("hit research pre", "CHANGELOG-FOOT-APPEND" in [f[0] for f in lint(RR_PRE)]),
        ("research post clean", "CHANGELOG-FOOT-APPEND" not in [f[0] for f in lint(RR_POST)]),
        ("hit books pre", "STALE-BOOK-NAME" in [f[0] for f in lint(BOOKS_PRE)]),
        ("hit onedrive", "STALE-SCHED-PATH" in [f[0] for f in lint(ONEDRIVE)]),
        ("nul-guard advisory fires", "MISSING-NUL-GUARD" in [f[0] for f in lint(RR_PRE)]),
        ("nul-guard clears post", "MISSING-NUL-GUARD" not in [f[0] for f in lint(RR_POST)]),
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
