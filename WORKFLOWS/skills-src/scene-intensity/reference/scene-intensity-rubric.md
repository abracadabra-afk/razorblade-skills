# Scene Intensity Rubric — v2.1

A reproducible instrument for scoring scene intensity so Claude can analyze pacing at
the **scene → chapter → work** level. Calibrated on *Ghost River* Ch. 1 and *Witchwood*
Ch. 1, revised against a 5-pass variance study, and validated on a held-out set
(*Ghost River* Ch. 2 + *Witchwood* Ch. 2, 12 scenes, 4 independent passes).

---

## Changelog

**v2.1 — the carried-dread layer (held-out validated).** Folds in Addendum D. The gate
transferred on the held-out set: every lure/irony scene independently drew +2, every
overt-horror scene drew 0. Two consequential changes from v2:

- **Mechanism swap.** v2 lifted D1/D2 in a "reader channel" and produced a second
  composite (I_reader = 67, etc.). That manufactured false precision — a reader does
  not experience "67." v2.1 replaces it with **two tracks never merged**: the local
  composite is left pristine, and carried dread is a small, capped, separately-reported
  `dread` field that only ever promotes a *band*, never a number.
- **I withdrew v2's band-edge move.** v2 shifted the edges to 42/60/82 to dodge the
  seam flips. The held-out data killed that idea: it pushes GR-S5 (37) and WW-S2 (58)
  into bands that contradict the cold passes (4 of 5 put WW-S2 in HIGH). v2.1 **reverts
  to the original ranges** and fixes seams the right way — a spread-based seam rule
  (§5) that flags ambiguity from the scoring spread itself rather than from edge
  placement.

**v2 → fixed three variance-check defects:** mixed scoring modes (the carried-dread
problem, now §4), band seams (§5), and undefined D1/D4 scope (§2).

---

## 0. Design target

The scorer is an LLM, so the target is **low run-to-run variance and zero drift across a
long document**, not the impossible removal of all judgment. Three mechanisms: evidence
before number; fixed scene boundaries; anchored bands with named tracks.

---

## 1. Segment into scenes

A new scene begins at a shift in **POV**, **time**, or **location**, or an explicit
break. Apply mechanically. Cross-cutting yields multiple scenes sharing a timeframe —
the cut is itself a pacing event. Record id, POV, location, one-line summary.

---

## 2. The six dimensions (0–3 each)

Two are **script-mechanized** (D5/D6 — computed from the prose, the objective floor).
The other four are **author-supplied**: the semantic dims D1/D2/D4 (judged,
evidence-gated) and D3, a reading-count of turns the script does **not** compute (it
requires comprehension, not regex). Only D5 and D6 come from the engine.

**Scope rule:** D1 and D4 are scored **for the POV character or a party they are bound
to** (self, kin, ward, ally, charge) — not unbound strangers or prey. **Recalled or
expository violence does not raise D1/D2** (not present-tense threat); it may raise D5.

**D2 predator-POV clause.** When the POV character *is* the threat (a predator-POV
scene), D2 measures the predator's proximity to their **prey/target** in the scene, not
a threat to the POV. D1 still attaches to the endangered bound party (the victim), even
though the POV embodies the danger. The carried-dread gate's reader-asymmetry
(condition 4) is satisfied structurally in this case — the reader fears for the victim
the predator is closing on — so a predator-POV scene with the victim present and unaware
can carry dread (and is scored present, not latent) even though nothing threatens the POV.

- **D1 — Stakes** *(name the bound party at risk)* — 0 nothing · 1 abstract/future/
  offscreen · 2 concrete present risk to a bound party · 3 concrete + irreversible +
  imminent, now.
- **D2 — Proximity** *(locate the present threat)* — 0 none · 1 latent/symbolic ·
  2 present and closing · 3 contact range, acting now.
- **D3 — Turns** *(author-supplied reading-count; **not** script-mechanized)* — 0 static
  · 1 one · 2 two–three · 3 four+ / continuous escalation.
