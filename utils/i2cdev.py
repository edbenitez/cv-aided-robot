import ctypes
import pylibi2c
from log_setup import logger

# Power management register bitfields
# Default power on state for MPU6050 is sleep mode
# Setting the cycle bit and disabling sleep mode, the
# MPU6050 will cycle between sleep and wake to take
# single sample at rate determined by LP_WAKE_CTRL reg
MPU6050_PWR1_DEVICE_RESET_BIT = 7
MPU6050_PWR1_SLEEP_BIT = 6
MPU6050_PWR1_CYCLE_BIT = 5
MPU6050_PWR1_TEMP_DIS_BIT = 3
MPU6050_PWR1_CLK_SEL_BIT = 3

MPU6050_RA_PWR_MGMT_1 = 0x6B

def readByte(i2cdevice, reg_addr):
	# read 1 byte starting from reg_addr
	logger.info('Reading 1 byte starting from %x' % reg_addr)
	return i2cdevice.ioctl_read(reg_addr, 1)

def writeByte(i2cdevice, reg_addr, data):
	pass

def writeBits(i2cdevice, reg_addr, bit_start, length, data):
	pass

def writeBit(i2cdevice, reg_addr, bit_pos, data):
	current_data = readByte(i2cdevice, reg_addr)
	print('Current data: ', current_data)
	
	
	final_data = bytes([ current_data[0] | (1 << 3) ])
	logger.debug('Setting bit')
	
	final_data = bytes([ final_data[0] & ~(1 << bit_pos) ])
	logger.debug('Clearing bit')

	print('Data after preparation: ', final_data)
	logger.debug('Writing bit to reg addr %x at bit pos %d' % (reg_addr, bit_pos))

	#test_buf = b'\x40'
	i2cdevice.write(reg_addr, final_data)

def setSleepMode(i2cdevice, enabled=0):
	writeBit(i2cdevice, reg_addr=MPU6050_RA_PWR_MGMT_1, bit_pos=MPU6050_PWR1_SLEEP_BIT, data=enabled)

