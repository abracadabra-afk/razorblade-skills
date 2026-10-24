// branch-writing-expert: the one writer for Branch Writing boards, in node, outside Obsidian (no clicks in a window CRE
// may be using). Every write goes through here so that: (1) the installed plugin and the schema are checked against the
// skill's calibration record before anything is written; (2) each run is recorded first in the per-board change log with
// the exact before-text of every card it touches, so "undo the last run" restores those cards byte-for-byte and "redo" puts
// them back; (3) cards outside the run stay byte-identical (the plugin's own parse/serialize round-trip is the gate).
//
//   node board_tool.mjs check   [--board <board.md>]                 version check (+ the board's round-trip status)
//   node board_tool.mjs read    <board.md> [--full]                  the board as the run's source of truth (JSON)
//   node board_tool.mjs apply   <ops.json> [--dry]                   execute an ops file (shape: references/ops.md)
//   node board_tool.mjs undo    <board.md> [--run <id>] [--force]    restore the last applied run's cards
//   node board_tool.mjs redo    <board.md> [--run <id>] [--force]    re-apply the last undone run
//   node board_tool.mjs import  --source <note.md> --board <new.md> [--title <t>]        prose → board, verbatim
//   node board_tool.mjs import  --book <project dir> --board <new.md> [--title <t>]      one board from CHAPTERS/*/draft.md
//   node board_tool.mjs import  (--source <note.md> | --book <dir>) --into <existing.md> [--source-label <t>] [--dry]
//                                                                   the same, appended under an existing board's Project (one undoable run)
//   node board_tool.mjs propose <board.md> [--out <file.json>]       structure proposals for an imported board (ruled, never landed)
//   node board_tool.mjs suggest-tags <board.md> [--out <file.json>]  char:/place: tag offers from names in bodies (ruled)
//   node board_tool.mjs log     <board.md>                           the runs in the board's change log
//   node board_tool.mjs calibrate                                    record the installed plugin + schema as calibrated (after reading what changed)
//   node board_tool.mjs normalize <board.md>                         a logged whole-file run that makes a hand-edited file round-trip
//
// Options: --vault <path> (default CRE's vault), --dev <path> (the plugin dev folder, whose test/core.mjs is the plugin's
// pure core), --log-dir <path> (default <vault>/SYSTEM/board-logs), --manifest <path>, --schema <path>, --calibration <path>
// (test overrides for the version check). JSON inputs always come from a file, never a shell argument (^obs-444).
// Console output is UTF-8 (DIR-020). Exit 0 = done, 2 = refused (nothing written), 3 = finished with NOT DONE lines (a dry run
// exits 3 too when an op would be refused; it still writes nothing). Ids printed by --dry are provisional: the real run draws its own.
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, unlinkSync, statSync } from "node:fs";
import { dirname, basename, resolve, join } from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

