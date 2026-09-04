#!/usr/bin/env python3
"""lint_bootstrap.py - the deterministic half of the bootstrap-manager pass.

Two jobs, both mechanical:

  1. SIZE   - census the five files every session loads (CLAUDE.md + the four
              loading-order anchors) so the report can state the boot budget.
  2. REPORT - enforce the evidence bar on a bootstrap-review report:
              every PROPOSED item carries >= 2 distinct citations, nothing under
              the bar sits outside QUERY, every item names a target and quotes
              replacement text, a Not-checked section states a date range, and a
              regeneration list exists whenever an item targets CLAUDE.md.

It normalises the arithmetic. It never decides an item - proposal quality is
CRE's call, per WORKFLOWS/bootstrap-manager.md.

Substrate (DIR-020): any non-mount host. Preferred route is the desktop shell
(Desktop Commander / windows-cli), which reads the real Dropbox folder; sandbox
bash is an acceptable second. If neither runs, the checks are performed by hand
from the file-tools read and the report says so under Not checked.

stdlib only (DIR-007 - nothing installs on the mount).
Exit 0 clean - 1 findings - 2 gate failure.
"""

import argparse
import io
import json
import os
import re
import sys
import tempfile

# The Windows console defaults to cp1252 and the vault's arrows and dashes
# crash it. Force UTF-8 at entry (DIR-020, console-encoding-safe).
for _stream in ("stdout", "stderr"):
    _s = getattr(sys, _stream, None)
    if _s is not None and hasattr(_s, "buffer"):
        setattr(sys, _stream, io.TextIOWrapper(_s.buffer, encoding="utf-8", errors="replace"))

BOOT_FILES = [
    "CLAUDE.md",
    "_ME.md",
    "_VAULT MAP.md",
    "_SKILLS MAP.md",
    "_DIRECTIVES.md",
]

# Bin headings the report must use.
BIN_HEADINGS = {
    "BATCH-RATIFY": re.compile(r"^#{2,3}\s*\d?\.?\s*BATCH-RATIFY\b", re.I | re.M),
    "PROPOSED": re.compile(r"^#{2,3}\s*\d?\.?\s*PROPOSED\b", re.I | re.M),
    "QUERY": re.compile(r"^#{2,3}\s*\d?\.?\s*QUERY\b", re.I | re.M),
}

# An item opens with a level-4 heading carrying a bin-prefixed id: B1 / P1 / Q1.
ITEM_RE = re.compile(r"^#{3,4}\s+([BPQ])(\d+)\s*(?:[-—:]\s*(.*))?$", re.M)

# Citation shapes that count. Each distinct match is one citation; two
# citations of the same anchor count once (the bar is two INDEPENDENT
# instances, so a repeated anchor is one instance).
CITE_PATTERNS = [
    re.compile(r"\^obs-\d+"),
    re.compile(r"\^cobs-\d+"),
    re.compile(r"\^wgt-\d+"),
    re.compile(r"\bdec-\d{3}\b"),
    re.compile(r"\bDIR-\d{3}\b"),
    re.compile(r"\bCDIR-\d{3}\b"),
    re.compile(r"`[^`\n]*?\.md[^`\n]*?`"),
    re.compile(r"\b_(?:CHANGELOG|QUICK LOG|OBSERVATIONS)\b[^.\n]{0,40}?\d{4}-\d{2}-\d{2}"),
    re.compile(r"\bPattern\s+#\d+"),
]

TARGET_RE = re.compile(r"\*\*Target:\*\*", re.I)
TEXT_RE = re.compile(r"\*\*(?:Proposed text|Replacement text|Cut):\*\*", re.I)
DIRECTION_RE = re.compile(r"\*\*Direction:\*\*\s*(ADD|CUT)\b", re.I)
NOTCHECKED_RE = re.compile(r"^#{2,3}.*not\s+checked", re.I | re.M)
DATERANGE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\s*(?:[-–—>]|to|through)\s*\d{4}-\d{2}-\d{2}", re.I)
REGEN_RE = re.compile(r"^#{2,3}.*regenerat", re.I | re.M)
CLAUDEMD_RE = re.compile(r"\bCLAUDE\.md\b")
CARRY_RE = re.compile(r"^#{2,3}.*(rejected|retired|carried forward)", re.I | re.M)


class Finding:
    __slots__ = ("level", "check", "where", "msg")

    def __init__(self, level, check, where, msg):
        self.level = level          # ERROR | WARN | INFO
        self.check = check
        self.where = where
        self.msg = msg

    def as_dict(self):
        return {"level": self.level, "check": self.check, "where": self.where, "msg": self.msg}

    def __str__(self):
        return "[%-5s] %-10s %s :: %s" % (self.level, self.check, self.where, self.msg)


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


# --------------------------------------------------------------------------
# SIZE - boot-surface census
# --------------------------------------------------------------------------

