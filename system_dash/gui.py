# Standard Library
from math import pi, ceil

# Local Library
from .circle import (
    CPUCircle,
    MemoryCircle,
    DiskCircle,
    NetworkCircle
)

from .table import ProcessTable

from .util import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_speed,
    get_network_speed,
    get_process,
    Human
)

# Third-Party Library
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gio

class system_dash_window(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_default_size(500, 300)

        GLib.timeout_add_seconds(1, self.update)

        self.cpu_circle = CPUCircle(
            (158, 158, 158),
            (255, 255, 255),
            color=(63, 81, 181),
            track_color=(158, 158, 158)
        )

        cpu_label = Gtk.Label(label="CPU")
        cpu_box = Gtk.VBox()
        cpu_box.pack_start(self.cpu_circle, True, True, 0)
        cpu_box.pack_start(cpu_label, False, False, 0)

        self.memory_circle = MemoryCircle(
            (158, 158, 158),
            (255, 255, 255),
            color=(0, 188, 212),
            track_color=(158, 158, 158)
        )

        memory_label = Gtk.Label(label="Memory")
        memory_box = Gtk.VBox()
        memory_box.pack_start(self.memory_circle, True, True, 0)
        memory_box.pack_start(memory_label, False, False, 0)

        self.disk_db = [(0, 0)]

        self.disk_circle = DiskCircle(
            (158, 158, 158),
            (255, 255, 255),
            (76, 175, 80),
            (255, 152, 0),
            color_1=(76, 175, 80),
            color_2=(255, 152, 0),
            track_color=(158, 158, 158)
        )

        disk_label = Gtk.Label(label="Disk")
        disk_box = Gtk.VBox()
        disk_box.pack_start(self.disk_circle, True, True, 0)
        disk_box.pack_start(disk_label, False, False, 0)

        self.network_db = [(0, 0)]

        self.network_circle = NetworkCircle(
            (158, 158, 158),
            (255, 255, 255),
            (233, 30, 99),
            (139, 195, 74),
            color_1=(233, 30, 99),
            color_2=(139, 195, 74),
            track_color=(158, 158, 158)
        )

        network_label = Gtk.Label(label="Network")
        network_box = Gtk.VBox()
        network_box.pack_start(self.network_circle, True, True, 0)
        network_box.pack_start(network_label, False, False, 0)

        box = Gtk.HBox(spacing=10)
        box.set_homogeneous(True)
        box.pack_start(cpu_box, True, True, 0)
        box.pack_start(memory_box, True, True, 0)
        box.pack_start(disk_box, True, True, 0)
        box.pack_start(network_box, True, True, 0)

        self.process_table = ProcessTable()

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.process_table)

        vbox = Gtk.VBox(spacing=10)
        vbox.set_homogeneous(True)
        vbox.pack_start(box, True, True, 0)
        vbox.pack_start(scroll, True, True, 0)

        self.update()

        self.add(vbox)
        self.show_all()

    def update(self):
        cpu_usage = get_cpu_usage(False)
        memory = get_memory_usage()
        disk_speed = get_disk_speed()
        network_speed = get_network_speed()

        self.disk_db.append(disk_speed)
        self.network_db.append(network_speed)

        if len(self.network_db) > 60:
            self.disk_db.pop(0)
            self.network_db.pop(0)

        self.cpu_circle.set_progress(cpu_usage)

        self.memory_circle.set_progress(
            memory.percent,
            {
                "used": str(Human(memory.used)),
                "total": str(Human(memory.total))
            }
        )

        self.disk_circle.set_progress(
            disk_speed[0],
            disk_speed[1],
            max([i[0] for i in self.disk_db]),
            max([i[1] for i in self.disk_db]),
            {
                "read": str(Human(disk_speed[0], "B/s")),
                "write": str(Human(disk_speed[1], "B/s"))
            }
        )

        self.network_circle.set_progress(
            network_speed[0],
            network_speed[1],
            max([i[0] for i in self.network_db]),
            max([i[1] for i in self.network_db]),
            {
                "sent": str(Human(network_speed[0], "bps")),
                "recive": str(Human(network_speed[1], "bps"))
            }
        )

        self.process_table.update(get_process())

        return True


class system_dash(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="org.fascode.systemdashboard",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = system_dash_window(
                application=self,
                title="System Dash"
            )

        self.window.present()

def main():
    app = system_dash()
    app.run()
