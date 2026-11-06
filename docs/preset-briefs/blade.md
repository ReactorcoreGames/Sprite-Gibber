# Blade — 12 presets (registry #79–90)

Module: `presets/blade.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Sword and axe cleaves that split the object, mechanical and elemental-imbued.

**Gimmick lock** (new): **The cut is the event**: split `BLAST_MODE` with the matching `CHUNK_BIAS` axis, very few chunks (2–8), clean halves that part and settle. Sword = clean (2–4 chunks, low spin); axe (`-dull`) = rougher (more chunks, mass variance). Mechanical variants carry a 1 px crimson wound line (`TINT_DEPTH_OUTER` 0.04, 0.06 on `-dull`, `TINT_ANIM="early"` so the slash appears); elemental variants put their element on the halves' edges.

**Locales present:** terra ×9, aqua, space, wave.

**Why these locales:** No depth or inner — a blade is an external cut; terra carries the sword/axe and elemental variants.

**Current state (2026-10-30):** chunks 2–6, explode 0.6–2.0; blast: vertical_split 8, horizontal_split 3, x_split 1; gravity: directional 12; tint on 4/12, dissolve 3/12, mask 0/12, stretched chunks 12/12.

**Stage 3 notes:**

- **Cut convention (decided in Stage 2):** `-H` = horizontal cut line, top and bottom halves part → `BLAST_MODE="vertical_split"` + `CHUNK_BIAS="halves-h"`. `-V` = vertical cut line, left and right halves part → `BLAST_MODE="horizontal_split"` + `CHUNK_BIAS="halves-v"`. Every current preset in this type pairs them crosswise (seeds split one way, pieces fly the other), so the clean two-halves read never happens — fix the pairing first, then tune.
- Stretch parallel to the cut line (vertical cut → `CHUNK_SHAPE_ANGLE=0`, horizontal cut → `90`) so the few Voronoi cells come out as clean halves; the idea briefs below give the angles backwards for Blade.
- Several presets end after 1–2 ticks (`Cleave-H-terra`, `Cleave-aqua`) — halves need enough velocity/gravity travel to read as parting.

## Stage 3 result (2026-10-30)

- Axes fixed per the cut convention: `-V` = `horizontal_split` + `halves-v` + stretch angle 0; `-H` = `vertical_split` + `halves-h` + angle 90; `Slash` = `x_split` + `quadrants`; `Cleave-aqua` is a V cut, `Cleave-space` and `Cleave-wave` are H cuts.
- **"Tint along the cut only" can't be built:** chunk-mode border tint also covers the silhouette, so the wound line outlines each half as well as the cut. Accepted, since it reads as a fresh wound.
- **Engine limit:** a canvas-filling sprite (`confined_32`) is boxed in on all four sides, so a 2-piece vertical cut can't move at all (V, wave and Cryo flag a 1-tick sim there). The wound line fading in is what makes the cut read on such sprites; on any sprite with room the halves part as intended.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

79. `*.Blade-Cleave-V-terra` — vertical sword cleave; BLAST_MODE=vertical_split, CHUNK_BIAS=halves-v, CHUNK_SHAPE_STRETCH high (CHUNK_SHAPE_ANGLE=90 horizontal slivers along the cut), low EXPLODE so halves fall apart cleanly, low SPIN, no tint, chunks settle downward
   - **Fix:** Vertical cut → `horizontal_split` + `halves-v`.
80. `*.Blade-Cleave-V-terra-dull` — axe vertical hack; same as Cleave-V but more CHUNKS, higher SPIN, CHUNK_MASS_VARIANCE for uneven fragments, slightly higher EXPLODE for rougher scatter
   - **Fix:** Vertical cut → `horizontal_split` + `halves-v`.
81. `*.Blade-Cleave-H-terra` — horizontal sword cleave; BLAST_MODE=horizontal_split, CHUNK_BIAS=halves-h, CHUNK_SHAPE_STRETCH high (CHUNK_SHAPE_ANGLE=0 vertical slivers along horizontal cut), low EXPLODE, low SPIN, no tint, top half rises slightly then settles
   - **Fix:** Horizontal cut → `vertical_split` + `halves-h`. Currently ends after 2 ticks.
   - **Flag:** confined: sim ended after 2 tick(s)
82. `*.Blade-Cleave-H-terra-dull` — axe horizontal hack; same as Cleave-H but more CHUNKS, higher SPIN, CHUNK_MASS_VARIANCE, rougher scatter
   - **Fix:** Horizontal cut → `vertical_split` + `halves-h`.
83. `*.Blade-Slash-terra` — diagonal slash approximated with x_split; BLAST_MODE=x_split, CHUNK_SHAPE_STRETCH moderate at 45° diagonal, low EXPLODE, low SPIN, no tint, clean quadrant separation
   - **Fix:** `x_split` pairs with `CHUNK_BIAS="quadrants"`.
84. `*.Blade-Cleave-aqua` — sword cleave in buoyant medium; BLAST_MODE=vertical_split, GRAVITY_ANGLE=0 so cut halves drift upward and apart, CHUNK_SHAPE_STRETCH high horizontal slivers, low EXPLODE, no tint
   - **Fix:** The name has no axis — pick one and pair blast + bias accordingly. Currently 1 tick, 13/16 distinct frames.
   - **Flag:** confined: only 13/16 distinct frames; sim ended after 1 tick(s)
85. `*.Blade-Cleave-space` — sword cleave in zero gravity; GRAVITY_STRENGTH=0, BLAST_MODE=vertical_split, halves drift slowly apart in opposite directions, CHUNK_SHAPE_STRETCH high, very low EXPLODE, low SPIN, no tint
   - **Fix:** Same axis fix; zero-g halves should drift apart for the whole animation.
   - **Flag:** confined: only 14/16 distinct frames
86. `*.Blade-Cleave-wave` — high-speed lateral blade sweep; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 sweeps halves rightward, CHUNK_SHAPE_STRETCH high (CHUNK_SHAPE_ANGLE=0 vertical slivers perpendicular to sweep motion), moderate EXPLODE, no tint
   - **Fix:** A lateral sweep — consider a horizontal cut (`vertical_split` + `halves-h`) with gravity 90° carrying both halves right.
87. `*.Blade-Fire-Cleave-terra` — fire-imbued sword cleave; BLAST_MODE=vertical_split, CHUNK_SHAPE_STRETCH high horizontal slivers, orange outer to yellow inner bidirectional tint along cut edges, moderate dissolve as fire burns the wound, low SPIN
   - **Fix:** Axis fix (vertical cut).
88. `*.Blade-Cryo-Cleave-terra` — ice-imbued sword cleave; BLAST_MODE=vertical_split, CHUNK_SHAPE_STRETCH high, icy-white outer to deep-blue inner bidirectional tint, no dissolve (frozen clean cut), very low SPIN for rigid shard behavior
   - **Fix:** Axis fix (vertical cut).
89. `*.Blade-Electric-Cleave-terra` — electric-imbued sword cleave; BLAST_MODE=vertical_split, CHUNK_SHAPE_STRETCH high but with CHUNK_SHAPE_ANGLE=45 for jagged diagonal slivers, cyan outer to yellow inner bidirectional tint, fast dissolve with DISSOLVE_CHUNK_STAGGER for staggered spark fade
   - **Fix:** Axis fix (vertical cut).
90. `*.Blade-Acid-Cleave-terra` — acid-imbued sword cleave; BLAST_MODE=vertical_split, CHUNK_SHAPE_STRETCH moderate, TINT_MODE=edges lime-green tint eating from cut surface inward, TINT_NOISE moderate for irregular corrosion, moderate dissolve as wound is consumed
   - **Fix:** Axis fix (vertical cut).
