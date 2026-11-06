import tkinter as tk
import tkinter.ttk as _tk_ttk
import tkinter.colorchooser as _cc

import ttkbootstrap as ttk

from gui.theme import PALETTE, FONT_BODY, FONT_SMALL, FONT_MONO, Tooltip as _Tooltip
from gui.widgets.controls import MoreOptions, choice_combo, slider_row
from utils.config import DEFAULT_CONFIG

_ANIM_OPTIONS       = ["instant", "linear", "early", "late", "pulse", "per_chunk"]
_BLEND_MODE_OPTIONS = ["unidirectional", "bidirectional"]
_COLLISION_OPTIONS  = ["blend", "outer_wins", "inner_wins"]

# ------------------------------------------------------------------ #
#  Tooltip strings                                                     #
# ------------------------------------------------------------------ #

_TIP_ENABLE = (
    "Switch the tint/wound effect on or off. When off, all the settings below are ignored "
    "and rendering is faster."
)

_TIP_MODE = (
    "Chunks — tint is painted along the cracks between gib pieces. Great for blood or wound effects.\n\n"
    "Edges — tint is painted around the outer silhouette of the whole sprite. Better for glow or disintegration looks."
)

_TIP_BLEND_MODE = (
    "Border only — Outer color bleeds inward from chunk borders only. Classic single-BFS tint.\n\n"
    "Border + center — Inner color also radiates outward from each chunk's center while Outer bleeds inward "
    "from the border. The two color fronts collide somewhere in the middle.\n\n"
    "Use the Inner section and Collision controls to shape the two-color look."
)

_TIP_COLLISION = (
    "Controls what happens where the Outer and Inner color fronts overlap (Border + center only).\n\n"
    "Blend — both fronts mix together; use the Blend slider to shift where they meet.\n"
    "Outer wins — Outer color takes full priority wherever it reaches.\n"
    "Inner wins — Inner color takes full priority wherever it reaches."
)

_TIP_BLEND = (
    "In Blend collision mode: shifts where the two color fronts meet "
    f"(default: {DEFAULT_CONFIG['TINT_BLEND']}).\n\n"
    "0.0 = Inner color dominates the whole chunk.\n"
    "1.0 = Outer color dominates the whole chunk.\n"
    "0.5 = fronts meet exactly at the geometric midpoint.\n\n"
    "Only meaningful in Border + center blend mode with Blend collision."
)

_TIP_DEPTH_OUTER = (
    "How far the Outer (border) color front travels inward, as a fraction of the sprite's size "
    f"(default: {DEFAULT_CONFIG['TINT_DEPTH_OUTER'] * 100:.0f}%).\n\n"
    "Higher = thicker outer rim. At 100% the front can flood an entire chunk interior. "
    "This also acts as the master enable: set to 0 to disable tint entirely."
)

_TIP_DEPTH_INNER = (
    "How far the Inner (center) color front travels outward, as a fraction of the sprite's size "
    f"(default: {DEFAULT_CONFIG['TINT_DEPTH_INNER'] * 100:.0f}%).\n\n"
    "Only used in Border + center mode. Set independently from Outer Depth to create "
    "asymmetric effects (e.g. wide outer crust, tiny inner glow).\n\n"
    "At 100% both fronts can overlap heavily — use Collision mode to control the result."
)

_TIP_JITTER_OUTER = (
    f"Randomises the outer front's edge so it looks ragged and organic (default: {DEFAULT_CONFIG['TINT_JITTER_OUTER']}).\n\n"
    "0 = crisp outer border. 1 = very rough/noisy outer edge."
)

_TIP_JITTER_INNER = (
    f"Randomises the inner front's edge independently from the outer front (default: {DEFAULT_CONFIG['TINT_JITTER_INNER']}).\n\n"
    "0 = smooth inner glow. 1 = very rough inner core.\n\n"
    "Only used in Border + center mode. Lets you have e.g. a smooth outer crust but a ragged inner wound."
)

_TIP_OPACITY_OUTER = (
    f"Strength of the Outer color at the chunk border (default: {DEFAULT_CONFIG['TINT_OPACITY_OUTER']}).\n\n"
    "0 = invisible. 1 = fully opaque. Fades to zero at the outer depth cutoff."
)

_TIP_OPACITY_INNER = (
    f"Strength of the Inner color at the chunk centroid (default: {DEFAULT_CONFIG['TINT_OPACITY_INNER']}).\n\n"
    "0 = invisible. 1 = fully opaque. Fades to zero at the inner depth cutoff.\n\n"
    "Only used in Border + center mode."
)

_TIP_BORDER_FADE = (
    f"Makes border pixels semi-transparent so the outer wound edge looks frayed or bloody "
    f"(default: {DEFAULT_CONFIG['TINT_ALPHA_BLEED_OUTER']}).\n\n"
    "0 = no transparency at border. 1 = fully transparent at the very border, fading back to solid."
)

