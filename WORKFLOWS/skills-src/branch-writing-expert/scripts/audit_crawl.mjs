// Audit the board (CRE, 2026-10-21: "an agent audit the board and check continuity, beat mapping, alignments and idenify
// any meaning issues around plotting or repeition"). READ-ONLY: never writes the board, the plan or anything in the vault
// except the work folder it is given. It boils a whole board down into digests an agent can read across, in story order,
// so the judgment passes (references/audit.md) work from the whole book at once instead of one thread at a time:
//
//   outline-P<n>.md  every Sequence, Scene and Beat of part n in story order: titles, summaries, story from → to, goal
//                    holder, outcome, with the arc steps and markers placed on each — the spine the checks walk
//   prose-P<n>.md    every micro-beat of part n, one line each, prefixed with its position and id (grep it for a fact)
//   arcs.md          every arc (character arcs with their model role, plot arcs and subplots with goal / stakes /
//                    planned outcome): its steps in step order, where each sits, its silences, its order inversions
//   markers.md       every redraft marker ("held —", "body —", "bond —", "adage —", "hermit —", "audit —"), classed: keep-dark
//                    ("held — hold the mystery: …"), sources-disagree, other held, and the named families
//   alignment.md     the approved plan against the board: subplots on one side only, plan words no longer on the board,
//                    steps sitting in another scene than the card their plan cell cites
//   names.md         every cast member and world entry (with aliases): where it is mentioned and its longest silences
//   repeats.md       repeated phrases across scenes (his words) and near-twin beat summaries (repeated moves) — candidates
//   README.md        counts, the files, and what this crawl does NOT check (DIR-018)
//
//   node audit_crawl.mjs <board.md> --out <work folder> [--plan <plan.md>] [--gram 6] [--gap 12] [--twin 0.35]
//
// Story order is board order. Positions read "P3 · Chapter 9 - … › Scene title" with a running scene number (sc 042) so a
// gap can be measured. Every quote is the card's own text; ids are block ids (^abc123). Console output is UTF-8 (DIR-020).
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { pathToFileURL } from "node:url";

for (const st of [process.stdout, process.stderr]) try { st.setDefaultEncoding("utf8"); } catch {}
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const WIN = process.platform === "win32";
const DEV = arg("--dev", WIN ? "C:/Users/Chad/dev/branch-writing" : `${process.env.HOME}/dev/branch-writing`);
const VAULT = arg("--vault", WIN ? "C:/Users/Chad/Dropbox/razorblade_mermaid" : `${process.env.HOME}/Dropbox/razorblade_mermaid`);
const fix = (p) => p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`).replace(/\\/g, "/");
const abs = (p) => (/^[A-Za-z]:|^\//.test(fix(p)) ? fix(p) : `${VAULT}/${p}`);
const die = (m) => { console.error("REFUSED: " + m); process.exit(2); };
const [boardPath] = argv.filter((a, i) => !a.startsWith("--") && !(i > 0 && argv[i - 1].startsWith("--")));
const OUT = arg("--out") ? fix(arg("--out")) : null;
if (!boardPath || !OUT) die("usage: node audit_crawl.mjs <board.md> --out <work folder> [--plan <plan.md>]");
const CORE = `${DEV}/test/core.mjs`;
if (!existsSync(CORE)) die(`the plugin's node core is missing at ${CORE}; run \`npm run build\` in the dev folder`);
const bw = await import(pathToFileURL(CORE).href);
const GRAM = parseInt(arg("--gram", "6"), 10);
const GAP = parseInt(arg("--gap", "12"), 10);
const TWIN = parseFloat(arg("--twin", "0.35"));

const text = readFileSync(abs(boardPath), "utf8");
if (!bw.isBoardText(text)) die(`${boardPath} is not a Branch Writing board`);
const doc = bw.parse(text);
const s = bw.settingsOf(doc);
const L = s.levels.map((l) => l.key);
const [K_PART, K_SEQ, K_SCENE, K_BEAT, K_MICRO] = [L[1], L[2], L[3], L[4], L[5]];
const title = (c) => (c.body || "").split("\n")[0].trim();
const one = (t) => String(t || "").replace(/\s+/g, " ").trim();
const norm = (t) => one(t).replace(/[’‘]/g, "'").replace(/[“”]/g, '"').toLowerCase();
const cut = (t, n = 160) => { t = one(t); return t.length > n ? t.slice(0, n - 1) + "…" : t; };
const F = (c, k) => (c.meta.fields || {})[k] || "";

// ── Story order: every structural card gets its part, sequence, scene and a running scene number ─────────────────────
const project = bw.projectCard(doc);
const pos = new Map(); // card id → { part, partTitle, seq, scene, sc, label }
let partN = 0, scN = 0, cur = { part: 0, partTitle: "", seq: "", scene: "", sc: 0 };
const order = [];
const walk = (c) => {
  const k = c.meta.kind;
  if (k === K_PART) { partN++; cur = { part: partN, partTitle: title(c), seq: "", scene: "", sc: scN }; }
  else if (k === K_SEQ) cur = { ...cur, seq: title(c), scene: "" };
  else if (k === K_SCENE) { scN++; cur = { ...cur, scene: title(c), sc: scN }; }
  if ([K_PART, K_SEQ, K_SCENE, K_BEAT, K_MICRO].includes(k)) {
    pos.set(c.id, { ...cur, sc: k === K_PART || k === K_SEQ ? scN + 1 : cur.sc });
    order.push(c);
  }
  for (const ch of c.children || []) walk(ch);
};
for (const ch of (project ? project.children : doc.cards.filter((c) => !c.parent))) walk(ch);
const where = (id) => { const p = pos.get(id); if (!p) return "unplaced"; return `P${p.part} · ${p.seq || p.partTitle}${p.scene ? ` › ${p.scene}` : ""}`; };
const scOf = (id) => (pos.get(id) || {}).sc || 0;
const scLabel = (n) => `sc ${String(n).padStart(3, "0")}`;
const sceneTitleByN = new Map(); for (const c of order) if (c.meta.kind === K_SCENE) sceneTitleByN.set(scOf(c.id), where(c.id));

