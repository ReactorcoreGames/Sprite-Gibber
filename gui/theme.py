import tkinter as tk

_TOOLTIP_FONT    = ("Segoe UI", 10)
_TOOLTIP_BG      = "#FFFFDD"
_TOOLTIP_WRAP    = 480


class Tooltip:
    """Shared hover tooltip used across all GUI tabs. Pass a string or a callable that returns one."""

    def __init__(self, widget, text):
        self._win  = None
        self._text = text
        widget.bind("<Enter>",       self._show)
        widget.bind("<Motion>",      self._move)
        widget.bind("<Leave>",       lambda e: self._hide())
        widget.bind("<ButtonPress>", lambda e: self._hide())

    def _place(self, tw, mx, my):
        tw.update_idletasks()
        tw_w = tw.winfo_width()
        tw_h = tw.winfo_height()
        scr_w = tw.winfo_screenwidth()
        scr_h = tw.winfo_screenheight()
        x = mx + 12
        if x + tw_w + 60 > scr_w:
            x = mx - tw_w - 12
        y_below = my + 16
        y_above = my - tw_h - 8
        y = y_above if y_below + tw_h + 60 > scr_h else y_below
        tw.geometry(f"+{x}+{y}")

    def _show(self, event):
        self._hide()
        text = self._text() if callable(self._text) else self._text
        if not text:
            return
        self._win = tw = tk.Toplevel()
        tw.overrideredirect(True)
        tw.attributes("-topmost", True)
        tk.Label(
            tw, text=text, justify="left",
            background=_TOOLTIP_BG, relief="solid", borderwidth=1,
            font=_TOOLTIP_FONT, padx=6, pady=3, wraplength=_TOOLTIP_WRAP,
        ).pack()
        self._place(tw, event.x_root, event.y_root)

    def _move(self, event):
        if self._win:
            self._place(self._win, event.x_root, event.y_root)

    def _hide(self):
        if self._win:
            self._win.destroy()
            self._win = None


PALETTE = {
    # Backgrounds — warm parchment tones
    "bg_base":        "#F2EDE8",   # warm putty — app background, panel base
    "bg_surface":     "#EAE2DA",   # slightly darker putty — sections, LabelFrames, headers
    "bg_input":       "#FBF8F5",   # near-white — entry fields, dropdowns

    # Accents — terracotta red
    "accent_strong":  "#8B3A1E",   # deep terracotta — primary buttons, slider thumbs, active tabs
    "accent_mid":     "#C05030",   # mid terracotta — hover states
    "accent_soft":    "#8B3A1E",   # same as accent_strong (no lighter link color needed on light bg)
    "accent_glow":    "#C8B8A8",   # warm taupe — borders, separators

    # Text
    "text_primary":   "#1C1714",   # near-black with warm tint — all body text, labels
    "text_secondary": "#6B5E52",   # medium warm brown — captions, value badges, hints

    # Semantic
    "success":        "#2E7A3E",   # forest green — Generate All button
    "danger":         "#B83030",   # brick red — Stop / Delete buttons
    "warning":        "#A06820",   # dark amber
    "info":           "#2A5090",   # slate blue
}

FONT_FAMILY    = "Segoe UI"
FONT_TITLE     = (FONT_FAMILY, 26, "bold")   # app title in header
FONT_HEADING   = (FONT_FAMILY, 14, "bold")   # section titles, LabelFrame labels
FONT_BODY      = (FONT_FAMILY, 13)           # labels, buttons, sliders
FONT_BODY_BOLD = (FONT_FAMILY, 13, "bold")   # emphasis labels, primary action buttons
FONT_SMALL     = (FONT_FAMILY, 12)           # value badges, captions, tab labels
FONT_TINY      = (FONT_FAMILY, 11)           # footer attribution only
FONT_ENTRY     = (FONT_FAMILY, 13)           # entry fields, dropdowns
FONT_SPINBOX   = (FONT_FAMILY, 14)           # spinbox number value (+1pt over body)
FONT_MONO      = ("Consolas", 12)            # seed field, hex values
FONT_DROPDOWN  = (FONT_FAMILY, 13)           # combobox dropdown list entries (matches entry size)


def _inject_gibber_theme():
    from ttkbootstrap.themes.standard import STANDARD_THEMES
    p = PALETTE
    STANDARD_THEMES["gibber"] = {
        "type": "light",
        "colors": {
            "primary":   p["accent_strong"],
            "secondary": p["bg_surface"],
            "success":   p["success"],
            "info":      p["info"],
            "warning":   p["warning"],
            "danger":    p["danger"],
            "light":     p["bg_input"],
            "dark":      p["text_primary"],
            "bg":        p["bg_base"],
            "fg":        p["text_primary"],
            "selectbg":  p["accent_strong"],
            "selectfg":  p["bg_input"],
            "border":    p["accent_glow"],
            "inputfg":   p["text_primary"],
            "inputbg":   p["bg_input"],
            "active":    p["accent_mid"],
        },
    }