_TIP_CENTER_FADE = (
    f"Makes centroid pixels semi-transparent so the inner glow looks hollow or ethereal "
    f"(default: {DEFAULT_CONFIG['TINT_ALPHA_BLEED_INNER']}).\n\n"
    "0 = no transparency at center. 1 = fully transparent at the centroid, fading back to solid.\n\n"
    "Only used in Border + center mode."
)

_TIP_WOUND_COLOR = (
    "The Inner color — radiates outward from the center of each chunk in Border + center mode, "
    "or appears at the deepest tint zone in Border only mode."
)

_TIP_EDGE_COLOR = (
    "The Outer color — bleeds inward from chunk borders (or sprite silhouette edges). "
    "Disabled when 'Single color' is on."
)

_TIP_SINGLE_COLOR = (
    "Use only the Inner color for the whole tint zone. The Outer color is ignored.\n\n"
    "Handy for simple solid-colour outlines or glows."
)

_TIP_ANIM = (
    "Controls how the tint builds up across animation frames.\n\n"
    "Instant — fully tinted from frame 1 onward\n"
    "Linear — tint fades in evenly across all frames\n"
    "Early — tint appears quickly then holds steady\n"
    "Late — tint stays low then surges near the end\n"
    "Pulse — tint peaks at mid-animation then fades\n"
    "Per chunk — each chunk fades in individually as it breaks away"
)

_TIP_NOISE = (
    "Large-scale noise field that warps the tint boundary into organic, blobby shapes.\n\n"
    "0 = clean BFS distance ring (current behaviour)\n"
    "Higher values = more blobby, irregular tint boundary\n\n"
    "Different from Jitter: Jitter is per-pixel randomness; Noise gives large regional variation. "
    "They stack together — you can use both at once."
)

_TIP_SATURATION = (
    f"Shifts the HSV saturation of chunk pixels after tinting "
    f"(default: {DEFAULT_CONFIG['TINT_SATURATION_SHIFT']}).\n\n"
    "Negative = desaturate toward grey (wither, drain, stone, shadow effects)\n"
    "0 = no change\n"
    "Positive = oversaturate (corrupted, energized, plasma effects)\n\n"
    "Works together with tint color — e.g. desaturate + blue tint gives cryo effects."
)

_TIP_GRAIN = (
    "Per-pixel grain: each pixel gets a fixed random brighter/darker shade after tinting.\n\n"
    "0 = smooth (off)\n"
    "0.1–0.25 = subtle texture (flesh, bone, stone, rust)\n"
    "0.4+ = coarse, gritty speckle\n\n"
    "Unlike Noise and Jitter it works at any chunk count, even on 1–2 px pieces, "
    "and it applies even when the tint itself is off."
)

_TIP_COLOR_ANIM_INNER = (
    "When enabled, the Inner color shifts over the animation timeline — "
    "starting at the Inner color and ending at this end color by the last frame.\n\n"
    "Example: inner starts bright red, ends dark brown for a wound-blackening effect.\n\n"
    "Separate from opacity animation (TINT_ANIM) — both work together."
)

_TIP_COLOR_ANIM_OUTER = (
    "When enabled, the Outer color shifts over the animation timeline — "
    "starting at the Outer color and ending at this end color by the last frame.\n\n"
    "Example: outer starts yellow, ends orange-red for a fire color shift.\n\n"
    "Disabled when 'Single color' is on."
)

_TIP_COLOR_ANIM_CURVE = (
    f"Gamma curve controlling the speed of the color animation "
    f"(default: {DEFAULT_CONFIG['TINT_COLOR_ANIM_CURVE']}).\n\n"
    "1.0 = linear shift across all frames\n"
    "< 1.0 = color changes fast early, then slows (fast-out)\n"
    "> 1.0 = color changes slowly at first, then accelerates (slow-out)\n\n"
    "Same curve convention as Dissolve Curve."
)


