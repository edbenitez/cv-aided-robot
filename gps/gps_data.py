from __future__ import print_function
import serial
import adafruit_gps
from log_setup import logger

class GPS:
	def __init__(self, port='/dev/ttyTHS1', baudrate=9600, timeout=3000):
		self.port = port
		self.baudrate = baudrate
		self.timeout = timeout
		self.uart = serial.Serial(port, baudrate=self.baudrate, timeout=self.timeout)
		self.gps = adafruit_gps.GPS(self.uart) 
		self.gps.send_command(b"PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0") # RMC data
		self.gps.send_command(b"PMTK220, 1000") # 1000 ms interval

	def parse_data(self):
		data = self.gps.readline()
		# convert data to string
		data_string = "".join([chr(b) for b in data])
		data_list = data_string.split(',')
		

		# parse NMEA sentence
		parsed_data = []

		
		if data_list[0] == '$GPRMC':
			# get data type
			parsed_data.append(data_list[0])
			
			# get longitude
			parsed_data.append(data_list[3] + data_list[4])

			# get latitude
			parsed_data.append(data_list[5] + data_list[6])
	
		logger.info(parsed_data)
	
		return parsed_data
		
			

