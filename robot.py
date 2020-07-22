from motor import Motor
from traitlets import HasTraits,Instance

class Robot(HasTraits):
	motor_l = Instance(Motor)
	motor_r = Instance(Motor)

	def __init__(self):
		self.motor_l = Motor(side = 0) 
		self.motor_r = Motor(side = 1)
		
	def fwd(self, value=60):
		self.motor_l.speed = value
		self.motor_r.speed = value

	def bwd(self, value=60):
		self.motor_l.speed = value
		self.motor_r.speed = value

	def right(self, value=60):
		self.motor_l.speed = value
		self.motor_r.speed = -value

	def left(self, value=60):
		self.motor_l.speed = -value
		self.motor_r.speed = value

	def stop(self):
		self.motor_l.speed = 0
		self.motor_r.speed = 0
