// The DEV-sequence importer (2026-10-20, the Witchwood board build): a part's structure built from the DEV tree's own
// sequence files, as one ops file for board_tool.mjs (one run, one undo). The plan names the part, its chapters (his
// chapter containers, with the DEV sequences each covers), their scenes (a DEV sequence, or a run of its beats) and one
// Beat per DEV beat; titles, summaries and chains are the plan's — administrative, plain words saying what the material
// does. This script holds the plan to the DEV files: every scene's beats are exactly its DEV beats, every DEV sequence the
// plan claims is covered beat for beat, once; every scene chain has one line per Beat. It also lifts the quoted lines of
// each DEV read and keeps only those found word for word in CRE's dictation floors — those become ideas on their Beat,
// the text taken from the floor by board_tool (never retyped here). Prose (place-prose), arc steps and other ideas are
// passed through as the plan gives them.
// Before any beat is built, the neighbour check (below) reads each sequence's neighbours and refuses until every flagged seam
// is resolved in the plan's "seams"; beats resolved as carried by a neighbour become the ruling list (--rulings).
//   node dev_import.mjs <plan.json> --out <ops.json> [--report <quotes.json>] [--rulings <rulings.md>]
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";

for (const st of [process.stdout, process.stderr]) try { st.setDefaultEncoding("utf8"); } catch {}
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const WIN = process.platform === "win32";
const VAULT = arg("--vault", WIN ? "C:/Users/Chad/Dropbox/razorblade_mermaid" : `${process.env.HOME}/Dropbox/razorblade_mermaid`).replace(/\\/g, "/");
const fix = (p) => p.replace(/^\/([A-Za-z])\//, (m, d) => `${d.toUpperCase()}:/`).replace(/\\/g, "/");
const abs = (p) => (/^[A-Za-z]:|^\//.test(fix(p)) ? fix(p) : `${VAULT}/${p}`);
const read = (p) => readFileSync(abs(p), "utf8").replace(/\r\n/g, "\n");
const sha = (t) => createHash("sha256").update(Buffer.from(t, "utf8")).digest("hex");
const plan = JSON.parse(readFileSync(fix(argv[0]), "utf8"));
const problems = [], notes = [];

// ── DEV sequence files: the numbered list under "## Beats", and the quotes in each beat and in the arc ─────────────────
function devSeq(file) {
  const p = `${plan.devDir}/sequences/${file}`;
  if (!existsSync(abs(p))) { problems.push(`no DEV sequence file ${p}`); return null; }
  const t = read(p);
  const sect = (h) => { const m = new RegExp(`^## ${h}[^\\n]*\\n([\\s\\S]*?)(?=^## |^---|(?![\\s\\S]))`, "m").exec(t); return m ? m[1] : ""; };
  // a read captured at sequence grain (SEQ 01, the prologue) numbers its beats under "## Scenes (in order)" instead
  const list = (x) => x.split("\n").filter((l) => /^\d+\.\s/.test(l)).map((l) => l.replace(/^\d+\.\s+/, ""));
  const beats = list(sect("Beats")).length ? list(sect("Beats")) : list(sect("Scenes \\(in order\\)"));
  // prev / next as the read's own Connections line names them ("prev: [[sequences/SEQ 23B - …|…]]")
  const link = (k) => { const m = new RegExp(`${k}:\\s*\\[\\[sequences/(SEQ [^|\\]]+)`, "i").exec(t); return m ? m[1].trim() + ".md" : null; };
  return { path: p, file, id: seqId(file), text: t, sha256: sha(t), beats, arc: sect("The arc"), prev: link("prev"), next: link("next") };
}
const seqId = (f) => (/^SEQ (\w+)/.exec(f) || [, f])[1];

// ── The neighbour check (CRE, 2026-10-21): a beat the next or previous sequence already carries is never built twice and
// never dropped silently. Found on Part 3: SEQ 24's beat 1 (back on the trail, the boy wanting to know what happened) was
// written before SEQ 23B was recovered and slotted in ahead of it; 23B carries that whole stretch and ends where 24 begins.
// The script finds the seams that need a look — a "B" sequence on either side, a note in either read naming the other
// (slotted between / superseded / onset / recovered / placement / inserted), or edge beats whose words overlap a
// neighbour's — and refuses until the plan resolves each one. Whether a beat is really carried is a reading call, recorded
// in the plan, never decided by the overlap score (DIR-014: a rescue may ask, never decide); the score only asks. A beat
// resolved as carried goes to CRE's ruling list as "resolved against SEQ X — confirm", with what decided it — where a landed
// or Drive draft covers the stretch, the draft's order decides which sequence owns the beat.
const TRIGGER = /slotted|superseded|onset|recovered|placement|inserted|filed as \d+B|between \[\[sequences/i;
const STOP = new Set("that this with from into back their them they then than when what where which while have will been were over just only even more most some such very also the and for her his its she him not but are was one out off".split(" "));
const words = (s) => new Set(String(s).toLowerCase().replace(/\[\[[^\]|]*\|([^\]]*)\]\]/g, "$1").replace(/[^a-z' ]+/g, " ").split(/\s+/).filter((w) => w.length >= 4 && !STOP.has(w)));
const overlap = (a, b) => { const A = words(a), B = words(b); if (!A.size || !B.size) return 0; let n = 0; for (const w of A) if (B.has(w)) n++; return n / Math.min(A.size, B.size); };
// near-identical wording, measured against the longer of the two lines (naming the same event is not a copy)
const sameWords = (a, b) => { const A = words(a), B = words(b); if (!A.size || !B.size) return 0; let n = 0; for (const w of A) if (B.has(w)) n++; return n / Math.max(A.size, B.size); };
const seamKey = (a, b) => [a, b].sort().join("|");
function noteMentions(text, otherId) {
  // the trigger word and the neighbour's number in the same clause (a Connections line lists every link with " · ")
  const out = [];
  for (const seg of text.split(/\n| · |(?<=[.;])\s+/)) {
    const m = new RegExp(`SEQ ${otherId}(?![\\w])`).exec(seg);
    if (!m || !TRIGGER.test(seg)) continue;
    const t = TRIGGER.exec(seg);
    if (Math.abs(t.index - m.index) > 140) continue;
    out.push(seg.replace(/\[\[[^\]|]*\|([^\]]*)\]\]/g, "$1").replace(/\[\[([^\]]*)\]\]/g, "$1").replace(/[*>]/g, "").replace(/\s+/g, " ").trim().slice(0, 170));
  }
  return out;
}
const devCache = {};
const devOf = (file) => (devCache[file] !== undefined ? devCache[file] : (devCache[file] = existsSync(abs(`${plan.devDir}/sequences/${file}`)) ? devSeq(file) : null));
function neighbourCheck() {
  const used = [...new Set(plan.chapters.flatMap((c) => c.scenes.map((s) => s.seq).filter(Boolean)))];
  const seams = new Map(); // key → {a, b} with a before b
  used.forEach((f, i) => {
    const d = devOf(f); if (!d) return;
    const add = (x, y) => { if (x && y && x !== y) { const k = seamKey(seqId(x), seqId(y)); if (!seams.has(k)) seams.set(k, { a: x, b: y }); } };
    add(d.prev, f); add(f, d.next); if (i) add(used[i - 1], f);
  });
  const resolved = new Map((plan.seams || []).map((s) => [seamKey(...s.between.map((x) => x.replace(/^SEQ /, ""))), s]));
  const carried = {}, rulings = [], open = [];
  for (const [k, { a, b }] of seams) {
    const A = devOf(a), B = devOf(b); if (!A || !B) continue;
    const why = [];
    if (/B$/.test(A.id) || /B$/.test(B.id)) why.push(`a "B" sequence (${/B$/.test(A.id) ? A.id : B.id}) was slotted in here`);
    for (const l of noteMentions(A.text, B.id)) why.push(`SEQ ${A.id} notes: ${l}`);
    for (const l of noteMentions(B.text, A.id)) why.push(`SEQ ${B.id} notes: ${l}`);
    // edge beats: the last two of the earlier sequence and the first two of the later, each against the whole neighbour
    const hints = [];
    const edge = (S, idx, N) => idx.forEach((i) => { if (!S.beats[i]) return; let best = { s: 0 }; N.beats.forEach((nb, j) => { const s = overlap(S.beats[i], nb); if (s > best.s) best = { s, j }; }); if (best.s >= 0.34) hints.push(`SEQ ${S.id} beat ${i + 1} ~ SEQ ${N.id} beat ${best.j + 1} (${Math.round(best.s * 100)}% shared words)`); });
    edge(B, [0, 1], A); edge(A, [A.beats.length - 2, A.beats.length - 1], B);
    if (hints.length) why.push(...hints);
    if (!why.length) continue;
    const r = resolved.get(k);
    if (!r) { open.push(`SEQ ${A.id} → SEQ ${B.id}: ${why.join("; ")}`); continue; }
    if (!r.carried && !r.clear) { open.push(`SEQ ${A.id} → SEQ ${B.id}: the plan's entry needs "carried" or "clear" (with its reason)`); continue; }
    notes.push(`seam SEQ ${A.id} → SEQ ${B.id} checked (${why.length} flag${why.length === 1 ? "" : "s"})${r.clear ? ": clear — " + r.clear : ""}`);
    for (const c of r.carried || []) {
      const S = devOf(used.find((f) => seqId(f) === String(c.seq).replace(/^SEQ /, "")) || ""), by = String(c.by).replace(/^SEQ /, "");
      if (!S) { problems.push(`seam ${k}: carried beat names ${c.seq}, which no scene uses`); continue; }
      if (!c.decidedBy) problems.push(`${c.seq} beat ${c.beat}: a carried beat needs "decidedBy" (the draft order, or the reason)`);
      if (!S.beats[c.beat - 1]) { problems.push(`${c.seq} has no beat ${c.beat}`); continue; }
      (carried[S.file] = carried[S.file] || new Set()).add(Number(c.beat));
      rulings.push(`SEQ ${S.id} beat ${c.beat} ("${S.beats[c.beat - 1].replace(/\[\[[^\]|]*\|([^\]]*)\]\]/g, "$1").replace(/\[\[([^\]]*)\]\]/g, "$1").replace(/\*\*/g, "").slice(0, 110)}…") — resolved against SEQ ${by}${c.byBeats ? ` (beats ${c.byBeats})` : ""}: ${c.decidedBy} — not built here; confirm`);
    }
  }
  // a resolution for a seam that isn't one is a stale plan entry: say so rather than keep it quietly
  for (const [k] of resolved) if (!seams.has(k)) notes.push(`plan names seam ${k}, which is not adjacent in this plan`);
  if (open.length) problems.push(`neighbour check: ${open.length} seam${open.length === 1 ? "" : "s"} to resolve in the plan's "seams" (carried beats, or clear with a reason):\n    ` + open.join("\n    "));
  return { carried, rulings };
}
const NB = neighbourCheck();
// Quoted spans: "…", “…”, and italic *…* runs; a span joined by an ellipsis is checked piece by piece.
function quotesIn(line) {
  const out = [];
  const plain = line.replace(/\[\[[^\]|]*\|([^\]]*)\]\]/g, "$1").replace(/\[\[([^\]]*)\]\]/g, "$1").replace(/\*\*/g, ""); // bold is the reader's emphasis, not a quote
  for (const m of plain.matchAll(/[“"]([^”"]{8,})[”"]|\*([^*]{8,})\*/g)) {
    const q = (m[1] || m[2]).replace(/^[“"]|[”"]$/g, "");
    for (const piece of q.split(/…|\.\.\.|\s—\s|\s\/\s/)) { const w = piece.trim().replace(/^[“"']+|[”"'.,;:!?]+$/g, ""); if (w.split(/\s+/).length >= 4) out.push(w); }
  }
  return out;
}
// Normalised search: case, quote marks, dashes and runs of whitespace ignored; the hit is returned as the floor's own text.
const normCh = (ch) => ({ "’": "'", "‘": "'", "“": '"', "”": '"', "—": "-", "–": "-" }[ch] || ch).toLowerCase();
function indexed(t) { let n = "", map = []; for (let i = 0; i < t.length; i++) { const ch = t[i]; if (/\s/.test(ch)) { if (n.endsWith(" ")) continue; n += " "; map.push(i); continue; } n += normCh(ch); map.push(i); } return { n, map }; }
const floors = (plan.floors || []).map((p) => { const t = read(p); const fm = /^---\n[\s\S]*?\n---[ \t]*\n/.exec(t); const body = fm ? t.slice(fm[0].length) : t; return { path: p, body, ...indexed(body) }; });
function findInFloors(q) {
  const qn = indexed(q.trim()).n;
  for (const f of floors) { const i = f.n.indexOf(qn); if (i >= 0) return { path: f.path, quote: f.body.slice(f.map[i], f.map[i + qn.length - 1] + 1) }; }
  return null;
}

// ── ops ────────────────────────────────────────────────────────────────────────────────────────────────────────────────
const ops = [], quoteLog = [], claimed = {};
const T = (t) => `title:${t}`;
const P = plan.part;
ops.push({ op: "add-card", kind: "part", ...(P.after ? { after: P.after } : {}), title: P.title, fields: P.fields || {} });
const lateLinks = [], prose = [];
for (const ch of plan.chapters) {
  ops.push({ op: "add-card", kind: "sequence", under: T(P.title), title: ch.title, fields: ch.fields || {} });
  for (const sc of ch.scenes) {
    ops.push({ op: "add-card", kind: "scene", under: T(ch.title), title: sc.title, fields: sc.fields || {} });
    if (sc.era) ops.push({ op: "set-era", card: T(sc.title), era: sc.era });
    let dev = null, range = null;
    if (sc.seq) {
      dev = devOf(sc.seq);
      if (!dev) problems.push(`no DEV sequence file ${plan.devDir}/sequences/${sc.seq}`);
      if (dev) {
        range = sc.devBeats || [1, dev.beats.length];
        // beats the neighbour check resolved as carried by the next or previous sequence: covered there, built nowhere here
        const gone = NB.carried[sc.seq] || new Set();
        sc._devs = [];
        for (let i = range[0]; i <= range[1]; i++) if (!gone.has(i)) sc._devs.push(i);
        if (range[0] < 1 || range[1] > dev.beats.length) problems.push(`${sc.title}: DEV beats ${range.join("–")} are not in ${sc.seq} (${dev.beats.length} beats)`);
        const n = range[1] - range[0] + 1;
        claimed[sc.seq] = claimed[sc.seq] || { total: dev.beats.length, got: [] };
        // Beats normally map one to one onto the DEV beats, in order. When his prose runs the DEV beats in another order, each
        // Beat names the DEV beat it carries (`dev`) and the Beats follow the prose: every DEV beat in range must still be carried.
        if ((sc.beats || []).some((b) => b.dev != null)) {
          const devs = sc.beats.map((b) => b.dev);
          if (devs.some((d) => !(d >= range[0] && d <= range[1]))) problems.push(`${sc.title}: every Beat needs a dev beat number in ${range.join("–")}`);
          if (devs.some((d) => gone.has(d))) problems.push(`${sc.title}: a Beat carries a DEV beat the neighbour check resolved to another sequence`);
          for (let i = range[0]; i <= range[1]; i++) { if (!gone.has(i) && !devs.includes(i)) problems.push(`${sc.title}: DEV beat ${i} of ${sc.seq} is carried by no Beat`); if (claimed[sc.seq].got.includes(i)) problems.push(`${sc.seq} beat ${i} is claimed twice`); claimed[sc.seq].got.push(i); }
          notes.push(`${sc.title}: Beats follow the prose — DEV beats in the order ${devs.join(", ")}`);
        } else {
          if ((sc.beats || []).length !== sc._devs.length) problems.push(`${sc.title}: ${(sc.beats || []).length} Beats for ${sc._devs.length} DEV beats (${sc.seq} ${range.join("–")}${gone.size ? `, less ${[...gone].join(", ")} carried by a neighbour` : ""})`);
          for (let i = range[0]; i <= range[1]; i++) { if (claimed[sc.seq].got.includes(i)) problems.push(`${sc.seq} beat ${i} is claimed twice`); claimed[sc.seq].got.push(i); }
        }
        notes.push(`${sc.title} ← ${dev.path} beats ${range.join("–")} (sha ${dev.sha256.slice(0, 12)})`);
      }
    } else if ((sc.beats || []).length && !sc.prose) notes.push(`${sc.title}: no DEV sequence (beats from the plan)`);
    (sc.beats || []).forEach((b, i) => {
      ops.push({ op: "add-card", kind: "beat", under: T(sc.title), title: b.title });
      const ref = `beat:${T(sc.title)}:${i}`;
      if (b.type) ops.push({ op: "set-type", card: ref, type: b.type });
      if (b.summary) ops.push({ op: "set-summary", card: ref, text: b.summary });
      if (b.prose) prose.push({ op: "place-prose", under: ref, ...b.prose });
      if (dev && plan.quotes !== false) {
        // a DEV beat carried by several Beats (prose order) gives its quotes to the first of them only
        const dn = b.dev != null ? b.dev : sc._devs[i];
        const first = b.dev == null || sc.beats.findIndex((x) => x.dev === b.dev) === i;
        const devLine = first ? dev.beats[dn - 1] || "" : "";
        for (const q of quotesIn(devLine)) {
          const hit = findInFloors(q);
          quoteLog.push({ seq: sc.seq, beat: dn, quote: q, found: hit ? hit.path : null });
          if (hit) prose.push({ op: "add-idea", from: { source: hit.path, quote: hit.quote }, on: ref, type: "beat", tags: [`seq:${sc.seq.replace(/^SEQ (\w+).*$/, "$1")}`, "dev dictation"] });
        }
      }
    });
    if (dev && plan.quotes !== false && range[0] === 1) for (const q of quotesIn(dev.arc)) {
      const hit = findInFloors(q);
      quoteLog.push({ seq: sc.seq, beat: "arc", quote: q, found: hit ? hit.path : null });
      if (hit) prose.push({ op: "add-idea", from: { source: hit.path, quote: hit.quote }, on: T(sc.title), type: "beat", tags: [`seq:${sc.seq.replace(/^SEQ (\w+).*$/, "$1")}`, "dev dictation"] });
    }
    // a scene of his prose that no DEV sequence carries (a landed chapter's extra scenes): the prose goes under the scene,
    // and the breakdown groups it into Beats afterwards
    if (sc.prose) { if ((sc.beats || []).length) problems.push(`${sc.title}: prose goes on the scene or on its Beats, not both`); else prose.push({ op: "place-prose", under: T(sc.title), ...sc.prose }); }
    if (sc.summary) ops.push({ op: "set-summary", card: T(sc.title), text: sc.summary });
    if (sc.goalHolder) ops.push({ op: "set-field", card: T(sc.title), field: "goal holder", value: sc.goalHolder });
    if (sc.chain) {
      ops.push({ op: "set-chain", card: T(sc.title), ...sc.chain });
      const lines = 2 + (sc.chain.turns || []).length;
      if ((sc.beats || []).length) {
        if (lines !== sc.beats.length) problems.push(`${sc.title}: ${lines} chain lines for ${sc.beats.length} Beats (one line per Beat)`);
        else sc.beats.forEach((b, i) => lateLinks.push({ op: "link-from", card: `beat:${T(sc.title)}:${i}`, parent: T(sc.title), lines: i }));
      }
    }
  }
  if (ch.summary) ops.push({ op: "set-summary", card: T(ch.title), text: ch.summary });
  if (ch.goalHolder) ops.push({ op: "set-field", card: T(ch.title), field: "goal holder", value: ch.goalHolder });
  if (ch.era) ops.push({ op: "set-era", card: T(ch.title), era: ch.era });
  if (ch.chain) {
    ops.push({ op: "set-chain", card: T(ch.title), ...ch.chain });
    const lines = 2 + (ch.chain.turns || []).length, used = new Set();
    for (const l of ch.links || []) {
      const [a, b] = l.lines.length === 1 ? [l.lines[0], l.lines[0]] : l.lines;
      if (!(a >= 0 && b >= a && b < lines)) problems.push(`${ch.title}: link lines ${JSON.stringify(l.lines)} not in its chain of ${lines}`);
      for (let i = a; i <= b; i++) { if (used.has(i)) problems.push(`${ch.title}: line ${i} feeds two scenes`); used.add(i); }
      lateLinks.push({ op: "link-from", card: T(ch.scenes[l.scene].title), parent: T(ch.title), lines: l.lines });
    }
    // A chapter's chain sits a level above its scenes (CRE, 2026-10-21; Chapter 1 as the model: four lines for two scenes):
    // about one line per scene or turn — never more than two per linked scene — and in chapter-level words, never a copy of
    // a scene's own lines. The overlap test only asks for a rewrite; it decides nothing about the story.
    const linkedScenes = (ch.links || []).map((l) => ch.scenes[l.scene]).filter(Boolean);
    if (linkedScenes.length && lines > Math.max(3, 2 * linkedScenes.length)) problems.push(`${ch.title}: ${lines} chain lines for ${linkedScenes.length} linked scene(s) — a chapter's chain runs about one line per scene or turn (at most ${Math.max(3, 2 * linkedScenes.length)})`);
    const chLines = [ch.chain.entry, ...(ch.chain.turns || []).map((x) => x.text), ch.chain.exit && ch.chain.exit.text].filter(Boolean);
    for (const sc of linkedScenes) {
      const scLines = sc.chain ? [sc.chain.entry, ...(sc.chain.turns || []).map((x) => x.text), sc.chain.exit && sc.chain.exit.text].filter(Boolean) : [];
      for (const a of chLines) for (const b of scLines) if (sameWords(a, b) >= 0.6) problems.push(`${ch.title}: the chapter line "${a}" repeats ${sc.title}'s line "${b}" — write it a level up`);
    }
  }
}
for (const [seq, c] of Object.entries(claimed)) { const miss = []; for (let i = 1; i <= c.total; i++) if (!c.got.includes(i)) miss.push(i); if (miss.length) problems.push(`${seq}: DEV beats ${miss.join(", ")} are on no scene`); }
for (const want of plan.expectSeqs || []) if (!claimed[want]) problems.push(`${want} is on no scene`);
ops.push(...lateLinks, ...prose);
// Arc steps go on the chain line of the Beat that carries them (CRE, 2026-10-21: "at line level, not just on the scene"):
// `{id, on: <scene>, beat: n}` → the scene's n-th Beat's line. A step with no beat to carry it (an interlude slot with no
// chain yet) stays on the scene as a Need only with a stated `sceneOnly` reason; otherwise the plan is refused. A step that
// spans scenes gives `parts: [{text, on, beat}]` instead — its own words split by scene — and becomes sub-steps.
const stepLines = [];
for (const st of plan.steps || []) {
  // A step whose material spans scenes (CRE 2026-10-21, "yes, sub steps"): one sub-step per scene, each the step's own words
  // for that piece, on the line of the Beat that carries it; the parent comes off the board as a category.
  if (Array.isArray(st.parts) && st.parts.length) {
    if (st.parts.length < 2) { problems.push(`step ^${st.id}: "parts" needs two or more (one per scene)`); continue; }
    stepLines.push({ op: "split-step", step: `^${st.id}`, unplace: true, parts: st.parts.map((p) => ({ text: p.text, via: `beat:${p.on}:${p.beat}` })) });
    continue;
  }
  if (st.beat != null) { stepLines.push({ op: "place-on-line", step: `^${st.id}`, via: `beat:${st.on}:${st.beat}` }); continue; }
  if (!st.sceneOnly) { problems.push(`step ^${st.id} on ${st.on}: give the Beat that carries it ("beat": n) or say why it stays on the scene ("sceneOnly")`); continue; }
  ops.push({ op: "place-idea", idea: `^${st.id}`, on: st.on });
  notes.push(`step ^${st.id} stays on ${st.on.replace(/^title:/, "")} (a Need): ${st.sceneOnly}`);
}
ops.push(...stepLines);
for (const id of plan.ideas || []) ops.push({ op: "add-idea", ...id });
const titles = [P.title, ...plan.chapters.flatMap((c) => [c.title, ...c.scenes.map((s) => s.title)])];
const dup = titles.filter((t, i) => titles.findIndex((x) => x.toLowerCase() === t.toLowerCase()) !== i);
if (dup.length) problems.push(`titles used twice in the plan: ${dup.join(", ")}`);
// a Beat may share a title with another Beat (they are named by position), never with a container a later op names by title
const lower = new Set(titles.map((x) => x.toLowerCase()));
for (const c of plan.chapters) for (const sc of c.scenes) for (const b of sc.beats || []) if (lower.has(String(b.title).toLowerCase())) problems.push(`Beat "${b.title}" (${sc.title}) has the same title as a part, chapter or scene`);
if (arg("--report")) writeFileSync(fix(arg("--report")), JSON.stringify({ notes, quotes: quoteLog, rulings: NB.rulings }, null, 1));
if (arg("--rulings") && NB.rulings.length) writeFileSync(fix(arg("--rulings")), "# Ruling list — beats a neighbour already carries\n\n" + NB.rulings.map((r, i) => `${i + 1}. ${r}`).join("\n") + "\n");
if (problems.length) { console.error("REFUSED — the plan doesn't fit the DEV tree:\n  " + problems.join("\n  ")); process.exit(2); }
writeFileSync(fix(arg("--out")), JSON.stringify({ board: plan.board, label: plan.label, ops }, null, 1));
const found = quoteLog.filter((q) => q.found).length;
console.log(`${ops.length} ops → ${arg("--out")}`);
for (const n of notes) console.log("  " + n);
if (NB.rulings.length) { console.log(`  RULING LIST — ${NB.rulings.length} beat${NB.rulings.length === 1 ? "" : "s"} a neighbour already carries (not built; for CRE to confirm):`); NB.rulings.forEach((r, i) => console.log(`    ${i + 1}. ${r}`)); }
console.log(`  DEV quotes: ${quoteLog.length} lifted, ${found} found word for word in the dictation floors (ideas), ${quoteLog.length - found} not found (left off)`);
