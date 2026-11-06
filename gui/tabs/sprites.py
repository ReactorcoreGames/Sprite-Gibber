import os
import tkinter as tk
import tkinter.ttk as _tk_ttk
import tkinter.filedialog as _filedialog
from tkinter import messagebox

import ttkbootstrap as ttk
from PIL import Image

from gui.theme import PALETTE, FONT_BODY, FONT_SMALL, FONT_SPINBOX, Tooltip as _Tooltip
from utils.config import DEFAULT_CONFIG
from utils.log import log, short_reason
from utils.paths import (EXPORT_SUBFOLDER, normalize_user_file, same_path,
                         list_pngs, resolve_user_path)


def _truncate_left(path: str, max_chars: int = 50) -> str:
    return path if len(path) <= max_chars else "…" + path[-(max_chars - 1):]


# Images bigger than this (either side) still work but render slowly; warn on add.
_LARGE_IMAGE_PX = 512


def _check_image(path: str):
    """(reason, size): reason is None if path opens as an image, else a one-line reason."""
    try:
        with Image.open(path) as img:
            size = img.size
            img.verify()
    except Exception as exc:
        log.warning("Not adding %s: %s", path, exc)
        return short_reason(exc), None
    return None, size


def _large_image_note(large: list) -> str:
    """One-line warning for [(name, (w, h)), …] of oversized images just added."""
    if len(large) == 1:
        name, (w, h) = large[0]
        what = f"{name} is {w}×{h}"
    else:
        what = f"{len(large)} of the added images are"
    return f"{what} — over {_LARGE_IMAGE_PX}×{_LARGE_IMAGE_PX}, so previews and exports may be slow."


