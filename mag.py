import time
import board
import busio
import adafruit_lsm303dlh_mag
from math import degrees, atan2

class Mag():
	def __init__(self):
		i2c = busio.I2C(board.SCL, board.SDA)
		self.sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

	def read_compass(self):
		mag_x, mag_y, mag_z = self.sensor.magnetic

	def _vector_to_deg(self, x, y):
		angle = degrees(atan2(y,x))
		if angle < 0:
			angle += 360
		return angle

	def heading(self):
		mag_x, mag_y, _ = self.sensor.magnetic
		return self._vector_to_deg(mag_x, mag_y)


