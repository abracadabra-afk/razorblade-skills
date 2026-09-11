#!/usr/bin/env python3
"""skill-test mechanical shell: scaffold the test tree + report stub, check a finished report.

stdlib only. Console forced to UTF-8 at entry (DIR-020). Never touches the skill under test.

  scaffold --vault V --skill NAME --goal "one line" [--date YYYY-MM-DD] [--json]
  check    --vault V --report PATH [--json]
  --selftest

Exit codes: 0 clean · 1 findings · 2 gate failure (unreadable, bad args).
"""
import argparse
import datetime as _dt
import io
import json
import os
import re
import sys
import tempfile
from pathlib import Path

for _s in ("stdout", "stderr"):
    _f = getattr(sys, _s)
    if hasattr(_f, "buffer"):
        setattr(sys, _s, io.TextIOWrapper(_f.buffer, encoding="utf-8", errors="replace"))

VERDICTS = ("PASS", "PASS-WITH-NOTES", "FAIL")

SECTIONS = [
    "## Verdict line",
    "## Goal and bar",
    "## Runs",
    "## Stand-in rulings",
    "## Consistency",
    "## Verdict detail",
    "## skill-creator handoff",
    "## Drift noticed",
    "## Not checked (DIR-018)",
]

RUN_HEADS = ["### RUN 1", "### RUN 2", "### RUN 3"]

STUB_BODY = """# Skill test — {skill} — {date}

## Verdict line

VERDICT: TBD — one plain sentence.

## Goal and bar

**Goal:** {goal}

**Success conditions (CRE-ruled):**
- (condition 1)

**Test case:** (verbatim)

**Write class:** read-only | writes → fixture at `SYSTEM/skill-tests/{skill}/{date}/fixture/`

## Runs

### RUN 1
(summary + output paths under `SYSTEM/skill-tests/{skill}/{date}/run-1/`)

### RUN 2
(summary + output paths under `SYSTEM/skill-tests/{skill}/{date}/run-2/`)

### RUN 3
(summary + output paths under `SYSTEM/skill-tests/{skill}/{date}/run-3/`)

## Stand-in rulings

| gate question | ruling | basis | runs it reached | re-rule? |
|---|---|---|---|---|
| none reached | — | — | — | — |

## Consistency

(what agreed · what diverged · did it move the verdict)

## Verdict detail

**Sound:**
**Usable:**
**Consistent:**

## skill-creator handoff

None — PASS

## Drift noticed

None noticed. (Route: skill-audit.)

## Not checked (DIR-018)

- (what the test could not exercise)
"""


def _serialize_frontmatter(data: dict) -> str:
    """DIR-004: serialized, never hand-formatted. yaml.safe_dump when present, else
    JSON-escaped double-quoted scalars (valid YAML) for a flat mapping."""
    try:
        import yaml  # type: ignore

        body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    except Exception:
        lines = []
        for k, v in data.items():
            if isinstance(v, list):
                lines.append(f"{k}: [{', '.join(json.dumps(str(x), ensure_ascii=False) for x in v)}]")
            else:
                lines.append(f"{k}: {json.dumps(str(v), ensure_ascii=False)}")
        body = "\n".join(lines) + "\n"
    return "---\n" + body + "---\n\n"


def _parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    raw = m.group(1)
    try:
        import yaml  # type: ignore

        return yaml.safe_load(raw)
    except Exception:
        out = {}
        for line in raw.splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                v = v.strip()
                try:
                    out[k.strip()] = json.loads(v)
                except Exception:
                    out[k.strip()] = v
        return out


