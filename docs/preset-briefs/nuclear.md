# Nuclear — 7 presets (registry #465–471)

Module: `presets/nuclear.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Exploded and obliterated with the most extreme physics and the flashiest visuals; orange-magenta.

**Gimmick lock** (revised in Stage 3 session 5b): the top of the chunk range on every preset (300–1000), maximal spin, fast consuming dissolve, and an orange → magenta colour arc at full opacity with yellow spark specks. (Was: "orange→magenta bidirectional tint with heavy `TINT_NOISE`", but `TINT_NOISE` has no effect at 200+ chunks.)

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 200–256, explode 2.0–12.0; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 5b)

- Lock **revised**: the top of the chunk range (300–1000; `Detonate-inner` is per-pixel at 1000), maximal spin (30–40), fast consuming dissolve, and an **orange → magenta colour arc** at full opacity, `instant`, with jittered yellow spark specks (deep outer front + small inner front, `blend` 0.12). The old "heavy `TINT_NOISE`" did nothing at 200+ chunks, and its 0.9-opacity `early` blend was what made the before sheets peach.
- `TINT_COLOR_ANIM_CURVE` is `t^(1/curve)`: values > 1 rush to the end colour. Fast-dissolving presets use 1.5–1.8 so the magenta shows before the pixels are gone.
- Locales differ mechanically: rain of specks burning out (`Obliterate-terra`, `random` dissolve, yellow fade); `filled_circle` fireball that swells, holds its shape, rises slowly and smoulders in dark magenta (`-fireball`, `noise` curve 1.6); rising column eaten by a `gravity_aligned` dissolve (aqua); `implode` with no gravity and no drag, so the specks rush in, cross the centre and blow out the far side as the colour flips magenta → orange (depth, the brief's "collapse then reverse"); `burst` scatter that spins down and leaves a few hanging embers (space, `DISSOLVE_MIN_PCT` 0.04); `shatter` + gravity 4.5 with full mass variance smearing sideways, leading edge vaporizing first (wave, `DISSOLVE_DIRECTION=90` (the brief's 270 predated the 3a correction)); yellow → orange → magenta flash that hollows from inside (inner, `explode` 1.4 instead of `burst`).
- Flags by design: `-fireball` stops at its `MAX_SIM_TICKS` (slow rise); `Implode-depth` ends 97 % off the confined canvas after the pixels have dissolved.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

465. `*.Nuclear-Obliterate-terra` — total nuclear obliteration, the most extreme physics in the library; max CHUNKS, max EXPLODE, max SPIN, orange-to-magenta bidirectional tint at max opacity with high TINT_NOISE for a chaotic fireball boundary, fast dissolve (DISSOLVE_CURVE<0.6) as the blast consumes everything
466. `*.Nuclear-Obliterate-terra-fireball` — fireball-style detonation with a billowing afterglow; max CHUNKS and EXPLODE, orange-magenta tint with elevated TINT_ALPHA_BLEED_OUTER for a glowing fringe, slower dissolve (DISSOLVE_CURVE>1.5) so the fireball lingers before fading
467. `*.Nuclear-Float-aqua` — underwater detonation, fragments rocket upward through the water column; GRAVITY_ANGLE=0, max CHUNKS and EXPLODE, orange-magenta tint, fast dissolve as the blast disperses through the water
468. `*.Nuclear-Implode-depth` — the detonation first collapses inward before the shockwave reverses outward; BLAST_MODE=implode, GRAVITY_MODE=centripetal, max CHUNKS, orange-magenta tint with high TINT_NOISE, fast dissolve as the collapsed mass vaporizes
469. `*.Nuclear-Drift-space` — zero-gravity obliteration, fragments scatter outward in all directions and spin down to a drift; GRAVITY_STRENGTH=0, max CHUNKS and EXPLODE, max SPIN, orange-magenta tint, fast dissolve
470. `*.Nuclear-Shockwave-wave` — struck by a lateral nuclear shockwave, blasted sideways at extreme force; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, max CHUNKS and EXPLODE, orange-magenta tint at max opacity, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments vaporize last
471. `*.Nuclear-Detonate-inner` — detonation originates from the sprite's own core, the most violent internal blast possible; BLAST_MODE=burst, max CHUNKS/EXPLODE/SPIN, bidirectional tint with a blinding orange-magenta inner core (inner_wins) and max TINT_NOISE, DISSOLVE_PATTERN=centrifugal fast dissolve as the blast consumes chunks outward from center
