import tensorflow as tf
import numpy as np

class ObjectDetector:
    def __init__(self, graph_path=None):
        self.graph_path = graph_path
    
    def startSession(self):
        
        #FRZ_GRAPH_PATH = './ssdlite_mobilenet_v2_coco_2018_05_09/frozen_inference_graph.pb'
        tf.compat.v1.disable_eager_execution()

        detection_graph = tf.compat.v1.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(self.graph_path, 'rb') as f:
                serialized_graph = f.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.TFSess = tf.compat.v1.Session(graph=detection_graph)

        self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # image_tensor expects numpy array of shape [1, None, None, 3]
    def run(self, image):
        #img = jpeg_to_nparray(image)
        #frame = np.expand_dims(img, axis=0)
        boxes, scores, classes, num = self.TFSess.run(
        [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
        feed_dict={self.image_tensor: image})
        return boxes, scores, classes, num


