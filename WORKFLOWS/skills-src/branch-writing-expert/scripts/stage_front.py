"""Stage the beats: the brief's frontmatter, serialized and parse-gated (DIR-004), from stage_scene.mjs's facts.json.

    python stage_front.py <facts.json> <brief.md>

Rewrites only the brief's frontmatter block (adds one if it has none); the body is left byte-identical. The written file
is read back and its frontmatter parsed; the fingerprint must survive the round trip or the script exits 1.
"""
import json
import re
import sys

import yaml


def main(facts_path, brief_path):
    f = json.load(open(facts_path, encoding="utf-8"))
    s = f["scene"]
    text = open(brief_path, encoding="utf-8").read()
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end < 0:
            sys.exit("REFUSED: the brief's frontmatter has no closing ---")
        body = text[end + 5:]
    # Sources = what the brief cites: the board, the DEV note, the threads its body names, the trace reports it names.
    src = ["board"]
    if f["sources"].get("devNote"):
        src.append(f["sources"]["devNote"])
    threads = sorted(set(re.findall(r"\bT\d{2}\b", body)))
    if threads:
        src.append("WRITING/PROJECTS/WITCHWOOD/REFERENCE/threads.md (" + ", ".join(threads) + ")")
    src += [t["file"] for t in f["sources"].get("traces", []) if t["file"].rsplit("/", 1)[-1].removesuffix(".md") in body]
    front = {
        "type": "beat-brief",
        "board": re.sub(r"^.*?/razorblade_mermaid/", "", f["board"]),  # vault-relative where it can be
        "scene": "^" + s["id"],
        "chapter": s["chapter"],
        "title": s["chapterTitle"] or s["title"],
        "built": f["built"],
        "fingerprint": f["fingerprint"]["hash"],
        "fingerprint_parts": json.dumps(f["fingerprint"]["parts"], separators=(",", ":")),
        "mode": 'branch-writing-expert, "stage the beats"',
        "sources": src,
    }
    out = "---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000) + "---\n" + body
    open(brief_path, "w", encoding="utf-8", newline="\n").write(out)
    back = open(brief_path, encoding="utf-8").read()
    got = yaml.safe_load(back.split("\n---\n", 1)[0][4:])
    if got.get("fingerprint") != front["fingerprint"] or json.loads(got["fingerprint_parts"]) != f["fingerprint"]["parts"]:
        sys.exit("PARSE GATE FAILED: the fingerprint did not survive the round trip")
    print(f"frontmatter ok · fp {front['fingerprint']} · {brief_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
