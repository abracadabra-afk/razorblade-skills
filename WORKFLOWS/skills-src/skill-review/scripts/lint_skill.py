#!/usr/bin/env python3
"""lint_skill.py — deterministic half of the skill-review skill.

Decides only what a script can decide exactly about ONE skill source dir
(WORKFLOWS/skills-src/<name>/): frontmatter shape, description limits,
size band, referenced paths, scripts, shell-candidate lines, gate phrases,
line overlap with sibling skills, consumers (callers), canon pairing,
invocation flags. Judgment (split/merge, what to script) stays with the
reasoning pass in SKILL.md. Never writes anything.

Usage:
  lint_skill.py --skills-src DIR --workflows DIR --skill NAME [--canon DOC] [--json] [--strict]
  lint_skill.py --selftest

Exit: 0 clean (INFO/WARN only) · 1 ERROR findings (or WARN with --strict)
      · 2 gate failure (bad path, unparseable frontmatter).
stdlib only (DIR-007).
"""
import argparse
import json
import os
import re
import sys
import tempfile

SEV_ORDER = {"ERROR": 0, "WARN": 1, "INFO": 2}
DESC_MAX = 1024
TOKENS_GREEN = 8000
TOKENS_WARN = 16000
OVERLAP_MIN_WORDS = 12

SHELL_PATTERNS = [
    (r"_DIRECTIVES\.md", "sentinel read"),
    (r"type:\s*ai-os-brain", "sentinel check"),
    (r"frontmatter|yaml\.safe_dump|YAML", "frontmatter / YAML write"),
    (r"\bwrite\b.*\b(files?|folder|dir)\b", "file scaffold"),
    (r"_CHANGELOG", "changelog entry"),
    (r"exit\s*`?[012]`?|exit code", "exit status"),
    (r"\bcensus\b|\bcount\b.*\b(segments?|lines?|items?)\b", "census / count"),
    (r"\bverify\b.*\bre-?read", "write verification"),
]
# matched against NORMALIZED lines (lowercased, underscores stripped)
BOILERPLATE_PATTERNS = [
    r"directives\.md",
    r"ai-os-brain",
    r"changelog",
    r"observations",
    r"dir-0[0-9][0-9]",
    r"file tools",
    r"sentinel",
]
GATE_PATTERNS = [
    r"\bhalt\b", r"\bask\b", r"CRE rules", r"\bgated?\b", r"never auto",
    r"stop and ask", r"await", r"one at a time",
]
TRIGGER_RE = re.compile(r"[\"“]([^\"”]{3,80})[\"”]")
REL_PATH_RE = re.compile(
    r"(?<![\w/])((?:scripts|templates|references|assets|evals)/[\w./\-]+)")
VERSION_RE = re.compile(r"\bv(\d+(?:\.\d+)*)\b")
LAST_UPDATED_RE = re.compile(r"^last_updated:\s*(\S+)", re.M)


class Findings:
    def __init__(self):
        self.items = []

    def add(self, sev, check, msg, where=None):
        self.items.append({"severity": sev, "check": check,
                           "message": msg, "where": where})

    def worst(self):
        if not self.items:
            return None
        return min(self.items, key=lambda f: SEV_ORDER[f["severity"]])["severity"]


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def parse_frontmatter(text):
    """Minimal YAML-ish frontmatter parser: top-level `key: value` with
    optional indented continuation lines. Returns (dict, body, error)."""
    if not text.startswith("---"):
        return None, text, "no opening --- fence"
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text, "no closing --- fence"
    fm, key = {}, None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] in " \t" and key:
            fm[key] = (fm[key] + " " + raw.strip()).strip()
            continue
        m = re.match(r"^([A-Za-z_][\w\-]*):\s*(.*)$", raw)
        if not m:
            return None, text, "unparseable line: %r" % raw[:60]
        key, val = m.group(1), m.group(2).strip()
        if val in (">", "|", ">-", "|-"):
            val = ""
        fm[key] = val
    body = "\n".join(lines[end + 1:])
    return fm, body, None


