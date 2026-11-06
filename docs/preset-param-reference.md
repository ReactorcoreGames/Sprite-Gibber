# Sprite Gibber — Preset Parameter Reference

Every parameter that can appear in a preset's `params` dict (`presets/<type>.py`). Loading a preset first resets every effect key to `DEFAULT_CONFIG` (`utils/config.py`), then applies the preset — so an omitted key always takes its default, never the previous preset's value. GUI-only keys (`FRAMES`, `GIF_SCALE`, `SHEET_COLUMNS`, the sprite list and other app state — `GUI_ONLY_KEYS`) are stripped from presets; the CLI-only `OVERWRITE`/`INPUT_DIR`/`OUTPUT_DIR` live in `params.py`. Engine behaviour behind these parameters (containment, floors, split axes, fade timing) is documented in `docs/preset-ideation-workflow.md` → *Engine facts*.

---

## Physics

| Parameter | Type | Default | Range / Values | Effect | Interactions |
|---|---|---|---|---|---|
| `FRAMES` | int | `16` | 2–64 | Total output frames (frame 0 = intact, last = fully settled or MAX_SIM_TICKS) | **Not preset-able** — user setting (GUI-only key); listed for reference |
| `SEED` | int | `42` | any int | RNG seed for Voronoi layout and per-chunk randomness | Preset-able and reset to 42 on preset load; set it only when one specific layout is essential |
| `MAX_SIM_TICKS` | int | `500` | 50–2000 | Safety cap on the pre-simulation | Preset-able. Never-settling modes (`noise`, `vortex`, `orbital`, `repulsor`, `GRAVITY_STRENGTH = 0`) run until at rest or this cap, so set it explicitly for them |
| `CHUNKS` | int | `16` | 1–1000 (GUI slider 2–200, typed up to 1000) | Number of Voronoi regions the sprite is split into | Ignored when `SINGLE_CHUNK = True` |
| `EXPLODE` | float | `2.5` | 0.0–20.0 | Initial outward speed scale (pixels/frame) | Scales velocity for all `BLAST_MODE` values |
| `GRAVITY_STRENGTH` | float | `1.2` | 0.0–10.0 | Acceleration along gravity direction (pixels/frame²); `0` = zero-gravity / drift | `0` disables settling; pre-sim caps at `MAX_SIM_TICKS` |
| `GRAVITY_ANGLE` | int | `180` | 0–359 | Gravity direction in degrees: 0=up, 90=right, 180=down, 270=left | Determines which canvas edge chunks settle against; auto-used by `DISSOLVE_PATTERN = "gravity_aligned"`; ignored by non-directional `GRAVITY_MODE` values |
| `GRAVITY_MODE` | str (enum) | `"directional"` | `"directional"` `"centripetal"` `"repulsor"` `"orbital"` `"vortex"` `"noise"` | Per-tick gravity behaviour: `directional`=follows `GRAVITY_ANGLE`; `centripetal`=pulls toward sprite center; `repulsor`=pushes away from center (continuously accelerates outward — use low `GRAVITY_STRENGTH` and high `DRAG` or chunks escape canvas); `orbital`=tangential orbit force; `vortex`=centripetal+tangential (spirals inward); `noise`=per-chunk slowly-varying random direction (keep `EXPLODE ≤ 0.5`) | Non-directional modes ignore `GRAVITY_ANGLE`; `centripetal`/`repulsor`/`orbital` disable edge containment; `vortex` and `noise` keep all four walls contained (no floor) |
| `DRAG` | float | `0.18` | 0.0–1.0 | Fraction of velocity lost per tick | Per-chunk drag modified by `CHUNK_MASS_VARIANCE` |
| `SPREAD` | float | `1.2` | 0.0–5.0 | Randomness spread multiplier on initial velocity direction | Higher = more chaotic initial directions |
| `SPIN` | float | `8.0` | 0.0–45.0 | Max rotation rate (degrees/tick) | Decays over time when `SPIN_DRAG > 0` |
| `EDGE_ZONE` | int | `6` | 0–200 (GUI slider 0–32) | Pixel width of wall-proximity damping zone | Containment is off for `implode`, `hollow_circle`, `filled_circle` blast modes and for `centripetal`/`repulsor`/`orbital` gravity |
| `BLAST_MODE` | str (enum) | `"explode"` | `"explode"` `"implode"` `"hollow_circle"` `"filled_circle"` `"shatter"` `"x_split"` `"vertical_split"` `"horizontal_split"` `"burst"` | Initial velocity pattern for all chunks | `implode`/circle modes disable edge containment |
| `CHUNK_MASS_VARIANCE` | float | `0.0` | 0.0–1.0 | Random per-chunk drag multiplier spread; `0` = uniform mass | Modifies effective `DRAG` per chunk |
| `BOUNCE` | float | `0.0` | 0.0–1.0 | Velocity restitution on floor collision; `0` = dead-stop; a chunk settles once its rebound is too weak to leave the floor | Only active with directional gravity and `GRAVITY_STRENGTH > 0` |
| `SPIN_DRAG` | float | `0.0` | 0.0–1.0 | Per-tick spin decay multiplier; `0` = no decay | Applied before angle accumulation each tick |
| `LAUNCH_STAGGER` | float | `0.0` | 0.0–1.0 | Random onset delay spread across sim ticks; `0` = simultaneous launch | Each chunk waits up to `LAUNCH_STAGGER × MAX_SIM_TICKS` ticks before moving; the sim always runs until every chunk has launched, so values above ~0.15 stretch the timeline and squash the first bursts into early frames |
| `SINGLE_CHUNK` | bool | `False` | `True` / `False` | Treat entire sprite as one Voronoi region (no gibbing, just one piece) | Overrides `CHUNKS`; all other systems unaffected |
| `GRAVITY_RAMP_TICKS` | int | `0` | 0–60 | Free-flight ticks before centripetal / vortex / orbital force activates; during this window no center-relative force and no drag are applied so the sprite visibly breaks apart before being pulled in | Only active when `GRAVITY_MODE` is `"centripetal"`, `"vortex"`, or `"orbital"`; `0` = force acts from tick 1 |
| `CHUNK_BIAS` | str (enum) | `"none"` | `"none"` `"halves-h"` `"halves-v"` `"core"` `"shell"` `"quadrants"` | Controls where Voronoi seeds are drawn from: `none`=fully random; `halves-h`/`halves-v`=top-bottom or left-right split; `core`=seeds cluster toward centroid; `shell`=seeds cluster toward edges; `quadrants`=seeds distributed into four corner regions | Ignored when `SINGLE_CHUNK = True`; `CHUNK_BIAS_STRENGTH = 0` makes this identical to `"none"` |
| `CHUNK_BIAS_STRENGTH` | float | `0.0` | 0.0–1.0 | Blend between random seed placement (0.0) and strict zone/distance bias (1.0) | Ignored when `CHUNK_BIAS = "none"` or `SINGLE_CHUNK = True` |
| `CHUNK_SHAPE_STRETCH` | float | `1.0` | 1.0–10.0 | Axis stretch factor for Voronoi distance metric; `1.0` = standard Euclidean (current behavior, true no-op); higher = longer thinner chunks elongated along `CHUNK_SHAPE_ANGLE` | Ignored when `SINGLE_CHUNK = True` |
| `CHUNK_SHAPE_ANGLE` | int | `0` | 0–359 | Direction of chunk elongation in degrees: 0=vertical slivers, 90=horizontal strips, 45=diagonal shards | Only meaningful when `CHUNK_SHAPE_STRETCH > 1.0`; ignored when `SINGLE_CHUNK = True` |

