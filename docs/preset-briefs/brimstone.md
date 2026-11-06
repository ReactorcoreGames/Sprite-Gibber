# Brimstone — 7 presets (registry #426–432)

Module: `presets/brimstone.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Infernal smoulder with heavy smoke and red embers; orange-red.

**Gimmick lock** (new): **Sooty smoulder**: red/orange ember tint with a smoky dark-grey `DISSOLVE_FADE_COLOR` and alpha bleed, slow curves, low motion. Fire flares; Brimstone smoulders and smokes.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 25–65, explode 0.2–2.4; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 5a)

- Lock kept: vivid ember red/orange on the outer front (`#9A0E00`–`#FF5A00`, opacity 1.0, `instant`) with **sulphur-yellow specks** on a small jittered inner front (0.12–0.16), a mid smoke-grey `DISSOLVE_FADE_COLOR` (`#504A4C`, strength 0.9–1.0) so every pixel turns to smoke before it vanishes, alpha bleed 0.1–0.25, slow curves (1.3–2.0) and low motion except `-violent`. A darker grey fade (`#2E2A2A`) over red read as maroon-brown, not smoke. The sulphur flecks and the smoke-out are what separate it from Fire's flare arcs.
- Mechanics per locale: slow slump while cooling to crimson (terra); spinning embers raining down (`-violent`); embers puffing up one after another and cooling to dark smoke via a colour arc (aqua); a drag-limited implode whose lumps *heat up* (crimson → blazing orange arc) and burn out from their hearts (`centripetal` dissolve, depth); cinders dimming and winking out whole (`chunks` dissolve, stagger 0.7, space); horizontal ember streaks pushed right (wave); 20 coals with yellow-hot hearts burning down from their edges (`centrifugal`, inner).
- **Fix applied:** `Sunder-wave` uses a low-force `explode` with 90° gravity and `DISSOLVE_DIRECTION=90` (leading side first, so the trail glows on as the brief intended). `Ignition-inner` uses `explode`, not `burst`.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

426. `*.Brimstone-Smolder-terra` — infernal smolder with heavy smoke and embers; low EXPLODE and SPIN, red outer to orange inner bidirectional tint, TINT_ALPHA_BLEED_OUTER high for a smoky fringe, slow dissolve (DISSOLVE_CURVE>1) as embers fade to ash over many frames
427. `*.Brimstone-Erupt-terra-violent` — violent infernal eruption; high EXPLODE and CHUNKS, orange-red tint at high TINT_OPACITY with TINT_NOISE moderate, moderate dissolve as embers scatter and fade
428. `*.Brimstone-Vent-aqua` — infernal heat vents upward as smoke and embers; GRAVITY_ANGLE=0 chunks rise, orange-red tint with high TINT_ALPHA_BLEED_OUTER, slow dissolve as embers fade while rising
429. `*.Brimstone-Collapse-depth` — smoldering mass collapses inward under infernal pressure; BLAST_MODE=implode, red-orange tint with TINT_COLLISION=inner_wins, moderate dissolve as the embers choke out
430. `*.Brimstone-Drift-space` — zero-gravity smoldering embers and smoke drift apart; GRAVITY_STRENGTH=0, low EXPLODE, orange-red bidirectional tint, slow dissolve (DISSOLVE_CURVE>1) over many frames
431. `*.Brimstone-Sunder-wave` — struck laterally by infernal force, embers and smoke scatter in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, orange-red tint at high TINT_OPACITY_OUTER, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing embers fade last
432. `*.Brimstone-Ignition-inner` — infernal fire erupts outward from a point within, embers radiating; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER deep-red core spreading to orange outer edge, DISSOLVE_PATTERN=centrifugal as embers disperse outward from center
