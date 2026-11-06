import random
import tkinter as tk
import tkinter.ttk as _tk_ttk

import ttkbootstrap as ttk

from utils.config import DEFAULT_CONFIG
from gui.theme import PALETTE, FONT_BODY_BOLD, FONT_SMALL, Tooltip as _Tooltip

_BLAST_OPTIONS = [
    "explode", "implode", "hollow_circle", "filled_circle",
    "shatter", "x_split", "vertical_split", "horizontal_split", "burst",
]
_GRAVITY_MODE_OPTIONS     = ["directional", "centripetal", "repulsor", "orbital", "vortex", "noise"]
_TINT_MODE_OPTIONS        = ["chunks", "edges"]
_TINT_ANIM_OPTIONS        = ["instant", "linear", "early", "late", "pulse", "per_chunk"]
_DISSOLVE_PATTERN_OPTIONS = [
    "random", "noise", "directional", "centrifugal", "centripetal",
    "chunks", "gravity_aligned",
]
_MASK_ANIM_OPTIONS = ["instant", "linear", "early", "late", "pulse"]
_MASK_FIT_OPTIONS  = ["stretch", "fit", "crop_center"]


_VARY_AMOUNT = 0.25     # "Vary current": move this far from the current value toward a fresh roll
_VARY_SWITCH = 0.2      # "Vary current": chance a choice (mode, pattern...) switches at all


def _rand_color() -> str:
    return "#%06x" % random.randint(0, 0xFFFFFF)


def _nudge(cur, fresh):
    """Blend a fresh random roll into the current value (vary-current mode)."""
    if cur is None or fresh is None or isinstance(fresh, bool) or isinstance(cur, bool):
        return fresh if random.random() < _VARY_SWITCH else cur
    if isinstance(fresh, (int, float)) and isinstance(cur, (int, float)):
        v = cur + (fresh - cur) * _VARY_AMOUNT
        return int(round(v)) if isinstance(fresh, int) else round(v, 3)
    if (isinstance(fresh, str) and isinstance(cur, str) and fresh.startswith("#")
            and cur.startswith("#") and len(fresh) == len(cur) == 7):
        a = [int(cur[i:i + 2], 16) for i in (1, 3, 5)]
        b = [int(fresh[i:i + 2], 16) for i in (1, 3, 5)]
        return "#" + "".join("%02x" % round(x + (y - x) * _VARY_AMOUNT) for x, y in zip(a, b))
    return fresh if random.random() < _VARY_SWITCH else cur


