import math
import numpy as np


def _biased_seed_indices(coords, num_chunks, rng, mode, strength):
    n = len(coords)

    if mode in ("halves-h", "halves-v", "quadrants"):
        rows = coords[:, 0]
        cols = coords[:, 1]
        row_mid = (rows.min() + rows.max()) / 2.0
        col_mid = (cols.min() + cols.max()) / 2.0

        if mode == "halves-h":
            zones = [rows < row_mid, rows >= row_mid]
        elif mode == "halves-v":
            zones = [cols < col_mid, cols >= col_mid]
        else:  # quadrants
            zones = [
                (rows < row_mid) & (cols < col_mid),
                (rows < row_mid) & (cols >= col_mid),
                (rows >= row_mid) & (cols < col_mid),
                (rows >= row_mid) & (cols >= col_mid),
            ]

        num_zones = len(zones)
        base_quota = num_chunks // num_zones
        quotas = [base_quota] * num_zones
        for i in range(num_chunks - base_quota * num_zones):
            quotas[i] += 1

        chosen = []
        available = np.ones(n, dtype=bool)

        for zone_mask, quota in zip(zones, quotas):
            if quota == 0:
                continue
            zone_w = zone_mask.astype(float)
            weights = strength * zone_w + (1.0 - strength) * np.ones(n, dtype=float)
            weights[~available] = 0.0
            total = weights.sum()
            if total == 0.0:
                weights = available.astype(float)
                total = weights.sum()
            weights /= total
            k = min(quota, int(available.sum()))
            if k == 0:
                continue
            picked = rng.choice(n, size=k, replace=False, p=weights)
            chosen.extend(picked.tolist())
            available[picked] = False

        return np.array(chosen, dtype=int)

    else:  # core or shell
        centroid = coords.mean(axis=0)
        diffs = coords - centroid
        dist = np.sqrt((diffs ** 2).sum(axis=1))
        max_dist = dist.max() or 1.0
        dist_norm = dist / max_dist

        if mode == "core":
            base_weights = 1.0 - dist_norm
        else:  # shell
            base_weights = dist_norm

        uniform = np.ones(n, dtype=float)
        weights = strength * base_weights + (1.0 - strength) * uniform
        total = weights.sum()
        if total == 0.0:
            weights = uniform
            total = float(n)
        weights /= total
        return rng.choice(n, size=num_chunks, replace=False, p=weights)


def voronoi_chunks(opaque_coords, num_chunks, rng,
                   chunk_bias="none", chunk_bias_strength=0.0,
                   chunk_shape_stretch=1.0, chunk_shape_angle=0):
    n = len(opaque_coords)
    if n == 0:
        return {}
    num_chunks = min(num_chunks, n)

    if chunk_bias == "none" or chunk_bias_strength == 0.0:
        seed_indices = rng.choice(n, size=num_chunks, replace=False)
    else:
        seed_indices = _biased_seed_indices(opaque_coords, num_chunks, rng, chunk_bias, chunk_bias_strength)

    seeds = opaque_coords[seed_indices]
    diff = opaque_coords[:, None, :] - seeds[None, :, :]  # (N, K, 2)

    if chunk_shape_stretch != 1.0:
        rad = math.radians(chunk_shape_angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        dr = diff[..., 0]
        dc = diff[..., 1]
        d_stretch =  dr * cos_a + dc * sin_a
        d_perp    = -dr * sin_a + dc * cos_a
        d_stretch /= chunk_shape_stretch
        dist2 = d_stretch ** 2 + d_perp ** 2
    else:
        dist2 = (diff ** 2).sum(axis=2)

    assignments = dist2.argmin(axis=1)
    chunks = {}
    for i in range(num_chunks):
        mask = assignments == i
        if mask.any():
            chunks[i] = opaque_coords[mask]
    return chunks


def chunk_centroid(pixels):
    return pixels.mean(axis=0)


def make_gravity_dir(gravity_angle):
    """Return (row, col) unit vector for gravity_angle (0=up, 90=right, 180=down, 270=left)."""
    rad = math.radians(gravity_angle)
    vec = np.array([-math.cos(rad), math.sin(rad)])
    # Snap float noise (sin(180°) = 1.2e-16) to exact zero: wall containment keys off the
    # sign of each component, and a stray epsilon silently disabled a whole wall.
    vec[np.abs(vec) < 1e-9] = 0.0
    return vec


def initial_velocity(centroid, sprite_center, W, H, rng, p):
    dy = centroid[0] - sprite_center[0]
    dx = centroid[1] - sprite_center[1]
    dist = math.sqrt(dx * dx + dy * dy) or 1.0

    blast_mode = p.BLAST_MODE
    explode    = p.EXPLODE
    spread     = p.SPREAD

    if blast_mode == "explode":
        vx = (dx / dist + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        vy = (dy / dist + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        return np.array([vy, vx], dtype=float)

    if blast_mode == "implode":
        vx = (-dx / dist + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        vy = (-dy / dist + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        return np.array([vy, vx], dtype=float)

    if blast_mode == "hollow_circle":
        # Tangent to the radial vector (counter-clockwise rotation in image space).
        tx = -dy / dist  # tangent col component
        ty =  dx / dist  # tangent row component
        vx = (tx + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        vy = (ty + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        return np.array([vy, vx], dtype=float)

    if blast_mode == "filled_circle":
        # Radial outward, speed proportional to distance from center.
        half_diag = math.sqrt((H / 2.0) ** 2 + (W / 2.0) ** 2) or 1.0
        speed = (dist / half_diag) * explode
        vx = (dx / dist) * speed
        vy = (dy / dist) * speed
        return np.array([vy, vx], dtype=float)

    if blast_mode == "shatter":
        return np.zeros(2, dtype=float)

    if blast_mode == "x_split":
        row_dir = -1.0 if centroid[0] < sprite_center[0] else 1.0
        col_dir = -1.0 if centroid[1] < sprite_center[1] else 1.0
        length = math.sqrt(2.0)
        vx = (col_dir / length + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        vy = (row_dir / length + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        return np.array([vy, vx], dtype=float)

    if blast_mode == "vertical_split":
        row_dir = -1.0 if centroid[0] < sprite_center[0] else 1.0
        vy = (row_dir + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        vx = rng.uniform(-spread * 0.5, spread * 0.5) * explode
        return np.array([vy, vx], dtype=float)

    if blast_mode == "horizontal_split":
        col_dir = -1.0 if centroid[1] < sprite_center[1] else 1.0
        vx = (col_dir + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        vy = rng.uniform(-spread * 0.5, spread * 0.5) * explode
        return np.array([vy, vx], dtype=float)

    if blast_mode == "burst":
        # Each chunk bursts outward in a random direction independent of sprite-center
        # position — uniform push for all chunks, so central chunks move too (unlike "explode").
        angle = rng.uniform(0, 2 * math.pi)
        vx = (math.cos(angle) + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        vy = (math.sin(angle) + rng.uniform(-spread * 0.5, spread * 0.5)) * explode
        return np.array([vy, vx], dtype=float)

    raise ValueError(f"Unknown BLAST_MODE: {blast_mode!r}")