- **D4 — Irreversibility** *(consequence to a bound party enacted on the page)* —
  0 nothing enacted · 1 referenced / slow chronic advance · 2 a real step / lasting loss
  · 3 death or terminal. *An ongoing irreversible condition that does not change state
  during the scene is context, not a turn, and scores ≤ 1.*
- **D5 — Somatic load** *(countable; involuntary body signals per ~250 words)* — 0 none ·
  1 sparse · 2 several · 3 saturated. **Lock to script.**
- **D6 — Pacing surface** *(script-mechanized; **narration-only** fragment fraction +
  dialogue share — quoted dialogue is excluded from the fragment count and a
  dialogue-dominated scene is capped below the top, so talky tender prose does not read
  as action-staccato)* — 0 long/ruminative · 1 mostly long · 2 mixed ·
  3 clipped/staccato/real-time. **Lock to script.** *(A global fragment-% proxy cannot
  separate a dialogue-dense tender scene from a kill — both run short; the narration-only
  count is what distinguishes them.)*

---

## 3. Composite & weighting

```
Intensity  = 2·D1 + 2·D2 + 1·D3 + 2·D4 + 1·D5 + 1·D6     (max 27)
Normalized = round(Intensity / 27 × 100)                  (0–100)
```

Stakes/proximity/irreversibility carry double — they read *as* intensity; turns/somatic/
pace are accelerants. Fix the weights once. **This composite is Track 1 and is never
touched by carried dread.**

---

## 4. Carried dread — two tracks, never merged

Cold scene-local scoring reproduces the author's seeds on self-contained scenes but
under-scores intercut / dramatic-irony scenes by up to two bands (GR-S7: seed 63, cold
32). That gap is not an error — it is the instrument correctly reporting that the
scene's menace is **not on its own page**. This layer captures that menace without
contaminating the local score.

- **Track 1 — local intensity.** §2–§3, scored scene-locally and evidence-gated.
  Reproducible spine (variance check: composite SD 1.86, countable dims ≈ 0).
- **Track 2 — carried dread.** A bounded, separately-reported modifier for intensity the
  reader feels *here* because of what *earlier* scenes established.

The carried value is **never** added into Intensity or Normalized. The two are reported
as a pair. The difference between "this page is hot" and "the reader is afraid here" is
exactly the signal you want to see.

### 4.1 The gate (binary — most scenes get 0)

A scene earns a mark **only if all five hold**:

1. **Named prior threat.** An *earlier* scene established a specific threat — entity,
   intent, or fact of danger (not mood, not genre atmosphere).
2. **Implicated here.** The threatening agent appears, or its target is present, or the
   threat is actively approached.
3. **Unresolved.** The threat is not neutralized as of this scene.
4. **Reader-side asymmetry.** The reader knows or fears something the POV does not act on
   — dramatic irony, helplessness, or misreading.
5. **Not an on-page detonation.** If the established threat finally acts in full view
   (the predator strikes; the dying child dies), the scene is scored **local only,
   dread = 0** — the menace is now on the page, so local D1–D4 already carry it. The
   buildup credit belongs to the *prior* scenes, not the payoff. *(Held-out: W3, the
   boy's on-page death, split scorers 2/1/1/0 because v1 lacked this rule. It is a clean
   local PEAK; carried = 0.)*

Any condition fails → **carried = 0**. The mark is re-evaluated each scene against
condition 3, so it decays naturally when the threat resolves or leaves the page
(stateful, auditable — no timed-decay rule needed).

### 4.2 Magnitude (+1 or +2, hard cap)

- **+1 priming** — threat latent/approaching; agent not in contact this scene.
- **+2 loaded irony** — agent *present and in contact* while the POV misreads it as
  safe/neutral or cannot act (GR-S7).

Cap at +2 so the layer can never dwarf the local read. Every nonzero mark **must cite
its source** (prior scene id + the priming fact). Uncited marks are invalid.

### 4.3 Band derivation (the only combined readout, for contour use)

