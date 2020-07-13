from __future__ import print_function
import time
import busio
import adafruit_gps
import serial

# create serial connection
uart = serial.Serial("/dev/ttyTHS1", baudrate=9600, timeout=3000)

# create gps module instance
gps = adafruit_gps.GPS(uart)

# packet type: 314 PMTK314_API_SET_NMEA_OUTPUT
# turn on Recommended Minimum (RMC) info
# https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf
gps.send_command(b"PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")


# packet type: 220 PMTK_SET_NMEA_UPDATERATE
# Set interval values from range 100 to 10000 millisec
gps.send_command(b"PMTK220, 1000")

timestamp = time.monotonic()
if gps.has_fix:
    print('Current fix for location info available')

while True:
    # read up to 32 bytes
    data = gps.readline() 

    if data:
        # convert to string
        data_string = "".join([chr(b) for b in data])
        print(data_string, end='')

        if time.monotonic() - timestamp > 5:
            gps.send_command(b"PMTK605") 
            timestamp = time.monotonic()



