using GTop;
using Gtk;

namespace Dashboard {
    public class SwapCircle: Gtk.Box {
        private Circle circle = new Circle("#4CAF50", "#9E9E9E");
        private Gtk.Label label = new Gtk.Label("");

        public SwapCircle() {
            Object(orientation: Gtk.Orientation.VERTICAL, spacing: 10);

            this.pack_start(circle, true, true, 0);
            this.pack_start(label, false, false, 0);

            Timeout.add(1000, this.update);
        }

        public bool update() {
            GTop.Swap swap;
            GTop.get_swap(out swap);

            double percentage = (((double) swap.used / swap.total) * 100);

            circle.set_progress(percentage);
            label.set_text(to_human(swap.used)+ " / " + to_human(swap.total));

            return true;
        }
    }

    [GtkTemplate (ui = "/org/fascode/dashboard/ui/swap-box.ui")]
    public class SwapBox: Gtk.Box {
        [GtkChild]
        private unowned Gtk.Box swap_box;

        public SwapBox() {
            this.swap_box.pack_start(new SwapCircle(), true, true, 0);
        }
    }
}