# Stone — 9 presets (registry #249–257)

Module: `presets/stone.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Petrification: one statue, slabs, medium stones, pebbles.

**Gimmick lock** (new): **Heavy and opaque**: grey tint at high opacity, no dissolve (except pebble dust), high gravity and low spin, and the size ladder single → slab → medium → pebble.

**Locales present:** terra ×4, aqua, depth, space, wave, inner.

**Why these locales:** All six; aqua is 'sinks slowly' (stone doesn't float).

**Current state (2026-10-30):** chunks 1–130, explode 0.15–2.6; blast: explode 6, implode 1, horizontal_split 1, burst 1; gravity: directional 8, centripetal 1; tint on 9/9, dissolve 1/9, mask 0/9, stretched chunks 0/9.

**Stage 3 notes:**

- `Stone-Petrify-terra-single` ends after 1 tick by design (single chunk resting on the floor); its animation is the petrification tint.

## Stage 3 result (2026-10-31, session 3b)

- Lock kept. Stone is real grey rock: a mottled shade front (`#4E4B46`–`#6A6761`, jitter 0.9–1.0, `TINT_NOISE` 0.5–0.8, `blend`) into a warm-grey body (`#8C8A84`, light variant `#A6A299`), `TINT_GRAIN` 0.2–0.3, opacity 1.0, no bleed. Keep the shade close to the body. At 15–30 chunks most pixels are chunk-border pixels (see workflow doc → *Textured materials*), so a dark shade becomes a hard outline.
- Size ladder: `Petrify-terra-single` 1 (a `linear` grey ramp with saturation −0.5, so the mid-frames drain the colour instead of muddying it; 1-tick sim by design) → `Shatter-terra-slab` 6 horizontal strata slabs (`CHUNK_SHAPE_STRETCH` 1.8 at 90°, no bounce) → `-medium` 20 → `Crumble-terra-pebble` 110 skittering pebbles (bounce 0.3, and the only dissolve: whole `chunks` puff away, min 0.65).
- Locales differ mechanically: `Sink-aqua` wet blue-grey stones sinking at different rates (`CHUNK_MASS_VARIANCE` 0.9, gravity 0.18); `Crush-depth` centripetal boulder that darkens under pressure (colour arc); `Drift-space` nine pitted moon-grey boulders (`burst`, so the bottom-sitting lion isn't pushed into the floor); `Sunder-wave` upright shards (stretch at 0°) carried right by 90° gravity; `Fracture-inner` turns to stone chunk by chunk (`per_chunk`) along 1 px dark crack lines.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

249. `*.Stone-Petrify-terra-single` — body petrifies solid as one stone statue; SINGLE_CHUNK=True, very low EXPLODE so it barely moves, medium-grey tint at high TINT_OPACITY_OUTER, TINT_ANIM=linear as petrification spreads, no dissolve
   - **Flag:** confined: sim ended after 1 tick(s); wide: sim ended after 1 tick(s)
250. `*.Stone-Shatter-terra-slab` — petrified form shatters into large slabs; low CHUNKS, low EXPLODE so heavy slabs don't fly far, light-grey tint, no dissolve so the slabs remain
251. `*.Stone-Shatter-terra-medium` — shatters into medium stone chunks; moderate CHUNKS, moderate EXPLODE, medium-grey tint, no dissolve
   - **Flag:** wide: only 14/16 distinct frames
252. `*.Stone-Crumble-terra-pebble` — crumbles into a scatter of small pebbles; high CHUNKS, high EXPLODE and SPREAD, light-grey tint, mild dissolve as the smallest pebble dust fades
253. `*.Stone-Sink-aqua` — petrified chunks sink slowly through water rather than dropping fast; GRAVITY_STRENGTH low and DRAG high so settling takes far longer than terra, medium-grey tint, no dissolve
254. `*.Stone-Crush-depth` — petrified form crushed inward under pressure; BLAST_MODE=implode, light-grey tint with TINT_COLLISION=inner_wins, no dissolve so the crushed rubble remains
   - **Flag:** confined: only 13/16 distinct frames; wide: only 14/16 distinct frames
255. `*.Stone-Drift-space` — zero-gravity petrified fragments drift apart; GRAVITY_STRENGTH=0, moderate CHUNKS, low EXPLODE, medium-grey tint, no dissolve
256. `*.Stone-Sunder-wave` — struck laterally, the petrified form shatters off in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, moderate CHUNKS, light-grey tint at high TINT_OPACITY_OUTER, no dissolve
257. `*.Stone-Fracture-inner` — petrification and fracture spread outward from a point within; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER medium-grey core, moderate CHUNKS, no dissolve
