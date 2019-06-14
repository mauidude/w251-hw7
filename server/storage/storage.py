import os
import paho.mqtt.client as mqtt
from uuid import uuid4
from datetime import datetime
# import ibm_boto3
# from ibm_botocore.client import Config, ClientError
import boto3


endpoint = os.environ['COS_ENDPOINT']
bucket = os.environ['BUCKET']

cos = boto3.client('s3', endpoint_url=endpoint)

client = mqtt.Client('storage')
client.connect(os.environ['MQTT_BROKER'])


def on_message(client, userdata, message):
    # segment images by current minute to make them easier to find
    now = datetime.now().strftime('%Y-%m-%d-%H-%M')
    key = 'hw3/%s/%s.jpg' % (now, uuid4())
    print('saving face to %s', key)
    cos.put_object(
        Body=message.payload,
        Bucket=bucket,
        Key=key,
        ContentType='image/jpeg',
        ACL='public-read'
    )


client.on_message = on_message

client.subscribe('jetson/webcam/faces')
client.loop_forever()
