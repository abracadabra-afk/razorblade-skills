#!/usr/bin/env python3
"""dev-capture scaffolder self-test — exercises every gate + profile map, and proves the
hand-laid Witchwood DEV/ tree matches what scaffold_dev.py would generate.

Teed up 2026-06-21 because the sandbox never finished cold-booting during the steps-1-3 build
(^obs-109), so scaffold_dev.py was hand-executed via the file tools for the Witchwood run and its
gates were never actually fired. Run this once the sandbox is healthy:

    python3 WORKFLOWS/skills-src/dev-capture/scripts/selftest.py

Fully isolated + self-cleaning: all scaffolding happens in a dot-prefixed temp tree under the vault
(Obsidian-ignored) and in /tmp; both are removed in a finally block. The real Witchwood DEV/ is only
READ (for the parity diff), never written. Exit 0 = all pass; non-zero = at least one failure.
"""
import re, shutil, subprocess, sys, tempfile, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCAFFOLD = HERE / "scaffold_dev.py"

# Locate the vault root by walking up for _DIRECTIVES.md (same rule the scaffolder uses).
VAULT = None
for p in [HERE, *HERE.parents]:
    if (p / "_DIRECTIVES.md").is_file():
        head = (p / "_DIRECTIVES.md").read_text(encoding="utf-8")[:400]
        if "type: ai-os-brain" in head and "file: directives" in head:
            VAULT = p
            break
if VAULT is None:
    print("FAIL: could not locate the vault root (no _DIRECTIVES.md with the right frontmatter above this script).")
    sys.exit(3)

WITCHWOOD = VAULT / "WRITING" / "PROJECTS" / "WITCHWOOD"
SANDBOX = VAULT / ".devcap_selftest"          # under the vault → sentinel passes; dot-prefixed → Obsidian ignores
TODAY = datetime.date.today().isoformat()

results = []  # (name, ok, detail)


def run(project, *args):
    cmd = [sys.executable, str(SCAFFOLD), "--project", str(project), *args]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))


def expected_files(profile):
    common = {
        "_DEV.md", "_DEV_MAP.md", "_POETICS.md",
        "scenes/README.md", "registry/README.md",
        "registry/characters/README.md", "registry/locations/README.md",
        "registry/lore/README.md", "registry/items.md",
        "_intake/README.md", "_intake/_LEDGER.md", "_intake/_audit/README.md",
    }
    if profile == "novel":
        return common | {"project.md", "sequences/README.md"}
    if profile == "novella":
        return common | {"movements/README.md"}
    return common  # short


def make_project(name):
    """A minimal real-looking project under the vault: has REFERENCE/ so the project gate passes."""
    proj = SANDBOX / name
    (proj / "REFERENCE").mkdir(parents=True, exist_ok=True)
    return proj


def main():
    if not SCAFFOLD.is_file():
        print(f"FAIL: scaffold_dev.py not found at {SCAFFOLD}")
        sys.exit(3)
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)

    try:
        # --- Gate 1: project gate (no CHAPTERS/ or REFERENCE/) ---
        bare = SANDBOX / "bare"
        bare.mkdir(parents=True)
        code, out = run(bare)
        check("project-gate (no CHAPTERS/REFERENCE → GATE)",
              code == 2 and "neither CHAPTERS" in out, f"code={code}")

        # --- Gate 2: vault sentinel (project OUTSIDE the vault) ---
        ext = Path(tempfile.mkdtemp(prefix="devcap_nosentinel_"))
        (ext / "REFERENCE").mkdir()
        code, out = run(ext)
        check("vault-sentinel (outside vault → GATE)",
              code == 2 and "sentinel failed" in out, f"code={code}")
        shutil.rmtree(ext, ignore_errors=True)

        # --- Gate 3 + profile maps: happy path for each profile ---
        for profile in ("short", "novella", "novel"):
            proj = make_project(f"proj_{profile}")
            code, out = run(proj, "--profile", profile)
            dev = proj / "DEV"
            got = {str(p.relative_to(dev)).replace("\\", "/")
                   for p in dev.rglob("*") if p.is_file()} if dev.is_dir() else set()
            want = expected_files(profile)
            ok = code == 0 and got == want
            check(f"scaffold --profile {profile} (file set)", ok,
                  f"code={code} missing={want-got} extra={got-want}")
            # placeholder refusal: no unsubstituted tokens survived
            leftover = [str(p.relative_to(dev)) for p in dev.rglob("*")
                        if p.is_file() and re.search(r"\{\{(PROJECT|DATE|PROFILE)\}\}", p.read_text(encoding="utf-8"))]
            check(f"placeholder-substitution --profile {profile}", not leftover,
                  f"unsubstituted in {leftover}")

        # --- Gate 4: never-overwrite (DEV/ already exists) ---
        proj_novel = SANDBOX / "proj_novel"   # already scaffolded above
        code, out = run(proj_novel, "--profile", "novel", "--dry-run")
        check("never-overwrite (existing DEV/ → GATE, even on --dry-run)",
              code == 2 and "already exists" in out, f"code={code}")

        # --- Parity: a fresh WITCHWOOD-named novel scaffold == the hand-laid Witchwood DEV/ ---
        # (normalize only the last_updated date, which legitimately varies by run-day)
        if WITCHWOOD.is_dir():
            mirror = make_project("WITCHWOOD")
            code, out = run(mirror, "--profile", "novel")
            mdev, rdev = mirror / "DEV", WITCHWOOD / "DEV"
            diffs = []
            for rel in sorted(expected_files("novel")):
                m, r = mdev / rel, rdev / rel
                if not r.is_file():
                    diffs.append(f"{rel} (missing in Witchwood)"); continue
                norm = lambda s: re.sub(r"last_updated: \d{4}-\d{2}-\d{2}", "last_updated: DATE", s)
                if norm(m.read_text(encoding="utf-8")) != norm(r.read_text(encoding="utf-8")):
                    diffs.append(rel)
            check("parity: scaffolder output == hand-laid Witchwood DEV/ (date-normalized)",
                  code == 0 and not diffs, f"differs: {diffs}")
        else:
            check("parity vs Witchwood DEV/", False, "WITCHWOOD project not found")

    finally:
        shutil.rmtree(SANDBOX, ignore_errors=True)

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"\ndev-capture self-test: {passed}/{total} passed.")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
