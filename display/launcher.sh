cd /home/pi/pi_status/display
# Uncomment the following line for Raspbian Bullseye
# PYTHONPATH=/usr/bin python3 /home/pi/pi_status/display/code.py -v
# Uncomment the following line for Raspbian Bookworm
python3 -m venv env --system-site-packages && source env/bin/activate && python /home/pi/pi_status/display/code.py -v
