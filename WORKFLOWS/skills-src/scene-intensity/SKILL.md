---
name: scene-intensity
description: >-
  Score scene intensity and analyze pacing for any prose fiction project. Segment a
  chapter into scenes, score each on the six-dimension rubric across a reproducible
  scene-local track and a carried-dread reader track, then read the intensity contour
  at chapter and work level. Use when the author asks to "score scene intensity",
  "analyze pacing", "run the intensity rubric", "build a tension/intensity contour",
  "where does my chapter sag", "find the pacing valleys/peaks", or wants relentlessness,
  monotony, or a missing climax diagnosed across scenes or chapters. Project-agnostic:
  each project calibrates its bands, somatic lexicon, and dread rule via
  intensity_config.json. Do NOT use for line-editing, prose revision, or copy-editing.
---

# Scene Intensity

Turn a chapter into a measurable pacing contour. The instrument splits the work in two:

- **Deterministic layer — `scene_intensity.py`.** Mechanical dims (D5 somatic load,
  D6 pacing surface), the weighted composite, banding, the seam rule, the carried-dread
  band math, validation, and YAML/contour output. Same answer every run.
- **Judgment layer — you (the model).** Scene segmentation, the semantic dims
  (D1 stakes, D2 proximity, D4 irreversibility, D3 turns), and the carried-dread gate.

Full method, dimension anchors, and the worked Ghost River / Witchwood calibration are
in `reference/scene-intensity-rubric.md`. Read it before scoring a new project.

## Workflow

1. **Segment.** Cut the chapter into scenes — a new scene starts at a shift in POV,
   time, or location, or an explicit break. Cross-cut threads = separate scenes.

   **Single-location / screen-mediated stories (2026-07-22, from the EP 01 DOOMSCROLLER
   run):** the mechanical rule collapses when one POV never leaves one room (a
   doomscroll story, a phone-call story, found-footage). When the project has ruled
   that the perceptual envelope IS a feed/screen, treat **each served item + its
   real-world aftermath as one scene** — the clip is a location shift in the world the
   reader actually inhabits — plus every physical move (window, yard, power-down) as
   its own boundary. State the convention in the report so reruns segment identically.

2. **Score the judgment dims** for each scene, with a quote/count as evidence
   (0–3 each):
   - **D1 Stakes** — risk to the POV or a *bound* party (kin/ward/ally), present on the page.
   - **D2 Proximity** — how close the present threat is (latent → contact range).
   - **D3 Turns** — count of reversals / new-danger beats.
   - **D4 Irreversibility** — a lasting consequence to a bound party *enacted in the scene*.
   - Recalled/expository violence does **not** raise D1/D2 (it may raise D5).
   - Leave D5/D6 out — the script fills them from the scene's prose.

3. **Apply the dread gate** (carried dread; most scenes get 0). Mark `dread: +1/+2`
   only if ALL hold: (1) a *named prior* threat, (2) implicated here, (3) unresolved,
   (4) reader-side asymmetry (irony/helplessness/misreading), (5) **not** an on-page
   detonation. +1 = primed/approaching; +2 = agent present and in contact while the POV
   misreads it. Every mark needs a `dread_source` citing the prior scene. When the
   threat finally acts in full view, set `on_page_detonation: true` (the script zeros
   dread — the buildup credit belongs to the prior scenes).

4. **Build `scenes.json`** (see `templates/scenes.example.json`). Per scene: id, pov,
   location, summary, `scores` (D1–D4, optionally D5/D6 to override), and the dread
   fields. Paste the scene `prose` so D5/D6 compute mechanically.

5. **Run it:**
   ```
   python scene_intensity.py score scenes.json [--config intensity_config.json]
   ```
   Emits per-scene YAML (local composite, band, seam, dread, reader_band) and the dual
   contour. `metrics <prose.txt>` shows just the mechanical dims for spot-checking.

6. **Read the contour.** Local track = honest on-page intensity; reader track = with
   carried dread. Look for: no PEAK (no climax), no REST (relentless/numbing), near-flat
   (monotony), a long BUILD run with no REST/PEAK (the sag), and wide local↔reader gaps
   (scenes running on earned dread). At work level, chart per-chapter median + peak +
   mean dread-gap.

   **Check ruled intent before reporting a contour defect (DIR-011, 2026-07-22).** A
   missing PEAK or a deep valley is only a *defect* if the author didn't rule it. Before
   flagging, sweep the project's own canon — runway close rules, premise register flags,
   rulings blocks. EP 01's contour has no PEAK on either track; its runway rules "ends
   flat on the wrong fact — no punishment scene," so the correct verdict was **"matches
   ruled design — confirm,"** not a climax defect. Same for a valley the premise placed
   on purpose (a silence beat rendered at REST). Report the mechanical lever anyway
   (what would move the band) so the author rules with the tradeoff visible.

## Calibrate mode (v2.2, 2026-07-22) — build the config from the material, gated

