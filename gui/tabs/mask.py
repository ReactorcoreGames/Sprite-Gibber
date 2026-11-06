import os
import re
import tkinter as tk
import tkinter.ttk as _tk_ttk

import ttkbootstrap as ttk
from PIL import Image, ImageTk

from gui.theme import PALETTE, FONT_BODY, FONT_SMALL, FONT_MONO, Tooltip as _Tooltip
from gui.widgets.controls import MoreOptions, choice_combo, slider_row
from utils.config import DEFAULT_CONFIG

_FIT_OPTIONS  = ["stretch", "fit", "crop_center"]
_ANIM_OPTIONS = ["instant", "linear", "early", "late", "pulse"]

_THUMB_SIZE   = 64  # px per cell image
_GRID_COLS    = 6
_GRID_HEIGHT  = 380  # max height of scrollable canvas

# ------------------------------------------------------------------ #
#  Tooltip strings                                                     #
# ------------------------------------------------------------------ #

_TIP_MASK = (
    "Click a mask thumbnail to select it. White areas keep pixels; black areas force "
    "them transparent.\n\n"
    "Mask is applied at render time only — physics is unaffected. "
    "Frame 0 (intact sprite) is always unmasked."
)

_TIP_NONE = (
    "Disable masking — no mask image is applied to output frames."
)

_TIP_FIT = (
    "Controls how the mask image is scaled to fit the sprite canvas.\n\n"
    "Stretch — fills the canvas exactly; distorts aspect ratio (default; fine at pixel-art scale).\n"
    "Fit — scales uniformly to fit within canvas, letterboxed with transparent padding.\n"
    "Crop to fill — scales uniformly to fill canvas, then center-crops any overflow."
)

_TIP_SOFTNESS = (
    "Gaussian blur radius applied to the mask before compositing.\n\n"
    "0 = hard crisp edge (default).\n"
    "Higher values feather the mask boundary for softer, smoother fade-outs.\n\n"
    f"(default: {DEFAULT_CONFIG['FRAME_MASK_SOFTNESS']})"
)

_TIP_FLIP = (
    "Flip the mask image vertically (top becomes bottom).\n\n"
    "Useful when the mask was designed for a different gravity direction."
)

_TIP_MIRROR = (
    "Mirror the mask image horizontally (left becomes right).\n\n"
    "Useful for asymmetric masks that need to face the other direction."
)

_TIP_ROTATE90 = (
    "Rotate the mask image 90 degrees clockwise.\n\n"
    "Combine with Flip and Mirror to reach any of the 4 rotations you need."
)

_TIP_ANIM = (
    "Controls how mask opacity builds up across frames. Frame 0 is always unmasked.\n\n"
    "Instant — mask snaps to full strength at frame 1.\n"
    "Linear — opacity ramps evenly from frame 1 to the last frame.\n"
    "Early — opacity reaches full strength quickly in the first third of the animation.\n"
    "Late — opacity holds weak then surges near the end.\n"
    "Pulse — opacity peaks at the mid-point of the animation and fades back out."
)

_TIP_REFRESH = (
    "Re-scan assets/masks/ for new PNG files added since the app launched. "
    "Use this if you drop new mask images into the folder while the app is open."
)


def _masks_dir() -> str:
    """Return the absolute path to assets/masks/ whether running frozen or from source."""
    from utils.paths import masks_dir
    return str(masks_dir())


