# Squeeze — 4 presets (registry #457–460)

Module: `presets/squeeze.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** x_split into four quarters with very low force and high drag — pressure, not detonation.

**Gimmick lock** (kept): `x_split`, very low `EXPLODE`, high drag, no tint, no dissolve.

**Locales present:** terra ×2, depth, space.

**Why these locales:** terra, depth, space.

**Current state (2026-10-30):** chunks 8–14, explode 0.12–1.5; blast: x_split 3, implode 1; gravity: directional 3, centripetal 1; tint on 4/4 (4 only via the default), dissolve 0/4, mask 0/4, stretched chunks 0/4.

**Stage 3 notes:**

- **Tint is currently on** (default red wound tint) — set `TINT_DEPTH_OUTER=0`.
- `x_split` pairs naturally with `CHUNK_BIAS="quadrants"`.

## Stage 3 result (2026-10-31, session 5b)

- Lock kept: `x_split` + `CHUNK_BIAS="quadrants"` on every preset (the brief's `implode` for `Crush-depth` broke the lock and was replaced), very low `EXPLODE` (0.25–0.6), high drag (0.35–0.5), `TINT_DEPTH_OUTER=0` (red tint gone), `DISSOLVE=False`.
- Pressure, not detonation: high drag + a weak force gives slow terminal motion (the 5a Tar note), so the quarters ooze apart and sag (`Vice-terra`, gravity 0.2 at drag 0.38), and hairline X cracks open by a pixel or two (`-tight`, 4 chunks). `Crush-depth` uses weak centripetal gravity (0.12, drag 0.4) after a ramp, so the quarters crack open and creep back into a compressed knot (the lion is pulled up to mid-canvas and squeezed thin). `Drift-space` eases the quarters apart with almost no spin.
- `x_split` also cuts at the canvas centre, so on the bottom-anchored lion the "X" is really a left/right split moving down. Sims that hit `MAX_SIM_TICKS` are drag-limited creeps, by design.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

457. `*.Squeeze-Vice-terra` — split into quarters by an x-shaped cut, very low EXPLODE and high DRAG keep the pieces close together rather than scattering; BLAST_MODE=x_split, no tint, no dissolve
458. `*.Squeeze-Vice-terra-tight` — tighter squeeze, pieces stay even closer together and barely separate at all; BLAST_MODE=x_split, near-zero EXPLODE, even higher DRAG, no dissolve
459. `*.Squeeze-Crush-depth` — the squeeze intensifies past the split into a full crushing implosion; BLAST_MODE=implode, GRAVITY_MODE=centripetal, no dissolve so the crushed mass remains
460. `*.Squeeze-Drift-space` — zero-gravity x-split squeeze, quarters held close by drag but drifting slowly apart with no settle; BLAST_MODE=x_split, GRAVITY_STRENGTH=0, no dissolve