for (const st of [process.stdout, process.stderr]) try { st.setDefaultEncoding("utf8"); } catch {}
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const flag = (k) => argv.includes(k);
const HOME = process.env.USERPROFILE || process.env.HOME || "";
const WIN = process.platform === "win32";
const VAULT = arg("--vault", WIN ? "C:/Users/Chad/Dropbox/razorblade_mermaid" : `${HOME}/Dropbox/razorblade_mermaid`).replace(/\\/g, "/");
const DEV = arg("--dev", WIN ? "C:/Users/Chad/dev/branch-writing" : `${HOME}/dev/branch-writing`).replace(/\\/g, "/");
const LOG_DIR = arg("--log-dir", `${VAULT}/SYSTEM/board-logs`).replace(/\\/g, "/");
const HERE = dirname(fileURLToPath(import.meta.url)).replace(/\\/g, "/");
const positional = argv.filter((a, i) => !a.startsWith("--") && !(i > 0 && argv[i - 1].startsWith("--") && !["--dry", "--force", "--full"].includes(argv[i - 1])));
const cmd = positional[0];
// A path is absolute, else relative to the current folder when something is there, else relative to the vault.
const abs = (p) => { if (!p) return p; p = p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`); if (/^[A-Za-z]:|^\//.test(p)) return p.replace(/\\/g, "/"); const cwd = resolve(process.cwd(), p).replace(/\\/g, "/"); return existsSync(cwd) || existsSync(dirname(cwd)) && !existsSync(`${VAULT}/${p}`) && !existsSync(dirname(`${VAULT}/${p}`)) ? cwd : `${VAULT}/${p}`.replace(/\\/g, "/"); };
const rel = (p) => abs(p).startsWith(VAULT + "/") ? abs(p).slice(VAULT.length + 1) : abs(p);
const sha = (s) => createHash("sha256").update(typeof s === "string" ? Buffer.from(s, "utf8") : s).digest("hex");
const today = () => new Date().toISOString().slice(0, 10);
const die = (m) => { console.error("REFUSED: " + m); process.exit(2); };
const readText = (p) => readFileSync(abs(p), "utf8");
const out = (x) => console.log(typeof x === "string" ? x : JSON.stringify(x, null, 2));

if (!cmd) die("usage: see the header of this file");

// ── The plugin's pure core (the same bundle its unit tests and tools/build-plan.mjs run) ─────────────────────────────
const CORE = `${DEV}/test/core.mjs`;
if (!existsSync(CORE)) die(`the plugin's node core is missing at ${CORE}; run \`npm run build\` in the dev folder (outside Dropbox, DIR-007)`);
const bw = await import(pathToFileURL(CORE).href);

// ── Version check (every launch, automatic) ───────────────────────────────────────────────────────────────────────────
const CAL_SRC = `${VAULT}/WORKFLOWS/skills-src/branch-writing-expert/calibration.json`;
const CAL_PATH = arg("--calibration", existsSync(CAL_SRC) ? CAL_SRC : join(HERE, "..", "calibration.json").replace(/\\/g, "/"));
const MANIFEST = abs(arg("--manifest", `${VAULT}/.obsidian/plugins/branch-writing/manifest.json`));
const SCHEMA = abs(arg("--schema", `${VAULT}/WORKFLOWS/branch-writing-schema.md`));
const semver = (v) => String(v || "0").split(".").map((x) => parseInt(x, 10) || 0);
const cmpVer = (a, b) => { const A = semver(a), B = semver(b); for (let i = 0; i < 3; i++) if ((A[i] || 0) !== (B[i] || 0)) return (A[i] || 0) < (B[i] || 0) ? -1 : 1; return 0; };
function liveVersions() {
  const live = { installed: null, devManifest: null, schemaPluginVersion: null, schemaVersion: null, schemaSha256: null, calibration: null, problems: [] };
  try { live.installed = JSON.parse(readFileSync(MANIFEST, "utf8")).version; } catch (e) { live.problems.push(`installed manifest unreadable at ${MANIFEST}: ${e.message}`); }
  try { live.devManifest = JSON.parse(readFileSync(`${DEV}/manifest.json`, "utf8")).version; } catch (e) { live.problems.push(`dev manifest unreadable: ${e.message}`); }
  try {
    const t = readFileSync(SCHEMA, "utf8");
    live.schemaSha256 = sha(t);
    const fm = /^---\r?\n([\s\S]*?)\r?\n---/.exec(t);
    const get = (k) => { const m = new RegExp(`^${k}:\\s*['"]?([^'"\\r\\n]+)`, "m").exec(fm ? fm[1] : ""); return m ? m[1].trim() : null; };
    live.schemaPluginVersion = get("plugin_version");
    live.schemaVersion = parseInt(get("schema_version") || "0", 10) || null;
  } catch (e) { live.problems.push(`schema doc unreadable at ${SCHEMA}: ${e.message}`); }
  try { live.calibration = JSON.parse(readFileSync(CAL_PATH, "utf8")); } catch (e) { live.problems.push(`calibration record unreadable at ${CAL_PATH}: ${e.message}`); }
  return live;
}
/** ok → writes allowed. newer → read what changed, then `calibrate`. breaking → read-only for this run. */
function versionStatus() {
  const L = liveVersions();
  const c = L.calibration || {};
  const r = { status: "ok", installed: L.installed, calibrated: c.plugin || null, schemaPluginVersion: L.schemaPluginVersion, schemaVersion: L.schemaVersion, schemaCalibrated: c.schemaSha256 ? c.schemaSha256.slice(0, 12) : null, schemaNow: L.schemaSha256 ? L.schemaSha256.slice(0, 12) : null, devManifest: L.devManifest, reasons: [], readFirst: [] };
  if (L.problems.length) { r.status = "breaking"; r.reasons.push(...L.problems); return r; }
  if (L.schemaVersion !== 1) { r.status = "breaking"; r.reasons.push(`the schema doc says schema_version ${L.schemaVersion}; this skill knows v1 only`); }
  if (c.schemaVersion && L.schemaVersion !== c.schemaVersion) { r.status = "breaking"; r.reasons.push(`schema_version moved from ${c.schemaVersion} to ${L.schemaVersion}`); }
  const dv = cmpVer(L.installed, c.plugin);
  if (dv < 0) { r.status = "breaking"; r.reasons.push(`the installed plugin ${L.installed} is OLDER than the calibrated ${c.plugin} (a rollback); the format this skill writes may not be read`); }
  if (dv > 0 && r.status === "ok") { r.status = "newer"; r.reasons.push(`the installed plugin is ${L.installed}, calibrated to ${c.plugin}`); r.readFirst.push(`SYSTEM/reports/2026-10-07-branch-writing-build.md: every "## <version>" section after ${c.plugin}`); }
  if (L.schemaSha256 !== c.schemaSha256 && r.status === "ok") { r.status = "newer"; r.reasons.push(`the schema doc changed since calibration (plugin_version ${L.schemaPluginVersion})`); r.readFirst.push("WORKFLOWS/branch-writing-schema.md: §1–§4, §8–§9 and every section whose plugin version is newer than the calibrated one"); }
  if (cmpVer(L.devManifest, L.installed) !== 0) { if (r.status === "ok") r.status = "newer"; r.reasons.push(`the node core is built from dev ${L.devManifest} but the installed plugin is ${L.installed}: run \`npm run build\` in the dev folder (and deploy) so both are one version`); }
  if (r.status === "newer") r.readFirst.push("then: node board_tool.mjs calibrate — only if the marker fields this skill writes (§4, §5a–§5h, §5q, §5r) read the same; otherwise stay read-only and say so");
  return r;
}
function requireWritable() {
  const v = versionStatus();
  if (v.status !== "ok") {
    console.error(`READ-ONLY this run (version check: ${v.status}). ${v.reasons.join("; ")}.`);
    for (const x of v.readFirst) console.error("  read first: " + x);
    process.exit(2);
  }
  return v;
}

// ── Boards, segments, logs ────────────────────────────────────────────────────────────────────────────────────────────
const seg = (c) => (c.rawMarker ?? "") + (c.innerRaw ?? "") + (c.rawEnd ?? "");
function loadBoard(path) {
  const text = readText(path);
  if (!bw.isBoardText(text)) die(`${rel(path)} is not a Branch Writing board (no %%bw markers)`);
  const doc = bw.parse(text);
  const roundTrip = bw.serialize(doc) === text;
  return { text, doc, roundTrip };
}
/** Byte offsets of every card segment, walked in file order (segments are located by their marker, after the preamble). */
function offsets(text, doc) {
  const res = new Map();
  let at = doc.preamble.length;
  for (const c of doc.cards) {
    const i = text.indexOf(c.rawMarker, at);
    if (i < 0) die(`internal: card ^${c.id} not located in the file text`);
    const s = seg(c);
    res.set(c.id, { start: i, end: i + s.length });
    at = i + s.length;
  }
  return res;
}
function snapshot(text, doc) {
  const m = new Map();
  doc.cards.forEach((c, i) => m.set(c.id, { text: seg(c), prev: i ? doc.cards[i - 1].id : "", idx: i, children: c.children.map((k) => k.id), parent: c.parent ? c.parent.id : "" }));
  return m;
}
/** The whitespace after the last card (the plugin's serializer may leave a blank line there after a move). */
function tailOf(text, doc) { if (!doc.cards.length) return ""; const o = offsets(text, doc); return text.slice(o.get(doc.cards[doc.cards.length - 1].id).end); }
function withTail(text, doc, tail) { if (!doc.cards.length) return text; const o = offsets(text, doc); return text.slice(0, o.get(doc.cards[doc.cards.length - 1].id).end) + (tail || "\n"); }
const logPath = (board) => `${LOG_DIR}/${basename(abs(board)).replace(/\.md$/, "")}.md`;
function readLog(board) {
  const p = logPath(board);
  if (!existsSync(p)) return { path: p, text: "", runs: [] };
  const text = readFileSync(p, "utf8");
  const runs = [];
  for (const m of text.matchAll(/```json\r?\n([\s\S]*?)\r?\n```/g)) { try { runs.push(JSON.parse(m[1])); } catch {} }
  return { path: p, text, runs };
}
function writeRun(board, run) {
  const L = readLog(board);
  mkdirSync(dirname(L.path), { recursive: true });
  let text = L.text;
  if (!text) text = `---\ntype: board-log\nboard: "${rel(board)}"\nwriter: branch-writing-expert\n---\n\n# Change log — ${basename(abs(board)).replace(/\.md$/, "")}\n\nThe branch-writing-expert skill's own record of its writes to this board: one run per section, the exact before- and after-text of every card it touched, so a run can be undone and redone byte-for-byte. The assistant reads this; CRE never has to. Edit nothing here by hand.\n`;
  text += `\n## run ${run.id} — ${run.date} — ${run.label.replace(/\n/g, " ")}\n\n\`\`\`json\n${JSON.stringify(run)}\n\`\`\`\n`;
  writeFileSync(L.path, text, "utf8");
  const back = readLog(board);
  if (!back.runs.some((r) => r.id === run.id)) die("the log entry did not read back; nothing written to the board");
  return L.path;
}
function updateRunStatus(board, id, status, extra = {}) {
  const L = readLog(board);
  let done = false;
  const text = L.text.replace(/```json\r?\n([\s\S]*?)\r?\n```/g, (m, j) => {
    let r; try { r = JSON.parse(j); } catch { return m; }
    if (r.id !== id) return m;
    done = true;
    return "```json\n" + JSON.stringify({ ...r, status, ...extra }) + "\n```";
  });
  if (!done) die(`run ${id} not in ${L.path}`);
  writeFileSync(L.path, text, "utf8");
}
const newRunId = (board) => { const L = readLog(board); return `r${L.runs.length + 1}-${today()}`; };
function safeWriteBoard(path, text) {
  writeFileSync(abs(path), text, "utf8");
  const back = readFileSync(abs(path), "utf8");
  if (back !== text) die(`${rel(path)} did not read back byte-identical after the write (left in place for inspection)`);
}
function gate(text) {
  const d = bw.parse(text);
  if (bw.serialize(d) !== text) die("parse gate: the result does not read back byte-identical through the plugin's own serializer; nothing written");
  return d;
}

// ── Resolving what CRE names ──────────────────────────────────────────────────────────────────────────────────────────
const title = (c) => (c.body || "").split("\n")[0].trim();
const norm = (s) => String(s || "").toLowerCase().replace(/\s+/g, " ").trim();
function findCardRef(doc, ref) {
  if (!ref) return null;
  const r = String(ref).trim();
  // "beat:<scene ref>:<n>" — the scene's n-th Beat (0-based): Beats a run has just made have no unique title to name them by.
  const bm = /^beat:(.+):(\d+)$/.exec(r);
  if (bm) { const sc = findCardRef(doc, bm[1]); if (!sc) return null; const lv = bw.settingsOf(doc).levels; return sc.children.filter((k) => k.meta.kind === lv[lv.length - 2].key)[Number(bm[2])] || null; }
  const byId = bw.findCard(doc, r.replace(/^\^/, ""));
  if (byId) return byId;
  const t = r.replace(/^title:/, "");
  const hits = doc.cards.filter((c) => norm(title(c)) === norm(t) && !["cast", "world", "idea", "arcbeat"].includes(c.meta.kind));
  if (hits.length === 1) return hits[0];
  if (hits.length > 1) throw new Error(`"${t}" names ${hits.length} cards; give the id (^…)`);
  return null;
}
function castRef(doc, ref) { if (!ref) return null; return bw.findCard(doc, String(ref).replace(/^\^/, "")) && bw.isCast(bw.findCard(doc, String(ref).replace(/^\^/, ""))) ? bw.findCard(doc, String(ref).replace(/^\^/, "")) : bw.findCastByName(doc, String(ref)); }
function worldRef(doc, ref) { if (!ref) return null; const c = bw.findCard(doc, String(ref).replace(/^\^/, "")); return c && bw.isWorld(c) ? c : bw.findWorldByName(doc, String(ref)); }
function eraRef(doc, ref) { if (!ref) return null; return bw.eraById(doc, String(ref)) || bw.eraByName(doc, String(ref)); }
const isContainerKind = (s, k) => { const lv = s.levels.map((l) => l.key); const i = lv.indexOf(k); if (i > 0 && i < lv.length - 1) return true; const ct = (s.customTypes || []).find((c) => c.key === k); return !!ct && ct.like !== "side" && lv.indexOf(ct.like) > 0 && lv.indexOf(ct.like) < lv.length - 1; };
const isProseKind = (s, k) => k === s.levels[s.levels.length - 1].key || (s.customTypes || []).some((c) => c.key === k && c.like === s.levels[s.levels.length - 1].key);
const sceneKey = (s) => (s.intensity && s.intensity.levels && s.intensity.levels.inner) || "scene";
const isUnitKind = (s, k) => k === sceneKey(s) || (s.customTypes || []).some((c) => c.key === k && c.like === sceneKey(s));
// Fields the author owns outright (statements, chain, outcomes) or that arrive only as offers (summary, intensity).
const NEVER_FIELDS = new Set(["goal holders", "summary", "story from", "story to", "outcome", "outcome detail", "decision", "goal", "sets goal", "reacts to", "reacts to (short)", "stakes", "opposition", "conflict", "what changed", "intensity start", "intensity end", "physical start", "physical end"]);
const NEVER_KEYS = new Set(["plotChain", "plotMarks", "plotComplete", "plotFrom", "plotBloc", "plotLine", "plotPins", "plotUntag", "plotNeeds", "plotTurnedAt", "convo", "vis", "visUnit"]);

/** A card by `^id` / `title:…`, or "beat:<scene ref>:<n>" — the scene's n-th Beat (0-based). */
function cardOrBeat(doc, s, ref) {
  const bm = /^beat:(.+):(\d+)$/.exec(String(ref || ""));
  if (!bm) return findCardRef(doc, ref) || bw.findCard(doc, String(ref || "").replace(/^\^/, ""));
  const sc = findCardRef(doc, bm[1]) || bw.findCard(doc, bm[1].replace(/^\^/, ""));
  return sc ? sc.children.filter((k) => k.meta.kind === s.levels[s.levels.length - 2].key)[Number(bm[2])] || null : null;
}
/** A source file read once per run (frontmatter skipped, CRLF normalised), its hash kept for the run's log and re-checked before the write. */
function sourceOf(path, ctx) {
  ctx.sources = ctx.sources || {};
  const p = rel(path);
  if (!ctx.sources[p]) {
    if (!existsSync(abs(path))) throw new Error(`no source file ${p}`);
    const t = readText(path);
    const { body } = bodyOf(t);
    ctx.sources[p] = { sha256: sha(t), body, blocks: bw.splitBlocks(body) };
  }
  return ctx.sources[p];
}
const sourceBlocks = (path, ctx) => sourceOf(path, ctx).blocks;
function sourceText(from, ctx) {
  if (!from || !from.source) throw new Error("from needs a source");
  const src = sourceOf(from.source, ctx);
  if (from.block != null) { const b = src.blocks[Number(from.block)]; if (b == null) throw new Error(`block ${from.block} is not in ${rel(from.source)}`); return b; }
  if (typeof from.quote === "string" && from.quote) { if (!src.body.includes(from.quote)) throw new Error(`the quote is not in ${rel(from.source)} word for word: ${JSON.stringify(from.quote.slice(0, 60))}`); return from.quote; }
  throw new Error("from needs block or quote");
}

/** Every span `text` puts in quotation marks must be his words: on this board (any card's body but arc steps, plot arcs'
 *  own fields), in `extra` strings (an entry's notes), or in a `sources` file. Throws naming the first that isn't. */
function checkQuotes(doc, ctx, text, extra, sources, label) {
  if (!text) return;
  const qn = (x) => String(x || "").replace(/[’‘]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, " ").trim().toLowerCase();
  const quotes = [...String(text).matchAll(/“([^”]+)”|"([^"]+)"/g)].map((m) => m[1] || m[2]);
  if (!quotes.length) return;
  if (!ctx.hisWords) ctx.hisWords = qn([...doc.cards.filter((k) => k.meta.kind !== "arcbeat").map((k) => k.body), ...bw.plotArcs(doc).flatMap((a) => ["goal", "stakes", "planned_outcome", "outcome_detail"].map((f) => a[f] || ""))].join("\n"));
  const more = [...(extra || []), ...(sources || []).map((p) => sourceOf(p, ctx).body)].map(qn).join("\n");
  for (const q of quotes) if (!ctx.hisWords.includes(qn(q)) && !more.includes(qn(q))) throw new Error(`${label}: the quote ${JSON.stringify(q.slice(0, 60))} is not his words on this board, in its notes${sources && sources.length ? " or in its sources" : ""}`);
}

// ── apply ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
function applyOps(doc, s, ops, made, skipped, ctx) {
  const idOf = (c) => `^${c.id}`;
  for (const [n, op] of ops.entries()) {
    const what = `${n + 1}. ${op.op}`;
    try {
      switch (op.op) {
        case "add-cast": {
          if (!op.name || !String(op.name).trim()) throw new Error("name is required");
          if (bw.findCastByName(doc, op.name)) throw new Error(`"${op.name}" is already in the cast`);
          const c = bw.addCastMember(doc, String(op.name));
          if (Array.isArray(op.aliases) && op.aliases.length) bw.setMeta(c, "aliases", op.aliases.map(String));
          for (const [k, v] of Object.entries(op.profile || {})) bw.setProfileValue(c, k, String(v));
          made.push(`cast: ${op.name}${op.aliases && op.aliases.length ? ` (${op.aliases.join(", ")})` : ""}${Object.keys(op.profile || {}).length ? " — " + Object.entries(op.profile).map(([k, v]) => `${k}: ${v}`).join("; ") : ""} ${idOf(c)}`);
          break;
        }
        case "add-alias": {
          // On his word (2026-10-21: "Dargon and Raella are both named — aliases of the black and brown hounds"): another name
          // for a cast member already on the board. Refused if another cast member already answers to it.
          const c = castRef(doc, op.cast); if (!c) throw new Error(`no cast member "${op.cast}"`);
          const al = String(op.alias || "").trim(); if (!al) throw new Error("alias is required");
          const other = bw.findCastByName(doc, al); if (other && other !== c) throw new Error(`"${al}" already names ${bw.castName(other)}`);
          const cur = bw.castAliases(c);
          if (cur.some((x) => norm(x) === norm(al))) throw new Error(`${bw.castName(c)} already has the alias "${al}"`);
          bw.setMeta(c, "aliases", [...cur, al]);
          made.push(`cast ${bw.castName(c)}: alias ${al}`);
          break;
        }
        case "set-cast": {
          const c = castRef(doc, op.cast); if (!c) throw new Error(`no cast member "${op.cast}"`);
          if (op.field === undefined) throw new Error("field is required");
          bw.setProfileValue(c, String(op.field), op.value == null ? "" : String(op.value));
          made.push(`cast ${bw.castName(c)}: ${op.field} = ${op.value}`);
          break;
        }
        case "add-era": {
          const parent = op.parent ? eraRef(doc, op.parent) : null;
          if (op.parent && !parent) throw new Error(`no era "${op.parent}" to sit inside`);
          const id = bw.addEra(doc, String(op.name), op.label ? String(op.label) : "", parent ? parent.id : "");
          if (!id) throw new Error(`era "${op.name}" not added (taken name, or no Project card)`);
          if (op.history) bw.setEraDef(doc, id, { history: true });
          made.push(`era: ${op.name}${op.label ? ` (${op.label})` : ""}${parent ? ` inside ${parent.name}` : ""}${op.history ? ", history" : ""}`);
          break;
        }
        case "set-era": {
          const c = findCardRef(doc, op.card); if (!c) throw new Error(`no card ${op.card}`);
          if (op.era === null || op.era === "") { bw.setCardEra(c, ""); made.push(`era cleared on ${title(c) || c.meta.kind} ${idOf(c)}`); break; }
          const e = eraRef(doc, op.era); if (!e) throw new Error(`no era "${op.era}"`);
          bw.setCardEra(c, e.id);
          made.push(`era ${e.name} on ${title(c) || c.meta.kind} ${idOf(c)}`);
          break;
        }
        case "file-beats-in-era": {
          const e = eraRef(doc, op.era); if (!e) throw new Error(`no era "${op.era}"`);
          let n2 = 0;
          for (const c of doc.cards) if (c.meta.kind === "arcbeat" && !c.meta.era && c.parent && c.parent.meta.kind === "project") { bw.setCardEra(c, e.id); n2++; }
          made.push(`${n2} unplaced arc steps filed in era ${e.name}`);
          break;
        }
        case "add-relation-type": {
          if (!bw.addRelationType(doc, String(op.name), op.inverse ? String(op.inverse) : "", !!op.forWorld)) throw new Error(`relation type "${op.name}" not added (taken?)`);
          made.push(`relation type: ${op.name}${op.inverse ? ` → ${op.inverse}` : ""}`);
          break;
        }
        case "add-relation": {
          const a = castRef(doc, op.a) || worldRef(doc, op.a), b = castRef(doc, op.b) || worldRef(doc, op.b);
          if (!a) throw new Error(`"${op.a}" is not on the board`); if (!b) throw new Error(`"${op.b}" is not on the board`);
          if (!bw.relationType(doc, String(op.type))) throw new Error(`relation type "${op.type}" is not on this board (its types: ${bw.relationTypes(doc).map((t) => t.name).join(", ")}); add it only on CRE's word (add-relation-type)`);
          const from = op.from ? eraRef(doc, op.from) : null, to = op.to ? eraRef(doc, op.to) : null;
          if (op.from && !from) throw new Error(`no era "${op.from}"`); if (op.to && !to) throw new Error(`no era "${op.to}"`);
          const id = bw.addRelation(doc, String(op.type), a.id, b.id, from ? from.id : "", to ? to.id : "");
          if (!id) throw new Error("relation not added (same entry twice?)");
          if (op.note) bw.updateRelation(doc, id, { note: String(op.note) });
          const nm = (c) => (bw.isCast(c) ? bw.castName(c) : bw.worldName(c));
          made.push(`relation: ${nm(a)} is ${op.type} of ${nm(b)}${from ? ` from ${from.name}` : ""}${to ? ` to ${to.name}` : ""}${op.note ? ` (${op.note})` : ""}`);
          break;
        }
        case "add-aliases": {
          // His instruction: more names for an existing cast member (kept, never removed or reordered; duplicates skipped).
          const c = castRef(doc, op.cast); if (!c) throw new Error(`no cast member "${op.cast}"`);
          const have = bw.castAliases(c).map(String);
          const add = (Array.isArray(op.aliases) ? op.aliases : [op.aliases]).map(String).filter((a) => a && !have.some((h) => h.toLowerCase() === a.toLowerCase()) && a.toLowerCase() !== bw.castName(c).toLowerCase());
          if (!add.length) throw new Error(`${bw.castName(c)} already has ${(Array.isArray(op.aliases) ? op.aliases : [op.aliases]).join(", ")}`);
          bw.setMeta(c, "aliases", [...have, ...add]);
          made.push(`cast ${bw.castName(c)}: aliases + ${add.join(", ")}`);
          break;
        }
        case "add-world": {
          if (!op.kind || !op.name) throw new Error("kind and name are required");
          if (bw.findWorldByName(doc, op.name, op.kind)) throw new Error(`"${op.name}" is already a ${op.kind}`);
          // The world walk (2026-10-22): a description is a plain line drawn from his words; any span it puts in quotation
          // marks claims to be his and must occur in the entry's own notes, this board's words or a `sources` file.
          checkQuotes(doc, ctx, (op.fields || {}).description, [(op.fields || {}).notes || ""], op.sources, `"${op.name}" description`);
          const c = bw.addWorldEntry(doc, s, String(op.kind), String(op.name));
          if (!c) throw new Error(`world kind "${op.kind}" is not on this board (kinds: ${bw.worldKinds(s).map((k) => k.key).join(", ")})`);
          if (Array.isArray(op.aliases) && op.aliases.length) bw.setMeta(c, "aliases", op.aliases.map(String));
          for (const [k, v] of Object.entries(op.fields || {})) bw.setWorldValue(c, k, String(v));
          made.push(`${op.kind}: ${op.name}${Object.keys(op.fields || {}).length ? " — " + Object.entries(op.fields).map(([k, v]) => `${k}: ${v}`).join("; ") : ""} ${idOf(c)}`);
          break;
        }
        case "set-world": {
          const c = worldRef(doc, op.entry); if (!c) throw new Error(`no world entry "${op.entry}"`);
          if (String(op.field) === "description") checkQuotes(doc, ctx, op.value, [((c.meta.fields || {}).notes) || ""], op.sources, `${bw.worldName(c)} description`);
          bw.setWorldValue(c, String(op.field), op.value == null ? "" : String(op.value));
          made.push(`${bw.worldKindOf(c)} ${bw.worldName(c)}: ${op.field} = ${op.value}`);
          break;
        }
        case "link-world": {
          // The world walk (2026-10-22): a scene (or any container) linked to a world entry it names, through the plugin's own
          // linkWorld — the entry's id goes in the card's `world` list, and the kind's field (a place → `setting`) is filled
          // when the card's level has it. Admin once the entry is approved. A field he already filled with another name is
          // kept as it was (the id link still lands), so a scene naming two places never loses its first.
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card || "").replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.card}`);
          if (!isContainerKind(s, c.meta.kind)) throw new Error(`${idOf(c)} is a ${c.meta.kind} card; link the scene (or sequence) it sits in — cards inside carry it`);
          const e = worldRef(doc, op.entry); if (!e) throw new Error(`no world entry "${op.entry}"`);
          if (bw.cardWorldIds(c).includes(e.id)) { skipped.push(`${what}: ${bw.worldName(e)} is already linked from ${idOf(c)}`); break; }
          const kd = bw.worldKindDef(s, e);
          const fld = kd && kd.field ? kd.field : "";
          const had = fld ? String((c.meta.fields || {})[fld] || "") : "";
          if (!bw.linkWorld(doc, s, c, e)) throw new Error(`${idOf(c)} could not be linked to ${bw.worldName(e)}`);
          // A card naming a place is not set there (the boy's wish for the Moon Sea is spoken in the cottage): the kind's field
          // is left exactly as it was unless the op says `fill: true` — where a scene happens is his call, not a name match.
          let note = "";
          if (fld && op.fill !== true) { if (String((c.meta.fields || {})[fld] || "") !== had) bw.setField(c, fld, had); }
          else if (fld && had.trim() && !bw.allWorldNames(e).some((n) => norm(n) === norm(had))) { bw.setField(c, fld, had); note = ` (its ${fld} stays "${had}")`; }
          else if (fld && (c.meta.fields || {})[fld] && !had.trim()) note = ` (${fld}: ${(c.meta.fields || {})[fld]})`;
          made.push(`${title(c) || c.meta.kind} ${idOf(c)} → ${bw.worldKindOf(e)} ${bw.worldName(e)}${note}`);
          break;
        }
        case "unlink-world": {
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card || "").replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.card}`);
          const e = worldRef(doc, op.entry); if (!e) throw new Error(`no world entry "${op.entry}"`);
          if (!bw.cardWorldIds(c).includes(e.id)) throw new Error(`${idOf(c)} does not link ${bw.worldName(e)}`);
          bw.unlinkWorld(doc, s, c, e);
          made.push(`${title(c) || c.meta.kind} ${idOf(c)} no longer linked to ${bw.worldName(e)}`);
          break;
        }
        case "pin-event": {
          // The world walk (2026-10-22): an existing event pinned to the card it happens on, through the plugin's pinEvent.
          // Pinning makes the event's era the card's era, so a card in another era is refused unless the ruling says the era
          // moves too (`moveEra: true`) — which era an event sits in is a story call.
          const evs = bw.eventsOf(doc);
          const ref = String(op.event || "").trim();
          let ev = evs.find((x) => x.id === ref);
          if (!ev) { const hits = evs.filter((x) => norm(bw.eventLabel(doc, x)) === norm(ref) || (x.name && norm(x.name) === norm(ref))); if (hits.length > 1) throw new Error(`"${ref}" names ${hits.length} events; give the id (evt-…)`); ev = hits[0]; }
          if (!ev) throw new Error(`no event "${ref}"`);
          const c = findCardRef(doc, op.on) || bw.findCard(doc, String(op.on || "").replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.on}`);
          if (ev.at === c.id) { skipped.push(`${what}: ${bw.eventLabel(doc, ev)} is already pinned to ${idOf(c)}`); break; }
          const cardEra = bw.eraIdAt(c);
          if (!cardEra) throw new Error(`${title(c) || c.meta.kind} ${idOf(c)} sits in no era; the plugin pins an event only to a card with one`);
          if (cardEra !== ev.era && op.moveEra !== true) throw new Error(`${title(c) || c.meta.kind} ${idOf(c)} is in ${bw.eraById(doc, cardEra)?.name || cardEra}, the event in ${bw.eraById(doc, ev.era)?.name || ev.era}; pinning moves the event's era — only on his ruling (moveEra: true)`);
          const was = ev.era;
          if (!bw.pinEvent(doc, ev.id, c)) throw new Error(`${bw.eventLabel(doc, ev)} could not be pinned`);
          made.push(`event ${bw.eventLabel(doc, ev)} pinned on ${title(c) || c.meta.kind} ${idOf(c)}${cardEra !== was ? ` (era ${bw.eraById(doc, was)?.name || was} → ${bw.eraById(doc, cardEra)?.name})` : ""}`);
          break;
        }
        case "set-parents": {
          // 2026-10-23, on his ruling only: the parents on an existing `born` event (schema §5e), through the plugin's own
          // updateEvent. Parents make the family links (parent/child, siblings, half-siblings) the board derives. Who a
          // character's parents are is a story call; `parents: []` clears them.
          const evs = bw.eventsOf(doc);
          const ref = String(op.event || "").trim();
          let ev = evs.find((x) => x.id === ref);
          if (!ev) { const hits = evs.filter((x) => norm(bw.eventLabel(doc, x)) === norm(ref) || (x.name && norm(x.name) === norm(ref))); if (hits.length > 1) throw new Error(`"${ref}" names ${hits.length} events; give the id (evt-…)`); ev = hits[0]; }
          if (!ev) throw new Error(`no event "${ref}"`);
          if (ev.type !== "born") throw new Error(`${bw.eventLabel(doc, ev)} is a "${ev.type}" event; parents go only on a born event`);
          const ps = (op.parents || []).map((r) => { const x = castRef(doc, r); if (!x) throw new Error(`parent "${r}" is not in the cast`); return x; });
          if (ps.length > 2) throw new Error("a birth names at most two parents");
          if (ps.some((x) => (ev.who || []).includes(x.id))) throw new Error("a character can't be their own parent");
          bw.updateEvent(doc, ev.id, { parents: ps.length ? ps.map((x) => x.id) : undefined });
          made.push(`parents of ${bw.eventLabel(doc, ev)}: ${ps.length ? ps.map((x) => bw.castName ? bw.castName(x) : title(x)).join(" + ") : "cleared"}`);
          break;
        }
        case "unpin-event": {
          const ev = bw.eventsOf(doc).find((x) => x.id === op.event); if (!ev) throw new Error(`no event ${op.event} (give the id)`);
          if (!ev.at) throw new Error(`${bw.eventLabel(doc, ev)} is not pinned`);
          bw.unpinEvent(doc, ev.id);
          made.push(`event ${bw.eventLabel(doc, ev)} unpinned (stays in ${bw.eraById(doc, ev.era)?.name || ev.era})`);
          break;
        }
        case "add-idea": {
          // `from: {source, block | quote}` takes the text from a file instead of the ops file, so his words are never retyped:
          // `block` is the n-th block (0-based, the plugin's own block split, frontmatter skipped), `quote` must occur in the
          // source word for word. `on` places the new idea on a card at once (a card made earlier in the same run, by title or
          // `beat:<scene>:<n>`), since the real run draws the idea's id fresh.
          let text = op.text;
          if (op.from) {
            const fromText = sourceText(op.from, ctx);
            if (op.text != null && op.text !== fromText) throw new Error("text and from disagree; give one");
            text = fromText;
          }
          if (typeof text !== "string" || !text.trim()) throw new Error("text is required (CRE's words, verbatim)");
          const types = s.ideaTypes || bw.defaultIdeaTypes();
          if (op.type && !types.includes(op.type)) throw new Error(`idea type "${op.type}" is not one of this board's (${types.join(", ")})`);
          const host = op.on ? cardOrBeat(doc, s, op.on) : null;
          if (op.on && !host) throw new Error(`no card ${op.on} to place the idea on`);
          const c = bw.addIdea(doc, text, op.type || undefined, []);
          for (const t of op.tags || []) bw.addTag(c, String(t), op.by === "cre" ? "cre" : "ai");
          if (host && !bw.placeIdea(doc, c, host)) throw new Error(`the idea could not be placed on ${op.on}`);
          made.push(`idea${op.type ? ` (${op.type})` : ""}: ${text.replace(/\s+/g, " ").slice(0, 90)}${text.length > 90 ? "…" : ""} ${idOf(c)}${host ? ` on ${title(host) || host.meta.kind} ${idOf(host)}` : ""}${op.from ? ` (from ${rel(op.from.source)})` : ""}`);
          break;
        }
        case "place-prose": {
          // His prose from a source file, block for block, as micro-beats appended under a container (a Beat, or a Scene).
          // The tool reads the words from the file (the plugin's own block split, frontmatter skipped) — the ops file names
          // only the file and the block range, never the text — and records the file's hash in the run; `skip` lists block
          // numbers inside the range that are not prose (a chapter heading, a `***` break), left off and named in the change list.
          const host = cardOrBeat(doc, s, op.under);
          if (!host) throw new Error(`no card ${op.under}`);
          if (!isContainerKind(s, host.meta.kind)) throw new Error(`${idOf(host)} is not a container; prose goes under a Beat or a Scene`);
          const blocks = sourceBlocks(op.source, ctx);
          const [a, b] = Array.isArray(op.blocks) ? (op.blocks.length === 1 ? [op.blocks[0], op.blocks[0]] : op.blocks) : [op.blocks, op.blocks];
          if (!(Number.isInteger(a) && Number.isInteger(b) && a >= 0 && b >= a && b < blocks.length)) throw new Error(`blocks ${JSON.stringify(op.blocks)} are not in ${rel(op.source)} (${blocks.length} blocks)`);
          const skip = new Set((op.skip || []).map(Number));
          const prose = s.levels[s.levels.length - 1].key;
          let n2 = 0;
          for (let i = a; i <= b; i++) {
            if (skip.has(i)) continue;
            if (headingRank(blocks[i]) && !blocks[i].includes("\n")) throw new Error(`block ${i} of ${rel(op.source)} is a heading; skip it or end the range before it`);
            const k = bw.insertChild(doc, host, { kind: prose });
            bw.setBody(k, blocks[i]);
            if (k.body !== blocks[i]) throw new Error(`internal: block ${i} did not land word for word`);
            n2++;
          }
          made.push(`${n2} micro-beat${n2 === 1 ? "" : "s"} under ${title(host) || host.meta.kind} ${idOf(host)}: blocks ${a}–${b} of ${rel(op.source)}, word for word${skip.size ? ` (left off: ${[...skip].map((i) => `block ${i} ${JSON.stringify(blocks[i].slice(0, 30))}`).join(", ")})` : ""}`);
          break;
        }
        case "place-idea": {
          const idea = bw.findFloat(doc, String(op.idea).replace(/^\^/, "")); if (!idea) throw new Error(`no idea or arc step ${op.idea}`);
          const on = findCardRef(doc, op.on) || bw.findCard(doc, String(op.on).replace(/^\^/, "")); if (!on) throw new Error(`no card ${op.on}`);
          // An idea sits on a card, never on a floating step: a target that is a step means the card that step sits on.
          let host = on; while (host && bw.isFloat(host)) host = host.parent;
          if (!host || host.meta.kind === "project") throw new Error(`${op.on} is an arc step that isn't placed on any card yet; place the step first (or name the card the idea should sit on)`);
          if (idea.parent === host) throw new Error(`${op.idea} is already on ${title(host) || host.meta.kind} ${idOf(host)}`);
          if (!bw.placeIdea(doc, idea, host)) throw new Error(`${op.idea} could not be placed on ${op.on}`);
          made.push(`placed "${title(idea) || idea.meta.label || idea.id}" on ${title(host) || host.meta.kind} ${idOf(host)}${host !== on ? ` (the card step ${idOf(on)} sits on)` : ""}`);
          break;
        }
        case "place-on-line": {
          // CRE, 2026-10-21: an arc step sits on the chain line of the beat that carries it, not loose on the scene (where the
          // plugin draws it as a Need). `via` names the card that carries it — a Beat, or a micro-beat (its Beat is used) — and
          // the step goes on the scene line that Beat is linked to (its plotFrom; the first line of a run), through the
          // plugin's own putFloatOnLine (plotLine; moved to that scene first if it sits elsewhere). Or `on` + `line` (0 = ENTRY).
          const st = bw.findCard(doc, String(op.step || "").replace(/^\^/, ""));
          if (!st || st.meta.kind !== "arcbeat") throw new Error(`no arc step ${op.step}`);
          let host, lineId;
          if (op.via) {
            let b = findCardRef(doc, op.via) || bw.findCard(doc, String(op.via).replace(/^\^/, ""));
            if (!b) throw new Error(`no card ${op.via}`);
            const beatKey = s.levels[s.levels.length - 2].key;
            while (b && b.meta.kind !== beatKey) b = b.parent && isProseKind(s, b.meta.kind) ? b.parent : null;
            if (!b) throw new Error(`${op.via} is not a Beat or a micro-beat under one`);
            const pf = typeof b.meta.plotFrom === "string" ? b.meta.plotFrom : "";
            if (!pf) throw new Error(`Beat "${title(b)}" ${idOf(b)} is linked to no line of its scene`);
            const [pid, run] = pf.split(":");
            host = bw.findCard(doc, pid);
            lineId = (run || "").split("..")[0];
          } else {
            host = findCardRef(doc, op.on);
            if (!host) throw new Error(`no card ${op.on}`);
            const ls = bw.chainLines(doc, host).filter((l) => l.id === "entry" || l.id === "exit" || /^t/.test(l.id));
            if (!ls[Number(op.line)]) throw new Error(`line ${op.line} is not in ${idOf(host)}'s chain of ${ls.length}`);
            lineId = ls[Number(op.line)].id;
          }
          if (!host || !bw.lineOrder(host).includes(lineId)) throw new Error(`line ${lineId} is not on ${host ? idOf(host) : "the card"}`);
          const from = st.parent && st.parent.meta.kind !== "project" ? st.parent : null, fromLine = st.meta.plotLine || "";
          if (from === host && fromLine === lineId) throw new Error(`${idOf(st)} is already on that line`);
          if (!bw.putFloatOnLine(doc, st.id, host.id, lineId)) throw new Error(`${idOf(st)} could not be put on ${idOf(host)}'s line`);
          const ls = bw.chainLines(doc, host).filter((l) => l.id === "entry" || l.id === "exit" || /^t/.test(l.id));
          const li = ls.findIndex((l) => l.id === lineId);
          const nm = li === 0 ? "ENTRY" : li === ls.length - 1 ? "EXIT" : (ls[li].k || "turn").toUpperCase();
          made.push(`step "${(st.meta.label || "").slice(0, 40)}" ${idOf(st)} on ${title(host)} ${idOf(host)}, line ${li + 1} (${nm})${from && from !== host ? ` — moved from ${title(from)}` : ""}${op.why ? ` · ${op.why}` : ""}`);
          break;
        }
        // ── Subplots (CRE, 2026-10-21: "the subplot beats would hit the scenes and lines like the others, so each unit holds
        //    the entirety of narrative needs - plus they are linked to larger arcs"). A subplot is a plot Arc (§5q `plotArcs`)
        //    with NO model role — only the external spine carries one — and its steps are arcbeat cards with `plotArc`.
        case "add-plot-arc": {
          if (!op.label || !String(op.label).trim()) throw new Error("label is required (his words, or a working label he rules)");
          if (bw.plotArcs(doc).some((a) => norm(a.label) === norm(op.label))) throw new Error(`a plot arc "${op.label}" is already on the board`);
          const OK = new Set(["goal", "stakes", "opposition", "conflict", "planned_outcome", "outcome_detail", "planned_change", "span", "action_type"]);
          const init = { label: String(op.label).trim() };
          for (const [k, v] of Object.entries(op.fields || {})) { if (!OK.has(k)) throw new Error(`"${k}" is not a plot-arc field this op writes (${[...OK].join(", ")})`); if (v) init[k] = String(v); }
          if (op.goalHolder) { const gh = castRef(doc, op.goalHolder); if (!gh) throw new Error(`no cast member "${op.goalHolder}"`); init.goal_holder = gh.id; }
          const a = bw.addPlotArc(doc, init);
          made.push(`plot arc "${init.label}" (${a.id}; a subplot — no model role)${init.goal_holder ? `, goal holder ${op.goalHolder}` : ""}${Object.keys(op.fields || {}).length ? " — " + Object.keys(op.fields).join(", ") : ""}`);
          break;
        }
        case "add-plot-step": {
          // A subplot step: `text` his words (or `from` a source, as add-idea), `label` where it sits; then `via` puts it on the
          // line of the Beat that carries it, `parts` makes it a parent with one sub-step per scene (each `{text, via}`, a verbatim
          // span of `text`), and with neither it waits unplaced in the Characters panel — `unplaced` says why (shown in the log).
          const arc = bw.plotArcs(doc).find((a) => a.id === op.arc || norm(a.label) === norm(op.arc));
          if (!arc) throw new Error(`no plot arc "${op.arc}"`);
          if (arc.model) throw new Error(`"${arc.label}" carries a model role; subplot steps go on a plot arc without one`);
          // `from` + `text`: the quote is checked in its source and the step carries the plain line (CRE 2026-10-22)
          const quoted = op.from ? sourceText(op.from, ctx) : null;
          const text = op.from && op.text ? String(op.text) : quoted ?? String(op.text || "");
          const st = bw.addPlotArcStep(doc, arc.id, String(op.label || ""), text);
          let where = "";
          const lineOf = (via, i) => {
            const beatKey = s.levels[s.levels.length - 2].key;
            let k = findCardRef(doc, via) || bw.findCard(doc, String(via || "").replace(/^\^/, ""));
            // a whole scene cited (a scene-level marker): its own opening line, ENTRY (CRE 2026-10-21, the held calls)
            if (k && isUnitKind(s, k.meta.kind) && bw.lineOrder(k).includes("entry")) return { host: k, line: "entry", beat: { body: "ENTRY" } };
            while (k && k.meta.kind !== beatKey) k = k.parent && isProseKind(s, k.meta.kind) ? k.parent : null;
            if (!k || typeof k.meta.plotFrom !== "string") throw new Error(`${i}: ${via} is not a Beat (or a micro-beat under one) linked to a scene line`);
            const [pid, run] = k.meta.plotFrom.split(":");
            return { host: bw.findCard(doc, pid), line: run.split("..")[0], beat: k };
          };
          if (op.parts && op.parts.length) {
            if (op.parts.length < 2) throw new Error("parts needs two or more");
            let at = 0;
            const lines = op.parts.map((p, i) => { const j = text.indexOf(p.text, at); if (!p.text || j < 0) throw new Error(`part ${i + 1} is not a span of the step's words, in order`); at = j + p.text.length; return lineOf(p.via, `part ${i + 1}`); });
            op.parts.forEach((p, i) => { const sub = bw.addPlotArcStep(doc, arc.id, String(op.label || ""), p.text, { parentStep: st.id }); if (!bw.putFloatOnLine(doc, sub.id, lines[i].host.id, lines[i].line)) throw new Error(`part ${i + 1} could not be put on its line`); });
            where = ` — ${op.parts.length} sub-steps: ${lines.map((l) => `${title(l.host)} · ${title(l.beat)}`).join("; ")} (the parent off the board, a category)`;
          } else if (op.via) {
            const l = lineOf(op.via, "via");
            if (!bw.putFloatOnLine(doc, st.id, l.host.id, l.line)) throw new Error("the step could not be put on its line");
            where = ` — on ${title(l.host)} · ${title(l.beat)}`;
          } else where = ` — unplaced${op.unplaced ? ": " + op.unplaced : ""}`;
          // `before`: an inserted step goes ahead of an existing step of the same arc (story order), moved up through the
          // plugin's own movePlotStep, which renumbers the list (CRE 2026-10-21: a step added between two in The Warning).
          if (op.before) {
            const tgt = bw.findCard(doc, String(op.before).replace(/^\^/, ""));
            if (!tgt || tgt.meta.plotArc !== arc.id || tgt.meta.parentStep) throw new Error(`${op.before} is not a top-level step of "${arc.label}"`);
            let guard = 0;
            while (st.meta.step > tgt.meta.step && guard++ < 500) if (!bw.movePlotStep(doc, st, arc.id, -1)) break;
            if (st.meta.step !== tgt.meta.step - 1) throw new Error(`the step could not be put before ${op.before}`);
            where += ` — step ${st.meta.step}, before "${(tgt.meta.label || "").slice(0, 30)}"`;
          }
          made.push(`◆ ${arc.label} step "${(op.label || "").slice(0, 30)}": ${text.replace(/\s+/g, " ").slice(0, 70)}${text.length > 70 ? "…" : ""} ${idOf(st)}${where}`);
          break;
        }
        case "split-step": {
          // CRE, 2026-10-21 ("yes, sub steps"): an arc step whose plan cell cites more than one scene becomes a parent step
          // with one sub-step per cited scene, each on the line of the Beat that carries it. Through the plugin's own
          // sub-step mechanism (addSubStep / addPlotArcStep with parentStep — §5c "Sub-steps"). Each part's words must be a
          // verbatim span of the step's own text (his words, split by its citations — never new wording), in order, not
          // overlapping. The parent keeps its whole text and label; with `unplace` it comes off the board and lives in the
          // Characters panel as a category whose checklist shows each landed sub-step (a placed parent would flag every
          // sub-step outside its card).
          const st = bw.findCard(doc, String(op.step || "").replace(/^\^/, ""));
          if (!st || st.meta.kind !== "arcbeat") throw new Error(`no arc step ${op.step}`);
          if (bw.subSteps(doc, st.id).length) throw new Error(`${idOf(st)} already has sub-steps`);
          const parts = op.parts || [];
          if (parts.length < 2) throw new Error("a split needs two or more parts");
          let at = 0;
          for (const [i, p] of parts.entries()) {
            const j = st.body.indexOf(String(p.text || ""), at);
            if (!p.text || j < 0) throw new Error(`part ${i + 1} is not the step's own words, in order: ${JSON.stringify(String(p.text).slice(0, 50))}`);
            at = j + p.text.length;
          }
          const beatKey = s.levels[s.levels.length - 2].key;
          const lines = parts.map((p, i) => {
            const b = findCardRef(doc, p.via) || bw.findCard(doc, String(p.via || "").replace(/^\^/, ""));
            // a whole scene cited (an unwritten interlude slot, no Beats yet): its own opening line, ENTRY — as add-plot-step
            // (2026-10-22, the second board audit's housekeeping)
            if (b && isUnitKind(s, b.meta.kind) && bw.lineOrder(b).includes("entry")) return { host: b, line: "entry", beat: { body: "ENTRY" } };
            let k = b; while (k && k.meta.kind !== beatKey) k = k.parent && isProseKind(s, k.meta.kind) ? k.parent : null;
            if (!k || typeof k.meta.plotFrom !== "string") throw new Error(`part ${i + 1}: ${p.via} is not a Beat linked to a scene line`);
            const [pid, run] = k.meta.plotFrom.split(":");
            return { host: bw.findCard(doc, pid), line: run.split("..")[0], beat: k };
          });
          const cast = st.meta.cast ? bw.findCard(doc, st.meta.cast) : null;
          const label = st.meta.label || "";
          const made2 = [];
          parts.forEach((p, i) => {
            const sub = st.meta.plotArc ? bw.addPlotArcStep(doc, st.meta.plotArc, label, p.text, { parentStep: st.id }) : bw.addSubStep(doc, cast, st, label, p.text);
            if (!bw.putFloatOnLine(doc, sub.id, lines[i].host.id, lines[i].line)) throw new Error(`part ${i + 1} could not be put on its line`);
            made2.push(`${i + 1}. "${p.text.slice(0, 50)}${p.text.length > 50 ? "…" : ""}" → ${title(lines[i].host)} · ${title(lines[i].beat)} ${idOf(sub)}`);
          });
          if (op.unplace && st.parent && st.parent.meta.kind !== "project") bw.unplaceIdea(doc, st);
          made.push(`step "${label.slice(0, 40)}" ${idOf(st)} split into ${parts.length} sub-steps${op.unplace ? " (the parent now off the board, a category in the Characters panel)" : ""}: ${made2.join("; ")}`);
          break;
        }
        case "unplace-idea": {
          const idea = bw.findFloat(doc, String(op.idea).replace(/^\^/, "")); if (!idea) throw new Error(`no idea or arc step ${op.idea}`);
          if (!bw.unplaceIdea(doc, idea)) throw new Error(`${op.idea} is already in the inbox`);
          made.push(`back to the inbox: "${title(idea) || idea.meta.label}"`);
          break;
        }
        case "add-tag": {
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card).replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.card}`);
          const before = bw.tagNames(c).length;
          bw.addTag(c, String(op.tag), "ai");
          if (bw.tagNames(c).length === before) { skipped.push(`${what}: ${op.tag} is already on ${idOf(c)}`); break; }
          made.push(`tag ${op.tag} (by: ai) on ${title(c) || c.meta.kind} ${idOf(c)}`);
          break;
        }
        case "remove-tag": {
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card).replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.card}`);
          const t = bw.tagsOf(c).find((x) => x.tag === op.tag); if (!t) throw new Error(`${op.tag} is not on ${idOf(c)}`);
          if (t.by !== "ai") throw new Error(`${op.tag} on ${idOf(c)} is CRE's (by: ${t.by}); never changed or removed`);
          bw.removeTag(c, String(op.tag));
          made.push(`tag ${op.tag} (by: ai) removed from ${idOf(c)}`);
          break;
        }
        case "add-link": {
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card).replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.card}`);
          let to = String(op.to);
          if (!to.startsWith("[[")) { const t = findCardRef(doc, to); if (!t) throw new Error(`no card ${to} to link to`); to = `[[#^${t.id}]]`; }
          const before = bw.linksOf(c).length;
          bw.addLink(c, to, "ai", op.rel ? String(op.rel) : undefined);
          if (bw.linksOf(c).length === before) { skipped.push(`${what}: ${to} is already linked from ${idOf(c)}`); break; }
          made.push(`link ${to}${op.rel ? ` (${op.rel})` : ""} (by: ai) on ${idOf(c)}`);
          break;
        }
        case "remove-link": {
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card).replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.card}`);
          const l = bw.linksOf(c).find((x) => x.to === op.to); if (!l) throw new Error(`${op.to} is not linked from ${idOf(c)}`);
          if (l.by !== "ai") throw new Error(`link ${op.to} on ${idOf(c)} is CRE's (by: ${l.by}); never changed or removed`);
          bw.removeLink(c, String(op.to));
          made.push(`link ${op.to} (by: ai) removed from ${idOf(c)}`);
          break;
        }
        case "set-field": {
          const c = findCardRef(doc, op.card); if (!c) throw new Error(`no card ${op.card}`);
          const f = String(op.field);
          if (NEVER_FIELDS.has(f.toLowerCase())) throw new Error(`"${f}" is the author's (a statement, outcome or summary); offer it (op "offer") or leave it`);
          if (isProseKind(s, c.meta.kind)) throw new Error(`${idOf(c)} is a prose-level card; its fields and body are CRE's`);
          bw.setField(c, f, op.value == null ? "" : String(op.value));
          made.push(`${f} = ${op.value} on ${title(c) || c.meta.kind} ${idOf(c)}`);
          break;
        }
        case "set-type": {
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card).replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.card}`);
          const allowed = bw.typesFor(s, c.meta.kind);
          if (op.type && allowed.length && !allowed.includes(op.type)) throw new Error(`type "${op.type}" is not in this level's list (${allowed.join(", ")})`);
          bw.setMeta(c, "type", op.type || undefined);
          if (op.speaker !== undefined) bw.setMeta(c, "speaker", op.speaker ? bw.castSpelling(doc, String(op.speaker)) : undefined);
          made.push(`type ${op.type || "cleared"}${op.speaker ? `, speaker ${op.speaker}` : ""} on ${idOf(c)}`);
          break;
        }
        case "add-card": {
          if (!op.kind) throw new Error("kind is required");
          if (!isContainerKind(s, op.kind)) throw new Error(`"${op.kind}" is not a container level on this board; the assistant adds containers only (never prose cards, ideas or arc steps by this op)`);
          let c;
          // `first: true` puts it ahead of the parent's other children (an interlude slot opens its chapter)
          if (op.under) { const p = findCardRef(doc, op.under); if (!p) throw new Error(`no card ${op.under}`); c = bw.insertChild(doc, p, { kind: op.kind }, !!op.first); }
          else if (op.after) { const r = findCardRef(doc, op.after); if (!r) throw new Error(`no card ${op.after}`); c = bw.insertSibling(doc, r, { kind: op.kind }, true); }
          else { const p = bw.projectCard(doc); if (!p) throw new Error("no Project card"); c = bw.insertChild(doc, p, { kind: op.kind }); }
          if (op.title) bw.setBody(c, String(op.title));
          for (const [k, v] of Object.entries(op.fields || {})) { if (NEVER_FIELDS.has(k.toLowerCase())) throw new Error(`"${k}" is the author's`); bw.setField(c, k, String(v)); }
          made.push(`${bw.kindName(s, op.kind)} "${op.title || ""}"${Object.keys(op.fields || {}).length ? " — " + Object.entries(op.fields).map(([k, v]) => `${k}: ${v}`).join("; ") : ""} ${idOf(c)}`);
          break;
        }
        case "wrap": {
          const cards = (op.cards || []).map((r) => { const c = findCardRef(doc, r) || bw.findCard(doc, String(r).replace(/^\^/, "")); if (!c) throw new Error(`no card ${r}`); return c; });
          if (!cards.length) throw new Error("cards is required");
          if (!isContainerKind(s, op.kind)) throw new Error(`"${op.kind}" is not a container level`);
          const w = bw.wrapCards(doc, cards, { kind: op.kind });
          if (!w) throw new Error("the cards could not be wrapped (not siblings?)");
          if (op.title) bw.setBody(w, String(op.title));
          for (const [k, v] of Object.entries(op.fields || {})) { if (NEVER_FIELDS.has(k.toLowerCase())) throw new Error(`"${k}" is the author's`); bw.setField(w, k, String(v)); }
          made.push(`${op.title ? `${bw.kindName(s, op.kind)} "${op.title}"` : `untitled ${bw.kindName(s, op.kind)}`} around ${cards.length} card${cards.length === 1 ? "" : "s"}, beginning "${cards[0].body.replace(/\s+/g, " ").slice(0, 50)}" ${idOf(w)}`);
          break;
        }
        case "offer": {
          // Tagging mode's by: ai offers (type, speaker, summary, wants, states, chain summary): kept under one marker key the
          // plugin preserves untouched (§4 unknown keys), never in the author's own fields. Becomes CRE's when he moves it over.
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card).replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.card}`);
          const cur = (c.meta.ai && typeof c.meta.ai === "object") ? { ...c.meta.ai } : {};
          const fields = { ...(op.offer || {}) };
          const OFFER_KEYS = new Set(["type", "speaker", "summary", "wants", "states", "chain", "tags", "note"]);
          for (const k of Object.keys(fields)) { if (NEVER_KEYS.has(k)) throw new Error(`"${k}" is never offered`); if (!OFFER_KEYS.has(k)) throw new Error(`"${k}" is not an offer key (${[...OFFER_KEYS].join(", ")})`); }
          if (!Object.keys(fields).length) throw new Error("offer needs at least one key");
          Object.assign(cur, fields, { by: "ai", offered: today() });
          bw.setMeta(c, "ai", cur);
          made.push(`offer (by: ai) on ${title(c) || c.meta.kind} ${idOf(c)}: ${Object.keys(fields).join(", ")}`);
          break;
        }
        case "offer-intensity": {
          // §6a: measured/offered intensity never sits in a marker; it goes to the board's sidecar, keyed by card id with a hash of the prose it read.
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card).replace(/^\^/, "")); if (!c) throw new Error(`no card ${op.card}`);
          ctx.sidecar = ctx.sidecar || {};
          ctx.sidecar[c.id] = { emotional: op.emotional ?? null, physical: op.physical ?? null, rubric: op.rubric || "scene-intensity", note: op.note || "", by: "ai", offered: today(), proseSha256: sha(c.body) };
          made.push(`intensity offer (sidecar) on ${title(c) || c.meta.kind} ${idOf(c)}`);
          break;
        }
        // ── The administrative levels (CRE-ruled 2026-10-19): "the prose level (micro-beats) are my words — those are hands off.
        //    But the levels above it are administrative." Beats, scenes and sequences: grouping, types, titles, summaries and
        //    chains are written here, logged and undoable; a prose card's body and marker are never touched beyond its parent.
        case "split-micro": {
          // CRE, 2026-10-19: a paragraph that fires several micro-beats becomes one card per micro-beat, at the sentence where
          // the type changes. The words are the forbidden zone: the pieces, in order, must be the card's words exactly —
          // re-joined with the whitespace between them they read back as the body, byte for byte, or nothing is split. A
          // paragraph wrapped whole in *…* (or _…_) is split inside the markers and each piece re-wrapped, so it still reads italic.
          const c = bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          if (!c) throw new Error(`no card ${op.card}`);
          if (!isProseKind(s, c.meta.kind)) throw new Error(`${idOf(c)} is not a micro-beat`);
          if (c.children.length || c.meta.convo) throw new Error(`${idOf(c)} has cards under it or is a conversation; left alone`);
          const pieces = (op.pieces || []).map((x) => ({ text: String(x.text), type: x.type || "" }));
          if (pieces.length < 2) throw new Error("a split needs two or more pieces");
          const body = c.body;
          const m = /^(\s*)([*_])(?!\2)([\s\S]*?[^\s*_])\2(\s*)$/.exec(body);
          const wrap = m ? m[2] : "";
          const inner = m ? m[3] : body;
          let at = 0;
          const gaps = [];
          for (const [i, pc] of pieces.entries()) {
            const j = inner.indexOf(pc.text, at);
            if (j < 0 || (i === 0 ? inner.slice(0, j).trim() : inner.slice(at, j).trim())) throw new Error(`piece ${i + 1} is not the next words of ${idOf(c)}: ${JSON.stringify(pc.text.slice(0, 50))}`);
            gaps.push(inner.slice(at, j));
            at = j + pc.text.length;
          }
          if (inner.slice(at).trim()) throw new Error(`the pieces leave words of ${idOf(c)} out: ${JSON.stringify(inner.slice(at).trim().slice(0, 50))}`);
          if (pieces.some((pc) => pc.text.trim() !== pc.text || !pc.text)) throw new Error("a piece starts or ends with whitespace");
          if (gaps.slice(1).some((g) => !/^\s+$/.test(g))) throw new Error("pieces must split at whitespace between sentences");
          const btypes = s.beatTypes || [];
          for (const pc of pieces) {
            if (pc.type && !btypes.includes(pc.type)) throw new Error(`"${pc.type}" is not in the board's beat types`);
            if (pc.type === "dialogue" && !/["“”«»]|(^|[\s*_(])‘/.test(pc.text)) throw new Error(`dialogue type on a piece that carries no quote marks:${JSON.stringify(pc.text.slice(0, 40))}`);
          }
          const w = (x) => (wrap ? wrap + x + wrap : x);
          const keep = c.meta.type;
          bw.setBody(c, w(pieces[0].text));
          if (pieces[0].type) bw.setMeta(c, "type", pieces[0].type);
          else if (keep === "dialogue" && !/["“”«»]|(^|[\s*_(])‘/.test(pieces[0].text)) bw.setMeta(c, "type", undefined);
          if (c.meta.speaker && c.meta.type !== "dialogue") bw.setMeta(c, "speaker", undefined);
          let prev = c;
          for (const pc of pieces.slice(1)) {
            const k = bw.insertSibling(doc, prev, { kind: c.meta.kind, ...(pc.type ? { type: pc.type } : {}) }, true);
            bw.setBody(k, w(pc.text));
            prev = k;
          }
          made.push(`split ${idOf(c)} into ${pieces.length} micro-beats: ${pieces.map((x) => x.type || "untyped").join(" → ")}`);
          break;
        }
        case "regroup-beats": {
          // A scene's micro-beats regrouped into Beats: every Beat under the scene that holds only micro-beats is dissolved (its
          // micro-beats stay in order), then each group — a run of neighbouring micro-beats, in order, covering every one —
          // is wrapped in a new Beat with its type, title and summary.
          const sc = findCardRef(doc, op.scene) || bw.findCard(doc, String(op.scene || "").replace(/^\^/, ""));
          if (!sc) throw new Error(`no card ${op.scene}`);
          if (!isUnitKind(s, sc.meta.kind)) throw new Error(`${idOf(sc)} is not a scene`);
          const beatKey = s.levels[s.levels.length - 2].key;
          for (const b of sc.children.filter((k) => k.meta.kind === beatKey)) {
            if (b.children.some((k) => !isProseKind(s, k.meta.kind))) throw new Error(`${idOf(b)} holds more than micro-beats; left alone`);
            if (b.meta.plotChain || b.meta.plotFrom) throw new Error(`${idOf(b)} has a chain; regroup it by hand`);
          }
          for (const b of sc.children.filter((k) => k.meta.kind === beatKey)) {
            for (const k of [...b.children].reverse()) bw.moveOut(doc, k);
            bw.removeCard(doc, b);
          }
          const prose = sc.children.filter((k) => isProseKind(s, k.meta.kind));
          const groups = op.groups || [];
          const flat = groups.flatMap((g) => g.cards.map((r) => String(r).replace(/^\^/, "")));
          const want = prose.map((k) => k.id);
          if (flat.length !== want.length || flat.some((id, i) => id !== want[i])) throw new Error(`the groups must cover the scene's ${want.length} micro-beats once each, in order (got ${flat.length})`);
          const btypes = bw.typesFor(s, beatKey);
          for (const g of groups) {
            const cards = g.cards.map((r) => bw.findCard(doc, String(r).replace(/^\^/, "")));
            const b = bw.wrapCards(doc, cards, { kind: beatKey });
            if (!b) throw new Error("a group could not be wrapped");
            if (g.type) { if (btypes.length && !btypes.includes(g.type)) throw new Error(`beat type "${g.type}" is not in (${btypes.join(", ")})`); bw.setMeta(b, "type", g.type); }
            if (g.title) bw.setBody(b, String(g.title).trim());
            if (g.summary) bw.setField(b, "summary", String(g.summary).trim());
            made.push(`Beat${g.type ? ` (${g.type})` : ""} "${g.title || ""}" around ${cards.length} micro-beat${cards.length === 1 ? "" : "s"} ${idOf(b)}`);
          }
          break;
        }
        case "set-title":
        case "set-summary": {
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          if (!c) throw new Error(`no card ${op.card}`);
          if (isProseKind(s, c.meta.kind) || ["project", "cast", "world", "idea", "arcbeat"].includes(c.meta.kind)) throw new Error(`${idOf(c)} is not a beat, scene or sequence`);
          const v = String(op.text == null ? "" : op.text).trim();
          if (op.op === "set-title") { if (bw.setTitle) bw.setTitle(c, v); else bw.setBody(c, v); made.push(`title "${v}" on ${idOf(c)}`); }
          else { bw.setField(c, "summary", v); made.push(`summary on ${title(c) || c.meta.kind} ${idOf(c)}: ${v.slice(0, 70)}${v.length > 70 ? "…" : ""}`); }
          break;
        }
        case "place-in-bloc": {
          // Administrative (2026-10-19): a micro-beat placed in its beat's chain slot (0 = ENTRY … the last = EXIT), through the
          // plugin's own move, which keeps the file in slot order. The words never move relative to each other when the slots
          // are filled in reading order; the run's word check is the proof.
          const m = bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          if (!m) throw new Error(`no card ${op.card}`);
          const beat = m.parent;
          if (!beat || !isProseKind(s, m.meta.kind)) throw new Error(`${idOf(m)} is not a micro-beat under a beat`);
          const pts = bw.blocPoints(beat);
          const i = Number(op.line);
          if (!(i >= 0 && i < pts.length)) throw new Error(`line ${op.line} is not in ${idOf(beat)}'s chain of ${pts.length}`);
          if (!bw.moveToBloc(doc, m, pts[i])) throw new Error(`${idOf(m)} could not be placed (does ${idOf(beat)} have a chain?)`);
          made.push(`${idOf(m)} in ${title(beat) || "beat"}'s ${i === 0 ? "ENTRY" : i === pts.length - 1 ? "EXIT" : "turn " + i}`);
          break;
        }
        case "link-from": {
          // Administrative (2026-10-19): a child card linked to the chain line — or run of lines — it carries, by position in
          // the parent's chain (0 = ENTRY, the last = EXIT). One line feeds at most one child; the child's EXIT ending is then
          // read from its run's last line (the plugin's drill rule), so the ending belongs on the parent's line.
          // `card` may also be "beat:<scene ref>:<n>" — the scene's n-th Beat (0-based), for a plan that regroups and links in one run.
          const bm = /^beat:(.+):(\d+)$/.exec(String(op.card || ""));
          const bsc = bm ? findCardRef(doc, bm[1]) || bw.findCard(doc, bm[1].replace(/^\^/, "")) : null;
          const c = bm ? (bsc ? bsc.children.filter((k) => k.meta.kind === s.levels[s.levels.length - 2].key)[Number(bm[2])] : null) : findCardRef(doc, op.card) || bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          const par = findCardRef(doc, op.parent) || bw.findCard(doc, String(op.parent || "").replace(/^\^/, ""));
          if (!c || !par) throw new Error(`no card ${!c ? op.card : op.parent}`);
          const lines = bw.chainLines(doc, par).filter((l) => l.id === "entry" || l.id === "exit" || /^t/.test(l.id));
          const [a, b] = Array.isArray(op.lines) ? (op.lines.length === 1 ? [op.lines[0], op.lines[0]] : op.lines) : [op.lines, op.lines];
          if (!(a >= 0 && b >= a && b < lines.length)) throw new Error(`lines ${JSON.stringify(op.lines)} are not in ${idOf(par)}'s chain of ${lines.length}`);
          const first = lines[a].id, last = lines[b].id;
          const claim = new Set(lines.slice(a, b + 1).map((l) => l.id));
          for (const k of doc.cards) {
            if (k === c || typeof k.meta.plotFrom !== "string") continue;
            const [pid, run] = k.meta.plotFrom.split(":");
            if (pid !== par.id) continue;
            const [f, l] = run.includes("..") ? run.split("..") : [run, run];
            const fi = lines.findIndex((x) => x.id === f), li = lines.findIndex((x) => x.id === l);
            if (lines.slice(fi, li + 1).some((x) => claim.has(x.id))) throw new Error(`${idOf(k)} already carries one of those lines`);
          }
          bw.setMeta(c, "plotFrom", `${par.id}:${first === last ? first : first + ".." + last}`);
          made.push(`${title(c) || c.meta.kind} ${idOf(c)} linked to ${title(par) || par.meta.kind}'s ${a === b ? "line " + (a + 1) : "lines " + (a + 1) + "–" + (b + 1)}`);
          break;
        }
        case "set-line": {
          // One chain line's words, in place (its id, flavor, ending and every link to it stay): `line` by position, 0 = ENTRY.
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          if (!c) throw new Error(`no card ${op.card}`);
          if (isProseKind(s, c.meta.kind)) throw new Error(`${idOf(c)} is a prose card`);
          const lines = bw.chainLines(doc, c).filter((l) => l.id === "entry" || l.id === "exit" || /^t/.test(l.id));
          const l = lines[Number(op.line)];
          if (!l) throw new Error(`line ${op.line} is not in ${idOf(c)}'s chain of ${lines.length}`);
          bw.setLinePart(doc, c, l.id, "text", String(op.text));
          made.push(`line ${Number(op.line) + 1} of ${title(c) || c.meta.kind} ${idOf(c)}: ${String(op.text).slice(0, 60)}`);
          break;
        }
        case "set-chain": {
          // ENTRY → BUT / THEREFORE turns → EXIT, replacing the card's turns; outcomes are the E3 labels.
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          if (!c) throw new Error(`no card ${op.card}`);
          // 0.71: a Part, a Book and the Project card (the series) carry chains too.
          if (isProseKind(s, c.meta.kind) || ["cast", "world", "idea", "arcbeat"].includes(c.meta.kind)) throw new Error(`${idOf(c)} is not a chain card (series, book, part, sequence, scene or beat)`);
          const OUT = ["Success", "Failure", "False Victory", "False Defeat", "Unresolved", "Disruption"];
          const chk = (o) => { if (o && !OUT.includes(o)) throw new Error(`outcome "${o}" is not one of ${OUT.join(", ")}`); };
          const K = (k) => (k === "but" || k === "therefore" ? k : "");
          for (const tn of bw.chainRec(c).turns.slice()) bw.removeTurn(c, tn.id);
          if (op.entry != null) bw.setLinePart(doc, c, "entry", "text", String(op.entry));
          for (const tn of op.turns || []) {
            const k = K(tn.k); if (!k) throw new Error('a turn needs k "but" or "therefore"');
            chk(tn.outcome);
            const id = bw.addTurn(c, k);
            if (tn.text) bw.setLinePart(doc, c, id, "text", String(tn.text));
            if (tn.outcome) bw.setLinePart(doc, c, id, "outcome", tn.outcome);
            if (tn.detail) bw.setLinePart(doc, c, id, "detail", String(tn.detail));
          }
          const ex = op.exit || {};
          chk(ex.outcome);
          bw.setExitFlavor(c, K(ex.k));
          if (ex.text != null) bw.setLinePart(doc, c, "exit", "text", String(ex.text));
          if (ex.outcome && K(ex.k) !== "therefore") bw.setLinePart(doc, c, "exit", "outcome", ex.outcome);
          if (ex.detail && K(ex.k) !== "therefore") bw.setLinePart(doc, c, "exit", "detail", String(ex.detail));
          made.push(`chain on ${title(c) || c.meta.kind} ${idOf(c)}: ENTRY → ${(op.turns || []).map((x) => x.k.toUpperCase()).join(" → ") || "—"} → EXIT${K(ex.k) ? " (" + K(ex.k).toUpperCase() + ")" : ""}${ex.outcome ? " · " + ex.outcome : ""}`);
          break;
        }
        case "replace-words": {
          // ONLY on his explicit word naming the change (2026-10-19: "please change to the woodswoman"): an exact phrase swapped
          // for the phrase he gave, on the cards he means. `count` is how many times `from` must appear on the card — any other
          // number refuses the op, so a guess about his words never lands. Never on the AI's own initiative.
          const c = bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          if (!c) throw new Error(`no card ${op.card}`);
          if (!op.from || op.to == null || !op.ruled) throw new Error('replace-words needs from, to and ruled ("<his words>")');
          const n = c.body.split(op.from).length - 1;
          if (n !== Number(op.count || 1)) throw new Error(`${idOf(c)} has "${op.from}" ${n} time(s), not ${op.count || 1}`);
          bw.setBody(c, c.body.split(op.from).join(op.to));
          made.push(`"${op.from}" → "${op.to}" on ${idOf(c)} (${n}×; CRE: ${op.ruled})`);
          break;
        }
        case "fill-step": {
          // An EMPTY arc step takes its words from his approved plan (2026-10-22, the board audit: a cell he ruled after the
          // build never reached the board). The words come from the plan record, never from the op — so nothing is typed in
          // his name — and only into a step whose body is blank and whose beat number is the cell's. A step with any text is
          // refused: changing his words is replace-words, on his explicit word.
          const c = bw.findCard(doc, String(op.step || "").replace(/^\^/, ""));
          if (!c || c.meta.kind !== "arcbeat") throw new Error(`${op.step} is not an arc step`);
          if (c.body.trim()) throw new Error(`${idOf(c)} already has words; fill-step only fills an empty step`);
          const f = op.from || {};
          if (!f.source || f.n == null || !f.spine) throw new Error("fill-step needs from: {source: <plan.md>, n, spine, set?}");
          const blocks = [...readText(f.source).matchAll(/```json\r?\n([\s\S]*?)\r?\n```/g)];
          if (!blocks.length) throw new Error(`no JSON record in ${f.source}`);
          const plan = JSON.parse(blocks[blocks.length - 1][1]);
          const pool = f.set ? ((plan.spines || []).find((x) => x.key === f.set) || {}).beats || [] : plan.beats || [];
          const cell = pool.find((b) => Number(b.n) === Number(f.n) && b.spine === f.spine && (f.sub ? b.sub === f.sub : !b.sub));
          if (!cell || !String(cell.text || "").trim()) throw new Error(`the plan has no filled cell B${f.n} ${f.spine}${f.set ? ` in set ${f.set}` : ""}`);
          if (c.meta.beat != null && Number(c.meta.beat) !== Number(f.n)) throw new Error(`${idOf(c)} is B${c.meta.beat}, not B${f.n}`);
          bw.setBody(c, String(cell.text).trim());
          made.push(`${idOf(c)} filled from the plan's B${f.n} ${f.spine}${f.set ? ` (${f.set})` : ""}: "${String(cell.text).trim().slice(0, 80)}"`);
          break;
        }
        case "set-step-text": {
          // Administrative (CRE 2026-10-22: "Sometimes a summary is better than a quote, because their job is to tell me what
          // something is, not to stand as my prose"; "if a quote is key, it should stay as my words, but its context needs
          // inclusion"). An arc step's or sub-step's text becomes a plain line saying what happens there. `was` must be the
          // step's current text (a moved board refuses). Any span the new text puts in quotation marks claims to be his words:
          // it must occur word for word in his prose, ideas or arc fields on this board, or in a `sources` file — never typed
          // in his name. Markers (held —, audit —, …) are not steps and are refused. Undo restores the old text from the log.
          const c = bw.findCard(doc, String(op.step || "").replace(/^\^/, ""));
          if (!c || c.meta.kind !== "arcbeat") throw new Error(`${op.step} is not an arc step`);
          const qn = (x) => String(x || "").replace(/[’‘]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, " ").trim().toLowerCase();
          if (op.was == null || qn(op.was) !== qn(c.body)) throw new Error(`${idOf(c)}: was ≠ its current text (${JSON.stringify(c.body.trim().slice(0, 60))}); read the board again`);
          const isMark = /^(held|audit|body|hermit|bond|adage|keep-dark|sources disagree)\b/i.test(c.body.trim()) || /^(held|audit|body|hermit|bond|adage)\s+—/i.test(c.meta.label || "");
          const text = String(op.text || "").trim();
          if (!text) throw new Error("set-step-text needs text");
          // A ruling marker's text (2026-10-22: "audit —" rulings lead with the ruling, not the raw chat) only with `marker:
          // true`, keeping its prefix up to the first colon so the marker family still reads; its quotes may come from its
          // own old text (his chat words), which the plan keeps in full.
          if (isMark && !op.marker) throw new Error(`${idOf(c)} is a redraft marker, not a step (marker: true rewrites a ruling's text)`);
          if (isMark) { const b0 = c.body.trim(); const pre = b0.includes(":") ? b0.split(":")[0] + ":" : b0.split(/\s+—\s+/)[0] + " —"; if (!text.startsWith(pre)) throw new Error(`${idOf(c)}: a marker keeps its prefix "${pre}"`); }
          const quotes = [...text.matchAll(/“([^”]+)”|"([^"]+)"/g)].map((m) => m[1] || m[2]);
          if (quotes.length) {
            if (!ctx.hisWords) ctx.hisWords = qn([...doc.cards.filter((k) => k.meta.kind !== "arcbeat").map((k) => k.body), ...bw.plotArcs(doc).flatMap((a) => ["goal", "stakes", "planned_outcome", "outcome_detail"].map((f) => a[f] || ""))].join("\n"));
            // a subplot step's old text was his words by the old rule (a DEV ruling or his prose), so it may be quoted too
            const sub = !!c.meta.plotArc && !(bw.plotArcs(doc).find((a) => a.id === c.meta.plotArc) || {}).model;
            const extra = (op.sources || []).map((p) => qn(sourceOf(p, ctx).body)).join("\n") + (isMark || sub ? "\n" + qn(c.body) : "");
            for (const q of quotes) if (!ctx.hisWords.includes(qn(q)) && !extra.includes(qn(q))) throw new Error(`${idOf(c)}: the quote ${JSON.stringify(q.slice(0, 60))} is not his words on this board${op.sources ? " or in its sources" : ""}`);
          }
          bw.setBody(c, text);
          made.push(`${idOf(c)} "${(c.meta.label || "").slice(0, 30)}": ${text.slice(0, 90)}${text.length > 90 ? "…" : ""}`);
          break;
        }
        case "set-arc-text": {
          // Administrative, on his ruling (CRE 2026-10-22: a subplot goal written as a line "becomes the arc's motto with the
          // goal stated plainly beside it"): one text field of a plot Arc rewritten as a plain line, through the plugin's
          // setPlotArc. `was` must be the field's current value; quoted spans must be his words — the old value or this
          // board's prose — so the motto stays his line exactly.
          const FIELDS = ["goal", "stakes", "planned_outcome", "outcome_detail", "planned_change", "opposition", "conflict"];
          const qn = (x) => String(x || "").replace(/[’‘]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, " ").trim().toLowerCase();
          const a = bw.plotArcs(doc).find((x) => x.id === op.arc || qn(x.label) === qn(op.arc));
          if (!a) throw new Error(`no plot arc "${op.arc}"`);
          if (!FIELDS.includes(op.field)) throw new Error(`field must be one of ${FIELDS.join(", ")}`);
          if (op.was == null || qn(op.was) !== qn(a[op.field])) throw new Error(`"${a.label}" ${op.field} ≠ was; read the board again`);
          const text = String(op.text || "").trim();
          if (!text) throw new Error("set-arc-text needs text");
          if (!ctx.hisWords) ctx.hisWords = qn([...doc.cards.filter((k) => k.meta.kind !== "arcbeat").map((k) => k.body), ...bw.plotArcs(doc).flatMap((x) => ["goal", "stakes", "planned_outcome", "outcome_detail"].map((f) => x[f] || ""))].join("\n"));
          for (const m of text.matchAll(/“([^”]+)”|"([^"]+)"/g)) { const q = m[1] || m[2]; if (!ctx.hisWords.includes(qn(q))) throw new Error(`"${a.label}": the quote ${JSON.stringify(q.slice(0, 60))} is not his words on this board`); }
          bw.setPlotArc(doc, a.id, op.field, text);
          made.push(`"${a.label}" ${op.field.replace("_", " ")}: ${text.slice(0, 100)}`);
          break;
        }
        case "replace-arc-words": {
          // replace-words for a plot Arc's own fields (2026-10-22: "the dead withdraw" for Assimilation's planned outcome).
          // ONLY on his explicit word naming the change: an exact phrase swapped in one text field of one plot Arc, through the
          // plugin's setPlotArc. `count` must match, as in replace-words. Never the chain, marks or anything structural.
          const FIELDS = ["goal", "stakes", "planned_outcome", "outcome_detail", "planned_change", "opposition", "conflict", "span"];
          const norm = (x) => String(x || "").trim().toLowerCase();
          const a = bw.plotArcs(doc).find((x) => x.id === op.arc || norm(x.label) === norm(op.arc));
          if (!a) throw new Error(`no plot arc "${op.arc}"`);
          if (!FIELDS.includes(op.field)) throw new Error(`field must be one of ${FIELDS.join(", ")}`);
          if (!op.from || op.to == null || !op.ruled) throw new Error('replace-arc-words needs from, to and ruled ("<his words>")');
          const v = String(a[op.field] || "");
          const n = v.split(op.from).length - 1;
          if (n !== Number(op.count || 1)) throw new Error(`"${a.label}" ${op.field} has "${op.from}" ${n} time(s), not ${op.count || 1}`);
          bw.setPlotArc(doc, a.id, op.field, v.split(op.from).join(op.to));
          made.push(`"${op.from}" → "${op.to}" in "${a.label}" ${op.field.replace("_", " ")} (${n}×; CRE: ${op.ruled})`);
          break;
        }
        case "move-step": {
          // On his word (2026-10-22: "Step renumbering (two swaps)"): a step moves one place up or down among its siblings in
          // its arc, through the plugin's own Plot-tab move (moveStep / movePlotStep), which renumbers the list. Words untouched.
          const c = bw.findCard(doc, String(op.step || "").replace(/^\^/, ""));
          if (!c || c.meta.kind !== "arcbeat") throw new Error(`${op.step} is not an arc step`);
          const dir = Number(op.dir);
          if (dir !== -1 && dir !== 1) throw new Error("move-step needs dir: -1 (up) or 1 (down)");
          const was = c.meta.step;
          const ok = c.meta.plotArc ? bw.movePlotStep(doc, c, c.meta.plotArc, dir) : bw.moveStep(doc, c, dir);
          if (!ok) throw new Error(`${idOf(c)} cannot move ${dir < 0 ? "up" : "down"} (end of its list)`);
          made.push(`step ${idOf(c)}${c.meta.label ? ` "${c.meta.label}"` : ""}: s${was} → s${c.meta.step}`);
          break;
        }
        case "remove-empty-card": {
          // On his word (2026-10-21: a Beat built from a stale DEV beat its neighbour carries): a Beat or Scene with nothing
          // under it — no micro-beat, idea, arc step or card — and nothing linking to it is taken off the board. The log keeps
          // its text; undo puts it back. A card with anything under it, or one another card points at, is refused.
          const c = findCardRef(doc, op.card);
          if (!c) throw new Error(`no card ${op.card}`);
          // 2026-10-23, on his word ("remove the empty micro-beat under All her fault"): a micro-beat qualifies only when it holds
          // nothing at all — no words, type, speaker, tags, links or fields (an accidental Write click). Any word on it refuses.
          const emptyMicro = c.meta.kind === "micro" && !String(c.body || "").trim() && !c.meta.type && !c.meta.speaker && !(c.meta.tags || []).length && !bw.linksOf(c).length && !Object.keys(c.meta.fields || {}).length;
          if (c.meta.kind === "micro" && !emptyMicro) throw new Error(`${idOf(c)} is a micro-beat with something on it (words, a type, tags, links or fields); his card, left alone`);
          if (!emptyMicro && (!isContainerKind(s, c.meta.kind) || ["part", "sequence"].includes(c.meta.kind) && c.children.length)) throw new Error(`${idOf(c)} is not an empty container`);
          if (c.children.length) throw new Error(`${idOf(c)} has ${c.children.length} card(s) under it; left alone`);
          const pointing = doc.cards.filter((k) => k !== c && (String(k.meta.plotFrom || "").startsWith(c.id + ":") || bw.linksOf(k).some((l) => String(l.to).includes(c.id))));
          if (pointing.length) throw new Error(`${idOf(c)} is linked from ${pointing.map(idOf).join(", ")}; left alone`);
          const t = title(c) || c.meta.kind;
          bw.removeCard(doc, c);
          made.push(`removed the empty ${bw.kindName(s, c.meta.kind)} "${t}" ${idOf(c)} (nothing under it; undo restores it)`);
          break;
        }
        case "remove-duplicate-idea": {
          // On his word only (2026-10-22, the second audit: "remove dulpicates - no clutter"): an idea card whose text is
          // byte-identical (trimmed) to a `twin` idea in the same scene comes off the board; the twin keeps his words. Refused
          // when the texts differ by a single character, the two sit in different scenes, or the idea carries tags, links or
          // children. The log keeps its text; undo puts it back.
          const c = bw.findCard(doc, String(op.idea || "").replace(/^\^/, ""));
          const tw = bw.findCard(doc, String(op.twin || "").replace(/^\^/, ""));
          if (!c || c.meta.kind !== "idea") throw new Error(`no idea card ${op.idea}`);
          if (!tw || tw.meta.kind !== "idea" || tw === c) throw new Error(`no twin idea card ${op.twin}`);
          if ((c.body || "").trim() !== (tw.body || "").trim()) throw new Error(`${idOf(c)} and ${idOf(tw)} differ in their words; left alone`);
          const sceneOf = (k) => { let x = k.parent; while (x && x.meta.kind !== "scene") x = x.parent; return x; };
          if (!sceneOf(c) || sceneOf(c) !== sceneOf(tw)) throw new Error(`${idOf(c)} and ${idOf(tw)} are not in the same scene; left alone`);
          // nothing may be lost with it: every tag and link it carries must also be on the twin
          const lost = bw.tagNames(c).filter((g) => !bw.tagNames(tw).includes(g))
            .concat(bw.linksOf(c).filter((l) => !bw.linksOf(tw).some((m) => String(m.to) === String(l.to))).map((l) => "link " + l.to));
          if (c.children.length || lost.length) throw new Error(`${idOf(c)} carries ${c.children.length ? "cards" : lost.join(", ")} its twin doesn't; left alone`);
          const pointing = doc.cards.filter((k) => k !== c && bw.linksOf(k).some((l) => String(l.to).includes(c.id)));
          if (pointing.length) throw new Error(`${idOf(c)} is linked from ${pointing.map(idOf).join(", ")}; left alone`);
          const on = c.parent;
          bw.removeCard(doc, c);
          made.push(`removed the duplicate idea "${title(c).slice(0, 50)}" ${idOf(c)} from ${title(on)} ${idOf(on)} — its twin ${idOf(tw)} stays on ${title(tw.parent)}`);
          break;
        }
        case "remove-break-card": {
          // On his word only (2026-10-19): a scene-break card the import kept word for word ("***"), once the Scenes around it
          // export their own break. Refused for anything else: never a card with words, children or keys of its own.
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          if (!c) throw new Error(`no card ${op.card}`);
          if (!isProseKind(s, c.meta.kind) || !/^\s*(\*\s*\*\s*\*|\*{3,}|-{3,}|_{3,}|~{3,}|#\s*#\s*#|§)\s*$/.test(c.body)) throw new Error(`${idOf(c)} is not a scene-break card`);
          if (c.children.length || Object.keys(c.meta).some((k) => !["v", "kind", "depth"].includes(k))) throw new Error(`${idOf(c)} carries more than the break; left alone`);
          bw.removeCard(doc, c);
          made.push(`scene-break card "${c.body.trim()}" ${idOf(c)} removed`);
          break;
        }
        case "rename-spine-set": {
          // On his word (2026-10-22, "rename it"): a spine set's display name in the board's model settings — its pill tag is
          // derived from the name (arcid.ts setTag). The key never changes (steps, roles and the plan key off it); arc names
          // built from the old set name stay as they are (display text, not a key).
          const pc = bw.projectCard(doc); if (!pc) throw new Error("no Project card");
          const st = JSON.parse(JSON.stringify(pc.meta.settings || {}));
          const set = ((st.model || {}).sets || []).find((x) => x.key === op.key);
          if (!set) throw new Error(`no spine set "${op.key}" in the board's model`);
          if (!op.name || !String(op.name).trim()) throw new Error("name is required");
          if (set.name === op.name) { skipped.push(`set ${op.key} is already named "${op.name}"`); break; }
          const was = set.name; set.name = String(op.name);
          bw.setMeta(pc, "settings", st);
          made.push(`spine set ${op.key}: "${was}" → "${set.name}"${typeof bw.setTag === "function" ? ` (pill tag ${bw.setTag(set.name)})` : ""}`);
          break;
        }
        case "set-era-source": {
          // On his word (plugin 0.64): this board's eras come from its scenes (on) or from its sequences as before (off).
          const pc = bw.projectCard(doc); if (!pc) throw new Error("no Project card");
          const st = JSON.parse(JSON.stringify(pc.meta.settings || {}));
          const was = st.eraSource === "scene";
          if (was === !!op.on) { skipped.push(`eras already ${was ? "from scenes" : "from sequences"}`); break; }
          if (op.on) st.eraSource = "scene"; else delete st.eraSource;
          bw.setMeta(pc, "settings", st);
          made.push(`eras now come from ${op.on ? "scenes" : "sequences"}`);
          break;
        }
        case "set-flashback": {
          // A scene marked a flashback (its era applies to it only) — a story call: on his word or an approved proposal.
          const c = findCardRef(doc, op.card) || bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          if (!c || !isUnitKind(s, c.meta.kind)) throw new Error(`${op.card} is not a scene`);
          bw.setFlashback(c, op.on !== false);
          made.push(`${title(c) || "scene"} ${idOf(c)} ${op.on !== false ? "is a flashback" : "is not a flashback"}`);
          break;
        }
        case "set-remembers": {
          // A memory micro-beat's era ("" = not known). The card must already be typed memory.
          const c = bw.findCard(doc, String(op.card || "").replace(/^\^/, ""));
          if (!c || c.meta.type !== bw.MEMORY_TYPE) throw new Error(`${op.card} is not a memory micro-beat`);
          const e = op.era ? eraRef(doc, op.era) : null;
          if (op.era && !e) throw new Error(`no era ${op.era}`);
          bw.setRemembers(c, e ? e.id : "");
          made.push(`${idOf(c)} remembers ${e ? e.name : "(not known)"}`);
          break;
        }
        case "add-beat-type": {
          // A micro-beat type added to the board's list (e.g. "memory", plugin 0.64), on his word.
          const pc = bw.projectCard(doc); if (!pc) throw new Error("no Project card");
          const st = JSON.parse(JSON.stringify(pc.meta.settings || {}));
          const list = Array.isArray(st.beatTypes) ? st.beatTypes : [...s.beatTypes];
          const name = String(op.name || "").trim();
          if (!name) throw new Error("name is required");
          if (list.includes(name)) { skipped.push(`"${name}" is already a type`); break; }
          st.beatTypes = [...list, name];
          bw.setMeta(pc, "settings", st);
          s.beatTypes = st.beatTypes; // later ops in this run see the new type
          made.push(`micro-beat type "${name}" added`);
          break;
        }
        case "set-tag-mode": {
          // On his word only: how the export adds dialogue tags ("never" for prose written with its own tags; plugin 0.63).
          if (!["never", "first", "every"].includes(op.mode)) throw new Error('mode is "never", "first" or "every"');
          const pc = bw.projectCard(doc); if (!pc) throw new Error("no Project card");
          const st = JSON.parse(JSON.stringify(pc.meta.settings || {}));
          const was = (st.dialogue && st.dialogue.mode) || "first";
          if (was === op.mode) { skipped.push(`dialogue tags already "${op.mode}"`); break; }
          st.dialogue = { ...(st.dialogue || {}), mode: op.mode };
          bw.setMeta(pc, "settings", st);
          made.push(`dialogue tags "${was}" → "${op.mode}"`);
          break;
        }
        case "add-book-level": {
          // 0.71 (CRE 2026-10-23, "isn't the chain series -> books -> parts" … "yes"): the plugin's own "Add Book level…" —
          // every story card under the Project card moves into one new Book card, in order; text and export unchanged. Once per
          // board, on his word only. `title` names the Book (default "Book 1").
          const b = bw.addBookLevel(doc);
          if (!b) throw new Error("the board already has a Book level (or no Project card)");
          if (op.title) bw.setBody(b, String(op.title).trim());
          made.push(`Book level added: "${(b.body.split(String.fromCharCode(10))[0] || "").trim()}" ${idOf(b)} holds the story`);
          break;
        }
        case "set-plotting": {
          if (op.on === false) { bw.disablePlotting(doc); made.push("Statement Plotting off"); break; }
          const added = bw.enablePlotting(doc);
          made.push(`Statement Plotting on${added.length ? ` (${added.length} fields added)` : ""}`);
          break;
        }
        case "set-arc-role": {
          // 0.65.1 (2026-10-20): the Interlocking Arc Model role an existing arc carries — `role` null clears it; `set` names a
          // spine set (0.65). On CRE's word or his ruling only (which arc carries which spine is his call); the builder never
          // reassigns an arc itself, and an arc holding a role in a set blocks that set's template arc on a copy build.
          const c = castRef(doc, op.cast); if (!c) throw new Error(`no cast member "${op.cast}"`);
          const arc = bw.arcsOf(c).find((a) => a.name === op.arc || a.id === op.arc); if (!arc) throw new Error(`no arc "${op.arc}" on ${bw.castName(c)}`);
          const role = op.role == null ? null : String(op.role);
          if (role !== null && typeof bw.isIamRole === "function" && !bw.isIamRole(role)) throw new Error(`"${role}" is not a model role`);
          const against = op.against ? castRef(doc, op.against) : null; if (op.against && !against) throw new Error(`no cast member "${op.against}" to face`);
          bw.setArcRole(c, arc.id, role, against ? against.id : undefined, op.set ? String(op.set) : undefined);
          made.push(`arc "${arc.name}" of ${bw.castName(c)}: model role ${role === null ? "cleared" : role + (op.set ? ` (set ${op.set})` : " (main set)") + (against ? ", facing " + bw.castName(against) : "")}`);
          break;
        }
        case "add-lead": {
          const c = castRef(doc, op.cast); if (!c) throw new Error(`no cast member "${op.cast}"`);
          if (!bw.plottingOn(bw.settingsOf(doc))) throw new Error("Statement Plotting is off on this board (set-plotting first, on CRE's word)");
          bw.addLead(doc, c.id);
          made.push(`POV lead: ${bw.castName(c)}`);
          break;
        }
        case "set-lead-exit": {
          const c = castRef(doc, op.cast); if (!c) throw new Error(`no cast member "${op.cast}"`);
          if (op.unit === null || op.unit === "") { bw.setLeadExit(doc, c.id, null); made.push(`${bw.castName(c)} stays to the end`); break; }
          const u = findCardRef(doc, op.unit); if (!u) throw new Error(`no card ${op.unit}`);
          const s2 = bw.settingsOf(doc);
          if (isUnitKind(s2, u.meta.kind)) { bw.setLeadExit(doc, c.id, u.id); made.push(`lead exit: ${bw.castName(c)} after ${title(u)} ${idOf(u)}`); break; }
          // Since plugin 0.62.2 an exit stored on a sequence (or a chapter, part, book) reads at the last unit inside it
          // (exitUnitId). An older core has no exitUnitId and honours units only, so the refusal stays for it.
          if (typeof bw.exitUnitId !== "function" || !isContainerKind(s2, u.meta.kind)) throw new Error(`${idOf(u)} is a ${bw.kindName(s2, u.meta.kind)}; this plugin build honours a lead exit only on a unit (a ${bw.kindName(s2, sceneKey(s2))}-level card)${typeof bw.exitUnitId !== "function" ? " — 0.62.2 adds containers" : ""}. Name the unit where ${bw.castName(c)} leaves`);
          bw.setLeadExit(doc, c.id, u.id);
          const at = bw.exitUnitId(bw.plotModel(doc), u.id);
          if (at) made.push(`lead exit: ${bw.castName(c)} after ${title(u)} ${idOf(u)} (reads at its last ${bw.kindName(s2, sceneKey(s2))}, ${title(bw.findCard(doc, at))} ^${at})`);
          else { made.push(`lead exit: ${bw.castName(c)} after ${title(u)} ${idOf(u)}`); skipped.push(`${what}: ${title(u)} has no ${bw.kindName(s2, sceneKey(s2))} under it yet, so ${bw.castName(c)}'s exit reads "stays to the end" until one is added (stored; nothing to undo by hand)`); }
          break;
        }
        case "add-event": {
          // An event on CRE's instruction (schema §5e/§5i): {type, who, era, parents?, at?, name?, until?}. Everything is
          // checked before anything is written, so a refused op leaves the board as it was. Stored on the Project card, so the
          // run log's segment record makes undo byte-exact like every other op.
          if (!op.type) throw new Error("type is required (born, died, married, separated, built, destroyed, or one of the board's own)");
          const t = bw.eventType(doc, String(op.type));
          if (!t) throw new Error(`event type "${op.type}" is not on this board (its types: ${bw.eventTypes(doc).map((x) => x.name).join(", ")}); a new type is added only on CRE's word`);
          const eraOf = (ref) => { if (!ref) return null; const e = eraRef(doc, ref); if (e) return e; const hits = bw.erasOf(doc).filter((x) => x.label && norm(x.label) === norm(String(ref))); return hits.length === 1 ? hits[0] : null; };
          if (!op.era && !op.at) throw new Error("era is required (an event belongs to an era), or at: the card it happens on");
          const e = op.era ? eraOf(op.era) : null;
          if (op.era && !e) throw new Error(`no era "${op.era}" on this board (eras: ${bw.erasOf(doc).map((x) => x.name + (x.label ? ` (${x.label})` : "")).join(", ") || "none"}); add it only on CRE's word (add-era)`);
          const who = (Array.isArray(op.who) ? op.who : op.who ? [op.who] : []).map((r) => {
            const x = t.for === "world" ? worldRef(doc, r) : t.for === "cast" ? castRef(doc, r) : castRef(doc, r) || worldRef(doc, r);
            if (!x) throw new Error(`"${r}" is not ${t.for === "world" ? "a world entry" : t.for === "cast" ? "in the cast" : "on the board"} (a "${t.name}" event is about ${t.for === "world" ? "places and things" : t.for === "cast" ? "characters" : "anyone"})`);
            return x;
          });
          if (who.length > t.people) throw new Error(`"${t.name}" is about ${t.people === 0 ? "nobody in particular" : t.people === 1 ? "one subject" : "two people"}; ${who.length} named`);
          const parents = (op.parents || []).map((r) => { const x = castRef(doc, r); if (!x) throw new Error(`parent "${r}" is not in the cast`); return x; });
          if (parents.length && t.name !== "born") throw new Error("parents go only on a born event");
          if (parents.length > 2) throw new Error("a birth names at most two parents");
          const until = op.until ? eraOf(op.until) : null;
          if (op.until && !until) throw new Error(`no era "${op.until}" for until`);
          let atCard = null;
          if (op.at) {
            atCard = findCardRef(doc, op.at); if (!atCard) throw new Error(`no card ${op.at}`);
            const cardEra = bw.eraIdAt(atCard);
            if (!cardEra) throw new Error(`${title(atCard) || atCard.meta.kind} ^${atCard.id} sits in no era, and the plugin pins an event only to a card with one; set its era first (on CRE's word), or leave at off`);
            if (e && cardEra !== e.id) throw new Error(`${title(atCard) || atCard.meta.kind} ^${atCard.id} is in era ${bw.eraById(doc, cardEra)?.name || cardEra}, not ${e.name}; pinning takes the card's era, so name one or the other`);
          }
          const eraId = e ? e.id : bw.eraIdAt(atCard);
          const id = bw.addEvent(doc, t.name, eraId, who.map((x) => x.id), parents.map((x) => x.id));
          if (!id) throw new Error("event not added (no Project card?)");
          if (atCard) bw.pinEvent(doc, id, atCard);
          const patch = {};
          if (op.name && String(op.name).trim()) patch.name = String(op.name);
          if (until) patch.until = until.id;
          if (Object.keys(patch).length) bw.updateEvent(doc, id, patch);
          const ev = bw.eventById(doc, id);
          made.push(`event: ${bw.eventLabel(doc, ev)} in ${bw.eraById(doc, ev.era)?.name || ev.era}${until ? ` until ${until.name}` : ""}${parents.length ? `, parents ${parents.map((x) => bw.castName(x)).join(" & ")}` : ""}${atCard ? `, on ${title(atCard)} ^${atCard.id}` : ""}${who.length < t.people ? ` (${who.length} of ${t.people} named)` : ""} [${id}]`);
          break;
        }
        case "mark-working-copy": {
          ctx.preamble = (pre) => {
            const lines = [`bw-working-copy: true`, `bw-source: "${String(op.source || "").replace(/"/g, "'")}"`, `bw-authority: "the pipeline's drafts, until ^backlog-branch-writing-replacement-review rules"`];
            const m = /^---\r?\n([\s\S]*?)\r?\n---[ \t]*(\r?\n|$)/.exec(pre);
            if (!m) return `---\n${lines.join("\n")}\n---\n` + pre;
            const body = (m[1] || "").split(/\r?\n/).filter((l) => !/^bw-(working-copy|source|authority):/.test(l));
            return `---\n${[...body, ...lines].join("\n")}\n---\n` + pre.slice(m[0].length);
          };
          made.push(`marked a working copy of ${op.source || "?"} (frontmatter)`);
          break;
        }
        default:
          throw new Error(`unknown op "${op.op}" (see references/ops.md)`);
      }
    } catch (e) {
      skipped.push(`${what}: ${e.message}`);
    }
  }
}

