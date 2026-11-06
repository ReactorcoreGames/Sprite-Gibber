import tkinter as tk
import tkinter.ttk as _tk_ttk

import ttkbootstrap as ttk

from gui.theme import PALETTE, FONT_BODY, FONT_SMALL, FONT_TINY, FONT_BODY_BOLD, Tooltip as _Tooltip
from gui.widgets.randomizer_panel import RandomizerPanel
from utils.dev import DEV_MODE
from utils.log import log, short_reason
from utils.presets_io import (
    save_user_preset_from_config, delete_user_preset, search_presets,
    load_user_presets, get_preset, is_official_name, is_modified, display_stem,
    validate_custom_name, custom_preset_exists,
)

_SCOPE_OPTIONS = ["All", "Official", "Custom"]

_LEGEND = "*  built-in (read-only)   ·   no *  your own   ·   hover for help"

_TIP_LEGEND = (
    "Preset names follow  Category-Subtype-locale[-variant].\n\n"
    "* at the start = built-in preset. Built-ins can't be changed or deleted, so the\n"
    "original is always there. To keep your own version, use Save As Copy.\n"
    "No * = a custom preset you saved. Name yours in the same format so it sorts\n"
    "next to the preset it came from (e.g. Fire-Burn-terra-copy).\n\n"
    "Locales — where the effect happens:\n"
    "  terra  — normal ground: chunks fall and settle on the floor\n"
    "  aqua   — underwater: chunks float upward\n"
    "  depth  — crushing pressure: chunks pull inward into a clump\n"
    "  space  — zero gravity: chunks drift and scatter\n"
    "  wave   — shockwave or wind: chunks are blasted sideways\n"
    "  inner  — from within: little motion; the sprite rots, corrupts or fades in place"
)


