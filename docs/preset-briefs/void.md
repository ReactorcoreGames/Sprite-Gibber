# Void — 6 presets (registry #138–143)

Module: `presets/void.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Pulled into murky darkness / taken into the shadow realm; deep dark blue.

**Gimmick lock** (kept): zero motion (`EXPLODE=0`, `GRAVITY_STRENGTH=0`, `SPIN=0`, `DISSOLVE=False`), 6–9 chunks, all interest from X-Splat `FRAME_MASK` opacity animation + tint.

**Locales present:** terra, aqua, depth, space, wave, inner.

**Why these locales:** All six by name, distinguished by mask shape, orientation and animation curve rather than physics (zero motion is the lock).

**Current state (2026-10-30):** chunks 6–9, explode 0.0–0.0; blast: explode 6; gravity: directional 6; tint on 6/6, dissolve 0/6, mask 6/6, stretched chunks 0/6.

**Stage 3 notes:**

- The idea file lists `per_chunk` among `FRAME_MASK_ANIM` values — not valid for masks (`instant`/`linear`/`early`/`late`/`pulse` only).
- All six are flagged (1-tick sims, 6–14 distinct frames). That's the lock, but a 6/16 distinct-frame animation is mostly holds — use a mask curve and tint animation that change every frame.

## Stage 3 result (2026-10-31)

- Lock kept (zero motion, no dissolve, 6–9 chunks, X-Splat masks). The old masks were round/soft and barely bit; now spiky or holey splats (`X Splat (20/21/26/29/35/37)`) carve a visible silhouette.
- Every preset changes every frame: a saturated ultramarine (`#1830FF`) → black colour arc on top of the mask curve, so the distinct-frame flags are gone. The remaining 1-tick flags are the lock.
- `Vortex-space` keeps the `pulse` mask (the rift swells and recedes) but its tint is `early` + an ultramarine → violet arc, so it ends on a vivid violet body rather than the intact sprite.
- `Hollow-inner` uses `per_chunk`, so the tint arrives patchily and late; it ends vivid violet/black, pocked by `X Splat (35)`'s holes.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

138. `*.Void-Consume-terra` — the sprite doesn't break apart, it is consumed in place; near-zero motion, deep dark-blue-to-black tint floods in as an X-Splat void rift mask swallows the silhouette from within
   - **Flag:** confined: sim ended after 1 tick(s); wide: sim ended after 1 tick(s)
139. `*.Void-Bloom-aqua` — a void bloom opens softly, the rift's edges reading as a pale-blue splat silhouette that grows outward; opacity ramps in slowly as if surfacing from deep water, no chunk motion at all
   - **Fix:** Only 9/16 distinct frames.
   - **Flag:** confined: only 9/16 distinct frames; sim ended after 1 tick(s); wide: only 9/16 distinct frames; sim ended after 1 tick(s)
140. `*.Void-Crush-depth` — crushing void pressure without any physical implosion; the sprite stays put while a jagged X-Splat rift mask eats inward and near-black tint floods to maximum depth and opacity, reading as annihilation-by-erasure
   - **Fix:** Only 6/16 distinct frames.
   - **Flag:** confined: only 6/16 distinct frames; sim ended after 1 tick(s); wide: only 6/16 distinct frames; sim ended after 1 tick(s)
141. `*.Void-Vortex-space` — a void rift hangs in zero gravity; a wide spiky X-Splat mask pulses its opacity in rhythmic waves as if the rift is breathing, dark-blue-to-black tint underneath with a noisy warped boundary
   - **Fix:** Only 9/16 distinct frames.
   - **Flag:** confined: only 9/16 distinct frames; sim ended after 1 tick(s); wide: only 9/16 distinct frames; sim ended after 1 tick(s)
142. `*.Void-Drag-wave` — the void rift opens to one side, dragging the silhouette's presence into it; a laterally-mirrored X-Splat mask erodes in from that side while dark-blue tint deepens, motion stays minimal since the erasure itself is the pull
   - **Fix:** Only 6/16 distinct frames.
   - **Flag:** confined: only 6/16 distinct frames; sim ended after 1 tick(s); wide: only 6/16 distinct frames; sim ended after 1 tick(s)
143. `*.Void-Hollow-inner` — a void opens from within the sprite's own core; a tight rounded X-Splat mask grows outward from the center while near-black inner tint dominates over a dark-blue outer edge, the interior hollowing out before the shape is claimed
   - **Flag:** confined: only 14/16 distinct frames; sim ended after 1 tick(s); wide: only 14/16 distinct frames; sim ended after 1 tick(s)
