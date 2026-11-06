"""Render the promo showcase: one preset per Main Type (61), each on an input/ animal, as
individual upscaled GIFs plus a combined grid GIF, and a contact sheet for judging the picks.

All GIFs share one timing (the presets' own MS_PER_FRAME/HOLD_* are overridden) so the
grid cells stay in sync, and frames are composited onto an opaque background so
semi-transparent tint/glow survives GIF's 1-bit alpha. 12 frames keeps the pixel-art
crunch and the files small.

Usage:
    python tools/promo_showcase.py sheet     # -> shots/promo/showcase_sheet.png
    python tools/promo_showcase.py gifs      # -> promo/showcase_grid_{1x,3x}.gif + showcase_gifs/*.gif
"""
import argparse
import os

from PIL import Image, ImageDraw

from _preset_tools import ROOT
from presets import PRESETS
from utils.config import DEFAULT_CONFIG
from core.pipeline import build_params, run_sprite
from core.output import frame_durations

BG = (60, 54, 68)
FRAMES = 12
MS_PER_FRAME, HOLD_FIRST, HOLD_LAST = 90, 500, 1000
GRID_COLS = 9
GUTTER, GUTTER_BG = 2, (18, 14, 20)

# One preset per Main Type, in library order: (preset without the leading "*.", animal number in input/).
# Animals are picked to contrast with the effect's colour so the change reads instantly.
PICKS = [
    ("Fire-Burn-terra", 22),                ("Cryo-Shatter-terra", 2),
    ("Electric-Shock-terra", 7),           ("Plasma-Burst-terra", 10),
    ("Water-Splash-terra", 27),            ("Acid-Melt-terra", 12),
    ("Singularity-Event-Horizon-space", 1),      ("Blade-Fire-Cleave-terra", 15),
    ("Hammer-Smash-terra-heavy", 5),       ("Slash-H-terra-deep", 35),
    ("Grenade-Fire-terra", 35),            ("Bullet-Explosive-wave", 4),
    ("Void-Consume-terra", 33),            ("Psychic-Shatter-terra-high", 3),
    ("Arcane-Burst-terra", 9),             ("Holy-Ascend-terra", 10),
    ("Heal-Bloom-inner", 29),              ("Photon-Vaporize-terra", 26),
    ("Flash-Annihilate-terra", 4),         ("Shadow-Fade-terra-fast", 32),
    ("Blood-Gibs-terra", 1),               ("Meat-Gib-terra-medium", 32),
    ("Bone-Shatter-terra", 29),            ("Biodegrade-Crumble-terra-fast", 9),
    ("Rot-Bloat-terra", 21),               ("Plague-Pustule-terra", 28),
    ("Wither-Drain-terra", 30),            ("Stone-Shatter-terra-medium", 23),
    ("Gold-Shatter-terra", 7),            ("Crystal-Shatter-terra", 6),
    ("Rust-Oxidize-terra", 24),            ("Goo-Splatter-terra", 32),
    ("Sand-Crumble-terra", 18),            ("Break-Shatter-terra", 19),
    ("Crush-Powder-terra", 23),            ("Grind-Tumble-terra", 25),
    ("Shred-Strip-terra", 17),             ("Laser-Slice-terra", 4),
    ("Ion-Disperse-terra", 13),            ("Crack-Fracture-terra", 34),
    ("Disintegrate-Crumble-terra", 35),     ("Evaporate-Fade-terra", 31),
    ("Liquify-Pool-terra", 2),             ("Smoke-Billow-terra", 17),
    ("Ash-Crumble-terra", 23),             ("Entropy-Decay-terra", 10),
    ("Glitch-Corrupt-terra", 8),           ("Chromatic-Destabilize-terra", 3),
    ("Matrix-Cascade-terra-down", 11),     ("Tar-Pool-terra", 3),
    ("Fungal-Colonize-terra", 34),         ("Spore-Burst-terra", 3),
    ("Brimstone-Erupt-terra-violent", 35), ("Curse-Corrupt-terra", 33),
    ("Vanish-Fade-terra", 9),              ("Burst-Rupture-terra-violent", 1),
    ("Clamp-Vice-terra", 20),              ("Squeeze-Vice-terra", 15),
    ("Flatten-Slam-terra", 24),            ("Nuclear-Obliterate-terra", 1),
    ("Antimatter-Annihilate-terra", 15),
]