def _natural_key(name: str):
    """Sort key for natural ordering: 'Splat (10).png' comes after 'Splat (9).png'."""
    parts = re.split(r"(\d+)", name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def list_mask_files() -> list[str]:
    """Return naturally-sorted list of .png filenames in assets/masks/."""
    d = _masks_dir()
    if not os.path.isdir(d):
        return []
    return sorted(
        (f for f in os.listdir(d) if f.lower().endswith(".png")),
        key=_natural_key,
    )


class MaskTab:
    def __init__(self, parent, config: dict, app):
        self._cfg = config
        self._app = app

        # tk.Vars
        self._mask_var      = tk.StringVar(value=config.get("FRAME_MASK") or "None")
        self._fit_var       = tk.StringVar(value=config.get("FRAME_MASK_FIT", "stretch"))
        self._softness_var  = tk.IntVar(value=config.get("FRAME_MASK_SOFTNESS", 0))
        self._flip_var      = tk.BooleanVar(value=config.get("FRAME_MASK_FLIP", False))
        self._mirror_var    = tk.BooleanVar(value=config.get("FRAME_MASK_MIRROR", False))
        self._rotate90_var  = tk.BooleanVar(value=config.get("FRAME_MASK_ROTATE90", False))
        self._anim_var      = tk.StringVar(value=config.get("FRAME_MASK_ANIM", "instant"))

        # Thumbnail cache: filename → ImageTk.PhotoImage (kept to prevent GC)
        self._thumb_cache: dict[str, ImageTk.PhotoImage] = {}

        # Grid cell widgets: filename → (outer_frame, img_label, name_label)
        self._cell_widgets: dict[str, tuple] = {}

        # Scrollable canvas refs
        self._grid_canvas: tk.Canvas | None = None
        self._grid_frame: ttk.Frame | None = None

        # Status label ref
        self._status_label: ttk.Label | None = None

        # None-button ref (for highlight toggling)
        self._none_btn: ttk.Button | None = None

        # Settings widget group (enabled only when a mask is selected)
        self._settings_widgets: list = []

        self._build(parent)
        self._update_status()
        self._apply_enabled_state()

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def _build(self, parent):
        parent.columnconfigure(0, weight=1)
        self._build_image_section(parent, row=0)
        self._build_settings_section(parent, row=1)

    def _build_image_section(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Mask image", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=(10, 4))
        frame.columnconfigure(0, weight=1)

        # Row 0: "None" deselect button
        none_frame = ttk.Frame(frame)
        none_frame.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        none_frame.columnconfigure(0, weight=0)

        self._none_btn = ttk.Button(
            none_frame,
            text="None (no mask)",
            bootstyle="secondary",
            command=lambda: self._select_mask("None"),
            width=18,
        )
        self._none_btn.pack(side="left")
        _Tooltip(self._none_btn, _TIP_NONE)

        # Row 1: scrollable thumbnail grid
        grid_outer = ttk.Frame(frame)
        grid_outer.grid(row=1, column=0, sticky="ew", pady=(0, 4))
        grid_outer.columnconfigure(0, weight=1)

        self._grid_canvas = tk.Canvas(
            grid_outer,
            height=_GRID_HEIGHT,
            highlightthickness=1,
            highlightbackground=PALETTE["accent_glow"],
            bg=PALETTE["bg_surface"],
        )
        self._grid_canvas.grid(row=0, column=0, sticky="ew")

        scrollbar = ttk.Scrollbar(grid_outer, orient="vertical",
                                  command=self._grid_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._grid_canvas.configure(yscrollcommand=scrollbar.set)

        self._grid_frame = ttk.Frame(self._grid_canvas)
        self._grid_canvas_window = self._grid_canvas.create_window(
            (0, 0), window=self._grid_frame, anchor="nw"
        )

        self._grid_frame.bind("<Configure>", self._on_grid_frame_resize)
        self._grid_canvas.bind("<Configure>", self._on_canvas_resize)
        self._grid_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self._grid_frame.bind("<MouseWheel>", self._on_mousewheel)

        # Row 2: status bar (selected name + Refresh button)
        status_row = ttk.Frame(frame)
        status_row.grid(row=2, column=0, sticky="ew", pady=(2, 0))
        status_row.columnconfigure(0, weight=1)

        self._status_label = ttk.Label(
            status_row,
            text=self._status_text(),
            font=FONT_SMALL,
            bootstyle="secondary",
        )
        self._status_label.grid(row=0, column=0, sticky="w")

        ref_btn = ttk.Button(
            status_row, text="Refresh", bootstyle="secondary",
            command=self._refresh_grid, width=8,
        )
        ref_btn.grid(row=0, column=1, sticky="e")
        _Tooltip(ref_btn, _TIP_REFRESH)

        # Populate grid
        self._refresh_grid()

    def _build_settings_section(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Settings", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=(4, 10))
        frame.columnconfigure(0, weight=1)

        # Fit mode
        fit_row = ttk.Frame(frame)
        fit_row.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        fit_row.columnconfigure(1, weight=1)

        fit_lbl = ttk.Label(fit_row, text="Fit mode", font=FONT_BODY,
                            background=PALETTE["bg_surface"])
        fit_lbl.grid(row=0, column=0, sticky="w", padx=(0, 8))
        _Tooltip(fit_lbl, _TIP_FIT)

        fit_combo = choice_combo(
            fit_row, self._fit_var, _FIT_OPTIONS,
            lambda e: self._save("FRAME_MASK_FIT", self._fit_var.get()), width=12,
        )
        fit_combo.grid(row=0, column=1, sticky="w")
        _Tooltip(fit_combo, _TIP_FIT)
        self._settings_widgets.append(fit_combo)

        # Softness slider
        _sf, sf_scale, sf_readout = self._add_int_slider(
            frame, row=1, label="Softness", var=self._softness_var,
            from_=0, to=10, key="FRAME_MASK_SOFTNESS", limits=(0, 20),
            tooltip=_TIP_SOFTNESS,
        )

        # Anim mode
        anim_row = ttk.Frame(frame)
        anim_row.grid(row=2, column=0, sticky="ew", pady=(4, 0))
        anim_row.columnconfigure(1, weight=1)

        anim_lbl = ttk.Label(anim_row, text="Mask animation", font=FONT_BODY,
                             background=PALETTE["bg_surface"])
        anim_lbl.grid(row=0, column=0, sticky="w", padx=(0, 8))
        _Tooltip(anim_lbl, _TIP_ANIM)

        anim_combo = choice_combo(
            anim_row, self._anim_var, _ANIM_OPTIONS,
            lambda e: self._save("FRAME_MASK_ANIM", self._anim_var.get()), width=10,
        )
        anim_combo.grid(row=0, column=1, sticky="w")
        _Tooltip(anim_combo, _TIP_ANIM)
        self._settings_widgets.append(anim_combo)

        # Flip / mirror / rotate are advanced
        self._more = MoreOptions(
            frame, ["FRAME_MASK_FLIP", "FRAME_MASK_MIRROR", "FRAME_MASK_ROTATE90"],
            text="Flip, mirror & rotate")
        self._more.grid(row=3, column=0, sticky="ew")
        more = self._more.body

        # Flip checkbox
        flip_cb = ttk.Checkbutton(
            more, text="Flip (vertical)",
            variable=self._flip_var,
            command=lambda: self._save("FRAME_MASK_FLIP", self._flip_var.get()),
        )
        flip_cb.grid(row=0, column=0, sticky="w", pady=(4, 2))
        _Tooltip(flip_cb, _TIP_FLIP)
        self._settings_widgets.append(flip_cb)

        # Mirror checkbox
        mirror_cb = ttk.Checkbutton(
            more, text="Mirror (horizontal)",
            variable=self._mirror_var,
            command=lambda: self._save("FRAME_MASK_MIRROR", self._mirror_var.get()),
        )
        mirror_cb.grid(row=1, column=0, sticky="w", pady=(2, 4))
        _Tooltip(mirror_cb, _TIP_MIRROR)
        self._settings_widgets.append(mirror_cb)

        # Rotate 90 checkbox
        rotate90_cb = ttk.Checkbutton(
            more, text="Rotate 90° (clockwise)",
            variable=self._rotate90_var,
            command=lambda: self._save("FRAME_MASK_ROTATE90", self._rotate90_var.get()),
        )
        rotate90_cb.grid(row=2, column=0, sticky="w", pady=(2, 4))
        _Tooltip(rotate90_cb, _TIP_ROTATE90)
        self._settings_widgets.append(rotate90_cb)

    # ------------------------------------------------------------------ #
    #  Slider helper (matches dissolve.py pattern)                        #
    # ------------------------------------------------------------------ #

    def _add_int_slider(self, parent, row, label, var, from_, to, key,
                        limits=None, tooltip=None):
        rf, slider, readout, _lbl = slider_row(
            parent, row, label, var, from_, to,
            commit=lambda k=key, v=var: self._save(k, int(v.get())),
            limits=limits, default=DEFAULT_CONFIG.get(key),
            tooltip=tooltip, tooltip_cls=_Tooltip)
        self._settings_widgets.extend([slider, readout])
        return rf, slider, readout

    # ------------------------------------------------------------------ #
    #  Thumbnail loading                                                   #
    # ------------------------------------------------------------------ #

    def _load_thumbnail(self, filename: str) -> ImageTk.PhotoImage | None:
        """Load (or return cached) thumbnail PhotoImage for a mask filename."""
        if filename in self._thumb_cache:
            return self._thumb_cache[filename]
        mask_path = os.path.join(_masks_dir(), filename)
        if not os.path.exists(mask_path):
            return None
        try:
            img = Image.open(mask_path).convert("L").resize(
                (_THUMB_SIZE, _THUMB_SIZE), Image.NEAREST
            )
            photo = ImageTk.PhotoImage(img)
            self._thumb_cache[filename] = photo
            return photo
        except Exception:
            return None

    # ------------------------------------------------------------------ #
    #  Grid build / refresh                                                #
    # ------------------------------------------------------------------ #

    def _refresh_grid(self):
        """Re-scan disk and rebuild the thumbnail grid."""
        # Destroy existing cell widgets
        for w in self._grid_frame.winfo_children():
            w.destroy()
        self._cell_widgets.clear()

        files = list_mask_files()
        for idx, filename in enumerate(files):
            row = idx // _GRID_COLS
            col = idx % _GRID_COLS

            photo = self._load_thumbnail(filename)

            # Outer frame acts as the selection border
            cell = tk.Frame(
                self._grid_frame,
                bd=2,
                relief="flat",
                highlightthickness=2,
                highlightbackground=PALETTE["bg_base"],
                bg=PALETTE["bg_surface"],
                cursor="hand2",
            )
            cell.grid(row=row, column=col, padx=3, pady=3)

            # Image label
            img_lbl = tk.Label(
                cell,
                image=photo if photo else None,
                width=_THUMB_SIZE,
                height=_THUMB_SIZE,
                bg=PALETTE["bg_surface"],
                cursor="hand2",
            )
            img_lbl.pack()

            # Short name label (strip extension, truncate)
            short = os.path.splitext(filename)[0]
            if len(short) > 20:
                short = short[:19] + "…"
            name_lbl = tk.Label(
                cell,
                text=short,
                font=FONT_SMALL,
                bg=PALETTE["bg_surface"],
                fg=PALETTE["text_secondary"],
                cursor="hand2",
                wraplength=_THUMB_SIZE,
            )
            name_lbl.pack()

            # Bind clicks on all three widgets
            for widget in (cell, img_lbl, name_lbl):
                widget.bind("<Button-1>", lambda e, f=filename: self._select_mask(f))
                widget.bind("<MouseWheel>", self._on_mousewheel)

            _Tooltip(cell, filename)

            self._cell_widgets[filename] = (cell, img_lbl, name_lbl)

        # Configure columns to distribute space equally
        for c in range(_GRID_COLS):
            self._grid_frame.columnconfigure(c, weight=1)

        self._highlight_selected()

    # ------------------------------------------------------------------ #
    #  Canvas scroll helpers                                               #
    # ------------------------------------------------------------------ #

    def _on_grid_frame_resize(self, event=None):
        self._grid_canvas.configure(scrollregion=self._grid_canvas.bbox("all"))

    def _on_canvas_resize(self, event=None):
        self._grid_canvas.itemconfig(
            self._grid_canvas_window, width=event.width if event else None
        )

    def _on_mousewheel(self, event):
        self._grid_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ------------------------------------------------------------------ #
    #  Mask selection                                                      #
    # ------------------------------------------------------------------ #

    def _select_mask(self, name: str):
        self._mask_var.set(name)
        value = None if name == "None" else name
        self._save("FRAME_MASK", value)
        self._highlight_selected()
        self._update_status()
        self._apply_enabled_state()

    def _highlight_selected(self):
        """Update border highlight to reflect the current selection."""
        current = self._mask_var.get()

        # None button styling
        if self._none_btn:
            if current == "None":
                self._none_btn.configure(bootstyle="primary")
            else:
                self._none_btn.configure(bootstyle="secondary")

        # Thumbnail cell borders
        for filename, (cell, img_lbl, name_lbl) in self._cell_widgets.items():
            if filename == current:
                cell.configure(
                    highlightbackground=PALETTE["accent_glow"],
                    bg=PALETTE["bg_base"],
                )
                img_lbl.configure(bg=PALETTE["bg_base"])
                name_lbl.configure(bg=PALETTE["bg_base"])
            else:
                cell.configure(
                    highlightbackground=PALETTE["bg_base"],
                    bg=PALETTE["bg_surface"],
                )
                img_lbl.configure(bg=PALETTE["bg_surface"])
                name_lbl.configure(bg=PALETTE["bg_surface"])

    def _update_status(self):
        if self._status_label:
            current = self._mask_var.get()
            selected = current and current != "None"
            self._status_label.configure(
                text=self._status_text(),
                foreground=PALETTE["success"] if selected else PALETTE["danger"],
            )

    def _status_text(self) -> str:
        current = self._mask_var.get()
        if current == "None" or not current:
            return "No mask selected"
        return f"Selected: {current}"

    # ------------------------------------------------------------------ #
    #  Enabled state                                                       #
    # ------------------------------------------------------------------ #

    def _apply_enabled_state(self):
        active = self._mask_var.get() != "None"
        state = "normal" if active else "disabled"
        for w in self._settings_widgets:
            try:
                w.configure(state=state)
            except tk.TclError:
                pass

    # ------------------------------------------------------------------ #
    #  Save helper                                                         #
    # ------------------------------------------------------------------ #

    def _save(self, key, value):
        self._cfg[key] = value
        self._app.save_config()
        self._app.mark_preview_dirty()

    # ------------------------------------------------------------------ #
    #  Refresh (called by app._refresh_all_tabs after preset load)        #
    # ------------------------------------------------------------------ #

    def refresh(self, config):
        self._cfg = config

        raw = config.get("FRAME_MASK", None)
        display = raw if raw else "None"
        self._mask_var.set(display)
        self._fit_var.set(config.get("FRAME_MASK_FIT", "stretch"))
        self._softness_var.set(config.get("FRAME_MASK_SOFTNESS", 0))
        self._flip_var.set(config.get("FRAME_MASK_FLIP", False))
        self._mirror_var.set(config.get("FRAME_MASK_MIRROR", False))
        self._rotate90_var.set(config.get("FRAME_MASK_ROTATE90", False))
        self._anim_var.set(config.get("FRAME_MASK_ANIM", "instant"))

        self._highlight_selected()
        self._update_status()
        self._apply_enabled_state()
        self._more.sync(config)
