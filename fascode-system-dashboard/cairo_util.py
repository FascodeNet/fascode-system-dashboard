#!/usr/bin/env python3
# Third-Party Library
from cairo import Context


def set_rgb(ctx: Context, rgb: str, alpha: int = 100):
    rgb = rgb.strip("#")
    r = int(rgb[0:2], 16)
    g = int(rgb[2:4], 16)
    b = int(rgb[4:6], 16)

    ctx.set_source_rgba(r / 255, g / 255, b / 255, alpha / 100)