def render(num, preset, frames=FRAMES):
    img = Image.open(os.path.join(ROOT, "input", f"animal ({num}).png")).convert("RGBA")
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(PRESETS["*." + preset]["params"])
    cfg["FRAMES"] = frames
    out = []
    for f in run_sprite(img, build_params(cfg)).frames:
        tile = Image.new("RGBA", f.size, BG + (255,))
        tile.alpha_composite(f)
        out.append(tile.convert("RGB"))
    return out


def save_gif(frames, path, scale=1):
    if scale > 1:
        frames = [f.resize((f.width * scale, f.height * scale), Image.NEAREST) for f in frames]
    durations = frame_durations(len(frames), MS_PER_FRAME, HOLD_FIRST, HOLD_LAST)
    pal = [f.quantize(colors=256, method=Image.Quantize.MEDIANCUT) for f in frames]
    pal[0].save(path, save_all=True, append_images=pal[1:], loop=0,
                duration=durations, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["sheet", "gifs"])
    ap.add_argument("--only", nargs="*", help="substrings of preset names to render")
    args = ap.parse_args()

    picks = [(p, n) for p, n in PICKS if not args.only or any(o.lower() in p.lower() for o in args.only)]
    rendered = [render(n, p) for p, n in picks]

    if args.mode == "sheet":
        out = os.path.join(ROOT, "shots", "promo")
        os.makedirs(out, exist_ok=True)
        scale, row_h = 3, 32 * 3 + 16
        sheet = Image.new("RGB", (FRAMES * (32 * scale + 4) + 4, row_h * len(picks)), (90, 90, 100))
        d = ImageDraw.Draw(sheet)
        for r, ((p, n), frames) in enumerate(zip(picks, rendered)):
            d.text((4, r * row_h + 2), f"{r + 1}: {p} (animal {n})", fill=(255, 255, 255))
            for c, f in enumerate(frames):
                sheet.paste(f.resize((32 * scale, 32 * scale), Image.NEAREST),
                            (4 + c * (32 * scale + 4), r * row_h + 14))
        sheet.save(os.path.join(out, "showcase_sheet.png"))
        return

    indiv = os.path.join(ROOT, "showcase_gifs")
    os.makedirs(indiv, exist_ok=True)
    for i, ((p, n), frames) in enumerate(zip(picks, rendered), 1):
        save_gif(frames, os.path.join(indiv, f"{i:02d}_{p.lower().replace('-', '_')}.gif"), scale=4)

    if len(picks) == len(PICKS):
        rows = -(-len(picks) // GRID_COLS)
        last_row_pad = (rows * GRID_COLS - len(picks)) * (32 + GUTTER) // 2  # centre a short last row
        grid = []
        for i in range(FRAMES):
            g = Image.new("RGB", (GRID_COLS * (32 + GUTTER) + GUTTER, rows * (32 + GUTTER) + GUTTER), GUTTER_BG)
            for k, frames in enumerate(rendered):
                row = k // GRID_COLS
                g.paste(frames[i], (GUTTER + (k % GRID_COLS) * (32 + GUTTER) + (last_row_pad if row == rows - 1 else 0),
                                    GUTTER + row * (32 + GUTTER)))
            grid.append(g)
        promo = os.path.join(ROOT, "promo")
        save_gif(grid, os.path.join(promo, "showcase_grid_1x.gif"))
        save_gif(grid, os.path.join(promo, "showcase_grid_3x.gif"), scale=3)


if __name__ == "__main__":
    main()
