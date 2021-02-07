#!/usr/bin/env python3
# Local Library
from cairo_util import set_rgb

# Third-Party Library
import gi
gi.require_version("Gtk", "3.0")

from cairo import Context
from gi.repository import Gtk


class HeaderLabel(Gtk.HBox):
    def __init__(self, color: str, **kwargs):
        super().__init__()

        self.color = color

        header = Gtk.DrawingArea()
        header.set_size_request(20, -1)
        header.connect("draw", self._draw)

        label = Gtk.Label(**kwargs)

        self.pack_start(header, False, False, 0)
        self.pack_start(label, False, True, 10)

    def _draw(self, widget: Gtk.Widget, ctx: Context):
        height = widget.get_allocated_height()

        ctx.scale(20, height)
        ctx.rectangle(0, 0, 1, 1)
        set_rgb(ctx, self.color)

        ctx.fill()

class LabelBox(Gtk.VBox):
    def __init__(
        self,
        label_1: str,
        label_2: str,
        color_1: str,
        color_2: str
    ):
        super().__init__(spacing=10)

        self.pack_start(HeaderLabel(color_1, label=label_1), True, True, 0)
        self.pack_start(HeaderLabel(color_2, label=label_2), True, True, 0)
