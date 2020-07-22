import qwiic_scmd
from log_setup import logger
from traitlets import HasTraits, observe, Int

class Motor(HasTraits):
  #-------------------------------------------
  # Class variables for setting up the motor 
  # driver for all instances of the Motor class
	speed = Int()
	myMotor = qwiic_scmd.QwiicScmd(address=0x58)
	myMotor.begin()
	myMotor.set_drive(1,0,0)
	myMotor.set_drive(0,0,0)
	myMotor.enable()
	FWD = 0
	BWD = 1
	
	def __init__(self, side):
		self.side = side
		
		if self.myMotor.is_connected():
			print('Motor driver connection established')
		else:
			print('Motor driver not connected')
		

	#--------------------------------------------
  # Utilize observer pattern so Motor instance
  # can modulate speed in response to change in 
  # speed-value
	@observe('speed')
	def _observe_speed(self, change):
		self._run(change['new'])



	#--------------------------------------------
	# Speed input will be in range of -255 to 255
  # Values < 0 imply reverse direction
	def _run(self, speed):
		if speed < 0: # backward
			self.myMotor.set_drive(self.side, self.BWD, abs(speed))
		else: # forward
			self.myMotor.set_drive(self.side, self.FWD, speed)
	
	#--------------------------------------------
  # Calling disable from any instance of Motor
  # will disable the motor driver for ALL instances
	def disable(self):
		self.myMotor.set_drive(0,0,0)
		self.myMotor.set_drive(1,0,0)
		self.myMotor.disable()
	
