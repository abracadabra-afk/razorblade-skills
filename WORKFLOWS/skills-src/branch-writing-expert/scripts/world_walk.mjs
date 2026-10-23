// The world walk (CRE, 2026-10-22: does anything "walk the board, assign or create eras for scenes, fill in items for
// tracking, build systems?"). READ-ONLY: it never writes the board, DEV, REFERENCE or the plan — only its work folder. For
// one stage at a time it lays out the candidates and the evidence each proposal rests on, from his three sources (the
// board's own words, the project's DEV registry, REFERENCE/threads.md), so the ruling list (references/world-walk.md) is
// written from facts, not from a memory of the board. Run it again after each stage lands: every stage reads the board as
// it is now (later stages find what earlier ones made).
//
//   node world_walk.mjs <board.md> --out <work folder> --stage <registry|links|eras|seeds|events|profiles|ideas|all>
//        [--project <WRITING/PROJECTS/X>]  (default: the project whose name the board's title or file name carries)
//        [--threads <threads.md>]          (default: <project>/REFERENCE/threads.md)
//
// Each stage writes <stage>.json (the candidates, for building ops) and <stage>.md (the same, readable, in story order),
// and README.md lists what the walk did not check (DIR-018). Matching is case-insensitive on word boundaries, with a
// leading "the" optional, over his words only: micro-beats and idea cards (never summaries, titles or chain lines, which
// this skill wrote). Console output is UTF-8 (DIR-020).
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { basename } from "node:path";

for (const st of [process.stdout, process.stderr]) try { st.setDefaultEncoding("utf8"); } catch {}
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const WIN = process.platform === "win32";
const DEV = arg("--dev", WIN ? "C:/Users/Chad/dev/branch-writing" : `${process.env.HOME}/dev/branch-writing`);
const VAULT = arg("--vault", WIN ? "C:/Users/Chad/Dropbox/razorblade_mermaid" : `${process.env.HOME}/Dropbox/razorblade_mermaid`);
const fix = (p) => p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`).replace(/\\/g, "/");
// A path is absolute, else relative to the current folder when it exists there, else relative to the vault.
const abs = (p) => (/^[A-Za-z]:|^\//.test(fix(p)) ? fix(p) : existsSync(p) ? fix(process.cwd() + "/" + p) : `${VAULT}/${p}`);
const relv = (p) => (abs(p).startsWith(VAULT + "/") ? abs(p).slice(VAULT.length + 1) : abs(p));
const die = (m) => { console.error("REFUSED: " + m); process.exit(2); };
const [boardPath] = argv.filter((a, i) => !a.startsWith("--") && !(i > 0 && argv[i - 1].startsWith("--")));
const OUT = arg("--out") ? fix(arg("--out")) : null;
const STAGE = arg("--stage", "all");
const STAGES = ["registry", "links", "eras", "seeds", "events", "profiles", "ideas", "settings"];
if (!boardPath || !OUT) die("usage: node world_walk.mjs <board.md> --out <work folder> --stage <" + STAGES.join("|") + "|all>");
if (STAGE !== "all" && !STAGES.includes(STAGE)) die(`no stage "${STAGE}" (${STAGES.join(", ")}, all)`);
const CORE = `${DEV}/test/core.mjs`;
if (!existsSync(CORE)) die(`the plugin's node core is missing at ${CORE}; run \`npm run build\` in the dev folder`);
const bw = await import(pathToFileURL(CORE).href);

const text = readFileSync(abs(boardPath), "utf8");
if (!bw.isBoardText(text)) die(`${boardPath} is not a Branch Writing board`);
const doc = bw.parse(text);
const s = bw.settingsOf(doc);
const L = s.levels.map((l) => l.key);
const [K_PART, K_SEQ, K_SCENE, K_BEAT, K_MICRO] = [L[1], L[2], L[3], L[4], L[5]];
const title = (c) => (c.body || "").split("\n")[0].trim();
const one = (t) => String(t || "").replace(/\s+/g, " ").trim();
const qn = (t) => one(t).replace(/[’‘]/g, "'").replace(/[“”]/g, '"').replace(/…/g, "...");
const low = (t) => qn(t).toLowerCase();
const cut = (t, n = 160) => { t = one(t); return t.length > n ? t.slice(0, n - 1) + "…" : t; };
const esc = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const bare = (n) => one(n).replace(/^the\s+/i, "");
mkdirSync(OUT, { recursive: true });

// ── Project, registry, threads ────────────────────────────────────────────────────────────────────────────────────────
const project = bw.projectCard(doc);
const boardTitle = project ? title(project) : basename(boardPath, ".md");
let PROJ = arg("--project");
if (!PROJ) {
  const root = `${VAULT}/WRITING/PROJECTS`;
  const want = [boardTitle, basename(boardPath, ".md")].map((x) => x.toLowerCase());
  const hit = existsSync(root) ? readdirSync(root).find((d) => want.some((w) => w.includes(d.toLowerCase()))) : null;
  if (hit) PROJ = `WRITING/PROJECTS/${hit}`;
}
const REG = PROJ ? `${abs(PROJ)}/DEV/registry` : null;
const THREADS = arg("--threads") ? abs(arg("--threads")) : PROJ ? `${abs(PROJ)}/REFERENCE/threads.md` : null;

