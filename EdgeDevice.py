
import time
import zmq
from threading import Thread
from paho.mqtt import client as mqtt

AWS_INSTANCE = "tcp://localhost:5555"


#MQTT Stuff
clientId = "fc-edge"
broker = 'broker.hivemq.com'
topic1 = "/traffic/lane1"
topic2= "/traffic/lane2"
port = 1883

#ZeroMQ Stuff
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(AWS_INSTANCE)

## Connects to MQTT broker
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


## The sensor data is stored temporarily to make the calculations, since we don't need to keep past records of this data in our specific use case.
latestSensorData1 = []
latestSensorData2 = []
def calcTrafficAverage():
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
    latestSensorData1.clear()
    latestSensorData2.clear()

    return cloudMsg  

## The ZeroMQ connection is made to the AWS instance
def sendDataToCloud():
    while True:
        time.sleep(20)
        socket.send(calcTrafficAverage().encode())
        cloudResponse = socket.recv()
        print("Prioritize " + cloudResponse.decode())

## We subscribe to the MQTT topics, and every message we get it gets added to the lists. 
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

## We run the average calculation and ZeroMQ data transfer on a thread in order to keep recienving the sensor data if the connection to cloud is down.
def run():
    thread = Thread(target = sendDataToCloud)
    thread.start()
    client = connect()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()