# Shadow — 7 presets (registry #186–192)

Module: `presets/shadow.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Dark fade with minimal physics — disappear into the shadows.

**Gimmick lock** (new): **Darkness, not motion**: `EXPLODE` ≤ 1, near-black tint that floods in at high opacity with some alpha bleed so the body goes dark *and* thin before dropping out; 16–30 chunks. Differs from Void (mask, zero motion) and Entropy (desaturation + black fade-colour).

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 16–30, explode 0.15–1.0; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31)

- Identity: inky violet-black (`#300060` → `#040008` arc), kept apart from Void's bright ultramarine. Edges mode, depth 3.0, alpha bleed 0.1–0.45 so the body goes thin, black fade colour, force ≤ 1, 16–30 chunks.
- `Sink-depth`/`Consume-inner` use chunk-mode violet bodies with 1 px black cores (`inner_wins`, inner ≤ 0.06). Larger inner fronts swallowed the violet and let the sprite's own colours through.
- `Drift-space` uses `noise` gravity at 0.04 (cap 90) for slow wandering.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

186. `*.Shadow-Fade-terra` — quiet disappearance into darkness; low EXPLODE and SPIN so chunks barely move, near-black bidirectional tint at high TINT_OPACITY, slow dissolve (DISSOLVE_CURVE>1) as the form sinks into shadow over many frames
187. `*.Shadow-Fade-terra-fast` — abrupt vanishing; very low EXPLODE, near-black tint with TINT_ANIM=early so darkness floods in immediately, fast dissolve (DISSOLVE_CURVE<1) as the chunks blink out
188. `*.Shadow-Seep-aqua` — shadow rises off the body like dark smoke; GRAVITY_ANGLE=0 chunks drift upward slowly, low EXPLODE, near-black tint with TINT_ALPHA_BLEED_OUTER moderate for a wispy edge, slow dissolve as it dissipates while rising
189. `*.Shadow-Sink-depth` — darkness pulls the form inward and down into itself; BLAST_MODE=implode, low EXPLODE, near-black tint with TINT_COLLISION=inner_wins so the core darkens first, moderate dissolve as it collapses into nothing
190. `*.Shadow-Drift-space` — zero-gravity dissolution into the void of shadow; GRAVITY_STRENGTH=0, very low EXPLODE so chunks barely separate, near-black bidirectional tint, slow dissolve (DISSOLVE_CURVE>1) as the form fades over many frames with minimal movement
191. `*.Shadow-Lash-wave` — struck by a wave of encroaching darkness; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks gently rightward, near-black tint at high TINT_OPACITY_OUTER, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments fade last
192. `*.Shadow-Consume-inner` — darkness spreads outward from within, swallowing the form; BLAST_MODE=burst with low EXPLODE so motion stays subtle, bidirectional tint with large TINT_DEPTH_INNER near-black core spreading to a paler outer edge, DISSOLVE_PATTERN=centrifugal as the shadow consumes the chunks from the center out
