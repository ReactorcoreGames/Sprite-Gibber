# Antimatter — 7 presets (registry #472–478)

Module: `presets/antimatter.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Imploded and obliterated with the most extreme negative physics; red-blue, max saturation, oddly shaped fragments.

**Gimmick lock** (kept): implode + centripetal at the most extreme overdamped values, bizarre `CHUNK_SHAPE_STRETCH` angles, `TINT_SATURATION_SHIFT=+1.0`.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 150–220, explode 0.15–3.5; blast: implode 3, explode 2, horizontal_split 1, shatter 1; gravity: centripetal 6, vortex 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 7/7.

## Stage 3 result (2026-10-31, session 5b)

- Lock kept with two noted exceptions: `implode`/`shatter`/split blasts with overdamped `centripetal` gravity, `TINT_SATURATION_SHIFT=+1.0` and bizarre stretch angles (17°, 37°, 73°, 101°, 128°, 152°, 163°) on every preset. `Float-aqua` swaps centripetal for weak upward gravity (the brief's "implosion fighting a rise" needs both, and a preset gets one gravity mode) and `Vortex-depth` uses `vortex` as the brief asks.
- Centripetal-dot problem solved by dropping from 150–220 chunks to 14–70 stretched slivers: overlapped at the centre they form a spiky star (`-instant`, `Drift-space`) or a warped knot, not a 1 px dot. A spinning core keeps the `-instant` sim alive after the fold (spin with no spin drag), so the snap happens in the first frames and the star whirls while it annihilates.
- Colour: vivid red/blue only (no white tint, so the +1 saturation is safe), opacity 1.0 `instant`, deep outer front + a small `inner_wins` heart. Each locale does its own colour behaviour: red slivers with blue hearts arcing to violet (terra), electric blue with red hearts (`-instant`), translucent red → blue with alpha bleed (aqua), blue → red with hearts heating to yellow as the spiral tightens (depth), red → blue with cyan hearts and a partial `chunks` dissolve leaving a stalled formation (space, `DISSOLVE_MIN_PCT` 0.35), red streaks with cyan hearts (wave), and blue shards with thin red rims hollowing from their hearts through a `centripetal` dissolve (inner, 14 fat shards so the blue core shows). Fades are saturated magenta/cyan/violet (`#FF00FF`, `#00C8FF`, `#8000FF`).
- Flags by design: `-instant` and `Float-aqua` run to their `MAX_SIM_TICKS` (spinning core; slow rise), `Singularity-inner` on the wide sprite (slow creep).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

472. `*.Antimatter-Annihilate-terra` — standard total annihilation; extreme overdamped centripetal implosion collapses the sprite into a warped, elongated red-blue core before it vanishes, chunks settle-crushed at the center
473. `*.Antimatter-Annihilate-terra-instant` — a near-instant collapse with almost no visible outward phase; higher GRAVITY_STRENGTH and lower EXPLODE than the standard version so the sprite folds in on itself within the first couple frames, most violent single-moment version of the type
474. `*.Antimatter-Float-aqua` — the collapse happens while chunks are also buoyed upward, an implosion fighting a rise; low upward drift layered under the centripetal pull produces a wobbling, unstable-looking compaction rather than a clean pull to center
475. `*.Antimatter-Vortex-depth` — instead of a straight pull to center, GRAVITY_MODE=vortex spirals the collapse inward with a tangential twist, chunks corkscrewing into the core rather than falling straight in — the one locale in this type that isn't plain centripetal
476. `*.Antimatter-Drift-space` — zero-gravity: chunks are pulled toward center by a weak repulsor-inverted pull that never fully forms (kept as centripetal but with GRAVITY_RAMP_TICKS so free-flight dominates), leaving fragments to hang and rotate mid-collapse rather than completing it, an annihilation caught mid-formation
477. `*.Antimatter-Shockwave-wave` — struck by a lateral field first, chunks fly sideways before centripetal force reverses them back toward center; the only locale with a real outward physical phase before the collapse, GRAVITY_RAMP_TICKS lets the sideways burst read clearly
478. `*.Antimatter-Singularity-inner` — collapse originates from and is centered on the sprite's own core with near-zero initial launch; a near-static implosion where chunks barely move before crushing inward, deep-blue core bleeding to red rim at max saturation