class RandomizerPanel(_tk_ttk.LabelFrame):
    def __init__(self, parent, config: dict, app, notify_dirty_cb):
        super().__init__(parent, text="Randomize", padding=8)
        self.columnconfigure(0, weight=1)
        self._config = config
        self._app = app
        self._notify_dirty_cb = notify_dirty_cb

        self._rand_chunk_physics_var    = tk.BooleanVar()
        self._rand_gravity_ramp_var     = tk.BooleanVar()
        self._rand_chunk_shape_var      = tk.BooleanVar()
        self._rand_tint_advanced_var    = tk.BooleanVar()
        self._rand_tint_color_anim_var  = tk.BooleanVar()
        self._rand_dissolve_stagger_var = tk.BooleanVar()

        self._rand_gravity_mode_var       = tk.BooleanVar()
        self._rand_gravity_angle_var      = tk.BooleanVar()
        self._rand_gravity_strength_var   = tk.BooleanVar()
        self._rand_velocity_motion_var    = tk.BooleanVar()
        self._rand_chunk_count_var        = tk.BooleanVar()
        self._rand_blast_mode_var         = tk.BooleanVar()
        self._rand_tint_colors_var        = tk.BooleanVar()
        self._rand_tint_opacity_bleed_var = tk.BooleanVar()
        self._rand_tint_mode_anim_var     = tk.BooleanVar()
        self._rand_dissolve_pattern_var   = tk.BooleanVar()
        self._rand_dissolve_color_var     = tk.BooleanVar()
        self._rand_dissolve_min_fade_var  = tk.BooleanVar()

        self._rand_mask_image_var    = tk.BooleanVar()
        self._rand_mask_softness_var = tk.BooleanVar()
        self._rand_mask_anim_var     = tk.BooleanVar()
        self._rand_mask_fit_var      = tk.BooleanVar()
        self._vary_var               = tk.BooleanVar()

        self._build()

    def _build(self):
        r = 0

        # ── Physics ────────────────────────────────────────────────────
        _phys_hdr = ttk.Label(self, text="Physics", font=FONT_BODY_BOLD)
        _phys_hdr.grid(row=r, column=0, sticky="w", pady=(0, 2))
        _Tooltip(_phys_hdr,
                 "Randomizes physics parameters.\n\n"
                 "Tip: Single Chunk mode (on the Physics tab) is a manual toggle — "
                 "enable it before randomizing if you want the whole sprite to move as one piece.")
        r += 1

        _phys_items = [
            ("Gravity angle",     self._rand_gravity_angle_var,    "rand_gravity_angle",
             "Picks a random cardinal gravity direction — down, up, left, or right.\nDiagonal angles are excluded so the result always has a clean settle wall."),
            ("Gravity strength",  self._rand_gravity_strength_var, "rand_gravity_strength",
             "Picks a random gravity pull strength (mostly 0.3–3.0, sometimes 0).\n0 = zero-gravity drift; higher values make chunks crash down faster."),
            ("Gravity mode",      self._rand_gravity_mode_var,     "rand_gravity_mode",
             "Randomly picks a gravity mode: directional, centripetal, repulsor, orbital, vortex, or noise.\nCentripetal/vortex converge to center; repulsor/orbital scatter outward; noise gives organic wandering drift."),
            ("Velocity & motion", self._rand_velocity_motion_var,  "rand_velocity_motion",
             "Randomizes outward speed, drag, directional spread, spin rate, and edge damping zone.\nThese together control how energetically and erratically chunks fly."),
            ("Chunk count",       self._rand_chunk_count_var,      "rand_chunk_count",
             "Picks a random number of chunks the sprite is split into (3–40).\nFewer chunks = big beefy gibs; more chunks = fine shrapnel.\nThis range is intentionally capped at 40 so each roll looks visually distinct on small sprites."),
            ("Blast mode",        self._rand_blast_mode_var,       "rand_blast_mode",
             "Picks a random blast pattern — e.g. explode outward, implode inward, ring, shatter, split by axis, burst, etc."),
            ("Mass, bounce & stagger", self._rand_chunk_physics_var, "rand_chunk_physics",
             "Randomizes per-chunk mass variation, bounce restitution on landing, spin decay rate, and launch stagger.\nTogether these add weight and personality to individual chunks."),
            ("Gravity ramp ticks",  self._rand_gravity_ramp_var,   "rand_gravity_ramp",
             "Randomizes the free-flight window (0–20 ticks) before centripetal / vortex / orbital force activates.\nOnly meaningful when Gravity Mode is centripetal, vortex, or orbital."),
            ("Chunk shape & bias", self._rand_chunk_shape_var,     "rand_chunk_shape",
             "Randomly picks a chunk zone bias (e.g. core vs shell vs halves) and an axis-stretch factor that makes chunks elongated slivers or horizontal strips instead of blobby squares."),
        ]
        for text, var, key, tip in _phys_items:
            cb = ttk.Checkbutton(
                self, text=text, variable=var, bootstyle="primary",
                command=lambda k=key, v=var: self._save_rand(k, v),
            )
            cb.grid(row=r, column=0, sticky="w", padx=(16, 0))
            _Tooltip(cb, tip)
            r += 1

        # ── Tint ───────────────────────────────────────────────────────
        ttk.Separator(self, orient="horizontal").grid(
            row=r, column=0, sticky="ew", pady=(6, 4))
        r += 1

        _tint_hdr = ttk.Label(self, text="Tint", font=FONT_BODY_BOLD)
        _tint_hdr.grid(row=r, column=0, sticky="w", pady=(0, 2))
        _Tooltip(_tint_hdr,
                 "Randomizes tint / wound-bleed parameters.\n\n"
                 "Enable Tint is controlled on the Tint tab (sets Outer Depth to 0 when off). "
                 "If 'Mode & animation' is checked, the randomizer will set a new Outer Depth "
                 "and may turn tint back on. Other tint sub-options only affect appearance if "
                 "tint is already enabled.")
        r += 1

        _tint_items = [
            ("Colors",                self._rand_tint_colors_var,        "rand_tint_colors",
             "Picks two random colours for the wound/tint effect — one for the chunk border, one for the inner edge."),
            ("Opacity & border fade", self._rand_tint_opacity_bleed_var, "rand_tint_opacity_bleed",
             "Randomizes how strongly the tint colour is painted on, and how transparent the chunk edges become."),
            ("Mode & animation",      self._rand_tint_mode_anim_var,     "rand_tint_mode_anim",
             "Randomly picks whether tint follows chunk borders or the sprite's outer silhouette, plus how the tint grows across frames."),
            ("Blend mode, noise & saturation", self._rand_tint_advanced_var, "rand_tint_advanced",
             "Randomly picks unidirectional vs bidirectional tint, whether a single colour is used, a noise warp amount for organic blob edges, and a saturation shift (desaturate or oversaturate the tinted pixels)."),
            ("Color animation",       self._rand_tint_color_anim_var,    "rand_tint_color_anim",
             "Randomly picks an end colour for the tint to animate toward over the frames — or sets it to none — and picks the animation curve speed.\nTip: color animation is most visible when Dissolve is also enabled — otherwise the shift only shows on settled chunks."),
        ]
        for text, var, key, tip in _tint_items:
            cb = ttk.Checkbutton(
                self, text=text, variable=var, bootstyle="primary",
                command=lambda k=key, v=var: self._save_rand(k, v),
            )
            cb.grid(row=r, column=0, sticky="w", padx=(16, 0))
            _Tooltip(cb, tip)
            r += 1

        # ── Dissolve ───────────────────────────────────────────────────
        ttk.Separator(self, orient="horizontal").grid(
            row=r, column=0, sticky="ew", pady=(6, 4))
        r += 1

        _dissolve_hdr = ttk.Label(self, text="Dissolve", font=FONT_BODY_BOLD)
        _dissolve_hdr.grid(row=r, column=0, sticky="w", pady=(0, 2))
        _Tooltip(_dissolve_hdr,
                 "Randomizes dissolve parameters.\n\n"
                 "Tip: Dissolve must be switched ON in the Dissolve tab to see any effect — "
                 "these settings only control how it behaves once enabled.")
        r += 1

        _dissolve_items = [
            ("Pattern, direction & timing", self._rand_dissolve_pattern_var, "rand_dissolve_pattern",
             "Randomly picks the pixel dropout pattern (e.g. random, noise, directional, chunks, gravity-aligned), a random direction angle, and the timing curve that controls whether pixels vanish early or late."),
            ("Dissolve color",              self._rand_dissolve_color_var,   "rand_dissolve_color",
             "Randomly picks a colour that pixels shift toward just before they disappear — or sets it to none (transparent dropout)."),
            ("Min % & fade strength",       self._rand_dissolve_min_fade_var, "rand_dissolve_min_fade",
             "Randomizes how many pixels survive to the last frame (as a percentage), and how strongly pixels shift toward the dissolve colour before vanishing."),
            ("Chunk stagger",               self._rand_dissolve_stagger_var,  "rand_dissolve_stagger",
             "Randomly picks how staggered each chunk's dissolve onset is — 0 means all chunks dissolve together, 1 means fully sequential one-by-one."),
        ]
        for text, var, key, tip in _dissolve_items:
            cb = ttk.Checkbutton(
                self, text=text, variable=var, bootstyle="primary",
                command=lambda k=key, v=var: self._save_rand(k, v),
            )
            cb.grid(row=r, column=0, sticky="w", padx=(16, 0))
            _Tooltip(cb, tip)
            r += 1

        # ── Mask ───────────────────────────────────────────────────────
        ttk.Separator(self, orient="horizontal").grid(
            row=r, column=0, sticky="ew", pady=(6, 4))
        r += 1

        _mask_hdr = ttk.Label(self, text="Mask", font=FONT_BODY_BOLD)
        _mask_hdr.grid(row=r, column=0, sticky="w", pady=(0, 2))
        _Tooltip(_mask_hdr,
                 "Randomizes frame mask parameters.\n\n"
                 "Note: mask image randomization picks from whatever PNG files are currently "
                 "in assets/masks/. If the folder is empty, mask is set to None.")
        r += 1

        _mask_items = [
            ("Mask image, flip & mirror", self._rand_mask_image_var,    "rand_mask_image",
             "Picks a random mask image from assets/masks/ (or None), and randomizes vertical flip and horizontal mirror."),
            ("Mask softness",             self._rand_mask_softness_var,  "rand_mask_softness",
             "Randomizes the Gaussian blur radius applied to the mask edge (0–6)."),
            ("Mask animation",            self._rand_mask_anim_var,      "rand_mask_anim",
             "Picks a random mask opacity animation curve (instant/linear/early/late/pulse)."),
            ("Mask fit mode",             self._rand_mask_fit_var,       "rand_mask_fit",
             "Randomly picks how the mask image is scaled to the canvas (stretch/fit/crop_center)."),
        ]
        for text, var, key, tip in _mask_items:
            cb = ttk.Checkbutton(
                self, text=text, variable=var, bootstyle="primary",
                command=lambda k=key, v=var: self._save_rand(k, v),
            )
            cb.grid(row=r, column=0, sticky="w", padx=(16, 0))
            _Tooltip(cb, tip)
            r += 1

        # ── Button ─────────────────────────────────────────────────────
        ttk.Separator(self, orient="horizontal").grid(
            row=r, column=0, sticky="ew", pady=(8, 6))
        r += 1

        vary_cb = ttk.Checkbutton(
            self, text="Vary current settings", variable=self._vary_var,
            bootstyle="primary",
            command=lambda: self._save_rand("rand_vary_current", self._vary_var),
        )
        vary_cb.grid(row=r, column=0, sticky="w", pady=(0, 4))
        _Tooltip(vary_cb,
                 "On: nudge the current values (e.g. the loaded preset) a little toward a "
                 "random roll, and only sometimes switch modes/patterns - good for "
                 "variations of an effect you like.\nOff: roll the ticked settings from scratch.")
        r += 1

        rand_btn = ttk.Button(
            self, text="Randomize",
            bootstyle="primary",
            command=self._on_randomize,
        )
        rand_btn.grid(row=r, column=0, sticky="ew", pady=(0, 2))
        _Tooltip(rand_btn,
                 "Roll random values for all ticked categories above, apply them, and refresh the preview (right away in Live mode).")

    def _save_rand(self, key, var):
        self._config[key] = bool(var.get())
        self._app.save_config()

    def _on_randomize(self):
        updates = self._roll()
        if not updates:
            return
        if self._vary_var.get():
            updates = {k: _nudge(self._config.get(k), v) for k, v in updates.items()}
        self._config.update(updates)
        self._app.save_config()
        self._app._refresh_all_tabs()
        # Same path as any other setting change: live mode renders once after the
        # debounce, paused/off mode just marks the preview stale.
        if hasattr(self._app, "preview_panel"):
            self._app.preview_panel.set_dirty(True)
        else:
            self._notify_dirty_cb(True)

    def _roll(self) -> dict:
        """Fresh random values for every ticked category."""
        updates = {}

        if self._rand_gravity_angle_var.get():
            updates["GRAVITY_ANGLE"] = random.choice([0, 90, 180, 270])

        if self._rand_gravity_strength_var.get():
            updates["GRAVITY_STRENGTH"] = 0.0 if random.random() < 0.1 else round(random.uniform(0.3, 3.0), 1)

        if self._rand_gravity_mode_var.get():
            updates["GRAVITY_MODE"] = random.choice(_GRAVITY_MODE_OPTIONS)

        if self._rand_velocity_motion_var.get():
            updates["EXPLODE"]       = round(random.uniform(1.0, 6.0), 1)
            updates["DRAG"]          = round(random.uniform(0.0, 0.15), 2)
            updates["SPREAD"]        = round(random.uniform(0.2, 1.5), 2)
            updates["SPIN"]          = random.randint(0, 20)
            updates["EDGE_ZONE"]     = random.randint(0, 8)

        if self._rand_chunk_count_var.get():
            updates["CHUNKS"] = random.randint(3, 40)

        if self._rand_blast_mode_var.get():
            updates["BLAST_MODE"] = random.choice(_BLAST_OPTIONS)

        if self._rand_chunk_physics_var.get():
            updates["CHUNK_MASS_VARIANCE"] = round(random.uniform(0.0, 0.8), 2)
            updates["BOUNCE"]              = round(random.uniform(0.0, 0.6), 2)
            updates["SPIN_DRAG"]           = round(random.uniform(0.0, 0.5), 2)
            updates["LAUNCH_STAGGER"]      = round(random.uniform(0.0, 0.15), 2)

        if self._rand_gravity_ramp_var.get():
            updates["GRAVITY_RAMP_TICKS"] = random.randint(0, 20)

        if self._rand_chunk_shape_var.get():
            updates["CHUNK_BIAS"] = random.choice(
                ["none", "halves-h", "halves-v", "core", "shell", "quadrants"])
            updates["CHUNK_BIAS_STRENGTH"] = round(random.uniform(0.3, 1.0), 2)
            if random.random() < 0.7:
                updates["CHUNK_SHAPE_STRETCH"] = round(random.uniform(1.5, 8.0), 1)
                updates["CHUNK_SHAPE_ANGLE"]   = random.randint(0, 359)
            else:
                updates["CHUNK_SHAPE_STRETCH"] = 1.0
                updates["CHUNK_SHAPE_ANGLE"]   = 0

        if self._rand_tint_colors_var.get():
            updates["TINT_COLOR_OUTER"] = _rand_color()
            updates["TINT_COLOR_INNER"] = _rand_color()

        if self._rand_tint_opacity_bleed_var.get():
            updates["TINT_OPACITY_OUTER"]     = round(random.uniform(0.4, 1.0), 2)
            updates["TINT_OPACITY_INNER"]     = round(random.uniform(0.4, 1.0), 2)
            updates["TINT_ALPHA_BLEED_OUTER"] = round(random.uniform(0.0, 0.5), 2)
            updates["TINT_ALPHA_BLEED_INNER"] = round(random.uniform(0.0, 0.5), 2)

        if self._rand_tint_mode_anim_var.get():
            updates["TINT_MODE"]         = random.choice(_TINT_MODE_OPTIONS)
            updates["TINT_JITTER_OUTER"] = round(random.uniform(0.0, 0.6), 2)
            updates["TINT_JITTER_INNER"] = round(random.uniform(0.0, 0.6), 2)
            updates["TINT_BLEND"]        = round(random.uniform(0.2, 0.8), 2)
            updates["TINT_ANIM"]         = random.choice(_TINT_ANIM_OPTIONS)
            updates["TINT_DEPTH_OUTER"]  = round(random.uniform(0.05, 0.4), 3)
            updates["TINT_DEPTH_INNER"]  = round(random.uniform(0.05, 0.4), 3)

        if self._rand_tint_advanced_var.get():
            updates["TINT_BLEND_MODE"]       = random.choice(["unidirectional", "bidirectional"])
            updates["TINT_SINGLE_COLOR"]     = random.random() < 0.2
            updates["TINT_NOISE"]            = round(random.uniform(0.0, 0.7), 2)
            updates["TINT_SATURATION_SHIFT"] = round(random.uniform(-0.5, 0.5), 2)
            updates["TINT_GRAIN"]            = round(random.uniform(0.0, 0.3), 2) if random.random() < 0.5 else 0.0

        if self._rand_tint_color_anim_var.get():
            updates["TINT_COLOR_OUTER_END"] = (
                _rand_color() if random.random() < 0.5 else None)
            updates["TINT_COLOR_INNER_END"] = (
                "#%06x" % random.randint(0, 0xFFFFFF) if random.random() < 0.5 else None)
            updates["TINT_COLOR_ANIM_CURVE"] = round(random.uniform(0.3, 2.5), 1)

        if self._rand_dissolve_pattern_var.get():
            updates["DISSOLVE_PATTERN"]   = random.choice(_DISSOLVE_PATTERN_OPTIONS)
            updates["DISSOLVE_DIRECTION"] = random.randint(0, 360)
            updates["DISSOLVE_CURVE"]     = round(random.uniform(0.4, 2.5), 1)

        if self._rand_dissolve_color_var.get():
            if random.random() < 0.5:
                updates["DISSOLVE_FADE_COLOR"] = None
            else:
                updates["DISSOLVE_FADE_COLOR"] = _rand_color()

        if self._rand_dissolve_min_fade_var.get():
            updates["DISSOLVE_MIN_PCT"]       = random.randint(1, 25) / 100.0
            updates["DISSOLVE_FADE_STRENGTH"] = round(random.uniform(0.0, 1.0), 2)

        if self._rand_dissolve_stagger_var.get():
            updates["DISSOLVE_CHUNK_STAGGER"] = round(random.uniform(0.0, 1.0), 2)

        if self._rand_mask_image_var.get():
            from gui.tabs.mask import list_mask_files
            mask_files = list_mask_files()
            updates["FRAME_MASK"]          = random.choice([None] + mask_files) if mask_files else None
            updates["FRAME_MASK_FLIP"]     = random.random() < 0.3
            updates["FRAME_MASK_MIRROR"]   = random.random() < 0.3
            updates["FRAME_MASK_ROTATE90"] = random.random() < 0.3

        if self._rand_mask_softness_var.get():
            updates["FRAME_MASK_SOFTNESS"] = random.randint(0, 6)

        if self._rand_mask_anim_var.get():
            updates["FRAME_MASK_ANIM"] = random.choice(_MASK_ANIM_OPTIONS)

        if self._rand_mask_fit_var.get():
            updates["FRAME_MASK_FIT"] = random.choice(_MASK_FIT_OPTIONS)

        return updates

    def refresh(self, config: dict):
        self._config = config
        self._rand_gravity_mode_var.set(      config.get("rand_gravity_mode", DEFAULT_CONFIG["rand_gravity_mode"]))
        self._rand_gravity_angle_var.set(     config.get("rand_gravity_angle", DEFAULT_CONFIG["rand_gravity_angle"]))
        self._rand_gravity_strength_var.set(  config.get("rand_gravity_strength", DEFAULT_CONFIG["rand_gravity_strength"]))
        self._rand_velocity_motion_var.set(   config.get("rand_velocity_motion", DEFAULT_CONFIG["rand_velocity_motion"]))
        self._rand_chunk_count_var.set(       config.get("rand_chunk_count", DEFAULT_CONFIG["rand_chunk_count"]))
        self._rand_blast_mode_var.set(        config.get("rand_blast_mode", DEFAULT_CONFIG["rand_blast_mode"]))
        self._rand_chunk_physics_var.set(     config.get("rand_chunk_physics", DEFAULT_CONFIG["rand_chunk_physics"]))
        self._rand_gravity_ramp_var.set(      config.get("rand_gravity_ramp", DEFAULT_CONFIG["rand_gravity_ramp"]))
        self._rand_chunk_shape_var.set(       config.get("rand_chunk_shape", DEFAULT_CONFIG["rand_chunk_shape"]))
        self._rand_tint_colors_var.set(       config.get("rand_tint_colors", DEFAULT_CONFIG["rand_tint_colors"]))
        self._rand_tint_opacity_bleed_var.set(config.get("rand_tint_opacity_bleed", DEFAULT_CONFIG["rand_tint_opacity_bleed"]))
        self._rand_tint_mode_anim_var.set(    config.get("rand_tint_mode_anim", DEFAULT_CONFIG["rand_tint_mode_anim"]))
        self._rand_tint_advanced_var.set(     config.get("rand_tint_advanced", DEFAULT_CONFIG["rand_tint_advanced"]))
        self._rand_tint_color_anim_var.set(   config.get("rand_tint_color_anim", DEFAULT_CONFIG["rand_tint_color_anim"]))
        self._rand_dissolve_pattern_var.set(  config.get("rand_dissolve_pattern", DEFAULT_CONFIG["rand_dissolve_pattern"]))
        self._rand_dissolve_color_var.set(    config.get("rand_dissolve_color", DEFAULT_CONFIG["rand_dissolve_color"]))
        self._rand_dissolve_min_fade_var.set( config.get("rand_dissolve_min_fade", DEFAULT_CONFIG["rand_dissolve_min_fade"]))
        self._rand_dissolve_stagger_var.set(  config.get("rand_dissolve_stagger", DEFAULT_CONFIG["rand_dissolve_stagger"]))
        self._rand_mask_image_var.set(        config.get("rand_mask_image", DEFAULT_CONFIG["rand_mask_image"]))
        self._rand_mask_softness_var.set(     config.get("rand_mask_softness", DEFAULT_CONFIG["rand_mask_softness"]))
        self._rand_mask_anim_var.set(         config.get("rand_mask_anim", DEFAULT_CONFIG["rand_mask_anim"]))
        self._rand_mask_fit_var.set(          config.get("rand_mask_fit", DEFAULT_CONFIG["rand_mask_fit"]))
        self._vary_var.set(                   config.get("rand_vary_current", DEFAULT_CONFIG["rand_vary_current"]))
