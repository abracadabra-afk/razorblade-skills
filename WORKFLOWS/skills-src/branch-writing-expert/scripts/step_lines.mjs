// Arc steps onto chain lines (CRE, 2026-10-21): "place arc steps at line level, not just on the scene". For every arc step
// on a board, its plan cell (matched by its text, which is CRE's words in both places) names the board cards that carry it
// — `support` ("[id] …") in order, else `src` ("board cards a, b"). The first cited card that is a Beat, or a micro-beat
// under one, decides: the step goes on the scene chain line that Beat is linked to (the first cited beat when it spans
// several). Writes one ops file of `place-on-line` ops for board_tool.mjs; lists, never guesses, the steps it can't settle:
// a cell citing no board card (DEV / chapter cites — a placement for CRE's ruling list), a cited Beat linked to no line, a
// cited scene. Steps already on the right line are skipped. A cell citing cards in more than one scene is listed for a split
// into sub-steps (CRE 2026-10-21), never put on one line.
//   node step_lines.mjs <board.md> <plan.md> --out <ops.json> [--report <file.json>]
import { readFileSync, writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

for (const st of [process.stdout, process.stderr]) try { st.setDefaultEncoding("utf8"); } catch {}
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const WIN = process.platform === "win32";
const DEV = arg("--dev", WIN ? "C:/Users/Chad/dev/branch-writing" : `${process.env.HOME}/dev/branch-writing`);
const VAULT = arg("--vault", WIN ? "C:/Users/Chad/Dropbox/razorblade_mermaid" : `${process.env.HOME}/Dropbox/razorblade_mermaid`);
const fix = (p) => p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`).replace(/\\/g, "/");
const abs = (p) => (/^[A-Za-z]:|^\//.test(fix(p)) ? fix(p) : `${VAULT}/${p}`);
const bw = await import(pathToFileURL(`${DEV}/test/core.mjs`).href);
const [boardPath, planPath] = argv.filter((a, i) => !a.startsWith("--") && !(i > 0 && argv[i - 1].startsWith("--")));
const doc = bw.parse(readFileSync(abs(boardPath), "utf8"));
const s = bw.settingsOf(doc);
const beatKey = s.levels[s.levels.length - 2].key, prose = s.levels[s.levels.length - 1].key;
const planText = readFileSync(abs(planPath), "utf8");
const blocks = [...planText.matchAll(/```json\n([\s\S]*?)\n```/g)];
if (!blocks.length) { console.error("REFUSED: no JSON record in the plan"); process.exit(2); }
const plan = JSON.parse(blocks[blocks.length - 1][1]);
const cells = [...(plan.beats || []), ...(plan.spines || []).flatMap((sp) => sp.beats || [])];
const cited = (b) => {
  const ids = (b.support || []).map((x) => (/^\[(\w{6})\]/.exec(x) || [])[1]).filter(Boolean);
  if (ids.length) return ids;
  const m = /board cards? ([\w, ]+)/.exec(b.src || "");
  return m ? m[1].split(",").map((x) => x.trim()).filter((x) => /^\w{6}$/.test(x)) : [];
};
const byText = new Map(); for (const b of cells) if ((b.text || "").trim()) byText.set(b.text.trim(), b);
const title = (c) => (c.body || "").split("\n")[0].trim();
const ops = [], left = [];
const where = (c) => { const sc = c.parent && c.parent.meta.kind !== "project" ? c.parent : null; return sc ? title(sc) : "unplaced"; };
for (const st of doc.cards.filter((c) => c.meta.kind === "arcbeat" && c.body.trim())) {
  const cell = byText.get(st.body.trim());
  const tag = `B${st.meta.beat} ${st.meta.label || ""}`.trim();
  if (!cell) { left.push({ step: st.id, beat: tag, on: where(st), why: "no plan cell has this step's words" }); continue; }
  const ids = cited(cell);
  if (!ids.length) { left.push({ step: st.id, beat: tag, on: where(st), why: `cites no board card (${(cell.src || "").slice(0, 80)})` }); continue; }
  // A cell whose cited cards span more than one scene becomes sub-steps (split-step), not one line: listed, never placed here.
  const sceneOf = (k) => { for (let p = k; p; p = p.parent) if (p.meta.kind === s.levels[s.levels.length - 3].key) return p; return null; };
  const scenes = [...new Set(ids.map((id) => bw.findCard(doc, id)).filter(Boolean).map(sceneOf).filter(Boolean))];
  if (scenes.length > 1) { left.push({ step: st.id, beat: tag, on: where(st), why: `spans ${scenes.length} scenes (${scenes.map(title).join(" · ")}) — split it into sub-steps (split-step), one per scene in its own words, or put it on the ruling list` }); continue; }
  let pick = null, skipped = [];
  for (const id of ids) {
    let k = bw.findCard(doc, id);
    if (!k) { skipped.push(`[${id}] not on the board`); continue; }
    if (k.meta.kind === prose) k = k.parent;
    if (!k || k.meta.kind !== beatKey) { skipped.push(`[${id}] is a ${bw.findCard(doc, id).meta.kind}, not a Beat`); continue; }
    if (typeof k.meta.plotFrom !== "string") { skipped.push(`Beat "${title(k)}" [${id}] is on no line`); continue; }
    pick = { id, beat: k }; break;
  }
  if (!pick) { left.push({ step: st.id, beat: tag, on: where(st), why: skipped.join("; ") }); continue; }
  const [pid, run] = pick.beat.meta.plotFrom.split(":");
  const line = run.split("..")[0];
  if (st.parent && st.parent.id === pid && st.meta.plotLine === line) continue;
  ops.push({ op: "place-on-line", step: `^${st.id}`, via: `^${pick.id}`, why: `first cited: Beat "${title(pick.beat)}"${skipped.length ? ` (passed over: ${skipped.join("; ")})` : ""}` });
}
writeFileSync(fix(arg("--out")), JSON.stringify({ board: boardPath, label: arg("--label", "arc steps onto the chain lines of the beats that carry them"), ops }, null, 1));
if (arg("--report")) writeFileSync(fix(arg("--report")), JSON.stringify({ placed: ops.length, left }, null, 1));
console.log(`${ops.length} place-on-line ops → ${arg("--out")}; ${left.length} step(s) left as they are:`);
for (const l of left) console.log(`  ^${l.step} ${l.beat} (on ${l.on}): ${l.why}`);
