# Goo — 7 presets (registry #280–286)

Module: `presets/goo.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Viscous splatter, blobby numerous chunks, weak force, gooification; violet.

**Gimmick lock** (revised in Stage 3): **Rubbery slime**: very high chunk counts, translucent glossy violet (alpha bleed + gloss specks), `BOUNCE` 0.45–0.6 so blobs jiggle, low `EXPLODE`, no dissolve. (Was: high drag, which overlapped Liquify and Tar; see *Stage 3 result*.)

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 180–220, explode 0.2–1.8; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 0/7, mask 1/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 3b)

- **Lock revised:** "high drag, no dissolve, very high chunks" was indistinguishable from Liquify (`BOUNCE=0` + high drag) and Tar (maximum drag). New lock: **rubbery slime**: very high chunk counts (160–240), translucent glossy violet (`#8A20E0` body on the all-border tiny blobs, alpha bleed 0.22–0.38, `#F6DCFF` gloss specks at the blob cores, grain 0.2, saturation +0.2), and **`BOUNCE` 0.45–0.6** so blobs jiggle and hop; moderate drag; no dissolve.
- `Drip-terra-slow` drips blob by blob (`LAUNCH_STAGGER` 0.1) while pale slime deepens to violet; `Collapse-depth` is a drag-limited implode with no pull (centripetal at 200 chunks overlaps every blob into one dot); `Ooze-inner` quivers on very weak `noise` gravity while darkening. Engine limit: blobs don't stack, so floor piles are a thin puddle.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

280. `*.Goo-Splatter-terra` — viscous violet splatter; high CHUNKS, low EXPLODE so blobs ooze rather than fly, high DRAG, violet tint at high TINT_OPACITY_OUTER, no dissolve so the gooey pile remains
281. `*.Goo-Drip-terra-slow` — slow gooification, chunks sag and settle; very high CHUNKS, very low EXPLODE and high DRAG, violet tint with TINT_ANIM=linear, no dissolve
282. `*.Goo-Float-aqua` — gooey blobs rise and drift in water; GRAVITY_ANGLE=0 chunks rise slowly, high CHUNKS, low EXPLODE, violet tint with high TINT_ALPHA_BLEED_OUTER for a translucent blobby look, no dissolve
283. `*.Goo-Collapse-depth` — gooey mass collapses inward into a thick blob; BLAST_MODE=implode, low EXPLODE, violet tint with TINT_COLLISION=inner_wins, no dissolve so the collapsed blob remains
284. `*.Goo-Drift-space` — zero-gravity gooification, blobs drift apart weightlessly; GRAVITY_STRENGTH=0, high CHUNKS, very low EXPLODE, violet tint, no dissolve
285. `*.Goo-Splat-wave` — struck laterally, goo splatters off in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, high CHUNKS, low EXPLODE, violet tint at high TINT_OPACITY_OUTER, no dissolve
286. `*.Goo-Ooze-inner` — gooification spreads outward from a point of liquefaction within; BLAST_MODE=burst with low EXPLODE, bidirectional tint with large TINT_DEPTH_INNER deep-violet core spreading to a paler outer edge, high CHUNKS, no dissolve