---

## Tint

> Tint applies a BFS color flood over each chunk from borders inward (and centroids outward in bidirectional mode).
> `TINT_DEPTH_OUTER = 0.0` disables tint entirely (zero-cost path).

| Parameter | Type | Default | Range / Values | Effect | Interactions |
|---|---|---|---|---|---|
| `TINT_BLEND_MODE` | str (enum) | `"unidirectional"` | `"unidirectional"` `"bidirectional"` | `unidirectional`: border BFS only. `bidirectional`: border BFS + centroid BFS | Enables all `*_INNER` params when `"bidirectional"` |
| `TINT_MODE` | str (enum) | `"chunks"` | `"chunks"` `"edges"` | `chunks`: tint follows inter-chunk borders. `edges`: tint follows sprite silhouette | — |
| `TINT_COLOR_OUTER` | str (hex color) | `"#660000"` | any valid hex e.g. `"#FF2222"` | Border/outer tint color | Ignored when `TINT_DEPTH_OUTER = 0.0`; animates toward `TINT_COLOR_OUTER_END` if set |
| `TINT_COLOR_INNER` | str (hex color) | `"#FF2222"` | any valid hex | Center/centroid tint color | Only used when `TINT_BLEND_MODE = "bidirectional"` or `TINT_SINGLE_COLOR = True` |
| `TINT_DEPTH_OUTER` | float | `0.12` | 0.0–1.0 | Outer front reach as fraction of `sqrt(opaque_px)`; `0.0` = tint disabled | — |
| `TINT_DEPTH_INNER` | float | `0.12` | 0.0–1.0 | Inner front reach (bidirectional only) | Only active when `TINT_BLEND_MODE = "bidirectional"` |
| `TINT_OPACITY_OUTER` | float | `0.8` | 0.0–1.0 | Color strength at border | — |
| `TINT_OPACITY_INNER` | float | `0.8` | 0.0–1.0 | Color strength at centroid | Only active when `TINT_BLEND_MODE = "bidirectional"` |
| `TINT_JITTER_OUTER` | float | `0.3` | 0.0–1.0 | Raggedness of outer front edge | Higher = more organic, irregular boundary |
| `TINT_JITTER_INNER` | float | `0.3` | 0.0–1.0 | Raggedness of inner front edge | Only active when `TINT_BLEND_MODE = "bidirectional"` |
| `TINT_ALPHA_BLEED_OUTER` | float | `0.0` | 0.0–1.0 | Extra transparency at border edge | Creates a semi-transparent fringe at chunk borders |
| `TINT_ALPHA_BLEED_INNER` | float | `0.0` | 0.0–1.0 | Extra transparency at centroid center | Only active when `TINT_BLEND_MODE = "bidirectional"` |
| `TINT_COLLISION` | str (enum) | `"blend"` | `"blend"` `"outer_wins"` `"inner_wins"` | How inner and outer BFS fronts interact when they meet | Only active when `TINT_BLEND_MODE = "bidirectional"` |
| `TINT_BLEND` | float | `0.5` | 0.0–1.0 | In `"blend"` collision mode: meeting-point ratio; `0`=inner wins, `1`=outer wins | Only active when `TINT_COLLISION = "blend"` and `TINT_BLEND_MODE = "bidirectional"` |
| `TINT_SINGLE_COLOR` | bool | `False` | `True` / `False` | Ignore outer color; use inner color everywhere | Simplifies to one-color tint regardless of blend mode |
| `TINT_ANIM` | str (enum) | `"instant"` | `"instant"` `"linear"` `"early"` `"late"` `"pulse"` `"per_chunk"` | Tint intensity progression over frames | `"per_chunk"` staggers onset randomly per chunk |
| `TINT_COLOR_OUTER_END` | str (hex) or None | `None` | hex string or `None` | If set, outer color shifts from `TINT_COLOR_OUTER` to this by the last frame | Enables color animation; curve controlled by `TINT_COLOR_ANIM_CURVE` |
| `TINT_COLOR_INNER_END` | str (hex) or None | `None` | hex string or `None` | If set, inner color shifts from `TINT_COLOR_INNER` to this by the last frame | Only meaningful when `TINT_BLEND_MODE = "bidirectional"` or `TINT_SINGLE_COLOR = True` |
| `TINT_COLOR_ANIM_CURVE` | float | `1.0` | 0.1–4.0 | Gamma exponent for color animation: `1.0`=linear, `<1`=fast-out, `>1`=slow-out | Only active when `TINT_COLOR_OUTER_END` or `TINT_COLOR_INNER_END` is set |
| `TINT_NOISE` | float | `0.0` | 0.0–1.0 | Large-scale noise field warps BFS depth cutoff per pixel | Creates organic blob shapes in tint boundary; `0` = no noise |
| `TINT_SATURATION_SHIFT` | float | `0.0` | -1.0–1.0 | HSV saturation shift applied after tinting; `-1`=fully desaturate, `+1`=oversaturate | Applied post-tint; fades in with tint opacity when `TINT_ANIM != "instant"` |
| `TINT_GRAIN` | float | `0.0` | 0.0–1.0 | Per-pixel grain: each pixel's RGB is scaled by a fixed seeded factor in `1 ± TINT_GRAIN` after tint and saturation shift (same factor for the start and end colours of a colour arc) | Works at any chunk count and with the tint off; fades in with tint opacity when `TINT_ANIM != "instant"`; draws RNG only when > 0, so grain-free presets are unaffected |