function cmdApply() {
  const opsPath = positional[1]; if (!opsPath) die("apply <ops.json>");
  let spec; try { spec = JSON.parse(readText(opsPath)); } catch (e) { die(`${opsPath} is not JSON: ${e.message}`); }
  if (!spec.board) die("the ops file needs \"board\"");
  if (!Array.isArray(spec.ops) || !spec.ops.length) die("the ops file needs a non-empty \"ops\" list");
  const DRY = flag("--dry");
  if (!DRY) requireWritable(); else { const v = versionStatus(); if (v.status !== "ok") console.log(`note: version check ${v.status} — a real run would be read-only (${v.reasons.join("; ")})`); }
  const board = abs(spec.board);
  // The ops file names its board; a `--board` that names another one is refused, never silently overridden either way
  // (2026-10-22, ^obs-474: a "scratch copy" test wrote the live board because the ops file named it).
  if (arg("--board")) {
    const same = (p) => { const x = resolve(abs(p)).replace(/\\/g, "/"); return process.platform === "win32" ? x.toLowerCase() : x; };
    if (same(arg("--board")) !== same(spec.board)) die(`--board ${rel(abs(arg("--board")))} is not the ops file's board ${rel(board)}: nothing written. For a scratch test, write an ops file whose "board" is the scratch copy`);
  }
  const { text, doc, roundTrip } = loadBoard(board);
  if (!roundTrip) die(`${rel(board)} does not round-trip through the plugin's serializer (a hand edit, or a file saved by an older version): a write would alter bytes outside the run. Open and save it once in Obsidian, or run \`normalize\` as its own logged run first`);
  const s = bw.settingsOf(doc);
  const before = snapshot(text, doc);
  const beforeTail = tailOf(text, doc); // measured before any op mutates the parsed document
  const made = [], skipped = [], ctx = {};
  applyOps(doc, s, spec.ops, made, skipped, ctx);
  let textNew = bw.serialize(doc);
  if (ctx.preamble) { const d2 = bw.parse(textNew); const pre2 = ctx.preamble(d2.preamble); textNew = pre2 + textNew.slice(d2.preamble.length); }
  const docNew = gate(textNew);
  const after = snapshot(textNew, docNew);
  const records = [];
  for (const [id, b] of before) { const a = after.get(id); if (!a) records.push({ id, before: b, after: null }); else if (a.text !== b.text || a.prev !== b.prev || (a.parent || "") !== (b.parent || "")) records.push({ id, before: b, after: a }); }
  for (const [id, a] of after) if (!before.has(id)) records.push({ id, before: null, after: a });
  const preChanged = bw.parse(textNew).preamble !== doc.preamble;
  const changed = records.length > 0 || preChanged || !!ctx.sidecar;
  console.log(`${DRY ? "DRY RUN — nothing written" : "run"}: ${rel(board)} — ${spec.label || "(no label)"}`);
  for (const m of made) console.log("  made: " + m);
  for (const x of skipped) console.log("  NOT DONE: " + x);
  if (!changed) { console.log("  nothing changed on the board"); process.exit(skipped.length ? 3 : 0); }
  console.log(`  cards touched: ${records.length} (${records.filter((r) => !r.before).length} added, ${records.filter((r) => !r.after).length} removed, ${records.filter((r) => r.before && r.after).length} changed)${preChanged ? "; frontmatter changed" : ""}; every other card byte-identical`);
  if (DRY) process.exit(skipped.length ? 3 : 0);
  const srcs = Object.entries(ctx.sources || {}).map(([path, x]) => ({ path, sha256: x.sha256 }));
  for (const x of srcs) if (sha(readText(x.path)) !== x.sha256) die(`${x.path} changed during the run; nothing written`);
  const run = { id: newRunId(board), date: new Date().toISOString(), board: rel(board), label: String(spec.label || made[0] || "run"), kind: "apply", status: "applied", ops: spec.ops, made, notDone: skipped, sources: srcs.length ? srcs : undefined, file: { beforeSha256: sha(text), afterSha256: sha(textNew), beforeTail, afterTail: tailOf(textNew, docNew) }, preamble: preChanged ? { before: doc.preamble, after: bw.parse(textNew).preamble } : null, cards: records };
  if (ctx.sidecar) {
    const sp = board.replace(/\.md$/, ".measure.json");
    const cur = existsSync(sp) ? JSON.parse(readFileSync(sp, "utf8")) : {};
    run.sidecar = { path: rel(sp), before: JSON.parse(JSON.stringify(cur)) };
    Object.assign(cur, ctx.sidecar);
    run.sidecar.after = cur;
  }
  const lp = writeRun(board, run); // the log first: a run that can't write its log entry doesn't write the board
  safeWriteBoard(board, textNew);
  if (run.sidecar) writeFileSync(abs(run.sidecar.path), JSON.stringify(run.sidecar.after, null, 1), "utf8");
  console.log(`  logged as ${run.id} in ${rel(lp)}; written`);
  process.exit(skipped.length ? 3 : 0);
}

