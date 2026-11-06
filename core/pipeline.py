"""Single source of truth for the gib pipeline.

Every caller (GUI preview, GUI batch, CLI, tools/) goes through build_params()
and run_sprite() so parameter handling and simulation can't drift apart.
"""
import os
import types

import numpy as np
from PIL import Image

from core.chunking import voronoi_chunks, chunk_centroid, initial_velocity, make_gravity_dir
from core.physics import simulate_step
from core.rendering import snapshot, apply_tint, build_dissolve_schedule, apply_frame_mask
from core.output import render_frames, save_frame_pngs, save_spritesheet, save_gif

# Gravity modes with no settle condition — pre-sim runs until motion dies out or MAX_SIM_TICKS.
NEVER_SETTLE_MODES = ("repulsor", "orbital", "noise", "vortex")

# Below these, a launched chunk counts as at rest for the early-exit check.
_REST_SPEED = 0.05   # px/tick
_REST_SPIN  = 0.25   # deg/tick


class RenderCancelled(Exception):
    """Raised by run_sprite when its cancel callback returns True."""


def build_params(cfg: dict, gif_bg_hex=None) -> types.SimpleNamespace:
    """Build the engine params namespace from a config dict.

    Every uppercase key in DEFAULT_CONFIG gets a value (cfg wins, else default),
    so the engine never sees a missing parameter. Extra uppercase keys in cfg
    (e.g. params.py's INPUT_DIR) are passed through untouched.
    """
    from utils.config import DEFAULT_CONFIG

    values = {k: v for k, v in DEFAULT_CONFIG.items() if k.isupper()}
    values.update({k: v for k, v in cfg.items() if k.isupper()})

    # Legacy configs stored DISSOLVE_MIN_PCT as a whole-number percent.
    if values["DISSOLVE_MIN_PCT"] > 1.0:
        values["DISSOLVE_MIN_PCT"] /= 100.0
    values["SPIN"] = float(values["SPIN"])

    use_bg = bool(cfg.get("gif_use_preview_bg", cfg.get("GIF_USE_PREVIEW_BG", False)))
    values["GIF_USE_PREVIEW_BG"] = use_bg
    values["GIF_BG_HEX"] = gif_bg_hex if use_bg else None
    return types.SimpleNamespace(**values)


def _init_states(arr, chunks, sprite_center, W, H, rng, p):
    launch_stagger = p.LAUNCH_STAGGER
    mass_variance  = p.CHUNK_MASS_VARIANCE
    gravity_mode   = p.GRAVITY_MODE

    states = {}
    for cid, pixels in chunks.items():
        centroid   = chunk_centroid(pixels).astype(float)
        vel        = initial_velocity(centroid, sprite_center, W, H, rng, p)
        spin       = rng.uniform(-p.SPIN, p.SPIN)
        mass_drag  = 1.0 + rng.uniform(-mass_variance, mass_variance)
        onset      = int(rng.uniform(0, launch_stagger * p.MAX_SIM_TICKS)) if launch_stagger > 0 else 0
        noise_seed = float(rng.random()) if gravity_mode == "noise" else 0.0
        states[cid] = {
            "pixels":     pixels,
            "colors":     arr[pixels[:, 0], pixels[:, 1]],
            "centroid":   centroid.copy(),
            "vel":        np.zeros(2) if onset > 0 else vel,
            "launch_vel": vel,
            "spin":       spin,
            "offset":     np.zeros(2),
            "angle":      0.0,
            "settled":    False,
            "mass_drag":  mass_drag,
            "onset":      onset,
            "tick":       0,
            "noise_seed": noise_seed,
        }
    return states


def _at_rest(s, check_spin):
    """True when a chunk can no longer change the picture on its own.

    Spin only counts when nothing in the sprite translates (shatter-in-place):
    otherwise a slowly decaying spin tail would stretch the pre-sim and squash
    the actual flight into the first frame or two.
    """
    if s["settled"]:
        return True
    if s["tick"] <= s["onset"]:
        return False  # still waiting to launch
    if float(np.linalg.norm(s["vel"])) >= _REST_SPEED:
        return False
    return not check_spin or abs(s["spin"]) < _REST_SPIN


