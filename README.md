# MQTT driver for DHT11 sensor

DHT11 is an inexpensive temperature and humidity sensor. 

This Python script will poll data from a DHT11 attached to a Raspberry Pi using the [dht11km](http://www.tortosaforum.com/raspberrypi/dht11driver.htm) device driver and publish it to an MQTT broker. 

## Installation

[See this post](https://www.endian.se/content/?p=127) for a description how the DHT11 can be attached to the Raspberry Pi and how to build the device driver. 

This script requires the argh and paho-mqtt Python modules which can be installed if you run the following command on your Pi.

    pip install -r requirements.txt

You need to have a running MQTT broker on your Pi (or on another server reachable from your Pi). 
The MQTT broker mosquitto is available for the Raspberry Pi and can be installed with the following command. 

    sudo apt-get install mosquitto

## Run it!

    usage: dht11-mqtt-driver.py [-h] [--host HOST] [-p PORT] [-d DEVICE] topic

    positional arguments:
      topic                 MQTT topic on which to publish the DHT11 result

    optional arguments:
      -h, --help            show this help message and exit
      --host HOST           MQTT host to connect to (default: 127.0.0.1)
      -p PORT, --port PORT  Port to connect to (default: 1883)
      -d DEVICE, --device DEVICE
                            Device node for dht11km driver (default: /dev/dht11)


Example.

    ./dht11-mqtt-driver.py --host 127.0.0.1 --port 1883 --device /dev/dht11 sensor/dht11/data