def normalize_line(line):
    line = re.sub(r"[`*_>#\[\]|]", " ", line)
    line = re.sub(r"\s+", " ", line).strip().lower()
    return line


def content_lines(body):
    out = []
    for i, ln in enumerate(body.split("\n"), start=1):
        n = normalize_line(ln)
        if len(n.split()) >= OVERLAP_MIN_WORDS:
            out.append((i, n, ln))
    return out


def is_boilerplate(line):
    return any(re.search(p, line) for p in BOILERPLATE_PATTERNS)


def lint(skills_src, workflows, name, f, canon_override=None):
    skill_dir = os.path.join(skills_src, name)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isdir(skill_dir):
        f.add("ERROR", "GATE", "skill dir not found: %s" % skill_dir)
        return None
    if not os.path.isfile(skill_md):
        f.add("ERROR", "GATE", "SKILL.md missing in %s" % skill_dir)
        return None
    text = read_text(skill_md)
    fm, body, err = parse_frontmatter(text)
    if err:
        f.add("ERROR", "GATE", "frontmatter: %s" % err, "SKILL.md")
        return None

    summary = {"skill": name}

    # FM-PARSE
    fm_name = fm.get("name", "")
    if fm_name != name:
        f.add("ERROR", "FM-PARSE",
              "frontmatter name %r != folder %r" % (fm_name, name), "SKILL.md:2")
    desc = fm.get("description", "")
    if not desc:
        f.add("ERROR", "FM-PARSE", "description missing", "SKILL.md")

    # DESC-*
    summary["desc_chars"] = len(desc)
    if len(desc) > DESC_MAX:
        f.add("ERROR", "DESC-LEN",
              "description %d chars > %d (pack fails)" % (len(desc), DESC_MAX))
    elif len(desc) > DESC_MAX - 100:
        f.add("WARN", "DESC-LEN",
              "description %d chars, within 100 of the %d cap" % (len(desc), DESC_MAX))
    if "<" in desc or ">" in desc:
        f.add("ERROR", "DESC-BRACKET", "angle bracket in description (pack fails)")
    triggers = TRIGGER_RE.findall(desc)
    summary["desc_triggers"] = len(triggers)
    if len(triggers) < 2:
        f.add("WARN", "DESC-TRIGGERS",
              "only %d quoted trigger phrase(s) in description" % len(triggers))
    if not re.search(r"do not use|don't use|not for", desc, re.I):
        f.add("WARN", "DESC-NEGATIVE", "description has no Do-NOT-use clause")

    # SIZE
    nbytes = len(text.encode("utf-8"))
    words = len(body.split())
    nlines = body.count("\n") + 1
    tokens = nbytes // 4
    band = "GREEN" if tokens <= TOKENS_GREEN else "WARN" if tokens <= TOKENS_WARN else "HEAVY"
    summary.update({"bytes": nbytes, "words": words, "lines": nlines,
                    "tokens_est": tokens, "size_band": band})
    f.add("INFO" if band == "GREEN" else "WARN", "SIZE",
          "%d bytes / %d words / %d lines ~%d tokens — %s" % (nbytes, words, nlines, tokens, band))

    # REF-PATHS
    refs = sorted(set(r.rstrip(".,;:") for r in REL_PATH_RE.findall(text)))
    missing = [r for r in refs if not os.path.exists(os.path.join(skill_dir, r))]
    summary["ref_paths"] = refs
    summary["ref_paths_missing"] = missing
    for r in missing:
        f.add("ERROR", "REF-PATHS", "referenced path does not exist in skill dir: %s (DIR-009)" % r)

    # SCRIPTS
    scripts_dir = os.path.join(skill_dir, "scripts")
    scripts = []
    if os.path.isdir(scripts_dir):
        for root, _, files in os.walk(scripts_dir):
            for fn in files:
                if fn.endswith((".py", ".ps1", ".sh")):
                    scripts.append(os.path.relpath(os.path.join(root, fn), skill_dir).replace("\\", "/"))
    summary["scripts"] = scripts
    dangling = [s for s in scripts if os.path.basename(s) not in text]
    for s in dangling:
        f.add("WARN", "SCRIPTS", "script shipped but never named in SKILL.md: %s" % s)
    f.add("INFO", "SCRIPTS", "%d script(s): %s" % (len(scripts), ", ".join(scripts) or "none"))

    # SHELL-CANDIDATES
    cands = []
    for i, ln in enumerate(body.split("\n"), start=1):
        for pat, label in SHELL_PATTERNS:
            if re.search(pat, ln, re.I):
                cands.append({"line": i, "kind": label, "text": ln.strip()[:120]})
                break
    summary["shell_candidates"] = cands
    if cands and not scripts:
        f.add("INFO", "SHELL-CANDIDATES",
              "%d mechanical-shell line(s) and no script — reasoning pass decides what clusters" % len(cands))
    else:
        f.add("INFO", "SHELL-CANDIDATES", "%d mechanical-shell line(s)" % len(cands))

    # GATES
    gates = 0
    for ln in body.split("\n"):
        if any(re.search(p, ln, re.I) for p in GATE_PATTERNS):
            gates += 1
    summary["gate_lines"] = gates
    f.add("INFO", "GATES", "%d line(s) carrying gate phrases" % gates)

    # OVERLAP
    own = content_lines(body)
    own_map = {n: (i, raw) for i, n, raw in own}
    overlap = {}
    boiler_total = 0
    for sib in sorted(os.listdir(skills_src)):
        if sib == name:
            continue
        sib_md = os.path.join(skills_src, sib, "SKILL.md")
        if not os.path.isfile(sib_md):
            continue
        sfm, sbody, serr = parse_frontmatter(read_text(sib_md))
        if serr:
            continue
        shared = [n for _, n, _ in content_lines(sbody) if n in own_map]
        if not shared:
            continue
        real = [n for n in shared if not is_boilerplate(n)]
        boiler = len(shared) - len(real)
        boiler_total += boiler
        if real:
            overlap[sib] = [{"line": own_map[n][0], "text": own_map[n][1].strip()[:120]} for n in real]
    summary["overlap"] = overlap
    summary["overlap_boilerplate_lines"] = boiler_total
    for sib, lines in overlap.items():
        f.add("WARN" if len(lines) >= 3 else "INFO", "OVERLAP",
              "%d non-boilerplate line(s) shared with %s (lines %s)"
              % (len(lines), sib, ", ".join(str(x["line"]) for x in lines[:8])))
    if not overlap:
        f.add("INFO", "OVERLAP", "no non-boilerplate line overlap with siblings (%d boilerplate)" % boiler_total)

    # CONSUMERS
    consumers = {}
    name_re = re.compile(r"(?<![\w-])%s(?![\w-])" % re.escape(name))
    scan = []
    if os.path.isdir(workflows):
        for fn in sorted(os.listdir(workflows)):
            if fn.endswith(".md"):
                scan.append(("WORKFLOWS/" + fn, os.path.join(workflows, fn)))
    for sib in sorted(os.listdir(skills_src)):
        if sib == name:
            continue
        p = os.path.join(skills_src, sib, "SKILL.md")
        if os.path.isfile(p):
            scan.append(("skills-src/%s/SKILL.md" % sib, p))
    for label, p in scan:
        if label.endswith("/%s.md" % name):
            continue
        hits = []
        for i, ln in enumerate(read_text(p).split("\n"), start=1):
            if name_re.search(ln):
                hits.append({"line": i, "text": ln.strip()[:160]})
        if hits:
            consumers[label] = hits
    summary["consumers"] = consumers
    f.add("INFO", "CONSUMERS", "%d file(s) name this skill: %s"
          % (len(consumers), ", ".join(sorted(consumers)) or "none"))

    # CANON-PAIR — WORKFLOWS/<name>.md, or --canon, or a doc that names skills-src/<name>
    canon = os.path.join(workflows, (canon_override or name) + ".md")
    canon_how = "override" if canon_override else "by name"
    if not os.path.isfile(canon) and os.path.isdir(workflows):
        needle = "skills-src/%s" % name
        cands = []
        for fn in sorted(os.listdir(workflows)):
            p = os.path.join(workflows, fn)
            if fn.endswith(".md") and os.path.isfile(p) and needle in read_text(p):
                cands.append(fn)
        if len(cands) == 1:
            canon, canon_how = os.path.join(workflows, cands[0]), "by skills-src reference (%s)" % cands[0]
        elif cands:
            f.add("WARN", "CANON-PAIR", "several docs reference skills-src/%s: %s — pass --canon" % (name, ", ".join(cands)))
    if os.path.isfile(canon):
        ctext = read_text(canon)
        m = LAST_UPDATED_RE.search(ctext)
        canon_updated = m.group(1) if m else None
        head = "\n".join(body.split("\n")[:12])
        vm = VERSION_RE.search(head)
        summary["canon"] = {"exists": True, "path": os.path.basename(canon), "found": canon_how,
                            "last_updated": canon_updated,
                            "skill_version_line": vm.group(0) if vm else None}
        f.add("INFO", "CANON-PAIR", "canon %s (%s; last_updated %s); skill head version %s — drift is skill-audit's call"
              % (os.path.basename(canon), canon_how, canon_updated, vm.group(0) if vm else "unstated"))
    else:
        summary["canon"] = {"exists": False}
        f.add("WARN", "CANON-PAIR", "no WORKFLOWS/%s.md canon doc" % name)

    # INVOKE-FLAGS
    flags = {k: fm[k] for k in ("user-invocable", "disable-model-invocation") if k in fm}
    summary["invoke_flags"] = flags
    f.add("INFO", "INVOKE-FLAGS", ("flags present: %s" % flags) if flags
          else "no invocation flags (Cowork support unverified — DIR-010)")

    return summary


