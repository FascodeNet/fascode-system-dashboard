#!/usr/bin/env python3
# Standard Library
from time import time
from typing import Optional, Union

# Third-Party Library
import psutil
from gi.repository import Gio

OLD_DISK_IO = psutil.disk_io_counters()
OLD_DISK_TIME = time()

OLD_NETWORK_IO = psutil.net_io_counters()
OLD_NETWORK_TIME = time()

APP = {}
CPU_COUNT = psutil.cpu_count()

for app in Gio.DesktopAppInfo().get_all():
    app_id = app.get_id()
    app_cmdline = app.get_commandline()

    if app_id:
        APP[app_id.replace(".desktop", "")] = app
    if app_cmdline:
        APP[app_cmdline.split()[0].split("/")[-1]] = app


def zero(numerator: Union[int, float], denominator: Union[int, float]) -> float:
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0.0


def to_human(number: int, byte: bool = True) -> str:
    label = ("", "Ki", "Mi", "Gi") if byte else ("", "K", "M", "G")
    power = 1024 if byte else 1000
    count = 0

    while number >= power and count < len(label) - 1:
        number /= power
        count += 1

    return str(round(number, 1)) + label[count]


def is_app(process: psutil.Process) -> bool:
    if process.info["name"] in APP:
        return True

    return False


def get_cpu_usage(percpu: bool = True) -> Union[float, list[float]]:
    return psutil.cpu_percent(percpu=percpu)


def get_cpu_count() -> int:
    return CPU_COUNT


def get_memory():
    return psutil.virtual_memory()


def get_swap():
    return psutil.swap_memory()


def get_disk_speed() -> tuple[float]:
    global OLD_DISK_IO, OLD_DISK_TIME

    disk_io = psutil.disk_io_counters()
    now_time = time()

    read_delta = disk_io.read_bytes - OLD_DISK_IO.read_bytes
    write_delta = disk_io.write_bytes - OLD_DISK_IO.write_bytes
    time_delta = now_time - OLD_DISK_TIME

    OLD_DISK_IO = disk_io
    OLD_DISK_TIME = now_time

    read_speed = zero(read_delta, time_delta)
    write_speed = zero(write_delta, time_delta)

    return read_speed, write_speed


def get_network_speed() -> tuple[float]:
    global OLD_NETWORK_IO, OLD_NETWORK_TIME

    network_io = psutil.net_io_counters()
    now_time = time()

    sent_delta = network_io.bytes_sent - OLD_NETWORK_IO.bytes_sent
    recieve_delta = network_io.bytes_recv - OLD_NETWORK_IO.bytes_recv
    time_delta = now_time - OLD_NETWORK_TIME

    OLD_NETWORK_IO = network_io
    OLD_NETWORK_TIME = now_time

    sent_speed = zero(sent_delta, time_delta) * 8
    recive_speed = zero(recieve_delta, time_delta) * 8

    return sent_speed, recive_speed


def get_process() -> dict[str, dict[str, Union[Gio.DesktopAppInfo, float, int]]]:
    app_info = {}

    for process in psutil.process_iter(["name", "cpu_percent", "memory_info"]):
        if is_app(process):
            name = process.info["name"]
            app = APP[name]
        else:
            name = "system"
            app = None

        if not name in app_info:
            app_info[name] = {
                "app": app,
                "cpu": 0.0,
                "memory": 0
            }

        info = app_info[name]
        info["cpu"] += process.info["cpu_percent"] / CPU_COUNT
        info["memory"] += process.info["memory_info"].rss

    return app_info
