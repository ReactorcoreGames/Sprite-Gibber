import random
import tkinter as tk
import tkinter.ttk as _tk_ttk

import ttkbootstrap as ttk

from gui.theme import PALETTE, FONT_BODY, FONT_SMALL, FONT_MONO, Tooltip as _Tooltip
from gui.widgets.direction_widget import DirectionStrengthWidget
from gui.widgets.controls import MoreOptions, choice_combo, slider_row
from utils.config import DEFAULT_CONFIG

_BLAST_OPTIONS = [
    "explode",
    "implode",
    "hollow_circle",
    "filled_circle",
    "shatter",
    "burst",
    "x_split",
    "vertical_split",
    "horizontal_split",
]

_BLAST_TOOLTIP = (
    "Explode — chunks burst outward from center\n"
    "Implode — chunks fly inward toward center\n"
    "Hollow circle — ring of outward velocity\n"
    "Filled circle — circular outward burst\n"
    "Shatter — random micro-velocity in all directions\n"
    "Burst — each chunk gets a random outward direction (uniform push, central chunks move too)\n"
    "X split — diagonal X split outward\n"
    "Vertical split — left/right split\n"
    "Horizontal split — up/down split"
)

_GRAVITY_MODE_OPTIONS = ["directional", "centripetal", "repulsor", "orbital", "vortex", "noise"]

_GRAVITY_MODE_TOOLTIP = (
    "Directional — gravity pulls chunks toward a canvas edge (set by Angle above)\n"
    "Centripetal  — pulls every chunk toward sprite center; chunks converge and settle.\n"
    "               Gravity Angle ignored.\n"
    "Repulsor     — pushes every chunk away from sprite center indefinitely.\n"
    "               Gravity Angle ignored.\n"
    "Orbital      — tangential force only; chunks orbit center in an outward spiral.\n"
    "               Gravity Angle ignored.\n"
    "Vortex       — centripetal pull + tangential force; chunks spiral inward and\n"
    "               settle at center. Gravity Angle ignored.\n"
    "Noise        — each chunk drifts in a slowly-varying random direction independently.\n"
    "               Organic gas/goo movement. Gravity Angle ignored."
)


