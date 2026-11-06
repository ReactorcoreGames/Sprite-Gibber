import copy
import json
import pathlib

from utils.paths import (app_path, write_text_atomic, quarantine_corrupt,
                         resolve_user_path, list_pngs)

# Keys that are GUI/session state or the user's own export settings — never saved
# into a preset's params dict, and left untouched when a preset is loaded.
# FRAME_MASK* and the GIF timing keys (MS_PER_FRAME, HOLD_*) ARE preset params:
# presets tune their own pacing. Frame count, GIF scale and sheet layout are the
# user's (driven by their game engine), so they survive preset switches.
# Kept here (not in gui/) so presets_io.py can import it without a circular dependency.
GUI_ONLY_KEYS = {
    "SHEET_COLUMNS", "GIF_SCALE",
    "sprite_files", "export_dest", "export_folder", "active_preset",
    "zoom_level", "active_tab",
    "preview_lumi", "preview_colr", "preview_satu", "preview_checker",
    "gif_use_preview_bg", "save_frames", "save_spritesheet",
    "save_gif", "window_geometry",
    "FRAMES", "live_preview",
    # randomize checkbox states
    "rand_gravity_mode",
    "rand_gravity_angle", "rand_gravity_strength", "rand_velocity_motion",
    "rand_chunk_count", "rand_blast_mode", "rand_tint_colors",
    "rand_tint_opacity_bleed", "rand_tint_mode_anim", "rand_dissolve_pattern",
    "rand_dissolve_color", "rand_dissolve_min_fade",
    "rand_chunk_physics", "rand_gravity_ramp", "rand_chunk_shape",
    "rand_tint_advanced", "rand_tint_color_anim",
    "rand_dissolve_stagger", "rand_vary_current",
    "rand_mask_image", "rand_mask_softness", "rand_mask_anim", "rand_mask_fit",
}

