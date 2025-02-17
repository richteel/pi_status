#!/home/pi/env/bin/python
import time
import board
import digitalio
import os
import sys
import argparse

from status import display
from status import system
from status import GracefulKiller
from status import log

version_number = "0.2"
updateFreq = 10  # Time in seconds
currentIndex = 99
displayItems = ["NAME", "RAM", "TEMP", "DISK", "CPU"]

script_path = os.path.realpath(os.path.dirname(__file__))
logs_path = os.path.join(script_path, "logs")
verbose_file = None
stdout_file = None
stderr_file = None

parser = argparse.ArgumentParser(description="Raspberry Pi Status Monitor")
parser.add_argument("-l", help="Turn on basic logging",
                    dest="logging", action="store_true")
parser.add_argument("-v", help="Allow verbose logging of status data to a file",
                    dest="verbose", action="store_true")
args = parser.parse_args()

if args.logging or args.verbose:
    stdout_file = os.path.realpath(os.path.join(logs_path, "status.txt"))
    stderr_file = os.path.realpath(
        os.path.join(logs_path, "error.txt"))

if args.verbose:
    verbose_file = os.path.realpath(
        os.path.join(logs_path, "detail.txt"))

status_log = log.log(log_file=stdout_file,
                     err_file=stderr_file, verbose_file=verbose_file)

disp = display.display(status_log)
hw = system.hw_info()
led = digitalio.DigitalInOut(board.D27)
led.direction = digitalio.Direction.OUTPUT
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led.value = True

t = disp.getTimeString()
status_log.log_print("Starting Pi Status")
status_log.err_print("Starting Pi Status")
status_log.log_print("Logging = {0}".format(bool(stdout_file)))
status_log.log_print("Logging Verbose = {0}".format(bool(verbose_file)))

# Show Splash Screen
disp.updateDisplay("Pi Status", "Version", version_number, -1, True)

# Allow clean exit when stopping
# REF: https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
killer = GracefulKiller.GracefulKiller()

timer = time.time()

shutdownFlag = False
buttonPressedTime = time.time()
blinkTimer = time.time()
lastButtonState = False

status_log.verbose_print("Host Name", "IP Address",
                         "IP Ethernet", "IP Wi-Fi",
                         "CPU Temperature",
                         "Memory Total", "Memory Free", "Memory Used", "Memory Percent",
                         "Disk Total", "Disk Used", "Disk Free", "Disk Percent",
                         "CPU Usage Percent 1 min", "CPU Usage Percent 5 min", "CPU Usage Percent 15 min")

while not killer.kill_now:
    if not button.value:
        if not lastButtonState:
            t = disp.getTimeString()
            status_log.log_print("Button Pressed")
            lastButtonState = True
            buttonPressedTime = time.time()
        elif time.time() > buttonPressedTime + 10:
            if not shutdownFlag:
                shutdownFlag = True
                t = disp.getTimeString()
                status_log.log_print("Shutting Down")
                os.system("/usr/sbin/shutdown now -h")
    else:
        if lastButtonState:
            status_log.log_print("Button Released")
        lastButtonState = False

    if shutdownFlag:
        if time.time() > blinkTimer + 2:
            led.value = not led.value
            blinkTimer = time.time()
        continue

    if time.time() > timer + updateFreq:
        if currentIndex >= len(displayItems):
            currentIndex = 0

        hw.update()

        status_log.verbose_print(hw.hostname, hw.ipaddress,
                                 hw.ip_eth0, hw.ip_wlan0,
                                 hw.cpuTemperature,
                                 hw.memTotal, hw.memFree, hw.memUsed, hw.memPercent,
                                 hw.diskTotal, hw.diskUsed, hw.diskFree, hw.diskPercent,
                                 hw.cpuUsagePercent_1, hw.cpuUsagePercent_5, hw.cpuUsagePercent_15)

        ipAddress = "IP: {0}".format(hw.ipaddress)
        valTitle = displayItems[currentIndex]
        valText = ""
        valValue = 0

        if valTitle.upper() == "NAME":
            valText = hw.hostname
            valValue = -1
        elif valTitle.upper() == "RAM":
            valTitle = valTitle + " ({0:.1f} GB)".format(hw.memTotalGB)
            valText = "{0:.2f} %".format(hw.memPercent)
            valValue = round(hw.memPercent / 10)
        elif valTitle.upper() == "TEMP":
            valText = "{0:.2f} C".format(hw.cpuTemperature)
            # Offically works from -40 to 85 C [ 12.5 = (85 + 40)/10 ]
            valValue = round((hw.cpuTemperature + 40) / 12.5)
        elif valTitle.upper() == "DISK":
            valTitle = valTitle + " ({0:.0f} GB)".format(hw.diskTotalGB)
            valText = "{0:.2f} %".format(hw.diskPercent)
            valValue = round(hw.diskPercent / 10)
        elif valTitle.upper() == "CPU":
            valText = "{0:.2f} %".format(hw.cpuUsagePercent_1)
            valValue = round(hw.cpuUsagePercent_1 / 10)
        else:
            valText = ""
            valValue = 0

        disp.updateDisplay(ipAddress, valTitle, valText, valValue)

        currentIndex += 1

        timer = time.time()

disp.clearScreen()
led.value = False
t = disp.getTimeString()
status_log.log_print("Exiting from Pi Status")
status_log.err_print("Exiting from Pi Status")
exit(1)
