import os
import cv2 as cv
import tensorflow as tf
import paho.mqtt.client as mqtt
import numpy as np
from PIL import Image
from io import BytesIO

model_file = os.environ['MODEL']

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
cap = cv.VideoCapture(0)

qos = int(os.environ['MQTT_QOS'])

client = mqtt.Client('detector')
client.connect(os.environ['MQTT_BROKER'])

graph = tf.Graph()
with graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(model_file, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

with graph.as_default():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(graph=graph, config=config)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == 0:
        break

    frame = cv.flip(frame, 1)

    # borrowed from: https://github.com/yeephycho/tensorflow-face-detection/blob/master/inference_usbCam_face.py#L53-L75
    image_np = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    boxes = graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = graph.get_tensor_by_name('detection_scores:0')
    classes = graph.get_tensor_by_name('detection_classes:0')
    num_detections = graph.get_tensor_by_name(
        'num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    if num_detections > 0:
        print('found %d faces' % num_detections)

    img = Image.fromarray(np.uint8(image_np)).convert('RGB')

    for face in boxes[0]:
        print(face)
        (ymin, xmin, ymax, xmax) = face
        im_width, im_height = img.size
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                      ymin * im_height, ymax * im_height)
        cropped = img.crop((left, top, right, bottom))
        data = BytesIO()
        cropped.save(data, format="jpeg")
        client.publish('jetson/webcam/faces', data.getvalue(), qos)
