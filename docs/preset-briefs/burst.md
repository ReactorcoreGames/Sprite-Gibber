# Burst — 6 presets (registry #447–452)

Module: `presets/burst.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Internal detonation, centre explodes outward, rupture aesthetic; no tint.

**Gimmick lock** (kept): extreme spin + high `EXPLODE`, no tint, `DISSOLVE=False` — fragments remain.

**Locales present:** terra ×3, aqua, space, wave.

**Why these locales:** terra, aqua, space, wave — depth contradicts outward force, inner restates the type.

**Current state (2026-10-30):** chunks 30–90, explode 2.0–9.0; blast: burst 5, horizontal_split 1; gravity: directional 6; tint on 6/6 (6 only via the default), dissolve 0/6, mask 0/6, stretched chunks 0/6.

**Stage 3 notes:**

- **Tint is currently on** (default red wound tint) — set `TINT_DEPTH_OUTER=0`.

## Stage 3 result (2026-10-31, session 5a)

- Lock kept: extreme spin (18–40) and high `EXPLODE`, `TINT_DEPTH_OUTER=0` (the inherited red wound tint is gone), `DISSOLVE=False`. Light grain (0.08) only on `-violent` and space.
- Variety from the size ladder and bounce: 60 fragments that clatter to rest (`BOUNCE` 0.3, terra); 140 stretched splinters with lower gravity and drag and bounce 0.55, so the debris hangs and rattles instead of being over by mid-animation (`-violent`); 14 big chunks tumbling into a heap (`-contained`, fixes its 14/16 flag); fragments spinning as they float up at mass-variance speeds (aqua); long splinters (stretch 3) coasting to a stop mid-canvas and still spinning (space, explode 1.8 so they don't jam the walls).
- `Sunder-wave` stays a `horizontal_split` (the brief's deliberate exception) but with 6 chunks and `CHUNK_BIAS="halves-v"`, so two halves cartwheel apart before the 90° wind drags them right. On the confined bear the left half starts against the wall, so the split reads mostly as tumbling.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

447. `*.Burst-Rupture-terra` — internal detonation, center explodes outward, no tint; BLAST_MODE=burst, high EXPLODE and CHUNKS, high SPIN, no dissolve so the rupture fragments remain scattered
448. `*.Burst-Rupture-terra-violent` — extreme internal detonation; BLAST_MODE=burst, extreme EXPLODE and CHUNKS, extreme SPIN, no dissolve
449. `*.Burst-Rupture-terra-contained` — smaller contained internal rupture; BLAST_MODE=burst, low-moderate EXPLODE, fewer CHUNKS, no dissolve
   - **Flag:** wide: only 14/16 distinct frames
450. `*.Burst-Float-aqua` — internal detonation underwater, fragments rise buoyantly as they scatter instead of falling; BLAST_MODE=burst, GRAVITY_ANGLE=0 chunks rise, moderate EXPLODE, no dissolve
451. `*.Burst-Drift-space` — zero-gravity internal detonation, fragments scatter in all directions with no settle; BLAST_MODE=burst, GRAVITY_STRENGTH=0, high CHUNKS, no dissolve
452. `*.Burst-Sunder-wave` — a lateral shockwave splits the body clean in half instead of scattering it omnidirectionally, a genuinely different fragmentation pattern from Rupture; BLAST_MODE=horizontal_split (not burst), GRAVITY_ANGLE=90, high EXPLODE, no dissolve
