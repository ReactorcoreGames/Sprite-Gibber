import colorsys
import os
import threading
import tkinter as tk
import tkinter.ttk as _tk_ttk

import numpy as np
import ttkbootstrap as ttk
from PIL import Image, ImageTk

from gui.theme import PALETTE, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_TINY, FONT_SPINBOX, Tooltip as _Tooltip
from utils.config import DEFAULT_CONFIG
from utils.log import log, short_reason


_PLACEHOLDER = "No preview — click Update Preview"
_EMPTY_LIST_TEXT = ("Add sprites to get started\n\n"
                    "Open the Sprites & Export tab and click\n"
                    "Add files… or Add folder…")

# Update Preview button state colors
_BTN_OK_BG        = "#2EAA3E"  # forest green
_BTN_OK_BORDER    = "#1FEC2D"  # bright green
_BTN_DIRTY_BG     = "#C0392B"  # vivid red
_BTN_DIRTY_BORDER = "#F0E040"  # orange
_BTN_BUSY_BG      = "#555555"  # neutral grey
_BTN_BUSY_BORDER  = "#F0C040"  # yellow

# Luminosity levels: index → L value (HLS)
_LUMI_LEVELS = [0.95, 0.75, 0.50, 0.25, 0.05]
_LUMI_LABELS = ["White", "Light", "Mid", "Dark", "Black"]

# Hue table: key → H in degrees, or None for neutral grey
_COLR_HUES = {
    "Red":    0,
    "Orange": 30,
    "Yellow": 60,
    "Green":  120,
    "Blue":   210,
    "Indigo": 240,
    "Violet": 270,
    "Brown":  25,
    "Grey":   None,
}
_COLR_KEYS = list(_COLR_HUES.keys())

# Saturation values
_SATU_VALUES = {"Lo": 0.40, "Hi": 0.80}

_SWATCH_SIZE = 20  # canvas swatch square side length in pixels

# ------------------------------------------------------------------ #
#  Tooltip strings                                                     #
# ------------------------------------------------------------------ #

_TIP_UPDATE_BTN = (
    "Regenerates the preview with your current settings.\n\n"
    "Green = preview is up to date.\n"
    "Red = settings have changed since the last preview — click to refresh.\n"
    "Grey = currently rendering, please wait.\n\n"
    "With Live on, the preview refreshes by itself after each change."
)

_TIP_LIVE = (
    "Live preview: the preview re-renders by itself a moment after you change a setting.\n\n"
    "It switches itself off when a render takes longer than about 1.5 seconds "
    "(big sprites, many frames or chunks) so the app stays responsive — then use "
    "Update Preview, or tick Live again."
)

_LIVE_DEBOUNCE_MS = 300   # quiet time after the last change before a live render starts
_SLOW_RENDER_MS   = 1500  # a render running longer than this pauses live mode

_TIP_FRAMES = (
    f"How many frames the animation has in total (default: {DEFAULT_CONFIG['FRAMES']}).\n\n"
    "Frame 0 is always the intact sprite. The last frame is fully exploded (or settled, "
    "depending on gravity). More frames = smoother animation but slower to generate and larger files.\n\n"
    "Recommended: 16 frames for most use cases — smooth enough for pixel art at a reasonable cost.\n\n"
    "Avoid values above 64 unless you specifically need a long, slow animation. "
    "256 frames is the maximum and will be significantly slower to generate and produce large output files.\n\n"
    "This affects both the preview and the exported output."
)

_TIP_ZOOM = (
    "Zooms the preview canvas so you can see small sprites more clearly.\n\n"
    "Sprites too big for the canvas are shrunk to fit at 1× (the readout shows the percentage).\n\n"
    "This only affects the preview display — it has no effect on the exported output."
)


def _hsl_to_hex(h_deg, l, s) -> str:
    """Convert HLS (hue degrees, lightness 0-1, saturation 0-1) to #RRGGBB."""
    r, g, b = colorsys.hls_to_rgb(h_deg / 360.0, l, s)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


