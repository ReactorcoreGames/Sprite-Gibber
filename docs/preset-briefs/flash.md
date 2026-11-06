# Flash — 7 presets (registry #179–185)

Module: `presets/flash.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Violently turned into light particles by extreme physics — annihilating beam, nuclear fireball.

**Gimmick lock** (new): **Front-loaded annihilation**: high `EXPLODE`, `DISSOLVE_CURVE` ≤ 0.5, `TINT_ANIM="early"`, cold white — the whole event happens in the first third of the frames and the rest is afterglow.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 90–200, explode 2.2–6.0; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 7; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

**Stage 3 notes:**

- Nuclear is the type for the most extreme physics; Flash is about the light. Keep Flash less fragmented than Nuclear and whiter.

## Stage 3 result (2026-10-31)

- Front-loaded: `TINT_ANIM="instant"` white, `DISSOLVE_CURVE` 0.3–0.5, white → electric blue/violet afterglow arc held with `TINT_COLOR_ANIM_CURVE` 0.4–0.6, matching blue fade colour. 60–120 chunks (less fragmented than Nuclear).
- `Implode-depth` = `implode` with zero gravity: pieces converge, punch through the centre and blow back out, vaporising (sim capped at 20 ticks). The off-canvas metric flag on the bear is that blowout.
- `Detonate-inner` cracks in place (`shatter` 0.5): inner locale, so the burn-out carries it, not travel.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

179. `*.Flash-Annihilate-terra` — violent total annihilation; extreme EXPLODE, extreme CHUNKS, extreme SPIN, cold-white tint at max TINT_OPACITY_OUTER, TINT_ALPHA_BLEED_OUTER high for a blinding fringe, fast dissolve (DISSOLVE_CURVE<1) as the body is consumed almost instantly
180. `*.Flash-Overload-terra-mega` — single catastrophic beam strike, the most extreme version; max EXPLODE and CHUNKS, max SPIN, cold-white bidirectional tint with TINT_NOISE high for a chaotic blinding boundary, very fast dissolve as nothing remains within a couple frames
181. `*.Flash-Vent-aqua` — annihilated underwater, flash-boiled upward; GRAVITY_ANGLE=0 chunks rocket upward, extreme EXPLODE, cold-white tint with high TINT_ALPHA_BLEED_INNER, fast dissolve as the steam-light burst dissipates
182. `*.Flash-Implode-depth` — beam collapses the target inward before detonating outward; BLAST_MODE=implode then high SPIN, cold-white tint with TINT_DEPTH_OUTER large covering the whole form, fast dissolve as the collapsed mass vaporizes
183. `*.Flash-Burst-space` — zero-gravity beam annihilation; GRAVITY_STRENGTH=0, extreme EXPLODE and CHUNKS so fragments scatter in all directions, cold-white bidirectional tint, fast dissolve (DISSOLVE_CURVE<1) as the particle field disperses into nothing
184. `*.Flash-Beamstrike-wave` — struck dead-on by a lateral annihilation beam; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks violently rightward, extreme EXPLODE, cold-white tint at max opacity, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments vaporize last
185. `*.Flash-Detonate-inner` — annihilation originates from the sprite's core in a blinding internal blast; BLAST_MODE=burst, extreme EXPLODE and SPIN, bidirectional tint with large TINT_DEPTH_INNER blinding-white core, DISSOLVE_PATTERN=centrifugal fast dissolve as the blast consumes the chunks outward from center
