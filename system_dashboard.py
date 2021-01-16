#!/usr/bin/env python3
# Standard Lib
import sys
from configparser import ConfigParser
from math import ceil, pi

# Local Lib
import util

# Third-Party Lib
import gi

# Gtk Lib
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, GLib, Gtk

config = ConfigParser()
config.read("system_dashboard.conf")

try:
    Color = config["color"]

    DESCRIPTION = util.LoadRGB(Color["Description"])
    TEXT =  util.LoadRGB(Color["Text"])
    CPU = util.LoadRGB(Color["CPU"])
    MEMORY =  util.LoadRGB(Color["Memory"])
    DISK =  util.LoadRGB(Color["Disk"])
    NETWORKSENT = util.LoadRGB(Color["NetworkSent"])
    NETWORKRECIVE = util.LoadRGB(Color["NetworkRecive"])

    General = config["general"]

    INTERVAL = float(General["Interval"])
except:
    print("Config Error")
    sys.exit(1)

class SystemDashBoardWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        # Window
        super().__init__(*args, **kwargs)
        self.set_default_size(1000, 300)
        self.set_border_width(10)

        # Timer
        # GLib.timeout_add_seconds(INTERVAL, self.update)
        GLib.timeout_add(INTERVAL, self.update)

        # CPU
        self.CPUUsage = util.GetCPUUsage(False)

        self.CPUCircle = Gtk.DrawingArea()
        self.CPUCircle.connect("draw", self.CPUCircleDraw)

        # Memory
        self.MemoryUsage = util.GetMemoryUsage()
        self.MemoryUsed = util.GetMemoryUsed()
        self.MemoryTotal = util.GetMemoryTotal()

        self.MemoryCircle = Gtk.DrawingArea()
        self.MemoryCircle.connect("draw", self.MemoryCircleDraw)

        # Disk
        self.RootUsage = util.GetRootUsage()

        self.RootCircle = Gtk.DrawingArea()
        self.RootCircle.connect("draw", self.RootCircleDraw)

        # Network
        self.NetworkSentSpeed, self.NetworkReciveSpeed = util.GetNetworkSpeed()

        self.NetworkCircle = Gtk.DrawingArea()
        self.NetworkCircle.connect("draw", self.NetworkCircleDraw)

        # Stack
        StackBox = Gtk.HBox()
        self.Stack = Gtk.Stack()
        Sidebar = Gtk.StackSidebar()
        Sidebar.set_stack(self.Stack)
        StackBox.pack_start(Sidebar, False, False, 0)
        StackBox.pack_start(self.Stack, True, True, 0)

        # CPU
        self.CPUUsages = [util.GetCPUUsage()]

        CPUGraph = Gtk.DrawingArea()
        CPUGraph.connect("draw", self.CPUGraphDraw)
        self.Stack.add_titled(CPUGraph, "CPU", "CPU")

        # Finalizing
        HBox = Gtk.HBox()
        HBox.pack_start(self.CPUCircle, True, True, 0)
        HBox.pack_start(self.MemoryCircle, True, True, 0)
        HBox.pack_start(self.RootCircle, True, True, 0)
        HBox.pack_start(self.NetworkCircle, True, True, 0)

        VBox = Gtk.VBox()
        VBox.pack_start(HBox, True, True, 0)
        VBox.pack_start(StackBox, True, True, 0)

        self.add(VBox)
        self.show_all()

    def update(self):
        self.CPUUsage = util.GetCPUUsage(False)
        self.MemoryUsage = util.GetMemoryUsage()
        self.MemoryUsed = util.GetMemoryUsed()
        self.RootUsage = util.GetRootUsage()
        self.NetworkSentSpeed, self.NetworkReciveSpeed = util.GetNetworkSpeed()
        self.CPUUsages.append(util.GetCPUUsage())

        if len(self.CPUUsages) > 60:
            self.CPUUsages.pop(0)

        self.CPUCircle.queue_draw()
        self.MemoryCircle.queue_draw()
        self.NetworkCircle.queue_draw()
        self.Stack.get_visible_child().queue_draw()

        return True
    
    def CPUCircleDraw(self, widget, ctx):
        AllocatedWidth = widget.get_allocated_width()
        AllocatedHeight = widget.get_allocated_height()

        Width = AllocatedWidth if AllocatedWidth < AllocatedHeight else AllocatedHeight
        Point = (2 * pi) * (self.CPUUsage / 100) + pi /2

        ctx.scale(Width, Width)
        
        ctx.set_line_width(0.02)

        ctx.arc(0.5, 0.5, 0.4, pi / 2, Point)
        util.SetRGB(ctx, CPU)
        ctx.stroke()

        ctx.arc(0.5, 0.5, 0.4, Point, pi / 2)
        util.SetRGB(ctx, DESCRIPTION)
        ctx.stroke()

        util.ShowText(ctx, 0.45, 0.05, "使用率")
        util.SetRGB(ctx, TEXT)
        util.ShowText(ctx, 0.55, 0.1, f"{self.CPUUsage}%")
    
    def MemoryCircleDraw(self, widget, ctx):
        AllocatedWidth = widget.get_allocated_width()
        AllocatedHeight = widget.get_allocated_height()

        Width = AllocatedWidth if AllocatedWidth < AllocatedHeight else AllocatedHeight

        Point = (2 * pi) * (self.MemoryUsage / 100) + pi /2

        ctx.scale(Width, Width)
        
        ctx.set_line_width(0.02)

        ctx.arc(0.5, 0.5, 0.4, pi / 2, Point)
        util.SetRGB(ctx, MEMORY)
        ctx.stroke()

        ctx.arc(0.5, 0.5, 0.4, Point, pi / 2)
        util.SetRGB(ctx, DESCRIPTION)
        ctx.stroke()

        util.ShowText(ctx, 0.3, 0.05, "使用率")
        util.ShowText(ctx, 0.5, 0.05, "使用済み")
        util.ShowText(ctx, 0.76, 0.05, "容量")

        ctx.set_line_width(0.01)
        ctx.move_to(0.3, 0.615)
        ctx.line_to(0.7, 0.615)
        ctx.stroke()

        util.SetRGB(ctx, TEXT)
        util.ShowText(ctx, 0.4, 0.1, f"{self.MemoryUsage}%")
        util.ShowText(ctx, 0.6, 0.1, self.MemoryUsed)
        util.ShowText(ctx, 0.7, 0.1, self.MemoryTotal)
    
    def RootCircleDraw(self, widget, ctx):
        AllocatedWidth = widget.get_allocated_width()
        AllocatedHeight = widget.get_allocated_height()

        Width = AllocatedWidth if AllocatedWidth < AllocatedHeight else AllocatedHeight

        X = 0.1 + 0.8 * (self.RootUsage["percent"] / 100)

        ctx.scale(Width, Width)

        ctx.set_line_width(0.01)
        util.SetRGB(ctx, DISK)

        ctx.move_to(0.1, 0.1)
        ctx.line_to(0.9, 0.1)
        ctx.line_to(0.9, 0.3)
        ctx.line_to(0.1, 0.3)
        ctx.line_to(0.1, 0.1)
        ctx.stroke()

        ctx.move_to(0.1, 0.1)
        ctx.line_to(X, 0.1)
        ctx.line_to(X, 0.3)
        ctx.line_to(0.1, 0.3)
        ctx.line_to(0.1, 0.1)
        ctx.fill()
        ctx.stroke()

        util.SetRGB(ctx, DESCRIPTION)
        util.ShowText(ctx, 0.45, 0.1, "使用済み")
        util.ShowText(ctx, 0.95, 0.1, "容量")

        ctx.set_line_width(0.01)
        ctx.move_to(0.1, 0.65)
        ctx.line_to(0.9, 0.65)
        ctx.stroke()

        util.SetRGB(ctx, TEXT)
        util.ShowText(ctx, 0.6, 0.15, self.RootUsage["used"])
        util.ShowText(ctx, 0.8, 0.15, self.RootUsage["total"])
    
    def NetworkCircleDraw(self, widget, ctx):
        AllocatedWidth = widget.get_allocated_width()
        AllocatedHeight = widget.get_allocated_height()

        Width = AllocatedWidth if AllocatedWidth < AllocatedHeight else AllocatedHeight

        ctx.scale(Width, Width)

        util.SetRGB(ctx, DESCRIPTION)
        util.ShowText(ctx, 0.15, 0.1, "送信速度")
        util.ShowText(ctx, 0.65, 0.1, "受信速度")

        util.SetRGB(ctx, NETWORKSENT)
        ctx.set_line_width(0.01)
        ctx.move_to(0.3, 0.2)
        ctx.line_to(0.7, 0.2)
        ctx.stroke()
        
        util.SetRGB(ctx, NETWORKRECIVE)
        ctx.set_line_width(0.01)
        ctx.move_to(0.3, 0.7)
        ctx.line_to(0.7, 0.7)
        ctx.stroke()

        util.SetRGB(ctx, TEXT)
        util.ShowText(ctx, 0.45, 0.2, self.NetworkSentSpeed)
        util.ShowText(ctx, 0.95, 0.2,  self.NetworkReciveSpeed)
    
    def CPUGraphDraw(self, widget, ctx):
        Color = [
            [63, 81, 181],
            [0, 188, 212],
            [233, 30, 99],
            [139, 195, 74]
        ]

        AllocatedWidth = widget.get_allocated_width()
        AllocatedHeight = widget.get_allocated_height()

        ctx.scale(AllocatedWidth, AllocatedHeight)

        ctx.set_line_width(0.01)

        # Box
        ctx.move_to(0.1, 0.1)
        ctx.line_to(0.1, 0.9)
        ctx.line_to(0.9, 0.9)
        ctx.line_to(0.9, 0.1)
        ctx.line_to(0.1, 0.1)
        ctx.stroke()

        # Vertical line
        x = 0.1

        while x < 0.9:
            ctx.move_to(x, 0.1)
            ctx.line_to(x, 0.9)
            ctx.stroke()
            x += 0.8 / 6

        # Horizontal line
        y = 0.1

        while y < 0.9:
            ctx.move_to(0.1, y)
            ctx.line_to(0.9, y)
            ctx.stroke()
            y += 0.8 / 4

        for i in reversed(range(util.GetCPUCount())):
            ctx.move_to(0.1 +  0.8 - 0.8 * len(self.CPUUsages) / 60, 0.9)
            
            for number, data in enumerate(self.CPUUsages):
                x = 0.1 + 0.8 / 60 * number + 0.8 - 0.8 * len(self.CPUUsages) / 60
                y = 0.9 - 0.8 * (sum(data[:i + 1]) / util.GetCPUCount()) / 100
                ctx.line_to(x,  y)
            else:
                y = 0.9 - 0.8 * (sum(data[:i + 1]) / util.GetCPUCount()) / 100
                ctx.line_to(0.9,  y)
                ctx.line_to(0.9, 0.9)

            if len(Color) <= i:
                color_number=i - len(Color)
            else:
                color_number=i
            util.SetRGB(ctx, Color[color_number])
            ctx.fill()
            ctx.stroke()

class SystemDashBoard(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="org.fascode.systemdashboard",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.window = None
    
    def do_activate(self):
        if not self.window:
            self.window = SystemDashBoardWindow(
                application=self,
                title="System Dash Board"
            )
        
        self.window.present()


if __name__ == "__main__":
    app = SystemDashBoard()
    app.run()
