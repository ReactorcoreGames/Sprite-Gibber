# Matrix — 8 presets (registry #397–404)

Module: `presets/matrix.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Data-particle dissolve sweeping in a direction; green; Matrix-inspired (down, up, right — left is a mirror in-game).

**Gimmick lock** (kept): green digital-rain tint; each locale has a different dissolve mechanic (terra/aqua directional cascade, depth centripetal compile, space noise static, wave scan-line stream, inner centrifugal decode).

**Locales present:** terra ×3, aqua, depth, space, wave, inner.

**Why these locales:** All six, kept by explicit request after a redesign.

**Current state (2026-10-30):** chunks 80–100, explode 0.15–3.0; blast: explode 5, implode 1, horizontal_split 1, burst 1; gravity: directional 7, centripetal 1; tint on 8/8, dissolve 8/8, mask 0/8, stretched chunks 1/8.

## Stage 3 result (2026-10-31, session 4b)

- Lock kept: green digital rain with one dissolve mechanic per locale. Vivid: a deep full-opacity `#00E040` body with jittered pale `#B0FFB8` glint specks (`blend` 0.12), `instant`, and a dark-green `#005A14` "trail" fade at 0.9, so code dims before it vanishes. The rain presets use vertical code slivers (`CHUNK_SHAPE_STRETCH` 4, angle 0).
- Mechanics: `-down` falling slivers erased from the top (`DISSOLVE_DIRECTION=0`); `-up` a wipe climbing from the floor (180); `-right` a left-to-right column wipe (270); aqua strands peel off (`LAUNCH_STAGGER`) and rise with their trailing ends erased first (180); `Compile-depth` an overdamped centripetal knot brightening to a white-green byte (arc curve 0.5, so the green holds) while whole packets blink out (`chunks`, stagger 0.6); `Static-space` 120 green pixels flickering out at `random` with a lime flash; `Stream-wave` horizontal scan lines (stretch 7, angle 90) carried right with the leading packets first (90); `Decode-inner` a grid of 1 px green code points inside the sprite-coloured pieces (zero-opacity outer front + `inner_wins`), each piece eroding from its rim (`centrifugal` works at 40 pieces) until only the code points remain.
- **Fixes applied:** `DISSOLVE_DIRECTION` names the side that goes first, so the brief's directions were reversed: falling code wipes from the top (0, not 180) and the upward wipe starts at the floor (180, not 0). `Stream-wave` uses `CHUNK_SHAPE_ANGLE=90` for horizontal strips (0 is vertical slivers) and direction 90 (leading packets first). `Compile-depth` uses `chunks`, not per-chunk `centripetal` speckle. `Decode-inner` uses `explode` at 0.12, not `burst`.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

397. `*.Matrix-Cascade-terra-down` — data-particle dissolve cascading downward like falling code; low EXPLODE and SPIN, green tint at high TINT_OPACITY_OUTER, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=180
398. `*.Matrix-Cascade-terra-up` — data-particle dissolve cascading upward; low EXPLODE and SPIN, green tint, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=0
399. `*.Matrix-Cascade-terra-right` — data-particle dissolve cascading sideways; low EXPLODE and SPIN, green tint, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=90
400. `*.Matrix-Drift-aqua` — green data-particles rise and dissolve away like reversed rain; GRAVITY_ANGLE=0 chunks rise, green tint with TINT_ALPHA_BLEED_OUTER moderate, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=0 cascading upward as it ascends
401. `*.Matrix-Compile-depth` — the data structure doesn't cascade, it compresses into a single glowing byte before vanishing entirely; BLAST_MODE=implode, GRAVITY_MODE=centripetal, green tint with TINT_COLLISION=inner_wins and a bright white-green inner core, DISSOLVE_PATTERN=centripetal so the erasure tracks the compaction rather than a falling sweep
402. `*.Matrix-Static-space` — zero-gravity signal loss; no directional cascade at all, fragments hang and flicker out at random like a broadcast losing lock, GRAVITY_STRENGTH=0, low EXPLODE, green tint, DISSOLVE_PATTERN=noise with high DISSOLVE_CHUNK_STAGGER for scattered per-fragment flicker
403. `*.Matrix-Stream-wave` — struck laterally, raw packet data visibly streams across the strike direction as a scan-line burst rather than falling code; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, CHUNK_SHAPE_STRETCH high with CHUNK_SHAPE_ANGLE=0 for horizontal streaking strips, green tint at high TINT_OPACITY_OUTER, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 sweeping opposite the strike like scrolling packet data
404. `*.Matrix-Decode-inner` — data-particle dissolve radiates outward from a point of origin within, like a decode routine unpacking from a seed; BLAST_MODE=burst with low EXPLODE, bidirectional green tint with large TINT_DEPTH_INNER, DISSOLVE_PATTERN=centrifugal as the form dissolves outward from center
