#!/usr/bin/env python3
"""storyline-sync deterministic file writer (backlog ^storyline-serializer-rebundle; DIR-004).

Emit a StoryLine scene or Codex .md file with its frontmatter serialized by
yaml.safe_dump — NEVER hand-formatted. safe_dump auto-escapes every value that has
bitten this lane (^obs-025 / ^obs-028 / ^obs-029, recurred on CH2/CH4/CH5): wikilinks
that contain apostrophes (``[[Baby Bird's Box]]``), scalars that start with ``"`` or
contain ``: ``, and lists of ``[[wikilinks]]``. The write is GATED on a real
yaml.safe_load of the file it just produced — a file that "looks right" is not done
until a loader accepts it AND the values round-trip (the Step-6 self-test discipline;
^obs-014: parse a fresh handle, never a stale mount).

The body (manuscript prose regenerated from draft.md) is written VERBATIM — this writer
never reflows prose; it only owns the frontmatter serialization + the parse-gate.

Write a file:
  write_storyline.py --out PATH --frontmatter @fm.json [--body @body.md | --body-stdin]
    --frontmatter  JSON object (literal string, or @file). Emitted as YAML frontmatter.
    --body         body text (literal, or @file). Default: empty.
    --body-stdin   read the body from stdin (use for large prose).

Verify only (the Step-6 self-test — parse a fresh handle, not the bash mount):
  write_storyline.py --verify PATH [PATH ...]
    Parse each file's frontmatter via yaml.safe_load; exit 0 if all parse, 1 if any fail.

Exit: 0 ok · 1 the YAML parse-gate / verify failed · 2 usage/IO error
"""
import argparse, json, os, sys

try:
    import yaml
except ImportError:
    print("pyyaml required: pip install pyyaml --break-system-packages", file=sys.stderr)
    sys.exit(2)

DUMP = dict(default_flow_style=False, sort_keys=False, allow_unicode=True, width=100000)


def parse_frontmatter(text):
    """Return the parsed YAML frontmatter dict, or raise on malformed YAML."""
    if not text.startswith("---"):
        raise ValueError("no leading frontmatter block")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("no closing --- for frontmatter")
    return yaml.safe_load(text[3:end].strip("\n"))


def read_arg(val):
    """A literal string, or @path to read the value from a file."""
    if val is None:
        return None
    if val.startswith("@"):
        with open(val[1:], encoding="utf-8") as f:
            return f.read()
    return val


def cmd_verify(paths):
    bad = []
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                parse_frontmatter(f.read())
        except Exception as e:
            bad.append(f"{p}: {e}")
    if bad:
        for b in bad:
            print("PARSE-FAIL " + b, file=sys.stderr)
        return 1
    print(f"OK: {len(paths)} file(s) frontmatter parse")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--frontmatter")
    ap.add_argument("--body")
    ap.add_argument("--body-stdin", action="store_true")
    ap.add_argument("--verify", nargs="+")
    a = ap.parse_args()

    if a.verify:
        sys.exit(cmd_verify(a.verify))

    if not a.out or not a.frontmatter:
        print("ERROR: --out and --frontmatter are required to write", file=sys.stderr)
        sys.exit(2)

    try:
        fm = json.loads(read_arg(a.frontmatter))
    except Exception as e:
        print(f"ERROR: --frontmatter is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(fm, dict):
        print("ERROR: --frontmatter must be a JSON object", file=sys.stderr)
        sys.exit(2)

    if a.body_stdin:
        body = sys.stdin.read()
    else:
        body = read_arg(a.body) or ""

    block = yaml.safe_dump(fm, **DUMP)
    text = f"---\n{block}---\n\n{body}"
    if not text.endswith("\n"):
        text += "\n"

    out_abs = os.path.abspath(a.out)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    with open(out_abs, "w", encoding="utf-8") as f:
        f.write(text)

    # parse-gate: re-read what we just wrote; a loader must accept it AND values round-trip
    try:
        with open(out_abs, encoding="utf-8") as f:
            reparsed = parse_frontmatter(f.read())
    except Exception as e:
        print(f"PARSE-GATE FAILED for {a.out}: {e}", file=sys.stderr)
        sys.exit(1)
    if reparsed != fm:
        print(f"PARSE-GATE FAILED for {a.out}: frontmatter did not round-trip", file=sys.stderr)
        sys.exit(1)

    print(f"WROTE {a.out} ({len(fm)} frontmatter keys, body {len(body)} chars) — parse-gate OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
