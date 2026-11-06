import tkinter as tk
import tkinter.ttk as _tk_ttk
import tkinter.colorchooser as _cc

import ttkbootstrap as ttk

from gui.theme import PALETTE, FONT_BODY, FONT_SMALL, FONT_MONO, Tooltip as _Tooltip
from gui.widgets.controls import MoreOptions, ReadonlyCombo, choice_combo, slider_row
from utils.config import DEFAULT_CONFIG

_PATTERN_OPTIONS = ["random", "noise", "directional", "centrifugal", "centripetal", "chunks", "gravity_aligned"]

_CURVE_OPTIONS = [
    ("Very Early", 0.35),
    ("Early",      0.6),
    ("Linear",     1.0),
    ("Late",       1.8),
    ("Very Late",  3.0),
]

# ------------------------------------------------------------------ #
#  Tooltip strings                                                     #
# ------------------------------------------------------------------ #

_TIP_ENABLE = (
    "Switch the dissolve effect on or off. When off, all the settings below are ignored "
    "and pixels simply remain in place until the animation ends."
)

_TIP_PATTERN = (
    "Controls the order in which pixels disappear as the sprite dissolves.\n\n"
    "Random — pixels vanish in a completely random order across the whole sprite.\n\n"
    "Noise — pixels vanish in a smooth, organic, cloud-like pattern (similar to random but less speckly).\n\n"
    "Directional — pixels vanish in a sweeping wave from one side to the other. "
    "Use the Direction slider below to choose which direction the wave travels.\n\n"
    "Centrifugal — pixels near the centre of the sprite vanish last; outer pixels go first.\n\n"
    "Centripetal — outer pixels vanish last; pixels near the centre disappear first.\n\n"
    "Chunks — entire chunks vanish all at once in a random order. "
    "Great for Thanos-snap shard wink-outs and crystalline shatter effects.\n\n"
    "Gravity-aligned — same as Directional but automatically matches the current Gravity Angle, "
    "so fire/smoke effects always dissolve in the right direction without manual tuning."
)

_TIP_DIRECTION = (
    "Sets the direction the dropout wave travels when Dropout Pattern is set to Directional.\n\n"
    "0° = wave sweeps upward (bottom pixels vanish first).\n"
    "90° = wave sweeps rightward (left pixels vanish first).\n"
    "180° = wave sweeps downward (top pixels vanish first).\n"
    "270° = wave sweeps leftward (right pixels vanish first).\n\n"
    f"This slider is greyed out unless Pattern is set to Directional. (default: {DEFAULT_CONFIG['DISSOLVE_DIRECTION']}°)"
)

_TIP_MIN_KEPT = (
    "How many pixels are still visible in the very last frame of the animation, "
    "expressed as a percentage of the sprite's total opaque pixels.\n\n"
    "0.00% keeps at least 1 pixel (the sprite never becomes completely empty). "
    "At 1% the sprite is nearly gone by the final frame. "
    "At 100% all pixels survive — useful when you only want the Fade color effect "
    "without any pixels disappearing.\n\n"
    "Sub-1% values are meaningful on large sprites (256px+) where 0.01% can still "
    f"represent dozens of pixels. (default: {round(DEFAULT_CONFIG['DISSOLVE_MIN_PCT'] * 100, 2)}%)"
)

_TIP_CURVE = (
    "Controls how quickly pixels start disappearing over the course of the animation.\n\n"
    "Very Early — most pixels vanish in the first third; sprite is nearly gone at the halfway point.\n\n"
    "Early — pixels drop out faster than average; fades quickly then tapers off.\n\n"
    "Linear — pixels drop out at a steady, even pace throughout (default).\n\n"
    "Late — sprite holds together for a long time, then dissolves quickly near the end.\n\n"
    "Very Late — almost all pixels survive until the final frames, then vanish in a rush."
)

_TIP_CHUNK_STAGGER = (
    "Spreads each chunk's dissolve start time across the animation.\n\n"
    "0.0 = all chunks begin dissolving at the same time (current behaviour).\n"
    "1.0 = chunks dissolve fully sequentially — each chunk starts at a random point "
    "across the whole frame range.\n\n"
    "Works with any Dropout Pattern. Useful for turn-to-smoke, evaporate, and wisp effects "
    f"where chunks fade out one by one. (default: {DEFAULT_CONFIG.get('DISSOLVE_CHUNK_STAGGER', 0.0)})"
)

