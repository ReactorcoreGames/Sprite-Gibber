"""Render contact sheets: every frame of each preset, on both test sprites, side by side.

Each row is one preset: the confined 32x32 subject's frames, then the wide 64x64
subject's frames, all at the same pixel scale so the canvas difference is visible.
Canvas bounds are outlined. The label carries the preset name plus any metric flags.
--clean drops the flags, top-aligns the canvases under a larger name label and
divides the rows (the customer-facing preset catalog).

Usage:
    python tools/preset_sheet.py Fire                 # -> shots/Fire_01.png, ...
    python tools/preset_sheet.py all --per-sheet 12
    python tools/preset_sheet.py "*.Fire-Burn-terra" --out C:/somewhere --scale 3
    python tools/preset_sheet.py "*.Fire-" --every 2      # every 2nd frame + the last (compact judging view)
    python tools/preset_sheet.py "*.Fire-" --every 2 --clean  # catalog style, no QA flags
    python tools/preset_sheet.py "*.Fire-Burn-terra" --sprites a.png b.png --set CHUNKS=40 --set FRAMES=20
"""
import argparse
import ast
import os
import re

from PIL import Image, ImageDraw, ImageFont

from _preset_tools import ROOT, match_presets, load_sprites, run_preset, flags

BG       = (104, 104, 118, 255)
CANVAS   = (128, 128, 142, 255)
OUTLINE  = (70, 70, 82, 255)
TEXT     = (255, 255, 255, 255)
WARN     = (255, 190, 90, 255)
LABEL_H  = 14
GAP      = 4
DIVIDER  = (215, 215, 225, 255)


def _clean_font():
    try:
        return ImageFont.truetype("arialbd.ttf", 18)
    except OSError:
        return ImageFont.load_default()


def render_row(name, sprites, scale, every=1, overrides=None, clean=False):
    cells = []
    warnings = []
    for key, img in sprites.items():
        result, m = run_preset(name, img, overrides)
        warnings += [f"{key}: {f}" for f in flags(m)]
        frames = result.frames
        if every > 1:
            frames = frames[::every] + ([frames[-1]] if (len(frames) - 1) % every else [])
        cells.append((img.size, frames))

    row_h = max(size[1] for size, _ in cells) * scale
    width = sum((size[0] * scale + GAP) * len(frames) + GAP * 3 for size, frames in cells)
    label_h = 26 if clean else LABEL_H
    top = 3 if clean else 0  # room for the divider above the label
    row = Image.new("RGBA", (width, top + row_h + label_h + GAP * (3 if clean else 1)), BG)
    d = ImageDraw.Draw(row)
    if clean:
        d.rectangle([0, 0, width, 1], fill=DIVIDER)
        d.text((GAP, top + 2), name, fill=TEXT, font=_clean_font())
    else:
        d.text((GAP, 1), name, fill=TEXT)
    if warnings and not clean:
        d.text((GAP + 7 * len(name) + 12, 1), "  ".join(warnings), fill=WARN)

    x = GAP
    for (w, h), frames in cells:
        cw, ch = w * scale, h * scale
        # bottom-align canvases of different heights; clean mode top-aligns so the name sits on both
        y = top + label_h + (0 if clean else row_h - ch)
        for f in frames:
            tile = Image.new("RGBA", (cw, ch), CANVAS)
            tile.alpha_composite(f.resize((cw, ch), Image.NEAREST))
            row.paste(tile, (x, y))
            d.rectangle([x - 1, y - 1, x + cw, y + ch], outline=OUTLINE)
            x += cw + GAP
        x += GAP * 3
    return row


def _parse_set(kv):
    key, _, val = kv.partition("=")
    try:
        return key, ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return key, val


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="+", help="'all', exact preset names, or substrings")
    ap.add_argument("--per-sheet", type=int, default=10, help="presets per image (default 10)")
    ap.add_argument("--scale", type=int, default=2, help="pixel scale (default 2)")
    ap.add_argument("--every", type=int, default=1, help="show every Nth frame, plus the last (default 1)")
    ap.add_argument("--out", default=os.path.join(ROOT, "shots"), help="output folder")
    ap.add_argument("--clean", action="store_true", help="catalog style: no metric flags, name right above the frames")
    ap.add_argument("--sprites", nargs="+", help="PNG paths to use instead of the two test sprites")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="param override, repeatable (value parsed as a Python literal, else a string)")
    args = ap.parse_args()
    overrides = dict(_parse_set(kv) for kv in args.set)

    names = match_presets(args.terms)
    if not names:
        raise SystemExit(f"No presets matched: {args.terms}")

    os.makedirs(args.out, exist_ok=True)
    if args.sprites:
        sprites = {os.path.splitext(os.path.basename(f))[0]: Image.open(f).convert("RGBA") for f in args.sprites}
    else:
        sprites = load_sprites()
    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", "_".join(args.terms)).strip("_")[:40] or "sheet"

    for start in range(0, len(names), args.per_sheet):
        rows = [render_row(n, sprites, args.scale, args.every, overrides, args.clean) for n in names[start:start + args.per_sheet]]
        sheet = Image.new("RGBA", (max(r.width for r in rows), sum(r.height for r in rows)), BG)
        y = 0
        for r in rows:
            sheet.paste(r, (0, y))
            y += r.height
        path = os.path.join(args.out, f"{stem}_{start // args.per_sheet + 1:02d}.png")
        sheet.save(path)
        print(path)


if __name__ == "__main__":
    main()