Trigger: "build the intensity config" / "calibrate the intensity config" / "calibrate the rubric for <project>". Two legs, then a gate:

1. **Deterministic leg:** `python scene_intensity.py calibrate <scenes.json> [more.json ...] [--out path]`
   scans every scene's prose, measures the somatic-density and fragment-fraction
   distributions, and proposes `d5_bins`/`d6_bins` **only where a real cluster gap
   exists** — it refuses on small/uniform corpora and warns when an "upper cluster"
   is a single scene. The proposal embeds its full `_evidence` block (corpus, n,
   distributions, notes) so the config carries its own cause (DIR-013: a ruling is
   contingent on its cause). It never proposes `band_edges` or `weights` — those move
   only via hand-scored anchor scenes. It never overwrites an existing config
   without `--force`: **a ratified config is frozen.**
2. **Judgment leg (you):** audit the proposal against known register anchors before
   adopting. The trap is noise-slicing: a body-quiet corpus with no crisis cluster
   will yield "gaps" inside the calm band that score calm scenes hot (first live run:
   EP 01's max density 2.4/250 is calm-range; the auto-fit 0.69/1.9 edges were
   rejected and witchwood-inherited bins adopted instead). Also propose
   `somatic_extra` candidates you noticed while reading — body-signal vocabulary the
   base lexicon misses. Record every amendment in a `_judgment_note`.
3. **Gate:** the author ratifies; the config lands in the work folder as
   `intensity_config.json` with `_status`, `_judgment_note`, `_evidence`, and a
   `revisit_when` condition. Unattended runs propose only (DIR-012).

**Circularity guard:** never re-fit the config inside a scoring run, and never
calibrate from a single work then treat its contour as validated — bands fitted to
one story make every story look well-shaped. Recalibrate only over the project's
full scored corpus, on the `revisit_when` trigger, deliberately.

## Calibrating a new project

Defaults are tuned to a horror corpus; recalibrate per project — it takes a few anchor
scenes. Copy `templates/intensity_config.example.json` to `intensity_config.json` beside
your `scenes.json` (auto-loaded) and adjust:

- **`band_edges`** — set the REST/BUILD/HIGH/PEAK cutoffs. Score 4–6 anchor scenes you
  already understand, then place edges in the *gaps* between their clusters (not on top
  of them). Keep `seam_distance` ≈ your between-pass SD.
- **`weights`** — relative pull of the six dims (default doubles stakes/proximity/
  irreversibility). Fix once.
- **`somatic_extra`** — regex terms to add to the somatic lexicon for your register;
  if you change it, re-fit `d5_bins` against a couple of hand-scored scenes.
- **`d5_bins` / `d6_bins`** — the density/fragmentation cutoffs for D5/D6.
- **`d6_bins` operate on the NARRATION-only fragment fraction** (quoted dialogue is
  excluded), and **`dialogue_dominated_frac`** caps D6 below the top for talky scenes.
  This is what separates a dialogue-dense tender scene from an action beat — a global
  fragment-% cannot. Re-fit these against a calm-but-talky anchor and a kill anchor.
- **`dread_lift_bands`** and **`dread_floor`** — how carried dread maps to a reader band.
  Default: +2 promotes one band. To make "predator in contact with the victim" always
  read at least HIGH regardless of how quiet the page is, set
  `"dread_floor": {"2": "HIGH"}`.

**Register caveat — D5 can be a weak signal.** Some registers (e.g. quiet literary
prose) are *bimodal* in somatic density: calm scenes ~1-2/250, visceral crises ~10,
nothing between. There the D5=2 band is unexercised and the composite leans almost
entirely on the author-supplied D1/D2/D4 — the mechanical floor is thin, so the
variance-reduction benefit is smaller than in a visceral register. A grief-driven
scene with zero somatic words can still be HIGH via stakes; that is correct, not a bug.

Run `python scene_intensity.py selftest` after any code change — it asserts the engine
invariants (banding, seams, dread promotion, detonation, the floor rule).

## Known limits (documented, not bugs)

- **Juxtaposition-dread is invisible.** A calm scene intercut with an off-page
  catastrophe (the gate requires the threat *named to the target on the page*) scores
  REST with no dread. The contour will understate it; flag such scenes by hand.
- **The "helplessness" arm of the gate is the softest.** A +1 that cites helplessness
  rather than true irony is where mood can leak in as dread — audit those.

## Changelog

- Dialogue-aware D6 (narration-only fragments + `dialogue_dominated_frac` cap).
- Seam-span off-by-one fixed.
- D3 relabeled author-supplied (not script-mechanized); only D5/D6 are computed.
- D2 predator-POV clause + mandatory `juxtaposition_dread` hand-flag (surfaced, never banded).
- `templates/intensity_config.witchwood-example.json`: a worked literary recalibration (d5_bins moved off the calm cluster; dialogue cap 0.35).
