# Plague — 8 presets (registry #234–241)

Module: `presets/plague.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Biological infection spreading, pustules; hazard red/green.

**Gimmick lock** (kept): `TINT_NOISE`-driven blotchy pustule pattern + high `TINT_JITTER` on every preset.

**Locales present:** terra ×3, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 35–100, explode 0.2–3.4; blast: explode 4, burst 2, implode 1, horizontal_split 1; gravity: directional 7, centripetal 1; tint on 8/8, dissolve 8/8, mask 1/8, stretched chunks 0/8.

## Stage 3 result (2026-10-31, session 3a)

- Lock kept (`TINT_NOISE` 0.9–1.0 + jitter 0.8–1.0 on every preset). Textured style: infected green flesh (`#7AA02C`, grain 0.15–0.25) with a rash front (depth 0.35) whose colour arcs from the body green to angry red (`#C8243A`), so the rash *blooms* over the animation in noise-warped blotches — that is how "infection spreads" is done without a washed `linear` ramp. Necrotic fade `#4A0C1E`.
- Red over green blends through brown where the fronts meet; kept as necrotic tissue, but `Seep-aqua` and `Contagion-inner` were tightened (lower bleed, green fade, inner-favoured `TINT_BLEND` 0.03) so they don't end as brown mush. `Pustule-terra` uses yellow pus cores and a red rupture fade.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

234. `*.Plague-Spread-terra` — infection spreads visibly before the body breaks down; moderate EXPLODE, hazard-green outer to red inner bidirectional tint with moderate TINT_NOISE and high TINT_JITTER for a blotchy spreading rash, TINT_ANIM=linear so infection visibly spreads over frames, moderate dissolve as infected tissue falls away
235. `*.Plague-Pustule-terra` — pustules rupture across the body; high CHUNKS, moderate EXPLODE, hazard-red and green tint with TINT_NOISE high for a blotchy pustule pattern, TINT_JITTER high, moderate dissolve as ruptured matter scatters
236. `*.Plague-Outbreak-terra-violent` — violent infectious rupture; high EXPLODE and CHUNKS, hazard-green tint at high TINT_OPACITY with TINT_NOISE high, fast dissolve (DISSOLVE_CURVE<1) as the infected mass rapidly disperses
237. `*.Plague-Seep-aqua` — infection disperses into the water as a hazardous bloom; GRAVITY_ANGLE=0 chunks rise, hazard-green tint with TINT_NOISE moderate for a blotchy cloud texture and TINT_ALPHA_BLEED_OUTER high for a spreading cloud edge, slow dissolve (DISSOLVE_CURVE>1) as it disperses while rising
238. `*.Plague-Collapse-depth` — infected mass collapses inward as pustules burst inward; BLAST_MODE=implode, hazard-red tint with TINT_NOISE moderate for blotchy rupture texture, TINT_COLLISION=inner_wins, moderate dissolve as it caves into a diseased heap
239. `*.Plague-Drift-space` — zero-gravity infectious spores and fragments scatter; GRAVITY_STRENGTH=0, moderate EXPLODE, hazard red-green bidirectional tint with TINT_NOISE and TINT_JITTER pushed higher for a blotchier drifting pattern, slow dissolve (DISSOLVE_CURVE>1) as fragments drift and fade
240. `*.Plague-Burst-wave` — struck laterally, infected pustules rupture in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, hazard-green tint at high TINT_OPACITY_OUTER with moderate TINT_NOISE for blotchy rupture texture, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing matter disperses last
241. `*.Plague-Contagion-inner` — infection originates and erupts from a point of contagion at the core; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER hazard-red core spreading to hazard-green outer edge, TINT_NOISE high, DISSOLVE_PATTERN=centrifugal as the infection consumes the chunks from the center out
