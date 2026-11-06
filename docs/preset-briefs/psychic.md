# Psychic — 6 presets (registry #144–149)

Module: `presets/psychic.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Telekinetic crush / scatter / shove; purple used on the outer edge to show the mind's grip.

**Gimmick lock** (kept): mask-driven with the C-Shape (geometric polygon) family, 100–300 chunks so the polygon remainder reads against dense debris; purple outer tint only.

**Locales present:** terra ×2, aqua, depth, space, wave.

**Why these locales:** terra (×2), aqua, depth, space, wave.

**Current state (2026-10-30):** chunks 130–260, explode 0.3–2.6; blast: explode 4, implode 1, horizontal_split 1; gravity: directional 5, centripetal 1; tint on 6/6, dissolve 4/6, mask 6/6, stretched chunks 0/6.

**Stage 3 notes:**

- Psychic, Arcane, Holy and Heal all share the 'mask + 100–300 chunks' recipe, differing by mask family. On the sheets, make sure they also differ in motion and tint so the four types don't look interchangeable.

## Stage 3 result (2026-10-31)

- Tint is a hot violet → magenta silhouette glow (`TINT_MODE="edges"`, 0.6–2.0). At 130–250 chunks a chunk-mode rim covers every chunk, and edges mode is independent of chunk size.
- **Masks vs. walls:** a canvas-centred polygon erases anything that ends against a wall or on the floor of a roomy canvas. Presets that settle there (`Crush-terra`, `Shatter-terra-high`, `Shove-wave`) use `FRAME_MASK_ANIM="pulse"`: the grip holds the shape mid-animation, then releases and the pile is visible. Depth/space keep the mask on.
- `Shove-wave`: a right-pointing triangle (`ROTATE90`) never overlaps a bottom-anchored sprite, so it uses the upright triangle as a wedge.
- `Levitate-aqua` caps the sim (`MAX_SIM_TICKS` 80, gravity 0.05) so it hovers instead of rising off the canvas; the metric flag is intended.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

144. `*.Psychic-Crush-terra` — a telekinetic grip crushes then releases; dense chunk field with a clean C-Shape polygon mask revealing the exact geometric remainder the mind chose to leave intact, purple outer tint only, chunks scatter and settle downward
145. `*.Psychic-Shatter-terra-high` — violent psychic rupture; extreme chunk count and spin, a jagged near-circular C-Shape mask reveals the fractured mind-shard silhouette the release leaves behind, thick purple rim glow, fast dissolve at the edges
146. `*.Psychic-Levitate-aqua` — telekinetic lift; a dense field of tiny chunks rises as if levitated, a soft hexagonal C-Shape mask frames the hovering remainder with a faint purple glow while barely dissolving
147. `*.Psychic-Crush-depth` — pure telekinetic crush with no release; centripetal compression under a heptagonal C-Shape mask that tightens the visible remainder inward, clean purple pressure boundary, moderate dissolve
148. `*.Psychic-Toss-space` — telekinetic toss in zero gravity; a dense chunk field tumbles freely, a near-circular C-Shape mask frames a stable remainder shape while the rest drifts, faint purple glow, no settle
149. `*.Psychic-Shove-wave` — telekinetic shove throws the sprite sideways with force; a dense chunk field impacts under a triangular C-Shape mask pointed in the direction of the shove, purple tint marks the impact, trailing fragments dissolve last
