// The words proof (CRE, 2026-10-19: "the words themselves are the forbidden zone"). Every micro-beat's words on a board, in
// file order, with emphasis markers (* _) set aside and whitespace collapsed: one sha256 and a word count. Run it before and
// after any run that splits, regroups or moves micro-beats; the two lines must match.
//   node words.mjs <board.md> [--dev <plugin dev folder>]
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { pathToFileURL } from "node:url";

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const DEV = arg("--dev", process.platform === "win32" ? "C:/Users/Chad/dev/branch-writing" : `${process.env.HOME}/dev/branch-writing`);
const bw = await import(pathToFileURL(`${DEV}/test/core.mjs`).href);
const fix = (p) => p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`);
const doc = bw.parse(readFileSync(fix(argv[0]), "utf8"));
const prose = bw.settingsOf(doc).levels.at(-1).key;
const words = doc.cards.filter((c) => c.meta.kind === prose).map((c) => c.body.replace(/[*_]/g, "")).join(" ").replace(/\s+/g, " ").trim();
console.log(`${createHash("sha256").update(words, "utf8").digest("hex").slice(0, 16)} ${words ? words.split(" ").length : 0} words`);
