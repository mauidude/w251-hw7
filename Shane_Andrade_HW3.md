# HW 3 Submission
## Shane Andrade

### Links

* Github Repo: [github.com/mauidude/w251-hw3](https://github.com/mauidude/w251-hw3)

Some sample images:
* [image 1](http://s3.us.cloud-object-storage.appdomain.cloud/shane-w251/hw3/2019-05-18-21-52/5070b1ff-6610-4a7f-86ab-d038e37c6081.jpg)
* [image 2](http://s3.us.cloud-object-storage.appdomain.cloud/shane-w251/hw3/2019-05-18-21-52/a2ae21c9-0ee3-4309-94d0-a09041868a81.jpg)
* [image 3](http://s3.us.cloud-object-storage.appdomain.cloud/shane-w251/hw3/2019-05-18-21-52/75544139-69ac-4afa-abbd-1955623b0b85.jpg)

List of all images can be found here: [http://s3.us.cloud-object-storage.appdomain.cloud/shane-w251](http://s3.us.cloud-object-storage.appdomain.cloud/shane-w251)

### MQTT

The topic used for MQTT on both brokers is `jetson/webcam/faces`. This path was chosen as it describes in a hierarchical fashion the following: 1. which device type the data came from (`jetson`), 2. the sensor type of that device (`webcam`), and 3. the type of data coming in (`faces`).

The QoS chosen was `0` which refers to at most once delivery. This QoS was chosen due to the streaming nature of the data. Since we are dealing with a video stream, if we drop a frame, the subsequent frames will have similar data assuming we are capturing at a reasonable FPS. At least once and exactly once will cause too much backpressure when there is an issue with delivery and since the data is streaming in nature, we can just continue with the next frame when connectivity is regained.