// ── Arcs and their steps ──────────────────────────────────────────────────────────────────────────────────────────────
const cast = bw.castOf(doc);
const castName = new Map(cast.map((c) => [c.id, bw.castName(c)]));
const arcs = new Map(); // arc id → { id, name, owner, role, kind, meta }
for (const c of cast) for (const a of c.meta.arcs || []) arcs.set(a.id, { id: a.id, name: a.name, owner: bw.castName(c), role: a.model ? `${a.model.role}${a.model.set ? ` (${a.model.set})` : ""}` : "", kind: "character", meta: a });
for (const a of bw.plotArcs(doc)) arcs.set(a.id, { id: a.id, name: a.label || a.id, owner: a.goal_holder ? castName.get(a.goal_holder) || a.goal_holder : "", role: a.model ? `${a.model.role}${a.model.set ? ` (${a.model.set})` : ""}` : "subplot", kind: "plot", meta: a });
const steps = doc.cards.filter((c) => c.meta.kind === "arcbeat");
const placedOn = (st) => (st.parent && st.parent.meta.kind !== "project" && pos.has(st.parent.id) ? st.parent : null);
const stepArc = (st) => st.meta.plotArc || st.meta.arc || "";
const stepsOnCard = new Map(); for (const st of steps) { const p = placedOn(st); if (p) { if (!stepsOnCard.has(p.id)) stepsOnCard.set(p.id, []); stepsOnCard.get(p.id).push(st); } }

// ── Markers ───────────────────────────────────────────────────────────────────────────────────────────────────────────
const MARK = /^(held|body|bond|adage|hermit|audit) —/;
const markerClass = (t) => { t = one(t); if (/^held — hold the mystery:/.test(t)) return "keep-dark"; if (/^held — sources disagree:/.test(t)) return "sources-disagree"; const m = MARK.exec(t); return m ? (m[1] === "held" ? "held (other)" : m[1]) : ""; };
const isMarker = (c) => MARK.test(one(c.body)) || MARK.test(one(c.meta.label || ""));
const markerCards = doc.cards.filter((c) => c.meta.kind !== "project" && isMarker(c));

