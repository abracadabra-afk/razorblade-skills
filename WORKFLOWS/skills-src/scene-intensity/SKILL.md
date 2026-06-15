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
