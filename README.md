# pi_status #
Add I2C SD1306 Display and Lighted Momentary Push-button to Raspberry Pi

More information is available at [https://teelsys.com/2022/10/16/raspberry-pi-4-19-rack-with-four-units/](https://teelsys.com/2022/10/16/raspberry-pi-4-19-rack-with-four-units/)

The inspiration for this project is from a UCTRONICS Pi Rack that [Jeff Geerling](https://youtu.be/akJ97oqmQlU "Jeff Geerling") reviewed on his YouTube channel. The UTRONICS product may be seen at [https://www.uctronics.com/cluster-and-rack-mount/for-raspberry-pi/1u-rack-mount/uctronics-pi-rack-pro-for-raspberry-pi-4b-19-1u-rack-mount-support-for-4-2-5-ssds.html](https://www.uctronics.com/cluster-and-rack-mount/for-raspberry-pi/1u-rack-mount/uctronics-pi-rack-pro-for-raspberry-pi-4b-19-1u-rack-mount-support-for-4-2-5-ssds.html).

## Materials ##

- SD1306 128x64 pixel display
- Lighted momentary switch (Normally Open (NO))
- 220 Ohm Resistor
- Raspberry Pi 4

## Wiring ##
<table>
	<tr>
		<th>Item</th>
		<th>Physical Pin</th>
		<th>GPIO/Function</th>
		<th>Note</th>
	</tr>
	<tr>
		<td>Display VCC</td>
		<td>1</td>
		<td>3v3</td>
		<td></td>
	</tr>
	<tr>
		<td>Display SDA</td>
		<td>3</td>
		<td>2 (SDA)</td>
		<td></td>
	</tr>
	<tr>
		<td>Display SCL</td>
		<td>5</td>
		<td>3 (SCL)</td>
		<td></td>
	</tr>
	<tr>
		<td>Display GND</td>
		<td>6</td>
		<td>GND</td>
		<td></td>
	</tr>
	<tr>
		<td>Switch</td>
		<td>7</td>
		<td>4</td>
		<td>Pulled High</td>
	</tr>
	<tr>
		<td>Switch</td>
		<td>9</td>
		<td>GND</td>
		<td></td>
	</tr>
	<tr>
		<td>LED+</td>
		<td>13</td>
		<td>27</td>
		<td>220 Ohm Resistor in Series</td>
	</tr>
	<tr>
		<td>LED-</td>
		<td>14</td>
		<td>GND</td>
		<td></td>
	</tr>
</table>

## Installation ##
***NOTES:***

- The following steps make are run with the pi user account in the home directory. If running as a different user or location other than /home/pi, you will need to adjust the paths used in this document.
- The instructions below are for verbose logging, which may result in large files that may cause the disk space to fill up and/or cause excessive writes. If this behavior is not desired, remove the "-v" flag from the launcher.sh file.
- To capture all errors and output, with or without logging turned on, you may change the line in crontab to "sh /home/pi/pi_status/display/launcher.sh 2>>/home/pi/pi_status/display/logs/cron_err.txt 1>/home/pi/pi_status/display/logs/cron_log.txt"
- This script was originally written and tested in Raspbian Bullseye. There are significant changes in Raspbian Bookworm for the execution of Python code. The steps reflect the changes to allow it to run in Raspbian Bookworm.

### Prerequisites

- Raspberry Pi device running Raspbian Bullseye or Bookworm (Lite or Full)

- OLED and switch connected to the Raspberry Pi header as indicated in the wiring table above.

- Username and Password for the Raspberry Pi (If the user is not Pi, you will need to edit the scripts and commands!)

- Ensure that the diskspace has been expanded.

  - Run lsblk, if the partitions do not fill the drive, run "sudo raspi-config" to expand the filesystem

    ```shell
    pi@pi-two:~ $ lsblk
    NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
    sda      8:0    0 119.2G  0 disk
    ├─sda1   8:1    0   512M  0 part /boot/firmware
    └─sda2   8:2    0 118.7G  0 part /
    ```

- Get the latest updates by running the following commands

  ```shell
  sudo apt update
  sudo apt full-upgrade
  sudo apt clean
  # sudo rpi-update
  # sudo reboot now
  ```

- Enable I2C interface

  ```shell
  sudo raspi-config
  ```

- Install I2C Tools

  ```shell
  sudo apt install i2c-tools
  ```

- Reboot the Raspberry Pi

  ```shell
  sudo reboot now
  ```

  

### Installation Steps ###

1. Verify that the OLED display is found using i2cdetect. You should see the LCD assigned to address 3C.

  ```shell
  pi@pi-two:~ $ i2cdetect -y 1
  	 0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
  00:                         -- -- -- -- -- -- -- --
  10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
  40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  70: -- -- -- -- -- -- -- --
  ```

2. Verify that Python 3 is installed

  ```shell
  pi@pi-two:~ $ python
  Python 3.11.2 (main, Nov 30 2024, 21:22:50) [GCC 12.2.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> quit()
  pi@pi-two:~ $
  ```

3. Install required libraries (See [https://learn.adafruit.com/monochrome-oled-breakouts/python-setup](https://learn.adafruit.com/monochrome-oled-breakouts/python-setup))
  *Use the commands for your operating system*

  - Raspbian Bullseye

    ```shell
    sudo pip3 install adafruit-blinka
    sudo pip3 install adafruit-circuitpython-ssd1306
    ```

  - Raspbian Bookworm

    ```shell
    sudo apt install python3-pip
    sudo apt install python3-venv
    # sudo apt autoremove
    cd ~
    python3 -m venv env --system-site-packages
    source env/bin/activate
    pip3 install --upgrade adafruit-python-shell
    wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
    sudo -E env PATH=$PATH python3 raspi-blinka.py
    
    # Raspberry Pi Reboots
    
    python3 -m venv env --system-site-packages && source env/bin/activate && pip3 install adafruit-circuitpython-ssd1306
    pip3 install psutil
    sudo apt install python3-pil
    sudo apt install python3-numpy
    ```

4. Install Git

  ```shell
  sudo apt install git
  ```

5. Clone the files from GitHub

  ```shell
  cd ~
  git clone https://github.com/richteel/pi_status.git
  ```

6. Reboot the Raspberry Pi

  ```shell
  sudo reboot now
  ```

7. Make the launcher script executable

  ```shell
  chmod 755 /home/pi/pi_status/display/launcher.sh
  ```

8. If running Raspbian Bullseye, edit launcher.sh by commenting the Bookworm line and uncommenting the Bullseye line.

9. Test the script to make certain it works as expected.

  ```shell
  /home/pi/pi_status/display/launcher.sh
  ```

10. If the code runs properly, you should see the OLED display and switch LED light up. The OLED will cycle information on the display. The terminal window will display information as shown in this sample.

  ```shell
  pi@pi-two:~ $ /home/pi/pi_status/display/launcher.sh
  2025-02-17 17:43:54     Failed to obtain IP Address for wlan0
  2025-02-17 17:43:54     Starting Pi Status
  2025-02-17 17:43:54     Starting Pi Status
  2025-02-17 17:43:54     Logging = True
  2025-02-17 17:43:54     Logging Verbose = True
  2025-02-17 17:43:54     Pi Status       Version 0.2     -1
  2025-02-17 17:44:04     Failed to obtain IP Address for wlan0
  2025-02-17 17:44:04     IP: 192.168.0.228       NAME    pi-two  -1
  ```

11. Press &lt;Ctrl&gt; + c to exit the script.

12. Add a Cron Job to run the script on startup.

   ```shell
   sudo crontab -e
   ```

   If prompted, select your editor of choice. I selected Nano in this example.

   ```shell
   pi@pi-two:~ $ sudo crontab -e
   no crontab for root - using an empty one
   
   Select an editor.  To change later, run 'select-editor'.
     1. /bin/nano        <---- easiest
     2. /usr/bin/vim.tiny
     3. /bin/ed
   
   Choose 1-3 [1]: 1
   ```

   Add the following line to the end of the file.

   ```shell
   @reboot sh /home/pi/pi_status/display/launcher.sh
   ```

13. Reboot to see if all is working as expected

   ```shell
   sudo reboot now
   ```

14. On reboot, make certain that the OLED display is showing information as expected and the power switch LED is lit.

## Notes on the Running Script ##
You may want to stop the script or view the output of the script. First you will need to know the PID of the running script. Run the following to find the PID

- ps ax | grep 'code.py' | grep -v grep

You will see output similar to the following

<pre><span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span> ps ax | grep 'code.py' | grep -v grep
 403 ?        R     17:35 python3 /home/pi/pi_status/display/code.py</pre>

From the output, we see that the PID is 403. We may now stop the script using the following command.

- sudo kill 403

We can view the error output by using the tail command.

- sudo tail -f /proc/403/fd/2

	or

- sudo tail -f /home/pi/pi\_status/display/logs/error.txt

We can view the standard output by using the tail command.

- sudo tail -f /proc/403/fd/1

	or

- sudo tail -f /home/pi/pi\_status/display/logs/detail.txt

We can view the verbose output by using the tail command.

- sudo tail -f /home/pi/pi\_status/display/logs/detail.txt

**NOTE**: Use CTRL + C to exit from the tail command.

You may start the script again by running the following command.

- sh /home/pi/pi\_status/display/launcher.sh -v &

<pre><span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span> sh /home/pi/pi_status/display/launcher.sh -v &
[2] 1974
[1]   Exit 1                  sh /home/pi/pi_status/display/launcher.sh 2>> /home/pi/pi_status/display/logs/cron_err.txt > /home/pi/pi_status/display/logs/cron_log.txt
<span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span> 2022-10-10 18:46:17      Starting Pi Status
2022-10-10 18:46:17     Starting Pi Status
2022-10-10 18:46:17     Logging = True
2022-10-10 18:46:17     Logging Verbose = True
2022-10-10 18:46:17     Pi Status       Version 0.2     -1
</pre>

or 

- sh /home/pi/pi_status/display/launcher.sh 2>>/home/pi/pi_status/display/logs/cron_err.txt 1>/home/pi/pi_status/display/logs/cron_log.txt &

<pre><span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span> sh /home/pi/pi_status/display/launcher.sh 2>>/home/pi/pi_status/display/logs/cron_err.txt 1>/home/pi/pi_status/display/logs/cron_log.txt &
[1] 1931
<span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span>
</pre>

# Operation #
The script addresses a few requirements for providing system status, script status, and shutting down of the Raspberry Pi. There are optional parameters to control logging. Logs are written to the the logs directory within the script folder. Default location if installed in the pi user's home directory is /home/pi/pi\_status/display/logs.

- -h Display help
<pre><span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span> python3 /home/pi/pi_status/display/code.py -h
usage: code.py [-h] [-l] [-v]

Raspberry Pi Status Monitor

optional arguments:
  -h, --help  show this help message and exit
  -l          Turn on basic logging
  -v          Allow verbose logging of status data to a file
<span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span></pre>
- -l Default Logging
	- Writes stdout to /home/pi/pi\_status/display/logs/status.txt
		- Messages such as start, end, startup parameters, and information shown on OLED display 
	- Writes stderr to /home/pi/pi\_status/display/logs/error.txt
		- Start and end messages as well as trapped errors
		- Will not capture error messages resulting in a crash. To capture errors from a crash, it is necessary to redirect stderr to a file by executing the script with a redirection such as code.py 2>errors.log
	- Information from the display is logged as
		- Line 1 (IP Address)
		- Line 2 (Title)
		- Line 3 (Value)
		- Line 4 (Number of blocks to shade from 0 to 10. The value -1 indicates not to show the blocks.)
- -v Verbose Logging (Includes Default Logging plus Details)
	- When using the verbose option, there is no need for the logging option as the verbose option turns on the default logging option
	- Writes to /home/pi/pi\_status/display/logs/detail.txt
	- Produces a tab delimited file that may be imported into a spreadsheet or database
	- Contains all data from each update at a rate of once every 10 seconds.
		- Date and Time (local)
		- Host Name
		- IP Address
		- IP Ethernet
		- IP Wi-Fi
		- CPU Temperature
		- Memory Total
		- Memory Free
		- Memory Used
		- Memory Percent
		- Disk Total
		- Disk Used
		- Disk Free
		- Disk Percent
		- CPU Usage Percent 1 min
		- CPU Usage Percent 5 min
		- CPU Usage Percent 15 min

## Screens ##
There are a few screens to provide system information. The screens are shown for 10 seconds each. Once the last screen is shown, the first screen is shown. The system information is refreshed before each screen is shown but is not updated while being displayed.

- **Splash screen**: Shown once to display software version information
- **NAME**: Displays the hostname of the Raspberry Pi
- **RAM**: Shows the total memory as well as the percentage of memory in use
- **TEMP**: Shows the CPU Temperature in degrees Celsius (NOTE: The scale shows the temperature between the operational limits of the Raspberry Pi, with the low end bring -40 C and the high end being 85 C)
- **DISK**: Shows the total disk space in GB and the percentage of disk space in use
- **CPU**: Shows the average percent load of the CPU over the last minute

## Switch ##
Pressing and holding the switch for 10 seconds will cause the Raspberry Pi to shutdown safely by issuing the shutdown command to the system.

## LED ##
The LED in the lighted switch will be lit when the script is running. If there is a delay from issuing the shutdown command and the script exiting, the LED will flash once every second. It is unlikely that you will see the LED flashing unless the operating system is busy with other tasks before signaling the script to terminate.

**NOTE**: The screen and the switch's LED will turn off when the script ends.


<hr />

# Troubleshooting #
Here are some things to try to determine what may be an issue if the display or script fails.

1. Display not working and "ValueError: No I2C device at address: 0x3c" is shown in the cron_erros.txt log file 
	- Open a terminal and type the following command:<br />
	i2cdetect -y 1<br /><br />
	If you see the following output, check your wiring to the display as the display was not found on the I2C bus.<br />
<pre><span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span> i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
<span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span>
</pre><br />
The expected output is the following showing a device was detected at address 3c,<br/>
<pre><span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span> i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- <span style=background-color:yellow">3c</span> -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
<span style="color: green;">pi@pi-four</span>:<span style="color: blue;">~ $</span>
</pre>

More troubleshooting tips are available at [https://teelsys.com/2022/10/16/raspberry-pi-4-19-rack-with-four-units/](https://teelsys.com/2022/10/16/raspberry-pi-4-19-rack-with-four-units/).