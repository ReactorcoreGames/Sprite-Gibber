"""Shared helpers for the headless preset tools (smoke test, metrics, contact sheets)."""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import numpy as np
from PIL import Image

from presets import PRESETS, PRESET_LIST
from utils.config import DEFAULT_CONFIG
from core.pipeline import build_params, run_sprite
from core.rendering import rotate_pixels

# Two reference subjects: one that fills a tight 32x32 canvas edge to edge, and one
# bottom-centred on a roomy 64x64 canvas. Presets should read well on both.
TEST_SPRITES = {
    "confined": os.path.join(ROOT, "tools", "test_sprites", "confined_32.png"),
    "wide":     os.path.join(ROOT, "tools", "test_sprites", "wide_64.png"),
}


def match_presets(terms):
    """Resolve CLI terms to preset names, in registry order (so types stay grouped).

    'all' matches everything; an exact name matches itself; anything else is a
    case-insensitive substring match (e.g. 'Plague' or '-space').
    """
    if any(t.lower() == "all" for t in terms):
        return [e["name"] for e in PRESET_LIST]
    wanted = set()
    for term in terms:
        if term in PRESETS:
            wanted.add(term)
        else:
            wanted.update(n for n in PRESETS if term.lower() in n.lower())
    return [e["name"] for e in PRESET_LIST if e["name"] in wanted]


def load_sprites(keys=None):
    keys = keys or list(TEST_SPRITES)
    return {k: Image.open(TEST_SPRITES[k]).convert("RGBA") for k in keys}


def preset_params(name, overrides=None):
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(PRESETS[name]["params"])
    cfg.update(overrides or {})
    return build_params(cfg)


def run_preset(name, img, overrides=None):
    """Run one preset on one image (plus optional param overrides). Returns (result, metrics dict)."""
    p = preset_params(name, overrides)
    result = run_sprite(img, p)
    return result, measure(result, img)


def measure(result, img):
    """Cheap numeric signals for spotting broken-looking animations."""
    W, H = img.size
    frames = result.frames
    start_px = int((np.array(img)[:, :, 3] > 0).sum()) or 1

    off = total = 0
    for s in result.states.values():
        pos = rotate_pixels(s["pixels"].astype(float), s["centroid"], s["angle"]) + s["offset"]
        r = np.floor(pos[:, 0] + 0.5)
        c = np.floor(pos[:, 1] + 0.5)
        off += int(((r < 0) | (r >= H) | (c < 0) | (c >= W)).sum())
        total += len(pos)

    hashes = {hashlib.md5(f.tobytes()).hexdigest() for f in frames}
    last_px = int((np.array(frames[-1])[:, :, 3] > 0).sum()) if frames else 0
    return {
        "ticks":       result.ticks,
        "stop":        result.stop_reason,
        "never_settles": result.never_settles,
        "distinct":    len(hashes),
        "frames":      len(frames),
        "off_canvas":  round(100.0 * off / max(total, 1), 1),
        "last_vis":    round(last_px / start_px, 2),
    }


def flags(m):
    """Human-readable warnings for a metrics dict (empty list = nothing suspicious)."""
    out = []
    if m["distinct"] < m["frames"] - 1:
        out.append(f"only {m['distinct']}/{m['frames']} distinct frames")
    if m["ticks"] <= 3:
        out.append(f"sim ended after {m['ticks']} tick(s)")
    if m["stop"] == "max_ticks" and not m["never_settles"]:
        # For never-settling modes MAX_SIM_TICKS is the intended duration, not a symptom.
        out.append("hit MAX_SIM_TICKS")
    if m["off_canvas"] > 25:
        out.append(f"{m['off_canvas']}% pixels off-canvas")
    return out
