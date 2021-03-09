using GTop;
using Gtk;

namespace Dashboard {
    public class CpuCircle: Gtk.Box {
        private uint64 old_total = 0;
        private uint64 old_used = 0;
        private Circle circle = new Circle("#F44336", "#9E9E9E");
        private Gtk.Label label = new Gtk.Label("");

        public CpuCircle() {
            Object(orientation: Gtk.Orientation.VERTICAL, spacing: 10);

            this.pack_start(circle, true, true, 0);
            this.pack_start(label, false, false, 0);

            Timeout.add(1000, this.update);
        }

        private bool update() {
            GTop.Cpu cpu;
            GTop.get_cpu(out cpu);

            uint64 used = cpu.user + cpu.nice + cpu.sys;
            double percentage = (((double) (used - old_used)) / (cpu.total - old_total)) * 100;

            circle.set_progress(percentage);

            label.set_text("%.1f%%".printf(percentage));
            
            old_total = cpu.total;
            old_used = used;

            return true;
        }
    }
}
