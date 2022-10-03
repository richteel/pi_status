import socket
import psutil
import os

class hw_info(object):
    def __init__(self):
        self.update()

    def update(self):
        self.hostname = socket.gethostname()
        self.ipaddress = socket.gethostbyname(self.hostname + ".local")

        self.cpuTemperature = psutil.sensors_temperatures()['cpu_thermal'][0].current

        mem = psutil.virtual_memory()
        self.memTotal = mem.total
        self.memTotalGB = round(mem.total / (1024 ** 3))
        self.memFree = mem.free
        self.memPercent = mem.percent

        disk = psutil.disk_usage(os.getcwd())
        self.diskTotal = disk.total
        self.diskTotalGB = round(disk.total / (1024 ** 3))
        self.diskUsed = disk.used
        self.diskFree = disk.free
        self.diskPercent = disk.percent

        # Getting loadover15 minutes
        load1, load5, load15 = psutil.getloadavg()
        
        self.cpuUsagePercent_1 = (load1/os.cpu_count()) * 100
        self.cpuUsagePercent_5 = (load5/os.cpu_count()) * 100
        self.cpuUsagePercent_15 = (load15/os.cpu_count()) * 100