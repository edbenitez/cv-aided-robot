import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from util import vis
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from PIL import ImageFont


FRZ_GRAPH_PATH = './ssdlite_mobilenet_v2_coco_2018_05_09/frozen_inference_graph.pb'
tf.compat.v1.disable_eager_execution()

detection_graph = tf.compat.v1.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(FRZ_GRAPH_PATH, 'rb') as f:
        serialized_graph = f.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

TFSess = tf.compat.v1.Session(graph=detection_graph)

image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

img = jpeg_to_nparray('./cellphone.jpeg')
frame = np.expand_dims(img, axis=0)

print(frame.shape)
print(image_tensor.shape)
print(detection_classes.shape)
print(num_detections.shape)
print(detection_boxes.shape)

boxes, scores, classes, num = TFSess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame})

print(scores)
print(scores.shape)
print(classes)
print(boxes[0][0])

img_pillow = Image.fromarray(img)
draw_bounding_box_on_image(image=img_pillow,
                               ymin=boxes[0][0][0],
                               xmin=boxes[0][0][1],
                               ymax=boxes[0][0][2],
                               xmax=boxes[0][0][3],
                               color='red',
                               thickness=4,
                               display_str_list=['cellphone'],
                               use_normalized_coordinates=True)
