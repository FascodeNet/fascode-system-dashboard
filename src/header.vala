using Cairo;
using Gtk;

namespace Dashboard {
    public class Header: Gtk.DrawingArea {
        private string color;

        public Header(string color) {
            this.set_size_request(20, 60);
            this.color = color;
        }

        protected override bool draw(Cairo.Context ctx) {
            Gtk.Allocation allocation;

            this.get_allocation(out allocation);

            ctx.rectangle(0, 0, 20, allocation.height);
            set_rgba(ctx, color);
            ctx.fill();

            return false;
        }
    }
}
