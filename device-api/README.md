
# Device API

We used `Node-RED`, a visual tool for wiring the Internet of Things, in order to model the data flow of our Device API.

### Overview

In IBM Bluemix, we created a `Node-RED` Cloud Foundry application.
From here, we could model and implement our data flow in `Node-RED`'s [web interface](https://device-api.eu-gb.mybluemix.net/red).

The overall flow is shown below:

![Node-RED Flow](http://rawgit.com/miwurster/msc-iot-kaffeekanne/master/device-api-flow.png)

First of all, we created a _device_ in IBM's Watson IoT Platform. This _device_ represents our [Gram scale](https://github.com/miwurster/msc-iot-kaffeekanne/wiki/GRAM-RZ30K-Device).

We were then able to create an `input` node for this device in order to process the data received by the Gram scale.
On the one hand, we simply store the sensor data in a NoSQL database (utilizing IBM's Cloudant data storage service).
On the other hand, we are checking the current weight of the coffee can in order to decide if we have to trigger additional actions.
In our case, the action is to tweet about the current coffee level.
If the filling of the coffee can reaches a certain level, we will tweet that someone should make new coffee.
If the state changes back, then we will tweet that there is now new coffee available.

### Data Storage Layer

From the Gram scale, we receive bulked sensor data every 30 seconds. This bulk contains the measurements of the last 30 seconds (one measurement per second). For each measurement we are going to create an entry in our NoSQL data store.

Due to the fact that a single measurement consists of six values ([details](https://github.com/miwurster/msc-iot-kaffeekanne/tree/master/sensor#python-sensor)) we are using the median of those values to persist.

The following shows a single measurement we get from the Gram scale:

```json
{
    "timestamp": 1465143375,
    "measurements": [
        "136",
        "136",
        "136",
        "136",
        "136",
        "136",
        "136"
    ]
}
```

The `ParseMessage` node in our `Node-RED` flow parses this payload and transforms it into the following payload:

```json
{
    "timestamp": 1465143375,
    "weight": 136
}
```

This payload ends up in IBM's Cloudant document store.
