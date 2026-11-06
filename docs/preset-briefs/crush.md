# Crush — 7 presets (registry #302–308)

Module: `presets/crush.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Break into powder, no tint.

**Gimmick lock** (new): **Compression to powder**: implode/centripetal motion, high chunk counts, dissolve as the powder disperses; no tint.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 80–150, explode 0.15–1.5; blast: implode 6, horizontal_split 1; gravity: directional 6, centripetal 1; tint on 0/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

**Stage 3 notes:**

- Six of seven are `BLAST_MODE="implode"` with directional gravity — implode turns edge containment off, so pieces converge, cross and fall to the floor. Decide per preset whether that's the read or whether it needs centripetal.

## Stage 3 result (2026-10-31, session 4a)

- Lock kept: every preset is an `implode` (plus `centripetal` on `Compact-depth`), 140–260 chunks, dissolve on, no tint, light `TINT_GRAIN` (0.1–0.2) for a powdery look. Locales differ by where the converging powder goes: `Powder-terra` slumps into a dusty floor heap (min 0.3 residue); `-fine` converges fast with low drag so the dust sprays through the middle before raining down and blowing away (`random`, curve 0.55); `Disperse-aqua` squeezes into a clot that lifts as a cloud thinning from the top (`gravity_aligned`, mass variance 1.0); `Compact-depth` is a slow overdamped centripetal knot (strength 0.3, drag 0.3; the confirmed 0.8/0.24 collapsed to a dot by frame 4); `Drift-space` has almost no drag, so the powder passes through the centre and drifts out the far side (it leaves the confined canvas only after it has dissolved); `Pulverize-wave` is carried right at 90° with mass variance 1.0; `Implosion-inner` is a drag-limited implode that squeezes slightly and stops, then hollows out in `noise` patches.
- **Fix applied:** `Pulverize-wave` uses `DISSOLVE_DIRECTION=90` (leading side first; the brief's 270 predates the session-3a correction).
- `Implosion-inner` no longer uses `centripetal` dissolve: that pattern measures from each chunk's own centroid (see the workflow doc), so at 220 chunks it was uniform speckle, not a hollowing core.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

302. `*.Crush-Powder-terra` — crushed down to fine powder, no tint; BLAST_MODE=implode, high CHUNKS, low EXPLODE so fragments compress rather than scatter, moderate dissolve as the powder disperses
303. `*.Crush-Powder-terra-fine` — ground to very fine dust; very high CHUNKS, BLAST_MODE=implode, fast dissolve (DISSOLVE_CURVE<1) as the dust vanishes quickly
304. `*.Crush-Disperse-aqua` — crushed powder drifts upward and disperses in water; GRAVITY_ANGLE=0 chunks rise, high CHUNKS, BLAST_MODE=implode, slow dissolve (DISSOLVE_CURVE>1) as the cloud disperses while rising
305. `*.Crush-Compact-depth` — extreme compression crushes the form to almost nothing; BLAST_MODE=implode, very high CHUNKS, very low EXPLODE, fast dissolve as the compacted mass crumbles away
306. `*.Crush-Drift-space` — zero-gravity crushed powder scatters slowly; GRAVITY_STRENGTH=0, high CHUNKS, low EXPLODE, slow dissolve (DISSOLVE_CURVE>1) as powder fades over many frames
307. `*.Crush-Pulverize-wave` — struck laterally and pulverized in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, high CHUNKS, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing powder disperses last
308. `*.Crush-Implosion-inner` — crushing force originates from a point within and compresses outward then collapses; BLAST_MODE=implode, very high CHUNKS, DISSOLVE_PATTERN=centripetal as the powder is drawn inward and vanishes
