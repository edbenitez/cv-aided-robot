from motor import Motor
from traitlets import HasTraits,Instance
from gps import gps_data
from time import sleep
from log_setup import logger
from mag import Mag

class Robot(HasTraits):
	motor_l = Instance(Motor)
	motor_r = Instance(Motor)

	def __init__(self):
		self.motor_l = Motor(side = 0) 
		self.motor_r = Motor(side = 1)
		self.gps = gps_data.GPS()
		self.mag = Mag()		

	def fwd(self, value=60):
		self.motor_l.speed = value
		self.motor_r.speed = value

	def bwd(self, value=60):
		self.motor_l.speed = -value
		self.motor_r.speed = -value

	def right(self, value=60):
		self.motor_l.speed = value
		self.motor_r.speed = -value

	def left(self, value=60):
		self.motor_l.speed = -value
		self.motor_r.speed = value

	def left_turn(self, value=120):
		self.left(value)
		sleep(0.1)
		self.stop()
		
	def right_turn(self, value=120):
		self.right(value)
		sleep(0.1)
		self.stop()
		
	def stop(self):
		self.motor_l.speed = 0
		self.motor_r.speed = 0

	
	def go_to_chkpt(self, chkpt):
		while True:
			current_loc = self.gps.parse_data()
			if current_loc == (None,None):
				logger.info('GPS: waiting to establish current location fix')
				continue			
			else:
				logger.info('Current coordinates (%f, %f)' % current_loc)
				distance_to_chkpt = self.gps.distance(current_loc, chkpt).km
				direction_to_chkpt = self.gps.direction(current_loc, chkpt)
				heading = self.mag.heading()
				
				logger.info('Distance to checkpoint: %f' % distance_to_chkpt)
				logger.info('Desired heading: %f' % direction_to_chkpt)
				logger.info('Actual heading: %f' % heading)
	
				if distance_to_chkpt <= 0.01:
					self.stop()
					logger.info('ROBOT: arrived at checkpoint')
					break
				else:
					if abs(direction_to_chkpt - heading) <= 10:
						self.fwd()
					else:
						a = direction_to_chkpt - 360
						b = heading - a
						c = b - 360
						if c <= 180 and c >= 0:
							self.left_turn()
						else:
							self.right_turn()


if __name__ == "__main__":
	robo = Robot()
	try:
		test_coord = (41.47713, -87.48371399999999)
		robo.stop()
		robo.go_to_chkpt(test_coord)
	except(KeyboardInterrupt, SystemExit, AttributeError) as exErr:
		print("Ending test.")
		print(exErr)
		robo.stop()


		
