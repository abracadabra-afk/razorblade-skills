// Breakdown, step 1: a split spec → `split-micro` ops. The spec names, per micro-beat card, its pieces in order as
// [type, the piece's opening words]; each piece runs to the next one's opening words (or the end). The pieces are his words
// exactly — this script only finds where they start; board_tool refuses any piece that isn't his next words.
//   node split_plan.mjs <board.md> <splits.json> --out <ops.json> [--board-ref <path the ops file names>] [--label "<words>"]
//   splits.json: { "<card id>": [["sensory/setting", "Snow fell"], ["action", "Cried and cried"], …], … }
import { readFileSync, writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const DEV = arg("--dev", process.platform === "win32" ? "C:/Users/Chad/dev/branch-writing" : `${process.env.HOME}/dev/branch-writing`);
const bw = await import(pathToFileURL(`${DEV}/test/core.mjs`).href);
const fix = (p) => p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`);
const doc = bw.parse(readFileSync(fix(argv[0]), "utf8"));
const spec = JSON.parse(readFileSync(fix(argv[1]), "utf8"));
const ops = [], bad = [];
for (const [id, parts] of Object.entries(spec)) {
  const c = bw.findCard(doc, id);
  if (!c) { bad.push(`no card ^${id}`); continue; }
  // A paragraph wrapped whole in *…* / _…_ is split inside its markers (board_tool re-wraps each piece).
  const m = /^(\s*)([*_])(?!\2)([\s\S]*?[^\s*_])\2(\s*)$/.exec(c.body);
  const inner = m ? m[3] : c.body;
  const starts = [];
  let at = 0;
  for (const [, w] of parts) {
    const j = inner.indexOf(w, at);
    if (j < 0) { bad.push(`^${id}: "${w}" not found after character ${at}`); break; }
    starts.push(j);
    at = j + 1;
  }
  if (starts.length !== parts.length) continue;
  if (inner.slice(0, starts[0]).trim()) { bad.push(`^${id}: words before the first piece`); continue; }
  const pieces = parts.map(([type], i) => ({ type, text: inner.slice(starts[i], i + 1 < starts.length ? starts[i + 1] : inner.length).trim() }));
  // A piece marked dialogue that doesn't open with a quotation mark (a stray closing quote, an italic quote) is left untyped:
  // the export would wrap it in quote marks. Said in one line.
  for (const pc of pieces) if (pc.type === "dialogue" && !/^\s*["“«]/.test(pc.text)) { console.log(`  left untyped: a piece of ^${id} ("${pc.text.slice(0, 30)}…")`); pc.type = ""; }
  ops.push({ op: "split-micro", card: `^${id}`, pieces });
}
if (bad.length) { console.error("REFUSED:\n  " + bad.join("\n  ")); process.exit(2); }
writeFileSync(fix(arg("--out")), JSON.stringify({ board: arg("--board-ref", argv[0]), label: arg("--label", "split micro-beats one per beat"), ops }, null, 1));
console.log(`${ops.length} split ops → ${arg("--out")}`);
