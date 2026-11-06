# Sprite Gibber — Preset Authoring Workflow

How presets are designed, built and judged. Load this at the start of any preset session (retuning presets, or adding presets/types). The whole library was rebuilt this way in the Stage 3 overhaul (finished 2026-10-31); "session" and "Stage 3" labels below date the findings to that pass.

**Docs to have open:**

- `docs/preset-briefs/_index.md` — library-wide findings, per-type index
- `docs/preset-briefs/<type>.md` — only the types in this session
- `docs/preset-param-reference.md` — every parameter, type, range, default
- `docs/mask-catalog.md` — only if a preset uses `FRAME_MASK`

---

## Session procedure

1. **Pick the types** to work on (`docs/preset-briefs/_index.md`; keep to ~50 presets per session, split at type boundaries). Read each type's brief: intent, gimmick lock, locales, Stage 3 notes, per-preset look/Fix/Flag lines.
2. **Triage:** `python tools/preset_metrics.py "*.Fire-" "*.Cryo-" …` flags likely-broken animations: too few distinct frames, a sim ending in 1–3 ticks, a settling sim hitting `MAX_SIM_TICKS`, >25 % pixels off-canvas. Use the `*.Type-` prefix as the term — a bare `Fire` also matches `Blade-Fire-Cleave`, `Grenade-Fire` and so on.
3. **Render the "before" sheets:** `python tools/preset_sheet.py "*.Fire-"` writes contact sheets to `shots/` (every frame of each preset on both test sprites, metric flags in each label; `--per-sheet N`, `--scale S`, `--out DIR`, `--every 2` for every 2nd frame + the last — the compact view that fits a whole type legibly in one image, e.g. `--every 2 --per-sheet 18 --out shots/stage3-sN/before`). Read the sheets — they are the judging view, not the GUI.
4. **Rebuild** each preset in `presets/<type>.py` to match its brief and the type's lock. Keep the name and the entry's `category`/`locale`/`intensity` fields. Rewrite the `description` (shown in the app) to match the new look in one plain sentence.
5. **Re-render and iterate** until every preset in the type passes the checks under *Judging a contact sheet*.
6. **Smoke-test** the touched types: `python tools/smoke_test_presets.py "*.Fire-"`.
7. **Keep the brief current:** if a brief turned out wrong, fix the brief too (it stays the reference for later).

Contact sheets and test renders go in `shots/`, never the scratchpad. The test sprites are `tools/test_sprites/confined_32.png` (polar bear filling a 32×32 canvas, pale palette — worst case for wall contact) and `wide_64.png` (lion bottom-centred on a 64×64 canvas, saturated warm palette — roomy, and shows where "centre" really is).

### Ground rules

- **Every preset stays, with its name.** No culling, merging or renaming. Naming stays `*.Category-Subtype-locale[-mod]` in one flat list.
- **Use the parameter space widely.** Most presets cluster around a few mid values and one recipe per locale. The overhaul exists to fix that.
- **Set the keys that define the look explicitly.** Loading a preset resets every effect key to `DEFAULT_CONFIG` before applying the preset's `params`, so anything left out silently takes the default. Always set at least: `CHUNKS` (or `SINGLE_CHUNK`), `BLAST_MODE`, `EXPLODE`, `GRAVITY_MODE` when not directional, `GRAVITY_ANGLE`/`GRAVITY_STRENGTH`, `DRAG`, `SPIN`, **`TINT_DEPTH_OUTER`** (0 = no tint — the default is a dark-red wound tint, and 42 presets that were meant to be untinted picked it up), and `DISSOLVE`.
- **Never put `FRAMES` in `params`.** Frame count is user-controlled (GUI-only key, default 16) and stripped on load. Presets must look good at 16 frames and hold up at 8 and 32. Express timing through `TINT_ANIM`, curves, stagger and the GIF timing keys.
- **GIF timing is preset-able:** `MS_PER_FRAME`, `HOLD_FIRST_MS`, `HOLD_LAST_MS` (330 presets set them). Use them to pace the effect: fast snaps want short frames, lingering fades longer ones.
- **`SEED` is preset-able too** (default 42, reset on load). Leave it unset unless a specific Voronoi layout is essential to the look — and then note why in the brief.
- **Masks:** read `docs/mask-catalog.md` first. A mask is justified only when its shape is the gimmick or as containment for an extreme preset — never because its filename matches the type's theme. `FRAME_MASK_ANIM` accepts `instant`/`linear`/`early`/`late`/`pulse` (no `per_chunk`).

### Judging a contact sheet

A preset passes when, on **both** sprites:

- frame 0 is the intact sprite and the motion reads from frame 1 on — no long static stretch, no event that's over by frame 2 (unless the brief wants a snap);
- the arc has a beginning, middle and end, and the last frame is a deliberate final state (settled pile, clump, empty canvas, residue);
- nothing important leaves the canvas or jams against a wall unless that's the point;
- the type's gimmick lock is visible — you could tell which type this is with the name hidden;
- it's visibly different from its siblings, not the same recipe at another strength;
- tint and dissolve read on both palettes (pale bear, warm lion).

Metric flags are hints, not verdicts: Void's zero motion and the single-chunk statues are flagged by design; an unflagged preset can still look bad.

---

## Engine facts that matter (fixed engine, 2026-10-30)

These are verified against the code and override anything older docs or idea lines say.

