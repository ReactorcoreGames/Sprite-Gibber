# Bone — 8 presets (registry #211–218)

Module: `presets/bone.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Drained to bones and crumble, instant skeleton shatter, explode into bones.

**Gimmick lock** (new): **Brittle clatter**: beige/ivory tint that drains in (flesh → bone via colour animation or `linear`), and hard pieces with some `BOUNCE` (0.2–0.4) so bones clatter. Bone is the type that uses `BOUNCE` as identity.

**Locales present:** terra ×3, aqua, depth, space, wave, inner.

**Why these locales:** All six.

**Current state (2026-10-30):** chunks 25–70, explode 0.2–6.0; blast: explode 4, shatter 1, implode 1, horizontal_split 1, burst 1; gravity: directional 7, centripetal 1; tint on 8/8, dissolve 3/8, mask 1/8, stretched chunks 0/8.

**Stage 3 notes:**

- `BOUNCE` works since the engine fix and settles normally — see the workflow doc.

## Stage 3 result (2026-10-31, session 3a)

- **Style change (user):** flat bright ivory read as "energised". Bone is now aged ivory `#EADDB8` with warm grey-brown shading (`#8A7458`) mottled in from every chunk border (depth 0.15, jitter 0.9, noise 0.5, `blend`), `TINT_GRAIN` 0.15, no saturation shift. Flesh in the flesh → bone arcs is `#C0202C`, not neon. Fade colours are bone dust `#F2EAD4`.
- Lock kept. The "drain in" is a flesh → ivory colour arc (`Drain-terra`, `Explode-terra` with curve 0.5 so the red holds through the flight, `Drift-space`) or an outlined ivory piece from frame 1 (`Shatter`, `Sunder`, `Drain-aqua`, `Crush`). The red → ivory lerp passes through salmon for a few frames; kept as the flesh-stripping read. `BOUNCE` 0.25–0.45 on every floored preset; `Crush-depth` and `Drift-space` have no floor, so the clatter there is spin/collision only.
- `Burst-inner`: ivory bone cores (inner front 0.3, `TINT_BLEND` 0.04) inside raw flesh, and a `centrifugal` dissolve with no fade colour peels the flesh off each piece's edge so the bones are left. With a fade colour the surviving cores took it at the end and the bones vanished.

- **Final pass (2026-10-31):** `Crush-depth` clumped by frame 3–5 of 15 and then sat as a static lump for the rest of the GIF (no dissolve to carry it). Centripetal slowed to strength 0.3 / drag 0.32 (drag-limited creep), so the pieces converge over the whole animation. Sheet: `shots/stage3-final/depthfix/`.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

211. `*.Bone-Drain-terra` — flesh drains away leaving a crumbling skeleton; low EXPLODE and SPIN, beige tint with TINT_ANIM=linear so the bone color builds gradually, moderate dissolve as the drained husk crumbles apart
212. `*.Bone-Shatter-terra` — instant skeleton shatter; high CHUNKS, high EXPLODE and SPIN, beige tint at high TINT_OPACITY_OUTER, no dissolve so the scattered bone fragments remain
213. `*.Bone-Explode-terra` — body explodes directly into bones; extreme EXPLODE, high CHUNKS, beige tint, fast TINT_ANIM=early so bone color is immediate, no dissolve
214. `*.Bone-Drain-aqua` — flesh dissolves away in water, bones drift upward; GRAVITY_ANGLE=0 chunks rise, low EXPLODE, beige tint, slow dissolve (DISSOLVE_CURVE>1) as the lightened bones float and the last flesh fades
215. `*.Bone-Crush-depth` — skeleton crushed and collapsed inward; BLAST_MODE=implode, beige tint with TINT_COLLISION=inner_wins, moderate dissolve as fragments grind down to bone powder
216. `*.Bone-Drift-space` — zero-gravity bone fragments scatter; GRAVITY_STRENGTH=0, high CHUNKS, moderate EXPLODE, beige tint, no dissolve so fragments drift indefinitely
217. `*.Bone-Sunder-wave` — struck laterally, bones shatter off in the hit direction; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases chunks rightward, high CHUNKS, beige tint at high TINT_OPACITY_OUTER, no dissolve
218. `*.Bone-Burst-inner` — skeletal structure bursts outward from within; BLAST_MODE=burst, bidirectional tint with large TINT_DEPTH_INNER beige core, high CHUNKS and SPIN, no dissolve
