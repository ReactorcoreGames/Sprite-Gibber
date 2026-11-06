# Rust — 7 presets (registry #273–279)

Module: `presets/rust.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Oxidation and crumble with partial dissolve; orange-brown.

**Gimmick lock** (new): **Oxidation arc**: colour animation raw → rust brown (`TINT_COLOR_*_END`) on every preset + partial dissolve (`DISSOLVE_MIN_PCT` 0.3–0.6, `noise` pattern) so corroded fragments remain.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 30–45, explode 0.2–2.4; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 3b)

- Lock kept. Recipe: **steel on the deep outer front** (`#848C94`) with jittered, noisy rust spots from each core (`#8A3A14`, depth 0.14–0.2, `TINT_NOISE` 0.7), both arcing to rust (steel → `#B8501C` orange-brown, spots → `#5C2410`), grain 0.25. The first try put the rust spots on the outer front and was brown from frame 1: at ~30 chunks about 60 % of pixels are chunk-border pixels, so the outer colour dominates whatever its depth. Dissolve fade is bright rust `#D06424` (flakes flash orange as they peel, and survivors end orange-brown).
- `Crumble-terra-fast` rushes the arc (curve 2.5) and dissolves fast; `Oxidize-terra` is a slow, even arc. `Seep-aqua` flat flakes (stretch at 90°) float up; `Collapse-depth` gives way piece by piece (`LAUNCH_STAGGER` 0.12 into centripetal); `Drift-space` flakes wander on `noise` gravity; `Spread-inner` hollows each piece from the core (`centripetal` dissolve) into orange shells.
- **Fix applied:** `Sunder-wave` uses `DISSOLVE_DIRECTION=90` (leading side flakes first, trailing scraps linger). The brief's 270 predates the session-3a correction and would have removed the trailing side first.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

273. `*.Rust-Oxidize-terra` — gradual oxidation and crumble; low EXPLODE and SPIN, orange-brown tint with TINT_ANIM=linear as rust spreads over frames, partial dissolve (DISSOLVE_MIN_PCT moderate) so some corroded fragments remain
274. `*.Rust-Crumble-terra-fast` — rapid corrosion collapse; moderate EXPLODE, orange-brown tint at high TINT_OPACITY_OUTER, faster dissolve (DISSOLVE_CURVE<1) as the corroded shell falls away quickly
275. `*.Rust-Seep-aqua` — rusting underwater, flakes drift upward; GRAVITY_ANGLE=0 chunks rise, orange-brown tint with TINT_ALPHA_BLEED_OUTER moderate, slow dissolve (DISSOLVE_CURVE>1) as rust flakes disperse while floating
276. `*.Rust-Collapse-depth` — corroded structure collapses inward under pressure; BLAST_MODE=implode, orange-brown tint with TINT_COLLISION=inner_wins, partial dissolve as the weakened structure crumbles
277. `*.Rust-Drift-space` — zero-gravity rust flakes scatter slowly; GRAVITY_STRENGTH=0, low EXPLODE, orange-brown tint, partial dissolve (DISSOLVE_CURVE>1) as flakes fade over many frames
278. `*.Rust-Sunder-wave` — struck laterally, the corroded structure crumbles off in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, orange-brown tint at high TINT_OPACITY_OUTER, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments corrode last
279. `*.Rust-Spread-inner` — oxidation spreads outward from a point of corrosion within; BLAST_MODE=burst with low EXPLODE, bidirectional tint with large TINT_DEPTH_INNER deep-rust core spreading to a paler orange-brown outer edge, partial dissolve as corrosion consumes the chunks from the center out
