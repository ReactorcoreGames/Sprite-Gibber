# Holy — 7 presets (registry #158–164)

Module: `presets/holy.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Softly turn white and phase out of existence; warm white.

**Gimmick lock** (kept): mask-driven with the Y-Flower family as a halo/bloom, 100–300 chunks, warm-white tint with a soft glowing fringe.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six; `Smother-depth` deliberately inverts the type (light being snuffed).

**Current state (2026-10-30):** chunks 130–200, explode 0.2–1.8; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 7/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31)

- Identity: gold-white light (`#FFEC50` → `#FFFCE8` arc, edges mode, depth 2.5), a slight translucent fringe (`TINT_ALPHA_BLEED_OUTER` 0.12; 0.35 read as mustard over the background), and a saturated gold `DISSOLVE_FADE_COLOR` (`#FFB000`) flash before each mote vanishes.
- Gentler than Arcane: force ≤ 0.6 except `Smother-depth`, and mostly `shatter` in place, so the Y-Flower masks (8-ray star, petals, rays) read on the bear.
- `Smother-depth` inverts the type with a gold → ash-grey arc. A negative `TINT_SATURATION_SHIFT` turned it grey from frame 1, so it was dropped.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

158. `*.Holy-Ascend-terra` — a gentle divine dissolution; a dense chunk field barely scatters beneath a soft 4-petal Y-Flower mask that reads as a radiating halo bloom, warm-white tint floods in with a soft glowing fringe as the body slowly fades to light
159. `*.Holy-Ascend-terra-fast` — a sudden divine claiming; a dense chunk field reveals an 8-petal Y-Flower radiant bloom mask immediately as the warm-white glow floods in, the chunks vanishing almost at once
160. `*.Holy-Rise-aqua` — the soul rises and dissolves into warm light; a dense chunk field floats upward beneath a rounded-diamond Y-Flower bloom mask, a translucent radiant core ascends gently out of frame
161. `*.Holy-Smother-depth` — divine light is crushed and snuffed out; a dense chunk field collapses inward beneath a tightening 6-petal Y-Flower mask, warm-white tint desaturating as the glow is choked out
162. `*.Holy-Drift-space` — zero-gravity sanctified motes; a dense chunk field drifts gently apart beneath a wide-petal Y-Flower halo mask, a soft even glow fades over many frames
163. `*.Holy-Smite-wave` — struck by a lateral beam of divine light; a dense chunk field impacts beneath a Y-Flower radiant mask blown open on the impact side, strong warm-white tint marks the impact as trailing fragments fade last
164. `*.Holy-Radiance-inner` — divine light erupts from within; a dense chunk field reveals a Y-Flower halo mask blooming outward from the core, a warm-white core spreads outward to a paler edge, consuming the chunks outward from the core
