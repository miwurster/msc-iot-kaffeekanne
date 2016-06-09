
# IoT Kaffeekanne

The lab exercise in the form of a two-day hackathon, in the course of the lecture Internet of Things, was to use a [scale](http://gram.es/eng/productos012.php?idc=46&idp=217) to measure the current coffee level at our institute's coffee pot.
The challange was, based on this starting position, to build an IoT solution collecting this data from the scale, processing and providing it in an appropriate form to the end users.

### MVP

After a brainstorming, the team agreed to the following requirements in order to provide a minimal viable product:

* Implement a sensor (`Python`) reading the measurements from the scale
* Sensor script has to publish those measurements (one measurement per second) in bulks to IBM's Watson IoT Platform
* The sensor's time-series data has to be persisted in a NoSQL database
* A backend function has to check thresholds to trigger additional actions
    * Must: Tweet about the current status of the coffee can
    * Optional: Learn thresholds automatically based on historical data
* Implement a RESTful interface to request the current state of the coffee can
* Having a simple but mobile friendly web application utilizing the RESTful interface to visualize the state

### Architecture

![Overview](http://rawgit.com/miwurster/msc-iot-kaffeekanne/master/overview.svg)

The [GRAM RZ-30](sensor) scale is connected to a Raspberry Pi. Those two parts build our sensor. On the Raspberry Pi, a Python script receives the measurements from the scale and pushes them to IBM Bluemix.

The [Device API](device-api) is implemented as `Node-RED` Cloud Foundry application and receives the data from our sensor. The data will be persisted into a NoSQL data store. Additionally, the application checks a certain threshold and if this threshold is violated it will tweet in order to inform the end users about its current status.

The [Kaffee API](kaffee-api) is also implemented as `Node-RED` Cloud Foundry application and is responsible to serve the latest state of the coffee can in a RESTful manner.

Using Cloud Foundry's `staticfile` buildpack, we are going to serve the end-user's [web application](kaffeekanne). The end-users will access the application simply thru their web browser (optimized for mobile devices).

### Components

* [Sensor](sensor) (Scale & Raspberry Pi)
* [Device API](device-api)
* [Kaffee API](kaffee-api)
* [Web UI](kaffeekanne)

### Links

* [Current Coffee Level](https://kaffeekanne1.eu-gb.mybluemix.net)
* [IoT Kaffeekanne on Twitter](https://twitter.com/kaffeekanne1)

### Contributors (and Responsibilities)

* Daniel Joos (Python Sensor, Raspberry Pi integration)
* Eduard Yarolyan (Kaffee API, NoSQL Database Layer)
* Manuel Breithaupt (Device API, Twitter Integration)
* Michael Wurster (Raspberry Pi integration, Web Application)
* Arbnora Selimi (Documentation, Web Application)
* Emrullah Apaydin (Documentation, IBM Bluemix Setup, supported other team members)
