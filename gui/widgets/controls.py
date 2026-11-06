"""Shared setting controls for the settings tabs.

- choice_combo: readonly combobox that shows friendly names for snake_case values
  while its StringVar keeps the config value (config/presets never see the names).
- slider_row: label + slider + typed value entry. The slider covers the useful
  range; the entry accepts the full allowed range. Double-click the slider to
  reset it to its default.
- MoreOptions: collapsible "More options" block for advanced controls. It opens
  by itself whenever one of its keys is set away from its default, so nothing a
  preset uses is ever hidden.
"""
import tkinter as tk

import ttkbootstrap as ttk

from gui.theme import PALETTE, FONT_BODY, FONT_SMALL
from utils.config import DEFAULT_CONFIG

# Names that the generic snake_case → "Sentence case" rule gets wrong or unclear.
_DISPLAY_OVERRIDES = {
    "x_split":         "X split",
    "halves-h":        "Halves (top / bottom)",
    "halves-v":        "Halves (left / right)",
    "crop_center":     "Crop to fill",
    "gravity_aligned": "Gravity-aligned",
    "per_chunk":       "Per chunk",
    "unidirectional":  "Border only",
    "bidirectional":   "Border + center",
}


def display_name(value) -> str:
    """Friendly label for a config choice value ("hollow_circle" → "Hollow circle")."""
    if value is None:
        return "None"
    value = str(value)
    if value in _DISPLAY_OVERRIDES:
        return _DISPLAY_OVERRIDES[value]
    text = value.replace("_", " ").replace("-", " ")
    return text[:1].upper() + text[1:]


class ReadonlyCombo(ttk.Combobox):
    """Combobox that stays readonly: the tabs re-enable controls with
    state="normal", which would otherwise make the friendly names typeable."""

    def configure(self, cnf=None, **kw):
        if kw.get("state") == "normal":
            kw["state"] = "readonly"
        return super().configure(cnf, **kw)

    config = configure


def choice_combo(parent, var: tk.StringVar, values, on_select, width=16):
    """Readonly combobox over `values` (config values) showing display_name()s.

    `var` holds the config value: set it to a config value and the box follows;
    on a pick, `var` is set to the picked config value and on_select(event) runs.
    """
    shown = tk.StringVar(value=display_name(var.get()))
    back = {display_name(v): v for v in values}
    combo = ReadonlyCombo(parent, textvariable=shown, state="readonly", font=FONT_BODY,
                         values=[display_name(v) for v in values], width=width)
    var.trace_add("write", lambda *_: shown.set(display_name(var.get())))

    def _picked(event):
        var.set(back.get(shown.get(), var.get()))
        on_select(event)

    combo.bind("<<ComboboxSelected>>", _picked)
    return combo