class PreviewPanel:
    def __init__(self, parent, config: dict, app):
        self.config = config
        self.app    = app

        self._frames: list      = []
        self._frame_idx: int    = 0
        self._zoom: int         = config.get("zoom_level", 1)
        self._lumi_idx: int     = config.get("preview_lumi", 2)
        self._colr_key          = config.get("preview_colr", None)
        self._satu_key: str     = config.get("preview_satu", "Lo")
        self._checker_on: bool  = bool(config.get("preview_checker", True))
        self._tk_img            = None
        self._checker_img       = None  # cached PhotoImage for checkerboard bg
        self._checker_img_size  = (0, 0)
        self._checker_img_key   = None  # (lumi_idx, colr_key, satu_key) when cached
        self._play_after_id     = None
        self._batch_running     = False

        # Render state: one worker at a time; _render_gen identifies the newest
        # request, so results from superseded jobs are recognised and dropped.
        self._render_job: dict | None = None  # {"gen", "cancel", "path", "p"} while a worker runs
        self._render_gen        = 0
        self._render_pending    = False  # a newer request is waiting for the running job to return
        self._render_after_batch = False # a request arrived during an export
        self._debounce_id       = None
        self._preview_dirty     = False
        self._fit_pending       = True   # zoom-to-fit when the next result for a new sprite lands
        self._live_var          = tk.BooleanVar(value=bool(config.get("live_preview", True)))

        self._sprite_list: list = []
        self._sprite_idx: int   = 0

        self._sprite_dims: dict = {}  # cache: path → (w, h)
        self._error_text = None       # last preview failure, drawn on the canvas

        self._outer = ttk.Frame(parent)
        self._outer.grid(row=0, column=2, sticky="nsew", padx=(4, 4), pady=4)
        self._outer.columnconfigure(0, weight=0)  # swatch strip — fixed width, left side
        self._outer.columnconfigure(1, weight=1)  # canvas + controls
        self._outer.rowconfigure(1, weight=1)  # canvas expands (row 1 now)

        self._build_swatch_strip()         # column=0, rowspan=5
        self._build_sprite_nav_bar(row=0)  # sprite picker above canvas
        self._build_canvas_area(row=1)     # canvas
        self._build_controls_bar(row=2)    # play + scrubber
        self._build_zoom_bar(row=3)        # zoom slider
        self._build_config_bar(row=4)      # update preview + live + frames
        self._build_pause_note(row=5)      # "live preview paused" line, hidden until needed

        from gui.export_bar import ExportBar
        self.export_bar = ExportBar(self._outer, config, app, row=6)

        self._refresh_sprite_list()
        self._redraw_canvas()

    # ------------------------------------------------------------------ #
    #  Canvas area                                                         #
    # ------------------------------------------------------------------ #

    def _build_canvas_area(self, row):
        self._canvas_frame = ttk.Frame(self._outer, style="TFrame")
        self._canvas_frame.grid(row=row, column=1, sticky="nsew", pady=(0, 2))
        self._canvas_frame.columnconfigure(0, weight=1)
        self._canvas_frame.rowconfigure(0, weight=1)

        self._canvas = tk.Canvas(
            self._canvas_frame,
            background=self._resolve_bg_hex(),
            highlightthickness=1,
            highlightbackground=PALETTE["accent_glow"],
        )
        self._canvas.grid(row=0, column=0, sticky="nsew")
        self._canvas.bind("<Configure>", lambda e: self._redraw_canvas())

    def _build_checker_image(self, w: int, h: int) -> ImageTk.PhotoImage:
        """Build a PIL-based checkerboard image for the given canvas size and cache it."""
        shade_a, shade_b = self._checker_shades()

        def _hex_to_rgb(hx):
            hx = hx.lstrip("#")
            return int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)

        ra, ga, ba = _hex_to_rgb(shade_a)
        rb, gb, bb = _hex_to_rgb(shade_b)

        tile = 8
        cols = (w + tile - 1) // tile
        rows = (h + tile - 1) // tile

        # build one row of tile pixels, then stack rows
        row_a = np.empty((tile, cols * tile, 3), dtype=np.uint8)
        row_b = np.empty((tile, cols * tile, 3), dtype=np.uint8)
        for col in range(cols):
            x = col * tile
            row_a[:, x:x + tile] = (ra, ga, ba) if col % 2 == 0 else (rb, gb, bb)
            row_b[:, x:x + tile] = (rb, gb, bb) if col % 2 == 0 else (ra, ga, ba)

        full = np.empty((rows * tile, cols * tile, 3), dtype=np.uint8)
        for row in range(rows):
            full[row * tile:(row + 1) * tile] = row_a if row % 2 == 0 else row_b

        img = Image.fromarray(full[:h, :w], "RGB")
        return ImageTk.PhotoImage(img)

    def _get_checker_image(self, w: int, h: int) -> ImageTk.PhotoImage:
        """Return cached checker PhotoImage, rebuilding only when size or colours change."""
        key = (self._lumi_idx, self._colr_key, self._satu_key)
        if (self._checker_img is None
                or self._checker_img_size != (w, h)
                or self._checker_img_key != key):
            self._checker_img = self._build_checker_image(w, h)
            self._checker_img_size = (w, h)
            self._checker_img_key = key
        return self._checker_img

    def _redraw_canvas(self):
        c = self._canvas
        c.delete("all")

        w = c.winfo_width()
        h = c.winfo_height()
        if w < 2 or h < 2:
            return

        bg_hex = self._resolve_bg_hex()
        c.configure(background=bg_hex)

        # checker pattern — single pre-rendered image, no per-tile canvas items
        if self._checker_on:
            checker = self._get_checker_image(w, h)
            c.create_image(0, 0, anchor="nw", image=checker)

        # sprite image
        if self._frames:
            img = self._frames[self._frame_idx]
            iw, ih = img.size
            # At 1× a sprite bigger than the canvas is shrunk to fit; otherwise the
            # centred image would show only its middle and crop the rest.
            shrink = min((w - 16) / iw, (h - 16) / ih)
            if self._zoom == 1 and shrink < 1:
                size = (max(1, int(iw * shrink)), max(1, int(ih * shrink)))
                scaled = img.resize(size, Image.BOX)
                readout = f"{max(1, int(shrink * 100))}%"
            else:
                scaled = img.resize((iw * self._zoom, ih * self._zoom), Image.NEAREST)
                readout = f"{self._zoom}×"
            if self._zoom_readout.cget("text") != readout:
                self._zoom_readout.configure(text=readout)
            self._tk_img = ImageTk.PhotoImage(scaled)
            cx, cy = w // 2, h // 2
            c.create_image(cx, cy, anchor="center", image=self._tk_img)
        else:
            placeholder_color = "#000000" if _LUMI_LEVELS[self._lumi_idx] >= 0.5 else "#ffffff"
            text = self._error_text or (_PLACEHOLDER if self._sprite_list else _EMPTY_LIST_TEXT)
            c.create_text(
                w // 2, h // 2,
                text=text,
                fill=PALETTE["danger"] if self._error_text else placeholder_color,
                font=FONT_BODY_BOLD,
                anchor="center",
                justify="center",
                width=max(200, w - 40),
            )

    # ------------------------------------------------------------------ #
    #  Color resolution helpers                                            #
    # ------------------------------------------------------------------ #

    def _resolve_bg_hex(self) -> str:
        l = _LUMI_LEVELS[self._lumi_idx]
        h_deg = _COLR_HUES.get(self._colr_key) if self._colr_key else None
        if h_deg is None:
            return _hsl_to_hex(0, l, 0.0)
        s = _SATU_VALUES.get(self._satu_key, 0.25)
        return _hsl_to_hex(h_deg, l, s)

    def _checker_shades(self) -> tuple:
        l = _LUMI_LEVELS[self._lumi_idx]
        if l >= 0.5:
            a = max(0.0, l - 0.08)
            b = max(0.0, l - 0.16)
        else:
            a = min(1.0, l + 0.08)
            b = min(1.0, l + 0.16)
        h_deg = _COLR_HUES.get(self._colr_key) if self._colr_key else None
        if h_deg is None:
            return _hsl_to_hex(0, a, 0.0), _hsl_to_hex(0, b, 0.0)
        s = _SATU_VALUES.get(self._satu_key, 0.40) * 0.5
        return _hsl_to_hex(h_deg, a, s), _hsl_to_hex(h_deg, b, s)

    # ------------------------------------------------------------------ #
    #  Swatch strip                                                        #
    # ------------------------------------------------------------------ #

    def _build_swatch_strip(self):
        strip = ttk.Frame(self._outer)
        strip.grid(row=0, column=0, sticky="ns", padx=(0, 2), pady=0,
                   rowspan=7)

        self._lumi_btns: list = []
        self._colr_btns: dict = {}
        self._satu_btns: dict = {}

        _GROUP_TIPS = {
            "LUMI": "Preview Background Color:\nBrightness — from white (top) to black (bottom)",
            "COLR": "Preview Background Color:\nHue — click to tint; click again to remove tint",
            "SATU": "Preview Background Color:\nSaturation — Low = muted, High = vivid",
            "CHEC": "Preview Background Type:\nToggle transparency checkerboard",
        }

        def _group(label_text):
            g = ttk.Frame(strip)
            g.pack(side="top", pady=(0, 4))
            lbl = tk.Label(g, text=label_text, font=FONT_TINY,
                           bg=PALETTE["bg_base"], fg=PALETTE["text_secondary"])
            lbl.pack()
            _Tooltip(lbl, _GROUP_TIPS[label_text])
            col_frame = ttk.Frame(g)
            col_frame.pack()
            return col_frame

        # ── LUMI ──
        lumi_col = _group("LUMI")
        for i, (lbl, l) in enumerate(zip(_LUMI_LABELS, _LUMI_LEVELS)):
            bg = _hsl_to_hex(0, l, 0.0)
            c = self._make_swatch(lumi_col, bg, lambda idx=i: self._select_lumi(idx))
            c.pack(pady=1)
            _Tooltip(c, f"{lbl} ({int(l*100)}%)")
            self._lumi_btns.append(c)
        self._apply_lumi_btn_styles()

        # ── COLR ──
        colr_col = _group("COLR")
        for key in _COLR_KEYS:
            h_deg = _COLR_HUES[key]
            bg = _hsl_to_hex(0, 0.50, 0.0) if h_deg is None else _hsl_to_hex(h_deg, 0.50, 0.55)
            c = self._make_swatch(colr_col, bg, lambda k=key: self._select_colr(k))
            c.pack(pady=1)
            _Tooltip(c, key)
            self._colr_btns[key] = c
        self._apply_colr_btn_styles()

        # ── SATU ──
        satu_col = _group("SATU")
        for key, s_val in _SATU_VALUES.items():
            h_deg = _COLR_HUES.get(self._colr_key) if self._colr_key else None
            bg = _hsl_to_hex(0, 0.50, 0.0) if h_deg is None else _hsl_to_hex(h_deg, 0.50, s_val)
            c = self._make_swatch(satu_col, bg, lambda k=key: self._select_satu(k))
            c.pack(pady=1)
            _Tooltip(c, "Low saturation (muted)" if key == "Lo" else "High saturation (vivid)")
            self._satu_btns[key] = c
        self._apply_satu_btn_styles()

        # ── CHEC ──
        chec_col = _group("CHEC")
        self._checker_btn = self._make_swatch(chec_col, PALETTE["bg_surface"],
                                              self._toggle_checker)
        self._checker_btn.create_text(
            _SWATCH_SIZE // 2, _SWATCH_SIZE // 2 - 2,
            text="⊞", font=FONT_TINY,
            fill=PALETTE["text_primary"], tags="glyph",
        )
        self._checker_btn.pack(pady=1)
        _Tooltip(self._checker_btn, "Toggle transparency checkerboard")
        self._apply_checker_btn_style()

        self._swatch_strip = strip

    def _make_swatch(self, parent, bg_hex: str, command) -> tk.Canvas:
        c = tk.Canvas(
            parent,
            width=_SWATCH_SIZE, height=_SWATCH_SIZE,
            bd=0, highlightthickness=2,
            highlightbackground=PALETTE["bg_base"],
            cursor="hand2",
        )
        c._fill_hex = bg_hex
        c.create_rectangle(0, 0, _SWATCH_SIZE, _SWATCH_SIZE,
                            fill=bg_hex, outline="black", width=3, tags="fill")
        c.bind("<Button-1>", lambda e: command())
        return c

    def _select_lumi(self, idx: int):
        self._lumi_idx = idx
        self._save("preview_lumi", idx)
        self._apply_lumi_btn_styles()
        self._refresh_satu_btn_colors()
        self._redraw_canvas()

    def _select_colr(self, key: str):
        # toggle off if already selected
        if self._colr_key == key:
            self._colr_key = None
            self._save("preview_colr", None)
        else:
            self._colr_key = key
            self._save("preview_colr", key)
        self._apply_colr_btn_styles()
        self._refresh_satu_btn_colors()
        self._redraw_canvas()

    def _select_satu(self, key: str):
        self._satu_key = key
        self._save("preview_satu", key)
        self._apply_satu_btn_styles()
        self._redraw_canvas()

    def _toggle_checker(self):
        self._checker_on = not self._checker_on
        self._save("preview_checker", self._checker_on)
        self._apply_checker_btn_style()
        self._redraw_canvas()

    def _apply_lumi_btn_styles(self):
        for i, c in enumerate(self._lumi_btns):
            c.configure(highlightbackground=(
                PALETTE["accent_strong"] if i == self._lumi_idx else PALETTE["bg_base"]
            ))

    def _apply_colr_btn_styles(self):
        for key, c in self._colr_btns.items():
            c.configure(highlightbackground=(
                PALETTE["accent_strong"] if key == self._colr_key else PALETTE["bg_base"]
            ))

    def _apply_satu_btn_styles(self):
        for key, c in self._satu_btns.items():
            c.configure(highlightbackground=(
                PALETTE["accent_strong"] if key == self._satu_key else PALETTE["bg_base"]
            ))

    def _refresh_satu_btn_colors(self):
        l = _LUMI_LEVELS[self._lumi_idx]
        h_deg = _COLR_HUES.get(self._colr_key) if self._colr_key else None
        for key, c in self._satu_btns.items():
            s_val = _SATU_VALUES[key]
            bg = _hsl_to_hex(0, l, 0.0) if h_deg is None else _hsl_to_hex(h_deg, l, s_val)
            c.itemconfig("fill", fill=bg)
            c._fill_hex = bg

    def _apply_checker_btn_style(self):
        if self._checker_on:
            self._checker_btn.configure(highlightbackground=PALETTE["accent_strong"])
            self._checker_btn.itemconfig("fill", fill=PALETTE["accent_glow"])
        else:
            self._checker_btn.configure(highlightbackground=PALETTE["bg_base"])
            self._checker_btn.itemconfig("fill", fill=PALETTE["bg_surface"])

    # ------------------------------------------------------------------ #
    #  Controls bar — Play Loop + scrubber                                #
    # ------------------------------------------------------------------ #

    def _build_controls_bar(self, row):
        bar = ttk.Frame(self._outer)
        bar.grid(row=row, column=1, sticky="ew", pady=(0, 2))
        bar.columnconfigure(3, weight=1)

        self._play_btn = ttk.Button(bar, text="Play Loop", command=self._toggle_play)
        self._play_btn.grid(row=0, column=0, padx=(0, 8))

        ttk.Button(bar, text="◀", width=2,
                   command=self._step_back).grid(row=0, column=1, padx=(0, 2))

        self._scrubber = ttk.Scale(bar, from_=0, to=0, orient="horizontal")
        self._scrubber.grid(row=0, column=3, sticky="ew", padx=2)
        self._scrubber.bind("<ButtonRelease-1>", self._on_scrub)

        ttk.Button(bar, text="▶", width=2,
                   command=self._step_forward).grid(row=0, column=4, padx=(2, 6))

        self._frame_label = ttk.Label(bar, text="Frame 0 / 0",
                                      font=FONT_SMALL, bootstyle="secondary")
        self._frame_label.grid(row=0, column=5, padx=(0, 4))

    def _on_scrub(self, event=None):
        self._stop_playback()
        self._frame_idx = int(round(self._scrubber.get()))
        self._update_frame_label()
        self._redraw_canvas()

    def _step_back(self):
        self._stop_playback()
        if self._frames:
            self._frame_idx = max(0, self._frame_idx - 1)
            self._scrubber.set(self._frame_idx)
            self._update_frame_label()
            self._redraw_canvas()

    def _step_forward(self):
        self._stop_playback()
        if self._frames:
            self._frame_idx = min(len(self._frames) - 1, self._frame_idx + 1)
            self._scrubber.set(self._frame_idx)
            self._update_frame_label()
            self._redraw_canvas()

    def _update_frame_label(self):
        total = len(self._frames)
        n = self._frame_idx if total else 0
        self._frame_label.configure(text=f"Frame {n} / {max(0, total - 1)}")

    # ------------------------------------------------------------------ #
    #  Zoom bar                                                            #
    # ------------------------------------------------------------------ #

    def _build_zoom_bar(self, row):
        bar = ttk.Frame(self._outer)
        bar.grid(row=row, column=1, sticky="ew", pady=(0, 2))
        bar.columnconfigure(1, weight=1)

        zoom_lbl = ttk.Label(bar, text="Zoom:", font=FONT_BODY,
                             background=PALETTE["bg_base"])
        zoom_lbl.grid(row=0, column=0, padx=(0, 4))
        _Tooltip(zoom_lbl, _TIP_ZOOM)

        self._zoom_var = tk.IntVar(value=self._zoom)
        self._zoom_slider = ttk.Scale(
            bar, from_=1, to=20, orient="horizontal",
            variable=self._zoom_var,
            command=self._on_zoom_slide,
        )
        self._zoom_slider.grid(row=0, column=1, sticky="ew", padx=(0, 6))
        _Tooltip(self._zoom_slider, _TIP_ZOOM)

        self._zoom_readout = ttk.Label(
            bar, text=f"{self._zoom}×",
            font=FONT_SMALL, bootstyle="secondary", width=5, anchor="w",
        )
        self._zoom_readout.grid(row=0, column=2, padx=(0, 4))

    def _toggle_play(self):
        if self._play_after_id is not None:
            self._stop_playback()
        else:
            self._start_playback()

    def _start_playback(self):
        if not self._frames:
            return
        self._play_btn.configure(text="■  Stop")
        self._schedule_next_frame()

    def _stop_playback(self):
        if self._play_after_id is not None:
            self.app.root.after_cancel(self._play_after_id)
            self._play_after_id = None
        self._play_btn.configure(text="Play Loop")

    def _schedule_next_frame(self):
        # Same timing as the exported GIF: first/last frames held, the rest at MS_PER_FRAME.
        from core.output import frame_durations
        c = self.config
        durations = frame_durations(len(self._frames),
                                    c.get("MS_PER_FRAME", DEFAULT_CONFIG["MS_PER_FRAME"]),
                                    c.get("HOLD_FIRST_MS", DEFAULT_CONFIG["HOLD_FIRST_MS"]),
                                    c.get("HOLD_LAST_MS", DEFAULT_CONFIG["HOLD_LAST_MS"]))
        delay_ms = durations[min(self._frame_idx, len(durations) - 1)]
        self._play_after_id = self.app.root.after(delay_ms, self._advance_frame)

    def _advance_frame(self):
        if not self._frames:
            self._stop_playback()
            return
        self._frame_idx = (self._frame_idx + 1) % len(self._frames)
        self._scrubber.set(self._frame_idx)
        self._update_frame_label()
        self._redraw_canvas()
        if self._play_after_id is not None:
            self._schedule_next_frame()

    def _on_zoom_slide(self, value):
        self._set_zoom(round(float(value)))

    def _zoom_to_fit(self) -> bool:
        """Largest whole zoom that shows the current frames entirely; False if the
        canvas isn't laid out yet."""
        c = self._canvas
        cw, ch = c.winfo_width(), c.winfo_height()
        if cw < 2 or ch < 2 or not self._frames:
            return False
        iw, ih = self._frames[0].size
        self._set_zoom(int(min((cw - 16) / iw, (ch - 16) / ih)))
        return True

    def _set_zoom(self, value: int):
        v = max(1, min(20, value))
        self._zoom = v
        self._zoom_var.set(v)
        self._zoom_readout.configure(text=f"{v}×")
        self._save("zoom_level", v)
        self._redraw_canvas()

    # ------------------------------------------------------------------ #
    #  Sprite navigation bar                                               #
    # ------------------------------------------------------------------ #

    def _build_sprite_nav_bar(self, row):
        bar = ttk.Frame(self._outer)
        bar.grid(row=row, column=1, sticky="ew", pady=(0, 2))
        bar.columnconfigure(1, weight=1)

        ttk.Button(bar, text="◀ Prev", width=7,
                   command=self._prev_sprite).grid(row=0, column=0, padx=(0, 4))

        self._sprite_label = ttk.Label(bar, text="(no sprites)", font=FONT_BODY_BOLD,
                                       anchor="center")
        self._sprite_label.grid(row=0, column=1, sticky="ew")

        ttk.Button(bar, text="Next ▶", width=7,
                   command=self._next_sprite).grid(row=0, column=2, padx=(4, 0))

    def _prev_sprite(self):
        if self._sprite_list:
            self.show_sprite((self._sprite_idx - 1) % len(self._sprite_list))

    def _next_sprite(self):
        if self._sprite_list:
            self.show_sprite((self._sprite_idx + 1) % len(self._sprite_list))

    def show_sprite(self, idx: int):
        """Switch the preview to sprite idx of the list and render it."""
        if not self._sprite_list:
            return
        self._sprite_idx = max(0, min(idx, len(self._sprite_list) - 1))
        self._on_sprite_changed()
        self.trigger_auto_preview()

    def current_index(self) -> int:
        return self._sprite_idx

    def _on_sprite_changed(self):
        self._invalidate_running_render()
        self._fit_pending = True
        self._stop_playback()
        self._error_text = None
        self._frames = []
        self._frame_idx = 0
        self._scrubber.configure(to=0)
        self._scrubber.set(0)
        self._update_frame_label()
        self._update_sprite_label()
        self._redraw_canvas()
        if hasattr(self.app, "sprites_tab"):
            self.app.sprites_tab.highlight(self._sprite_idx)

    def _update_sprite_label(self):
        if self._sprite_list:
            path = self._sprite_list[self._sprite_idx]
            name = os.path.splitext(os.path.basename(path))[0]
            total = len(self._sprite_list)
            if path not in self._sprite_dims:
                try:
                    with Image.open(path) as img:
                        self._sprite_dims[path] = img.size
                except Exception:
                    self._sprite_dims[path] = (0, 0)
            w, h = self._sprite_dims[path]
            dims = f"  {w}×{h}" if w and h else ""
            self._sprite_label.configure(text=f"{name}  ({self._sprite_idx + 1}/{total}){dims}")
        else:
            self._sprite_label.configure(text="(no sprites)")

    def _refresh_sprite_list(self):
        self._sprite_list = list(self.config.get("sprite_files", []))
        self._sprite_idx = min(self._sprite_idx, max(0, len(self._sprite_list) - 1))
        self._update_sprite_label()

    # ------------------------------------------------------------------ #
    #  Config bar — Update Preview, Live, Frames                          #
    # ------------------------------------------------------------------ #

    def _build_config_bar(self, row):
        bar = ttk.Frame(self._outer)
        bar.grid(row=row, column=1, sticky="ew", pady=(2, 4))

        # Update Preview button — tk.Frame as 2px border wrapper; tk.Button inside
        self._update_btn_border = tk.Frame(bar, bd=0, padx=4, pady=4)
        self._update_btn_border.pack(side="left")
        self._update_btn = tk.Button(
            self._update_btn_border, text="Update Preview",
            font=FONT_BODY_BOLD,
            fg="#FFFFFF", activeforeground="#FFFFFF",
            relief="flat", bd=0,
            highlightthickness=0,
            padx=14, pady=6,
            cursor="hand2",
            width=16,  # fixed char-width so button stays same size across all states
            command=self._on_update_preview,
        )
        self._update_btn.pack()
        _Tooltip(self._update_btn, _TIP_UPDATE_BTN)
        self._apply_btn_state("ok")

        live_cb = ttk.Checkbutton(bar, text="Live", variable=self._live_var,
                                  bootstyle="round-toggle", command=self._on_live_toggle)
        live_cb.pack(side="left", padx=(8, 4))
        _Tooltip(live_cb, _TIP_LIVE)

        # Frames spinbox
        frames_lbl = ttk.Label(bar, text="Frames:", font=FONT_BODY,
                               background=PALETTE["bg_base"])
        frames_lbl.pack(side="left", padx=(8, 4))
        _Tooltip(frames_lbl, _TIP_FRAMES)

        self._frames_var = tk.IntVar(value=self.config.get("FRAMES", DEFAULT_CONFIG["FRAMES"]))
        frames_sb = ttk.Spinbox(bar, from_=2, to=256, textvariable=self._frames_var, width=4, font=FONT_SPINBOX)
        frames_sb.pack(side="left", padx=(0, 8))
        _Tooltip(frames_sb, _TIP_FRAMES)

        def _save_frames(e=None):
            current = self.config.get("FRAMES", DEFAULT_CONFIG["FRAMES"])
            try:
                v = int(frames_sb.get())
            except (ValueError, tk.TclError):
                v = current
            v = max(2, min(256, v))
            self._frames_var.set(v)
            if v == current:
                return  # focus-out / Return without an edit: nothing to re-render
            self._save("FRAMES", v)
            if hasattr(self.app, "physics_tab"):
                self.app.physics_tab.refresh(self.config)

        frames_sb.bind("<<Increment>>", _save_frames)
        frames_sb.bind("<<Decrement>>", _save_frames)
        frames_sb.bind("<FocusOut>",    _save_frames)
        frames_sb.bind("<Return>",      _save_frames)
        self._save_frames = _save_frames

    def _build_pause_note(self, row):
        """One line shown when live mode paused itself after a slow render."""
        self._pause_note = ttk.Frame(self._outer)
        self._pause_note.grid(row=row, column=1, sticky="ew", pady=(0, 2))
        self._pause_note_lbl = ttk.Label(self._pause_note, text="", font=FONT_SMALL,
                                         bootstyle="warning", background=PALETTE["bg_base"])
        self._pause_note_lbl.pack(side="left")
        resume = ttk.Label(self._pause_note, text="Turn live preview back on",
                           font=FONT_SMALL, foreground=PALETTE["accent_soft"],
                           background=PALETTE["bg_base"], cursor="hand2")
        resume.pack(side="left", padx=(6, 0))
        resume.bind("<Button-1>", lambda e: self._resume_live())
        self._pause_note.grid_remove()

    def _apply_btn_state(self, state: str):
        if state == "ok":
            self._update_btn_border.configure(bg=_BTN_OK_BORDER)
            self._update_btn.configure(
                bg=_BTN_OK_BG, activebackground=_BTN_OK_BG,
                text="Preview Ready", state="normal", cursor="hand2",
            )
        elif state == "dirty":
            self._update_btn_border.configure(bg=_BTN_DIRTY_BORDER)
            self._update_btn.configure(
                bg=_BTN_DIRTY_BG, activebackground=_BTN_DIRTY_BG,
                text="Update Preview", state="normal", cursor="hand2",
            )
        elif state == "rendering":
            self._update_btn_border.configure(bg=_BTN_BUSY_BORDER)
            self._update_btn.configure(
                bg=_BTN_BUSY_BG, activebackground=_BTN_BUSY_BG,
                text="Rendering…", state="disabled", cursor="arrow",
            )

    def _refresh_btn(self):
        """Button state from the render state: busy while an export runs, a render is
        in flight or a live render is about to start; otherwise ok / dirty."""
        if self._batch_running or self._render_job is not None or self._debounce_id is not None:
            self._apply_btn_state("rendering")
        else:
            self._apply_btn_state("dirty" if self._preview_dirty else "ok")

    # ------------------------------------------------------------------ #
    #  Live mode                                                           #
    # ------------------------------------------------------------------ #

    def _on_live_toggle(self):
        live = self._live_var.get()
        self._save("live_preview", live)
        self._pause_note.grid_remove()
        if live and self._preview_dirty:
            self._request_render()
        else:
            self._refresh_btn()

    def _resume_live(self):
        self._live_var.set(True)
        self._on_live_toggle()

    def _pause_live(self):
        """Slow render: switch live mode off for this session (the saved preference is
        kept, so the next start is live again) and say why."""
        self._live_var.set(False)
        self._cancel_debounce()
        self._pause_note_lbl.configure(
            text=f"Live preview paused — this render took over {_SLOW_RENDER_MS / 1000:g} s. "
                 "Use Update Preview after changes, or")
        self._pause_note.grid()
        log.info("Live preview paused: render of %s exceeded %d ms",
                 os.path.basename(self._render_job["path"]) if self._render_job else "?",
                 _SLOW_RENDER_MS)

    def _cancel_debounce(self):
        if self._debounce_id is not None:
            self.app.root.after_cancel(self._debounce_id)
            self._debounce_id = None

    def _invalidate_running_render(self):
        """Make the job in flight stale and ask it to stop early."""
        if self._render_job is not None:
            self._render_job["cancel"].set()
            self._render_gen += 1

    # ------------------------------------------------------------------ #
    #  Rendering — one worker at a time, the newest request wins          #
    # ------------------------------------------------------------------ #

    def _on_update_preview(self):
        """Update Preview button (and the randomizer): render now."""
        self._request_render()

    def _request_render(self):
        """Render the shown sprite with the current settings, superseding any render
        in flight. The running job is cancelled; the new one starts as soon as that
        worker returns, so there is never more than one."""
        self._cancel_debounce()
        if not self._sprite_list:
            self._refresh_btn()
            return
        if self._batch_running:
            self._render_after_batch = True
            return
        if self._render_job is not None:
            self._invalidate_running_render()
            self._render_pending = True
            return
        self._render_gen += 1
        self._start_render()

    def _start_render(self):
        self._render_pending = False
        self._save_frames()        # pick up a typed-but-uncommitted frame count
        self._cancel_debounce()    # ...without that edit queueing a second render
        self.config["CHUNKS"] = max(2, min(1000, self.config.get("CHUNKS", 16)))
        self.config["FRAMES"] = max(2, min(256, self.config.get("FRAMES", DEFAULT_CONFIG["FRAMES"])))
        self._preview_dirty = False  # this render reflects every change so far
        # Params are built here, on the Tk thread, so the worker never reads a
        # config dict that the GUI is changing underneath it.
        job = {"gen": self._render_gen, "cancel": threading.Event(),
               "path": self._sprite_list[self._sprite_idx], "p": self.build_p()}
        self._render_job = job
        self._refresh_btn()
        self.app.root.after(_SLOW_RENDER_MS, lambda: self._check_slow_render(job))
        threading.Thread(target=self._run_preview, args=(job,), daemon=True).start()

    def _check_slow_render(self, job):
        if (self._render_job is job and not job["cancel"].is_set()
                and self._live_var.get()):
            self._pause_live()

    def _run_preview(self, job):
        from core.pipeline import run_sprite, RenderCancelled
        frames, error = None, None
        img_path = job["path"]
        try:
            with Image.open(img_path) as img:
                img.load()
                frames = run_sprite(img, job["p"], cancel=job["cancel"].is_set).frames
            if not frames:
                error = "This image has no visible (non-transparent) pixels."
        except RenderCancelled:
            frames = None
        except Exception as exc:
            log.exception("Preview failed for %s", img_path)
            frames = []
            error = f"{short_reason(exc)}\n\n(details in sprite_gibber.log)"
        if error:
            error = f"Preview failed — {os.path.basename(img_path)}\n\n{error}"
        self.app.root.after(0, lambda: self._on_preview_done(job, frames, error))

    def _on_preview_done(self, job, frames, error=None):
        self._render_job = None
        if self._render_pending:
            # A newer request was waiting for this worker to return.
            self._start_render()
            return
        if job["gen"] != self._render_gen or frames is None:
            # Superseded or cancelled (sprite removed, export started): drop it.
            self._refresh_btn()
            return

        self._refresh_btn()
        if hasattr(self.app, "presets_tab"):
            self.app.presets_tab.notify_preview_updated()

        # On failure clear the old frames, so a stale animation is never
        # mistaken for the result of the current settings.
        self._error_text = error
        self._stop_playback()
        self._frames    = frames if not error else []
        self._frame_idx = 0
        self._scrubber.configure(to=max(0, len(self._frames) - 1))
        self._scrubber.set(0)
        if self._frames and self._fit_pending and self._zoom_to_fit():
            self._fit_pending = False
        self._update_frame_label()
        self._redraw_canvas()
        self._start_playback()

    # ------------------------------------------------------------------ #
    #  Cross-panel interface                                               #
    # ------------------------------------------------------------------ #

    def set_dirty(self, dirty: bool):
        """A setting changed (dirty=True). In live mode, re-render once the changes
        stop for _LIVE_DEBOUNCE_MS; the render in flight is already stale, so stop it."""
        self._preview_dirty = dirty
        if (dirty and self._live_var.get() and self._sprite_list
                and not self._batch_running):
            self._invalidate_running_render()
            self._cancel_debounce()
            self._debounce_id = self.app.root.after(_LIVE_DEBOUNCE_MS, self._request_render)
        self._refresh_btn()
        if hasattr(self, "app") and hasattr(self.app, "presets_tab"):
            self.app.presets_tab.notify_dirty(dirty)

    def set_batch_running(self, running: bool):
        """An export started/finished. The preview is off during export (the export
        worker gets the CPU); whatever was requested meanwhile renders afterwards."""
        self._batch_running = running
        if running:
            self._cancel_debounce()
            if self._render_job is not None or self._render_pending:
                self._invalidate_running_render()
                self._render_pending = False
                self._render_after_batch = True
            if self._preview_dirty and self._live_var.get():
                self._render_after_batch = True
        elif self._render_after_batch or (self._preview_dirty and self._live_var.get()):
            self._render_after_batch = False
            self.app.root.after(0, self._request_render)
        self._refresh_btn()

    def trigger_auto_preview(self):
        """Render now (new sprite shown, app start) — regardless of live mode."""
        self._request_render()

    def notify_sprite_list_changed(self, show=None):
        """The sprite list was edited. Show `show` (a path) if given; otherwise keep the
        current sprite if it's still listed. Re-renders only when the shown sprite changes."""
        old = self._sprite_list[self._sprite_idx] if self._sprite_list else None
        self._sprite_list = list(self.config.get("sprite_files", []))
        target = show if show is not None else old
        if target in self._sprite_list:
            self._sprite_idx = self._sprite_list.index(target)
        else:
            self._sprite_idx = min(self._sprite_idx, max(0, len(self._sprite_list) - 1))
        new = self._sprite_list[self._sprite_idx] if self._sprite_list else None
        if new != old or not self._sprite_list:
            self._on_sprite_changed()
            if new is not None:
                self.app.root.after(50, self.trigger_auto_preview)
        else:
            self._update_sprite_label()
            if hasattr(self.app, "sprites_tab"):
                self.app.sprites_tab.highlight(self._sprite_idx)
        self.export_bar.update_sprite_count()

    def build_p(self):
        """Engine params from the current config (shared by preview and export)."""
        from core.pipeline import build_params
        bg_hex = self._resolve_bg_hex() if self.config.get("gif_use_preview_bg") else None
        return build_params(self.config, gif_bg_hex=bg_hex)

    def refresh(self, config: dict):
        self.config = config
        self._frames_var.set(config.get("FRAMES", DEFAULT_CONFIG["FRAMES"]))
        # _live_var is not reloaded here: a preset load must not undo a slow-render pause.
        new_zoom = config.get("zoom_level", 1)
        if new_zoom != self._zoom:
            self._zoom = new_zoom
            self._zoom_var.set(new_zoom)
            self._zoom_readout.configure(text=f"{new_zoom}×")
        self._lumi_idx = config.get("preview_lumi", 2)
        self._colr_key = config.get("preview_colr", None)
        self._satu_key = config.get("preview_satu", "Lo")
        self._apply_lumi_btn_styles()
        self._apply_colr_btn_styles()
        self._refresh_satu_btn_colors()
        self._apply_satu_btn_styles()
        new_checker = bool(config.get("preview_checker", True))
        if new_checker != self._checker_on:
            self._checker_on = new_checker
            self._apply_checker_btn_style()
        self._refresh_sprite_list()
        self.export_bar.refresh(config)
        self._redraw_canvas()

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _save(self, key: str, value):
        self.config[key] = value
        self.app.save_config()
        if key == "FRAMES":
            self.app.mark_preview_dirty()
