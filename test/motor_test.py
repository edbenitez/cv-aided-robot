from __future__ import print_function
import time
import sys
import math
import qwiic_scmd
from log_setup import logger

#------------------------------------------
# Default I2C assigned by qwiic library is bus 1.
# This motor driver will be using bus 0 therefore
# a modification has been made to change the default
# bus to bus 0 in file:
# ~/.local/lib/python3.6/site-packages/qwiic_i2c/linux_i2c.py
# Line number 65

myMotor = qwiic_scmd.QwiicScmd(address=0x58)

def run_motor_test():
	print("Start: ")
	motor_left = 0
	motor_right = 1
	forward = 0
	backward = 1

	if not myMotor.is_connected():
		print("Motor driver not connected!", file=sys.stderr)
	else:
		print("Motor driver connection established.")

	logger.info('Initializing operation of SCMD module')
	myMotor.begin()
	logger.info('Initialization complete')

	myMotor.set_drive(0,0,0)
	myMotor.set_drive(1,0,0)
	logger.info('Motor speeds set to zero')
	#sys.exit(0)
	myMotor.enable()
	logger.info('Enabled motor driver functions')

	time.sleep(1)

	logger.info('Start test')
  #logger.info('Left Motor test, forward direction')
	for speed in range(80,255):
		print(speed)
		myMotor.set_drive(motor_left, forward, speed)
		time.sleep(.05)
	for speed in range(254,20,-1):
		print(speed)
		myMotor.set_drive(motor_left, forward, speed)
		time.sleep(.05)
  
	#logger.info('Left Motor test, backward direction')
	for speed in range(80,255):
		print(speed)
		myMotor.set_drive(motor_left, backward, speed)
		time.sleep(.05)
	for speed in range(254,20,-1):
		print(speed)
		myMotor.set_drive(motor_left, backward, speed)
		time.sleep(.05)


	logger.info('Right Motor test, forward direction')
	for speed in range(80,255):
		print(speed)
		myMotor.set_drive(motor_right, forward, speed)
		time.sleep(.05)
	for speed in range(254,20,-1):
		print(speed)
		myMotor.set_drive(motor_right, forward, speed)
		time.sleep(.05)
	
	#logger.info('Right Motor test, backward direction')
	for speed in range(80,255):
		print(speed)
		myMotor.set_drive(motor_right, backward, speed)
		time.sleep(.05)
	for speed in range(254,20,-1):
		print(speed)
		myMotor.set_drive(motor_right, backward, speed)
		time.sleep(.05)


	myMotor.set_drive(0,0,0)
	myMotor.set_drive(1,0,0)

	logger.info('Test complete')

if __name__ == "__main__":
	try:
		run_motor_test()
	except(KeyboardInterrupt, SystemExit, AttributeError) as exErr:
		print("Ending test.")
		print(exErr)
		myMotor.disable()
		sys.exit(0)


