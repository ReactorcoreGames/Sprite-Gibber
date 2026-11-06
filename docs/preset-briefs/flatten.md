# Flatten — 4 presets (registry #461–464)

Module: `presets/flatten.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Strongly and quickly reduced to a flat plane with harsh gravity and many tiny chunks.

**Gimmick lock** (kept): very high chunk count + extreme gravity + `BOUNCE=0`, no tint, no dissolve.

**Locales present:** terra ×2, depth, inner.

**Why these locales:** terra, depth, inner.

**Current state (2026-10-30):** chunks 140–220, explode 0.2–1.8; blast: explode 2, implode 1, burst 1; gravity: directional 3, centripetal 1; tint on 4/4 (4 only via the default), dissolve 0/4, mask 0/4, stretched chunks 0/4.

**Stage 3 notes:**

- **Tint is currently on** (default red wound tint) — set `TINT_DEPTH_OUTER=0`.
- `Flatten-Slam-terra-extreme` settles in 3 ticks; frames interpolate between ticks, so it's smooth but over in a blink. Decide whether that's the joke or whether it needs a few more ticks.

## Stage 3 result (2026-10-31, session 5b)

- Lock kept: 160–400 chunks, extreme gravity, `BOUNCE=0`, `TINT_DEPTH_OUTER=0` (red tint gone), `DISSOLVE=False`; light grain (0.06) on three presets.
- `Slam-terra`: `shatter` + gravity 2.2 with mass variance, so the crumbs pour down at slightly different rates into a thin layer (no longer a blink). `-extreme` keeps the snap as the joke: 400 specks, gravity 9, a short `MS_PER_FRAME` and a long last-frame hold (13/16 distinct frames, by design).
- `Crush-depth`: overdamped centripetal (strength 1.2, drag 0.6) capped at 14 ticks, so the crumbs move inward at terminal speed and the sprite shrinks into a dense compressed slug instead of a single dot (the cap hit is by design).
- `Implode-inner`: no more `burst` (inner locale rule). `shatter` with mass variance 0.8 and drag 0.45 makes crumbs sag at very different rates, so the body caves in raggedly from within before settling flat.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

461. `*.Flatten-Slam-terra` — reduced to a flat plane fast and hard; high CHUNKS, low EXPLODE, very high GRAVITY_STRENGTH so chunks slam down quickly, BOUNCE=0, no dissolve so the flattened pile remains
   - **Flag:** wide: only 12/16 distinct frames
462. `*.Flatten-Slam-terra-extreme` — instant total flattening; even higher CHUNKS, max GRAVITY_STRENGTH, BOUNCE=0, no dissolve
   - **Flag:** confined: sim ended after 3 tick(s); wide: sim ended after 3 tick(s)
463. `*.Flatten-Crush-depth` — flattened by being crushed inward toward a point rather than slammed against a wall; BLAST_MODE=implode, GRAVITY_MODE=centripetal, no dissolve so the crushed mass remains
   - **Flag:** confined: only 13/16 distinct frames; wide: only 13/16 distinct frames
464. `*.Flatten-Implode-inner` — internal collapse flattens the form from within, starting from a burst-from-point pattern rather than the original silhouette, then slams flat; BLAST_MODE=burst with low EXPLODE followed by very high GRAVITY_STRENGTH, BOUNCE=0, no dissolve
