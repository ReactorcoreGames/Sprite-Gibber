# Laser — 7 presets (registry #323–329)

Module: `presets/laser.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Clean laser cuts into strips perpendicular to the cut axis (terra: cut axis vertical, strips horizontal); red.

**Gimmick lock** (kept): extreme `CHUNK_SHAPE_STRETCH` strips on every preset, `DISSOLVE` off throughout — a clean physical cut, visual interest from chunk shape + tint.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 45–130, explode 0.2–3.5; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 0/7, mask 0/7, stretched chunks 7/7.

## Stage 3 result (2026-10-31, session 4a)

- Lock kept (extreme stretch 6–16, no dissolve); colour follows *Vivid colour*: opacity 1.0, no jitter, ~1 px cut-line fronts (`TINT_DEPTH_OUTER` 0.03–0.06), saturated reds/oranges, `instant`, with colour arcs carrying the change (yellow-hot → red cooling on `Slice-terra`, `Beam-wave`, `Burst-inner`; red → yellow-white heating on `Collapse-depth`; orange → hot pink quench on `Float-aqua`).
- **Finding:** an extremely stretched strip is only ~2 px thick at 12+ chunks, so every pixel is a border pixel and a "thin cut line" paints the whole strip (the old library's solid red blob). For sprite-coloured slabs with glowing cut lines use 6–8 chunks (`Slice-terra` 6, `Burst-inner` 8). The fully coloured strip presets (`-fine` 50 scarlet slivers, `Drift-space` 30 crimson splints, `Collapse-depth` bars) are deliberate contrast.
- Brief's alpha-bleed glow for `Float-aqua` cut to 0.1 (bleed greys colour over the background). `Burst-inner` dropped `per_chunk`, which spent most frames as a pale pink mix.

- **Final pass (2026-10-31):** `Collapse-depth` clumped by frame 3–5 of 15 and then sat as a static lump for the rest of the GIF (no dissolve to carry it). `EXPLODE` 1.6 → 0.6 and centripetal 0.6 → 0.25 (drag 0.32), so the bars squeeze together into one hot column over the whole animation. Sheet: `shots/stage3-final/depthfix/`.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

323. `*.Laser-Slice-terra` — laser cuts vertically, thin horizontal strips fall and settle; high CHUNKS, CHUNK_SHAPE_STRETCH extreme with CHUNK_SHAPE_ANGLE=90, red tint glowing at the cut edges, no dissolve
324. `*.Laser-Slice-terra-fine` — surgical precision slicing, many razor-thin strips; very high CHUNKS, CHUNK_SHAPE_STRETCH at max, tint depth shallow and sharp so only the cut edge glows, no dissolve
325. `*.Laser-Float-aqua` — laser-sliced strips drift upward through water, tumbling gently as they rise; GRAVITY_ANGLE=0, CHUNK_SHAPE_STRETCH extreme with CHUNK_SHAPE_ANGLE=90, red tint softened by higher alpha bleed for a diffused underwater glow, no dissolve
326. `*.Laser-Collapse-depth` — laser-cut strips are drawn inward by a compressive field and stack into a compact core; GRAVITY_MODE=centripetal, BLAST_MODE=implode, CHUNK_SHAPE_STRETCH extreme, bidirectional red-to-white tint with inner_wins collision at the glowing core, no dissolve
327. `*.Laser-Drift-space` — zero-gravity, cut strips tumble apart slowly in all directions, spin decaying to a slow drift; GRAVITY_STRENGTH=0, CHUNK_SHAPE_STRETCH extreme with CHUNK_SHAPE_ANGLE=90, red tint, no dissolve
328. `*.Laser-Beam-wave` — struck by a lateral sweeping beam, sliced apart and blasted sideways; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, CHUNK_SHAPE_STRETCH extreme with CHUNK_SHAPE_ANGLE=0 so strips run perpendicular to the lateral cut, red tint at high opacity along the beam path, no dissolve
329. `*.Laser-Burst-inner` — cuts radiate outward from a single ignition point within the sprite, chunks barely separating; BLAST_MODE=burst, EXPLODE tiny, GRAVITY_STRENGTH=0, CHUNK_SHAPE_STRETCH extreme, bidirectional tint with a bright white-red inner core (inner_wins) radiating to a red rim, no dissolve