- `dread 0` → `reader_band = band`.
- `dread +1` → `reader_band = band`, tagged "elevated — do not promote."
- `dread +2` → `reader_band =` one band above `band`.

Raw `Normalized` and `band` stay pristine.

### 4.4 Juxtaposition-dread (mandatory hand-flag)

The gate is deliberately blind to **juxtaposition-dread**: a calm scene intercut with an
*off-page* catastrophe involving a bound party — the gate requires the threat *named to a
target on the page* (conditions 1–2), so a scene where the danger is happening elsewhere
draws dread 0. This is correct scene-locally but it is the single most charged thing a
reader can feel, and the contour will silently understate it.

Because the engine cannot detect it, flagging it is a **required manual step**. When a
scene's intensity for the reader comes from a bound party's peril unfolding *off this
scene's page*, set `juxtaposition_dread: true` with a `juxtaposition_source`. The engine
surfaces the flag in the YAML and lists it on the contour but **never changes the band** —
it is an annotation, not a promotion, so the local track stays honest while the reader-
experience note is not lost. Auditing a chapter is not complete until every cross-cut of
this kind is either flagged or consciously ruled out.

---

## 5. Bands — original ranges + spread-based seam rule

| Band | Range |
|------|-------|
| **REST** | 0–30 |
| **BUILD** | 31–55 |
| **HIGH** | 56–75 |
| **PEAK** | 76–100 |