class PhysicsTab:
    def __init__(self, parent, config: dict, app):
        self.config = config
        self.app = app

        # --- tk.Vars ---
        self._chunks_var          = tk.IntVar(value=config.get("CHUNKS", 16))
        self._single_chunk_var    = tk.BooleanVar(value=config.get("SINGLE_CHUNK", False))
        self._chunk_bias_var      = tk.StringVar(value=config.get("CHUNK_BIAS", "none"))
        self._chunk_bias_str_var  = tk.DoubleVar(value=config.get("CHUNK_BIAS_STRENGTH", 0.0))
        self._chunk_stretch_var   = tk.DoubleVar(value=config.get("CHUNK_SHAPE_STRETCH", 1.0))
        self._chunk_angle_var     = tk.IntVar(value=config.get("CHUNK_SHAPE_ANGLE", 0))
        self._blast_var           = tk.StringVar(value=config.get("BLAST_MODE", "explode"))
        self._explode_var       = tk.DoubleVar(value=config.get("EXPLODE", 2.5))
        self._drag_var          = tk.DoubleVar(value=config.get("DRAG", 0.18))
        self._spread_var        = tk.DoubleVar(value=config.get("SPREAD", 1.2))
        self._spin_var          = tk.IntVar(value=config.get("SPIN", 8))
        self._spin_drag_var     = tk.DoubleVar(value=config.get("SPIN_DRAG", 0.0))
        self._mass_variance_var = tk.DoubleVar(value=config.get("CHUNK_MASS_VARIANCE", 0.0))
        self._bounce_var        = tk.DoubleVar(value=config.get("BOUNCE", 0.0))
        self._stagger_var       = tk.DoubleVar(value=config.get("LAUNCH_STAGGER", 0.0))
        self._edge_zone_var     = tk.IntVar(value=config.get("EDGE_ZONE", 6))
        self._max_ticks_var     = tk.IntVar(value=config.get("MAX_SIM_TICKS", 500))
        self._angle_var         = tk.IntVar(value=config.get("GRAVITY_ANGLE", 180))
        self._strength_var      = tk.DoubleVar(value=config.get("GRAVITY_STRENGTH", 1.2))
        self._gravity_mode_var  = tk.StringVar(value=config.get("GRAVITY_MODE", "directional"))
        self._gravity_ramp_var  = tk.IntVar(value=config.get("GRAVITY_RAMP_TICKS", 0))
        self._seed_var          = tk.StringVar(value=str(config.get("SEED", 42)))

        self._build(parent)

    # ------------------------------------------------------------------ #
    #  Build                                                               #
    # ------------------------------------------------------------------ #

    def _build(self, parent):
        parent.columnconfigure(0, weight=1)

        self._build_chunks_blast(parent, row=0)
        self._build_velocity(parent, row=1)
        self._build_gravity(parent, row=2)
        self._build_seed(parent, row=3)

    # --- Section 1: Chunks & Blast ---

    def _build_chunks_blast(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Chunks & Blast Mode", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=(10, 4))
        frame.columnconfigure(0, weight=1)

        _chunks_default = DEFAULT_CONFIG.get("CHUNKS", 16)
        self._add_int_slider(
            frame, row=0,
            label="Chunks", var=self._chunks_var,
            from_=2, to=200, key="CHUNKS", limits=(2, 1000),
            tooltip=(
                f"How many pieces the sprite is split into (default: {_chunks_default}).\n\n"
                "Fewer chunks = big chunky gibs. More chunks = fine shrapnel.\n"
                "8–64 is a good range for most pixel art sprites.\n"
                "The slider goes to 200; type a number (up to 1000) for more.\n"
                "Ignored when Single Chunk is enabled."
            ),
        )

        # Single chunk checkbox
        _SINGLE_CHUNK_TOOLTIP = (
            "Treat the entire sprite as one piece instead of splitting it into chunks.\n\n"
            "Tint, dissolve, and physics (gravity, drag, spin) all apply normally.\n"
            "Useful for statue-fall, Midas touch, or slow-drift-into-shadow effects.\n"
            "Blast Mode is less meaningful here (no centroid geometry) but still gives\n"
            "the whole sprite a directional launch kick."
        )
        sc_row = ttk.Frame(frame)
        sc_row.grid(row=1, column=0, sticky="w", pady=(4, 2))
        sc_cb = ttk.Checkbutton(
            sc_row,
            text="Single Chunk",
            variable=self._single_chunk_var,
            bootstyle="round-toggle",
            command=lambda: self._save("SINGLE_CHUNK", bool(self._single_chunk_var.get())),
        )
        sc_cb.grid(row=0, column=0, sticky="w")
        _Tooltip(sc_cb, _SINGLE_CHUNK_TOOLTIP)

        # Blast mode row
        blast_row = ttk.Frame(frame)
        blast_row.grid(row=2, column=0, sticky="ew", pady=(6, 2))
        blast_row.columnconfigure(1, weight=1)

        blast_lbl = ttk.Label(blast_row, text="Blast Mode", font=FONT_BODY,
                              background=PALETTE["bg_surface"])
        blast_lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
        _Tooltip(blast_lbl, _BLAST_TOOLTIP)

        self._blast_combo = choice_combo(
            blast_row, self._blast_var, _BLAST_OPTIONS,
            lambda e: self._save("BLAST_MODE", self._blast_var.get()), width=16,
        )
        self._blast_combo.grid(row=0, column=1, sticky="w")
        _Tooltip(self._blast_combo, _BLAST_TOOLTIP)

        # Chunk shape controls are advanced: collapsed unless a preset uses them
        self._chunk_more = MoreOptions(
            frame, ["CHUNK_BIAS", "CHUNK_BIAS_STRENGTH", "CHUNK_SHAPE_STRETCH", "CHUNK_SHAPE_ANGLE"],
            text="Chunk shape options")
        self._chunk_more.grid(row=3, column=0, sticky="ew")
        more = self._chunk_more.body

        # Chunk Bias combobox
        _BIAS_OPTIONS = ["none", "halves-h", "halves-v", "core", "shell", "quadrants"]
        _BIAS_TOOLTIP = (
            "Controls where Voronoi seed points are drawn from, giving structural coherence to chunks.\n\n"
            "None — fully random (default)\n"
            "Halves (top / bottom) — seeds split evenly into top and bottom halves\n"
            "Halves (left / right) — seeds split evenly into left and right halves\n"
            "Quadrants — seeds distributed across all four corner regions\n"
            "Core — seeds concentrated toward the sprite centroid\n"
            "Shell — seeds concentrated toward the sprite edges\n\n"
            "Use Bias Strength to blend between random and strict zone placement.\n"
            "Ignored when Single Chunk is enabled."
        )
        _BIAS_STR_TOOLTIP = (
            "How strongly seed placement follows the chosen Chunk Bias zone.\n\n"
            "0.0 = fully random seeds (Chunk Bias has no effect)\n"
            "1.0 = strict zone enforcement\n"
            "Values in between blend zone-biased and random pools.\n"
            "Ignored when Chunk Bias is None."
        )

        bias_row = ttk.Frame(more)
        bias_row.grid(row=0, column=0, sticky="ew", pady=(2, 2))
        bias_row.columnconfigure(1, weight=1)

        bias_lbl = ttk.Label(bias_row, text="Chunk Bias", font=FONT_BODY,
                             background=PALETTE["bg_surface"])
        bias_lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
        _Tooltip(bias_lbl, _BIAS_TOOLTIP)

        self._bias_combo = choice_combo(
            bias_row, self._chunk_bias_var, _BIAS_OPTIONS, self._on_bias_changed, width=20,
        )
        self._bias_combo.grid(row=0, column=1, sticky="w")
        _Tooltip(self._bias_combo, _BIAS_TOOLTIP)

        # Bias Strength slider
        _f, self._bias_str_slider, self._bias_str_readout, self._bias_str_lbl = self._add_float_slider(
            more, row=1, label="Bias Strength", var=self._chunk_bias_str_var,
            from_=0.0, to=1.0, dp=2, key="CHUNK_BIAS_STRENGTH",
            tooltip=_BIAS_STR_TOOLTIP,
        )

        self._update_bias_strength_state()

        # Shape Stretch slider
        _STRETCH_TOOLTIP = (
            "Stretches the Voronoi distance metric along an axis, making chunks elongate into slivers or strips.\n\n"
            "1.0 = standard round/blobby chunks (default)\n"
            "Higher values = longer, thinner chunks along the Stretch Angle direction\n"
            "Works independently of Chunk Bias."
        )
        _ANGLE_TOOLTIP = (
            "Direction the chunks elongate, in degrees.\n\n"
            "0 = vertical slivers\n"
            "90 = horizontal strips\n"
            "45 = diagonal shards\n"
            "Ignored when Shape Stretch is 1.0."
        )
        self._add_float_slider(
            more, row=2, label="Shape Stretch", var=self._chunk_stretch_var,
            from_=1.0, to=10.0, dp=1, key="CHUNK_SHAPE_STRETCH",
            tooltip=_STRETCH_TOOLTIP,
        )
        self._add_int_slider(
            more, row=3, label="Stretch Angle", var=self._chunk_angle_var,
            from_=0, to=359, key="CHUNK_SHAPE_ANGLE",
            tooltip=_ANGLE_TOOLTIP,
        )

    def _on_bias_changed(self, event=None):
        self._save("CHUNK_BIAS", self._chunk_bias_var.get())
        self._update_bias_strength_state()

    def _update_bias_strength_state(self):
        is_none = self._chunk_bias_var.get() == "none"
        state = "disabled" if is_none else "normal"
        self._bias_str_slider.configure(state=state)
        self._bias_str_lbl.configure(state=state)
        self._bias_str_readout.configure(state=state)

    # --- Section 2: Velocity & Motion ---

    def _build_velocity(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Chunk Velocity & Motion", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=4)
        frame.columnconfigure(0, weight=1)

        _explode_default       = DEFAULT_CONFIG.get("EXPLODE", 2.5)
        _drag_default          = DEFAULT_CONFIG.get("DRAG", 0.18)
        _spread_default        = DEFAULT_CONFIG.get("SPREAD", 1.2)
        _spin_default          = DEFAULT_CONFIG.get("SPIN", 8)
        _spin_drag_default     = DEFAULT_CONFIG.get("SPIN_DRAG", 0.0)
        _mass_var_default      = DEFAULT_CONFIG.get("CHUNK_MASS_VARIANCE", 0.0)
        _bounce_default        = DEFAULT_CONFIG.get("BOUNCE", 0.0)
        _stagger_default       = DEFAULT_CONFIG.get("LAUNCH_STAGGER", 0.0)
        _edge_default          = DEFAULT_CONFIG.get("EDGE_ZONE", 6)
        _ticks_default         = DEFAULT_CONFIG.get("MAX_SIM_TICKS", 500)

        self._motion_more = MoreOptions(
            frame, ["SPIN_DRAG", "CHUNK_MASS_VARIANCE", "LAUNCH_STAGGER", "EDGE_ZONE", "MAX_SIM_TICKS"],
            text="More motion options")
        self._motion_more.grid(row=5, column=0, sticky="ew")
        more = self._motion_more.body

        self._add_float_slider(
            frame, row=0, label="Explode", var=self._explode_var,
            from_=0.0, to=10.0, dp=1, key="EXPLODE", limits=(0.0, 20.0),
            tooltip=(
                f"How fast chunks fly outward when the sprite explodes (default: {_explode_default}).\n\n"
                "0 = no outward push at all. Higher values = more violent, faster separation."
            ),
        )
        self._add_float_slider(
            frame, row=1, label="Drag", var=self._drag_var,
            from_=0.0, to=0.50, dp=2, key="DRAG", limits=(0.0, 1.0),
            tooltip=(
                f"Air resistance — how quickly chunks slow down each tick (default: {_drag_default}).\n\n"
                "0 = no slowdown (chunks coast forever). Higher values = chunks decelerate quickly after launch."
            ),
        )
        self._add_float_slider(
            frame, row=2, label="Spread", var=self._spread_var,
            from_=0.0, to=3.0, dp=2, key="SPREAD", limits=(0.0, 5.0),
            tooltip=(
                f"How randomly the launch angle varies per chunk (default: {_spread_default}).\n\n"
                "0 = all chunks fly in a perfectly uniform pattern. Higher values add chaotic, jittery directions."
            ),
        )
        self._add_int_slider(
            frame, row=3, label="Spin", var=self._spin_var,
            from_=0, to=40, key="SPIN", limits=(0, 180),
            tooltip=(
                f"Maximum rotation speed of each chunk in degrees per tick (default: {_spin_default}).\n\n"
                "0 = no rotation. Each chunk gets a random spin up to this value."
            ),
        )
        self._add_float_slider(
            more, row=0, label="Spin Drag", var=self._spin_drag_var,
            from_=0.0, to=0.5, dp=2, key="SPIN_DRAG", limits=(0.0, 1.0),
            tooltip=(
                f"How quickly each chunk's rotation slows down over time (default: {_spin_drag_default}).\n\n"
                "0 = spin stays constant throughout. 1 = rotation stops almost immediately.\n"
                "Useful for debris that tumbles wildly at first then settles flat."
            ),
        )
        self._add_float_slider(
            more, row=1, label="Mass Variance", var=self._mass_variance_var,
            from_=0.0, to=1.0, dp=2, key="CHUNK_MASS_VARIANCE",
            tooltip=(
                f"Random weight difference between chunks (default: {_mass_var_default}).\n\n"
                "0 = all chunks decelerate identically. Higher values make lighter chunks drift\n"
                "further while heavier ones drop sooner. Unlocks ash, sand, and debris effects."
            ),
        )
        self._add_float_slider(
            frame, row=4, label="Bounce", var=self._bounce_var,
            from_=0.0, to=1.0, dp=2, key="BOUNCE",
            tooltip=(
                f"How much velocity chunks retain after hitting the settle plane (default: {_bounce_default}).\n\n"
                "0 = dead stop on landing (current default). 1 = perfectly elastic bounce.\n"
                "Great for frozen shatter clatter, rocky debris, ricocheting fragments."
            ),
        )
        self._add_float_slider(
            more, row=2, label="Launch Stagger", var=self._stagger_var,
            from_=0.0, to=1.0, dp=2, key="LAUNCH_STAGGER",
            tooltip=(
                f"Spreads chunk launch times across the simulation (default: {_stagger_default}).\n\n"
                "0 = all chunks launch simultaneously. 1 = chunks launch sequentially across\n"
                "the full simulation span. Great for crumble, cascading disintegration effects."
            ),
        )
        self._add_int_slider(
            more, row=3, label="Edge Zone", var=self._edge_zone_var,
            from_=0, to=32, key="EDGE_ZONE", limits=(0, 200),
            tooltip=(
                f"Width in pixels of the invisible zone near canvas edges where chunks slow down (default: {_edge_default}).\n\n"
                "Stops chunks from flying off-canvas. 0 = no edge damping (chunks can slam right to the wall).\n"
                "Scale with your sprite — roughly 15–20% of canvas width works well\n"
                "(e.g. 6 for 32 px, 25 for 128 px, 50 for 256 px)."
            ),
        )
        self._add_int_slider(
            more, row=4, label="Max Simulation Steps", var=self._max_ticks_var,
            from_=50, to=1000, key="MAX_SIM_TICKS", limits=(50, 2000),
            tooltip=(
                f"Hard limit on how many physics steps are simulated before stopping (default: {_ticks_default}).\n\n"
                "Normally the simulation stops automatically once all chunks have settled. "
                "This cap prevents infinite loops in zero-gravity or unusual setups where chunks never fully settle."
            ),
        )

    # --- Section 3: Gravity ---

    def _build_gravity(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Gravity", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=(4, 10))
        frame.columnconfigure(0, weight=1)

        # Direction widget centred
        dial = DirectionStrengthWidget(
            frame,
            angle_var=self._angle_var,
            strength_var=self._strength_var,
        )
        dial.grid(row=0, column=0, pady=(4, 8))
        _Tooltip(dial,
                 "Drag the dot to set gravity direction and strength visually.\n"
                 "The dot's angle sets which way chunks fall; distance from centre sets pull strength.")

        _angle_default    = DEFAULT_CONFIG.get("GRAVITY_ANGLE", 180)
        _strength_default = DEFAULT_CONFIG.get("GRAVITY_STRENGTH", 1.2)

        self._add_int_slider(
            frame, row=1,
            label="Angle", var=self._angle_var,
            from_=0, to=360, key="GRAVITY_ANGLE",
            tooltip=(
                f"Direction gravity pulls chunks, in degrees (default: {_angle_default}).\n\n"
                "0 = up, 90 = right, 180 = down, 270 = left. "
                "Chunks pile against whichever canvas edge this points toward."
            ),
        )
        self._add_float_slider(
            frame, row=2,
            label="Strength", var=self._strength_var,
            from_=0.0, to=5.0, dp=1, key="GRAVITY_STRENGTH", limits=(0.0, 10.0),
            tooltip=(
                f"How strongly gravity pulls chunks toward the settle edge, in pixels per tick² (default: {_strength_default}).\n\n"
                "0 = zero gravity — chunks drift and never settle (simulation runs until Max Simulation Steps)."
            ),
        )

        # Gravity Mode combobox
        gmode_row = ttk.Frame(frame)
        gmode_row.grid(row=3, column=0, sticky="ew", pady=(6, 2))
        gmode_row.columnconfigure(1, weight=1)

        gmode_lbl = ttk.Label(gmode_row, text="Gravity Mode", font=FONT_BODY,
                              background=PALETTE["bg_surface"])
        gmode_lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
        _Tooltip(gmode_lbl, _GRAVITY_MODE_TOOLTIP)

        self._gravity_mode_combo = choice_combo(
            gmode_row, self._gravity_mode_var, _GRAVITY_MODE_OPTIONS,
            lambda e: self._save("GRAVITY_MODE", self._gravity_mode_var.get()), width=14,
        )
        self._gravity_mode_combo.grid(row=0, column=1, sticky="w")
        _Tooltip(self._gravity_mode_combo, _GRAVITY_MODE_TOOLTIP)

        _ramp_default = DEFAULT_CONFIG.get("GRAVITY_RAMP_TICKS", 0)
        self._gravity_more = MoreOptions(frame, ["GRAVITY_RAMP_TICKS"], text="More gravity options")
        self._gravity_more.grid(row=4, column=0, sticky="ew")
        self._add_int_slider(
            self._gravity_more.body, row=0,
            label="Gravity Ramp Ticks", var=self._gravity_ramp_var,
            from_=0, to=40, key="GRAVITY_RAMP_TICKS", limits=(0, 200),
            tooltip=(
                f"Free-flight ticks before centripetal / vortex / orbital force activates (default: {_ramp_default}).\n\n"
                "0 = force acts from tick 1.\n"
                "During the ramp window chunks travel freely with no center-relative force and no drag,\n"
                "so the sprite visibly breaks apart before being pulled into the vortex or orbit.\n"
                "Only affects Gravity Mode: centripetal, vortex, orbital.\n"
                "Scale with your sprite — roughly 25% of canvas width works well\n"
                "(e.g. 8 for 32 px, 32 for 128 px, 64 for 256 px)."
            ),
        )

    # --- Section 4: Seed ---

    def _build_seed(self, parent, row):
        frame = _tk_ttk.LabelFrame(parent, text="Physics Randomization Seed", padding=8)
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=(4, 10))
        frame.columnconfigure(1, weight=1)

        _SEED_TOOLTIP = (
            "Controls all randomness in gib generation:\n"
            "  • Voronoi chunk shapes\n"
            "  • Outward velocity direction jitter (Spread)\n"
            "  • Spin rate per chunk\n\n"
            "Same seed + same settings = identical output every time.\n"
            "Change the seed to get a different arrangement of chunks without touching any other settings."
        )

        lbl = ttk.Label(frame, text="Seed", font=FONT_BODY,
                        background=PALETTE["bg_base"])
        lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
        _Tooltip(lbl, _SEED_TOOLTIP)

        seed_entry = ttk.Entry(frame, textvariable=self._seed_var,
                               font=FONT_MONO, width=10)
        seed_entry.grid(row=0, column=1, sticky="w", padx=(0, 6))
        self.app.attach_context_menu(seed_entry)
        _Tooltip(seed_entry, _SEED_TOOLTIP)

        def _save_seed(e=None):
            try:
                v = int(self._seed_var.get())
            except (ValueError, tk.TclError):
                v = 42
            self._seed_var.set(str(v))
            self._save("SEED", v)

        seed_entry.bind("<FocusOut>", _save_seed)
        seed_entry.bind("<Return>",   _save_seed)

        rand_seed_btn = ttk.Button(frame, text="Randomize",
                                   command=self._randomize_seed)
        rand_seed_btn.grid(row=0, column=2, padx=(0, 2))
        _Tooltip(rand_seed_btn,
                 "Pick a new random seed number.\n"
                 "This gives you a different chunk layout and velocity jitter without changing any other settings.")

    def _randomize_seed(self):
        v = random.randint(0, 2 ** 31 - 1)
        self._seed_var.set(str(v))
        self._save("SEED", v)

    # ------------------------------------------------------------------ #
    #  Slider helpers                                                      #
    # ------------------------------------------------------------------ #

    def _add_int_slider(self, parent, row, label, var, from_, to, key, tooltip=None,
                        limits=None):
        return slider_row(
            parent, row, label, var, from_, to,
            commit=lambda k=key, v=var: self._save(k, int(v.get())),
            limits=limits, default=DEFAULT_CONFIG.get(key),
            tooltip=tooltip, tooltip_cls=_Tooltip)

    def _add_float_slider(self, parent, row, label, var, from_, to, dp, key, tooltip=None,
                          limits=None):
        return slider_row(
            parent, row, label, var, from_, to,
            commit=lambda k=key, v=var, d=dp: self._save(k, round(float(v.get()), d)),
            dp=dp, limits=limits, default=DEFAULT_CONFIG.get(key),
            tooltip=tooltip, tooltip_cls=_Tooltip)

    # ------------------------------------------------------------------ #
    #  Save / refresh                                                      #
    # ------------------------------------------------------------------ #

    def _save(self, key, value):
        self.config[key] = value
        self.app.save_config()
        self.app.mark_preview_dirty()

    def refresh(self, config):
        self.config = config
        self._chunks_var.set(config.get("CHUNKS", 16))
        self._single_chunk_var.set(config.get("SINGLE_CHUNK", False))
        self._chunk_bias_var.set(config.get("CHUNK_BIAS", "none"))
        self._chunk_bias_str_var.set(config.get("CHUNK_BIAS_STRENGTH", 0.0))
        self._chunk_stretch_var.set(config.get("CHUNK_SHAPE_STRETCH", 1.0))
        self._chunk_angle_var.set(config.get("CHUNK_SHAPE_ANGLE", 0))
        self._update_bias_strength_state()
        self._blast_var.set(config.get("BLAST_MODE", "explode"))
        self._explode_var.set(config.get("EXPLODE", 2.5))
        self._drag_var.set(config.get("DRAG", 0.18))
        self._spread_var.set(config.get("SPREAD", 1.2))
        self._spin_var.set(config.get("SPIN", 8))
        self._spin_drag_var.set(config.get("SPIN_DRAG", 0.0))
        self._mass_variance_var.set(config.get("CHUNK_MASS_VARIANCE", 0.0))
        self._bounce_var.set(config.get("BOUNCE", 0.0))
        self._stagger_var.set(config.get("LAUNCH_STAGGER", 0.0))
        self._edge_zone_var.set(config.get("EDGE_ZONE", 6))
        self._max_ticks_var.set(config.get("MAX_SIM_TICKS", 500))
        self._angle_var.set(config.get("GRAVITY_ANGLE", 180))
        self._strength_var.set(config.get("GRAVITY_STRENGTH", 1.2))
        self._gravity_mode_var.set(config.get("GRAVITY_MODE", "directional"))
        self._gravity_ramp_var.set(config.get("GRAVITY_RAMP_TICKS", 0))
        self._seed_var.set(str(config.get("SEED", 42)))
        for more in (self._chunk_more, self._motion_more, self._gravity_more):
            more.sync(config)
