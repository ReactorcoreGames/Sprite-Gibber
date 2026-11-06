# Ion — 7 presets (registry #330–336)

Module: `presets/ion.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Break into small rough pieces that dissolve and fade; cyan.

**Gimmick lock** (revised in Stage 3): dissolve on in every preset, irregular Voronoi (no stretch), full-opacity saturated cyan with saturated blue/violet fade colours — the dissolve carries the weight. Direct contrast to Laser. (Was: a *modest* cyan tint, which mixed to grey-green over warm sprites; see *Stage 3 result*.)

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 60–100, explode 0.2–3.0; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 4a)

- Lock kept (dissolve on everywhere, round unstretched pieces), but the tint is vivid rather than "modest": the old partial-opacity cyan went grey-green over the lion. Every preset is full-opacity cyan `#00F0FF`, either flat (`-fast`, `Burst-inner`, `Sunder-wave`) or two-tone with jittered deep-blue `#0050FF` core specks (`Disperse-terra`, `Float-aqua`, `Drift-space`; blend 0.15). `Collapse-depth` has 1 px white sparks (`inner_wins`). Fade colours are saturated blues/violet (`#0030FF`–`#00A0FF`, `#8000FF`), strength 0.9–0.95, so the dissolve carries an electric flicker instead of washing out.
- `TINT_MODE="edges"` was tried for a "modest" cyan rim and dropped: its falling opacity mixes orange lion + cyan into grey.
- Locales differ by dissolve mechanic: `noise` patches (terra), a `random` near-instant blink (`-fast`, curve 0.45), a top-down `gravity_aligned` sweep while rising (aqua), centripetal pull (depth), slow `noise` wink-out with a cyan → blue/violet arc (space), a leading-edge `directional` sweep (wave), a flat cyan → blue flood fizzing away in place (inner).
- **Fix applied:** `Sunder-wave` uses `DISSOLVE_DIRECTION=90` (the brief's 270 removed the trailing side first). The `centripetal`/`centrifugal` patterns on depth/inner work per chunk (see the workflow doc), so their descriptions no longer promise a sprite-wide hollowing.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

330. `*.Ion-Disperse-terra` — ionizing breakdown into small rough pieces that crumble and fall, fading as they go; high CHUNKS, moderate EXPLODE, cyan tint at moderate opacity, DISSOLVE_CURVE around 1.3 so fragments fade steadily as they settle
331. `*.Ion-Disperse-terra-fast` — rapid ionization, fragments crumble and fade almost immediately; high CHUNKS, cyan tint, fast dissolve (DISSOLVE_CURVE<0.6) as ionized fragments vanish in the first few frames
332. `*.Ion-Float-aqua` — ionized fragments rise and fade out while suspended in water; GRAVITY_ANGLE=0, high CHUNKS, cyan tint with elevated TINT_ALPHA_BLEED_OUTER for a diffusing look, slow dissolve (DISSOLVE_CURVE>1.5) as they fade while still rising
333. `*.Ion-Collapse-depth` — ionized structure collapses inward as it fades, chunks crumbling toward center; GRAVITY_MODE=centripetal, BLAST_MODE=implode, high CHUNKS, cyan tint with inner_wins collision, DISSOLVE_PATTERN=centripetal so the fading tracks the inward collapse
334. `*.Ion-Drift-space` — zero-gravity ionized fragments drift apart slowly and fade over many frames; GRAVITY_STRENGTH=0, high CHUNKS, low EXPLODE, cyan tint, slow dissolve (DISSOLVE_CURVE>1.8) so fragments linger before fading
335. `*.Ion-Sunder-wave` — struck laterally by an ionizing field, fragments blown sideways and fading in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, cyan tint at higher opacity, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments fade last
336. `*.Ion-Burst-inner` — ionization radiates outward from within, chunks barely separating while fading; BLAST_MODE=burst, EXPLODE tiny, GRAVITY_STRENGTH=0, bidirectional cyan tint with large TINT_DEPTH_INNER and inner_wins collision, DISSOLVE_PATTERN=centrifugal so the fade radiates outward from the ignition point