---

## Dissolve

> `DISSOLVE = False` disables dissolve entirely (zero-cost path).
> Dissolve operates at render time only — physics simulation is unaffected.

> **Preset authoring note:** `DISSOLVE_MIN_PCT` must be a **float fraction** (e.g. `0.01` for 1%).
> The GUI displays it as a float percent (0.00–100.00%) with a spinbox for precision; the config default is `0.01`.
> Never omit `DISSOLVE_MIN_PCT` from a dissolve preset — without it the default `0.01` (1%) applies,
> which is usually fine, but making it explicit documents your intent.

| Parameter | Type | Default | Range / Values | Effect | Interactions |
|---|---|---|---|---|---|
| `DISSOLVE` | bool | `False` | `True` / `False` | Master switch; `False` = no dissolve | All other dissolve params ignored when `False` |
| `DISSOLVE_MIN_PCT` | float | `0.01` | 0.001–1.0 | Fraction of opaque pixels kept in the last frame; prevents a fully empty final frame. **Always a float in presets** — `0.01` = 1%, `0.10` = 10% | Minimum enforced as `max(1, total_opaque * DISSOLVE_MIN_PCT)`. At `1.0` nothing drops, and the fade colour becomes one uniform wash over the last few frames — pattern/curve/stagger then do nothing |
| `DISSOLVE_PATTERN` | str (enum) | `"random"` | `"random"` `"noise"` `"directional"` `"centrifugal"` `"centripetal"` `"chunks"` `"gravity_aligned"` | Pixel dropout ordering pattern | `"directional"` uses `DISSOLVE_DIRECTION`; `"gravity_aligned"` uses `GRAVITY_ANGLE` |
| `DISSOLVE_DIRECTION` | int | `180` | 0–359 | Degrees (0=up, 90=right, 180=down, 270=left); direction pixels dissolve toward | Only used when `DISSOLVE_PATTERN = "directional"` |
| `DISSOLVE_CURVE` | float | `1.0` | 0.1–4.0 | Gamma exponent: `1.0`=linear, `<1`=fast-out (dissolves quickly then slows), `>1`=slow-out | — |
| `DISSOLVE_CHUNK_STAGGER` | float | `0.0` | 0.0–1.0 | Random per-chunk onset delay before dissolve begins; `0`=simultaneous, `1`=fully sequential | Every chunk is guaranteed a proportional dissolve window regardless of onset — `DISSOLVE_MIN_PCT` remains the sole authority on final-frame survivors |
| `DISSOLVE_FADE_COLOR` | str (hex) or None | `None` | hex string or `None` | If set, pixels shift toward this color as they approach their dropout frame | Only active when `DISSOLVE = True` and not `None` |
| `DISSOLVE_FADE_STRENGTH` | float | `0.8` | 0.0–1.0 | Blend strength toward `DISSOLVE_FADE_COLOR`, ramping over the `max(2, FRAMES // 4)` frames before each pixel's dropout; the last visible frame reaches `strength × (1 − 1/window)` (75 % at 16 frames) | Only active when `DISSOLVE_FADE_COLOR` is set |

