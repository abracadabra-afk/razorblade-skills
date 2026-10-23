// Subplots onto a board (CRE, 2026-10-21: "the subplot beats would hit the scenes and lines like the others, so each unit
// holds the entirety of narrative needs - plus they are linked to larger arcs"). Reads a plan's `subplots` (plan_tool.py) and
// writes one ops file for board_tool.mjs: the plot arc (no model role — only the external spine carries one), then its
// steps in story order by today's rules — a step whose `cards` name a board card goes on the line of the Beat that carries
// it (its text must be words on that card); `parts` make sub-steps, one per scene; a step with a `from` source has its text
// re-checked word for word there by the tool; anything else waits unplaced with its reason, and a `ruling` step is listed for
// CRE, never placed. Prints the ruling list.
//   node subplot_build.mjs <plan.md> <board.md> --key <subplot key> --out <ops.json>
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
const [planPath, boardPath] = argv.filter((a, i) => !a.startsWith("--") && !(i > 0 && argv[i - 1].startsWith("--")));
const blocks = [...readFileSync(abs(planPath), "utf8").matchAll(/```json\r?\n([\s\S]*?)\r?\n```/g)];
const plan = JSON.parse(blocks[blocks.length - 1][1]);
const sp = (plan.subplots || []).find((x) => x.key === arg("--key"));
if (!sp) { console.error(`REFUSED: no subplot "${arg("--key")}" in the plan`); process.exit(2); }
if (sp.model || sp.role) { console.error("REFUSED: a subplot carries no model role"); process.exit(2); }
const doc = bw.parse(readFileSync(abs(boardPath), "utf8"));
const problems = [], rulings = [], ops = [];
ops.push({ op: "add-plot-arc", label: sp.label, ...(sp.goal_holder ? { goalHolder: sp.goal_holder } : {}), fields: Object.fromEntries(["goal", "stakes", "planned_outcome"].filter((k) => sp[k]).map((k) => [k, sp[k]])) });
const norm = (s) => String(s).replace(/[’‘]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, " ");
(sp.steps || []).forEach((st, i) => {
  const base = { op: "add-plot-step", arc: sp.label, label: st.label || "" };
  const n = `${i + 1}. ${st.label || ""}`;
  // his words prove the step: `quote` when the step's text is a plain administrative line (CRE 2026-10-22), else the text itself
  const words = st.quote || st.text;
  if (st.ruling) { rulings.push(`${n} — "${st.text}" — ${st.ruling}`); ops.push({ ...base, ...(st.from ? { from: { source: st.from, quote: words }, ...(st.quote ? { text: st.text } : {}) } : { text: st.text }), unplaced: `for CRE's ruling: ${st.ruling}` }); return; }
  // placed on his ruling where its words aren't on a board card (a DEV ruling's words): `via` names the Beat
  if (st.via) { ops.push({ ...base, ...(st.from ? { from: { source: st.from, quote: words }, ...(st.quote ? { text: st.text } : {}) } : { text: st.text }), via: st.via }); return; }
  if (st.parts && st.parts.length) { ops.push({ ...base, text: st.text, parts: st.parts.map((p) => ({ text: p.text, via: p.via || `^${p.card}` })) }); return; }
  if (st.cards && st.cards.length) {
    const c = bw.findCard(doc, st.cards[0]);
    if (!c) { problems.push(`${n}: card ^${st.cards[0]} is not on the board`); return; }
    // a name he has ruled renamed (e.g. Shadow → Thistle, 2026-10-21) where the card hasn't caught up: checked against the card with the rename applied
    const body = (st.renamed || []).reduce((b, r) => b.split(r.from).join(r.to), c.body);
    if (!norm(body).includes(norm(words))) problems.push(`${n}: its words are not on card ^${st.cards[0]}`);
    ops.push({ ...base, text: st.text, via: `^${st.cards[0]}` });
    return;
  }
  const op = { ...base, unplaced: st.unplaced || "no board card yet" };
  if (st.from) { op.from = { source: st.from, quote: words }; if (st.quote) op.text = st.text; } else op.text = st.text;
  ops.push(op);
});
if (problems.length) { console.error("REFUSED:\n  " + problems.join("\n  ")); process.exit(2); }
writeFileSync(fix(arg("--out")), JSON.stringify({ board: boardPath, label: `subplot "${sp.label}" (${sp.status || "pilot"}): its plot arc and ${sp.steps.length} steps by today's rules`, ops }, null, 1));
console.log(`${ops.length} ops → ${arg("--out")}`);
if (rulings.length) { console.log(`RULING LIST (${rulings.length}, not placed):`); for (const r of rulings) console.log("  " + r); }
