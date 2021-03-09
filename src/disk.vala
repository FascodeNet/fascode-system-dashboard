using GTop;
using Gtk;

namespace Dashboard {
    [GtkTemplate (ui = "/org/fascode/dashboard/ui/disk-speed.ui")]
    public class DiskSpeed: Gtk.Box {
        [GtkChild]
        private unowned Gtk.Box read_header;

        [GtkChild]
        private unowned Gtk.Label read_label;

        [GtkChild]
        private unowned Gtk.Box write_header;

        [GtkChild]
        private unowned Gtk.Label write_label;

        private uint64 old_read;
        private uint64 old_write;

        public DiskSpeed() {
            read_header.pack_start(new Header("#9C27B0"), true, true, 0);
            write_header.pack_start(new Header("#FF9800"), true, true, 0);

            GTop.FsUsage fsusage;
            GTop.get_fsusage(out fsusage, "/");;

            old_read = fsusage.read;
            old_write = fsusage.write;

            Timeout.add(1000, this.update);
        }

        public bool update() {
            GTop.FsUsage fsusage;
            GTop.get_fsusage(out fsusage, "/");;

            read_label.set_text(to_human(fsusage.read - old_read) + "/s");
            write_label.set_text(to_human(fsusage.write - old_write) + "/s");

            old_read = fsusage.read;
            old_write = fsusage.write;

            return true;
        }
    }
}
