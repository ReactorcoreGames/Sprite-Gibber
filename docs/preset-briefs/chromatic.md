# Chromatic — 7 presets (registry #390–396)

Module: `presets/chromatic.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Chromatic aberration: the object destabilises smoothly out of existence; red/green/blue fringes, opacity flowing toward zero.

**Gimmick lock** (revised): **Revised**: no pixel loss, carried by bidirectional red/blue tint with high alpha bleed on both fronts and a channel-swap colour animation (`TINT_COLOR_*_END`, e.g. red ↔ blue) so the fringes visibly shift every frame. `DISSOLVE=True` + `DISSOLVE_MIN_PCT=1.0` may stay as a late uniform wash, but it can't carry the type.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 35–45, explode 0.2–2.0; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

**Stage 3 notes:**

- Why revised: with `DISSOLVE_MIN_PCT=1.0` every pixel gets the same 'dropout' frame (= FRAMES), so the fade colour is one uniform tint over the last ~3 frames at most 75 % strength; pattern, direction, stagger and curve have no effect. The old lock ('pure fade-colour opacity animation') therefore did almost nothing.

## Stage 3 result (2026-10-31, session 4b)

- Revised lock applied: `DISSOLVE=False` on every preset, bidirectional `#FF0040` red fringe (`outer_wins`, shallow outer front 0.06–0.15) over a deep `#2040FF` blue body, alpha bleed 0.25–0.4 on both fronts, and the channel swap on every preset (`OUTER_END` blue, `INNER_END` red, passing through vivid purple). At 12–40 pieces the border majority makes the red "fringe" a broad red skin with blue cores, so the swap reads as red → purple → blue across the body.
- Locales differ by geometry and arc timing: 20 sagging pieces (terra, curve 1.0); 40 tall slivers flipping almost at once (`-fast`, stretch 3 at 0°, curve 2.5); 30 rising pieces with more bleed (aqua); an overdamped centripetal knot (depth, 0.8/0.24); 16 slow-turning slabs that hold their colours (space, curve 0.5); 12 slivers sheared right by mass variance (wave); noise-warped patches swapping in place (inner, a 3-tick sim by design).
- Tint ramps lerp RGBA, so an `early`/`linear` ramp would also fade in the bleed. A colour arc cannot change alpha: the translucency is constant from frame 1.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

390. `*.Chromatic-Destabilize-terra` — smooth chromatic-aberration destabilization; low EXPLODE and SPIN, red outer to blue inner bidirectional tint, high TINT_ALPHA_BLEED_OUTER and TINT_ALPHA_BLEED_INNER so opacity flows toward transparent smoothly, DISSOLVE_MIN_PCT=1.0 so no pixels are lost — only the fade color and alpha bleed carry the destabilization
391. `*.Chromatic-Destabilize-terra-fast` — rapid destabilization; moderate EXPLODE, red-blue bidirectional tint with high alpha bleed, faster TINT_ANIM/DISSOLVE_CURVE pacing so the fringe-and-fade reads as sudden rather than smooth, still DISSOLVE_MIN_PCT=1.0
392. `*.Chromatic-Drift-aqua` — chromatic fringes separate and rise as the form destabilizes upward; GRAVITY_ANGLE=0 chunks rise, red-blue bidirectional tint with high alpha bleed both sides, slow fade pacing as it ascends, DISSOLVE_MIN_PCT=1.0
393. `*.Chromatic-Collapse-depth` — chromatic fringes collapse inward as the form destabilizes; BLAST_MODE=implode, GRAVITY_MODE=centripetal, red outer to blue inner tint with TINT_COLLISION=blend, high alpha bleed, DISSOLVE_MIN_PCT=1.0 so the compacted mass simply fades rather than vanishing
394. `*.Chromatic-Drift-space` — zero-gravity chromatic destabilization, fringes separate and drift apart; GRAVITY_STRENGTH=0, low EXPLODE, red-blue bidirectional tint with high alpha bleed, very slow fade pacing over many frames, DISSOLVE_MIN_PCT=1.0
395. `*.Chromatic-Sunder-wave` — struck laterally, chromatic fringes shear apart and destabilize in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, red-blue tint with high TINT_ALPHA_BLEED_OUTER, fade color leans toward the trailing (blue) channel, DISSOLVE_MIN_PCT=1.0
396. `*.Chromatic-Unravel-inner` — destabilization spreads outward from a point of failure within, fringes separating as it goes; BLAST_MODE=burst with low EXPLODE, bidirectional red-blue tint with large TINT_DEPTH_INNER and high alpha bleed both sides, fade pacing radiates outward from center, DISSOLVE_MIN_PCT=1.0
