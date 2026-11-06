# Singularity — 6 presets (registry #73–78)

Module: `presets/singularity.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Intense gravity-well collapse; red/black.

**Gimmick lock** (kept): depth + space only; extreme black-red saturation (jitter/overlap 0.7–0.8, depth 0.7–0.9) with `pulse`/`early`/`late` throbbing; 60–90 chunks.

**Locales present:** depth ×3, space ×3.

**Why these locales:** depth and space only — a singularity has no ground or weather, only crushing inward or devouring drifting matter.

**Current state (2026-10-30):** chunks 65–90, explode 1.0–2.4; blast: implode 3, explode 3; gravity: centripetal 3, vortex 2, repulsor 1; tint on 6/6, dissolve 6/6, mask 1/6, stretched chunks 3/6.

**Stage 3 notes:**

- `Singularity-Event-Horizon-space` uses `LAUNCH_STAGGER`; since the fix, the sim runs until every chunk has launched — above ~0.15 the first launches squash into the opening frames. Check the sheet.

## Stage 3 result (2026-10-30)

- Pure `#FF0000`–`#FF0040` against black, jitter 0.8 on both fronts. `Annihilate` and `Devour` pulse, `Event-Horizon` builds `late`, the rest flood `early` with a red → darker-red/black arc.
- `Annihilate-depth` at centripetal 1.2 / drag 0.3 oscillated to `MAX_SIM_TICKS` (instant-clump look); 0.8 / 0.3 settles cleanly.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

73. `*.Singularity-Collapse-depth` — standard gravity-well collapse; blood-red bleeds into near-total-black core with extreme ragged overlap at the event horizon, chunks stretch radially and vanish as matter crosses the point of no return
74. `*.Singularity-Annihilate-depth` — pure maximum-force annihilation; extreme centripetal pull under saturated black-red pulse tint, intensity throbs as spacetime strains before all matter is crushed to a point
75. `*.Singularity-Tidal-Crush-depth` — tidal spaghettification under sustained inward pull; chunks stretch into long radial slivers with heavy orbital spin, deep red and near-black fronts overlap heavily into a warped crushed boundary
76. `*.Singularity-Vortex-space` — zero-gravity singularity pulling from all directions; chunks spiral inward through an extreme ragged black-red overlap boundary with heavy noise warping the front, vanishing at the horizon
77. `*.Singularity-Devour-space` — weightless matter drifts before the well violently claims it in a pulse of intensifying black-red tint; extreme jitter and deep front overlap give the boundary a hungry throbbing quality as chunks are devoured piecemeal
78. `*.Singularity-Event-Horizon-space` — slow orbital drain under zero gravity; chunks pulled in sequentially with heavy spin and staggered launch, black-red overlap builds gradually with extreme jitter before final annihilation