// ── outline-P<n>.md ───────────────────────────────────────────────────────────────────────────────────────────────────
mkdirSync(OUT, { recursive: true });
const eraNameOf = (id) => (id ? (bw.erasOf(doc).find((e) => e.id === id) || {}).name || id : "—");
// The tagging pass's offers (by: ai, never his): speaker / wants / states, shown after his words, marked as offers.
const aiNote = (c) => { const a = c.meta.ai; if (!a || typeof a !== "object") return ""; const p = []; if (a.speaker && !c.meta.speaker) p.push(`speaker? ${a.speaker}`); if (Array.isArray(a.wants) && a.wants.length) p.push(`wants? ${a.wants.join("; ")}`); if (Array.isArray(a.states) && a.states.length) p.push(`states? ${a.states.join("; ")}`); return p.length ? `  ‹ai offer: ${p.join(" · ")}›` : ""; };
const stepLine = (st) => {
  const a = arcs.get(stepArc(st)) || { name: stepArc(st) || "?", owner: "" };
  const mk = markerClass(st.body) || markerClass(st.meta.label || "");
  return `  - ${mk ? `⚑ ${mk} · ` : "◆ "}${a.name}${a.owner && a.kind === "character" ? ` (${a.owner})` : ""} s${st.meta.step ?? "?"}${st.meta.beat ? ` B${st.meta.beat}` : ""}${st.meta.label ? ` "${st.meta.label}"` : ""}${st.meta.plotLine ? ` on line ${st.meta.plotLine}` : ""} ^${st.id}: ${cut(st.body, 400) || "(empty)"}`;
};
const parts = order.filter((c) => c.meta.kind === K_PART);
const partFiles = [];
for (const p of parts) {
  const n = pos.get(p.id).part;
  const out = [`# Outline — P${n} · ${title(p)}`, "", `Story order. ◆ = an arc step placed here; ⚑ = a redraft marker. Ids are block ids.`, ""];
  const prose = [`# Prose — P${n} · ${title(p)}`, "", "One micro-beat per line: `sc NNN · ^id [type] words`. His words, verbatim; grep for a fact.", ""];
  const visit = (c) => {
    const k = c.meta.kind;
    const sts = stepsOnCard.get(c.id) || [];
    if (k === K_SEQ) {
      out.push(`## ${title(c)} ^${c.id}`);
      const f = ["chapter", "goal holder", "outcome", "shape", "serves arc"].filter((x) => F(c, x)).map((x) => `${x}: ${F(c, x)}`);
      if (f.length) out.push(f.join(" · "));
      if (F(c, "summary")) out.push(`> ${one(F(c, "summary"))}`);
      if (F(c, "story from") || F(c, "story to")) out.push(`from: ${one(F(c, "story from"))} → to: ${one(F(c, "story to"))}`);
      for (const st of sts) out.push(stepLine(st));
      out.push("");
    } else if (k === K_SCENE) {
      const sc = scOf(c.id);
      out.push(`### ${scLabel(sc)} · ${title(c)} ^${c.id}`);
      const f = ["goal holder", "outcome"].filter((x) => F(c, x)).map((x) => `${x}: ${F(c, x)}`);
      // The bible layer (world walk, 2026-10-22): the era the scene reads as, its flashback mark, its setting and the
      // world entries it links — so continuity and alignment can test against them.
      f.push(`era: ${eraNameOf(bw.eraIdAt(c))}${bw.isFlashback(c) ? " (flashback)" : ""}${c.meta.era ? "" : " (inherited)"}`);
      if (F(c, "setting")) f.push(`setting: ${F(c, "setting")}`);
      const wl = bw.cardWorldIds(c).map((id) => bw.findCard(doc, id)).filter(Boolean).map((w) => bw.worldName(w));
      if (wl.length) f.push(`links: ${wl.join(", ")}`);
      if (f.length) out.push(f.join(" · "));
      if (F(c, "summary")) out.push(`> ${one(F(c, "summary"))}`);
      if (F(c, "story from") || F(c, "story to")) out.push(`from: ${one(F(c, "story from"))} → to: ${one(F(c, "story to"))}`);
      for (const st of sts) out.push(stepLine(st));
      prose.push(`## ${scLabel(sc)} · ${title(c)} ^${c.id}`);
    } else if (k === K_BEAT) {
      out.push(`- ^${c.id} [${c.meta.type || "—"}] ${title(c)}${F(c, "summary") ? ` — ${one(F(c, "summary"))}` : ""}${isMarker(c) ? ` ⚑ ${markerClass(c.body)}` : ""}`);
      for (const st of sts) out.push(stepLine(st));
    } else if (k === K_MICRO) {
      prose.push(`${scLabel(scOf(c.id))} · ^${c.id} [${c.meta.type || "—"}${c.meta.speaker ? `: ${c.meta.speaker}` : ""}] ${one(c.body)}${aiNote(c)}`);
      for (const st of sts) out.push("  " + stepLine(st));
    } else if (k === K_PART) {
      if (sts.length) { out.push("Part-level steps:"); for (const st of sts) out.push(stepLine(st)); out.push(""); }
    }
    for (const ch of c.children || []) if (ch.meta.kind !== "arcbeat" && ch.meta.kind !== "idea") visit(ch);
  };
  visit(p);
  writeFileSync(`${OUT}/outline-P${n}.md`, out.join("\n") + "\n");
  writeFileSync(`${OUT}/prose-P${n}.md`, prose.join("\n") + "\n");
  partFiles.push({ n, title: title(p), scenes: order.filter((c) => c.meta.kind === K_SCENE && pos.get(c.id).part === n).length });
}

// ── arcs.md ───────────────────────────────────────────────────────────────────────────────────────────────────────────
const arcOut = ["# Arcs — every step in step order", "", `Silence = a stretch of more than ${GAP} scenes between two placed steps of one arc. Inversion = a step placed earlier in the story than a lower-numbered step of the same arc (sub-steps excluded). Both are facts for the checks, never findings on their own.`, ""];
const arcStats = [];
for (const a of arcs.values()) {
  const own = steps.filter((st) => stepArc(st) === a.id);
  if (!own.length && a.kind === "character") continue;
  const top = own.filter((st) => !st.meta.parentStep).sort((x, y) => (x.meta.step ?? 0) - (y.meta.step ?? 0));
  const subs = own.filter((st) => st.meta.parentStep);
  const m = a.meta;
  arcOut.push(`## ${a.name}${a.owner ? ` — ${a.owner}` : ""}${a.role ? ` · ${a.role}` : ""} (${a.kind}, ${a.id})`);
  const hdr = ["goal", "stakes", "planned_outcome", "outcome_detail", "planned_change"].filter((k) => m[k]).map((k) => `${k.replace("_", " ")}: ${one(m[k])}`);
  if (hdr.length) arcOut.push(hdr.join(" · "));
  const placedSc = [];
  for (const st of top) {
    const p = placedOn(st);
    const kids = subs.filter((x) => x.meta.parentStep === st.id);
    arcOut.push(`- s${st.meta.step ?? "?"}${st.meta.beat ? ` B${st.meta.beat}` : ""}${st.meta.label ? ` "${st.meta.label}"` : ""} ^${st.id} @ ${p ? `${scLabel(scOf(p.id))} ${where(p.id)}` : `UNPLACED${st.meta.hint ? ` (${one(st.meta.hint)})` : ""}`}: ${cut(st.body, 300) || "(empty)"}`);
    for (const k of kids) { const kp = placedOn(k); arcOut.push(`  - sub ^${k.id} @ ${kp ? `${scLabel(scOf(kp.id))} ${where(kp.id)}` : "UNPLACED"}: ${cut(k.body, 240)}`); if (kp) placedSc.push(scOf(kp.id)); }
    if (p) placedSc.push(scOf(p.id));
  }
  const inv = [];
  let maxSc = 0, maxStep = null;
  for (const st of top) { const p = placedOn(st); if (!p) continue; const sc = scOf(p.id); if (sc < maxSc) inv.push(`s${st.meta.step} (${scLabel(sc)}) sits before s${maxStep} (${scLabel(maxSc)})`); if (sc >= maxSc) { maxSc = sc; maxStep = st.meta.step; } }
  const sorted = [...new Set(placedSc)].sort((x, y) => x - y);
  const gaps = [];
  for (let i = 1; i < sorted.length; i++) if (sorted[i] - sorted[i - 1] > GAP) gaps.push(`${scLabel(sorted[i - 1])} → ${scLabel(sorted[i])} (${sorted[i] - sorted[i - 1]} scenes: ${sceneTitleByN.get(sorted[i - 1]) || "?"} → ${sceneTitleByN.get(sorted[i]) || "?"})`);
  const unplaced = top.filter((st) => !placedOn(st)).length, empty = own.filter((st) => !st.body.trim()).length;
  arcOut.push(`facts: ${top.length} steps (${subs.length} sub-steps), ${unplaced} unplaced, ${empty} empty; spans ${sorted.length ? `${scLabel(sorted[0])}–${scLabel(sorted[sorted.length - 1])}` : "—"}`);
  if (inv.length) arcOut.push(`inversions: ${inv.join("; ")}`);
  if (gaps.length) arcOut.push(`silences: ${gaps.join("; ")}`);
  arcOut.push("");
  arcStats.push({ arc: a.name, kind: a.kind, steps: top.length, unplaced, inversions: inv.length, silences: gaps.length });
}
writeFileSync(`${OUT}/arcs.md`, arcOut.join("\n") + "\n");

