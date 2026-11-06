import colorsys
import math
import numpy as np
from collections import deque
from PIL import Image


def _tint_weight(frame_idx, p, chunk_onset=0.0):
    """Return blend weight 0.0 (original colors) → 1.0 (full tint) for this frame."""
    if p.TINT_ANIM == "instant" or p.FRAMES <= 1:
        return 1.0
    t = frame_idx / (p.FRAMES - 1)
    if p.TINT_ANIM == "linear":
        return t
    if p.TINT_ANIM == "early":
        return min(1.0, t * 3.0)
    if p.TINT_ANIM == "late":
        return max(0.0, (t - 0.5) * 2.0)
    if p.TINT_ANIM == "pulse":
        return math.sin(math.pi * t)
    if p.TINT_ANIM == "per_chunk":
        if t < chunk_onset:
            return 0.0
        return (t - chunk_onset) / max(1e-6, 1.0 - chunk_onset)
    return 1.0


def _tint_color_t(frame_idx, p):
    """Return gamma-curved color-animation t in [0,1] for this frame."""
    if p.FRAMES <= 1:
        return 1.0
    t = frame_idx / (p.FRAMES - 1)
    curve = getattr(p, 'TINT_COLOR_ANIM_CURVE', 1.0)
    return t ** (1.0 / max(curve, 1e-6))


def rotate_pixels(pixels, centroid, angle_deg):
    angle = math.radians(angle_deg)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    shifted = pixels - centroid
    row_rot = shifted[:, 0] * cos_a - shifted[:, 1] * sin_a
    col_rot = shifted[:, 0] * sin_a + shifted[:, 1] * cos_a
    return np.stack([row_rot, col_rot], axis=1) + centroid


def _splat(canvas, rows_f, cols_f, colors, H, W):
    """Write each fractional-position pixel to the canvas, splatting to the
    neighbor cell on any axis where rounding is ambiguous (frac near 0.5).
    This closes the sub-pixel gaps that appear between adjacent source pixels
    once a chunk is rotated to a non-axis-aligned angle, without fattening
    silhouettes at rest (0/90/180/270 deg stay single-cell)."""
    if len(rows_f) == 0:
        return
    base_r = np.floor(rows_f + 0.5)
    base_c = np.floor(cols_f + 0.5)
    frac_r = rows_f - np.floor(rows_f)
    frac_c = cols_f - np.floor(cols_f)

    AMBIG = 0.2  # distance from 0.5 within which we also fill the neighbor cell
    r_ambig = np.abs(frac_r - 0.5) < AMBIG
    c_ambig = np.abs(frac_c - 0.5) < AMBIG

    r_alt = np.where(rows_f - base_r >= 0, base_r + 1, base_r - 1)
    c_alt = np.where(cols_f - base_c >= 0, base_c + 1, base_c - 1)

    def _write(r, c, cols_arr):
        # Off-canvas pixels are dropped, not clamped — clamping smeared them into
        # lines along the canvas border.
        rr = r.astype(int)
        cc = c.astype(int)
        inside = (rr >= 0) & (rr < H) & (cc >= 0) & (cc < W)
        canvas[rr[inside], cc[inside]] = cols_arr[inside]

    _write(base_r, base_c, colors)
    if r_ambig.any():
        _write(r_alt[r_ambig], base_c[r_ambig], colors[r_ambig])
    if c_ambig.any():
        _write(base_r[c_ambig], c_alt[c_ambig], colors[c_ambig])
    both = r_ambig & c_ambig
    if both.any():
        _write(r_alt[both], c_alt[both], colors[both])