**Centre.** "Centre" for explode/implode/circle blasts and for centripetal/repulsor/orbital/vortex gravity is the **canvas centre**, not the sprite's. On `wide_64` (lion at the bottom of the canvas) an explode sends most pieces *down and sideways*, and centripetal pulls the whole lion *up* to mid-canvas.

**Floors and landing.** Floors are the canvas walls gravity points toward: one wall for cardinal gravity, two for diagonal (pieces slide along one floor into the corner). A chunk lands when its rotated leading pixel would cross the floor while moving into it. On landing, into-floor velocity is zeroed (or reflected by `BOUNCE`) and floor friction bleeds off sliding and spin, so split halves skid apart instead of freezing. On a roomy canvas pieces travel far: an aqua preset on `wide_64` rises to the top of a 64 px canvas.

**Edge containment.** Non-floor walls damp velocity inside `EDGE_ZONE` and hard-clamp the rotated chunk at the wall.

| Setting | Containment | Floors | Sim ends when |
|---|---|---|---|
| directional gravity > 0 | non-floor walls | the walls gravity points at | all chunks landed |
| `GRAVITY_STRENGTH = 0` | all four walls | none | all at rest, or `MAX_SIM_TICKS` |
| `noise` | all four walls | none | at rest / `MAX_SIM_TICKS` (force never stops — effectively the cap) |
| `vortex` | all four walls | none | at rest / `MAX_SIM_TICKS` |
| `centripetal` | **off** | none | all chunks settled at the centre |
| `repulsor`, `orbital` | **off** | none | at rest / `MAX_SIM_TICKS` |
| `BLAST_MODE` `implode` / `hollow_circle` / `filled_circle` | **off** (any gravity mode) | per gravity | per gravity |

With containment off, pieces can leave the canvas; off-canvas pixels are dropped at render (never smeared on the border). `implode` with ordinary down gravity means pieces converge, cross the centre and fall to the floor — a terra read, not a depth clump.

**Time-stretch.** Frames are spread evenly from tick 0 (intact) to the end of the sim, interpolating between ticks. A sim that ends in 2 ticks still gives smooth frames, but the motion reads as instant. A long tail (bounces, slow drift, `LAUNCH_STAGGER`) takes frame time away from the opening burst.

**`BOUNCE`** works and settles normally: each floor hit reflects the into-floor velocity × `BOUNCE` until the rebound is too weak to leave the floor. `0.2–0.5` gives one or two hops, above `0.6` reads as rubber. Use it when a bounce is part of the material (Bone, Crystal, pebbles), not as a casual touch.

**`LAUNCH_STAGGER`** works: each chunk waits up to `LAUNCH_STAGGER × MAX_SIM_TICKS` ticks, and the sim never ends while a chunk is still waiting. Above ~0.15 the timeline stretches and the first launches squash into the opening frames — pair it with a lower `MAX_SIM_TICKS`.

**Split axes.** `vertical_split` moves the top half up and the bottom half down (a *horizontal* cut line); `horizontal_split` moves the left half left and the right half right (a *vertical* cut). `CHUNK_BIAS` only places seeds: `halves-h` = top/bottom zones, `halves-v` = left/right zones, `quadrants` = four corners.

| Look | `BLAST_MODE` | `CHUNK_BIAS` |
|---|---|---|
| horizontal cut, top/bottom part (`-H`) | `vertical_split` | `halves-h` |
| vertical cut, left/right part (`-V`) | `horizontal_split` | `halves-v` |
| X cut, four quarters | `x_split` | `quadrants` |

**Chunk stretch.** `CHUNK_SHAPE_ANGLE` `0` = tall vertical slivers, `90` = horizontal strips, `45` = diagonal. Only active when `CHUNK_SHAPE_STRETCH > 1`.

**Sideways impact.** No blast mode gives every chunk the same direction. `horizontal_split` + gravity 90° (the old wave recipe) sends the left half *left* first. For "struck from the left, everything goes right", use a low-force `explode`/`shatter` and let strong 90° gravity carry everything right. The right wall is then the floor, so pieces pile against it.

**`burst`** gives every chunk an equal-speed random direction, regardless of position — centre pieces move as much as edge pieces. At tiny force it reads as jitter, not "radiating from the core". For radiating-from-within, use `explode` at tiny force (centre pieces barely move) or `shatter`, and let tint/dissolve (inner front; `centrifugal` erodes each chunk from its rim, see *Dissolve authoring*) carry the radiation.

**Bidirectional-only tint keys.** `TINT_DEPTH_INNER`, `TINT_OPACITY_INNER`, `TINT_JITTER_INNER`, `TINT_ALPHA_BLEED_INNER`, `TINT_COLOR_INNER_END`, `TINT_COLLISION` and `TINT_BLEND` do nothing unless `TINT_BLEND_MODE = "bidirectional"`. Many idea lines ask for `inner_wins` without saying bidirectional — set both. In unidirectional mode, `TINT_COLOR_INNER` is the colour at the depth cutoff (outer at the border → inner at the cutoff, opacity fading to 0).

**`DISSOLVE_MIN_PCT = 1.0` is a uniform late wash, not a colour-fade engine.** With no pixels dropping, every pixel's "dropout" frame is `FRAMES`, so the fade colour ramps in uniformly over the last `max(2, FRAMES // 4)` frames and peaks on the last frame (75 % of `DISSOLVE_FADE_STRENGTH` at 16 frames, 50 % at 8). Pattern, direction, curve and stagger have no effect. For a colour change over the whole animation use tint colour animation (`TINT_COLOR_*_END`). For a spatial colour sweep you need real dropout (`DISSOLVE_MIN_PCT` < 1).