// ── markers.md ────────────────────────────────────────────────────────────────────────────────────────────────────────
const byClass = new Map();
for (const c of markerCards) { const k = markerClass(c.body) || markerClass(c.meta.label || ""); if (!byClass.has(k)) byClass.set(k, []); byClass.get(k).push(c); }
const mkOut = ["# Redraft markers", "", "His placeholders: known, held gaps. Keep-dark ones are design. The audit never re-reports a marker; it checks whether the board has since answered one (a leaked mystery, for keep-dark).", ""];
for (const [k, list] of [...byClass.entries()].sort()) {
  mkOut.push(`## ${k} (${list.length})`);
  for (const c of list) { const p = c.meta.kind === "arcbeat" ? placedOn(c) : c; const a = c.meta.kind === "arcbeat" ? arcs.get(stepArc(c)) : null; mkOut.push(`- ^${c.id}${a ? ` (${a.name}${c.meta.label ? ` · ${c.meta.label}` : ""})` : ""} @ ${p ? `${scLabel(scOf(p.id))} ${where(p.id)}` : "UNPLACED"}: ${one(c.body)}`); }
  mkOut.push("");
}
writeFileSync(`${OUT}/markers.md`, mkOut.join("\n") + "\n");

// ── alignment.md (the approved plan against the board) ────────────────────────────────────────────────────────────────
const alOut = ["# Alignment — the plan against the board", ""];
let alCounts = null;
if (arg("--plan")) {
  const pt = readFileSync(abs(arg("--plan")), "utf8");
  const blocks = [...pt.matchAll(/```json\r?\n([\s\S]*?)\r?\n```/g)];
  if (!blocks.length) die("no JSON record in the plan");
  const plan = JSON.parse(blocks[blocks.length - 1][1]);
  const fm = /^---\r?\n([\s\S]*?)\r?\n---/.exec(pt);
  alOut.push(`Plan: ${arg("--plan")} · status ${(/status:\s*(\S+)/.exec(fm ? fm[1] : "") || [])[1] || "?"} · approved ${plan.approved ? (plan.approved.date || JSON.stringify(plan.approved)) + (plan.approved.phrase ? ` ("${plan.approved.phrase}")` : "") : "?"}`, "");
  const stepByText = new Map(); for (const st of steps) if (st.body.trim()) { const k = norm(st.body); if (!stepByText.has(k)) stepByText.set(k, []); stepByText.get(k).push(st); }
  const boardText = norm(doc.cards.filter((c) => c.meta.kind !== "arcbeat").map((c) => c.body).join("\n"));
  const citeIds = (b) => [...(b.cards || []), ...(b.support || []).map((x) => (/^\[(\w{6})\]/.exec(x) || [])[1]), ...((/board cards? ([\w, ]+)/.exec(b.src || "") || [, ""])[1].split(",").map((x) => x.trim()))].filter((x) => /^\w{6}$/.test(x || ""));
  const missing = [], moved = [], goneCards = [];
  const cells = [
    ...(plan.beats || []).map((b) => ({ where: `main B${b.n} ${b.spine}`, ...b })),
    ...(plan.spines || []).flatMap((sp) => (sp.beats || []).map((b) => ({ where: `${sp.name || sp.key} B${b.n} ${b.spine}`, ...b }))),
    ...(plan.subplots || []).flatMap((sp) => (sp.steps || []).map((b, i) => ({ where: `${sp.label} s${i + 1}${b.label ? ` "${b.label}"` : ""}`, subplot: sp.label, ...b }))),
  ].filter((b) => (b.text || "").trim());
  for (const b of cells) {
    const hit = stepByText.get(norm(b.text));
    if (!hit) { missing.push(`- ${b.where}: "${cut(b.text, 200)}"${boardText.includes(norm(b.text)) ? " — the words are on a board card, but no step carries them" : ""}`); continue; }
    for (const id of citeIds(b)) if (!bw.findCard(doc, id)) goneCards.push(`- ${b.where}: cites ^${id}, which is not on the board`);
    const ids = citeIds(b).filter((id) => bw.findCard(doc, id));
    if (!ids.length) continue;
    const citedSc = new Set(ids.map(scOf));
    for (const st of hit) { const p = placedOn(st); if (p && !citedSc.has(scOf(p.id))) moved.push(`- ${b.where}: step ^${st.id} sits at ${scLabel(scOf(p.id))} ${where(p.id)}; the plan cites ${ids.map((id) => `^${id} (${scLabel(scOf(id))})`).join(", ")}`); }
  }
  const planSub = new Set((plan.subplots || []).map((x) => norm(x.label)));
  const boardPlot = [...arcs.values()].filter((a) => a.kind === "plot" && a.role === "subplot");
  const onlyBoard = boardPlot.filter((a) => !planSub.has(norm(a.name))).map((a) => `- on the board, not in the plan: "${a.name}" (${a.id})`);
  const onlyPlan = (plan.subplots || []).filter((x) => !boardPlot.some((a) => norm(a.name) === norm(x.label))).map((x) => `- in the plan, not on the board: "${x.label}" (${x.status || "?"})`);
  const countDiff = (plan.subplots || []).map((x) => { const a = boardPlot.find((b) => norm(b.name) === norm(x.label)); if (!a) return null; const n = steps.filter((st) => stepArc(st) === a.id && !st.meta.parentStep).length; return n !== (x.steps || []).length ? `- "${x.label}": plan ${x.steps.length} steps, board ${n}` : null; }).filter(Boolean);
  const planTexts = new Set(cells.map((b) => norm(b.text)));
  // sub-steps (split-step, one per scene line) carry their own words from the cards, never a plan cell: not drift
  const boardOnly = steps.filter((st) => st.body.trim() && !st.meta.parentStep && !isMarker(st) && !planTexts.has(norm(st.body))).map((st) => { const a = arcs.get(stepArc(st)) || { name: "?" }; const p = placedOn(st); return `- ${a.name} s${st.meta.step ?? "?"} ^${st.id} @ ${p ? scLabel(scOf(p.id)) : "UNPLACED"}: "${cut(st.body, 160)}"`; });
  const sec = (h, list) => { alOut.push(`## ${h} (${list.length})`, ...(list.length ? list : ["- none"]), ""); };
  sec("Subplots on one side only", [...onlyBoard, ...onlyPlan]);
  sec("Subplot step counts that differ", countDiff);
  sec("Plan words no step on the board carries (edited on the board, or never built)", missing);
  sec("Steps sitting in another scene than the card their plan cell cites", moved);
  sec("Plan cells citing a card that is gone", goneCards);
  sec("Board steps whose words are not in the plan (added or edited on the board since approval; markers excluded)", boardOnly);
  alCounts = { cells: cells.length, missing: missing.length, moved: moved.length, gone: goneCards.length, onlyBoard: onlyBoard.length, onlyPlan: onlyPlan.length, countDiff: countDiff.length, boardOnly: boardOnly.length };
} else alOut.push("No plan given (--plan): alignment not crawled.");
writeFileSync(`${OUT}/alignment.md`, alOut.join("\n") + "\n");

