FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./storage.py" ]

ENV MQTT_BROKER=broker \
    COS_ENDPOINT=https://s3.us.cloud-object-storage.appdomain.cloud \
    COS_AUTH_ENDPOINT=https://iam.cloud.ibm.com/identity/token \
    BUCKET=shane-w251
