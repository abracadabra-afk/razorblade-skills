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
  doc.cards.forEach((c, i) => m.set(c.id, { text: seg(c), prev: i ? doc.cards[i - 1].id : "", idx: i, children: c.children.map((k) => k.id) }));
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
const NEVER_FIELDS = new Set(["summary", "story from", "story to", "outcome", "outcome detail", "decision", "goal", "sets goal", "reacts to", "reacts to (short)", "stakes", "opposition", "conflict", "what changed", "intensity start", "intensity end", "physical start", "physical end"]);
const NEVER_KEYS = new Set(["plotChain", "plotMarks", "plotComplete", "plotFrom", "plotBloc", "plotLine", "plotPins", "plotUntag", "plotNeeds", "plotTurnedAt", "convo", "vis", "visUnit"]);

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
        case "add-world": {
          if (!op.kind || !op.name) throw new Error("kind and name are required");
          if (bw.findWorldByName(doc, op.name, op.kind)) throw new Error(`"${op.name}" is already a ${op.kind}`);
          const c = bw.addWorldEntry(doc, s, String(op.kind), String(op.name));
          if (!c) throw new Error(`world kind "${op.kind}" is not on this board (kinds: ${bw.worldKinds(s).map((k) => k.key).join(", ")})`);
          if (Array.isArray(op.aliases) && op.aliases.length) bw.setMeta(c, "aliases", op.aliases.map(String));
          for (const [k, v] of Object.entries(op.fields || {})) bw.setWorldValue(c, k, String(v));
          made.push(`${op.kind}: ${op.name}${Object.keys(op.fields || {}).length ? " — " + Object.entries(op.fields).map(([k, v]) => `${k}: ${v}`).join("; ") : ""} ${idOf(c)}`);
          break;
        }
        case "set-world": {
          const c = worldRef(doc, op.entry); if (!c) throw new Error(`no world entry "${op.entry}"`);
          bw.setWorldValue(c, String(op.field), op.value == null ? "" : String(op.value));
          made.push(`${bw.worldKindOf(c)} ${bw.worldName(c)}: ${op.field} = ${op.value}`);
          break;
        }
        case "add-idea": {
          if (typeof op.text !== "string" || !op.text.trim()) throw new Error("text is required (CRE's words, verbatim)");
          const types = s.ideaTypes || bw.defaultIdeaTypes();
          if (op.type && !types.includes(op.type)) throw new Error(`idea type "${op.type}" is not one of this board's (${types.join(", ")})`);
          const c = bw.addIdea(doc, op.text, op.type || undefined, []);
          for (const t of op.tags || []) bw.addTag(c, String(t), op.by === "cre" ? "cre" : "ai");
          made.push(`idea${op.type ? ` (${op.type})` : ""}: ${op.text.replace(/\s+/g, " ").slice(0, 90)}${op.text.length > 90 ? "…" : ""} ${idOf(c)}`);
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
          if (op.under) { const p = findCardRef(doc, op.under); if (!p) throw new Error(`no card ${op.under}`); c = bw.insertChild(doc, p, { kind: op.kind }); }
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
        case "set-plotting": {
          if (op.on === false) { bw.disablePlotting(doc); made.push("Statement Plotting off"); break; }
          const added = bw.enablePlotting(doc);
          made.push(`Statement Plotting on${added.length ? ` (${added.length} fields added)` : ""}`);
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
          if (!isUnitKind(s2, u.meta.kind)) throw new Error(`${idOf(u)} is a ${bw.kindName(s2, u.meta.kind)}; the plugin honours a lead exit only on a unit (a ${bw.kindName(s2, sceneKey(s2))}-level card) — plottab.ts:241, flows.ts:84. Name the unit where ${bw.castName(c)} leaves`);
          bw.setLeadExit(doc, c.id, u.id);
          made.push(`lead exit: ${bw.castName(c)} after ${title(u)} ${idOf(u)}`);
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
  for (const [id, b] of before) { const a = after.get(id); if (!a) records.push({ id, before: b, after: null }); else if (a.text !== b.text || a.prev !== b.prev) records.push({ id, before: b, after: a }); }
  for (const [id, a] of after) if (!before.has(id)) records.push({ id, before: null, after: a });
  const preChanged = bw.parse(textNew).preamble !== doc.preamble;
  const changed = records.length > 0 || preChanged || !!ctx.sidecar;
  console.log(`${DRY ? "DRY RUN — nothing written" : "run"}: ${rel(board)} — ${spec.label || "(no label)"}`);
  for (const m of made) console.log("  made: " + m);
  for (const x of skipped) console.log("  NOT DONE: " + x);
  if (!changed) { console.log("  nothing changed on the board"); process.exit(skipped.length ? 3 : 0); }
  console.log(`  cards touched: ${records.length} (${records.filter((r) => !r.before).length} added, ${records.filter((r) => !r.after).length} removed, ${records.filter((r) => r.before && r.after).length} changed)${preChanged ? "; frontmatter changed" : ""}; every other card byte-identical`);
  if (DRY) process.exit(skipped.length ? 3 : 0);
  const run = { id: newRunId(board), date: new Date().toISOString(), board: rel(board), label: String(spec.label || made[0] || "run"), kind: "apply", status: "applied", ops: spec.ops, made, notDone: skipped, file: { beforeSha256: sha(text), afterSha256: sha(textNew), beforeTail, afterTail: tailOf(textNew, docNew) }, preamble: preChanged ? { before: doc.preamble, after: bw.parse(textNew).preamble } : null, cards: records };
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
    cast: castList, eras, relations: rels, world, inbox, placedIdeas: placed, arcSteps: steps.length > 60 && !full ? { count: steps.length, filled: steps.filter((x) => x.filled).length, unplaced: steps.filter((x) => !x.placed).length, note: "--full lists them" } : steps,
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
function cmdImport() {
  requireWritable();
  const boardPath = abs(arg("--board")); if (!arg("--board")) die("import needs --board <new board.md>");
  if (existsSync(boardPath)) die(`${rel(boardPath)} exists; an import writes only a new board`);
  if (/(^|\/)REFERENCE\//.test(rel(boardPath)) || /\/(draft|brief)\.md$/.test(boardPath) || /\/(slate|revisions)\//.test(boardPath)) die("the target is a pipeline or REFERENCE path");
  const src = arg("--source"), book = arg("--book");
  if (!src && !book) die("import needs --source <note.md> or --book <project dir>");
  const settings = bw.defaultSettings();
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
