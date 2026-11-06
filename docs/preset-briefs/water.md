# Water — 12 presets (registry #52–63)

Module: `presets/water.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Turning into water / elemental water: splashes, pools, bubbles, tides, pressure.

**Gimmick lock** (new): **Translucent liquid droplets**: high chunk counts (150+), round chunks, translucent blue (opacity 1.0 with alpha bleed 0.15–0.35 as the translucency; revised in Stage 3) — translucency is what separates Water from Blood (opaque) and Goo (viscous).

**Locales present:** terra ×3, aqua ×2, depth ×2, space ×2, wave ×2, inner.

**Why these locales:** All six; terra has splash / pool / surge, aqua has merge vs. bubble, depth has hydraulic crush vs. draining vortex, space has tumbling droplets vs. noise drift, wave has current vs. tidal smash.

**Current state (2026-10-30):** chunks 80–300, explode 0.12–6.0; blast: explode 9, horizontal_split 2, shatter 1; gravity: directional 9, centripetal 1, vortex 1, noise 1; tint on 12/12, dissolve 11/12, mask 1/12, stretched chunks 0/12.

## Stage 3 result (2026-10-30)

- **Lock revised:** partial opacity mixed the sprite's own colours back in (orange + blue = grey). Translucency now comes only from alpha bleed; opacity is 1.0.
- At 150+ chunks every chunk is ~1 px across, so chunk-mode two-colour tint is meaningless. Most presets use `TINT_MODE="edges"` with a deep (≥ 2.0) front: light at the silhouette, deep inside, independent of chunk size. Foam (`Surge`, `Tidal`) comes from a white `DISSOLVE_FADE_COLOR`, because unidirectional edges tint can't put a white rim over a blue body.
- `Bubble-aqua` is the deliberate exception to 150+ chunks (40 hollow bubbles: 1 px white rim, translucent blue inside).
- Note: `centrifugal`/`centripetal` dissolve is per chunk centroid, so with tiny chunks it behaves like `random`.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

52. `*.Water-Splash-terra` — sprite liquefies and splashes outward; moderate CHUNKS scatter low and wide, mid-blue outer to light-blue inner bidirectional tint, TINT_NOISE moderate for fluid blob boundaries, moderate dissolve as droplets absorb downward
53. `*.Water-Pool-terra` — sprite collapses into a pool; very low EXPLODE so chunks fall nearly straight down, CHUNK_BIAS=core so mass concentrates centrally, deep blue tint unidirectional from edges, high DRAG for sluggish watery descent, minimal dissolve
54. `*.Water-Surge-terra` — powerful water blast impact; high EXPLODE, many CHUNKS, CHUNK_BIAS=shell for outward spray from edges, blue outer to white-blue inner bidirectional tint, TINT_NOISE high for chaotic fluid shapes, dissolve with DISSOLVE_CHUNK_STAGGER as droplets scatter and absorb
55. `*.Water-Merge-aqua` — sprite dissolves into surrounding water; GRAVITY_ANGLE=0 chunks rise gently, bidirectional tint blue outer to near-white inner with high TINT_ALPHA_BLEED_OUTER for translucent liquid fringe, heavy dissolve (DISSOLVE_CURVE>1 slow then fast) as sprite is absorbed
56. `*.Water-Bubble-aqua` — sprite converts to rising air bubbles; GRAVITY_ANGLE=0, high DRAG so bubbles drift slowly upward, low CHUNKS, bidirectional tint pale-blue outer to near-white inner, TINT_ALPHA_BLEED_INNER high for hollow bubble translucency, dissolve rapidly at top
57. `*.Water-Hydraulic-depth` — hydraulic pressure crush; BLAST_MODE=implode, deep blue outer tint compressing inward to white-blue inner pressure core, TINT_NOISE low for clean pressure boundary, moderate dissolve as sprite is compressed to nothing
58. `*.Water-Vortex-depth` — water caught in a draining vortex; GRAVITY_MODE=vortex, BLAST_MODE=explode then chunks arc inward in a tightening spiral, deep-blue outer compresses to white-blue pressure core, centripetal dissolve as sprite is consumed
59. `*.Water-Droplet-space` — zero-gravity water droplets floating apart; GRAVITY_STRENGTH=0, moderate CHUNKS with low SPIN (liquid droplets tumble slowly), blue bidirectional tint with TINT_NOISE for organic blob shapes, slow dissolve (DISSOLVE_CURVE>1) as droplets evaporate in vacuum
60. `*.Water-Drift-space` — weightless water in noise gravity; GRAVITY_MODE=noise so droplets wander in slowly-shifting organic directions with no fixed pull, pale-blue bidirectional tint with TINT_NOISE, slow noise dissolve as droplets evaporate
61. `*.Water-Current-wave` — swept sideways by a steady current; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, high DRAG so chunks carry momentum but decelerate, blue outer tint, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 as chunks dissolve trailing the current
62. `*.Water-Tidal-wave` — smashed by a tidal surge; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, high EXPLODE and many CHUNKS, TINT_NOISE high for violent chaotic fluid boundary, blue-to-white bidirectional tint, fast dissolve (DISSOLVE_CURVE<1) as spray disperses
63. `*.Water-Rupture-inner` — internal water pressure rupture from core; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER white-blue pressure core spreading to deep-blue outer, TINT_NOISE moderate for organic fluid spread, DISSOLVE_PATTERN=centrifugal outward from center