// ── Story order ───────────────────────────────────────────────────────────────────────────────────────────────────────
const pos = new Map(); // id → { part, partTitle, seq, scene, sc }
const scenes = [];
let partN = 0, scN = 0, cur = { part: 0, partTitle: "", seq: "", scene: "", sc: 0 };
const walk = (c) => {
  const k = c.meta.kind;
  if (k === K_PART) { partN++; cur = { part: partN, partTitle: title(c), seq: "", scene: "", sc: scN }; }
  else if (k === K_SEQ) cur = { ...cur, seq: title(c), scene: "" };
  else if (k === K_SCENE) { scN++; cur = { ...cur, scene: title(c), sc: scN }; scenes.push(c); }
  pos.set(c.id, { ...cur });
  for (const ch of c.children || []) walk(ch);
};
for (const ch of (project ? project.children : doc.cards.filter((c) => !c.parent))) walk(ch);
const where = (id) => { const p = pos.get(id); if (!p) return "unplaced"; return `P${p.part} · ${p.seq || p.partTitle}${p.scene ? ` › ${p.scene}` : ""}`; };
const scOf = (id) => (pos.get(id) || {}).sc || 0;
const sc = (n) => `sc ${String(n).padStart(3, "0")}`;
const descendants = (c) => { const out = []; const go = (x) => { for (const k of x.children || []) { out.push(k); go(k); } }; go(c); return out; };
const sceneOf = (c) => { let x = c; while (x && x.meta.kind !== K_SCENE) x = x.parent; return x; };
// His words per scene: micro-beats and idea cards, never summaries or titles.
const hisCards = (c) => descendants(c).filter((k) => k.meta.kind === K_MICRO || k.meta.kind === "idea");
const sceneWords = new Map(scenes.map((c) => [c.id, hisCards(c)]));
const eraName = (id) => (bw.eraById(doc, id) || {}).name || id || "";

/** A name finder for a list of names: case-insensitive, word-bounded, "the" optional. */
function finder(names) {
  const forms = [...new Set(names.filter(Boolean).flatMap((n) => [one(n), bare(n)]).filter((n) => n.length >= 3))].sort((a, b) => b.length - a.length);
  if (!forms.length) return null;
  return new RegExp(`(?<![\\p{L}\\p{N}])(?:${forms.map((f) => esc(qn(f)).replace(/\\ /g, "\\s+")).join("|")})(?![\\p{L}\\p{N}])`, "giu");
}
function hits(re, cards) {
  const out = [];
  if (!re) return out;
  for (const k of cards) { const t = qn(k.body); re.lastIndex = 0; let m; while ((m = re.exec(t))) out.push({ id: k.id, kind: k.meta.kind, at: m.index, form: m[0], text: t }); }
  return out;
}
const snippet = (h) => { const a = Math.max(0, h.at - 60), b = Math.min(h.text.length, h.at + h.form.length + 60); return (a ? "…" : "") + h.text.slice(a, b) + (b < h.text.length ? "…" : ""); };

