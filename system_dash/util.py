# Standard Library
from time import time
from typing import Union, Optional
from unicodedata import east_asian_width

# Third-Party Library
import psutil
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

cpu_num = psutil.cpu_count()

old_disk_io = psutil.disk_io_counters()
old_disk_time = time()
old_network_io = psutil.net_io_counters()
old_network_time = time()

theme = Gtk.IconTheme.get_default()


class Human(object):
    def __init__(self, number, optlabel="B"):
        label = ("", "K", "M", "G")
        count = 0

        self.raw_number = number

        while number >= 1000 and count < len(label) - 1:
            number /= 1000
            count += 1

        self.number = round(number, 1)
        self.label = label[count]
        self.optlabel = optlabel

    def __repr__(self):
        base = "Human(raw_number={}, number={}, label='{}', optlabel='{}')"
        return base.format(self.raw_number, self.number, self.label, self.optlabel)

    def __int__(self):
        return self.raw_number

    def __str__(self):
        return str(self.number) + self.label + self.optlabel


def zero(numerator: Union[int, float], denominator: Union[int, float]) -> float:
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0.0

def human_like_to_raw(human_like: str, optlabel: str = "B") -> float:
    replaced = human_like.replace(optlabel, "")
    power = 0
    
    if "K" in replaced:
        replaced = replaced.replace("K", "")
        power = 1
    elif "M" in replaced:
        replaced = replaced.replace("M", "")
        power = 2
    elif "G" in replaced:
        replaced = replaced.replace("G", "")
        power = 3

    return float(replaced) * 1000 ** power


def get_cpu_usage(percpu: bool = True) -> Union[float, list[float]]:
    return psutil.cpu_percent(percpu=percpu)


def get_cpu_count(logical: bool = True) -> int:
    return psutil.cpu_count(logical=logical)


def get_memory_usage():
    return psutil.virtual_memory()


def get_disk_speed() -> tuple[float]:
    global old_disk_io, old_disk_time

    disk_io = psutil.disk_io_counters()
    now_time = time()

    read_delta = disk_io.read_bytes - old_disk_io.read_bytes
    write_delta = disk_io.write_bytes - old_disk_io.write_bytes
    time_delta = now_time - old_disk_time

    old_disk_io = disk_io
    old_disk_time = now_time

    read_speed = zero(read_delta, time_delta)
    write_speed = zero(write_delta, time_delta)

    return read_speed, write_speed


def get_network_speed() -> tuple[float]:
    global old_network_io, old_network_time

    network_io = psutil.net_io_counters()
    now_time = time()

    sent_delta = network_io.bytes_sent - old_network_io.bytes_sent
    recieve_delta = network_io.bytes_recv - old_network_io.bytes_recv
    time_delta = now_time - old_network_time

    old_network_io = network_io
    old_network_time = now_time

    sent_speed = zero(sent_delta, time_delta) * 8
    recive_speed = zero(recieve_delta, time_delta) * 8

    return sent_speed, recive_speed


def get_process() -> Gtk.ListStore:
    liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str, int, int, str)

    for process in psutil.process_iter(["name", "pid", "cpu_percent", "memory_info"]):
        try:
            icon = theme.load_icon(process.info["name"], 24, 0)
        except:
            icon = theme.load_icon("application-default-icon", 24, 0)

        liststore.append(
            [
                icon,
                process.info["name"],
                process.info["pid"],
                int(process.info["cpu_percent"] / cpu_num),
                str(Human(process.info["memory_info"].rss))
            ]
        )

    return liststore
