# Disintegrate — 7 presets (registry #344–350)

Module: `presets/disintegrate.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Crumble + dissolve, no tint.

**Gimmick lock** (kept): 150+ chunks, `DISSOLVE_PATTERN="chunks"` preferred (whole fragments pop out), no tint.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six — each locale changes *how* the structure fails.

**Current state (2026-10-30):** chunks 150–220, explode 0.2–1.8; blast: explode 5, implode 1, horizontal_split 1; gravity: directional 5, centripetal 1, noise 1; tint on 7/7 (7 only via the default), dissolve 7/7, mask 0/7, stretched chunks 0/7.

**Stage 3 notes:**

- **Tint is currently on**: none of the 7 sets `TINT_DEPTH_OUTER`, so they inherit the default dark-red wound tint. Set `TINT_DEPTH_OUTER=0` on every preset.

## Stage 3 result (2026-10-31, session 4a)

- Lock kept: 160–240 chunks, no tint (`TINT_DEPTH_OUTER=0` on every preset — the inherited red wound tint is gone), light `TINT_GRAIN` 0.1–0.15, and `chunks` dissolve (whole fragments pop out) on every preset but `Sunder-wave` (leading-edge `directional` sweep, `DISSOLVE_DIRECTION=90` per the corrected note).
- Locales: `Crumble-terra` sags and falls while fragments blink out (stagger 0.6); `-fast` 240 fragments mostly gone in the first frames (curve 0.45); `Float-aqua` rises at uneven rates; `Collapse-depth` is a `vortex` that swirls the fragments in while they pop (instead of the brief's centripetal, which would duplicate Crush); `Drift-space` uses gentle `noise` (strength 0.05, `MAX_SIM_TICKS` 80; stronger pushed everything into a ring on the walls); `Burst-inner` holds its shape and drops fragments one at a time (stagger 0.85; the brief's `centrifugal` works per chunk and read as speckle).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

344. `*.Disintegrate-Crumble-terra` — standard crumble and fall apart, no tint; 150+ chunks, DISSOLVE_PATTERN=chunks so whole fragments pop out of existence as it falls
345. `*.Disintegrate-Crumble-terra-fast` — rapid total disintegration; even more chunks, fast dissolve curve, most fragments gone within the first few frames
346. `*.Disintegrate-Float-aqua` — fragments rise and fail apart in water; directional rise gravity, DISSOLVE_PATTERN=chunks with gravity-aligned stagger so upper fragments vanish first as the mass ascends and falls apart
347. `*.Disintegrate-Collapse-depth` — structure fails inward under centripetal compression; BLAST_MODE=implode, GRAVITY_MODE=centripetal, DISSOLVE_PATTERN=centripetal so the collapsing mass shrinks and vanishes from the center outward
348. `*.Disintegrate-Drift-space` — zero-gravity structural failure, fragments scatter with no settle; GRAVITY_MODE=noise for directionless drift, DISSOLVE_PATTERN=chunks, slower curve so fragments hang visibly before vanishing
349. `*.Disintegrate-Sunder-wave` — struck laterally, the structure fails in that direction as a fast physics event; horizontal_split blast, DISSOLVE_PATTERN=directional so trailing fragments vanish last behind the blast
350. `*.Disintegrate-Burst-inner` — structural failure spreads outward from a single point of flaw within, near-static; tiny EXPLODE via burst, DISSOLVE_PATTERN=centrifugal as the failure radiates outward from that origin point
