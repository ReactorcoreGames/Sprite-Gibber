# Photon — 7 presets (registry #172–178)

Module: `presets/photon.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** White-light vaporisation into many light particles — the gentle one.

**Gimmick lock** (new): **Light motes**: very high chunk counts (150+) of tiny pieces, pure-white crisp tint (energy row: opacity 0.85–1.0, no bleed except glow fringes), low `EXPLODE` (gentle dispersal), particles wink out via `chunks`/`random` dissolve. Photon is soft; Flash is violent.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 120–220, explode 0.2–1.8; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31)

- Crisp white motes (edges mode, no bleed: alpha bleed turned white into grey over the background), 150–260 chunks, low force. Each mote flashes saturated cyan (`DISSOLVE_FADE_COLOR` `#00E8FF`) as it winks out via `random`/`chunks` dissolve. This is the colour identity that separates Photon from Flash.
- `Drift-space` uses `burst` so motes spread above the lion too; `Ignite-inner` uses chunk-mode cyan bodies with 1 px white hearts.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

172. `*.Photon-Vaporize-terra` — standard light-particle vaporization; high CHUNKS so fragments read as motes, moderate EXPLODE, pure-white tint at high TINT_OPACITY_OUTER, TINT_ALPHA_BLEED_OUTER high for a glowing fringe, fast dissolve (DISSOLVE_CURVE<1) as particles wink out
173. `*.Photon-Vaporize-terra-dense` — denser particle breakdown; very high CHUNKS, lower EXPLODE so motes linger, pure-white bidirectional tint with high TINT_OPACITY_INNER, slower dissolve (DISSOLVE_CURVE close to 1) so the particle field is visible longer
174. `*.Photon-Scatter-aqua` — light particles drift upward and disperse; GRAVITY_ANGLE=0 chunks rise, high CHUNKS, low SPIN, pure-white tint with TINT_ALPHA_BLEED_OUTER high, slow dissolve (DISSOLVE_CURVE>1) as motes fade while ascending
175. `*.Photon-Collapse-depth` — light crushed into a single vaporizing point; BLAST_MODE=implode, high CHUNKS, pure-white tint with TINT_DEPTH_OUTER large so the whole form glows before vanishing, fast dissolve as it collapses to nothing
176. `*.Photon-Drift-space` — zero-gravity photon dispersal; GRAVITY_STRENGTH=0, high CHUNKS, low EXPLODE so particles drift gently outward, pure-white bidirectional tint with TINT_NOISE low for an even glow, slow dissolve (DISSOLVE_CURVE>1) as the field thins over many frames
177. `*.Photon-Beam-wave` — struck by a lateral beam, vaporizing directionally; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, pure-white tint at high TINT_OPACITY_OUTER, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments vaporize last
178. `*.Photon-Ignite-inner` — vaporization originates from the sprite's core and radiates outward; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER bright-white core fading to a paler outer edge, DISSOLVE_PATTERN=centrifugal as the light consumes the chunks from the center out
