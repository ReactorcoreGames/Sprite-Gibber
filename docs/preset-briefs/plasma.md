# Plasma — 12 presets (registry #40–51)

Module: `presets/plasma.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Hot ionised gas: plasma impacts, torches, flares, containment failure. Magenta/pink identity, distinct from Electric.

**Gimmick lock** (new): **Blob plasma with a white-hot core**: `TINT_NOISE` warps the boundary on every preset, bidirectional tint with a bright inner core, magenta ↔ white-pink swap. Chunks stay round (no stretch except `Torch`) — this is what separates it from Electric.

**Locales present:** terra ×4, aqua, depth ×2, space ×3, wave, inner.

**Why these locales:** All six, with three space-ish presets that differ by gravity mode (`Solar` drift, `Flare` violent, `Repulse` repulsor) and a vortex depth.

**Current state (2026-10-30):** chunks 28–100, explode 0.15–5.0; blast: explode 10, horizontal_split 1, shatter 1; gravity: directional 9, centripetal 1, vortex 1, repulsor 1; tint on 12/12, dissolve 12/12, mask 3/12, stretched chunks 1/12.

**Stage 3 notes:**

- `Plasma-Repulse-space` flings 100 % of pixels off-canvas (repulsor has no wall containment). Use repulsor at low strength with high drag and a fast centrifugal dissolve, or an explicit `MAX_SIM_TICKS` short enough that the bloom is still on screen.

## Stage 3 result (2026-10-30)

- White-hot cores are tiny inner fronts with `inner_wins` (inner depth 0.03–0.06 at 35–90 chunks); anything larger turns the whole preset pastel pink. In the 80–90-chunk presets the core is hot pink rather than white, since even 1 px is a big share of each chunk.
- `Repulse-space` fixed: repulsor strength 0.06, drag 0.3, explode 0.3, `MAX_SIM_TICKS` 40 + fast centrifugal dissolve. Wide is 11 % off-canvas; confined (canvas-filling bear) 38 %, by which point nearly every pixel has dissolved.
- `Torch-terra`'s 5x stretched slivers are too thin to show a separate border colour; it reads as magenta slivers flecked white.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

40. `*.Plasma-Burst-terra` — standard plasma ball impact; moderate CHUNKS scatter and settle, bidirectional tint with magenta outer glow to white-pink inner hot core, TINT_NOISE moderate for organic blob boundary, moderate dissolve as plasma cools
41. `*.Plasma-Burst-terra-high` — intense plasma detonation; high EXPLODE and CHUNKS, extreme bidirectional tint depth, bright white inner core to deep magenta outer, TINT_NOISE high, fast dissolve (DISSOLVE_CURVE<1) as superheated material vaporises
42. `*.Plasma-Torch-terra` — plasma cutter strips sprite along a vertical axis; CHUNK_SHAPE_STRETCH high (CHUNK_SHAPE_ANGLE=0 vertical slivers), low EXPLODE so strips fall nearly in place, white-pink inner to magenta outer tint, TINT_ANIM=early so heat peaks immediately then dissolve takes over
43. `*.Plasma-Flare-terra` — large plasma eruption settling downward; many chunks, high EXPLODE, TINT_NOISE high for fluid blob shapes, deep magenta outer to near-white inner, dissolve with DISSOLVE_CHUNK_STAGGER so chunks cool and vanish at different rates
44. `*.Plasma-Jet-aqua` — superheated plasma venting upward; GRAVITY_ANGLE=0 so chunks rise fast, intense bidirectional tint with bright white inner core, TINT_ALPHA_BLEED_INNER high for hot-core glow-through effect, fast dissolve as plasma cools rapidly on ascent
45. `*.Plasma-Collapse-depth` — magnetic confinement failure, plasma implodes; BLAST_MODE=implode, bidirectional tint with large TINT_DEPTH_INNER bright-white core crushed inward to magenta outer shell, TINT_NOISE moderate, dissolve at end as contained plasma vanishes
46. `*.Plasma-Vortex-depth` — tokamak failure; GRAVITY_MODE=vortex, BLAST_MODE=explode then plasma spirals inward in a tightening vortex, magenta outer shell compresses to blinding white core, TINT_NOISE high for fluid plasma boundary, centripetal dissolve as containment fails
47. `*.Plasma-Solar-space` — unconfined solar plasma drifting apart; GRAVITY_STRENGTH=0, chunks drift in all directions, bidirectional tint with high TINT_NOISE for amorphous blob shapes, magenta outer to white-pink inner, slow dissolve (DISSOLVE_CURVE>1) as plasma cools over many frames
48. `*.Plasma-Repulse-space` — uncontained plasma bloom; GRAVITY_MODE=repulsor keeps accelerating chunks outward past initial launch, spreading indefinitely beyond normal explode deceleration, magenta outer to white-pink inner, TINT_NOISE moderate, rapid centrifugal dissolve
   - **Fix:** 100 % off-canvas (repulsor, no containment). Keep the bloom on screen.
   - **Flag:** confined: only 6/16 distinct frames; 100.0% pixels off-canvas; wide: only 8/16 distinct frames; 100.0% pixels off-canvas
49. `*.Plasma-Flare-space` — violent solar flare eruption into vacuum; extreme EXPLODE into GRAVITY_STRENGTH=0, bright white-pink bidirectional tint, TINT_NOISE high, fast dissolve (DISSOLVE_CURVE<1) as plasma disperses instantly without atmosphere
50. `*.Plasma-Shockwave-wave` — lateral blast of superheated plasma gas; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90, magenta outer to white-pink inner tint with TINT_NOISE for soft fluid boundary, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 trailing edge last
51. `*.Plasma-Ignition-inner` — internal plasma ignition radiating from core; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER bright-white core spreading to magenta outer, TINT_NOISE moderate for organic spread, DISSOLVE_PATTERN=centrifugal outward from center
   - **Flag:** wide: sim ended after 2 tick(s)
