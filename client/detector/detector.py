import os
import cv2 as cv
import paho.mqtt.client as mqtt

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
cap = cv.VideoCapture(0)
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

qos = int(os.environ['MQTT_QOS'])

client = mqtt.Client('detector')
client.connect(os.environ['MQTT_BROKER'])

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # We don't use the color information, so might as well save space
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        print('found %d faces' % len(faces))

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        data = cv.imencode('.jpg', face)[1].tobytes()
        client.publish('jetson/webcam/faces', data, qos)