**Survivors take the fade colour too.** Pixels that never drop (the `DISSOLVE_MIN_PCT` residue) count as dropping on frame `FRAMES`, so they shift toward `DISSOLVE_FADE_COLOR` over the last `w` frames. With a residue, the fade colour *is* the final colour: a dark fade turns the leftover bones/cores dark, a brown fade ends a pale preset in brown. Use `None` when the residue must keep its tint.

**Fade colour timing in general.** A pixel shifts toward `DISSOLVE_FADE_COLOR` during the `max(2, FRAMES // 4)` window (`w`) before its own dropout frame; on its last visible frame the blend is `DISSOLVE_FADE_STRENGTH × (1 − 1/w)` — 75 % of the strength at 16 frames, 50 % at 8. Push the strength higher than the colour you want to *see*.

**`TINT_SATURATION_SHIFT`** is applied post-tint and fades in with tint opacity when `TINT_ANIM` isn't `instant`. With a near-zero tint depth its reach is limited too.

---

## Designing a type: gimmick lock and locale gate

Every type has a recorded **gimmick lock** — 1–2 mechanical commitments held across all its presets. The lock is what makes a type recognisable with the name hidden, and what keeps sibling types (Rot/Plague/Fungal/Biodegrade/Wither, Break/Crush/Grind/Shred/Crack, Stone/Gold/Crystal …) apart. A lock is a feature-usage pattern, not a colour or a locale. Kinds that work:

- zero motion (`SINGLE_CHUNK`, or `EXPLODE` ≈ 0 with high drag) — a tint/dissolve piece;
- tint-only (`DISSOLVE = False` throughout) or dissolve-only (`TINT_DEPTH_OUTER = 0` throughout);
- one end of the chunk-count range (always 150+, or always under 10);
- one exotic gravity mode as identity (`noise`, `vortex`, `orbital`, `repulsor`);
- mask-driven (the mask shape is the point — see `docs/mask-catalog.md`);
- translucency as identity (very translucent, or fully opaque with zero bleed);
- a signature timing shape (`late` everywhere, `pulse` everywhere, front-loaded);
- a signature colour behaviour (a colour arc on every preset, a channel swap, a saturation shift);
- a signature chunk geometry (stretch angle, `CHUNK_BIAS`, mass variance, bounce).

**Locale gate.** The six locales are candidates, not a checklist. For each, ask: *does gravity direction/mode here change what this concept means, or does it just move the same idea to another wall?* Physical events (Fire, Nuclear, Blade) earn many locales; transformations (Heal, Curse, Vanish) often earn only a few. Record the surviving locales and why in the type's brief. When an existing preset fails the gate, **keep it and rework it** (as with the four Heal presets) — only the user removes presets.

**Distinctness bar.** Two locales (or two subtypes) of one type that differ only in `CHUNKS`/`EXPLODE`/`GRAVITY_ANGLE`/`GRAVITY_STRENGTH` and a tint hex are the same preset twice. A locale earns its slot when it changes *which feature does the visual work* — e.g. terra pure tint with no dissolve while depth is pure dissolve with tint off. Use a `-mod` suffix only for a real intensity/scale variant of the same idea.

### Locale table

Locales are behavioural archetypes, not literal places. The recipes are starting points.

| Locale | Meaning | Starting recipe |
|---|---|---|
| `terra` | breaks/explodes/shatters and falls; settles on the floor | directional, `GRAVITY_ANGLE = 180` |
| `aqua` | buoyant, floaty, rising (or a heavy material sinking slowly through liquid) | directional, `GRAVITY_ANGLE = 0`, low strength + higher drag; or 180 with very low strength for sinking |
| `depth` | crushed inward into a clump at the centre | `centripetal` (+ `implode` for a clean converge) or `vortex`. Plain `implode` with down gravity is *not* depth — it falls to the floor |
| `space` | weightless: drift and scatter, spin decays, no settle | `GRAVITY_STRENGTH = 0`, or `noise`/`vortex`/`orbital`/`repulsor` |
| `wave` | struck sideways by a shockwave or wind | directional 90° with strong strength; see *Sideways impact* above |
| `inner` | corruption/transformation from within: tiny or no force, tint/dissolve carry it | `GRAVITY_STRENGTH = 0`, `explode` at 0.1–0.25 or `shatter`, high drag |

Non-directional modes ignore `GRAVITY_ANGLE` — don't set it with them.

### Inner locale

- Zero gravity is the safe default. Continuous modes keep accelerating pieces every tick; `orbital`/`repulsor`/`centripetal` also switch containment off. `noise` and `vortex` stay contained. Use a continuous mode only when the brief needs it, and check `off=` in the metrics.
- `EXPLODE` 0.1–0.25 with drag 0.28–0.35: enough to crack the sprite, not enough to send pieces anywhere.
- Design tint and dissolve first; physics just separates the pieces gently.
- Prefer `explode`/`shatter` over `burst` (see *burst* above). Don't combine `burst` with `noise` — double randomisation is chaos.

---

## Gravity mode reference

`directional` (the default) needs no special rules beyond the locale table. The rest:

### `noise` — organic, directionless drift