def slider_row(parent, row, label, var, from_, to, commit, *, dp=0, limits=None,
               default=None, scale=1, suffix="", tooltip=None, tooltip_cls=None,
               label_bg=None):
    """One "Label [slider] [value]" row; returns (frame, slider, entry, label).

    commit()   saves var's current value (called on slider release, typed entry,
               and double-click reset).
    dp         decimals shown/kept (0 = integer).
    limits     (lo, hi) accepted when typed; defaults to the slider range.
    default    value a double-click on the slider resets to (None = no reset).
    scale      display multiplier (100 shows a 0–1 fraction as a percentage).
    """
    lo, hi = limits if limits is not None else (from_, to)

    rf = ttk.Frame(parent)
    rf.grid(row=row, column=0, sticky="ew", pady=2)
    rf.columnconfigure(1, weight=1)

    lbl = ttk.Label(rf, text=label, font=FONT_BODY,
                    background=label_bg or PALETTE["bg_base"])
    lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))

    shown_dp = max(dp - 2, 0) if scale == 100 else dp

    entry = ttk.Entry(rf, width=6, font=FONT_SMALL, justify="right")
    entry.grid(row=0, column=2, sticky="e")

    def _current():
        try:
            v = float(var.get())
        except (tk.TclError, ValueError):
            v = float(lo)
        return int(round(v)) if dp == 0 else round(v, dp)

    def _show(*_):
        if entry.focus_get() is entry:
            return  # don't overwrite what the user is typing
        state = str(entry.cget("state"))
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, f"{_current() * scale:.{shown_dp}f}{suffix}")
        entry.configure(state=state)

    def _typed(leave):
        raw = entry.get().replace(suffix.strip(), "").strip() if suffix else entry.get().strip()
        try:
            v = max(lo, min(hi, float(raw) / scale))
        except ValueError:
            v = None
        if v is not None:
            v = int(round(v)) if dp == 0 else round(v, dp)
            if v != _current():
                var.set(v)
                commit()
        entry.selection_clear()
        if leave:
            entry.master.focus_set()   # Return: leave the box so _show can redraw it
        _show()

    var.trace_add("write", _show)
    entry.bind("<Return>", lambda e: _typed(True))
    entry.bind("<FocusOut>", lambda e: _typed(False))
    _show()

    def _slid(v):
        # Keep integer sliders on whole numbers while dragging.
        if dp == 0:
            var.set(int(round(float(v))))

    slider = ttk.Scale(rf, variable=var, from_=from_, to=to, orient="horizontal",
                       command=_slid)
    slider.grid(row=0, column=1, sticky="ew", padx=4)
    slider.bind("<ButtonRelease-1>", lambda e: commit())

    if default is not None:
        def _reset(_e):
            if str(slider.cget("state")) == "disabled":
                return "break"
            var.set(default)
            commit()
            return "break"   # stop the Scale's own click handling (no jump)
        slider.bind("<Double-Button-1>", _reset)

    if tooltip and tooltip_cls is not None:
        tip = tooltip + ("\n\nDouble-click the slider to reset it." if default is not None else "")
        for w in (lbl, slider, entry):
            tooltip_cls(w, tip)

    return rf, slider, entry, lbl


class MoreOptions(ttk.Frame):
    """Collapsible block of advanced controls; put them in `.body`.

    keys: config keys shown inside. sync(config) shows the block when the user
    opened it or any of its keys differs from DEFAULT_CONFIG (with how many are in
    use), and collapses it again when neither is true.
    """

    def __init__(self, parent, keys, text="More options"):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self._keys = list(keys)
        self._text = text
        self._open = False
        self._user_open = False
        self._header = ttk.Label(self, font=FONT_SMALL, cursor="hand2",
                                 foreground=PALETTE["accent_strong"])
        self._header.grid(row=0, column=0, sticky="w", pady=(4, 2))
        self._header.bind("<Button-1>", lambda e: self._on_click())
        self.body = ttk.Frame(self)
        self.body.columnconfigure(0, weight=1)
        self._in_use = 0
        self._render_header()

    def _render_header(self):
        arrow = "▾" if self._open else "▸"
        extra = f"  ({self._in_use} in use)" if self._in_use else ""
        self._header.configure(text=f"{arrow} {self._text}{extra}")

    def is_open(self) -> bool:
        return self._open

    def _on_click(self):
        self._user_open = not self._open
        self._show(self._user_open)

    def _show(self, open_):
        self._open = bool(open_)
        if self._open:
            self.body.grid(row=1, column=0, sticky="ew")
        else:
            self.body.grid_remove()
        self._render_header()

    def sync(self, config: dict):
        in_use = sum(1 for k in self._keys
                     if k in DEFAULT_CONFIG and config.get(k, DEFAULT_CONFIG[k]) != DEFAULT_CONFIG[k])
        changed = in_use != self._in_use
        self._in_use = in_use
        if changed:
            # Re-decide only when what's in use changed, so a block the user
            # collapsed doesn't spring open on every unrelated refresh.
            self._show(self._user_open or in_use > 0)
        else:
            self._render_header()
