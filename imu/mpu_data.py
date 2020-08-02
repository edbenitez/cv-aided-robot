import time
import board
import busio
import adafruit_mpu6050
from math import sin,asin,sqrt


class MPU():
	def __init__(self):
		i2c = busio.I2C(board.SCL, board.SDA)
		self.mpu = adafruit_mpu6050.MPU6050(i2c)
		self.angle_init = False
		self.pitch = 0
		self.roll = 0
		self.pitch_out = 0
		self.roll_out = 0

	def get_gyro(self):
		# returns (x,y,z) tuple with corresponding gyro data in deg/s
		return (self.mpu.gyro)

	def get_accel(self):
		# returns (x,y,z) type with corresponding accel data in m/s^2
		return (self.mpu.acceleration)

	def get_temp(self):
		# returns temp in degrees celsius
		return (self.mpu.temperature)

	def get_gyro_angles(self):
		gyro = self.mpu.gyro
		accel = self.mpu.acceleration

		self.pitch += (gyro[0] * 0.0000611)
		self.roll += (gyro[1] * 0.0000611)
		
		self.pitch += self.roll * sin(gyro[2] * 0.000001066)
		self.roll -= self.pitch * sin(gyro[2] * 0.000001066)
		
		accel_mag = sqrt( (accel[0]**2) + (accel[1]**2) + (accel[2]**2))
		pitch_acc = asin(accel[1]/accel_mag) * 57.296
		roll_acc = asin(accel[0]/accel_mag) * -57.296
		
		if self.angle_init:
			self.pitch = (self.pitch * 0.9996) + (pitch_acc * 0.0004)
			self.roll = (self.roll * 0.9996) + (roll_acc * 0.0004)
		else:
			self.pitch = pitch_acc
			self.roll = roll_acc
			self.angle_init = True


if __name__ == "__main__":

	mpu = MPU()

	timestamp = time.monotonic()

	while True:
		mpu.get_gyro_angles()
		print(mpu.pitch)
		print(mpu.roll)
		print('\n\n')

				
	'''
	print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.acceleration))
	print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(mpu.gyro))
	print("Temperature: %.2f C"%mpu.temperature)
	print("")
	'''
