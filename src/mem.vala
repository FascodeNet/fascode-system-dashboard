using GTop;
using Gtk;

namespace Dashboard {
    public class MemCircle: Gtk.Box {
        private Circle circle = new Circle("#E91E63", "#9E9E9E");
        private Gtk.Label label = new Gtk.Label("");

        public MemCircle() {
            Object(orientation: Gtk.Orientation.VERTICAL, spacing: 10);

            this.pack_start(circle, true, true, 0);
            this.pack_start(label, false, false, 0);

            Timeout.add(1000, this.update);
        }

        public bool update() {
            GTop.Mem mem;
            GTop.get_mem(out mem);

            double percentage = (((double) mem.user / mem.total) * 100);

            circle.set_progress(percentage);
            label.set_text(to_human(mem.user)+ " / " + to_human(mem.total));

            return true;
        }
    }
}