class PresetsTab:
    def __init__(self, parent, config: dict, app):
        self.parent = parent
        self.config = config
        self.app = app

        self._scope_var  = tk.StringVar(value="All")
        self._search_var = tk.StringVar()
        # flat list of preset entry dicts matching current filter (parallel to Listbox rows)
        self._filtered: list = []
        self._count_var = tk.StringVar(value="")

        self._build(parent)
        self.refresh(config)

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def _build(self, parent):
        parent.columnconfigure(0, weight=1)

        # --- Section: Preset selector ---
        sel_frame = _tk_ttk.LabelFrame(parent, text="Load Preset", padding=8)
        sel_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=(10, 4))
        sel_frame.columnconfigure(0, weight=1)

        # Preset status label
        self._preset_status_var = tk.StringVar(value="")
        self._preset_status_lbl = tk.Label(
            sel_frame, textvariable=self._preset_status_var,
            font=FONT_SMALL,
            bg=PALETTE["bg_surface"], fg=PALETTE["text_secondary"],
            anchor="w",
        )
        self._preset_status_lbl.grid(row=0, column=0, sticky="ew", pady=(0, 4))

        # Scope toggle (All / Official / Custom)
        scope_row = ttk.Frame(sel_frame)
        scope_row.grid(row=1, column=0, sticky="ew", pady=(0, 4))
        for label in _SCOPE_OPTIONS:
            rb = ttk.Radiobutton(
                scope_row, text=label, value=label,
                variable=self._scope_var,
                bootstyle="primary",
                command=self._on_filter_changed,
            )
            rb.pack(side="left", padx=(0, 8))
        _Tooltip(scope_row,
                 "Filter presets by source.\n\n"
                 "Official = built-in presets (names start with *).\n"
                 "Custom = presets you saved yourself.\n"
                 "All = show both.")
        tk.Label(
            scope_row,
            textvariable=self._count_var,
            font=FONT_SMALL,
            bg=PALETTE["bg_surface"],
            fg=PALETTE["text_secondary"],
        ).pack(side="right", padx=(8, 0))

        # Search entry
        search_row = ttk.Frame(sel_frame)
        search_row.grid(row=2, column=0, sticky="ew", pady=(0, 4))
        search_row.columnconfigure(1, weight=1)
        ttk.Label(search_row, text="Search:", font=FONT_SMALL,
                  bootstyle="secondary").pack(side="left", padx=(0, 4))
        search_entry = ttk.Entry(search_row, textvariable=self._search_var, font=FONT_BODY)
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda e: self._on_filter_changed())
        _Tooltip(search_entry, "Filter presets by name as you type (case-insensitive).\n"
                               "Try a category (fire), a locale (space) or both (fire-burn).")

        # Listbox + scrollbar
        lb_frame = ttk.Frame(sel_frame)
        lb_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 2))
        lb_frame.columnconfigure(0, weight=1)
        sel_frame.rowconfigure(3, weight=1)

        self._listbox = tk.Listbox(
            lb_frame,
            height=11,
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
        self._listbox.grid(row=0, column=0, sticky="nsew")
        lb_scrollbar = ttk.Scrollbar(lb_frame, orient="vertical",
                                     command=self._listbox.yview)
        lb_scrollbar.grid(row=0, column=1, sticky="ns")
        self._listbox.configure(yscrollcommand=lb_scrollbar.set)
        # <<ListboxSelect>> fires on every arrow-key move and would trigger a full
        # preset reload + tab refresh, which rebuilds the listbox and breaks
        # navigation. Use it only for lightweight highlight feedback; load on
        # explicit confirm (click or keyboard Enter/Space).
        self._listbox.bind("<<ListboxSelect>>", self._on_highlight)
        self._listbox.bind("<ButtonRelease-1>", self._on_select)
        self._listbox.bind("<Return>",          self._on_select)
        self._listbox.bind("<space>",           self._on_select)

        _Tooltip(self._listbox,
                 "Click a preset (or press Enter) to load it.\n"
                 "Arrow keys browse descriptions without loading.")

        # Legend: what * means and the naming format
        legend = tk.Label(sel_frame, text=_LEGEND, font=FONT_TINY,
                          bg=PALETTE["bg_surface"], fg=PALETTE["text_secondary"],
                          anchor="w", cursor="question_arrow")
        legend.grid(row=4, column=0, sticky="ew", pady=(0, 6))
        _Tooltip(legend, _TIP_LEGEND)

        # Description text box
        desc_label = ttk.Label(sel_frame, text="Description", font=FONT_SMALL,
                               bootstyle="secondary")
        desc_label.grid(row=5, column=0, sticky="w")

        self._desc_text = tk.Text(
            sel_frame,
            height=3,
            wrap="word",
            font=FONT_SMALL,
            bg=PALETTE["bg_input"],
            fg=PALETTE["text_secondary"],
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=PALETTE["accent_glow"],
            state="disabled",
            cursor="arrow",
        )
        self._desc_text.grid(row=6, column=0, sticky="ew", pady=(2, 0))
        _Tooltip(self._desc_text, "A short summary of what this preset does.")

        # --- Section: Actions (all act on the loaded preset) ---
        act_frame = _tk_ttk.LabelFrame(parent, text="Preset Actions", padding=8)
        act_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(4, 10))
        act_frame.columnconfigure(0, weight=1)
        act_frame.columnconfigure(1, weight=1)

        self._save_btn = ttk.Button(act_frame, text="Save As Copy…", bootstyle="primary",
                                    command=self._on_save_as)
        self._save_btn.grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=2)
        _Tooltip(self._save_btn,
                 "Save your current settings as a new custom preset.\n\n"
                 "Use this to keep your own version of a built-in preset —\n"
                 "the built-in original is never changed.")

        self._revert_btn = ttk.Button(act_frame, text="Revert", bootstyle="secondary",
                                      command=self._on_revert, state="disabled")
        self._revert_btn.grid(row=0, column=1, sticky="ew", padx=(4, 0), pady=2)
        _Tooltip(self._revert_btn,
                 "Throw away your changes and reload the preset as it was saved.\n\n"
                 "Only enabled when you've changed settings since loading it.")

        self._update_btn = ttk.Button(act_frame, text="Save Changes", bootstyle="success",
                                      command=self._on_update, state="disabled")
        self._update_btn.grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=2)
        _Tooltip(self._update_btn,
                 "Overwrite your custom preset with the current settings.\n\n"
                 "Built-in (*) presets can't be overwritten — use Save As Copy instead.")

        self._delete_btn = ttk.Button(act_frame, text="Delete", bootstyle="danger",
                                      command=self._on_delete, state="disabled")
        self._delete_btn.grid(row=1, column=1, sticky="ew", padx=(4, 0), pady=2)
        _Tooltip(self._delete_btn,
                 "Permanently delete the loaded custom preset.\n\n"
                 "Built-in (*) presets can't be deleted.")

        # Save to Source [DEV] — dev builds only
        if DEV_MODE:
            self._save_to_source_btn = ttk.Button(
                act_frame, text="Save to Source [DEV]", bootstyle="warning",
                command=self._on_save_to_source, state="disabled")
            self._save_to_source_btn.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 2))
            _Tooltip(self._save_to_source_btn,
                     "[Developer only — hidden in the exe]\n"
                     "Write the current settings into the loaded built-in preset's\n"
                     "presets/<type>.py entry. Only that entry is rewritten.\n"
                     "Enabled when a built-in preset is loaded and modified.")

        self._rebuild_values()
        self._randomizer_panel = RandomizerPanel(
            parent,
            config=self.config,
            app=self.app,
            notify_dirty_cb=self.notify_dirty,
        )
        self._randomizer_panel.grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 10))

    # ------------------------------------------------------------------ #
    #  Listbox population                                                  #
    # ------------------------------------------------------------------ #

    def _on_filter_changed(self):
        self._rebuild_values()
        self._select_active(scroll=True)

    def _rebuild_values(self):
        import presets
        entries = search_presets(self._search_var.get(), self._scope_var.get().lower())

        self._filtered = entries
        self._listbox.delete(0, "end")
        width = len(str(len(entries)))
        for i, entry in enumerate(entries):
            self._listbox.insert("end", f"{i+1:>{width}}. {entry['name']}")
        total = len(presets.PRESET_LIST) + len(load_user_presets())
        self._count_var.set(f"{len(entries)}/{total} Presets Shown")

    def _select_active(self, scroll=False):
        """Highlight the loaded preset's row if it's in the filtered list; return its entry."""
        active = self.config.get("active_preset")
        self._listbox.selection_clear(0, "end")
        for i, entry in enumerate(self._filtered):
            if entry["name"] == active:
                self._listbox.selection_set(i)
                if scroll:
                    self._listbox.see(i)
                return entry
        return None

    # ------------------------------------------------------------------ #
    #  Event handlers                                                      #
    # ------------------------------------------------------------------ #

    def _on_highlight(self, _event=None):
        sel = self._listbox.curselection()
        if sel:
            self._update_description(self._filtered[sel[0]])

    def _on_select(self, _event=None):
        sel = self._listbox.curselection()
        if not sel:
            return
        self.app.load_preset(self._filtered[sel[0]]["name"])

    def _update_description(self, entry):
        text = entry.get("description", "") if entry else ""
        self._desc_text.configure(state="normal")
        self._desc_text.delete("1.0", "end")
        if text:
            self._desc_text.insert("1.0", text)
        self._desc_text.configure(state="disabled")

    def _update_state(self):
        """Refresh the status line and button states from the loaded preset."""
        active = self.config.get("active_preset")
        entry = get_preset(active) if active else None
        if entry is None:
            active = None
        official = active is not None and is_official_name(active)
        custom = active is not None and not official
        modified = active is not None and is_modified(self.config, active)

        if active is None:
            self._set_status("No preset loaded — manual settings", "neutral")
        elif modified:
            self._set_status(f"Loaded: {active}  (modified)", "dirty")
        else:
            self._set_status(f"Loaded: {active}", "loaded")

        def _state(on):
            return "normal" if on else "disabled"
        self._revert_btn.configure(state=_state(modified))
        self._update_btn.configure(state=_state(custom and modified))
        self._delete_btn.configure(state=_state(custom))
        if DEV_MODE:
            self._save_to_source_btn.configure(state=_state(official and modified))

    def _active_entry(self):
        active = self.config.get("active_preset")
        return get_preset(active) if active else None

    # ------------------------------------------------------------------ #
    #  Small modal dialog helper                                           #
    # ------------------------------------------------------------------ #

    def _dialog(self, title, geometry):
        win = tk.Toplevel(self.app.root)
        win.title(title)
        win.geometry(geometry)
        win.resizable(False, False)
        win.transient(self.app.root)
        win.focus_force()
        self.app._apply_icon(win)
        win.bind("<Escape>", lambda e: win.destroy())
        return win

    def _confirm(self, title, message, sub, confirm_label, confirm_style, on_confirm,
                 geometry="400x150"):
        win = self._dialog(title, geometry)
        ttk.Label(win, text=message, font=FONT_BODY_BOLD, wraplength=370).pack(pady=(18, 4), padx=12)
        ttk.Label(win, text=sub, font=FONT_SMALL, bootstyle="secondary",
                  wraplength=370).pack(pady=(0, 8), padx=12)
        btn_frame = ttk.Frame(win)
        btn_frame.pack()

        def _go():
            win.destroy()
            on_confirm()

        ttk.Button(btn_frame, text=confirm_label, bootstyle=confirm_style,
                   command=_go).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Cancel", bootstyle="secondary",
                   command=win.destroy).pack(side="left", padx=6)
        return win

    # ------------------------------------------------------------------ #
    #  Save As Copy                                                        #
    # ------------------------------------------------------------------ #

    def _on_save_as(self):
        entry = self._active_entry()
        default_name = f"{display_stem(entry['name'])}-copy" if entry else ""
        default_desc = entry.get("description", "") if entry else ""

        win = self._dialog("Save As Copy", "420x230")
        win.columnconfigure(1, weight=1)

        ttk.Label(win, text="Name:", font=FONT_BODY).grid(
            row=0, column=0, sticky="w", padx=(12, 6), pady=(16, 4))
        name_var = tk.StringVar(value=default_name)
        name_entry = ttk.Entry(win, textvariable=name_var, font=FONT_BODY)
        name_entry.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=(16, 4))
        self.app.attach_context_menu(name_entry)

        ttk.Label(win, text="Description:", font=FONT_BODY).grid(
            row=1, column=0, sticky="w", padx=(12, 6), pady=4)
        desc_var = tk.StringVar(value=default_desc)
        desc_entry = ttk.Entry(win, textvariable=desc_var, font=FONT_BODY)
        desc_entry.grid(row=1, column=1, sticky="ew", padx=(0, 12), pady=4)
        self.app.attach_context_menu(desc_entry)

        msg_lbl = tk.Label(win, text="", font=FONT_SMALL, fg=PALETTE["danger"],
                           bg=PALETTE["bg_base"], wraplength=390, justify="left", anchor="w")
        msg_lbl.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=(2, 0))

        btn_frame = ttk.Frame(win)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 8))
        confirmed_overwrite = {"name": None}

        def _save():
            name = name_var.get().strip()
            error = validate_custom_name(name)
            if error:
                msg_lbl.configure(text=error)
                return
            if custom_preset_exists(name) and confirmed_overwrite["name"] != name:
                confirmed_overwrite["name"] = name
                msg_lbl.configure(text=f'You already have a preset called "{name}". '
                                       "Click Overwrite to replace it.")
                save_btn.configure(text="Overwrite", bootstyle="danger")
                return
            try:
                save_user_preset_from_config(name, desc_var.get().strip(), self.config)
            except Exception as exc:
                log.exception("Saving custom preset %r failed", name)
                msg_lbl.configure(text=f"Could not save: {short_reason(exc)}")
                return
            win.destroy()
            self.config["active_preset"] = name
            self.app.save_config()
            self._after_change(scroll=True)

        def _on_name_edit(*_):
            if confirmed_overwrite["name"] is not None:
                confirmed_overwrite["name"] = None
                save_btn.configure(text="Save", bootstyle="primary")
            msg_lbl.configure(text="")
        name_var.trace_add("write", _on_name_edit)

        save_btn = ttk.Button(btn_frame, text="Save", bootstyle="primary", command=_save)
        save_btn.pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Cancel", bootstyle="secondary",
                   command=win.destroy).pack(side="left", padx=6)

        name_entry.focus_set()
        name_entry.select_range(0, "end")
        win.bind("<Return>", lambda e: _save())

    # ------------------------------------------------------------------ #
    #  Revert / Save Changes / Delete                                      #
    # ------------------------------------------------------------------ #

    def _on_revert(self):
        active = self.config.get("active_preset")
        if active:
            self.app.load_preset(active)

    def _on_update(self):
        entry = self._active_entry()
        if entry is None or is_official_name(entry["name"]):
            return
        try:
            save_user_preset_from_config(entry["name"], entry.get("description", ""), self.config)
        except Exception as exc:
            log.exception("Saving custom preset %r failed", entry["name"])
            self.app.show_error("Save failed", f'Could not save "{entry["name"]}":\n\n{short_reason(exc)}')
            return
        self._after_change()

    def _on_delete(self):
        entry = self._active_entry()
        if entry is None or is_official_name(entry["name"]):
            return
        name = entry["name"]

        def _do_delete():
            delete_user_preset(name)
            self.config["active_preset"] = None
            self.app.save_config()
            self._after_change()

        self._confirm("Delete Preset", f'Delete preset "{name}"?', "This cannot be undone.",
                      "Delete", "danger", _do_delete)

    # ------------------------------------------------------------------ #
    #  Save to Source [DEV]                                                #
    # ------------------------------------------------------------------ #

    def _on_save_to_source(self):
        if not DEV_MODE:
            return
        entry = self._active_entry()
        if entry is None or not is_official_name(entry["name"]):
            return
        name = entry["name"]

        from utils.presets_io import save_official_preset_to_source, preset_source_path
        py_filename = f"presets/{preset_source_path(name).name}"

        def _do_save():
            try:
                save_official_preset_to_source(name, self.config)
            except Exception as exc:
                log.exception("Save to Source failed for %s", name)
                self.app.show_error("Save to Source failed", f"{name}\n\n{short_reason(exc)}")
                return
            self._after_change()
            self._set_status(f"Saved {name} to {py_filename}", "loaded")

        self._confirm("Save to Source [DEV]", f"Overwrite {name} in {py_filename}?",
                      "Only this preset's entry is rewritten; the rest of the file is untouched.",
                      "Overwrite", "warning", _do_save, geometry="440x150")

    # ------------------------------------------------------------------ #
    #  Refresh (called by app._refresh_all_tabs after preset load)        #
    # ------------------------------------------------------------------ #

    def _after_change(self, scroll=False):
        """Re-list presets and re-sync selection/description/buttons after a save or delete."""
        self._rebuild_values()
        self._update_description(self._select_active(scroll=scroll))
        self._update_state()

    def refresh(self, config):
        self.config = config
        # Preserve scroll position across rebuilds so clicking a preset doesn't
        # shift the list and disorient the user while auditing presets.
        scroll_top = self._listbox.yview()[0] if self._listbox.size() else 0.0
        self._rebuild_values()
        matched_entry = self._select_active()
        # Restore scroll position; only scroll to show the item if it would be
        # completely off-screen (i.e. the user has navigated away from that region).
        self._listbox.yview_moveto(scroll_top)
        sel = self._listbox.curselection()
        if sel:
            idx = sel[0]
            first_visible = int(self._listbox.yview()[0] * self._listbox.size())
            last_visible  = int(self._listbox.yview()[1] * self._listbox.size())
            if idx < first_visible or idx >= last_visible:
                self._listbox.see(idx)
        self._update_description(matched_entry)
        self._update_state()

        self._randomizer_panel.refresh(config)

    def notify_dirty(self, dirty: bool):
        self._update_state()

    def notify_preview_updated(self):
        self._update_state()

    def _set_status(self, text: str, kind: str):
        self._preset_status_var.set(text)
        if kind == "loaded":
            self._preset_status_lbl.configure(fg=PALETTE["success"])
        elif kind == "dirty":
            self._preset_status_lbl.configure(fg=PALETTE["warning"])
        else:
            self._preset_status_lbl.configure(fg=PALETTE["text_secondary"])