// ── Registry reading ──────────────────────────────────────────────────────────────────────────────────────────────────
function fm(t) { const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(t); const o = {}; if (m) for (const l of m[1].split(/\r?\n/)) { const x = /^([\w-]+):\s*(.*)$/.exec(l); if (x) o[x[1]] = x[2].replace(/^["']|["']$/g, ""); } return { meta: o, body: m ? t.slice(m[0].length) : t }; }
function sections(body) {
  const out = {}; let head = "_lead", buf = [];
  for (const l of body.replace(/<!--[\s\S]*?-->/g, "").split(/\r?\n/)) { const h = /^##\s+(.+)$/.exec(l); if (h) { out[head] = buf.join("\n").trim(); head = h[1].trim(); buf = []; } else buf.push(l); }
  out[head] = buf.join("\n").trim();
  return out;
}
// His rulings anywhere in an entry ("⚑ … RULED (CRE, date)"): a later ruling outranks the entry's opening section.
const rulingsOf = (body) => body.split(/\r?\n/).filter((l) => /⚑/.test(l) && /RULED|ruled/.test(l)).map((l) => cut(l.replace(/\*\*|\*/g, ""), 300));
const blurbOf = (body) => { const m = /^>\s.*?\*\((.+?)\)\*/m.exec(body); return m ? one(m[1]) : ""; };
function readRegistry() {
  const entries = [];
  if (!REG || !existsSync(REG)) return entries;
  const dirKind = { characters: "character", locations: "place", lore: "lore" };
  for (const [dir, kind] of Object.entries(dirKind)) {
    const d = `${REG}/${dir}`;
    if (!existsSync(d)) continue;
    for (const f of readdirSync(d).filter((x) => x.endsWith(".md") && x !== "README.md")) {
      const raw = readFileSync(`${d}/${f}`, "utf8");
      const { meta, body } = fm(raw);
      const name = meta.name || f.replace(/\.md$/, "");
      const sec = sections(body);
      const pick = (re) => { const k = Object.keys(sec).find((x) => re.test(x)); return k ? cut(sec[k], 1200) : ""; };
      entries.push({ name, kind, path: relv(`${d}/${f}`), status: meta.status || "", blurb: blurbOf(body), rulings: rulingsOf(body),
        whatItIs: kind === "character" ? pick(/^who they are/i) : pick(/^what it is/i),
        profile: kind === "character" ? { who: pick(/^who they are/i), flawWound: pick(/flaw|wound/i), want: pick(/want/i), transformation: pick(/transformation/i), voice: pick(/voice/i), appearance: pick(/appearance|look/i) } : undefined,
        feels: pick(/feels like/i), means: pick(/means/i) });
    }
  }
  const ip = `${REG}/items.md`;
  if (existsSync(ip)) {
    const { body } = fm(readFileSync(ip, "utf8"));
    const noFence = body.replace(/```[\s\S]*?```/g, "");
    const parts = noFence.split(/^###\s+/m).slice(1);
    for (const p of parts) {
      const name = one(p.split(/\r?\n/)[0]);
      const rest = p.slice(p.indexOf("\n") + 1);
      const w = /\*\*What it is\.\*\*\s*([^\n]+)/.exec(rest);
      const d = /\*\*What it does \/ means\.\*\*\s*([^\n]+)/.exec(rest);
      entries.push({ name, kind: "item", path: `${relv(ip)}#${name}`, status: "", blurb: "", rulings: rulingsOf(rest), whatItIs: cut(w ? w[1] : rest, 1200), means: d ? cut(d[1], 900) : "", feels: "" });
    }
  }
  // Display aliases he uses in the registry's own links: [[The Witch|lurker]], [[Old Man|The hound]], [[registry/items#Petyr the Brave|…]].
  const aliases = new Map();
  const scan = (t) => { for (const m of t.matchAll(/\[\[([^\]|]+?)\|([^\]]+)\]\]/g)) { const target = m[1].includes("#") ? m[1].split("#").pop() : m[1].split("/").pop(); const k = low(target.replace(/\.md$/, "")); const a = one(m[2]); if (!aliases.has(k)) aliases.set(k, new Map()); aliases.get(k).set(a, (aliases.get(k).get(a) || 0) + 1); } };
  const walkDir = (d) => { for (const f of readdirSync(d, { withFileTypes: true })) { if (f.isDirectory()) walkDir(`${d}/${f.name}`); else if (f.name.endsWith(".md")) scan(readFileSync(`${d}/${f.name}`, "utf8")); } };
  walkDir(REG);
  for (const e of entries) { const m = aliases.get(low(e.name)) || new Map(); e.linkAliases = [...m.entries()].filter(([a]) => low(bare(a)) !== low(bare(e.name)) && low(bare(a)).replace(/['’]s$/, "") !== low(bare(e.name))).sort((a, b) => b[1] - a[1]).map(([a, n]) => ({ alias: a, n })); }
  return entries;
}

// ── Board vocab ───────────────────────────────────────────────────────────────────────────────────────────────────────
const cast = bw.castOf(doc);
const world = bw.worldOf(doc);
const castNames = (c) => [bw.castName(c), ...bw.castAliases(c)];
const worldNames = (e) => bw.allWorldNames(e);
const allMicro = doc.cards.filter((c) => c.meta.kind === K_MICRO);
const allIdeas = doc.cards.filter((c) => c.meta.kind === "idea");
const notChecked = [];
const writeStage = (name, json, md) => { writeFileSync(`${OUT}/${name}.json`, JSON.stringify(json, null, 1), "utf8"); writeFileSync(`${OUT}/${name}.md`, md.join("\n") + "\n", "utf8"); console.log(`${name}: ${OUT}/${name}.md`); };

// ── Stage 1: the registry ─────────────────────────────────────────────────────────────────────────────────────────────
function stageRegistry() {
  const reg = readRegistry();
  const md = [`# Stage 1 — the registry (${relv(REG || "no registry")})`, "", "Proposals, one per registry entry not on the board. The registry is dev material (\"developing understanding, not committed canon\"): every row is his to rule. Mentions = his words (micro-beats · ideas).", ""];
  if (!reg.length) { md.push(`No DEV registry found${PROJ ? ` at ${relv(REG)}` : " (no project matched the board; pass --project)"} — stage skipped.`); writeStage("registry", { skipped: true, rows: [] }, md); return; }
  const rows = [];
  for (const e of reg) {
    const names = [e.name, ...e.linkAliases.filter((a) => a.n >= 1).map((a) => a.alias)];
    const reName = finder([e.name]);
    const micro = hits(reName, allMicro), ideas = hits(reName, allIdeas);
    let onBoard = null, evidence = "";
    if (e.kind === "character") {
      // Which registry character is which cast member is always his ruling: names drift (the registry's "Hunter" is the
      // board's woodswoman, while the board's "the hunter" is another man). Every candidate is listed with its evidence.
      const why = [];
      for (const c of cast) {
        if (castNames(c).some((n) => low(bare(n)) === low(bare(e.name)))) why.push(`same name as cast "${bw.castName(c)}"`);
        const a = e.linkAliases.find((x) => castNames(c).some((n) => low(bare(x.alias)) === low(bare(n))));
        if (a) why.push(`the registry links it as "${a.alias}" (${a.n}×), which is cast "${bw.castName(c)}"`);
      }
      for (const w of world) if (worldNames(w).some((n) => low(bare(n)) === low(bare(e.name)))) why.push(`world entry "${bw.worldName(w)}" (${bw.worldKindOf(w)}) — on the board, not as cast`);
      if (why.length) { onBoard = why.map((w) => (/(?:cast|entry) "([^"]+)"/.exec(w) || [])[1]).filter(Boolean).filter((x, i, l) => l.indexOf(x) === i).join(" or "); evidence = why.join("; "); }
    } else {
      const exact = world.find((w) => worldNames(w).some((n) => low(bare(n)) === low(bare(e.name))));
      if (exact) { onBoard = bw.worldName(exact); evidence = `world entry "${onBoard}" (${bw.worldKindOf(exact)})`; }
    }
    const row = { name: e.name, registryKind: e.kind, path: e.path, status: e.status, blurb: e.blurb, rulings: e.rulings || [], whatItIs: e.whatItIs, means: e.means || "", feels: e.feels || "", linkAliases: e.linkAliases, mentions: { micro: micro.length, ideas: ideas.length, firstScene: micro.length ? sc(scOf(sceneOf(doc.cards.find((k) => k.id === micro[0].id))?.id)) : "" }, onBoard, evidence,
      proposedKind: e.kind === "character" ? "cast" : e.kind === "lore" ? null : e.kind, kindOptions: e.kind === "lore" ? bw.worldKinds(s).map((k) => k.key) : undefined, profile: e.profile };
    row.action = !onBoard ? (e.kind === "character" ? "add-cast?" : "add-world?") : e.kind === "character" ? "same as? (his ruling)" : "on the board";
    rows.push(row);
  }
  const order = { "add-world?": 0, "add-cast?": 1, "same as? (his ruling)": 2, "on the board": 3 };
  rows.sort((a, b) => order[a.action] - order[b.action] || a.registryKind.localeCompare(b.registryKind) || (b.mentions.micro + b.mentions.ideas) - (a.mentions.micro + a.mentions.ideas));
  const tot = (a) => rows.filter((r) => r.action === a).length;
  md.push(`**Totals:** ${tot("add-world?")} world entries to propose · ${tot("add-cast?")} cast to propose · ${tot("same as? (his ruling)")} possible matches to confirm · ${tot("on the board")} already on the board.`, "");
  for (const r of rows) {
    md.push(`## ${r.name} — ${r.registryKind} · ${r.action}`, `- source: \`${r.path}\`${r.status ? ` (${r.status})` : ""}`, `- mentions: ${r.mentions.micro} · ${r.mentions.ideas}${r.mentions.firstScene ? `, first in ${r.mentions.firstScene}` : ""}`);
    if (r.evidence) md.push(`- board: ${r.evidence}`);
    if (r.linkAliases.length) md.push(`- the registry also calls it: ${r.linkAliases.map((a) => `"${a.alias}" (${a.n})`).join(", ")}`);
    if (r.kindOptions) md.push(`- kind: his call (${r.kindOptions.join(" / ")})`);
    if (r.blurb) md.push(`- blurb: ${r.blurb}`);
    if (r.whatItIs) md.push(`- what it is: ${cut(r.whatItIs, 600)}`);
    for (const x of r.rulings) md.push(`- ⚑ his ruling in the entry (outranks the above): ${x}`);
    md.push("");
  }
  writeStage("registry", { registry: relv(REG), rows }, md);
  notChecked.push("registry: whether each entry is current against the landed chapters (the registry is dev-layer; REFERENCE/bible.md was not read); mention counts are name matches, so a renamed thing under-counts and a common word over-counts.");
}

// ── Stage 2: links ────────────────────────────────────────────────────────────────────────────────────────────────────
function stageLinks() {
  const md = ["# Stage 2 — links (scenes whose words name a world entry)", "", "One link per scene; the cards inside carry it. A place fills the scene's `setting` where it is empty. **Direct** rows are admin once the entry is approved; **Ask** rows are names that are also ordinary words, so the matches need his one-line call per entry.", ""];
  const rows = [];
  for (const e of world) {
    const re = finder(worldNames(e));
    const per = [];
    let total = 0, capital = 0;
    for (const scn of scenes) {
      const h = hits(re, sceneWords.get(scn.id));
      if (!h.length) continue;
      total += h.length; capital += h.filter((x) => /^(the\s+)?\p{Lu}/u.test(x.form) && !/^The\s+\p{Ll}/u.test(x.form)).length;
      per.push({ scene: scn.id, sc: scOf(scn.id), where: where(scn.id), n: h.length, linked: bw.cardWorldIds(scn).includes(e.id), setting: (scn.meta.fields || {}).setting || "", example: snippet(h[0]) });
    }
    const proper = /^\p{Lu}/u.test(bare(bw.worldName(e)));
    const share = total ? capital / total : 0;
    const ask = !proper || share < 0.6 || /^(magic|religion|cottage)$/i.test(bare(bw.worldName(e)));
    rows.push({ entry: bw.worldName(e), id: e.id, kind: bw.worldKindOf(e), by: e.meta.by || "", total, capitalShare: Number(share.toFixed(2)), route: ask ? "ask" : "direct", scenes: per });
  }
  rows.sort((a, b) => (a.route === b.route ? b.total - a.total : a.route === "direct" ? -1 : 1));
  md.push(`**Totals:** ${rows.filter((r) => r.route === "direct").reduce((n, r) => n + r.scenes.filter((x) => !x.linked).length, 0)} scene links direct · ${rows.filter((r) => r.route === "ask").length} entries to ask about · ${rows.filter((r) => !r.total).length} entries no scene names.`, "");
  for (const r of rows) {
    md.push(`## ${r.entry} (${r.kind}) — ${r.route}, ${r.scenes.length} scenes, ${r.total} mentions${r.route === "ask" ? `, ${Math.round(r.capitalShare * 100)}% capitalised` : ""}`);
    for (const x of r.scenes) md.push(`- ${sc(x.sc)} ${x.where} ^${x.scene}${x.linked ? " (linked)" : ""}${x.setting ? ` [setting: ${x.setting}]` : ""} ×${x.n} — ${x.example}`);
    md.push("");
  }
  writeStage("links", { rows }, md);
  notChecked.push("links: a scene that is set somewhere without naming it is not found (setting by inference is not a link); a name inside a word he uses differently is caught only by the Ask route's capital-letter test.");
}

// ── Stage 3: the era walk ─────────────────────────────────────────────────────────────────────────────────────────────
function stageEras() {
  const sceneMode = s.eraSource === "scene" || (project && (project.meta.settings || {}).eraSource === "scene");
  const md = [`# Stage 3 — the era walk (eras come from ${sceneMode ? "scenes" : "sequences"})`, "", "Proposals only: a scene's era and a flashback call are story calls. Placed arc steps inherit their scene's era and are never stamped.", ""];
  const own = (c) => c.meta.era || "";
  const rowsA = [], rowsB = [];
  for (const scn of scenes) {
    const fb = bw.isFlashback(scn);
    const interlude = /interlude/i.test(title(scn)) || /interlude/i.test((pos.get(scn.id) || {}).seq || "");
    if (!(fb && !own(scn)) && !(interlude && !fb && !own(scn))) continue;
    const words = sceneWords.get(scn.id).filter((k) => k.meta.kind === K_MICRO).slice(0, 4).map((k) => cut(k.body, 220));
    const beats = (scn.children || []).filter((k) => k.meta.kind === K_BEAT).map((b) => cut(title(b), 80));
    const row = { scene: scn.id, sc: scOf(scn.id), where: where(scn.id), title: title(scn), flashback: fb, readsAs: eraName(bw.eraIdAt(scn)), seqEra: eraName(own(scn.parent || {})), opening: words, beats, summary: cut((scn.meta.fields || {}).summary || "", 300) };
    (fb ? rowsA : rowsB).push(row);
  }
  // Past scenes the "interlude" screen misses (Witchwood 2026-10-22: the Woodsgirl's midpoint chapters alternate with the
  // present and carry no "interlude" in their titles). A name that sits mostly in flashback scenes ("the woodsgirl") marks
  // the past; a non-flashback scene where such names outnumber every other cast name is listed for his call.
  const castForms = cast.flatMap((c) => castNames(c).map((n) => ({ n, re: finder([n]) })));
  const mentions = new Map(scenes.map((scn) => [scn.id, castForms.map((f) => hits(f.re, sceneWords.get(scn.id)).length)]));
  const markers = castForms.map((f, i) => { let inFb = 0, all = 0; for (const scn of scenes) { const m = mentions.get(scn.id)[i]; all += m; if (bw.isFlashback(scn) || /interlude/i.test(title(scn))) inFb += m; } return all >= 10 && inFb / all >= 0.4; });
  const rowsD = [];
  for (const scn of scenes) {
    if (bw.isFlashback(scn)) continue;
    const m = mentions.get(scn.id); let past = 0, other = 0;
    m.forEach((x, i) => (markers[i] ? (past += x) : (other += x)));
    if (past >= 3 && past > other) rowsD.push({ scene: scn.id, sc: scOf(scn.id), where: where(scn.id), title: title(scn), readsAs: eraName(bw.eraIdAt(scn)), pastNames: past, otherNames: other, summary: cut((scn.meta.fields || {}).summary || "", 300) });
  }
  // His placeholders (held —, body —, bond —, audit — …) are markers, not events: never given an era.
  const isMarker = (c) => /^(held|body|bond|adage|hermit|audit|keep-dark)\s+—/i.test(one(c.body));
  const unplaced = doc.cards.filter((c) => c.meta.kind === "arcbeat" && c.parent && c.parent.meta.kind === "project" && !own(c) && one(c.body) && !isMarker(c));
  const arcName = new Map(); for (const c of cast) for (const a of c.meta.arcs || []) arcName.set(a.id, `${bw.castName(c)} · ${a.name}`); for (const a of bw.plotArcs(doc)) arcName.set(a.id, a.label || a.id);
  const rowsC = unplaced.map((c) => ({ step: c.id, arc: arcName.get(c.meta.plotArc || c.meta.arc) || "", label: c.meta.label || "", set: c.meta.set || "", text: cut(c.body, 260) }));
  const used = new Set(doc.cards.map((c) => own(c)).filter(Boolean));
  const unusedEras = bw.erasOf(doc).filter((e) => !used.has(e.id) && !bw.erasOf(doc).some((x) => x.parent === e.id)).map((e) => e.name);
  md.push(`**Totals:** ${rowsA.length} flashbacks with no era · ${rowsB.length} interludes neither flashback nor given an era · ${rowsD.length} past scenes not marked a flashback · ${rowsC.length} unplaced arc steps with no era (placeholder markers left out) · eras no card sets: ${unusedEras.join(", ") || "none"} (listed, never proposed for removal).`, "");
  md.push("## Flashbacks with no era (each reads as the era around it)", "");
  for (const r of rowsA) md.push(`### ${sc(r.sc)} ${r.where} ^${r.scene} — reads as ${r.readsAs}`, ...r.opening.map((w) => `> ${w}`), r.beats.length ? `- beats: ${r.beats.join(" · ")}` : "", "");
  md.push("## Interludes not marked a flashback, no era", "");
  for (const r of rowsB) md.push(`### ${sc(r.sc)} ${r.where} ^${r.scene} — reads as ${r.readsAs}`, ...r.opening.map((w) => `> ${w}`), r.beats.length ? `- beats: ${r.beats.join(" · ")}` : "", "");
  md.push("## Past scenes not marked a flashback (names that live in the past outnumber the rest)", "");
  for (const r of rowsD) md.push(`- ${sc(r.sc)} ${r.where} ^${r.scene} — reads as ${r.readsAs}; past names ×${r.pastNames}, others ×${r.otherNames}${r.summary ? ` — ${r.summary}` : ""}`);
  md.push("", "## Unplaced arc steps with no era", "");
  for (const r of rowsC) md.push(`- ^${r.step} ${r.arc}${r.label ? ` [${r.label}]` : ""}${r.set ? ` (set ${r.set})` : ""}: ${r.text}`);
  writeStage("eras", { eraSource: sceneMode ? "scene" : "sequence", eras: bw.erasOf(doc).map((e) => ({ id: e.id, name: e.name, parent: e.parent || "" })), flashbacks: rowsA, interludes: rowsB, pastScenes: rowsD, unplacedSteps: rowsC, unusedEras }, md);
  notChecked.push("eras: a past scene that neither says \"interlude\" nor names a past-only cast name (the screen that caught Witchwood's Ch 42/44/46 missed Ch 40 and Ch 59, which name no one) is not listed — read the chapters around a flagged run; the DEV sequence notes and the arc plan are not read by the script (read them for the evidence of a proposal).");
}

// ── Stage 4: seeds from the thread list ───────────────────────────────────────────────────────────────────────────────
function readThreads() {
  if (!THREADS || !existsSync(THREADS)) return null;
  const t = readFileSync(THREADS, "utf8");
  const out = [];
  let section = "";
  for (const block of t.split(/^(?=##\s)/m)) {
    const h2 = /^##\s+(.+)$/m.exec(block); if (h2 && !/^###/.test(block)) section = h2[1].trim();
    for (const th of block.split(/^###\s+/m).slice(1)) {
      const head = one(th.split(/\r?\n/)[0]);
      const m = /^(T\d+)\s+—\s+(.+)$/.exec(head); if (!m) continue;
      const line = (k) => { const x = new RegExp(`^- \\*\\*${k}:\\*\\*\\s*(.+)$`, "m").exec(th); return x ? x[1].trim() : ""; };
      out.push({ id: m[1], name: m[2].replace(/\s+⚠️.*$|\s+⚑.*$/u, "").trim(), section, planted: line("Planted"), status: line("Status") });
    }
  }
  return out;
}
const quotesIn = (t) => [...String(t || "").matchAll(/"([^"]{6,})"|“([^”]{6,})”/g)].map((m) => m[1] || m[2]);
const frags = (q) => qn(q).split(/\.\.\.|\*/).map((x) => x.trim().replace(/^[,;:—-]\s*/, "")).filter((x) => x.split(/\s+/).length >= 3);
// Present = the quote's words, in order, in one scene's micro-beats read as one run (a split card doesn't hide it), with
// punctuation and case ignored (a moved comma is not a rewording of the span).
const letters = (t) => low(t).replace(/[^\p{L}\p{N}]+/gu, " ").trim();
let sceneRuns = null;
function runs() {
  if (sceneRuns) return sceneRuns;
  sceneRuns = scenes.map((scn) => { const cards = sceneWords.get(scn.id).filter((k) => k.meta.kind === K_MICRO); let at = 0; const spans = []; const parts = []; for (const k of cards) { const t = letters(k.body); spans.push({ id: k.id, start: at, end: at + t.length }); parts.push(t); at += t.length + 1; } return { scn, text: parts.join(" "), spans }; });
  return sceneRuns;
}
function matchQuote(q) {
  const fs = frags(q);
  if (!fs.length) return { state: "too short to match", q };
  const fl = fs.map(letters).filter(Boolean);
  for (const r of runs()) {
    const at = fl.map((f) => r.text.indexOf(f));
    if (at.every((i) => i >= 0)) {
      const cardAt = (i) => (r.spans.find((x) => i >= x.start && i <= x.end) || r.spans[0]).id;
      const first = cardAt(at[0]);
      return { state: "present", q, card: first, scene: r.scn.id, sc: scOf(r.scn.id), where: where(first), all: at.map(cardAt) };
    }
  }
  const found = fl.map((f) => runs().some((r) => r.text.includes(f)) ? [1] : []);
  // reworded? the micro-beat sharing the most of the quote's words (≥ 60%) is the candidate
  const words = new Set(low(fs.join(" ")).match(/[\p{L}']+/gu) || []);
  let best = null, bestScore = 0;
  for (const k of allMicro) { const kw = new Set(low(k.body).match(/[\p{L}']+/gu) || []); let n = 0; for (const w of words) if (kw.has(w)) n++; const sc2 = words.size ? n / words.size : 0; if (sc2 > bestScore) { bestScore = sc2; best = k; } }
  if (best && bestScore >= 0.6 && words.size >= 5) return { state: "reworded?", q, card: best.id, scene: sceneOf(best)?.id, sc: scOf(sceneOf(best)?.id), where: where(best.id), overlap: Number(bestScore.toFixed(2)), now: cut(best.body, 240), partial: found.map((x) => x.length > 0) };
  return { state: "gone", q, partial: found.map((x) => x.length > 0) };
}
function stageSeeds() {
  const md = ["# Stage 4 — seeds from the thread list", ""];
  const threads = readThreads();
  if (!threads) { md.push(`No thread list found${THREADS ? ` at ${relv(THREADS)}` : ""} — stage skipped.`); writeStage("seeds", { skipped: true, rows: [] }, md); return; }
  md.push(`Source: \`${relv(THREADS)}\` (spec material — never seed a board a blind-read or dev-edit panel will read). Span rule (DIR-019): present → propose the tag; gone → skip with a log line; reworded → one batched question.`, "");
  // A readable tag: the thread's name before any " / " or "(", leading "the" and possessive 's dropped, at most four words,
  // never ending on a small word ("t25-presence-in-the-darkness", not "t25-the-presence-in-the").
  const SMALL = new Set(["the", "a", "an", "of", "in", "on", "to", "and", "with", "for", "her", "his", "its"]);
  const slug = (th) => { let w = th.name.replace(/^["“]+/, "").split(/\s+\/\s+|\s*\(|"|”/)[0].toLowerCase().replace(/['’]s(?=\s|$)/g, "s").replace(/[^\p{L}\p{N}]+/gu, " ").trim().split(/\s+/); if (w[0] === "the" && w.length > 1) w = w.slice(1); w = w.slice(0, 4); while (w.length > 1 && SMALL.has(w[w.length - 1])) w.pop(); return `${th.id.toLowerCase()}-${w.join("-")}`; };
  const seenIds = new Set();
  const rows = threads.filter((th) => { const dup = seenIds.has(th.id) && !th.planted; seenIds.add(th.id); return !dup; }).map((th) => {
    const settled = /settled/i.test(th.section);
    const paid = settled && /\bpaid\b/i.test(th.status);
    const seedQ = quotesIn(th.planted).map(matchQuote);
    const payQ = paid ? quotesIn(th.status).map(matchQuote) : [];
    return { id: th.id, name: th.name, tag: slug(th), section: th.section, status: th.status ? cut(th.status, 200) : "", abandoned: /abandon/i.test(th.status), planted: cut(th.planted, 300), seed: seedQ, payoff: payQ, paid };
  });
  const n = (f) => rows.filter(f).length;
  md.push(`**Totals:** ${rows.length} threads · seed present ${n((r) => r.seed.some((x) => x.state === "present"))} · reworded? ${n((r) => !r.seed.some((x) => x.state === "present") && r.seed.some((x) => x.state === "reworded?"))} · gone ${n((r) => r.seed.length && r.seed.every((x) => x.state === "gone"))} · no quote in the Planted line ${n((r) => !r.seed.length)} · paid with a payoff quote found ${n((r) => r.payoff.some((x) => x.state === "present"))}.`, "");
  for (const r of rows) {
    md.push(`## ${r.id} — ${r.name}  → \`seed:${r.tag}\`${r.paid ? ` / \`payoff:${r.tag}\`` : ""} (${r.section}${r.abandoned ? ", abandoned" : ""})`);
    if (!r.seed.length) md.push(`- no quote to match in the Planted line: ${r.planted}`);
    for (const x of r.seed) md.push(`- seed ${x.state}: "${cut(x.q, 120)}"${x.card ? ` → ^${x.card} ${sc(x.sc)} ${x.where}` : ""}${x.now ? ` — now reads: ${x.now}` : ""}`);
    for (const x of r.payoff) md.push(`- payoff ${x.state}: "${cut(x.q, 120)}"${x.card ? ` → ^${x.card} ${sc(x.sc)} ${x.where}` : ""}${x.now ? ` — now reads: ${x.now}` : ""}`);
    md.push("");
  }
  writeStage("seeds", { threads: relv(THREADS), rows }, md);
  notChecked.push("seeds: a Planted line with no quoted words (\"devilkin dream-story, segment 1\") cannot be matched and is listed open; a quote matched in more than one place takes the first in story order (the others are in the json); payoffs come only from Settled threads marked paid, with a quote in their Status line.");
}

// ── Stage 6: events ───────────────────────────────────────────────────────────────────────────────────────────────────
function stageEvents() {
  const md = ["# Stage 6 — pin the events", "", "A pin is the card the event happens on — a story call, proposed with the card's words as the reason. Pinning takes the card's era: a candidate in another era is marked, and needs his ruling that the era moves.", ""];
  const STOP = new Set("the a an of in on to and her his their its key event multiple born died built destroyed".split(" "));
  const rows = [];
  for (const ev of bw.eventsOf(doc)) {
    const label = bw.eventLabel(doc, ev);
    if (ev.at) { rows.push({ id: ev.id, label, era: eraName(ev.era), pinned: ev.at, pinnedWhere: where(ev.at), candidates: [] }); continue; }
    const who = (ev.who || []).map((id) => bw.findCard(doc, id)).filter(Boolean);
    const reWho = finder(who.flatMap((c) => (bw.isCast(c) ? castNames(c) : worldNames(c))));
    const keys = (low(label).match(/[\p{L}']+/gu) || []).filter((w) => w.length > 2 && !STOP.has(w));
    const verb = ({ born: ["born", "birth"], died: ["died", "dead", "death", "dies"], built: ["built", "made", "build"], destroyed: ["destroyed", "burned", "broke"] })[ev.type] || [];
    const reKey = finder([...keys, ...verb]);
    const cands = [];
    for (const scn of scenes) {
      const cards = sceneWords.get(scn.id);
      const hw = hits(reWho, cards).length, hk = hits(reKey, cards);
      if (!hk.length) continue;
      const era = bw.eraIdAt(scn);
      cands.push({ scene: scn.id, sc: scOf(scn.id), where: where(scn.id), era: eraName(era), sameEra: era === ev.era, score: hk.length * 2 + Math.min(hw, 5), example: snippet(hk[0]) });
    }
    cands.sort((a, b) => (b.sameEra - a.sameEra) || b.score - a.score);
    rows.push({ id: ev.id, label, type: ev.type, era: eraName(ev.era), who: who.map((c) => (bw.isCast(c) ? bw.castName(c) : bw.worldName(c))), candidates: cands.slice(0, 6) });
  }
  const open = rows.filter((r) => !r.pinned);
  md.push(`**Totals:** ${rows.length} events · ${rows.length - open.length} pinned · ${open.length} to propose (${open.filter((r) => !r.candidates.some((c) => c.sameEra)).length} with no candidate in their own era).`, "");
  for (const r of open) {
    md.push(`## ${r.label} [${r.id}] — ${r.era}${r.who.length ? `, ${r.who.join(" & ")}` : ""}`);
    if (!r.candidates.length) md.push("- no scene's words name it — leave unpinned (open line)");
    for (const c of r.candidates) md.push(`- ${c.sameEra ? "same era" : `OTHER ERA (${c.era})`} · ${sc(c.sc)} ${c.where} ^${c.scene} — ${c.example}`);
    md.push("");
  }
  writeStage("events", { rows }, md);
  notChecked.push("events: candidates come from the event's words and its subjects' names in his words; an event the prose shows without naming (a birth told as \"the cry\") is missed — read the era's scenes when no candidate fits.");
}

// ── Stage 7: profiles ─────────────────────────────────────────────────────────────────────────────────────────────────
function stageProfiles() {
  const reg = readRegistry().filter((e) => e.kind === "character");
  const md = ["# Stage 7 — profiles from the registry character entries", "", "Proposals: each answer a plain line drawn from his words, his lines kept in `notes` with the registry path. Which registry entry is which cast member is confirmed in stage 1 — use those rulings, never this file's guess.", ""];
  const rows = cast.map((c) => {
    const names = castNames(c).map((n) => low(bare(n)));
    const guess = reg.find((e) => names.includes(low(bare(e.name))) || e.linkAliases.some((a) => names.includes(low(bare(a.alias)))));
    const have = {}; for (const k of ["role", "tagline", "want", "need", "flaw", "wound", "personality", "voice", "appearance", "notes"]) { const v = (c.meta.fields || {})[k] || ""; have[k] = v || ""; }
    return { cast: bw.castName(c), id: c.id, filled: Object.keys(have).filter((k) => have[k]), empty: Object.keys(have).filter((k) => !have[k]), registry: guess ? { name: guess.name, path: guess.path, profile: guess.profile } : null };
  });
  md.push(`**Totals:** ${rows.length} cast · ${rows.filter((r) => r.registry).length} with a registry entry (by name or link alias) · ${rows.filter((r) => !r.registry).length} with none (left as they are).`, "");
  for (const r of rows) {
    md.push(`## ${r.cast} — filled: ${r.filled.join(", ") || "nothing"}`);
    if (!r.registry) { md.push("- no registry entry: nothing to propose", ""); continue; }
    md.push(`- registry: \`${r.registry.path}\` (${r.registry.name})`);
    for (const [k, v] of Object.entries(r.registry.profile || {})) if (v) md.push(`- ${k}: ${cut(v, 500)}`);
    md.push("");
  }
  writeStage("profiles", { rows }, md);
  notChecked.push("profiles: only the registry's character entries are read; a profile answer the board's own prose implies is not proposed (that is a reading, and his to give).");
}

// ── Stage 8: idea admin ───────────────────────────────────────────────────────────────────────────────────────────────
function stageIdeas() {
  const md = ["# Stage 8 — idea admin (type, duplicates)", "", "Admin, written directly, logged and undoable (CRE 2026-10-22). Never an idea's words. `by: ai` tags on ideas come from stage 5 (tagging mode).", ""];
  const types = s.ideaTypes || ["dialogue", "beat", "scene", "twist", "image", "question"];
  const rows = allIdeas.map((c) => {
    const t = qn(c.body).trim();
    let sure = "";
    if (/^["“']/.test(c.body.trim()) && types.includes("dialogue")) sure = "dialogue";
    else if (/\?["”']?\s*$/.test(t) && types.includes("question")) sure = "question";
    return { id: c.id, type: c.meta.type || "", sure, scene: sceneOf(c)?.id || "", sc: scOf(sceneOf(c)?.id), text: t };
  });
  const dups = [];
  const seen = new Map();
  for (const r of rows) { const k = `${r.scene}|${(allIdeas.find((c) => c.id === r.id).body || "").trim()}`; if (seen.has(k)) dups.push({ idea: r.id, twin: seen.get(k), sc: r.sc, text: cut(r.text, 100) }); else seen.set(k, r.id); }
  const across = new Map(); for (const c of allIdeas) { const k = c.body.trim(); across.set(k, [...(across.get(k) || []), c]); }
  const crossScene = [...across.values()].filter((l) => l.length > 1 && new Set(l.map((c) => sceneOf(c)?.id)).size > 1).map((l) => ({ ids: l.map((c) => c.id), scenes: l.map((c) => sc(scOf(sceneOf(c)?.id))), text: cut(l[0].body, 100) }));
  const sure = rows.filter((r) => r.sure && r.sure !== r.type);
  const read = rows.filter((r) => !r.sure);
  md.push(`**Totals:** ${rows.length} ideas · ${sure.length} retyped by their form (opens with a quote → dialogue, ends with ? → question) · ${read.length} to read and type from the board's list (${types.join(", ")}) · ${dups.length} byte-identical twins in one scene.`, "");
  md.push("## Twins (remove-duplicate-idea)", ...dups.map((d) => `- ^${d.idea} = ^${d.twin} (${sc(d.sc)}): ${d.text}`), "");
  md.push("## Same words in different scenes (left alone: an idea placed twice is not clutter; listed for him)", ...crossScene.map((d) => `- ${d.ids.map((x) => "^" + x).join(" = ")} (${d.scenes.join(", ")}): ${d.text}`), "");
  md.push("## To read (chunked in ideas.json `read`)", `${read.length} ideas; type each from its words alone — dialogue (a line spoken), image (a picture), scene (a whole scene's idea), twist (a reveal or reversal), question (an open question), beat (a story beat). Unsure stays beat.`);
  writeStage("ideas", { types, sure: sure.map((r) => ({ id: r.id, from: r.type, to: r.sure })), duplicates: dups, crossScene, read: read.map((r) => ({ id: r.id, type: r.type, sc: r.sc, text: r.text })) }, md);
  notChecked.push("ideas: the form test only catches dialogue that opens with a quote mark and questions that end with one; everything else is a reading.");
}

// ── Stage 9: settings — where each scene happens, read, never matched ─────────────────────────────────────────────────
// CRE 2026-10-22: "couldn't stuff like scene locations be mappable without selecting the first name?" A scene's setting is
// where its action happens, read from its own words; a place it only names (a wish, a memory, a destination) is not it.
// This stage writes one evidence file per chunk of scenes for parallel readers; the readers propose, he rules.
function stageSettings() {
  const places = world.filter((w) => /place/i.test(bw.worldKindOf(w)));
  const placeRe = places.map((p) => ({ name: bw.worldName(p), re: finder(worldNames(p)) }));
  const N = parseInt(arg("--chunk", "20"), 10);
  const rows = scenes.map((scn) => {
    const micro = sceneWords.get(scn.id).filter((k) => k.meta.kind === K_MICRO).map((k) => one(k.body)).join(" ");
    const ideas = sceneWords.get(scn.id).filter((k) => k.meta.kind === "idea").map((k) => one(k.body)).join(" / ");
    const named = placeRe.map((p) => ({ name: p.name, n: hits(p.re, sceneWords.get(scn.id)).length })).filter((x) => x.n);
    const words = micro.length > 2400 ? micro.slice(0, 1700) + " […] " + micro.slice(-700) : micro;
    return { scene: scn.id, sc: scOf(scn.id), where: where(scn.id), title: title(scn), era: eraName(bw.eraIdAt(scn)), flashback: bw.isFlashback(scn), setting: (scn.meta.fields || {}).setting || "", named, beats: (scn.children || []).filter((k) => k.meta.kind === K_BEAT).map((b) => title(b)), summary: one((scn.meta.fields || {}).summary || ""), words, ideas: words ? "" : cut(ideas, 1200) };
  });
  mkdirSync(`${OUT}/settings`, { recursive: true });
  const chunks = [];
  for (let i = 0; i < rows.length; i += N) chunks.push(rows.slice(i, i + N));
  chunks.forEach((ch, i) => writeFileSync(`${OUT}/settings/chunk${i + 1}.md`, ch.map((r) => [`## ^${r.scene} · ${sc(r.sc)} · ${r.where}`, `era: ${r.era}${r.flashback ? " (flashback)" : ""}${r.setting ? ` · setting now: ${r.setting}` : ""}`, `places named in his words: ${r.named.map((x) => `${x.name} ×${x.n}`).join(", ") || "none"}`, `beats (tool titles): ${r.beats.join(" · ") || "—"}`, r.summary ? `summary (tool-written): ${r.summary}` : "", r.words ? `HIS PROSE: ${r.words}` : r.ideas ? `HIS IDEAS (no prose yet): ${r.ideas}` : "HIS WORDS: none on this scene", ""].filter(Boolean).join("\n")).join("\n"), "utf8"));
  const md = ["# Stage 9 — settings (where each scene happens)", "", `${rows.length} scenes in ${chunks.length} chunks of ${N} in \`settings/\`. Board places: ${places.map((p) => bw.worldName(p)).join(", ")}.`, `Already set: ${rows.filter((r) => r.setting).length}. With no words of his: ${rows.filter((r) => !r.words && !r.ideas).length}.`, "", "Reader brief: for each scene, the place its action happens, from its own words — one of the board's places, a place his words name that is not an entry yet (quoted), or \"not shown\". A place named only in talk, memory, a wish or as a destination is not the setting. A scene that moves: the place of its main action, with the other places listed. Return `^id<TAB>place<TAB>new?<TAB>quote`."];
  writeStage("settings", { places: places.map((p) => bw.worldName(p)), chunks: chunks.length, rows: rows.map(({ words, ideas, ...r }) => r) }, md);
  notChecked.push("settings: a scene with no prose of his (an empty slot) can only be read from its idea cards and the tool's summary, which is weaker evidence; the DEV sequence notes are not part of the evidence file.");
}

const run = { registry: stageRegistry, links: stageLinks, eras: stageEras, seeds: stageSeeds, events: stageEvents, profiles: stageProfiles, ideas: stageIdeas, settings: stageSettings };
for (const st of STAGE === "all" ? STAGES : [STAGE]) run[st]();
writeFileSync(`${OUT}/README.md`, [`# World walk — ${boardTitle}`, "", `Board: \`${relv(boardPath)}\` (${doc.cards.length} cards, ${scenes.length} scenes). Project: ${PROJ || "none matched"}. Read-only; nothing on the board changed.`, "", "## What this walk did not check", ...notChecked.map((x) => `- ${x}`), "- Stage 5 (tagging) is the existing tagging mode: run `suggest-tags`, not this script.", ""].join("\n"), "utf8");
