#!/usr/bin/env python3
"""
scene_intensity.py  —  engine for the Scene Intensity Rubric (project-agnostic)

Deterministic layer (this script):
  * mechanical dims  D5 (somatic load) + D6 (pacing surface) from raw prose
  * composite  Intensity = sum(weight_i * D_i)  and Normalized 0-100
  * banding, the spread-based seam rule, carried-dread band derivation
  * validation of the dread layer's rules, YAML emission, dual contour

Judgment layer (an LLM/author supplies, per the rubric):
  * scene segmentation (POV/time/location)        -> scenes.json
  * semantic dims D1 (stakes), D2 (proximity), D4 (irreversibility), D3 (turns)
  * the carried-dread gate: whether a scene earns dread (+1/+2) and its source

EVERY calibrated number lives in a config, not in code, so a new project tunes
weights / band edges / lexicon / D5-D6 thresholds / the dread rule without
touching this file.  Resolution order:  --config PATH  >  ./intensity_config.json
>  built-in DEFAULTS.

Usage:
  python scene_intensity.py metrics <prose.txt> [--config c.json]
  python scene_intensity.py score   <scenes.json> [--config c.json]
  python scene_intensity.py init-config > intensity_config.json   # default config
  python scene_intensity.py init        > scenes.json             # scenes template
  python scene_intensity.py selftest                              # engine math test
"""
from __future__ import annotations
import sys, os, json, re, statistics, argparse, copy

# --------------------------------------------------------------- defaults -----
DEFAULTS = {
    "weights": {"D1": 2, "D2": 2, "D3": 1, "D4": 2, "D5": 1, "D6": 1},  # max 27
    "band_edges": [30.5, 55.5, 75.5],
    "band_names": ["REST", "BUILD", "HIGH", "PEAK"],
    "seam_distance": 4.0,
    "fragment_max_words": 4,
    "d5_bins": [[2.0, 1], [4.5, 2]],          # som/250 <= t -> v ; 0 -> 0 ; else top
    "d6_bins": [[0.10, 1], [0.30, 2]],        # frag_frac < t -> v ; else top
    "d6_long_zero": [0.03, 16.0],             # frag<a and mean_len>b -> D6 0
    "somatic_extra": [],                      # project terms appended to the lexicon
    "dread_cap": 2,
    "dread_lift_bands": 1,                    # how many bands a +2 promotes
    "dread_floor": {},                        # e.g. {"2": "HIGH"}: +2 floors at HIGH
    "dialogue_dominated_frac": 0.35           # >= this share of dialogue caps D6 below top
}

BASE_SOMATIC = [
    r"breath\w*", r"breathe\w*", r"gasp\w*", r"pant\w*", r"wheez\w*",
    r"pulse", r"heartbeat", r"heart\s+(?:pound|rac|hammer)\w*",
    r"blood\w*", r"bleed\w*", r"bled",
    r"sweat\w*", r"flinch\w*", r"recoil\w*", r"shudder\w*", r"shiver\w*",
    r"trembl\w*", r"quiver\w*", r"twitch\w*", r"winc\w*", r"clench\w*",
    r"clamp\w*", r"chok\w*", r"gag\w*", r"gagged", r"retch\w*", r"vomit\w*",
    r"naus\w*", r"dizz\w*", r"tears", r"weep\w*", r"sob\w*",
    r"scream\w*", r"shriek\w*", r"yelp\w*", r"contraction\w*",
    r"shak\w*", r"spasm\w*", r"goosebump\w*", r"spit", r"spat", r"drool\w*",
]
SENT_SPLIT = re.compile(r"[.!?]+(?:\s+|$)|\n{2,}")
WORD_RE = re.compile(r"[A-Za-z']+")

# --------------------------------------------------------------- config -------
def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out

def load_config(path=None, near=None):
    cfg = copy.deepcopy(DEFAULTS)
    chosen = None
    if path:
        chosen = path
    else:
        for cand in [near and os.path.join(os.path.dirname(os.path.abspath(near)), "intensity_config.json"),
                     "intensity_config.json"]:
            if cand and os.path.exists(cand):
                chosen = cand; break
    if chosen:
        cfg = deep_merge(cfg, json.load(open(chosen, encoding="utf-8")))
        cfg["_source"] = chosen
    terms = BASE_SOMATIC + list(cfg.get("somatic_extra", []))
    cfg["_somatic_re"] = re.compile(r"\b(?:%s)\b" % "|".join(terms), re.I)
    cfg["_max_raw"] = sum(w * 3 for w in cfg["weights"].values())
    return cfg

