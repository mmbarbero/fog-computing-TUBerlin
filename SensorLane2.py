import random
import time
from paho.mqtt import client as mqtt


clientId = 'fc-traffic2'
broker = 'broker.hivemq.com'
topic = "/traffic/lane2"
port = 1883

def connect():
    def on_connect(client,userdata, flags, rc):
        if rc == 0:
            print("Success")
        else:
            print("Fail ", rc)

    client = mqtt.Client(clientId)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):

    while True:
        time.sleep(10)
        msg = f"{random.randint(0,10)}"
        response = client.publish(topic, msg)
        status = response[0]
        if status == 0:
            print(f"Send {msg} to topic {topic}")
        else:
            print("Fail")

def run():
    client = connect()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()