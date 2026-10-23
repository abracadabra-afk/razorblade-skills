// Stage the beats (CRE, 2026-10-22: "translate the map down into a list of instructions/needs and summaries that take the
// load off my head"). The deterministic half of the mode: read-only on the board, never writes it (the stamp and the link
// go through board_tool.mjs as an ops file this script prints). The reading and the brief's plain lines stay with the model.
//
//   node stage_scene.mjs gather <board.md> --scene <ref> --out <dir>     facts.json + facts.md + ideas.json + README.md
//   node stage_scene.mjs fingerprint <board.md> --scene <ref>            the scene's structure fingerprint (and its parts)
//   node stage_scene.mjs check <board.md> --scene <ref> [--brief <file>] fresh / stale (what moved) / unstaged
//   node stage_scene.mjs verify <brief.md> --facts <dir>/facts.json      coverage: sections, every step once, sources lines
//   node stage_scene.mjs stamp-ops <board.md> --scene <ref> --brief <vault path> --out <ops.json>
//   (the brief's frontmatter is written by stage_front.py: yaml.safe_dump, parse-gated, DIR-004)
//
// --name <board name> files a scratch copy's brief under its real board's folder name.
// <ref> is a scene ^id, "title:<scene title>", or "Ch 48" (the chapter's only scene; several → listed, pick the id).
// Step-to-beat mapping is mechanical (schema 0.42 runs, 0.51 plotLine): a step on line L of the scene belongs to the beat
// drilled from L (plotFrom "<scene>:L", or a run "<scene>:A..B" that covers L). A step sitting on a beat card is that beat's.
// Nothing is guessed: a step on a line no beat carries, or on no line (a need), is listed as such.
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { createHash } from "node:crypto";
import { basename } from "node:path";

for (const st of [process.stdout, process.stderr]) try { st.setDefaultEncoding("utf8"); } catch {}
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const WIN = process.platform === "win32";
const DEV = arg("--dev", WIN ? "C:/Users/Chad/dev/branch-writing" : `${process.env.HOME}/dev/branch-writing`);
const VAULT = arg("--vault", WIN ? "C:/Users/Chad/Dropbox/razorblade_mermaid" : `${process.env.HOME}/Dropbox/razorblade_mermaid`);
const PROJECT = arg("--project", "WRITING/PROJECTS/WITCHWOOD");
const fix = (p) => p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`).replace(/\\/g, "/");
const abs = (p) => (/^[A-Za-z]:|^\//.test(fix(p)) ? fix(p) : `${VAULT}/${p}`);
const pos = argv.filter((a, i) => !a.startsWith("--") && !(i > 0 && argv[i - 1].startsWith("--")));
const cmd = pos[0];
const die = (m) => { console.error("REFUSED: " + m); process.exit(2); };
if (!["gather", "fingerprint", "check", "verify", "stamp-ops"].includes(cmd)) die("command is gather | fingerprint | check | verify | stamp-ops");

const STAMP_FIELD = "staged";

// ── verify needs no board ────────────────────────────────────────────────────────────────────────────────────────────
if (cmd === "verify") {
  const brief = readFileSync(abs(pos[1]), "utf8");
  const facts = JSON.parse(readFileSync(abs(arg("--facts")), "utf8"));
  const sections = brief.split(/\n(?=## )/).filter((s) => s.startsWith("## "));
  const problems = [];
  if (sections.length !== facts.beats.length) problems.push(`${sections.length} beat sections; the scene has ${facts.beats.length} beats`);
  const seen = new Map();
  sections.forEach((sec, i) => {
    for (const m of sec.matchAll(/\^([a-z0-9]{6})\b/g)) if (facts.stepIds.includes(m[1])) { if (!seen.has(m[1])) seen.set(m[1], new Set()); seen.get(m[1]).add(i); }
    if (!/\*\*Sources:\*\*/.test(sec)) problems.push(`section ${i + 1} has no Sources line`);
    const b = facts.beats[i];
    if (b && !sec.includes(b.id)) problems.push(`section ${i + 1} does not cite its beat ^${b.id} ("${b.title}")`);
  });
  for (const b of facts.beats) for (const st of b.steps) {
    const at = seen.get(st.id);
    if (!at) problems.push(`step ^${st.id} (${st.arc} · ${st.label}) is in no section`);
    else if (at.size > 1) problems.push(`step ^${st.id} is cited under ${at.size} sections (${[...at].map((x) => x + 1).join(", ")})`);
    else if (![...at].includes(b.index)) problems.push(`step ^${st.id} sits under section ${[...at][0] + 1}, its beat is ${b.index + 1}`);
  }
  // A bundled beat is one exchange row per line: each of the run's line ids appears in a table row of its section.
  facts.beats.forEach((b, i) => {
    if (!b.run || !sections[i]) return;
    const rows = sections[i].split("\n").filter((l) => /^\|/.test(l));
    for (const l of b.lines) if (!rows.some((r) => r.includes(l.id))) problems.push(`section ${i + 1} is a run; line \`${l.id}\` has no exchange row`);
  });
  // Every quoted span (6+ characters) must be his words in a source the brief reads: the board, the DEV note, threads.md.
  const srcText = [facts.board, facts.sources.devNote && abs(facts.sources.devNote), abs(`${PROJECT}/REFERENCE/threads.md`)].filter((f) => f && existsSync(f)).map((f) => readFileSync(f, "utf8")).join("\n").replace(/[*_]/g, "");
  // A line marked "Ruled (CRE, <date>):" quotes his ruling from chat, logged where he gave it (DIR-014); it is not checked.
  const body = brief.replace(/^---[\s\S]*?\n---/, "").replace(/^>.*$/gm, "").replace(/^.*Ruled \(CRE, \d{4}-\d{2}-\d{2}\).*$/gm, "");
  for (const m of body.matchAll(/"([^"\n]{6,})"/g)) if (!srcText.includes(m[1])) problems.push(`quote not found in the board, DEV note or threads: "${m[1].slice(0, 80)}"`);
  const fp = (/^fingerprint:\s*"?([0-9a-f]+)/m.exec(brief) || [])[1];
  if (fp !== facts.fingerprint.hash) problems.push(`brief fingerprint ${fp || "(none)"} ≠ facts ${facts.fingerprint.hash}`);
  const placed = facts.beats.reduce((n, b) => n + b.steps.length, 0);
  console.log(`sections ${sections.length}/${facts.beats.length} · steps placed ${seen.size}/${placed}${facts.unmapped.length ? ` · ${facts.unmapped.length} off any beat (header)` : ""}`);
  if (problems.length) { for (const p of problems) console.log("PROBLEM: " + p); process.exit(1); }
  console.log("ok");
  process.exit(0);
}

