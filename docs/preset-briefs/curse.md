# Curse — 7 presets (registry #433–439)

Module: `presets/curse.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Slow-spreading magical corruption from within; green-black.

**Gimmick lock** (revised in Stage 3): **Corruption from within**: vivid instant green with a black heart in every piece (inner-favoured `blend`), spreading outward through a slow `centripetal` dissolve with a black fade; low chunk count (10–18), very low `EXPLODE`. (Was: `inner_wins` + `linear`/`late` ramp; see *Stage 3 result*.)

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 12–20, explode 0.1–1.0; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 5a)

- **Lock revised:** an `inner_wins` inner front paints the core at falling opacity straight onto the sprite, so the ring at its cutoff showed the raw sprite (pale and peach rings), and the `linear`/`late` ramp turned the green into mud. New lock: **corruption from within**: a vivid instant hex-green body (`#00D070`–`#80FF20`, opacity 1.0) with a 1–3 px black heart per piece via an inner-favoured `blend` (`TINT_BLEND` 0.05, no sprite ring). The spread is a slow **`centripetal` dissolve with a pure-black fade**: at 10–18 big chunks it hollows each piece from its heart outward as a black band, leaving black husks or rings. The slow pacing moved from the tint ramp to `DISSOLVE_CURVE` 1.4–2.0. Low chunk count and very low `EXPLODE` kept.
- Locales differ by motion and stagger: slow slump (terra); 12 pieces darkening to deep green as they sag, few flakes left (`-deep`); translucent emerald pieces breaking away one at a time and rising (aqua, `LAUNCH_STAGGER`); a drag-limited implode into a knot of black shells (depth); turning, drifting rings (space); a black front rolling in from the right after the pieces are shoved there (wave, `directional` 90 — the one preset whose spread is a sweep, not hearts); 10 big pieces quivering on weak `noise` gravity and hollowing one at a time (inner, stagger 0.7).
- **Fix applied:** `Sunder-wave` uses `DISSOLVE_DIRECTION=90` (trailing fragments decay last, as the brief wanted) and a low-force `explode` pushed by 90° gravity. `Origin-inner` uses `explode`, not `burst`.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

433. `*.Curse-Corrupt-terra` — a curse spreads slowly from within before the body finally falls apart; very low EXPLODE and SPIN, low CHUNKS, green outer to black inner bidirectional tint with TINT_COLLISION=inner_wins, TINT_ANIM=linear so corruption visibly spreads over frames, moderate dissolve as the cursed form crumbles
434. `*.Curse-Corrupt-terra-deep` — deeper, more consuming corruption; very low EXPLODE, green-black tint with TINT_DEPTH_INNER large and TINT_COLLISION=inner_wins, slow dissolve (DISSOLVE_CURVE>1) as the curse fully consumes the form
435. `*.Curse-Seep-aqua` — corruption seeps outward and rises as a dark bloom in water; GRAVITY_ANGLE=0 chunks rise slowly, green-black tint with TINT_COLLISION=inner_wins and high TINT_ALPHA_BLEED_OUTER, slow dissolve as it disperses while rising
436. `*.Curse-Collapse-depth` — the cursed form collapses inward as corruption consumes it; BLAST_MODE=implode, low CHUNKS, green-black tint with TINT_COLLISION=inner_wins, moderate dissolve as it caves into corrupted remains
437. `*.Curse-Drift-space` — zero-gravity cursed fragments drift apart, corruption still spreading; GRAVITY_STRENGTH=0, very low EXPLODE, low CHUNKS, green-black bidirectional tint with TINT_COLLISION=inner_wins, slow dissolve (DISSOLVE_CURVE>1) over many frames
438. `*.Curse-Sunder-wave` — struck laterally, the corrupted form breaks apart in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, low CHUNKS, green-black tint with TINT_COLLISION=inner_wins, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments decay last
439. `*.Curse-Origin-inner` — the curse's true origin point at the core, corruption radiating outward; BLAST_MODE=burst with very low EXPLODE, bidirectional tint with large TINT_DEPTH_INNER black core spreading to green outer edge, TINT_COLLISION=inner_wins, DISSOLVE_PATTERN=centrifugal as corruption consumes the chunks from the center out
