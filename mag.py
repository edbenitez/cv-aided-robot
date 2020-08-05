import time
import board
import busio
import adafruit_lsm303dlh_mag
from math import degrees, atan2, pi
from log_setup import logger
from numpy import interp

class Mag():
	def __init__(self):
		logger.info('MAG: initializing magnometer')
		i2c = busio.I2C(board.SCL, board.SDA)
		self.sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

	def read_compass(self):
		return self.sensor.magnetic
		
	def heading(self):
		mag_x, mag_y, mag_z = self.sensor.magnetic
		mag_x = interp(mag_x, [35, 80], [-2*pi, 2*pi])
		mag_y = interp(mag_y, [-60, -16], [-2*pi, 2*pi])
		heading = degrees(atan2(mag_y, mag_x))
		
		#Formula: (deg + (min / 60.0)) / (180 / M_PI)
		#declin_angle = (3 + (50.0/60.0)) / (180.0 / pi)
		#heading += declin_angle
		
		if heading < 0:
			heading += 360

		print(heading)	
		return (heading)

	#----------------------------------------------------------
	#	Run calibration to collect raw min and max and their range
	#	for each x and y. Then use 2 point calibration to map the
	# raw values to the expected range. See heading() above.
	def calibrate(self):
		min_x = float("inf")
		min_y = float("inf")
		max_x = float("-inf")
		max_y = float("-inf")
		
		for i in range(1000):
			mag_x, mag_y, _ = self.sensor.magnetic
			min_x = min(min_x, mag_x)
			min_y = min(min_y, mag_y)
			max_x = max(max_x, mag_x)
			max_y = max(max_y, mag_y)
		
			offset_x = (min_x + min_y) / 2.0
			offset_y = (min_y + min_y) / 2.0
			print(offset_x, offset_y)
			time.sleep(0.1)		
		print('Min x: ',min_x)
		print('Min y: ',min_y)
		print('Max x: ',max_x)
		print('Max y: ',max_y)
		return offset_x, offset_y
 
if __name__ == "__main__":
	compass = Mag()
	#compass.calibrate()
	while True:
		compass.heading()
