#!/usr/bin/env python3
# Standard Library
from math import pi
from typing import Optional

# Local Library
from cairo_util import set_rgb

# Third-Party Library
import gi
gi.require_version("Gtk", "3.0")

from cairo import Context, LINE_CAP_ROUND
from gi.repository import Gtk


class Circle(Gtk.AspectFrame):
    def __init__(
        self,
        color: str,
        track_color: str,
        line_width: float = 0.02,
        size: float = 2 * pi,
        start: float = 0
    ):
        super().__init__(obey_child=True)
        self.set_shadow_type(Gtk.ShadowType.NONE)

        self.circle = Gtk.DrawingArea()
        self.circle.connect("draw", self._draw)
        self.add(self.circle)

        self.progress = 0.0
        self.color = color
        self.track_color = track_color
        self.line_width = line_width
        self.size = size
        self.start = start

    def set_progress(self, progress: float):
        self.progress = progress
        self.circle.queue_draw()

    def _draw(self, widget: Gtk.Widget, ctx: Context):
        allocated_width = widget.get_allocated_width()
        allocated_height = widget.get_allocated_height()
        width = allocated_width if allocated_width < allocated_height else allocated_height

        ctx.scale(width, width)
        ctx.set_line_width(self.line_width)
        ctx.set_line_cap(LINE_CAP_ROUND)

        point = self.size * (self.progress / 100) + self.start
        end = self.size + self.start

        ctx.arc(0.5, 0.5, 0.4, point, end)
        set_rgb(ctx, self.track_color)
        ctx.stroke()

        ctx.arc(0.5, 0.5, 0.4, self.start, point)
        set_rgb(ctx, self.color)
        ctx.stroke()

class Chart(Gtk.VBox):
    def __init__(self, name: str, color: str, track_color: str):
        super().__init__(spacing=10)

        self.circle = Circle(color, track_color, size = pi * 5/3, start = pi * 2/3)

        self.label = Gtk.Label()

        self.pack_start(Gtk.Label(label=name), False, False, 0)
        self.pack_start(self.circle, True, True, 0)
        self.pack_start(self.label, False, False, 0)
