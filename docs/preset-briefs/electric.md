# Electric — 11 presets (registry #29–39)

Module: `presets/electric.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Electrocution, lightning strikes, arc discharge, EMP. Shatter plus a tint that feels electric.

**Gimmick lock** (new): **Bolt-shaped shards**: `CHUNK_SHAPE_STRETCH` at 30–60° on every preset, an electric palette (cyan / electric blue / white / yellow) with a colour arc that never dims and **never lerps cyan ↔ yellow** (revised in Stage 3, see below), and per-chunk staggered dissolve so sparks wink out one by one.

**Locales present:** terra ×4, aqua, depth, space ×2, wave, inner ×2.

**Why these locales:** All six. Two space presets are distinct by motion (tumbling `Discharge` vs. noise-drifting `Storm`); `Orbit-inner` uses orbital — check off-canvas.

**Current state (2026-10-30):** chunks 20–80, explode 0.18–8.0; blast: explode 8, shatter 2, horizontal_split 1; gravity: directional 9, centripetal 1, noise 1; tint on 11/11, dissolve 11/11, mask 1/11, stretched chunks 10/11.

**Stage 3 notes:**

- The colour-QA pass (July) settled the cyan↔yellow swap and `early` for discharge events — keep that.

## Stage 3 result (2026-10-30)

- **Lock revised:** a direct cyan ↔ yellow swap passes through mint green, both in the colour arc (RGB lerp over time) and in `blend` collisions (lerp across the chunk). Every preset looked green. Now: fronts that meet use `outer_wins`/`inner_wins`; arcs run yellow → white, blue → cyan, cyan → white; yellow is an accent (spark cores, crackling rims), blue/cyan the body. A yellow `DISSOLVE_FADE_COLOR` over cyan also reads green, so cyan presets fade to `#88CCFF`/white.
- Depth is a fraction of the *whole sprite's* √px, so at 30–50 chunks an outer front of 0.3 covers whole chunks. Accents: outer ≈ 0.07–0.1 for a rim line, or a small inner core (0.1) with `inner_wins` and the body colour on a deep outer front.
- `Discharge-space` uses `burst` so the wide lion's shards spread up as well as down; `Storm-space` noise strength 0.15 / 80 ticks keeps it off the walls.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

29. `*.Electric-Shock-terra` — standard electrocution shatter; moderate CHUNKS, CHUNK_SHAPE_STRETCH diagonal (CHUNK_SHAPE_ANGLE=45) for jagged bolt-shaped shards, high SPIN, cyan outer to yellow inner bidirectional tint, fast dissolve with DISSOLVE_CHUNK_STAGGER for staggered spark fade
30. `*.Electric-Strike-terra` — violent lightning impact; extreme EXPLODE and SPIN, many chunks, CHUNK_SHAPE_STRETCH diagonal, bright cyan outer to white-yellow inner, very fast dissolve (DISSOLVE_CURVE<1 fast-out) as energy disperses instantly
31. `*.Electric-Arc-terra` — sustained arc discharge; low EXPLODE so chunks barely scatter, tint-dominant with deep TINT_DEPTH_OUTER cyan and TINT_DEPTH_INNER yellow, TINT_ANIM=linear so arc builds over frames, mild dissolve at end
32. `*.Electric-Overload-terra` — catastrophic electrical overload; maximum EXPLODE, maximum CHUNKS, extreme SPIN, CHUNK_SHAPE_STRETCH at steep diagonal, cyan outer to near-white inner, aggressive fast-out dissolve, DISSOLVE_CHUNK_STAGGER high for chaotic staggered annihilation
33. `*.Electric-Electrolysis-aqua` — electricity conducted through water, energy rises; GRAVITY_ANGLE=0 chunks rise, cyan bidirectional tint, DISSOLVE_PATTERN=centrifugal as charge dissipates outward-upward, moderate dissolve rate
34. `*.Electric-Arc-depth` — EMP implosion, electricity collapses inward; BLAST_MODE=implode, CHUNK_SHAPE_STRETCH diagonal for jagged inward-collapsing shards, cyan outer tint pressing inward, moderate dissolve as charge is absorbed
35. `*.Electric-Discharge-space` — zero-gravity spark scatter; GRAVITY_STRENGTH=0 so bolt-shaped shards (CHUNK_SHAPE_STRETCH diagonal) tumble in all directions, extreme SPIN, cyan-to-yellow bidirectional tint, slow dissolve (DISSOLVE_CURVE>1) as sparks cool
36. `*.Electric-Pulse-wave` — lateral EMP shockwave; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 pulls shards rightward, CHUNK_SHAPE_STRETCH at shallow diagonal, cyan outer tint, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing edge dissolves last
37. `*.Electric-Overload-inner` — internal electrical buildup detonates from core; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER yellow core radiating to cyan outer arc-flash border, high EXPLODE, fast dissolve from center outward (DISSOLVE_PATTERN=centrifugal)
38. `*.Electric-Storm-space` — electrical storm in zero-field space; GRAVITY_MODE=noise so bolt shards scatter then drift in ever-shifting organic directions, cyan-to-yellow bidirectional tint, CHUNK_SHAPE_STRETCH diagonal, erratic noise dissolve as charge dissipates
39. `*.Electric-Orbit-inner` — electrons orbiting; GRAVITY_MODE=orbital so diagonal bolt shards circle the sprite center slowly, cyan outer arc-flash to hot-yellow inner core, barely any physical drift outward, staggered centrifugal dissolve