# --------------------------------------------------------------- mechanics ----
def sentences(text):
    return [s.strip() for s in SENT_SPLIT.split(text) if s and s.strip()]

DQUOTE_RE = re.compile(r'["\u201c\u201d]')

def mechanical_dims(text, cfg):
    sents = sentences(text)
    words = WORD_RE.findall(text)
    nwords = max(len(words), 1)
    nsents = max(len(sents), 1)
    fmax = cfg["fragment_max_words"]
    mean_len = nwords / nsents

    # D5 -- involuntary somatic signals per 250 words
    hits = cfg["_somatic_re"].findall(text)
    som = len(hits) / nwords * 250
    d5 = 0
    if som > 0:
        d5 = len(cfg["d5_bins"]) + 1
        for thr, val in cfg["d5_bins"]:
            if som <= thr:
                d5 = val; break

    # D6 -- action cadence. Fragment fraction is computed over NARRATION sentences
    # only (a sentence carrying a quote mark is dialogue and is excluded), so
    # dialogue-dense tender prose does not read as action-staccato. A scene that is
    # dialogue-dominated is conversational, not fast, so D6 is capped below the top.
    narr = [s for s in sents if not DQUOTE_RE.search(s)]
    n_narr = max(len(narr), 1)
    dialogue_frac = (nsents - len(narr)) / nsents
    narr_frags = sum(1 for s in narr if len(WORD_RE.findall(s)) <= fmax)
    narr_frag_frac = narr_frags / n_narr
    all_frags = sum(1 for s in sents if len(WORD_RE.findall(s)) <= fmax)

    d6 = len(cfg["d6_bins"]) + 1
    for thr, val in cfg["d6_bins"]:
        if narr_frag_frac < thr:
            d6 = val; break
    lz = cfg.get("d6_long_zero")
    if lz and narr_frag_frac < lz[0] and mean_len > lz[1]:
        d6 = 0
    dd = cfg.get("dialogue_dominated_frac")
    if dd and dialogue_frac >= dd:
        d6 = min(d6, len(cfg["d6_bins"]))      # cap at one below top

    return {"D5": d5, "D6": d6, "metrics": {
        "words": nwords, "sentences": nsents,
        "somatic_per_250": round(som, 2),
        "somatic_hits": sorted(set(h.lower() for h in hits)),
        "mean_sentence_len": round(mean_len, 1),
        "fragment_pct": round(all_frags / nsents * 100, 1),
        "narration_fragment_pct": round(narr_frag_frac * 100, 1),
        "dialogue_pct": round(dialogue_frac * 100, 1)}}

# --------------------------------------------------------------- scoring ------
def composite(dims, cfg):
    raw = sum(cfg["weights"][k] * float(dims[k]) for k in cfg["weights"])
    return raw, round(raw / cfg["_max_raw"] * 100)

def band_of(n, cfg):
    for edge, name in zip(cfg["band_edges"], cfg["band_names"]):
        if n < edge:
            return name
    return cfg["band_names"][-1]

def reader_band(band, dread, cfg):
    names = cfg["band_names"]
    if dread <= 0:
        return band
    if dread == 1:
        return band + " (elevated)"
    idx = min(names.index(band) + cfg.get("dread_lift_bands", 1), len(names) - 1)
    fb = cfg.get("dread_floor", {}).get(str(dread))
    if fb in names:
        idx = max(idx, names.index(fb))
    return names[idx]

def seam_flag(n, cfg, pass_bands=None):
    near = min(abs(n - e) for e in cfg["band_edges"])
    if not (near <= cfg["seam_distance"] or (pass_bands and len(set(pass_bands)) > 1)):
        return False, None
    names = cfg["band_names"]
    k = min(range(len(cfg["band_edges"])), key=lambda j: abs(n - cfg["band_edges"][j]))
    adj = {names[k], names[k + 1]} | set(pass_bands or [])
    return True, "/".join(sorted(adj, key=names.index))