// ── undo / redo ───────────────────────────────────────────────────────────────────────────────────────────────────────
function removeSegment(text, offs, doc, id) {
  const o = offs.get(id); if (!o) throw new Error(`^${id} is not in the file`);
  const i = doc.cards.findIndex((c) => c.id === id);
  const next = doc.cards[i + 1];
  if (next) { const n = offs.get(next.id); return text.slice(0, o.start) + text.slice(n.start); }
  const prev = doc.cards[i - 1];
  if (prev) { const p = offs.get(prev.id); return text.slice(0, p.end) + "\n"; }
  return text.slice(0, o.start);
}
function insertSegment(text, offs, doc, prevId, segText) {
  if (!prevId) { const p = doc.preamble; return p + segText + (doc.cards.length ? "\n\n" : "\n") + text.slice(p.length); }
  const o = offs.get(prevId);
  if (!o) { const pc = bw.projectCard(doc); if (!pc) throw new Error("anchor gone and no Project card"); const po = offs.get(pc.id); return text.slice(0, po.end) + "\n\n" + segText + text.slice(po.end); }
  return text.slice(0, o.end) + "\n\n" + segText + text.slice(o.end);
}
function cmdUndoRedo(redo) {
  requireWritable();
  const board = abs(positional[1]); if (!positional[1]) die(`${redo ? "redo" : "undo"} <board.md>`);
  const L = readLog(board);
  const want = arg("--run");
  // Stack order: undo takes the latest applied run; redo takes the earliest of the trailing undone runs (the one undone last).
  let pick = null;
  if (!want) {
    if (!redo) pick = [...L.runs].reverse().find((r) => r.status === "applied");
    else for (let i = L.runs.length - 1; i >= 0 && L.runs[i].status === "undone"; i--) pick = L.runs[i];
  }
  const run = want ? L.runs.find((r) => r.id === want) : pick;
  if (!run) die(redo ? "nothing to redo: no undone run in the log" : `nothing to undo: no applied run in ${rel(L.path)}`);
  if (run.status !== (redo ? "undone" : "applied")) die(`run ${run.id} is ${run.status}`);
  const FORCE = flag("--force");
  if (run.kind === "create") {
    if (redo) { if (existsSync(board)) die(`${rel(board)} exists; redo would overwrite it`); mkdirSync(dirname(board), { recursive: true }); safeWriteBoard(board, run.file.afterText); updateRunStatus(board, run.id, "applied", { redone: new Date().toISOString() }); console.log(`redo ${run.id}: ${rel(board)} re-created (${run.file.afterText.length} bytes)`); return; }
    if (!existsSync(board)) die(`${rel(board)} is already gone`);
    const cur = readFileSync(board, "utf8");
    if (sha(cur) !== run.file.afterSha256 && !FORCE) die(`${rel(board)} changed since the import (${sha(cur).slice(0, 8)} vs ${run.file.afterSha256.slice(0, 8)}); undo would lose those edits. --force removes it anyway (the log keeps the import's own text, not the edits)`);
    updateRunStatus(board, run.id, "undone", { undone: new Date().toISOString(), removedSha256: sha(cur) });
    unlinkSync(board);
    console.log(`undo ${run.id}: ${rel(board)} removed whole (the import); redo re-creates it`);
    return;
  }
  let { text, doc } = loadBoard(board);
  const startDoc = doc; // the tree as it stood before this undo/redo: children checks read it, so re-parenting caused by our own removals doesn't count as CRE's edits
  const untouched = snapshot(text, doc);
  const conflicts = [], done = [];
  const from = (r) => (redo ? r.before : r.after), to = (r) => (redo ? r.after : r.before);
  // 1. take out every segment the run left (its "after" when undoing, its "before" when redoing)
  for (const r of [...run.cards].reverse()) {
    const f = from(r); if (!f) continue;
    const c = bw.findCard(doc, r.id);
    if (!c) { conflicts.push(`^${r.id}: not on the board any more; its ${redo ? "before" : "after"} text can't be taken out`); continue; }
    const offs = offsets(text, doc);
    const cur = text.slice(offs.get(r.id).start, offs.get(r.id).end);
    if (cur !== f.text && !FORCE) { conflicts.push(`^${r.id}: changed since the run (not restored; --force overrides)`); continue; }
    // A card the run added is removed only if nothing new sits under it: cards it held at write time (a wrap's run) just re-parent.
    const startCard = bw.findCard(startDoc, r.id);
    const newKids = !to(r) && startCard ? startCard.children.filter((k) => !(f.children || []).includes(k.id)) : [];
    if (newKids.length && !FORCE) { conflicts.push(`^${r.id}: ${newKids.length} card(s) were put under it since the run; not removed (--force overrides)`); continue; }
    text = removeSegment(text, offs, doc, r.id); doc = bw.parse(text);
    done.push(r.id);
  }
  // 2. put back every segment the run replaced, earliest file position first so anchors exist
  const puts = run.cards.filter((r) => to(r) && !conflicts.some((x) => x.startsWith(`^${r.id}:`))).sort((a, b) => to(a).idx - to(b).idx);
  for (const r of puts) {
    const offs = offsets(text, doc);
    if (bw.findCard(doc, r.id)) { conflicts.push(`^${r.id}: still on the board after taking it out; skipped`); continue; }
    text = insertSegment(text, offs, doc, to(r).prev, to(r).text); doc = bw.parse(text);
    if (!done.includes(r.id)) done.push(r.id);
  }
  if (run.preamble) { const want2 = redo ? run.preamble.before : run.preamble.after, set = redo ? run.preamble.after : run.preamble.before; if (doc.preamble === want2) { text = set + text.slice(doc.preamble.length); doc = bw.parse(text); } else conflicts.push("frontmatter changed since the run; not restored"); }
  if (!done.length && run.cards.length) { console.error(`REFUSED: nothing could be ${redo ? "re-applied" : "restored"} — ${conflicts.join("; ")}`); process.exit(2); }
  if (!conflicts.length && run.file) { const d3 = bw.parse(text); text = withTail(text, d3, redo ? run.file.afterTail : run.file.beforeTail); }
  const docNew = gate(text);
  const now = snapshot(text, docNew);
  const runIds = new Set(run.cards.map((r) => r.id));
  for (const [id, u] of untouched) { if (runIds.has(id)) continue; const n = now.get(id); if (!n || n.text !== u.text) die(`internal: card ^${id} outside the run would change; nothing written`); }
  if (run.sidecar) { const sp = abs(run.sidecar.path); writeFileSync(sp, JSON.stringify(redo ? run.sidecar.after : run.sidecar.before, null, 1), "utf8"); }
  updateRunStatus(board, run.id, redo ? "applied" : "undone", { [redo ? "redone" : "undone"]: new Date().toISOString(), conflicts });
  safeWriteBoard(board, text);
  console.log(`${redo ? "redo" : "undo"} ${run.id} (${run.label}): ${done.length} of ${run.cards.length} cards ${redo ? "re-applied" : "restored"} byte-for-byte${run.preamble ? ", frontmatter too" : ""}`);
  for (const c of conflicts) console.log("  NOT DONE: " + c);
  process.exit(conflicts.length ? 3 : 0);
}

