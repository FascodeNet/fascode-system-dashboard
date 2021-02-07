#!/usr/bin/env python3
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


class Graph(Dazzle.GraphView):
    def __init__(self, color_1: str, color_2: str):
        super().__init__()

        self.model = Dazzle.GraphModel(value_min=0.0, value_max=100.0)
        self.model.add_column(Dazzle.GraphColumn(name="0", value_type=float))
        self.model.add_column(Dazzle.GraphColumn(name="1", value_type=float))

        self.add_renderer(Dazzle.GraphLineRenderer(column=0, stroke_color=color_1))
        self.add_renderer(Dazzle.GraphLineRenderer(column=1, stroke_color=color_2))
        self.set_model(self.model)
    
    def add(self, value_1: float, value_2: float):
        row = self.model.push(GLib.get_monotonic_time())

        self.model.iter_set(row, 0, value_1)
        self.model.iter_set(row, 1, value_2)


class VariableGraph(Dazzle.GraphView):
    def __init__(self, color_1: str, color_2: str):
        super().__init__()

        self.db = [[], []]

        self.model = Dazzle.GraphModel(value_min=0.0, value_max=100.0)
        self.model.add_column(Dazzle.GraphColumn(name="0", value_type=float))
        self.model.add_column(Dazzle.GraphColumn(name="1", value_type=float))

        self.add_renderer(Dazzle.GraphLineRenderer(column=0, stroke_color=color_1))
        self.add_renderer(Dazzle.GraphLineRenderer(column=1, stroke_color=color_2))
        self.set_model(self.model)

    def add(self, value_1: float, value_2: float):
        row = self.model.push(GLib.get_monotonic_time())

        self.model.iter_set(row, 0, value_1)
        self.model.iter_set(row, 1, value_2)

        self.db[0].append(value_1)
        self.db[1].append(value_2)

        if len(self.db[0]) > 120:
            self.db[0].pop(0)
            self.db[1].pop(0)

        value_1_max = max(self.db[0])
        value_2_max = max(self.db[1])

        self.model.props.value_max = value_1_max if value_1_max > value_2_max else value_2_max