def validate_dread(scene, dread, cfg):
    w = []
    if dread < 0 or dread > cfg["dread_cap"]:
        w.append("dread %d out of range (cap %d)" % (dread, cfg["dread_cap"]))
    if dread > 0 and not scene.get("dread_source"):
        w.append("nonzero dread without dread_source (uncited marks are invalid)")
    if int(scene.get("dread", 0) or 0) > 0 and scene.get("on_page_detonation"):
        w.append("dread set but on_page_detonation=true -> gate cond. 5: scored local, dread=0")
    return w

def score_scene(scene, cfg, prose=None, passes=None):
    rec = {"id": scene["id"], "pov": scene.get("pov", ""),
           "location": scene.get("location", ""), "summary": scene.get("summary", "")}
    passes = passes or scene.get("passes")
    if prose is None:
        prose = scene.get("prose")
    if passes:
        norms, bands = [], []
        for p in passes:
            _, nn = composite(p, cfg); norms.append(nn); bands.append(band_of(nn, cfg))
        normalized = round(statistics.mean(norms), 1)
        dims = {k: round(statistics.mean(p[k] for p in passes), 2) for k in cfg["weights"]}
        rec["passes"] = len(passes)
        rec["composite_sd"] = round(statistics.pstdev(norms), 2) if len(norms) > 1 else 0.0
        pass_bands = bands
    else:
        dims = dict(scene.get("scores", {}))
        if prose is not None:
            m = mechanical_dims(prose, cfg)
            dims.setdefault("D5", m["D5"]); dims.setdefault("D6", m["D6"])
            rec["metrics"] = m["metrics"]
        raw, normalized = composite(dims, cfg)
        rec["intensity"] = raw
        pass_bands = None

    band = band_of(normalized, cfg)
    seam, span = seam_flag(normalized, cfg, pass_bands)
    dread = int(scene.get("dread", 0) or 0)
    if scene.get("on_page_detonation"):
        dread = 0
    rec.update({"scores": {k: dims[k] for k in cfg["weights"]},
                "normalized": normalized, "band": band, "seam": seam})
    if seam:
        rec["seam_span"] = span
    rec.update({"dread": dread, "dread_source": scene.get("dread_source"),
                "reader_band": reader_band(band, dread, cfg)})
    if scene.get("juxtaposition_dread"):
        rec["juxtaposition_dread"] = True
        rec["juxtaposition_source"] = scene.get("juxtaposition_source")
    w = validate_dread(scene, dread, cfg)
    if w:
        rec["warnings"] = w
    return rec

# --------------------------------------------------------------- output -------
def emit_yaml(rec, cfg):
    L = ["- id: %s" % rec["id"], "  pov: %s" % rec["pov"],
         "  location: %s" % rec["location"], "  summary: %s" % rec["summary"],
         "  scores: { %s }" % ", ".join("%s: %s" % (k, rec["scores"][k]) for k in cfg["weights"])]
    if "intensity" in rec: L.append("  intensity: %s" % rec["intensity"])
    L.append("  normalized: %s" % rec["normalized"])
    L.append("  band: %s" % rec["band"])
    L.append("  seam: %s%s" % (str(rec["seam"]).lower(),
                               ("   # " + rec["seam_span"]) if rec.get("seam_span") else ""))
    if "composite_sd" in rec:
        L.append("  composite_sd: %s  # over %d passes" % (rec["composite_sd"], rec["passes"]))
    L.append("  dread: %s%s" % ("+" if rec["dread"] > 0 else "", rec["dread"]))
    if rec.get("dread_source"): L.append('  dread_source: "%s"' % rec["dread_source"])
    L.append("  reader_band: %s" % rec["reader_band"])
    if rec.get("juxtaposition_dread"):
        L.append("  juxtaposition_dread: true   # hand-flag: off-page catastrophe; bands unchanged")
        if rec.get("juxtaposition_source"):
            L.append('  juxtaposition_source: "%s"' % rec["juxtaposition_source"])
    for warn in rec.get("warnings", []):
        L.append("  # WARNING: " + warn)
    return "\n".join(L)

