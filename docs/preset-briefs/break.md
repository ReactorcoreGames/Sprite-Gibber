# Break — 8 presets (registry #294–301)

Module: `presets/break_.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Plain shatter, no tint — the neutral reference type.

**Gimmick lock** (new): **Neutral shatter**: no tint (`TINT_DEPTH_OUTER=0`), no dissolve, plain round Voronoi chunks (no stretch, no bias). Everything else in the library is a departure from this.

**Locales present:** terra ×3, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 7–50, explode 0.2–5.0; blast: explode 6, implode 1, horizontal_split 1; gravity: directional 7, centripetal 1; tint on 0/8, dissolve 0/8, mask 1/8, stretched chunks 0/8.

## Stage 3 result (2026-10-31, session 3b)

- Lock kept: no tint, no dissolve, round unbiased Voronoi, no grain (it stays the neutral reference). Variety comes from the parameter space: chunks 5 (`-light`, slumps in place) / 14 / 20 / 24 / 26 / 30 / 40 / 80 (`-heavy`, spin 18), bounce 0.1–0.4, mass variance 0–1.0.
- `Collapse-depth` stays centripetal but with only 14 chunks and no dissolve, which keeps it apart from Crush (high counts + dissolve). `Sunder-wave` is an `explode` with drag 0.2 and mass variance 1.0 so the pieces string out as 90° gravity carries them (a low-force shatter slid the sprite across intact). `Burst-inner` uses a gentle `explode` (0.7) rather than `burst`, so cracks open from the middle.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

294. `*.Break-Shatter-terra` — plain mechanical shatter, no tint; moderate-high CHUNKS, high EXPLODE and SPIN, no dissolve so fragments remain scattered
   - **Flag:** confined: only 14/16 distinct frames; wide: only 12/16 distinct frames
295. `*.Break-Shatter-terra-light` — light fracturing, just a few pieces; low CHUNKS, low EXPLODE, no dissolve
296. `*.Break-Shatter-terra-heavy` — violent total breakage; very high CHUNKS, extreme EXPLODE and SPIN, no dissolve
   - **Flag:** confined: only 14/16 distinct frames; wide: only 13/16 distinct frames
297. `*.Break-Float-aqua` — broken pieces rise and drift apart in water; GRAVITY_ANGLE=0 chunks rise, moderate CHUNKS, low EXPLODE, no dissolve
298. `*.Break-Collapse-depth` — structure crushed and broken inward; BLAST_MODE=implode, moderate CHUNKS, no dissolve so the crushed pieces remain
299. `*.Break-Drift-space` — zero-gravity breakage, fragments scatter in all directions; GRAVITY_STRENGTH=0, moderate CHUNKS, moderate EXPLODE, no dissolve
300. `*.Break-Sunder-wave` — struck laterally, the structure breaks apart in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, moderate CHUNKS, no dissolve
301. `*.Break-Burst-inner` — structural failure originates from within and bursts outward; BLAST_MODE=burst, high CHUNKS and SPIN, no dissolve