**Seam rule (supersedes v2's ±3 hysteresis).** A scene is tagged `seam` and reported
with **both** adjacent bands if **either**:

- its composite is within **±4** of a band edge, **or**
- its independent passes do not all fall in the same band (their range crosses an edge).

The range-crossing clause is the robust half — it flags ambiguity directly from the
scoring spread (empirical SD ≈ 3) rather than from a fixed distance, and caught all
three held-out flips (the ±2 buffer v2 first proposed caught only two). With this rule
the *position* of edges stops mattering, which is why v2.1 keeps the original ranges.

---

## 6. Output schema (per scene)

```yaml
- id: GR-S7
  pov: Stacy/Liz
  location: highway (tow truck arrives)
  summary: The tow truck stops; the driver smiles "like Jesus."
  # --- Track 1: local, pristine ---
  scores: { D1: 1, D2: 1, D3: 1, D4: 1, D5: 0, D6: 2 }
  intensity: 9
  normalized: 33
  band: BUILD
  seam: true            # within ±4 of the REST/BUILD edge → reported BUILD/REST
  # --- Track 2: carried dread ---
  dread: +2
  dread_source: "GR-S4/GR-S6 established the tow-truck driver as the predator (the Pig, 'a city of dead kids' fed by roadkill)"
  dread_basis: "predator in contact ('Need a tow?', 'smiling like Jesus'); targets present; they read him as rescue — reader knows otherwise"
  reader_band: HIGH
```

Fill D3/D5/D6 from the script; D1/D2/D4 by Claude with quotes. A scene scored high on D1
but body-quiet and long-sentenced (low D5/D6) is a flag to re-check.

---

## 7. Contour analysis (chapter & work)

Plot **both tracks** against scene order:

- **Peaks / valleys?** No PEAK = no climax; no REST = relentless (numbing).
- **Variance** — near-flat = monotony.
- **Local↔reader gap** — a wide gap marks a scene running on *earned dread* rather than
  present event (GR-S7). Many high-dread/low-local scenes = leaning on setups; many
  high-local/zero-dread = relentlessness. Neither is visible with one number.
- **Peak placement** vs act structure; **the sag** = a long BUILD run with no REST/PEAK.
- **Work level** — chart per-chapter medians, peaks, and mean local↔reader gap.

---

## Appendix A — *Ghost River* Ch. 1

Seven scenes, three intercut threads. Local composites are the validated cold-run
values. **Ledger:** **T1** = Minister/the Pig predation (severity 3, established S4 —
the throat-cutting memory; agent Minister; targets incl. Stacy/Liz). **T2** = the birth
ritual/Delora (severity 3, established S1; target Esther — her scenes already score high
locally, so carry is moot there).

| Scene | POV | Norm | band | dread | reader_band | gate note |
|-------|-----|------|------|-------|-------------|-----------|
| GR-S1 | Esther | 63 | HIGH | 0 | HIGH | — |
| GR-S2 | Minister | 30 | REST · *seam* | 0 | REST | on REST/BUILD edge |
| GR-S3 | Esther | 66 | HIGH | 0 | HIGH | — |
| GR-S4 | Minister | 30 | REST · *seam* | **+1** | REST (elevated) | window-shadow primed in S1; symbolic, not in contact → priming |
| GR-S5 | Stacy/Liz | 37 | BUILD | **0** | BUILD | gate fails cond. 1 — predator not yet *named-to-target*; unease is atmospheric |
| GR-S6 | Esther | 99 | PEAK | 0 | PEAK | on-page detonation → local only |
| GR-S7 | Stacy/Liz | 33 | BUILD | **+2** | **HIGH** | full gate; predator in contact, targets misread him as rescue |

**Contours:**
```
local :  63 · 30 · 66 · 30 · 37 · 99 · 33     (honest on-page intensity; back half flattens)
reader:  HIGH·REST·HIGH·REST·BUILD·PEAK·HIGH  (S7 promoted +2; S4 elevated, not promoted)
```
The flat back half of the local track is *correct* — S4/S5/S7's on-page intensity really
is low. The reader track restores the saw-tooth, and the gap is now a first-class
readout. GR-S5 is the instructive case: the gate **refuses to fire on mood alone**,
which is what stops the layer from quietly rewarding every tense-feeling scene.

---

## Appendix B — *Witchwood* Ch. 1

Two scenes, single POV, single thread → no carried threat, dread 0 throughout.

| Scene | POV | Norm | band | notes |
|-------|-----|------|------|-------|
| WW-S1 | hunter | 30 | REST · *seam* | D4 ≤ 1: the boy's chronic decline is referenced/slow-advancing, not stepped in-scene (closes the 2/1/0 split). Tender, somatically rich, still REST — intensity ≠ emotional weight. |
| WW-S2 | hunter | 58 | HIGH · *seam* | **Correction from v2** (which called this BUILD via the withdrawn edge-move): under the original ranges and the cold passes (4 of 5 = HIGH), 58 lands HIGH, seam-flagged toward BUILD. The buck is unbound prey, so its death does not raise D1/D4; the score rises via the staccato kill (D3/D6), not peril. |

**Contour:** 30 · 58 — a low climb; a baseline/valley chapter that sets the floor the
rest of the book spikes above.

---

## Appendix C — anchors & known limits

*Ghost River* spans REST→PEAK in one chapter **and** carries the largest local↔reader
gaps (S7 +2), pinning both the peak end and the carried-dread mechanism. *Witchwood*
pins the low, flat end and the two scope edge-cases (chronic illness, unbound prey). The
held-out set (Ch. 2 of each) confirmed the gate transfers and surfaced the on-page-
detonation rule (cond. 5) and the wider seam rule.

**Two limits worth watching** (where the layer's judgment is thinnest):

1. **The "helplessness" arm of gate condition 4 is the softest gate.** GR-S4's +1 rests
   on it (Minister *knows* about the shadow — there is no true irony, only his inability
   to keep it out) plus reading the symbolic window-shadow as a present threat. Defensible,
   but this is the one place mood can leak back in as "dread." Audit +1 marks that cite
   helplessness rather than irony.
2. **Juxtaposition-dread is invisible to the gate — flag it by hand (§4.4).** GR-S5 — a
   stranded child intercut with a roaming predator not yet connected to her on the page —
   draws 0, because cond. 1/2 require the threat *named to the target*. The reader feels
   the noose anyway. This is precision bought at the cost of recall; the mandatory
   `juxtaposition_dread` hand-flag (§4.4) records it without disturbing the local band.

*Scores are calibration seeds, not verdicts. Adjust any anchor or ledger row and the
bands move — re-pin, then keep fixed.*
