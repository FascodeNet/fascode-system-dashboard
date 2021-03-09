#!/usr/bin/env python3
# Third-Party Library
import gi

from gi.repository import Gdk
from cairo import Context


def set_rgb(ctx: Context, color: str):
    rgba = Gdk.RGBA()
    rgba.parse(color)
    ctx.set_source_rgba(rgba.red, rgba.green, rgba.blue, rgba.alpha)
