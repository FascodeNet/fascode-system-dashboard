# Standard Library
from itertools import zip_longest

# Local Library
from .util import human_like_to_raw

# Third-Party Library
import cairo
import gi
import psutil

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, GdkPixbuf

class ProcessTable(Gtk.TreeView):
    def __init__(self):
        super().__init__()

        self.liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str, int, int, str)
        self.liststore.set_sort_func(4, self._compare)
        self.set_model(self.liststore)

        pixbuf = Gtk.TreeViewColumn("", Gtk.CellRendererPixbuf(), pixbuf=0)

        name_text = Gtk.TreeViewColumn("名前", Gtk.CellRendererText(), text=1)
        name_text.set_expand(True)
        name_text.set_sort_column_id(1)

        pid_text = Gtk.TreeViewColumn("PID", Gtk.CellRendererText(), text=2)
        pid_text.set_sort_column_id(2)

        text = Gtk.CellRendererText()
        cpu_text = Gtk.TreeViewColumn("CPU使用率")
        cpu_text.set_sort_column_id(3)
        cpu_text.pack_start(text, False)
        cpu_text.pack_start(Gtk.CellRendererText(text="%"), False)
        cpu_text.add_attribute(text, "text", 3)

        memory_text = Gtk.TreeViewColumn("メモリ使用量", Gtk.CellRendererText(), text=4)
        memory_text.set_sort_column_id(4)

        self.append_column(pixbuf)
        self.append_column(name_text)
        self.append_column(pid_text)
        self.append_column(cpu_text)
        self.append_column(memory_text)
    
    def _compare(self, model: Gtk.TreeModel, a: Gtk.TreeIter, b: Gtk.TreeIter, userdata: None):
        return human_like_to_raw(model.get_value(a, 4)) - human_like_to_raw(model.get_value(b, 4))
    
    def update(self, liststore: Gtk.ListStore):
        for row in self.liststore:
            if not psutil.pid_exists(row[2]):
                self.liststore.remove(row.iter)

        for old_row, new_row in zip_longest(self.liststore, liststore):
            if old_row and new_row:
                self.liststore.set_value(old_row.iter, 3, new_row[3])
                self.liststore.set_value(old_row.iter, 4, new_row[4])
            elif not old_row and new_row:
                self.liststore.append(new_row[:])
