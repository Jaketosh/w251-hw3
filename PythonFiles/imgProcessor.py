import paho.mqtt.client as mqtt
import os
from random import randint

LOCAL_MQTT_HOST="remotebroker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="faces"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client,userdata, msg):
  try:
    print("message received!")

    #Push to s3 bucket***
    img = msg.payload
    print('attempting image write')
    val = randint(0, 1000)
    fileName = '/tmp/images/face' + str(val)
    newFile = open(fileName, "w+b")
    newFile.write(img)
    os.system('s3cmd sync /tmp/images s3://w251jake/hw3/')
    print('finished attempt:')
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message



# go into a loop
local_mqttclient.loop_forever()