def census(vault):
    rows = []
    findings = []
    total_bytes = 0
    for name in BOOT_FILES:
        path = os.path.join(vault, name)
        if not os.path.isfile(path):
            findings.append(Finding("ERROR", "SIZE", name, "boot file missing - a partial boot surface cannot be reviewed"))
            continue
        raw = read_text(path)
        nbytes = len(raw.encode("utf-8"))
        total_bytes += nbytes
        rows.append({
            "file": name,
            "bytes": nbytes,
            "words": len(raw.split()),
            "lines": raw.count("\n") + 1,
            "approx_tokens": nbytes // 4,
        })
    rows.append({
        "file": "TOTAL (boot surface)",
        "bytes": total_bytes,
        "words": sum(r["words"] for r in rows),
        "lines": sum(r["lines"] for r in rows),
        "approx_tokens": total_bytes // 4,
    })
    return rows, findings


# --------------------------------------------------------------------------
# REPORT - the evidence bar
# --------------------------------------------------------------------------

def split_items(report_text):
    """Return [(bin_letter, item_id, heading, body)] in document order."""
    items = []
    matches = list(ITEM_RE.finditer(report_text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(report_text)
        # An item body stops at the next level-2 heading, if one comes first.
        nxt = re.search(r"^##\s+", report_text[start:end], re.M)
        if nxt:
            end = start + nxt.start()
        items.append((m.group(1).upper(), m.group(1).upper() + m.group(2),
                      (m.group(3) or "").strip(), report_text[start:end]))
    return items


FIELD_RE = re.compile(r"^\s*\*\*[A-Za-z][^*]{0,30}:\*\*")


def evidence_span(body):
    """Strip the parts of an item that are NOT evidence.

    The target file and the quoted replacement text routinely name .md paths and
    directive ids; counting those as citations lets an item clear the
    two-instance bar on its own subject matter. Only the remainder counts.
    """
    kept = []
    skipping = False
    for line in body.splitlines():
        if TEXT_RE.search(line):
            skipping = True
            continue
        if skipping:
            # A new bold field, a heading, or a list item ends the quoted block.
            if FIELD_RE.match(line) or line.startswith("#"):
                skipping = False
            else:
                continue
        if TARGET_RE.search(line) or DIRECTION_RE.search(line):
            continue
        kept.append(line)
    return "\n".join(kept)


def count_citations(body):
    hits = set()
    span = evidence_span(body)
    for pat in CITE_PATTERNS:
        for m in pat.finditer(span):
            hits.add(m.group(0).strip().lower())
    return hits


def lint_report(report_path):
    findings = []
    if not os.path.isfile(report_path):
        return [Finding("ERROR", "REPORT", report_path, "report not found")], {}
    text = read_text(report_path)

    stats = {"items": 0, "BATCH-RATIFY": 0, "PROPOSED": 0, "QUERY": 0}

    for label, pat in BIN_HEADINGS.items():
        if not pat.search(text):
            findings.append(Finding("ERROR", "BIN", label, "bin heading absent - the report must carry all three bins, even when empty"))

    items = split_items(text)
    stats["items"] = len(items)
    if not items:
        findings.append(Finding("ERROR", "BIN", "report", "no items found - items open with a heading like '### P1 - title'"))

    letter_to_bin = {"B": "BATCH-RATIFY", "P": "PROPOSED", "Q": "QUERY"}
    for letter, item_id, heading, body in items:
        binname = letter_to_bin.get(letter, "?")
        stats[binname] = stats.get(binname, 0) + 1
        cites = count_citations(body)
        ncites = len(cites)

        if letter == "P":
            if ncites < 2:
                findings.append(Finding(
                    "ERROR", "CITES", item_id,
                    "PROPOSED with %d distinct citation(s) - under the two-instance bar, move to QUERY" % ncites))
            if not TARGET_RE.search(body):
                findings.append(Finding("ERROR", "TEXT", item_id, "no '**Target:**' line - every item names the file it changes"))
            if not TEXT_RE.search(body):
                findings.append(Finding("ERROR", "TEXT", item_id, "no quoted replacement text ('**Proposed text:**' / '**Cut:**')"))
            if not DIRECTION_RE.search(body):
                findings.append(Finding("WARN", "TEXT", item_id, "no '**Direction:** ADD|CUT' line - cuts and adds are graded on the same bar"))

        if letter == "B":
            if not TARGET_RE.search(body):
                findings.append(Finding("WARN", "TEXT", item_id, "BATCH-RATIFY item names no target file"))

        if letter == "Q" and ncites >= 2:
            findings.append(Finding(
                "INFO", "BIN", item_id,
                "QUERY carries %d citations - if both are independent instances this may belong in PROPOSED" % ncites))

    # Coverage statement (DIR-018).
    if not NOTCHECKED_RE.search(text):
        findings.append(Finding("ERROR", "NOTCHECKED", "report", "no 'Not checked' section - a review that passed on partial evidence has not reviewed the thing"))
    elif not DATERANGE_RE.search(text):
        findings.append(Finding("WARN", "NOTCHECKED", "report", "'Not checked' section states no date range (YYYY-MM-DD to YYYY-MM-DD)"))

    # Derived-surface regeneration list (DIR-016).
    targets_claude = any(
        CLAUDEMD_RE.search(body) and TARGET_RE.search(body)
        for letter, _id, _h, body in items if letter in ("B", "P"))
    if targets_claude and not REGEN_RE.search(text):
        findings.append(Finding("ERROR", "REGEN", "report", "an item targets CLAUDE.md but no regeneration list is present (DIR-016)"))

    # Carry-forward list.
    if not CARRY_RE.search(text):
        findings.append(Finding("WARN", "CARRY", "report", "no rejected/retired carry-forward section - a later run will re-propose a closed call"))

    return findings, stats


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

GOOD_REPORT = """# bootstrap review

## BATCH-RATIFY

### B1 - fix a stale count
**Target:** `_ME.md` frontmatter
**Proposed text:** `file: 1-of-4`

## PROPOSED

### P1 - name the gate rule
**Target:** `_ME.md` -> How I work with AI
**Direction:** ADD
**Evidence:** `^obs-260` and `^obs-264`
**Proposed text:** "Never leave work waiting on CRE to remember it."

## QUERY

### Q1 - only one instance
**Target:** `CLAUDE.md`
**Evidence:** `^obs-275`

## Derived-surface regeneration list
- _SESSION START.md

## Rejected / retired, carried forward
- none (no prior review)

## Not checked (DIR-018)
Covered 2026-06-14 to 2026-09-04. Session transcripts unreachable.
"""

BAD_REPORT = """# bootstrap review

## BATCH-RATIFY

## PROPOSED

### P1 - one citation only
**Target:** `CLAUDE.md`
**Evidence:** `^obs-260`
**Proposed text:** "something"

### P2 - no target, no text
**Evidence:** `^obs-260` and `^obs-264`

## QUERY
"""


def selftest():
    ok = True
    tmp = tempfile.mkdtemp(prefix="lint_bootstrap_")

    good = os.path.join(tmp, "good.md")
    with open(good, "w", encoding="utf-8") as fh:
        fh.write(GOOD_REPORT)
    f, stats = lint_report(good)
    errs = [x for x in f if x.level == "ERROR"]
    if errs:
        ok = False
        print("SELFTEST FAIL: clean report produced errors:")
        for e in errs:
            print("   ", e)
    else:
        print("  pass: clean report -> 0 errors")
    if stats.get("PROPOSED") != 1 or stats.get("QUERY") != 1 or stats.get("BATCH-RATIFY") != 1:
        ok = False
        print("SELFTEST FAIL: bin counts wrong:", stats)
    else:
        print("  pass: bin counts 1/1/1")

    bad = os.path.join(tmp, "bad.md")
    with open(bad, "w", encoding="utf-8") as fh:
        fh.write(BAD_REPORT)
    f, _ = lint_report(bad)
    checks = set(x.check for x in f if x.level == "ERROR")
    for want in ("CITES", "TEXT", "NOTCHECKED", "REGEN"):
        if want in checks:
            print("  pass: caught %s" % want)
        else:
            ok = False
            print("SELFTEST FAIL: missed %s (got %s)" % (want, sorted(checks)))

    missing = os.path.join(tmp, "nope.md")
    f, _ = lint_report(missing)
    if f and f[0].check == "REPORT":
        print("  pass: missing report gated")
    else:
        ok = False
        print("SELFTEST FAIL: missing report not gated")

    print("SELFTEST", "GREEN" if ok else "RED")
    return 0 if ok else 1


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="bootstrap-manager deterministic linter")
    ap.add_argument("--vault", help="vault root (for the boot-surface census)")
    ap.add_argument("--report", help="path to the bootstrap-review report to lint")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--selftest", action="store_true", help="run the built-in catch tests")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if not args.vault and not args.report:
        ap.print_help()
        return 2

    findings = []
    out = {"census": [], "stats": {}, "findings": []}

    if args.vault:
        if not os.path.isdir(args.vault):
            print("[ERROR] gate: --vault is not a directory: %s" % args.vault)
            return 2
        rows, f = census(args.vault)
        findings.extend(f)
        out["census"] = rows

    if args.report:
        rp = args.report
        if args.vault and not os.path.isabs(rp):
            rp = os.path.join(args.vault, rp)
        f, stats = lint_report(rp)
        if f and f[0].check == "REPORT":
            print("[ERROR] gate: %s" % f[0].msg)
            return 2
        findings.extend(f)
        out["stats"] = stats

    out["findings"] = [x.as_dict() for x in findings]

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        if out["census"]:
            print("BOOT SURFACE CENSUS")
            print("  %-24s %9s %8s %7s %9s" % ("file", "bytes", "words", "lines", "~tokens"))
            for r in out["census"]:
                print("  %-24s %9d %8d %7d %9d" % (r["file"], r["bytes"], r["words"], r["lines"], r["approx_tokens"]))
            print("")
        if out["stats"]:
            s = out["stats"]
            print("REPORT BINS: BATCH-RATIFY %d - PROPOSED %d - QUERY %d (items %d)" % (
                s.get("BATCH-RATIFY", 0), s.get("PROPOSED", 0), s.get("QUERY", 0), s.get("items", 0)))
            print("")
        if findings:
            print("FINDINGS")
            for x in findings:
                print("  %s" % x)
        else:
            print("FINDINGS: none")

    return 1 if any(x.level == "ERROR" for x in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
