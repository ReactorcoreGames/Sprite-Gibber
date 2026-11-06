"""Rebuild the customer-facing preset catalog in promo/Full Preset Catalog Reference/.

One clean contact sheet per Main Type (each presets/<type>.py module), named
<Type>-_01.png (_02... if a type outgrows one sheet), via preset_sheet.py
--every 2 --per-sheet 20 --clean. Grouped by module, not name prefix, and checked to
cover every preset exactly once. Existing sheets of the same name are replaced.

Usage:
    python tools/preset_catalog.py
"""
import collections
import glob
import importlib
import os
import pkgutil
import subprocess
import sys
import tempfile

from _preset_tools import ROOT

import presets

OUT = os.path.join(ROOT, "promo", "Full Preset Catalog Reference")


def module_presets(mod):
    return [p["name"] for v in vars(mod).values()
            if isinstance(v, list) and v and isinstance(v[0], dict) and "name" in v[0] for p in v]


def main():
    seen = collections.Counter()
    with tempfile.TemporaryDirectory() as tmp:
        for m in sorted(x.name for x in pkgutil.iter_modules(presets.__path__)):
            names = module_presets(importlib.import_module("presets." + m))
            types = {n[2:].split("-")[0] for n in names}
            if len(types) != 1:
                raise SystemExit(f"presets/{m}.py mixes types: {types}")
            t = types.pop()
            seen.update(names)
            d = os.path.join(tmp, m)
            subprocess.run([sys.executable, os.path.join(ROOT, "tools", "preset_sheet.py"), *names,
                            "--every", "2", "--per-sheet", "20", "--clean", "--out", d],
                           check=True, capture_output=True)
            for i, f in enumerate(sorted(glob.glob(os.path.join(d, "*.png"))), 1):
                os.replace(f, os.path.join(OUT, f"{t}-_{i:02d}.png"))
            print(f"{t}: {len(names)}")

    dupes = [n for n, c in seen.items() if c > 1]
    missing = {p["name"] for p in presets.PRESET_LIST} - set(seen)
    print(f"{len(seen)} presets, {len(dupes)} duplicated, {len(missing)} missing")
    if dupes or missing:
        raise SystemExit(f"coverage problem: dupes={dupes} missing={sorted(missing)}")


if __name__ == "__main__":
    main()
