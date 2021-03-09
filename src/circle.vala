using Cairo;
using Gtk;

namespace Dashboard {
    public class Circle: Gtk.DrawingArea {
        private string color;
        private string track_color;
        private double progress = 0.0;

        public Circle(string color, string track_color) {
            this.color = color;
            this.track_color = track_color;
        }

        protected override bool draw(Cairo.Context ctx) {
            Gtk.Allocation allocation;
            int width;

            this.get_allocation(out allocation);

            if (allocation.width < allocation.height) {
                width = allocation.width / 2;
            }
            else {
                width = allocation.height / 2;
            }

            ctx.set_line_width(width / 10);
            ctx.set_line_cap(Cairo.LineCap.ROUND);

            var point = Math.PI * 5/3 * (this.progress / 100) + Math.PI * 2/3;
            var end = Math.PI * 5/3 + Math.PI * 2/3;

            ctx.arc(allocation.width / 2, allocation.height / 2, width * 0.9, point, end);
            set_rgba(ctx, this.track_color);
            ctx.stroke();

            ctx.arc(allocation.width / 2, allocation.height / 2, width * 0.9, Math.PI * 2/3, point);
            set_rgba(ctx, this.color);
            ctx.stroke();

            return false;
        }

        public void set_progress(double progress) {
            this.progress = progress;
            this.queue_draw();
        }
    }
}
