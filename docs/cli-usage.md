# Sprite Gibber — CLI Usage

This covers the non-GUI batch entry point, `main_cli.py`. It's for scripted or automated
use (e.g. calling it from a build pipeline or another tool) — most people should just use
the GUI (`main.py`), which is what the compiled exe launches. This doc isn't bundled with
the Windows exe release; it's here for anyone working from the GitHub source.

## Requirements

Running from source requires Python 3.10+ and the project's dependencies (`numpy`,
`Pillow`). There's no separate CLI-only install — same environment as the GUI.

## Running it

```
python main_cli.py
```

That's the entire interface — there are no command-line flags or arguments. All behavior
is controlled by editing `params.py` before you run it.

## How it works

1. Reads every setting from `params.py` (see below).
2. Scans `INPUT_DIR` (default `input/`) for `.png` files.
3. For each sprite, runs the full gib pipeline (chunking, physics, tint, dissolve, frame mask) and writes results to `OUTPUT_DIR` (default `output/`), into a folder named `<stem>` where `<stem>` is `<sprite name>_<preset name>` (preset name without the leading `*.`), or just `<sprite name>` when `PRESET = None`:
   - numbered frame PNGs (`<stem>_00.png`, `<stem>_01.png`, …; 3 digits past 100 frames)
   - a spritesheet PNG (`<stem>_sheet.png`)
   - an animated GIF (`<stem>.gif`)
4. If `OVERWRITE = False` and a sprite's output folder already exists, that sprite is
   skipped rather than regenerated.

The same RNG seed (`SEED`) is reused for every sprite in the batch, so re-running the
script with unchanged `params.py` values reproduces identical output.

## Configuring a run

Open `params.py` in a text editor. It's a flat list of uppercase constants — the same
parameters documented in this project's `CLAUDE.md` "Key parameters" table and in
`docs/preset-param-reference.md`. Change whichever values you want, save, and run the
script again.

There is no live preview in the CLI path — if you want to see results before committing
to a full batch run, either use the GUI to tune settings first (then copy the values you
like into `params.py`), or just run the CLI against a small `input/` folder and inspect
the output.

## Using a preset from the CLI

`params.py` has a `PRESET` constant at the very top:

```python
PRESET = None  # e.g. "*.Blood-Explode-terra" — set to None for full manual control
```

Set it to any preset name from the built-in library (see `presets/` — one `.py` file per
Main Type, or browse names in the GUI's Presets tab) and every value that preset defines
overrides the manual constants below it at import time:

```python
PRESET = "*.Blood-Explode-terra"
```

Leave the rest of `params.py` as-is; only the keys the preset actually sets get
overridden, everything else falls back to the manual values in the file. Set
`PRESET = None` to go back to pure manual control.

An invalid preset name raises a `KeyError` at startup (from the `_PRESETS[PRESET]` lookup
in `params.py`) rather than silently falling back to manual params — check spelling
(including the leading `*.`) if the script won't start.

## What the CLI does *not* do

- No preset browsing/search — you have to know or look up the exact preset name.
- No custom preset save/load (`user_presets.json` is a GUI-only concept).
- No live preview, scrubber, or zoom.
- No per-sprite parameter overrides — every sprite in `INPUT_DIR` is processed with the
  exact same `params.py` settings in a single run.

If you need any of that, use the GUI instead.

## Headless preset QA (developer tool, not end-user CLI)

`tools/smoke_test_presets.py` is a separate, unrelated script — it doesn't process your
`input/` folder or produce real output. It runs the full pipeline in-memory against the two
test sprites in `tools/test_sprites/` to confirm a preset's parameters don't crash the engine
(see also `tools/preset_metrics.py` and `tools/preset_sheet.py` for visual QA):

```
python tools/smoke_test_presets.py all
python tools/smoke_test_presets.py Fire
python tools/smoke_test_presets.py "*.Blood-Explode-terra"
```

This is a development/QA tool for anyone editing `presets/*.py`, not a way to batch-
generate your own sprites — use `main_cli.py` or the GUI for that.
