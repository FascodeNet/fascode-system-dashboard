using Gtk;

namespace Dashboard {
    [GtkTemplate (ui = "/org/fascode/dashboard/ui/about-dialog.ui")]
    public class About: Gtk.AboutDialog {
        public class About(Gtk.Window window) {
            this.set_transient_for(window);
        }
    }
}