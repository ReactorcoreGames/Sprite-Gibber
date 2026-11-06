# Sand — 7 presets (registry #287–293)

Module: `presets/sand.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Crumble into particles; beige.

**Gimmick lock** (new): **Granular pour**: very high chunk counts (200+), low `EXPLODE`, gravity builds a pile; dissolve only takes the finest grains (`DISSOLVE_MIN_PCT` ≥ 0.3). Differs from Ash (dark, residue) and Crush (powder implode).

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 180–280, explode 0.35–2.4; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 3b)

- Lock kept. Golden sand (`#D8B068`, damp `#B48A4C`) flat on the all-border grains, sparse dark grain specks (`#94682E`) at the cores, `TINT_GRAIN` 0.25–0.3, saturation +0.1. Dissolve thins grains (`chunks`/`random`/`noise`, min 0.3–0.6) with no fade colour, so the remaining sand keeps its colour.
- Locales: `Pour-terra-fine` trickles out grain by grain (`LAUNCH_STAGGER` 0.15, 300 chunks); `Scatter-aqua` translucent silt cloud rising (bleed 0.3); `Collapse-depth` is a `vortex` sinkhole draining from the centre (`centripetal` dissolve); `Drift-space` `burst` cloud; `Blast-wave` dune banked against the right wall.
- **Fix applied:** `Blast-wave` uses `DISSOLVE_DIRECTION=90` (leading grains thin first, trailing grains last, as the brief intended; its 270 predates the session-3a correction).
- Engine limits: grains don't stack, so "builds a pile" ends as a 1–3 px floor layer; `Erode-inner` is a 1-tick sim by design (the outside-in `centrifugal` dissolve and the damp → dry colour arc carry it).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

287. `*.Sand-Crumble-terra` — standard sand crumble; high CHUNKS, low-moderate EXPLODE, beige tint at moderate TINT_OPACITY, moderate dissolve as the finest grains disperse and fade
288. `*.Sand-Pour-terra-fine` — fine sand pouring apart; very high CHUNKS, low EXPLODE so grains trickle rather than scatter, beige tint, fast dissolve (DISSOLVE_CURVE<1) as grains vanish quickly
289. `*.Sand-Scatter-aqua` — sand disperses into the water as a drifting cloud; GRAVITY_ANGLE=0 chunks rise slowly, high CHUNKS, beige tint with TINT_ALPHA_BLEED_OUTER high for a diffusing cloud, slow dissolve (DISSOLVE_CURVE>1) as it disperses while rising
290. `*.Sand-Collapse-depth` — sand structure collapses inward into a compact mound; BLAST_MODE=implode, high CHUNKS, beige tint with TINT_COLLISION=inner_wins, moderate dissolve as the mound settles and the dust fades
   - **Flag:** wide: only 14/16 distinct frames
291. `*.Sand-Drift-space` — zero-gravity sand grains scatter and drift; GRAVITY_STRENGTH=0, high CHUNKS, low EXPLODE, beige tint, slow dissolve (DISSOLVE_CURVE>1) as grains fade over many frames
292. `*.Sand-Blast-wave` — struck laterally, sand sprays off in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, very high CHUNKS, beige tint at high TINT_OPACITY_OUTER, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing grains fade last
293. `*.Sand-Erode-inner` — erosion spreads outward from a weak point within, sand sloughing off; BLAST_MODE=burst with moderate EXPLODE, bidirectional tint with large TINT_DEPTH_INNER beige core, DISSOLVE_PATTERN=centrifugal as grains disperse outward from center
