# Standard Library
from unicodedata import east_asian_width

# Third-Party Library
from cairo import Context


def set_rgb(ctx: Context, rgb: tuple, alpha: int = 100) -> None:
    ctx.set_source_rgba(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, alpha / 100)


def show_text(ctx: Context, y: float, font_size: float, text: str):
    count = 0
    ctx.set_font_size(font_size)

    for char in text:
        if east_asian_width(char) in "AFW":
            count += 2
        else:
            count += 1

    ctx.move_to(0.5 - font_size * count / 4, y)
    ctx.show_text(text)