// ── names.md (mentions and silences) ──────────────────────────────────────────────────────────────────────────────────
const textCards = order.filter((c) => [K_BEAT, K_MICRO].includes(c.meta.kind)).map((c) => ({ id: c.id, sc: scOf(c.id), t: ` ${norm(c.body + " " + F(c, "summary"))} ` }));
for (const st of steps) { const p = placedOn(st); if (p && !isMarker(st)) textCards.push({ id: st.id, sc: scOf(p.id), t: ` ${norm(st.body)} ` }); }
const esc = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const entities = [
  ...cast.map((c) => ({ kind: "cast", name: bw.castName(c), aliases: bw.castAliases(c) })),
  ...bw.worldOf(doc).map((c) => ({ kind: bw.worldKindOf(c), name: bw.worldName(c), aliases: bw.worldAliases(c) })),
];
const nmOut = ["# Names — mentions and silences", "", `Mentions in beat titles and summaries, micro-beats and placed arc steps (markers excluded), by whole-word match on the name and its aliases, case-insensitive. A silence is more than ${GAP} scenes without a mention. A name the prose never uses (a role, a nickname) reads silent: check before calling anything missing.`, ""];
const totalSc = scN;
for (const e of entities) {
  const forms = [e.name, ...(e.aliases || [])].map(norm).filter((x) => x.length > 2);
  if (!forms.length) continue;
  const re = new RegExp(`(?<![a-z0-9])(${forms.map(esc).join("|")})(?![a-z0-9])`);
  const hits = [...new Set(textCards.filter((x) => re.test(x.t)).map((x) => x.sc))].filter(Boolean).sort((a, b) => a - b);
  const perPart = parts.map((p) => { const n = pos.get(p.id).part; return `P${n} ${hits.filter((h) => sceneTitleByN.get(h)?.startsWith(`P${n} `)).length}`; }).join(" · ");
  const gaps = [];
  for (let i = 1; i < hits.length; i++) if (hits[i] - hits[i - 1] > GAP) gaps.push([hits[i - 1], hits[i]]);
  gaps.sort((a, b) => (b[1] - b[0]) - (a[1] - a[0]));
  nmOut.push(`## ${e.name}${e.aliases && e.aliases.length ? ` (${e.aliases.join(", ")})` : ""} · ${e.kind}`);
  nmOut.push(hits.length ? `${hits.length} of ${totalSc} scenes · first ${scLabel(hits[0])} ${sceneTitleByN.get(hits[0])} · last ${scLabel(hits[hits.length - 1])} ${sceneTitleByN.get(hits[hits.length - 1])} · ${perPart}` : "never mentioned by name");
  for (const [a, b] of gaps.slice(0, 4)) nmOut.push(`- silent ${b - a - 1} scenes: after ${scLabel(a)} ${sceneTitleByN.get(a)} until ${scLabel(b)} ${sceneTitleByN.get(b)}`);
  nmOut.push("");
}
writeFileSync(`${OUT}/names.md`, nmOut.join("\n") + "\n");

