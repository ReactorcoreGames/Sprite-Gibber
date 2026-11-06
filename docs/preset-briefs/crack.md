# Crack — 7 presets (registry #337–343)

Module: `presets/crack.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Break into rough chunks.

**Gimmick lock** (kept): no dissolve, tint minimal (a faint crack-line accent at most), jagged `CHUNK_SHAPE_STRETCH` fracture shapes + physics carry it.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six — fracture is a physical event.

**Current state (2026-10-30):** chunks 22–60, explode 0.25–2.2; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 0/7, dissolve 0/7, mask 0/7, stretched chunks 7/7.

## Stage 3 result (2026-10-31, session 4a)

- Lock kept: jagged stretch 2.0–3.0 at a different angle on every preset (20°–150°), low force, no dissolve. The crack-line accent is a 1 px dark front (`#3A3530`; wet `#1E3448` on aqua) at opacity 0.45. At 0.6–0.7 it darkened the whole small lion, because stretched shards are mostly border pixels. `-fine` and `Drift-space` stay untinted for contrast. `Fracture-terra` and `Sunder-wave` use `early` so the cracks appear as the pieces part; `Burst-inner` uses `linear` so the cracks spread over the whole animation while the 20 pieces ease apart slowly (drag 0.08, so it no longer stops after 5 ticks).
- `Collapse-depth` is a drag-limited `implode` (zero gravity, drag 0.2): 18 long pieces squeeze inward and lock, instead of Break's centripetal jumble. `Sunder-wave` is `shatter` + 90° gravity with mass variance 1.0, so tall slabs break off and slide right one after another.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

337. `*.Crack-Fracture-terra` — plain rough fracture, jagged irregular chunk silhouettes, no tint; moderate CHUNKS, low-moderate EXPLODE, low SPIN so pieces settle close to where they fell, no dissolve
338. `*.Crack-Fracture-terra-fine` — finer cracking into more numerous rough pieces with tighter fracture lines; high CHUNKS, low EXPLODE, no dissolve
339. `*.Crack-Float-aqua` — cracked pieces drift apart slowly in water, jagged edges tumbling gently; GRAVITY_ANGLE=0 chunks rise, moderate CHUNKS, low EXPLODE, no dissolve
340. `*.Crack-Collapse-depth` — structure cracks and caves inward, rubble piling into a jagged compact heap; BLAST_MODE=implode, GRAVITY_MODE=centripetal, moderate CHUNKS, no dissolve so the cracked rubble remains intact
   - **Flag:** confined: only 14/16 distinct frames
341. `*.Crack-Drift-space` — zero-gravity cracked fragments drift apart gently, tumbling in place with no settle; GRAVITY_STRENGTH=0, moderate CHUNKS, low EXPLODE, no dissolve
342. `*.Crack-Sunder-wave` — struck laterally, the structure cracks apart in that direction, jagged pieces thrown sideways; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, moderate CHUNKS, no dissolve
343. `*.Crack-Burst-inner` — cracking originates from a stress point within and spreads outward, pieces barely separating around the fracture origin; BLAST_MODE=burst, moderate CHUNKS, low EXPLODE, no dissolve
   - **Flag:** confined: only 12/16 distinct frames; wide: only 14/16 distinct frames