// ── read ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
function cmdRead() {
  const board = abs(positional[1]); if (!positional[1]) die("read <board.md>");
  const { text, doc, roundTrip } = loadBoard(board);
  const s = bw.settingsOf(doc);
  const full = flag("--full");
  const v = versionStatus();
  const pc = bw.projectCard(doc);
  const castList = bw.castOf(doc).map((c) => ({ id: c.id, name: bw.castName(c), aliases: bw.castAliases(c), fields: c.meta.fields || {}, arcs: (c.meta.arcs || []).map((a) => ({ id: a.id, name: a.name, model: a.model || null, plot: !!a.plot })) }));
  const eras = bw.erasOf(doc).map((e) => ({ id: e.id, name: e.name, label: e.label || "", parent: e.parent || "", history: !!e.history }));
  const events = (bw.eventsOf ? bw.eventsOf(doc) : []).map((e) => ({ id: e.id, type: e.type, name: e.name || "", label: bw.eventLabel ? bw.eventLabel(doc, e) : "", era: e.era || "", who: e.who || [], at: e.at || "" }));
  const rels = bw.relationsOf(doc).map((l) => ({ id: l.id, text: bw.relationLabel(doc, l), type: l.type, a: l.a, b: l.b, from: l.from || "", to: l.to || "", note: l.note || "" }));
  const world = bw.worldOf(doc).map((c) => ({ id: c.id, kind: bw.worldKindOf(c), name: bw.worldName(c), aliases: bw.worldAliases(c), fields: c.meta.fields || {} }));
  const inbox = bw.inboxIdeas(doc).map((c) => ({ id: c.id, type: c.meta.type || "", text: c.body, tags: bw.tagNames(c) }));
  const placed = bw.placedIdeas(doc).map((c) => ({ id: c.id, type: c.meta.type || "", text: c.body, on: c.parent ? c.parent.id : "", onTitle: c.parent ? title(c.parent) : "" }));
  const steps = doc.cards.filter((c) => c.meta.kind === "arcbeat").map((c) => ({ id: c.id, cast: c.meta.cast || "", arc: c.meta.arc || c.meta.plotArc || "", step: c.meta.step, beat: c.meta.beat, label: c.meta.label || "", filled: !!c.body.trim(), placed: c.parent && c.parent.meta.kind !== "project" ? c.parent.id : "", era: c.meta.era || "" }));
  const tree = [];
  for (const c of doc.cards) {
    if (["project", "cast", "world", "idea", "arcbeat"].includes(c.meta.kind)) continue;
    if (isProseKind(s, c.meta.kind) && !full) continue;
    const row = { id: c.id, depth: c.depth, kind: c.meta.kind, title: isProseKind(s, c.meta.kind) ? c.body.replace(/\s+/g, " ").slice(0, 80) : title(c), type: c.meta.type || "", speaker: c.meta.speaker || "", chapter: c.meta.fields?.chapter || "", pov: c.meta.fields?.pov || "", era: c.meta.era || "", tags: bw.tagNames(c), words: isProseKind(s, c.meta.kind) ? bw.wordCount(c.body) : undefined };
    if (full) { row.body = c.body; row.fields = c.meta.fields || {}; row.links = bw.linksOf(c); row.derivedTags = bw.derivedTags(s, c); if (c.meta.world) row.world = c.meta.world; }
    if (c.meta.ai) row.aiOffer = c.meta.ai;
    tree.push(row);
  }
  out({
    board: rel(board), title: pc ? title(pc) : "", cards: doc.cards.length, roundTrip, version: v,
    levels: s.levels.map((l) => l.key), ideaTypes: s.ideaTypes || bw.defaultIdeaTypes(), beatTypes: s.beatTypes, tagPrefixes: s.tagPrefixes, worldKinds: bw.worldKinds(s).map((k) => k.key), relationTypes: bw.relationTypes(doc).map((t) => t.name),
    plotting: { on: bw.plottingOn(s), leads: bw.plottingOn(s) ? bw.leadsOf(doc, s) : [], exits: bw.leadExits(s) }, model: s.model || null,
    cast: castList, eras, events, relations: rels, world, inbox, placedIdeas: placed, arcSteps: steps.length > 60 && !full ? { count: steps.length, filled: steps.filter((x) => x.filled).length, unplaced: steps.filter((x) => !x.placed).length, note: "--full lists them" } : steps,
    tree, log: readLog(board).runs.map((r) => ({ id: r.id, date: r.date, label: r.label, status: r.status, touched: (r.cards || []).length })),
  });
}

