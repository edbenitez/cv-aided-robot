from utils import i2cdev
from log_setup import logger
import pylibi2c
import time




class MPU():
	
	def __init__(self):
		logger.info('MPU: Opening i2c device @/dev/i2c-1, addr 0x68')
		self.device = pylibi2c.I2CDevice('/dev/i2c-1', 0x68)
		self.device.delay = 10
		self.device.page_bytes = 8
		self.device.flags = pylibi2c.I2C_M_IGNORE_NAK
		time.sleep(3)
		logger.info('MPU: disabling sleep mode')
		i2cdev.setSleepMode(self.device, enabled=0)
		self.gyro_cal_x = 0
		self.gyro_cal_y = 0
		self.gyro_cal_z = 0

	def calibrate(self):
		logger.info('MPU: calibrating gyroscope')
		for i in range(500):
			self.gyro_cal_x += self.read_gyro_x()
			self.gyro_cal_y += self.read_gyro_y()
			self.gyro_cal_z += self.read_gyro_z()
			#print(self.gyro_cal_x)
			#print(self.gyro_cal_y)
			#print(self.gyro_cal_z)
		self.gyro_cal_x /= 1000
		self.gyro_cal_y /= 1000
		self.gyro_cal_z /= 1000

		print(self.gyro_cal_x)
		print(self.gyro_cal_y)
		print(self.gyro_cal_z)

	def read_gyro_x(self):
		return int.from_bytes(i2cdev.read_16_bit_register(self.device, 0x43), byteorder='little', signed=True) 

	def read_gyro_y(self):
		return int.from_bytes(i2cdev.read_16_bit_register(self.device, 0x45), byteorder='little', signed=True)
	
	def read_gyro_z(self):
		return int.from_bytes(i2cdev.read_16_bit_register(self.device, 0x47), byteorder='little', signed=True)



	def read_gyro(self):
			
		gyro_x = self.read_gyro_x() - self.gyro_cal_x
		gyro_y = self.read_gyro_y() - self.gyro_cal_y
		gyro_z = self.read_gyro_z() - self.gyro_cal_z

		print(gyro_x)
		print(gyro_y)
		print(gyro_z)


if __name__ == "__main__":
	mpu = MPU()
	mpu.calibrate()
	mpu.read_gyro()	
