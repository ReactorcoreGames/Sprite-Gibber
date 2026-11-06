# Biodegrade — 7 presets (registry #219–225)

Module: `presets/biodegrade.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Earthy breakdown, shrivelling; brown.

**Gimmick lock** (kept): dissolve-only decay — minimal tint, slow `DISSOLVE_CURVE` + `DISSOLVE_FADE_COLOR` toward dark soil.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 25–55, explode 0.18–1.8; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 3a)

- **Lock revised:** "minimal tint" left the raw sprite showing for most of the animation (the fade colour only appears in the few frames before each pixel drops), so nothing read as decay. New lock: **dissolve-driven decay in an earth palette** — a flat, instant moist-umber wash (`#8E4A18`, `TINT_GRAIN` 0.2–0.25) that darkens to soil (`#5A2400`) via a colour arc, never two-tone, never late; some presets add a 1 px mottled humus crack line on chunk borders. The slow dissolve and its dark-soil fade still carry the shape, and since surviving pixels also take the fade colour at the end, the residue is always soil.
- Locales differ by dissolve shape: `Shrivel-terra` `centrifugal` (clods shrink in on themselves), `Crumble-terra-fast` `chunks` (clumps pop), `Seep-aqua` `gravity_aligned` silt, `Sink-depth` `noise` into a humus lump, `Drift-space` `noise` gravity mode + per-chunk stagger, `Crumble-wave` `directional` 90 (leading side rots first), `Rot-inner` `centripetal` (hollows from the core).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

219. `*.Biodegrade-Shrivel-terra` — slow earthy breakdown, the form shrivels in place; very low EXPLODE and SPIN, brown tint with TINT_ANIM=linear building gradually, slow dissolve (DISSOLVE_CURVE>1) as it crumbles to soil over many frames
220. `*.Biodegrade-Crumble-terra-fast` — faster breakdown into earthy debris; low-moderate EXPLODE, moderate CHUNKS, minimal brown tint so dissolve carries the effect, near-linear dissolve curve with DISSOLVE_FADE_COLOR toward dark soil as the body falls apart into compost-like fragments
221. `*.Biodegrade-Seep-aqua` — decomposing matter rises and disperses in water; GRAVITY_ANGLE=0 chunks drift upward slowly, minimal brown tint, slow dissolve with DISSOLVE_FADE_COLOR toward dark soil as the matter breaks down while floating
222. `*.Biodegrade-Sink-depth` — the form collapses inward and settles into the earth; BLAST_MODE=implode, low EXPLODE, brown tint with TINT_COLLISION=inner_wins, moderate dissolve as it sinks into decay
223. `*.Biodegrade-Drift-space` — zero-gravity organic breakdown, fragments scatter slowly; GRAVITY_STRENGTH=0, low EXPLODE, minimal brown tint, slow dissolve with heavy DISSOLVE_CHUNK_STAGGER and DISSOLVE_FADE_COLOR toward dark soil so fragments decay unevenly and weightlessly over many frames
224. `*.Biodegrade-Crumble-wave` — struck laterally, the weakened form crumbles in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, minimal brown tint, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 with DISSOLVE_FADE_COLOR toward dark soil so trailing fragments decay last
225. `*.Biodegrade-Rot-inner` — decay spreads outward from a point of rot at the core; BLAST_MODE=burst with low EXPLODE so motion stays subtle, bidirectional tint with large TINT_DEPTH_INNER dark-brown core spreading to a paler outer edge, DISSOLVE_PATTERN=centrifugal with DISSOLVE_FADE_COLOR toward dark soil as decay consumes the chunks from the center out
