# Adding New Parameters — Developer Reference

This document describes the exact pattern for wiring a new parameter end-to-end: from default value through GUI control, config persistence, physics engine, randomizer, and preset system.

## The 7-Stop Flow

Every parameter touches these locations in order:

```
utils/config.py          ← default value
params.py                ← CLI/batch fallback + documentation
gui/tabs/<tab>.py        ← tk.Var + UI control + _save() + refresh()
core/pipeline.py         ← build_params() — automatic, no edit needed (see Step 4)
gui/widgets/randomizer_panel.py  ← randomizer checkbox + logic
core/chunking.py         ← initial velocity (per-chunk, called once)
  or core/physics.py     ← per-tick simulation (gravity, drag, settle)
  or core/rendering.py   ← render-time effects (tint, dissolve)
presets/<type>.py        ← optional override in named presets
```

---

## Step-by-Step Checklist

### Step 1 — `utils/config.py` (DEFAULT_CONFIG)

Add an entry to the `DEFAULT_CONFIG` dict (lines 5–99). The key is the exact string name used everywhere else.

```python
# String enum
"MY_PARAM": "default_value",

# Integer
"MY_INT_PARAM": 16,

# Float
"MY_FLOAT_PARAM": 1.2,

# Boolean
"MY_BOOL_PARAM": False,

# Hex color
"MY_COLOR_PARAM": "#ff0000",
```

---

### Step 2 — `params.py` (CLI/batch documentation)

Add a matching variable. This file is the legacy batch-mode entry point and doubles as human-readable parameter documentation.

```python
MY_PARAM = "default_value"  # "option_a" | "option_b" | "option_c"
```

---

### Step 3 — `gui/tabs/<tab>.py` (GUI control)

Which tab owns the parameter:
- **PhysicsTab** (`gui/tabs/physics.py`) — velocity, gravity, spin, blast, chunks, bounce, mass
- **TintTab** (`gui/tabs/tint.py`) — all `TINT_*` params
- **DissolveTab** (`gui/tabs/dissolve.py`) — all `DISSOLVE_*` params

#### 3a. Declare the `tk.Var` in `__init__`

```python
# String enum
self._my_param_var = tk.StringVar(value=config.get("MY_PARAM", "default_value"))

# Integer slider
self._my_int_var = tk.IntVar(value=config.get("MY_INT_PARAM", 16))

# Float slider
self._my_float_var = tk.DoubleVar(value=config.get("MY_FLOAT_PARAM", 1.2))

# Boolean
self._my_bool_var = tk.BooleanVar(value=config.get("MY_BOOL_PARAM", False))
```

#### 3b. Define options list (string enums only)

Place near the top of the module, alongside other `_*_OPTIONS` lists:

```python
_MY_PARAM_OPTIONS = ["option_a", "option_b", "option_c"]

_MY_PARAM_TOOLTIP = (
    "option_a — describe what it does\n"
    "option_b — describe what it does\n"
    "option_c — describe what it does"
)
```

#### 3c. Build the UI control

The shared controls live in `gui/widgets/controls.py`; use them rather than raw ttk widgets so every tab behaves the same.

**String enum → `choice_combo()`** (shows friendly names, the var keeps the snake_case config value):
```python
row = ttk.Frame(frame)
row.grid(row=N, column=0, sticky="ew", pady=(6, 2))
row.columnconfigure(1, weight=1)

lbl = ttk.Label(row, text="My Param", font=FONT_BODY, background=PALETTE["bg_surface"])
lbl.grid(row=0, column=0, sticky="w", padx=(0, 6))
_Tooltip(lbl, _MY_PARAM_TOOLTIP)

combo = choice_combo(row, self._my_param_var, _MY_PARAM_OPTIONS,
                     lambda e: self._save("MY_PARAM", self._my_param_var.get()), width=14)
combo.grid(row=0, column=1, sticky="w")
_Tooltip(combo, _MY_PARAM_TOOLTIP)
```
Values display as "Option a" automatically; add an entry to `_DISPLAY_OVERRIDES` in `controls.py` if that reads badly. Write tooltips with the display names, not the config values.

**Integer slider → use the tab's `_add_int_slider()` helper** (wraps `controls.slider_row`: slider + typed value box, double-click resets to the `DEFAULT_CONFIG` value):
```python
self._add_int_slider(frame, row=N, label="My Int", var=self._my_int_var,
                     from_=0, to=100, key="MY_INT_PARAM", limits=(0, 1000),
                     tooltip="Describe the parameter here")
```
`from_`/`to` is the slider's travel — keep it to the range people actually use (check what presets use). `limits` is what the typed box accepts; omit it when it equals the slider range.

**Float slider → use the `_add_float_slider()` helper:**
```python
self._add_float_slider(frame, row=N, label="My Float", var=self._my_float_var,
                       from_=0.0, to=2.0, dp=2, key="MY_FLOAT_PARAM",
                       tooltip="Describe the parameter here")
```

**Basic vs. advanced:** controls most users won't touch go in a `MoreOptions(frame, [keys…], text=…)` block (build them into its `.body`) and the tab's `refresh()` calls `.sync(config)` on it — the block opens by itself when a preset sets any of those keys, so nothing a preset uses is hidden.

**Boolean → Checkbutton:**
```python
cb = ttk.Checkbutton(frame, text="My Bool", variable=self._my_bool_var,
                     command=lambda: self._save("MY_BOOL_PARAM", self._my_bool_var.get()))
cb.grid(row=N, column=0, sticky="w")
_Tooltip(cb, "Describe what enabling this does")
```

#### 3d. Add to `refresh()` method