def run_sprite(img, p, rng=None, cancel=None):
    """Run the full pipeline on one RGBA image. Returns a SimpleNamespace with:

    frames      list of PIL RGBA frames (frame mask already applied); [] if no opaque pixels
    states      final chunk states
    ticks       number of simulated ticks
    stop_reason "settled" | "at_rest" | "max_ticks"
    never_settles True when the gravity mode has no landing (runs until at rest or MAX_SIM_TICKS)

    cancel: optional no-arg callable (e.g. threading.Event.is_set), polled between sim
    ticks and between rendered frames; when it returns True, RenderCancelled is raised.
    Without it the result is identical — it never touches the RNG or the params.
    """
    def _check_cancel():
        if cancel is not None and cancel():
            raise RenderCancelled()

    img = img.convert("RGBA")
    arr = np.array(img)
    H, W = arr.shape[:2]
    if rng is None:
        rng = np.random.default_rng(p.SEED)

    opaque_coords = np.argwhere(arr[:, :, 3] > 0)
    if len(opaque_coords) == 0:
        return types.SimpleNamespace(frames=[], states={}, ticks=0, stop_reason="empty",
                                     never_settles=False)

    gravity_dir   = make_gravity_dir(p.GRAVITY_ANGLE)
    sprite_center = np.array([H / 2.0, W / 2.0])

    num_chunks = 1 if p.SINGLE_CHUNK else p.CHUNKS
    chunks = voronoi_chunks(opaque_coords, num_chunks, rng,
                            chunk_bias=p.CHUNK_BIAS,
                            chunk_bias_strength=p.CHUNK_BIAS_STRENGTH,
                            chunk_shape_stretch=p.CHUNK_SHAPE_STRETCH,
                            chunk_shape_angle=p.CHUNK_SHAPE_ANGLE)
    _check_cancel()
    states = _init_states(arr, chunks, sprite_center, W, H, rng, p)

    _check_cancel()
    apply_tint(states, arr, p, rng=rng)

    dissolve_fade_rgb = None
    dissolve_masks = None
    _check_cancel()
    if p.DISSOLVE and p.FRAMES >= 2:
        if p.DISSOLVE_FADE_COLOR is not None:
            h = p.DISSOLVE_FADE_COLOR.lstrip("#")
            dissolve_fade_rgb = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        dissolve_masks = build_dissolve_schedule(states, rng, H, W, p.FRAMES, p)

    never_settles = p.GRAVITY_STRENGTH == 0 or p.GRAVITY_MODE in NEVER_SETTLE_MODES

    tick_snapshots = [snapshot(states)]  # tick 0: at rest, before any motion
    stop_reason = "max_ticks"
    translated = False
    for _ in range(p.MAX_SIM_TICKS):
        _check_cancel()
        simulate_step(states, W, H, p, gravity_dir, sprite_center=sprite_center)
        tick_snapshots.append(snapshot(states))
        translated = translated or any(
            float(np.linalg.norm(s["offset"])) >= 0.5 for s in states.values())
        if not never_settles and all(s["settled"] for s in states.values()):
            stop_reason = "settled"
            break
        if all(_at_rest(s, check_spin=not translated) for s in states.values()):
            stop_reason = "at_rest"
            break

    frames = render_frames(states, tick_snapshots, img, H, W, p,
                           dissolve_masks=dissolve_masks,
                           dissolve_fade_rgb=dissolve_fade_rgb,
                           before_frame=_check_cancel)
    apply_frame_mask(frames, p)
    return types.SimpleNamespace(frames=frames, states=states,
                                 ticks=len(tick_snapshots) - 1, stop_reason=stop_reason,
                                 never_settles=never_settles)


def process_sprite_file(img_path, out_dir, stem, p, rng=None,
                        write_frames=True, write_sheet=True, write_gif=True):
    """Run the pipeline on a file and write the requested outputs. Returns the frames.

    `stem` names every file (see core.output.export_stem): <stem>_00.png …,
    <stem>_sheet.png, <stem>.gif.
    """
    with Image.open(img_path) as img:
        img.load()
        result = run_sprite(img, p, rng=rng)
    frames = result.frames
    if not frames:
        return frames
    if write_frames or write_sheet or write_gif:
        os.makedirs(out_dir, exist_ok=True)
    if write_frames:
        save_frame_pngs(frames, out_dir, stem)
    if write_sheet:
        save_spritesheet(frames, out_dir, stem, p)
    if write_gif:
        save_gif(frames, out_dir, stem, p)
    return frames
