using GTop;
using Gtk;

namespace Dashboard {
    [GtkTemplate (ui = "/org/fascode/dashboard/ui/net-speed.ui")]
    public class NetSpeed: Gtk.Box {
        [GtkChild]
        private unowned Gtk.Box send_header;

        [GtkChild]
        private unowned Gtk.Label send_label;

        [GtkChild]
        private unowned Gtk.Box recive_header;

        [GtkChild]
        private unowned Gtk.Label recive_label;

        private string device;
        private uint64 old_send;
        private uint64 old_recive;

        public NetSpeed() {
            send_header.pack_start(new Header("#3F51B5"), true, true, 0);
            recive_header.pack_start(new Header("#FF5722"), true, true, 0);

            GTop.NetList netlist;
            string[] devices = GTop.get_netlist(out netlist);
            device = devices[1];

            GTop.NetLoad netload;
            GTop.get_netload(out netload, device);

            old_send = netload.bytes_in;
            old_recive = netload.bytes_out;

            Timeout.add(1000, this.update);
        }

        public bool update() {
            GTop.NetLoad netload;
            GTop.get_netload(out netload, device);

            send_label.set_text(to_human(netload.bytes_in - this.old_send) + "/s");
            recive_label.set_text(to_human(netload.bytes_out - this.old_recive) + "/s");

            old_send = netload.bytes_in;
            old_recive = netload.bytes_out;

            return true;
        }
    }
}
