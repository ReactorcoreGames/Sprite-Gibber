# Cryo — 10 presets (registry #19–28)

Module: `presets/cryo.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Freezing: frost creeping over the body, freezing solid as one block, freezing and shattering into shards, sublimating ice.

**Gimmick lock** (new): **Rigid ice**: every multi-chunk preset uses `CHUNK_SHAPE_STRETCH` ≥ 2 for sheet/shard geometry, tint is crisp and opaque (white frost → cyan → deep blue, alpha bleed only on `Melt-aqua`), spin is low and nothing wobbles. Dissolve only as slow sublimation.

**Locales present:** terra ×4, aqua ×2, depth, space, wave, inner.

**Why these locales:** terra (freeze/shatter/frost), aqua (melt rising vs. ice sinking — two genuinely different reads), depth (pressure crush), space (shards tumbling), wave (cold blast), inner (freeze radiating from the core).

**Current state (2026-10-30):** chunks 1–80, explode 0.15–4.0; blast: explode 8, horizontal_split 1, shatter 1; gravity: directional 9, centripetal 1; tint on 10/10, dissolve 6/10, mask 1/10, stretched chunks 5/10.

**Stage 3 notes:**

- Only 5/10 presets currently stretch chunks — bring the rest onto the lock.
- `Cryo-Freeze-terra` is `SINGLE_CHUNK` and ends after 1 tick by design; its animation is the frost tint spreading. Consider a tiny slump (small gravity) so it isn't a still image with a tint fade.

## Stage 3 result (2026-10-30)

- Every multi-chunk preset now stretches (sheets 90°, icicles 0°, shards 30–135°); no dissolve except sublimation (Frost, Melt, Crush, Drift).
- `Freeze-terra` stays a static `SINGLE_CHUNK` statue (its 1-tick flag is intended); the animation is the frost arriving `early` and the colour arc deepening pale cyan → electric blue.
- Never use a positive `TINT_SATURATION_SHIFT` with white/near-white tint: white has no hue, so the shift turns it **pink** (`Shatter-terra-small` went salmon). With many small chunks every pixel is near a border, so put the strong colour on the outer front (`#00C8FF` outer, white inner).
- On warm sprites a `linear` blue ramp passes through muddy purple; reach full tint `early` and carry the progression with the colour arc.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

19. `*.Cryo-Freeze-terra` — sprite petrifies into a single ice block (SINGLE_CHUNK=True), barely moves, icy-white outer tint spreads from edges inward via unidirectional BFS, no dissolve; frozen solid
   - **Flag:** confined: sim ended after 1 tick(s); wide: sim ended after 1 tick(s)
20. `*.Cryo-Shatter-terra` — frozen solid then cracks apart; many chunks with CHUNK_SHAPE_STRETCH for flat sheet-like shards (CHUNK_SHAPE_ANGLE=90 horizontal), high SPIN, light-blue outer to deep-blue inner bidirectional tint, shards settle downward
21. `*.Cryo-Shatter-terra-small` — same as Shatter-terra but high CHUNKS count for many tiny ice splinters with tight CHUNK_SHAPE_STRETCH; chips scatter wide
22. `*.Cryo-Frost-terra` — surface frost accumulation then crumble; very low EXPLODE so chunks barely move, icy-white tint via edges mode (TINT_MODE=edges) spreading inward, chunks=chunks dissolve pattern as ice crumbles away
23. `*.Cryo-Melt-aqua` — ice floating upward as it melts; GRAVITY_ANGLE=0 so chunks rise, icy-white bidirectional tint with high TINT_ALPHA_BLEED_OUTER for translucent fringe, heavy dissolve with DISSOLVE_CURVE>1 slow-out so chunks linger then vanish as they ascent
24. `*.Cryo-Sink-aqua` — flash-frozen in liquid, chunks slow-sink; GRAVITY_ANGLE=180 but very low GRAVITY_STRENGTH and high DRAG for sluggish descent, deep icy-blue tint, minimal dissolve; frozen chunks settling through water
25. `*.Cryo-Crush-depth` — pressure implosion of ice; BLAST_MODE=implode, chunks converge inward, icy-white outer tint collapses to dark-blue inner as pressure increases, moderate dissolve at end as shards vanish under compression
26. `*.Cryo-Drift-space` — zero-gravity ice shard scatter; GRAVITY_STRENGTH=0 so shards float in all directions, high SPIN, light-blue tint, slow gentle dissolve (DISSOLVE_CURVE>1) as shards sublimate over frames
27. `*.Cryo-Blast-wave` — lateral cold shockwave shatters sprite sideways; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 pulls shards rightward, CHUNK_SHAPE_STRETCH for horizontal strips, icy-white outer tint, directional dissolve rightward
28. `*.Cryo-Snap-inner` — internal freeze radiating from core outward; bidirectional tint with large TINT_DEPTH_INNER (deep blue inner, icy-white outer), chunks crack and scatter from center (BLAST_MODE=burst or explode with low EXPLODE), tint animates linear over frames