DEFAULT_CONFIG = {
    # --- Physics / animation parameters (match params.py defaults) ---
    "SEED":             42,
    "FRAMES":           16,
    "CHUNKS":           16,
    "EXPLODE":          2.5,
    "GRAVITY_STRENGTH": 1.2,
    "GRAVITY_ANGLE":    180,
    "DRAG":             0.18,
    "SPREAD":           1.2,
    "SPIN":             8.0,
    "EDGE_ZONE":        6,
    "MAX_SIM_TICKS":    500,
    "BLAST_MODE":       "explode",
    "GRAVITY_MODE":     "directional",  # "directional"|"centripetal"|"repulsor"|"orbital"|"vortex"|"noise"
    "CHUNK_MASS_VARIANCE": 0.0,
    "BOUNCE":           0.0,
    "SPIN_DRAG":        0.0,
    "LAUNCH_STAGGER":   0.0,
    "SINGLE_CHUNK":     False,
    "GRAVITY_RAMP_TICKS": 0,      # ticks of free-flight before centripetal/vortex/orbital force activates; 0 = immediate
    "CHUNK_BIAS":          "none",
    "CHUNK_BIAS_STRENGTH": 0.0,
    "CHUNK_SHAPE_STRETCH": 1.0,
    "CHUNK_SHAPE_ANGLE":   0,

    # --- Tint ---
    "TINT_BLEND_MODE":        "unidirectional",  # "unidirectional" | "bidirectional"
    "TINT_MODE":              "chunks",          # "chunks" | "edges"
    "TINT_COLOR_OUTER":       "#660000",         # outer/border color
    "TINT_COLOR_INNER":       "#FF2222",         # inner/center color
    "TINT_DEPTH_OUTER":       0.12,              # outer front reach (fraction of sqrt(opaque px)); 0.0 = disabled
    "TINT_DEPTH_INNER":       0.12,              # inner front reach (fraction of sqrt(opaque px)); bidir only
    "TINT_OPACITY_OUTER":     0.8,               # color strength at border
    "TINT_OPACITY_INNER":     0.8,               # color strength at centroid; bidir only
    "TINT_JITTER_OUTER":      0.3,               # raggedness of outer front edge
    "TINT_JITTER_INNER":      0.3,               # raggedness of inner front edge; bidir only
    "TINT_ALPHA_BLEED_OUTER": 0.0,               # transparency at border edge
    "TINT_ALPHA_BLEED_INNER": 0.0,               # transparency at centroid center; bidir only
    "TINT_COLLISION":         "blend",           # "blend" | "outer_wins" | "inner_wins"; bidir only
    "TINT_BLEND":             0.5,               # collision meeting-point: 0=inner wins, 1=outer wins; bidir only
    "TINT_SINGLE_COLOR":      False,             # if True, outer color is ignored
    "TINT_ANIM":              "instant",         # "instant" | "linear" | "early" | "late" | "pulse" | "per_chunk"
    "TINT_COLOR_OUTER_END":   None,              # hex string or None; outer color shifts to this by last frame
    "TINT_COLOR_INNER_END":   None,              # hex string or None; inner color shifts to this by last frame
    "TINT_COLOR_ANIM_CURVE":  1.0,               # gamma for color animation: 1.0=linear, <1=fast-out, >1=slow-out
    "TINT_NOISE":             0.0,               # 0.0–1.0: large-scale noise modulates BFS depth cutoff
    "TINT_SATURATION_SHIFT":  0.0,               # -1.0–1.0: HSV saturation shift after tinting; 0 = no change
    "TINT_GRAIN":             0.0,               # 0.0–1.0: per-pixel ±brightness grain after tinting; 0 = off

    # --- Dissolve ---
    "DISSOLVE":              False,
    "DISSOLVE_MIN_PCT":      0.01,    # float fraction (0.001–1.0); GUI displays as integer percent
    "DISSOLVE_PATTERN":      "random",
    "DISSOLVE_DIRECTION":    180,
    "DISSOLVE_CURVE":        1.0,
    "DISSOLVE_CHUNK_STAGGER": 0.0,   # 0.0–1.0: random per-chunk onset delay
    "DISSOLVE_FADE_COLOR":   None,
    "DISSOLVE_FADE_STRENGTH": 0.8,

    # --- Frame Mask ---
    "FRAME_MASK":          None,      # filename from assets/masks/, or None to disable
    "FRAME_MASK_FIT":      "stretch", # "stretch" | "fit" | "crop_center"
    "FRAME_MASK_SOFTNESS": 0,         # Gaussian blur radius; 0 = hard edge
    "FRAME_MASK_FLIP":     False,     # flip mask vertically
    "FRAME_MASK_MIRROR":   False,     # mirror mask horizontally
    "FRAME_MASK_ROTATE90": False,     # rotate mask 90 degrees clockwise
    "FRAME_MASK_ANIM":     "instant", # "instant" | "linear" | "early" | "late" | "pulse"

    # --- Output ---
    "SHEET_COLUMNS":  0,
    "GIF_SCALE":      4,
    "MS_PER_FRAME":   80,            # ms per middle frame, GIF and preview playback (min 10, step 10)
    "HOLD_FIRST_MS":  500,           # display time of first frame in ms
    "HOLD_LAST_MS":   800,           # display time of last frame in ms

    # --- GUI-only state ---
    "sprite_files":    [],       # absolute paths of the sprites in the Sprites & Export list
    "export_dest":     "beside", # "beside" = <sprite folder>/gibbed/ | "folder" = export_folder
    "export_folder":   None,     # chosen export folder (used when export_dest == "folder")
    "active_preset":   None,
    "zoom_level":      1,
    "live_preview":    True,     # re-render the preview automatically after each change
    "active_tab":      0,
    "preview_lumi":    2,        # 0=White 1=Light 2=Mid 3=Dark 4=Black
    "preview_colr":    None,     # None or hue key e.g. "Red"
    "preview_satu":    "Lo",     # "Lo" or "Hi"
    "preview_checker": True,
    "gif_use_preview_bg": False,
    "save_frames":     True,
    "save_spritesheet": True,
    "save_gif":        True,
    "window_geometry": None,

    # --- Randomize checkbox states ---
    "rand_gravity_mode":       False,
    "rand_gravity_angle":      False,
    "rand_gravity_strength":   False,
    "rand_velocity_motion":    True,
    "rand_chunk_count":        True,
    "rand_blast_mode":         True,
    "rand_gravity_ramp":       False,
    "rand_chunk_physics":      False,
    "rand_chunk_shape":        False,
    "rand_tint_colors":        True,
    "rand_tint_opacity_bleed": False,
    "rand_tint_mode_anim":     False,
    "rand_tint_advanced":      False,
    "rand_tint_color_anim":    False,
    "rand_dissolve_pattern":   False,
    "rand_dissolve_color":     False,
    "rand_dissolve_min_fade":  False,
    "rand_dissolve_stagger":   False,
    "rand_vary_current":       False,

    # --- Randomize mask checkbox states ---
    "rand_mask_image":     False,
    "rand_mask_softness":  False,
    "rand_mask_anim":      False,
    "rand_mask_fit":       False,
}


def _config_path(filename: str) -> pathlib.Path:
    return app_path(filename)


def read_json_file(path, expected_type):
    """Load a JSON file; None if it doesn't exist.

    An unreadable or wrongly-shaped file is renamed aside (and logged) rather than
    treated as empty, so the next save can't silently destroy the user's data.
    """
    from utils.log import log
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, expected_type):
            return data
        reason = f"expected {expected_type.__name__}, got {type(data).__name__}"
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        reason = str(exc)
    try:
        moved = quarantine_corrupt(path)
        log.warning("Could not read %s (%s); moved it to %s", path, reason, moved.name)
    except OSError:
        log.warning("Could not read %s (%s)", path, reason)
    return None


# Keys from the old fixed input/output-folder workflow and the old separate
# preview speed (playback now uses the GIF timing); dropped on load.
_LEGACY_KEYS = ("input_folder", "output_folder", "OVERWRITE", "PREVIEW_MS_PER_FRAME")


def load_config() -> dict:
    data = read_json_file(_config_path("config.json"), dict)
    merged = copy.deepcopy(DEFAULT_CONFIG)
    if data:
        merged.update(data)
        # Migrate the old fixed input folder into the sprite list, once.
        if "sprite_files" not in data and data.get("input_folder"):
            try:
                merged["sprite_files"] = list_pngs(resolve_user_path(data["input_folder"]))
            except OSError:
                pass
    for key in _LEGACY_KEYS:
        merged.pop(key, None)
    if not isinstance(merged.get("sprite_files"), list):
        merged["sprite_files"] = []
    return merged


def save_config(config: dict) -> None:
    write_text_atomic(_config_path("config.json"), json.dumps(config, indent=2))
