"""Flag presets whose animation is likely broken or weak, without looking at it.

Runs each preset on both test sprites and reports numeric warning signs:
too few distinct frames (static animation), a sim that ends after 1–3 ticks,
a sim that runs to MAX_SIM_TICKS (motion squashed into the first frames), or a
large share of pixels flung off-canvas. A preset with no flags can still look
bad — this is a triage pass before contact sheets, not a replacement for them.

Usage:
    python tools/preset_metrics.py all
    python tools/preset_metrics.py Fire -space
    python tools/preset_metrics.py all --all-rows     # print every preset, not just flagged ones
"""
import sys

from _preset_tools import match_presets, load_sprites, run_preset, flags


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_all = "--all-rows" in sys.argv
    if not args:
        print(__doc__)
        sys.exit(1)

    names = match_presets(args)
    if not names:
        print(f"No presets matched: {args}")
        sys.exit(1)

    sprites = load_sprites()
    flagged = 0
    for name in names:
        lines = []
        any_flag = False
        for key, img in sprites.items():
            _, m = run_preset(name, img)
            f = flags(m)
            any_flag = any_flag or bool(f)
            lines.append(
                f"    {key:<8} ticks={m['ticks']:<4} stop={m['stop']:<9} "
                f"distinct={m['distinct']}/{m['frames']} off={m['off_canvas']:>5}% "
                f"last_vis={m['last_vis']:<5}" + (f"  <- {'; '.join(f)}" if f else "")
            )
        if any_flag:
            flagged += 1
        if any_flag or show_all:
            print(name)
            print("\n".join(lines))

    print(f"\n{flagged}/{len(names)} presets flagged")


if __name__ == "__main__":
    main()