_TIP_FADE_COLOR = (
    "Optional: pixels shift toward this color in the frames just before they vanish. "
    "Great for effects like burning edges (orange/red), freezing (pale blue), or magic (purple glow).\n\n"
    "Click the color swatch or 'Pick…' to choose a color. 'Clear' removes the fade color "
    "so pixels simply disappear without a color shift (None = no shift).\n\n"
    "The Fade strength slider controls how strongly pixels shift toward this color."
)

_TIP_FADE_STRENGTH = (
    "How strongly pixels shift toward the Fade color in the frame just before they disappear.\n\n"
    "0.0 = no shift at all (same result as having no Fade color).\n"
    "1.0 = pixels fully become the Fade color before vanishing.\n\n"
    f"(default: {DEFAULT_CONFIG['DISSOLVE_FADE_STRENGTH']})"
)


class DissolveTab:
    def __init__(self, parent, config: dict, app):
        self._cfg = config
        self._app = app

        self._dissolve_enabled = config.get("DISSOLVE", False)

        # tk.Vars
        self._enabled_var      = tk.BooleanVar(value=self._dissolve_enabled)
        self._pattern_var      = tk.StringVar(value=config.get("DISSOLVE_PATTERN", "random"))
        self._direction_var    = tk.IntVar(value=config.get("DISSOLVE_DIRECTION", 180))
        # Min pct stored as float (0.0–1.0); displayed as float percent (0.00–100.00)
        self._min_pct_var      = tk.DoubleVar(value=round(config.get("DISSOLVE_MIN_PCT", 0.01) * 100, 2))
        self._curve_label_var   = tk.StringVar(
            value=self._float_to_curve_label(config.get("DISSOLVE_CURVE", 1.0))
        )
        self._chunk_stagger_var = tk.DoubleVar(value=config.get("DISSOLVE_CHUNK_STAGGER", 0.0))
        self._fade_strength_var = tk.DoubleVar(value=config.get("DISSOLVE_FADE_STRENGTH", 0.5))

        # Fade color stored as plain str (not tk.StringVar) — same approach as tint.py
        raw_color = config.get("DISSOLVE_FADE_COLOR", None)
        self._fade_color: str | None = raw_color  # None or hex string

        # Widget groups for bulk state management
        self._toggleable:      list = []   # all controls below master toggle
        self._direction_widgets: list = [] # direction Scale + readout only
        self._fade_toggleable: list = []   # fade strength Scale + readout only
        # Swatch managed separately (no state= option)
        self._fade_swatch:  tk.Canvas | None = None
        self._fade_hex_lbl: ttk.Label | None = None
        self._fade_swatch_click = None     # stored callback for rebind

        self._build(parent)
        self._apply_toggle_state()

    @staticmethod
    def _float_to_curve_label(value: float) -> str:
        return min(_CURVE_OPTIONS, key=lambda opt: abs(opt[1] - value))[0]

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def _build(self, parent):
        parent.columnconfigure(0, weight=1)

        # Section 1 — master enable toggle
        en_frame = _tk_ttk.LabelFrame(parent, text="Dissolve", padding=8)
        en_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=(10, 4))
        en_frame.columnconfigure(0, weight=1)

        en_cb = ttk.Checkbutton(
            en_frame,
            text="Enable dissolve",
            variable=self._enabled_var,
            bootstyle="round-toggle",
            command=self._on_toggle,
        )
        en_cb.grid(row=0, column=0, sticky="w")
        _Tooltip(en_cb, _TIP_ENABLE)

        # Section 2 — Settings
        self._build_settings(parent, row=1)


    def _build_settings(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Settings", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=4)
        frame.columnconfigure(0, weight=1)

        # Pattern dropdown
        pat_row = ttk.Frame(frame)
        pat_row.grid(row=0, column=0, sticky="ew", pady=(0, 2))
        pat_row.columnconfigure(1, weight=1)

        pat_lbl = ttk.Label(pat_row, text="Dropout Pattern", font=FONT_BODY,
                            background=PALETTE["bg_surface"])
        pat_lbl.grid(row=0, column=0, sticky="w", padx=(0, 8))
        _Tooltip(pat_lbl, _TIP_PATTERN)

        self._pattern_combo = choice_combo(
            pat_row, self._pattern_var, _PATTERN_OPTIONS, self._on_pattern_change, width=16,
        )
        self._pattern_combo.grid(row=0, column=1, sticky="w")
        _Tooltip(self._pattern_combo, _TIP_PATTERN)
        self._toggleable.append(self._pattern_combo)

        # Direction slider (only active when pattern="directional")
        dir_frame, dir_scale, dir_readout = self._add_int_slider(
            frame, row=1, label="Direction", var=self._direction_var,
            from_=0, to=360, key="DISSOLVE_DIRECTION", display_suffix="°",
            tooltip=_TIP_DIRECTION,
        )
        # Override: direction widgets are NOT in _toggleable — managed separately
        # _add_int_slider already appended scale+readout to _toggleable; remove them
        self._toggleable.remove(dir_scale)
        self._toggleable.remove(dir_readout)
        self._direction_widgets = [dir_scale, dir_readout]

        # Min survive — slider (coarse) + spinbox (precision), same DoubleVar
        min_row = ttk.Frame(frame)
        min_row.grid(row=2, column=0, sticky="ew", pady=2)
        min_row.columnconfigure(1, weight=1)

        min_lbl = ttk.Label(min_row, text="Minimum kept", font=FONT_BODY,
                            background=PALETTE["bg_base"])
        min_lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
        _Tooltip(min_lbl, _TIP_MIN_KEPT)

        def _snap_min_pct(v):
            self._min_pct_var.set(round(float(v), 2))

        # Slider covers the useful 0–50 %; the spinbox takes the full 0–100 %.
        min_slider = ttk.Scale(min_row, variable=self._min_pct_var,
                               from_=0.0, to=50.0, orient="horizontal",
                               command=_snap_min_pct)
        min_slider.grid(row=0, column=1, sticky="ew", padx=4)
        def _on_slider_release(_e):
            snapped = round(self._min_pct_var.get(), 2)
            self._min_pct_var.set(snapped)
            self._save_min_pct()

        min_slider.bind("<ButtonRelease-1>", _on_slider_release)

        def _reset_min_pct(_e):
            if str(min_slider.cget("state")) != "disabled":
                self._min_pct_var.set(round(DEFAULT_CONFIG["DISSOLVE_MIN_PCT"] * 100, 2))
                self._save_min_pct()
            return "break"

        min_slider.bind("<Double-Button-1>", _reset_min_pct)
        _Tooltip(min_slider, _TIP_MIN_KEPT + "\n\nDouble-click the slider to reset it.")

        self._min_pct_sb = ttk.Spinbox(
            min_row, from_=0.0, to=100.0, increment=0.01,
            textvariable=self._min_pct_var,
            width=6, font=FONT_SMALL, format="%.2f",
        )
        self._min_pct_sb.grid(row=0, column=2, sticky="e", padx=(0, 2))
        _Tooltip(self._min_pct_sb, _TIP_MIN_KEPT)

        pct_lbl = ttk.Label(min_row, text="%", font=FONT_SMALL,
                            bootstyle="secondary")
        pct_lbl.grid(row=0, column=3, sticky="w")

        def _save_min_pct_sb(e=None):
            try:
                v = float(self._min_pct_sb.get())
            except (ValueError, tk.TclError):
                v = 1.0
            v = max(0.0, min(100.0, round(v, 2)))
            self._min_pct_var.set(v)
            self._save_min_pct()

        self._min_pct_sb.bind("<<Increment>>", _save_min_pct_sb)
        self._min_pct_sb.bind("<<Decrement>>", _save_min_pct_sb)
        self._min_pct_sb.bind("<FocusOut>",    _save_min_pct_sb)
        self._min_pct_sb.bind("<Return>",      _save_min_pct_sb)

        self._toggleable.extend([min_slider, self._min_pct_sb])

        # Dropout timing dropdown
        curve_row = ttk.Frame(frame)
        curve_row.grid(row=3, column=0, sticky="ew", pady=(0, 2))
        curve_row.columnconfigure(1, weight=1)

        curve_lbl = ttk.Label(curve_row, text="Dropout timing", font=FONT_BODY,
                              background=PALETTE["bg_surface"])
        curve_lbl.grid(row=0, column=0, sticky="w", padx=(0, 8))
        _Tooltip(curve_lbl, _TIP_CURVE)

        self._curve_combo = ReadonlyCombo(
            curve_row,
            textvariable=self._curve_label_var,
            values=[label for label, _ in _CURVE_OPTIONS],
            state="readonly",
            font=FONT_BODY,
            width=14,
        )
        self._curve_combo.grid(row=0, column=1, sticky="w")
        self._curve_combo.bind("<<ComboboxSelected>>", self._on_curve_change)
        _Tooltip(self._curve_combo, _TIP_CURVE)
        self._toggleable.append(self._curve_combo)

        # Chunk stagger + fade color are advanced
        self._more = MoreOptions(
            frame, ["DISSOLVE_CHUNK_STAGGER", "DISSOLVE_FADE_COLOR", "DISSOLVE_FADE_STRENGTH"],
            text="Stagger & fade color")
        self._more.grid(row=4, column=0, sticky="ew")

        self._add_float_slider(
            self._more.body, row=0, label="Chunk stagger", var=self._chunk_stagger_var,
            from_=0.0, to=1.0, dp=2, key="DISSOLVE_CHUNK_STAGGER",
            tooltip=_TIP_CHUNK_STAGGER,
        )
        self._build_fade(self._more.body, row=1)

    def _build_fade(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Fade color", padding=8)
        frame.grid(row=row, column=0, sticky="ew", pady=(4, 2))
        frame.columnconfigure(0, weight=1)

        # Color row
        color_row = ttk.Frame(frame)
        color_row.grid(row=0, column=0, sticky="ew", pady=(0, 4))

        fade_lbl = ttk.Label(color_row, text="Fade color", font=FONT_BODY,
                             background=PALETTE["bg_surface"])
        fade_lbl.pack(side="left", padx=(0, 6))
        _Tooltip(fade_lbl, _TIP_FADE_COLOR)

        swatch_bg = self._fade_color if self._fade_color else PALETTE["bg_surface"]
        self._fade_swatch = tk.Canvas(
            color_row, width=24, height=18, highlightthickness=1,
            highlightbackground=PALETTE["accent_glow"],
            bg=swatch_bg,
        )
        self._fade_swatch.pack(side="left", padx=(0, 4))
        _Tooltip(self._fade_swatch, _TIP_FADE_COLOR)

        hex_text = self._fade_color.upper() if self._fade_color else "None"
        self._fade_hex_lbl = ttk.Label(
            color_row, text=hex_text, font=FONT_MONO, width=8,
            background=PALETTE["bg_surface"],
        )
        self._fade_hex_lbl.pack(side="left", padx=(0, 6))

        pick_btn = ttk.Button(color_row, text="Pick…", width=6, command=self._pick_fade_color)
        pick_btn.pack(side="left", padx=(0, 4))
        _Tooltip(pick_btn, _TIP_FADE_COLOR)
        self._toggleable.append(pick_btn)

        clear_btn = ttk.Button(color_row, text="Clear", width=6, command=self._clear_fade_color)
        clear_btn.pack(side="left")
        _Tooltip(clear_btn, _TIP_FADE_COLOR)
        self._toggleable.append(clear_btn)

        # Swatch click — store callback for rebind
        def _swatch_click(e):
            self._pick_fade_color()
        self._fade_swatch_click = _swatch_click
        self._fade_swatch.bind("<Button-1>", _swatch_click)

        # Fade strength slider — appended to both _toggleable and _fade_toggleable
        str_frame, str_scale, str_readout = self._add_float_slider(
            frame, row=1, label="Fade strength", var=self._fade_strength_var,
            from_=0.0, to=1.0, dp=2, key="DISSOLVE_FADE_STRENGTH",
            tooltip=_TIP_FADE_STRENGTH,
        )
        # Move from _toggleable to _fade_toggleable so they're controlled independently
        self._toggleable.remove(str_scale)
        self._toggleable.remove(str_readout)
        self._fade_toggleable = [str_scale, str_readout]

    # ------------------------------------------------------------------ #
    #  Slider helpers (mirrors tint.py pattern)                           #
    # ------------------------------------------------------------------ #

    def _add_int_slider(self, parent, row, label, var, from_, to, key,
                        display_suffix="", tooltip=None):
        rf, slider, readout, _lbl = slider_row(
            parent, row, label, var, from_, to,
            commit=lambda k=key, v=var: self._save(k, int(v.get())),
            default=DEFAULT_CONFIG.get(key), suffix=display_suffix,
            tooltip=tooltip, tooltip_cls=_Tooltip)
        self._toggleable.extend([slider, readout])
        return rf, slider, readout

    def _add_float_slider(self, parent, row, label, var, from_, to, dp, key,
                          tooltip=None):
        rf, slider, readout, _lbl = slider_row(
            parent, row, label, var, from_, to,
            commit=lambda k=key, v=var, d=dp: self._save(k, round(float(v.get()), d)),
            dp=dp, default=DEFAULT_CONFIG.get(key), tooltip=tooltip, tooltip_cls=_Tooltip)
        self._toggleable.extend([slider, readout])
        return rf, slider, readout

    # ------------------------------------------------------------------ #
    #  Toggle                                                              #
    # ------------------------------------------------------------------ #

    def _on_toggle(self):
        self._dissolve_enabled = self._enabled_var.get()
        self._save("DISSOLVE", self._dissolve_enabled)
        self._apply_toggle_state()
        self._apply_direction_state()
        self._apply_fade_state()

    def _apply_toggle_state(self):
        state = "normal" if self._dissolve_enabled else "disabled"
        for w in self._toggleable:
            try:
                w.configure(state=state)
            except tk.TclError:
                pass
        # Swatch: bind/unbind click; cursor follows
        if self._fade_swatch is not None:
            if self._dissolve_enabled and self._fade_color is not None:
                self._fade_swatch.bind("<Button-1>", self._fade_swatch_click)
                self._fade_swatch.configure(cursor="hand2")
            else:
                self._fade_swatch.unbind("<Button-1>")
                self._fade_swatch.configure(cursor="")

    # ------------------------------------------------------------------ #
    #  Pattern / Direction                                                 #
    # ------------------------------------------------------------------ #

    def _on_pattern_change(self, event=None):
        self._save("DISSOLVE_PATTERN", self._pattern_var.get())
        self._apply_direction_state()

    def _on_curve_change(self, event=None):
        label = self._curve_label_var.get()
        float_val = next(v for lbl, v in _CURVE_OPTIONS if lbl == label)
        self._save("DISSOLVE_CURVE", float_val)

    def _apply_direction_state(self):
        active = self._dissolve_enabled and self._pattern_var.get() == "directional"
        state = "normal" if active else "disabled"
        for w in self._direction_widgets:
            try:
                w.configure(state=state)
            except tk.TclError:
                pass

    # ------------------------------------------------------------------ #
    #  Fade color                                                          #
    # ------------------------------------------------------------------ #

    def _pick_fade_color(self):
        initial = self._fade_color if self._fade_color else "#ffffff"
        result = _cc.askcolor(color=initial, title="Fade color")
        if result and result[1]:
            hex_val = result[1].upper()
            self._fade_color = hex_val
            self._fade_swatch.configure(bg=hex_val)
            self._fade_hex_lbl.configure(text=hex_val)
            self._save("DISSOLVE_FADE_COLOR", hex_val)
            self._apply_fade_state()
            self._apply_toggle_state()  # re-sync swatch cursor/bind

    def _clear_fade_color(self):
        self._fade_color = None
        self._fade_swatch.configure(bg=PALETTE["bg_surface"])
        self._fade_hex_lbl.configure(text="None")
        self._save("DISSOLVE_FADE_COLOR", None)
        self._apply_fade_state()
        self._apply_toggle_state()  # remove swatch cursor/bind

    def _apply_fade_state(self):
        active = self._dissolve_enabled and self._fade_color is not None
        state = "normal" if active else "disabled"
        for w in self._fade_toggleable:
            try:
                w.configure(state=state)
            except tk.TclError:
                pass

    # ------------------------------------------------------------------ #
    #  Save helpers                                                        #
    # ------------------------------------------------------------------ #

    def _save_min_pct(self):
        self._save("DISSOLVE_MIN_PCT", self._min_pct_var.get() / 100.0)

    def _save(self, key, value):
        self._cfg[key] = value
        self._app.save_config()
        self._app.mark_preview_dirty()

    # ------------------------------------------------------------------ #
    #  Refresh (called by app._refresh_all_tabs after preset load)        #
    # ------------------------------------------------------------------ #

    def refresh(self, config):
        self._cfg = config

        enabled = config.get("DISSOLVE", False)
        self._dissolve_enabled = enabled
        self._enabled_var.set(enabled)

        self._pattern_var.set(config.get("DISSOLVE_PATTERN", "random"))
        self._direction_var.set(config.get("DISSOLVE_DIRECTION", 180))
        self._min_pct_var.set(round(config.get("DISSOLVE_MIN_PCT", 0.01) * 100, 2))
        self._curve_label_var.set(self._float_to_curve_label(config.get("DISSOLVE_CURVE", 1.0)))
        self._chunk_stagger_var.set(config.get("DISSOLVE_CHUNK_STAGGER", 0.0))
        self._fade_strength_var.set(config.get("DISSOLVE_FADE_STRENGTH", 0.5))

        raw = config.get("DISSOLVE_FADE_COLOR", None)
        self._fade_color = raw
        if raw:
            self._fade_swatch.configure(bg=raw.upper())
            self._fade_hex_lbl.configure(text=raw.upper())
        else:
            self._fade_swatch.configure(bg=PALETTE["bg_surface"])
            self._fade_hex_lbl.configure(text="None")

        self._apply_toggle_state()
        self._apply_direction_state()
        self._apply_fade_state()
        self._more.sync(config)
