// The administrative pass's plan → one ops file (CRE-ruled 2026-10-19: the levels above the micro-beats are administrative).
// A plan names, per chapter Sequence, its summary, goal holder and chain; per Scene its title, summary, goal holder, chain and
// its Beats (each a run of the scene's micro-beats, in order, with a type, title and summary); and a type for each untyped
// micro-beat. The micro-beats' words and their existing types are never touched; a "dialogue" type is never given to a card
// that doesn't open with a quotation mark (the export would add quote marks to it). Scenes with `linkBeats` get one chain line
// per beat and each beat linked to its line; `sequence.links` links scenes to runs of the chapter's lines.
//   node admin_plan.mjs <plan.json> --board <board.md> --out <ops.json> [--label "<words>"]
import { readFileSync, writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const WIN = process.platform === "win32";
const DEV = arg("--dev", WIN ? "C:/Users/Chad/dev/branch-writing" : `${process.env.HOME}/dev/branch-writing`);
const bw = await import(pathToFileURL(`${DEV}/test/core.mjs`).href);
const fix = (p) => p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`);
const plan = JSON.parse(readFileSync(fix(argv[0]), "utf8"));
const boardPath = fix(arg("--board"));
const doc = bw.parse(readFileSync(boardPath, "utf8"));
const s = bw.settingsOf(doc);
const problems = [];
const ops = [];
const micro = s.levels[s.levels.length - 1].key;
const btypes = s.beatTypes || [];

// A card may be named "<id>#<k>": the k-th piece (0-based) of a micro-beat split earlier in the same breakdown — the pieces
// sit right after the original card, in order (split-micro), so a plan can be written before the split's new ids exist.
const pieceOf = (ref) => {
  const m = /^\^?([A-Za-z0-9-]+)#(\d+)$/.exec(String(ref));
  if (!m) return String(ref).replace(/^\^/, "");
  const c = bw.findCard(doc, m[1]);
  if (!c || !c.parent) return `?${ref}`;
  const sib = c.parent.children, i = sib.indexOf(c) + Number(m[2]);
  return sib[i] ? sib[i].id : `?${ref}`;
};
for (const sc of plan.scenes || []) {
  for (const b of sc.beats || []) b.cards = b.cards.map(pieceOf);
  if (sc.micro) sc.micro = Object.fromEntries(Object.entries(sc.micro).map(([k, v]) => [pieceOf(k), v]));
}
const seq = plan.sequence ? bw.findCard(doc, plan.sequence.id) : null;
const links = [];
for (const sc of plan.scenes) {
  const card = bw.findCard(doc, sc.id);
  if (!card) { problems.push(`no scene ^${sc.id}`); continue; }
  if (seq && card.parent !== seq) problems.push(`^${sc.id} is not under ^${plan.sequence.id}`);
  const prose = card.children.flatMap((k) => (k.meta.kind === micro ? [k] : k.children.filter((x) => x.meta.kind === micro)));
  const flat = sc.beats.flatMap((b) => b.cards);
  const ids = prose.map((k) => k.id);
  if (flat.length !== ids.length || flat.some((id, i) => id !== ids[i])) {
    const missing = ids.filter((id) => !flat.includes(id)), extra = flat.filter((id) => !ids.includes(id));
    problems.push(`^${sc.id}: beats must cover its ${ids.length} micro-beats once each in order (plan has ${flat.length}; missing ${missing.join(",") || "-"}; extra ${extra.join(",") || "-"})`);
  }
  // CRE 2026-10-16 / 2026-10-23: a Beat's position (setup … outcome) is read live from the scene line it is linked to, and
  // climax / valley / hook are his marks on that line — so a Beat is never given a position type. Any other type a plan
  // names (one of his own) still goes through.
  const POS = ["setup/hook", "escalation", "scene-climax", "valley", "outcome/hook", "setup", "outcome", "climax", "hook"];
  for (const b of sc.beats) if (b.type && POS.includes(String(b.type).toLowerCase())) console.log(`  not typed: Beat "${b.title || ""}" (${b.type} is read from its scene line, never stored)`);
  ops.push({ op: "regroup-beats", scene: `^${sc.id}`, groups: sc.beats.map((b) => ({ cards: b.cards.map((x) => `^${x}`), type: b.type && !POS.includes(String(b.type).toLowerCase()) ? b.type : undefined, title: b.title, summary: b.summary })) });
  for (const [id, type] of Object.entries(sc.micro || {})) {
    const m = bw.findCard(doc, id);
    if (!m || m.meta.kind !== micro) { problems.push(`no micro-beat ^${id}`); continue; }
    if (m.meta.type) continue; // a type already there stays (his, or ruled earlier)
    if (!btypes.includes(type)) { problems.push(`^${id}: "${type}" is not in the board's beat types`); continue; }
    // A card that doesn't open with a quotation mark (an italic *“…”* memory, a stray closing quote) is left untyped rather
    // than typed dialogue: the export would wrap it in quote marks. Said in one line, never an error.
    if (type === "dialogue" && !/^\s*["“«]/.test(m.body)) { console.log(`  left untyped: ^${id} (dialogue, but it doesn't open with a quotation mark)`); continue; }
    ops.push({ op: "set-type", card: `^${id}`, type });
  }
  if (sc.title) ops.push({ op: "set-title", card: `^${sc.id}`, text: sc.title });
  if (sc.summary) ops.push({ op: "set-summary", card: `^${sc.id}`, text: sc.summary });
  if (sc.goalHolder) ops.push({ op: "set-field", card: `^${sc.id}`, field: "goal holder", value: sc.goalHolder });
  if (sc.chain) ops.push({ op: "set-chain", card: `^${sc.id}`, ...sc.chain });
  // One scene chain line per beat, each beat linked to its line (breakdown.md): the chain must have as many lines as beats.
  if (sc.linkBeats) {
    const n = sc.chain ? 2 + (sc.chain.turns || []).length : 0;
    if (n !== sc.beats.length) problems.push(`^${sc.id}: linkBeats needs one chain line per beat (${n} lines, ${sc.beats.length} beats)`);
    else sc.beats.forEach((b, i) => links.push({ op: "link-from", card: `beat:^${sc.id}:${i}`, parent: `^${sc.id}`, lines: i }));
  }
}
if (plan.sequence) {
  const q = plan.sequence;
  if (!seq) problems.push(`no sequence ^${q.id}`);
  if (q.summary) ops.push({ op: "set-summary", card: `^${q.id}`, text: q.summary });
  if (q.goalHolder) ops.push({ op: "set-field", card: `^${q.id}`, field: "goal holder", value: q.goalHolder });
  if (q.chain) ops.push({ op: "set-chain", card: `^${q.id}`, ...q.chain });
  // A scene linked to the run of the chapter's chain lines it carries; a flashback interlude usually stands beside the chain.
  for (const l of q.links || []) links.push({ op: "link-from", card: `^${l.scene}`, parent: `^${q.id}`, lines: l.lines });
}
ops.push(...links);
if (problems.length) { console.error("REFUSED — the plan doesn't fit the board:\n  " + problems.join("\n  ")); process.exit(2); }
writeFileSync(fix(arg("--out")), JSON.stringify({ board: arg("--board-ref", boardPath), label: arg("--label", "administrative pass"), ops }, null, 1));
console.log(`${ops.length} ops → ${arg("--out")}`);