def apply_theme(style, root=None):
    import tkinter.ttk as _stdlib_ttk
    p = PALETTE

    if root is not None:
        root.configure(bg=p["bg_base"])
        # Combobox dropdown list is a plain Tk Listbox — style it via the option DB.
        root.option_add("*TCombobox*Listbox.font", FONT_DROPDOWN)
        root.option_add("*TCombobox*Listbox.background", p["bg_input"])
        root.option_add("*TCombobox*Listbox.foreground", p["text_primary"])
        root.option_add("*TCombobox*Listbox.selectBackground", p["accent_strong"])
        root.option_add("*TCombobox*Listbox.selectForeground", p["bg_input"])

    style.configure(".",
                    background=p["bg_base"],
                    foreground=p["text_primary"],
                    bordercolor=p["accent_glow"],
                    darkcolor=p["bg_base"],
                    lightcolor=p["bg_surface"],
                    troughcolor=p["bg_base"],
                    selectbackground=p["accent_strong"],
                    selectforeground=p["bg_input"],
                    fieldbackground=p["bg_input"],
                    font=FONT_BODY,
                    borderwidth=1)

    # Apply LabelFrame styles to both ttkbootstrap and stdlib ttk engines so that
    # _tk_ttk.LabelFrame widgets also pick up the surface colours.
    for s in (style, _stdlib_ttk.Style()):
        s.configure("TLabelframe",       background=p["bg_surface"], bordercolor=p["accent_glow"])
        s.configure("TLabelframe.Label", background=p["bg_surface"], foreground=p["accent_soft"],
                    font=FONT_SMALL)

    style.configure("TFrame",             background=p["bg_base"])
    style.configure("Surface.TFrame",     background=p["bg_surface"])
    style.configure("ScrollInner.TFrame", background=p["bg_base"])

    style.configure("TLabel",
                    background=p["bg_surface"],
                    foreground=p["text_primary"],
                    font=FONT_BODY)
    style.configure("secondary.TLabel",
                    foreground=p["text_secondary"],
                    font=FONT_SMALL,
                    background=p["bg_surface"])
    style.configure("primary.TLabel",  foreground=p["accent_soft"],    font=FONT_BODY,  background=p["bg_surface"])
    style.configure("success.TLabel",  foreground=p["success"],        font=FONT_BODY,  background=p["bg_surface"])
    style.configure("danger.TLabel",   foreground=p["danger"],         font=FONT_BODY,  background=p["bg_surface"])
    style.configure("warning.TLabel",  foreground=p["warning"],        font=FONT_BODY,  background=p["bg_surface"])
    style.configure("info.TLabel",     foreground=p["info"],           font=FONT_BODY,  background=p["bg_surface"])

    # Base button — utility / secondary
    style.configure("TButton",
                    font=FONT_BODY,
                    background=p["bg_surface"],
                    foreground=p["text_primary"],
                    bordercolor=p["accent_glow"])
    # Primary action — terracotta bg, near-white text
    style.configure("primary.TButton",
                    background=p["accent_strong"],
                    foreground=p["bg_input"],
                    bordercolor=p["accent_glow"],
                    font=FONT_BODY_BOLD)
    style.map("primary.TButton",
              background=[("active", p["accent_mid"]), ("pressed", p["accent_glow"])])
    # Folder-picker: primary colours, regular weight
    style.configure("Folder.TButton",
                    background=p["accent_strong"],
                    foreground=p["bg_input"],
                    bordercolor=p["accent_glow"],
                    font=FONT_BODY)
    style.map("Folder.TButton",
              background=[("active", p["accent_mid"]), ("pressed", p["accent_glow"])])
    style.configure("secondary.TButton",
                    background=p["bg_surface"],
                    foreground=p["text_secondary"],
                    bordercolor=p["accent_glow"],
                    font=FONT_BODY)
    # near-white on forest green — readable
    style.configure("success.TButton",
                    background=p["success"],   foreground="#F0FBF2",
                    bordercolor=p["success"],  font=FONT_BODY_BOLD)
    # near-white on brick red — readable
    style.configure("danger.TButton",
                    background=p["danger"],    foreground="#FBF2F2",
                    bordercolor=p["danger"],   font=FONT_BODY_BOLD)
    style.configure("info.TButton",
                    background=p["info"],      foreground="#F0F4FB",
                    bordercolor=p["info"],     font=FONT_BODY_BOLD)

    style.configure("TEntry",
                    fieldbackground=p["bg_input"],
                    foreground=p["text_primary"],
                    bordercolor=p["accent_glow"],
                    font=FONT_ENTRY)
    style.map("TEntry",
              fieldbackground=[("disabled", p["bg_surface"]), ("readonly", p["bg_surface"])],
              foreground=[("disabled", p["accent_glow"]), ("readonly", p["text_secondary"])],
              bordercolor=[("readonly", p["accent_glow"])])

    style.configure("TCombobox",
                    fieldbackground=p["bg_input"],
                    foreground=p["text_primary"],
                    background=p["bg_surface"],
                    arrowcolor=p["accent_strong"],
                    font=FONT_ENTRY)

    style.configure("TNotebook",     background=p["bg_base"], bordercolor=p["bg_base"])
    style.configure("TNotebook.Tab",
                    background=p["bg_surface"],
                    foreground=p["text_secondary"],
                    font=FONT_SMALL,
                    padding=(8, 5))  # six tabs must fit the 560 px left panel
    style.map("TNotebook.Tab",
              background=[("selected", p["accent_strong"])],
              foreground=[("selected", p["bg_input"])])

    style.configure("TRadiobutton",
                    background=p["bg_surface"],
                    foreground=p["text_primary"],
                    font=FONT_BODY)
    style.configure("primary.TRadiobutton",
                    background=p["bg_surface"],
                    foreground=p["text_primary"],
                    font=FONT_BODY)

    style.configure("TCheckbutton",
                    background=p["bg_surface"],
                    foreground=p["text_primary"],
                    font=FONT_BODY)

    style.configure("TProgressbar",
                    background=p["accent_strong"],
                    troughcolor=p["bg_base"])
    style.configure("striped.Horizontal.TProgressbar",
                    background=p["accent_strong"],
                    troughcolor=p["bg_base"])

    style.configure("TSeparator", background=p["accent_glow"])
