# Grenade — 14 presets (registry #116–129)

Module: `presets/grenade.py`. Stage 3 brief, consolidated in Stage 2 (2026-10-30) from the archived preset design docs (idea file, type list, colour QA notes) and the current library. Read `docs/preset-ideation-workflow.md` first — its engine facts and rules apply to every type.

**Intent:** Frag grenades plus incendiary, cryo, EMP, acid, flash, chaff and underwater/depth/space variants.

**Gimmick lock** (new): **Fragmentation**: high spin, high `CHUNK_MASS_VARIANCE` (uneven fragments), explosion from the canvas centre; each variant's identity comes from its element tint/dissolve on top of the same frag physics.

**Locales present:** terra ×9, aqua, depth, space, wave, inner.

**Why these locales:** terra (×9), aqua, depth, space, wave, inner.

**Current state (2026-10-30):** chunks 22–80, explode 0.2–5.5; blast: explode 13, horizontal_split 1; gravity: directional 13, centripetal 1; tint on 7/14, dissolve 7/14, mask 1/14, stretched chunks 3/14.

**Stage 3 notes:**

- `Grenade-Depth-depth` currently reads as a terra slam — make the pressure crush visible.

## Stage 3 result (2026-10-31)

- Lock held on every preset: spin 6–30, `CHUNK_MASS_VARIANCE` 0.5–0.9, centre explosion (`burst` for `Frag-space`/`Burst-inner` so pieces spread up as well as down on the bottom-anchored lion).
- Chunk-border scorch at 40–140 chunks covers whole fragments (orange then black). The frag scorch is now silhouette-based (`TINT_MODE="edges"`, 0.25–0.4, jitter 0.6–0.7), so the sprite colour survives with blackened outer faces.
- `Depth-depth` now shows the pressure crush: explode 3.2 then centripetal (strength 0.8, drag 0.3, ramp 5 ticks, cap 90) into a navy knot. Drag below 0.3 oscillated on the bear and ran to `MAX_SIM_TICKS`.
- `Cryo` deliberately breaks the high-spin half of the lock (spin 6, `SPIN_DRAG`) for rigid ice, with a `BOUNCE` clink. `Chaff` uses `TINT_ANIM="pulse"` on silver foil strips for a glint.

## Presets

Each entry: the look to aim for (the original idea brief — parameter hints in it are suggestions, not requirements), then any Stage 2 correction (**Fix**) and the baseline metric flags (**Flag**, from `tools/preset_metrics.py` on 2026-10-30).

116. `*.Grenade-Frag-terra` — standard frag grenade; high EXPLODE, many small CHUNKS, very high SPIN, moderate DRAG, CHUNK_MASS_VARIANCE high for uneven fragment sizes, LAUNCH_STAGGER low for simultaneous detonation, no tint, fragments settle downward
117. `*.Grenade-Frag-terra-small` — concussion/micro grenade; fewer but larger chunks, moderate EXPLODE, very high SPIN, lower DRAG so chunks carry farther, no tint; read is "smaller blast, bigger pieces"
118. `*.Grenade-Frag-terra-large` — large fragmentation shell; maximum CHUNKS, extreme EXPLODE, very high SPIN, CHUNK_MASS_VARIANCE high, LAUNCH_STAGGER slight for chaotic stagger effect, no tint; maximum mechanical carnage
119. `*.Grenade-Fire-terra` — incendiary grenade; same high EXPLODE/SPIN/CHUNKS as Frag, orange outer to yellow inner bidirectional tint on all fragments, TINT_ANIM=early (fire peaks immediately), moderate dissolve with DISSOLVE_CHUNK_STAGGER as burning fragments cool at different rates, DISSOLVE_FADE_COLOR dark orange
120. `*.Grenade-Cryo-terra` — cryo grenade; high EXPLODE, many CHUNKS, low SPIN for rigid ice fragments, icy-white outer to deep-blue inner bidirectional tint, CHUNK_SHAPE_STRETCH moderate for flat shard-like ice fragments, minimal dissolve (frozen solid)
121. `*.Grenade-EMP-terra` — EMP grenade; high EXPLODE, many CHUNKS, very high SPIN, CHUNK_SHAPE_STRETCH diagonal (CHUNK_SHAPE_ANGLE=45) for jagged bolt-shaped fragments, cyan outer to yellow inner bidirectional tint, fast dissolve (DISSOLVE_CURVE<1) with DISSOLVE_CHUNK_STAGGER for chaotic spark scatter
122. `*.Grenade-Acid-terra` — acid grenade; high EXPLODE, many CHUNKS, moderate SPIN, TINT_MODE=edges lime-green tint eating inward from fragment surfaces, TINT_NOISE moderate for irregular corrosion, heavy dissolve with DISSOLVE_CHUNK_STAGGER as fragments dissolve at different rates
123. `*.Grenade-Flash-terra` — flash grenade; extreme EXPLODE, many CHUNKS, very high SPIN, near-white outer to pure-white inner bidirectional tint, TINT_ANIM=early (flash peaks instantly), very fast dissolve (DISSOLVE_CURVE<1) as all matter vaporises in blinding burst
124. `*.Grenade-Chaff-terra` — chaff grenade; many CHUNKS with CHUNK_SHAPE_STRETCH high (CHUNK_SHAPE_ANGLE=0 horizontal strips for foil strips), moderate EXPLODE, low GRAVITY_STRENGTH and high DRAG so strips flutter slowly, silver-grey unidirectional tint from edges, no dissolve; strips settle lazily downward
125. `*.Grenade-Frag-aqua` — underwater detonation; high EXPLODE but GRAVITY_ANGLE=0 so fragments rise, high DRAG (water resistance), bidirectional tint with pale-blue outer to near-white inner for bubble/cavitation effect, heavy dissolve (DISSOLVE_CURVE>1) as fragments are quenched on ascent
126. `*.Grenade-Depth-depth` — depth charge underwater implosion; BLAST_MODE=explode then GRAVITY_STRENGTH very high slams all fragments to bottom instantly, many CHUNKS, high SPIN, no tint; read is "detonation instantly crushed by water pressure and gravity"
   - **Fix:** Terra slam under a depth name — make the pressure crush visible.
   - **Flag:** wide: only 13/16 distinct frames
127. `*.Grenade-Frag-space` — zero-gravity fragmentation; GRAVITY_STRENGTH=0, low DRAG (vacuum), high EXPLODE, many CHUNKS, very high SPIN, CHUNK_MASS_VARIANCE high, no tint; fragments tumble outward indefinitely with no settling
128. `*.Grenade-Shaped-wave` — shaped charge directional blast; BLAST_MODE=horizontal_split, GRAVITY_ANGLE=90 biases fragments rightward, high EXPLODE, many CHUNKS, high SPIN, DISSOLVE_PATTERN=directional DISSOLVE_DIRECTION=270 so trailing fragments dissolve last, no tint
129. `*.Grenade-Burst-inner` — grenade detonates from inside the sprite; BLAST_MODE=burst, high EXPLODE, many CHUNKS, very high SPIN, CHUNK_MASS_VARIANCE high, LAUNCH_STAGGER low, no tint; rupture aesthetic from within
