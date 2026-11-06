# Acid — 9 presets (registry #64–72)

Module: `presets/acid.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Corrosion: split into large chunks that melt and dissolve, with low-power physics.

**Gimmick lock** (new): **Edge-eating corrosion**: `TINT_MODE="edges"` + `TINT_NOISE` corrosion front on most presets, few large chunks (8–30, per the original type note), low `EXPLODE`, dissolve that eats from the surface inward; lime → deep toxic-green arc (olive read as mud on both sprites; revised in Stage 3).

**Locales present:** terra ×4, aqua, depth, space, wave, inner.

**Why these locales:** All six; terra has melt / slow melt / splash / burn.

**Current state (2026-10-30):** chunks 30–120, explode 0.15–3.5; blast: explode 7, horizontal_split 1, shatter 1; gravity: directional 8, centripetal 1; tint on 9/9, dissolve 9/9, mask 1/9, stretched chunks 0/9.

**Stage 3 notes:**

- Current chunk counts are 30–120; the original type intent is *large* chunks melting — bring them down.

## Stage 3 result (2026-10-30)

- Edges-mode corrosion leaves the interior of each piece in the sprite's own colours until the front reaches it; that's Acid's identity against the full-recolour types. Use edges depth ≥ 1.0 when the body should go fully green.
- `Corrode-inner` hollows the cores with `centripetal` dissolve (works because the chunks are big).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

64. `*.Acid-Melt-terra` — standard acid corrosion; low EXPLODE so chunks barely move, TINT_MODE=edges so lime-green tint eats inward from silhouette, TINT_NOISE moderate for irregular corrosion front, TINT_ALPHA_BLEED_OUTER high for eaten-away transparent fringe, heavy dissolve (DISSOLVE_CURVE>1) as surface is consumed
65. `*.Acid-Melt-terra-slow` — prolonged acid exposure; same as Melt-terra but TINT_ANIM=late so corrosion builds gradually, very slow dissolve (DISSOLVE_CURVE high, DISSOLVE_CHUNK_STAGGER high) with most pixels surviving until final frames
66. `*.Acid-Splash-terra` — acid thrown at sprite; moderate EXPLODE for small scatter, CHUNK_MASS_VARIANCE high for uneven chunk sizes mimicking irregular dissolution, lime-green outer to yellow-green inner bidirectional tint, dissolve with DISSOLVE_CHUNK_STAGGER as chunks dissolve at different rates
67. `*.Acid-Burn-terra` — intense acid burn; faster and more violent than Melt; TINT_ANIM=early so green tint peaks quickly, fast dissolve (DISSOLVE_CURVE<1) with DISSOLVE_FADE_COLOR lime-green so pixels shift green before dropout
68. `*.Acid-Bubble-aqua` — chemical reaction produces rising gas bubbles; GRAVITY_ANGLE=0 chunks rise, lime-green outer to yellow-green inner bidirectional tint, TINT_NOISE moderate for bubbling irregular boundary, heavy fast dissolve as reaction completes on ascent
69. `*.Acid-Flood-depth` — acid flooding from all sides, eating inward under pressure; BLAST_MODE=implode, TINT_MODE=edges lime-green tint pressing inward from silhouette, TINT_NOISE high for uneven corrosion front, heavy dissolve as sprite is consumed from outside in
70. `*.Acid-Droplet-space` — acid droplets scatter in zero gravity, corroding slowly; GRAVITY_STRENGTH=0, very low EXPLODE so chunks drift minimally, TINT_MODE=edges for surface corrosion, TINT_NOISE high, heavy slow dissolve (DISSOLVE_CURVE>1 with DISSOLVE_CHUNK_STAGGER) as each chunk is consumed
71. `*.Acid-Spray-wave` — lateral acid spray impact; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, lime-green outer tint, TINT_NOISE moderate, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so chunks dissolve trailing the spray direction
72. `*.Acid-Corrode-inner` — acid eating from within outward; bidirectional tint with large TINT_DEPTH_INNER lime-green radiating from centroid to yellow-green outer, TINT_NOISE high for irregular corrosion spread, low EXPLODE, DISSOLVE_PATTERN=centripetal so innermost pixels dissolve first
