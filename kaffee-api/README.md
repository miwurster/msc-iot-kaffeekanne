
# Kaffee API

We used `Node-RED`, a visual tool for wiring the Internet of Things, in order to model and implement the data flow of our Kaffee API.

### Overview

In IBM Bluemix, we created a `Node-RED` Cloud Foundry application.
From here, we could model and implement our data flow in `Node-RED`'s [web interface](https://device-api.eu-gb.mybluemix.net/red).

The overall flow is shown below:

![Node-RED Flow](http://rawgit.com/miwurster/msc-iot-kaffeekanne/master/kaffee-api-flow.png)

We are exposing a simple `GET` HTTP [endpoint](https://kaffee-api.eu-gb.mybluemix.net/state) (`/state`) which returns a `JSON` response representing the last measurement received from the Gram scale.

```json
{
    "timestamp": 1465310789,
    "weight": 1922,
    "capacity": {
        "max": 2000,
        "current": 22
    },
    "level": 1
}
```

The [Web UI](../kaffeekanne) project uses this endpoint to request the current filling level of the coffee can.
