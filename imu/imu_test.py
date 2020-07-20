import ctypes
import pylibi2c
import time
from log_setup import logger
from utils import i2cdev

logger.info('Opening i2c device @/dev/i2c-1, addr 0x68')
i2c = pylibi2c.I2CDevice('/dev/i2c-1', 0x68)

i2c.delay = 10
logger.info('Set delay = 10')

i2c.page_bytes = 8
logger.info('Set page bytes = 8')

i2c.flags = pylibi2c.I2C_M_IGNORE_NAK
logger.info('Set flags to ignore i2c device nak signal')

#i2cdev.setSleepMode(i2c, 0)

time.sleep(3)

pwr_reg = i2cdev.readByte(i2c, 0x6B)
#print(i2c.read(0x0, 256))
print(pwr_reg)

#logger.debug('Reading PWR MGMT register field')
#print(pwr_reg)

while True:
	data = i2c.read(0x43, 6)
	
	# convert byte array to list
	#data_int = int.from_bytes(data, byteorder='little')

	print('Data (byte array):', data)
	#print('Data:', data_int)
	#print('Data:', bin(data_int))
