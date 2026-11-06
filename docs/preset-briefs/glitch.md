# Glitch — 7 presets (registry #383–389)

Module: `presets/glitch.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Pixel corruption; chaotic chunks, noise dissolve, jarring physics; cyan/magenta.

**Gimmick lock** (kept): high `CHUNK_MASS_VARIANCE` (0.5+), high `TINT_NOISE`, `DISSOLVE_PATTERN="noise"` everywhere — corruption never resolves cleanly.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 40–70, explode 0.2–6.0; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 7/7, mask 0/7, stretched chunks 0/7.

## Stage 3 result (2026-10-31, session 4b)

- Lock kept: mass variance 0.8–1.0, `TINT_NOISE` 0.9–1.0, `noise` dissolve everywhere, and a residue or unsettled end on every preset. The colour is vivid: bidirectional full-opacity cyan `#00F0FF` on a noise-warped outer front, `outer_wins` over a deep magenta `#FF00C8` body, `instant`, and a saturated fade flash (magenta, or cyan on the magenta presets). At 35–120 pieces the border front dominates, so most presets read cyan with magenta cores. `-heavy` and `Cascade-inner` swap the roles (magenta-dominant).
- Glitch geometry varies by locale: horizontal scanline strips (`CHUNK_SHAPE_ANGLE=90`, stretch 3–8) dropping (terra), slicing apart (space) or sliding right by uneven amounts (wave); 120 spinning shards (`-heavy`, spin 25); blocks jerking loose at random moments (aqua, `LAUNCH_STAGGER`); an **underdamped** centripetal snap that overshoots and jitters around the centre without settling (depth, strength 0.8, drag 0.06); a barely cracked body eaten through by noise, leaving broken blocks (inner, min 0.08).
- Tried and dropped: a black fade (it turned cyan into muddy teal), `pulse` + cyan ↔ magenta arcs (the RGB lerp passes pastel lavender), and `per_chunk` corruption (peach + teal mixes). `pulse` is a single half-sine hump over the animation, not a flicker.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

383. `*.Glitch-Corrupt-terra` — pixel corruption with chaotic jarring physics; high SPREAD and SPIN with CHUNK_MASS_VARIANCE high for erratic motion, cyan outer to magenta inner bidirectional tint, TINT_NOISE high and TINT_JITTER high, DISSOLVE_PATTERN=noise for corrupted dropout
384. `*.Glitch-Corrupt-terra-heavy` — severe corruption, extreme erratic physics; extreme SPREAD, SPIN, and CHUNK_MASS_VARIANCE, cyan-magenta tint with TINT_NOISE max, DISSOLVE_PATTERN=noise with fast dissolve (DISSOLVE_CURVE<1)
385. `*.Glitch-Float-aqua` — corrupted fragments glitch upward erratically; GRAVITY_ANGLE=0 chunks rise, high SPREAD and SPIN, cyan-magenta tint with TINT_NOISE high, DISSOLVE_PATTERN=noise
386. `*.Glitch-Collapse-depth` — corrupted data collapses inward chaotically; BLAST_MODE=implode, GRAVITY_MODE=centripetal, high SPIN and CHUNK_MASS_VARIANCE, cyan-magenta tint with TINT_COLLISION=blend and TINT_NOISE high, DISSOLVE_PATTERN=noise
387. `*.Glitch-Drift-space` — zero-gravity corrupted fragments scatter erratically; GRAVITY_STRENGTH=0, high SPREAD and SPIN, cyan-magenta tint with TINT_NOISE high, DISSOLVE_PATTERN=noise
388. `*.Glitch-Sunder-wave` — struck laterally, corruption spreads jarringly in that direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward with high CHUNK_MASS_VARIANCE for erratic spread, cyan-magenta tint, DISSOLVE_PATTERN=noise
389. `*.Glitch-Cascade-inner` — corruption cascades outward from a point of failure within; BLAST_MODE=burst, high SPIN and SPREAD, bidirectional cyan-magenta tint with TINT_NOISE high, DISSOLVE_PATTERN=noise
