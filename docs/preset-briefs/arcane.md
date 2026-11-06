# Arcane — 8 presets (registry #150–157)

Module: `presets/arcane.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Magic energy burst; blue/purple; more explosive than Psychic.

**Gimmick lock** (kept): mask-driven with the Y-Gears family read as a rune circle, 100–300 chunks, blue outer → purple inner through a noisy boundary.

**Locales present:** terra ×3, aqua, depth, space, wave, inner.

**Why these locales:** All six; terra has burst / overload / channel.

**Current state (2026-10-30):** chunks 120–280, explode 0.2–3.2; blast: explode 5, implode 1, horizontal_split 1, burst 1; gravity: directional 7, centripetal 1; tint on 8/8, dissolve 8/8, mask 8/8, stretched chunks 0/8.

## Stage 3 result (2026-10-31)

- Two-tone via chunk-mode bidirectional tint: royal-blue body on a deep outer front with a 1 px purple/magenta heart (`inner_wins`, inner 0.06–0.12), plus `TINT_NOISE`. Edges mode can't do this: it is unidirectional only (bidirectional keys ignored) and its colour and opacity share one ramp.
- `TINT_ANIM="instant"` throughout. With `early`, explosive presets had mostly dissolved before the tint reached full strength, so they read pale lilac.
- Fade colours must be saturated (`#0090FF`, `#C000FF`): in a preset that drops pixels all animation long, most visible pixels are mid-fade, and a pale fade colour washes the whole thing out.
- Gear choice: `Collapse-depth` uses the solid-centred sun gear `Y Gears (9)` because ring gears (`(2)`, `(3)`, `(4)`, `(6)`) erase the centre where depth pieces end up. `Burst-terra` drops dissolve and uses a `late` mask, so the gear stamps the floor pile at the end.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

150. `*.Arcane-Burst-terra` — a standard arcane detonation; dense chunk field beneath a solid gear-tooth Y-Gears mask reading as a rune-circle remainder, blue outer tint bleeds into a purple inner core through a swirling noisy boundary as energy disperses
151. `*.Arcane-Burst-terra-high` — a violent arcane overload; extreme chunk count and spin under an open-center toothed Y-Gears mask reading as a shattering rune-circle, bright blue-to-deep-purple tint through a chaotic noisy boundary as the spell consumes itself
152. `*.Arcane-Channel-terra` — sustained arcane channeling then release; a dense chunk field barely scatters at first while a hex-nut Y-Gears rune-circle mask fades in gradually alongside the blue-purple tint, discharging at the end
153. `*.Arcane-Vent-aqua` — arcane energy vents upward as mystical motes; a dense chunk field rises under a spoked-wheel Y-Gears mask, a translucent glowing core dissipates as motes ascend and fade
154. `*.Arcane-Collapse-depth` — an unstable spell collapses inward; a dense chunk field crushes under a thin-spoke Y-Gears rune-circle mask that tightens with the implosion, a deep purple core is crushed inward through a blue outer shell
155. `*.Arcane-Drift-space` — a zero-gravity arcane discharge; a dense chunk field drifts in all directions under a spiky sun-gear Y-Gears mask, an amorphous blue-to-purple glow fades slowly over many frames
156. `*.Arcane-Bolt-wave` — an arcane bolt impact triggers a directional eruption; a dense chunk field under a Y-Gears rune-circle mask rocks rightward, blue outer bleeds into purple inner at the impact, trailing fragments dissolve last
157. `*.Arcane-Ignition-inner` — the spell's origin point ignites at the sprite's core; a dense chunk field under a Y-Gears rune-circle mask reveals a deep purple core spreading outward to a blue outer border, consuming the chunks from the center out