def render(summary, f):
    out = []
    if summary:
        out.append("skill-review lint — %s" % summary["skill"])
        out.append("  size %s (~%d tokens) · desc %d chars · %d script(s) · %d consumer file(s)"
                   % (summary["size_band"], summary["tokens_est"], summary["desc_chars"],
                      len(summary["scripts"]), len(summary["consumers"])))
    for sev in ("ERROR", "WARN", "INFO"):
        rows = [x for x in f.items if x["severity"] == sev]
        if not rows:
            continue
        out.append("")
        out.append("%s (%d)" % (sev, len(rows)))
        for x in rows:
            loc = (" [%s]" % x["where"]) if x.get("where") else ""
            out.append("  %-16s %s%s" % (x["check"], x["message"], loc))
    if summary and summary.get("shell_candidates"):
        out.append("")
        out.append("SHELL-CANDIDATES (for the reasoning pass)")
        for c in summary["shell_candidates"][:40]:
            out.append("  L%-4d %-22s %s" % (c["line"], c["kind"], c["text"]))
    if summary and summary.get("consumers"):
        out.append("")
        out.append("CONSUMERS (contract surface)")
        for label, hits in summary["consumers"].items():
            out.append("  %s" % label)
            for h in hits[:6]:
                out.append("    L%-4d %s" % (h["line"], h["text"]))
    return "\n".join(out)


