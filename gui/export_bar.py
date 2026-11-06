import os
import threading
import tkinter as tk

import numpy as np
import ttkbootstrap as ttk

from core.output import export_stem
from gui.theme import PALETTE, FONT_SMALL, Tooltip as _Tooltip
from utils.log import log, short_reason
from utils.paths import EXPORT_SUBFOLDER, export_dir_for


class ExportBar:
    """Export controls under the preview, reachable from every tab.

    Exports the sprites in config["sprite_files"] with the current settings to the
    destination chosen on the Sprites & Export tab, on a worker thread.
    """

    def __init__(self, parent, config: dict, app, row: int):
        self.config = config
        self.app = app

        self._status_var   = tk.StringVar(value="")
        self._progress_var = tk.DoubleVar(value=0.0)
        self._stop_event: threading.Event | None = None
        self._running = False
        self._last_out_dir = None

        bar = ttk.Frame(parent)
        bar.grid(row=row, column=1, sticky="ew", pady=(2, 4))
        bar.columnconfigure(4, weight=1)

        self._export_one_btn = ttk.Button(bar, text="Export this sprite",
                                          style="success.TButton",
                                          command=self.export_current)
        self._export_one_btn.grid(row=0, column=0, sticky="w")
        _Tooltip(self._export_one_btn,
                 "Export the sprite shown in the preview with the current settings.\n"
                 "Which files are written (frames, spritesheet, GIF) and where is set on the "
                 "Sprites & Export tab.")

        self._export_all_btn = ttk.Button(bar, text="Export all (0)",
                                          style="success.TButton",
                                          command=self.export_all)
        self._export_all_btn.grid(row=0, column=1, sticky="w", padx=(6, 0))
        _Tooltip(self._export_all_btn,
                 "Export every sprite in the list with the current settings.")

        self._stop_btn = ttk.Button(bar, text="■  Stop", bootstyle="danger",
                                    command=self.stop)
        self._stop_btn.grid(row=0, column=2, sticky="w", padx=(6, 0))
        self._stop_btn.grid_remove()
        _Tooltip(self._stop_btn,
                 "Stop after the current sprite finishes.\n"
                 "Sprites already exported are kept.")

        self._open_btn = ttk.Button(bar, text="Open folder", bootstyle="secondary",
                                    command=self._open_last_folder)
        self._open_btn.grid(row=0, column=3, sticky="w", padx=(6, 0))
        self._open_btn.grid_remove()
        _Tooltip(self._open_btn, "Open the folder the last export was saved to.")

        self._status_lbl = ttk.Label(bar, textvariable=self._status_var, font=FONT_SMALL,
                                     bootstyle="secondary", anchor="w", width=1,
                                     background=PALETTE["bg_base"])
        self._status_lbl.grid(row=0, column=4, sticky="ew", padx=(10, 0))

        self._progressbar = ttk.Progressbar(bar, orient="horizontal", mode="determinate",
                                            variable=self._progress_var)
        self._progressbar.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(4, 0))

        self.update_sprite_count()

    # ------------------------------------------------------------------ #
    #  State                                                               #
    # ------------------------------------------------------------------ #

    def _files(self) -> list:
        return list(self.config.get("sprite_files", []))

    def update_sprite_count(self):
        n = len(self._files())
        self._export_all_btn.configure(text=f"Export all ({n})")
        if not self._running:
            state = "normal" if n else "disabled"
            self._export_one_btn.configure(state=state)
            self._export_all_btn.configure(state=state)
            self.update_idle_status()

    def update_idle_status(self):
        if self._running:
            return
        if not self._files():
            self._status_var.set("Add sprites on the Sprites & Export tab to export.")
        elif self.config.get("export_dest") == "folder" and self.config.get("export_folder"):
            folder = self.config["export_folder"]
            self._status_var.set(f"Saves to {folder if len(folder) <= 60 else '…' + folder[-59:]}")
        else:
            self._status_var.set(f"Saves to a {EXPORT_SUBFOLDER}/ folder next to each sprite.")

    def refresh(self, config: dict):
        self.config = config
        self.update_sprite_count()

    def is_running(self) -> bool:
        return self._running

    # ------------------------------------------------------------------ #
    #  Export                                                              #
    # ------------------------------------------------------------------ #

    def export_current(self):
        preview = self.app.preview_panel
        files = self._files()
        if self._running or not files:
            return
        self._start([files[preview.current_index()]])

    def export_all(self):
        files = self._files()
        if self._running or not files:
            return
        self._start(files)

    def stop(self):
        if self._stop_event:
            self._stop_event.set()
        self._status_var.set("Stopping after the current sprite…")

    def _start(self, files: list):
        # Snapshot settings now, so changing a preset mid-export can't mix effects
        # (or mismatch the effect name in the file names).
        p = self.app.preview_panel.build_p()
        jobs = self._plan_jobs(files, self._effect_label())
        writes = dict(write_frames=self.config.get("save_frames", True),
                      write_sheet=self.config.get("save_spritesheet", True),
                      write_gif=self.config.get("save_gif", True))

        self._running = True
        self.app.preview_panel.set_batch_running(True)
        self._export_one_btn.configure(state="disabled")
        self._export_all_btn.configure(state="disabled")
        self._open_btn.grid_remove()
        self._stop_btn.grid()
        self._progress_var.set(0.0)
        self._progressbar.configure(maximum=len(jobs))
        self._status_var.set(f"Exporting 0 / {len(jobs)}…" if len(jobs) > 1
                             else f"Exporting {os.path.basename(files[0])}…")

        self._stop_event = threading.Event()
        threading.Thread(target=self._worker, args=(jobs, p, writes, self._stop_event),
                         daemon=True).start()

    def _plan_jobs(self, files: list, effect: str) -> list:
        """(img_path, sprite_dir, stem) per sprite.

        Two sprites with the same name from different folders would land on the same
        <stem>/ in a chosen export folder; the later one gets ' (2)', ' (3)', ….
        """
        dest_mode = self.config.get("export_dest", "beside")
        dest_folder = self.config.get("export_folder")
        jobs, used = [], set()
        for path in files:
            out_dir = export_dir_for(path, dest_mode, dest_folder)
            name = os.path.splitext(os.path.basename(path))[0]
            stem, n = export_stem(name, effect), 1
            while os.path.normcase(os.path.join(out_dir, stem)) in used:
                n += 1
                stem = export_stem(f"{name} ({n})", effect)
            used.add(os.path.normcase(os.path.join(out_dir, stem)))
            jobs.append((path, os.path.join(out_dir, stem), stem))
        return jobs

    def _worker(self, jobs: list, p, writes: dict, stop: threading.Event):
        failed = []  # (filename, reason)
        n_done = 0
        out_dirs = []
        for img_path, sprite_dir, stem in jobs:
            if stop.is_set():
                break
            reason = self._export_one(img_path, sprite_dir, stem, p, writes)
            if reason:
                failed.append((os.path.basename(img_path), reason))
            else:
                out_dirs.append(sprite_dir)
            n_done += 1
            self.app.root.after(0, lambda d=n_done, t=len(jobs): self._on_progress(d, t))
        stopped = stop.is_set()
        self.app.root.after(0, lambda: self._on_done(jobs, n_done, stopped, failed, out_dirs))

    @staticmethod
    def _export_one(img_path: str, sprite_dir: str, stem: str, p, writes: dict):
        """Export one sprite; return None on success or a one-line failure reason."""
        from core.pipeline import process_sprite_file
        try:
            rng = np.random.default_rng(p.SEED)
            if not process_sprite_file(img_path, sprite_dir, stem, p, rng=rng, **writes):
                return "the image has no visible (non-transparent) pixels"
        except Exception as exc:
            log.exception("Export failed for %s", img_path)
            return short_reason(exc)
        return None

    def _on_progress(self, n_done: int, n_total: int):
        self._progress_var.set(n_done)
        if n_total > 1:
            self._status_var.set(f"Exporting {n_done} / {n_total}…")

    def _on_done(self, jobs, n_done, stopped, failed, out_dirs):
        self._running = False
        self._stop_event = None
        self._stop_btn.grid_remove()
        self.app.preview_panel.set_batch_running(False)
        self.update_sprite_count()
        n_total, n_ok = len(jobs), len(out_dirs)

        if out_dirs:
            # One sprite → its own folder; several → the folder holding them.
            self._last_out_dir = out_dirs[0] if n_total == 1 else os.path.dirname(out_dirs[0])
            self._open_btn.grid()

        if stopped:
            msg = f"Stopped — {n_ok} of {n_total} sprites exported."
        elif n_total == 1:
            sprite_dir = jobs[0][1]
            short_dir = os.path.join(os.path.basename(os.path.dirname(sprite_dir)),
                                     os.path.basename(sprite_dir))
            msg = (f"Exported {os.path.basename(jobs[0][0])} → {short_dir}" if n_ok
                   else f"Export failed — {os.path.basename(jobs[0][0])}.")
        else:
            msg = f"Done — {n_ok} of {n_total} sprites exported."
        self._status_var.set(msg)
        self._progress_var.set(n_done)

        if failed and n_total == 1:
            fname, reason = failed[0]
            self.app.show_error("Export failed", f"{fname} could not be exported:\n\n{reason}")
        elif failed:
            self.app.show_error(
                "Some sprites failed",
                f"{len(failed)} of {n_total} sprites could not be exported. "
                "The rest were saved normally.",
                details=[f"{fname}: {reason}" for fname, reason in failed])

    def _open_last_folder(self):
        if self._last_out_dir:
            self.app.open_file(self._last_out_dir, "Export folder")

    def _effect_label(self) -> str:
        """Effect part of export names: the loaded preset ('-mod' if tweaked), else 'custom'."""
        from utils.presets_io import get_preset, display_stem, is_modified
        active = self.config.get("active_preset")
        if not active or get_preset(active) is None:
            return "custom"
        return display_stem(active) + ("-mod" if is_modified(self.config, active) else "")
