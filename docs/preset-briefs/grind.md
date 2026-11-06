# Grind — 7 presets (registry #309–315)

Module: `presets/grind.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Break into rough smaller pieces, tumbling debris.

**Gimmick lock** (new): **Tumble**: high spin with no spin drag in flight (floor friction stops it on landing), `CHUNK_MASS_VARIANCE`, rough debris; no tint, no dissolve.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 50–100, explode 0.2–2.8; blast: explode 5, implode 1, horizontal_split 1; gravity: directional 6, centripetal 1; tint on 0/7, dissolve 0/7, mask 1/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 4a)

- Lock kept: spin 14–35 with `SPIN_DRAG=0` on every preset, `CHUNK_MASS_VARIANCE` 0.6–1.0, `TINT_GRAIN` 0.15–0.2 for grit (the only colour change; it keeps Grind rougher than the clean, grain-free Break), no tint, no dissolve. Chunks 22–60, so the tumbling pieces stay big enough for the spin to show.
- Locales: `Tumble-terra` 60 gritty lumps, `-coarse` 22 cartwheeling lumps with bounce 0.25; `Float-aqua` rises at uneven rates; `Collapse-depth` is a `vortex` "millstone" (lumps swirl in while tumbling); `Drift-space` uses `LAUNCH_STAGGER` 0.12 so spinning lumps break off one after another; `Sunder-wave` tumbles rubble right against the wall; `Erupt-inner` barely separates and keeps turning in place (spin keeps the sim alive until `MAX_SIM_TICKS`).
- Tried and dropped: `orbital` for space (even at strength 0.1 it threw half the confined pieces off-canvas) and diagonal gravity for wave (every chunk ends in the same corner and they overlap into one small lump, since chunks don't collide).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

309. `*.Grind-Tumble-terra` — ground into rough tumbling debris, no tint; moderate-high CHUNKS, moderate EXPLODE, high SPIN and SPIN_DRAG low so pieces tumble visibly as they fall, no dissolve
   - **Flag:** wide: only 14/16 distinct frames
310. `*.Grind-Tumble-terra-coarse` — coarser grinding, fewer larger rough chunks; moderate CHUNKS, moderate EXPLODE, high SPIN, no dissolve
311. `*.Grind-Float-aqua` — ground debris rises and tumbles upward in water; GRAVITY_ANGLE=0 chunks rise, moderate CHUNKS, high SPIN, no dissolve
312. `*.Grind-Collapse-depth` — debris ground down and collapsed inward; BLAST_MODE=implode, moderate CHUNKS, high SPIN, no dissolve so the rough rubble remains
   - **Flag:** wide: only 14/16 distinct frames
313. `*.Grind-Drift-space` — zero-gravity tumbling debris scatters in all directions; GRAVITY_STRENGTH=0, moderate CHUNKS, high SPIN, no dissolve
314. `*.Grind-Sunder-wave` — struck laterally, the form grinds apart in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, moderate CHUNKS, high SPIN, no dissolve
315. `*.Grind-Erupt-inner` — grinding force originates from within and tumbles outward; BLAST_MODE=burst, high CHUNKS and SPIN, no dissolve
