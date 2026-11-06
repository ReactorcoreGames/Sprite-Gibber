import math
import tkinter as tk

from gui.theme import PALETTE, FONT_TINY

_SIZE = 240
_HALF = _SIZE // 2
_RING_RADIUS = 92
_CENTER_DOT_R = 5
_ARROWHEAD_SIZE = 11
_STRENGTH_MAX = 5.0

# Color stops for arrow (green → yellow → red) across strength [0 .. 5]
_C_LOW  = (0x44, 0xCC, 0x44)   # strength 0
_C_MID  = (0xFF, 0xCC, 0x00)   # strength 2.5
_C_HIGH = (0xFF, 0x33, 0x33)   # strength 5.0


def _lerp_color(c1, c2, t):
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def _arrow_color(strength):
    s = max(0.0, min(5.0, float(strength)))
    if s <= 2.5:
        return _lerp_color(_C_LOW, _C_MID, s / 2.5)
    else:
        return _lerp_color(_C_MID, _C_HIGH, (s - 2.5) / 2.5)


class DirectionStrengthWidget(tk.Canvas):
    """120×120 compass dial — shows gravity angle and strength as an arrow."""

    def __init__(self, parent, angle_var: tk.IntVar, strength_var: tk.DoubleVar, **kwargs):
        kwargs.setdefault("width", _SIZE)
        kwargs.setdefault("height", _SIZE)
        kwargs.setdefault("bg", PALETTE["bg_base"])
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(parent, **kwargs)

        self._angle_var = angle_var
        self._strength_var = strength_var

        self.bind("<Button-1>", self._on_drag)
        self.bind("<B1-Motion>", self._on_drag)

        angle_var.trace_add("write", lambda *_: self._redraw())
        strength_var.trace_add("write", lambda *_: self._redraw())

        self._redraw()

    # ------------------------------------------------------------------ #

    def _on_drag(self, event):
        dx = event.x - _HALF
        dy = event.y - _HALF
        if dx == 0 and dy == 0:
            return
        # atan2 with y-axis flipped: 0° = up
        angle_rad = math.atan2(dx, -dy)
        angle_deg = math.degrees(angle_rad) % 360
        ctrl_held = (event.state & 0x0004) != 0
        if ctrl_held:
            angle_deg = round(angle_deg / 45) * 45 % 360
        self._angle_var.set(int(round(angle_deg)) % 360)

        dist = math.hypot(dx, dy)
        raw = (dist / _RING_RADIUS) * _STRENGTH_MAX
        self._strength_var.set(round(min(raw, _STRENGTH_MAX) * 10) / 10)

    def _redraw(self):
        self.delete("all")

        cx, cy = _HALF, _HALF
        r = _RING_RADIUS
        p = PALETTE

        # Background circle
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                         fill=p["bg_surface"], outline=p["accent_glow"], width=1)

        # Cardinal labels outside ring
        label_r = r + 14
        for label, angle_deg in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
            lx = cx + label_r * math.sin(math.radians(angle_deg))
            ly = cy - label_r * math.cos(math.radians(angle_deg))
            self.create_text(lx, ly, text=label, fill=p["text_secondary"],
                             font=FONT_TINY, anchor="center")

        # Arrow
        try:
            angle = float(self._angle_var.get())
            strength = float(self._strength_var.get())
        except (tk.TclError, ValueError):
            angle, strength = 0.0, 0.0

        arrow_len = (strength / 5.0) * r * 0.9

        if arrow_len > 1:
            color = _arrow_color(strength)
            dx = math.sin(math.radians(angle))
            dy = -math.cos(math.radians(angle))

            tip_x = cx + dx * arrow_len
            tip_y = cy + dy * arrow_len

            # Shaft
            self.create_line(cx, cy, tip_x, tip_y, fill=color, width=2)

            # Filled-triangle arrowhead
            perp_x = -dy
            perp_y = dx
            h = _ARROWHEAD_SIZE
            w = _ARROWHEAD_SIZE * 0.5
            base_x = tip_x - dx * h
            base_y = tip_y - dy * h
            pts = [
                tip_x, tip_y,
                base_x + perp_x * w, base_y + perp_y * w,
                base_x - perp_x * w, base_y - perp_y * w,
            ]
            self.create_polygon(pts, fill=color, outline="")

        # Center dot (always on top)
        self.create_oval(cx - _CENTER_DOT_R, cy - _CENTER_DOT_R,
                         cx + _CENTER_DOT_R, cy + _CENTER_DOT_R,
                         fill=p["text_secondary"], outline="")
