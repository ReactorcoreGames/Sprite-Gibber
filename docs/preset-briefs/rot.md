# Rot — 8 presets (registry #226–233)

Module: `presets/rot.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Organic decay, putrid, bloat; sickly yellow / disgusting green.

**Gimmick lock** (new): **Late putrid flood**: two-tone sickly tint that arrives late (`TINT_ANIM` `late`/`per_chunk`) with alpha bleed for slime, and a putrid `DISSOLVE_FADE_COLOR`. The rot sets in, then the body sloughs. Differs from Plague (noise blotches), Fungal (purple growth), Biodegrade (brown, dissolve-only), Wither (desaturation).

**Locales present:** terra ×3, aqua, depth, space, wave, inner.

**Why these locales:** All six; terra has putrid / bloat / heavy bloat.

**Current state (2026-10-30):** chunks 35–90, explode 0.2–3.2; blast: explode 3, burst 3, implode 1, horizontal_split 1; gravity: directional 7, centripetal 1; tint on 8/8, dissolve 8/8, mask 0/8, stretched chunks 0/8.

## Stage 3 result (2026-10-31, session 3a)

- **Lock revised:** a `late`/`per_chunk` opacity ramp spends half the animation in muddy sprite-plus-green mixes (olive on the lion, pastel on the bear). New lock: **late putrid turn** — the body is sallow, sickly flesh from frame 1 (`TINT_ANIM="instant"`, `#D8B828` body with a mottled olive rim, `TINT_GRAIN` 0.15, slime bleed 0.08–0.18), and the rot arrives late as a colour arc to bile green / sludge (`TINT_COLOR_ANIM_CURVE` 0.45 holds the start colour, then rushes), with a dark putrid fade (`#24400A`). Yellow → green never lerps through mud.
- Kept apart from Biodegrade (brown, dissolve-shaped), Plague (noise blotches, red rash) and Wither (grey) by palette *and* by the late arc. `Bloat-terra` pops its boils with `LAUNCH_STAGGER`; `Collapse-depth` and `Fester-inner` carry yellow pus / bile cores (`blend`, low `TINT_BLEND`, not `inner_wins`).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

226. `*.Rot-Putrid-terra` — standard putrid decay; low EXPLODE and SPIN, sickly-yellow outer to disgusting-green inner bidirectional tint, TINT_JITTER moderate for a mottled diseased look, moderate dissolve as the decayed matter falls apart
227. `*.Rot-Bloat-terra` — body bloats then bursts with rot; BLAST_MODE=burst, moderate EXPLODE, sickly-green tint with TINT_ANIM=late so decay color floods in just before rupture, moderate dissolve as putrid chunks scatter and decay further
228. `*.Rot-Bloat-terra-heavy` — severe bloating, violent rupture; high EXPLODE and CHUNKS, sickly yellow-green tint at high TINT_OPACITY, TINT_NOISE moderate for diseased patchiness, fast dissolve (DISSOLVE_CURVE<1) as the burst matter rapidly decays away
229. `*.Rot-Seep-aqua` — rot disperses into the water as putrid film; GRAVITY_ANGLE=0 chunks rise slowly, sickly-green tint with TINT_ALPHA_BLEED_OUTER high for a murky diffusing edge, slow dissolve (DISSOLVE_CURVE>1) as it disperses while rising
230. `*.Rot-Collapse-depth` — decayed mass collapses inward under its own putrescence; BLAST_MODE=implode, sickly-green tint with TINT_COLLISION=inner_wins, moderate dissolve as it caves into a rotten heap
231. `*.Rot-Drift-space` — zero-gravity decayed fragments drift and putrefy; GRAVITY_STRENGTH=0, low EXPLODE, sickly yellow-green bidirectional tint, slow dissolve (DISSOLVE_CURVE>1) as fragments decay over many frames
232. `*.Rot-Rupture-wave` — struck laterally, the bloated rot ruptures in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, sickly-green tint at high TINT_OPACITY_OUTER, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing matter decays last
233. `*.Rot-Fester-inner` — rot festers and spreads outward from a point of infection at the core; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER putrid-green core spreading to sickly-yellow outer edge, DISSOLVE_PATTERN=centrifugal as decay consumes the chunks from the center out
