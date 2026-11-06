# Shred — 7 presets (registry #316–322)

Module: `presets/shred.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Splinter strips oriented along the cut axis, peeling laterally.

**Gimmick lock** (new): **Strips along the cut**: `CHUNK_SHAPE_STRETCH` ≥ 4 on every preset, high drag so strips flutter; no tint, no dissolve. Opposite of Laser (strips perpendicular to the cut).

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 35–60, explode 0.2–2.8; blast: explode 5, implode 1, horizontal_split 1; gravity: directional 6, centripetal 1; tint on 0/7, dissolve 0/7, mask 1/7, stretched chunks 7/7.

## Stage 3 result (2026-10-31, session 4a)

- Lock kept: stretch 5–8 on every preset, drag 0.22–0.32 (except space), no tint, no dissolve, no grain. Strip angle varies with the locale: upright strips that flutter down (`Strip-terra` 40, `-fine` 110 hair-thin slivers), horizontal ribbons rising in water (`Float-aqua`), diagonal strips balled into a tangle (`Collapse-depth`, centripetal), long 30° splinters drifting with decaying spin (`Drift-space`).
- `Peel-wave` peels: `shatter` + `LAUNCH_STAGGER` 0.12 so horizontal ribbons leave one at a time and flutter right. `Burst-inner` uses `horizontal_split` at force 0.9 with zero gravity, so upright slats fan open to both sides like a shredded page.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

316. `*.Shred-Strip-terra` — torn into splinter strips along the cut axis, no tint; moderate-high CHUNKS, moderate EXPLODE, CHUNK_SHAPE_STRETCH high with CHUNK_SHAPE_ANGLE=0 for vertical splinter strips, high DRAG so strips flutter as they fall, no dissolve
   - **Flag:** wide: only 14/16 distinct frames
317. `*.Shred-Strip-terra-fine` — finely shredded into thin slivers; very high CHUNKS, CHUNK_SHAPE_STRETCH very high, high DRAG, no dissolve
   - **Flag:** confined: only 14/16 distinct frames
318. `*.Shred-Float-aqua` — shredded strips drift upward and flutter in water; GRAVITY_ANGLE=0 chunks rise, CHUNK_SHAPE_STRETCH high, high DRAG, no dissolve
319. `*.Shred-Collapse-depth` — strips torn and drawn inward; BLAST_MODE=implode, CHUNK_SHAPE_STRETCH high, no dissolve so the shredded strips remain piled
320. `*.Shred-Drift-space` — zero-gravity shredded strips tumble apart; GRAVITY_STRENGTH=0, CHUNK_SHAPE_STRETCH high, moderate EXPLODE, no dissolve
321. `*.Shred-Peel-wave` — struck laterally, strips peel off sideways in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, CHUNK_SHAPE_STRETCH high with CHUNK_SHAPE_ANGLE=90 so strips peel laterally along the strike, no dissolve
322. `*.Shred-Burst-inner` — shredding force originates from within, strips peeling outward; BLAST_MODE=burst, CHUNK_SHAPE_STRETCH high, high CHUNKS, no dissolve
