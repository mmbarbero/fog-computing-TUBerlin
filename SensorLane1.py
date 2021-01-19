import random
import time
import sys
from paho.mqtt import client as mqtt


clientId = 'fc-traffic1'
broker = 'broker.hivemq.com'
topic = "/traffic/lane1"
port = 1883

def generateData(args):
    args = args.upper()
    if (args == "HIGH"):
       return random.randint(15,20)
    elif (args == "MED"):
       return random.randint(10,15)
    elif(args == "LOW"):
       return random.randint(0,10)

def connect():
    def onConnect(client,userdata, flags, rc):
        if rc == 0:
            print("Success")
        else:
            print("Fail ", rc)

    client = mqtt.Client(clientId)
    client.on_connect = onConnect
    client.connect(broker, port)
    return client

def publish(client):
    if (len(sys.argv) > 1):
        while True:
            time.sleep(2)
            data = generateData(sys.argv[1])
            response = client.publish(topic, data)
            status = response[0]
            if status == 0:
                print(f"Send {data} to topic {topic}")
            else:
                print("Fail")
    else:
        print("Please insert intensity")

def run():
    client = connect()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()