def contour(records):
    loc = " . ".join(str(r["normalized"]) for r in records)
    rdr = " . ".join(r["reader_band"].replace(" (elevated)", "*") for r in records)
    out = ["local : " + loc, "reader: " + rdr + "    (* = elevated, not promoted)"]
    lifts = []
    for r in records:
        if r["dread"] > 0:
            if r["dread"] == 1:
                lifts.append("%s +1 (elevated)" % r["id"])
            elif r["reader_band"] != r["band"]:
                lifts.append("%s +%d (%s->%s)" % (r["id"], r["dread"], r["band"], r["reader_band"]))
            else:
                lifts.append("%s +%d (no band change)" % (r["id"], r["dread"]))
    if lifts:
        out.append("dread lifts: " + ", ".join(lifts))
    jx = [r["id"] for r in records if r.get("juxtaposition_dread")]
    if jx:
        out.append("juxtaposition-dread (hand-flagged, not banded): " + ", ".join(jx))
    return "\n".join(out)

# --------------------------------------------------------------- CLI ----------
SCENES_TEMPLATE = {"scenes": [
    {"id": "CH1-S1", "pov": "", "location": "", "summary": "",
     "scores": {"D1": 0, "D2": 0, "D3": 0, "D4": 0},
     "prose": "(optional: paste scene text; D5/D6 fill in from it)",
     "dread": 0, "dread_source": None, "on_page_detonation": False}]}

def cmd_metrics(a):
    cfg = load_config(a.config, near=a.path)
    print(json.dumps({"config": cfg.get("_source", "built-in defaults"),
                      **{k: v for k, v in mechanical_dims(open(a.path, encoding="utf-8").read(), cfg).items()
                         if k != "metrics"},
                      **mechanical_dims(open(a.path, encoding="utf-8").read(), cfg)["metrics"]}, indent=2))

def cmd_score(a):
    cfg = load_config(a.config, near=a.path)
    data = json.load(open(a.path, encoding="utf-8"))
    cfg = deep_merge(cfg, data.get("config", {})) if data.get("config") else cfg
    if data.get("config"):
        terms = BASE_SOMATIC + list(cfg.get("somatic_extra", []))
        cfg["_somatic_re"] = re.compile(r"\b(?:%s)\b" % "|".join(terms), re.I)
        cfg["_max_raw"] = sum(w * 3 for w in cfg["weights"].values())
        # provenance fix (2026-07-22): the merge branch never updated _source, so the
        # banner claimed "built-in defaults" while a per-file config was silently live.
        # A silent fallback/misreport is worse than a crash (DIR-013) — name the source.
        base = cfg.get("_source")
        cfg["_source"] = ("per-file config block in %s" % a.path) + (
            " (over %s)" % base if base else "")
    recs = [score_scene(s, cfg) for s in data["scenes"]]
    print("# config: %s" % cfg.get("_source", "built-in defaults"))
    print("# bands: " + "  ".join("%s<%g" % (n, e) for n, e in zip(cfg["band_names"], cfg["band_edges"] + [100]))
          + "  (seam +/-%g)" % cfg["seam_distance"])
    print()
    for r in recs:
        print(emit_yaml(r, cfg)); print()
    print("# --- contour ---")
    print(contour(recs))

def _gap_edges(vals, lo_label, hi_label):
    """Sort values, find the two largest gaps, propose bin edges at gap midpoints.
    Returns (edges, note). Small-corpus honest: if a gap structure isn't there
    (uniform spread, or too few points), say so instead of inventing edges."""
    v = sorted(vals)
    n = len(v)
    if n < 4 or v[-1] - v[0] < 1e-9:
        return None, "corpus too small/uniform (%d scenes, range %.2f-%.2f) — keep defaults" % (n, v[0] if v else 0, v[-1] if v else 0)
    gaps = [(v[i + 1] - v[i], (v[i] + v[i + 1]) / 2.0) for i in range(n - 1)]
    gaps.sort(reverse=True)
    g1, g2 = gaps[0], (gaps[1] if len(gaps) > 1 else None)
    spread = v[-1] - v[0]
    if g1[0] < spread * 0.25:
        return None, "no clear cluster gap (largest gap %.2f over spread %.2f) — keep defaults" % (g1[0], spread)
    edges = sorted([round(g1[1], 2)] + ([round(g2[1], 2)] if g2 and g2[0] >= spread * 0.15 else []))
    note = "edge(s) placed in measured gap(s); %s cluster %.2f-%.2f, %s cluster %.2f-%.2f" % (
        lo_label, v[0], max(x for x in v if x < edges[0]),
        hi_label, min(x for x in v if x > edges[-1]), v[-1])
    upper = [x for x in v if x > edges[-1]]
    if len(upper) < 2:
        note += "; WARNING: upper cluster is a single scene — edge statistically unreliable, judgment leg must audit against known register anchors before adopting"
    if len(edges) == 1:
        note += "; SECOND edge unexercised in this corpus (bimodal) — provisional, keep default upper edge"
    return edges, note