// ── import ────────────────────────────────────────────────────────────────────────────────────────────────────────────
function headingRank(b) { const m = /^(#{1,6})\s/.exec(b); return m ? m[1].length : 0; }
/** Blocks → cards under `parent`, the plugin's own convert rule: headings become containers by rank, every other block a prose card. */
function blocksInto(doc, s, parent, blocks, containerKinds) {
  const prose = s.levels[s.levels.length - 1].key;
  const depths = [...new Set(blocks.filter((b) => headingRank(b) && !b.includes("\n")).map(headingRank))].sort((a, b) => a - b);
  const open = [];
  const parentFor = (rank) => { while (open.length && open[open.length - 1].rank >= rank) open.pop(); return open.length ? open[open.length - 1].card : parent; };
  for (const b of blocks) {
    if (headingRank(b) && !b.includes("\n")) {
      const rank = Math.min(depths.indexOf(headingRank(b)), containerKinds.length - 1);
      const kind = containerKinds.length ? containerKinds[Math.max(0, rank)] : prose;
      const c = bw.insertChild(doc, parentFor(rank), { kind }); bw.setBody(c, b); open.push({ rank, card: c });
    } else { const c = bw.insertChild(doc, open.length ? open[open.length - 1].card : parent, { kind: prose }); bw.setBody(c, b); }
  }
}
/** Book import source: the chapter folders (CHAPTERS/<folder>/draft.md) in chapter-number order. */
function bookSources(book) {
  const dir = abs(book);
  const chapDir = existsSync(`${dir}/CHAPTERS`) ? `${dir}/CHAPTERS` : dir;
  const folders = readdirSync(chapDir).filter((f) => { try { return statSync(`${chapDir}/${f}`).isDirectory() && existsSync(`${chapDir}/${f}/draft.md`); } catch { return false; } });
  const num = (f) => { const m = /(\d+)/.exec(f); return m ? parseInt(m[1], 10) : 1e9; };
  folders.sort((a, b) => num(a) - num(b) || a.localeCompare(b));
  if (!folders.length) die(`no chapter folders with draft.md under ${rel(chapDir)}`);
  return folders.map((f) => ({ folder: f, path: `${chapDir}/${f}/draft.md` }));
}
const FM_RE = /^---\r?\n[\s\S]*?\r?\n---[ \t]*(\r?\n|$)/;
const bodyOf = (t) => { const fm = FM_RE.exec(t); return { body: (fm ? t.slice(fm[0].length) : t).replace(/\r\n/g, "\n"), fm: !!fm }; };
/** import --into: the same verbatim convert, appended under an existing board's Project card as one logged apply-kind run
 *  (undo takes out exactly the cards it added; every card already on the board stays byte-identical). */
function cmdImportInto() {
  requireWritable();
  const DRY = flag("--dry");
  const board = abs(arg("--into"));
  if (!existsSync(board)) die(`${rel(board)} does not exist; --into needs an existing board (use --board for a new one)`);
  if (/(^|\/)REFERENCE\//.test(rel(board)) || /\/(draft|brief)\.md$/.test(board) || /\/(slate|revisions)\//.test(board)) die("the target is a pipeline or REFERENCE path");
  const src = arg("--source"), book = arg("--book");
  if (!src && !book) die("import needs --source <note.md> or --book <project dir>");
  const { text, doc, roundTrip } = loadBoard(board);
  if (!roundTrip) die(`${rel(board)} does not round-trip through the plugin's serializer; open and save it once in Obsidian, or run \`normalize\` as its own logged run first`);
  const s = bw.settingsOf(doc);
  const project = bw.projectCard(doc); if (!project) die(`${rel(board)} has no Project card`);
  const containers = s.levels.slice(1, -1).map((l) => l.key);
  const before = snapshot(text, doc);
  const beforeTail = tailOf(text, doc);
  const sources = [], made = [];
  const add = (path, t, fm) => sources.push({ path: rel(path), sha256: sha(t), bytes: Buffer.byteLength(t, "utf8"), frontmatterSkipped: fm });
  if (src) {
    const t = readText(src); const { body, fm } = bodyOf(t); add(src, t, fm);
    const seq = bw.insertChild(doc, project, { kind: containers[0] }); bw.setBody(seq, arg("--title", "") || basename(abs(src)).replace(/\.md$/, ""));
    blocksInto(doc, s, seq, bw.splitBlocks(body), containers.slice(1));
    made.push(`${bw.kindName(s, containers[0])} "${title(seq)}" ^${seq.id} with ${seq.children.length} cards from ${rel(src)}`);
  } else if (arg("--under")) {
    // Chapters continuing a part he already built (the Witchwood build, 2026-10-21: "CH12–18 via import --into after Chapter
    // 14, verbatim, marked pre-redraft"): each folder becomes a chapter container under the named part, numbered on from
    // --number-from in his board's numbering, the pipeline folder name kept in `landed`; with --scenes-at-breaks each run of
    // prose between his breaks is a Scene (the break itself is the Scene's own break on export). Only the pipeline's own
    // notes are left off — the "# Draft" heading line, status blockquotes, `---` rules, break lines — each listed in the log.
    const under = findCardRef(doc, arg("--under")); if (!under || !isContainerKind(s, under.meta.kind)) die(`--under ${arg("--under")} is not a container on this board`);
    const lv = s.levels.map((l) => l.key); const chKind = lv[lv.indexOf(under.meta.kind) + 1], scKind = lv[lv.indexOf(under.meta.kind) + 2];
    const [lo, hi] = String(arg("--chapters", "1-9999")).split("-").map(Number);
    let n = Number(arg("--number-from", "0"));
    const SMALL = new Set(["a", "an", "and", "of", "the", "to", "in", "on", "with", "for", "at", "by", "or"]);
    const tc = (x) => x.toLowerCase().split(" ").map((w, i) => (i && SMALL.has(w) ? w : w.charAt(0).toUpperCase() + w.slice(1))).join(" ");
    const structural = (b) => /^#{1,6}\s+Draft\b/.test(b) || /^>/.test(b) && b.split("\n").every((l) => /^>/.test(l)) || /^(-{3,}|\*{3,}|\* \* \*)\s*$/.test(b);
    const isBreak = (b) => /^(\*{3,}|\* \* \*)\s*$/.test(b);
    for (const { folder, path } of bookSources(book)) {
      const num = parseInt((/(\d+)/.exec(folder) || [])[1], 10); if (!(num >= lo && num <= hi)) continue;
      const t = readText(path); const { body, fm } = bodyOf(t); add(path, t, fm);
      const name = folder.replace(/^CHAPTER\s+\d+\s*-\s*/i, "");
      const seq = bw.insertChild(doc, under, { kind: chKind }); bw.setBody(seq, n ? `Chapter ${n} - ${tc(name)}` : folder);
      if (n) bw.setField(seq, "chapter", String(n));
      bw.setField(seq, "landed", `${folder} (pipeline, pre-redraft) — this chapter's prose, imported verbatim; which copy is canon is yours`);
      const blocks = bw.splitBlocks(body); const skipped = [];
      let scene = null;
      for (const b of blocks) {
        if (structural(b)) { skipped.push(b.split("\n")[0].slice(0, 70)); if (isBreak(b)) scene = null; continue; }
        if (flag("--scenes-at-breaks") && !scene) scene = bw.insertChild(doc, seq, { kind: scKind });
        const c = bw.insertChild(doc, flag("--scenes-at-breaks") ? scene : seq, { kind: s.levels[s.levels.length - 1].key }); bw.setBody(c, b);
      }
      sources[sources.length - 1].skipped = skipped;
      made.push(`${bw.kindName(s, chKind)} "${title(seq)}" ^${seq.id} under "${title(under)}" — ${seq.children.length} ${flag("--scenes-at-breaks") ? "scenes" : "cards"} from ${folder}; left off ${skipped.length} pipeline note/break lines`);
      if (n) n++;
    }
  } else {
    for (const { folder, path } of bookSources(book)) {
      const t = readText(path); const { body, fm } = bodyOf(t); add(path, t, fm);
      const seq = bw.insertChild(doc, project, { kind: containers[0] }); bw.setBody(seq, folder);
      const n = /(\d+)/.exec(folder); if (n) bw.setField(seq, "chapter", String(parseInt(n[1], 10)));
      blocksInto(doc, s, seq, bw.splitBlocks(body), containers.slice(1));
      made.push(`${bw.kindName(s, containers[0])} "${folder}"${n ? ` (chapter ${parseInt(n[1], 10)})` : ""} ^${seq.id}`);
    }
  }
  let textNew = bw.serialize(doc);
  if (book && !arg("--under")) {
    const label = arg("--source-label", rel(abs(book))).replace(/"/g, "'");
    const lines = [`bw-working-copy: true`, `bw-source: "${label}"`, `bw-authority: "the pipeline's drafts, until ^backlog-branch-writing-replacement-review rules"`];
    // same frontmatter rule as the mark-working-copy op
    const pre = bw.parse(textNew).preamble; const m = /^---\r?\n([\s\S]*?)\r?\n---[ \t]*(\r?\n|$)/.exec(pre);
    const pre2 = m ? `---\n${[...(m[1] || "").split(/\r?\n/).filter((l) => !/^bw-(working-copy|source|authority):/.test(l)), ...lines].join("\n")}\n---\n` + pre.slice(m[0].length) : `---\n${lines.join("\n")}\n---\n` + pre;
    textNew = pre2 + textNew.slice(pre.length);
    made.push(`marked a working copy of ${label} (frontmatter)`);
  }
  const docNew = gate(textNew);
  const after = snapshot(textNew, docNew);
  const records = [];
  for (const [id, b] of before) { const a = after.get(id); if (!a) records.push({ id, before: b, after: null }); else if (a.text !== b.text || a.prev !== b.prev || (a.parent || "") !== (b.parent || "")) records.push({ id, before: b, after: a }); }
  // (--under inserts mid-file: the one card after the new run keeps its text and only its neighbour changes — logged for undo)
  const changedOld = records.filter((r) => r.before && (r.after ? r.after.text !== r.before.text || !arg("--under") : true));
  if (changedOld.length) die(`internal: ${changedOld.length} card(s) already on the board would change (first ^${changedOld[0].id}); nothing written`);
  for (const [id, a] of after) if (!before.has(id)) records.push({ id, before: null, after: a });
  const bodies = new Set(records.map((r) => docNew.cards.find((c) => c.id === r.id)).filter((c) => c && isProseKind(s, c.meta.kind)).map((c) => c.body));
  const skipLine = (x) => (b) => !(x.skipped || []).includes(b.split("\n")[0].slice(0, 70));
  const srcBlocks = sources.flatMap((x) => bw.splitBlocks(bodyOf(readText(x.path)).body).filter(skipLine(x)));
  const missing = srcBlocks.filter((b) => !bodies.has(b));
  // in order, too: the prose cards this run added read back as the source blocks, one for one
  if (arg("--under")) {
    const addedProse = docNew.cards.filter((c) => !before.has(c.id) && isProseKind(s, c.meta.kind)).map((c) => c.body);
    if (addedProse.length !== srcBlocks.length || addedProse.some((b, i) => b !== srcBlocks[i])) die(`the imported prose does not read back as the source blocks in order (${addedProse.length} cards for ${srcBlocks.length} blocks); nothing written`);
  }
  if (missing.length) die(`${missing.length} source blocks are not on the board word for word; nothing written. First: ${JSON.stringify(missing[0].slice(0, 80))}`);
  for (const x of sources) if (sha(readText(x.path)) !== x.sha256) die(`${x.path} changed while importing; nothing written`);
  const preChanged = docNew.preamble !== doc.preamble;
  const nProse = records.filter((r) => { const c = docNew.cards.find((k) => k.id === r.id); return c && isProseKind(s, c.meta.kind); }).length;
  const label = `import ${src ? rel(src) : arg("--source-label", rel(abs(book)))} into this board`;
  console.log(`${DRY ? "DRY RUN — nothing written" : "run"}: ${rel(board)} — ${label}`);
  for (const m of made) console.log("  made: " + m);
  console.log(`  cards added: ${records.length} (${nProse} prose, ${records.length - nProse} containers) from ${sources.length} source file(s); ${srcBlocks.length} blocks, all on the board word for word; sources untouched (${sources.map((x) => x.sha256.slice(0, 8)).join(", ")})${preChanged ? "; frontmatter changed" : ""}; every card already on the board byte-identical`);
  if (DRY) return;
  const run = { id: newRunId(board), date: new Date().toISOString(), board: rel(board), label, kind: "apply", status: "applied", ops: [{ op: "import-into", source: src ? rel(src) : rel(abs(book)) }], sources, made, notDone: [], file: { beforeSha256: sha(text), afterSha256: sha(textNew), beforeTail, afterTail: tailOf(textNew, docNew) }, preamble: preChanged ? { before: doc.preamble, after: docNew.preamble } : null, cards: records };
  const lp = writeRun(board, run);
  safeWriteBoard(board, textNew);
  console.log(`  logged as ${run.id} in ${rel(lp)}; written — "undo" takes out exactly these cards; next: \`propose\` for the structure (ruled, never landed by itself)`);
}
function cmdImport() {
  if (arg("--into")) return cmdImportInto();
  requireWritable();
  const boardPath = abs(arg("--board")); if (!arg("--board")) die("import needs --board <new board.md> (or --into <existing board.md>)");
  if (existsSync(boardPath)) die(`${rel(boardPath)} exists; an import writes only a new board`);
  if (/(^|\/)REFERENCE\//.test(rel(boardPath)) || /\/(draft|brief)\.md$/.test(boardPath) || /\/(slate|revisions)\//.test(boardPath)) die("the target is a pipeline or REFERENCE path");
  const src = arg("--source"), book = arg("--book");
  if (!src && !book) die("import needs --source <note.md> or --book <project dir>");
  const settings = bw.defaultSettings();
  // Plugin 0.63: imported prose carries its own dialogue tags, so the export never adds the template's (the plugin's Convert does the same).
  settings.dialogue = { ...settings.dialogue, mode: "never" };
  const doc = bw.parse(""); doc.cards = []; doc.roots = [];
  const project = bw.newCard(doc, { kind: "project", depth: 0, settings }); doc.roots.push(project); doc.cards.push(project); bw.flatten(doc); doc.structureDirty = true;
  const sources = [];
  const containers = settings.levels.slice(1, -1).map((l) => l.key); // sequence, scene, beat
  let titleText = arg("--title", "");
  if (src) {
    const t = readText(src); sources.push({ path: rel(src), sha256: sha(t), bytes: Buffer.byteLength(t, "utf8") });
    const fm = /^---\r?\n[\s\S]*?\r?\n---[ \t]*(\r?\n|$)/.exec(t);
    const body = (fm ? t.slice(fm[0].length) : t).replace(/\r\n/g, "\n");
    bw.setBody(project, titleText || basename(abs(src)).replace(/\.md$/, ""));
    blocksInto(doc, settings, project, bw.splitBlocks(body), containers);
    if (fm) sources[0].frontmatterSkipped = true;
  } else {
    const dir = abs(book);
    const chapDir = existsSync(`${dir}/CHAPTERS`) ? `${dir}/CHAPTERS` : dir;
    const folders = readdirSync(chapDir).filter((f) => { try { return statSync(`${chapDir}/${f}`).isDirectory() && existsSync(`${chapDir}/${f}/draft.md`); } catch { return false; } });
    const num = (f) => { const m = /(\d+)/.exec(f); return m ? parseInt(m[1], 10) : 1e9; };
    folders.sort((a, b) => num(a) - num(b) || a.localeCompare(b));
    if (!folders.length) die(`no chapter folders with draft.md under ${rel(chapDir)}`);
    bw.setBody(project, titleText || basename(dir));
    for (const f of folders) {
      const t = readText(`${chapDir}/${f}/draft.md`); const fm = /^---\r?\n[\s\S]*?\r?\n---[ \t]*(\r?\n|$)/.exec(t);
      sources.push({ path: rel(`${chapDir}/${f}/draft.md`), sha256: sha(t), bytes: Buffer.byteLength(t, "utf8"), frontmatterSkipped: !!fm });
      const seq = bw.insertChild(doc, project, { kind: containers[0] }); bw.setBody(seq, f); // the folder name, CRE's words
      const n = /(\d+)/.exec(f); if (n) bw.setField(seq, "chapter", String(parseInt(n[1], 10)));
      blocksInto(doc, settings, seq, bw.splitBlocks((fm ? t.slice(fm[0].length) : t).replace(/\r\n/g, "\n")), containers.slice(1));
    }
  }
  let text = bw.withBoardMark(bw.serialize(doc));
  if (book) {
    const lines = [`bw-working-copy: true`, `bw-source: "${rel(abs(book)).replace(/"/g, "'")}"`, `bw-authority: "the pipeline's drafts, until ^backlog-branch-writing-replacement-review rules"`];
    text = text.replace(/^---\n/, `---\n${lines.join("\n")}\n`);
  }
  const d2 = gate(text);
  // The grader's own check, done here too: every source block is a card body, and every prose body is a source block.
  const bodies = d2.cards.filter((c) => c.meta.kind !== "project").map((c) => c.body);
  const srcBlocks = sources.flatMap((x) => { const t = readText(x.path); const fm = /^---\r?\n[\s\S]*?\r?\n---[ \t]*(\r?\n|$)/.exec(t); return bw.splitBlocks((fm ? t.slice(fm[0].length) : t).replace(/\r\n/g, "\n")); });
  const missing = srcBlocks.filter((b) => !bodies.includes(b));
  if (missing.length) die(`${missing.length} source blocks are not on the board word for word; nothing written. First: ${JSON.stringify(missing[0].slice(0, 80))}`);
  for (const x of sources) if (sha(readText(x.path)) !== x.sha256) die(`${x.path} changed while importing; nothing written`);
  const run = { id: newRunId(boardPath), date: new Date().toISOString(), board: rel(boardPath), label: `import ${src ? rel(src) : rel(abs(book))}`, kind: "create", status: "applied", sources, file: { beforeSha256: null, afterSha256: sha(text), afterText: text }, cards: [], made: [`board ${rel(boardPath)} created: ${d2.cards.length - 1} cards from ${sources.length} source file(s), every block word for word${book ? "; marked a working copy" : ""}`], notDone: [] };
  const lp = writeRun(boardPath, run);
  mkdirSync(dirname(boardPath), { recursive: true });
  writeFileSync(boardPath, text, { encoding: "utf8", flag: "wx" });
  if (readFileSync(boardPath, "utf8") !== text) die("the written board did not read back byte-identical");
  console.log(`import: ${rel(boardPath)} created — ${d2.cards.length - 1} cards (${d2.cards.filter((c) => isProseKind(settings, c.meta.kind)).length} prose, ${d2.cards.filter((c) => containers.includes(c.meta.kind)).length} containers) from ${sources.length} source file(s); ${srcBlocks.length} blocks, all on the board word for word; sources untouched (${sources.map((x) => x.sha256.slice(0, 8)).join(", ")})${sources.some((x) => x.frontmatterSkipped) ? "; source frontmatter not imported (metadata, not prose)" : ""}${book ? "; marked a working copy (frontmatter)" : ""}`);
  console.log(`  logged as ${run.id} in ${rel(lp)} — "undo" removes the import whole; next: \`propose\` for the structure (ruled, never landed by itself)`);
}

// ── propose (import structure) and suggest-tags ───────────────────────────────────────────────────────────────────────
function cmdPropose() {
  const board = abs(positional[1]); if (!positional[1]) die("propose <board.md>");
  const { doc } = loadBoard(board); const s = bw.settingsOf(doc);
  const prose = (c) => isProseKind(s, c.meta.kind);
  const P = { board: rel(board), note: "Proposals only. Each becomes an op in an apply file once CRE approves it; nothing here lands by itself. POV per scene is left to CRE (no guess).", scenes: [], chapters: [], dialogue: [], cast: [], pov: [] };
  const breakRe = /^\s*(\*\s*\*\s*\*|\*{3,}|-{3,}|_{3,}|~{3,}|#\s*#\s*#|§)\s*$/;
  // scene breaks: runs of prose cards between break cards under one container → a Scene card around each run
  for (const c of doc.cards) {
    if (isProseKind(s, c.meta.kind) || !c.children.some(prose)) continue;
    const kids = c.children; const breaks = kids.filter((k) => prose(k) && breakRe.test(k.body));
    if (!breaks.length) continue;
    let run = [];
    const flush = (after) => { if (run.length) P.scenes.push({ under: `^${c.id}`, underTitle: title(c), cards: run.map((k) => `^${k.id}`), firstWords: run[0].body.replace(/\s+/g, " ").slice(0, 60), reason: `${run.length} blocks between scene breaks${after ? ` (break card ^${after.id} kept, word for word)` : ""}`, op: { op: "wrap", kind: sceneKey(s), cards: run.map((k) => `^${k.id}`) } }); run = []; };
    for (const k of kids) { if (prose(k) && breakRe.test(k.body)) { flush(k); } else if (prose(k)) run.push(k); else flush(null); }
    flush(null);
  }
  // chapters: a container whose title reads like a chapter heading → the chapter field
  for (const c of doc.cards) {
    if (prose(c) || c.meta.kind === "project" || !isContainerKind(s, c.meta.kind)) continue;
    const m = /^#*\s*(?:chapter|ch\.?)\s*(\d+|[ivxlc]+)\b/i.exec(title(c));
    if (m && !(c.meta.fields && c.meta.fields.chapter)) P.chapters.push({ card: `^${c.id}`, title: title(c), chapter: m[1], reason: "the title names a chapter", op: { op: "set-field", card: `^${c.id}`, field: "chapter", value: m[1] } });
  }
  // dialogue: a prose block that opens with a quote; the speaker from a plain "X said" tag when there is one
  const said = /[”"']\s*,?\s*([A-Z][\w'’-]+(?:\s[A-Z][\w'’-]+)?)\s+(said|asked|whispered|shouted|replied|answered|called|muttered|murmured|hissed|snapped|told|cried|growled|laughed)\b|\b(said|asked|whispered|shouted|replied|answered|called|muttered|murmured|hissed|snapped|cried|growled|laughed)\s+([A-Z][\w'’-]+(?:\s[A-Z][\w'’-]+)?)/;
  const names = new Map();
  for (const c of doc.cards) {
    if (!prose(c) || c.meta.type) continue;
    if (/^\s*[“"']/.test(c.body) && !breakRe.test(c.body)) {
      const m = said.exec(c.body); const who = m ? (m[1] || m[4]) : "";
      P.dialogue.push({ card: `^${c.id}`, firstWords: c.body.replace(/\s+/g, " ").slice(0, 60), speaker: who, reason: who ? `opens with a quote; "${who}" tags the line` : "opens with a quote; no tag names the speaker (CRE's call)", op: { op: "set-type", card: `^${c.id}`, type: "dialogue", ...(who ? { speaker: who } : {}) } });
      if (who) names.set(who, (names.get(who) || 0) + 1);
    }
  }
  // cast: names that tag dialogue, plus capitalised words that recur ≥ 3 times and aren't sentence starts only
  const freq = new Map();
  for (const c of doc.cards) if (prose(c)) for (const m of c.body.matchAll(/(?<=[^.!?\n]\s)([A-Z][a-z]{2,})\b/g)) freq.set(m[1], (freq.get(m[1]) || 0) + 1);
  const stop = new Set(["The", "And", "But", "She", "He", "They", "Then", "When", "There", "That", "This", "His", "Her", "Its", "You", "Not", "For", "With", "What", "Who", "Why", "How", "Yes", "No", "God", "Lord", "Mister", "Miss"]);
  const existing = new Set(bw.castNames(doc).map(norm));
  for (const [n, k] of [...names.entries(), ...[...freq.entries()].filter(([w, k]) => k >= 3 && !stop.has(w) && !names.has(w))]) if (!existing.has(norm(n))) P.cast.push({ name: n, reason: names.has(n) ? `tags ${names.get(n)} dialogue line(s)` : `${k} mentions mid-sentence`, op: { op: "add-cast", name: n } });
  for (const c of doc.cards) if (isUnitKind(s, c.meta.kind) && !(c.meta.fields && c.meta.fields.pov)) P.pov.push({ card: `^${c.id}`, title: title(c), reason: "POV is CRE's call; set-field pov once he names it", op: { op: "set-field", card: `^${c.id}`, field: "pov", value: "" } });
  const o = arg("--out"); if (o) { writeFileSync(abs(o), JSON.stringify(P, null, 2), "utf8"); console.log(`wrote ${rel(o)}: ${P.scenes.length} scene(s), ${P.chapters.length} chapter(s), ${P.dialogue.length} dialogue, ${P.cast.length} cast, ${P.pov.length} POV slots open`); } else out(P);
}
function cmdSuggestTags() {
  const board = abs(positional[1]); if (!positional[1]) die("suggest-tags <board.md>");
  const { doc } = loadBoard(board); const s = bw.settingsOf(doc);
  const S = { board: rel(board), note: "Offers only (by: ai once approved). Existing tags, derived tags and plotUntag are honoured; by: cre entries are never touched.", tags: [] };
  const people = bw.castOf(doc).map((c) => ({ id: c.id, name: bw.castName(c), names: [...new Set([bw.castName(c), ...bw.castAliases(c), ...bw.allAliases(c)])].filter(Boolean) }));
  const places = bw.worldOf(doc).map((c) => ({ id: c.id, kind: bw.worldKindOf(c), name: bw.worldName(c), names: [...new Set([bw.worldName(c), ...bw.worldAliases(c), ...bw.allWorldNames(c)])].filter(Boolean), prefix: (bw.worldKindDef(s, c) || {}).prefix || `${bw.worldKindOf(c)}:` }));
  for (const c of doc.cards) {
    if (["project", "cast", "world"].includes(c.meta.kind) || !c.body.trim()) continue; // ideas and arc steps take tags like any card (§5a, §5c)
    const have = bw.filterTags(s, c); const untag = new Set(Array.isArray(c.meta.plotUntag) ? c.meta.plotUntag : []);
    const low = ` ${c.body.toLowerCase()} `;
    for (const p of people) { if (untag.has(p.id)) continue; const tag = `char:${p.name}`; if (have.has(norm(tag)) || [...have].some((h) => norm(h) === norm(tag))) continue; const hit = p.names.find((n) => n && new RegExp(`(^|[^\\w])${n.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}([^\\w]|$)`).test(low)); if (hit) S.tags.push({ card: `^${c.id}`, tag, reason: `"${hit}" is in the text`, op: { op: "add-tag", card: `^${c.id}`, tag } }); }
    for (const w of places) { if (untag.has(w.id)) continue; const tag = `${w.prefix}${w.name}`; if ([...have].some((h) => norm(h) === norm(tag))) continue; const hit = w.names.find((n) => n && low.includes(` ${n.toLowerCase()} `) || n && low.includes(` ${n.toLowerCase()}.`) || n && low.includes(` ${n.toLowerCase()},`)); if (hit) S.tags.push({ card: `^${c.id}`, tag, reason: `"${hit}" is in the text`, op: { op: "add-tag", card: `^${c.id}`, tag } }); }
  }
  const o = arg("--out"); if (o) { writeFileSync(abs(o), JSON.stringify(S, null, 2), "utf8"); console.log(`wrote ${rel(o)}: ${S.tags.length} tag offer(s)`); } else out(S);
}

// ── check / calibrate / log / normalize ───────────────────────────────────────────────────────────────────────────────
function cmdCheck() {
  const v = versionStatus();
  const b = arg("--board");
  const r = { ...v, writes: v.status === "ok" ? "allowed" : "refused (read-only this run)" };
  if (b) { const { doc, roundTrip } = loadBoard(abs(b)); r.board = { path: rel(abs(b)), cards: doc.cards.length, roundTrip, log: readLog(abs(b)).runs.length }; }
  out(r);
  if (v.status !== "ok") process.exit(2);
}
function cmdCalibrate() {
  const L = liveVersions();
  if (L.problems.length) die(L.problems.join("; "));
  if (cmpVer(L.devManifest, L.installed) !== 0) die(`dev ${L.devManifest} ≠ installed ${L.installed}: build and deploy first so the node core matches the plugin`);
  const cal = { skill: "branch-writing-expert", plugin: L.installed, schemaPluginVersion: L.schemaPluginVersion, schemaVersion: L.schemaVersion, schemaSha256: L.schemaSha256, coreSha256: sha(readFileSync(CORE)), calibrated: today(), note: "Written by `board_tool.mjs calibrate` after the schema's changes were read. The version check compares the installed plugin and the schema doc with this record at every launch; newer → read, then recalibrate; a format change the skill can't account for → read-only." };
  const target = existsSync(dirname(CAL_SRC)) ? CAL_SRC : CAL_PATH;
  writeFileSync(target, JSON.stringify(cal, null, 2) + "\n", "utf8");
  console.log(`calibrated to plugin ${cal.plugin}, schema ${cal.schemaPluginVersion} (${cal.schemaSha256.slice(0, 12)}) → ${rel(target)}`);
}
function cmdLog() {
  const board = abs(positional[1]); if (!positional[1]) die("log <board.md>");
  const L = readLog(board);
  out({ log: rel(L.path), runs: L.runs.map((r) => ({ id: r.id, date: r.date, label: r.label, kind: r.kind, status: r.status, touched: (r.cards || []).length, made: r.made, notDone: r.notDone, undone: r.undone, redone: r.redone, undoConflicts: r.conflicts && r.conflicts.length ? r.conflicts : undefined })) });
}
function cmdNormalize() {
  requireWritable();
  const board = abs(positional[1]); if (!positional[1]) die("normalize <board.md>");
  const { text, doc, roundTrip } = loadBoard(board);
  if (roundTrip) { console.log(`${rel(board)} already round-trips; nothing to do`); return; }
  const textNew = bw.serialize(doc); gate(textNew);
  const run = { id: newRunId(board), date: new Date().toISOString(), board: rel(board), label: "normalize (whole file: the plugin's own serialization)", kind: "whole-file", status: "applied", file: { beforeSha256: sha(text), afterSha256: sha(textNew), beforeText: text, afterText: textNew }, cards: [], made: ["whole file re-serialized by the plugin's core; the log keeps the exact bytes before"], notDone: [] };
  writeRun(board, run); safeWriteBoard(board, textNew);
  console.log(`normalized ${rel(board)} (logged ${run.id}; undo restores the exact bytes)`);
}

switch (cmd) {
  case "check": cmdCheck(); break;
  case "read": cmdRead(); break;
  case "apply": cmdApply(); break;
  case "undo": cmdUndoRedo(false); break;
  case "redo": cmdUndoRedo(true); break;
  case "import": cmdImport(); break;
  case "propose": cmdPropose(); break;
  case "suggest-tags": cmdSuggestTags(); break;
  case "log": cmdLog(); break;
  case "calibrate": cmdCalibrate(); break;
  case "normalize": cmdNormalize(); break;
  default: die(`unknown command "${cmd}"; see the header of this file`);
}
