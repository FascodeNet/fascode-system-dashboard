# Standard Library
from math import pi
from typing import Callable, Optional

# Local Library
from .cairo_util import set_rgb, show_text
from .util import Human

# Third-Party Library
import cairo
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

TEXT_DRAW_FUNCTION = Callable[[cairo.Context, Optional[dict[str, str]]], None]

class Circle(Gtk.DrawingArea):
    def __init__(
        self,
        color: tuple[int] = (0, 0, 0),
        track_color: tuple[int] = (255, 255, 255),
        line_width: float = 0.02,
        size: float = 2 * pi,
        start: float = 0,
        text_draw: Optional[TEXT_DRAW_FUNCTION] = None,
        text_dict: Optional[dict[str, str]] = None
    ):
        super().__init__()

        self.progress = 0
        self.color = color
        self.track_color = track_color
        self.line_width = line_width
        self.size = size
        self.start = start
        self.text_draw = text_draw
        self.text_dict = text_dict

        self.connect("draw", self._draw)

    def set_progress(
        self,
        progress: float,
        text_dict: Optional[dict[str, str]] = None
    ):
        self.progress = progress

        if text_dict:
            self.text_dict = text_dict

        self.queue_draw()

    def _draw(self, widget: Gtk.Widget, ctx: cairo.Context):
        allocated_width = widget.get_allocated_width()
        allocated_height = widget.get_allocated_height()
        width = allocated_width if allocated_width < allocated_height else allocated_height

        point = self.size * (self.progress / 100) + self.start
        end = self.size + self.start

        ctx.scale(width, width)
        ctx.set_line_width(self.line_width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)

        ctx.arc(0.5, 0.5, 0.4, point, end)
        set_rgb(ctx, self.track_color)
        ctx.stroke()

        ctx.arc(0.5, 0.5, 0.4, self.start, point)
        set_rgb(ctx, self.color)
        ctx.stroke()

        if self.text_draw:
            if self.text_dict:
                self.text_draw(ctx, self.text_dict)
            else:
                self.text_draw(ctx)


class DoubleCircle(Gtk.DrawingArea):
    def __init__(
        self,
        color_1: tuple[int] = (0, 0, 0),
        color_2: tuple[int] = (0, 0, 0),
        track_color: tuple[int] = (255, 255, 255),
        line_width: float = 0.02,
        size: float = 2 * pi,
        start: float = 0,
        max_1: float = 100,
        max_2: float = 100,
        text_draw: Optional[TEXT_DRAW_FUNCTION] = None,
        text_dict: Optional[dict[str, str]] = None
    ):
        super().__init__()

        self.progress_1 = 0
        self.progress_2 = 0

        self.color_1 = color_1
        self.color_2 = color_2
        self.track_color = track_color
        self.line_width = line_width
        self.size = size
        self.start = start
        self.max_1 = max_1
        self.max_2 = max_2
        self.text_draw = text_draw
        self.text_dict = text_dict

        self.connect("draw", self._draw)

    def set_progress(
        self,
        progress_1: float,
        progress_2: float,
        max_1: Optional[float] = None,
        max_2: Optional[float] = None,
        text_dict: Optional[dict[str, str]] = None
    ):
        self.progress_1 = progress_1
        self.progress_2 = progress_2

        if max_1:
            self.max_1 = max_1

        if max_2:
            self.max_2 = max_2

        if text_dict:
            self.text_dict = text_dict

        self.queue_draw()

    def _draw(self, widget: Gtk.Widget, ctx: cairo.Context):
        allocated_width = widget.get_allocated_width()
        allocated_height = widget.get_allocated_height()
        width = allocated_width if allocated_width < allocated_height else allocated_height

        point_1 = self.size * (self.progress_1 / self.max_1) + self.start
        point_2 = self.size * (self.progress_2 / self.max_2) + self.start
        end = self.size + self.start

        ctx.scale(width, width)
        ctx.set_line_width(self.line_width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)

        ctx.arc(0.5, 0.5, 0.4, point_1, end)
        set_rgb(ctx, self.track_color)
        ctx.stroke()

        ctx.arc(0.5, 0.5, 0.4, self.start, point_1)
        set_rgb(ctx, self.color_1)
        ctx.stroke()

        ctx.arc(0.5, 0.5, 0.4 - self.line_width, point_2, end)
        set_rgb(ctx, self.track_color)
        ctx.stroke()

        ctx.arc(0.5, 0.5, 0.4 - self.line_width, self.start, point_2)
        set_rgb(ctx, self.color_2)
        ctx.stroke()

        if self.text_draw:
            if self.text_dict:
                self.text_draw(ctx, self.text_dict)
            else:
                self.text_draw(ctx)