const bw = await import(pathToFileURL(`${DEV}/test/core.mjs`).href);
const boardPath = abs(pos[1] || die("board path"));
const boardText = readFileSync(boardPath, "utf8");
const doc = bw.parse(boardText);
const s = bw.settingsOf(doc);
const L = s.levels.map((l) => l.key);
const [SCENE, BEAT, PROSE] = [L[L.length - 3], L[L.length - 2], L[L.length - 1]];
const order = new Map(doc.cards.map((c, i) => [c.id, i]));
const title = (c) => (c ? (c.body || "").split("\n").find((l) => l.trim()) || "" : "").replace(/^#+\s*/, "").trim();
const fld = (c, k) => (c && c.meta.fields && c.meta.fields[k] != null ? String(c.meta.fields[k]) : "");
const kids = (c) => doc.cards.filter((k) => k.parent === c);
const castName = (id) => { const c = id ? bw.findCard(doc, id) : null; return c ? bw.castName(c) : ""; };

// ── the scene ────────────────────────────────────────────────────────────────────────────────────────────────────────
function resolveScene(ref) {
  if (!ref) die("--scene is required");
  const r = String(ref).trim();
  if (/^\^?[a-z0-9]{6}$/i.test(r)) { const c = bw.findCard(doc, r.replace(/^\^/, "")); if (!c || c.meta.kind !== SCENE) die(`${r} is not a scene`); return c; }
  if (r.startsWith("title:")) { const t = r.slice(6).trim(); const m = doc.cards.filter((c) => c.meta.kind === SCENE && title(c) === t); if (m.length !== 1) die(`${m.length} scenes titled "${t}"`); return m[0]; }
  const ch = /^(?:ch(?:apter)?\.?\s*)(\d+[a-z]?)$/i.exec(r);
  if (ch) {
    const m = doc.cards.filter((c) => c.meta.kind === SCENE && bw.chapterOf(c) === ch[1]);
    if (m.length === 1) return m[0];
    if (!m.length) die(`no scene in chapter ${ch[1]}`);
    die(`chapter ${ch[1]} has ${m.length} scenes — name one: ${m.map((c) => `^${c.id} "${title(c)}"`).join(" · ")}`);
  }
  die(`"${r}" is not a scene ref (^id, title:…, or Ch N)`);
}
const scene = resolveScene(arg("--scene"));
const lines = bw.chainLines(doc, scene);
const lineIdx = new Map(lines.map((l, i) => [l.id, i]));
const beats = kids(scene).filter((c) => c.meta.kind === BEAT);

// Beat → the lines it carries (a single line or a bundled run). A run is CRE's grouping; it is read, never made.
const beatLines = new Map();
for (const b of beats) {
  const ref = bw.pointRef(b);
  if (!ref || ref.parent !== scene.id) { beatLines.set(b.id, []); continue; }
  beatLines.set(b.id, bw.runLines(lines, ref.first, ref.last) || []);
}
const lineBeat = new Map();
for (const b of beats) for (const l of beatLines.get(b.id)) lineBeat.set(l.id, b);
// Chain order: beats by their first line; beats drilled from nothing keep file order after them.
beats.sort((a, b) => { const la = beatLines.get(a.id)[0], lb = beatLines.get(b.id)[0]; const ia = la ? lineIdx.get(la.id) : 1e9, ib = lb ? lineIdx.get(lb.id) : 1e9; return ia - ib || order.get(a.id) - order.get(b.id); });

// ── arcs ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
const plotArcs = bw.plotArcs(doc);
function arcFlat(st) {
  // Every step and sub-step of the step's arc, depth first in step order — "the step before it on that arc".
  let top;
  if (typeof st.meta.plotArc === "string") top = bw.plotArcSteps(doc, st.meta.plotArc);
  else if (typeof st.meta.cast === "string") top = bw.arcSteps(doc, st.meta.cast, st.meta.arc);
  else return [];
  const out = [];
  const walk = (list) => { for (const c of list) { out.push(c); walk(bw.subSteps(doc, c.id)); } };
  walk(top);
  return out;
}
function where(c) {
  const host = c.parent && c.parent.meta.kind !== "project" ? c.parent : null;
  if (!host) return { chapter: "", card: "", line: "", text: "unplaced" };
  const ls = bw.chainLines(doc, host);
  const l = ls.find((x) => x.id === c.meta.plotLine);
  return { chapter: bw.chapterOf(host), card: host.id, cardTitle: title(host), line: l ? l.k : "", lineText: l ? l.text : "" };
}
function arcInfo(st) {
  if (typeof st.meta.plotArc === "string") {
    const a = plotArcs.find((x) => x.id === st.meta.plotArc) || {};
    return { kind: "plot", arcId: a.id || st.meta.plotArc, arc: a.label || castName(a.goal_holder) || st.meta.plotArc, role: a.main ? "main plot" : "subplot", goal: a.goal || "", stakes: a.stakes || "", holder: castName(a.goal_holder) };
  }
  const cast = typeof st.meta.cast === "string" ? bw.findCard(doc, st.meta.cast) : null;
  const def = cast ? bw.arcById(cast, st.meta.arc) : null;
  const role = cast ? bw.arcRole(cast, st.meta.arc) : null;
  return { kind: "character", arcId: st.meta.arc || "", arc: def ? def.name || "" : "", cast: cast ? bw.castName(cast) : "", role: role ? role.role + (role.set ? ` (${role.set})` : "") + (role.against ? ` against ${castName(role.against)}` : "") : "", goal: def && def.goal ? def.goal : "" };
}
function marker(label) {
  const m = /^(held|audit)\s*[—-]\s*(.*)$/i.exec(label || "");
  return m ? { kind: m[1].toLowerCase(), code: m[2] } : null;
}
function stepFacts(st, lineId) {
  const label = bw.stepLabel(st) || st.meta.label || "";
  const flat = arcFlat(st);
  const i = flat.findIndex((c) => c.id === st.id);
  const prev = i > 0 ? flat[i - 1] : null;
  const par = typeof st.meta.parentStep === "string" ? bw.findCard(doc, st.meta.parentStep) : null;
  const a = arcInfo(st);
  return {
    id: st.id, line: lineId, label, text: (st.body || "").trim(), number: bw.stepNumber(doc, st), modelBeat: st.meta.beat ?? null,
    ...a, arcLabel: a.kind === "character" ? `${a.cast} · ${a.arc}` : a.arc,
    marker: marker(label) || marker(st.body),
    parentStep: par ? { id: par.id, label: bw.stepLabel(par) || par.meta.label || "", text: (par.body || "").trim() } : null,
    prev: prev ? { id: prev.id, label: bw.stepLabel(prev) || prev.meta.label || "", text: (prev.body || "").trim(), ...where(prev) } : null,
  };
}

// ── what sits on the scene ───────────────────────────────────────────────────────────────────────────────────────────
const isStep = (c) => c.meta.kind === "arcbeat";
const isIdea = (c) => c.meta.kind === "idea";
const sceneSteps = kids(scene).filter(isStep);
const unmapped = [];
const perBeat = new Map(beats.map((b) => [b.id, []]));
for (const st of sceneSteps) {
  const ln = st.meta.plotLine;
  if (!ln || !lineIdx.has(ln)) { unmapped.push({ ...stepFacts(st, ""), why: "on the scene, on no line (a need)" }); continue; }
  const b = lineBeat.get(ln);
  if (!b) { unmapped.push({ ...stepFacts(st, ln), why: `on line ${lines[lineIdx.get(ln)].k} "${lines[lineIdx.get(ln)].text.slice(0, 60)}", which no beat carries` }); continue; }
  perBeat.get(b.id).push(stepFacts(st, ln));
}
for (const b of beats) for (const st of kids(b).filter(isStep)) perBeat.get(b.id).push({ ...stepFacts(st, st.meta.plotLine || ""), onBeat: true });
for (const [id, list] of perBeat) list.sort((x, y) => (lineIdx.get(x.line) ?? 99) - (lineIdx.get(y.line) ?? 99) || order.get(x.id) - order.get(y.id));

// Inherited needs (0.56): steps on the sequence lines this scene was drilled from.
const seq = scene.parent && scene.parent.meta.kind !== "project" ? scene.parent : null;
const inherited = [];
const sref = bw.pointRef(scene);
if (sref) {
  const p = bw.findCard(doc, sref.parent);
  if (p) {
    const pl = bw.runLines(bw.chainLines(doc, p), sref.first, sref.last) || [];
    const ids = new Set(pl.map((l) => l.id));
    for (const st of kids(p).filter(isStep)) if (ids.has(st.meta.plotLine)) inherited.push({ ...stepFacts(st, st.meta.plotLine), from: `${title(p)} · ${pl.find((l) => l.id === st.meta.plotLine).k}` });
  }
}

// World: entries linked to the scene/beats, and board entry names his scene's words use without a link.
// Plugin 0.66.2: a World chip from the words (a name in a typed card's chain lines, not untagged with ×) is a link too —
// it reaches the entry's Through the story. So `linked` is the plugin's own worldLinksOf (by id, by the kind's field, by
// words); `byWords` keeps which ones came only from the words, so the brief can say so.
const worldAll = bw.worldOf ? bw.worldOf(doc) : doc.cards.filter((c) => bw.isWorld(c));
const linksOf = (c) => (bw.worldLinksOf ? bw.worldLinksOf(doc, s, c).map((l) => ({ id: l.entry.id, by: l.by })) : bw.cardWorldIds(c).map((id) => ({ id, by: "id" })));
const allLinks = [scene, ...beats].flatMap(linksOf);
const linked = new Set(allLinks.map((l) => l.id));
const byWords = new Set(allLinks.filter((l) => l.by === "words" && !allLinks.some((m) => m.id === l.id && m.by !== "words")).map((l) => l.id));
const textOf = (c) => [title(c), fld(c, "summary"), fld(c, "story from"), fld(c, "story to"), ...bw.chainLines(doc, c).map((l) => l.text)].join("\n");
function namesIn(text) {
  const out = [];
  const low = text.toLowerCase();
  for (const w of worldAll) for (const n of bw.allWorldNames(w)) {
    if (n.length < 4) continue;
    const re = new RegExp(`(^|[^\\p{L}])${n.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?=$|[^\\p{L}])`, "u");
    if (re.test(low)) { out.push({ id: w.id, name: bw.worldName(w), as: n, kind: bw.worldKindOf(w) }); break; }
  }
  return out;
}
// Cast: members his words name, and whether the scene or the beat carries their char: tag. A missing cast member is
// checked here too, so a name the World tab lacks is never called missing from the board (the Trailkeeper is cast).
const castAll = doc.cards.filter((c) => c.meta.kind === "cast");
const charTags = (c) => bw.tagNames(c).filter((t) => t.startsWith("char:")).map((t) => t.slice(5).toLowerCase());
function castIn(text, cards) {
  const low = text.toLowerCase();
  const tagged = new Set(cards.flatMap(charTags));
  const out = [];
  for (const c of castAll) {
    const name = bw.castName(c);
    const names = [name, ...(Array.isArray(c.meta.aliases) ? c.meta.aliases : [])].filter((n) => typeof n === "string" && n.length >= 4);
    const hit = names.find((n) => new RegExp(`(^|[^\\p{L}])${n.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?=$|[^\\p{L}])`, "u").test(low));
    if (hit) out.push({ id: c.id, name, as: hit, tagged: tagged.has(name.toLowerCase()) });
  }
  return out;
}

// Intensity side file.
let measure = {};
const mp = boardPath.replace(/\.md$/, ".measure.json");
if (existsSync(mp)) try { measure = JSON.parse(readFileSync(mp, "utf8")); } catch {}

// Tags (seed:/payoff:) on the scene, its beats and what sits on them, and where the pair sits on the board.
const tagHome = new Map();
for (const c of doc.cards) for (const t of bw.tagNames(c)) if (/^(seed|payoff):/.test(t)) { if (!tagHome.has(t)) tagHome.set(t, []); tagHome.get(t).push(c); }
const tagsHere = (c) => bw.tagNames(c).filter((t) => /^(seed|payoff):/.test(t)).map((t) => {
  const other = t.startsWith("seed:") ? "payoff:" + t.slice(5) : "seed:" + t.slice(7);
  return { tag: t, pair: (tagHome.get(other) || []).map((k) => ({ id: k.id, chapter: bw.chapterOf(k), title: title(k) })) };
});

// Timeline label of a line or beat: his "past:" / "present:" lead-in, else blank (read by the model, never guessed here).
const tl = (txt) => { const m = /^\s*(past|present)\s*:/i.exec(txt || ""); return m ? m[1].toLowerCase() : ""; };

// The previous beat in story order (crossing into the scene before), and the previous beat in the same timeline.
const allBeats = doc.cards.filter((c) => c.meta.kind === BEAT && c.parent && c.parent.meta.kind === SCENE);
const beatFacts = beats.map((b, i) => {
  const ls = beatLines.get(b.id);
  const ideasOn = [...kids(b).filter(isIdea), ...kids(scene).filter((c) => isIdea(c) && ls.some((l) => l.id === c.meta.plotLine))];
  const micro = kids(b).filter((c) => c.meta.kind === PROSE);
  const bl = bw.chainLines(doc, b);
  const hasChain = bw.beatHasChain ? bw.beatHasChain(b) : false;
  const blocs = hasChain && bw.blocsOf ? bw.blocsOf(s, b) : null;
  const timeline = tl(ls[0] && ls[0].text) || tl(fld(b, "summary"));
  const prevAny = i > 0 ? beats[i - 1] : allBeats[allBeats.findIndex((x) => x === b) - 1] || null;
  let prevSame = null;
  if (timeline) for (let j = i - 1; j >= 0; j--) { const t2 = tl((beatLines.get(beats[j].id)[0] || {}).text) || tl(fld(beats[j], "summary")); if (t2 === timeline) { prevSame = beats[j]; break; } }
  const words = [textOf(b), ...perBeat.get(b.id).map((x) => x.text), ...ideasOn.map((c) => c.body)].join("\n");
  const names = namesIn(words);
  const others = kids(b).filter((c) => !isIdea(c) && !isStep(c) && c.meta.kind !== PROSE);
  return {
    index: i, id: b.id, title: title(b), type: b.meta.type || "", summary: fld(b, "summary"), plotFrom: b.meta.plotFrom || "",
    run: ls.length > 1, timeline,
    lines: ls.map((l) => ({ id: l.id, k: l.k, text: l.text, outcome: l.outcome, detail: l.detail, steps: perBeat.get(b.id).filter((x) => x.line === l.id).map((x) => x.id) })),
    steps: perBeat.get(b.id),
    ownChain: hasChain ? bl.map((l) => ({ id: l.id, k: l.k, text: l.text, outcome: l.outcome })) : null,
    blocs: blocs ? blocs.blocs.map((x) => ({ line: x.point || x.id || "", micro: (x.cards || x.micro || []).map((c) => c.id) })) : null,
    prose: micro.map((c) => ({ id: c.id, type: c.meta.type || "", bloc: c.meta.plotBloc || "", words: (c.body || "").split(/\s+/).filter(Boolean).length })),
    ideas: ideasOn.map((c) => ({ id: c.id, type: c.meta.type || "", line: c.meta.plotLine || "", text: c.body.trim() })),
    others: others.map((c) => ({ id: c.id, kind: c.meta.kind, meta: c.meta.fields || {}, body: title(c) })),
    offers: b.meta.ai || null,
    tags: tagsHere(b),
    world: names.map((n) => ({ ...n, linked: linked.has(n.id), byWords: byWords.has(n.id) })),
    cast: castIn(words, [scene, b]),
    intensity: measure[b.id] || null,
    prevBeat: prevAny ? { id: prevAny.id, title: title(prevAny), summary: fld(prevAny, "summary"), chapter: bw.chapterOf(prevAny), sameScene: prevAny.parent === scene } : null,
    prevSameTimeline: prevSame ? { id: prevSame.id, title: title(prevSame), summary: fld(prevSame, "summary") } : null,
  };
});

// ── the fingerprint ──────────────────────────────────────────────────────────────────────────────────────────────────
function fingerprint() {
  const h = (o) => createHash("sha256").update(JSON.stringify(o)).digest("hex").slice(0, 12);
  const f = { ...(scene.meta.fields || {}) }; delete f[STAMP_FIELD];
  const parts = {
    chain: h({ fields: f, chain: scene.meta.plotChain || null, from: scene.meta.plotFrom || null, title: title(scene) }),
    beats: h(beats.map((b) => ({ id: b.id, from: b.meta.plotFrom || null, type: b.meta.type || "", title: title(b), fields: b.meta.fields || {}, chain: b.meta.plotChain || null }))),
    steps: h([...sceneSteps, ...beats.flatMap((b) => kids(b).filter(isStep))].map((c) => ({ id: c.id, on: c.parent.id, line: c.meta.plotLine || null, label: c.meta.label || "", text: c.body || "", parent: c.meta.parentStep || null }))),
    ideas: h([scene, ...beats].flatMap((p) => kids(p).filter(isIdea)).map((c) => ({ id: c.id, on: c.parent.id, line: c.meta.plotLine || null }))),
    prose: h(beats.flatMap((b) => kids(b).filter((c) => c.meta.kind === PROSE)).map((c) => ({ id: c.id, bloc: c.meta.plotBloc || null, sha: createHash("sha256").update(c.body || "").digest("hex").slice(0, 8) }))),
  };
  return { hash: h(parts), parts };
}
const FP = fingerprint();
const stampRaw = fld(scene, STAMP_FIELD);
const stamp = (() => { const m = /^(\d{4}-\d{2}-\d{2}) · fp ([0-9a-f]{12}) · (.+)$/.exec(stampRaw); return m ? { date: m[1], hash: m[2], brief: m[3] } : null; })();

if (cmd === "fingerprint") { console.log(JSON.stringify({ scene: scene.id, ...FP, stamp }, null, 1)); process.exit(0); }

if (cmd === "check") {
  // Fresh only when the board's stamp and the brief's frontmatter both name the scene's current fingerprint.
  const briefPath = arg("--brief") || (stamp && stamp.brief);
  let bfp = null, bparts = null;
  if (briefPath && existsSync(abs(briefPath))) {
    const t = readFileSync(abs(briefPath), "utf8");
    bfp = (/^fingerprint:\s*"?([0-9a-f]{12})/m.exec(t) || [])[1] || null;
    const pm = /^fingerprint_parts:\s*'?(\{.*?\})'?\s*$/m.exec(t); if (pm) try { bparts = JSON.parse(pm[1]); } catch {}
  }
  if (!stamp && !bfp) { console.log(`unstaged — ^${scene.id} "${title(scene)}" carries no staged stamp and no brief was found`); process.exit(3); }
  const ref = bfp || stamp.hash;
  if (ref === FP.hash && (!stamp || stamp.hash === FP.hash)) { console.log(`fresh — fp ${FP.hash} (${stamp ? "stamp " + stamp.date : "no stamp yet"}; brief ${briefPath})`); process.exit(0); }
  const moved = bparts ? Object.keys(FP.parts).filter((k) => bparts[k] !== FP.parts[k]) : ["(the brief carries no parts; rebuild)"];
  console.log(`STALE — the scene moved since the brief: ${moved.join(", ")} changed (fp now ${FP.hash}, brief ${ref}${stamp && stamp.hash !== ref ? `, board stamp ${stamp.hash}` : ""}). Rebuild on his word: "restage ${(seq ? title(seq).replace(/^Chapter\s+\d+[a-z]?\s*[-–—:]\s*/i, "") : "") || title(scene)}".`);
  process.exit(1);
}

const boardName = arg("--name", basename(boardPath).replace(/\.md$/, "")); // --name: a test copy files under its real board's name
const ch = bw.chapterOf(scene);
const chTitle = seq ? title(seq).replace(/^Chapter\s+\d+[a-z]?\s*[-–—:]\s*/i, "") : "";
const scenesInCh = doc.cards.filter((c) => c.meta.kind === SCENE && bw.chapterOf(c) === ch);
const fileTitle = `${ch ? `Ch ${ch} - ` : ""}${scenesInCh.length > 1 || !chTitle ? title(scene) : chTitle}`.replace(/[\\/:*?"<>|#^[\]]/g, "");
const briefDefault = `WRITING/BOARD BRIEFS/${boardName}/${fileTitle}.md`;

if (cmd === "stamp-ops") {
  const brief = arg("--brief", briefDefault);
  const date = new Date().toLocaleDateString("sv-SE"); // local day, YYYY-MM-DD
  const ops = [
    { op: "set-field", card: `^${scene.id}`, field: STAMP_FIELD, value: `${date} · fp ${FP.hash} · ${brief}` },
    { op: "add-link", card: `^${scene.id}`, to: `[[${brief.replace(/\.md$/, "")}]]`, rel: "beat brief" },
  ];
  writeFileSync(abs(arg("--out") || die("--out")), JSON.stringify({ board: boardPath, label: `stage the beats for ${title(scene)}: the staged stamp and the brief's link`, ops }, null, 1));
  console.log(`stamp ops → ${arg("--out")} (fp ${FP.hash})`);
  process.exit(0);
}

// ── gather ───────────────────────────────────────────────────────────────────────────────────────────────────────────
const out = abs(arg("--out") || die("--out"));
mkdirSync(out, { recursive: true });
const proj = abs(PROJECT);
const seqName = fld(scene, "seq") || fld(seq, "seq");
let devNote = "";
if (seqName && existsSync(`${proj}/DEV/sequences`)) devNote = (readdirSync(`${proj}/DEV/sequences`).find((f) => f.startsWith(seqName + " ") || f === seqName + ".md") || "");
devNote = devNote ? `${PROJECT}/DEV/sequences/${devNote}` : "";

// threads.md: threads whose entry names a world entry the scene's words use (linked or not). Candidates, read before use.
const sceneWords = [textOf(scene), ...beatFacts.flatMap((b) => [b.summary, ...b.lines.map((l) => l.text), ...b.steps.map((x) => x.text), ...b.ideas.map((x) => x.text)])].join("\n");
const sceneNames = namesIn(sceneWords);
const threads = [];
const tp = `${proj}/REFERENCE/threads.md`;
if (existsSync(tp)) {
  const t = readFileSync(tp, "utf8").split("\n");
  let cur = null;
  t.forEach((ln, i) => {
    const h = /^### (T\d+)\s*—\s*(.*)$/.exec(ln);
    if (h) { cur = { id: h[1], name: h[2].trim(), line: i + 1, planted: "", status: "", body: "" }; threads.push(cur); return; }
    if (/^##\s/.test(ln)) { cur = null; return; }
    if (!cur) return;
    cur.body += ln + "\n";
    if (/^- \*\*Planted:\*\*/.test(ln)) cur.planted = ln.replace(/^- \*\*Planted:\*\*\s*/, "");
    if (/^- \*\*Status:\*\*/.test(ln)) cur.status = ln.replace(/^- \*\*Status:\*\*\s*/, "");
  });
}
const nameRes = sceneNames.flatMap((n) => [...new Set([n.name, n.as])]).filter(Boolean);
const threadHits = threads.filter((th) => nameRes.some((n) => (th.name + "\n" + th.body).toLowerCase().includes(n.toLowerCase()))).map((th) => ({ id: th.id, name: th.name, line: th.line, planted: th.planted, status: th.status.slice(0, 200), names: nameRes.filter((n) => (th.name + th.body).toLowerCase().includes(n.toLowerCase())) }));

// Trace reports citing the scene, a beat or a step id, or the scene's SEQ.
const traces = [];
const rp = `${VAULT}/SYSTEM/reports`;
const ids = [scene.id, ...beats.map((b) => b.id), ...beatFacts.flatMap((b) => b.steps.map((x) => x.id))];
if (existsSync(rp)) for (const f of readdirSync(rp).filter((f) => /trace/.test(f) && f.endsWith(".md"))) {
  const t = readFileSync(`${rp}/${f}`, "utf8").split("\n");
  const hits = [];
  t.forEach((ln, i) => { if (ids.some((id) => ln.includes(id)) || (seqName && new RegExp(`\\b${seqName.replace(/\s+/g, "\\s+")}\\b`).test(ln))) hits.push(i + 1); });
  if (hits.length) traces.push({ file: `SYSTEM/reports/${f}`, lines: hits.slice(0, 12), count: hits.length });
}

// Choreography: a beat map in the chapter's choreo/ folder, where one exists (never designed here).
let choreo = [];
const chDir = `${proj}/CHAPTERS`;
if (ch && existsSync(chDir)) {
  const d = readdirSync(chDir).find((f) => new RegExp(`^CHAPTER 0*${ch}\\b`, "i").test(f));
  if (d && existsSync(`${chDir}/${d}/choreo`)) choreo = readdirSync(`${chDir}/${d}/choreo`).map((f) => `${PROJECT}/CHAPTERS/${d}/choreo/${f}`);
}

const shelfIdeas = kids(scene).filter((c) => isIdea(c) && !(c.meta.plotLine && lineIdx.has(c.meta.plotLine)));
const facts = {
  board: boardPath, boardName, briefPath: briefDefault, built: new Date().toLocaleDateString("sv-SE"),
  fingerprint: FP, stamp,
  scene: {
    id: scene.id, title: title(scene), chapter: ch, chapterTitle: chTitle,
    part: (() => { const p = bw.partOf(scene); return p ? title(p) : ""; })(),
    sequence: seq ? { id: seq.id, title: title(seq), summary: fld(seq, "summary"), from: fld(seq, "story from"), to: fld(seq, "story to"), drive: fld(seq, "drive") } : null,
    era: (() => { try { const e = bw.eraIdAt(scene); return e ? bw.eraNameOf(scene, e) || e : ""; } catch { return ""; } })(),
    flashback: bw.isFlashback(scene), timelines: fld(scene, "timelines"), setting: fld(scene, "setting"), goalHolder: fld(scene, "goal holder"),
    summary: fld(scene, "summary"), storyFrom: fld(scene, "story from"), storyTo: fld(scene, "story to"), seq: seqName,
    plotFrom: scene.meta.plotFrom || "", lines: lines.map((l) => ({ id: l.id, k: l.k, text: l.text, outcome: l.outcome, beat: (lineBeat.get(l.id) || {}).id || "" })),
    world: [...linked].map((id) => { const w = bw.findCard(doc, id); return w ? { id, name: bw.worldName(w), kind: bw.worldKindOf(w), byWords: byWords.has(id) } : { id, name: "(gone)" }; }),
    namedNotLinked: sceneNames.filter((n) => !linked.has(n.id)),
    cast: castIn(sceneWords, [scene, ...beats]),
    intensity: measure[scene.id] || null, tags: tagsHere(scene),
  },
  beats: beatFacts, stepIds: [...beatFacts.flatMap((b) => b.steps.map((x) => x.id)), ...unmapped.map((x) => x.id)],
  unmapped, inherited, shelfIdeas: shelfIdeas.length,
  sources: { devNote, threads: threadHits, traces, choreo, measure: existsSync(mp) ? mp : "" },
};
writeFileSync(`${out}/facts.json`, JSON.stringify(facts, null, 1));
writeFileSync(`${out}/ideas.json`, JSON.stringify(shelfIdeas.map((c) => ({ id: c.id, type: c.meta.type || "", text: c.body.trim() })), null, 1));

// facts.md: the readable form, in chain order.
const q = (t, n = 200) => (t || "").replace(/\s+/g, " ").trim().slice(0, n);
const md = [];
const S = facts.scene;
md.push(`# Stage facts — Ch ${S.chapter} · ${S.chapterTitle || S.title} · ^${S.id}`, "");
md.push(`fingerprint ${FP.hash} · parts ${JSON.stringify(FP.parts)} · stamp ${stamp ? `${stamp.date} ${stamp.hash}${stamp.hash === FP.hash ? " (fresh)" : " (STALE)"}` : "none"}`);
md.push(`brief → ${briefDefault}`, "");
md.push(`**Part** ${S.part} · **Sequence** ${S.sequence ? S.sequence.title : "—"} · **Scene** ${S.title} · era ${S.era || "—"}${S.flashback ? " (flashback)" : ""} · setting ${S.setting || "—"} · goal holder ${S.goalHolder || "—"}`);
md.push(`timelines: ${S.timelines || "—"}`, `summary: ${S.summary}`, `from → to: ${S.storyFrom} → ${S.storyTo}`);
md.push(`cast named: ${S.cast.map((c) => `${c.name}${c.tagged ? "" : " (no char: tag on the scene or a beat)"}`).join(", ") || "none"}`);
md.push(`world linked: ${S.world.map((w) => `${w.name}${w.byWords ? " (chip from the words)" : ""}`).join(", ") || "none"} · named, not linked: ${S.namedNotLinked.map((w) => `${w.name}${w.as !== w.name ? ` ("${w.as}")` : ""}`).join(", ") || "none"}`);
md.push(`intensity: ${S.intensity ? JSON.stringify({ e: S.intensity.emotional, p: S.intensity.physical }) : "none (no score)"} · DEV: ${devNote || "none found"} · choreo: ${choreo.join(", ") || "none"}`);
md.push(`steps: ${facts.stepIds.length} on the scene · ${unmapped.length} off any beat · ${inherited.length} inherited from the sequence · ${shelfIdeas.length} ideas on the scene, on no line`, "");
if (unmapped.length) { md.push("## Off any beat (header)"); for (const x of unmapped) md.push(`- ^${x.id} ${x.arcLabel} · ${x.label}: ${q(x.text)} — ${x.why}`); md.push(""); }
if (inherited.length) { md.push("## Inherited from the sequence (0.56)"); for (const x of inherited) md.push(`- ^${x.id} ${x.arcLabel} · ${x.label} (${x.from}): ${q(x.text)}`); md.push(""); }
for (const b of beatFacts) {
  md.push(`## ${b.index + 1}. ${b.title} · ^${b.id} · ${b.type || "untyped"}${b.timeline ? ` · ${b.timeline}` : ""}${b.run ? ` · RUN of ${b.lines.length} lines` : ""}`);
  md.push(`summary: ${b.summary}`);
  for (const l of b.lines) md.push(`- line ${l.k} \`${l.id}\`: ${l.text}${l.outcome ? ` [${l.outcome}]` : ""}${l.steps.length ? ` — steps ${l.steps.map((x) => "^" + x).join(" ")}` : ""}`);
  for (const x of b.steps) {
    md.push(`- STEP ^${x.id} · ${x.kind} · ${x.arcLabel}${x.role ? ` (${x.role})` : ""} · #${x.number}${x.modelBeat ? ` B${x.modelBeat}` : ""} · ${x.label}${x.marker ? ` · MARKER ${x.marker.kind}` : ""}${x.onBeat ? " · on the beat card" : ""}`);
    md.push(`  text: ${x.text}`);
    if (x.goal) md.push(`  arc goal: ${x.goal}`);
    if (x.parentStep) md.push(`  parent ^${x.parentStep.id}: ${x.parentStep.label} — ${q(x.parentStep.text, 160)}`);
    md.push(`  before it: ${x.prev ? `^${x.prev.id} ${x.prev.label} — ${q(x.prev.text, 160)} (Ch ${x.prev.chapter || "?"} · ${x.prev.cardTitle || x.prev.text}${x.prev.lineText ? ` · ${x.prev.line}: ${q(x.prev.lineText, 80)}` : ""})` : "first on its arc"}`);
  }
  md.push(`coming in: ${b.prevBeat ? `${b.prevBeat.sameScene ? "" : `(Ch ${b.prevBeat.chapter}) `}${b.prevBeat.title} ^${b.prevBeat.id} — ${q(b.prevBeat.summary)}` : "—"}${b.prevSameTimeline && b.prevSameTimeline.id !== (b.prevBeat || {}).id ? ` · same timeline: ${b.prevSameTimeline.title} ^${b.prevSameTimeline.id} — ${q(b.prevSameTimeline.summary)}` : ""}`);
  md.push(`cast: ${b.cast.map((c) => `${c.name}${c.tagged ? "" : " (not tagged)"}`).join(", ") || "—"}`);
  md.push(`world: ${b.world.map((w) => `${w.name}${w.linked ? (w.byWords ? " (chip from the words)" : "") : " (NOT LINKED)"}`).join(", ") || "—"} · tags: ${b.tags.map((t) => `${t.tag}${t.pair.length ? ` ↔ ${t.pair.map((p) => `Ch ${p.chapter} ^${p.id}`).join(", ")}` : " (no pair)"}`).join("; ") || "—"} · intensity: ${b.intensity ? "scored" : "none"}`);
  md.push(`prose: ${b.prose.length ? `${b.prose.length} micro-beats, ${b.prose.reduce((n, p) => n + p.words, 0)} words` : "none"} · own chain: ${b.ownChain ? b.ownChain.map((l) => `${l.k}: ${q(l.text, 60)}`).join(" → ") : "none"} · ideas on it: ${b.ideas.length} · offers: ${b.offers ? JSON.stringify(b.offers).slice(0, 200) : "none"}`);
  for (const i of b.ideas) md.push(`  idea ^${i.id} (${i.type}): ${q(i.text, 160)}`);
  md.push("");
}
md.push("## Sources to read");
md.push(`- DEV: ${devNote || "none"}`);
for (const th of threadHits) md.push(`- threads ${th.id} — ${th.name} (REFERENCE/threads.md:${th.line}) · names ${th.names.join(", ")} · planted ${q(th.planted, 160)}`);
for (const tr of traces) md.push(`- trace ${tr.file} lines ${tr.lines.join(", ")}${tr.count > tr.lines.length ? " …" : ""}`);
writeFileSync(`${out}/facts.md`, md.join("\n") + "\n");
writeFileSync(`${out}/README.md`, [
  "# What stage_scene.mjs did not check",
  "- Thread matches are by world-entry name only: a thread that names none of them is not listed. Read threads.md for the arcs' own plants.",
  "- Timeline per beat is read from a \"past:\" / \"present:\" lead-in only; an unlabelled beat's timeline is the model's reading of the scene.",
  "- Character states come from ledger rows / offers when present, else from the steps' own words (the model's read).",
  "- Ideas on the scene on no line are listed in ideas.json; where each belongs is his ruling list, never placed here.",
  "- \"Before it\" is the previous step or sub-step in the arc's own order, which is not always story order.",
  "",
].join("\n"));
console.log(`gathered ^${scene.id} "${title(scene)}" (Ch ${ch}) → ${out}: ${beatFacts.length} beats, ${facts.stepIds.length} steps (${facts.stepIds.length - unmapped.length} on a beat, ${unmapped.length} off), ${inherited.length} inherited, ${shelfIdeas.length} ideas to place, fp ${FP.hash}`);
