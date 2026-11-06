# Slash — 13 presets (registry #103–115)

Module: `presets/slash.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Slashes that leave thin slivers across the cut, with a wound channel; mechanical and elemental.

**Gimmick lock** (new): **Slivers across the cut**: very high `CHUNK_SHAPE_STRETCH` (6+) perpendicular to the cut line, split `BLAST_MODE` with matching bias. More, thinner pieces than Blade.

**Locales present:** terra ×8, aqua, depth, space, wave, inner.

**Why these locales:** terra (×8), aqua, depth (wound closing), space, wave, inner (stress fracture).

**Current state (2026-10-30):** chunks 2–7, explode 0.18–2.8; blast: horizontal_split 9, vertical_split 2, implode 1, explode 1; gravity: directional 12, centripetal 1; tint on 5/13, dissolve 4/13, mask 1/13, stretched chunks 13/13.

**Stage 3 notes:**

- **Cut convention (decided in Stage 2):** `-H` = horizontal cut line, top and bottom halves part → `BLAST_MODE="vertical_split"` + `CHUNK_BIAS="halves-h"`. `-V` = vertical cut line, left and right halves part → `BLAST_MODE="horizontal_split"` + `CHUNK_BIAS="halves-v"`. Every current preset in this type pairs them crosswise (seeds split one way, pieces fly the other), so the clean two-halves read never happens — fix the pairing first, then tune. For slivers *across* the cut: a horizontal cut (`-H`) wants vertical slivers (`CHUNK_SHAPE_ANGLE=0`), a vertical cut (`-V`) wants horizontal strips (`90`).
- `Slash-H-terra` ends after 1 tick with only 12/16 distinct frames.

## Stage 3 result (2026-10-31)

- Axes fixed per the cut convention: `-H` = `vertical_split` + `halves-h` with vertical slivers (`CHUNK_SHAPE_ANGLE=0`), `-V` = `horizontal_split` + `halves-v` with horizontal strips (`90`); stretch 6.5–9 on every split preset, 12–26 slivers (more and thinner than Blade).
- Mechanical cuts are untinted on purpose (`H-terra`, `V-terra`, `H-space`); the `-deep` variants carry a ragged crimson wound (outer 0.03, jitter 0.5), which at ~20 slivers floods most of each sliver red — accepted, they read as bloody heaps. Elementals: Fire (yellow→orange→char arc), Cryo (white frost rim, deep-blue body, `BOUNCE` 0.3), Electric (cyan body, 1 px yellow spark cores, `inner_wins`), Acid (deep edges lime with noise).
- `Slash-Fast-wave` uses `shatter` + gravity 90° (not a split) so every sliver goes right; on the canvas-filling bear they stack into a column against the right wall, which the white directional fade turns into a speed streak.
- `Slash-Stress-inner` uses `shatter` at 0.2 with 14 diagonal slivers (fewer chunks so the 1 px crack line doesn't cover whole slivers); `Slash-Wound-depth` uses `explode` + centripetal (overdamped 0.8/0.24) instead of implode.
- Metric flags left: `H-terra` / `H-terra-deep` show 13–14/16 distinct frames on `confined_32`. The canvas-filling bear's top half is clamped by the top wall, so the opening frames barely move (the same boxed-in limit as Blade).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

103. `*.Slash-H-terra` — horizontal slash; BLAST_MODE=horizontal_split, CHUNK_SHAPE_STRETCH very high (CHUNK_SHAPE_ANGLE=0 vertical slivers across horizontal cut), CHUNK_BIAS=halves-h, low EXPLODE so slivers separate cleanly, low SPIN, no tint, slivers settle downward
   - **Fix:** Horizontal cut → `vertical_split` + `halves-h`, slivers `CHUNK_SHAPE_ANGLE=0`. Currently 1 tick, 12/16 distinct frames.
   - **Flag:** confined: only 12/16 distinct frames; sim ended after 1 tick(s)
104. `*.Slash-H-terra-deep` — deep horizontal slash; same as Slash-H but higher EXPLODE so slivers scatter more forcefully, more CHUNKS for finer slivering, low SPIN maintained for clean cut aesthetic
   - **Fix:** Same axis fix as `Slash-H-terra`.
   - **Flag:** wide: only 14/16 distinct frames
105. `*.Slash-V-terra` — vertical slash; BLAST_MODE=vertical_split, CHUNK_SHAPE_STRETCH very high (CHUNK_SHAPE_ANGLE=90 horizontal strips across vertical cut), CHUNK_BIAS=halves-v, low EXPLODE, low SPIN, no tint, strips settle downward
   - **Fix:** Vertical cut → `horizontal_split` + `halves-v`, strips `CHUNK_SHAPE_ANGLE=90`.
   - **Flag:** wide: sim ended after 3 tick(s)
106. `*.Slash-V-terra-deep` — deep vertical slash; same as Slash-V but higher EXPLODE and more CHUNKS for finer slivering and more scatter
   - **Fix:** Same axis fix as `Slash-V-terra`.
107. `*.Slash-H-aqua` — horizontal slash in buoyant medium; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=0 so slivers drift upward and apart, CHUNK_SHAPE_STRETCH very high vertical slivers, low EXPLODE, no tint
   - **Fix:** Horizontal-cut axis fix.
108. `*.Slash-Wound-depth` — slash wound compressed inward under pressure; BLAST_MODE=implode, CHUNK_SHAPE_STRETCH high (CHUNK_SHAPE_ANGLE=90) so slivers collapse inward, TINT_MODE=edges moderate tint on wound surface, slivers converge and dissolve as wound closes
109. `*.Slash-H-space` — horizontal slash in zero gravity; GRAVITY_STRENGTH=0, BLAST_MODE=horizontal_split, CHUNK_SHAPE_STRETCH very high vertical slivers, very low EXPLODE so slivers drift apart slowly in opposite directions, low SPIN, no tint
   - **Fix:** Horizontal-cut axis fix.
110. `*.Slash-Fast-wave` — high-speed lateral slash swing; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, CHUNK_SHAPE_STRETCH very high (CHUNK_SHAPE_ANGLE=0 vertical slivers), moderate-high EXPLODE for fast swing momentum, low SPIN, no tint
   - **Fix:** Axis fix; keep the gravity-90° sweep.
111. `*.Slash-Stress-inner` — internal stress fracture radiating slash lines from core; BLAST_MODE=burst, CHUNK_SHAPE_STRETCH high (CHUNK_SHAPE_ANGLE=45 diagonal slivers along stress lines), low EXPLODE so slivers radiate minimally from center, no tint
   - **Fix:** `burst` + tiny force reads as jitter; radiating stress lines want `explode` at tiny force (centre pieces barely move) or `shatter` + tint.
   - **Flag:** wide: only 14/16 distinct frames
112. `*.Slash-Fire-H-terra` — fire-imbued horizontal slash; BLAST_MODE=horizontal_split, CHUNK_SHAPE_STRETCH very high vertical slivers, orange outer to yellow inner bidirectional tint concentrated on wound edges, TINT_MODE=edges, moderate dissolve as wound burns
   - **Fix:** Horizontal-cut axis fix.
113. `*.Slash-Cryo-H-terra` — ice-imbued horizontal slash; BLAST_MODE=horizontal_split, CHUNK_SHAPE_STRETCH very high vertical slivers, icy-white outer to deep-blue inner bidirectional tint, no dissolve for clean frozen-cut look, very low SPIN
   - **Fix:** Horizontal-cut axis fix.
114. `*.Slash-Electric-H-terra` — electric-imbued horizontal slash; BLAST_MODE=horizontal_split, CHUNK_SHAPE_STRETCH high but CHUNK_SHAPE_ANGLE=45 for jagged diagonal electric slivers, cyan outer to yellow inner tint, fast dissolve DISSOLVE_CHUNK_STAGGER for staggered spark fade
   - **Fix:** Horizontal-cut axis fix.
115. `*.Slash-Acid-H-terra` — acid-imbued horizontal slash; BLAST_MODE=horizontal_split, CHUNK_SHAPE_STRETCH very high vertical slivers, TINT_MODE=edges lime-green eating inward from wound surface, TINT_NOISE moderate, moderate dissolve as wound is corroded
   - **Fix:** Horizontal-cut axis fix.