class CPUCircle(Circle):
    def __init__(self, desc_color: tuple[int], text_color: tuple[int], **kwargs):
        super().__init__(
            size=pi * 5/3,
            start=pi * 2/3,
            text_draw=self._draw_text,
            **kwargs
        )

        self.desc_color = desc_color
        self.text_color = text_color

    def _draw_text(self, ctx: cairo.Context):
        set_rgb(ctx, self.desc_color)
        show_text(ctx, 0.45, 0.05, "使用率")

        set_rgb(ctx, self.text_color)
        show_text(ctx, 0.55, 0.1, f"{self.progress}%")


class MemoryCircle(Circle):
    def __init__(self, desc_color: tuple[int], text_color: tuple[int], **kwargs):
        super().__init__(
            size=pi * 5/3,
            start=pi * 2/3,
            text_draw=self._draw_text,
            **kwargs
        )

        self.desc_color = desc_color
        self.text_color = text_color

    def _draw_text(self, ctx: cairo.Context, text_dict: dict):
        set_rgb(ctx, self.desc_color)
        show_text(ctx, 0.3, 0.05, "使用率")
        show_text(ctx, 0.5, 0.05, "使用済み")
        show_text(ctx, 0.76, 0.05, "容量")

        ctx.set_line_width(0.01)
        ctx.move_to(0.3, 0.615)
        ctx.line_to(0.7, 0.615)
        ctx.stroke()

        set_rgb(ctx, self.text_color)
        show_text(ctx, 0.4, 0.1, f"{self.progress}%")
        show_text(ctx, 0.6, 0.1, text_dict["used"])
        show_text(ctx, 0.7, 0.1, text_dict["total"])


class DiskCircle(DoubleCircle):
    def __init__(
        self,
        desc_color: tuple[int],
        text_color: tuple[int],
        disk_read_color: tuple[int],
        disk_write_color: tuple[int],
        **kwargs
    ):
        super().__init__(
            size=pi * 5/3,
            start=pi * 2/3,
            text_draw=self._draw_text,
            **kwargs
        )

        self.desc_color = desc_color
        self.text_color = text_color
        self.disk_read_color = disk_read_color
        self.disk_write_color = disk_write_color

    def _draw_text(self, ctx: cairo.Context, text_dict: dict):
        set_rgb(ctx, self.desc_color)
        show_text(ctx, 0.3, 0.05, "読み込み速度")
        show_text(ctx, 0.6, 0.05, "書き込み速度")
        show_text(ctx, 0.85, 0.05, str(Human(self.max_2, "B/s")))
        show_text(ctx, 0.9, 0.05, str(Human(self.max_1, "B/s")))

        set_rgb(ctx, self.disk_read_color)
        ctx.set_line_width(0.01)
        ctx.move_to(0.3, 0.33)
        ctx.line_to(0.7, 0.33)
        ctx.stroke()

        set_rgb(ctx, self.disk_write_color)
        ctx.set_line_width(0.01)
        ctx.move_to(0.3, 0.63)
        ctx.line_to(0.7, 0.63)
        ctx.stroke()

        set_rgb(ctx, self.text_color)
        show_text(ctx, 0.45, 0.1, text_dict["read"])
        show_text(ctx, 0.75, 0.1, text_dict["write"])


class NetworkCircle(DoubleCircle):
    def __init__(
        self,
        desc_color: tuple[int],
        text_color: tuple[int],
        network_sent_color: tuple[int],
        network_recive_color: tuple[int],
        **kwargs
    ):
        super().__init__(
            size=pi * 5/3,
            start=pi * 2/3,
            text_draw=self._draw_text,
            **kwargs
        )

        self.desc_color = desc_color
        self.text_color = text_color
        self.network_sent_color = network_sent_color
        self.network_recive_color = network_recive_color

    def _draw_text(self, ctx: cairo.Context, text_dict: dict):
        set_rgb(ctx, self.desc_color)
        show_text(ctx, 0.3, 0.05, "送信速度")
        show_text(ctx, 0.6, 0.05, "受信速度")
        show_text(ctx, 0.85, 0.05, str(Human(self.max_2, "bps")))
        show_text(ctx, 0.9, 0.05, str(Human(self.max_1, "bps")))

        set_rgb(ctx, self.network_sent_color)
        ctx.set_line_width(0.01)
        ctx.move_to(0.3, 0.33)
        ctx.line_to(0.7, 0.33)
        ctx.stroke()

        set_rgb(ctx, self.network_recive_color)
        ctx.set_line_width(0.01)
        ctx.move_to(0.3, 0.63)
        ctx.line_to(0.7, 0.63)
        ctx.stroke()

        set_rgb(ctx, self.text_color)
        show_text(ctx, 0.45, 0.1, text_dict["sent"])
        show_text(ctx, 0.75, 0.1, text_dict["recive"])
