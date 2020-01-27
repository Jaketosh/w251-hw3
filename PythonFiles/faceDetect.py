import numpy as np
import cv2 as cv
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="faces"

def on_publish(client,userdata,result):
    print("Face Detected, published.")
    pass

local_mqttclient = mqtt.Client()
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_publish = on_publish

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
cap = cv.VideoCapture(1)
face_cascade = cv.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # We don't use the color information, so might as well save space
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # face detection and other logic goes here
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # your logic goes here; for instance
        # cut out face from the frame.. 
        # rc,png = cv2.imencode('.png', face)
        # msg = png.tobytes()
        # ...
        face = (x,y,w,h)
        print(face)

        face = gray[y:y+h, x:x+w]
        rc,png = cv.imencode('.png', face)
        msg = bytearray(png)
        #cv.imshow('face', png)

        ret = local_mqttclient.publish(LOCAL_MQTT_TOPIC, msg)

