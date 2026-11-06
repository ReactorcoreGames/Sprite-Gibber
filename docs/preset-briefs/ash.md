# Ash — 7 presets (registry #369–375)

Module: `presets/ash.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Turn to dust; dark grey.

**Gimmick lock** (kept): solid particulate — 100+ chunks, a residue always remains (`DISSOLVE_MIN_PCT` ≥ 0.10), soot palette.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six — unlike smoke, ash can honestly compress into a clump.

**Current state (2026-10-30):** chunks 100–150, explode 0.18–1.8; blast: explode 5, implode 1, horizontal_split 1; gravity: directional 5, centripetal 1, noise 1; tint on 6/7 (1 only via the default), dissolve 6/7, mask 0/7, stretched chunks 0/7.

**Stage 3 notes:**

- `Ash-Scatter-wave` is meant to be untinted but inherits the default red tint — set `TINT_DEPTH_OUTER=0` (or a soot tint if the lock's palette should apply).

## Stage 3 result (2026-10-31, session 4b)

- Lock kept: 130–220 chunks, a residue on every preset (`DISSOLVE_MIN_PCT` 0.12–0.45; `Scatter-wave` has no dissolve at all), soot palette. It is textured per *Textured materials*: a deep full-opacity body (`TINT_DEPTH_OUTER` 4.0) plus jittered contrasting specks (`TINT_DEPTH_INNER` 0.12–0.14, `blend` 0.1) and grain 0.2–0.25. Pieces are 1–3 px, so speck mottling is the only two-tone that survives.
- Palettes vary: char black → flecked grey ash arc (`Crumble-terra`, min 0.45 heap); pale powdery ash mostly blown off in a `random` speckle (`-fine`, min 0.15); dark soot floating up and gathering as surface scum (aqua, min 0.3); a black charcoal lump (depth); pale speckled flakes on gentle `noise` gravity (space); a grey streak blown right (wave); ember orange burning out to grey ash in place (`Crumble-inner`, arc `#FF5200` → `#66615C`).
- `Collapse-depth` is a drag-limited implode (zero gravity, drag 0.2), not centripetal: centripetal at 150 chunks overlapped the lump into a dot. `Crumble-inner` dropped `per_chunk` + an ember fade colour, because survivors take the fade colour and the residue ended as orange blobs. `centrifugal` dissolve was not used (per chunk; see the workflow doc).

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

369. `*.Ash-Crumble-terra` — body crumbles to ash and settles into a pile; tint-led (dark-grey TINT_OPACITY_OUTER high), minimal dissolve so most ash remains as visible debris
370. `*.Ash-Crumble-terra-fine` — finer ash, more of it blows away as fine dust; higher CHUNKS, lower DISSOLVE_MIN_PCT floor and faster DISSOLVE_CURVE than the standard Crumble, but still leaves a residue (never near-zero)
371. `*.Ash-Drift-aqua` — sooty cloud disperses upward into water; directional rise, bidirectional dark-grey/pale tint, DISSOLVE_PATTERN=noise as the cloud thins while ascending
372. `*.Ash-Collapse-depth` — ash compresses inward into a compact clump under centripetal gravity; TINT_DEPTH_OUTER near-zero (dissolve-only identity), fast DISSOLVE_PATTERN=centripetal as the crumbling mass shrinks
   - **Flag:** confined: only 14/16 distinct frames
373. `*.Ash-Drift-space` — zero-gravity ash drifts apart in all directions with no settle; near-zero tint, GRAVITY_MODE=noise for directionless scatter, slow dissolve fading over many frames
374. `*.Ash-Scatter-wave` — struck laterally, ash scatters sideways as a fast all-physics event, no tint, no dissolve — the scattering motion itself is the entire effect
375. `*.Ash-Crumble-inner` — combustion to ash radiates outward from a point within, near-static; bidirectional tint with inner_wins collision so the smoldering origin reads through, slow centrifugal dissolve
