# Spore — 7 presets (registry #419–425)

Module: `presets/spore.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Spores burst outward then drift slowly; lime/yellow.

**Gimmick lock** (kept): very high drag (0.30–0.34) → burst-then-drift; dissolve mostly off so spores linger.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 130–220, explode 0.25–2.4; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 2/7, mask 1/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 5a)

- Lock kept: drag 0.30–0.34 on every preset. The *drift* after the burst comes from a weak sustained force that the high drag turns into a slow terminal speed: gravity 0.07–0.12 to sift down (terra), 0.09 up (aqua), `noise` 0.03–0.04 (space, inner), 0.12 sideways (wave), a 0.09 centripetal pull after a 4-tick ramp (depth). Without it the spores just stop. Dissolve is on only for `-dense` (min 0.5) and aqua (min 0.25).
- Textured per *Textured materials*: 160–240 spores on most presets, so the colour is a deep body on the outer front plus jittered contrasting specks and grain 0.18–0.22. Palettes vary: lime (`Burst-terra`), mustard with olive specks (`-dense`), green-yellow (aqua, depth), pale yellow-green (space), ochre (wave).
- Several presets cap at `MAX_SIM_TICKS` on purpose (they drift forever). `Scatter-wave` ends mid-drift as a stretched cloud, not another wall pile. `Eruption-inner` is 40 big sacs ripening green → yellow (colour arc) and popping loose with `LAUNCH_STAGGER`, so it doesn't repeat `Drift-space`. `Drift-space` lost its `A Rounded (2)` mask (no shape rationale).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

419. `*.Spore-Burst-terra` — spores burst outward then drift slowly to rest; high CHUNKS, moderate EXPLODE with high DRAG so the initial burst quickly slows to a drift, lime-yellow tint at moderate TINT_OPACITY, no dissolve so the settled spores remain
420. `*.Spore-Burst-terra-dense` — dense spore cloud bursts and lingers; very high CHUNKS, moderate EXPLODE, high DRAG, lime-yellow tint, moderate dissolve as some spores fade
421. `*.Spore-Release-aqua` — spores burst then drift upward through water; GRAVITY_ANGLE=0 chunks rise after the initial burst, high CHUNKS, high DRAG, lime-yellow tint with TINT_ALPHA_BLEED_OUTER moderate, slow dissolve as they disperse while floating
422. `*.Spore-Collapse-depth` — spore cloud drawn inward and compacted; BLAST_MODE=implode, high CHUNKS, lime-yellow tint with TINT_COLLISION=inner_wins, no dissolve so the compacted spores remain
   - **Flag:** wide: only 14/16 distinct frames
423. `*.Spore-Drift-space` — zero-gravity spore burst, scattering then drifting weightlessly forever; GRAVITY_STRENGTH=0, high CHUNKS, moderate EXPLODE with high DRAG so motion settles into a slow drift, lime-yellow tint, no dissolve
424. `*.Spore-Scatter-wave` — struck laterally, spores burst off in that direction then drift; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, high CHUNKS, high DRAG, lime-yellow tint at high TINT_OPACITY_OUTER, no dissolve
425. `*.Spore-Eruption-inner` — spores burst outward from a point of release within, then drift; BLAST_MODE=burst, high CHUNKS with high DRAG, bidirectional lime-yellow tint with large TINT_DEPTH_INNER, no dissolve
