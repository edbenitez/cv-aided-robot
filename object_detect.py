import tensorflow as tf
import numpy as np
from log_setup import logger

class ObjectDetector:
	def __init__(self, graph_path=None):
		self.graph_path = graph_path
		self.trt_graph = _get_frozen_graph(self.graph_path)
		self._config()
						
	def _get_frozen_graph(graph_path):
		logger.info('Reading graph file: %s' % self.graph_path)
		with tf.gfile.GFile(pb_file, 'rb') as f:
			graph_def = tf.compat.v1.GraphDef()
			graph_def.ParseFromString(f.read())
		return graph_def
	
	def _config():
		logger.info('Configuring tf session')
		self.tf_config = tf.compat.v1.ConfigProto()
		self.tf_config.gpu_options.allow_growth = True

	def startSession(self):
		#tf.compat.v1.disable_eager_execution()
		
		# Start TensorFlow session
		self.tf_sess = tf.compat.v1.Session(config=self.tf_config)
		# Load graph
		tf.import_graph_def(self.trt_graph, name='')
		
		# Get input/output tensors from graph
		self.image_tensor = self.tf_sess.graph.get_tensor_by_name('image_tensor:0')
		self.num_detections = self.tf_sess.get_tensor_by_name('num_detections:0')
		self.detection_boxes = self.tf_sess.get_tensor_by_name('detection_boxes:0')
		self.detection_scores = self.tf_sess.get_tensor_by_name('detection_scores:0')
		self.detection_classes = self.tf_sess.get_tensor_by_name('detection_classes:0')

			
	# image_tensor expects numpy array of shape [1, None, None, 3]
	def run(self, image):
		#img = jpeg_to_nparray(image)
		#frame = np.expand_dims(img, axis=0)
		
		boxes, scores, classes, num = self.TFSess.run(
		[self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
		feed_dict={self.image_tensor: image})
		return boxes, scores, classes, num


