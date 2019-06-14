import os
import paho.mqtt.client as mqtt

qos = int(os.environ['MQTT_QOS'])

incoming = mqtt.Client('forwarder')
incoming.connect(os.environ['MQTT_INCOMING_BROKER'])

outgoing = mqtt.Client('forwarder')
outgoing.connect(os.environ['MQTT_OUTGOING_BROKER'])


def on_message(client, userdata, message):
    print('publishing message')
    outgoing.publish('jetson/webcam/faces', message.payload, qos)


incoming.on_message = on_message

incoming.subscribe('jetson/webcam/faces')
incoming.loop_forever()
