import os
import json
from dotenv import load_dotenv

import paho.mqtt.client as paho
from paho import mqtt
import time
import random


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    """
        Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param flags: these are response flags sent by the broker
        :param rc: stands for reasonCode, which is a code for the connection result
        :param properties: can be used in MQTTv5, but is optional
    """
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    """
        Prints mid to stdout to reassure a successful publish ( used as callback for publish )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param properties: can be used in MQTTv5, but is optional
    """
    print("PUBLISHED, mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """
        Prints a reassurance for successfully subscribing
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
        :param properties: can be used in MQTTv5, but is optional
    """
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """

    print("MESSAGE RECEIVED, topic: " + msg.topic + " qos:" + str(msg.qos) + " message: " + str(msg.payload) )


if __name__ == '__main__':
    load_dotenv(dotenv_path='./credentials.env')

    broker_address = os.environ.get('BROKER_ADDRESS')
    broker_port = int(os.environ.get('BROKER_PORT'))
    username = os.environ.get('USER_NAME')
    password = os.environ.get('PASSWORD')

    sender1 = paho.Client(paho.CallbackAPIVersion.VERSION1, client_id="sender1", userdata=None, protocol=paho.MQTTv5)
    sender1.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    sender1.username_pw_set(username, password)
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    sender1.on_connect = on_connect
    sender1.connect(broker_address, broker_port)
    sender1.loop_start()
    sender1.on_publish = on_publish 

    sender2 = paho.Client(paho.CallbackAPIVersion.VERSION1, client_id="sender2", userdata=None, protocol=paho.MQTTv5)
    sender2.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    sender2.username_pw_set(username, password)
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    sender2.on_connect = on_connect
    sender2.connect(broker_address, broker_port)
    sender2.loop_start()
    sender2.on_publish = on_publish

    receiver = paho.Client(paho.CallbackAPIVersion.VERSION1, client_id="receiver", userdata=None, protocol=paho.MQTTv5)
    receiver.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    receiver.username_pw_set(username, password)
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    receiver.on_connect = on_connect
    receiver.connect(broker_address, broker_port)
    receiver.loop_start()
    receiver.on_subscribe = on_subscribe 
    receiver.on_message = on_message
    receiver.subscribe("ece140b/ch1", qos=1)


    i = 0
    while i < 10:
        r1 = random.randint(0, 10)
        r2 = random.randint(20, 30)
        sender1.publish("ece140b/ch1", payload=str(r1), qos=1)
        sender2.publish("ece140b/ch1", payload=str(r2), qos=1)
        i=i+1
        time.sleep(3)

    sender1.loop_stop()
    sender2.loop_stop()
    receiver.loop_stop()
