from __future__ import print_function
import serial
import adafruit_gps
from log_setup import logger
from geopy.distance import geodesic
from math import sin,cos,atan2,pi,radians,degrees

class GPS:
	def __init__(self, port='/dev/ttyTHS1', baudrate=9600, timeout=3000):
		self.port = port
		self.baudrate = baudrate
		self.timeout = timeout
		self.uart = serial.Serial(port, baudrate=self.baudrate, timeout=self.timeout)
		self.gps = adafruit_gps.GPS(self.uart)
		self._set_output()
		self._set_update_rate()
	
	def distance(self, loc_a, loc_b):
		# Calculate distance between points
    # Inputs should be tuples of size 2
		return geodesic(loc_a, loc_b)
	
	def direction(self, loc_a, loc_b):
		diff_lon = radians(loc_b[1] - loc_a[1])
		lat_a = radians(loc_a[0])
		lat_b = radians(loc_b[0])
		n = sin(diff_lon) * cos(lat_b)
		p = sin(lat_a) * cos(lat_b) * cos(diff_lon)
		p = cos(lat_a) * sin(lat_b) - p
		p = atan2(n, p)
		if p < 0.0:
			p += (2 * pi)
		return degrees(p)
 
	def _set_output(self):
		# Packet type 314 PMTK314_API_SET_NMEA_OUTPUT
		# Turn on Recommended Minimum Info (RMC)
		logger.info('GPS: setting RMC as NMEA output format')
		self.gps.send_command(b"PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
	
	def _set_update_rate(self, rate=1000):
		# Packet type 220 PMTK_SET_NMEA_UPDATERATE
		# Unit milliseconds
		logger.info('GPS: setting update rate to 1 Hz')
		self.gps.send_command(b"PMTK220, 1000") # 1 Hz

	def has_fix(self):
		# True if a current fix for location info is available
		logger.info('GPS: checking if current fix for location info is avail')
		return self.gps.has_fix

	def parse_data(self):
		logger.info('GPS: reading and parsing a line of NMEA data')
		
		data = self.gps.readline()

		# convert data to string to parse into list
		data_string = "".join([chr(b) for b in data])
		data_list = data_string.split(',')
		

		# parse NMEA sentence
		parsed_data = []

		
		if data_list[0] == '$GPRMC':	
			# get longitude
			print(type(data_list[4]))
			if data_list[4] == 'S':
				parsed_data.append((float(data_list[3])/10/10) * -1)
			else:
				parsed_data.append((float(data_list[3])/10/10))

			# get latitude
			if data_list[6] == 'W':
				parsed_data.append((float(data_list[5])/10/10) * -1)
			else:
				parsed_data.append((float(data_list[5])/10/10))
	
		
		logger.info(parsed_data)
	
		return parsed_data
			
				
if __name__ == "__main__":
	g = GPS()
	while True:
		g.parse_data()
