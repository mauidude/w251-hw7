# W251 Homework 3

## Shane Andrade

### Usage

#### Jetson

On the Jetson run the following:
```bash
cd client
./start.sh $REMOTE_BROKER

# run the following to stop the containers:
./stop.sh
```

Where `$REMOTE_BROKER` is the public ip of the MQTT broker running on Softlayer.

#### Softlayer Instance

On your VM run the following:
```bash
cd server
./start.sh $ACCESS_KEY $SECRET_ACCESS_KEY

# run the following to stop the containers:
./stop.sh
```

### MQTT
 * Topic `jetson/webcam/faces`
 * QoS 0
