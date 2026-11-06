import numpy as np

from core.rendering import rotate_pixels

# Per-tick fraction of floor-parallel velocity and spin lost while a chunk skids on a floor.
_FLOOR_FRICTION = 0.35
# Floor-parallel speed (px/tick) below which a skidding chunk comes to rest.
_SLIDE_REST = 0.15


def simulate_step(states, W, H, p, gravity_dir, sprite_center=None):
    """Advance all chunk states by one physics tick. Mutates states in place."""
    gravity_strength  = p.GRAVITY_STRENGTH
    drag              = p.DRAG
    edge_zone         = p.EDGE_ZONE
    blast_mode        = p.BLAST_MODE
    bounce            = getattr(p, "BOUNCE", 0.0)
    spin_drag         = getattr(p, "SPIN_DRAG", 0.0)
    gravity_mode      = getattr(p, "GRAVITY_MODE", "directional")
    gravity_ramp_ticks = getattr(p, "GRAVITY_RAMP_TICKS", 0)

    for s in states.values():
        if s["settled"]:
            continue

        # Launch stagger: hold chunk at rest until its onset tick, then apply launch velocity.
        s["tick"] = s.get("tick", 0) + 1
        if s["tick"] <= s.get("onset", 0):
            s["angle"] += s["spin"]
            s["spin"] *= (1.0 - spin_drag)
            continue
        if s["tick"] == s.get("onset", 0) + 1 and "launch_vel" in s:
            s["vel"] = s["launch_vel"].copy()

        # Gravity ramp: hold center-relative forces at zero for the first N ticks,
        # giving chunks free-flight time before vortex/centripetal/orbital activates.
        chunk_tick = s.get("tick", 0) - s.get("onset", 0)
        grav_scale = 0.0 if (gravity_ramp_ticks > 0 and chunk_tick <= gravity_ramp_ticks) else 1.0

        if gravity_mode == "centripetal" and sprite_center is not None:
            current_pos = s["centroid"] + s["offset"]
            pull_vec = sprite_center - current_pos
            dist = float(np.linalg.norm(pull_vec))
            if dist > 0.5:
                s["vel"] += (pull_vec / dist) * gravity_strength * grav_scale

        elif gravity_mode == "repulsor" and sprite_center is not None:
            current_pos = s["centroid"] + s["offset"]
            push_vec = current_pos - sprite_center
            dist = float(np.linalg.norm(push_vec))
            if dist > 0.5:
                s["vel"] += (push_vec / dist) * gravity_strength * grav_scale

        elif gravity_mode == "orbital" and sprite_center is not None:
            current_pos = s["centroid"] + s["offset"]
            radial = current_pos - sprite_center
            dist = float(np.linalg.norm(radial))
            if dist > 0.5:
                radial_dir = radial / dist
                tangent = np.array([-radial_dir[1], radial_dir[0]])  # 90° CCW in (row,col)
                s["vel"] += tangent * gravity_strength * grav_scale

        elif gravity_mode == "vortex" and sprite_center is not None:
            current_pos = s["centroid"] + s["offset"]
            pull_vec = sprite_center - current_pos
            dist = float(np.linalg.norm(pull_vec))
            if dist > 0.5:
                pull_dir = pull_vec / dist
                tangent = np.array([-pull_dir[1], pull_dir[0]])  # 90° CCW
                # 80% centripetal / 20% tangential so the spiral decays inward to center.
                s["vel"] += pull_dir * (gravity_strength * 0.8) * grav_scale
                s["vel"] += tangent * (gravity_strength * 0.2) * grav_scale

        elif gravity_mode == "noise":
            # Per-chunk slowly-varying direction; seed+tick driven, always active
            angle = s.get("noise_seed", 0.0) * (2.0 * np.pi) + s.get("tick", 0) * 0.08
            s["vel"] += np.array([np.sin(angle), np.cos(angle)]) * gravity_strength

        else:
            s["vel"] += gravity_dir * gravity_strength

        # During the ramp window, skip drag so initial velocity carries chunks outward freely.
        _in_ramp = (gravity_ramp_ticks > 0 and grav_scale == 0.0
                    and gravity_mode in ("vortex", "centripetal", "orbital"))
        if not _in_ramp:
            s["vel"] *= (1.0 - drag * s.get("mass_drag", 1.0))

        s["spin"] *= (1.0 - spin_drag)
        s["angle"] += s["spin"]

        new_offset = s["offset"] + s["vel"]
        # Containment and settling test the chunk exactly as it will be drawn this
        # tick (rotated), so a spun chunk can't poke through a wall or the floor.
        rotated = rotate_pixels(s["pixels"].astype(float), s["centroid"], s["angle"])
        chunk_rows = rotated[:, 0]
        chunk_cols = rotated[:, 1]

        # Edge containment is skipped for inward/circular modes and centripetal gravity.
        # Vortex and noise keep containment active (all 4 walls) to prevent off-canvas escape.
        if (edge_zone > 0
                and blast_mode not in ("implode", "hollow_circle", "filled_circle")
                and gravity_mode not in ("centripetal", "repulsor", "orbital")):
            # With no floor (vortex/noise, or zero gravity) all 4 walls are contained;
            # otherwise the walls gravity points toward are floors, handled below.
            _no_floor = gravity_mode in ("vortex", "noise") or gravity_strength == 0
            _gd = np.zeros(2) if _no_floor else gravity_dir

            # Left wall: damps leftward (negative col) velocity.
            # Skip if gravity points left (_gd[1] < 0) — that is the settle wall.
            if _gd[1] >= 0:
                left_col = chunk_cols.min() + new_offset[1]
                if left_col < edge_zone and s["vel"][1] < 0:
                    s["vel"][1] *= max(0.0, left_col / edge_zone)

            # Right wall: damps rightward (positive col) velocity.
            if _gd[1] <= 0:
                right_col = chunk_cols.max() + new_offset[1]
                if right_col > (W - 1 - edge_zone) and s["vel"][1] > 0:
                    s["vel"][1] *= max(0.0, (W - 1 - right_col) / edge_zone)

            # Top wall: damps upward (negative row) velocity.
            if _gd[0] >= 0:
                top_row = chunk_rows.min() + new_offset[0]
                if top_row < edge_zone and s["vel"][0] < 0:
                    s["vel"][0] *= max(0.0, top_row / edge_zone)

            # Bottom wall: damps downward (positive row) velocity.
            if _gd[0] <= 0:
                bot_row = chunk_rows.max() + new_offset[0]
                if bot_row > (H - 1 - edge_zone) and s["vel"][0] > 0:
                    s["vel"][0] *= max(0.0, (H - 1 - bot_row) / edge_zone)

            new_offset = s["offset"] + s["vel"]

            # Hard stop at the contained walls: damping alone can't stop spin from
            # swinging a chunk's pixels past a wall it is already touching.
            for axis, limit, extent in ((0, H - 1, chunk_rows), (1, W - 1, chunk_cols)):
                lo = extent.min() + new_offset[axis]
                hi = extent.max() + new_offset[axis]
                if _gd[axis] >= 0 and lo < 0:
                    new_offset[axis] -= lo
                    s["vel"][axis] = max(s["vel"][axis], 0.0)
                elif _gd[axis] <= 0 and hi > limit:
                    new_offset[axis] -= hi - limit
                    s["vel"][axis] = min(s["vel"][axis], 0.0)

        if gravity_mode in ("centripetal", "vortex") and sprite_center is not None:
            # Settle when close to sprite center and nearly stopped.
            current_pos = s["centroid"] + new_offset
            dist = float(np.linalg.norm(sprite_center - current_pos))
            speed = float(np.linalg.norm(s["vel"]))
            if dist < 1.5 and speed < 0.3:
                s["vel"][:] = 0.0
                s["settled"] = True
        elif gravity_mode == "noise" or (
                gravity_mode in ("repulsor", "orbital") and sprite_center is not None):
            pass  # never-settling; sim runs to MAX_SIM_TICKS
        elif gravity_strength > 0:
            # Floors are the canvas walls gravity points toward (one wall for cardinal
            # gravity, two for diagonal). A chunk lands on a floor when its leading
            # (rotated) pixel would cross it this tick while moving into it — a chunk
            # moving away is never caught. Under diagonal gravity a chunk that has hit
            # one floor slides along it into the corner, settling once both hold it.
            # Also used as fallback when center-relative modes have sprite_center=None.
            resting = True
            on_floor = False
            for axis, limit, extent in ((0, H - 1, chunk_rows), (1, W - 1, chunk_cols)):
                g = gravity_dir[axis]
                if abs(g) < 1e-6:
                    continue
                if g > 0:
                    overshoot = extent.max() + new_offset[axis] - limit
                else:
                    overshoot = -(extent.min() + new_offset[axis])
                into_wall = s["vel"][axis] * np.sign(g)
                if overshoot >= 0.0 and into_wall > 0.0:
                    new_offset[axis] -= np.sign(g) * overshoot
                    rebound = into_wall * bounce
                    if rebound > max(gravity_strength * abs(g), 0.3):
                        # Reflect off the floor, attenuated by BOUNCE.
                        s["vel"][axis] = -np.sign(g) * rebound
                        resting = False
                    else:
                        # Too slow to visibly leave the floor again (or BOUNCE = 0).
                        s["vel"][axis] = 0.0
                        on_floor = True
                else:
                    resting = False

            if on_floor:
                # Sliding along the floor: friction bleeds off motion parallel to it
                # (and spin), so split halves skid apart instead of freezing on contact.
                for axis in (0, 1):
                    if abs(gravity_dir[axis]) < 1e-6:
                        s["vel"][axis] *= (1.0 - _FLOOR_FRICTION)
                        if abs(s["vel"][axis]) >= _SLIDE_REST:
                            resting = False
                s["spin"] *= (1.0 - _FLOOR_FRICTION)
            if resting:
                s["vel"][:] = 0.0
                s["settled"] = True

        s["offset"] = new_offset
