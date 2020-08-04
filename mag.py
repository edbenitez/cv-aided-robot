import time
import board
import busio
import adafruit_lsm303dlh_mag
from math import degrees, atan2
from log_setup import logger

class Mag():
	def __init__(self):
		logger.info('MAG: initializing magnometer')
		i2c = busio.I2C(board.SCL, board.SDA)
		self.sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

	def read_compass(self):
		return self.sensor.magnetic
		
	def _vector_to_deg(self, x, y):
		angle = degrees(atan2(y,x))
		if angle < 0:
			angle += 360
		return angle

	def heading(self):
		mag_x, mag_y, _ = self.sensor.magnetic
		return self._vector_to_deg(mag_x, mag_y)

if __name__ == "__main__":
	compass = Mag()
	while True:
		print('Reading heading: ',compass.heading())

