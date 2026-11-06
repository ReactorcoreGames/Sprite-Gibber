# Liquify — 7 presets (registry #356–362)

Module: `presets/liquify.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Turn to liquid without tint.

**Gimmick lock** (kept): no dissolve (liquid pools), high chunk counts, `BOUNCE=0` + high drag so chunks ooze and dead-stop.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** All six; each gets a distinct tint treatment (none / single-colour / bidirectional) and `Splash-wave` is the type's one motion-forward entry.

**Current state (2026-10-30):** chunks 150–240, explode 0.12–1.6; blast: explode 5, implode 1, horizontal_split 1; gravity: directional 5, centripetal 1, noise 1; tint on 7/7 (4 only via the default), dissolve 0/7, mask 0/7, stretched chunks 0/7.

**Stage 3 notes:**

- 4 presets (`Pool-terra`, `Pool-terra-slow`, `Drift-space`, `Splash-wave`) meant to be untinted inherit the default red tint — set `TINT_DEPTH_OUTER=0`.

## Stage 3 result (2026-10-31, session 4b)

- Lock kept: no dissolve, 160–260 droplets, `BOUNCE=0` with high drag (0.24–0.45, Splash 0.1), so drops ooze and dead-stop. The four untinted presets (`Pool-terra`, `-slow`, `Drift-space`, `Splash-wave`) keep the sprite's own colours with a *wet* sheen: a zero-opacity tint front (`TINT_DEPTH_OUTER` 0.05, `TINT_OPACITY_OUTER` 0) only enables the post-tint `TINT_SATURATION_SHIFT` (+0.12), which applies to every pixel. +0.3 turned the pale bear cyan and the lion neon.
- The three tinted presets are three different liquids: `Diffuse-aqua` cobalt ink (flat edges-mode `#1E50E8`, alpha bleed 0.3) billowing up at uneven rates; `Collapse-depth` **liquid silver** (`#7C8698` body, jittered white specks, grain, slight brighten arc) in a drag-limited implode, replacing the brief's crust/molten idea so it doesn't overlap `Ooze-inner`. Centripetal at 180 droplets overlapped everything into a dot. `Ooze-inner` turns red-hot droplet by droplet (`TINT_ANIM="per_chunk"`, flat `#E82000` → `#FF7A00`) while it oozes in place with zero gravity.
- `Pool-terra-slow` melts drop by drop (`LAUNCH_STAGGER` 0.12, `MAX_SIM_TICKS` 110). `Splash-wave` slaps against the right wall and sticks (14/16 distinct frames, by design).
- Engine limit found: `TINT_NOISE` can't make molten patches at 160 chunks, because border pixels always take a front (cutoff ≥ 1 px) and nearly every pixel is a border pixel.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

356. `*.Liquify-Pool-terra` — body liquifies and pools in place, no tint at all; high CHUNKS, low EXPLODE so chunks ooze rather than fly, high DRAG, BOUNCE=0 dead-stop settle
357. `*.Liquify-Pool-terra-slow` — slower, more viscous liquification; even higher CHUNKS and DRAG, near-zero EXPLODE, no tint, takes longer to fully settle
358. `*.Liquify-Diffuse-aqua` — liquid disperses upward through water like ink diffusing; directional rise, single-color pale-blue tint (TINT_SINGLE_COLOR) so the whole body reads as one translucent dye, no dissolve
359. `*.Liquify-Collapse-depth` — liquified mass compresses inward into a thick puddle under centripetal gravity; bidirectional tint (dark crust outer, molten-looking inner) with inner_wins collision, no dissolve so the compressed puddle remains intact
360. `*.Liquify-Drift-space` — zero-gravity liquification, droplets drift apart weightlessly with no settle; no tint, GRAVITY_MODE=noise for directionless drift, no dissolve — droplets simply separate and hang
361. `*.Liquify-Splash-wave` — struck laterally, liquid splashes off sideways as a fast physics event; no tint, high EXPLODE and low drag relative to the rest of the type (this locale is the type's one motion-forward entry), no dissolve
362. `*.Liquify-Ooze-inner` — liquification spreads outward from a point of melting within, near-static; bidirectional tint with inner_wins collision so the molten origin point glows through, tiny EXPLODE, no dissolve
