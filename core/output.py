import math
import os
import re

from PIL import Image

from core.rendering import apply_snapshot, interpolate_snapshots, render_states

_GIF_ALPHA_CUTOFF = 128

_ILLEGAL_FILENAME_CHARS = r'<>:"/\|?*'


def safe_filename(text: str) -> str:
    """Replace characters Windows forbids in file names; trim trailing dots/spaces."""
    cleaned = "".join("_" if c in _ILLEGAL_FILENAME_CHARS or ord(c) < 32 else c for c in text)
    return cleaned.rstrip(" .") or "_"


def export_stem(sprite_name: str, effect: str = None) -> str:
    """Base name for one sprite's exported files: '<sprite>_<effect>' (or just '<sprite>').

    Including the effect means exporting the same sprite with a second effect
    lands next to the first instead of overwriting it.
    """
    stem = safe_filename(sprite_name)
    return f"{stem}_{safe_filename(effect)}" if effect else stem


def render_frames(states, tick_snapshots, img, H, W, p,
                  dissolve_masks=None, dissolve_fade_rgb=None, before_frame=None):
    """Render FRAMES PIL Images and return them as a list.

    Frame 0 is the intact original; remaining frames are evenly spaced in time
    across the whole simulation. tick_snapshots[0] must be the at-rest state;
    frames that fall between two ticks are interpolated, so a fast settle
    still produces smooth, distinct frames instead of repeated ticks.
    before_frame, if given, is called before each frame (the pipeline's cancel check).
    """
    last_tick = len(tick_snapshots) - 1
    frames = [img]

    for frame in range(1, p.FRAMES):
        if before_frame is not None:
            before_frame()
        t = (frame / (p.FRAMES - 1)) * last_tick
        apply_snapshot(states, interpolate_snapshots(tick_snapshots, t))
        frames.append(render_states(states, H, W, p,
                                    dissolve_masks=dissolve_masks,
                                    frame_idx=frame,
                                    dissolve_fade_rgb=dissolve_fade_rgb))

    return frames


def save_frame_pngs(frames, out_dir, stem):
    """Write frames as <stem>_00.png, <stem>_01.png, … into out_dir.

    Zero-padded to at least 2 digits (3 past 100 frames) so they sort correctly.
    A re-export replaces the previous one: this stem's old frame files are
    removed first, so a shorter re-export doesn't leave stale trailing frames.
    """
    os.makedirs(out_dir, exist_ok=True)
    old_frame = re.compile(re.escape(stem) + r"_\d{2,3}\.png", re.IGNORECASE)
    for name in os.listdir(out_dir):
        if old_frame.fullmatch(name):
            os.remove(os.path.join(out_dir, name))
    pad = max(2, len(str(len(frames) - 1)))
    for i, frame in enumerate(frames):
        frame.save(os.path.join(out_dir, f"{stem}_{i:0{pad}d}.png"))


def save_spritesheet(frames, out_dir, stem, p):
    """Composite all frames into a single row-major PNG grid."""
    n = len(frames)
    cols = p.SHEET_COLUMNS if p.SHEET_COLUMNS > 0 else n
    rows = math.ceil(n / cols)
    W, H = frames[0].size
    sheet = Image.new("RGBA", (cols * W, rows * H), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        col = i % cols
        row = i // cols
        sheet.paste(frame, (col * W, row * H))
    sheet.save(os.path.join(out_dir, f"{stem}_sheet.png"))


def frame_durations(n, ms_per_frame, hold_first_ms, hold_last_ms):
    """Display time in ms of each of n frames: first/last frames held, the rest at
    ms_per_frame, all rounded to 10 ms (GIF centiseconds). Shared by the GIF writer
    and the GUI preview playback so the two always match."""
    def _round10(ms) -> int:
        return max(10, round(int(ms) / 10) * 10)

    base, first, last = _round10(ms_per_frame), _round10(hold_first_ms), _round10(hold_last_ms)
    if n == 1:
        return [first]
    if n == 2:
        return [first, last]
    return [first] + [base] * (n - 2) + [last]


def save_gif(frames, out_dir, stem, p):
    """Save an animated GIF with per-frame durations and nearest-neighbour upscale.

    HOLD_FIRST_MS / HOLD_LAST_MS set the display time of the first/last frame
    individually.  MS_PER_FRAME governs all other frames.  No frames are
    duplicated — Pillow writes each frame's delay directly into the GIF block.
    All values are rounded to the nearest 10 ms (GIF centisecond resolution).
    """
    if not frames:
        return

    durations = frame_durations(len(frames), p.MS_PER_FRAME, p.HOLD_FIRST_MS, p.HOLD_LAST_MS)

    W, H = frames[0].size
    new_W, new_H = W * p.GIF_SCALE, H * p.GIF_SCALE

    def _to_palette(img_rgba):
        # GIF has 1-bit transparency: alpha >= 128 is drawn, the rest is clear.
        # Opaque colours are quantised into palette slots 0–254; slot 255 is
        # reserved for transparency so it can never collide with a real colour.
        import numpy as np
        arr = np.array(img_rgba)
        opaque = arr[:, :, 3] >= _GIF_ALPHA_CUTOFF
        rgb = arr[:, :, :3].copy()
        if opaque.any():
            # Fill clear pixels with an existing colour so they don't eat a palette slot.
            rgb[~opaque] = rgb[opaque][0]
        q = Image.fromarray(rgb, "RGB").quantize(colors=255)
        idx = np.array(q)
        idx[~opaque] = 255
        palette = (q.getpalette() or [])[:255 * 3]
        palette += [0] * (256 * 3 - len(palette))
        out = Image.fromarray(idx, "P")
        out.putpalette(palette)
        out.info["transparency"] = 255
        return out

    scaled = [f.resize((new_W, new_H), Image.NEAREST) for f in frames]

    if getattr(p, "GIF_USE_PREVIEW_BG", False) and getattr(p, "GIF_BG_HEX", None):
        hx = p.GIF_BG_HEX.lstrip("#")
        bg_rgb = (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16))
        composited = []
        for f in scaled:
            bg = Image.new("RGBA", f.size, bg_rgb + (255,))
            bg.paste(f, mask=f.split()[3])
            composited.append(bg)
        scaled = composited

    palette_frames = [_to_palette(f) for f in scaled]

    path = os.path.join(out_dir, f"{stem}.gif")
    palette_frames[0].save(
        path,
        save_all=True,
        append_images=palette_frames[1:],
        loop=0,
        duration=durations,
        disposal=2,
        transparency=255,
        optimize=False,
    )
