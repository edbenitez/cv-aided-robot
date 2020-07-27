import cv2
import numpy as np
import threading
from log_setup import logger

class Camera():
	def __init__(self, window_name='test'):
		self.cap = cv2.VideoCapture(self.gstreamer_pipeline())
		#self.cap = cv2.VideoCapture(self._gst_str())
		self.window_name = window_name
		
	def gstreamer_pipeline(self):
		return ("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !  appsink")

	def begin(self):
		logger.info('Start camera. Open Video Capture object')
		if not self.cap.isOpened():
			self.cap.open(self.gstreamer_pipeline(), cv2.CAP_GSTREAMER)
		
		logger.info('Starting thread for video capture')
		if not hasattr(self, 'thread') or not self.thread.isAlive():
			self.thread = threading.Thread(target=self._capture)
			self.thread.start()
		
	def end(self):
		logger.info('Stopping camera. Released Video Capture object')
		if hasattr(self, 'cap'):
			self.cap.release()
		
		logger.info('Joining video capture thread')
		if hasattr(self, 'thread'):
			self.thread.join()
		
		if hasattr(self, 'thread_2'):
			logger.info('Joining live view thread')
			self.thread_2.join()

		logger.info('Closing window(s) and de-alloc any assoc. memory')
		cv2.destroyAllWindows()	

	def view(self):
		if not hasattr(self, 'thread_2') or not self.thread_2.isAlive():
			logger.info('Starting live view')
      # Create window and configure it
			cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
			cv2.resizeWindow(self.window_name, 640, 480)
			cv2.moveWindow(self.window_name, 0, 0)
			cv2.setWindowTitle(self.window_name, 'Live View')
			font = cv2.FONT_HERSHEY_PLAIN
					
			self.thread_2 = threading.Thread(target=self._view)
			self.thread_2.start()

	def _view(self):
		while cv2.getWindowProperty(self.window_name, 0) >= 0:
			cv2.imshow(self.window_name, self.image)
	
			# if user hits 'q' key, close window
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			# if capture is off
			if not self.ret:
				break

	def _capture(self):
		while True:
			# read frame and allow in-place modification
			ret, frame = self.cap.read()
			self.ret = ret
			if ret:
				self.image = frame
				self.image.setflags(write=1) 
			else:
				break

if __name__ == "__main__":
	logger.info('Running quick camera test')
	try:
		cam = Camera()
		cam.begin()
		cam.view()
	except:
		cam.end()


