# Heal — 7 presets (registry #165–171)

Module: `presets/heal.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Restoration, the inverse of damage: a D-Cross mending seam while the tint animates from a sickly damage hue to a clean healed hue.

**Gimmick lock** (kept): D-Cross mask family, `TINT_COLOR_*_END` sickly green → cyan-white on every preset, `DISSOLVE=False` everywhere (healing never destroys pixels), 100–300 chunks.

**Locales present:** terra ×2, aqua, depth, space, wave, inner.

**Why these locales:** aqua, depth, inner pass the gate. terra, terra-fast, space and wave were flagged `[NEEDS REWORK]` (generic shatter/drift/shove recipes that read as destruction). They stay, with the rework briefs below.

**Current state (2026-10-30):** chunks 130–220, explode 0.15–0.9; blast: explode 4, implode 1, horizontal_split 1, burst 1; gravity: directional 6, centripetal 1; tint on 7/7, dissolve 0/7, mask 7/7, stretched chunks 0/7.

**Stage 3 notes:**

- Rework principle: the body must never visibly fly apart. Use `BLAST_MODE="shatter"` or `EXPLODE` ≤ 0.2 with high drag so chunks only shimmer. Make the locale show in *how the healing arrives* — `TINT_ANIM` (`per_chunk`, `linear`, `early`, `pulse`), `TINT_MODE` (edges vs. chunks) and mask orientation/animation — not in where pieces travel.
- Spatial colour sweeps aren't available without pixel loss: `DISSOLVE_MIN_PCT=1.0` only gives a uniform fade over the last ~quarter of frames (see the workflow doc).

## Stage 3 result (2026-10-31)

- Lock kept: D-Cross mask, sickly chartreuse (`#A8E800`) → aqua/cyan-white arc on every preset, no dissolve, 100–200 chunks, never visibly breaks (force ≤ 0.3).
- The damage hue must show first: with `linear`/`per_chunk` tint the colour arc had already moved on before the tint reached strength, so the sickly green never appeared. Healing is carried by `instant`/`early` tint plus the arc, and locales differ in how it arrives: mottled patches (`Mend`), white snap (`Restore`), translucent (`Buoy`), compaction (`Knit`, capped at 22 ticks so it doesn't shrink to a dot), breathing `pulse` that returns to the sprite's own healthy colours (`Drift`), noisy front (`Surge`), cyan-white 1 px hearts (`Bloom`).
- Most masks `pulse`, so the cross passes over the body and it ends whole. The D-Cross shapes only trim the corners; they're a subtle presence, not a cut.
- Metric flags: six presets end after 1 tick (zero motion is the point), and `Knit-depth` hits its 22-tick cap on purpose.
- The four rework presets follow their rework briefs: no break, healing via tint anim/mode and mask animation.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

165. `*.Heal-Mend-terra` — [NEEDS REWORK] a wound closes and knits back together; a dense chunk field barely scatters beneath a thin-armed D-Cross mask reading as a mending seam, sickly-green tint shifts to clean cyan-white over the animation as the damage visibly reverses
   - **Fix:** REWORK: no visible break. `shatter`/near-zero force; healing creeps in chunk by chunk (`TINT_ANIM="per_chunk"`) from the outer edge (`TINT_MODE="edges"`) while the cross mask fades in `linear`. 'terra' = grounded, steady mend.
166. `*.Heal-Restore-terra-fast` — [NEEDS REWORK] a burst of restorative magic snaps the body back together at once; a dense chunk field beneath a thick D-Cross mask, sickly-green rapidly shifts to bright cyan-white as the mend completes almost instantly, no dissolve since nothing is being destroyed
   - **Fix:** REWORK: same no-break rule; everything snaps clean at once — `TINT_ANIM="early"`, fast colour curve, mask `early`.
167. `*.Heal-Buoy-aqua` — restorative energy rises through the body like a soothing current; a dense chunk field drifts gently upward beneath a soft D-Cross mask, sickly-green fades to clear cyan-white as it ascends, a translucent healed core glows at the center
168. `*.Heal-Knit-depth` — scattered damage is drawn back together and knitted whole; a dense chunk field is pulled inward beneath a D-Cross mask that tightens as the mend completes, sickly-green outer heals to cyan-white inner, the wound compresses into a healthy core
169. `*.Heal-Drift-space` — [NEEDS REWORK] restorative motes hang weightless and gently converge; a dense chunk field drifts under a D-Cross mask, sickly-green fades to clean cyan-white slowly over many frames as if the healing is patient and unhurried (currently redundant with Knit-depth — both are "motes converge")
   - **Fix:** REWORK (currently redundant with `Knit-depth`): weightless and patient — chunks hang perfectly still, tint `pulse`s while the colour animation creeps slowly; the only one-look-per-frame 'breathing' heal.
170. `*.Heal-Surge-wave` — [NEEDS REWORK] a wave of restorative force rolls through the body sideways; a dense chunk field is nudged rightward beneath a D-Cross mask stretched along the surge, sickly-green washes to cyan-white as the healing energy passes through
   - **Fix:** REWORK: no shove. A healing wave passes left→right — the mask (mirrored/rotated so it opens from the left) animates in while the colour arc runs; at most a tiny gravity-90° shimmer.
171. `*.Heal-Bloom-inner` — restoration blooms outward from a point deep within; a dense chunk field reveals a D-Cross mask growing outward from the core, cyan-white health radiates from center to a fading sickly-green edge, healing the chunks outward from within
