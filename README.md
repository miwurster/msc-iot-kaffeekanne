
# IoT Kaffeekanne

The lab exercise in the form of a two-day hackathon, in the course of the lecture Internet of Things, was to use a [scale](http://gram.es/eng/productos012.php?idc=46&idp=217) to measure the current coffee level at our institute's coffee pot.
The challange was, based on this starting position, to build an IoT solution collecting this data from the scale, processing and providing it in an appropriate form to the end users.

### MVP

After a brainstorming, the team agreed to the following requirements in order provide a minimal viable product:

* Implement sensor (`Python`) reading the measurements from the scale
* Sensor script has to publish those measurements (one measurement per second) in bulks to IBM's Watson IoT Platform
* Time-series data of sensor has to be persisted in a NoSQl database
* Backend has to use thresholds to trigger additional actions
* Threshold action: Tweet about the current status of the coffee can
* Optional: Learn thresholds automatically based on historical data
* Implement a RESTful interface to request the current state of the coffee can
* Having a simple web application utilizing the RESTful interface to visualize the state

### Architecture

![Overview](http://rawgit.com/miwurster/msc-iot-kaffeekanne/master/overview.svg)

### Components

* [Sensor](sensor)
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
* Nora Selimi (Documentation, Web Application)
* Emrullah Apaydin (Documentation)
