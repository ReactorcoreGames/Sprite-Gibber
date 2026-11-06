# Sprite Gibber — Project Context

## What this project is

A standalone Windows GUI app (Python, ttkbootstrap, compiled with PyInstaller) that turns pixel art sprites (PNG with transparent background) into "gibbing" animations: the sprite explodes into rotating chunks that fly outward and settle under simulated gravity. Purpose: let a layperson indiedev make gib frames for their sprites as hassle-free as possible.

Released: paid Windows build at https://reactorcore.itch.io/sprite-gibber, MIT source on GitHub. The project is in maintenance: the engine, GUI and 479-preset library are finished. New work is bug fixes, features and preset changes on request.

## Commands

```
python main.py                                      # GUI
python main_cli.py                                  # headless batch: input/ -> output/, settings in params.py (docs/cli-usage.md)
build_release.bat [nopause]                         # dist/SpriteGibber/ + dist/SpriteGibber.zip
python tools/smoke_test_presets.py <terms|all>      # crash check, full pipeline per preset
python tools/preset_metrics.py <terms|all>          # flags likely-broken animations (67/479 flagged by design, listed in docs/preset-briefs/_index.md)
python tools/preset_sheet.py <terms> [--every 2]    # contact sheets into shots/, on both test sprites
```

Terms are exact names or substrings; use the `"*.Fire-"` prefix to match one type (a bare `Fire` also matches `Blade-Fire-Cleave`). There is no unit-test suite. Engine changes are checked with the smoke test plus contact sheets, GUI changes by driving the real app.

## Architecture

All callers (GUI preview, GUI export, CLI, `tools/`) go through `core/pipeline.py`: `build_params()` turns a config dict into the engine's `p` namespace, and `run_sprite()` runs chunking → tint → dissolve schedule → physics → render → frame mask. Its optional `cancel` callable is polled between stages, sim ticks and frames and raises `RenderCancelled`; omitting it changes nothing. **Never duplicate pipeline steps in a caller**; an earlier four-copy setup drifted apart.

```
main.py                 # GUI entry point
main_cli.py, params.py  # headless batch CLI and its hardcoded settings (GUI uses config.json)
build_release.bat       # PyInstaller -> release folder + zip. --collect-submodules gui + PYTHONPATH because the lazy tabs are imported by name. Ships exe, assets/, example_sprites/ (from input/), README, LICENSE, guide.md, promo/ (minus the og_img source art); never promo.md, config, user presets or the log
core/
  pipeline.py           # build_params, run_sprite, process_sprite_file
  chunking.py           # voronoi_chunks, chunk_centroid, initial_velocity, make_gravity_dir
  physics.py            # simulate_step: gravity modes, drag, edge containment, floors, bounce, floor friction
  rendering.py          # rotate_pixels, render_states, snapshots + interpolation, apply_tint, build_dissolve_schedule, apply_frame_mask
  output.py             # render_frames, frame_durations (GIF + preview timing), save_frame_pngs, save_spritesheet, save_gif, export_stem
gui/
  app.py                # GibberApp: window, layout, lazy tabs (_ensure_tab), _refresh_all_tabs, show_error
  preview.py            # PreviewPanel: canvas, playback, zoom, sprite cycle, live mode; build_p() shared with export
  export_bar.py         # ExportBar: export this/all, stop, progress, open folder; worker thread
  theme.py              # custom "gibber" theme (Warm Putty palette), PALETTE, FONT_*
  tabs/                 # sprites (Sprites & Export), presets, physics, tint, dissolve, mask
  widgets/              # controls (choice_combo, slider_row, MoreOptions), randomizer_panel, direction_widget
utils/
  config.py             # load_config, save_config, DEFAULT_CONFIG, GUI_ONLY_KEYS, legacy-key migration
  presets_io.py         # custom presets, search, is_modified, name validation, dev save_official_preset_to_source
  paths.py              # app_dir, resolve_user_path, masks_dir, normalize_user_file, list_pngs, export_dir_for, write_text_atomic, quarantine_corrupt
  log.py                # sprite_gibber.log + excepthooks, short_reason (friendly errors)
  dev.py                # DEV_MODE (source vs. frozen), gates dev-only GUI features
presets/                # 61 type modules + __init__.py (PRESETS dict, PRESET_LIST, rebuild())
assets/                 # icon.ico, masks/ (BW PNGs for FRAME_MASK)
input/                  # 35 animal sprites (~32x32, free, no attribution): CLI input, shipped as example_sprites/
tools/                  # QA tools above, shared _preset_tools.py, test_sprites/, promo builders (promo_images, promo_showcase, preset_catalog)
promo/                  # store images, screenshots, showcase GIFs, catalog sheets; ships in the release zip
docs/                   # see below
guide.md                # layperson guide for the exe (opened by the Help Guide button)
promo.md                # marketing notes + itch/GitHub/YouTube copy; not in the release zip
```