def scaffold(vault: Path, skill: str, goal: str, date: str):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", skill):
        return 2, {"error": f"skill name not slug-case: {skill!r}"}, None
    base = vault / "SYSTEM" / "skill-tests" / skill / date
    made = []
    for d in ("fixture", "run-1", "run-2", "run-3", "audit"):
        p = base / d
        p.mkdir(parents=True, exist_ok=True)
        made.append(str(p))
    sr = base / "audit" / "stand-in-rulings.md"
    if not sr.exists():
        sr.write_text(
            "# Stand-in rulings — auditor, gate mode\n\n"
            "One ruling per gate, sent to all three runs (CRE-ruled 2026-09-11).\n\n"
            "| gate question | ruling | basis |\n|---|---|---|\n",
            encoding="utf-8",
        )
    reports = vault / "SYSTEM" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    report = reports / f"{date}-skill-test-{skill}.md"
    if report.exists():
        return 1, {"warning": "report already exists; not overwritten", "report": str(report)}, report
    fm = _serialize_frontmatter(
        {
            "type": "report",
            "workflow": "skill-test",
            "skill": skill,
            "date": date,
            "lane": "meta",
            "verdict": "TBD",
            "test_tree": f"SYSTEM/skill-tests/{skill}/{date}/",
            "status": "in-progress",
        }
    )
    report.write_text(fm + STUB_BODY.format(skill=skill, date=date, goal=goal), encoding="utf-8")
    return 0, {"tree": made, "report": str(report)}, report


