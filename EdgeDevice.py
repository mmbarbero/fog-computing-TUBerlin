
import time
import zmq
from threading import Thread
from paho.mqtt import client as mqtt

ENV_AWS_INSTANCE = "tcp://localhost:5555"


#MQTT Stuff
clientId = "fc-edge"
broker = 'broker.hivemq.com'
topic1 = "/traffic/lane1"
topic2= "/traffic/lane2"
port = 1883

#ZeroMQ Stuff
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(ENV_AWS_INSTANCE)

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

latestSensorData1 = []
latestSensorData2 = []
def calcTrafficIntesity():
    while True:
        time.sleep(10)
        if (len(latestSensorData1) != 0):
            avg1 = sum(latestSensorData1) / len(latestSensorData1)
            print("The list contains " + str(latestSensorData1)[1:-1] +" and the average is "+ str(avg1))
        else:
            avg1 = 0
        if (len(latestSensorData2) != 0):
            avg2 = sum(latestSensorData2) / len(latestSensorData2)
            print("The list contains " + str(latestSensorData2)[1:-1] +" and the average is "+ str(avg2))
        else:
            avg2 = 0
        cloudMsg = str(avg1) + "," + str(avg2)
        socket.send(cloudMsg.encode())
        cloudResponse = socket.recv()
        print(cloudResponse.decode())
        latestSensorData1.clear()
        latestSensorData2.clear()


def subscribe(client: mqtt):
    def onMessage(client, userdata, msg):
        if (topic1 == msg.topic):
            latestSensorData1.append(int(msg.payload.decode()))
        elif (topic2 == msg.topic):
            latestSensorData2.append(int(msg.payload.decode()))
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic1)
    client.subscribe(topic2)
    client.on_message = onMessage


def run():
    thread = Thread(target = calcTrafficIntesity)
    thread.start()
    client = connect()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()