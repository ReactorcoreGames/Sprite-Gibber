# Preset Briefs — authoring reference

One brief per Main Type, consolidated in Stage 2 (2026-10-30) from the old preset design docs (`docs/presets WIP/`, now archived), the original type list and the current library. Each brief gives the type's intent, gimmick lock, locales and why, its current state, Stage 3 notes, and one line per preset describing the look to aim for, plus any Stage 2 fix and the baseline metric flags.

**How to use:** read `docs/preset-ideation-workflow.md` once per session (process, engine facts, rules), then open only the briefs for the types you're working on. All 61 types were rebuilt to these briefs in the Stage 3 overhaul (finished 2026-10-31), so the session plan and **Stage 3** column below are a record of that pass. Fix lines inside a brief are already applied.

**Ground rules:** every preset stays and keeps its name (`*.Category-Subtype-locale[-mod]`, single flat list). The briefs describe the target look; the parameter hints inside the original idea lines are suggestions, not requirements. Use the parameter space widely.

## Library-wide findings (fix in Stage 3 wherever they apply)

1. **Locale monoculture.** 62 of 65 wave presets are `horizontal_split` + gravity 90°; 46 of 60 depth presets are implode + centripetal; 46 of 67 space presets are plain zero-gravity explode; 47 of 58 aqua presets are explode + upward gravity; 31 of 55 inner presets are `burst` with zero gravity. About 25 types were stamped from the same six-locale template. Each type's locales should be built *through its gimmick lock*, not from the shared recipe.
2. **Default red tint on "untinted" presets.** Loading a preset resets every effect key to `DEFAULT_CONFIG` first, and the default tint is on (`TINT_DEPTH_OUTER=0.12`, dark red). 42 presets never set `TINT_DEPTH_OUTER`, so all of Disintegrate, Evaporate, Vanish, Burst, Clamp, Squeeze and Flatten, 4 Liquify and 1 Ash render a red wound tint they were never meant to have. Every preset must set `TINT_DEPTH_OUTER` explicitly (0 = off).
3. **Split axes crossed.** All 22 Blade/Slash split presets pair `BLAST_MODE` and `CHUNK_BIAS` on opposite axes. The cut convention is in `blade.md`/`slash.md`.
4. **Missing gimmick locks.** 31 types had no recorded lock; Stage 2 wrote one for each (marked *new*). Of the 30 existing locks, 29 were kept and Chromatic's was *revised* because `DISSOLVE_MIN_PCT=1.0` can't do what it relied on.
5. **Off-canvas repulsor.** `Plasma-Repulse-space` and `Smoke-Vent-aqua` put 100 % of pixels off-canvas.
6. **Heal.** Four locales (`Mend-terra`, `Restore-terra-fast`, `Drift-space`, `Surge-wave`) carry rework briefs.
7. **Original Blood preset** recovered — see `blood.md`; restored as-is in session 1 (first entry of `presets/blood.py`, library now 479).
8. **Washed-out colour** (found in session 1; full rules in `docs/preset-ideation-workflow.md` → *Colour authoring* → *Vivid colour*). The old presets mixed tint at partial strength into the sprite's own colours, so even pure reds came out peach and tan. Vivid needs opacity 1.0, fronts deep enough that opacity stays high, fully saturated hexes, and accent fronts sized to the chunk count. Several locks were revised for this (Electric, Water, Acid). Session 2 found more washout sources: `early`/`linear` tint ramps, pale dissolve fade colours on presets that drop pixels all animation, alpha bleed over the background, and partially animated masks. It also found two engine limits: edges mode is unidirectional only, and an `inner_wins` inner front swallows the body inside its cutoff. Blood's lock was revised to `instant`.

