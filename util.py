# Standard Lib
from time import time
from unicodedata import east_asian_width

# Third-Party Lib
import psutil

OldDiskIO = psutil.disk_io_counters()
OldDiskTime = time()
OldNetworkIO = psutil.net_io_counters()
OldNetworkTime = time()

class Human:
    def __init__(self, number, OptLabel="B"):
        label = ("", "K", "M", "G")
        count = 0

        self.RawNumber = number

        while number >= 1000 and count < len(label) - 1:
            number /= 1000
            count += 1

        self.Number = round(number, 1)
        self.Label = label[count]
        self.OptLabel = OptLabel
    
    def __repr__(self):
        return f"Human(RawNumber={self.RawNumber}, Number={self.Number}, Label='{self.Label}', OptLabel='{self.OptLabel}')"
    
    def __str__(self):
        return str(self.Number) + self.Label + self.OptLabel

def Zero(numerator, denominator):
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0.0

def GetCPUUsage(percpu=True):
    return psutil.cpu_percent(percpu=percpu)

def GetCPUCount(logical=True):
    return psutil.cpu_count(logical=logical)

def GetMemoryUsage():
    return psutil.virtual_memory().percent

def GetMemoryUsed():
    return  Human(psutil.virtual_memory().used)

def GetMemoryTotal():
    return  Human(psutil.virtual_memory().total)

def GetRootUsage():
    PartitionUsage = psutil.disk_usage("/")
    PartitonInfo = {
        "used": Human(PartitionUsage.used),
        "total": Human(PartitionUsage.total),
        "percent": PartitionUsage.percent
    }

    return PartitonInfo

def GetDiskUsage():
    Disk = {}

    for partition in psutil.disk_partitions():
        DiskName = partition.device[:-1]
        PartitionUsage = psutil.disk_usage(partition.mountpoint)
        PartitonInfo = {
            "name": partition.device,
            "mountpoint": partition.mountpoint,
            "used": Human(PartitionUsage.used),
            "total": Human(PartitionUsage.total),
            "percent": PartitionUsage.percent
        }

        if not DiskName in Disk:
            Disk[DiskName] = {"total": PartitonInfo["total"].RawNumber, "partition": [PartitonInfo]}
        else:
            Disk[DiskName]["total"] += PartitonInfo["total"].RawNumber
            Disk[DiskName]["partition"].append(PartitonInfo)
    
    for disk in Disk:
        Disk[disk]["total"] = Human(Disk[disk]["total"])
        Disk[disk]["partition"] = sorted(Disk[disk]["partition"], key=lambda dict: dict["name"])
    
    return dict(sorted(Disk.items(), key=lambda tuple: tuple[0]))

def GetNetworkSpeed():
    global OldNetworkIO, OldNetworkTime

    NetworkIO = psutil.net_io_counters()
    Time = time()

    SentDelta = NetworkIO.bytes_sent - OldNetworkIO.bytes_sent
    RecieveDelta = NetworkIO.bytes_recv - OldNetworkIO.bytes_recv
    TimeDelta = Time - OldNetworkTime

    OldNetworkIO = NetworkIO
    OldNetworkTime = Time

    SentSpeed = Human(Zero(SentDelta, TimeDelta) * 8, "bps")
    ReciveSpeed = Human(Zero(RecieveDelta, TimeDelta) * 8, "bps")
    
    return SentSpeed, ReciveSpeed

def SetRGB(ctx, rgb):
    ctx.set_source_rgb(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)

def ShowText(ctx, y, font_size, text):
    Count = 0

    text = str(text)

    ctx.set_font_size(font_size)

    for char in text:
        if east_asian_width(char) in "AFW":
            Count += 2
        else:
            Count += 1

    ctx.move_to(0.5 -  font_size * Count / 4, y)
    ctx.show_text(text)

def LoadRGB(string):
    return [int(value) for value in string.split(",")]