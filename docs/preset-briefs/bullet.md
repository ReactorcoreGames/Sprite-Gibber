# Bullet — 8 presets (registry #130–137)

Module: `presets/bullet.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Slug, buckshot, armour-piercing, incendiary, explosive, tracer and ricochet impacts. The bullet sprite always faces right; the animation is the impact or airburst.

**Gimmick lock** (new): **Wave-only, directional right**: every preset is a left-to-right impact (gravity 90°), heat-orange tint, trailing-edge dissolve. Left-facing is the game's job (mirror).

**Locales present:** wave ×8.

**Why these locales:** wave only — per the original type note. The idea file also listed `Slug-terra`, `Slug-depth` and `Buckshot-space`; they were never built and are dropped (the built set added `Slug-wave-heavy`, `Tracer-wave`, `Ricochet-wave` instead).

**Current state (2026-10-30):** chunks 3–45, explode 2.8–4.2; blast: horizontal_split 8; gravity: directional 8; tint on 8/8, dissolve 8/8, mask 0/8, stretched chunks 2/8.

**Stage 3 notes:**

- All 8 are `horizontal_split` — the left half initially flies *left*. For a pure rightward impact use explode/shatter with strong gravity 90°, or keep the split only where the brief wants a punch-through.

## Stage 3 result (2026-10-31)

- Lock kept (every preset wave, gravity 90°, heat-orange family, trailing-edge dissolve on most), but each round now differs mechanically: Slug (6 chunks, one dominant lump), Slug-heavy (20 pieces, yellow→red→char), Buckshot (170 grit, random pocking), Armor-Piercing (`horizontal_split` punch-through: left half kicks back, right half blown on, 8× horizontal spikes), Incendiary (noise burn-out), Explosive (`explode` in all directions, then the blast wind carries it right), Tracer (7× streaks with yellow-white cores), Ricochet (`BOUNCE` 0.6 off the right wall, sparks wink out with `chunks` dissolve).
- Everything ends against the right wall (it's the floor under 90° gravity); on the canvas-filling bear that's a column at the right edge by design.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

130. `*.Bullet-Slug-wave` — standard slug impact; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases fragments rightward, low CHUNKS (single deforming mass), moderate EXPLODE, CHUNK_MASS_VARIANCE high so one large deformed chunk dominates, no tint, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 trailing edge dissolves last
131. `*.Bullet-Slug-wave-heavy` — *(no idea line — from the in-app description)* Heavy caliber slug; more fragmentation and violent scatter with intense orange-red heat flash.
132. `*.Bullet-Buckshot-wave` — shotgun pellet spray; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, very high CHUNKS for many small pellets, high EXPLODE and SPREAD for cone-shaped scatter, no tint, fragments settle downward after the rightward push
133. `*.Bullet-Armor-Piercing-wave` — penetrator round; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, very low CHUNKS (minimal fragmentation), CHUNK_SHAPE_STRETCH high (CHUNK_SHAPE_ANGLE=90 horizontal slivers) for a punch-through spike read, low SPREAD so chunks stay tightly aligned to the impact line, no tint
134. `*.Bullet-Incendiary-wave` — incendiary round impact; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, moderate CHUNKS, orange outer to yellow inner bidirectional tint on fragments, TINT_ANIM=early so ignition is immediate, moderate dissolve with DISSOLVE_CHUNK_STAGGER as burning fragments cool, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270
135. `*.Bullet-Explosive-wave` — explosive/HE round detonation; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, high EXPLODE and CHUNKS for shaped-charge violence, high SPIN, no tint, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments linger longest
136. `*.Bullet-Tracer-wave` — *(no idea line — from the in-app description)* Tracer round; tight elongated streak blasts rightward with a bright yellow-white core fading to orange, trailing burn dissolves last.
137. `*.Bullet-Ricochet-wave` — *(no idea line — from the in-app description)* Ricochet impact; high mass variance sends one big deflected chunk wide while sparks spray with hot yellow-orange flash.