def render_states(states, H, W, p, dissolve_masks=None, frame_idx=None, dissolve_fade_rgb=None):
    """Render a single frame from the current chunk states. Returns an RGBA Image."""
    dissolve_fade_window = max(2, p.FRAMES // 4)
    canvas = np.zeros((H, W, 4), dtype=np.uint8)

    # Pre-compute color-animation lerp factor for this frame.
    has_color_anim = (getattr(p, 'TINT_COLOR_OUTER_END', None) is not None or
                      getattr(p, 'TINT_COLOR_INNER_END', None) is not None)
    color_t = _tint_color_t(frame_idx, p) if (has_color_anim and frame_idx is not None) else 0.0

    for cid, s in states.items():
        pixels = s["pixels"].astype(float)
        rotated = rotate_pixels(pixels, s["centroid"], s["angle"])
        translated = rotated + s["offset"]
        rows_f = translated[:, 0]
        cols_f = translated[:, 1]

        # Resolve tint animation blend for this chunk/frame.
        if "colors_orig" in s and frame_idx is not None:
            w = _tint_weight(frame_idx, p, s.get("tint_onset", 0.0))
            # Resolve the tinted color (lerp between start and end tint if color anim active).
            if has_color_anim and "colors_end" in s and color_t > 0.0:
                if color_t >= 1.0:
                    tinted = s["colors_end"]
                else:
                    tinted = (s["colors"] * (1.0 - color_t) + s["colors_end"] * color_t).astype(np.uint8)
            else:
                tinted = s["colors"]
            if w >= 1.0:
                base_colors = tinted
            elif w <= 0.0:
                base_colors = s["colors_orig"]
            else:
                base_colors = (s["colors_orig"] * (1.0 - w) + tinted * w).astype(np.uint8)
        else:
            base_colors = s["colors"]

        if dissolve_masks is not None:
            mask = dissolve_masks[cid]           # shape (n_pixels,)
            alive = mask > frame_idx             # True = still visible this frame
            rf = rows_f[alive]
            cf = cols_f[alive]
            pixel_colors = base_colors[alive].astype(float)   # copy; never mutate arrays

            if dissolve_fade_rgb is not None and alive.any():
                dropout_frames = mask[alive].astype(float)
                proximity = np.clip(
                    1.0 - (dropout_frames - frame_idx) / dissolve_fade_window, 0.0, 1.0
                )
                blend = proximity * p.DISSOLVE_FADE_STRENGTH
                fr, fg, fb = dissolve_fade_rgb
                pixel_colors[:, 0] = pixel_colors[:, 0] * (1 - blend) + fr * blend
                pixel_colors[:, 1] = pixel_colors[:, 1] * (1 - blend) + fg * blend
                pixel_colors[:, 2] = pixel_colors[:, 2] * (1 - blend) + fb * blend

            pixel_colors = np.clip(pixel_colors, 0, 255).astype(np.uint8)
            _splat(canvas, rf, cf, pixel_colors, H, W)
        else:
            _splat(canvas, rows_f, cols_f, base_colors, H, W)

    return Image.fromarray(canvas, "RGBA")


def snapshot(states):
    """Deep-copy the per-chunk mutable state (offset, angle, settled). Pixels/colors are immutable."""
    return {
        cid: {
            "offset":  s["offset"].copy(),
            "angle":   s["angle"],
            "settled": s["settled"],
        }
        for cid, s in states.items()
    }


def apply_snapshot(states, snap):
    """Overlay a snapshot onto states for rendering without touching pixels/colors."""
    for cid, saved in snap.items():
        states[cid]["offset"]  = saved["offset"].copy()
        states[cid]["angle"]   = saved["angle"]
        states[cid]["settled"] = saved["settled"]


def interpolate_snapshots(tick_snapshots, t):
    """Snapshot at fractional tick t, linearly blending offset and angle between ticks."""
    i0 = int(math.floor(t))
    i1 = min(i0 + 1, len(tick_snapshots) - 1)
    f = t - i0
    if f <= 1e-9 or i0 == i1:
        return tick_snapshots[i0]
    a, b = tick_snapshots[i0], tick_snapshots[i1]
    return {
        cid: {
            "offset":  a[cid]["offset"] * (1.0 - f) + b[cid]["offset"] * f,
            "angle":   a[cid]["angle"] * (1.0 - f) + b[cid]["angle"] * f,
            "settled": b[cid]["settled"],
        }
        for cid in a
    }


def _parse_hex(hex_str):
    h = hex_str.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _lerp_color(start_rgb, end_rgb, t):
    """Linearly interpolate two RGB tuples."""
    return (
        int(round(start_rgb[0] + t * (end_rgb[0] - start_rgb[0]))),
        int(round(start_rgb[1] + t * (end_rgb[1] - start_rgb[1]))),
        int(round(start_rgb[2] + t * (end_rgb[2] - start_rgb[2]))),
    )


def _bfs_depths(seed_pixels, allowed_set):
    depth = {}
    queue = deque()
    for rc in seed_pixels:
        if rc in allowed_set and rc not in depth:
            depth[rc] = 0
            queue.append(rc)
    while queue:
        r, c = queue.popleft()
        d = depth[(r, c)]
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if (nr, nc) in allowed_set and (nr, nc) not in depth:
                depth[(nr, nc)] = d + 1
                queue.append((nr, nc))
    return depth


def _centroid_seeds(state, chunk_set):
    """Return the BFS seed pixel(s) for the inner-outward pass, snapped to the chunk."""
    cr, cc = state["centroid"]
    candidate = (int(round(cr)), int(round(cc)))
    if candidate in chunk_set:
        return [candidate]
    return [min(chunk_set, key=lambda rc: (rc[0] - cr) ** 2 + (rc[1] - cc) ** 2)]


def _apply_saturation_shift(state, shift):
    """Shift HSV saturation of all chunk pixels in-place. Alpha is preserved."""
    colors = state["colors"]
    for i, rgba in enumerate(colors):
        r, g, b, a = int(rgba[0]), int(rgba[1]), int(rgba[2]), int(rgba[3])
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        s = max(0.0, min(1.0, s + shift))
        nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
        colors[i] = [round(nr * 255), round(ng * 255), round(nb * 255), a]


def _apply_grain(state, factors):
    """Scale each pixel's RGB by its fixed grain factor in-place. Alpha is preserved."""
    colors = state["colors"]
    rgb = colors[:, :3].astype(float) * factors[:, None]
    colors[:, :3] = np.clip(np.rint(rgb), 0, 255).astype(colors.dtype)


def _apply_depth_map(state, depth_map, p, rng=None, pixel_depth=1,
                     noise_field=None, tint_noise=0.0,
                     override_outer=None, override_inner=None):
    """Unidirectional tint: Outer color at border, Inner color at depth cutoff."""
    outer  = override_outer if override_outer is not None else _parse_hex(p.TINT_COLOR_OUTER)
    inner  = override_inner if override_inner is not None else _parse_hex(p.TINT_COLOR_INNER)
    jitter = getattr(p, 'TINT_JITTER_OUTER', 0.0)
    colors = state["colors"]
    if pixel_depth <= 0:
        return

    for i, (r, c) in enumerate(state["pixels"]):
        d = depth_map.get((r, c))
        if d is None:
            continue
        if rng is not None and jitter > 0.0:
            effective_cutoff = max(1.0, pixel_depth * (1.0 + rng.uniform(-jitter, jitter)))
        else:
            effective_cutoff = float(pixel_depth)
        if noise_field is not None and tint_noise > 0.0:
            noise_val = noise_field[r, c]
            noise_mod = 1.0 + tint_noise * (noise_val - 0.5) * 2.0
            effective_cutoff = max(1.0, effective_cutoff * noise_mod)
        if d >= effective_cutoff:
            continue
        t = d / effective_cutoff                          # 0 at border → 1 at cutoff
        opacity      = p.TINT_OPACITY_OUTER * (1.0 - t)
        inner_weight = t                                  # pure Outer at t=0, pure Inner at t=1
        tint_r = outer[0] + inner_weight * (inner[0] - outer[0])
        tint_g = outer[1] + inner_weight * (inner[1] - outer[1])
        tint_b = outer[2] + inner_weight * (inner[2] - outer[2])
        orig  = colors[i]
        new_r = int(round(orig[0] * (1.0 - opacity) + tint_r * opacity))
        new_g = int(round(orig[1] * (1.0 - opacity) + tint_g * opacity))
        new_b = int(round(orig[2] * (1.0 - opacity) + tint_b * opacity))
        bleed = p.TINT_ALPHA_BLEED_OUTER * (1.0 - t)
        new_a = int(round(orig[3] * (1.0 - bleed)))
        colors[i] = [
            max(0, min(255, new_r)),
            max(0, min(255, new_g)),
            max(0, min(255, new_b)),
            max(0, min(255, new_a)),
        ]


def _apply_depth_map_bidir(state, depth_outer, depth_inner,
                           depth_outer_px, depth_inner_px, p, rng=None,
                           noise_field=None, tint_noise=0.0,
                           override_outer=None, override_inner=None):
    """Bidirectional tint: Outer bleeds inward from border, Inner radiates outward from centroid."""
    outer         = override_outer if override_outer is not None else _parse_hex(p.TINT_COLOR_OUTER)
    inner         = override_inner if override_inner is not None else _parse_hex(p.TINT_COLOR_INNER)
    jitter_outer  = getattr(p, 'TINT_JITTER_OUTER', 0.0)
    jitter_inner  = getattr(p, 'TINT_JITTER_INNER', 0.0)
    collision     = getattr(p, 'TINT_COLLISION', 'blend')
    blend         = getattr(p, 'TINT_BLEND', 0.5)
    colors        = state["colors"]

    for i, (r, c) in enumerate(state["pixels"]):
        d_out = depth_outer.get((r, c))
        d_in  = depth_inner.get((r, c))
        if d_out is None or d_in is None:
            continue

        if depth_outer_px <= 0:
            t_out = 1.0
        else:
            if rng is not None and jitter_outer > 0.0:
                cutoff_outer = max(1.0, depth_outer_px * (1.0 + rng.uniform(-jitter_outer, jitter_outer)))
            else:
                cutoff_outer = float(depth_outer_px)
            if noise_field is not None and tint_noise > 0.0:
                noise_val = noise_field[r, c]
                noise_mod = 1.0 + tint_noise * (noise_val - 0.5) * 2.0
                cutoff_outer = max(1.0, cutoff_outer * noise_mod)
            t_out = min(d_out / cutoff_outer, 1.0)   # 0 at border, 1 past outer cutoff

        if depth_inner_px <= 0:
            t_in = 1.0
        else:
            if rng is not None and jitter_inner > 0.0:
                cutoff_inner = max(1.0, depth_inner_px * (1.0 + rng.uniform(-jitter_inner, jitter_inner)))
            else:
                cutoff_inner = float(depth_inner_px)
            if noise_field is not None and tint_noise > 0.0:
                noise_val = noise_field[r, c]
                noise_mod = 1.0 + tint_noise * (noise_val - 0.5) * 2.0
                cutoff_inner = max(1.0, cutoff_inner * noise_mod)
            t_in = min(d_in / cutoff_inner, 1.0)     # 0 at centroid, 1 past inner cutoff

        if t_out >= 1.0 and t_in >= 1.0:
            continue   # pixel beyond both cutoffs — untinted

        opacity_out = p.TINT_OPACITY_OUTER * (1.0 - t_out)
        opacity_in  = p.TINT_OPACITY_INNER * (1.0 - t_in)

        if collision == "outer_wins":
            if t_out < 1.0:
                inner_weight = 0.0
                opacity = opacity_out
            else:
                inner_weight = 1.0
                opacity = opacity_in
        elif collision == "inner_wins":
            if t_in < 1.0:
                inner_weight = 1.0
                opacity = opacity_in
            else:
                inner_weight = 0.0
                opacity = opacity_out
        else:  # "blend"
            # raw = 0.5 exactly at the geometric midpoint where t_out == t_in
            raw = t_out / (t_out + t_in + 1e-9)
            # bias by TINT_BLEND: 0.5=no shift, 1.0=outer wins, 0.0=inner wins
            m = blend
            inner_weight = raw * (1.0 - m) / max(1e-9, raw * (1.0 - m) + (1.0 - raw) * m)
            opacity = opacity_out * (1.0 - inner_weight) + opacity_in * inner_weight

        if opacity <= 0.0:
            continue

        tint_r = outer[0] + inner_weight * (inner[0] - outer[0])
        tint_g = outer[1] + inner_weight * (inner[1] - outer[1])
        tint_b = outer[2] + inner_weight * (inner[2] - outer[2])
        orig  = colors[i]
        new_r = int(round(orig[0] * (1.0 - opacity) + tint_r * opacity))
        new_g = int(round(orig[1] * (1.0 - opacity) + tint_g * opacity))
        new_b = int(round(orig[2] * (1.0 - opacity) + tint_b * opacity))
        bleed_out = p.TINT_ALPHA_BLEED_OUTER * (1.0 - t_out)
        bleed_in  = p.TINT_ALPHA_BLEED_INNER * (1.0 - t_in)
        bleed     = max(bleed_out, bleed_in)
        new_a     = int(round(orig[3] * (1.0 - bleed)))
        colors[i] = [
            max(0, min(255, new_r)),
            max(0, min(255, new_g)),
            max(0, min(255, new_b)),
            max(0, min(255, new_a)),
        ]


def _run_tint_pass(states, arr, p, rng, noise_field, tint_noise,
                   depth_outer_px, depth_inner_px,
                   override_outer=None, override_inner=None):
    """Run one full tint BFS pass across all chunks, writing into state["colors"]."""
    pixel_to_chunk = {}
    for cid, s in states.items():
        for rc in s["pixels"]:
            pixel_to_chunk[(rc[0], rc[1])] = cid

    blend_mode = getattr(p, 'TINT_BLEND_MODE', 'unidirectional')

    if p.TINT_MODE == "chunks":
        for cid, s in states.items():
            if len(s["pixels"]) == 0:
                continue
            chunk_set = {(rc[0], rc[1]) for rc in s["pixels"]}
            border = []
            for r, c in chunk_set:
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if pixel_to_chunk.get((nr, nc)) != cid:
                        border.append((r, c))
                        break
            depth_outer_map = _bfs_depths(border, chunk_set)
            if blend_mode == "bidirectional":
                depth_inner_map = _bfs_depths(_centroid_seeds(s, chunk_set), chunk_set)
                # A Voronoi cell clipped by the silhouette can split into pieces the centroid
                # BFS never reaches; seed each such piece at its pixel nearest the centroid.
                unreached = chunk_set - depth_inner_map.keys()
                while unreached:
                    piece = _bfs_depths(_centroid_seeds(s, unreached), unreached)
                    depth_inner_map.update(piece)
                    unreached -= piece.keys()
                _apply_depth_map_bidir(s, depth_outer_map, depth_inner_map,
                                       depth_outer_px, depth_inner_px, p, rng=rng,
                                       noise_field=noise_field, tint_noise=tint_noise,
                                       override_outer=override_outer, override_inner=override_inner)
            else:
                _apply_depth_map(s, depth_outer_map, p, rng=rng, pixel_depth=depth_outer_px,
                                 noise_field=noise_field, tint_noise=tint_noise,
                                 override_outer=override_outer, override_inner=override_inner)

    elif p.TINT_MODE == "edges":
        all_opaque = set(pixel_to_chunk.keys())
        border = []
        for r, c in all_opaque:
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if (nr, nc) not in all_opaque:
                    border.append((r, c))
                    break
        depth_map = _bfs_depths(border, all_opaque)
        for cid, s in states.items():
            chunk_depth = {(rc[0], rc[1]): depth_map[(rc[0], rc[1])]
                           for rc in s["pixels"] if (rc[0], rc[1]) in depth_map}
            _apply_depth_map(s, chunk_depth, p, rng=rng, pixel_depth=depth_outer_px,
                             noise_field=noise_field, tint_noise=tint_noise,
                             override_outer=override_outer, override_inner=override_inner)


def apply_tint(states, arr, p, rng=None):
    import types as _types

    total_opaque = sum(len(s["pixels"]) for s in states.values())
    sq           = max(1.0, math.sqrt(total_opaque))

    depth_outer_raw = getattr(p, 'TINT_DEPTH_OUTER', 0.12)
    depth_inner_raw = getattr(p, 'TINT_DEPTH_INNER', 0.12)
    depth_outer_px  = 0 if depth_outer_raw <= 0.0 else max(1, round(depth_outer_raw * sq))
    depth_inner_px  = 0 if depth_inner_raw <= 0.0 else max(1, round(depth_inner_raw * sq))

    # Per-pixel grain factors, drawn only when grain is on so grain-free presets keep their RNG
    # stream (and therefore their exact Voronoi/jitter/dissolve results).
    grain = getattr(p, 'TINT_GRAIN', 0.0)
    grain_factors = None
    if grain > 0.0 and rng is not None:
        grain_factors = {cid: 1.0 + grain * rng.uniform(-1.0, 1.0, len(s["pixels"]))
                         for cid, s in states.items()}

    if depth_outer_px <= 0 and depth_inner_px <= 0:
        if grain_factors is not None:
            for cid, s in states.items():
                _apply_grain(s, grain_factors[cid])
        return

    if getattr(p, 'TINT_SINGLE_COLOR', False):
        p = _types.SimpleNamespace(**vars(p))
        p.TINT_COLOR_OUTER = p.TINT_COLOR_INNER

    tint_noise = getattr(p, 'TINT_NOISE', 0.0)
    sat_shift  = getattr(p, 'TINT_SATURATION_SHIFT', 0.0)
    outer_end  = getattr(p, 'TINT_COLOR_OUTER_END', None)
    inner_end  = getattr(p, 'TINT_COLOR_INNER_END', None)
    has_color_anim = (outer_end is not None or inner_end is not None)

    # Determine if we need colors_orig saved (animated opacity or animated color).
    needs_orig = p.TINT_ANIM != "instant" or has_color_anim
    if needs_orig:
        for s in states.values():
            s["colors_orig"] = s["colors"].copy()

    # Assign per-chunk random onset fractions for the per_chunk mode.
    if p.TINT_ANIM == "per_chunk" and rng is not None:
        for s in states.values():
            s["tint_onset"] = float(rng.random())

    # Build noise field once (shared across all chunks).
    noise_field = None
    if tint_noise > 0.0 and rng is not None:
        H, W = arr.shape[:2]
        grid_h = max(2, H // 8)
        grid_w = max(2, W // 8)
        grid = rng.random((grid_h, grid_w))
        row_coords = np.linspace(0, grid_h - 1, H)
        col_coords = np.linspace(0, grid_w - 1, W)
        upsampled = np.zeros((H, grid_w))
        for c in range(grid_w):
            upsampled[:, c] = np.interp(row_coords, np.arange(grid_h), grid[:, c])
        noise_field = np.zeros((H, W))
        for r in range(H):
            noise_field[r, :] = np.interp(col_coords, np.arange(grid_w), upsampled[r, :])

    # --- Primary tint pass (start colors) ---
    _run_tint_pass(states, arr, p, rng, noise_field, tint_noise,
                   depth_outer_px, depth_inner_px)

    # Apply saturation shift to primary tinted colors.
    if sat_shift != 0.0:
        for s in states.values():
            _apply_saturation_shift(s, sat_shift)
    if grain_factors is not None:
        for cid, s in states.items():
            _apply_grain(s, grain_factors[cid])

    # --- Secondary tint pass (end colors for color animation) ---
    if has_color_anim:
        outer_start = _parse_hex(p.TINT_COLOR_OUTER)
        inner_start = _parse_hex(p.TINT_COLOR_INNER)
        override_outer = _parse_hex(outer_end) if outer_end is not None else outer_start
        override_inner = _parse_hex(inner_end) if inner_end is not None else inner_start

        # Stash primary result, reset colors to originals for the end-color pass.
        for s in states.values():
            s["colors_start"] = s["colors"].copy()
            s["colors"] = s["colors_orig"].copy()

        _run_tint_pass(states, arr, p, rng, noise_field, tint_noise,
                       depth_outer_px, depth_inner_px,
                       override_outer=override_outer, override_inner=override_inner)

        if sat_shift != 0.0:
            for s in states.values():
                _apply_saturation_shift(s, sat_shift)
        if grain_factors is not None:
            for cid, s in states.items():
                _apply_grain(s, grain_factors[cid])

        # Rename: colors = end result, colors_start back to colors.
        for s in states.values():
            s["colors_end"] = s["colors"].copy()
            s["colors"] = s["colors_start"]
            del s["colors_start"]


def _build_dissolve_scores(states, rng, H, W, p):
    """Return list of (cid, pixel_index, score). Higher score = survives longer (dissolves last)."""
    entries = []

    if p.DISSOLVE_PATTERN == "noise":
        grid_h = max(2, min(H, H // 8))
        grid_w = max(2, min(W, W // 8))
        grid = rng.random((grid_h, grid_w))
        row_coords = np.linspace(0, grid_h - 1, H)
        col_coords = np.linspace(0, grid_w - 1, W)
        upsampled = np.zeros((H, grid_w))
        for c in range(grid_w):
            upsampled[:, c] = np.interp(row_coords, np.arange(grid_h), grid[:, c])
        noise_field = np.zeros((H, W))
        for r in range(H):
            noise_field[r, :] = np.interp(col_coords, np.arange(grid_w), upsampled[r, :])

    elif p.DISSOLVE_PATTERN == "directional":
        rad = math.radians(p.DISSOLVE_DIRECTION)
        dir_vec = np.array([-math.cos(rad), math.sin(rad)])

    for cid, s in states.items():
        pixels = s["pixels"]
        n = len(pixels)
        if n == 0:
            continue

        if p.DISSOLVE_PATTERN == "random":
            scores = rng.random(n)

        elif p.DISSOLVE_PATTERN == "noise":
            rows = np.clip(pixels[:, 0], 0, H - 1)
            cols = np.clip(pixels[:, 1], 0, W - 1)
            scores = noise_field[rows, cols]

        elif p.DISSOLVE_PATTERN == "directional":
            dots = pixels @ dir_vec
            scores = -dots  # furthest in direction = lowest score = dissolves first

        elif p.DISSOLVE_PATTERN == "centrifugal":
            centroid = s["centroid"]
            dists = np.linalg.norm(pixels.astype(float) - centroid, axis=1)
            scores = -dists  # farther = dissolves sooner = lower score

        elif p.DISSOLVE_PATTERN == "centripetal":
            centroid = s["centroid"]
            scores = np.linalg.norm(pixels.astype(float) - centroid, axis=1)
            # closer to center = lower score = dissolves sooner

        elif p.DISSOLVE_PATTERN == "chunks":
            chunk_score = rng.random()
            scores = np.full(n, chunk_score)

        elif p.DISSOLVE_PATTERN == "gravity_aligned":
            rad = math.radians(p.GRAVITY_ANGLE)
            dir_vec = np.array([-math.cos(rad), math.sin(rad)])
            dots = pixels @ dir_vec
            scores = -dots

        else:
            scores = rng.random(n)

        for i, score in enumerate(scores):
            entries.append((cid, i, float(score)))

    return entries


def build_dissolve_schedule(states, rng, H, W, frames, p):
    """Compute per-pixel dropout frame indices. Returns dict[cid -> np.ndarray(n_pixels, int)].
    Pixel is hidden at render frame f when schedule[cid][i] <= f."""
    total_opaque = sum(len(s["pixels"]) for s in states.values())
    survive_count = min(total_opaque, max(1, int(total_opaque * p.DISSOLVE_MIN_PCT)))
    drop_count = total_opaque - survive_count

    # initialise all pixels as survivors (value = frames means mask > frame_idx is always True)
    schedule = {cid: np.full(len(s["pixels"]), frames, dtype=int) for cid, s in states.items()}

    if drop_count == 0:
        return schedule

    entries = _build_dissolve_scores(states, rng, H, W, p)
    entries.sort(key=lambda x: x[2])  # ascending: lowest score = first to vanish

    # Guaranteed-window stagger: every chunk gets proportional time to dissolve.
    # min_window_frames scales down as frame count grows (more frames = less % needed).
    _STAGGER_WIN_FRAMES = [4,    8,    16,   32,   64,   128,   256  ]
    _STAGGER_WIN_PCTS   = [0.50, 0.40, 0.30, 0.20, 0.10, 0.075, 0.05 ]
    pct = float(np.interp(frames, _STAGGER_WIN_FRAMES, _STAGGER_WIN_PCTS))
    min_window = max(1, round(pct * (frames - 1)))
    max_onset  = max(0, (frames - 1) - min_window)

    stagger   = getattr(p, "DISSOLVE_CHUNK_STAGGER", 0.0)
    curve_exp = 1.0 / max(p.DISSOLVE_CURVE, 1e-6)

    chunk_onsets = {}
    if stagger > 0.0:
        for cid in states:
            chunk_onsets[cid] = round(rng.random() * stagger * max_onset)
    else:
        for cid in states:
            chunk_onsets[cid] = 0

    for rank, (cid, pix_idx, _) in enumerate(entries[:drop_count]):
        t = rank / drop_count
        O = chunk_onsets[cid]
        available = (frames - 1) - O          # always >= min_window >= 1
        frame_val = O + max(1, round(available * (t ** curve_exp)))
        frame_val = min(frame_val, frames - 1)
        schedule[cid][pix_idx] = frame_val

    return schedule


def apply_frame_mask(frames, p):
    """Apply FRAME_MASK alpha mask to frames[1:] in-place. Frame 0 always unmasked."""
    import os
    from PIL import ImageFilter

    mask_name = getattr(p, "FRAME_MASK", None)
    if not mask_name or len(frames) <= 1:
        return

    from utils.paths import masks_dir
    mask_path = os.path.join(str(masks_dir()), mask_name)
    if not os.path.exists(mask_path):
        from utils.log import log
        log.warning("Frame mask %r not found in %s; rendering without it", mask_name, masks_dir())
        return

    fit       = getattr(p, "FRAME_MASK_FIT", "stretch")
    softness  = int(getattr(p, "FRAME_MASK_SOFTNESS", 0))
    flip      = getattr(p, "FRAME_MASK_FLIP", False)
    mirror    = getattr(p, "FRAME_MASK_MIRROR", False)
    rotate90  = getattr(p, "FRAME_MASK_ROTATE90", False)
    anim_mode = getattr(p, "FRAME_MASK_ANIM", "instant")
    total     = len(frames)
    W, H      = frames[0].size  # PIL size = (W, H)

    raw = Image.open(mask_path).convert("L")
    if rotate90:
        raw = raw.transpose(Image.ROTATE_270)  # 90 degrees clockwise
    rw, rh = raw.size

    if fit == "stretch":
        mask_img = raw.resize((W, H), Image.NEAREST)
    elif fit == "fit":
        scale = min(W / rw, H / rh)
        nw, nh = int(rw * scale), int(rh * scale)
        resized = raw.resize((nw, nh), Image.NEAREST)
        mask_img = Image.new("L", (W, H), 0)
        mask_img.paste(resized, ((W - nw) // 2, (H - nh) // 2))
    else:  # crop_center
        scale = max(W / rw, H / rh)
        nw, nh = int(rw * scale), int(rh * scale)
        resized = raw.resize((nw, nh), Image.NEAREST)
        x0 = (nw - W) // 2
        y0 = (nh - H) // 2
        mask_img = resized.crop((x0, y0, x0 + W, y0 + H))

    if flip:
        mask_img = mask_img.transpose(Image.FLIP_TOP_BOTTOM)
    if mirror:
        mask_img = mask_img.transpose(Image.FLIP_LEFT_RIGHT)
    if softness > 0:
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=softness))

    mask_arr = np.array(mask_img, dtype=np.float32) / 255.0  # (H, W), 0.0–1.0

    for i, frame in enumerate(frames):
        if i == 0:
            continue
        t = i / max(total - 1, 1)
        if anim_mode == "instant":
            opacity = 1.0
        elif anim_mode == "linear":
            opacity = t
        elif anim_mode == "early":
            opacity = min(1.0, t * 3.0)
        elif anim_mode == "late":
            opacity = max(0.0, (t - 0.5) * 2.0)
        elif anim_mode == "pulse":
            opacity = math.sin(math.pi * t)
        else:
            opacity = 1.0

        # Lerp: at opacity=0 mask has no effect (multiplier=1); at opacity=1 full mask applied
        effective = opacity * mask_arr + (1.0 - opacity)
        arr = np.array(frame)
        arr[:, :, 3] = np.clip(arr[:, :, 3] * effective, 0, 255).astype(np.uint8)
        frames[i] = Image.fromarray(arr)
