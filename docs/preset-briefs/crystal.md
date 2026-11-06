# Crystal — 7 presets (registry #266–272)

Module: `presets/crystal.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Shatter into crystal shards; light blue / pink.

**Gimmick lock** (new): **Translucent gem shards**: `CHUNK_SHAPE_STRETCH` on every preset, alpha bleed for translucency, a little `BOUNCE` for a glassy clink, no dissolve. Differs from Cryo (opaque frost progression).

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six; aqua and inner are both 'bloom' (growth) reads, distinct by direction — rising vs. bursting from a seed.

**Current state (2026-10-30):** chunks 45–70, explode 0.2–3.2; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 0/7, mask 0/7, stretched chunks 7/7.

## Stage 3 result (2026-10-31, session 3b)

- Lock kept. Glass recipe: a **saturated colour on the outer front** (`#0CA8F4` ice, `#FF1E9A` rose, depth ≈ 1 px) and a **pale clear core** (`#A8EEFF` / `#FFC0E8`) with `TINT_ALPHA_BLEED_INNER` 0.3, `blend` 0.5, no jitter, no `TINT_NOISE`, grain 0.06. The first try (white edges around a saturated translucent body) came out pastel. Stretched shards are mostly border pixels, so the outer colour is the shard colour and the clear core is the accent. Crisp and smooth is what separates Crystal from the mottled, grainy Stone/Gold/Rust.
- Every preset is stretched (1.6–3.5) and bounces 0.25–0.55 where there is a floor; the `-pink` variant has fewer, longer shards and a higher clink. `Bloom-aqua` = upright spires (stretch at 0°, low spin) that rise and hang from the surface like a crystal cluster, deepening to vivid cyan. `Collapse-depth` = `vortex` geode (shards swirl into a magenta cluster). `Bloom-inner` = 20 wider two-tone gem shards (rose core, 1 px blue rim, `instant`).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

266. `*.Crystal-Shatter-terra` — standard crystalline shatter; moderate-high CHUNKS, high EXPLODE and SPIN, light-blue tint at high TINT_OPACITY_OUTER, CHUNK_SHAPE_STRETCH moderate with CHUNK_SHAPE_ANGLE matching GRAVITY_ANGLE for flat sheet-like shards, no dissolve so shards remain
267. `*.Crystal-Shatter-terra-pink` — pink-crystal variant shatter; same physics as the base, pink tint at high TINT_OPACITY, CHUNK_SHAPE_STRETCH moderate, no dissolve
268. `*.Crystal-Bloom-aqua` — crystal shards drift upward like growing formations; GRAVITY_ANGLE=0 chunks rise, light-blue tint with high TINT_ALPHA_BLEED_OUTER for a translucent gleam, CHUNK_SHAPE_STRETCH moderate, no dissolve
269. `*.Crystal-Collapse-depth` — crystalline form crushed inward into fragments; BLAST_MODE=implode, pink tint with TINT_COLLISION=inner_wins, CHUNK_SHAPE_STRETCH moderate, no dissolve so the crushed shards remain
270. `*.Crystal-Drift-space` — zero-gravity crystal shards scatter and gleam; GRAVITY_STRENGTH=0, high CHUNKS, high SPIN, light-blue tint, CHUNK_SHAPE_STRETCH moderate, no dissolve
271. `*.Crystal-Sunder-wave` — struck laterally, crystal shatters off in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, CHUNK_SHAPE_ANGLE=90 for shards aligned with the strike, light-blue tint at high TINT_OPACITY_OUTER, no dissolve
272. `*.Crystal-Bloom-inner` — crystalline growth bursts outward from a seed point within; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER pink core spreading to light-blue outer edge, CHUNK_SHAPE_STRETCH moderate, no dissolve
