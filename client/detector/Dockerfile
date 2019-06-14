FROM w251/cuda:dev-tx2-4.2_b158
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get -y install python-pip
RUN apt-get -y install python-opencv

WORKDIR /usr/src/app

RUN curl -o haarcascade_frontalface_default.xml https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./detector.py" ]

ENV MQTT_BROKER=broker \
    MQTT_QOS=0
