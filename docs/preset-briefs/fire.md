# Fire — 18 presets (registry #1–18)

Module: `presets/fire.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Burning and extreme heat: ignition, charring, embers, flash-burns, fire jets. Orange/yellow identity.

**Gimmick lock** (new): Every preset tells a **colour arc** with `TINT_COLOR_OUTER_END`/`INNER_END` (ignite → char black, or ignite → white-hot), and every dissolving preset gets a char or ember `DISSOLVE_FADE_COLOR` (white for `Steam-aqua`, where the fire becomes steam). Fire consumes rather than shatters: chunk counts stay low-to-mid (8–100), `TINT_ANIM` mostly `early`.

**Locales present:** terra ×8, aqua ×2, depth, space ×3, wave, inner ×3.

**Why these locales:** All six — fire genuinely means something different falling (embers settle), rising (steam/scorch), compressed (magma), weightless (flares, vortex), blown sideways (jet) and self-igniting (inner). terra carries 8 intensity/style variants.

**Current state (2026-10-30):** chunks 8–100, explode 0.1–7.0; blast: explode 14, shatter 3, horizontal_split 1; gravity: directional 16, centripetal 1, vortex 1; tint on 18/18, dissolve 17/18, mask 2/18, stretched chunks 0/18.

**Stage 3 notes:**

- `Fire-Orbit-inner` and `Fire-Vortex-space` use orbital/vortex — check `off=` in metrics; orbital has no wall containment.
- With 18 presets, make sure the terra family reads as distinct styles on the sheet (burn / smoulder / inferno / char / ember / flash-burn / small blast / big blast), not one recipe at eight strengths.

## Stage 3 result (2026-10-30)

- Rebuilt with full-opacity, deep fronts and saturated hexes (`#FF2E00`, `#FFD000` …); every preset still carries a colour arc. The terra family reads as distinct styles: burn (top-down burn-off), smoulder (10 big red-hot husks), inferno (90 chunks, white-hot), char (coal body + glowing cracks), ember shower (no dissolve), flash burn (instant white + black flecks), small blast (yellow rims eating in), big blast (100 chunks).
- Avoid arcs that end on white unless the white should dominate quickly: the RGB lerp makes mid-frames pastel pink (`Blast-wave` was fixed this way). `TINT_COLOR_ANIM_CURVE` < 1 delays the colour change, > 1 rushes it.
- `Orbit-inner` (orbital) needed strength 0.15 / drag 0.25 / 60 ticks to stay on canvas; `Flare-space` explode 2.2 / drag 0.12 so pieces don't jam the walls.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

1. `*.Fire-Burn-terra` — standard immolation; moderate chunks settle downward, orange-to-dark-ash tint (outer: orange, inner: dark grey), mid physics, mild dissolve fade to black
2. `*.Fire-Burn-terra-low` — slow smoldering burn; fewer large chunks, gentle settle, deep red outer tint bleeding to dark char inner, slow dissolve
3. `*.Fire-Burn-terra-high` — intense inferno; many small chunks, fast violent settle, bright yellow outer to near-black inner, aggressive dissolve fade to black
4. `*.Fire-Char-terra` — post-fire charring; chunks are nearly static (very low EXPLODE), dark grey-to-black tint throughout, chunks crumble with heavy dissolve at end
5. `*.Fire-Ember-terra` — gentle ember shower; low chunk count, very low EXPLODE, high drag so chunks drift slowly downward, warm orange-to-dim-red tint, no dissolve
6. `*.Fire-Flash-Burn-terra` — sudden surface ignition then instant collapse; TINT_ANIM=early so tint peaks in the first frames, then fast-out DISSOLVE_CURVE so pixels drop rapidly, minimal EXPLODE, near-white outer tint
7. `*.Fire-Explode-terra-low` — small contained burst; few large chunks with moderate scatter, orange tint, brief dissolve, low spin
8. `*.Fire-Explode-terra-high` — violent detonation; many tiny chunks, extreme EXPLODE and SPIN, bright yellow outer to deep orange inner, fast dissolve fade to black
9. `*.Fire-Scorch-aqua` — fire in a buoyant medium; GRAVITY_ANGLE=0 so chunks rise upward, bidirectional tint with high TINT_ALPHA_BLEED_INNER for translucent center, heavy dissolve as chunks evaporate on ascent
10. `*.Fire-Steam-aqua` — fire extinguished by water, converting to steam; chunks rise fast, dissolve rapidly into nothing, near-white tint replacing orange, very high dissolve rate
11. `*.Fire-Magma-depth` — superheated implosion; chunks implode inward (BLAST_MODE implode), deep red-to-orange inner tint radiating outward from center, heavy physics, slow settle at core
12. `*.Fire-Drift-space` — zero-gravity ember scatter; chunks drift in all directions with no settle, warm orange tint, slow gentle dissolve as embers cool over frames
13. `*.Fire-Flare-space` — solar flare eruption; extreme EXPLODE into zero gravity, bright white-yellow outer to orange inner, chunks scatter far and dissolve rapidly, high SPIN
14. `*.Fire-Blast-wave` — directional fire jet or shaped-charge detonation; GRAVITY_ANGLE=90 pulls chunks rightward, BLAST_MODE=horizontal_split biases velocity sideways, orange-to-yellow tint, DISSOLVE_PATTERN=directional with DISSOLVE_DIRECTION=270 (trailing left edge dissolves last)
15. `*.Fire-Combust-inner` — spontaneous internal combustion; fire originates at center (inner locale), deep red-orange inner tint pushes outward to yellow border, chunks scatter from core, moderate physics
16. `*.Fire-Ignite-inner` — gentle self-ignition spreading from within; slow chunk scatter, warm orange inner tint spreading gradually outward with low jitter, soft dissolve toward edges
17. `*.Fire-Vortex-space` — fire caught in a vortex; GRAVITY_MODE=vortex so chunks burst outward then arc inward in a tightening spiral, deep-red outer to hot-orange inner bidirectional tint, centrifugal dissolve as they spiral in
18. `*.Fire-Orbit-inner` — dying fire; GRAVITY_MODE=orbital so chunks hang in slow orbit around the sprite center barely drifting outward, orange-to-red inner tint smolders from core, noise dissolve as embers cool
