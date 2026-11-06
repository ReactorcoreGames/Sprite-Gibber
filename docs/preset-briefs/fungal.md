# Fungal — 7 presets (registry #412–418)

Module: `presets/fungal.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Colonised by something growing; pale/purple.

**Gimmick lock** (kept): `TINT_NOISE`-driven blob/colony growth, purple palette, slower `linear`/`late` pacing than Plague.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 35–60, explode 0.2–2.4; blast: explode 3, burst 2, implode 1, horizontal_split 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 5a)

- Lock kept: `TINT_NOISE` 0.7–1.0 with jitter 0.8–1.0 at **12–45 chunks**, which is big enough for the noise-warped cutoff to leave real colony blotches (at 100+ chunks noise does nothing). Saturated purples (`#5C1088`–`#B070E8`) with pale lilac mould edges or caps, grain 0.15–0.18 and a deep-purple rot fade (`#3A0A52`). Kept apart from Plague (green body + red rash arc) by palette and pacing.
- Pacing stays slow as the lock asks: `linear` on terra/depth/space, `late` on wave and inner, `early` only on `-fast`, and an instant lilac → violet arc on aqua (its `linear` ramp left salmon pieces on the lion). The slow ramps pass through mauve on the warm lion; that reads as fungus, not mud, because the fronts are full-opacity and deep.
- Mechanics per locale: slump and patchy crumble (terra); burst with pale caps (`-fast`); clumps rising unevenly and thinning from the top (aqua); a drag-limited implode with each lump hollowed by a per-chunk `centripetal` dissolve (depth; centripetal gravity overlapped 36 chunks into a dot); big chunks breaking off one at a time with `LAUNCH_STAGGER` (space); a late bloom on the pile against the right wall (wave); 12 colonies with dark `inner_wins` hearts under pale rims, eroded from their rims by `centrifugal` (inner, which works at 12 big chunks), quivering on weak `noise` gravity.
- **Fix applied:** `Rupture-wave` uses `DISSOLVE_DIRECTION=90` (the brief wanted the trailing matter to decay last, so the leading side goes first) and a low-force `explode` pushed by 90° gravity instead of `horizontal_split`.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

412. `*.Fungal-Colonize-terra` — fungal growth slowly colonizes the body before it falls apart; low EXPLODE and SPIN, pale outer to purple inner bidirectional tint, TINT_ANIM=linear so colonization visibly spreads over frames, TINT_NOISE moderate for blotchy growth patches, moderate dissolve as colonized tissue crumbles
413. `*.Fungal-Bloom-terra-fast` — rapid fungal overgrowth and rupture; moderate EXPLODE, purple tint at high TINT_OPACITY with TINT_NOISE high, TINT_ANIM=early so growth floods in immediately, moderate dissolve
414. `*.Fungal-Spread-aqua` — fungal spores disperse upward through water; GRAVITY_ANGLE=0 chunks rise, pale-purple tint with TINT_NOISE moderate for blotchy colony texture and TINT_ALPHA_BLEED_OUTER high, slow dissolve (DISSOLVE_CURVE>1) as it disperses while rising
415. `*.Fungal-Collapse-depth` — colonized mass collapses inward as the growth consumes it; BLAST_MODE=implode, purple tint with TINT_NOISE moderate for blotchy colony texture, TINT_COLLISION=inner_wins, moderate dissolve as it caves into a fungal mass
416. `*.Fungal-Drift-space` — zero-gravity colonized fragments drift apart, spores trailing; GRAVITY_STRENGTH=0, low EXPLODE, pale-purple bidirectional tint with TINT_NOISE and TINT_JITTER pushed higher for a blotchier drifting colony pattern, slow dissolve (DISSOLVE_CURVE>1) over many frames
417. `*.Fungal-Rupture-wave` — struck laterally, colonized tissue ruptures in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, purple tint at high TINT_OPACITY_OUTER with moderate TINT_NOISE for blotchy colony texture, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing matter decays last
418. `*.Fungal-Colony-inner` — fungal colonization originates from a single spore at the core and spreads outward; BLAST_MODE=burst with low EXPLODE, bidirectional tint with large TINT_DEPTH_INNER deep-purple core spreading to pale outer edge, TINT_NOISE high, DISSOLVE_PATTERN=centrifugal as growth consumes the chunks from the center out
