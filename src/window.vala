using Gtk;

namespace Dashboard {
    [GtkTemplate (ui = "/org/fascode/dashboard/ui/window.ui")]
    public class Window: Gtk.ApplicationWindow {
        [GtkChild]
        private unowned Gtk.Box circle_box;

        [GtkChild]
        private unowned Gtk.Box cpu_box;

        [GtkChild]
        private unowned Gtk.Box mem_box;

        [GtkChild]
        private unowned Gtk.Box disk_box;

        [GtkChild]
        private unowned Gtk.Box net_box;

        [GtkChild]
        private unowned  Gtk.ScrolledWindow app_box;

        [GtkChild]
        private unowned  Gtk.Box cpu_graph;

        [GtkChild]
        private unowned  Gtk.Box mem_graph;

        [GtkChild]
        private unowned  Gtk.Box disk_graph;

        [GtkChild]
        private unowned  Gtk.Box net_graph;

        [GtkChild]
        private unowned  Gtk.Box proc_box;

        public Window(Gtk.Application application) {
            Object(application: application);

            cpu_box.pack_start(new CpuCircle(), true, true, 0);
            mem_box.pack_start(new MemCircle(), true, true, 0);
            disk_box.pack_start(new DiskSpeed(), true, true, 0);
            net_box.pack_start(new NetSpeed(), true, true, 0);

            GTop.Swap swap;
            GTop.get_swap(out swap);

            if (swap.total != 0) {
                circle_box.pack_start(new SwapBox(), true, true, 0);
            }
        }

        [GtkCallback]
        private void about(Gtk.MenuItem menu_item) {
            About dialog = new About(this);
            dialog.present();
        }

        [GtkCallback]
        private void quit(Gtk.MenuItem menu_item) {
            this.destroy();
        }
    }
}