def cmd_calibrate(a):
    """Evidence-first config proposal from one or more scenes.json corpora.
    Mechanical bins only (d5/d6) — band_edges and weights move ONLY via
    hand-scored anchor scenes (the judgment layer + the author), never here.
    Never overwrites an existing config without --force: a ratified config is
    frozen (re-pin is a deliberate act, not a side effect of rescoring)."""
    cfg = load_config(a.config)
    dens, frags, dlg, corpus, n = [], [], [], [], 0
    for path in a.paths:
        data = json.load(open(path, encoding="utf-8"))
        for s in data.get("scenes", []):
            if not s.get("prose"):
                continue
            m = mechanical_dims(s["prose"], cfg)["metrics"]
            dens.append(m["somatic_per_250"])
            frags.append(m["narration_fragment_pct"] / 100.0)
            dlg.append(m["dialogue_pct"] / 100.0)
            n += 1
        corpus.append(os.path.basename(path))
    if n == 0:
        print("calibrate: no scenes with prose found", file=sys.stderr); return 2
    d5_edges, d5_note = _gap_edges(dens, "calm", "crisis")
    d6_edges, d6_note = _gap_edges(frags, "ruminative", "staccato")
    prop = {
        "_status": "proposed — author ratifies; frozen after ratify (re-pin deliberately, never auto)",
        "_evidence": {
            "date": __import__("datetime").date.today().isoformat(),
            "corpus": corpus, "n_scenes": n,
            "somatic_per_250": [round(x, 2) for x in sorted(dens)],
            "narr_frag_frac": [round(x, 3) for x in sorted(frags)],
            "dialogue_frac": [round(x, 3) for x in sorted(dlg)],
            "d5_note": d5_note, "d6_note": d6_note,
            "band_edges_note": "NOT auto-fit — edges move only via hand-scored anchor scenes (rubric: place edges in gaps between anchor clusters, then keep fixed)",
        },
    }
    if d5_edges:
        bins = [[d5_edges[0], 1]] + ([[d5_edges[1], 2]] if len(d5_edges) > 1 else [[DEFAULTS["d5_bins"][1][0], 2]])
        prop["d5_bins"] = bins
    if d6_edges:
        bins = [[d6_edges[0], 1]] + ([[d6_edges[1], 2]] if len(d6_edges) > 1 else [[DEFAULTS["d6_bins"][1][0], 2]])
        prop["d6_bins"] = bins
    if max(dlg) >= DEFAULTS["dialogue_dominated_frac"]:
        prop["_evidence"]["dialogue_note"] = "max dialogue share %.2f — re-fit dialogue_dominated_frac against a calm-talky anchor" % max(dlg)
    out = a.out or "intensity_config.json"
    if os.path.exists(out) and not a.force:
        print("calibrate: %s already exists — a ratified config is frozen; use --force to re-pin" % out, file=sys.stderr)
        print(json.dumps(prop, indent=2))
        return 1
    json.dump(prop, open(out, "w", encoding="utf-8"), indent=2)
    print("# proposed config written to %s (status: proposed — ratify before relying on it)" % out)
    print(json.dumps(prop, indent=2))
    return 0

def cmd_initcfg(a):
    print(json.dumps(DEFAULTS, indent=2))

def cmd_init(a):
    print(json.dumps(SCENES_TEMPLATE, indent=2))

