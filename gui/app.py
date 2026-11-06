import os
import subprocess
import sys
import webbrowser
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

import ttkbootstrap as ttk

from gui.theme import (
    _inject_gibber_theme, apply_theme,
    PALETTE, FONT_TITLE, FONT_SMALL, FONT_TINY,
)
from utils.config import load_config, save_config as _save_config
from utils.log import log, setup_logging, short_reason
from utils.paths import app_path


class GibberApp:
    def __init__(self):
        setup_logging()
        self.config = load_config()
        self._geo_after_id = None

        _inject_gibber_theme()
        self.root = ttk.Window(themename="gibber")
        self.root.title("Sprite Gibber")
        self.root.geometry("1200x800")
        self.root.minsize(760, 600)
        self.root.state("zoomed")

        style = ttk.Style()
        apply_theme(style, root=self.root)
        self.root.report_callback_exception = self._on_callback_error
        self._callback_error_shown = False

        self._apply_icon(self.root)
        self._build_ui()
        self._refresh_all_tabs()
        self._left_notebook.select(0)
        self._restore_geometry()
        self.root.after(150, self._auto_preview_on_startup)
        self.root.after(1500, self._prebuild_next_tab)

    # ------------------------------------------------------------------ #
    #  Icon                                                                #
    # ------------------------------------------------------------------ #

    def _apply_icon(self, window):
        project_root = Path(__file__).resolve().parent.parent
        icon_paths = [
            app_path("assets", "icon.ico"),
            project_root / "assets" / "icon.ico",
        ]
        if hasattr(sys, "_MEIPASS"):
            icon_paths.insert(0, Path(sys._MEIPASS) / "icon.ico")
        for p in icon_paths:
            if p.exists():
                try:
                    window.iconbitmap(str(p))
                    return
                except Exception:
                    continue

    # ------------------------------------------------------------------ #
    #  UI build                                                            #
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=0)
        self.root.rowconfigure(4, weight=0)
        self.root.columnconfigure(0, weight=1)

        self._build_header()
        ttk.Separator(self.root, orient="horizontal").grid(row=1, column=0, sticky="ew")
        self._build_main_area()
        ttk.Separator(self.root, orient="horizontal").grid(row=3, column=0, sticky="ew")
        self._build_footer()
        self.root.bind("<Configure>", self._on_configure)

    def _build_header(self):
        hf = ttk.Frame(self.root, padding=(12, 6))
        hf.grid(row=0, column=0, sticky="ew")
        hf.columnconfigure(0, weight=0)
        hf.columnconfigure(1, weight=1)
        hf.columnconfigure(2, weight=0)

        ttk.Label(hf, text="Sprite Gibber",
                  font=FONT_TITLE, background=PALETTE["bg_base"]).grid(
                  row=0, column=0, rowspan=2, sticky="w", padx=(0, 16))

        ttk.Label(hf, text="The easy sprite gib animation generator",
                  font=FONT_SMALL, bootstyle="secondary",
                  background=PALETTE["bg_base"]).grid(
                  row=0, column=1, sticky="sw", pady=(4, 0))
        ttk.Label(hf, text="Add sprites  →  pick a preset  →  tweak & preview  →  export",
                  font=FONT_TINY, bootstyle="secondary",
                  background=PALETTE["bg_base"]).grid(
                  row=1, column=1, sticky="nw", pady=(0, 4))

        ttk.Button(hf, text="Help Guide", bootstyle="secondary",
                   command=self._open_help_guide).grid(
                   row=0, column=2, rowspan=2, sticky="e", padx=(16, 0))

    def _open_help_guide(self):
        self.open_file(app_path("guide.md"), "Help Guide")

    def open_file(self, path, what):
        """Open a file with its associated app; fall back to Notepad for text files
        with no association (e.g. .md / .log on a fresh Windows install)."""
        path = str(path)
        if not os.path.exists(path):
            messagebox.showinfo(what, f"{what} not found.\n\nExpected: {path}", parent=self.root)
            return
        try:
            os.startfile(path)
        except OSError:
            try:
                subprocess.Popen(["notepad.exe", path])
            except OSError as exc:
                log.exception("Could not open %s", path)
                messagebox.showerror(what, f"Could not open {path}\n\n{short_reason(exc)}",
                                     parent=self.root)

    def _build_main_area(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=2, column=0, sticky="nsew", padx=6, pady=4)
        self.main_frame.columnconfigure(0, weight=0)  # left panel: fixed width
        self.main_frame.columnconfigure(1, weight=0)  # separator
        self.main_frame.columnconfigure(2, weight=1)  # preview panel: expands
        self.main_frame.rowconfigure(0, weight=1)

        sep1 = ttk.Separator(self.main_frame, orient="vertical")
        sep1.grid(row=0, column=1, sticky="ns", padx=2)

        self._build_left_panel()
        self._build_preview_panel()

    def _build_preview_panel(self):
        from gui.preview import PreviewPanel
        self.preview_panel = PreviewPanel(self.main_frame, self.config, self)
        self.export_bar = self.preview_panel.export_bar

    def _build_left_panel(self):
        lp = ttk.Frame(self.main_frame, width=560)
        lp.grid(row=0, column=0, sticky="ns", padx=(0, 4))
        lp.grid_propagate(False)
        lp.rowconfigure(0, weight=1)
        lp.columnconfigure(0, weight=1)

        nb = ttk.Notebook(lp)
        nb.grid(row=0, column=0, sticky="nsew")

        self._sprites_inner  = self._make_scrollable_tab(nb, "Sprites & Export")
        self._presets_inner  = self._make_scrollable_tab(nb, "Presets")
        self._physics_inner  = self._make_scrollable_tab(nb, "Physics")
        self._tint_inner     = self._make_scrollable_tab(nb, "Tint")
        self._dissolve_inner = self._make_scrollable_tab(nb, "Dissolve")
        self._mask_inner     = self._make_scrollable_tab(nb, "Mask")

        self._left_notebook = nb
        nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        from gui.tabs.sprites import SpritesTab
        self.sprites_tab = SpritesTab(self._sprites_inner, self.config, self)

        # The other tabs are built when first shown (or in idle time shortly after
        # startup) — building and laying out every tab up front was most of the
        # startup time. Everything that touches a tab checks hasattr() first.
        self._lazy_tabs = {
            1: ("presets_tab",  "gui.tabs.presets",  "PresetsTab",  self._presets_inner),
            2: ("physics_tab",  "gui.tabs.physics",  "PhysicsTab",  self._physics_inner),
            3: ("tint_tab",     "gui.tabs.tint",     "TintTab",     self._tint_inner),
            4: ("dissolve_tab", "gui.tabs.dissolve", "DissolveTab", self._dissolve_inner),
            5: ("mask_tab",     "gui.tabs.mask",     "MaskTab",     self._mask_inner),
        }

    def _ensure_tab(self, idx: int):
        """Build the tab at notebook index idx if it hasn't been built yet."""
        spec = self._lazy_tabs.pop(idx, None)
        if spec is None:
            return
        attr, module, cls, inner = spec
        import importlib
        tab = getattr(importlib.import_module(module), cls)(inner, self.config, self)
        setattr(self, attr, tab)
        tab.refresh(self.config)

    def _prebuild_next_tab(self):
        """Build the remaining hidden tabs one per idle slot, so switching to them
        later is instant without delaying the first paint."""
        if self._lazy_tabs:
            self._ensure_tab(min(self._lazy_tabs))
            self.root.after(120, self._prebuild_next_tab)

    def _make_scrollable_tab(self, notebook, title):
        outer = ttk.Frame(notebook)
        notebook.add(outer, text=title)
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)

        canvas = tk.Canvas(outer, highlightthickness=0, background=PALETTE["bg_base"])
        canvas.grid(row=0, column=0, sticky="nsew")

        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        sb.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=sb.set)

        inner = ttk.Frame(canvas, style="ScrollInner.TFrame")
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _update_scrollregion(_=None):
            bbox = canvas.bbox("all")
            if bbox:
                # Clamp bottom to at least canvas height so content can't be
                # scrolled downward when it's shorter than the visible area.
                canvas_h = canvas.winfo_height()
                bottom = max(bbox[3], canvas_h)
                canvas.configure(scrollregion=(0, 0, bbox[2], bottom))
        inner.bind("<Configure>", _update_scrollregion)

        def _on_canvas_resize(e):
            canvas.itemconfig(window_id, width=e.width)
            _update_scrollregion()
        canvas.bind("<Configure>", _on_canvas_resize)

        def _on_mousewheel(e):
            # Let native-scrolling widgets (Listbox, Text, etc.) handle their
            # own wheel events; only scroll the tab canvas for everything else.
            if isinstance(e.widget, (tk.Listbox, tk.Text)):
                e.widget.yview_scroll(int(-1 * (e.delta / 120)), "units")
                return
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        return inner

    def _restore_geometry(self):
        geo = self.config.get("window_geometry")
        if geo and self.root.state() != "zoomed":
            try:
                self.root.geometry(geo)
            except Exception:
                pass

    def _auto_preview_on_startup(self):
        self.preview_panel.trigger_auto_preview()

    def _on_tab_changed(self, event=None):
        try:
            idx = self._left_notebook.index("current")
        except Exception:
            return
        self._ensure_tab(idx)
        self.config["active_tab"] = idx
        self.save_config()

    def _on_configure(self, event=None):
        if self._geo_after_id is not None:
            self.root.after_cancel(self._geo_after_id)
        self._geo_after_id = self.root.after(100, self._save_geometry)

    def _save_geometry(self):
        self._geo_after_id = None
        if self.root.state() == "zoomed":
            return
        geo = self.root.geometry()
        self.config["window_geometry"] = geo
        self.save_config()

    def _build_footer(self):
        ff = ttk.Frame(self.root, padding=(8, 4))
        ff.grid(row=4, column=0, sticky="ew")

        ttk.Label(ff, text="Made by Reactorcore", font=FONT_TINY,
                  background=PALETTE["bg_base"]).pack(side="left", padx=(4, 2))
        link = ttk.Label(ff, text="https://linktr.ee/reactorcore",
                         font=FONT_TINY, foreground=PALETTE["accent_soft"],
                         background=PALETTE["bg_base"], cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: webbrowser.open("https://linktr.ee/reactorcore"))

    # ------------------------------------------------------------------ #
    #  Error reporting                                                     #
    # ------------------------------------------------------------------ #

    def _on_callback_error(self, exc_type, exc, tb):
        """Tk swallows exceptions raised in callbacks (to stderr, which the windowed
        exe doesn't have). Log every one; tell the user once per session."""
        log.error("Error in GUI callback", exc_info=(exc_type, exc, tb))
        if self._callback_error_shown:
            return
        self._callback_error_shown = True
        self.show_error(
            "Something went wrong",
            f"An unexpected error occurred:\n\n{short_reason(exc)}\n\n"
            "The app may keep working, but if something looks off, restart it. "
            "Further errors this session are only written to the log.")

    def show_error(self, title, message, details=None):
        """Error dialog with an Open Log button. `details` is an optional scrollable list."""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.transient(self.root)
        win.resizable(False, False)
        self._apply_icon(win)
        ttk.Label(win, text=message, font=FONT_SMALL, wraplength=440,
                  justify="left").pack(padx=16, pady=(16, 8), anchor="w")
        if details:
            box = tk.Text(win, height=min(10, 2 * len(details)), width=64, wrap="word",
                          font=FONT_TINY, relief="flat", borderwidth=1,
                          highlightthickness=1, highlightbackground=PALETTE["accent_glow"])
            box.insert("1.0", "\n".join(details))
            box.configure(state="disabled")
            box.pack(padx=16, pady=(0, 8), fill="x")
        btns = ttk.Frame(win)
        btns.pack(pady=(4, 14))
        from utils.log import log_path
        ttk.Button(btns, text="Open Log", bootstyle="secondary",
                   command=lambda: self.open_file(log_path(), "Log file")).pack(side="left", padx=6)
        ttk.Button(btns, text="OK", bootstyle="primary",
                   command=win.destroy).pack(side="left", padx=6)
        win.bind("<Escape>", lambda e: win.destroy())
        win.focus_force()

    # ------------------------------------------------------------------ #
    #  Public helpers called by tab classes                                #
    # ------------------------------------------------------------------ #

    def attach_context_menu(self, entry_widget):
        menu = tk.Menu(entry_widget, tearoff=0)
        menu.add_command(label="Cut",        command=lambda: entry_widget.event_generate("<<Cut>>"))
        menu.add_command(label="Copy",       command=lambda: entry_widget.event_generate("<<Copy>>"))
        menu.add_command(label="Paste",      command=lambda: entry_widget.event_generate("<<Paste>>"))
        menu.add_command(label="Select All", command=lambda: entry_widget.event_generate("<<SelectAll>>"))

        def _show(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        entry_widget.bind("<Button-3>", _show)

    def save_config(self):
        _save_config(self.config)

    def load_preset(self, name):
        from utils.presets_io import get_preset

        if name is None or name == "None (manual params)":
            self.config["active_preset"] = None
            self.save_config()
            self._refresh_all_tabs()
            return

        entry = get_preset(name)
        if entry is not None:
            from utils.config import DEFAULT_CONFIG, GUI_ONLY_KEYS
            # Reset all effect params to defaults before applying the preset, so no
            # stale values from a previously loaded preset bleed through. GUI state
            # and the user's export settings (GUI_ONLY_KEYS) are kept.
            for key, default_val in DEFAULT_CONFIG.items():
                if key not in GUI_ONLY_KEYS:
                    self.config[key] = default_val
            for key, val in entry["params"].items():
                if key not in GUI_ONLY_KEYS:
                    self.config[key] = val
            self.config["active_preset"] = name
            self.save_config()

        self._refresh_all_tabs()
        if hasattr(self, "preview_panel"):
            self.preview_panel.set_dirty(True)  # preset loaded but preview not yet updated

    def on_sprite_list_changed(self, show=None):
        if hasattr(self, "preview_panel"):
            self.preview_panel.notify_sprite_list_changed(show=show)

    def current_sprite_index(self) -> int:
        return self.preview_panel.current_index() if hasattr(self, "preview_panel") else 0

    def mark_preview_dirty(self):
        if hasattr(self, "preview_panel"):
            self.preview_panel.set_dirty(True)

    def _refresh_all_tabs(self):
        if hasattr(self, "presets_tab"):
            self.presets_tab.refresh(self.config)
        if hasattr(self, "physics_tab"):
            self.physics_tab.refresh(self.config)
        if hasattr(self, "tint_tab"):
            self.tint_tab.refresh(self.config)
        if hasattr(self, "dissolve_tab"):
            self.dissolve_tab.refresh(self.config)
        if hasattr(self, "mask_tab"):
            self.mask_tab.refresh(self.config)
        if hasattr(self, "sprites_tab"):
            self.sprites_tab.refresh(self.config)
        if hasattr(self, "preview_panel"):
            self.preview_panel.refresh(self.config)

    # ------------------------------------------------------------------ #
    #  Run                                                                 #
    # ------------------------------------------------------------------ #

    def run(self):
        self.root.mainloop()
