"""Build the static promo images from promo/sprite gibber og_img.jpg, real renders and the
GUI screenshots in shots/promo/gui/ (taken by driving the real app):

- cover_1280x720:    title + 6 effects x 5 frames (blood, fire, acid, ice, stone, plasma)
- thumbnail_630x500: title + one animal burning
- screenshot_effects_1600x900: 12 effects as filmstrips
- screenshot_0N_*: the GUI screenshots with an ad-style headline sticker, a spotlight on
  the part of the window it's about, and an arrow to it

Usage:
    python tools/promo_images.py              # -> shots/promo/
    python tools/promo_images.py --out promo
"""
import argparse
import io
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from _preset_tools import ROOT
from presets import PRESET_LIST
from promo_showcase import PICKS, BG, render

FONT_BLACK = "C:/Windows/Fonts/seguibl.ttf"
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
OG = os.path.join(ROOT, "promo", "sprite gibber og_img.jpg")
GUI_SHOTS = os.path.join(ROOT, "shots", "promo", "gui")
N_PRESETS = len(PRESET_LIST)
N_TYPES = len({e["name"][2:].split("-")[0] for e in PRESET_LIST})

YELLOW, ORANGE, GREEN = (255, 236, 120), (255, 120, 60), (140, 255, 120)
STICKER, INK = (255, 214, 64), (28, 18, 20)

# Cover rows: label, preset, animal number, label colour. Animals contrast with their
# effect colour (white bear in blood, teal reindeer in fire) so the change reads instantly.
COVER_ROWS = [
    ("BLOOD",  "Blood-Gibs-terra",           1,  (255, 90, 90)),
    ("FIRE",   "Fire-Burn-terra",            22,  (255, 150, 60)),
    ("ACID",   "Acid-Melt-terra",            12, (170, 255, 80)),
    ("ICE",    "Cryo-Shatter-terra",         2,  (150, 225, 255)),
    ("STONE",  "Stone-Shatter-terra-medium", 23, (215, 215, 215)),
    ("PLASMA", "Plasma-Burst-terra",         30, (255, 110, 255)),
]
COVER_FRAMES = [0, 2, 4, 6, 9]          # of the 12-frame render

# GUI screenshot stamps: (source, output, headline, subline, highlight boxes, sticker xy)
STAMPS = [
    ("01_presets", "screenshot_01_presets", f"{N_PRESETS} presets", "search, click, done",
     [(18, 244, 540, 650)], (690, 160)),
    ("02_sprites", "screenshot_02_sprites", "Batch your whole game", "add a folder, hit Export all",
     [(16, 170, 538, 548), (846, 788, 1034, 838)], (690, 160)),
    ("03_physics", "screenshot_03_physics", "Real physics", "chunks · blasts · gravity · spin · bounce",
     [(12, 136, 548, 640)], (690, 160)),
    ("04_tint", "screenshot_04_tint", "Pick your gib colours", "any colour on the edges and insides",
     [(12, 296, 548, 540)], (690, 160)),
    ("06_mask", "screenshot_05_mask", "Shape masks", "cut it into splats, stars, gears, runes",
     [(16, 222, 548, 628)], (980, 650)),      # sticker low so the splat in the preview stays visible
]


def font(path, size):
    return ImageFont.truetype(path, size)


def cover_crop(img, w, h, y_bias=0.5):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = int((img.height - h) * y_bias)
    return img.crop((x, y, x + w, y + h))


def shadow_text(base, xy, text, fnt, fill=(255, 255, 255), anchor="la", stroke=0, blur=10, offset=6):
    """Text with a soft drop shadow plus a hard dark outline, so it reads over busy art."""
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0] + offset, xy[1] + offset), text, font=fnt, anchor=anchor,
                            fill=(0, 0, 0, 230), stroke_width=stroke + 4, stroke_fill=(0, 0, 0, 230))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(base).text(xy, text, font=fnt, anchor=anchor, fill=fill,
                              stroke_width=stroke, stroke_fill=(20, 10, 15))


def drop_shadow(base, box, radius, blur=12, offset=(8, 10), alpha=200):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle([x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]],
                                         radius, fill=(0, 0, 0, alpha))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))


def vgrad(w, h, top, bottom):
    g = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return g


def rounded_panel(img, radius, border=(255, 255, 255, 60)):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    ImageDraw.Draw(out).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius,
                                          outline=border, width=3)
    return out


def tile(frame, scale):
    t = Image.new("RGBA", (frame.width * scale, frame.height * scale), BG + (255,))
    t.alpha_composite(frame.convert("RGBA").resize(t.size, Image.NEAREST))
    return t