def check(vault: Path, report: Path):
    findings = []
    try:
        text = report.read_text(encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        return 2, {"error": f"unreadable: {e}"}
    if len(text.strip()) < 200:
        return 2, {"error": "report too short to be a finished report"}

    fm = _parse_frontmatter(text)
    if not isinstance(fm, dict):
        findings.append("FM: frontmatter missing or unparseable")
        fm = {}

    for s in SECTIONS:
        if not re.search(r"^" + re.escape(s) + r"\s*$", text, re.M):
            findings.append(f"SECTION: missing '{s}'")
    for h in RUN_HEADS:
        if not re.search(r"^" + re.escape(h) + r"\b", text, re.M):
            findings.append(f"RUNS: missing '{h}'")

    m = re.search(r"^VERDICT:\s*([A-Z-]+)", text, re.M)
    verdict = m.group(1) if m else None
    if verdict not in VERDICTS:
        findings.append(f"VERDICT: line missing or not one of {VERDICTS} (got {verdict!r})")
    if verdict and fm.get("verdict") not in (None, verdict):
        findings.append(f"VERDICT: frontmatter says {fm.get('verdict')!r}, body says {verdict!r}")
    if fm and fm.get("verdict") == "TBD":
        findings.append("VERDICT: frontmatter still TBD")

    # Verdict first: the first non-frontmatter, non-title content line must be the verdict.
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    content_lines = [ln for ln in body.splitlines() if ln.strip() and not ln.startswith("# ")]
    if content_lines:
        first = content_lines[0].strip()
        if not (first.startswith("## Verdict line") or first.startswith("VERDICT:")):
            findings.append("ORDER: verdict is not the first content line")
        if len(content_lines) > 1 and content_lines[0].startswith("## Verdict line") and not content_lines[1].startswith("VERDICT:"):
            findings.append("ORDER: '## Verdict line' is not followed by the VERDICT: line")

    # Handoff block present iff verdict short of PASS.
    hm = re.search(r"^## skill-creator handoff\s*$\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    handoff = (hm.group(1).strip() if hm else "")
    if verdict in ("FAIL", "PASS-WITH-NOTES"):
        if not handoff or handoff.startswith("None"):
            findings.append("HANDOFF: verdict short of PASS but handoff block is empty or 'None'")
        elif len(handoff) < 200:
            findings.append("HANDOFF: block too thin to open skill-creator with (<200 chars)")
    elif verdict == "PASS" and handoff and not handoff.startswith("None"):
        findings.append("HANDOFF: PASS verdict carries a handoff block; say 'None — PASS'")

    # Stand-in rulings table present.
    if not re.search(r"^\|\s*gate question\s*\|", text, re.M):
        findings.append("RULINGS: stand-in rulings table missing")

    # Backlog anchor on FAIL / PASS-WITH-NOTES.
    if verdict in ("FAIL", "PASS-WITH-NOTES"):
        skill = fm.get("skill") or (re.search(r"skill-test-([a-z0-9-]+)\.md$", report.name) or [None, None])[1]
        date = fm.get("date") or (re.search(r"^(\d{4}-\d{2}-\d{2})-skill-test", report.name) or [None, None])[1]
        anchor = f"^backlog-skilltest-{skill}-{date}"
        bl = vault / "_BACKLOG.md"
        try:
            bl_text = bl.read_text(encoding="utf-8")
            if anchor not in bl_text:
                findings.append(f"BACKLOG: anchor {anchor} not found in _BACKLOG.md (mount may be stale — confirm by file-tools read)")
        except Exception as e:  # noqa: BLE001
            findings.append(f"BACKLOG: could not read _BACKLOG.md ({e}) — confirm by file-tools read")

    nc = re.search(r"^## Not checked \(DIR-018\)\s*$\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if nc and len(nc.group(1).strip()) < 20:
        findings.append("NOTCHECKED: section present but empty")

    return (1 if findings else 0), {"verdict": verdict, "findings": findings}


def selftest():
    with tempfile.TemporaryDirectory() as td:
        v = Path(td)
        (v / "_BACKLOG.md").write_text("# BACKLOG\n\n## OS / Meta\n\n", encoding="utf-8")
        code, info, rep = scaffold(v, "demo-skill", "Produce a thing.", "2026-01-01")
        assert code == 0, info
        code, info = check(v, rep)
        assert code == 1 and any(f.startswith("VERDICT") for f in info["findings"]), info
        # Fill as a FAIL without backlog → HANDOFF + BACKLOG findings.
        t = rep.read_text(encoding="utf-8")
        t = t.replace("VERDICT: TBD — one plain sentence.", "VERDICT: FAIL — runs disagree.")
        t = t.replace('verdict: "TBD"', 'verdict: "FAIL"').replace("verdict: TBD", "verdict: FAIL")
        t = t.replace("- (what the test could not exercise)", "- the desktop host was not probed this run")
        rep.write_text(t, encoding="utf-8")
        code, info = check(v, rep)
        fs = " ".join(info["findings"])
        assert "HANDOFF" in fs and "BACKLOG" in fs, info
        # Add handoff + backlog anchor → clean.
        t = t.replace("None — PASS", "Skill: demo-skill. Goal: produce a thing. " + "Evidence: run-1/out.md vs run-2/out.md differ. " * 4 + "Change: make the section order deterministic because CRE reads verdict first. After: three runs agree.")
        rep.write_text(t, encoding="utf-8")
        with open(v / "_BACKLOG.md", "a", encoding="utf-8") as fh:
            fh.write("- [ ] **skill-test demo-skill — FAIL 2026-01-01.** x #p2 ^backlog-skilltest-demo-skill-2026-01-01\n")
        code, info = check(v, rep)
        assert code == 0, info
        # PASS with a handoff block → finding.
        t2 = t.replace("VERDICT: FAIL", "VERDICT: PASS").replace('verdict: "FAIL"', 'verdict: "PASS"').replace("verdict: FAIL", "verdict: PASS")
        rep.write_text(t2, encoding="utf-8")
        code, info = check(v, rep)
        assert code == 1 and any(f.startswith("HANDOFF") for f in info["findings"]), info
        # Re-scaffold refuses to overwrite.
        code, info, _ = scaffold(v, "demo-skill", "x", "2026-01-01")
        assert code == 1, info
    print("selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("scaffold")
    s.add_argument("--vault", required=True)
    s.add_argument("--skill", required=True)
    s.add_argument("--goal", required=True)
    s.add_argument("--date", default=_dt.date.today().isoformat())
    s.add_argument("--json", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("--vault", required=True)
    c.add_argument("--report", required=True)
    c.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if a.cmd == "scaffold":
        code, info, _ = scaffold(Path(a.vault), a.skill, a.goal, a.date)
    elif a.cmd == "check":
        code, info = check(Path(a.vault), Path(a.report))
    else:
        ap.print_help()
        return 2
    if getattr(a, "json", False):
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        for k, v in info.items():
            if isinstance(v, list):
                print(f"{k}:")
                for x in v:
                    print(f"  - {x}")
            else:
                print(f"{k}: {v}")
    return code


if __name__ == "__main__":
    sys.exit(main())
