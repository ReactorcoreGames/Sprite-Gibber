import os
import sys

import params as _params_mod
from core.output import export_stem
from core.pipeline import build_params, process_sprite_file


def _build_params():
    """Snapshot all uppercase names from the params module into an engine params namespace."""
    return build_params(
        {k: getattr(_params_mod, k) for k in dir(_params_mod) if k.isupper()}
    )


def main():
    if len(sys.argv) > 1:
        # No CLI flags exist — everything comes from params.py. Refuse rather than
        # silently running a full batch over input/ -> output/.
        print("Usage: python main_cli.py   (takes no arguments; edit params.py to configure)")
        sys.exit(1)
    p = _build_params()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir  = os.path.join(script_dir, p.INPUT_DIR)
    output_dir = os.path.join(script_dir, p.OUTPUT_DIR)

    png_files = sorted(
        f for f in os.listdir(input_dir) if f.lower().endswith(".png")
    )
    if not png_files:
        print(f"No PNG files found in '{input_dir}'.")
        return

    preset = getattr(_params_mod, "PRESET", None)
    effect = preset.lstrip("*").lstrip(".") if preset else None

    print(f"Found {len(png_files)} sprites. Processing...")
    for fname in png_files:
        stem = export_stem(os.path.splitext(fname)[0], effect)
        img_path = os.path.join(input_dir, fname)
        out_dir  = os.path.join(output_dir, stem)
        if not p.OVERWRITE and os.path.isdir(out_dir):
            print(f"  Skipping (already exists): {fname}")
            continue
        print(f"  {fname} -> {out_dir}/")
        if not process_sprite_file(img_path, out_dir, stem, p):
            print(f"  Skipping (no opaque pixels): {fname}")

    print("Done.")


if __name__ == "__main__":
    main()