class SpritesTab:
    """Sprites & Export tab: the remembered sprite list, export destination and output formats.

    config["sprite_files"] (absolute paths) is the source of truth; the preview's
    Prev/Next cycles it and the export bar under the preview exports from it.
    """

    def __init__(self, parent, config: dict, app):
        self.config = config
        self.app = app

        # ── tk.Vars ──────────────────────────────────────────────────── #
        self._save_frames_var    = tk.BooleanVar(value=config.get("save_frames", True))
        self._save_sheet_var     = tk.BooleanVar(value=config.get("save_spritesheet", True))
        self._save_gif_var       = tk.BooleanVar(value=config.get("save_gif", True))
        self._sheet_cols_var     = tk.IntVar(value=config.get("SHEET_COLUMNS", 0))
        self._gif_scale_var      = tk.IntVar(value=config.get("GIF_SCALE", 4))
        self._ms_per_frame_var   = tk.IntVar(value=config.get("MS_PER_FRAME", 80))
        self._hold_first_ms_var  = tk.IntVar(value=config.get("HOLD_FIRST_MS", 500))
        self._hold_last_ms_var   = tk.IntVar(value=config.get("HOLD_LAST_MS", 800))
        self._gif_bg_var         = tk.BooleanVar(value=config.get("gif_use_preview_bg", False))
        self._dest_var           = tk.StringVar(value=config.get("export_dest", "beside"))
        self._list_note_var      = tk.StringVar(value="")

        self._gif_sub_widgets: list   = []
        self._sheet_col_widgets: list = []

        # parent is the scrollable inner frame supplied by _make_scrollable_tab
        self._frame = parent
        self._frame.columnconfigure(0, weight=1)

        self._drop_missing_files()

        self._build_sprite_list(row=0)
        self._build_destination(row=1)
        self._build_output_options(row=2)

        # initialise enable/disable state
        self._on_gif_toggle()
        self._on_spritesheet_toggle()
        self._fill_listbox()
        self._update_dest_label()

    # ────────────────────────────────────────────────────────────────── #
    #  Section 1 — Sprites                                               #
    # ────────────────────────────────────────────────────────────────── #

    def _build_sprite_list(self, row):
        lf = _tk_ttk.LabelFrame(self._frame, text="Sprites", padding=8)
        lf.grid(row=row, column=0, sticky="ew", padx=6, pady=(10, 4))
        lf.columnconfigure(0, weight=1)

        btns = ttk.Frame(lf)
        btns.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        add_files_btn = ttk.Button(btns, text="Add files…", style="Folder.TButton",
                                   command=self._on_add_files)
        add_files_btn.pack(side="left")
        _Tooltip(add_files_btn, "Pick one or more PNG sprites to add to the list.")

        add_folder_btn = ttk.Button(btns, text="Add folder…", style="Folder.TButton",
                                    command=self._on_add_folder)
        add_folder_btn.pack(side="left", padx=(6, 0))
        _Tooltip(add_folder_btn,
                 "Add every PNG directly inside a folder (subfolders are not included).")

        self._clear_btn = ttk.Button(btns, text="Clear", bootstyle="secondary",
                                     command=self._on_clear)
        self._clear_btn.pack(side="right")
        _Tooltip(self._clear_btn,
                 "Empty the list. Your sprite files are not touched.")

        self._remove_btn = ttk.Button(btns, text="Remove", bootstyle="secondary",
                                      command=self._on_remove)
        self._remove_btn.pack(side="right", padx=(0, 6))
        _Tooltip(self._remove_btn,
                 "Take the selected sprites off the list (Delete key works too).\n"
                 "Your sprite files are not touched.")

        lb_frame = ttk.Frame(lf)
        lb_frame.grid(row=1, column=0, sticky="ew")
        lb_frame.columnconfigure(0, weight=1)

        self._listbox = tk.Listbox(
            lb_frame,
            height=10,
            selectmode="extended",
            font=FONT_BODY,
            bg=PALETTE["bg_input"],
            fg=PALETTE["text_primary"],
            selectbackground=PALETTE["accent_strong"],
            selectforeground=PALETTE["bg_input"],
            activestyle="none",
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=PALETTE["accent_glow"],
            exportselection=False,
        )
        self._listbox.grid(row=0, column=0, sticky="ew")
        lb_scrollbar = ttk.Scrollbar(lb_frame, orient="vertical", command=self._listbox.yview)
        lb_scrollbar.grid(row=0, column=1, sticky="ns")
        self._listbox.configure(yscrollcommand=lb_scrollbar.set)
        # Show a sprite on explicit click / Enter only — <<ListboxSelect>> also fires
        # on every arrow-key step, which would start a render per step.
        self._listbox.bind("<ButtonRelease-1>", self._on_list_click)
        self._listbox.bind("<Return>",          self._on_list_click)
        self._listbox.bind("<Delete>",          lambda e: self._on_remove())
        _Tooltip(self._listbox,
                 "Click a sprite to show it in the preview.\n"
                 "Shift/Ctrl-click to select several, then Remove.")

        self._path_lbl = ttk.Label(lf, text="", font=FONT_SMALL, bootstyle="secondary",
                                   anchor="w", background=PALETTE["bg_surface"])
        self._path_lbl.grid(row=2, column=0, sticky="ew", pady=(4, 0))

        self._list_note_lbl = ttk.Label(lf, textvariable=self._list_note_var,
                                        font=FONT_SMALL, bootstyle="warning",
                                        anchor="w", wraplength=480,
                                        background=PALETTE["bg_surface"])
        self._list_note_lbl.grid(row=3, column=0, sticky="ew")
        # Only take up space when there is something to say.
        self._list_note_var.trace_add("write", lambda *_: self._list_note_lbl.grid()
                                      if self._list_note_var.get() else self._list_note_lbl.grid_remove())
        if not self._list_note_var.get():
            self._list_note_lbl.grid_remove()

    # ── list contents ── #

    def sprite_files(self) -> list:
        return list(self.config.get("sprite_files", []))

    def _drop_missing_files(self):
        files = self.sprite_files()
        kept = [f for f in files if os.path.isfile(f)]
        if len(kept) != len(files):
            gone = len(files) - len(kept)
            log.info("Dropped %d missing sprite(s) from the list: %s",
                     gone, [f for f in files if f not in kept])
            self._list_note_var.set(
                f"{gone} sprite{'s' if gone != 1 else ''} no longer found on disk "
                f"{'were' if gone != 1 else 'was'} removed from the list.")
            self._save("sprite_files", kept)

    def _set_files(self, files: list, show=None):
        """Store a new list, redraw it, and tell the preview/export bar. `show` = path to preview."""
        self._save("sprite_files", list(files))
        self._fill_listbox()
        self.app.on_sprite_list_changed(show=show)

    def _fill_listbox(self):
        files = self.sprite_files()
        names = [os.path.basename(f) for f in files]
        lb = self._listbox
        lb.delete(0, "end")
        for f, name in zip(files, names):
            # Same file name from two folders: add the folder so they can be told apart.
            if names.count(name) > 1:
                name = f"{name}   ({os.path.basename(os.path.dirname(f))})"
            lb.insert("end", name)
        state = "normal" if files else "disabled"
        self._remove_btn.configure(state=state)
        self._clear_btn.configure(state=state)
        if not files:
            self._path_lbl.configure(text="No sprites yet — click Add files… or Add folder….")
        self.highlight(self.app.current_sprite_index() if hasattr(self.app, "preview_panel") else 0)

    def highlight(self, idx: int):
        """Select row idx (the sprite shown in the preview) and show its full path."""
        files = self.sprite_files()
        if not files or not (0 <= idx < len(files)):
            return
        lb = self._listbox
        lb.selection_clear(0, "end")
        lb.selection_set(idx)
        lb.activate(idx)
        lb.see(idx)
        self._path_lbl.configure(text=_truncate_left(files[idx]))

    def _add_paths(self, paths: list):
        files = self.sprite_files()
        added, failed, large = [], [], []
        for raw in paths:
            path = normalize_user_file(raw)
            if any(same_path(path, f) for f in files + added):
                continue
            reason, size = _check_image(path)
            if reason:
                failed.append(f"{os.path.basename(path)}: {reason}")
            else:
                added.append(path)
                if max(size) > _LARGE_IMAGE_PX:
                    large.append((os.path.basename(path), size))
        self._list_note_var.set("")
        if added:
            self._set_files(files + added, show=added[0])
        if large:
            self._list_note_var.set(_large_image_note(large))
        if failed:
            self.app.show_error(
                "Some files were not added",
                f"{len(failed)} file{'s' if len(failed) != 1 else ''} could not be read "
                "as an image and {} left out.".format("were" if len(failed) != 1 else "was"),
                details=failed)
        return added

    def _initial_dir(self):
        files = self.sprite_files()
        if files:
            idx = self.app.current_sprite_index()
            return os.path.dirname(files[min(idx, len(files) - 1)])
        return None

    def _on_add_files(self):
        paths = _filedialog.askopenfilenames(
            title="Add sprites",
            initialdir=self._initial_dir(),
            filetypes=[("PNG images", "*.png"), ("PNG images", "*.PNG")],
        )
        if paths:
            self._add_paths(list(paths))

    def _on_add_folder(self):
        folder = _filedialog.askdirectory(title="Add every PNG in a folder",
                                          initialdir=self._initial_dir())
        if folder:
            self.add_folder(folder)

    def add_folder(self, folder: str):
        try:
            pngs = list_pngs(folder)
        except OSError as exc:
            log.exception("Could not read folder %s", folder)
            self.app.show_error("Could not read folder",
                                f"{folder}\n\n{short_reason(exc)}")
            return
        if not pngs:
            self._list_note_var.set(f"No PNG files found directly inside {os.path.basename(folder)}.")
            return
        self._add_paths(pngs)

    def _on_remove(self):
        sel = set(self._listbox.curselection())
        if not sel:
            return
        files = self.sprite_files()
        self._list_note_var.set("")
        self._set_files([f for i, f in enumerate(files) if i not in sel])

    def _on_clear(self):
        if not self.sprite_files():
            return
        if not messagebox.askyesno("Clear sprite list",
                                   "Remove all sprites from the list?\n\n"
                                   "Your sprite files are not touched.",
                                   parent=self.app.root):
            return
        self._list_note_var.set("")
        self._set_files([])

    def _on_list_click(self, event=None):
        sel = self._listbox.curselection()
        if len(sel) == 1:
            files = self.sprite_files()
            self._path_lbl.configure(text=_truncate_left(files[sel[0]]))
            self.app.preview_panel.show_sprite(sel[0])

    # ────────────────────────────────────────────────────────────────── #
    #  Section 2 — Export destination                                    #
    # ────────────────────────────────────────────────────────────────── #

    def _build_destination(self, row):
        lf = _tk_ttk.LabelFrame(self._frame, text="Export To", padding=8)
        lf.grid(row=row, column=0, sticky="ew", padx=6, pady=4)
        lf.columnconfigure(1, weight=1)

        beside_rb = ttk.Radiobutton(
            lf, text=f"Next to each sprite, in a {EXPORT_SUBFOLDER}/ subfolder",
            variable=self._dest_var, value="beside", command=self._on_dest_change)
        beside_rb.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 4))
        _Tooltip(beside_rb,
                 f"Each sprite's results go into a '{EXPORT_SUBFOLDER}' folder created next to the sprite file.\n"
                 "Each export gets its own sub-folder named <sprite>_<effect>.")

        folder_rb = ttk.Radiobutton(
            lf, text="This folder:", variable=self._dest_var, value="folder",
            command=self._on_dest_change)
        folder_rb.grid(row=1, column=0, sticky="w")
        _Tooltip(folder_rb,
                 "Send every export to one folder of your choice.\n"
                 "Each export gets its own sub-folder named <sprite>_<effect>.")

        choose_btn = ttk.Button(lf, text="Choose folder…", style="Folder.TButton",
                                command=self._choose_folder)
        choose_btn.grid(row=1, column=2, sticky="e")
        _Tooltip(choose_btn, "Pick the folder that exports are saved into.")

        self._dest_path_lbl = ttk.Label(lf, text="", font=FONT_SMALL, bootstyle="secondary",
                                        anchor="w", background=PALETTE["bg_surface"])
        self._dest_path_lbl.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(2, 4))

        note = ttk.Label(lf, text="Exporting the same sprite with the same effect again replaces "
                                  "the earlier result.",
                         font=FONT_SMALL, bootstyle="secondary", anchor="w", wraplength=480,
                         background=PALETTE["bg_surface"])
        note.grid(row=3, column=0, columnspan=3, sticky="ew")

    def _on_dest_change(self):
        if self._dest_var.get() == "folder" and not self.config.get("export_folder"):
            if not self._choose_folder():
                self._dest_var.set("beside")
                return
        self._save("export_dest", self._dest_var.get())
        self._update_dest_label()

    def _choose_folder(self) -> bool:
        current = self.config.get("export_folder")
        folder = _filedialog.askdirectory(
            title="Choose export folder",
            initialdir=resolve_user_path(current) if current else self._initial_dir(),
        )
        if not folder:
            return False
        self.set_export_folder(folder)
        return True

    def set_export_folder(self, folder: str):
        self._save("export_folder", normalize_user_file(folder))
        self._dest_var.set("folder")
        self._save("export_dest", "folder")
        self._update_dest_label()

    def _update_dest_label(self):
        folder = self.config.get("export_folder")
        if self._dest_var.get() == "folder" and folder:
            self._dest_path_lbl.configure(text=_truncate_left(folder))
        elif folder:
            self._dest_path_lbl.configure(text=f"(chosen folder: {_truncate_left(folder, 34)})")
        if folder:
            self._dest_path_lbl.grid()
        else:
            self._dest_path_lbl.grid_remove()
        if hasattr(self.app, "export_bar"):
            self.app.export_bar.update_idle_status()

    # ────────────────────────────────────────────────────────────────── #
    #  Section 3 — Output files                                          #
    # ────────────────────────────────────────────────────────────────── #

    def _build_output_options(self, row):
        lf = _tk_ttk.LabelFrame(self._frame, text="Output Files", padding=8)
        lf.grid(row=row, column=0, sticky="ew", padx=6, pady=(4, 10))
        lf.columnconfigure(0, weight=1)

        # Frame PNGs
        frame_png_cb = ttk.Checkbutton(
            lf, text="Frame PNGs",
            variable=self._save_frames_var,
            command=lambda: self._on_save_toggle("save_frames", self._save_frames_var),
        )
        frame_png_cb.grid(row=0, column=0, sticky="w", pady=(0, 4))
        _Tooltip(frame_png_cb,
                 "Save each animation frame as a separate PNG file\n"
                 "(<sprite>_<effect>_00.png, _01.png, …).")

        # Spritesheet row
        sheet_row = ttk.Frame(lf)
        sheet_row.grid(row=1, column=0, sticky="ew", pady=(0, 4))

        sheet_cb = ttk.Checkbutton(
            sheet_row, text="Spritesheet",
            variable=self._save_sheet_var,
            command=lambda: self._on_save_toggle("save_spritesheet", self._save_sheet_var),
        )
        sheet_cb.grid(row=0, column=0, sticky="w")
        _Tooltip(sheet_cb,
                 "Save all frames tiled into a single PNG image (a spritesheet).\n"
                 "Useful for importing into game engines that expect a single texture atlas.")

        cols_lbl = ttk.Label(sheet_row, text="Frames per row:", font=FONT_BODY,
                             background=PALETTE["bg_surface"])
        cols_lbl.grid(row=0, column=1, sticky="w", padx=(14, 4))

        cols_sb = self._make_spinbox(sheet_row, self._sheet_cols_var, 0, 64, "SHEET_COLUMNS", width=4)
        cols_sb.grid(row=0, column=2, sticky="w")

        _cols_default = DEFAULT_CONFIG.get("SHEET_COLUMNS", 0)
        _cols_tip = (
            f"How many frames to place in each row of the spritesheet.\n"
            f"0 puts all frames in a single row (default: {_cols_default})."
        )
        _Tooltip(cols_lbl, _cols_tip)
        _Tooltip(cols_sb,  _cols_tip)

        hint_lbl = ttk.Label(sheet_row, text="(0 = one row)", font=FONT_SMALL,
                              bootstyle="secondary", background=PALETTE["bg_surface"])
        hint_lbl.grid(row=0, column=3, sticky="w", padx=(6, 0))
        _Tooltip(hint_lbl, _cols_tip)

        self._sheet_col_widgets = [cols_lbl, cols_sb, hint_lbl]

        # Animated GIF checkbox
        gif_cb = ttk.Checkbutton(
            lf, text="Animated GIF",
            variable=self._save_gif_var,
            command=lambda: self._on_save_toggle("save_gif", self._save_gif_var),
        )
        gif_cb.grid(row=2, column=0, sticky="w", pady=(0, 2))
        _Tooltip(gif_cb,
                 "Save the animation as a looping animated GIF.\n"
                 "GIFs are great for sharing previews but are limited to 256 colours per frame.")

        # GIF sub-controls (indented)
        gif_sub = ttk.Frame(lf)
        gif_sub.grid(row=3, column=0, sticky="ew", padx=(16, 0), pady=(0, 4))
        gif_sub.columnconfigure(1, weight=1)
        self._build_gif_sub(gif_sub)

    def _build_gif_sub(self, parent):
        _scale_default = DEFAULT_CONFIG.get("GIF_SCALE", 4)
        _dur_default   = DEFAULT_CONFIG.get("MS_PER_FRAME", 80)
        _hf_default    = DEFAULT_CONFIG.get("HOLD_FIRST_MS", 500)
        _hl_default    = DEFAULT_CONFIG.get("HOLD_LAST_MS", 800)

        # Scale slider (1–20×)
        scale_row = ttk.Frame(parent)
        scale_row.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(2, 4))
        scale_row.columnconfigure(1, weight=1)

        _scale_tip = (
            f"How many times larger to make the GIF compared to the original sprite.\n"
            f"Pixel art looks best at whole-number multiples (2×, 4×, 8×). Default: {_scale_default}×.\n"
            f"Higher values make a bigger file."
        )
        lbl = ttk.Label(scale_row, text="GIF Scale:", font=FONT_BODY,
                        background=PALETTE["bg_surface"])
        lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
        self._gif_sub_widgets.append(lbl)
        _Tooltip(lbl, _scale_tip)

        self._gif_scale_slider = ttk.Scale(
            scale_row, from_=1, to=20, orient="horizontal",
            variable=self._gif_scale_var,
            command=self._on_gif_scale_slide,
        )
        self._gif_scale_slider.grid(row=0, column=1, sticky="ew", padx=(0, 6))
        self._gif_sub_widgets.append(self._gif_scale_slider)
        _Tooltip(self._gif_scale_slider, _scale_tip + "\nDouble-click the slider to reset it.")

        def _reset_scale(_e):
            self._on_gif_scale_slide(_scale_default)
            return "break"
        self._gif_scale_slider.bind("<Double-Button-1>", _reset_scale)

        self._gif_scale_readout = ttk.Label(
            scale_row, text=f"{self._gif_scale_var.get()}×",
            font=FONT_SMALL, bootstyle="secondary", width=4, anchor="w",
        )
        self._gif_scale_readout.grid(row=0, column=2, sticky="w")
        self._gif_sub_widgets.append(self._gif_scale_readout)

        # Duration slider
        dur_row = ttk.Frame(parent)
        dur_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 4))
        dur_row.columnconfigure(1, weight=1)

        _dur_tip = (
            f"How long each frame is shown in the GIF, in milliseconds.\n"
            f"Lower = faster animation. Default: {_dur_default} ms.\n"
            f"Example: 80 ms ≈ 12 frames per second.\n"
            f"The slider covers 20–250 ms; type any value from 10 to 2000 ms in the box.\n"
            f"Double-click the slider to reset it."
        )
        dur_lbl = ttk.Label(dur_row, text="GIF Frame speed:", font=FONT_BODY,
                            background=PALETTE["bg_surface"])
        dur_lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
        self._gif_sub_widgets.append(dur_lbl)
        _Tooltip(dur_lbl, _dur_tip)

        self._dur_readout = ttk.Spinbox(dur_row, from_=10, to=2000, increment=10,
                                        textvariable=self._ms_per_frame_var,
                                        width=5, font=FONT_SPINBOX)
        self._dur_readout.grid(row=0, column=2, sticky="e")
        for seq in ("<<Increment>>", "<<Decrement>>", "<FocusOut>", "<Return>"):
            self._dur_readout.bind(seq, lambda e: self._save_ms_per_frame())
        self._gif_sub_widgets.append(self._dur_readout)
        _Tooltip(self._dur_readout, _dur_tip)

        ms_lbl = ttk.Label(dur_row, text="ms/frame", font=FONT_SMALL,
                           bootstyle="secondary", background=PALETTE["bg_surface"])
        ms_lbl.grid(row=0, column=3, sticky="w", padx=(4, 0))
        self._gif_sub_widgets.append(ms_lbl)

        dur_slider = ttk.Scale(
            dur_row, variable=self._ms_per_frame_var,
            from_=20, to=250, orient="horizontal",
            command=lambda v: self._ms_per_frame_var.set(round(float(v) / 10) * 10),
        )
        dur_slider.grid(row=0, column=1, sticky="ew", padx=4)
        dur_slider.bind("<ButtonRelease-1>", lambda e: self._save_ms_per_frame())

        def _reset_dur(_e):
            self._ms_per_frame_var.set(_dur_default)
            self._save_ms_per_frame()
            return "break"
        dur_slider.bind("<Double-Button-1>", _reset_dur)
        self._gif_sub_widgets.append(dur_slider)
        _Tooltip(dur_slider, _dur_tip)

        # First / last frame holds share one row
        hold_row = ttk.Frame(parent)
        hold_row.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 2))

        _hf_tip = (
            f"How long to hold (freeze) the first frame of the GIF before the animation plays.\n"
            f"Useful for giving viewers a moment to see the intact sprite. Default: {_hf_default} ms."
        )
        _hl_tip = (
            f"How long to hold (freeze) the last frame of the GIF after the animation finishes.\n"
            f"Useful for letting viewers see the final gib result before it loops. Default: {_hl_default} ms."
        )
        col = 0
        for text, var, key, tip in (("Pause first frame:", self._hold_first_ms_var, "HOLD_FIRST_MS", _hf_tip),
                                    ("last:", self._hold_last_ms_var, "HOLD_LAST_MS", _hl_tip)):
            lbl = ttk.Label(hold_row, text=text, font=FONT_BODY,
                            background=PALETTE["bg_surface"])
            lbl.grid(row=0, column=col, sticky="w", padx=(0 if col == 0 else 14, 6))
            self._gif_sub_widgets.append(lbl)
            _Tooltip(lbl, tip)

            sb = self._make_ms_spinbox(hold_row, var, key, width=6)
            sb.grid(row=0, column=col + 1, sticky="w")
            self._gif_sub_widgets.append(sb)
            _Tooltip(sb, tip)

            unit = ttk.Label(hold_row, text="ms", font=FONT_SMALL,
                             bootstyle="secondary", background=PALETTE["bg_surface"])
            unit.grid(row=0, column=col + 2, sticky="w", padx=(4, 0))
            self._gif_sub_widgets.append(unit)
            col += 3

        # GIF background colour
        gif_bg_cb = ttk.Checkbutton(
            parent, text="Use preview background colour in GIF",
            variable=self._gif_bg_var,
            bootstyle="round-toggle",
            command=lambda: self._save("gif_use_preview_bg", self._gif_bg_var.get()),
        )
        gif_bg_cb.grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 0))
        self._gif_sub_widgets.append(gif_bg_cb)
        _Tooltip(gif_bg_cb,
                 "Fill the GIF background with the same colour shown in the preview panel, instead of leaving it transparent.\n"
                 "Handy for sharing GIFs on platforms that don't support transparency (e.g. Twitter/X).")

    def _on_save_toggle(self, key: str, var: tk.BooleanVar):
        if not var.get():
            others_on = any([
                self._save_frames_var.get() if key != "save_frames" else False,
                self._save_sheet_var.get()  if key != "save_spritesheet" else False,
                self._save_gif_var.get()    if key != "save_gif" else False,
            ])
            if not others_on:
                var.set(True)
                return
        self._save(key, var.get())
        if key == "save_spritesheet":
            self._on_spritesheet_toggle()
        elif key == "save_gif":
            self._on_gif_toggle()

    def _on_gif_toggle(self):
        state = "normal" if self._save_gif_var.get() else "disabled"
        for w in self._gif_sub_widgets:
            try:
                w.configure(state=state)
            except tk.TclError:
                pass

    def _on_spritesheet_toggle(self):
        state = "normal" if self._save_sheet_var.get() else "disabled"
        for w in self._sheet_col_widgets:
            try:
                w.configure(state=state)
            except tk.TclError:
                pass

    def _save_ms_per_frame(self):
        try:
            raw = float(self._dur_readout.get())
        except (ValueError, tk.TclError):
            raw = self.config.get("MS_PER_FRAME", 80)
        rounded = max(10, min(2000, int(round(raw / 10) * 10)))
        self._ms_per_frame_var.set(rounded)
        if rounded != self.config.get("MS_PER_FRAME"):
            self._save("MS_PER_FRAME", rounded)

    def _on_gif_scale_slide(self, value):
        v = max(1, min(20, round(float(value))))
        self._gif_scale_var.set(v)
        self._gif_scale_readout.configure(text=f"{v}×")
        self._save("GIF_SCALE", v)

    def _make_ms_spinbox(self, parent, var: tk.IntVar, key: str, width: int = 6) -> ttk.Spinbox:
        """Spinbox for millisecond values — steps in 10 ms increments, range 0–10000."""
        sb = ttk.Spinbox(parent, from_=0, to=10000, increment=10,
                         textvariable=var, width=width, font=FONT_SPINBOX)

        def _clamp(e=None):
            try:
                v = int(var.get())
            except (ValueError, tk.TclError):
                v = 0
            rounded = max(0, round(v / 10) * 10)
            var.set(rounded)
            self._save(key, rounded)

        sb.bind("<<Increment>>", _clamp)
        sb.bind("<<Decrement>>", _clamp)
        sb.bind("<FocusOut>",    _clamp)
        sb.bind("<Return>",      _clamp)
        return sb

    def _make_spinbox(self, parent, var: tk.IntVar, min_val: int, max_val: int,
                      key: str, width: int = 5) -> ttk.Spinbox:
        sb = ttk.Spinbox(parent, from_=min_val, to=max_val,
                         textvariable=var, width=width, font=FONT_SPINBOX)

        def _clamp(e=None):
            try:
                v = int(var.get())
            except (ValueError, tk.TclError):
                v = min_val
            clamped = max(min_val, min(max_val, v))
            var.set(clamped)
            self._save(key, clamped)

        sb.bind("<<Increment>>", _clamp)
        sb.bind("<<Decrement>>", _clamp)
        sb.bind("<FocusOut>",    _clamp)
        sb.bind("<Return>",      _clamp)
        return sb

    # ────────────────────────────────────────────────────────────────── #
    #  Save / refresh                                                     #
    # ────────────────────────────────────────────────────────────────── #

    def _save(self, key: str, value):
        self.config[key] = value
        self.app.save_config()

    def refresh(self, config: dict):
        self.config = config
        self._save_frames_var.set(config.get("save_frames", True))
        self._save_sheet_var.set(config.get("save_spritesheet", True))
        self._save_gif_var.set(config.get("save_gif", True))
        self._sheet_cols_var.set(config.get("SHEET_COLUMNS", 0))
        gif_scale = config.get("GIF_SCALE", 4)
        self._gif_scale_var.set(gif_scale)
        self._gif_scale_readout.configure(text=f"{gif_scale}×")
        self._ms_per_frame_var.set(config.get("MS_PER_FRAME", 80))
        self._hold_first_ms_var.set(config.get("HOLD_FIRST_MS", 500))
        self._hold_last_ms_var.set(config.get("HOLD_LAST_MS", 800))
        self._gif_bg_var.set(config.get("gif_use_preview_bg", False))
        self._dest_var.set(config.get("export_dest", "beside"))
        self._on_gif_toggle()
        self._on_spritesheet_toggle()
        self._update_dest_label()
