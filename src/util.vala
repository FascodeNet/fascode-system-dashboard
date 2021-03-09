using Cairo;
using Gdk;

namespace Dashboard {
    public void set_rgba(Cairo.Context ctx, string color) {
        Gdk.RGBA rgba = Gdk.RGBA();
        rgba.parse(color);
        ctx.set_source_rgba(rgba.red, rgba.green, rgba.blue, rgba.alpha);
    }

    public void show_text(Cairo.Context ctx, string text, double font_size, double x, double y) {
        double real_x = x - text.length / 4 * font_size;
        ctx.set_font_size(font_size);
        ctx.move_to(real_x, y);
        ctx.show_text(text);
    }

    public string to_human(uint64 number) {
        if (number >= Math.pow(1000, 4)) {
            return "%.1fTB".printf((double)number/ (double)Math.pow(1000, 4));
        }
        else if (number >= Math.pow(1000, 3)) {
            return "%.1fGB".printf((double)number/ (double)Math.pow(1000, 3));
        }
        else if (number >= Math.pow(1000, 2)) {
            return "%.1fMB".printf((double)number/ (double)Math.pow(1000, 2));
        }
        else if (number >= Math.pow(1000, 1)) {
            return "%.1fKB".printf((double)number/ (double)Math.pow(1000, 1));
        }
        else {
            return "%.1fB".printf((double)number);
        }
    }
}
