# The WIW three-step model — what each slot means

Source: CRE's `SCRATCHPAD/WiW Workflow rev1.md` (the three steps, rev1 order: trigger → Therefore → But → Penalty) and `SCRATCHPAD/New WiW Story Model.md` (shapes, the minimal recipe, wound-as-moment). Read those by path at run time when a slot's meaning is in doubt; this file is the map, not the craft. CRE's own definitions are quoted; nothing here is a rule the tool adds.

## Step 1 — Forge: premise / promise / shape

| Slot | CRE's definition | What the check looks for |
|---|---|---|
| **Premise** | "Each opening is a single witnessed instance. No 'keeps,' no 'always,' no pattern. The reader is *in the room* when it happens for the first time." | pattern words (keeps, always, every night, used to); one moment not four sentences |
| **Promise** | "The promise of dread, wrongness, and destruction of something. The horror reader's compact established for future pay-off." | present, not a placeholder |
| **Shape** | Declared from CRE's list: slow burn · single incident · twist/reveal · circular · frame story · epistolary · cat-and-mouse, plus the rhythm shapes: dread curve · slow burn to sudden shock · kishōtenketsu. "Shape determines what the reader is waiting for." | on the list, or recorded as his if he names a new one; asked after the gut, on SPARKs only |

Bag examples, his: *A commuting man turns on the radio in his car. Between stations, in the static, he hears his daughter's voice* (premise). *She's been dead for two years* (promise). Sub-genre is free under the horror promise (dec-034); shape and sub-genre are separate fields.

## Step 2 — Want vs Inescapability

| Slot | CRE's definition |
|---|---|
| **Want** | "Never stated as 'she wants to X.' It's shown in the first physical move: stacking the chair, turning off the radio, putting the card in her pocket, boarding the bus. Surface-level human reaction that ignores the inescapable that is already in the room or coming soon. THE BRIDGE TO FIRST BUT ESCALATION." |
| **Rationale** | "The reason the character acts and reacts like they do — their ultimate goal preserving and achieving their want — surface-level response." |
| **Inescapable** | "The driver that forces engagement with the premise. The reason beneath the rationale the story surfaces, but never states. The opposite of what the character wants to face because it is their worst fear represented by the wrongness, the supernatural, the antagonistic engine that refuses them." Recorded as two halves: **force** (what refuses) and **truth** (what the force represents). |
| **Story** | "The fight between rationale-fueled want and the inescapable that will lead to escalating attempts and failures until climax and confrontation. The 'do this' / 'or else' clause. Pure conflict with stakes." Recorded as **must** / **or else**. |
| **Setting** | 3–4 sensory details that feel *off*, each an early signature of the Inescapable — tagged **force** or **truth**. Era, region, class only when the premise needs them (`placing facts — none needed` otherwise). Texture is filled at the mic (DIR-017 §2). |

His worked Step 2 (radio): Want *Drive home. Get through the commute. Don't think about the heavy stuff.* · Rationale *Much easier to ignore than facing the haunting truth of what happened his daughter.* · Inescapable *His daughter wants to be heard. No matter what he tries to stop it.* · Story *He must silence her accusations or else admit the horrible truth of what happened to her.*

## Step 3 — Escalations

| Slot | CRE's definition |
|---|---|
| **trigger** | the thing that just happened that the character now has to answer |
| **Therefore** | "forced action — each 'therefore' is the only logical next move *given that specific denial*. Not a new random event. A consequence." |
| **But** | "success denied — each 'but' names the exact thing the character was counting on that the world refuses." Recorded with `denies:` naming the assumption. |
| **Penalty** | "What each escalation and failed attempt subtracts from the character's well-being and arsenal of options." Recorded with `subtracts:` naming the loss; each must be a loss the previous did not take. |
| **Climax** | "Final play — the inescapable collides with the character and the character must play their last, best hand, and/or fail completely." The ultimate Therefore. |
| **Cut** | the last line on the page; the peak, before any explanation |
| **Pay-off** | "The unsaid, implied, and thematic resonance that surfaces and survives after the story ends. What the reader is ultimately left with." Off the page — budget `(~0)`. |
| **Opening** | the witnessed instance on the page plus the want in the first move; budgeted, not re-described |

Budget per section (Opening, each E, Climax, Cut) sums inside the band. The band is prescriptive at plan time; the draft is never graded against it.

His worked Step 3 (radio), the shape a filled spine should match:

```
E1  trigger: He hears his daughter's voice on the radio.
    therefore: The man turns off the radio.
    but: The radio turns back on.
    penalty: Forces him to think about his dead daughter.
E2  trigger: The radio won't stay off.
    therefore: The man changes the station to something else.
    but: His daughter's voice bleeds through the broadcast on every channel.
    penalty: Forces him to think of her accusations about him.
E3  trigger: Nothing stops her voice or his thoughts about her.
    therefore: He pulls over on the side of the road and shuts the car off. Silence at last.
    but: The radio turns back on, speaking to him directly — asking him to admit his guilt.
    penalty: Must face his apex fear — confess what he had never wanted to.
CLIMAX (ultimate therefore): He pops the hood, gets out of the car, and tears the battery out.
THE CUT: Silence achieved, car wrecked … until he hears his daughter's voice, right behind him. Not buried in the static.
THE PAY-OFF: Cannot escape his daughter, or his sins, by trying to snuff them out in silence. They are literally behind him now.
```

The full fixture: `evals/fixtures/pass-spine-radio-stamped.md`.

## What is deliberately not in this model

- **No flaw.** The novel route (Witchwood, Craft Beliefs arc chain) is flaw-first and untouched. Here the wound is the entry point, shown through action; the character's response to the denial is what tells the reader who they are.
- **No backstory.** Pattern and declaration are what backstory looks like in short form.
- **No knot field on the triage.** The premise is the wound. `episode-init` reads `## Premise` + `## Promise` where it used to read the what-if and the knot.
