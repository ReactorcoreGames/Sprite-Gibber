# Wither — 7 presets (registry #242–248)

Module: `presets/wither.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Organic decay by draining colour; desaturated.

**Gimmick lock** (kept): strongly negative `TINT_SATURATION_SHIFT` with minimal tint colour — desaturation is the effect.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 20–35, explode 0.2–1.4; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

**Stage 3 notes:**

- `TINT_SATURATION_SHIFT` fades in with tint opacity, so a near-zero tint depth also limits the desaturation reach — check the sheet before assuming 'minimal tint' is enough.

## Stage 3 result (2026-10-31, session 3a)

- Lock kept: `TINT_SATURATION_SHIFT` −1.0 everywhere. The saturation shift hits every pixel (not just tinted ones), but greying alone does nothing to the near-white bear, so the "minimal tint" is a mottled dark crack line (`#2E2C2A`, depth 0.06–0.14, jitter 0.9, opacity 0.85) plus `TINT_GRAIN` 0.15 — value texture on the husk.
- Here a gradual ramp is the point (draining colour), so locales differ by drain timing: `Drain-terra` `per_chunk` (pieces grey out one by one), `-slow` `linear` with `LAUNCH_STAGGER`, `Seep-aqua` `early` + translucent (colour leaches into the water), `Collapse-depth`/`Sap-wave` `linear`/`early`, `Drift-space` `late`, `Curse-inner` `instant` (colour gone at once, then hollows from the core).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

242. `*.Wither-Drain-terra` — life drains away leaving a desaturated husk; low EXPLODE and SPIN, TINT_SATURATION_SHIFT strongly negative, minimal tint color (low TINT_DEPTH_OUTER) so desaturation does the work, mild dissolve as the husk crumbles
243. `*.Wither-Drain-terra-slow` — gradual withering over the full animation; very low EXPLODE, TINT_SATURATION_SHIFT negative with TINT_ANIM=linear so color drains progressively, slow dissolve (DISSOLVE_CURVE>1) as it crumbles over many frames
244. `*.Wither-Seep-aqua` — color and vitality leach out into the water; GRAVITY_ANGLE=0 chunks rise slowly, TINT_SATURATION_SHIFT negative, mild dissolve as the bleached husk disperses while floating
245. `*.Wither-Collapse-depth` — withered form collapses inward, drained of all color; BLAST_MODE=implode, TINT_SATURATION_SHIFT strongly negative, mild dissolve as it caves into a grey husk
246. `*.Wither-Drift-space` — zero-gravity withering, fragments desaturate and drift; GRAVITY_STRENGTH=0, low EXPLODE, TINT_SATURATION_SHIFT negative, mild dissolve (DISSOLVE_CURVE close to 1) as fragments fade over many frames
247. `*.Wither-Sap-wave` — struck laterally, vitality saps away in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, TINT_SATURATION_SHIFT negative, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments wither last
248. `*.Wither-Curse-inner` — a withering curse spreads outward from within, draining color from the core out; BLAST_MODE=burst with low EXPLODE, TINT_SATURATION_SHIFT strongly negative, DISSOLVE_PATTERN=centrifugal as the withering consumes the chunks from the center out