Local and gitignored: `config.json`, `user_presets.json`, `sprite_gibber.log`, `dist/`, `output/`, `showcase_gifs/`, `shots/` (`shots/promo/gui/` holds the raw GUI captures `tools/promo_images.py` stamps), `promo/Military Unit Samples/`, and `old wip/` (finished trailers and their build scripts, checklists, review renders, the original design doc). `old wip/` is history: only look there if asked, and its trailer scripts expect to sit at `trailer/` in the project root.

Docs:
- `docs/preset-param-reference.md`: every preset parameter with type, range and interactions. Check here rather than guessing.
- `docs/adding-parameters.md`: wiring a new parameter end to end (GUI → config → engine → randomizer → presets).
- `docs/preset-ideation-workflow.md`: preset authoring procedure, contact-sheet judging, verified engine facts, colour recipes. Read before any preset work.
- `docs/preset-briefs/`: one brief per type (intent, gimmick lock, locales, per-preset look) + `_index.md`.
- `docs/mask-catalog.md`: every `FRAME_MASK` shape by silhouette.
- `docs/cli-usage.md`: headless CLI.

## Engine behaviour

- **Chunks:** Voronoi over opaque pixels (alpha > 0). `CHUNKS` (GUI slider 2–200, typed up to 1000), `SINGLE_CHUNK`, `CHUNK_BIAS`, `CHUNK_SHAPE_STRETCH`/`ANGLE`.
- **Pre-simulation time-stretch:** `FRAMES` always spans intact sprite → settled state (or all motion stopped / `MAX_SIM_TICKS`). Tick 0 is at rest and frames between ticks are interpolated, so fast settles still give smooth frames. The sim never ends while a `LAUNCH_STAGGER` chunk is still waiting; spin only keeps it alive when nothing translates (shatter-in-place).
- **`GRAVITY_MODE`:** `directional` (follows `GRAVITY_ANGLE`: 0 up, 90 right, 180 down, 270 left), `centripetal`, `repulsor`, `orbital`, `vortex` (80/20 centripetal/tangential), `noise` (per-chunk slow random direction). `centripetal`/`repulsor`/`orbital`/`vortex` never settle and run to `MAX_SIM_TICKS`. `GRAVITY_RAMP_TICKS` gives free flight before a centre-relative force engages. "Centre" is the canvas centre. `GRAVITY_STRENGTH = 0` = zero gravity.
- **`BLAST_MODE`:** `explode`, `implode`, `hollow_circle`, `filled_circle`, `shatter`, `burst`, `x_split`, `vertical_split`, `horizontal_split`. Split modes cut at the canvas centre.
- **Floors:** the canvas walls gravity points toward (one for cardinal gravity, two for diagonal: chunks slide along one into the corner). A chunk lands only when its rotated leading pixel would cross a floor while moving into it. Landing zeroes the into-floor velocity (or reflects it by `BOUNCE` until the rebound can't leave the floor), and floor friction bleeds off sliding and spin.
- **Edge containment:** non-floor walls damp (`EDGE_ZONE`) and hard-clamp, tested on the rotated chunk so spin can't swing pixels through. All four walls contain when there is no floor (zero gravity, vortex, noise). Disabled for implode/circle blasts and centripetal/repulsor/orbital gravity. Off-canvas pixels are dropped at render time, never clamped onto the border.
- **Tint:** two-front BFS: outer bleeds in from chunk borders, inner radiates out from centroids (`bidirectional`). Controls: `TINT_DEPTH_*`, `OPACITY`, `JITTER`, `ALPHA_BLEED`, `COLLISION`, `NOISE`, `SATURATION_SHIFT`, `GRAIN`, `ANIM`, and colour arcs via `*_END` + `TINT_COLOR_ANIM_CURVE`. `TINT_DEPTH_OUTER = 0` disables it. A Voronoi cell split by the silhouette gets an inner-front seed per piece. `TINT_GRAIN` draws RNG only when > 0.
- **Dissolve:** render-time pixel dropout, physics unaffected. `DISSOLVE_PATTERN` has 7 patterns, plus `CURVE`, `CHUNK_STAGGER`, `FADE_COLOR`/`STRENGTH`. Keeps at least `max(1, total_opaque * DISSOLVE_MIN_PCT)` pixels.
- **Frame mask:** render-time alpha from `assets/masks/`, frames 1+. `FRAME_MASK*` are preset-able, and reset when loading a preset that doesn't set them. Masked PNGs are re-saved so disk matches sheet and GIF.
- **Output:** `<dest>/<stem>/` with `<stem>` = `<sprite>_<effect>` (`core.output.export_stem`; effect = preset name without `*.`, `-mod` if tweaked, or `custom`). Frame PNGs `<stem>_00.png…` (3-digit pad past 100 frames), `<stem>_sheet.png`, `<stem>.gif` (nearest-neighbour upscale, hold frames, 1-bit transparency with palette slot 255 reserved). Re-exports replace, and `save_frame_pngs` clears stale frames first. Only the CLI has `OVERWRITE = False`.

## Constraints that bite

- **All output stays within the sprite's canvas.** There is no canvas growth.
- **Floors are canvas walls, never the sprite's extent**, and containment must not push back against a floor wall.
- **`make_gravity_dir` snaps float noise to zero** (sin 180° ≈ 1e-16), because containment keys off the sign of each component.
- **Blast modes affect containment.** Implode is not inverted explode: velocity aims at the centre, containment is off, and gravity/drag decelerate it.
- **Zero gravity + shatter-in-place** never settles, so the sim must cap at `MAX_SIM_TICKS`.
- **RNG order is part of the look.** New random draws must be conditional (as with `noise_seed` and `TINT_GRAIN`) or every preset's seed changes.
- **Every preset sets `TINT_DEPTH_OUTER` and `DISSOLVE` explicitly.** Loading a preset resets effect keys to `DEFAULT_CONFIG`, whose tint is on (dark red), so omitting them inherits a red tint.

## GUI behaviour

- **Lazy tabs:** only Sprites & Export builds at startup; the others build on first view or in idle time from 1.5 s. Anything touching a tab must check `hasattr(app, "<name>_tab")`.
- **Live preview:** every setting change goes through `PreviewPanel.set_dirty`, with a 300 ms debounce when *Live* is on. One render worker runs at a time; a generation counter + cancel event drop stale results. A render over 1.5 s pauses live mode for the session (saved preference untouched). Preview is off during export. Playback uses GIF timing (`core.output.frame_durations`).
- **Controls** (`gui/widgets/controls.py`): `choice_combo` shows friendly names while var/config/presets keep snake_case. `slider_row` = slider + typed box + double-click reset; slider travel covers what presets use, the box accepts the full range. `MoreOptions` collapses advanced controls and opens itself when loaded settings use one of its keys, so nothing a preset sets is hidden.
- **Presets:** officials (`presets/*.py`, names start with `*`) are read-only in the app; custom presets live in `user_presets.json` (names never start with `*`). "Modified" = `presets_io.is_modified()` comparing config to the loaded preset. Dev-only "Save to Source" rewrites just that entry in `presets/<type>.py` (comments, order, line endings kept) and calls `presets.rebuild()`.
- **Sprites & export:** remembered list in `config["sprite_files"]`. Destination `export_dest` = `"beside"` (`gibbed/` next to each sprite) or `"folder"` (`export_folder`). Export snapshots settings at start; same-named sprites going into one folder get ` (2)`, ` (3)`…
- **`GUI_ONLY_KEYS`** (`FRAMES`, `GIF_SCALE`, `SHEET_COLUMNS`, sprite list, destination, `rand_*`, `live_preview`…) survive preset loads and aren't saved into presets.
- **Randomizer:** ticked groups roll from usable ranges; *Vary current settings* nudges 25 % toward a fresh roll. It applies through `set_dirty`.
- **Errors:** Tk callback, thread and uncaught errors go to `sprite_gibber.log`. Failed previews show the reason on the canvas; export failures end in a dialog with per-file reasons (`GibberApp.show_error`).
- **User files** resolve via `utils/paths.app_dir()`: the exe's folder when frozen, the project root from source. JSON is written atomically; corrupt files are renamed aside (`*.corrupt-N.json`), never wiped.
- **`requirements.txt` pins `ttkbootstrap>=2.2,<3`:** the custom theme relies on 2.x's legacy path.

## Preset library

479 presets in 61 Main Types, named `*.Category-Subtype-locale[-mod]` in one flat list (deliberate; see memory). Entries carry `name`, `category`, `locale`, `intensity`, `description`, `params`. Every type has a **gimmick lock** (1–2 mechanical commitments held across its presets) and a **locale gate** (`terra`/`aqua`/`depth`/`space`/`wave`/`inner`, included only if gravity there changes what the preset means), so some types have fewer than six locales by design.

Any preset change follows `docs/preset-ideation-workflow.md`: judge by contact sheets on both test sprites (`tools/test_sprites/`: `confined_32.png`, `wide_64.png`), not in the GUI. Energy types are vivid; physical materials are saturated but textured.

## Instructions for Claude

After a feature or fix, update this file only if the structure, commands, or behaviour described here changed, and do it at clean completion rather than mid-task. If a doc referenced here gets moved or removed, fix the reference in the same pass. Keep this file about the current project; history belongs in git.
