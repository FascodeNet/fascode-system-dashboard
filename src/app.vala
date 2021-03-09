using GTop;
using Gdk;
using Gtk;

namespace Dashboard {
    public class  AppBox: Gtk.TreeView {
        private HashTable<string, AppInfo> app = new HashTable<string, AppInfo>(str_hash, str_equal);
        private Gtk.ListStore model = Gtk.ListStore(Gdk.Pixbuf, string, string, string);

        public AppBox() {
            foreach (AppInfo appinfo in AppInfo.get_all()) {
                string ?id = null;
                id = info.get_id();

                if (id != null && id.has_suffix (".desktop")) {
                    id = id[0:id.length - 8];
                }

                if (id != null) {
                    appid_map.insert (id, info);
                }
            }

            Gtk.TreeViewColumn icon = Gtk.TreeViewColumn();
            icon.set_attributes(_("Icon"), new Gtk.CellRendererPixbuf(), gicon: 0);
            this.append_column(icon);

            Gtk.CellRendererText renderer_text = new Gtk.CellRendererText();

            Gtk.TreeViewColumn name = Gtk.TreeViewColumn();
            name.set_attributes(_("Name"), renderer_text, text: 1);
            this.append_column(name);

            Gtk.TreeViewColumn cpu = Gtk.TreeViewColumn();
            cpu.set_attributes(_("CPU"), renderer_text, text: 2);
            this.append_column(cpu);

            Gtk.TreeViewColumn mem = Gtk.TreeViewColumn();
            mem.set_attributes(_("Memory"), renderer_text, text: 3);
            this.append_column(mem);
        }
    }
}