def make_cover(out):
    W, H = 1280, 720
    base = cover_crop(Image.open(OG).convert("RGBA"), W, H, 0.42)
    base.alpha_composite(vgrad(W, H, (0, 0, 0, 60), (0, 0, 0, 160)))

    # Right: 6 effects, each a row of 5 frames from intact to aftermath
    scale, gap, lab_w, pad = 3, 8, 150, 14
    cell = 32 * scale
    pw = pad * 2 + lab_w + len(COVER_FRAMES) * (cell + gap) - gap
    ph = pad * 2 + len(COVER_ROWS) * (cell + gap) - gap
    panel = Image.new("RGBA", (pw, ph), (16, 12, 18, 235))
    lab = font(FONT_BLACK, 34)
    for r, (label, preset, num, colour) in enumerate(COVER_ROWS):
        frames = render(num, preset)
        y = pad + r * (cell + gap)
        shadow_text(panel, (pad + 4, y + cell // 2), label, lab, fill=colour, anchor="lm", stroke=2, blur=4, offset=3)
        for c, fi in enumerate(COVER_FRAMES):
            panel.paste(tile(frames[fi], scale), (pad + lab_w + c * (cell + gap), y))
    panel = rounded_panel(panel, 16)
    px, py = W - pw - 30, (H - ph) // 2
    drop_shadow(base, (px, py, px + pw, py + ph), 16)
    base.alpha_composite(panel, (px, py))

    left = 40
    shadow_text(base, (left, 40), "SPRITE", font(FONT_BLACK, 118), fill=YELLOW, stroke=3)
    shadow_text(base, (left, 168), "GIBBER", font(FONT_BLACK, 118), fill=ORANGE, stroke=3)
    shadow_text(base, (left + 4, 330), "Pixel art gib", font(FONT_BOLD, 50), stroke=2)
    shadow_text(base, (left + 4, 388), "animations", font(FONT_BOLD, 50), stroke=2)
    shadow_text(base, (left + 4, 446), "in seconds", font(FONT_BOLD, 50), stroke=2)
    shadow_text(base, (left + 4, 548), f"{N_PRESETS} PRESETS", font(FONT_BLACK, 58), fill=GREEN, stroke=2)
    shadow_text(base, (left + 6, 634), "PNG · spritesheet · GIF", font(FONT_BOLD, 34), fill=(235, 235, 235), stroke=2, blur=6, offset=4)
    save(base, out, "cover_1280x720")


def make_thumb(out):
    W, H = 630, 500
    base = cover_crop(Image.open(OG).convert("RGBA"), W, H, 0.45)
    base.alpha_composite(vgrad(W, H, (0, 0, 0, 40), (0, 0, 0, 170)))

    # One animal burning, intact -> ashes
    frames = render(22, "Fire-Burn-terra")
    scale, gap, pad = 4, 10, 10
    cell = 32 * scale
    idxs = [0, 2, 4, 7]
    pw, ph = pad * 2 + len(idxs) * (cell + gap) - gap, pad * 2 + cell
    panel = Image.new("RGBA", (pw, ph), (16, 12, 18, 235))
    for c, fi in enumerate(idxs):
        panel.paste(tile(frames[fi], scale), (pad + c * (cell + gap), pad))
    panel = rounded_panel(panel, 12)
    px, py = (W - pw) // 2, H - ph - 20
    drop_shadow(base, (px, py, px + pw, py + ph), 12)
    base.alpha_composite(panel, (px, py))

    shadow_text(base, (W // 2, 8), "SPRITE", font(FONT_BLACK, 112), fill=YELLOW, anchor="ma", stroke=3)
    shadow_text(base, (W // 2, 122), "GIBBER", font(FONT_BLACK, 112), fill=ORANGE, anchor="ma", stroke=3)
    shadow_text(base, (W // 2, 246), "Destroy anything", font(FONT_BLACK, 56), fill=GREEN, anchor="ma", stroke=2)
    save(base, out, "thumbnail_630x500")


def make_gallery(out):
    """16:9 screenshot: 12 effects, each as a 7-frame filmstrip."""
    W, H = 1600, 900
    base = vgrad(W, H, (34, 26, 36, 255), (20, 16, 24, 255))
    d = ImageDraw.Draw(base)
    shadow_text(base, (W // 2, 22), f"{N_PRESETS} presets across {N_TYPES} effect types", font(FONT_BLACK, 52),
                fill=YELLOW, anchor="ma", stroke=2, blur=6, offset=4)
    animal = dict(PICKS)
    picks = ["Fire-Burn-terra", "Cryo-Shatter-terra", "Blood-Gibs-terra", "Electric-Shock-terra",
             "Gold-Shatter-terra", "Acid-Melt-terra", "Nuclear-Obliterate-terra", "Crystal-Shatter-terra",
             "Brimstone-Erupt-terra-violent", "Plague-Pustule-terra", "Matrix-Cascade-terra-down", "Laser-Slice-terra"]
    scale, gap, n_frames = 3, 6, 7
    cell = 32 * scale
    col_w = n_frames * (cell + gap) - gap
    x0s = [(W - 2 * col_w - 70) // 2, (W - 2 * col_w - 70) // 2 + col_w + 70]
    lab = font(FONT_BOLD, 24)
    row_h = cell + 34
    for k, preset in enumerate(picks):
        x, y = x0s[k // 6], 108 + (k % 6) * row_h
        d.text((x, y), preset.replace("-terra", "").replace("-", " "), font=lab, fill=(235, 225, 215))
        frames = render(animal[preset], preset)
        for j in range(n_frames):
            fi = round(j * (len(frames) - 1) / (n_frames - 1) * 0.8)
            base.paste(tile(frames[fi], scale), (x + j * (cell + gap), y + 30))
    save(base, out, "screenshot_effects_1600x900")


def arrow(d, p0, p1, fill, outline, shaft=14, head=44, head_w=46, edge=5):
    """One closed arrow polygon (shaft + head), so the outline wraps it evenly."""
    import math
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    bx, by = p1[0] - ux * head, p1[1] - uy * head
    s, h = shaft / 2, head_w / 2
    pts = [(p0[0] + nx * s, p0[1] + ny * s), (bx + nx * s, by + ny * s), (bx + nx * h, by + ny * h), p1,
           (bx - nx * h, by - ny * h), (bx - nx * s, by - ny * s), (p0[0] - nx * s, p0[1] - ny * s)]
    d.polygon(pts, fill=fill, outline=outline, width=edge)


def make_stamped(out):
    for src, stem, head, sub, boxes, (sx, sy) in STAMPS:
        path = os.path.join(GUI_SHOTS, src + ".png")
        if not os.path.exists(path):
            print("skipped", stem, "(no", src + ".png in shots/promo/gui)")
            continue
        base = Image.open(path).convert("RGBA")

        # Spotlight: dim everything except the highlighted boxes
        dim = Image.new("RGBA", base.size, (10, 6, 12, 120))
        hole = Image.new("L", base.size, 255)
        for b in boxes:
            ImageDraw.Draw(hole).rounded_rectangle(b, 12, fill=0)
        dim.putalpha(Image.eval(hole, lambda v: v * 120 // 255))
        base.alpha_composite(dim)
        d = ImageDraw.Draw(base)
        for b in boxes:
            d.rounded_rectangle([b[0] - 3, b[1] - 3, b[2] + 3, b[3] + 3], 14, outline=INK, width=10)
            d.rounded_rectangle(b, 12, outline=STICKER, width=6)

        # Sticker: headline + subline on a tilted yellow card
        fh, fs = font(FONT_BLACK, 64), font(FONT_BOLD, 32)
        tw = max(d.textlength(head, font=fh), d.textlength(sub, font=fs))
        cw, ch = int(tw) + 60, 150
        card = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([20, 20, 20 + cw, 20 + ch], 18, fill=STICKER, outline=INK, width=6)
        cd.text((50, 34), head, font=fh, fill=INK)
        cd.text((52, 116), sub, font=fs, fill=(70, 40, 30))
        card = card.rotate(2.5, resample=Image.BICUBIC, expand=True)
        drop_shadow(base, (sx + 20, sy + 20, sx + 20 + cw, sy + 20 + ch), 18, blur=14)

        # Arrows from the sticker's left edge to each box's right edge
        for b in boxes:
            target = (b[2] + 14, (b[1] + b[3]) // 2) if b[2] < sx else ((b[0] + b[2]) // 2, b[1] - 14)
            start = (sx + 30, sy + 20 + ch // 2) if b[2] < sx else (sx + 20 + cw // 2, sy + ch + 30)
            arrow(d, start, target, STICKER, INK)
        base.alpha_composite(card, (sx, sy))
        save(base, out, stem)


def save(img, out, stem):
    """Encode as PNG and JPG in memory and write whichever is smaller."""
    rgb = img.convert("RGB")
    best = None
    for ext, kw in (("png", {"optimize": True}), ("jpg", {"quality": 92, "optimize": True, "subsampling": 0})):
        buf = io.BytesIO()
        rgb.save(buf, "PNG" if ext == "png" else "JPEG", **kw)
        if best is None or buf.tell() < len(best[1]):
            best = (ext, buf.getvalue())
    path = os.path.join(out, f"{stem}.{best[0]}")
    with open(path, "wb") as f:
        f.write(best[1])
    print(os.path.basename(path), len(best[1]) // 1024, "KB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join("shots", "promo"))
    ap.add_argument("--only", choices=["cover", "thumb"], help="build just this image")
    args = ap.parse_args()
    out = os.path.join(ROOT, args.out)
    os.makedirs(out, exist_ok=True)
    if args.only:
        {"cover": make_cover, "thumb": make_thumb}[args.only](out)
        return
    make_cover(out)
    make_thumb(out)
    make_gallery(out)
    make_stamped(out)


if __name__ == "__main__":
    main()
