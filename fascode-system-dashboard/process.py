#!/usr/bin/env python3
# Standard Library
from typing import Optional, Union, Callable

# Local Library
from util import to_human

# Third-Party Library
import gi
gi.require_versions(
    {
        "Gio": "2.0",
        "Gtk": "3.0"
    }
)

from gi.repository import Gio, Gtk

APP = dict[str, Union[Gio.DesktopAppInfo, float, int]]

class ProcessRow(Gtk.ListBoxRow):
    def __init__(
        self,
        name: str,
        data: Union[int, float],
        icon: Optional[Gio.Icon] = None
    ):
        super().__init__()

        self.label = Gtk.Label()
        self.data = data

        box = Gtk.HBox(spacing=10)

        if icon:
            box.pack_start(
                Gtk.Image().new_from_gicon(icon, Gtk.IconSize.MENU),
                False,
                True,
                0
            )

        box.pack_start(Gtk.Label(label=name), False, True, 0)
        box.pack_end(self.label, False, True, 0)

        self.add(box)


class Process(Gtk.ListBox):
    def __init__(
        self,
        key: str,
        text_func: Callable[[Gtk.Widget, APP], None]
    ):
        super().__init__()

        self.key = key
        self.text_func = text_func

        self.map = {}

    def update(self, process: dict[str, APP]):
        self.invalidate_sort()

        for name, info in process.items():
            if not name in self.map:
                icon = info["app"].get_icon() if info["app"] else None
                row = ProcessRow(name, info[self.key], icon)

                self.map[name] = row
                self.add(row)
                self.show_all()

            self.text_func(self.map[name].label, info)

        remove = []

        for name, row in self.map.items():
            if not name in process:
                self.remove(row)
                self.show_all()
                remove.append(name)

        for name in remove:
            self.map.pop(name)


class CPUProcess(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.process = Process("cpu", self._text)
        self.process.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(self.process)

    def _text(self, widget: Gtk.Widget, data: APP):
        text = round(data["cpu"], 1)
        widget.set_text(f"{text}%")


class MemoryProcess(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.process = Process("memory", self._text)
        self.process.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(self.process)

    def _text(self, widget: Gtk.Widget, data: APP):
        text = to_human(data["memory"])
        widget.set_text(f"{text}B")
