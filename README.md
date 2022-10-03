# pi_status #
Add I2C SD1306 Display and Lighted Momentary Pushbutton to Raspberry Pi

The inspiration for this project is from a UCTRONICS Pi Rack that [Jeff Geerling](https://youtu.be/akJ97oqmQlU "Jeff Geerling") reviewed on his YouTube channel. The UTRONICS product may be seen at [https://www.uctronics.com/cluster-and-rack-mount/for-raspberry-pi/1u-rack-mount/uctronics-pi-rack-pro-for-raspberry-pi-4b-19-1u-rack-mount-support-for-4-2-5-ssds.html](https://www.uctronics.com/cluster-and-rack-mount/for-raspberry-pi/1u-rack-mount/uctronics-pi-rack-pro-for-raspberry-pi-4b-19-1u-rack-mount-support-for-4-2-5-ssds.html).

## Materials ##

- SD1306 128x64 pixel display
- Lighted momentary switch (Normally Open (NO))
- 150 or 220 Ohm Resistor
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
		<td>150 or 220 Ohm Resistor in Series</td>
	</tr>
	<tr>
		<td>LED-</td>
		<td>14</td>
		<td>GND</td>
		<td></td>
	</tr>
</table>

## Installation ##
1. Install Required Libraries (See [https://learn.adafruit.com/monochrome-oled-breakouts/python-setup](https://learn.adafruit.com/monochrome-oled-breakouts/python-setup))
	- sudo pip3 install adafruit-blinka
	- sudo pip3 install adafruit-circuitpython-ssd1306
2. Copy files to /home/pi/display
	- git clone https://github.com/richteel/pi_status.git
3. Run the script on reboot
	- sudo crontab -e
	- Add the following line to the end of the file<br />@reboot sh /home/pi/display/launcher.sh 2>>/home/pi/display/logs/cron_err.txt 1>/home/pi/display/logs/cron_log.txt
4. Make the logs directory
	- mkdir /home/pi/display/logs
5. Run the statement in the crontab to make certain that all is fine
	- sh /home/pi/display/launcher.sh 2>>/home/pi/display/logs/cron_err.txt 1>/home/pi/display/logs/cron_log.txt &
6. Reboot to see if all is working as expected
	- sudo reboot now

## Notes on the Running Script ##
You may want to stop the script or view the output of the script. First you will need to know the PID of the running script. Run the following to find the PID

- ps ax | grep 'code.py' | grep -v grep

You will see output similar to the following

<pre>pi@pi-one:~ $ ps ax | grep 'code.py' | grep -v grep
 403 ?        R     17:35 python3 /home/pi/display/code.py</pre>

From the output, we see that the PID is 403. We may now stop the script using the following command.

- sudo kill 403

We can view the error output by using the tail command.

- sudo tail -f /proc/403/fd/2

	or

- sudo tail -f /home/pi/display/logs/cron_err.txt

We can view the standard output by using the tail command.

- sudo tail -f /proc/403/fd/1

	or

- sudo tail -f /home/pi/display/logs/cron_log.txt

**NOTE**: Use CTRL + C to exit from the tail command.

# Operation #
The script addresses a few requirements for providing system status, script status, and shutting down of the Raspberry Pi.

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
  