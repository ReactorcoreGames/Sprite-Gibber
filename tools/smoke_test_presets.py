"""Headless smoke test for presets — runs the full gib pipeline (chunking,
tint, dissolve, physics, frame mask) on both test sprites without the GUI and
reports pass/fail per preset. Catches crashes only; use preset_metrics.py and
preset_sheet.py to judge how presets actually look.

Usage:
    python tools/smoke_test_presets.py all
    python tools/smoke_test_presets.py Plague
    python tools/smoke_test_presets.py "*.Plague-Spread-terra" "*.Fungal-Bloom-terra-fast"

A bare argument is matched as a case-insensitive substring against preset
names (e.g. "Plague" matches every *.Plague-* preset). Exact names also work.
"""
import sys

from _preset_tools import match_presets, load_sprites, run_preset


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    names = match_presets(sys.argv[1:])
    if not names:
        print(f"No presets matched: {sys.argv[1:]}")
        sys.exit(1)

    sprites = load_sprites()
    failures = 0
    for name in names:
        try:
            parts = []
            for key, img in sprites.items():
                _, m = run_preset(name, img)
                parts.append(f"{key}: {m['frames']} frames, {m['ticks']} ticks")
            print(f"{name} -> OK ({'; '.join(parts)})")
        except Exception as e:
            failures += 1
            print(f"{name} -> ERROR: {e!r}")

    print(f"\n{len(names) - failures}/{len(names)} passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