class TintTab:
    def __init__(self, parent, config: dict, app):
        self.config = config
        self.app = app

        self._tint_enabled = config.get("TINT_DEPTH_OUTER", 0.0) > 0

        # tk.Vars
        self._enabled_var        = tk.BooleanVar(value=self._tint_enabled)
        self._depth_outer_var    = tk.DoubleVar(value=config.get("TINT_DEPTH_OUTER", 0.12) or 0.12)
        self._depth_inner_var    = tk.DoubleVar(value=config.get("TINT_DEPTH_INNER", 0.12) or 0.12)
        self._jitter_outer_var   = tk.DoubleVar(value=config.get("TINT_JITTER_OUTER", 0.3))
        self._jitter_inner_var   = tk.DoubleVar(value=config.get("TINT_JITTER_INNER", 0.3))
        self._opacity_outer_var  = tk.DoubleVar(value=config.get("TINT_OPACITY_OUTER", 0.8))
        self._opacity_inner_var  = tk.DoubleVar(value=config.get("TINT_OPACITY_INNER", 0.8))
        self._ab_outer_var       = tk.DoubleVar(value=config.get("TINT_ALPHA_BLEED_OUTER", 0.0))
        self._ab_inner_var       = tk.DoubleVar(value=config.get("TINT_ALPHA_BLEED_INNER", 0.0))
        self._blend_mode_var     = tk.StringVar(value=config.get("TINT_BLEND_MODE", "unidirectional"))
        self._collision_var      = tk.StringVar(value=config.get("TINT_COLLISION", "blend"))
        self._blend_var          = tk.DoubleVar(value=config.get("TINT_BLEND", 0.5))
        self._mode_var           = tk.StringVar(value=config.get("TINT_MODE", "chunks"))
        self._anim_var           = tk.StringVar(value=config.get("TINT_ANIM", "instant"))
        self._single_color_var   = tk.BooleanVar(value=config.get("TINT_SINGLE_COLOR", False))
        self._noise_var          = tk.DoubleVar(value=config.get("TINT_NOISE", 0.0))
        self._sat_shift_var      = tk.DoubleVar(value=config.get("TINT_SATURATION_SHIFT", 0.0))
        self._grain_var          = tk.DoubleVar(value=config.get("TINT_GRAIN", 0.0))
        self._color_anim_curve_var = tk.DoubleVar(value=config.get("TINT_COLOR_ANIM_CURVE", 1.0))
        self._anim_inner_end_var = tk.BooleanVar(
            value=config.get("TINT_COLOR_INNER_END") is not None)
        self._anim_outer_end_var = tk.BooleanVar(
            value=config.get("TINT_COLOR_OUTER_END") is not None)

        # Plain str — not tk.StringVar (updated by color picker directly)
        self._outer_color = config.get("TINT_COLOR_OUTER", "#660000")
        self._inner_color = config.get("TINT_COLOR_INNER", "#FF2222")
        self._outer_end_color = config.get("TINT_COLOR_OUTER_END") or "#FF6600"
        self._inner_end_color = config.get("TINT_COLOR_INNER_END") or "#440000"

        # Widget collections for bulk enable/disable
        self._toggleable: list = []    # widgets disabled when tint is off
        self._bidir_only: list = []    # widgets additionally disabled in unidirectional mode
        self._swatches:   list = []    # (canvas, color_attr, pick_callback) tuples
        self._edge_widgets: list = []  # outer-color widgets disabled by single-color toggle
        self._edge_swatches: list = []
        self._outer_end_widgets: list = []    # outer end color picker; disabled by single-color

        self._build(parent)
        self._apply_toggle_state()
        self._apply_edge_color_state()
        self._apply_bidir_state()
        self._apply_color_anim_state()

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def _build(self, parent):
        parent.columnconfigure(0, weight=1)

        # Section 1 — master enable toggle
        en_frame = _tk_ttk.LabelFrame(parent, text="Tint", padding=8)
        en_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=(10, 4))
        en_frame.columnconfigure(0, weight=1)

        en_cb = ttk.Checkbutton(
            en_frame,
            text="Enable tint",
            variable=self._enabled_var,
            bootstyle="round-toggle",
            command=self._on_toggle,
        )
        en_cb.grid(row=0, column=0, sticky="w")
        _Tooltip(en_cb, _TIP_ENABLE)

        # Section 2 — Settings
        self._build_settings(parent, row=1)

        # Section 3 — Colors
        self._build_colors(parent, row=2)

        # Section 4 — Animation
        self._build_animation(parent, row=3)

    def _build_settings(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Settings", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=4)
        frame.columnconfigure(0, weight=1)

        # Mode radios
        mode_row = ttk.Frame(frame)
        mode_row.grid(row=0, column=0, sticky="ew", pady=(0, 4))

        mode_lbl = ttk.Label(mode_row, text="Mode", font=FONT_BODY,
                             background=PALETTE["bg_surface"])
        mode_lbl.pack(side="left", padx=(0, 10))
        _Tooltip(mode_lbl, _TIP_MODE)

        for label, value in (("Chunks", "chunks"), ("Edges", "edges")):
            rb = ttk.Radiobutton(
                mode_row,
                text=label,
                variable=self._mode_var,
                value=value,
                bootstyle="primary",
                command=self._on_mode_change,
            )
            rb.pack(side="left", padx=(0, 8))
            self._toggleable.append(rb)
            _Tooltip(rb, _TIP_MODE)

        # Outer sub-section
        outer_frame = _tk_ttk.LabelFrame(frame, text="Outer (border)", padding=6)
        outer_frame.grid(row=1, column=0, sticky="ew", pady=(6, 2))
        outer_frame.columnconfigure(0, weight=1)

        self._add_float_slider(outer_frame, row=0, label="Depth",
                               var=self._depth_outer_var,
                               from_=0.0, to=1.0, dp=3, key="TINT_DEPTH_OUTER",
                               release_cmd=self._save_tint_outer_depth, percent=True,
                               tooltip=_TIP_DEPTH_OUTER)
        self._add_float_slider(outer_frame, row=1, label="Jitter",
                               var=self._jitter_outer_var,
                               from_=0.0, to=1.0, dp=2, key="TINT_JITTER_OUTER",
                               tooltip=_TIP_JITTER_OUTER)
        self._add_float_slider(outer_frame, row=2, label="Opacity",
                               var=self._opacity_outer_var,
                               from_=0.0, to=1.0, dp=2, key="TINT_OPACITY_OUTER",
                               tooltip=_TIP_OPACITY_OUTER)
        self._add_float_slider(outer_frame, row=3, label="Border Fade",
                               var=self._ab_outer_var,
                               from_=0.0, to=1.0, dp=2, key="TINT_ALPHA_BLEED_OUTER",
                               tooltip=_TIP_BORDER_FADE)

        # Two-color (bidirectional) tint, noise and saturation are advanced
        self._settings_more = MoreOptions(frame, [
            "TINT_BLEND_MODE", "TINT_COLLISION", "TINT_BLEND", "TINT_DEPTH_INNER",
            "TINT_JITTER_INNER", "TINT_OPACITY_INNER", "TINT_ALPHA_BLEED_INNER",
            "TINT_NOISE", "TINT_SATURATION_SHIFT", "TINT_GRAIN",
        ], text="Two-color tint, noise, saturation, grain")
        self._settings_more.grid(row=2, column=0, sticky="ew")
        more = self._settings_more.body

        # Blend Mode dropdown
        bm_row = ttk.Frame(more)
        bm_row.grid(row=0, column=0, sticky="ew", pady=2)
        bm_row.columnconfigure(1, weight=1)
        bm_lbl = ttk.Label(bm_row, text="Blend Mode", font=FONT_BODY,
                           background=PALETTE["bg_surface"])
        bm_lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
        _Tooltip(bm_lbl, _TIP_BLEND_MODE)
        self._blend_mode_combo = choice_combo(
            bm_row, self._blend_mode_var, _BLEND_MODE_OPTIONS,
            lambda e: self._on_blend_mode_change(), width=16,
        )
        self._blend_mode_combo.grid(row=0, column=1, sticky="w")
        _Tooltip(self._blend_mode_combo, _TIP_BLEND_MODE)
        self._toggleable.append(self._blend_mode_combo)

        # Collision dropdown + Blend slider (bidir only)
        col_row = ttk.Frame(more)
        col_row.grid(row=1, column=0, sticky="ew", pady=2)
        col_row.columnconfigure(1, weight=1)
        col_lbl = ttk.Label(col_row, text="Collision", font=FONT_BODY,
                            background=PALETTE["bg_surface"])
        col_lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
        _Tooltip(col_lbl, _TIP_COLLISION)
        self._collision_combo = choice_combo(
            col_row, self._collision_var, _COLLISION_OPTIONS,
            lambda e: self._save("TINT_COLLISION", self._collision_var.get()), width=16,
        )
        self._collision_combo.grid(row=0, column=1, sticky="w")
        _Tooltip(self._collision_combo, _TIP_COLLISION)
        self._toggleable.append(self._collision_combo)
        self._bidir_only.append(self._collision_combo)

        self._add_float_slider(more, row=2, label="Blend",
                               var=self._blend_var,
                               from_=0.0, to=1.0, dp=2, key="TINT_BLEND",
                               tooltip=_TIP_BLEND, bidir_only=True)

        # Inner sub-section (bidir only)
        self._inner_frame = _tk_ttk.LabelFrame(more, text="Inner (center)", padding=6)
        self._inner_frame.grid(row=3, column=0, sticky="ew", pady=(2, 4))
        self._inner_frame.columnconfigure(0, weight=1)

        self._add_float_slider(self._inner_frame, row=0, label="Depth",
                               var=self._depth_inner_var,
                               from_=0.0, to=1.0, dp=3, key="TINT_DEPTH_INNER", percent=True,
                               tooltip=_TIP_DEPTH_INNER, bidir_only=True)
        self._add_float_slider(self._inner_frame, row=1, label="Jitter",
                               var=self._jitter_inner_var,
                               from_=0.0, to=1.0, dp=2, key="TINT_JITTER_INNER",
                               tooltip=_TIP_JITTER_INNER, bidir_only=True)
        self._add_float_slider(self._inner_frame, row=2, label="Opacity",
                               var=self._opacity_inner_var,
                               from_=0.0, to=1.0, dp=2, key="TINT_OPACITY_INNER",
                               tooltip=_TIP_OPACITY_INNER, bidir_only=True)
        self._add_float_slider(self._inner_frame, row=3, label="Center Fade",
                               var=self._ab_inner_var,
                               from_=0.0, to=1.0, dp=2, key="TINT_ALPHA_BLEED_INNER",
                               tooltip=_TIP_CENTER_FADE, bidir_only=True)

        # Noise + Saturation sliders (global, not per-inner/outer)
        self._add_float_slider(more, row=4, label="Noise",
                               var=self._noise_var,
                               from_=0.0, to=1.0, dp=2, key="TINT_NOISE",
                               tooltip=_TIP_NOISE)
        self._add_float_slider(more, row=5, label="Saturation",
                               var=self._sat_shift_var,
                               from_=-1.0, to=1.0, dp=2, key="TINT_SATURATION_SHIFT",
                               tooltip=_TIP_SATURATION)
        self._add_float_slider(more, row=6, label="Grain",
                               var=self._grain_var,
                               from_=0.0, to=1.0, dp=2, key="TINT_GRAIN",
                               tooltip=_TIP_GRAIN)

    def _build_colors(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Colors", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=4)
        frame.columnconfigure(0, weight=1)

        self._inner_swatch, self._inner_hex_lbl, inner_lbl, inner_btn = self._make_color_row(
            frame, row=0, label="Inner",
            color_attr="_inner_color", config_key="TINT_COLOR_INNER",
            extra_widget_list=None, extra_swatch_list=None,
        )
        for w in (inner_lbl, self._inner_swatch, inner_btn):
            _Tooltip(w, _TIP_WOUND_COLOR)

        self._outer_swatch, self._outer_hex_lbl, outer_lbl, outer_btn = self._make_color_row(
            frame, row=1, label="Outer",
            color_attr="_outer_color", config_key="TINT_COLOR_OUTER",
            extra_widget_list=self._edge_widgets,
            extra_swatch_list=self._edge_swatches,
        )
        for w in (outer_lbl, self._outer_swatch, outer_btn):
            _Tooltip(w, _TIP_EDGE_COLOR)

        self._single_color_cb = ttk.Checkbutton(
            frame,
            text="Single color (ignore Outer color)",
            variable=self._single_color_var,
            bootstyle="round-toggle",
            command=self._on_single_color_toggle,
        )
        self._single_color_cb.grid(row=2, column=0, sticky="w", pady=(6, 0))
        self._toggleable.append(self._single_color_cb)
        _Tooltip(self._single_color_cb, _TIP_SINGLE_COLOR)

    def _build_animation(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Animation", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=(4, 10))
        frame.columnconfigure(0, weight=1)

        anim_row = ttk.Frame(frame)
        anim_row.grid(row=0, column=0, sticky="ew")
        anim_row.columnconfigure(1, weight=1)

        anim_lbl = ttk.Label(anim_row, text="Animation", font=FONT_BODY,
                             background=PALETTE["bg_surface"])
        anim_lbl.grid(row=0, column=0, sticky="w", padx=(0, 8))
        _Tooltip(anim_lbl, _TIP_ANIM)

        self._anim_combo = choice_combo(
            anim_row, self._anim_var, _ANIM_OPTIONS,
            lambda e: self._save("TINT_ANIM", self._anim_var.get()), width=14,
        )
        self._anim_combo.grid(row=0, column=1, sticky="w")
        _Tooltip(self._anim_combo, _TIP_ANIM)
        self._toggleable.append(self._anim_combo)

        # Color Animation sub-section (advanced)
        self._anim_more = MoreOptions(
            frame, ["TINT_COLOR_INNER_END", "TINT_COLOR_OUTER_END", "TINT_COLOR_ANIM_CURVE"],
            text="Color animation")
        self._anim_more.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        color_anim_frame = _tk_ttk.LabelFrame(self._anim_more.body, text="Color Animation", padding=6)
        color_anim_frame.grid(row=0, column=0, sticky="ew", pady=(4, 0))
        color_anim_frame.columnconfigure(0, weight=1)

        # Inner end color
        inner_end_row = ttk.Frame(color_anim_frame)
        inner_end_row.grid(row=0, column=0, sticky="ew", pady=2)
        inner_end_row.columnconfigure(2, weight=1)

        inner_end_cb = ttk.Checkbutton(
            inner_end_row, text="Animate inner →", variable=self._anim_inner_end_var,
            bootstyle="round-toggle", command=self._on_color_anim_toggle,
        )
        inner_end_cb.pack(side="left", padx=(0, 4))
        _Tooltip(inner_end_cb, _TIP_COLOR_ANIM_INNER)
        self._toggleable.append(inner_end_cb)

        self._inner_end_swatch = tk.Canvas(
            inner_end_row, width=24, height=18, highlightthickness=1,
            highlightbackground=PALETTE["accent_glow"],
            bg=self._inner_end_color,
        )
        self._inner_end_swatch.pack(side="left", padx=(0, 4))

        self._inner_end_hex_lbl = ttk.Label(
            inner_end_row, text=self._inner_end_color.upper(),
            font=FONT_MONO, width=8, background=PALETTE["bg_surface"],
        )
        self._inner_end_hex_lbl.pack(side="left", padx=(0, 4))

        inner_end_btn = ttk.Button(
            inner_end_row, text="Pick…", width=6,
            command=lambda: self._pick_end_color(
                "_inner_end_color", "TINT_COLOR_INNER_END",
                self._inner_end_swatch, self._inner_end_hex_lbl,
                self._anim_inner_end_var,
            ),
        )
        inner_end_btn.pack(side="left")
        _Tooltip(self._inner_end_swatch, _TIP_COLOR_ANIM_INNER)
        _Tooltip(self._inner_end_hex_lbl, _TIP_COLOR_ANIM_INNER)
        _Tooltip(inner_end_btn, _TIP_COLOR_ANIM_INNER)
        self._toggleable.extend([self._inner_end_hex_lbl, inner_end_btn])

        def _inner_end_swatch_click(e):
            if self._anim_inner_end_var.get():
                self._pick_end_color(
                    "_inner_end_color", "TINT_COLOR_INNER_END",
                    self._inner_end_swatch, self._inner_end_hex_lbl,
                    self._anim_inner_end_var,
                )
        self._inner_end_swatch.bind("<Button-1>", _inner_end_swatch_click)

        # Outer end color
        outer_end_row = ttk.Frame(color_anim_frame)
        outer_end_row.grid(row=1, column=0, sticky="ew", pady=2)

        outer_end_cb = ttk.Checkbutton(
            outer_end_row, text="Animate outer →", variable=self._anim_outer_end_var,
            bootstyle="round-toggle", command=self._on_color_anim_toggle,
        )
        outer_end_cb.pack(side="left", padx=(0, 4))
        _Tooltip(outer_end_cb, _TIP_COLOR_ANIM_OUTER)
        self._toggleable.append(outer_end_cb)
        self._outer_end_widgets.append(outer_end_cb)

        self._outer_end_swatch = tk.Canvas(
            outer_end_row, width=24, height=18, highlightthickness=1,
            highlightbackground=PALETTE["accent_glow"],
            bg=self._outer_end_color,
        )
        self._outer_end_swatch.pack(side="left", padx=(0, 4))

        self._outer_end_hex_lbl = ttk.Label(
            outer_end_row, text=self._outer_end_color.upper(),
            font=FONT_MONO, width=8, background=PALETTE["bg_surface"],
        )
        self._outer_end_hex_lbl.pack(side="left", padx=(0, 4))

        outer_end_btn = ttk.Button(
            outer_end_row, text="Pick…", width=6,
            command=lambda: self._pick_end_color(
                "_outer_end_color", "TINT_COLOR_OUTER_END",
                self._outer_end_swatch, self._outer_end_hex_lbl,
                self._anim_outer_end_var,
            ),
        )
        outer_end_btn.pack(side="left")
        _Tooltip(self._outer_end_swatch, _TIP_COLOR_ANIM_OUTER)
        _Tooltip(self._outer_end_hex_lbl, _TIP_COLOR_ANIM_OUTER)
        _Tooltip(outer_end_btn, _TIP_COLOR_ANIM_OUTER)
        self._outer_end_widgets.extend([
            self._outer_end_swatch, self._outer_end_hex_lbl, outer_end_btn,
        ])
        self._toggleable.extend([self._outer_end_hex_lbl, outer_end_btn])

        def _outer_end_swatch_click(e):
            if self._anim_outer_end_var.get() and not self._single_color_var.get():
                self._pick_end_color(
                    "_outer_end_color", "TINT_COLOR_OUTER_END",
                    self._outer_end_swatch, self._outer_end_hex_lbl,
                    self._anim_outer_end_var,
                )
        self._outer_end_swatch.bind("<Button-1>", _outer_end_swatch_click)

        # Curve slider (only meaningful when color anim is active)
        self._add_float_slider(
            color_anim_frame, row=2, label="Curve",
            var=self._color_anim_curve_var,
            from_=0.1, to=3.0, dp=2, key="TINT_COLOR_ANIM_CURVE",
            tooltip=_TIP_COLOR_ANIM_CURVE,
        )

    # ------------------------------------------------------------------ #
    #  Slider helper                                                       #
    # ------------------------------------------------------------------ #

    def _add_float_slider(self, parent, row, label, var, from_, to, dp, key,
                          release_cmd=None, percent=False, tooltip=None,
                          bidir_only=False):
        if release_cmd is None:
            release_cmd = lambda k=key, v=var, d=dp: self._save(k, round(float(v.get()), d))
        _rf, slider, readout, _lbl = slider_row(
            parent, row, label, var, from_, to, commit=release_cmd, dp=dp,
            default=DEFAULT_CONFIG.get(key), scale=100 if percent else 1,
            suffix="%" if percent else "", tooltip=tooltip, tooltip_cls=_Tooltip)

        self._toggleable.extend([slider, readout])
        if bidir_only:
            self._bidir_only.extend([slider, readout])

    # ------------------------------------------------------------------ #
    #  Color row helper                                                    #
    # ------------------------------------------------------------------ #

    def _make_color_row(self, parent, row, label, color_attr, config_key,
                        extra_widget_list, extra_swatch_list):
        rf = ttk.Frame(parent)
        rf.grid(row=row, column=0, sticky="ew", pady=3)

        lbl_widget = ttk.Label(rf, text=label, font=FONT_BODY,
                               background=PALETTE["bg_surface"], width=6)
        lbl_widget.pack(side="left", padx=(0, 6))

        swatch = tk.Canvas(rf, width=24, height=18, highlightthickness=1,
                           highlightbackground=PALETTE["accent_glow"],
                           bg=getattr(self, color_attr))
        swatch.pack(side="left", padx=(0, 4))

        hex_lbl = ttk.Label(rf, text=getattr(self, color_attr).upper(),
                            font=FONT_MONO, width=8,
                            background=PALETTE["bg_surface"])
        hex_lbl.pack(side="left", padx=(0, 6))

        pick_btn = ttk.Button(
            rf, text="Pick…", width=6,
            command=lambda ca=color_attr, ck=config_key, sw=swatch, hl=hex_lbl:
                self._pick_color(ca, ck, sw, hl),
        )
        pick_btn.pack(side="left")

        def _swatch_click(e, ca=color_attr, ck=config_key, sw=swatch, hl=hex_lbl):
            self._pick_color(ca, ck, sw, hl)

        if extra_widget_list is not None:
            extra_widget_list.extend([pick_btn, hex_lbl])
        else:
            self._toggleable.append(pick_btn)

        if extra_swatch_list is not None:
            extra_swatch_list.append((swatch, _swatch_click))
        else:
            self._swatches.append((swatch, _swatch_click))

        swatch.bind("<Button-1>", _swatch_click)

        return swatch, hex_lbl, lbl_widget, pick_btn

    # ------------------------------------------------------------------ #
    #  Color picker                                                        #
    # ------------------------------------------------------------------ #

    def _pick_color(self, color_attr, config_key, swatch, hex_lbl):
        result = _cc.askcolor(color=getattr(self, color_attr), title="Pick color")
        if result and result[1]:
            hex_val = result[1].upper()
            setattr(self, color_attr, hex_val)
            swatch.configure(bg=hex_val)
            hex_lbl.configure(text=hex_val)
            self._save(config_key, hex_val)

    def _pick_end_color(self, color_attr, config_key, swatch, hex_lbl, enabled_var):
        result = _cc.askcolor(color=getattr(self, color_attr), title="Pick end color")
        if result and result[1]:
            hex_val = result[1].upper()
            setattr(self, color_attr, hex_val)
            swatch.configure(bg=hex_val)
            hex_lbl.configure(text=hex_val)
            if enabled_var.get():
                self._save(config_key, hex_val)

    # ------------------------------------------------------------------ #
    #  Toggle / state management                                           #
    # ------------------------------------------------------------------ #

    def _on_toggle(self):
        self._tint_enabled = self._enabled_var.get()
        self._apply_toggle_state()
        self._apply_edge_color_state()
        self._apply_color_anim_state()
        self._save_tint_outer_depth()

    def _apply_toggle_state(self):
        state = "normal" if self._tint_enabled else "disabled"
        for w in self._toggleable:
            try:
                w.configure(state=state)
            except tk.TclError:
                pass
        for (swatch, callback) in self._swatches:
            if self._tint_enabled:
                swatch.bind("<Button-1>", callback)
                swatch.configure(cursor="hand2")
            else:
                swatch.unbind("<Button-1>")
                swatch.configure(cursor="")
        # Re-apply sub-state on top of the enable state
        if self._tint_enabled:
            self._apply_bidir_state()
            self._apply_color_anim_state()

    def _on_blend_mode_change(self):
        self._save("TINT_BLEND_MODE", self._blend_mode_var.get())
        self._apply_bidir_state()

    def _apply_bidir_state(self):
        is_bidir = self._blend_mode_var.get() == "bidirectional"
        state = "normal" if (self._tint_enabled and is_bidir) else "disabled"
        for w in self._bidir_only:
            try:
                w.configure(state=state)
            except tk.TclError:
                pass

    def _on_single_color_toggle(self):
        self._save("TINT_SINGLE_COLOR", self._single_color_var.get())
        self._apply_edge_color_state()
        self._apply_color_anim_state()
        # If single-color is now on, clear the outer end color.
        if self._single_color_var.get():
            self._save("TINT_COLOR_OUTER_END", None)

    def _apply_edge_color_state(self):
        if not self._tint_enabled:
            return
        disabled = self._single_color_var.get()
        state = "disabled" if disabled else "normal"
        for w in self._edge_widgets:
            try:
                w.configure(state=state)
            except tk.TclError:
                pass
        for swatch, callback in self._edge_swatches:
            if disabled:
                swatch.unbind("<Button-1>")
                swatch.configure(cursor="")
            else:
                swatch.bind("<Button-1>", callback)
                swatch.configure(cursor="hand2")

    def _on_color_anim_toggle(self):
        inner_on = self._anim_inner_end_var.get()
        outer_on = self._anim_outer_end_var.get()
        self._save("TINT_COLOR_INNER_END",
                   self._inner_end_color if inner_on else None)
        self._save("TINT_COLOR_OUTER_END",
                   self._outer_end_color if (outer_on and not self._single_color_var.get()) else None)
        self._apply_color_anim_state()

    def _apply_color_anim_state(self):
        inner_on = self._anim_inner_end_var.get() and self._tint_enabled
        outer_on = (self._anim_outer_end_var.get() and self._tint_enabled
                    and not self._single_color_var.get())
        self._inner_end_swatch.configure(cursor="hand2" if inner_on else "")
        self._outer_end_swatch.configure(cursor="hand2" if outer_on else "")
        for w in (self._inner_end_hex_lbl,):
            try:
                w.configure(state="normal" if inner_on else "disabled")
            except tk.TclError:
                pass
        for w in self._outer_end_widgets:
            if w is self._outer_end_swatch:
                continue
            try:
                w.configure(state="normal" if outer_on else "disabled")
            except tk.TclError:
                pass

    def _on_mode_change(self):
        self._save("TINT_MODE", self._mode_var.get())

    # ------------------------------------------------------------------ #
    #  Save helpers                                                        #
    # ------------------------------------------------------------------ #

    def _save_tint_outer_depth(self):
        pct = round(float(self._depth_outer_var.get()), 3) if self._tint_enabled else 0.0
        self._save("TINT_DEPTH_OUTER", pct)

    def _save(self, key, value):
        self.config[key] = value
        self.app.save_config()
        self.app.mark_preview_dirty()

    # ------------------------------------------------------------------ #
    #  Refresh (called by app._refresh_all_tabs after preset load)        #
    # ------------------------------------------------------------------ #

    def refresh(self, config):
        self.config = config

        pct = config.get("TINT_DEPTH_OUTER", 0.0)
        if pct > 0:
            self._tint_enabled = True
            self._enabled_var.set(True)
            self._depth_outer_var.set(pct)
        else:
            self._tint_enabled = False
            self._enabled_var.set(False)

        self._depth_inner_var.set(config.get("TINT_DEPTH_INNER", 0.12))
        self._jitter_outer_var.set(config.get("TINT_JITTER_OUTER", 0.3))
        self._jitter_inner_var.set(config.get("TINT_JITTER_INNER", 0.3))
        self._opacity_outer_var.set(config.get("TINT_OPACITY_OUTER", 0.8))
        self._opacity_inner_var.set(config.get("TINT_OPACITY_INNER", 0.8))
        self._ab_outer_var.set(config.get("TINT_ALPHA_BLEED_OUTER", 0.0))
        self._ab_inner_var.set(config.get("TINT_ALPHA_BLEED_INNER", 0.0))
        self._blend_mode_var.set(config.get("TINT_BLEND_MODE", "unidirectional"))
        self._collision_var.set(config.get("TINT_COLLISION", "blend"))
        self._blend_var.set(config.get("TINT_BLEND", 0.5))
        self._mode_var.set(config.get("TINT_MODE", "chunks"))
        self._anim_var.set(config.get("TINT_ANIM", "instant"))
        self._single_color_var.set(config.get("TINT_SINGLE_COLOR", False))

        self._outer_color = config.get("TINT_COLOR_OUTER", "#660000")
        self._inner_color = config.get("TINT_COLOR_INNER", "#FF2222")
        self._outer_swatch.configure(bg=self._outer_color)
        self._outer_hex_lbl.configure(text=self._outer_color.upper())
        self._inner_swatch.configure(bg=self._inner_color)
        self._inner_hex_lbl.configure(text=self._inner_color.upper())

        self._noise_var.set(config.get("TINT_NOISE", 0.0))
        self._sat_shift_var.set(config.get("TINT_SATURATION_SHIFT", 0.0))
        self._grain_var.set(config.get("TINT_GRAIN", 0.0))
        self._color_anim_curve_var.set(config.get("TINT_COLOR_ANIM_CURVE", 1.0))

        inner_end = config.get("TINT_COLOR_INNER_END")
        outer_end = config.get("TINT_COLOR_OUTER_END")
        self._anim_inner_end_var.set(inner_end is not None)
        self._anim_outer_end_var.set(outer_end is not None)
        if inner_end:
            self._inner_end_color = inner_end
            self._inner_end_swatch.configure(bg=inner_end)
            self._inner_end_hex_lbl.configure(text=inner_end.upper())
        if outer_end:
            self._outer_end_color = outer_end
            self._outer_end_swatch.configure(bg=outer_end)
            self._outer_end_hex_lbl.configure(text=outer_end.upper())

        self._apply_toggle_state()
        self._apply_edge_color_state()
        self._apply_bidir_state()
        self._apply_color_anim_state()
        self._settings_more.sync(config)
        self._anim_more.sync(config)
