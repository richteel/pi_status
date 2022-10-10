import socket
import fcntl
import struct
from warnings import catch_warnings
import psutil
import os
from status import log


class hw_info(object):
    def __init__(self):
        self.log = log.log()
        self.DEFAULT_IP_ADDRESS = "127.0.0.1"
        self.update()

    def get_ip_address0(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', bytes(ifname[:15], 'utf-8'))
            )[20:24])
        except OSError:
            self.log.err_print(
                "Failed to obtain IP Address for {0}".format(ifname))
            return self.DEFAULT_IP_ADDRESS

    def update(self):
        self.hostname = socket.gethostname()
        self.ipaddress = socket.gethostbyname(self.hostname + ".local")

        # Get interface addresses
        self.ip_eth0 = self.get_ip_address("eth0")
        self.ip_wlan0 = self.get_ip_address("wlan0")

        if self.ipaddress != self.ip_eth0 and self.ip_eth0 != self.DEFAULT_IP_ADDRESS:
            self.ipaddress = self.ip_eth0
        elif self.ipaddress == self.DEFAULT_IP_ADDRESS and self.ip_wlan0 != self.DEFAULT_IP_ADDRESS:
            self.ipaddress = self.ip_wlan0

        self.cpuTemperature = psutil.sensors_temperatures()[
            'cpu_thermal'][0].current

        mem = psutil.virtual_memory()
        self.memTotal = mem.total
        self.memTotalGB = round(mem.total / (1024 ** 3))
        self.memUsed = mem.used
        self.memFree = mem.free
        self.memPercent = mem.percent

        disk = psutil.disk_usage(os.getcwd())
        self.diskTotal = disk.total
        self.diskTotalGB = round(disk.total / (1024 ** 3))
        self.diskUsed = disk.used
        self.diskFree = disk.free
        self.diskPercent = disk.percent

        # Getting load over 1, 5, & 15 minutes
        load1, load5, load15 = psutil.getloadavg()

        self.cpuUsagePercent_1 = (load1/os.cpu_count()) * 100
        self.cpuUsagePercent_5 = (load5/os.cpu_count()) * 100
        self.cpuUsagePercent_15 = (load15/os.cpu_count()) * 100
