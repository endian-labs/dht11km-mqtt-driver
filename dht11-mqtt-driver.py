#!/usr/bin/env python3

from collections import deque
import json

import argh
import paho.mqtt.client

class Driver(object):
    '''
    MQTT driver; reads DHT11 temperature and humidity and publish
    result to MQTT broker.
    '''

    def __init__(self, host, port, device, topic):
        self.connected = False

        self.device  = device
        self.topic   = topic

        self.mqtt_client = paho.mqtt.client.Client()

        # Ping MQTT broker every 60 seconds if no data is published
        # from this script.
        self.mqtt_client.connect(host, port, 60)

        self.mqtt_client.on_connect = self.on_connect

    def on_connect(self, client, userdata, rc):
        self.connected = rc == 0

    def run(self):

        self.mqtt_client.loop_start()

        def read_device_node(device):
            '''
            Read device node and parse result. Format from device driver
            is :

              1122334455OK|BAD where

              11 = Humidity - % - integral part
              22 = Humidity - % - decimal part
              33 = Temperature - C - integral part
              44 = Temperature - C - decimal part
              55 = Checksum (sum of other parts)
              OK | BAD = Result of checksum control from driver
            '''
            data = open(self.device, 'r').readline().strip()
            if len(data) == 12 and 'OK' in data:
                return (int(data[4:6], 16), int(data[0:2], 16))
            return (None, None)

        # The device driver sometimes returns incorrect values
        # even if the checksum is ok - we will try to filter out
        # those values. Incorrect values seems to be bit-shifted.
        print('caching data...')
        filter_list = deque()
        while len(filter_list) < 10:
            temperature, humidity = read_device_node(self.device)
            if not temperature is None:
                filter_list.append(temperature)

        print('publishing data...')
        while True:
            temperature, humidity = read_device_node(self.device)
            if not temperature is None and self.connected:

                # If the new temperature is > 5 C off the current
                # mean value this is probably an incorrect reading.
                mean = sum(filter_list) / 10.0
                if abs(temperature - mean) > 5:
                    continue

                result = {
                    'sensor': 'dht11',
                    'temperature': {
                        'value': temperature,
                        'unit': 'celsius',
                        'accuracy': '2'
                    },
                    'humidity': {
                        'value': humidity,
                        'unit': 'percent',
                        'accuracy': '5'
                    }
                }

                self.mqtt_client.publish(self.topic, json.dumps(result))

def run(topic   : 'MQTT topic on which to publish the DHT11 result',
        host    : 'MQTT host to connect to' = '127.0.0.1',
        port    : 'Port to connect to' = 1883,
        device  : 'Device node for dht11km driver' = '/dev/dht11'):

    driver = Driver(host, port, device, topic)
    driver.run()

if __name__ == '__main__':
    argh.dispatch_command(run, completion=False)