Baseline: `python tools/preset_metrics.py all` flagged 44/478 on 2026-10-30. **Stage 3 final pass (2026-10-31): 67/479 flagged, all by design** — 29 drag-limited drifts/creeps and rising sims capped at `MAX_SIM_TICKS`, 24 zero-motion/single-chunk/in-place presets ending in 1–3 ticks (Void, Heal, statues, inner fades) or a fast-settling split on the boxed-in bear, 12 with 13–15/16 distinct frames (settled piles held at the end, boxed-in bear, Flatten `-extreme` snap), 4 off-canvas after dissolving (Plasma-Repulse, Flash-Implode, Crush-Drift, Nuclear-Implode). Smoke 479/479. Most are intentional (Void's zero motion, single-chunk statues); the per-preset **Flag** lines say which.

## Stage 3 session plan

Sessions follow type boundaries so no type is split:

| Session | Types | Presets |
|---|---|---|
| 1 ✅ | Restore `*.Blood-Gibs-terra`; Fire → Hammer | #1–102 (102) |
| 2 ✅ | Slash → Blood | #103–200 (98) |
| 3a ✅ | Meat → Wither | #202–249 (48) |
| 3b ✅ | Stone → Break | #250–302 (53) |
| 4a ✅ | Crush → Disintegrate | #303–351 (49) |
| 4b ✅ | Evaporate → Matrix | #352–405 (54) |
| 5a ✅ | Tar → Burst | #406–453 (48) |
| 5b ✅ | Clamp → Antimatter | #454–479 (26) + final pass |

From session 3 on, each planned session is split in half at a type boundary (~50 presets) because sessions 1–2 ran long. Numbers in this table are post-restore (+1); the Types table below keeps the 2026-10-30 numbering.

## Types

| # | Type | Brief | Presets | Locales | Lock | Gimmick (first clause) | Stage 3 |
|---|---|---|---|---|---|---|---|
| 1–18 | Fire | [fire.md](fire.md) | 18 | terra ×8, aqua ×2, depth, space ×3, wave, inner ×3 | new | Every preset tells a **colour arc** with `TINT_COLOR_OUTER_END`/`INNER_END` (ignite → char black, or ignite → white-hot), and every … | ✅ 2026-10-30 |
| 19–28 | Cryo | [cryo.md](cryo.md) | 10 | terra ×4, aqua ×2, depth, space, wave, inner | new | every multi-chunk preset uses `CHUNK_SHAPE_STRETCH` ≥ 2 for sheet/shard geometry, tint is crisp and opaque (white frost → deep blue, … | ✅ 2026-10-30 |
| 29–39 | Electric | [electric.md](electric.md) | 11 | terra ×4, aqua, depth, space ×2, wave, inner ×2 | new | `CHUNK_SHAPE_STRETCH` at 30–60° on every preset, a saturated cyan ↔ yellow colour swap (`TINT_COLOR_*_END`, never dimming), and … | ✅ 2026-10-30 |
| 40–51 | Plasma | [plasma.md](plasma.md) | 12 | terra ×4, aqua, depth ×2, space ×3, wave, inner | new | `TINT_NOISE` warps the boundary on every preset, bidirectional tint with a bright inner core, magenta ↔ white-pink swap | ✅ 2026-10-30 |
| 52–63 | Water | [water.md](water.md) | 12 | terra ×3, aqua ×2, depth ×2, space ×2, wave ×2, inner | new | high chunk counts (150+), round chunks, semi-translucent blue (opacity 0.6–0.8, alpha bleed 0.1–0.3) — translucency is what separates … | ✅ 2026-10-30 |
| 64–72 | Acid | [acid.md](acid.md) | 9 | terra ×4, aqua, depth, space, wave, inner | new | `TINT_MODE="edges"` + `TINT_NOISE` corrosion front on most presets, few large chunks (8–30, per the original type note), low `EXPLODE`, … | ✅ 2026-10-30 |
| 73–78 | Singularity | [singularity.md](singularity.md) | 6 | depth ×3, space ×3 | kept | depth + space only; extreme black-red saturation (jitter/overlap 0.7–0.8, depth 0.7–0.9) with `pulse`/`early`/`late` throbbing; … | ✅ 2026-10-30 |
| 79–90 | Blade | [blade.md](blade.md) | 12 | terra ×9, aqua, space, wave | new | split `BLAST_MODE` with the matching `CHUNK_BIAS` axis, very few chunks (2–8), clean halves that part and settle | ✅ 2026-10-30 |
| 91–102 | Hammer | [hammer.md](hammer.md) | 12 | terra ×8, aqua, depth, space, wave | new | `CHUNK_BIAS="core"` + `CHUNK_MASS_VARIANCE` on every preset (powder in the middle, big rim pieces), blunt round chunks (no stretch … | ✅ 2026-10-30 |
| 103–115 | Slash | [slash.md](slash.md) | 13 | terra ×8, aqua, depth, space, wave, inner | new | very high `CHUNK_SHAPE_STRETCH` (6+) perpendicular to the cut line, split `BLAST_MODE` with matching bias | ✅ 2026-10-31 |
| 116–129 | Grenade | [grenade.md](grenade.md) | 14 | terra ×9, aqua, depth, space, wave, inner | new | high spin, high `CHUNK_MASS_VARIANCE` (uneven fragments), explosion from the canvas centre; each variant's identity comes from its … | ✅ 2026-10-31 |
| 130–137 | Bullet | [bullet.md](bullet.md) | 8 | wave ×8 | new | every preset is a left-to-right impact (gravity 90°), heat-orange tint, trailing-edge dissolve | ✅ 2026-10-31 |
| 138–143 | Void | [void.md](void.md) | 6 | terra, aqua, depth, space, wave, inner | kept | zero motion (`EXPLODE=0`, `GRAVITY_STRENGTH=0`, `SPIN=0`, `DISSOLVE=False`), 6–9 chunks, all interest from X-Splat `FRAME_MASK` … | ✅ 2026-10-31 |
| 144–149 | Psychic | [psychic.md](psychic.md) | 6 | terra ×2, aqua, depth, space, wave | kept | mask-driven with the C-Shape (geometric polygon) family, 100–300 chunks so the polygon remainder reads against dense debris; … | ✅ 2026-10-31 |
| 150–157 | Arcane | [arcane.md](arcane.md) | 8 | terra ×3, aqua, depth, space, wave, inner | kept | mask-driven with the Y-Gears family read as a rune circle, 100–300 chunks, blue outer → purple inner through a noisy boundary. | ✅ 2026-10-31 |
| 158–164 | Holy | [holy.md](holy.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | mask-driven with the Y-Flower family as a halo/bloom, 100–300 chunks, warm-white tint with a soft glowing fringe. | ✅ 2026-10-31 |
| 165–171 | Heal | [heal.md](heal.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | D-Cross mask family, `TINT_COLOR_*_END` sickly green → cyan-white on every preset, `DISSOLVE=False` everywhere (healing never … | ✅ 2026-10-31 |
| 172–178 | Photon | [photon.md](photon.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | very high chunk counts (150+) of tiny pieces, pure-white crisp tint (energy row: opacity 0.85–1.0, no bleed except glow fringes), low … | ✅ 2026-10-31 |
| 179–185 | Flash | [flash.md](flash.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | high `EXPLODE`, `DISSOLVE_CURVE` ≤ 0.5, `TINT_ANIM="early"`, cold white — the whole event happens in the first third of the frames and … | ✅ 2026-10-31 |
| 186–192 | Shadow | [shadow.md](shadow.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | `EXPLODE` ≤ 1, near-black tint that floods in at high opacity with some alpha bleed so the body goes dark *and* thin before dropping … | ✅ 2026-10-31 |
| 193–200 | Blood | [blood.md](blood.md) | 8 | terra ×3, aqua, depth, space, wave, inner | revised | very high chunk counts (150+), opaque ketchup red (opacity 1.0, no bleed except `Mist`/`Cloud`), `TINT_ANIM="instant"` + crimson darkening arcs | ✅ 2026-10-31 |
| 201–210 | Meat | [meat.md](meat.md) | 10 | terra ×5, aqua, depth, space, wave, inner | new | no dissolve (except `Gib-aqua`'s dispersal), wound tint on the chunk borders (`TINT_MODE="chunks"`), and the size ladder small → medium … | ✅ 2026-10-31 |
| 211–218 | Bone | [bone.md](bone.md) | 8 | terra ×3, aqua, depth, space, wave, inner | new | beige/ivory tint that drains in (flesh → bone via colour animation or `linear`), and hard pieces with some `BOUNCE` (0.2–0.4) so bones … | ✅ 2026-10-31 |
| 219–225 | Biodegrade | [biodegrade.md](biodegrade.md) | 7 | terra ×2, aqua, depth, space, wave, inner | revised | dissolve-driven decay in an earth palette — flat instant umber wash darkening to soil (colour arc), slow `DISSOLVE_CURVE` + dark-soil fade carry the shape | ✅ 2026-10-31 |
| 226–233 | Rot | [rot.md](rot.md) | 8 | terra ×3, aqua, depth, space, wave, inner | revised | sallow sickly flesh from frame 1, the rot arrives late as a colour arc to bile green (curve < 1), slime bleed, putrid fade | ✅ 2026-10-31 |
| 234–241 | Plague | [plague.md](plague.md) | 8 | terra ×3, aqua, depth, space, wave, inner | kept | `TINT_NOISE`-driven blotchy pustule pattern + high `TINT_JITTER` on every preset. | ✅ 2026-10-31 |
| 242–248 | Wither | [wither.md](wither.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | strongly negative `TINT_SATURATION_SHIFT` with minimal tint colour — desaturation is the effect. | ✅ 2026-10-31 |
| 249–257 | Stone | [stone.md](stone.md) | 9 | terra ×4, aqua, depth, space, wave, inner | new | grey tint at high opacity, no dissolve (except pebble dust), high gravity and low spin, and the size ladder single → slab → medium → pebble. | ✅ 2026-10-31 |
| 258–265 | Gold | [gold.md](gold.md) | 8 | terra ×3, aqua, depth, space, wave, inner | revised | deep-gold → bright-gold colour arc on every preset, positive `TINT_SATURATION_SHIFT`, bright glints (core specks or catch-light rims + grain); heavy … | ✅ 2026-10-31 |
| 266–272 | Crystal | [crystal.md](crystal.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | `CHUNK_SHAPE_STRETCH` on every preset, alpha bleed for translucency, a little `BOUNCE` for a glassy clink, no dissolve | ✅ 2026-10-31 |
| 273–279 | Rust | [rust.md](rust.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | colour animation raw → rust brown (`TINT_COLOR_*_END`) on every preset + partial dissolve (`DISSOLVE_MIN_PCT` 0.3–0.6, `noise` pattern) … | ✅ 2026-10-31 |
| 280–286 | Goo | [goo.md](goo.md) | 7 | terra ×2, aqua, depth, space, wave, inner | revised | very high chunk counts, translucent glossy violet, rubbery `BOUNCE` 0.45–0.6, low `EXPLODE`, no dissolve. | ✅ 2026-10-31 |
| 287–293 | Sand | [sand.md](sand.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | very high chunk counts (200+), low `EXPLODE`, gravity builds a pile; dissolve only takes the finest grains (`DISSOLVE_MIN_PCT` ≥ 0.3) | ✅ 2026-10-31 |
| 294–301 | Break | [break.md](break.md) | 8 | terra ×3, aqua, depth, space, wave, inner | new | no tint (`TINT_DEPTH_OUTER=0`), no dissolve, plain round Voronoi chunks (no stretch, no bias) | ✅ 2026-10-31 |
| 302–308 | Crush | [crush.md](crush.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | implode/centripetal motion, high chunk counts, dissolve as the powder disperses; no tint. | ✅ 2026-10-31 |
| 309–315 | Grind | [grind.md](grind.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | high spin with no spin drag in flight (floor friction stops it on landing), `CHUNK_MASS_VARIANCE`, rough debris; no tint, no dissolve. | ✅ 2026-10-31 |
| 316–322 | Shred | [shred.md](shred.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | `CHUNK_SHAPE_STRETCH` ≥ 4 on every preset, high drag so strips flutter; no tint, no dissolve | ✅ 2026-10-31 |
| 323–329 | Laser | [laser.md](laser.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | extreme `CHUNK_SHAPE_STRETCH` strips on every preset, `DISSOLVE` off throughout — a clean physical cut, visual interest from … | ✅ 2026-10-31 |
| 330–336 | Ion | [ion.md](ion.md) | 7 | terra ×2, aqua, depth, space, wave, inner | revised | dissolve on in every preset, irregular Voronoi (no stretch), full-opacity cyan + saturated blue fades — the dissolve carries the weight | ✅ 2026-10-31 |
| 337–343 | Crack | [crack.md](crack.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | no dissolve, tint minimal (a faint crack-line accent at most), jagged `CHUNK_SHAPE_STRETCH` fracture shapes + physics carry it. | ✅ 2026-10-31 |
| 344–350 | Disintegrate | [disintegrate.md](disintegrate.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | 150+ chunks, `DISSOLVE_PATTERN="chunks"` preferred (whole fragments pop out), no tint. | ✅ 2026-10-31 |
| 351–355 | Evaporate | [evaporate.md](evaporate.md) | 5 | terra ×2, aqua, space, wave | kept | dissolve-only, zero tint, a saturated `DISSOLVE_FADE_COLOR` flash right before pixels vanish, `DISSOLVE_MIN_PCT` near 0. | ✅ 2026-10-31 |
| 356–362 | Liquify | [liquify.md](liquify.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | no dissolve (liquid pools), high chunk counts, `BOUNCE=0` + high drag so chunks ooze and dead-stop. | ✅ 2026-10-31 |
| 363–368 | Smoke | [smoke.md](smoke.md) | 6 | terra ×2, aqua, space, wave, inner | revised | gas identity — always translucent (full-opacity smoke colour, high alpha bleed), high jitter for a wispy boundary, dissolve-pattern-driven … | ✅ 2026-10-31 |
| 369–375 | Ash | [ash.md](ash.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | solid particulate — 100+ chunks, a residue always remains (`DISSOLVE_MIN_PCT` ≥ 0.10), soot palette. | ✅ 2026-10-31 |
| 376–382 | Entropy | [entropy.md](entropy.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | strongly negative saturation shift, black/near-black `DISSOLVE_FADE_COLOR`, slow/late pacing — decay is gradual. | ✅ 2026-10-31 |
| 383–389 | Glitch | [glitch.md](glitch.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | high `CHUNK_MASS_VARIANCE` (0.5+), high `TINT_NOISE`, `DISSOLVE_PATTERN="noise"` everywhere — corruption never resolves cleanly. | ✅ 2026-10-31 |
| 390–396 | Chromatic | [chromatic.md](chromatic.md) | 7 | terra ×2, aqua, depth, space, wave, inner | revised | no pixel loss, carried by bidirectional red/blue tint with high alpha bleed on both fronts and a channel-swap colour animation … | ✅ 2026-10-31 |
| 397–404 | Matrix | [matrix.md](matrix.md) | 8 | terra ×3, aqua, depth, space, wave, inner | kept | green digital-rain tint; each locale has a different dissolve mechanic (terra/aqua directional cascade, depth centripetal … | ✅ 2026-10-31 |
| 405–411 | Tar | [tar.md](tar.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | maximum drag + very low `EXPLODE`, opaque glossy black-brown, no dissolve. | ✅ 2026-10-31 |
| 412–418 | Fungal | [fungal.md](fungal.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | `TINT_NOISE`-driven blob/colony growth, purple palette, slower `linear`/`late` pacing than Plague. | ✅ 2026-10-31 |
| 419–425 | Spore | [spore.md](spore.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | very high drag (0.30–0.34) → burst-then-drift; dissolve mostly off so spores linger. | ✅ 2026-10-31 |
| 426–432 | Brimstone | [brimstone.md](brimstone.md) | 7 | terra ×2, aqua, depth, space, wave, inner | new | red/orange ember tint with a smoky dark-grey `DISSOLVE_FADE_COLOR` and alpha bleed, slow curves, low motion | ✅ 2026-10-31 |
| 433–439 | Curse | [curse.md](curse.md) | 7 | terra ×2, aqua, depth, space, wave, inner | revised | vivid instant green with a black heart in every piece, spreading outward through a slow `centripetal` dissolve with a black fade; low chunk count … | ✅ 2026-10-31 |
| 440–446 | Vanish | [vanish.md](vanish.md) | 7 | terra ×3, depth, space, wave, inner | kept | magical erasure — strongly negative saturation shift, `DISSOLVE_PATTERN="random"` (except the deliberate `-noise` variant), no … | ✅ 2026-10-31 |
| 447–452 | Burst | [burst.md](burst.md) | 6 | terra ×3, aqua, space, wave | kept | extreme spin + high `EXPLODE`, no tint, `DISSOLVE=False` — fragments remain. | ✅ 2026-10-31 |
| 453–456 | Clamp | [clamp.md](clamp.md) | 4 | terra ×2, depth, space | kept | always a split `BLAST_MODE`, low-moderate chunks for two chunky halves, no tint, no dissolve. | ✅ 2026-10-31 |
| 457–460 | Squeeze | [squeeze.md](squeeze.md) | 4 | terra ×2, depth, space | kept | `x_split`, very low `EXPLODE`, high drag, no tint, no dissolve. | ✅ 2026-10-31 |
| 461–464 | Flatten | [flatten.md](flatten.md) | 4 | terra ×2, depth, inner | kept | very high chunk count + extreme gravity + `BOUNCE=0`, no tint, no dissolve. | ✅ 2026-10-31 |
| 465–471 | Nuclear | [nuclear.md](nuclear.md) | 7 | terra ×2, aqua, depth, space, wave, inner | revised | the top of the chunk range on every preset (300–1000), maximal spin, fast consuming dissolve, orange → magenta colour arc at full opacity with yellow sparks (`TINT_NOISE` dropped — no effect at 200+ chunks) | ✅ 2026-10-31 |
| 472–478 | Antimatter | [antimatter.md](antimatter.md) | 7 | terra ×2, aqua, depth, space, wave, inner | kept | implode + centripetal at the most extreme overdamped values, bizarre `CHUNK_SHAPE_STRETCH` angles, `TINT_SATURATION_SHIFT=+1.0`. | ✅ 2026-10-31 |
