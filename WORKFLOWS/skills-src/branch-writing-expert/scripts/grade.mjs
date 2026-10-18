// branch-writing-expert grader (^obs-442): "every word given is on the board, and nothing else" — plus the mechanical
// criteria of each mode — graded by a script against a run the author didn't drive. Writes grading.json in the shape the
// skill-creator viewer reads ({expectations: [{text, passed, evidence}]}).
//
//   node grade.mjs --mode direct|ideas|tagging|import|bible|version --after <board.md> [--before <board.md>] [--given <given.json>]
//                  [--log <board log.md>] [--orig <board>] [--undo <board after undo>] [--redo <board after redo>]
//                  [--sources a.md,b.md --source-hashes <sha.json>] [--run-output <text file>] --out <grading.json>
//
// given.json: {"given": ["CRE's strings…"], "allowed": ["other strings that may appear (ids, labels)"],
//              "placed": {"idea text": "card title"}, "inbox": ["idea text"], "approved": {"cast": [...], "dialogue": [...],
//              "chapters": {"title": "N"}, "scenes": N}}
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { createHash } from "node:crypto";
for (const st of [process.stdout, process.stderr]) try { st.setDefaultEncoding("utf8"); } catch {}
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const WIN = process.platform === "win32";
const HOME = process.env.USERPROFILE || process.env.HOME || "";
const VAULT = arg("--vault", WIN ? "C:/Users/Chad/Dropbox/razorblade_mermaid" : `${HOME}/Dropbox/razorblade_mermaid`).replace(/\\/g, "/");
const DEV = arg("--dev", WIN ? "C:/Users/Chad/dev/branch-writing" : `${HOME}/dev/branch-writing`).replace(/\\/g, "/");
const bw = await import(pathToFileURL(`${DEV}/test/core.mjs`).href);
const abs = (p) => { if (!p) return p; p = p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`); if (/^[A-Za-z]:|^\//.test(p)) return p.replace(/\\/g, "/"); const cwd = `${process.cwd().replace(/\\/g, "/")}/${p}`; return existsSync(cwd) || !existsSync(`${VAULT}/${p}`) ? cwd : `${VAULT}/${p}`; };
const sha = (s) => createHash("sha256").update(typeof s === "string" ? Buffer.from(s, "utf8") : s).digest("hex");
const read = (p) => readFileSync(abs(p), "utf8");
const mode = arg("--mode", "direct");
const exp = [];
const check = (text, passed, evidence) => exp.push({ text, passed: !!passed, evidence: String(evidence ?? "").slice(0, 600) });
const finish = () => {
  const outp = arg("--out", "grading.json");
  const summary = { passed: exp.filter((x) => x.passed).length, failed: exp.filter((x) => !x.passed).length, total: exp.length };
  writeFileSync(abs(outp), JSON.stringify({ mode, expectations: exp, summary }, null, 2), "utf8");
  console.log(`${mode}: ${summary.passed}/${summary.total} passed`);
  for (const x of exp.filter((e) => !e.passed)) console.log("  FAIL " + x.text + " — " + x.evidence.slice(0, 240));
  process.exit(summary.failed ? 1 : 0);
};
const seg = (c) => (c.rawMarker ?? "") + (c.innerRaw ?? "") + (c.rawEnd ?? "");
const title = (c) => (c.body || "").split("\n")[0].trim();
const norm = (s) => String(s || "").toLowerCase().replace(/\s+/g, " ").trim();
const G = arg("--given") ? JSON.parse(read(arg("--given"))) : {};
const given = (G.given || []).map(String);
const allowed = new Set((G.allowed || []).map(String));

// ── Version mode: the run went read-only and the board is untouched ───────────────────────────────────────────────────
if (mode === "version") {
  const outText = arg("--run-output") ? read(arg("--run-output")) : "";
  check("the run said plainly that it was read-only (version check)", /READ-ONLY|read-only/.test(outText), outText.slice(0, 300));
  check("the run named what to read first", /read first|readFirst/i.test(outText), outText.match(/read first[^\n]*|"readFirst"[\s\S]{0,160}/i)?.[0] || "");
  if (arg("--after") && arg("--orig")) check("the board is byte-identical to its copy before the run", read(arg("--after")) === read(arg("--orig")), `${sha(read(arg("--after"))).slice(0, 8)} vs ${sha(read(arg("--orig"))).slice(0, 8)}`);
  finish();
}

const afterText = read(arg("--after"));
const after = bw.parse(afterText);
const s = bw.settingsOf(after);
check("the board reads back byte-identical through the plugin's serializer (parse gate)", bw.serialize(after) === afterText);
const before = arg("--before") && existsSync(abs(arg("--before"))) ? bw.parse(read(arg("--before"))) : null;
const beforeMap = new Map((before ? before.cards : []).map((c) => [c.id, c]));
const afterMap = new Map(after.cards.map((c) => [c.id, c]));

// ── The run's log: which cards it claims to have touched ─────────────────────────────────────────────────────────────
let runs = [];
if (arg("--log") && existsSync(abs(arg("--log")))) runs = [...read(arg("--log")).matchAll(/```json\r?\n([\s\S]*?)\r?\n```/g)].map((m) => { try { return JSON.parse(m[1]); } catch { return null; } }).filter(Boolean);
const touchedIds = new Set(runs.flatMap((r) => (r.cards || []).map((c) => c.id)));
const runLabels = runs.map((r) => `${r.id} (${r.status}): ${(r.cards || []).length} cards`);

// ── Every word given is on the board ─────────────────────────────────────────────────────────────────────────────────
const leaves = [];
(function walk(v, path) { if (v == null) return; if (typeof v === "string") leaves.push({ path, v }); else if (Array.isArray(v)) v.forEach((x, i) => walk(x, `${path}[${i}]`)); else if (typeof v === "object") for (const [k, x] of Object.entries(v)) walk(x, `${path}.${k}`); })(after.cards.map((c) => ({ id: c.id, meta: c.meta, body: c.body })), "");
const haystack = leaves.map((l) => l.v);
const onBoard = (g) => afterText.includes(g) || haystack.some((h) => h === g || h.includes(g));
if (given.length) { const missing = given.filter((g) => !onBoard(g)); check(`every string CRE gave is on the board (${given.length} given)`, !missing.length, missing.length ? "missing: " + JSON.stringify(missing.slice(0, 5)) : "all present"); }

// ── …and nothing else: every new string leaf is explained ────────────────────────────────────────────────────────────
const STRUCT_KEYS = new Set(["kind", "wkind", "by", "era", "cast", "arc", "plotArc", "step", "label", "hint", "parentStep", "id", "to", "of", "at", "parent", "from", "color", "offered", "role", "against", "proseSha256", "rel"]); // rel: a by: ai link's relation label (echoes, pays off…) is the offer's own label, not story text
const ids = new Set(after.cards.map((c) => c.id));
const eraIds = new Set(bw.erasOf(after).map((e) => e.id));
const vocab = new Set([...(s.ideaTypes || bw.defaultIdeaTypes()), ...(s.beatTypes || []), ...s.levels.map((l) => l.key), ...s.levels.flatMap((l) => l.types || []), ...(s.customTypes || []).map((c) => c.key), ...bw.worldKinds(s).map((k) => k.key), ...bw.relationTypes(after).flatMap((t) => [t.name, t.inverse || ""]), "ai", "cre", "true", "false", "branch-writing"]);
const explained = (v, path) => {
  if (!v.trim()) return true;
  if (given.includes(v) || allowed.has(v)) return true;
  if (given.some((g) => v.endsWith(g) && /^[a-z]+:$/.test(v.slice(0, v.length - g.length)))) return true; // char:<given name>
  if (vocab.has(v) || ids.has(v) || eraIds.has(v) || /^(rel|era|arc|parc|stg|evt)-[a-z0-9]+$/.test(v) || /^\[\[#?\^?[A-Za-z0-9-]+\]\]$/.test(v)) return true;
  if (/^\d{4}-\d{2}-\d{2}/.test(v) || /^-?\d+(\.\d+)?$/.test(v) || /^[a-f0-9]{64}$/.test(v)) return true;
  if (/\.(profile|arcFields)\b/.test(path) && /\.(name|desc)$/.test(path)) return true; // profile field definitions, not answers
  if (/\.settings\./.test(path)) return true; // the Project card's settings (switching plotting on appends field templates)
  if (before && beforeLeaves.has(v)) return true; // a string the board already held (a label, a name) reused as a value
  return false;
};
const beforeLeaves = new Set();
if (before) (function walk(v) { if (v == null) return; if (typeof v === "string") beforeLeaves.add(v); else if (Array.isArray(v)) v.forEach(walk); else if (typeof v === "object") Object.values(v).forEach(walk); })(before.cards.map((c) => ({ meta: c.meta, body: c.body })));
if (before) {
  const newLeaves = [];
  for (const c of after.cards) {
    const b = beforeMap.get(c.id);
    if (b && seg(b) === seg(c)) continue;
    const bl = new Set(); if (b) (function walk(v) { if (v == null) return; if (typeof v === "string") bl.add(v); else if (Array.isArray(v)) v.forEach(walk); else if (typeof v === "object") Object.values(v).forEach(walk); })({ meta: b.meta, body: b.body });
    (function walk(v, path) { if (v == null) return; if (typeof v === "string") { if (!bl.has(v)) newLeaves.push({ id: c.id, path, v }); } else if (Array.isArray(v)) v.forEach((x, i) => walk(x, `${path}[${i}]`)); else if (typeof v === "object") for (const [k, x] of Object.entries(v)) { if (STRUCT_KEYS.has(k) && typeof x === "string") continue; walk(x, `${path}.${k}`); } })({ meta: c.meta, body: c.body }, "");
  }
  const unexplained = newLeaves.filter((l) => !explained(l.v, l.path));
  check(`nothing else: every new string on the board is CRE's words or board vocabulary (${newLeaves.length} new strings)`, !unexplained.length, unexplained.length ? "unexplained: " + JSON.stringify(unexplained.slice(0, 6)) : "all explained");
  // Untouched cards byte-identical
  const changed = [...beforeMap.values()].filter((b) => !afterMap.get(b.id) || seg(afterMap.get(b.id)) !== seg(b)).map((b) => b.id);
  const added = after.cards.filter((c) => !beforeMap.has(c.id)).map((c) => c.id);
  if (runs.length) { const outside = [...changed, ...added].filter((id) => !touchedIds.has(id)); check(`every card outside the run's log is byte-identical (${changed.length} changed, ${added.length} added, ${touchedIds.size} logged)`, !outside.length, outside.length ? "changed but not logged: " + outside.slice(0, 8).join(", ") : runLabels.join("; ")); }
  else check(`cards changed vs the copy before: ${changed.length} changed, ${added.length} added (no log given to compare)`, true, "");
}

