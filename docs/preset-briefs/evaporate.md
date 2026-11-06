# Evaporate — 5 presets (registry #351–355)

Module: `presets/evaporate.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Turn into vapour without tint; go transparent.

**Gimmick lock** (kept): dissolve-only, zero tint, a saturated `DISSOLVE_FADE_COLOR` flash right before pixels vanish (was *pale*; see *Stage 3 result*), `DISSOLVE_MIN_PCT` near 0.

**Locales present:** terra ×2, aqua, space, wave.

**Why these locales:** terra, aqua, space, wave — depth dropped (evaporation disperses, it doesn't compress), inner dropped (no natural origin point).

**Current state (2026-10-30):** chunks 55–60, explode 0.25–1.2; blast: explode 4, horizontal_split 1; gravity: directional 4, noise 1; tint on 5/5 (5 only via the default), dissolve 5/5, mask 0/5, stretched chunks 0/5.

**Stage 3 notes:**

- **Tint is currently on** (no `TINT_DEPTH_OUTER` set → default red wound tint). Set it to 0 on every preset.

## Stage 3 result (2026-10-31, session 4b)

- Lock kept with one change: the flash colour is **saturated**, not pale. Most visible pixels are mid-fade at any moment, so a pale fade washed the whole preset out. `TINT_DEPTH_OUTER=0` on every preset (the inherited red wound tint is gone), with no grain, so the sprite keeps its own colours until it flashes and vanishes. Fade strength 0.95.
- Each locale has its own flash colour and dissolve mechanic: `Fade-terra` sags slightly and boils off from the top down (`directional` 0, steam blue `#20B8FF`); `-fast` puffs apart and vanishes in a yellow-hot `random` speckle (curve 0.4); `Rise-aqua` lifts at uneven speeds and thins from the top (`gravity_aligned`, aqua `#00F0C8`); `Drift-space` drifts on gentle `noise` gravity (0.05) and thins in violet `noise` patches; `Sunder-wave` is a low-force explode carried right by 90° gravity with a leading-side-first sweep (`DISSOLVE_DIRECTION=90`, blue `#2060FF`).
- **Fix applied:** `Sunder-wave` no longer uses `horizontal_split` (it sends the left half left first) or `DISSOLVE_DIRECTION=270` (that removes the trailing side first; the brief wanted the trailing wisps to fade last).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

351. `*.Evaporate-Fade-terra` — body turns transparent and evaporates in place; low EXPLODE and SPIN, no tint, slow dissolve (DISSOLVE_CURVE>1) so the fade-out is gradual and visible, pale DISSOLVE_FADE_COLOR flash right before each pixel vanishes
352. `*.Evaporate-Fade-terra-fast` — rapid evaporation; fast dissolve (DISSOLVE_CURVE<1) as the body vanishes almost immediately, near-simultaneous DISSOLVE_CHUNK_STAGGER
353. `*.Evaporate-Rise-aqua` — body evaporates upward as steam; directional rise gravity, no tint, slow gravity_aligned dissolve as it thins out while ascending, pale fade color at the vanish moment
354. `*.Evaporate-Drift-space` — zero-gravity evaporation, fragments drift apart weightlessly and thin out with no directional bias; GRAVITY_MODE=noise, no tint, very slow dissolve fading over many frames
355. `*.Evaporate-Sunder-wave` — struck laterally, the body evaporates away in that direction as a fast physics event; horizontal_split blast, no tint, directional dissolve so trailing wisps fade last
