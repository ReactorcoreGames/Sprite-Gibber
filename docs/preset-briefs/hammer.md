# Hammer — 12 presets (registry #91–102)

Module: `presets/hammer.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Smash attacks: the centre is totalled while the shell fares better. Mechanical and elemental.

**Gimmick lock** (new): **Pulverised centre**: `CHUNK_BIAS="core"` + `CHUNK_MASS_VARIANCE` on every preset (powder in the middle, big rim pieces), blunt round chunks (no stretch except `Cryo-Smash`).

**Locales present:** terra ×8, aqua, depth, space, wave.

**Why these locales:** terra (×8 incl. elemental), aqua, depth, space, wave.

**Current state (2026-10-30):** chunks 10–50, explode 0.2–4.0; blast: explode 10, shatter 1, burst 1; gravity: directional 11, centripetal 1; tint on 4/12, dissolve 4/12, mask 0/12, stretched chunks 2/12.

**Stage 3 notes:**

- `Hammer-Press-depth` is a terra slam under a depth name — give it a real compression read (centripetal, or slam + very short travel) so the name is honest.

## Stage 3 result (2026-10-30)

- Smash family (`Smash`, `-heavy`, `Crater`, `Smash-space`, `Swing-wave`) carries a crimson bruise tint on chunk borders (outer 0.08–0.13): the pulverised core chunks are small enough to turn fully red, the big rim slabs only get bruised edges, which makes the core bias visible. `Pound`, `Smash-aqua` and `Press-depth` stay untinted as plain impact.
- `Press-depth` is now an implode + centripetal crush into one packed clump. `Crater` puffs its powder away as dust (random dissolve to 45 %). `Smash-space` uses `burst`.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

91. `*.Hammer-Smash-terra` — standard hammer blow; BLAST_MODE=explode, CHUNK_BIAS=core with high CHUNK_BIAS_STRENGTH so center is pulverized into many small chunks while edges stay larger, high EXPLODE, high SPIN, no tint, chunks scatter and settle downward
   - **Flag:** wide: only 14/16 distinct frames
92. `*.Hammer-Smash-terra-heavy` — heavy hammer blow; same as Smash but higher GRAVITY_STRENGTH so chunks slam down fast, higher CHUNK_MASS_VARIANCE, more CHUNKS for greater center destruction, no tint
93. `*.Hammer-Pound-terra` — slow deliberate pound; fewer but larger chunks, moderate EXPLODE, very high GRAVITY_STRENGTH so chunks hit the floor fast, LAUNCH_STAGGER low (simultaneous), no tint; the "weight" read comes from fast settle not fast scatter
94. `*.Hammer-Crater-terra` — boss-level hammer strike; maximum CHUNKS with CHUNK_BIAS=core at full strength for extreme center pulverization, high EXPLODE, high SPIN, CHUNK_MASS_VARIANCE high for mix of tiny center powder and large rim chunks, no tint
   - **Flag:** wide: only 14/16 distinct frames
95. `*.Hammer-Smash-aqua` — hammer blow in buoyant medium; BLAST_MODE=explode, CHUNK_BIAS=core, high EXPLODE pushes chunks outward then GRAVITY_ANGLE=0 pulls them upward so smashed chunks float away, moderate SPIN, no tint
96. `*.Hammer-Press-depth` — hydraulic press flattens sprite; BLAST_MODE=shatter (minimal velocity), very high GRAVITY_STRENGTH so all chunks slam to floor instantly, CHUNK_BIAS=core, many CHUNKS, no tint; compression read comes from near-zero scatter and instant settle
   - **Fix:** Terra slam under a depth name — give it a compression read.
   - **Flag:** confined: only 14/16 distinct frames
97. `*.Hammer-Smash-space` — hammer blow in zero gravity; GRAVITY_STRENGTH=0, BLAST_MODE=burst from center, CHUNK_BIAS=core, high SPIN, chunks tumble in all directions and drift indefinitely, no tint
98. `*.Hammer-Swing-wave` — lateral hammer swing; BLAST_MODE=explode, GRAVITY_ANGLE=90 flings chunks sideways, CHUNK_BIAS=core for pulverized center, high EXPLODE laterally, high SPIN, no CHUNK_SHAPE_STRETCH (blunt impact not a cut), no tint
99. `*.Hammer-Fire-Smash-terra` — fire-imbued hammer blow; BLAST_MODE=explode, CHUNK_BIAS=core, orange outer to yellow inner bidirectional tint on all chunks, moderate dissolve with DISSOLVE_CHUNK_STAGGER as embers scatter and burn out, high SPIN
100. `*.Hammer-Cryo-Smash-terra` — ice-imbued hammer blow; BLAST_MODE=explode, CHUNK_BIAS=core, icy-white outer to deep-blue inner bidirectional tint, CHUNK_SHAPE_STRETCH moderate for flat shard-like fragments, low SPIN for rigid ice behavior, minimal dissolve
101. `*.Hammer-Electric-Smash-terra` — electric-imbued hammer blow; BLAST_MODE=explode, CHUNK_BIAS=core, CHUNK_SHAPE_STRETCH diagonal for jagged fragments, cyan outer to yellow inner bidirectional tint, fast dissolve (DISSOLVE_CURVE<1) with DISSOLVE_CHUNK_STAGGER for staggered spark scatter
102. `*.Hammer-Acid-Smash-terra` — acid-imbued hammer blow; BLAST_MODE=explode, CHUNK_BIAS=core, TINT_MODE=edges lime-green tint eating inward from chunk surfaces, TINT_NOISE moderate, moderate dissolve with DISSOLVE_CHUNK_STAGGER as chunks are consumed at different rates