---

## Frame Mask

> `FRAME_MASK = None` disables masking entirely (zero-cost path). Applied to frames 1+; frame 0 is always unmasked.
> Unlike most other `FRAME_MASK*` params, these are **not** GUI-only sticky state — presets can set them like any other param, and they reset to default when switching to a preset that doesn't set them.

| Parameter | Type | Default | Range / Values | Effect | Interactions |
|---|---|---|---|---|---|
| `FRAME_MASK` | str or None | `None` | filename in `assets/masks/`, or `None` | BW PNG alpha mask composited onto frames 1+ | `None` disables the entire feature |
| `FRAME_MASK_FIT` | str (enum) | `"stretch"` | `"stretch"` `"fit"` `"crop_center"` | How the mask image is scaled to the sprite canvas | Only meaningful when `FRAME_MASK` is set |
| `FRAME_MASK_SOFTNESS` | int | `0` | 0–20 | Gaussian blur radius applied to mask before compositing; `0` = hard edge | Only meaningful when `FRAME_MASK` is set |
| `FRAME_MASK_FLIP` | bool | `False` | `True` / `False` | Flip mask vertically | Only meaningful when `FRAME_MASK` is set |
| `FRAME_MASK_MIRROR` | bool | `False` | `True` / `False` | Mirror mask horizontally | Only meaningful when `FRAME_MASK` is set |
| `FRAME_MASK_ROTATE90` | bool | `False` | `True` / `False` | Rotate mask 90° clockwise | Only meaningful when `FRAME_MASK` is set; combine with flip/mirror to reach any of the 4 rotations |
| `FRAME_MASK_ANIM` | str (enum) | `"instant"` | `"instant"` `"linear"` `"early"` `"late"` `"pulse"` | Mask opacity progression over frames | Only meaningful when `FRAME_MASK` is set |