- Keeps all four walls contained, no floor, force never stops (per-chunk direction drifting each tick).
- `EXPLODE` ≤ 0.5. For more scatter raise `SPREAD` or `CHUNKS`, not speed.
- Always set `MAX_SIM_TICKS` 80–120. At the 500 default, pieces have wandered far by the end and the time-stretched frames flash past.
- Never with `burst`.

### `repulsor` — continuous outward push

- Containment off, no settle: every tick pushes pieces further out. This is how `Plasma-Repulse-space` and `Smoke-Vent-aqua` ended up 100 % off-canvas.
- Safe start on ~32 px: `EXPLODE` 0.5–0.8, `GRAVITY_STRENGTH` 0.25–0.35, `DRAG` 0.24–0.28, explicit `MAX_SIM_TICKS` (≈80).
- Pair with a fast `centrifugal` dissolve (`DISSOLVE_CURVE` < 0.8) so pixels vanish before they reach the edge. Confirm with `off=` in the metrics.

### `vortex` — spirals inward

- 80 % centripetal / 20 % tangential. **Containment stays on** (all four walls, no floor).
- `GRAVITY_STRENGTH` 0.3–0.5; above 0.6 everything collapses in a few frames.
- `GRAVITY_RAMP_TICKS` ≈ 8 so the sprite visibly breaks apart before the pull; `MAX_SIM_TICKS` ≈ ramp + 45.
- `DRAG` 0.05–0.12 — more drag kills the spiral and it becomes plain centripetal.

### `centripetal` — pulls to the centre (depth)

- Containment off; the one non-directional mode that settles (pieces stop at the centre).
- Spring-like: underdamped settings overshoot and oscillate, and the time-stretch then shows "instant clump". Confirmed overdamped on ~32 px: `GRAVITY_STRENGTH` 0.8, `DRAG` 0.24, `EXPLODE` 1.5–2.0 — tune strength and drag together.
- Ramp usually unnecessary; add one only for a longer outward phase. Don't set `EDGE_ZONE` (no effect).

### `orbital` — tangential orbit

- Containment off, no settle. Chunks orbit the centre in an outward spiral.
- Use `GRAVITY_RAMP_TICKS` so pieces have radius before the orbit engages. `GRAVITY_STRENGTH` 0.3–0.8. Set `MAX_SIM_TICKS` explicitly and check `off=`.

---

## Colour authoring

### Tint vs. dissolve fade colour

- **Tint** answers "what colour is this material for the whole time it's on screen?" — sustained or slowly evolving.
- **Dissolve fade colour** answers "what colour does it flash as it disappears?" — an accent in the frames before each pixel vanishes.

Use both when the material has a sustained colour and a distinct vanish colour (fire: orange tint, char-black fade). Tint alone when nothing vanishes or the vanish is colourless. Fade colour alone (tint off) for a pure-dissolve effect. Whenever `DISSOLVE_FADE_COLOR` is set, also set `DISSOLVE_FADE_STRENGTH` (default 0.8).

| Element | Fade colour idea | Strength |
|---|---|---|
| Fire | `#111111` char, `#FF8800` ember | 0.5–0.8 |
| Cryo | `#CCEEFF` pale blue, `#FFFFFF` frost | 0.4–0.7 |
| Electric | `#FFFFAA` yellow-white, `#88CCFF` arc blue | 0.6–0.9 |
| Plasma | `#FFFFFF` hot white, `#FF88FF` magenta | 0.5–0.8 |
| Water | `#AADDFF` | 0.3–0.5 |
| Smoke | `#FFFFFF` to air, `#888888` wisps | 0.3–0.5 |
| Acid | `#66FF00` lime residue | 0.5–0.7 |
| Magic | tint-adjacent complementary | 0.4–0.7 |

### Vivid colour (Stage 3 session 1 findings)

The user wants every preset garish and clear in its colour identity. The old library looked washed out because of how tint mixes, not because of its hexes. How the engine mixes: each pixel is `sprite × (1 − opacity) + tint × opacity`, and opacity falls *linearly* from `TINT_OPACITY_*` at the front's seed (border or centroid) to 0 at the depth cutoff. A shallow front therefore averages ~50 % sprite colour (orange lion + blue tint = grey, pale bear + red = pink), and in unidirectional mode the inner colour only appears where opacity is already near 0.

