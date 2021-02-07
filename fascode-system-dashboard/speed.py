#!/usr/bin/env python3
# Local Library
from label import HeaderLabel

# Third-Party Library
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

class SpeedBox(Gtk.VBox):
    def __init__(
        self,
        title: str,
        label_1: str,
        label_2: str,
        color_1: str,
        color_2: str
    ):
        super().__init__(spacing=10)

        self.label_1 = Gtk.Label()
        self.label_2 = Gtk.Label()

        layout_1 = Gtk.HBox()
        layout_1 .pack_start(HeaderLabel(color_1, label=label_1), True, True, 0)
        layout_1 .pack_end(self.label_1, True, True, 0)

        layout_2 = Gtk.HBox()
        layout_2.pack_start(HeaderLabel(color_2, label=label_2), True, True, 0)
        layout_2.pack_end(self.label_2, True, True, 0)

        self.set_homogeneous(True)
        self.pack_start(Gtk.Label(label=title), True, True, 0)
        self.pack_start(layout_1, True, True, 0)
        self.pack_start(layout_2, True, True, 0)