def selftest():
    """Two fixtures: one must-clear, one must-hit. Returns 0 on pass."""
    tmp = tempfile.mkdtemp(prefix="skillreview-")
    src = os.path.join(tmp, "skills-src")
    wf = os.path.join(tmp, "WORKFLOWS")
    os.makedirs(src)
    os.makedirs(wf)

    good = os.path.join(src, "good-skill")
    os.makedirs(os.path.join(good, "scripts"))
    with open(os.path.join(good, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write('---\nname: good-skill\ndescription: Do the thing. Use when CRE says "do the thing" or "run the thing". Do NOT use for other things.\n---\n'
                 "# good\n\nRun `scripts/do.py` first.\n\n"
                 "This is a long enough line of procedure that only exists here and nowhere else at all in the tree.\n")
    with open(os.path.join(good, "scripts", "do.py"), "w") as fh:
        fh.write("print(1)\n")
    with open(os.path.join(wf, "good-skill.md"), "w") as fh:
        fh.write("---\ntype: workflow\nlast_updated: 2026-01-01\n---\n# doc\n")
    with open(os.path.join(wf, "orchestrator.md"), "w") as fh:
        fh.write("Leg 1 calls good-skill and reads status: floor-revised from it.\n")

    bad = os.path.join(src, "bad-skill")
    os.makedirs(bad)
    with open(os.path.join(bad, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("---\nname: wrong-name\ndescription: %s <tag>\n---\n# bad\n\nSee scripts/missing.py.\n"
                 "This is a long enough line of procedure that only exists here and nowhere else at all in the tree.\n"
                 % ("x" * 1030))

    failures = []
    f1 = Findings()
    s1 = lint(src, wf, "good-skill", f1)
    checks1 = {(x["check"], x["severity"]) for x in f1.items}
    if f1.worst() not in ("INFO", "WARN"):
        failures.append("good-skill should have no ERROR: %s" % [x for x in f1.items if x["severity"] == "ERROR"])
    if "WORKFLOWS/orchestrator.md" not in s1["consumers"]:
        failures.append("good-skill: consumer orchestrator.md not detected")
    if "scripts/do.py" not in s1["ref_paths"]:
        failures.append("good-skill: ref path scripts/do.py not detected")
    if "bad-skill" not in s1["overlap"]:
        failures.append("good-skill: overlap with bad-skill not detected")
    if not s1["canon"]["exists"]:
        failures.append("good-skill: canon doc not detected")

    f2 = Findings()
    lint(src, wf, "bad-skill", f2)
    checks2 = {(x["check"], x["severity"]) for x in f2.items}
    for want in [("FM-PARSE", "ERROR"), ("DESC-LEN", "ERROR"), ("DESC-BRACKET", "ERROR"),
                 ("REF-PATHS", "ERROR"), ("CANON-PAIR", "WARN")]:
        if want not in checks2:
            failures.append("bad-skill: expected %s" % (want,))

    f3 = Findings()
    if lint(src, wf, "nope", f3) is not None or f3.worst() != "ERROR":
        failures.append("missing skill should gate-fail")

    _ = checks1
    if failures:
        print("SELFTEST FAIL")
        for x in failures:
            print("  - " + x)
        return 1
    print("SELFTEST PASS (fixtures in %s)" % tmp)
    return 0


def main():
    # Windows consoles default to cp1252; the vault is full of arrows and dashes.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skills-src", help="path to WORKFLOWS/skills-src")
    ap.add_argument("--workflows", help="path to WORKFLOWS")
    ap.add_argument("--skill", help="skill folder name to lint")
    ap.add_argument("--canon", help="canon doc basename in WORKFLOWS when it differs from the skill name (e.g. transcoder)")
    ap.add_argument("--json", action="store_true", help="machine output")
    ap.add_argument("--strict", action="store_true", help="exit 1 on WARN too")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(selftest())
    if not (a.skills_src and a.workflows and a.skill):
        ap.error("--skills-src, --workflows and --skill are required (or --selftest)")

    f = Findings()
    summary = lint(a.skills_src, a.workflows, a.skill, f, canon_override=a.canon)
    if a.json:
        print(json.dumps({"summary": summary, "findings": f.items}, indent=2, ensure_ascii=False))
    else:
        print(render(summary, f))

    if summary is None:
        sys.exit(2)
    worst = f.worst()
    if worst == "ERROR" or (a.strict and worst == "WARN"):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