- **Opacity 1.0** on anything that should read as its colour. Get translucency from `TINT_ALPHA_BLEED_*`, not from lower opacity (Water's lock was revised for this).
- **Deep fronts.** The body colour's front should reach well past the chunk's radius (depth 1.0–2.0+) so opacity stays near 1 everywhere. Fully saturated hexes (`#FF2E00`, `#00F0FF`, `#FF00C0`, `#40FF00`), not pastel ones.
- **Size accents to the chunk count.** Depth is a fraction of the *whole sprite's* √(opaque px) (~26 px on the bear, ~20 on the lion), but chunks shrink as `CHUNKS` grows: radius ≈ √(area / CHUNKS / π) px. At 30–50 chunks a 0.3 front already covers whole chunks. A thin rim or crack line wants outer ≈ 0.04–0.1; a hot core wants a small inner front (0.03–0.15) with `inner_wins` and the body colour on a deep outer front. At 150+ chunks every chunk is ~1 px across, so use `TINT_MODE="edges"` (graded from the silhouette, independent of chunk size) or a single colour.
- **Watch the RGB lerps.** Colour arcs (`*_END`) and `blend` collisions lerp straight through RGB: cyan ↔ yellow passes mint green, any colour → white passes pastel, blue over a warm sprite during a `linear` ramp passes purple. Use `outer_wins`/`inner_wins` where two fronts mustn't mix, and route arcs through neighbouring hues (yellow → white, blue → cyan, red → black). `TINT_COLOR_ANIM_CURVE` < 1 holds the start colour longer, > 1 rushes to the end colour.
- **Prefer `early`/`instant` over `linear`/`late`** unless slowness is the point. A late ramp spends half the animation in muddy sprite-plus-tint mixes. Carry slow change with the colour arc instead.
- **Never a positive `TINT_SATURATION_SHIFT` on white or near-white tint.** White has no hue, and the shift turns it pink.
- **Dissolve fade colour mixes too:** a yellow fade over cyan pixels reads green.
- **Leave some presets untinted on purpose** (plain steel cuts, untinted hammer pounds). Contrast between presets is part of the variety.

Session 2 additions (2026-10-31):

- **`instant` beats `early` for energy and gore.** Even `early` spends the first frames as a pale sprite-plus-tint mix (pink blood, lilac arcane), and a fast burst has mostly dissolved before the ramp completes. Use `instant` and let a colour arc (`*_END`) carry any change. Likewise, a damage → healed arc under a `linear` ramp never shows the start colour at full strength.
- **Fade colour dominates a dissolving preset.** When pixels drop all through the animation, most visible pixels are mid-fade at any moment. A pale `DISSOLVE_FADE_COLOR` (`#C080FF`, `#80E0FF`, white) then washes the whole preset out, so use saturated fades (`#0090FF`, `#C000FF`, `#00E8FF`, `#5A0004`).
- **Alpha bleed shows the background.** Over the GIF's background, bleed turns white into grey and gold into mustard. Keep it ≤ 0.15 except where translucency *is* the material (aqua clouds, smoke).
- **`TINT_MODE="edges"` is unidirectional only.** It ignores every bidirectional key, and colour and opacity share one ramp (inner colour only where opacity → 0), so it can't give a two-tone at full opacity. Use it for a flat colour (`TINT_SINGLE_COLOR`, depth ≥ 2.5) at any chunk count.
- **An `inner_wins` inner front owns everything inside its cutoff**, at falling opacity, so where it reaches, the outer body colour disappears and the sprite shows through. A "heart" accent must stay under the chunk radius: inner ≈ 0.04–0.06 (1 px) at 30–150 chunks. At 160+ chunks even 1 px spans the droplet, so use a flat colour plus arcs instead.
- **Masks.** An animating mask (`linear`, `pulse`, `early`'s ramp) multiplies alpha only partly, so everything outside the shape is translucent until the mask reaches full strength, which reads as pale. A canvas-centred mask also removes whatever ends on the floor or against a wall of a roomy canvas. Use `early`/`instant` when the pieces stay central (depth, space, in place); use `pulse` (shape held mid-animation, then released) or `late` (stamps the final pile) when they end on a wall; and choose shapes with solid centres for depth clumps (ring gears remove the clump).

### Textured materials (Stage 3 session 3a, user direction)

From session 3a on, **physical and organic materials** (flesh, bone, decay, stone, metal, sand, wood…) are *saturated but textured and believable*, not flat garish fills. The vivid rules above still apply against washout (opacity 1.0, deep fronts, no `late`/`linear` mud), but energy-style flat neon reads as "energised" on materials. The energy types done in sessions 1–2 stay as they are.

- **Two-tone mottling:** a darker shade front about one chunk radius deep (`TINT_DEPTH_OUTER` ≈ 0.15–0.4 at 4–40 chunks) with `TINT_JITTER_OUTER` 0.8–1.0 and `TINT_NOISE` 0.4–0.7, `blend` collision into a deep body front (`TINT_DEPTH_INNER` 4.0). Avoid `outer_wins` for this: the jittered low-opacity tail of the outer front wins over the full-opacity body and the sprite shows through.
- **`TINT_GRAIN`** (new, 0–1): a fixed per-pixel ±brightness factor after tint and saturation shift (kept constant across colour arcs). 0.15–0.25 for flesh/bone/earth/rot. It is the only texture that works on 1–2 px pieces. Pieces that small are all border, so any border front paints them one flat colour. For those, use a deep body front plus small jittered inner specks (`TINT_DEPTH_INNER` ≈ 0.16, `TINT_JITTER_INNER` 1.0, `TINT_BLEND` ≈ 0.08) plus grain. Grain also applies with the tint off.
- Smaller saturation boosts (+0.1), believable hexes (raw meat `#D8202C`/`#6A0814`, aged ivory `#EADDB8`/`#8A7458`, umber `#8E4A18`, sallow `#D8B828`), and a darker natural shade instead of a near-black outline.
- Judge texture on a zoomed sheet: `python tools/preset_sheet.py "<names>" --every 5 --scale 4 --out shots/<session>/detail`. The `--every 2` overview is too small to show it.

Session 3b additions (2026-10-31):

- **Border pixels are the majority well before 1–2 px pieces.** The outer front's distance is 0 on every pixel touching another chunk or the silhouette, and those pixels always get the full outer colour. At ~30 chunks on a 32 px sprite (pieces ~5 px across) that is about 60 % of the pixels, more on stretched shards. So the **outer colour is the dominant colour** at 20+ chunks, whatever its depth. Put the colour the material should read as on the outer front, and the accent (rust spots, gloss, glints, a clear glass core) on a small inner front. A dark shade on the outer front becomes a hard outline, so keep shades close to the body (Stone: `#6A6761` on `#8C8A84`).
- **Glass:** a saturated edge colour on a ~1 px outer front plus a pale core with `TINT_ALPHA_BLEED_INNER` ≈ 0.3, no jitter, no noise, almost no grain. White edges around a saturated translucent body come out pastel.
- **Metal gleam:** a deep → bright colour arc, saturation +0.2–0.3, and pale core specks or a 1 px catch-light rim, plus grain. Grain is multiplicative, so on bright gold it brightens some pixels toward yellow-white glints.
- **Rubbery bounce** (Goo) and **drag-limited implode** (`implode` with zero gravity and drag ≈ 0.2: pieces squeeze inward and stop) are useful depth/terra alternatives when centripetal would overlap 200 tiny pieces into one dot.
- Tooling: the image viewer can serve a stale copy of a contact sheet rewritten at the same path. Copy each iteration to a unique filename (e.g. `shots/<session>/iter/<Type>_<time>.png`) before reading it.

Session 4a additions (2026-10-31):

- **Extreme stretch makes every pixel a border pixel.** At stretch 8+ and 12+ chunks a strip is ~2 px thick, so even a 1 px outer front paints the whole strip. For sprite-coloured slabs with a glowing 1 px cut line, use 6–8 chunks (Laser `Slice-terra`). Fully coloured slivers are fine when that's the intended look.
- **`TINT_MODE="edges"` muddies a partial rim.** Its opacity falls from the silhouette inward, so a "modest" cyan rim over an orange sprite passes through grey. For a vivid two-tone, use a deep full-opacity outer front plus jittered inner specks (`TINT_DEPTH_INNER` ≈ 0.12, `TINT_JITTER_INNER` 0.8, `blend` 0.15), as on Ion.
- **A faint accent line needs low opacity on stretched shards.** Stretched shards are mostly border pixels, so a dark 1 px crack line at 0.6–0.7 opacity darkens a small sprite all over. 0.45 reads as a hairline (Crack).

Session 4b additions (2026-10-31):

- **Saturation shift without a tint colour.** `TINT_SATURATION_SHIFT` (and grain) applies to every pixel once any tint pass runs. A zero-opacity front (`TINT_DEPTH_OUTER` 0.05, `TINT_OPACITY_OUTER` 0) shifts the sprite's own colours with no tint colour. Liquify's wet sheen uses +0.12; +0.3 turns the pale bear cyan. Non-`instant` `TINT_ANIM` ramps the shift in.
- **Gradual darkening:** a flat black edges-mode front (`TINT_SINGLE_COLOR`, depth 3.0) at opacity ~0.75 under an `early`/`linear` ramp, with saturation −1, drains a sprite to grey and then toward black while keeping some detail (Entropy). A black `DISSOLVE_FADE_COLOR` alone only darkens pixels in their last few frames.
- **Tint ramps lerp RGBA**, so `TINT_ALPHA_BLEED_*` ramps in with `TINT_ANIM` too. A colour arc can't change alpha. `pulse` is one half-sine hump over the whole animation (peak mid-way), not a flicker.
- **`TINT_NOISE` can't make patches at high chunk counts.** The warped cutoff never drops below 1 px and border pixels (distance 0) always take the front, so at 100+ chunks noise changes almost nothing. For patches, use fewer, bigger chunks or a `noise` dissolve.
- **Bleed shows the background (again).** Mid-grey smoke at bleed 0.5 vanishes against a grey background, and border pixels take the full bleed. For gases, keep a full-opacity colour that sits off the background's value, with bleed 0.3–0.45.
- **Black fade over cyan reads teal mud.** A dark fade over a bright saturated colour passes through a dull mid-tone in its last frames. Use a saturated contrasting fade (magenta over cyan) or none.
- **Dissolve direction for "rain":** falling code or rain erases its tail first, so a downward cascade uses `DISSOLVE_DIRECTION=0` (top first) and a rising one uses 180.

Session 5a additions (2026-10-31):

- **High drag + weak force = slow terminal motion.** Gravity is added and then drag applied each tick, so a piece settles at ≈ `GRAVITY_STRENGTH × (1 − DRAG) / DRAG` px/tick. At drag 0.3–0.6 a force of 0.05–0.15 gives a slow sag, sift or drift instead of a fall (Tar's viscous slump, Spore's burst-then-drift). Without a sustained force, high drag just stops pieces dead. Expect these sims to hit `MAX_SIM_TICKS`; set it to where the drift should end.
- **A spreading dark core:** `inner_wins` + a `linear`/`late` ramp can't do it cleanly (sprite ring at the cutoff, mud everywhere). Use an instant body with a small inner-favoured `blend` heart and a slow `centripetal` dissolve with a black fade at 10–20 big chunks: each piece hollows from its heart outward as a black band (Curse).
- **`TINT_SATURATION_SHIFT` −1 bleaches warm colours.** HSV desaturation keeps V = max(R,G,B), so orange becomes near-white, not mid-grey. For a grey drain that keeps detail, add a neutral grey tint at opacity ~0.35 (Vanish).
- **A dark grey fade over red reads maroon-brown.** For smoke over embers use a mid grey (`#504A4C`) at strength 0.9–1.0 (Brimstone).

Session 5b additions (2026-10-31):

- **Split modes cut at the canvas centre too.** `vertical_split`, `horizontal_split` and `x_split` choose each chunk's side from the canvas centre, not the sprite's. On a bottom-anchored sprite (`wide_64`'s lion) every chunk is below the centre row, so `vertical_split` sends everything down (no cut) and `x_split` becomes a left/right split moving down. Use `horizontal_split` when the cut must read on any sprite (Clamp).
- **`TINT_COLOR_ANIM_CURVE` is `t^(1/curve)`.** Values above 1 reach the end colour early. On a fast-dissolving preset an arc at curve ≤ 1 never shows its end colour, because the pixels are gone first (Nuclear uses 1.5–1.8).
- **A spinning core keeps a centripetal sim alive.** With `SPIN_DRAG` 0 the sim doesn't end when the pieces arrive (spin counts as motion once nothing translates), so a fast fold (strength 4, drag 0.45) followed by a whirling star fills the rest of the frames up to `MAX_SIM_TICKS` (Antimatter `-instant`).
- **`filled_circle` + drag = a swelling ball that keeps its shape.** Speed is proportional to distance from the centre, so the sprite scales up uniformly and stops (Nuclear fireball). Containment is off, so keep `EXPLODE` ≈ 3.5 on a canvas-filling sprite.
- **`implode` with no gravity and no drag = collapse, then reverse.** Pieces rush in, cross the centre and fly out the far side; a dissolve finishes them as they exit (Nuclear `Implode-depth`).
- **Centripetal recipe check:** the confirmed overdamped recipe (strength 0.8, drag 0.24, implode 1.5–2.0) finishes clumping around frame 4–7 of 15. Fine when a dissolve or colour arc carries the rest; with neither, the GIF sits on a static lump, so slow it (strength 0.25–0.3, drag 0.32, smaller `EXPLODE`), as done for Meat/Bone/Laser in the final pass. Fewer, stretched pieces (14–70) overlap into a spiky core instead of a dot.

### Single vs. dual colour

`TINT_SINGLE_COLOR = True` (inner colour everywhere) for a flat identity colour with no border-vs-centre story. Bidirectional dual colour only when the brief has two colours doing two things (orange border / black charred centre, dark crust / molten core). Bidirectional is not free complexity — a flat wash is often the more honest read.

### `TINT_COLLISION` / `TINT_BLEND` (bidirectional only)

- `"blend"` + `TINT_BLEND` — a natural transition zone; default for organic/elemental materials.
- `"outer_wins"` — a hard shell over a core that must not show through (charred crust over molten core).
- `"inner_wins"` — an internal glow or corruption that dominates even where the fronts overlap; the natural choice for most inner-locale presets and bright-core depth/space presets.

Depths don't need to add up to a tidy split. On tint-heavy presets, deep overlap (`0.7`/`0.7`, `0.4`/`0.8`) reads richer; that's what the collision mode resolves. Depth is a fraction of √(opaque pixels): about 26 px on a full 32×32 sprite, 20 px on a ~400-pixel one. Use 0.5–1.0 freely for full coverage.

### Tint colour animation (`TINT_COLOR_*_END` + `TINT_COLOR_ANIM_CURVE`)

Use it whenever the material's colour plausibly changes over the animation. There are two triggers:

1. **A different named colour** — the material changes state (frost white → deep ice blue, raw metal → rust, healthy → sickly).
2. **The same phenomenon getting more or less extreme** — more/less saturated, brighter/darker, or a flavourful hue shift (yellow flame → hot blue-white). This is the common case for fire, plasma, electric, acid, smoke.

It's a different axis from `TINT_ANIM` (how fast the tint reaches full strength); they often run together. Don't dim energetic types by default — the colour QA found saturated swaps (electric cyan ↔ yellow, plasma magenta ↔ white-pink) read better than fades to dull.

### Opacity and alpha bleed

| Material | `TINT_OPACITY_*` | `TINT_ALPHA_BLEED_*` |
|---|---|---|
| Translucent gas/vapour/mist | 0.4–0.7 | 0.3–0.6 |
| Semi-translucent liquid | 1.0 (lower opacity just greys it out — see *Vivid colour*) | 0.15–0.35 |
| Opaque liquid/solid (blood pool, flesh, stone, metal) | 0.8–1.0 | 0.0–0.1 |
| Energy/light | 0.85–1.0 | 0.0 (crisp edge) |

Bleed on a solid reads as a rendering error. Don't hedge at 0.5 opacity for clearly opaque materials.

### `TINT_ANIM` — match the phenomenon's speed

The default is `"instant"` (full tint from frame 1), which suits a material that *is* that colour from the start.

- `"early"` — full intensity within the first third: fast, violent, impact-driven (electric, plasma, explosions, blood spatter).
- `"linear"` — even ramp: genuinely gradual phenomena (smouldering, corroding, staining, petrifying, colonising).
- `"late"` — stable until near the end, then arrives: delayed reactions, a curse kicking in, rot setting in.
- `"pulse"` — rhythmic throb (Singularity's signature); `"per_chunk"` — random onset per chunk (organic gore, patchy healing).

---

## Dissolve authoring

**Always set `DISSOLVE_MIN_PCT` explicitly** when `DISSOLVE = True`. It's the fraction of pixels still visible on the last frame (a floor), not a rate — the rate is `DISSOLVE_CURVE`.

| Intent | `DISSOLVE_MIN_PCT` |
|---|---|
| total vanish (fire, smoke, plasma, annihilation) | 0.01 |
| a few specks remain | 0.03–0.06 |
| residue remains, very destroyed | 0.10–0.15 |
| heavy damage | 0.20–0.30 |
| medium damage | 0.40–0.60 |
| light damage | 0.70–0.90 |
| no loss — late uniform fade-colour wash only (see engine facts) | 1.00 |

**Set `DISSOLVE_CHUNK_STAGGER` deliberately** (default 0 = every chunk on the same schedule, which reads mechanical):

| Feel | Stagger |
|---|---|
| everything together (flash/bang) | 0.0–0.1 |
| natural, slightly varied | 0.2–0.35 |
| chunk-by-chunk wink-out | 0.5–0.7 |
| dramatic one-at-a-time | 0.8–1.0 |

With `directional`/`gravity_aligned` patterns, stagger competes with the sweep — keep it 0.0–0.2.

**`DISSOLVE_CURVE`:**

| Value | Feel |
|---|---|
| 0.3–0.5 | very fast — most pixels gone in the first third (explosion, flash, discharge) |
| 0.6–0.9 | fast-leaning (fire, burning) |
| 1.0 | linear — rarely the most interesting |
| 1.3–2.0 | slow-out — holds, then falls apart (smoke, slow melt, wither) |
| 2.5–3.5 | very slow-out — but at 16 frames, above ~2.5 the last frame drops a cliff of pixels; use stagger to spread it |

**Pattern × stagger:**

| Pattern | Use | Stagger |
|---|---|---|
| `noise` | organic cloud-like speckle — the workhorse | 0.3–0.6 |
| `chunks` | whole chunks pop out (crystal shatter, Thanos snap) | 0.3–0.8 |
| `gravity_aligned` | sweep that follows `GRAVITY_ANGLE` (fire burns up, water drips down) | 0.0–0.3 |
| `directional` | custom-angle sweep — always set `DISSOLVE_DIRECTION` | 0.0–0.2 |
| `centrifugal` | outer pixels of **each chunk** first | 0.2–0.4 |
| `centripetal` | centre pixels of **each chunk** first | 0.2–0.4 |
| `random` | zero spatial coherence (Vanish's erasure) | 0.2–0.5 |

**`centrifugal`/`centripetal` are per chunk** (verified in session 4a): distance is measured from each chunk's own centroid, not the sprite's or the canvas's. With a few big chunks each piece hollows out or erodes from its rim. At 100+ chunks (1–3 px pieces) they look like uniform speckle, not a sprite-wide "outside in" or "hollow core". There is no sprite-wide radial dissolve. For patchy hollowing use `noise`, for a sweep use `directional`, and for one-by-one pop-outs use `chunks` with high stagger.

**Diagonal gravity piles everything in one corner.** Chunks don't collide, so every piece that slides along a floor into the corner ends at the same spot and they overlap into one small lump. `orbital` gravity throws pieces off the confined canvas even at strength 0.1.

**`DISSOLVE_DIRECTION` is the side that goes first:** pixels furthest in that direction dissolve first. For a lateral blast with gravity 90°, `DISSOLVE_DIRECTION=90` eats the leading (right) side first so the trailing side lingers; 270 removes the trailing side first. (Corrected in session 3a; the earlier note had it backwards.)

---

## Chunk counts

Presets clustered at 10–30 chunks, which looks mushy for almost every material. Use the full range deliberately (GUI slider 2–200, typed values up to 1000; targets assume 32–64 px sprites):

| Material | Chunks |
|---|---|
| liquids (water, acid pools, blood) | ~200+ |
| gases (smoke, steam, mist) | ~150 |
| powder (stone dust, bone meal, sand) | ~100–250 |
| shatter (glass, crystal, ice sheet) | ~50 |
| break (planks, crates, bones) | ~30 |
| crumple/crack (thick metal, bark) | ~3–15 |
| clean cuts | 2–4 |
| statues | 1 (`SINGLE_CHUNK`) |

A liquid with 20 chunks looks like broken glass; 200 looks like a splash.

---

## Adding presets or types later

1. Write the brief first: add the preset line (or a new `docs/preset-briefs/<type>.md` with intent, gimmick lock, locales and why, one line per preset) and an `_index.md` row.
2. Check every claim in the brief against `docs/preset-param-reference.md` and the engine facts above. If an idea can't be built with current params, simplify it or drop it.
3. A new type needs a `presets/<type>.py` module (`PRESETS = [ {name, category, locale, intensity, description, params}, … ]`) registered in both tuples in `presets/__init__.py` (registry order = GUI order). New parameters follow `docs/adding-parameters.md`.
4. Build and judge with the Stage 3 procedure above.

### Naming

`*.Category-Subtype-locale` or `*.Category-Subtype-locale-mod`

- **Category** — PascalCase, the Main Type name
- **Subtype** — Title-Kebab-Case (`To-Smoke`, `Flash-Burn`)
- **locale** — `terra` / `aqua` / `depth` / `space` / `wave` / `inner`
- **mod** — free lowercase word, only for a meaningful variant of the same category + subtype + locale (`low`, `heavy`, `fine`, `single` …)

The `*` prefix marks official presets (read-only in the app); custom presets can't start with `*`.
