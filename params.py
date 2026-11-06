PRESET = None  # e.g. "*.Blood-Explode-terra" — set to None for full manual control

SEED             = 42
FRAMES           = 16
CHUNKS           = 16
EXPLODE          = 2.5    # initial outward speed scale (pixels/frame)
GRAVITY_STRENGTH = 1.2    # acceleration along gravity direction (pixels/frame²); 0 = zero-gravity / drift only
GRAVITY_ANGLE    = 180    # degrees: 0=up, 90=right, 180=down, 270=left
DRAG             = 0.18   # fraction of velocity lost per frame
SPREAD           = 1.2    # randomness spread multiplier on velocity direction
SPIN             = 8.0    # max rotation rate (degrees/frame)
EDGE_ZONE        = 6      # pixels from each wall where velocity is progressively killed
INPUT_DIR        = "input"
OUTPUT_DIR       = "output"
MAX_SIM_TICKS    = 500    # safety cap: stop pre-sim if chunks never fully settle

BLAST_MODE        = "explode"  # "explode" | "implode" | "hollow_circle" | "filled_circle" | "shatter" | "x_split" | "vertical_split" | "horizontal_split" | "burst"
GRAVITY_MODE      = "directional"  # "directional"|"centripetal"|"repulsor"|"orbital"|"vortex"|"noise"

CHUNK_MASS_VARIANCE  = 0.0   # 0.0–1.0: random per-chunk drag multiplier spread; 0 = uniform mass
BOUNCE               = 0.0   # 0.0–1.0: velocity restitution on settle-plane collision; 0 = dead-stop
SPIN_DRAG            = 0.0   # 0.0–1.0: per-tick spin decay multiplier; 0 = no decay
LAUNCH_STAGGER       = 0.0   # 0.0–1.0: random onset delay spread across sim ticks; 0 = simultaneous
SINGLE_CHUNK         = False # if True, treat entire sprite as one Voronoi region (ignores CHUNKS)
GRAVITY_RAMP_TICKS   = 0     # ticks of free-flight before centripetal/vortex/orbital force activates; 0 = immediate

CHUNK_BIAS          = "none"  # "none" | "halves-h" | "halves-v" | "core" | "shell" | "quadrants"
CHUNK_BIAS_STRENGTH = 0.0     # 0.0–1.0: 0 = fully random, 1 = strict zone enforcement; ignored when CHUNK_BIAS = "none"

CHUNK_SHAPE_STRETCH = 1.0   # 1.0–10.0: axis stretch factor; 1.0 = standard Euclidean (no effect)
CHUNK_SHAPE_ANGLE   = 0     # 0–359: stretch axis direction in degrees; 0=vertical slivers, 90=horizontal strips

TINT_BLEND_MODE        = "unidirectional"  # "unidirectional" | "bidirectional"
TINT_MODE              = "chunks"          # "chunks" | "edges"
TINT_COLOR_OUTER       = "#660000"         # outer/border color
TINT_COLOR_INNER       = "#FF2222"         # inner/center color
TINT_DEPTH_OUTER       = 0.12             # outer front reach (fraction of sqrt(opaque px))
TINT_DEPTH_INNER       = 0.12             # inner front reach (fraction of sqrt(opaque px)); bidir only
TINT_OPACITY_OUTER     = 0.8              # color strength at border
TINT_OPACITY_INNER     = 0.8              # color strength at centroid; bidir only
TINT_JITTER_OUTER      = 0.3              # raggedness of outer front edge
TINT_JITTER_INNER      = 0.3              # raggedness of inner front edge; bidir only
TINT_ALPHA_BLEED_OUTER = 0.0              # transparency at border edge
TINT_ALPHA_BLEED_INNER = 0.0              # transparency at centroid center; bidir only
TINT_COLLISION         = "blend"          # "blend" | "outer_wins" | "inner_wins"; bidir only
TINT_BLEND             = 0.5              # collision meeting-point: 0=inner wins, 1=outer wins; bidir only
TINT_SINGLE_COLOR      = False            # if True, outer color is ignored (uses inner color only)
TINT_ANIM              = "instant"        # "instant" | "linear" | "early" | "late" | "pulse" | "per_chunk"
TINT_COLOR_OUTER_END   = None             # hex string or None; if set, outer color shifts to this by last frame
TINT_COLOR_INNER_END   = None             # hex string or None; if set, inner color shifts to this by last frame
TINT_COLOR_ANIM_CURVE  = 1.0             # gamma for color animation: 1.0=linear, <1=fast-out, >1=slow-out
TINT_NOISE             = 0.0             # 0.0–1.0: large-scale noise modulates BFS depth cutoff per pixel
TINT_SATURATION_SHIFT  = 0.0             # -1.0–1.0: HSV saturation shift after tinting; 0 = no change
TINT_GRAIN             = 0.0             # 0.0–1.0: per-pixel ±brightness grain after tinting (texture); 0 = off

DISSOLVE            = False
DISSOLVE_MIN_PCT    = 0.01          # fraction of opaque pixels to keep in last frame
DISSOLVE_PATTERN    = "random"      # "random" | "noise" | "directional" | "centrifugal" | "centripetal" | "chunks" | "gravity_aligned"
DISSOLVE_DIRECTION  = 180           # degrees, same convention as GRAVITY_ANGLE; only used for "directional"
DISSOLVE_CURVE      = 1.0           # gamma: 1.0=linear, <1.0=fast-out, >1.0=slow-out
DISSOLVE_CHUNK_STAGGER = 0.0        # 0.0–1.0: random per-chunk onset delay; 0=all chunks dissolve together, 1=fully sequential
DISSOLVE_FADE_COLOR    = None       # hex string e.g. "#FFFFFF" or None
DISSOLVE_FADE_STRENGTH = 0.8        # 0.0–1.0: blend strength at the frame before dropout

FRAME_MASK          = None       # filename from assets/masks/, or None to disable
FRAME_MASK_FIT      = "stretch"  # "stretch" | "fit" | "crop_center"
FRAME_MASK_SOFTNESS = 0          # Gaussian blur radius applied to mask; 0 = hard edge
FRAME_MASK_FLIP     = False      # flip mask vertically
FRAME_MASK_MIRROR   = False      # mirror mask horizontally
FRAME_MASK_ROTATE90 = False      # rotate mask 90 degrees clockwise
FRAME_MASK_ANIM     = "instant"  # "instant" | "linear" | "early" | "late" | "pulse"

SHEET_COLUMNS  = 0     # 0 = all frames in one row; N = wrap at N columns
GIF_SCALE      = 4     # integer 1–8; nearest-neighbour upscale for GIF output
MS_PER_FRAME   = 80    # milliseconds per middle frame (rounded to nearest 10 ms in GIF)
HOLD_FIRST_MS  = 500   # display time of first frame in ms
HOLD_LAST_MS   = 800   # display time of last frame in ms
OVERWRITE      = True  # False = skip sprites whose output folder already exists

if PRESET is not None:
    from presets import PRESETS as _PRESETS
    import sys as _sys
    _bundle = _PRESETS[PRESET]["params"]
    _mod = _sys.modules[__name__]
    for _k, _v in _bundle.items():
        setattr(_mod, _k, _v)
    del _mod, _bundle, _k, _v, _PRESETS, _sys
