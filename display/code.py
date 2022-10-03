import signal
import time
import board
import digitalio
import os
import sys

from status import display
from status import system
from status import GracefulKiller

disp = display.display()
hw = system.hw_info()
led = digitalio.DigitalInOut(board.D27)
led.direction = digitalio.Direction.OUTPUT
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led.value = True

updateFreq = 10  # Time in seconds
currentIndex = 99
displayItems = ["NAME", "RAM", "TEMP", "DISK", "CPU"]

t = disp.getTimeString()
print("\r\nPi Status ->\t{0}\t{1}".format(t, "Starting Pi Status"), flush=True)
print("\nPi Status ->\t{0}\t{1}".format(t, "Starting Pi Status"), file=sys.stderr, flush=True)

# Show Splash Screen
disp.updateDisplay("Pi Status", "Version", "0.1", -1, True)

# Allow clean exit when stopping
# REF: https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
killer = GracefulKiller.GracefulKiller()
 
timer = time.time()

shutdownFlag = False
buttonPressedTime = time.time()
blinkTimer = time.time()
lastButtonState = False

while not killer.kill_now:
    if not button.value:
        if not lastButtonState:
            t = disp.getTimeString()
            print("Pi Status Button ->\t{0}\t{1}".format(t, "Button Pressed"), flush=True)
            lastButtonState = True
            buttonPressedTime = time.time()
        elif time.time() > buttonPressedTime + 10:
            if not shutdownFlag:
                shutdownFlag = True
                t = disp.getTimeString()
                print("Pi Status Button ->\t{0}\t{1}".format(t, "Shutting Down"), flush=True)
                os.system("/usr/sbin/shutdown now -h")
    else:
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
            valValue = round((hw.cpuTemperature + 40) / 12.5) # Offically works from -40 to 85 C [ 12.5 = (85 + 40)/10 ]
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
print("\r\nPi Status ->\t{0}\t{1}".format(t, "\nExiting from Pi Status"), flush=True)
print("Pi Status ->\t{0}\t{1}\n".format(t, "Exiting from Pi Status"), file=sys.stderr, flush=True)
exit(1)
