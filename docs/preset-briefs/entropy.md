# Entropy — 7 presets (registry #376–382)

Module: `presets/entropy.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Desaturate, dissolve, turn black.

**Gimmick lock** (kept): strongly negative saturation shift, black/near-black `DISSOLVE_FADE_COLOR`, slow/late pacing — decay is gradual.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 35–45, explode 0.2–1.8; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 4b)

- Lock kept: saturation −1.0 everywhere, a pure black `DISSOLVE_FADE_COLOR` at strength 1.0, slow dissolve curves (1.6–2.4). The tint is not a colour: a flat black edges-mode front at opacity 0.75 (`TINT_SINGLE_COLOR`, depth 3.0) ramps in with the saturation shift, so the sprite **drains to grey, then darkens toward black**, and each pixel goes fully black just before it vanishes. Desaturation plus a black fade alone left the lion peach until its pixels dropped.
- Kept apart from Wither (grey husks with crack lines and a grey fade, 18–60 slabs): Entropy has no crack line or colour, darkens to black and fades to nothing (1–2 % residue).
- The ramp is `early` on most presets so the drain reads, `linear` on `-slow`, and `late` on `Drift-space` (colour held, then drained). Locales differ by dissolve: `random` wink-out while slumping (terra); 40 pieces dropping one at a time and popping out (`-slow`, `chunks` + `LAUNCH_STAGGER`); top-first `gravity_aligned` while rising (aqua); `random` in an overdamped 50-piece centripetal husk (depth); 24 slabs eaten from their own rims (`centrifugal`, which works on big pieces) in space; a left-to-right front (wave); `noise` blotches at 200 grains in place (inner).
- **Fix applied:** `Sunder-wave` keeps `DISSOLVE_DIRECTION=270` on purpose: the entropy front sweeps *with* the push (the left side goes first). `Unmake-inner` uses `explode`, not `burst` (see the workflow doc).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

376. `*.Entropy-Decay-terra` — body desaturates and fades to black as it falls apart; low EXPLODE, TINT_SATURATION_SHIFT strongly negative, DISSOLVE_FADE_COLOR black with high DISSOLVE_FADE_STRENGTH so chunks darken just before dropping out, moderate dissolve
377. `*.Entropy-Decay-terra-slow` — gradual entropic decay over the full animation; very low EXPLODE, TINT_SATURATION_SHIFT negative, DISSOLVE_FADE_COLOR black, slow dissolve (DISSOLVE_CURVE>1) as the form fades to black over many frames
378. `*.Entropy-Seep-aqua` — entropy dissolves the form upward into nothing, as if being drawn out of existence; GRAVITY_ANGLE=0 chunks rise, TINT_SATURATION_SHIFT negative, DISSOLVE_FADE_COLOR black, slow dissolve as it darkens and fades while rising
379. `*.Entropy-Collapse-depth` — entropic decay collapses the form inward into a fading black husk; BLAST_MODE=implode, GRAVITY_MODE=centripetal, TINT_SATURATION_SHIFT strongly negative, DISSOLVE_FADE_COLOR black, moderate dissolve
380. `*.Entropy-Drift-space` — zero-gravity entropic decay, fragments desaturate and blacken as they drift apart into the void; GRAVITY_STRENGTH=0, low EXPLODE, TINT_SATURATION_SHIFT negative, DISSOLVE_FADE_COLOR black, slow dissolve (DISSOLVE_CURVE>1) over many frames
381. `*.Entropy-Sunder-wave` — struck laterally, entropy spreads in that direction like a rot passing through, darkening as it goes; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, TINT_SATURATION_SHIFT negative, DISSOLVE_FADE_COLOR black, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments decay last
382. `*.Entropy-Unmake-inner` — entropic collapse spreads outward from a point of decay within, the body unmaking itself from the inside; BLAST_MODE=burst with low EXPLODE, TINT_SATURATION_SHIFT strongly negative, DISSOLVE_FADE_COLOR black, DISSOLVE_PATTERN=centrifugal as it unmakes outward from center
