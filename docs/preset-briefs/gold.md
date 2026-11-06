# Gold — 8 presets (registry #258–265)

Module: `presets/gold.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Midas touch: turn to solid gold, or crumble into gold dust.

**Gimmick lock** (revised in Stage 3): **Midas gleam**: a deep-gold → bright-gold colour arc on every preset, positive `TINT_SATURATION_SHIFT`, bright glints (pale core specks or catch-light rims + grain); heavy, bounce-free Stone-like physics. (Was: a `linear`/`late` gold flood; see *Stage 3 result*.)

**Locales present:** terra ×3, aqua, depth, space, wave, inner.

**Why these locales:** All six; aqua sinks.

**Current state (2026-10-30):** chunks 1–140, explode 0.15–2.2; blast: explode 5, implode 1, horizontal_split 1, burst 1; gravity: directional 7, centripetal 1; tint on 8/8, dissolve 1/8, mask 0/8, stretched chunks 0/8.

**Stage 3 notes:**

- `Gold-Midas-terra-single` is a 1-tick single chunk by design.

## Stage 3 result (2026-10-31, session 3b)

- **Lock revised:** a `linear`/`late` flood spends half the animation in sprite-plus-gold mud, and plain yellow reads as mustard. New lock: **Midas gleam**: every preset has a colour arc from a deeper gold (`#C08010`–`#D89410`) up to bright gleaming gold (`#FFC81E`–`#FFD43C`), `TINT_SATURATION_SHIFT` +0.2–0.3, and glints from pale-gold core specks (`#FFF4B8`) or polished catch-light rims, plus `TINT_GRAIN` 0.18–0.3. Physics is heavy and dead: no bounce, high gravity. The progressive flood stays only where the brief is a transformation: `Midas-terra-single` (`linear`; gold over the sprite lerps cleanly) and `Spread-inner` (`per_chunk`, gilding piece by piece).
- Kept apart from Stone (no colour arc, mottled grey) by the arc and glints, and from Crystal by opacity and grain. `Crumble-terra-dust` is the only dissolve: 170 grains with a bright `#FFE600` sparkle as each winks out. `Sink-aqua` sinks straight down in formation (spread 0.4, spin 0.4, low mass variance), unlike Stone's tumbling, staggered sink. `Drift-space` uses bright rims (`#FFF0A0` on a 1 px outer front) and spins without spin drag.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

258. `*.Gold-Midas-terra-single` — Midas touch turns the body solid gold; SINGLE_CHUNK=True, very low EXPLODE, yellow-gold tint at high TINT_OPACITY_OUTER, TINT_ANIM=linear as the gold spreads across the form, no dissolve
   - **Flag:** confined: sim ended after 1 tick(s); wide: sim ended after 1 tick(s)
259. `*.Gold-Crumble-terra-dust` — gilded form crumbles into gold dust; high CHUNKS, moderate EXPLODE, yellow-gold tint, moderate dissolve (DISSOLVE_CURVE close to 1) as the dust scatters and fades
260. `*.Gold-Shatter-terra` — gilded form shatters into solid gold fragments; moderate CHUNKS, moderate EXPLODE, yellow-gold tint at high TINT_OPACITY, no dissolve so the gold fragments remain
   - **Flag:** wide: only 13/16 distinct frames
261. `*.Gold-Sink-aqua` — gilded chunks sink slowly through water, heavy and gleaming; low GRAVITY_STRENGTH and high DRAG so settling takes far longer than terra, yellow-gold tint, no dissolve
262. `*.Gold-Collapse-depth` — gilded form crushed inward under pressure; BLAST_MODE=implode, yellow-gold tint with TINT_COLLISION=inner_wins, no dissolve so the compacted gold remains
263. `*.Gold-Drift-space` — zero-gravity gilded fragments drift apart, gleaming; GRAVITY_STRENGTH=0, moderate CHUNKS, low EXPLODE, yellow-gold tint, no dissolve
264. `*.Gold-Sunder-wave` — struck laterally, the gilded form shatters off in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, moderate CHUNKS, yellow-gold tint at high TINT_OPACITY_OUTER, no dissolve
265. `*.Gold-Spread-inner` — the Midas transformation spreads outward from a point of contact within; BLAST_MODE=burst with low EXPLODE, bidirectional tint with large TINT_DEPTH_INNER yellow-gold core, no dissolve