Every tab has a `refresh(config)` method that reloads GUI state from the config dict when the user loads a preset or the config changes. Add a line here:

```python
self._my_param_var.set(config.get("MY_PARAM", "default_value"))
```

---

### Step 4 — `core/pipeline.py` — `build_params()` (no edit needed)

`build_params(cfg)` turns a config dict into the `SimpleNamespace` `p` the engine sees. It copies every uppercase key from `DEFAULT_CONFIG` (overridden by the config), so a new key added in Step 1 reaches the engine automatically — in the GUI preview, GUI batch, CLI, and the `tools/` scripts alike. All of them run the same `core/pipeline.run_sprite()`, so there is exactly one simulation code path.

Only touch `build_params()` if the new param needs normalisation (the way `DISSOLVE_MIN_PCT` converts legacy whole-number percents).

---

### Step 5 — `gui/widgets/randomizer_panel.py` — Randomizer

The Randomizer button fires randomized values for checked parameter groups. To include a new parameter:

#### 5a. Add to options list near the top (string enums only):
```python
_MY_PARAM_OPTIONS = ["option_a", "option_b", "option_c"]
```

#### 5b. Declare a checkbox `BooleanVar` in `__init__`:
```python
self._rand_my_param_var = tk.BooleanVar()
```

#### 5c. Add the key to `GUI_ONLY_KEYS` in `utils/config.py` (so the `rand_*` toggle survives preset switches and is never saved into a preset):
```python
"rand_my_param",
```

#### 5d. Add a checkbox in `_build_randomize()`:
```python
("My Param", self._rand_my_param_var, "rand_my_param", ...),
```

#### 5e. Add randomization logic in `_on_randomize()`:

```python
# String enum
if self._rand_my_param_var.get():
    updates["MY_PARAM"] = random.choice(_MY_PARAM_OPTIONS)

# Integer
if self._rand_my_int_var.get():
    updates["MY_INT_PARAM"] = random.randint(0, 100)

# Float
if self._rand_my_float_var.get():
    updates["MY_FLOAT_PARAM"] = round(random.uniform(0.0, 2.0), 2)

# Boolean
if self._rand_my_bool_var.get():
    updates["MY_BOOL_PARAM"] = random.random() < 0.3  # 30% chance of True

# Color
if self._rand_my_color_var.get():
    updates["MY_COLOR_PARAM"] = "#%06x" % random.randint(0, 0xFFFFFF)
```

#### 5f. Add to `refresh()`:
```python
self._rand_my_param_var.set(config.get("rand_my_param", False))
```

---

### Step 6 — Core engine (implement the logic)

Read the parameter from `p.MY_PARAM` in the appropriate core function.

| Parameter affects... | File | Function |
|---|---|---|
| Initial velocity per chunk | `core/chunking.py` | `initial_velocity()` |
| Per-tick gravity / drag / bounce | `core/physics.py` | `simulate_step()` |
| Tint / color bleeding | `core/rendering.py` | `apply_tint()` |
| Pixel dropout / dissolve | `core/rendering.py` | `build_dissolve_schedule()` |

Pattern:
```python
my_param = p.MY_PARAM

if my_param == "option_a":
    # ...
elif my_param == "option_b":
    # ...
else:
    raise ValueError(f"Unknown MY_PARAM: {my_param!r}")
```

---

### Step 7 — Preset files (optional)

To override the default in a named preset, add the key to its `"params"` dict in `presets/<type>.py`:

```python
{
    "name": "*.Fire-Burn-terra",
    "category": "fire",
    "params": {
        # ... existing params ...
        "MY_PARAM": "option_b",
    },
}
```

Omitting a key from `"params"` means the preset inherits the default from `DEFAULT_CONFIG`.

---

## Parameter Type Quick Reference

| Type | Config value | `tk.Var` | GUI control | Randomizer pattern |
|---|---|---|---|---|
| String enum | `"option_a"` | `StringVar` | `choice_combo()` | `random.choice(list)` |
| Integer | `16` | `IntVar` | `_add_int_slider()` | `random.randint(min, max)` |
| Float | `1.2` | `DoubleVar` | `_add_float_slider()` | `round(random.uniform(min, max), dp)` |
| Boolean | `False` | `BooleanVar` | `Checkbutton` | `random.random() < prob` |
| Hex color | `"#ff0000"` | `StringVar` | Color picker widget | `"#%06x" % random.randint(0, 0xFFFFFF)` |
| Integer (text entry) | `42` | `StringVar` (converted) | `Entry` field | `random.randint(0, 2**31-1)` |

---

## Key File Locations

| Task | File | Approx. lines |
|---|---|---|
| Define default values | `utils/config.py` | 5–99 |
| CLI/batch parameter docs | `params.py` | 1–77 |
| Physics tab GUI | `gui/tabs/physics.py` | full file |
| Tint tab GUI | `gui/tabs/tint.py` | full file |
| Dissolve tab GUI | `gui/tabs/dissolve.py` | full file |
| Build `p` SimpleNamespace | `core/pipeline.py` | `build_params()` |
| Run the whole pipeline (all callers) | `core/pipeline.py` | `run_sprite()` |
| Randomizer logic | `gui/widgets/randomizer_panel.py` | full file |
| Initial velocity (blast/explode) | `core/chunking.py` | 124–191 |
| Per-tick physics | `core/physics.py` | `simulate_step()` |
| Tint + dissolve render | `core/rendering.py` | `apply_tint()`, `build_dissolve_schedule()` |
| Preset aggregator | `presets/__init__.py` | 1–33 |
| Preset example | `presets/fire.py` | 2–30 |
