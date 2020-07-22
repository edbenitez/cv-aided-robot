import cv2
import numpy as np
import threading
from log_setup import logger

class Camera():
	def __init__(self, window_name='cvard'):
		self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)
		self.window_name = window_name
		cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
		cv2.resizeWindow(640,480)
		cv2.moveWindow(self.window_name, 0, 0)
		cv2.setWindowTitle(self.window_name, 'Live View')
		font = cv2.FONT_HERSHEY_PLAIN
		

	def _gst_str(self):
		return "nvarguscamerasrc ! video/x    -raw(memory:NVMM), width=(int)640, height=(int)480, for    mat=(string)NV12, framerate=(fraction)30/1 ! nvvidconv     ! video/x-raw, format=(string)BGRx ! videoconvert ! vid    eo/x-raw, format=(string)BGR ! appsink"

	def begin(self):
		logger.info('Start camera. Open Video Capture object')
		if not self.cap.isOpened():
			self.cap.open(self._gst_str(), cv2.CAP_GSTREAMER)
		
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

	def view(self):
		logger.info('Starting live view')
		while cv2.getWindowProperty(self.window_name, 0) >= 0:
			cv2.imshow(self.window_name, self.image)

	def _capture(self):
		while True:
			ret, frame = self.cap.read()
			print(type(frame))
			if ret:
				self.image = frame
			else:
				break
