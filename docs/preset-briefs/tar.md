# Tar — 7 presets (registry #405–411)

Module: `presets/tar.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Pools slowly; heavy physics; black-brown.

**Gimmick lock** (new): **Sluggish weight**: maximum drag + very low `EXPLODE`, opaque glossy black-brown, no dissolve.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six; aqua sinks slowly.

**Current state (2026-10-30):** chunks 80–120, explode 0.15–1.6; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 0/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 5a)

- Lock kept: drag 0.4–0.6 with `EXPLODE` 0.05–0.3 and no dissolve on every preset. With that much drag, gravity gives a slow terminal sag (≈ g(1−d)/d px/tick) instead of a fall, which is what makes tar read as heavy and viscous. Colour is textured per *Textured materials*: a deep full-opacity black-brown body on the outer front (`#150E0A`–`#3C2716`), small jittered sheen specks on the inner front (`TINT_DEPTH_INNER` 0.12–0.14, `blend` 0.08) and grain 0.12–0.15. Specks are warm amber on most presets, oily blue on `-thick` and oily green on aqua.
- Locales differ by mechanism: a cohesive slump that cools from warm brown to black (`Pool-terra`, low `SPREAD` and mass variance so it doesn't break into confetti); 34 big near-black globs at drag 0.6 (`-thick`); vertical strings (`CHUNK_SHAPE_STRETCH` 2.6, angle 0) peeling off with `LAUNCH_STAGGER` and sinking under weak gravity (aqua); a drag-limited implode that dulls to black as it compacts (depth); 30 globs oozing apart on weak `noise` gravity (space); horizontal smears (stretch 3, angle 90) creeping right at terminal speed with heavy blobs lagging (wave); `per_chunk` seep with a barely perceptible sag (inner).
- `Seep-inner` keeps `per_chunk` despite its mid-ramp mixes: patches of tar arriving one by one is the effect. It hits its `MAX_SIM_TICKS` cap by design (a 2–3 px sag).
- Engine limit (as Goo/Liquify): pieces don't stack, so a "thick pool" is a thin floor layer on a roomy canvas.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

405. `*.Tar-Pool-terra` — heavy tar pools slowly into a thick mass; low EXPLODE, very high DRAG, BOUNCE=0 for a dead-stop settle, black-brown tint at high TINT_OPACITY, no dissolve so the pool remains
406. `*.Tar-Pool-terra-thick` — extremely thick, slow-moving tar; very low EXPLODE, max DRAG, black-brown tint, no dissolve
407. `*.Tar-Float-aqua` — heavy tar sinks slowly rather than rising, drifting down through water; low GRAVITY_STRENGTH and high DRAG so settling takes far longer than terra, black-brown tint, no dissolve
408. `*.Tar-Collapse-depth` — tar mass crushed and compacted inward; BLAST_MODE=implode, high DRAG, black-brown tint with TINT_COLLISION=inner_wins, no dissolve so the compacted tar remains
   - **Flag:** confined: only 12/16 distinct frames
409. `*.Tar-Drift-space` — zero-gravity tar globs drift apart sluggishly; GRAVITY_STRENGTH=0, very low EXPLODE, high DRAG, black-brown tint, no dissolve
410. `*.Tar-Splatter-wave` — struck laterally, heavy tar splatters off in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, high DRAG, black-brown tint at high TINT_OPACITY_OUTER, no dissolve
411. `*.Tar-Seep-inner` — tar seeps and spreads outward from a point of corruption within; BLAST_MODE=burst with low EXPLODE and high DRAG, bidirectional black-brown tint with large TINT_DEPTH_INNER, no dissolve