// ── Undo / redo round trip ───────────────────────────────────────────────────────────────────────────────────────────
if (arg("--undo") && arg("--orig")) check("after \"undo the last run\" the board is byte-identical to its copy before the run", read(arg("--undo")) === read(arg("--orig")), `${sha(read(arg("--undo"))).slice(0, 8)} vs ${sha(read(arg("--orig"))).slice(0, 8)}`);
if (arg("--redo")) check("after \"redo\" the board is byte-identical to the board after the run", read(arg("--redo")) === afterText, `${sha(read(arg("--redo"))).slice(0, 8)} vs ${sha(afterText).slice(0, 8)}`);

// ── Mode-specific ────────────────────────────────────────────────────────────────────────────────────────────────────
if (mode === "direct") {
  const castNames = bw.castOf(after).map(bw.castName);
  check("the change log has at least one applied run for this board", runs.some((r) => r.status === "applied" || r.status === "undone"), runLabels.join("; "));
  if (G.expect) for (const [what, want] of Object.entries(G.expect)) {
    if (what === "cast") check(`cast members given are on the board: ${want.join(", ")}`, want.every((n) => castNames.some((c) => norm(c) === norm(n))), castNames.join(", "));
    if (what === "eras") check(`eras given are on the board: ${want.join(", ")}`, want.every((n) => bw.erasOf(after).some((e) => norm(e.name) === norm(n))), bw.erasOf(after).map((e) => e.name).join(", "));
    if (what === "relations") check(`relations given are on the board: ${want.join("; ")}`, want.every((w) => bw.relationsOf(after).some((l) => norm(bw.relationLabel(after, l)) === norm(w))), bw.relationsOf(after).map((l) => bw.relationLabel(after, l)).join("; "));
    if (what === "world") check(`world entries given are on the board: ${want.join(", ")}`, want.every((n) => bw.worldOf(after).some((c) => norm(bw.worldName(c)) === norm(n))), bw.worldOf(after).map((c) => `${bw.worldKindOf(c)} ${bw.worldName(c)}`).join(", "));
    if (what === "tags") check(`tags given are on the board, by: ai: ${want.join(", ")}`, want.every((t) => after.cards.some((c) => bw.tagsOf(c).some((x) => x.tag === t && x.by === "ai"))), "");
  }
}
if (mode === "ideas") {
  const inbox = bw.inboxIdeas(after), placed = bw.placedIdeas(after);
  const all = [...inbox, ...placed];
  const types = s.ideaTypes || bw.defaultIdeaTypes();
  check(`every idea given is an idea card verbatim (${given.length} given, ${all.length} ideas)`, given.every((g) => all.some((c) => c.body === g)), given.filter((g) => !all.some((c) => c.body === g)).slice(0, 3).join(" | "));
  check("every idea card carries one of the board's idea types", all.every((c) => types.includes(c.meta.type)), all.map((c) => c.meta.type || "(none)").join(", "));
  check("no idea's text was reworded (every idea body is one of the strings given)", all.every((c) => given.includes(c.body)), all.filter((c) => !given.includes(c.body)).map((c) => c.body.slice(0, 40)).join(" | "));
  for (const [text, where] of Object.entries(G.placed || {})) { const c = placed.find((x) => x.body === text); check(`approved idea sits on its card's tray: "${text.slice(0, 40)}…" → ${where}`, c && c.parent && norm(title(c.parent)) === norm(where), c ? `on ${title(c.parent)}` : "not placed"); }
  for (const [text, beat] of Object.entries(G.placed_step || {})) { const c = placed.find((x) => x.body === text); check(`approved idea sits on the arc step at beat ${beat}: "${text.slice(0, 40)}…"`, c && c.parent && c.parent.meta.kind === "arcbeat" && c.parent.meta.beat === beat, c ? `on ${c.parent.meta.kind} B${c.parent.meta.beat || "?"} "${c.parent.meta.label || ""}"` : "not placed"); }
  for (const text of G.inbox || []) check(`unruled or rejected idea stays in the inbox: "${text.slice(0, 40)}…"`, inbox.some((c) => c.body === text), "");
}
if (mode === "tagging") {
  check(`the fixture is a 200+ card board (${after.cards.length} cards)`, after.cards.length >= 200);
  if (before) {
    let bodyChanged = 0, creChanged = 0, nonAi = 0, offers = 0, otherMeta = 0;
    for (const c of after.cards) {
      const b = beforeMap.get(c.id); if (!b) { otherMeta++; continue; }
      if (b.body !== c.body) bodyChanged++;
      const bt = bw.tagsOf(b), at = bw.tagsOf(c), blk = bw.linksOf(b), alk = bw.linksOf(c);
      for (const t of bt) if (!at.some((x) => x.tag === t.tag && x.by === t.by)) creChanged++;
      for (const l of blk) if (!alk.some((x) => x.to === l.to && x.by === l.by)) creChanged++;
      for (const t of at) if (!bt.some((x) => x.tag === t.tag) && t.by !== "ai") nonAi++;
      for (const l of alk) if (!blk.some((x) => x.to === l.to) && l.by !== "ai") nonAi++;
      if (c.meta.ai && JSON.stringify(c.meta.ai) !== JSON.stringify(b.meta.ai)) { offers++; if (c.meta.ai.by !== "ai") nonAi++; }
      const strip = (m) => { const o = { ...m }; delete o.tags; delete o.links; delete o.ai; return JSON.stringify(o); };
      if (strip(c.meta) !== strip(b.meta)) otherMeta++;
    }
    check("no card body changed", bodyChanged === 0, `${bodyChanged} bodies changed`);
    check("no entry whose by is cre was changed or removed", creChanged === 0, `${creChanged} cre entries changed`);
    check("every entry added is by: ai (tags, links, offers)", nonAi === 0, `${nonAi} entries not by ai`);
    check("nothing but tags, links and the ai offer key changed on any card, and no card was added", otherMeta === 0, `${otherMeta} cards with other changes`);
    const added = after.cards.reduce((n, c) => n + bw.tagsOf(c).filter((t) => t.by === "ai").length + bw.linksOf(c).filter((l) => l.by === "ai").length, 0);
    check(`the run wrote something (${added} by: ai tags/links, ${offers} offers)`, added + offers > 0);
  }
}
if (mode === "import" || mode === "import-book") {
  const srcs = (arg("--sources") || "").split(",").filter(Boolean);
  const blocks = srcs.flatMap((p) => { const t = read(p); const fm = /^---\r?\n[\s\S]*?\r?\n---[ \t]*(\r?\n|$)/.exec(t); return bw.splitBlocks((fm ? t.slice(fm[0].length) : t).replace(/\r\n/g, "\n")); });
  const prose = after.cards.filter((c) => c.meta.kind !== "project" && !["cast", "world", "idea", "arcbeat"].includes(c.meta.kind)).map((c) => c.body);
  const titles = new Set([...(G.allowed || []), ...given]);
  check(`every source block is on the board word for word (${blocks.length} blocks)`, blocks.every((b) => prose.includes(b)), blocks.filter((b) => !prose.includes(b)).slice(0, 2).map((b) => b.slice(0, 60)).join(" | "));
  check("every card body is a source block or an approved title (nothing else)", prose.every((p) => blocks.includes(p) || titles.has(p) || p === ""), prose.filter((p) => !blocks.includes(p) && !titles.has(p) && p !== "").slice(0, 3).map((p) => p.slice(0, 60)).join(" | "));
  if (arg("--source-hashes")) { const H = JSON.parse(read(arg("--source-hashes"))); const changed = Object.entries(H).filter(([p, h]) => sha(readFileSync(abs(p))) !== h); check(`the source files are byte-identical afterwards (${Object.keys(H).length} files)`, !changed.length, changed.map(([p]) => p).join(", ")); }
  check("the board carries the board mark", bw.hasBoardMark(afterText));
  if (mode === "import-book") check("the book board is marked a working copy, the drafts staying the authority", /^bw-working-copy: true$/m.test(after.preamble) && /^bw-authority:/m.test(after.preamble), after.preamble.slice(0, 200));
  const ap = G.approved || {};
  const castNames = bw.castOf(after).map(bw.castName);
  check(`cast on the board is exactly the approved list (${(ap.cast || []).length})`, castNames.length === (ap.cast || []).length && (ap.cast || []).every((n) => castNames.some((c) => norm(c) === norm(n))), castNames.join(", "));
  const dlg = after.cards.filter((c) => c.meta.type === "dialogue");
  check(`dialogue-typed cards are exactly the approved ones (${(ap.dialogue || []).length})`, dlg.length === (ap.dialogue || []).length && (ap.dialogue || []).every((t) => dlg.some((c) => c.body.startsWith(t) || c.id === t.replace(/^\^/, ""))), dlg.map((c) => `${c.id}${c.meta.speaker ? " " + c.meta.speaker : ""}`).join(", "));
  const scenes = after.cards.filter((c) => c.meta.kind === (s.intensity?.levels?.inner || "scene"));
  if (ap.scenes !== undefined) check(`Scene cards are exactly the approved count (${ap.scenes})`, scenes.length === ap.scenes, `${scenes.length} scenes`);
  for (const [t, n] of Object.entries(ap.chapters || {})) { const c = after.cards.find((x) => norm(title(x)) === norm(t)); check(`chapter ${n} set on "${t}"`, c && c.meta.fields && String(c.meta.fields.chapter) === String(n), c ? JSON.stringify(c.meta.fields) : "no such card"); }
  if (ap.pov) for (const [t, who] of Object.entries(ap.pov)) { const c = after.cards.find((x) => norm(title(x)) === norm(t)); check(`pov ${who} set on "${t}"`, c && c.meta.fields && c.meta.fields.pov === who, c ? JSON.stringify(c.meta.fields) : "no such card"); }
  if (arg("--undo")) check("after \"undo the last run\" the import is removed whole (the board file is gone)", !existsSync(abs(arg("--undo"))), abs(arg("--undo")));
}
if (mode === "bible") {
  const eras = bw.erasOf(after);
  check("at least one era exists (a placeholder when none was named)", eras.length >= 1, eras.map((e) => e.name).join(", "));
  const steps = after.cards.filter((c) => c.meta.kind === "arcbeat");
  const inEra = steps.filter((c) => c.meta.era || (c.parent && c.parent.meta.kind !== "project"));
  check(`every arc step is filed in an era (own era, or placed on a card that has one): ${inEra.length}/${steps.length}`, steps.length > 0 && inEra.length === steps.length);
  const roleArcs = bw.castOf(after).flatMap((c) => (c.meta.arcs || []).filter((a) => a.model && a.model.role).map((a) => ({ cast: c, role: a.model.role })));
  const filled = roleArcs.filter((r) => r.cast.meta.fields && r.cast.meta.fields.role);
  check(`profile role filled on every cast member with a model role: ${filled.length}/${roleArcs.length}`, roleArcs.length > 0 && filled.length === roleArcs.length, roleArcs.map((r) => `${bw.castName(r.cast)}: ${r.role} → ${(r.cast.meta.fields || {}).role || "(blank)"}`).join("; "));
  const rels = bw.relationsOf(after).map((l) => bw.relationLabel(after, l));
  if (G.approved && G.approved.relations) check(`relations are exactly the approved ones (${G.approved.relations.length})`, rels.length === G.approved.relations.length && G.approved.relations.every((w) => rels.some((r) => norm(r) === norm(w))), rels.join("; "));
  check("no Place, Item or System was invented (world entries only where approved)", bw.worldOf(after).every((c) => (G.approved && G.approved.world || []).some((n) => norm(n) === norm(bw.worldName(c)))), bw.worldOf(after).map(bw.worldName).join(", ") || "none");
}
finish();
