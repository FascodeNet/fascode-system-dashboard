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
from gi.repository import Gtk, Gdk


class Circle(Gtk.DrawingArea):
    def __init__(
        self,
        color: str,
        track_color: str,
        size: float = 2 * pi,
        start: float = 0,
    ):
        super().__init__()

        self.progress = 0.0
        self.color = color
        self.track_color = track_color
        self.size = size
        self.start = start

    def set_progress(self, progress: float):
        self.progress = progress
        self.queue_draw()

    def do_draw(self, ctx: Context):
        allocation = self.get_allocation()
        width = allocation.width / 2 if allocation.width < allocation.height else allocation.height / 2

        ctx.set_line_width(width / 10)
        ctx.set_line_cap(LINE_CAP_ROUND)

        point = self.size * (self.progress / 100) + self.start
        end = self.size + self.start

        ctx.arc(allocation.width / 2, allocation.height / 2, width * 0.9, point, end)
        set_rgb(ctx, self.track_color)
        ctx.stroke()

        ctx.arc(allocation.width / 2, allocation.height / 2, width * 0.9, self.start, point)
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
