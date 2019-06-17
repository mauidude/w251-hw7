FROM w251/cuda:dev-tx2-4.2_b158
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y python3.5
RUN apt-get -y install python3-pip python-opencv

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./detector.py" ]

ENV MQTT_BROKER=broker \
    MQTT_QOS=0 \
    MODEL=/usr/src/app/model/frozen_inference_graph_face.pb