// ── repeats.md (repeated phrases in his words; near-twin beat summaries) ──────────────────────────────────────────────
const micros = order.filter((c) => c.meta.kind === K_MICRO && !isMarker(c)).map((c) => ({ id: c.id, sc: scOf(c.id), toks: norm(c.body).replace(/[^a-z0-9' ]+/g, " ").split(" ").filter(Boolean) }));
const gramSc = new Map();
for (const m of micros) for (let i = 0; i + GRAM <= m.toks.length; i++) { const g = m.toks.slice(i, i + GRAM).join(" "); if (!gramSc.has(g)) gramSc.set(g, new Set()); gramSc.get(g).add(m.sc); }
const runs = new Map(); // phrase → Set of "sc|id"
for (const m of micros) {
  let i = 0;
  while (i + GRAM <= m.toks.length) {
    const rep = (j) => j + GRAM <= m.toks.length && gramSc.get(m.toks.slice(j, j + GRAM).join(" ")).size > 1;
    if (!rep(i)) { i++; continue; }
    let j = i; while (rep(j + 1)) j++;
    const phrase = m.toks.slice(i, j + GRAM).join(" ");
    if (!runs.has(phrase)) runs.set(phrase, new Set());
    runs.get(phrase).add(`${m.sc}|${m.id}`);
    i = j + GRAM;
  }
}
// a phrase's occurrences: every micro whose tokens contain it
const microJoined = micros.map((m) => ({ ...m, j: ` ${m.toks.join(" ")} ` }));
const repList = [];
const seenPhrase = new Set();
for (const phrase of [...runs.keys()].sort((a, b) => b.length - a.length)) {
  if ([...seenPhrase].some((p) => p.includes(phrase))) continue;
  const occ = microJoined.filter((m) => m.j.includes(` ${phrase} `));
  const scs = [...new Set(occ.map((m) => m.sc))];
  if (scs.length < 2) continue;
  seenPhrase.add(phrase);
  repList.push({ phrase, n: phrase.split(" ").length, occ });
}
repList.sort((a, b) => b.occ.length - a.occ.length || b.n - a.n);
const STOP = new Set("the a an and or but of to in on at by for with from as is was were be been it its he she his her him they them their i you we me my your our that this then than there not no so if into out up down over under what who when where how all just like".split(" "));
const words = (t) => new Set(norm(t).replace(/[^a-z0-9' ]+/g, " ").split(" ").filter((w) => w.length > 2 && !STOP.has(w)));
const beats = order.filter((c) => c.meta.kind === K_BEAT && F(c, "summary")).map((c) => ({ id: c.id, sc: scOf(c.id), t: title(c), s: one(F(c, "summary")), w: words(F(c, "summary")) }));
const twins = [];
for (let i = 0; i < beats.length; i++) for (let j = i + 1; j < beats.length; j++) {
  const a = beats[i], b = beats[j];
  if (a.sc === b.sc || a.w.size < 5 || b.w.size < 5) continue;
  let inter = 0; for (const w of a.w) if (b.w.has(w)) inter++;
  const jac = inter / (a.w.size + b.w.size - inter);
  if (jac >= TWIN) twins.push({ jac, a, b });
}
twins.sort((x, y) => y.jac - x.jac);
const dupTitles = [...beats.reduce((m, b) => m.set(norm(b.t), [...(m.get(norm(b.t)) || []), b]), new Map()).values()].filter((l) => new Set(l.map((x) => x.sc)).size > 1);
const rpOut = ["# Repeats — candidates", "", `Phrases of ${GRAM}+ words that recur in his micro-beats in more than one scene, longest first within the same count, and beat summaries that read as near twins (content-word overlap ≥ ${TWIN}) or share a title. Candidates only: a refrain, the adage, a callback or a ritual is repetition on purpose — the check decides, never this list.`, ""];
rpOut.push(`## Repeated phrases (${repList.length})`);
for (const r of repList.slice(0, 250)) rpOut.push(`- "${r.phrase}" ×${r.occ.length}: ${r.occ.slice(0, 8).map((m) => `${scLabel(m.sc)} ^${m.id}`).join(", ")}${r.occ.length > 8 ? ", …" : ""}`);
if (repList.length > 250) rpOut.push(`- … ${repList.length - 250} more (shorter or rarer)`);
rpOut.push("", `## Near-twin beat summaries (${twins.length})`);
for (const t of twins.slice(0, 150)) rpOut.push(`- ${t.jac.toFixed(2)} · ${scLabel(t.a.sc)} ^${t.a.id} "${t.a.t}": ${t.a.s}\n  ${scLabel(t.b.sc)} ^${t.b.id} "${t.b.t}": ${t.b.s}`);
rpOut.push("", `## Beat titles used in more than one scene (${dupTitles.length})`);
for (const l of dupTitles) rpOut.push(`- "${l[0].t}": ${l.map((b) => `${scLabel(b.sc)} ^${b.id}`).join(", ")}`);
writeFileSync(`${OUT}/repeats.md`, rpOut.join("\n") + "\n");

// ── bible.md (the world walk's layer: timeline, places, seeds, events, profiles, offered states) ──────────────────────
const bbOut = ["# Bible layer — what the board's side panels say", "", "Facts for the checks, never findings. Eras, settings, seeds, pins and profiles were ruled by him (world walk); `‹ai offer›` lines are the tagging pass's offers, not his.", ""];
const scenesInOrder = order.filter((c) => c.meta.kind === K_SCENE);
const setting = (c) => F(c, "setting");
bbOut.push("## Timeline — every scene, story order", "", "`sc · era (fb = flashback) · setting · title`", "");
for (const c of scenesInOrder) bbOut.push(`- ${scLabel(scOf(c.id))} · ${eraNameOf(bw.eraIdAt(c))}${bw.isFlashback(c) ? " (fb)" : ""} · ${setting(c) || "—"} · ${title(c)} ^${c.id}`);
// Place jumps: consecutive present (non-flashback) scenes, both set, in different places — continuity reads whether the travel is shown.
const present = scenesInOrder.filter((c) => !bw.isFlashback(c) && setting(c));
const jumps = [];
for (let i = 1; i < present.length; i++) if (setting(present[i]) !== setting(present[i - 1])) jumps.push(`- ${scLabel(scOf(present[i - 1].id))} ${setting(present[i - 1])} → ${scLabel(scOf(present[i].id))} ${setting(present[i])} (${title(present[i])} ^${present[i].id})`);
bbOut.push("", `## Place changes between consecutive present scenes (${jumps.length})`, "", "Each is a move the story makes; check the travel is on the page or meant to be off it.", "", ...jumps);
// Era turns in the present.
const turns = []; let lastEra = "";
for (const c of scenesInOrder) { if (bw.isFlashback(c)) continue; const e = bw.eraIdAt(c); if (e !== lastEra) { turns.push(`- ${scLabel(scOf(c.id))} → ${eraNameOf(e)} (${title(c)})`); lastEra = e; } }
bbOut.push("", "## Where the present's era turns", "", ...turns);
// Seeds.
const seeds = bw.seedCheck ? bw.seedCheck(doc) : [];
const cardLine = (k) => `${scLabel(scOf(k.id) || scOf(k.parent?.id || ""))} ^${k.id} "${cut(k.body, 120)}"`;
bbOut.push("", `## Seed check (${seeds.length} threads: ${["paid", "open", "backwards", "orphan"].map((s) => `${seeds.filter((r) => r.status === s).length} ${s}`).join(", ")})`, "", "Open = planted, no payoff tagged yet: a candidate dangling plant to confirm against the prose. Backwards = a payoff before its plant.", "");
for (const r of seeds) bbOut.push(`- **${r.name}** — ${r.status} · seed ${r.seeds.map(cardLine).join(" | ") || "—"}${r.payoffs.length ? ` · payoff ${r.payoffs.map(cardLine).join(" | ")}` : ""}`);
// Events.
const evs = bw.eventsOf(doc);
bbOut.push("", `## Events (${evs.filter((e) => e.at).length} of ${evs.length} pinned)`, "", "A pinned event's era should match its card's era; a mismatch is listed.", "");
for (const e of evs) { const at = e.at ? bw.findCard(doc, e.at) : null; const cardEra = at ? bw.eraIdAt(at) : ""; bbOut.push(`- ${bw.eventLabel(doc, e)} · ${eraNameOf(e.era)}${at ? ` · on ${scLabel(scOf(at.id))} ${title(at)} ^${at.id}${cardEra !== e.era ? ` ⚠ card reads ${eraNameOf(cardEra)}` : ""}` : " · unpinned"}`); }
// Profiles.
bbOut.push("", "## Cast profiles (his ruled answers; checks test actions against want, need, flaw, wound)", "");
for (const c of cast) { const f = c.meta.fields || {}; const keys = ["role", "want", "need", "flaw", "wound", "personality"].filter((k) => f[k]); bbOut.push(`- **${bw.castName(c)}**${keys.length ? ": " + keys.map((k) => `${k}: ${one(f[k])}`).join(" · ") : " — no profile"}`); }
// Offered states and wants, per character, in story order.
const byChar = new Map();
for (const c of order) { const a = c.meta.ai; if (!a || typeof a !== "object") continue; for (const [kind, list] of [["state", a.states], ["want", a.wants]]) for (const s of Array.isArray(list) ? list : []) { const m = /^([^:]+):\s*(.+)$/.exec(String(s)); const who = m ? m[1].trim() : "?"; if (!byChar.has(who)) byChar.set(who, []); byChar.get(who).push(`${scLabel(scOf(c.id))} ${kind}: ${m ? m[2] : s} ^${c.id}`); } }
bbOut.push("", "## Offered state changes and wants, per character (‹ai offer›, story order)", "", "A state that reverses with nothing between, or a want that vanishes, is a continuity or meaning lead — confirm in the prose.", "");
for (const [who, l] of [...byChar.entries()].sort((a, b) => b[1].length - a[1].length)) bbOut.push(`### ${who} (${l.length})`, ...l.map((x) => `- ${x}`), "");
// World entries.
bbOut.push("## World entries", "");
for (const w of bw.worldOf(doc)) { const linked = scenesInOrder.filter((c) => bw.cardWorldIds(c).includes(w.id)).length; const set = scenesInOrder.filter((c) => setting(c) && bw.allWorldNames(w).some((n) => n.toLowerCase() === setting(c).toLowerCase())).length; bbOut.push(`- **${bw.worldName(w)}** (${bw.worldKindOf(w)}) · linked from ${linked} scenes${set ? ` · setting of ${set}` : ""} — ${cut((w.meta.fields || {}).description || "", 200)}`); }
writeFileSync(`${OUT}/bible.md`, bbOut.join("\n") + "\n");

// ── README.md ─────────────────────────────────────────────────────────────────────────────────────────────────────────
const count = (k) => order.filter((c) => c.meta.kind === k).length;
const readme = [
  `# Audit crawl — ${boardPath}`, "",
  `Crawled ${new Date().toISOString().slice(0, 16).replace("T", " ")} UTC · ${doc.cards.length} cards · ${parts.length} parts, ${count(K_SEQ)} sequences, ${totalSc} scenes, ${count(K_BEAT)} beats, ${count(K_MICRO)} micro-beats · ${steps.length} arc steps on ${arcStats.length} arcs · ${markerCards.length} markers · ${bw.placedIdeas(doc).length} placed ideas, ${bw.inboxIdeas(doc).length} in the inbox.`, "",
  "| File | Holds |", "|---|---|",
  ...partFiles.map((p) => `| outline-P${p.n}.md · prose-P${p.n}.md | ${p.title} (${p.scenes} scenes) |`),
  `| arcs.md | ${arcStats.length} arcs: ${arcStats.reduce((a, x) => a + x.unplaced, 0)} unplaced steps, ${arcStats.reduce((a, x) => a + x.inversions, 0)} order inversions, ${arcStats.reduce((a, x) => a + x.silences, 0)} silences > ${GAP} scenes |`,
  `| markers.md | ${[...byClass.entries()].map(([k, l]) => `${k} ${l.length}`).join(" · ")} |`,
  `| alignment.md | ${alCounts ? `${alCounts.cells} plan cells: ${alCounts.missing} not carried by a step, ${alCounts.moved} in another scene than cited, ${alCounts.gone} citing a gone card; subplots on one side only ${alCounts.onlyBoard + alCounts.onlyPlan}; count differences ${alCounts.countDiff}; board-only step words ${alCounts.boardOnly}` : "not crawled (no --plan)"} |`,
  `| names.md | ${entities.length} cast and world entries |`,
  `| bible.md | the side panels: timeline (${scenesInOrder.filter((c) => setting(c)).length}/${scenesInOrder.length} scenes set), ${jumps.length} place changes, ${turns.length} era turns, ${seeds.length} seed threads (${seeds.filter((r) => r.status === "open").length} open), ${evs.filter((e) => e.at).length}/${evs.length} events pinned, ${cast.length} profiles, offered states/wants for ${byChar.size} characters |`,
  `| repeats.md | ${repList.length} repeated phrases · ${twins.length} near-twin beat summaries · ${dupTitles.length} shared beat titles |`, "",
  "## What this crawl does not check",
  ...(() => { const thin = partFiles.filter((p) => order.filter((c) => c.meta.kind === K_MICRO && pos.get(c.id).part === p.n).length < 10).map((p) => `P${p.n}`); return thin.length ? [`- His prose in ${thin.join(", ")}: those parts carry beats and summaries but (almost) no micro-beats, so continuity, names and repeats there rest on summaries, not his words. Confirm a finding there against DEV or the landed chapters.`] : []; })(),
  "- Meaning. Every list here is a fact about the board, never a finding: a silence can be design, a repeat can be a refrain, an inversion can be a flashback.",
  "- POV strands. The board carries no `pov` field; the scene and sequence `goal holder` is the nearest proxy, and the outlines show it. Read every lead's strand before calling something missing.",
  "- Mentions by pronoun, description or role (\"she\", \"the old man\"): names.md matches names and aliases only.",
  "- Repeats under " + GRAM + " words, and repeated images said in different words.",
  "- Placed ideas (his idea cards on a card's tray) are counted, not crawled.",
  "- bible.md's place changes compare scene settings only: a scene with no setting (left blank by his ruling) breaks the chain, and travel inside one place isn't seen. Offered states and wants are a reader's offers, not his words; seed status reflects the tags, not the prose.",
  "- The model structure (beat order across spines, collisions, open blanks): that is `check-board.mjs`.",
];
writeFileSync(`${OUT}/README.md`, readme.join("\n") + "\n");
console.log(readme.slice(2, 4 + partFiles.length + 6).join("\n"));
console.log(`→ ${OUT}`);
