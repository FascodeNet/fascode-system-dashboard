#!/usr/bin/env python3
# Third-Party Library
import gi
gi.require_versions(
    {
        "Gio": "2.0",
        "Gtk": "3.0"
    }
)

from gi.repository import Gio, Gtk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)

        self.header = Gtk.VBox()
        self.main = Gtk.VBox()
        self.footer = Gtk.VBox()

        layout = Gtk.VBox()
        layout.set_spacing(10)
        layout.pack_start(self.header, False, True, 0)
        layout.pack_start(self.main, True, True, 0)
        layout.pack_start(self.footer, False, True, 0)

        self.add(layout)


class App(Gtk.Application):
    def __init__(self, application_name: str, window: Gtk.ApplicationWindow):
        application_id = application_name.replace(" ", "_").replace("Fascode", "").lower()

        super().__init__(
            application_id=f"org.fascode.{application_id}",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.application_name = application_name
        self.window = window

    def do_activate(self):
        window = self.window(
            application=self,
            title=self.application_name
        )

        window.present()
