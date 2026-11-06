# Vanish — 7 presets (registry #440–446)

Module: `presets/vanish.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Gradually fade away in various styles; desaturating.

**Gimmick lock** (kept): magical erasure — strongly negative saturation shift, `DISSOLVE_PATTERN="random"` (except the deliberate `-noise` variant), no tint colour (a neutral grey at opacity 0.35 keeps detail under the shift) and a white flash on every vanishing pixel.

**Locales present:** terra ×3, depth, space, wave, inner.

**Why these locales:** terra, depth, space, wave, inner — aqua dropped (rising adds nothing to random erasure).

**Current state (2026-10-30):** chunks 45–55, explode 0.12–1.5; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 5, centripetal 1, noise 1; tint on 7/7 (7 only via the default), dissolve 7/7, mask 0/7, stretched chunks 0/7.

**Stage 3 notes:**

- **Tint is currently on** (no `TINT_DEPTH_OUTER` → default red wound tint), which also means the saturation shift is riding on a red tint. Set `TINT_DEPTH_OUTER` explicitly; if desaturation needs a tint pass to act on, use a neutral grey tint at low opacity.

## Stage 3 result (2026-10-31, session 5a)

- Lock kept, with the brief's own suggestion applied: `TINT_SATURATION_SHIFT` −1.0 plus a **neutral cool-grey tint at opacity 0.35** (`#5E5E68`, depth 4.0). An HSV shift alone sets each pixel to grey at V = max(R,G,B), so the orange lion bleached to near-white and the effect read as white static. The grey keeps detail. Every vanishing pixel then flashes **white** (`DISSOLVE_FADE_COLOR` `#FFFFFF`, strength 0.9–1.0) — a magic eraser, apart from Evaporate (saturated flash, sprite colours kept), Entropy (darkens to black) and Wither (grey husks with cracks). `random` dissolve everywhere except `-noise`; nothing remains (min 0.01).
- The drain is `early` on most presets and `instant` on `-fast` and wave. `linear`/`late` drains passed through peach on the lion and were dropped. Locales differ by motion and stagger: a motionless `SINGLE_CHUNK` statue (`Fade-terra`, flagged 1-tick by design); a quick puff (`-fast`, curve 0.45); a patchy sagging erase (`-noise`); a drag-limited implode that shrinks as it thins (depth); a `noise`-gravity drift (space); horizontal streaks pushed right (wave); 12 still slabs erased one after another (inner, `DISSOLVE_CHUNK_STAGGER` 0.85).
- **Fix applied:** wave and inner keep `random` (the lock) instead of the brief's `directional`/`centrifugal`; `Collapse-depth` is a drag-limited implode, not centripetal.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

440. `*.Vanish-Fade-terra` — gradual even fade-out in place, no tint color, only a desaturating shift; very low EXPLODE and SPIN, slow dissolve (DISSOLVE_CURVE>1) with random-pattern dropout so the body fades evenly over many frames
441. `*.Vanish-Fade-terra-fast` — quick vanish; low EXPLODE, fast dissolve (DISSOLVE_CURVE<1) with random-pattern dropout so the body disappears rapidly
442. `*.Vanish-Fade-terra-noise` — organic patchy fade instead of uniform erasure; DISSOLVE_PATTERN=noise so patches vanish irregularly rather than evenly
443. `*.Vanish-Collapse-depth` — body shrinks and fades inward as it vanishes; BLAST_MODE=implode with centripetal gravity, DISSOLVE_PATTERN=centripetal so it visibly shrinks toward center while erasing
444. `*.Vanish-Drift-space` — zero-gravity fade with no directional bias; GRAVITY_MODE=noise for directionless drift, very low EXPLODE, slow random-pattern dissolve over many frames
445. `*.Vanish-Sunder-wave` — struck laterally, the body is erased in that direction as a fast physics event; horizontal_split blast, directional dissolve so trailing fragments fade last
446. `*.Vanish-Unmake-inner` — vanishing spreads outward from a point within, as if a spell unravels from its cast point; BLAST_MODE=burst with tiny EXPLODE, DISSOLVE_PATTERN=centrifugal as the body erases outward from that origin