---

## Output (GIF)

> Timing keys drive both GIF export and preview playback (`core.output.frame_durations`); they don't affect frame PNGs or the spritesheet. They are preset-able, so a preset can pace its own effect.

| Parameter | Type | Default | Range / Values | Effect | Interactions |
|---|---|---|---|---|---|
| `GIF_SCALE` | int | `4` | 1–20 | Nearest-neighbour upscale factor applied to each GIF frame | **Not preset-able** — export setting (GUI-only key) |
| `MS_PER_FRAME` | int | `80` | 10–2000 | Display time per middle frame in milliseconds (rounded to nearest 10 ms in GIF) | — |
| `HOLD_FIRST_MS` | int | `500` | 0–5000 | Display time of the first frame (intact sprite) in milliseconds | Set to `0` to not hold |
| `HOLD_LAST_MS` | int | `800` | 0–5000 | Display time of the last frame (fully settled) in milliseconds | Set to `0` to not hold |

---

## Quick-reference: conditional params

These params are **only meaningful** under specific conditions:

| Param | Only active when |
|---|---|
| `TINT_DEPTH_INNER`, `TINT_OPACITY_INNER`, `TINT_JITTER_INNER`, `TINT_ALPHA_BLEED_INNER`, `TINT_COLOR_INNER_END` | `TINT_BLEND_MODE = "bidirectional"` |
| `TINT_COLLISION`, `TINT_BLEND` | `TINT_BLEND_MODE = "bidirectional"` |
| `TINT_COLOR_ANIM_CURVE` | `TINT_COLOR_OUTER_END` or `TINT_COLOR_INNER_END` is not `None` |
| `DISSOLVE_DIRECTION` | `DISSOLVE_PATTERN = "directional"` |
| `DISSOLVE_FADE_STRENGTH` | `DISSOLVE_FADE_COLOR` is not `None` |
| `GRAVITY_RAMP_TICKS` | `GRAVITY_MODE` is `"centripetal"`, `"vortex"`, or `"orbital"` |
| All dissolve params except `DISSOLVE` | `DISSOLVE = True` |
| `CHUNKS` | `SINGLE_CHUNK = False` |
| `CHUNK_BIAS_STRENGTH` | `CHUNK_BIAS != "none"` and `SINGLE_CHUNK = False` |
| `CHUNK_SHAPE_ANGLE` | `CHUNK_SHAPE_STRETCH > 1.0` and `SINGLE_CHUNK = False` |
| `EDGE_ZONE` | `BLAST_MODE` not in `["implode", "hollow_circle", "filled_circle"]` and `GRAVITY_MODE` not in `["centripetal", "repulsor", "orbital", "vortex"]` |
| `GRAVITY_ANGLE` | `GRAVITY_MODE = "directional"` |
| All `FRAME_MASK_*` params | `FRAME_MASK` is not `None` |