def cmd_selftest(a):
    cfg = load_config()
    ok = True
    def check(name, cond):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s" % ("OK" if cond else "FAIL", name))
    # composite extremes
    check("all-3 dims -> 100 PEAK", composite({k: 3 for k in cfg["weights"]}, cfg)[1] == 100
          and band_of(100, cfg) == "PEAK")
    check("all-0 dims -> 0 REST", composite({k: 0 for k in cfg["weights"]}, cfg)[1] == 0
          and band_of(0, cfg) == "REST")
    # band edges
    check("band edges 30/56/76", band_of(30, cfg) == "REST" and band_of(31, cfg) == "BUILD"
          and band_of(56, cfg) == "HIGH" and band_of(76, cfg) == "PEAK")
    # seams
    check("seam by distance (33 near 30.5)", seam_flag(33, cfg)[0] is True)
    check("no seam mid-band (45)", seam_flag(45, cfg)[0] is False)
    check("seam by spread (mean clean, passes split)",
          seam_flag(54, cfg, ["BUILD", "HIGH"])[0] is True)
    # dread
    s_irony = {"id": "x", "scores": {"D1": 1, "D2": 1, "D3": 1, "D4": 1, "D5": 0, "D6": 2},
               "dread": 2, "dread_source": "prior scene"}
    r = score_scene(s_irony, cfg)
    check("local BUILD + dread+2 -> reader HIGH", r["band"] == "BUILD" and r["reader_band"] == "HIGH")
    s_elev = dict(s_irony, dread=1)
    check("dread+1 -> elevated, no promote",
          score_scene(s_elev, cfg)["reader_band"].endswith("(elevated)"))
    s_det = {"id": "y", "scores": {"D1": 3, "D2": 3, "D3": 3, "D4": 3, "D5": 3, "D6": 3},
             "dread": 2, "dread_source": "p", "on_page_detonation": True}
    check("on_page_detonation zeroes dread", score_scene(s_det, cfg)["dread"] == 0)
    # configurable: a HIGH floor for +2, and custom band names
    cfg2 = load_config()
    cfg2 = deep_merge(cfg2, {"dread_floor": {"2": "HIGH"}})
    s_rest = {"id": "z", "scores": {"D1": 1, "D2": 1, "D3": 0, "D4": 0, "D5": 0, "D6": 1},
              "dread": 2, "dread_source": "p"}
    base_rb = score_scene(s_rest, load_config())["reader_band"]
    floor_rb = score_scene(s_rest, cfg2)["reader_band"]
    check("dread_floor config lifts REST-local +2 to HIGH",
          band_of(score_scene(s_rest, cfg2)["normalized"], cfg2) == "REST" and floor_rb == "HIGH"
          and base_rb != "HIGH")
    # metrics directional
    sat = mechanical_dims("Blood. She gasped and bled and trembled, heart pounding, she screamed.", cfg)
    quiet = mechanical_dims("He considered the orchard and the long slow afternoon and the price of wheat in spring.", cfg)
    check("metrics: saturated D5 high > quiet D5", sat["D5"] > quiet["D5"] and quiet["D5"] == 0)
    jxr = score_scene({"id": "j", "scores": {"D1": 1, "D2": 0, "D3": 1, "D4": 0, "D5": 0, "D6": 1},
                       "juxtaposition_dread": True, "juxtaposition_source": "off-page death of a bound party"}, cfg)
    check("juxtaposition_dread surfaces without changing band",
          jxr.get("juxtaposition_dread") is True and jxr["reader_band"] == jxr["band"])
    # calibrate: bimodal data -> edge in the gap; uniform/small data -> refuse
    e_bi, _ = _gap_edges([1.5, 1.7, 2.0, 1.8, 9.5, 10.2], "calm", "crisis")
    check("calibrate: bimodal corpus places an edge inside the gap",
          e_bi is not None and 2.0 < e_bi[0] < 9.5)
    e_uni, note_uni = _gap_edges([1.0, 1.1, 1.2], "a", "b")
    check("calibrate: small/uniform corpus refuses to invent edges",
          e_uni is None and "defaults" in note_uni)
    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

def main():
    ap = argparse.ArgumentParser(description="Scene Intensity Rubric engine (project-agnostic)")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("metrics"); p.add_argument("path"); p.add_argument("--config")
    p = sub.add_parser("score");   p.add_argument("path"); p.add_argument("--config")
    p = sub.add_parser("calibrate"); p.add_argument("paths", nargs="+"); p.add_argument("--config"); p.add_argument("--out"); p.add_argument("--force", action="store_true")
    sub.add_parser("init-config")
    sub.add_parser("init")
    sub.add_parser("selftest")
    a = ap.parse_args()
    if a.cmd == "metrics": cmd_metrics(a)
    elif a.cmd == "score": cmd_score(a)
    elif a.cmd == "calibrate": sys.exit(cmd_calibrate(a))
    elif a.cmd == "init-config": cmd_initcfg(a)
    elif a.cmd == "init": cmd_init(a)
    elif a.cmd == "selftest": sys.exit(cmd_selftest(a))
    else: ap.print_help()

if __name__ == "__main__":
    main()
