# Smoke — 6 presets (registry #363–368)

Module: `presets/smoke.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Turn to smoke; grey.

**Gimmick lock** (kept): gas identity — always translucent (full-opacity smoke colour with high alpha bleed; was *mid-low opacity*, see *Stage 3 result*), high jitter for a wispy boundary, dissolve-pattern-driven fade, never a hard physics event.

**Locales present:** terra ×2, aqua, space, wave, inner.

**Why these locales:** terra, aqua, space, wave, inner — depth dropped (smoke disperses, it doesn't clump).

**Current state (2026-10-30):** chunks 100–140, explode 0.18–1.3; blast: explode 5, horizontal_split 1; gravity: directional 4, repulsor 1, noise 1; tint on 6/6, dissolve 6/6, mask 0/6, stretched chunks 0/6.

**Stage 3 notes:**

- `Smoke-Vent-aqua` flings 100 % of pixels off-canvas (repulsor, no containment) — rebuild it so the rise stays on screen.

## Stage 3 result (2026-10-31, session 4b)

- **Lock revised:** translucency comes from alpha bleed over a **full-opacity** smoke colour (bleed 0.3–0.45 on the outer front, about half that inside), not from mid-low opacity. Partial-opacity grey over the lion was the old grey-pink mush. Every preset is bidirectional at 60–150 chunks with jittered fronts, light grain and its own colour: pale grey `Billow-terra` (`#C8C8D2`), sooty black `-thick` (`#2C2C32`, bleed 0.32), steam-blue `Vent-aqua` (`#6EA8DC`), lavender `Drift-space` (`#A890E8`), dust-tan `Sunder-wave` (`#B08A58`), and dark smoke with ember specks dimming to deep red in `Plume-inner` (60 chunks, so the embers stay sparse).
- Bleed shows the background: mid-grey smoke at bleed 0.5 vanished against the grey sheet, and border pixels take the full bleed. Keep colours off the background's value.
- Locales differ by mechanic: `gravity_aligned` top-down thinning while rising (terra), a slow `noise` break-up after a long hang (`-thick`, curve 2.0), staggered puffs (`LAUNCH_STAGGER` 0.08) at mismatched rise speeds (aqua), gentle `noise` gravity drift (space), a leading-side-first sweep in a 90° gale (wave), smoulder in place (inner).
- **Fixes applied:** `Vent-aqua` no longer uses `repulsor` (100 % off-canvas). The chaotic rise is upward gravity + mass variance 1.0 + `SPREAD` 2 + launch stagger. `Sunder-wave` is tinted after all (the brief's near-zero tint breaks the translucency lock) and uses `DISSOLVE_DIRECTION=90`. `Plume-inner` uses `noise`, not `centrifugal` (per chunk, so it read as speckle).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

363. `*.Smoke-Billow-terra` — body turns to billowing grey smoke that rises and disperses under directional upward gravity; wispy alpha-bled edges, DISSOLVE_PATTERN=gravity_aligned so the plume thins from the top down as it climbs
364. `*.Smoke-Billow-terra-thick` — thick dense smoke, slower to disperse; higher TINT_OPACITY_OUTER and much slower DISSOLVE_CURVE, lingers many frames before gravity_aligned dissolve clears it
365. `*.Smoke-Vent-aqua` — bubbling vapor rising through water in an irregular, non-uniform column; GRAVITY_MODE=repulsor with low strength gives a chaotic bubble-like rise instead of a clean drift, bidirectional pale blue-grey/white tint, noise dissolve
   - **Fix:** 100 % off-canvas (repulsor, no containment). Rebuild the chaotic rise so it stays on screen (e.g. upward gravity + noise-like spread via `SPREAD`/mass variance).
   - **Flag:** confined: only 6/16 distinct frames; 100.0% pixels off-canvas; wide: only 8/16 distinct frames; 100.0% pixels off-canvas
366. `*.Smoke-Drift-space` — zero-gravity smoke with no directional bias at all; GRAVITY_MODE=noise gives per-chunk organic wandering in all directions, low TINT_OPACITY_OUTER (near-invisible haze), very slow noise dissolve lingering longest of the type
367. `*.Smoke-Sunder-wave` — struck laterally by a shockwave and blown sideways as a fast-moving physics event; horizontal_split blast at high GRAVITY_STRENGTH, TINT_DEPTH_OUTER near-zero (no tint) so the motion itself carries the read, directional dissolve trailing behind
368. `*.Smoke-Plume-inner` — smoke seeps outward from a smoldering point within, near-static; GRAVITY_STRENGTH=0, tiny EXPLODE, bidirectional tint with inner_wins collision so the glowing origin point reads through, centrifugal dissolve spreading slowly outward
