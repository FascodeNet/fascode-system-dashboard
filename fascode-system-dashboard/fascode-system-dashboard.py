#!/usr/bin/env python3
# Standard Library
import gettext

# Local Library
import util
from application import App, AppWindow
from circle import Chart
from graph import Graph, VariableGraph
from label import HeaderLabel, LabelBox
from process import CPUProcess, MemoryProcess
from speed import SpeedBox

# Third-Party Library
import gi
gi.require_versions(
    {
        "Dazzle": "1.0",
        "GLib": "2.0",
        "Gtk": "3.0"
    }
)

from gi.repository import Dazzle, GLib, Gtk


CPU_COLOR = [
    "#73D216",
    "#F57900",
    "#3465A4",
    "#EF2929",
    "#75507B",
    "#CE5C00",
    "#C17D11",
    "#CC0000"
]


gettext.textdomain("fascode-system-dashboard")
_ = gettext.gettext

class Main(AppWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        GLib.timeout_add(500, self.update)

        # Chart
        # CPU
        self.cpu_circle = Chart(
            _("CPU"),
            "#f44336",
            "#9E9E9E"
        )

        # Memory
        self.memory_circle = Chart(
            _("Memory"),
            "#E91E63",
            "#9E9E9E"
        )

        # Swap
        self.swap_circle = Chart(
            _("Swap"),
            "#4CAF50",
            "#9E9E9E"
        )

        # Speed
        # Disk
        self.disk_speed = SpeedBox(
            _("Disk"),
            _("Read Speed"),
            _("Write Speed"),
            "#9C27B0",
            "#FF9800"
        )

        # Network
        self.network_speed = SpeedBox(
            _("Network"),
            _("Send Speed"),
            _("Recive Speed"),
            "#3F51B5",
            "#FF5722"
        )

        # Finalize
        speed = Gtk.VBox(spacing=10)
        speed.set_homogeneous(True)
        speed.pack_start(self.disk_speed, True, True, 0)
        speed.pack_start(self.network_speed, True, True, 0)

        # Process List
        # CPU
        self.process_cpu = CPUProcess()

        # Memory
        self.process_memory = MemoryProcess()

        # Graph
        # Label
        cpu_label = Gtk.VBox(spacing=10)

        for number in range(util.get_cpu_count()):
            cpu_label.pack_start(
                HeaderLabel(CPU_COLOR[number], label=f"CPU{number}"),
                True,
                True,
                0
            )

        memory_label = LabelBox(
            _("Memory"),
            _("Swap"),
            "#E91E63",
            "#4CAF50"
        )

        disk_label = LabelBox(
            _("Read Speed"),
            _("Write Speed"),
            "#9C27B0",
            "#FF9800"
        )

        network_label = LabelBox(
            _("Send Speed"),
            _("Recive Speed"),
            "#3F51B5",
            "#FF5722"
        )

        # Memory
        self.memory_graph = Graph(
            "#E91E63",
            "#4CAF50"
        )

        # Disk
        self.disk_graph = VariableGraph(
            "#9C27B0",
            "#FF9800"
        )

        # Network
        self.network_graph = VariableGraph(
            "#3F51B5",
            "#FF5722"
        )

        # Main Layout 1
        # Layout 1
        layout_1 = Gtk.HBox(spacing=10)
        layout_1.set_homogeneous(True)
        layout_1.pack_start(self.cpu_circle, True, True, 0)
        layout_1.pack_start(self.memory_circle, True, True, 0)
        layout_1.pack_start(self.swap_circle, True, True, 0)
        layout_1.pack_start(speed, True, True, 0)

        # Layout 2
        layout_2 = Gtk.HBox(spacing=10)
        layout_2.set_homogeneous(True)
        layout_2.pack_start(self.process_cpu, True, True, 0)
        layout_2.pack_start(self.process_memory, True, True, 0)

        # Finalize
        main_layout_1 = Gtk.VBox(spacing=10)
        main_layout_1.set_homogeneous(True)
        main_layout_1.pack_start(layout_1, True, True, 0)
        main_layout_1.pack_start(layout_2, True, True, 0)

        # Main Layout 2
        # Layout 1
        layout_1 = Gtk.VBox(spacing=10)
        layout_1.set_homogeneous(True)
        layout_1.pack_start(cpu_label, True, True, 0)
        layout_1.pack_start(memory_label, True, True, 0)
        layout_1.pack_start(disk_label, True, True, 0)
        layout_1.pack_start(network_label, True, True, 0)

        # Layout 2
        layout_2 = Gtk.VBox(spacing=10)
        layout_2.set_homogeneous(True)
        layout_2.pack_start(Dazzle.CpuGraph(), True, True, 0)
        layout_2.pack_start(self.memory_graph, True, True, 0)
        layout_2.pack_start(self.disk_graph, True, True, 0)
        layout_2.pack_start(self.network_graph, True, True, 0)

        # Finalize
        main_layout_2 = Gtk.HBox(spacing=10)
        main_layout_2.pack_start(layout_1, False, False, 0)
        main_layout_2.pack_start(layout_2, True, True, 0)

        # Stack
        self.stack = Gtk.Stack()
        self.stack.add_titled(main_layout_1, "circle", _("Overview"))
        self.stack.add_titled(main_layout_2, "graph", _("Graph"))

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)

        # Finalize
        self.header.add(stack_switcher)
        self.main.add(self.stack)

        self.update()
        self.show_all()

    def update(self):
        memory = util.get_memory()
        swap = util.get_swap()
        disk_r, disk_w = util.get_disk_speed()
        net_s, net_r = util.get_network_speed()

        if self.stack.get_visible_child_name() == "circle":
            # Chart
            # CPU
            cpu_percent = util.get_cpu_usage(False)

            self.cpu_circle.circle.set_progress(cpu_percent)
            self.cpu_circle.label.set_text(f"{cpu_percent}%")

            # Memory
            memory_used = util.to_human(memory.used)
            memory_total = util.to_human(memory.total)

            self.memory_circle.circle.set_progress(memory.percent)
            self.memory_circle.label.set_text(
                f"{memory_used}B/{memory_total}B"
            )

            # Swap
            swap_used = util.to_human(swap.used)
            swap_total = util.to_human(swap.total)

            self.swap_circle.circle.set_progress(swap.percent)
            self.swap_circle.label.set_text(f"{swap_used}B/{swap_total}B")

            # Speed
            # Disk
            self.disk_speed.label_1.set_text(util.to_human(disk_r) + "B/s")
            self.disk_speed.label_2.set_text(util.to_human(disk_w) + "B/s")

            # Network
            self.network_speed.label_1.set_text(
                util.to_human(net_s, False) + "bps"
            )

            self.network_speed.label_2.set_text(
                util.to_human(net_r, False) + "bps"
            )

            # Process
            process = util.get_process()

            # CPU
            self.process_cpu.process.update(process)

            # Memory
            self.process_memory.process.update(process)

        # Graph
        # Memory
        self.memory_graph.add(memory.percent, swap.percent)

        # Disk
        self.disk_graph.add(disk_r, disk_w)

        # Network
        self.network_graph.add(net_s, net_r)

        return True


if __name__ == "__main__":
    app = App("Fascode System Dashboard", Main)
    app.run()
